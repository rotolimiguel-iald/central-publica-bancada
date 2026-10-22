"""Create/verify a new private NTFS directory using native Windows ACL APIs.

No execution-policy changes. No seed bytes are generated/read by this helper.
Protection is same-user procedural custody, not separation from administrators.
"""
from pathlib import Path
import ctypes,ctypes.wintypes as wt,csv,io,json,os,re,subprocess
B=Path(__file__).resolve().parents[1]


class SecurityAttributes(ctypes.Structure):
    _fields_=[('length',wt.DWORD),('descriptor',ctypes.c_void_p),('inherit',wt.BOOL)]


def native():
    if os.name!='nt':raise RuntimeError('Windows ACL API required')
    adv=ctypes.WinDLL('advapi32',use_last_error=True);kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    adv.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes=[wt.LPCWSTR,wt.DWORD,ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(wt.DWORD)]
    adv.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype=wt.BOOL
    adv.ConvertSecurityDescriptorToStringSecurityDescriptorW.argtypes=[ctypes.c_void_p,wt.DWORD,wt.DWORD,ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(wt.DWORD)]
    adv.ConvertSecurityDescriptorToStringSecurityDescriptorW.restype=wt.BOOL
    adv.GetNamedSecurityInfoW.argtypes=[wt.LPCWSTR,ctypes.c_int,wt.DWORD,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
    adv.GetNamedSecurityInfoW.restype=wt.DWORD
    kernel.CreateDirectoryW.argtypes=[wt.LPCWSTR,ctypes.POINTER(SecurityAttributes)];kernel.CreateDirectoryW.restype=wt.BOOL
    kernel.GetFileAttributesW.argtypes=[wt.LPCWSTR];kernel.GetFileAttributesW.restype=wt.DWORD
    kernel.LocalFree.argtypes=[ctypes.c_void_p];kernel.LocalFree.restype=ctypes.c_void_p
    return adv,kernel


def current_sid():
    executable=Path(os.environ['SystemRoot'])/'System32/whoami.exe'
    raw=subprocess.run([str(executable),'/user','/fo','csv','/nh'],capture_output=True,check=True,timeout=15).stdout
    rows=list(csv.reader(io.StringIO(raw.decode('utf-8',errors='replace').strip())))
    if len(rows)!=1 or len(rows[0])!=2 or not re.fullmatch(r'S-1-[0-9-]+',rows[0][1]):raise ValueError('Current Windows SID unavailable')
    return rows[0][1]


def check_sddl(text,sid,directory):
    prefix=text.split('(',1)[0];aces=re.findall(r'\(([^()]*)\)',text)
    if not prefix.startswith('D:') or len(aces)!=1:raise ValueError('DACL must have one explicit identity')
    fields=aces[0].split(';')
    if len(fields)!=6 or fields[0]!='A' or fields[2] not in ('FA','0x1f01ff') or fields[3:5]!=['',''] or fields[5]!=sid:
        raise ValueError('DACL is not current-user FullControl only')
    if directory:
        if 'P' not in prefix[2:] or fields[1] not in ('OICI','CIOI'):raise ValueError('Directory must be protected and inheritable')
    elif fields[1] not in ('','ID'):raise ValueError('Unexpected seed ACE flags')


def verify_acl(path,sid,directory,adv,kernel):
    attributes=kernel.GetFileAttributesW(str(path))
    if attributes==0xffffffff or attributes&0x400:raise ValueError('Missing or redirected ACL target')
    descriptor=ctypes.c_void_p();text_pointer=ctypes.c_void_p()
    error=adv.GetNamedSecurityInfoW(str(path),1,4,None,None,None,None,ctypes.byref(descriptor))
    if error:raise ctypes.WinError(error)
    try:
        if not adv.ConvertSecurityDescriptorToStringSecurityDescriptorW(descriptor,1,4,ctypes.byref(text_pointer),None):raise ctypes.WinError(ctypes.get_last_error())
        try:check_sddl(ctypes.wstring_at(text_pointer),sid,directory)
        finally:kernel.LocalFree(text_pointer)
    finally:kernel.LocalFree(descriptor)


def operate(action):
    if action not in ('Prepare','Verify','VerifySeed'):raise ValueError('Unknown ACL action')
    adv,kernel=native();sid=current_sid();folder=B/'cache/E2_PRIVATE'
    for parent in folder.parents:
        attributes=kernel.GetFileAttributesW(str(parent))
        if attributes==0xffffffff or attributes&0x400:raise ValueError('Missing or redirected parent')
    if action=='Prepare':
        if folder.exists():raise FileExistsError('Private directory exists; explicit audit required')
        descriptor=ctypes.c_void_p()
        if not adv.ConvertStringSecurityDescriptorToSecurityDescriptorW('D:P(A;OICI;FA;;;'+sid+')',1,ctypes.byref(descriptor),None):raise ctypes.WinError(ctypes.get_last_error())
        try:
            attributes=SecurityAttributes(ctypes.sizeof(SecurityAttributes),descriptor,False)
            if not kernel.CreateDirectoryW(str(folder),ctypes.byref(attributes)):raise ctypes.WinError(ctypes.get_last_error())
        finally:kernel.LocalFree(descriptor)
    verify_acl(folder,sid,True,adv,kernel)
    if action=='VerifySeed':verify_acl(folder/'BLIND_SEED_V1.bin.pending',sid,False,adv,kernel)
    return {'status':'CURRENT_WINDOWS_USER_ONLY_DACL_VERIFIED','protected':True,'allow_rules':1,'path':str(folder),
      'scope':'Native Windows ACL; current-user processes/WSL and privileged OS access are not independent custody; no script policy altered'}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--action',required=True,choices=['Prepare','Verify','VerifySeed']);args=ap.parse_args()
    print(json.dumps(operate(args.action)))
