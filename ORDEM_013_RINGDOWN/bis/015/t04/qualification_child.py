"""C04 sequential PRECALL/RETURN child, adapted to amended source and frozen R5 inputs."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[k]='1'
import sys,json,time,resource,multiprocessing
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CORE,(0,0));resource.setrlimit(resource.RLIMIT_CPU,(899,900));resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN');sys.path.insert(0,str(B/'bis/e2_code_v1_1_2'))
import numpy as np
from pseob_source import pseob_frequency_domain,set_cost_counter,set_edom_log
job=json.loads(Path(sys.argv[1]).read_bytes());cfg=job['config'];out=Path(sys.argv[2]);counter=multiprocessing.Array('d',[0.,0.,0.],lock=True)
set_cost_counter(counter);set_edom_log(out.parent/'EDOM_LOG.jsonl')
grid=np.fft.rfftfreq(int(cfg['duration_s']*cfg['sample_rate_hz']),1/cfg['sample_rate_hz'])
kw=dict(minimum_frequency=cfg['minimum_frequency_hz'],maximum_frequency=cfg['maximum_frequency_hz'],reference_frequency=cfg['reference_frequency_hz'],
        generation_maximum_frequency_hz=cfg['generation_maximum_frequency_hz'],generation_sample_rate_hz=cfg['generation_sample_rate_hz'],catch_waveform_errors=True,
        analysis_time_contract=dict(start_GPS=cfg['segment_start_GPS'],duration_s=cfg['duration_s'],roll_off_s=cfg['onsource_roll_off_s']))
with out.open('x',encoding='utf-8') as stream:
    def emit(r):stream.write(json.dumps(r,allow_nan=False)+'\n');stream.flush();os.fsync(stream.fileno())
    for index,item in enumerate(job['items']):
        emit(dict(precall=item['label'],generation_maximum_frequency_hz=cfg['generation_maximum_frequency_hz']))
        start=time.perf_counter();error=None
        try:
            wave=pseob_frequency_domain(grid,**item['parameters'],**kw)
            status='DOMAIN_RETURNED_NONE' if wave is None else 'FINITE_WAVEFORM'
        except Exception as e:status='PYTHON_EXCEPTION';error=dict(type=type(e).__name__,message=str(e))
        emit(dict(return_label=item['label'],status=status,error=error,wall_seconds=time.perf_counter()-start))
        if (index+1)%100==0:print(json.dumps(dict(completed=index+1,total=len(job['items']))),flush=True)
    emit(dict(summary=True,source_calls=int(counter[0]),edom=int(counter[2]),source_wall_seconds=float(counter[1])))
