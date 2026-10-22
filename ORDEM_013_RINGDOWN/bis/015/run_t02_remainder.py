"""Remaining T02 reproductions, sequential and isolated, without remote calls."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,subprocess,json,hashlib,time,resource,signal
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
BASE=B/'refeito/015';LOG=B/'bis/015/t02/remainder_runs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def limits():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_CPU,(899,900))
    resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
def main():
    assert json.loads((B/'bis/015/t02/dg02_runs/RESULT.json').read_bytes())['status']=='COMPLETE'
    LOG.mkdir(exist_ok=False)
    source=BASE/'DG02/dg02_nyquist.py';text=source.read_text()
    head=text.split('# ---- (a) prior draw, registered box, several seeds ----')[0]
    metadata=text[text.index('# ---- (b) GW250114'):]
    metadata=metadata.replace("open(OUT, 'w')","open(OUT, 'x')")
    meta=BASE/'DG02/dg02_metadata.py'
    with meta.open('x') as f:f.write(head+'\nres={}\n'+metadata)
    # Source-only crosscheck is isolated by copying the supplied crosscheck loop,
    # replacing only the waveform call with a one-process-per-waveform adapter.
    cross=text[text.index("# ---- (a') cross-check:"):text.index('# ---- (b) GW250114')]
    cross=cross.replace('from bilby.gw.source import lal_binary_black_hole','from isolated_waveform import lal_binary_black_hole')
    cp=BASE/'DG02/dg02_crosscheck.py'
    with cp.open('x') as f:f.write(head+'\nres={}\n'+cross+'\njson.dump(res, open(OUT,"x"), indent=2)\n')
    adapter=BASE/'DG02/isolated_waveform.py'
    adapter_code='''from pathlib import Path
import os,sys,json,subprocess,time,resource
HERE=Path(__file__).resolve().parent
D=HERE/'isolated_waveform_outputs'
D.mkdir(exist_ok=True)
if __name__=='__main__':
 import numpy as np
 from bilby.gw.source import lal_binary_black_hole as call
 x=json.loads(Path(sys.argv[1]).read_bytes())
 try:
  call(np.arange(0,1024+1/16,1/16),*x['args'],**x['kwargs'])
  print(json.dumps({'status':'FINITE_RETURN'}))
 except Exception as e:print(json.dumps({'status':'EXCEPTION','type':type(e).__name__,'message':str(e)}))
else:
 counter=0
 initial=resource.getrusage(resource.RUSAGE_CHILDREN)
 def lal_binary_black_hole(fa,*args,**kwargs):
  global counter
  counter+=1
  p=D/(str(counter)+'.json')
  raw=json.dumps({'args':args,'kwargs':kwargs},default=lambda v:v.item()).encode()
  with p.open('xb') as f:f.write(raw)
  start=time.perf_counter()
  child=subprocess.run([sys.executable,'-B',__file__,str(p)],capture_output=True,text=True,timeout=120)
  with (D/(str(counter)+'.stdout')).open('x') as f:f.write(child.stdout)
  with (D/(str(counter)+'.stderr')).open('x') as f:f.write(child.stderr)
  with (D/(str(counter)+'.receipt.json')).open('x') as f:json.dump({'rc':child.returncode,'wall_seconds':time.perf_counter()-start},f)
  u=resource.getrusage(resource.RUSAGE_CHILDREN)
  if u.ru_utime+u.ru_stime-initial.ru_utime-initial.ru_stime>880:raise SystemExit('CPU budget exhausted')
  if child.returncode!=0:raise RuntimeError('Native subprocess failed rc='+str(child.returncode))
  result=json.loads(child.stdout.strip().splitlines()[-1])
  if result['status']=='EXCEPTION':raise RuntimeError(result['message'])
  return None
'''
    with adapter.open('x') as f:f.write(adapter_code)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',NSCAN='120',NREPLAY='300')
    front=BASE/'E3_piloto_orcamento_cegos'
    stages=[('dg02_metadata',meta,[str(LOG/'metadata.json')]),('dg02_crosscheck',cp,[str(LOG/'crosscheck.json')]),
        ('front_versions',front/'run_repro.py',['versions']),('front_targeted',front/'run_repro.py',['targeted']),
        ('front_grid',front/'grid_stage.py',[]),('front_fine',front/'fine_stage.py',[]),
        ('front_replay',front/'replay_stage.py',[]),('front_scan_registered',front/'run_repro.py',['scan_registered'])]
    records=[]
    for label,p,args in stages:
        cmd=[sys.executable,'-B',str(p),*args];start=time.perf_counter();before=resource.getrusage(resource.RUSAGE_CHILDREN)
        localenv=dict(env,REPRO_OUT=str(LOG/(label+'.jsonl')))
        with (LOG/(label+'.stdout')).open('xb') as out,(LOG/(label+'.stderr')).open('xb') as err:
            child=subprocess.Popen(cmd,cwd=p.parent,env=localenv,stdout=out,stderr=err,start_new_session=True,preexec_fn=limits)
            try:rc=child.wait(timeout=1100)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid,signal.SIGTERM)
                try:child.wait(timeout=5)
                except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
                rc='TIMEOUT_1100S'
        after=resource.getrusage(resource.RUSAGE_CHILDREN)
        rec={'at':datetime.now(timezone.utc).isoformat(),'stage':label,'command':cmd,'rc':rc,
          'wall_seconds':time.perf_counter()-start,'cpu_seconds_including_children':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
          'script_sha256':sha(p),'stdout_sha256':sha(LOG/(label+'.stdout')),'stderr_sha256':sha(LOG/(label+'.stderr'))}
        records.append(rec)
        with (LOG/(label+'.receipt.json')).open('x') as f:json.dump(rec,f,indent=2)
        print(json.dumps(rec),flush=True)
        if rc!=0 or rec['cpu_seconds_including_children']>900:break
    with (LOG/'RESULT.json').open('x') as f:json.dump({'status':'COMPLETE' if len(records)==len(stages) and all(r['rc']==0 for r in records) else 'PARTIAL_MEASURED','records':records},f,indent=2)
if __name__=='__main__':main()
