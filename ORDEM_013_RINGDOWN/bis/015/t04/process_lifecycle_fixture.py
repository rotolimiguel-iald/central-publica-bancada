"""Observed lifecycle of supervisor/controller/runner/Pool24; no science."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,subprocess,multiprocessing,time,signal,hashlib,resource
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[2];CODE=B/'bis/e2_code_v1_1_2'
sys.path.insert(0,str(CODE))
from run_controlled import cleanup_group
from registration_guard import publish_new,sha

def sleep_task(i):time.sleep(2);return os.getpid()

def descendants(pid):
    todo=[pid];seen=[]
    while todo:
        p=todo.pop();base=Path('/proc')/str(p)
        try:
            text=(base/'status').read_text();threads=int(next(v.split(':')[1] for v in text.splitlines() if v.startswith('Threads:')))
            seen.append(dict(pid=p,threads=threads));todo.extend(int(v) for v in (base/f'task/{p}/children').read_text().split())
        except (FileNotFoundError,ProcessLookupError):pass
    return seen

def main():
    role=sys.argv[1] if len(sys.argv)>1 else 'supervisor'
    if role=='runner':
        with multiprocessing.get_context('fork').Pool(24) as pool:
            ids=pool.map(sleep_task,list(range(24)),chunksize=1)
        print(json.dumps(dict(worker_pids=sorted(set(ids)),fork=True)),flush=True);return
    if role=='controller':
        def interrupted(signum,frame):raise InterruptedError('Fixture controller interrupted')
        signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
        child=subprocess.Popen([sys.executable,'-B',str(Path(__file__)),'runner'],start_new_session=True)
        try:child.wait(timeout=30)
        finally:cleanup=cleanup_group(child)
        print(json.dumps(dict(controller_cleanup=cleanup,runner_rc=child.returncode)),flush=True)
        if not cleanup['group_absent'] or child.returncode:raise SystemExit(2)
        return
    assert (B/'bis/015/nulls_campaign_001/RESULT.json').exists(),'No27process fixture while6nullprocesses are active'
    out=D/'process_lifecycle_fixture_001';out.mkdir(exist_ok=False)
    start=datetime.now(timezone.utc).isoformat();wall=time.monotonic();usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    snapshots=[];child=None;error=None
    try:
        with (out/'PROCESS.log').open('xb') as f:
            child=subprocess.Popen([sys.executable,'-B',str(Path(__file__)),'controller'],stdout=f,stderr=subprocess.STDOUT,start_new_session=True,
                env={**os.environ,**{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')}})
            while child.poll() is None:
                snapshots.append(dict(at=datetime.now(timezone.utc).isoformat(),processes=descendants(child.pid)))
                if time.monotonic()-wall>40:raise TimeoutError('Fixture exceeded40s')
                time.sleep(.025)
    except BaseException as e:error=dict(type=type(e).__name__,message=str(e))
    finally:
        if child is not None and child.poll() is None:
            child.send_signal(signal.SIGTERM)
            try:child.wait(timeout=3)
            except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
    end=resource.getrusage(resource.RUSAGE_CHILDREN);peak=max((len(s['processes'])+1 for s in snapshots),default=1)
    content=[json.loads(v) for v in (out/'PROCESS.log').read_text().splitlines()]
    workers=next((v['worker_pids'] for v in content if 'worker_pids' in v),[])
    cleaned=next((v['controller_cleanup']['group_absent'] for v in content if 'controller_cleanup' in v),False)
    passed=child is not None and child.returncode==0 and error is None and peak==27 and len(workers)==24 and cleaned
    result=dict(status='POOL24_LIFECYCLE_OBSERVED' if passed else 'POOL24_LIFECYCLE_FAILED',
        started_utc=start,finished_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.monotonic()-wall,
        children_cpu_seconds=end.ru_utime+end.ru_stime-usage.ru_utime-usage.ru_stime,
        peak_observed_processes_including_supervisor=peak,worker_pids=workers,cleanup_confirmed=cleaned,
        snapshots=snapshots,error=error,returncode=child.returncode if child else None,
        cleanup_helper_file_sha256=sha(CODE/'run_controlled.py'),script_sha256=sha(Path(__file__)),
        log_sha256=sha(out/'PROCESS.log'),scope='Observed fixture and fixed topology; not a kernel-enforced process hardcap or proof about arbitrary native code',
        scientific_runs=0,gate_changed=False)
    publish_new(out/'RESULT.json',result)
    print(json.dumps({k:result[k] for k in ('status','peak_observed_processes_including_supervisor','cleanup_confirmed','wall_seconds')}))
    if not passed:raise SystemExit(2)
if __name__=='__main__':main()
