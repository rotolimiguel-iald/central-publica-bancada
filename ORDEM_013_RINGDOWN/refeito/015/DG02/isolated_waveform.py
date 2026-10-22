from pathlib import Path
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
