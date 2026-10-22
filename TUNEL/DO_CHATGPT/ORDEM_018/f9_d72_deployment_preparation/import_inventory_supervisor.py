"""One bounded import inspection, with real child handle and audited terminal."""
import time
ENTRY=time.monotonic()
import os,sys,json,hashlib,stat,subprocess,signal,selectors,resource
from pathlib import Path
BASE=Path('/opt/iald_ordem018_d72_d72f7125/inspection')
assert os.geteuid()==os.getegid()==65534
PLAN=json.loads((BASE/'IMPORT_INSPECTION_PLAN.json').read_bytes())
COMMAND=PLAN['collector_argv'];ENV=PLAN['environment']
assert COMMAND==['/usr/bin/python3.12','-I','-S','-B','-X','utf8',str(BASE/'runtime_import_collector.py')]
raw=(BASE/'runtime_import_collector.py').read_bytes();assert {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}==PLAN['collector_pin']
assert PLAN['limits']=={'total_seconds':120,'work_seconds':110,'memory_bytes':8589934592,'threads':1,'stdout_bytes':16777216,'stderr_bytes':1048576}
for name in ['PRE_IMPORT_RECEIPT.json','IMPORT_STDOUT.txt','IMPORT_STDERR.txt','IMPORT_TERMINAL.json']:
 assert not os.path.lexists(BASE/name),'INSPECTION_ALREADY_STARTED_NO_RETRY'
def save(name,obj):
 raw=(json.dumps(obj,sort_keys=True,indent=2)+'\n').encode();fd=os.open(BASE/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def identity(pid):
 root=Path('/proc')/str(pid);raw=(root/'stat').read_text();tail=raw[raw.rfind(')')+2:].split()
 return {'pid':pid,'ppid':int(tail[1]),'start_ticks':int(tail[19]),'exe':str((root/'exe').resolve()),'argv':[x.decode() for x in (root/'cmdline').read_bytes().split(b'\0')[:-1]]}
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(8589934592,8589934592));resource.setrlimit(resource.RLIMIT_CPU,(110,110));resource.setrlimit(resource.RLIMIT_FSIZE,(16777216,16777216));resource.setrlimit(resource.RLIMIT_NOFILE,(128,128));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
receipt={'schema':'F9_IMPORT_INSPECTION_BEFORE_EXECUTION_V1','collector_argv':COMMAND,'collector_pin':PLAN['collector_pin'],'supervisor_pid':os.getpid(),'supervisor_identity':identity(os.getpid()),'limits':PLAN['limits'],'environment':ENV,'entry_monotonic':ENTRY,'deadline_monotonic':ENTRY+120,'work_deadline_monotonic':ENTRY+110,'science_authorization':False,'scope':'ONE_RUNTIME_IMPORT_INVENTORY_ONLY'}
save('PRE_IMPORT_RECEIPT.json',receipt)
outputs={};captures={'stdout':0,'stderr':0};p=None;pidfd=None;ident=None;failure=None;reaped=False;killed=False;exit_code=None
try:
 for key in captures:outputs[key]=os.open(BASE/('IMPORT_'+key.upper()+'.txt'),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 p=subprocess.Popen(COMMAND,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=BASE,env=ENV,close_fds=True,start_new_session=True,preexec_fn=limits)
 pidfd=os.pidfd_open(p.pid,0);ident=identity(p.pid)
 assert ident['ppid']==os.getpid() and ident['exe']==COMMAND[0] and ident['argv']==COMMAND
 sel=selectors.DefaultSelector()
 for name,stream in [('stdout',p.stdout),('stderr',p.stderr)]:os.set_blocking(stream.fileno(),False);sel.register(stream,selectors.EVENT_READ,name)
 while sel.get_map():
  left=ENTRY+110-time.monotonic()
  if left<=0:raise TimeoutError('IMPORT_INSPECTION_WORK_DEADLINE')
  for key,_ in sel.select(min(left,0.1)):
   chunk=os.read(key.fileobj.fileno(),65536)
   if not chunk:sel.unregister(key.fileobj);continue
   name=key.data;captures[name]+=len(chunk)
   if captures[name]>PLAN['limits'][name+'_bytes']:raise RuntimeError('CAPTURE_LIMIT:'+name)
   view=memoryview(chunk)
   while view:view=view[os.write(outputs[name],view):]
 exit_code=p.wait(timeout=max(0.001,ENTRY+120-time.monotonic()));reaped=True
 if exit_code!=0:failure='CHILD_NONZERO_EXIT'
except BaseException as exc:
 failure=type(exc).__name__+':'+str(exc)
 if p is not None and not reaped:
  try:
   if pidfd is not None:signal.pidfd_send_signal(pidfd,signal.SIGKILL,None,0)
   else:p.kill() # Popen owns this not-yet-reaped child; no PID reuse possible.
   killed=True
  except ProcessLookupError:pass
  except BaseException as cleanup:failure+=';KILL_UNCERTAIN:'+str(cleanup)
  try:exit_code=p.wait(timeout=max(0.001,ENTRY+120-time.monotonic()));reaped=True
  except BaseException as cleanup:failure+=';REAP_UNCERTAIN:'+str(cleanup)
finally:
 for fd in outputs.values():os.fsync(fd);os.close(fd)
 if pidfd is not None:os.close(pidfd)
 elapsed=time.monotonic()-ENTRY
 if elapsed>120:failure=(failure or '')+';TOTAL_DEADLINE_EXCEEDED'
 if not reaped:failure=(failure or '')+';CLEANUP_UNCERTAIN'
 pins={}
 for key in captures:
  path=BASE/('IMPORT_'+key.upper()+'.txt')
  if path.exists():raw=path.read_bytes();pins[key]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
 terminal={'schema':'F9_IMPORT_SUPERVISOR_TERMINAL_V1','status':'IMPORT_ONLY_EXIT0_REAPED' if failure is None and exit_code==0 and reaped else 'FAILED_NO_AUTOMATIC_RETRY','child_identity':ident,'pidfd_opened':pidfd is not None,'child_exit_code':exit_code,'child_reaped':reaped,'kill_requested':killed,'failure':failure,'elapsed_from_supervisor_entry_seconds':elapsed,'capture_pins':pins,'limits':PLAN['limits'],'science_execution':False,'candidate_imports':0}
 save('IMPORT_TERMINAL.json',terminal);print(json.dumps(terminal))
if failure is not None or exit_code!=0:sys.exit(1)
