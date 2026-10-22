"""Compare amended generation/cropping to V1 at the same full generation grid."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import sys,json,importlib.util,multiprocessing,time,hashlib,resource
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN');D=B/'bis/015/t03/native_bin_control_001';sys.path.insert(0,str(B/'bis/e2_code_v1_1'))
import numpy as np
import pseob_source as new
spec=importlib.util.spec_from_file_location('original_source_reference',B/'bis/e2_code/pseob_source.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    resource.setrlimit(resource.RLIMIT_CPU,(899,900));resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3));D.mkdir(exist_ok=False)
    c=multiprocessing.Array('d',[0.,0.,0.],lock=True);new.set_cost_counter(c);new.set_edom_log(D/'EDOM_LOG.jsonl')
    cfg=json.loads((B/'bis/015/t03/R5/CONFIG_2048_INPUT.json').read_bytes());rows=[];start=time.perf_counter()
    p=dict(mass_1=65.,mass_2=50.,chi_1=.2,chi_2=-.1,luminosity_distance=500.,theta_jn=1.,phase=.3,dtau220=.1,dtau440=0.,domega220=.2,domega440=0.,geocent_time=1420878141.2)
    kw=dict(minimum_frequency=20.,reference_frequency=20.,catch_waveform_errors=True,
      analysis_time_contract=dict(start_GPS=cfg['segment_start_GPS'],duration_s=cfg['duration_s'],roll_off_s=cfg['onsource_roll_off_s']))
    f=np.fft.rfftfreq(16*4096,1/4096)
    for rate in [4096,8192]:
        g=np.fft.rfftfreq(16*rate,1/rate)
        reference=old.pseob_frequency_domain(g,**p,maximum_frequency=rate/2,**kw)
        actual=new.pseob_frequency_domain(f,**p,maximum_frequency=1024.,generation_maximum_frequency_hz=rate/2,generation_sample_rate_hz=rate,**kw)
        assert reference is not None and actual is not None
        mask=(f>=20)&(f<=1024);errors={};full={}
        for key in ('plus','cross'):
            expected=reference[key][:len(f)];errors[key]=float(np.max(np.abs(actual[key][mask]-expected[mask])));full[key]=float(np.max(np.abs(actual[key]-expected)))
            assert np.array_equal(actual[key],expected)
        rows.append(dict(generation_sample_rate_hz=rate,generation_maximum_frequency_hz=rate/2,data_sample_rate_hz=4096,band=[20,1024],max_error_active_band=errors,max_error_all_returned_bins=full))
    result=dict(status='NATIVE_BIN_RESTRICTION_MATCHES_REFERENCE',native_waveforms=4,rows=rows,source_original_sha256=sha(B/'bis/e2_code/pseob_source.py'),source_amended_sha256=sha(B/'bis/e2_code_v1_1/pseob_source.py'),
      wall_seconds=time.perf_counter()-start,cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,scope='One admissible parameter point, both qualified sampling pairs; comparison within same generation grid, not equality across sampling rates; no physical validation')
    with (D/'RESULT.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result))
if __name__=='__main__':main()
