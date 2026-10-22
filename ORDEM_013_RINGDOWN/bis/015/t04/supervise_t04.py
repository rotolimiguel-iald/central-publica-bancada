"""T04 mandatory adapter replication and separately launched budgeted pilot."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,time,signal,subprocess,resource,argparse
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[2];ROOT=B.parent;CODE=B/'bis/e2_code_v1_1_2'
sys.path.insert(0,str(CODE))
from registration_guard import checked_registration,load_authorized_configuration,sha,publish_new

def utc():return datetime.now(timezone.utc).isoformat()
def overflow_probe(cfg):
    import numpy as np
    import pseob_source as source
    import bilby.gw.source as backend
    original=backend.lal_binary_black_hole;calls=[]
    def trap(*a,**kw):calls.append(1);raise AssertionError('Reached native backend')
    backend.lal_binary_black_hole=trap
    params=dict(mass_1=65.,mass_2=50.,luminosity_distance=500.,chi_1=.2,chi_2=-.1,
        theta_jn=1.,phase=.3,dtau220=-.8,dtau440=2.,domega220=0.,domega440=0.,geocent_time=1420878141.2)
    try:
        try:source.pseob_frequency_domain(np.fft.rfftfreq(16*4096,1/4096),**params)
        except ValueError as e:
            assert str(e)=='NATIVE_RINGDOWN_BUFFER_BOUND_REFUSED_BEFORE_LAL'
        else:raise AssertionError('Overflow was accepted')
        assert calls==[]
        return dict(status='OVERFLOW_REJECTED_BEFORE_NATIVE_BACKEND',native_calls=0,source_sha256=sha(CODE/'pseob_source.py'))
    finally:backend.lal_binary_black_hole=original

def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['qualify','pilot']);args=parser.parse_args()
    nulls=B/'bis/015/nulls_campaign_001/RESULT.json'
    assert nulls.exists(),'T03 must finish first'
    assert not list((ROOT/'TUNEL/PARA_CHATGPT').glob('RECIBO_016_FECHAMENTO_PARCIAL*.md')),'Priority management receipt'
    reg,digest=checked_registration();view=load_authorized_configuration(reg,digest)
    cfg=view['pe_jobs']['GW250114_PILOT_V2_S220'];assert cfg['mode']=='calibration'
    allocation=B/'ORCAMENTO_015_v1.json';a=json.loads(allocation.read_bytes());assert view['_allocation_sha256']==sha(allocation)
    item='T04_runner_qualification' if args.stage=='qualify' else 'T04_pilot_220'
    cap=next(v['allocated_machine_hours'] for v in a['items'] if v['item']==item)*3600
    run=D/args.stage;run.mkdir(exist_ok=False)
    if args.stage=='qualify':
        plan=json.loads((D/'QUALIFICATION_PLAN.json').read_bytes())
        assert plan['registration_sha256']==digest
        assert plan['job_sha256']==sha(D/'QUALIFICATION_JOB.json')
        assert plan['child_sha256']==sha(D/'qualification_child.py')
        probe=overflow_probe(cfg);publish_new(run/'OVERFLOW.json',probe)
        command=[sys.executable,'-B',str(D/'qualification_child.py'),str(D/'QUALIFICATION_JOB.json'),str(run/'CALLS.jsonl')]
    else:
        q=json.loads((D/'qualify/RESULT.json').read_bytes())
        assert q['status']=='T04_ADAPTER_400_QUALIFIED' and q['registration_sha256']==digest
        assert q['child_sha256']==sha(D/'qualification_child.py')
        assert not (B/'cache'/cfg['output_directory_name']).exists(),'Never retry existing pilot'
        command=[sys.executable,'-B',str(CODE/'run_controlled.py'),'--job','GW250114_PILOT_V2_S220']
    start=utc();mono=time.monotonic();usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    publish_new(run/'PLAN.json',dict(start_utc=start,stage=args.stage,command=command,allocation_sha256=sha(allocation),
        registration_sha256=digest,allocated_seconds=cap,script_sha256=sha(Path(__file__)),blind=False))
    stream=(run/'PROCESS.log').open('xb');child=None;fault=None;stopped=False;snapshots=[]
    def interrupt(sig,frame):raise InterruptedError('Supervisor interrupted '+str(sig))
    signal.signal(signal.SIGTERM,interrupt);signal.signal(signal.SIGINT,interrupt)
    try:
        child=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True,
            env={**os.environ,**{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS')}})
        publish_new(run/'PROCESS.json',dict(pid=child.pid,start_utc=start,command=command))
        last=-100
        while child.poll() is None:
            elapsed=time.monotonic()-mono
            if elapsed>=cap-25:stopped=True;break
            if elapsed-last>=30:
                # Traverse only our own descendants; no foreign process inspection/termination.
                todo=[child.pid];seen=[]
                while todo:
                    pid=todo.pop()
                    try:
                        info=Path(f'/proc/{pid}/status').read_text()
                        threads=int(next(line.split(':')[1] for line in info.splitlines() if line.startswith('Threads:')))
                        seen.append(dict(pid=pid,threads=threads))
                        todo.extend(int(v) for v in Path(f'/proc/{pid}/task/{pid}/children').read_text().split())
                    except (FileNotFoundError,ProcessLookupError):pass
                snapshot=dict(at=utc(),elapsed_seconds=elapsed,processes=seen,total_with_supervisor=len(seen)+1)
                snapshots.append(snapshot)
                print(json.dumps(dict(stage=args.stage,elapsed_seconds=elapsed,process_count=snapshot['total_with_supervisor'])),flush=True)
                if snapshot['total_with_supervisor']>28:raise RuntimeError('Owned process limit exceeded')
                last=elapsed
            time.sleep(.5)
    except BaseException as e:fault=dict(type=type(e).__name__,message=str(e))
    finally:
        if child is not None and child.poll() is None:
            # SIGTERM lets the registered controller clean its separate runner group.
            child.send_signal(signal.SIGTERM)
            try:child.wait(timeout=18)
            except subprocess.TimeoutExpired:
                fault=dict(type='CLEANUP_UNCONFIRMED',message='Controller did not finish owned-group cleanup in18s')
                child.kill();child.wait()
        stream.close()
    end=resource.getrusage(resource.RUSAGE_CHILDREN)
    result=dict(stage=args.stage,started_utc=start,finished_utc=utc(),returncode=child.returncode if child else None,
        wall_seconds=time.monotonic()-mono,children_cpu_seconds=end.ru_utime+end.ru_stime-usage.ru_utime-usage.ru_stime,
        registration_sha256=digest,allocation_sha256=sha(allocation),budget_stopped=stopped,fault=fault,
        log_sha256=sha(run/'PROCESS.log'),process_snapshots=snapshots,blind=False,gate_changed=False)
    result['machine_hours']=result['wall_seconds']/3600
    if args.stage=='qualify':
        lines=[json.loads(s) for s in (run/'CALLS.jsonl').read_text().splitlines()] if (run/'CALLS.jsonl').exists() else []
        returns=[r for r in lines if 'return_label' in r]
        passed=(result['returncode']==0 and len(returns)==400 and all(r['status']=='FINITE_WAVEFORM' for r in returns) and not stopped and fault is None)
        result.update(status='T04_ADAPTER_400_QUALIFIED' if passed else 'T04_ADAPTER_400_FAILED',returned=len(returns),
            finite=sum(r['status']=='FINITE_WAVEFORM' for r in returns),child_sha256=sha(D/'qualification_child.py'),
            failures=[r for r in returns if r['status']!='FINITE_WAVEFORM'])
    else:
        receipt=B/'cache'/cfg['output_directory_name']/'CONTROLLER.json'
        result.update(status='T04_PILOT_FINISHED_REQUIRES_REVIEW',controller_receipt_sha256=sha(receipt) if receipt.exists() else None,
            controller_receipt=json.loads(receipt.read_bytes()) if receipt.exists() else None,
            review_required_before_any_posterior_claim=True)
    publish_new(run/'RESULT.json',result)
    print(json.dumps({k:result[k] for k in ('status','returncode','wall_seconds','children_cpu_seconds','fault')}),flush=True)
    if result['returncode']!=0 or fault or stopped:raise SystemExit(2)
if __name__=='__main__':main()
