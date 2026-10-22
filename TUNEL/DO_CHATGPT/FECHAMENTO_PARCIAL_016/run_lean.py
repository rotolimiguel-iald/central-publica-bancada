"""One isolated compilation, Windows Job bounded, append-only receipts."""
import ctypes as C
from ctypes import wintypes as W
from pathlib import Path
import os, sys, subprocess, time, json, hashlib
from datetime import datetime,timezone

class Basic(C.Structure):
    _fields_=[('process_time',C.c_int64),('job_time',C.c_int64),('flags',W.DWORD),('min_working',C.c_size_t),('max_working',C.c_size_t),('active_limit',W.DWORD),('affinity',C.c_size_t),('priority',W.DWORD),('scheduling',W.DWORD)]
class IO(C.Structure):
    _fields_=[(x,C.c_uint64) for x in ('r','w','o','rb','wb','ob')]
class Extended(C.Structure):
    _fields_=[('basic',Basic),('io',IO),('process_mem',C.c_size_t),('job_mem',C.c_size_t),('peak_process_mem',C.c_size_t),('peak_job_mem',C.c_size_t)]
class Accounting(C.Structure):
    _fields_=[('user',C.c_int64),('kernel',C.c_int64),('pu',C.c_int64),('pk',C.c_int64),('faults',W.DWORD),('total',W.DWORD),('active',W.DWORD),('terminated',W.DWORD)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    config=json.loads(Path(sys.argv[1]).read_bytes())
    source=Path(sys.argv[2]).resolve();label=sys.argv[3]
    root=Path(config['root']).resolve();logs=Path(config['logs']).resolve()
    assert source.is_relative_to(root)
    logs.mkdir(parents=True,exist_ok=True)
    log=logs/(label+'.log');receipt=logs/(label+'.json')
    if log.exists() or receipt.exists():raise FileExistsError(label)
    env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(root)]+config['imports']);env['ELAN_TOOLCHAIN']='leanprover/lean4:v4.31.0';env['OMP_NUM_THREADS']='1'
    cmd=[config['lake'],'env','lean','-j1','-M12288','-R',str(root),'-o',str(source.with_suffix('.olean')),str(source)]
    k=C.WinDLL('kernel32',use_last_error=True)
    k.CreateJobObjectW.argtypes=[C.c_void_p,W.LPCWSTR];k.CreateJobObjectW.restype=W.HANDLE
    for name,args in [('SetInformationJobObject',[W.HANDLE,C.c_int,C.c_void_p,W.DWORD]),('QueryInformationJobObject',[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.c_void_p]),('AssignProcessToJobObject',[W.HANDLE,W.HANDLE]),('TerminateJobObject',[W.HANDLE,W.UINT]),('CloseHandle',[W.HANDLE])]:
        f=getattr(k,name);f.argtypes=args;f.restype=W.BOOL
    job=k.CreateJobObjectW(None,None);limits=Extended();limits.basic.flags=0x4|0x100|0x2000;limits.basic.job_time=900*10000000;limits.process_mem=12*1024**3
    if not k.SetInformationJobObject(job,9,C.byref(limits),C.sizeof(limits)):raise C.WinError(C.get_last_error())
    start=time.monotonic();at=datetime.now(timezone.utc).isoformat()
    with log.open('xb') as f:
        p=subprocess.Popen(cmd,cwd=config['cwd'],env=env,stdout=f,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        if not k.AssignProcessToJobObject(job,W.HANDLE(int(p._handle))):
            p.kill();p.wait();raise C.WinError(C.get_last_error())
        try:rc=p.wait(timeout=900)
        except subprocess.TimeoutExpired:k.TerminateJobObject(job,124);rc=p.wait()
    a=Accounting();e=Extended();k.QueryInformationJobObject(job,1,C.byref(a),C.sizeof(a),None);k.QueryInformationJobObject(job,9,C.byref(e),C.sizeof(e),None);k.CloseHandle(job)
    data=dict(at=at,command=cmd,source=str(source),source_sha256=sha(source),rc=rc,wall_seconds=time.monotonic()-start,cpu_seconds=(a.user+a.kernel)/1e7,peak_committed_bytes=e.peak_process_mem,log_sha256=sha(log),config_sha256=sha(Path(sys.argv[1])))
    raw=(json.dumps(data,indent=2)+'\n').encode();tmp=receipt.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.rename(receipt)
    print(json.dumps(dict(file=source.name,rc=rc,seconds=data['wall_seconds'],log=str(log))),flush=True)
    sys.exit(0 if rc==0 else 1)
if __name__=='__main__':main()
