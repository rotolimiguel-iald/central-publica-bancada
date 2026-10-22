"""Run one pinned Lean command in a Windows Job, with bounded resources and custody."""
import ctypes as C
from ctypes import wintypes as W
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

class BasicLimits(C.Structure):
    _fields_ = [('process_time',C.c_int64),('job_time',C.c_int64),('flags',W.DWORD),
                ('min_working',C.c_size_t),('max_working',C.c_size_t),('active_limit',W.DWORD),
                ('affinity',C.c_size_t),('priority',W.DWORD),('scheduling',W.DWORD)]
class IO(C.Structure):
    _fields_ = [(x,C.c_uint64) for x in ('read_ops','write_ops','other_ops','read_bytes','write_bytes','other_bytes')]
class ExtendedLimits(C.Structure):
    _fields_ = [('basic',BasicLimits),('io',IO),('process_mem',C.c_size_t),('job_mem',C.c_size_t),
                ('peak_process_mem',C.c_size_t),('peak_job_mem',C.c_size_t)]
class Accounting(C.Structure):
    _fields_ = [('user',C.c_int64),('kernel',C.c_int64),('period_user',C.c_int64),('period_kernel',C.c_int64),
                ('faults',W.DWORD),('total',W.DWORD),('active',W.DWORD),('terminated',W.DWORD)]

def hash_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

kernel = Path(sys.argv[1]).resolve()
source = Path(sys.argv[2]).resolve()
label = sys.argv[3]
assert source.suffix == '.lean'
allowed = Path(__file__).resolve().parents[1]
assert source.is_relative_to(allowed) and not source.is_relative_to(kernel)
receipt = source.parent / (label + '.json')
log = source.parent / (label + '.log')
marker = source.parent / (label + '.marker')
for p in (receipt,log,marker):
    if p.exists(): raise FileExistsError(p)
toolchain = (kernel/'lean-toolchain').read_text().strip()
assert toolchain == 'leanprover/lean4:v4.31.0', toolchain
lake = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe')
assert lake.is_file(), lake
env = os.environ.copy()
extra_paths = [Path(x).resolve() for x in sys.argv[4:]]
readonly_paths = {Path(p).resolve() for p in json.loads((Path(__file__).parent/'READONLY_IMPORT_PATHS.json').read_bytes())}
assert all(x.is_relative_to(allowed) or x in readonly_paths for x in extra_paths)
env['LEAN_PATH'] = os.pathsep.join(map(str, [source.parent] + extra_paths))
env['ELAN_TOOLCHAIN'] = toolchain
env['OMP_NUM_THREADS'] = '1'
cmd = [str(lake),'env','lean','-j1','-M8192','-R',str(source.parent),'-o',str(source.with_suffix('.olean')),str(source)]
k32 = C.WinDLL('kernel32',use_last_error=True)
k32.CreateJobObjectW.argtypes=[C.c_void_p,W.LPCWSTR]; k32.CreateJobObjectW.restype=W.HANDLE
for name,args in [('SetInformationJobObject',[W.HANDLE,C.c_int,C.c_void_p,W.DWORD]),
                  ('QueryInformationJobObject',[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.c_void_p]),
                  ('AssignProcessToJobObject',[W.HANDLE,W.HANDLE]),('TerminateJobObject',[W.HANDLE,W.UINT]),
                  ('CloseHandle',[W.HANDLE])]:
    f=getattr(k32,name);f.argtypes=args;f.restype=W.BOOL
job=k32.CreateJobObjectW(None,None)
if not job:raise C.WinError(C.get_last_error())
limits=ExtendedLimits(); limits.basic.flags=0x4|0x100|0x2000
limits.basic.job_time=900*10_000_000;limits.process_mem=8*1024**3
if not k32.SetInformationJobObject(job,9,C.byref(limits),C.sizeof(limits)):raise C.WinError(C.get_last_error())
marker.write_bytes(b'Kernel modification marker; outside kernel.\n')
before_ns=marker.stat().st_mtime_ns
start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
with log.open('xb') as output:
    process=subprocess.Popen(cmd,cwd=kernel,env=env,stdout=output,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    if not k32.AssignProcessToJobObject(job,W.HANDLE(int(process._handle))):
        process.kill();process.wait();raise C.WinError(C.get_last_error())
    try:rc=process.wait(timeout=900)
    except subprocess.TimeoutExpired:
        k32.TerminateJobObject(job,124);rc=process.wait()
elapsed=time.monotonic()-start
account=Accounting();measured=ExtendedLimits()
ok_account=bool(k32.QueryInformationJobObject(job,1,C.byref(account),C.sizeof(account),None))
ok_mem=bool(k32.QueryInformationJobObject(job,9,C.byref(measured),C.sizeof(measured),None))
k32.CloseHandle(job)
newer=[];scan_errors=[]
def scan_error(error):scan_errors.append(str(error))
for root,dirs,files in os.walk(kernel,onerror=scan_error):
    for name in files:
        p=Path(root)/name
        try:
            st=p.stat()
            if st.st_mtime_ns>before_ns:newer.append({'path':str(p),'bytes':st.st_size,'mtime_ns':st.st_mtime_ns})
        except OSError as error:scan_errors.append(str(error))
data={'status':'REAL','utc':utc,'kernel':str(kernel),'command':cmd,'lean_path':env['LEAN_PATH'],
      'rc':rc,'wall_seconds':elapsed,'cpu_user_seconds':account.user/1e7 if ok_account else None,
      'cpu_kernel_seconds':account.kernel/1e7 if ok_account else None,
      'peak_process_committed_bytes':measured.peak_process_mem if ok_mem else None,
      'peak_job_committed_bytes':measured.peak_job_mem if ok_mem else None,
      'memory_metric':'Windows Job committed memory; not peak working-set RSS',
      'source_sha256':hash_file(source),'log_sha256':hash_file(log),'newer_kernel_files':newer,'scan_errors':scan_errors,
      'opening_sha256':hash_file(allowed.parent/'TUNEL/DO_CHATGPT/ENTREGA_016_ABERTURA_operador.md')}
raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
tmp=receipt.with_suffix('.json.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.rename(receipt)
print(json.dumps({k:data[k] for k in ('rc','wall_seconds','cpu_user_seconds','cpu_kernel_seconds','peak_process_committed_bytes','newer_kernel_files','scan_errors')},ensure_ascii=False))
print(log.read_text(encoding='utf-8',errors='replace')[:7000])
