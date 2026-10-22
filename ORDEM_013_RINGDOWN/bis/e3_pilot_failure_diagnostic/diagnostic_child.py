"""Isolated finite source diagnostic; invoked only by the bounded supervisor."""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[key] = "1"
import argparse
import hashlib
import json
import resource
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]


def publish(path, obj):
    with path.open("xb") as handle:
        handle.write((json.dumps(obj, indent=2, allow_nan=False)+"\n").encode())
        handle.flush(); os.fsync(handle.fileno())


def main():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    parser=argparse.ArgumentParser(); parser.add_argument("--replay",action="store_true"); parser.add_argument("--case");args=parser.parse_args()
    plan=json.loads((HERE/"PLAN_INPUTS.json").read_bytes())
    if datetime.now(timezone.utc)>=datetime.fromisoformat(plan["deadline_utc"]):raise TimeoutError("Diagnostic cap expired")
    for item in plan['source_evidence']:
        if item.get('original_path') and hashlib.sha256(Path(item['original_path']).read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('Source pin changed')
    sys.path.insert(0,str(B/'bis/e2_code'))
    import numpy as np
    import bilby
    import lal
    start=time.perf_counter();cpu=time.process_time()
    cfg=plan['pilot_configuration_INPUT']
    if args.replay:
        from pe_runner import build_priors
        priors=build_priors(cfg)
        bilby.core.utils.random.seed(cfg['sampler']['seed']);np.random.seed(cfg['sampler']['seed'])
        keys=[k for k,p in priors.items() if isinstance(p,bilby.core.prior.Prior) and p.is_fixed is False]
        rows=[]
        for n in range(8):
            theta=priors.sample_subset_constrained_as_array(keys,size=1)[:,0]
            params=dict(zip(keys,map(float,theta)))
            rows.append({'draw_index_starting_1':n+1,'parameters':params,
                         'mass_1_kg_using_Bilby':params['mass_1']*bilby.core.utils.solar_mass,
                         'mass_2_kg_using_Bilby':params['mass_2']*bilby.core.utils.solar_mass})
        publish(HERE/'PRIOR_REPLAY.json',{'status':'FINITE_PRIOR_REPLAY_ONLY_NOT_LIKELIHOOD','draws':rows,
             'calibration_sampler_seed':cfg['sampler']['seed'],'scope':'No sampler instantiated, no likelihood/data; exact crash draw not presumed',
             'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'source_calls':0})
        return
    casepath=HERE/'cases'/(args.case+'.json');case=json.loads(casepath.read_bytes())
    if case['plan_sha256']!=hashlib.sha256((HERE/'PLAN_INPUTS.json').read_bytes()).hexdigest():raise ValueError('Case plan pin differs')
    publish(HERE/'cases'/(args.case+'.ENTERED.json'),{'utc':datetime.now(timezone.utc).isoformat(),'case_sha256':hashlib.sha256(casepath.read_bytes()).hexdigest(),'parameters':case['parameters'],'generation_fmax':case['generation_fmax'],'native_calls_planned':len(case.get('sequence',[])) or 1})
    from pseob_source import pseob_frequency_domain,set_deadline
    set_deadline(datetime.fromisoformat(plan['deadline_utc']).timestamp()-5)
    grid=np.fft.rfftfreq(16*4096,1/4096)
    parameters=case['parameters']
    calls=case.get('sequence',[parameters]);summaries=[]
    for idx,params in enumerate(calls):
        publish(HERE/'cases'/(args.case+f'.CALL_{idx+1}.json'),{'utc':datetime.now(timezone.utc).isoformat(),'parameters':params,'native_call_started':True})
        kwargs=dict(minimum_frequency=20.,maximum_frequency=case['generation_fmax'],reference_frequency=20.,
                    analysis_time_contract={'start_GPS':cfg['segment_start_GPS'],'duration_s':cfg['duration_s'],'roll_off_s':cfg['onsource_roll_off_s']},
                    catch_waveform_errors=True)
        begin=time.perf_counter()
        try:
            waveform=pseob_frequency_domain(grid,**params,**kwargs)
            if waveform is None:
                result={'status':'DOMAIN_RETURNED_NONE','wall_seconds':time.perf_counter()-begin}
            else:
                mask=(grid>=20)&(grid<=1024)
                result={'status':'FINITE_WAVEFORM','wall_seconds':time.perf_counter()-begin,
                        'shape':list(waveform['plus'].shape),
                        'analysis_band_norm2':float(sum(np.vdot(v[mask],v[mask]).real for v in waveform.values())),
                        'frequency_grid_nyquist':float(grid[-1]),'generation_fmax':case['generation_fmax']}
        except Exception as error:
            result={'status':'PYTHON_EXCEPTION','error_type':type(error).__name__,'message':str(error),'wall_seconds':time.perf_counter()-begin}
        summaries.append(result)
        publish(HERE/'cases'/(args.case+f'.RETURN_{idx+1}.json'),result)
    publish(HERE/'cases'/(args.case+'.RESULT.json'),{'calls':summaries,'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu})


if __name__=='__main__':main()
