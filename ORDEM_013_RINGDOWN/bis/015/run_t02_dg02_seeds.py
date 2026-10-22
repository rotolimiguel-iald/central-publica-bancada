"""Execute the supplied prior-draw loop one original seed per bounded command."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,subprocess,json,hashlib,time,resource,signal
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
D=B/'refeito/015/DG02';LOG=B/'bis/015/t02/dg02_runs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def limits():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_CPU,(899,900))
    resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
def main():
    previous=json.loads((B/'bis/015/t02/dg14_runs/RESULT.json').read_bytes())
    assert previous['status']=='STAGES_COMPLETED','DG14 must finish before next single-worker stage'
    LOG.mkdir(exist_ok=False)
    p=D/'dg02_nyquist.py';source=p.read_text()
    head,tail=source.split('# ---- (a) prior draw, registered box, several seeds ----',1)
    body=tail.split("# ---- (a') cross-check:",1)[0]
    loop='for seed in (20260923, 132203, 7, 99):'
    assert body.count(loop)==1
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    records=[]
    for seed in (20260923,132203,7,99):
        generated=D/f'dg02_seed_{seed}.py'
        output=LOG/f'seed_{seed}.json'
        code=head+body.replace(loop,f'for seed in ({seed},):')+'\njson.dump(res, open(OUT, "x"), indent=2, default=lambda o: o.item() if hasattr(o,"item") else str(o))\n'
        with generated.open('x') as f:f.write(code)
        cmd=[sys.executable,'-B',str(generated),str(output)]
        start=time.perf_counter();before=resource.getrusage(resource.RUSAGE_CHILDREN)
        with (LOG/f'seed_{seed}.stdout').open('xb') as out,(LOG/f'seed_{seed}.stderr').open('xb') as err:
            child=subprocess.Popen(cmd,cwd=D,env=env,stdout=out,stderr=err,start_new_session=True,preexec_fn=limits)
            try:rc=child.wait(timeout=1100)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid,signal.SIGTERM)
                try:child.wait(timeout=5)
                except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
                rc='TIMEOUT_1100S'
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        rec={'at':datetime.now(timezone.utc).isoformat(),'seed':seed,'command':cmd,'rc':rc,
             'wall_seconds':time.perf_counter()-start,'cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
             'source_sha256':sha(p),'generated_sha256':sha(generated),'stdout_sha256':sha(LOG/f'seed_{seed}.stdout'),
             'stderr_sha256':sha(LOG/f'seed_{seed}.stderr'),'output_sha256':sha(output) if output.exists() else None}
        records.append(rec)
        with (LOG/f'seed_{seed}.receipt.json').open('x') as f:json.dump(rec,f,indent=2)
        print(json.dumps(rec),flush=True)
        if rc!=0:break
    with (LOG/'RESULT.json').open('x') as f:json.dump({'status':'COMPLETE' if len(records)==4 and all(r['rc']==0 for r in records) else 'PARTIAL_MEASURED','records':records},f,indent=2)
if __name__=='__main__':main()
