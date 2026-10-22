"""Focused controls for generation bins, overflow refusal and posterior EDOM veto."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import sys,json,hashlib,copy,multiprocessing,resource,time
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN');D=B/'bis/015/t03/source_tests_001'
sys.path.insert(0,str(B/'bis/e2_code_v1_1'))
import numpy as np
import pseob_source as s, pe_runner as runner
import bilby.gw.source as bg
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    resource.setrlimit(resource.RLIMIT_CPU,(899,900));resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3));D.mkdir(exist_ok=False)
    tests=[];started=time.perf_counter()
    def check(name,fn):
        fn();tests.append(dict(name=name,passed=True))
    def reject(fn):
        try:fn()
        except (ValueError,RuntimeError,KeyError):return
        raise AssertionError('Expected refusal')
    cfg=copy.deepcopy(json.loads((B/'RINGDOWN_5SIGMA_V1.json').read_bytes())['pe_jobs']['GW250114_PILOT'])
    cfg.update(generation_sample_rate_hz=4096,generation_maximum_frequency_hz=2048,variant='registered_fixed_deformation_variant',fixed_deformation_parameters=dict(dtau440=0.,domega440=0.))
    cfg['priors'].update(dtau440=0.,domega440=0.)
    check('valid_fixed_440_generation_config',lambda:runner.validate_config(cfg))
    for key,value in [('generation_sample_rate_hz',2048),('generation_sample_rate_hz',True),('generation_maximum_frequency_hz',float('nan')),('generation_maximum_frequency_hz',1024),('sample_rate_hz',8192)]:
        c=copy.deepcopy(cfg);c[key]=value;check('reject_'+key+'_'+str(value),lambda c=c:reject(lambda:runner.validate_config(c)))
    f=np.fft.rfftfreq(16*4096,1/4096)
    g=s.generation_grid(f,4096,8192,1024)
    assert np.array_equal(g[:len(f)],f) and len(g)==65537
    tests.append(dict(name='common_bins_exact_8192_to_4096',passed=True,generated_bins=len(g)))
    check('reject_nonuniform_grid',lambda:reject(lambda:s.generation_grid(np.array([0.,1.,2.1]),4096,8192,1024)))
    check('reject_shifted_grid',lambda:reject(lambda:s.generation_grid(f+1,4096,8192,1024)))
    counter=multiprocessing.Array('d',[0.,0.,0.],lock=True);s.set_cost_counter(counter);s.set_edom_log(D/'EDOM_LOG.jsonl')
    p=dict(mass_1=65.,mass_2=50.,chi_1=.2,chi_2=-.1,luminosity_distance=500.,theta_jn=1.,phase=.3,dtau220=0.,dtau440=0.,domega220=0.,domega440=0.,geocent_time=1420878141.2)
    kw=dict(minimum_frequency=20.,maximum_frequency=1024.,reference_frequency=20.,catch_waveform_errors=True,generation_maximum_frequency_hz=4096,generation_sample_rate_hz=8192,
      analysis_time_contract=dict(start_GPS=cfg['segment_start_GPS'],duration_s=cfg['duration_s'],roll_off_s=cfg['onsource_roll_off_s']))
    calls=[];original=bg.lal_binary_black_hole
    def fake(freq,*args,**kwargs):
        calls.append(dict(bins=len(freq),maximum=kwargs['maximum_frequency']));return dict(plus=(freq+1j),cross=2*freq+1j)
    try:
        bg.lal_binary_black_hole=fake
        wave=s.pseob_frequency_domain(f,**p,**kw)
        assert np.array_equal(wave['plus'],f+1j) and calls==[dict(bins=65537,maximum=4096)]
        tests.append(dict(name='generation_grid_and_exact_output_restriction',passed=True))
        bad=dict(p,dtau220=-.8,dtau440=2.)
        check('overflow_refused_before_native_call',lambda:reject(lambda:s.pseob_frequency_domain(f,**bad,**kw)))
        assert len(calls)==1
        bg.lal_binary_black_hole=lambda *args,**kwargs:None
        assert s.pseob_frequency_domain(f,**p,**kw) is None
        assert counter[0]==2 and counter[2]==1
        record=json.loads((D/'EDOM_LOG.jsonl').read_text());assert record['parameters']['mass_1']==65
        tests.append(dict(name='domain_return_logged_and_counted',passed=True))
    finally:bg.lal_binary_black_hole=original
    inside={k:np.linspace(p[k]-1,p[k]+1,1001) for k in ('mass_1','mass_2','chi_1','chi_2')}
    status=runner.edom_posterior_status(D/'EDOM_LOG.jsonl',inside,counter)
    assert status['status']=='FAILED_EDOM_INSIDE_POSTERIOR_REGION' and status['fraction']==.5
    tests.append(dict(name='inside_posterior_veto',passed=True))
    outside={k:a+10 for k,a in inside.items()};status2=runner.edom_posterior_status(D/'EDOM_LOG.jsonl',outside,counter)
    assert status2['inside']==0;tests.append(dict(name='outside_posterior_explicit_fraction_retained',passed=True))
    counter[2]=0;check('mismatched_log_counter_refused',lambda:reject(lambda:runner.edom_posterior_status(D/'EDOM_LOG.jsonl',inside,counter)))
    result=dict(status='FOCUSED_CONTROLS_PASSED_NOT_R5',tests=tests,native_waveforms=0,
      source_sha256=sha(B/'bis/e2_code_v1_1/pseob_source.py'),runner_sha256=sha(B/'bis/e2_code_v1_1/pe_runner.py'),wall_seconds=time.perf_counter()-started,
      cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime)
    with (D/'RESULT.json').open('xb') as out:out.write((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(dict(status=result['status'],tests=len(tests),wall_seconds=result['wall_seconds'])))
if __name__=='__main__':main()
