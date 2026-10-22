"""At E3.1 only: stop explicitly owned old diagnostic scripts and inventory bytes."""
from pathlib import Path
from datetime import datetime,timezone
import os,signal,time,json,hashlib,argparse,sys
B=Path(__file__).resolve().parents[1];R=B.parent
NAMES={'run_real_phase_importance.py','run_continuous_source_curves.py'}

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()

def identity(pid):
    root=Path('/proc')/str(pid)
    try:
        argv=[s.decode() for s in (root/'cmdline').read_bytes().split(b'\0') if s]
        if not argv or 'python' not in Path(argv[0]).name:return None
        cwd=(root/'cwd').resolve()
        if not cwd.is_relative_to(B.resolve()) or root.stat().st_uid!=os.getuid():return None
        matched=[x for x in argv[1:] if Path(x).name in NAMES]
        if len(matched)!=1:return None
        script=(cwd/matched[0]).resolve()
        if not script.is_relative_to(B.resolve()) or not script.is_file():return None
        stat=(root/'stat').read_text().rsplit(')',1)[1].split()
        return {'pid':pid,'argv':argv,'cwd':str(cwd),'script':str(script),'script_sha256':sha(script),
          'start_ticks':stat[19],'state':stat[0],'uid':root.stat().st_uid}
    except (FileNotFoundError,PermissionError,ProcessLookupError):return None

def inventory():return [v for p in Path('/proc').iterdir() if p.name.isdigit() and (v:=identity(int(p.name))) is not None]

def same(row):
    current=identity(row['pid'])
    return current is not None and current['start_ticks']==row['start_ticks'] and current['script_sha256']==row['script_sha256']

def signal_owned(row,sig):
    try:fd=os.pidfd_open(row['pid'])
    except ProcessLookupError:return False
    try:
        if not same(row):return False
        try:signal.pidfd_send_signal(fd,sig)
        except ProcessLookupError:return False
        return True
    finally:os.close(fd)

def create(p,d):
    with p.open('x') as f:json.dump(d,f,indent=2,allow_nan=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('--execute-at-E3-1',action='store_true');p.add_argument('--B2-delivery',required=True);a=p.parse_args()
    if not a.execute_at_E3_1 or os.name!='posix':raise ValueError('Explicit E3.1 phase and WSL required')
    sys.path.insert(0,str(B/'bis/e2_code'))
    from registration_guard import checked_registration
    reg,digest=checked_registration()
    delivery=Path(a.B2_delivery).resolve()
    if not delivery.is_relative_to(R/'TUNEL/DO_CHATGPT') or not delivery.is_file():raise ValueError('B2 delivery required before pilot')
    tag=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');before=inventory();mem_before=Path('/proc/meminfo').read_text()
    initial={'utc':datetime.now(timezone.utc).isoformat(),'status':'E3_1_OWNED_JOB_STOP_BEFORE_SIGNAL',
      'registration_sha256':digest,'B2_delivery_sha256':sha(delivery),'processes':before,'meminfo':mem_before,
      'scope':'Only these old script names, own UID, resolved cwd/script within ORDEM013; no current agents/pilots/third-party jobs'}
    create(B/'bis'/('F0_PRESTOP_'+tag+'.json'),initial)
    sent=[]
    for row in before:
        if signal_owned(row,signal.SIGTERM):sent.append({'pid':row['pid'],'signal':'SIGTERM'})
    stop=time.monotonic()+5
    while any(same(r) for r in before) and time.monotonic()<stop:time.sleep(.1)
    for row in before:
        if signal_owned(row,signal.SIGKILL):sent.append({'pid':row['pid'],'signal':'SIGKILL'})
    stop=time.monotonic()+3
    while inventory() and time.monotonic()<stop:time.sleep(.1)
    remaining=inventory()
    if remaining:
        create(B/'bis'/('F0_STOP_FAILED_'+tag+'.json'),{'remaining':remaining,'signals':sent,'registration_sha256':digest})
        raise RuntimeError('Owned old diagnostics still live; no heavy pilot allowed')
    roots=[B/'cache/source_evidence'/n for n in ('phase_real_refined','continuous_source_curves')]
    records=[]
    for root in roots:
        if not root.exists():continue
        for file in sorted(root.rglob('*')):
            if not file.is_file():continue
            s0=file.stat();h=sha(file);s1=file.stat()
            if (s0.st_size,s0.st_mtime_ns)!=(s1.st_size,s1.st_mtime_ns):raise RuntimeError('Diagnostic bytes changed during final hash')
            records.append({'path':file.relative_to(B).as_posix(),'bytes':s1.st_size,'sha256':h,
              'mtime_utc':datetime.fromtimestamp(s1.st_mtime,timezone.utc).isoformat()})
    result={'status':'F0_OWNED_DIAGNOSTIC_JOBS_CLOSED__ANNEX_ONLY','utc':datetime.now(timezone.utc).isoformat(),
      'registration_sha256':digest,'B2_delivery_sha256':sha(delivery),'signals':sent,'after_processes':remaining,
      'meminfo_before':mem_before,'meminfo_after':Path('/proc/meminfo').read_text(),'files':records,
      'scientific_use':'DIAGNOSTIC_ANNEX_ONLY; no result enters physical verdict, systematic gate or E0',
      'code_sha256':sha(Path(__file__))}
    out=B/'bis'/('F0_CLOSED_'+tag+'.json');create(out,result)
    print(json.dumps({'status':result['status'],'files':len(records),'sha256':sha(out),'receipt':str(out)}))

if __name__=='__main__':main()
