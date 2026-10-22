"""Budgeted T04 branch-C supervisor; original pilot supervisor remains untouched."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,time,signal,subprocess,resource,argparse,math
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


def qualify_records(lines,items):
    labels=[item['label'] for item in items]
    if len(labels)!=400 or len(set(labels))!=400 or len(lines)!=801:
        return False,'COUNTS_OR_LABELS_DIFFER'
    for i,label in enumerate(labels):
        pre,ret=lines[2*i:2*i+2]
        if pre.get('precall')!=label or ret.get('return_label')!=label:
            return False,'PRECALL_RETURN_IDENTITY_OR_ORDER_DIFFERS'
        if ret.get('status')!='FINITE_WAVEFORM' or ret.get('error') is not None:
            return False,'NONFINITE_OR_ERROR_RETURN'
        wall=ret.get('wall_seconds')
        if isinstance(wall,bool) or not isinstance(wall,(float,int)) or not math.isfinite(wall) or wall<0:
            return False,'INVALID_CALL_TIME'
    summary=lines[-1]
    if summary.get('summary') is not True or summary.get('source_calls')!=400 or summary.get('edom')!=0:
        return False,'SUMMARY_COUNTERS_DIFFER'
    return True,'EXACT_400_ORDERED_PAIRS_AND_COUNTERS'

def pilot_status(rc,fault,stopped,receipt,digest,job):
    if not isinstance(receipt,dict):return 'T04_CONTROLLER_RECEIPT_MISSING',False
    if receipt.get('registration_sha256')!=digest or receipt.get('job')!=job:
        return 'T04_CONTROLLER_IDENTITY_MISMATCH',False
    if receipt.get('cleanup',{}).get('group_absent') is not True:
        return 'T04_CLEANUP_UNCONFIRMED',False
    if stopped or receipt.get('status')=='BUDGET_STOPPED_PARTIAL_NOT_POSTERIOR':
        return 'T04_BUDGET_STOPPED_PARTIAL',True
    if rc!=0 or fault is not None or receipt.get('status')!='CHILD_COMPLETED_REQUIRES_REVIEW':
        return 'T04_FAILED_OR_PARTIAL_REQUIRES_BRANCH_REVIEW',True
    return 'T04_PILOT_FINISHED_REQUIRES_REVIEW',True

def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['branch_c']);args=parser.parse_args()
    nulls=B/'bis/015/nulls_campaign_001/RESULT.json'
    sys.path.insert(0,str(D.parent))
    from t03_terminal_guard import require_terminal
    terminal=require_terminal(D.parent)
    receipts=list((ROOT/'TUNEL/PARA_CHATGPT').glob('RECIBO_016_FECHAMENTO_PARCIAL*.md'))
    management_receipt_sha256=None
    if receipts:
        assert len(receipts)==1 and receipts[0].name=='RECIBO_016_FECHAMENTO_PARCIAL.md','Unknown priority management receipt'
        management_receipt_sha256=sha(receipts[0])
        assert management_receipt_sha256=='26bed47e51d4982609432425dde5ce973683f9bfed6379ea58fa499295577bcb','Management receipt changed'
        message=receipts[0].read_text(encoding='utf-8-sig')
        assert 'não pede correção' in message and 'Nenhuma correção deste recibo passa na frente dela.' in message,'Management correction requires review'
    reg,digest=checked_registration();view=load_authorized_configuration(reg,digest)
    branch_job='GW250114_PILOT_V2_S220_C1'
    cfg=view['pe_jobs'][branch_job];assert cfg['mode']=='calibration'
    allocation=max(B.glob('ORCAMENTO_015_v*.json'),key=lambda p:int(p.stem.rsplit('v',1)[1]));a=json.loads(allocation.read_bytes());assert view['_allocation_sha256']==sha(allocation)
    item='T04_branch_C'
    cap=next(v['allocated_machine_hours'] for v in a['items'] if v['item']==item)*3600
    run=D/args.stage;assert not run.exists(),'Branch C already reserved; inspect instead of retry'
    if args.stage=='qualify':
        plan=json.loads((D/'QUALIFICATION_PLAN.json').read_bytes())
        assert plan['registration_sha256']==digest
        assert plan['job_sha256']==sha(D/'QUALIFICATION_JOB.json')
        assert plan['child_sha256']==sha(D/'qualification_child.py')
        probe=overflow_probe(cfg)
        command=[sys.executable,'-B',str(D/'qualification_child.py'),str(D/'QUALIFICATION_JOB.json'),str(run/'CALLS.jsonl')]
    else:
        q=json.loads((D/'qualify/RESULT.json').read_bytes())
        assert q['status']=='T04_ADAPTER_400_QUALIFIED' and q['registration_sha256']==digest
        assert q['child_sha256']==sha(D/'qualification_child.py')
        assert not (B/'cache'/cfg['output_directory_name']).exists(),'Never retry existing branch'
        assert cfg['wall_budget_seconds']<=cap,'Controller hard cap exceeds allocated hours'
        assert cfg['sampler']['workers']==24,'This supervisor is scoped to the registered24-worker pilot'
        command=[sys.executable,'-B',str(CODE/'run_controlled.py'),'--job',branch_job]
    run.mkdir(exist_ok=False)
    start=utc();mono=time.monotonic();usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    publish_new(run/'PLAN.json',dict(start_utc=start,stage=args.stage,command=command,allocation_sha256=sha(allocation),
        registration_sha256=digest,allocated_seconds=cap,script_sha256=sha(Path(__file__)),blind=False,
        T03_terminal=terminal,T03_terminal_guard_sha256=sha(D.parent/'t03_terminal_guard.py'),
        management_receipt_sha256=management_receipt_sha256))
    if args.stage=='qualify':publish_new(run/'OVERFLOW.json',probe)
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
        try:
            lines=[json.loads(s) for s in (run/'CALLS.jsonl').read_text().splitlines()]
            qualified,diagnostic=qualify_records(lines,json.loads((D/'QUALIFICATION_JOB.json').read_bytes())['items'])
        except (ValueError,KeyError,TypeError,OSError) as exc:
            lines=[];qualified=False;diagnostic=type(exc).__name__+':'+str(exc)
        returns=[r for r in lines if 'return_label' in r]
        passed=(result['returncode']==0 and qualified and not stopped and fault is None)
        result.update(status='T04_ADAPTER_400_QUALIFIED' if passed else 'T04_ADAPTER_400_FAILED',returned=len(returns),
            finite=sum(r.get('status')=='FINITE_WAVEFORM' for r in returns),qualification_diagnostic=diagnostic,child_sha256=sha(D/'qualification_child.py'),
            failures=[r for r in returns if r.get('status')!='FINITE_WAVEFORM'])
    else:
        receipt=B/'cache'/cfg['output_directory_name']/'CONTROLLER.json'
        try:cr=json.loads(receipt.read_bytes())
        except (ValueError,OSError):cr=None
        classification,clean=pilot_status(result['returncode'],fault,stopped,cr,digest,branch_job)
        result.update(status=classification,cleanup_confirmed=clean,
            controller_receipt_sha256=sha(receipt) if receipt.exists() else None,controller_receipt=cr,
            next_job_forbidden_until_cleanup_confirmed=not clean,review_required_before_any_posterior_claim=True)
    publish_new(run/'RESULT.json',result)
    print(json.dumps({k:result[k] for k in ('status','returncode','wall_seconds','children_cpu_seconds','fault')}),flush=True)
    if result['status'] not in ('T04_ADAPTER_400_QUALIFIED','T04_PILOT_FINISHED_REQUIRES_REVIEW'):raise SystemExit(2)
if __name__=='__main__':main()
