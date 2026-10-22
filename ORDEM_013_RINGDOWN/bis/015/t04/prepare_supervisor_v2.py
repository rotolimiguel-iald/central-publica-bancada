"""Add a corrected supervisor beside the statically reviewed, immutable v1."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,hashlib
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    with p.open('xb') as f:f.write(raw)

def main():
    old=D/'supervise_t04.py';s=old.read_text();review=D/'review/T04_LOCAL_STATIC_REVIEW.json'
    assert sha(old)==json.loads(review.read_bytes())['files_sha256']['supervise_t04.py']
    s=s.replace('import os,sys,json,time,signal,subprocess,resource,argparse','import os,sys,json,time,signal,subprocess,resource,argparse,math')
    helper='''
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

'''
    s=s.replace('def main():',helper+'def main():')
    s=s.replace("allocation=B/'ORCAMENTO_015_v1.json';a=json.loads(allocation.read_bytes());assert view['_allocation_sha256']==sha(allocation)",
      "allocation=max(B.glob('ORCAMENTO_015_v*.json'),key=lambda p:int(p.stem.rsplit('v',1)[1]));a=json.loads(allocation.read_bytes());assert view['_allocation_sha256']==sha(allocation)")
    s=s.replace("run=D/args.stage;run.mkdir(exist_ok=False)","run=D/args.stage;assert not run.exists(),'Stage already reserved; inspect instead of retry'")
    s=s.replace("probe=overflow_probe(cfg);publish_new(run/'OVERFLOW.json',probe)","probe=overflow_probe(cfg)")
    s=s.replace("assert not (B/'cache'/cfg['output_directory_name']).exists(),'Never retry existing pilot'",
      "assert not (B/'cache'/cfg['output_directory_name']).exists(),'Never retry existing pilot'\n        assert cfg['wall_budget_seconds']<=cap,'Controller hard cap exceeds allocated hours'\n        assert cfg['sampler']['workers']==24,'This supervisor is scoped to the registered24-worker pilot'")
    s=s.replace("start=utc();mono=time.monotonic();usage=resource.getrusage(resource.RUSAGE_CHILDREN)",
      "run.mkdir(exist_ok=False)\n    start=utc();mono=time.monotonic();usage=resource.getrusage(resource.RUSAGE_CHILDREN)")
    s=s.replace("stream=(run/'PROCESS.log').open('xb');child=None;fault=None;stopped=False;snapshots=[]",
      "if args.stage=='qualify':publish_new(run/'OVERFLOW.json',probe)\n    stream=(run/'PROCESS.log').open('xb');child=None;fault=None;stopped=False;snapshots=[]")
    s=s.replace("lines=[json.loads(s) for s in (run/'CALLS.jsonl').read_text().splitlines()] if (run/'CALLS.jsonl').exists() else []",
      "try:\n            lines=[json.loads(s) for s in (run/'CALLS.jsonl').read_text().splitlines()]\n            qualified,diagnostic=qualify_records(lines,json.loads((D/'QUALIFICATION_JOB.json').read_bytes())['items'])\n        except (ValueError,KeyError,TypeError,OSError) as exc:\n            lines=[];qualified=False;diagnostic=type(exc).__name__+':'+str(exc)")
    s=s.replace("passed=(result['returncode']==0 and len(returns)==400 and all(r['status']=='FINITE_WAVEFORM' for r in returns) and not stopped and fault is None)",
      "passed=(result['returncode']==0 and qualified and not stopped and fault is None)")
    s=s.replace("finite=sum(r['status']=='FINITE_WAVEFORM' for r in returns),child_sha256=sha(D/'qualification_child.py'),",
      "finite=sum(r.get('status')=='FINITE_WAVEFORM' for r in returns),qualification_diagnostic=diagnostic,child_sha256=sha(D/'qualification_child.py'),")
    s=s.replace("failures=[r for r in returns if r['status']!='FINITE_WAVEFORM'])", "failures=[r for r in returns if r.get('status')!='FINITE_WAVEFORM'])")
    prior="""result.update(status='T04_PILOT_FINISHED_REQUIRES_REVIEW',controller_receipt_sha256=sha(receipt) if receipt.exists() else None,
            controller_receipt=json.loads(receipt.read_bytes()) if receipt.exists() else None,
            review_required_before_any_posterior_claim=True)"""
    replacement="""try:cr=json.loads(receipt.read_bytes())
        except (ValueError,OSError):cr=None
        classification,clean=pilot_status(result['returncode'],fault,stopped,cr,digest,'GW250114_PILOT_V2_S220')
        result.update(status=classification,cleanup_confirmed=clean,
            controller_receipt_sha256=sha(receipt) if receipt.exists() else None,controller_receipt=cr,
            next_job_forbidden_until_cleanup_confirmed=not clean,review_required_before_any_posterior_claim=True)"""
    assert prior in s;s=s.replace(prior,replacement)
    s=s.replace("if result['returncode']!=0 or fault or stopped:raise SystemExit(2)",
      "if result['status'] not in ('T04_ADAPTER_400_QUALIFIED','T04_PILOT_FINISHED_REQUIRES_REVIEW'):raise SystemExit(2)")
    ast.parse(s)
    target=D/'supervise_t04_v2.py';new(target,s.encode())
    new(D/'SUPERVISOR_V2_PREPARED.json',(json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),
        supersedes_sha256=sha(old),review_sha256=sha(review),script_sha256=sha(target),
        scientific_code_changed=False,registered_jobs_changed=False,executed=False,
        still_required=['budget_v2_reserving_controller8h_before_pilot','process_bound_verification','fixture_controls']),indent=2)+'\n').encode())
    print(sha(target))
if __name__=='__main__':main()
