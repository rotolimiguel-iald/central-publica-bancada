"""One new helper/double test run; no POSIX or scientific integration claim."""
from pathlib import Path
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
PREP=ROOT/'f9_profile_store_bridge_preparation'
MANIFEST=PREP/'MANIFESTO_PREPARACAO.json'
EXPECTED_MANIFEST='0cb87987e7a1e6e848bfdb0fda2f70f45975debcd68d656d9c8c48ae5e5f1e77'
WALL_LIMIT=120
MEMORY_CAP=1073741824

def pin(p):
    raw=p.read_bytes()
    return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def save_new(p,data):
    raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.read_bytes()!=raw or p.exists():raise RuntimeError('exclusive write verification')
    tmp.rename(p)

class Counters(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]

CHILD=r"""
import sys,os,json,unittest,unittest.mock
from pathlib import Path
prep=Path(sys.argv[1]); metadata=json.loads((prep/'MANIFESTO_PREPARACAO.json').read_bytes())
allowed={str(Path(v['path']).resolve()).casefold() for v in [{'path':str(prep/v['name'])} for v in metadata['files']]+list(metadata['source_pins'].values())}
stdlib=str((Path(sys.base_prefix)/'Lib').resolve()).casefold()+os.sep
blocked={'numpy','scipy','camb','bilby','lal','lalsimulation','torch','requests','httpx','anthropic'}
def guard(event,args):
    if event=='import' and str(args[0]).split('.')[0] in blocked:raise RuntimeError('scientific or remote import prohibited')
    if event.startswith(('socket.','subprocess.')) or event in ('os.system','os.spawn','os.fork','os.exec'):raise RuntimeError('network or child process prohibited')
    if event=='open' and not isinstance(args[0],int):
        name,mode,flags=args
        if isinstance(mode,str) and any(x in mode for x in 'wax+'):raise RuntimeError('test write prohibited')
        if flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):raise RuntimeError('test write prohibited')
        target=str(Path(name).resolve()).casefold()
        if target.endswith('.pyc') and not target.startswith(stdlib):raise FileNotFoundError('source-only loading required')
        if target not in allowed and not target.startswith(stdlib):raise RuntimeError('read outside pinned code or stdlib prohibited: '+target)
sys.dont_write_bytecode=True
sys.addaudithook(guard)
sys.path.insert(0,str(prep))
suite=unittest.defaultTestLoader.loadTestsFromName('test_readback_stdlib')
result=unittest.TextTestRunner(verbosity=2).run(suite)
print('@@TEST_RESULT@@'+json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'successful':result.wasSuccessful(),'scientific_modules_loaded':sorted(blocked.intersection(sys.modules))}),flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
"""

def main():
    if (OUT/'STARTED.json').exists():raise RuntimeError('already consumed; no automatic repeat')
    p=pin(MANIFEST)
    if p['sha256']!=EXPECTED_MANIFEST:raise RuntimeError('manifest changed')
    m=json.loads(MANIFEST.read_bytes())
    for v in [{'path':str(PREP/v['name']),'bytes':v['bytes'],'sha256':v['sha256']} for v in m['files']]+list(m['source_pins'].values()):
        if pin(Path(v['path']))!=v:raise RuntimeError('source drift')
    review=Path(sys.argv[1]).resolve()
    review_pin=pin(review)
    if review_pin['sha256']!=sys.argv[2]:raise RuntimeError('review changed')
    psapi=ctypes.WinDLL('psapi',use_last_error=True)
    get=psapi.GetProcessMemoryInfo
    get.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
    get.restype=wintypes.BOOL
    start=time.perf_counter()
    save_new(OUT/'STARTED.json',{'scope':'STDLIB_HELPERS_AND_DOUBLES_ONLY','manifest':p,'review':review_pin,'runner':pin(Path(__file__)),'wall_limit_seconds':WALL_LIMIT,'memory_observation_cap_bytes':MEMORY_CAP,'memory_enforcement':'polled at 50ms; not an absolute OS limit','automatic_retry':False})
    process=None; reason=None; peak=0; peak_commit=0; samples=0; sample_failures=0; rc=None
    try:
        with (OUT/'stdout.txt').open('xb') as so,(OUT/'stderr.txt').open('xb') as se:
            process=subprocess.Popen([sys.executable,'-I','-S','-B','-X','utf8','-c',CHILD,str(PREP)],stdin=subprocess.DEVNULL,stdout=so,stderr=se,cwd=OUT,creationflags=subprocess.CREATE_NO_WINDOW)
            while True:
                counters=Counters();counters.cb=ctypes.sizeof(counters)
                if get(wintypes.HANDLE(int(process._handle)),ctypes.byref(counters),counters.cb):
                    peak=max(peak,counters.PeakWorkingSetSize);peak_commit=max(peak_commit,counters.PeakPagefileUsage);samples+=1
                elif process.poll() is None:sample_failures+=1
                rc=process.poll()
                if rc is not None:break
                elapsed=time.perf_counter()-start
                if elapsed>=WALL_LIMIT-1 or max(peak,peak_commit)>MEMORY_CAP or sample_failures:
                    reason='wall_limit' if elapsed>=WALL_LIMIT-1 else ('memory_cap' if max(peak,peak_commit)>MEMORY_CAP else 'memory_measurement_failed')
                    process.kill();rc=process.wait(timeout=1);break
                time.sleep(.05)
    except BaseException as exc:
        reason=type(exc).__name__+': '+str(exc)
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            try:rc=process.wait(timeout=1)
            except subprocess.TimeoutExpired:reason='process_termination_uncertain'
    elapsed=time.perf_counter()-start
    result=None
    stdout=OUT/'stdout.txt'
    if stdout.exists():
        for line in stdout.read_text(encoding='utf-8',errors='strict').splitlines():
            if line.startswith('@@TEST_RESULT@@'):result=json.loads(line[len('@@TEST_RESULT@@'):])
    passed=rc==0 and reason is None and elapsed<=WALL_LIMIT and samples>0 and sample_failures==0 and max(peak,peak_commit)<=MEMORY_CAP and result is not None and result['tests_run']==26 and result['successful'] and not result['scientific_modules_loaded']
    receipt={'schema':'F9_PROFILE_STORE_HELPERS_QUALIFICATION_V1','status':'PASS_STDLIB_HELPERS_AND_DOUBLES_ONLY' if passed else 'FAILED_OR_UNCERTAIN_NO_AUTOMATIC_RETRY','manifest':p,'review':review_pin,'runner':pin(Path(__file__)),'elapsed_seconds':elapsed,'returncode':rc,'termination_reason':reason,'peak_working_set_bytes':peak,'peak_commit_bytes':peak_commit,'memory_samples':samples,'memory_sample_failures':sample_failures,'memory_enforcement':'polled 50ms; not an absolute OS limit','tests':result,'logs':[pin(OUT/n) for n in ('stdout.txt','stderr.txt') if (OUT/n).exists()],'science_executed':False,'remote_calls':0,'actual_profile_imported':False,'d72_P3_launched':False,'scientific_decision':None,'actual_registry_imported':False,'posix_store_tested':False,'full_recovery_tested':False,'elapsed_scope':'parent interval from before STARTED to child cleanup; excludes preflight and final receipt/log processing'}
    save_new(OUT/'RESULT.json',receipt)
    print(json.dumps(receipt,ensure_ascii=False))
    return 0 if passed else 1
if __name__=='__main__':sys.exit(main())
