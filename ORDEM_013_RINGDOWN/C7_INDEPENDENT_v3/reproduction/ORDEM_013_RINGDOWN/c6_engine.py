"""Registered, non-blind finite-interval GW250114 sensitivity measurement.

No physical exclusion is permitted when the two-family injection gate failed.
Uniform remnant priors and proper amplitude priors are integrated jointly;
published posteriors are not reused as priors on the same strain.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import h5py
from scipy.interpolate import CubicSpline
from scipy.special import logsumexp
from fetch_public import atomic_json,digests
from tgl_ringdown_prediction import prediction,scales
from tgl_ringdown_likelihood import linear_statistics

ROOT=Path(__file__).resolve().parent

def checked_registration():
    path=ROOT/'REGISTRO_C6.json'
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    receipt=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C6a_REGISTRO_TOEPLITZ.md'
    if digest not in receipt.read_text(encoding='utf-8'):raise ValueError('Registration does not match delivered receipt')
    reg=json.loads(path.read_bytes())
    for name,wanted in reg['code_and_input_hashes'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=wanted:
            raise ValueError(f'Registered code/input changed: {name}')
    return reg,digest

def observed_windows(reg,digest):
    receipt=json.loads((ROOT/'C6_DOWNLOADS.json').read_bytes())
    if receipt['registration_sha256']!=digest:raise ValueError('Download predates or differs from registration')
    rows=[]
    for item in receipt['files']:
        detector=item['detector'];p=ROOT/'cache/gwosc/on_source'/Path(item['path']).name
        if digests(p)[1]!=item['sha256']:raise ValueError('Observed file custody mismatch')
        reference=reg['reference_peak_GPS'][detector]
        with h5py.File(p) as handle:
            gps0=float(handle['meta/GPSstart'][()]);raw=handle['strain/Strain']
            fs=1/float(raw.attrs['Xspacing'])
            if fs!=4096:raise ValueError('Unexpected source sample rate')
            q=handle['quality/simple/DQmask'][:];inj=handle['quality/injections/Injmask'][:]
            qnames=[v.decode() for v in handle['quality/simple/DQShortnames'][:]]
            inames=[v.decode() for v in handle['quality/injections/InjShortnames'][:]]
            qm=sum(1<<qnames.index(k) for k in reg['quality_required'])
            im=sum(1<<inames.index(k) for k in reg['injection_flags_required'])
            for start in reg['start_times_tM']:
                requested=reference+start*reg['reference_tM_seconds']
                first=int(np.ceil((requested-gps0)*fs))
                stop=first+reg['interval_samples']*reg['sample_stride']
                seconds=np.arange(first//4096,(stop-1)//4096+1)
                if not np.all((q[seconds]&qm)==qm) or not np.all((inj[seconds]&im)==im):
                    raise ValueError('Registered data-quality gate failed')
                data=np.asarray(raw[first:stop:reg['sample_stride']],dtype=float)*1e21
                if len(data)!=reg['interval_samples'] or not np.all(np.isfinite(data)):
                    raise ValueError('Incomplete/nonfinite observed window')
                rows.append(dict(detector=detector,start_tM=start,requested_GPS=requested,
                    first_sample_GPS=gps0+first/fs,first_index=first,
                    last_sample_GPS=gps0+(stop-reg['sample_stride'])/fs,strain_scaled=data))
    return rows

def integration_grid(reg,level):
    shape=reg['quadrature_grids'][level]
    m=np.linspace(*reg['mass_detector_prior_solar'],shape[0])
    s=np.linspace(*reg['spin_prior'],shape[1])
    masses,spins=np.meshgrid(m,s,indexing='ij')
    weights=np.ones(shape);weights[[0,-1],:]*=.5;weights[:,[0,-1]]*=.5
    weights/=weights.sum()
    return masses.ravel(),spins.ravel(),np.log(weights.ravel()),shape

def evaluate_grid(reg,whitened,whitening,level,readings):
    masses,spins,logweight,shape=integration_grid(reg,level)
    grids=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']
    interpolators={k:CubicSpline(grids[k]['spins'],np.asarray(grids[k]['real'])+1j*np.asarray(grids[k]['imag']),extrapolate=False)
                   for k in ('220','440')}
    time=np.arange(reg['interval_samples'])/reg['analysis_sample_rate_hz']
    results=[]
    for reading in readings:
        by_sd={sd:[] for sd in reg['amplitude_prior_sd_scaled']}
        for offset in range(0,len(masses),512):
            ms=masses[offset:offset+512];ss=spins[offset:offset+512]
            qs={k:interpolators[k](ss) for k in interpolators}
            pred=[[prediction(float(m),float(s),reading,redshift=reg['reference_redshift'],
                       mode=mode,qnm_dimensionless=complex(qs[key][j])) for key,mode in [('220',(2,2,0)),('440',(4,4,0))]]
                  for j,(m,s) in enumerate(zip(ms,ss))]
            omega=np.array([[p['omega_rad_s'] for p in row] for row in pred])
            decay=np.array([[1/p['tau_gr_s']+p['gamma_per_s'] for p in row] for row in pred])
            envelope=np.exp(-decay[:,:,None]*time[None,None,:])
            raw=np.stack([envelope[:,0,:]*np.cos(omega[:,0,None]*time),envelope[:,0,:]*np.sin(omega[:,0,None]*time),
                          envelope[:,1,:]*np.cos(omega[:,1,None]*time),envelope[:,1,:]*np.sin(omega[:,1,None]*time)],axis=-1)
            subtotal={sd:np.zeros(len(ms)) for sd in by_sd}
            for detector in whitened:
                basis=np.einsum('kt,gti->gki',whitening[detector],raw,optimize=True)
                for sd in by_sd:
                    _,marginal=linear_statistics(basis,whitened[detector],sd)
                    subtotal[sd]+=marginal[:,0]
            for sd in by_sd:by_sd[sd].append(subtotal[sd])
        for sd,chunks in by_sd.items():
            loglike=np.concatenate(chunks);logz=float(logsumexp(loglike+logweight))
            posterior=np.exp(loglike+logweight-logz)
            pm=posterior.reshape(shape).sum(axis=1);ps=posterior.reshape(shape).sum(axis=0)
            mgrid=np.unique(masses);sgrid=np.unique(spins)
            row=dict(reading=reading,amplitude_prior_sd_strain=sd*1e-21,grid_shape=shape,
                lnZ_signal_over_noise=logz,
                mass_05_50_95=np.interp([.05,.5,.95],np.cumsum(pm),mgrid).tolist(),
                spin_05_50_95=np.interp([.05,.5,.95],np.cumsum(ps),sgrid).tolist(),
                prior_boundary_probability=float(posterior.reshape(shape)[[0,-1],:].sum()+posterior.reshape(shape)[:,[0,-1]].sum()),
                posterior_effective_grid_points=float(1/np.sum(posterior**2)))
            results.append(row)
    for sd in reg['amplitude_prior_sd_scaled']:
        ref=next(r['lnZ_signal_over_noise'] for r in results if r['reading']=='R-GLOBAL' and abs(r['amplitude_prior_sd_strain']-sd*1e-21)<1e-30)
        for row in results:
            if abs(row['amplitude_prior_sd_strain']-sd*1e-21)<1e-30:row['lnB_vs_GR']=row['lnZ_signal_over_noise']-ref
    return results

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--validate-only',action='store_true')
    parser.add_argument('--start',type=float);parser.add_argument('--level',type=int,default=0)
    args=parser.parse_args()
    reg,digest=checked_registration()
    caches={d:np.load(ROOT/'cache/empirical_noise'/f'{d}_noise.npz') for d in ('H1','L1')}
    whitening={d:caches[d]['whitener_scaled'] for d in caches}
    if args.validate_only:
        # Actual event samples are not read in this independent smoke/control run.
        from scipy.interpolate import CubicSpline
        q=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']['220']
        omega=complex(CubicSpline(q['spins'],np.array(q['real'])+1j*np.array(q['imag']))(.68))
        p=prediction(68.1,.68,'R-GLOBAL',qnm_dimensionless=omega)
        t=np.arange(reg['interval_samples'])/reg['analysis_sample_rate_hz']
        h=np.exp(-t/p['tau_gr_s'])*np.cos(p['omega_rad_s']*t+.3)
        signals={d:whitening[d]@h for d in whitening}
        norm=np.sqrt(sum(np.dot(y,y) for y in signals.values()))
        targets={d:y*40/norm for d,y in signals.items()}
        rows=evaluate_grid(reg,targets,whitening,args.level,['R-GLOBAL','R-B'])
        for row in rows:
            if row['reading']=='R-GLOBAL' and not (row['mass_05_50_95'][0]<=68.1<=row['mass_05_50_95'][-1]):
                raise ValueError('Synthetic remnant not in marginal 90% mass interval')
        out=dict(status='SYNTHETIC_GRID_CONTROL_ONLY',registration_sha256=digest,on_source_strain_read=False,results=rows)
        atomic_json(ROOT/f'C6_SYNTHETIC_GRID_{args.level}.json',out)
    else:
        if args.start not in reg['start_times_tM']:raise ValueError('Unregistered start time')
        windows=[r for r in observed_windows(reg,digest) if r['start_tM']==args.start]
        targets={r['detector']:whitening[r['detector']]@r['strain_scaled'] for r in windows}
        rows=evaluate_grid(reg,targets,whitening,args.level,reg['computed_readings'])
        out=dict(status='INCONCLUSIVE_SYSTEMATICS',reason='Two-IMR-family C5 calibration failed; these Bayes ratios are model-conditioned diagnostics, not exclusions',
            registration_sha256=digest,on_source_strain_read=True,start_tM=args.start,primary_start=args.start==10.,
            results=rows,windows=[{k:v for k,v in r.items() if k!='strain_scaled'} for r in windows],
            noise_metric_norm_squared={d:float(np.dot(y,y)) for d,y in targets.items()},
            numeric_aliases=reg['subresolution_readings'],
            scope=reg['scope'])
        atomic_json(ROOT/f'C6_STRAIN_{args.start:g}M_GRID_{args.level}.json',out)
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
