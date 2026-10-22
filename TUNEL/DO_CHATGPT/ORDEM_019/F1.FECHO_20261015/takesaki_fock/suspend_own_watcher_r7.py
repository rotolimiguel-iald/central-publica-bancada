"""Suspend ONLY this unit's identified Python scheduler, preserving its Lean child.
This is a reversible scheduling operation; no Lean or scientific result is killed.
"""
import ctypes, datetime, hashlib, json, os
from pathlib import Path
BASE=Path(__file__).resolve().parent
CHAIN=BASE/'consumer_chains/20261016T022713_082905Z'
start=json.loads((CHAIN/'START.json').read_bytes())
assert start['pid']==141088
assert start['script']['path']==str(BASE/'continue_coefficient_consumers_r7.py')
assert hashlib.sha256(Path(start['script']['path']).read_bytes()).hexdigest()==start['script']['sha256']
assert not (CHAIN/'SCHEDULER_SUSPENDED_R1.json').exists()
k=ctypes.WinDLL('kernel32',use_last_error=True)
k.OpenProcess.argtypes=[ctypes.c_ulong,ctypes.c_bool,ctypes.c_ulong]; k.OpenProcess.restype=ctypes.c_void_p
k.CloseHandle.argtypes=[ctypes.c_void_p]
k.QueryFullProcessImageNameW.argtypes=[ctypes.c_void_p,ctypes.c_ulong,ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong)]
h=k.OpenProcess(0x0800|0x1000,False,start['pid'])
if not h:raise ctypes.WinError(ctypes.get_last_error())
try:
 size=ctypes.c_ulong(32768); buf=ctypes.create_unicode_buffer(size.value)
 if not k.QueryFullProcessImageNameW(h,0,buf,ctypes.byref(size)):raise ctypes.WinError(ctypes.get_last_error())
 assert Path(buf.value).resolve()==Path(r'C:\Python314\python.exe').resolve(),buf.value
 # Creation time prevents PID reuse from selecting an unrelated process.
 class FILETIME(ctypes.Structure):_fields_=[('lo',ctypes.c_ulong),('hi',ctypes.c_ulong)]
 k.GetProcessTimes.argtypes=[ctypes.c_void_p,*([ctypes.POINTER(FILETIME)]*4)]
 times=[FILETIME() for _ in range(4)]
 if not k.GetProcessTimes(h,*[ctypes.byref(x) for x in times]):raise ctypes.WinError(ctypes.get_last_error())
 actual=datetime.datetime.fromtimestamp(((times[0].hi<<32)|times[0].lo)/10000000-11644473600,datetime.timezone.utc)
 expected=datetime.datetime.fromisoformat(start['start_utc'])
 assert 0 <= (expected-actual).total_seconds() < 10,(expected,actual)
 launched=list(CHAIN.glob('*.LAUNCH.json'))
 assert [p.name for p in launched]==['CanonicalFockGNSCovarianceR10.LAUNCH.json'],launched
 nt=ctypes.WinDLL('ntdll');nt.NtSuspendProcess.argtypes=[ctypes.c_void_p];nt.NtSuspendProcess.restype=ctypes.c_long
 status=nt.NtSuspendProcess(h)
 if status!=0:raise RuntimeError(('NtSuspendProcess',status))
 result={'status':'ONLY_OWN_SCHEDULER_SUSPENDED','pid':start['pid'],'creation_utc':actual.isoformat(),
   'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'image':buf.value,
   'reason':'Preserve running CovarianceR10 while consolidating consumers that have not started.',
   'lean_children_untouched':True,'next_action':'After the child builder exits, terminate this suspended scheduler and launch consolidated consumer.',
   'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 with (CHAIN/'SCHEDULER_SUSPENDED_R1.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.flush();os.fsync(f.fileno())
 print(json.dumps(result))
finally:k.CloseHandle(h)
