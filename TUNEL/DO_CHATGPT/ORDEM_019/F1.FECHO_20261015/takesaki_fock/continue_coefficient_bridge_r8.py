"""Wait for exact existing helper builds, then build one immutable joined consumer."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
B=Path(__file__).resolve().parent
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
O=B/'consumer_chains'/stamp;O.mkdir(parents=True,exist_ok=False)
def pin(p):
 d=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(d).hexdigest(),bytes=len(d))
def save(p,x):
 with p.open('x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
source=B/'CanonicalFockModularBridgeR3.lean'
sp=pin(source)
waits=[B/'attempts'/x/'RECEIPT.json' for x in ['20261016T024402_847111Z','20261016T024526_760923Z']]
save(O/'START.json',dict(script=pin(Path(__file__)),source=sp,pid=os.getpid(),start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),waiting=list(map(str,waits))))
print(json.dumps(dict(chain=str(O),pid=os.getpid())),flush=True)
for p in waits:
 while not p.exists():time.sleep(8)
 r=json.loads(p.read_bytes())
 if type(r['exit_code']) is not int or r['exit_code']!=0 or not r['readonly_dependencies_unchanged']:
  save(O/'RESULT.json',dict(status='DEPENDENCY_FAILED_NO_CONSUMER_RUN',receipt=pin(p)))
  print('DEPENDENCY_FAILED '+str(p),flush=True);sys.exit(2)
assert pin(source)==sp
cmd=[sys.executable,'-X','utf8','-B',str(B/'build_takesaki_stream_r4.py'),source.name]
with (O/'BUILD_CONSUMER_TRANSCRIPT.log').open('xb') as f:
 p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
 save(O/'LAUNCH.json',dict(command=cmd,builder_pid=p.pid,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=sp))
 print(json.dumps(dict(launched=source.name,builder_pid=p.pid)),flush=True)
 exitcode=p.wait()
save(O/'RESULT.json',dict(exit_code=exitcode,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_unchanged=pin(source)==sp,log=pin(O/'BUILD_CONSUMER_TRANSCRIPT.log')))
print(json.dumps(dict(exit_code=exitcode,chain=str(O))),flush=True)
raise SystemExit(exitcode)
