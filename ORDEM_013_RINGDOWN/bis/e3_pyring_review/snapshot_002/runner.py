"""Future controlled Kerr calibration. Never run during preparation."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import argparse,time,json
from datetime import datetime,timezone
from custody import HERE,ROOT,verify,strict_json,sha,publish_new,utc,contained


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--authorization',required=True)
    parser.add_argument('--context',required=True)
    args=parser.parse_args()
    cfg,manifest,auth,limit=verify(args.authorization)
    ctxpath=contained(ROOT,args.context);ctx=strict_json(ctxpath.read_bytes())
    out=ctxpath.parent
    expected_out=contained(ROOT,cfg['output_relative_to_Chatgpt'])
    if out.parent!=expected_out or out.name not in ('welch','public_psd') or ctxpath.name!='CONTEXT.json':raise ValueError('Unregistered run location')
    if ctx['controller_pid']!=os.getppid() or os.getpgrp()!=os.getpid():raise ValueError('Controlled process group required')
    ticks=Path(f'/proc/{os.getppid()}/stat').read_text().rsplit(')',1)[1].split()[19]
    if ticks!=ctx['controller_start_ticks'] or ctx['manifest_sha256']!=auth['manifest_sha256']:raise ValueError('Controller identity/pin changed')
    logstat=(out/'RUN.log').stat()
    for fd in (1,2):
        st=os.fstat(fd)
        if os.isatty(fd) or (st.st_dev,st.st_ino)!=(logstat.st_dev,logstat.st_ino):raise ValueError('Controller log descriptors required')
    stop=min(utc(ctx['stop_utc']).timestamp(),limit.timestamp())-15
    started=time.perf_counter();cpu=time.process_time();local_end=time.monotonic()+stop-time.time()
    def guard():
        if time.time()>=stop or time.monotonic()>=local_end:raise TimeoutError('Kerr calibration deadline')
    publish_new(out/'CLAIM.json',dict(pid=os.getpid(),context_sha256=sha(ctxpath),manifest_sha256=auth['manifest_sha256']))
    likelihood=None
    try:
        import bilby,numpy as np
        from scipy.stats import ks_2samp
        from strain_io import window,offsource_psd,require_pin
        from pe_runner import sampler_class,convergence
        from conditioning import prepare
        from kerr_model import make_likelihood,PARAMETERS
        blocks,receipts=prepare(cfg,out.name,ROOT,guard,(window,offsource_psd,require_pin))
        publish_new(out/'CONDITIONING.json',dict(receipts=receipts,status='CONTROL_PSD_NOT_IDENTICAL_RELEASE',
          preparation_seconds=time.perf_counter()-started))
        guard();likelihood=make_likelihood(blocks,cfg,guard)
        priors=bilby.core.prior.PriorDict({k:bilby.core.prior.Uniform(v[0],v[1],name=k,
          **({'boundary':'periodic'} if k in ('psi','phi2220_1','phi2220_2') else {})) for k,v in cfg['priors'].items()})
        settings=cfg['sampler'];bilby.core.utils.random.seed(settings['seed']);np.random.seed(settings['seed'])
        cls=sampler_class(settings)
        sampler=cls(likelihood=likelihood,priors=priors,label='Kerr220',outdir=str(out),plot=False,
          npool=1,nlive=settings['nlive'],sample='rwalk',walks=settings['walks'],
          maxcall=settings['maxcall'],dlogz=settings['dlogz'],seed=settings['seed'],
          resume=False,check_point=False,check_point_plot=False,print_progress=False,use_ratio=False)
        setup_calls=likelihood.calls
        result=bilby.run_sampler(likelihood=likelihood,priors=priors,sampler=sampler,
          label='Kerr220',outdir=str(out),save='hdf5',plot=False,
          meta_data=dict(mode='NONBLIND_CALIBRATION',manifest_sha256=auth['manifest_sha256']))
        guard();state=convergence(result,settings)
        cost=dict(wall_seconds=time.perf_counter()-started,parent_cpu_seconds=time.process_time()-cpu,
          likelihood_calls=likelihood.calls,likelihood_calls_after_sampler_constructor=setup_calls,
          sampler_ncall=state['ncall'],maxcall_nominal=settings['maxcall'],
          maxcall_scope='Sampler iteration/batch limit, not exact likelihood ceiling',workers=1,thread_caps_requested=1)
        publish_new(out/'CONVERGENCE.json',dict(**state,cost=cost))
        if not state['accepted_for_analysis']:
            publish_new(out/'STATUS.json',dict(status=state['status'],accepted=False,cost=cost))
            raise SystemExit(3)
        posterior=result.posterior
        if not set(PARAMETERS)<=set(posterior) or len(posterior)<2:raise ValueError('Incomplete Kerr posterior')
        arrays={k:np.asarray(posterior[k],float) for k in PARAMETERS}
        if any(v.shape!=(len(posterior),) or not np.isfinite(v).all() for v in arrays.values()):raise ValueError('Unpaired Kerr columns')
        # Only existing released calibration posterior, pinned before this run.
        target=contained(ROOT,cfg['reference_posterior_path']);require_pin(target,cfg['reference_posterior_sha256'])
        released=np.genfromtxt(target,names=True)
        summaries={}
        for key in ('Mf','af'):
            a=arrays[key];b=np.asarray(released[key],float)
            if not np.isfinite(b).all():raise ValueError('Nonfinite released posterior')
            qa=np.quantile(a,[.05,.5,.95]);qb=np.quantile(b,[.05,.5,.95])
            summaries[key]=dict(own_05_50_95=qa.tolist(),released_05_50_95=qb.tolist(),
              own_std_ddof1=float(np.std(a,ddof=1)),released_std_ddof1=float(np.std(b,ddof=1)),
              median_difference=float(qa[1]-qb[1]),
              difference_over_quadrature_width=float((qa[1]-qb[1])/np.hypot(np.std(a,ddof=1),np.std(b,ddof=1))),
              overlap_90pct=bool(max(qa[0],qb[0])<=min(qa[2],qb[2])),
              marginal_KS_distance=float(ks_2samp(a,b,method='asymp').statistic))
        cost.update(wall_seconds=time.perf_counter()-started,parent_cpu_seconds=time.process_time()-cpu)
        npz=out/'PAIRED_POSTERIOR.npz'
        with npz.open('xb') as f:np.savez_compressed(f,**arrays)
        guard()
        report=dict(status='CALIBRATION_COMPARISON_REQUIRES_REVIEW',equivalent_reproduction_paid=False,
          mass_frame='Mf detector-frame solar masses; af dimensionless; no component masses, redshift or cosmology inferred',
          parameter_order=list(PARAMETERS),posterior_sha256=sha(npz),samples=len(posterior),
          own_Mf_af_covariance_ddof1=np.cov(np.column_stack((arrays['Mf'],arrays['af'])),rowvar=False,ddof=1).tolist(),
          reference_Mf_af_covariance_ddof1=np.cov(np.column_stack((released['Mf'],released['af'])),rowvar=False,ddof=1).tolist(),
          comparison=summaries,comparison_scope='Same event. Descriptive overlap/KS/width ratio, no calibrated z, Bayes factor or independent evidence.',
          z_calibrated=None,reference_weighting='Existing posterior.dat interpreted as equal-weight; merge provenance remains OPEN',
          limitations=cfg['limitations'],cost=cost,convergence=state)
        publish_new(out/'COMPARISON.json',report)
    except Exception as error:
        publish_new(out/'FAILURE.json',dict(status='FAILED_NO_ACCEPTED_COMPARISON',error=repr(error),
          wall_seconds=time.perf_counter()-started,likelihood_calls=getattr(likelihood,'calls',None)))
        raise


if __name__=='__main__':main()
