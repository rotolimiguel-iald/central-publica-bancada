"""Continue exclusive coefficient consumers only after real successful prerequisites.
No existing attempt is repeated, no source is modified, and failure stops scheduling.
"""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
BASE=Path(__file__).resolve().parent
STAMP=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
OUT=BASE/'consumer_chains'/STAMP
OUT.mkdir(parents=True,exist_ok=False)
NODES={
 'CanonicalFockGNSCovarianceR10':['GenericStarConjugationR1'],
 'CanonicalFockCoefficientFlowR13':['CanonicalFockGNSCovarianceR10'],
 'CanonicalFockCoefficientGraphEqualityR9':['CanonicalFockCoefficientFlowR13','CanonicalFockCoefficientInclusionR6'],
 'CanonicalFockModularIdentificationR9':['CanonicalFockCoefficientGraphEqualityR9','CanonicalFockCoefficientUnitaryR3','ClosedTomitaSquareGraphR1'],
 'CanonicalFockWeightPolarR2':['CanonicalFockModularIdentificationR9','CanonicalFockWeightPolarBasicsR1','UnitaryRootGraphTransportR1']}
ALLOWED={'propext','Classical.choice','Quot.sound'}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write_x(p,v):
 with p.open('x',encoding='utf-8',newline='\n') as f:
  json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def state(name):
 src=BASE/(name+'.lean');expected=pin(src)['sha256']
 paths=sorted((BASE/'attempts').glob('*/'+name+'.lean'))
 if not paths:return {'state':'not_started'}
 if len(paths)!=1:raise RuntimeError('Multiple attempts for new immutable name: '+name)
 p=paths[0];rp=p.parent/'RECEIPT.json'
 if pin(p)['sha256']!=expected:raise RuntimeError('Source mismatch: '+name)
 if not rp.exists():return {'state':'running','attempt':str(p.parent)}
 r=json.loads(rp.read_bytes())
 if type(r['exit_code']) is not int or r['exit_code']!=0:
  return {'state':'failed','receipt':pin(rp),'exit_code':r['exit_code']}
 if not r['readonly_dependencies_unchanged']:raise RuntimeError('Dependency mutation: '+name)
 import re
 txt=(p.parent/'AXIOMS.txt').read_text(encoding='utf-8')
 axioms=[{x.strip() for x in a.split(',') if x.strip()} for a in re.findall(r"depends on axioms:\s*\[([^]]*)\]",txt,re.S)]
 axioms += [set() for _ in re.findall(r"'[^']+' does not depend on any axioms",txt)]
 if not axioms or not all(a<=ALLOWED for a in axioms):raise RuntimeError('Axiom refusal: '+name)
 if not (p.parent/(name+'.olean')).is_file():raise RuntimeError('Missing olean: '+name)
 return {'state':'passed','receipt':pin(rp),'source':pin(p),'axiom_prints':len(axioms)}
start=now(); processes={};handles={};observed={}
write_x(OUT/'START.json',{'start_utc':start,'pid':os.getpid(),'nodes':NODES,'script':pin(Path(__file__).resolve()),'builder':pin(BASE/'build_takesaki_stream_r4.py'),'scope':'sandbox only, direct Lean prerequisites; no canonical edits or main'})
print(json.dumps({'chain':str(OUT),'pid':os.getpid(),'start_utc':start}),flush=True)
try:
 while True:
  names=set(NODES).union(*(set(d) for d in NODES.values()))
  observed={n:state(n) for n in names}
  failed={n:s for n,s in observed.items() if s['state']=='failed'}
  if failed:raise RuntimeError('Failed prerequisite or consumer: '+','.join(failed))
  for n,proc in list(processes.items()):
   rc=proc.poll()
   if rc is not None:
    handles[n].close();del processes[n]
    if rc!=0:raise RuntimeError('Builder failed: '+n+' exit '+str(rc))
  if all(observed[n]['state']=='passed' for n in NODES):break
  for n,deps in NODES.items():
   if len(processes)>=2:break
   if observed[n]['state']!='not_started' or n in processes:continue
   if not all(observed[d]['state']=='passed' for d in deps):continue
   log=(OUT/(n+'.launcher.log')).open('xb');handles[n]=log
   cmd=[sys.executable,'-X','utf8','-B',str(BASE/'build_takesaki_stream_r4.py'),n+'.lean']
   proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,cwd=BASE)
   processes[n]=proc
   write_x(OUT/(n+'.LAUNCH.json'),{'start_utc':now(),'pid':proc.pid,'command':cmd,'source':pin(BASE/(n+'.lean')),'prerequisites':{d:observed[d] for d in deps}})
   print(json.dumps({'launched':n,'pid':proc.pid,'utc':now()}),flush=True)
  time.sleep(30)
 result={'status':'ALL_REAL_BUILDS_PASSED','start_utc':start,'end_utc':now(),'nodes':observed}
 code=0
except Exception as exc:
 # Keep the supervisor alive until all of its launched children have exited.
 # A terminal failure must not abandon active Lean processes without a receipt.
 for child in processes.values():
  child.wait()
 for log in handles.values():
  if not log.closed:log.close()
 result={'status':'STOPPED_VISIBLE_FAILURE','start_utc':start,'end_utc':now(),'error':repr(exc),'nodes':observed,'children_preserved':{n:p.pid for n,p in processes.items() if p.poll() is None}}
 code=1
write_x(OUT/'RESULT.json',result)
print(json.dumps({'receipt':pin(OUT/'RESULT.json'),'status':result['status']}),flush=True)
raise SystemExit(code)
