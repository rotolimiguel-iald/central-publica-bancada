"""Exercise only the new path-normalization guard; no scientific program import."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time

HERE=Path(__file__).resolve().parent
BASE=HERE/'guard_r4_test'
ROOT=BASE/'sandbox'
OUTSIDE=BASE/'outside'
if BASE.exists(): raise FileExistsError(BASE)
ROOT.mkdir(parents=True);OUTSIDE.mkdir()
LINK=ROOT/'escape_junction'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    with p.open('xb') as f:f.write(b)

# Native junction is temporary and targets only this test's outside directory.
# No path in the scientific originals or production is used as its target.
creation=subprocess.run(['powershell','-NoProfile','-Command',
    f"New-Item -ItemType Junction -Path '{LINK}' -Target '{OUTSIDE}' | Out-Null"],capture_output=True,text=True)
if creation.returncode or not LINK.is_junction() or LINK.resolve()!=OUTSIDE.resolve():
    raise RuntimeError('Controlled junction setup failed')
env=dict(os.environ,TGL_RITE_SANDBOX=str(ROOT),TGL_RITE_GUARD_PHASE='preflight',
    TGL_LAKE=r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe',
    PYTHONDONTWRITEBYTECODE='1')
code=r'''
import importlib.util,json,os,socket
from pathlib import Path
root=Path(os.environ['TGL_RITE_SANDBOX']);outside=root.parent/'outside'
spec=importlib.util.spec_from_file_location('rite_guard',os.environ['TEST_GUARD_SOURCE']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
import sys
_safety_hits=[]
def _independent_safety(event,args):
 if event in {'socket.connect','socket.connect_ex','socket.bind','socket.getaddrinfo','socket.gethostbyname','socket.gethostbyaddr','socket.getnameinfo','socket.sendto','socket.sendmsg'}:
  _safety_hits.append(event)
  raise RuntimeError('Independent safety intercepted network event: '+event)
sys.addaudithook(_independent_safety)
checks=[]
def yes(name,condition): checks.append({'name':name,'passed':bool(condition)})
def refused(name,action):
 try:action();yes(name,False)
 except PermissionError:yes(name,True)
ext=chr(92)*2+'?'+chr(92)
for name,path in [('ordinary',str(root/'ordinary')),('extended',ext+str(root/'extended'))]:
 os.mkdir(path);yes('mkdir_'+name,Path(path).is_dir())
 with open(str(Path(path)/'value.txt'),'x') as f:f.write('inside')
 yes('write_'+name,True)
refused('parent_escape',lambda:os.mkdir(str(root/'..'/'outside'/'escaped')))
refused('extended_parent_escape',lambda:os.mkdir(ext+str(root/'..'/'outside'/'extended_escape')))
refused('sibling_prefix_escape',lambda:os.mkdir(str(root.parent/'sandbox_evil')))
refused('junction_escape',lambda:os.mkdir(str(root/'escape_junction'/'escaped')))
refused('extended_junction_escape',lambda:os.mkdir(ext+str(root/'escape_junction'/'extended_escape')))
refused('ordinary_outside_write',lambda:open(outside/'forbidden','x'))
yes('UNC_rejected_without_remote_access',not m._inside(ext+'UNC'+chr(92)+'nonexistent.invalid'+chr(92)+'share'+chr(92)+'x'))
yes('NT_device_not_reinterpreted_inside',not m._inside(ext+'GLOBALROOT'+chr(92)+'Device'+chr(92)+'HarddiskVolumeShadowCopy1'+chr(92)+'x'))
refused('DNS_still_refused',lambda:socket.getaddrinfo('nonexistent.invalid',443))
# The real UDP call must be stopped by the audit event before transmission.
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as udp:
 refused('UDP_sendto_refused_before_transmission',lambda:udp.sendto(b'guard-probe',('127.0.0.1',9)))
refused('reverse_lookup_getnameinfo_refused',lambda:socket.getnameinfo(('127.0.0.1',9),0))
import sys
refused('sendmsg_audit_event_refused',lambda:sys.audit('socket.sendmsg',None,('127.0.0.1',9)))
yes('independent_safety_not_needed',not _safety_hits)
print(json.dumps({'checks':checks,'passed':all(x['passed'] for x in checks)}))
'''
env['TEST_GUARD_SOURCE']=str(HERE/'sitecustomize_rite_r4.py')
command=[sys.executable,'-B','-X','utf8','-c',code]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();timer=time.perf_counter()
try:
    run=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',timeout=120)
finally:
    # Validate both absolute locations and the link identity before deleting
    # only the junction itself. Never recurse through the target.
    if not LINK.absolute().is_relative_to(BASE.absolute()) or LINK.resolve()!=OUTSIDE.resolve() or not LINK.is_junction():
        raise RuntimeError('Junction identity changed; refusing cleanup')
    cleanup=subprocess.run(['powershell','-NoProfile','-Command',f"Remove-Item -LiteralPath '{LINK}' -Force"],capture_output=True,text=True)
    if cleanup.returncode or LINK.exists():raise RuntimeError('Junction cleanup failed')
try:result=json.loads(run.stdout.strip().splitlines()[-1])
except Exception:result={'passed':False}
report={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-timer,'command':command,'cwd':str(ROOT),'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'result':result,'guard_sha256':sha(HERE/'sitecustomize_rite_r4.py'),'script_sha256':sha(Path(__file__)),'junction_removed':not LINK.exists(),'outside_unchanged_empty':not any(OUTSIDE.iterdir()),'scientific_program_executed':False,'network_enabled':False}
report['passed']=run.returncode==0 and result['passed'] and report['junction_removed'] and report['outside_unchanged_empty']
save(HERE/'GUARD_PATHS_R4_RESULT.json',report)
print(json.dumps({'passed':report['passed'],'checks':len(result.get('checks',[])),'sha256':sha(HERE/'GUARD_PATHS_R4_RESULT.json')}))
raise SystemExit(0 if report['passed'] else 1)
