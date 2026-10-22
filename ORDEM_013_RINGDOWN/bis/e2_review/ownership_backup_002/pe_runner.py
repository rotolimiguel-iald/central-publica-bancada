"""Registered Bilby/dynesty runner. No execution until E2 and its witness exist.

The enclosing controller must keep blind-run logs/results private. This runner
only prints a completion status and paths, never posterior summary values.
"""
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name]='1'
import argparse,json,time,sys,logging
from pathlib import Path
import numpy as np
from registration_guard import checked_registration,authorize_event,time_guard,contained,output_path,sha
from pseob_source import pseob_frequency_domain,parameter_conversion
from strain_io import window,offsource_psd
from blinding import shifted_samples

def prior_conversion(params):return parameter_conversion(params)[0]

def build_priors(config):
    import bilby
    primitives={'Uniform':bilby.core.prior.Uniform,'Sine':bilby.core.prior.Sine,
      'Cosine':bilby.core.prior.Cosine,'Constraint':bilby.core.prior.Constraint}
    priors={}
    for name,item in config['priors'].items():
        if isinstance(item,(int,float)):
            if not np.isfinite(item):raise ValueError('Invalid fixed prior')
            priors[name]=float(item)
        else:
            if item['kind'] not in primitives:raise ValueError('Unregistered prior class')
            priors[name]=primitives[item['kind']](minimum=item['minimum'],maximum=item['maximum'],name=name,
              **({'boundary':item['boundary']} if 'boundary' in item else {}))
    required={'mass_1','mass_2','mass_ratio','chi_1','chi_2','luminosity_distance','theta_jn','phase','ra','dec','psi','geocent_time','dtau220','dtau440','domega220','domega440'}
    if set(priors)!=required:raise ValueError('Incomplete or extra pilot prior')
    return bilby.core.prior.PriorDict(dictionary=priors,conversion_function=prior_conversion)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--job',required=True);args=parser.parse_args()
    reg,digest=checked_registration()
    if args.job not in reg['pe_jobs']:raise ValueError('PE job not registered')
    cfg=reg['pe_jobs'][args.job];authorize_event(reg,cfg['event'],cfg['mode'])
    # Creating outputs follows all identity/authorization checks.
    outdir=output_path(cfg['output_directory_name'])
    if outdir.exists():raise FileExistsError('New job destination required; resume needs registered branch')
    outdir.mkdir()
    import bilby
    from gwpy.timeseries import TimeSeries
    bilby.core.utils.setup_logger(outdir=str(outdir),label=cfg['label'],log_level='INFO')
    # Console is redirected by the caller for blind jobs; no plots at any stage.
    ifos=bilby.gw.detector.InterferometerList(cfg['detectors']);psd_receipts=[]
    for ifo in ifos:
        d=cfg['data'][ifo.name]
        f,p,receipt=offsource_psd(contained(d['offsource_path']),d['offsource_sha256'],cfg)
        y,fs,start=window(contained(d['onsource_path']),d['onsource_sha256'],cfg['segment_start_GPS'],cfg['duration_s'],cfg['quality_required'],cfg['injection_flags_required'])
        if fs!=cfg['sample_rate_hz']:raise ValueError('No silent resampling of analysis strain')
        ifo.set_strain_data_from_gwpy_timeseries(TimeSeries(y,sample_rate=fs,t0=start))
        ifo.minimum_frequency=cfg['minimum_frequency_hz'];ifo.maximum_frequency=cfg['maximum_frequency_hz']
        ifo.power_spectral_density=bilby.gw.detector.PowerSpectralDensity(frequency_array=f,psd_array=p)
        psd_receipts.append({'detector':ifo.name,**receipt,'actual_start_GPS':start,'input_onsource_sha256':d['onsource_sha256']})
    generator=bilby.gw.WaveformGenerator(duration=cfg['duration_s'],sampling_frequency=cfg['sample_rate_hz'],
      start_time=cfg['segment_start_GPS'],frequency_domain_source_model=pseob_frequency_domain,
      parameter_conversion=parameter_conversion,waveform_arguments={'waveform_approximant':'pSEOBNRv4HM_PA',
        'minimum_frequency':cfg['minimum_frequency_hz'],'maximum_frequency':cfg['maximum_frequency_hz'],
        'reference_frequency':cfg['reference_frequency_hz'],'catch_waveform_errors':True})
    priors=build_priors(cfg)
    likelihood=bilby.gw.likelihood.GravitationalWaveTransient(interferometers=ifos,waveform_generator=generator,
      priors=priors,time_marginalization=False,distance_marginalization=False,phase_marginalization=False)
    start=time.perf_counter()
    np.random.seed(cfg['sampler']['seed'])
    result=bilby.run_sampler(likelihood=likelihood,priors=priors,sampler='dynesty',label=cfg['label'],
      outdir=str(outdir),save='hdf5',plot=False,npool=cfg['sampler']['workers'],
      nlive=cfg['sampler']['nlive'],dlogz=cfg['sampler']['dlogz'],sample='rwalk',
      walks=cfg['sampler']['walks'],maxcall=cfg['sampler']['maxcall'],resume=False,check_point=True,
      check_point_delta_t=60,print_progress=False,meta_data={'registration_sha256':digest,'job':args.job,
        'model_scope':'Aligned-spin pSEOBNRv4HM_PA, distinct from released precessing pSEOBNRv5PHM',
        'mode':cfg['mode']})
    time_guard(reg)
    post=result.posterior
    if len(post)<cfg['sampler']['minimum_posterior_samples']:raise ValueError('Insufficient posterior samples')
    columns={k:np.asarray(post[k],dtype=float) for k in ['dtau220','dtau440','domega220','domega440'] if k in post}
    if not all(np.isfinite(v).all() for v in columns.values()):raise ValueError('Nonfinite posterior')
    if cfg['mode']=='blind_test':science=shifted_samples(columns,cfg['event'],reg)
    else:science={'status':'NONBLIND_CALIBRATION_POSTERIOR','columns':{k:v.tolist() for k,v in columns.items()},
      'summaries':{k:{'quantiles_05_50_95':np.quantile(v,[.05,.5,.95]).tolist(),'std_ddof1':float(v.std(ddof=1))} for k,v in columns.items()}}
    science.update(registration_sha256=digest,job=args.job,wall_seconds=time.perf_counter()-start,
      posterior_samples=len(post),PSD_receipts=psd_receipts,systematic_gate='UNPAID_UNTIL_TWO_FAMILY_INJECTION_CALIBRATION',
      raw_result_files={p.name:sha(p) for p in outdir.glob('*result*') if p.is_file()},
      warning='Sample count alone does not certify nested-sampling convergence; maxcall/dlogz termination must be audited before using result.')
    with (outdir/'ANALYST_OUTPUT.json').open('x',encoding='utf-8') as f:json.dump(science,f,indent=2,allow_nan=False)
    print(json.dumps({'status':'RUN_FINISHED_REQUIRES_CONVERGENCE_AND_SYSTEMATICS_REVIEW','job':args.job,'analyst_output':str(outdir/'ANALYST_OUTPUT.json'),'registration_sha256':digest}))
if __name__=='__main__':main()
