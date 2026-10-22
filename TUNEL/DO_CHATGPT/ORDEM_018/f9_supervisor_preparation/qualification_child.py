"""Fixed stdlib process probe, preparation only. Never imports science."""
import argparse
import json
import os
from pathlib import Path
import resource
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from posix_protocol import (ProtectedDirectory, canonical, document, need, pinned,
    proc_identity, read_bytes, same_process, sha)
from cooperative_policy import CooperativePolicy

PACKAGE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-root',required=True);parser.add_argument('--nonce',required=True)
    parser.add_argument('--plan-sha256',required=True);parser.add_argument('--decision-sha256',required=True)
    args=parser.parse_args()
    need(len(args.nonce)==32 and all(c in '0123456789abcdef' for c in args.nonce),'NONCE')
    run=ProtectedDirectory(args.run_root)
    plan_raw=read_bytes(run.path+'/plan.json',2*1024*1024)
    decision_raw=read_bytes(run.path+'/decision.json',65536)
    need(sha(plan_raw)==args.plan_sha256 and sha(decision_raw)==args.decision_sha256,'INPUT_PINS')
    plan,decision=document(plan_raw),document(decision_raw)
    launch=document(read_bytes(run.path+'/launch.json',65536))
    # Wait for a single parent GO. EOF or wrong nonce never starts the probe.
    need(sys.stdin.buffer.readline(128)==b'GO '+args.nonce.encode('ascii')+b'\n','PARENT_GO_REQUIRED')
    child_record=document(read_bytes(run.path+'/child_identity.json',65536))
    me=proc_identity(os.getpid());parent=proc_identity(os.getppid())
    need(launch['nonce']==child_record['nonce']==args.nonce and
         same_process(me,child_record['process']) and same_process(parent,launch['parent']), 'INCARNATION_BINDING')
    need(launch['plan_sha256']==args.plan_sha256 and launch['decision_sha256']==args.decision_sha256 and
         plan['mode']=='STDLIB_PROCESS_QUALIFICATION' and
         decision['scope']=='F9_POSIX_STDLIB_PROCESS_QUALIFICATION_ONLY' and
         decision['authorize_single_execution'] is True and
         decision['execution_unit_id']==launch['execution_unit_id']==plan['execution_unit_id'], 'EXACT_SCOPE')
    lim=plan['limits'];need(time.monotonic()<launch['work_deadline'],'EXPIRED_BEFORE_CHILD_CLAIM')
    run.publish('child_claim.json',canonical({'nonce':args.nonce,'process':me,'parent':parent,
        'execution_unit_id':plan['execution_unit_id'],'automatic_retry':False}),lim['max_record_bytes'])
    caps={resource.RLIMIT_AS:lim['address_space_bytes'],resource.RLIMIT_CPU:lim['cpu_seconds'],
          resource.RLIMIT_FSIZE:lim['file_size_bytes'],resource.RLIMIT_NOFILE:lim['open_files'],resource.RLIMIT_CORE:0}
    for key,value in caps.items():
        resource.setrlimit(key,(value,value))
        need(resource.getrlimit(key)==(value,value),'RLIMIT_NOT_INSTALLED')
    reads={item['path']:{k:item[k] for k in ('bytes','sha256')} for item in plan['runtime_pins']}
    reads.update({str(PACKAGE/name):item for name,item in plan['package_pins'].items()})
    for path,item in reads.items():
        pinned(path,item,max(item['bytes'],1))
    # Staging descriptors are not authoritative records. Parent validates and
    # atomically publishes their final names after child termination.
    output=os.open(run.path+'/child_result.pending',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    ready_fd=os.open(run.path+'/child_ready.pending',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    policy=CooperativePolicy(read_pins=reads,journal_path=run.path+'/audit_journal.jsonl',
        output_fds={output,ready_fd,1,2},deadline=launch['work_deadline'])
    policy.install();policy.verify_loaded_modules()
    need(not any(n=='numpy' or n=='camb' or n.startswith(('numpy.','camb.','scipy.')) for n in sys.modules),
         'SCIENTIFIC_IMPORT_IN_STDLIB_PROBE')
    ready=canonical({'schema':'F9_POSIX_CHILD_READY_V1','nonce':args.nonce,
        'execution_unit_id':plan['execution_unit_id'],'behavior':plan['behavior'],
        'process':me,'policy':policy.receipt(),'limits_installed':{str(k):list(resource.getrlimit(k)) for k in caps},
        'limits_by_name':{n:list(resource.getrlimit(getattr(resource,n))) for n in
            ('RLIMIT_AS','RLIMIT_CPU','RLIMIT_FSIZE','RLIMIT_NOFILE','RLIMIT_CORE')}})
    need(len(ready)<=lim['max_record_bytes'],'READY_RECORD_CAP')
    view=memoryview(ready)
    while view:
        n=os.write(ready_fd,view);need(n>0,'READY_SHORT_WRITE');view=view[n:]
    os.fsync(ready_fd);os.fsync(run.fd)
    if plan['behavior']=='WAIT_FOR_KILL':
        # Deliberately no cooperative checkpoint: qualifies external termination
        # without invoking a solver. Parent deadline and hard CPU cap remain.
        while True:
            time.sleep(1)
    if plan['behavior']=='OUTPUT_OVERFLOW':
        # Stream a fixed block until the parent detects its frozen cap and kills.
        while True:
            os.write(1,b'x'*4096)
    need(plan['behavior']=='RETURN','UNKNOWN_BEHAVIOR')
    policy.checkpoint('BEFORE_RESULT')
    policy_receipt=policy.receipt()
    usage=resource.getrusage(resource.RUSAGE_SELF)
    result={'schema':'F9_POSIX_STDLIB_CHILD_RESULT_V1','execution_unit_id':plan['execution_unit_id'],
        'nonce':args.nonce,'process':me,'parent':parent,'status':'STDLIB_PROBE_RETURNED',
        'scientific_imports':0,'observed_reads':False,'audit':policy_receipt['snapshot'],
        'policy':policy_receipt,'limits_installed':{str(k):list(resource.getrlimit(k)) for k in caps},
        'measurements':{'user_cpu_s':usage.ru_utime,'system_cpu_s':usage.ru_stime,
                        'peak_RSS_native_units':usage.ru_maxrss,'RSS_units':'Linux KiB; AS cap is virtual address space'},
        'no_new_children_claim_scope':'No subprocess/fork in fixed trusted source; Python audit only',
        'physical_certification':False}
    raw=canonical(result)
    need(len(raw)<=lim['max_record_bytes'],'CHILD_RESULT_CAP')
    view=memoryview(raw)
    while view:
        n=os.write(output,view);need(n>0,'CHILD_SHORT_WRITE');view=view[n:]
    os.fsync(output);os.fsync(run.fd)
    policy.checkpoint('AFTER_RESULT_PERSISTENCE')
    os.write(1,raw)
    policy.checkpoint('AFTER_STDOUT')
    return 0

if __name__=='__main__':
    try:
        sys.exit(main())
    except BaseException as exc:
        if isinstance(exc,SystemExit):
            raise
        # Never return a success record on swallowed audit/IO/timeout failure.
        print(json.dumps({'status':'CHILD_FAILED_NO_RETRY','type':type(exc).__name__,
                          'message':str(exc)[:1000]}),file=sys.stderr,flush=True)
        sys.exit(2)
