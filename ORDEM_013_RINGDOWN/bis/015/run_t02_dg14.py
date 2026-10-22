"""Bounded sequential probes in the verified runtime; stdout/stderr retained."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,time,subprocess,resource,hashlib,signal
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
D=B/'refeito/015/dg14';LOG=B/'bis/015/t02/dg14_runs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert json.loads((B/'bis/015/t02/RUNTIME_CHECK.json').read_bytes())['status']=='RUNTIME_PINS_MATCH'
    LOG.mkdir(exist_ok=False)
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    stages=[('replay',['probe.py','replay']),('draws',['probe.py','draws']),('grid',['probe.py','grid','16','1024']),('line',['probe2.py'])]
    records=[]
    for label,args in stages:
        start=time.perf_counter();before=resource.getrusage(resource.RUSAGE_CHILDREN)
        cmd=[sys.executable,'-B',str(D/args[0]),*args[1:]]
        with (LOG/(label+'.stdout')).open('xb') as out,(LOG/(label+'.stderr')).open('xb') as err:
            p=subprocess.Popen(cmd,cwd=D,env=env,stdout=out,stderr=err,start_new_session=True)
            try:rc=p.wait(timeout=600)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid,signal.SIGTERM)
                try:p.wait(timeout=5)
                except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
                rc='TIMEOUT_600S'
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        used=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime
        record={'stage':label,'command':cmd,'rc':rc,'at':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-start,'cpu_seconds_including_children':used,
                'stdout_sha256':sha(LOG/(label+'.stdout')),'stderr_sha256':sha(LOG/(label+'.stderr'))}
        records.append(record)
        with (LOG/(label+'.receipt.json')).open('x') as f:json.dump(record,f,indent=2)
        print(json.dumps(record),flush=True)
        if rc!=0 or used>900:break
    result={'status':'STAGES_COMPLETED' if len(records)==4 and all(r['rc']==0 for r in records) else 'PARTIAL_MEASURED','records':records}
    with (LOG/'RESULT.json').open('x') as f:json.dump(result,f,indent=2)
if __name__=='__main__':main()
