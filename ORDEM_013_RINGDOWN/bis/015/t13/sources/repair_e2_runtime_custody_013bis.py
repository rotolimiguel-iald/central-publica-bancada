"""Transfer the unchanged E2 seed to the Windows identity hosting WSL.

Exclusive DACL only; no Everyone/group grants, no policy changes, no seed disclosure.
The original registration and its creation receipt stay byte-for-byte preserved.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ctypes,ctypes.wintypes as wt,hashlib,json,os
import e2_private_directory_native as acl
B=Path(__file__).resolve().parents[1]
TARGET=B/'bis/E2_RUNTIME_WINDOWS_IDENTITY_V1.json'
FOLDER=B/'cache/E2_PRIVATE';SEED=FOLDER/'BLIND_SEED_V1.bin'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def create(p,v):
    raw=(json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode();tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Incomplete metadata')
    os.link(tmp,p);tmp.unlink()

def unredirected(p,kernel):
    for q in (p,*p.parents):
        attributes=kernel.GetFileAttributesW(str(q))
        if attributes==0xffffffff or attributes&0x400:raise ValueError('Missing/redirected custody path')

def assign(path,sid,directory,adv,kernel):
    adv.GetSecurityDescriptorDacl.argtypes=[ctypes.c_void_p,ctypes.POINTER(wt.BOOL),ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(wt.BOOL)]
    adv.GetSecurityDescriptorDacl.restype=wt.BOOL
    adv.SetNamedSecurityInfoW.argtypes=[wt.LPWSTR,ctypes.c_int,wt.DWORD,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
    adv.SetNamedSecurityInfoW.restype=wt.DWORD
    descriptor=ctypes.c_void_p();dacl=ctypes.c_void_p();present=wt.BOOL();defaulted=wt.BOOL()
    text='D:P(A;'+('OICI' if directory else '')+';FA;;;'+sid+')'
    if not adv.ConvertStringSecurityDescriptorToSecurityDescriptorW(text,1,ctypes.byref(descriptor),None):raise ctypes.WinError(ctypes.get_last_error())
    try:
        if not adv.GetSecurityDescriptorDacl(descriptor,ctypes.byref(present),ctypes.byref(dacl),ctypes.byref(defaulted)):
            raise ctypes.WinError(ctypes.get_last_error())
        if not present.value or not dacl.value:raise ValueError('Null DACL refused')
        error=adv.SetNamedSecurityInfoW(str(path),1,0x80000004,None,None,dacl,None)
        if error:raise ctypes.WinError(error)
    finally:kernel.LocalFree(descriptor)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--action',required=True,choices=['record-target','transfer','verify'])
    ap.add_argument('--expected-target-sha256');ap.add_argument('--expected-registration-sha256');a=ap.parse_args()
    adv,kernel=acl.native();sid=acl.current_sid();sid_hash=hashlib.sha256(sid.encode()).hexdigest()
    now=datetime.now(timezone.utc).isoformat()
    if a.action=='record-target':
        value={'status':'WINDOWS_RUNTIME_HOST_IDENTITY_ONLY','created_utc':now,'sid':sid,'sid_sha256':sid_hash,
          'scope':'Captured by the explicitly escalated Windows host process used to launch WSL; identity metadata, no seed read',
          'script_sha256':sha(Path(__file__))}
        create(TARGET,value);print(json.dumps({'status':value['status'],'sha256':sha(TARGET),'sid_sha256':sid_hash}));return
    regpath=B/'RINGDOWN_5SIGMA_V1.json'
    if sha(TARGET)!=a.expected_target_sha256 or sha(regpath)!=a.expected_registration_sha256:raise ValueError('Explicit metadata/registration pins differ')
    target=json.loads(TARGET.read_bytes());reg=json.loads(regpath.read_bytes());target_sid=target['sid']
    if target['status']!='WINDOWS_RUNTIME_HOST_IDENTITY_ONLY' or hashlib.sha256(target_sid.encode()).hexdigest()!=target['sid_sha256']:
        raise ValueError('Target identity metadata inconsistent')
    for p in (TARGET,regpath,FOLDER,SEED):unredirected(p,kernel)
    common={'registration_sha256':sha(regpath),'target_identity_sha256':sha(TARGET),
      'seed_commitment_sha256':reg['blinding']['seed_commitment_sha256'],'script_sha256':sha(Path(__file__)),
      'utc':now,'seed_bytes_disclosed':False,'registration_modified':False,'execution_policy_changed':False}
    if a.action=='transfer':
        receipt=B/'bis/E2_CUSTODY_TRANSFER_V1.json'
        if receipt.exists():raise FileExistsError('Transfer already attempted')
        if sid==target_sid:raise ValueError('Expected distinct creation/runtime identities')
        acl.verify_acl(FOLDER,sid,True,adv,kernel);acl.verify_acl(SEED,sid,False,adv,kernel)
        if SEED.stat().st_size!=32 or sha(SEED)!=reg['blinding']['seed_commitment_sha256']:raise ValueError('Original commitment differs')
        create(B/'bis/E2_CUSTODY_TRANSFER_BEFORE_V1.json',{**common,'status':'AUTHORIZED_EXCLUSIVE_IDENTITY_TRANSFER_BEFORE_MUTATION',
          'creation_sid_sha256':sid_hash,'runtime_sid_sha256':target['sid_sha256'],
          'reason':'Windows sandbox creation identity differs from escalated Windows host identity used by WSL',
          'scope':'Metadata-only transfer, same seed bytes; same-user procedural custody, not separation from privileged OS access'})
        stages=[];error=None
        try:
            # Protected file first: no intermediate broad/group grant.
            assign(SEED,target_sid,False,adv,kernel);stages.append('seed_exclusive_target_DACL')
            assign(FOLDER,target_sid,True,adv,kernel);stages.append('directory_exclusive_target_DACL')
        except Exception as exc:error={'type':type(exc).__name__,'message':str(exc)}
        value={**common,'status':'DACL_TRANSFERRED_AWAITING_HOST_VERIFICATION' if error is None else 'TRANSFER_PARTIAL_OR_FAILED',
          'stages':stages,'error':error,'seed_bytes_rewritten':False}
        create(receipt,value);print(json.dumps(value))
        if error:raise SystemExit(2)
    else:
        if sid!=target_sid:raise ValueError('Verification must run as recorded runtime Windows identity')
        transfer=B/'bis/E2_CUSTODY_TRANSFER_V1.json'
        previous=json.loads(transfer.read_bytes())
        if previous['status']!='DACL_TRANSFERRED_AWAITING_HOST_VERIFICATION' or previous['registration_sha256']!=sha(regpath):raise ValueError('No completed metadata transfer')
        acl.verify_acl(FOLDER,sid,True,adv,kernel);acl.verify_acl(SEED,sid,False,adv,kernel)
        if SEED.stat().st_size!=32 or sha(SEED)!=reg['blinding']['seed_commitment_sha256']:raise ValueError('Runtime commitment differs')
        value={**common,'status':'HOST_EXCLUSIVE_DACL_AND_UNCHANGED_SEED_COMMITMENT_VERIFIED','transfer_receipt_sha256':sha(transfer),
          'one_full_control_identity':True,'WSL_integration':'Still requires separately recorded smoke test'}
        out=B/'bis/E2_CUSTODY_HOST_VERIFIED_V1.json';create(out,value);print(json.dumps({'status':value['status'],'sha256':sha(out)}))

if __name__=='__main__':main()
