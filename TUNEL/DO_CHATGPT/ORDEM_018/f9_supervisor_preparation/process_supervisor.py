"""Prepared one-child POSIX supervisor, fixed stdlib qualification worker.

No preparation grants execution. New operator/ROOT decision and pinned plan
are required. Q02 native science is explicitly refused before durable claim.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time

# Fixed sibling sources: a future caller pins the complete preparation before
# invoking this entry point. The entry point rechecks those bytes in preflight.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from posix_protocol import (ProtectedDirectory, Refusal, absolute, bounded_error,
    canonical, digest, document, exact, kill_exact, need, pinned, positive_integer,
    proc_identity, read_bytes, same_process, sha)

PREPARATION_ID = 'f7e2ffb8-6efb-4d0d-85c1-59c7a8f932bc'
PACKAGE = Path(__file__).resolve().parent
FLAGS = ['-I', '-S', '-B', '-X', 'utf8']
ENV = {'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1',
       'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1',
       'NUMEXPR_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','OMP_DYNAMIC':'FALSE'}

def preflight(plan_raw, decision_raw, plan_sha, decision_sha):
    need(os.name == 'posix' and os.geteuid() != 0, 'NONROOT_POSIX_ONLY')
    need(sha(plan_raw) == digest(plan_sha) and sha(decision_raw) == digest(decision_sha), 'EXTERNAL_PINS')
    plan, decision = document(plan_raw), document(decision_raw)
    exact(plan, ('schema','preparation_request_id','execution_unit_id','mode','behavior',
        'expected_outcome','python_executable','python_target','runtime_pins','package_pins',
        'qualification_root','root_binding_reference','limits','review_path','review_pin'))
    exact(decision, ('schema','preparation_request_id','execution_unit_id','plan_sha256',
        'scope','authorize_single_execution','review_sha256','root_binding_sha256'))
    need(plan['schema'] == 'F9_POSIX_PROCESS_PLAN_V1' and
         decision['schema'] == 'F9_POSIX_PROCESS_ROOT_DECISION_V1', 'SCHEMA')
    need(plan['preparation_request_id'] == decision['preparation_request_id'] == PREPARATION_ID, 'PREPARATION_ID')
    unit = plan['execution_unit_id']
    need(type(unit) is str and 0 < len(unit) <= 128 and unit != PREPARATION_ID and
         decision['execution_unit_id'] == unit, 'NEW_UNIT_REQUIRED')
    need(decision['plan_sha256'] == plan_sha and decision['authorize_single_execution'] is True and
         decision['scope'] == 'F9_POSIX_STDLIB_PROCESS_QUALIFICATION_ONLY', 'SPECIFIC_DECISION_REQUIRED')
    # No flag can upgrade this scope to universal native IO isolation or science.
    need(plan['mode'] == 'STDLIB_PROCESS_QUALIFICATION', 'Q02_NATIVE_POLICY_AND_CONTROLLER_BINDING_OPEN')
    need(plan['behavior'] in ('RETURN','WAIT_FOR_KILL','OUTPUT_OVERFLOW'), 'FIXED_BEHAVIOR_ONLY')
    expected = {'RETURN':'PASS','WAIT_FOR_KILL':'WORK_DEADLINE','OUTPUT_OVERFLOW':'OUTPUT_OVERFLOW'}
    need(plan['expected_outcome'] == expected[plan['behavior']], 'EXPECTED_OUTCOME_FROZEN')
    exact(plan['limits'], ('work_seconds','total_seconds','max_stdout_bytes','max_stderr_bytes',
        'max_record_bytes','address_space_bytes','cpu_seconds','file_size_bytes','open_files'))
    lim = plan['limits']
    for key in lim:
        positive_integer(lim[key], key)
    need(lim['work_seconds'] < lim['total_seconds'], 'CLEANUP_RESERVE_REQUIRED')
    need(lim['open_files'] >= 16 and lim['max_stdout_bytes'] >= 4096 and
         lim['max_stderr_bytes'] >= 1024 and lim['max_record_bytes'] >= 8192, 'MINIMUM_PROTOCOL_CAPS')
    need(len(plan_raw)<=lim['max_record_bytes'] and len(decision_raw)<=lim['max_record_bytes'],
         'PLAN_AND_DECISION_PUBLICATION_CAP')
    need(lim['file_size_bytes']>=lim['max_record_bytes'],'RLIMIT_FSIZE_RECORD_RESERVE')
    need(hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal'), 'PIDFD_REQUIRED')
    fd = os.pidfd_open(os.getpid(), 0)
    os.close(fd)
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, 'ISOLATED_NO_SITE_NO_BYTECODE')
    need(str(Path(sys.executable).resolve(strict=True)) == absolute(plan['python_target']), 'CURRENT_INTERPRETER_TARGET')
    need(str(Path(absolute(plan['python_executable'])).resolve(strict=True)) == plan['python_target'], 'CHILD_INTERPRETER_TARGET')
    expected_names = {'posix_protocol.py','process_supervisor.py','qualification_child.py',
                      'cooperative_policy.py','audit_guard.py','supervisor_adapter.py','supervisor_port.py'}
    need(set(plan['package_pins']) == expected_names, 'EXACT_PACKAGE_MODULES')
    for name, item in plan['package_pins'].items():
        pinned(str(PACKAGE/name), item, lim['max_record_bytes'] * 16)
    need(type(plan['runtime_pins']) is list and plan['runtime_pins'], 'RUNTIME_CLOSURE_REQUIRED')
    runtime_paths = []
    for item in plan['runtime_pins']:
        exact(item, ('path','bytes','sha256'))
        path = absolute(item['path']); runtime_paths.append(path)
        pinned(path, {k:item[k] for k in ('bytes','sha256')}, max(item['bytes'],1))
    need(len(set(runtime_paths)) == len(runtime_paths) and plan['python_target'] in runtime_paths,
         'UNIQUE_RUNTIME_AND_INTERPRETER_PIN')
    review_raw = pinned(absolute(plan['review_path']),plan['review_pin'],lim['max_record_bytes'])
    review = document(review_raw)
    need(sha(review_raw) == decision['review_sha256'] and review.get('target_preparation_request_id') == PREPARATION_ID and
         review.get('status') == 'INDEPENDENT_STATIC_REVIEW_ACCEPTED', 'INDEPENDENT_REVIEW_REQUIRED')
    binding = plan['root_binding_reference']; exact(binding, ('path','bytes','sha256'))
    binding_raw = pinned(absolute(binding['path']), {k:binding[k] for k in ('bytes','sha256')},lim['max_record_bytes'])
    bound = document(binding_raw)
    need(sha(binding_raw) == decision['root_binding_sha256'] and
         bound.get('schema') == 'F9_PROTECTED_ROOT_BINDING_V1' and
         bound.get('execution_unit_id') == unit and bound.get('qualification_root') == plan['qualification_root'],
         'STABLE_UNIT_ROOT_BINDING_REQUIRED')
    # This is an operational trust boundary, not a cryptographic ROOT signature.
    # The trusted caller supplies original decision/plan digests; it must keep
    # that decision and stable-root registry outside candidate write privileges.
    root = ProtectedDirectory(absolute(plan['qualification_root']))
    return plan, root

def capture(process, work_deadline, caps):
    selector = selectors.DefaultSelector()
    buffers = {name:bytearray() for name in ('stdout','stderr')}
    try:
        for name in buffers:
            stream = getattr(process,name)
            os.set_blocking(stream.fileno(),False)
            selector.register(stream,selectors.EVENT_READ,name)
        while selector.get_map() or process.poll() is None:
            if time.monotonic() >= work_deadline:
                return buffers, 'WORK_DEADLINE'
            for key,_ in selector.select(min(.05,max(0,work_deadline-time.monotonic()))):
                chunk = os.read(key.fileobj.fileno(),4096)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                room = caps[key.data] - len(buffers[key.data])
                buffers[key.data].extend(chunk[:max(0,room)])
                if len(chunk) > room:
                    return buffers, 'OUTPUT_OVERFLOW'
        return buffers, 'EXITED'
    finally:
        selector.close()

def execute_once(plan_raw, decision_raw, *, plan_sha256, decision_sha256):
    plan, root = preflight(plan_raw,decision_raw,plan_sha256,decision_sha256)
    lim = plan['limits']; unit = plan['execution_unit_id']
    nonce = os.urandom(16).hex()
    parent = proc_identity(os.getpid())
    # Stable-root + unit-only key prevents changed plan/decision from reopening
    # the same execution identity. This directory is never deleted or reused.
    run = root.reserve('unit_' + sha(unit.encode('utf-8')))
    process = None; pidfd = None; expected_child = None
    started = time.monotonic(); total = started + lim['total_seconds']
    work = started + lim['work_seconds']; streams = None; error = None
    status = 'FAILED'; outcome = None; reaped = False; killed = False
    try:
        launch = {'schema':'F9_POSIX_LAUNCH_CLAIM_V1','execution_unit_id':unit,'nonce':nonce,
            'parent':parent,'plan_sha256':plan_sha256,'decision_sha256':decision_sha256,
            'started_monotonic':started,'work_deadline':work,'total_deadline':total,'retry_allowed':False}
        run.publish('launch.json',canonical(launch),lim['max_record_bytes'])
        run.publish('plan.json',plan_raw,lim['max_record_bytes'])
        run.publish('decision.json',decision_raw,lim['max_record_bytes'])
        need(time.monotonic() < work,'EXPIRED_BEFORE_LAUNCH')
        argv = [plan['python_executable'],*FLAGS,str(PACKAGE/'qualification_child.py'),
                '--run-root',run.path,'--nonce',nonce,'--plan-sha256',plan_sha256,
                '--decision-sha256',decision_sha256]
        process = subprocess.Popen(argv,cwd=str(PACKAGE),env=dict(ENV),stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True,start_new_session=True)
        pidfd = os.pidfd_open(process.pid,0)
        expected_child = proc_identity(process.pid)
        need(expected_child['argv'] == argv and expected_child['exe'] == plan['python_target'] and
             expected_child['ppid'] == parent['pid'], 'CHILD_IDENTITY_AFTER_LAUNCH')
        run.publish('child_identity.json',canonical({'nonce':nonce,'process':expected_child}),lim['max_record_bytes'])
        # Child waits for GO before its claim, hooks or qualification behavior.
        process.stdin.write(b'GO '+nonce.encode('ascii')+b'\n');process.stdin.flush();process.stdin.close()
        streams,outcome = capture(process,work,{'stdout':lim['max_stdout_bytes'],'stderr':lim['max_stderr_bytes']})
        if process.poll() is None:
            need(time.monotonic() < total,'CLEANUP_BUDGET_EXHAUSTED')
            kill_exact(pidfd,expected_child);killed=True
        remaining = total-time.monotonic()
        need(remaining > 0,'REAP_BUDGET_EXHAUSTED')
        process.wait(timeout=remaining);reaped=True
        if outcome == 'EXITED':
            need(process.returncode == 0 and not streams['stderr'],'CHILD_EXIT_OR_STDERR')
            child = document(bytes(streams['stdout']))
            child_raw = read_bytes(run.path+'/child_result.pending',lim['max_record_bytes'])
            need(document(child_raw) == child,'STDOUT_PERSISTED_RESULT_MISMATCH')
            need(child['execution_unit_id'] == unit and child['nonce'] == nonce and
                 same_process(child['process'],expected_child) and same_process(child['parent'],parent),
                 'CHILD_TERMINAL_IDENTITY')
            need(child['status'] == 'STDLIB_PROBE_RETURNED' and child['scientific_imports'] == 0 and
                 child['observed_reads'] is False and child['audit']['latched'] is False and
                 child['audit']['denial_count'] == 0 and child['audit']['journal_error'] is None,
                 'CHILD_AUDIT_REJECTED')
            need(child['audit']['installed'] is True and
                 child['policy']['scope']=='PYTHON_AUDIT_EVENTS_COOPERATIVE_ONLY' and
                 child['policy']['native_network_operations'] is None and
                 child['policy']['native_file_operations'] is None,'COOPERATIVE_SCOPE_ONLY')
            run.publish('child_result.json',child_raw,lim['max_record_bytes'])
            outcome='PASS'
        ready_raw=read_bytes(run.path+'/child_ready.pending',lim['max_record_bytes'])
        ready=document(ready_raw)
        need(ready['schema']=='F9_POSIX_CHILD_READY_V1' and ready['nonce']==nonce and
             ready['execution_unit_id']==unit and ready['behavior']==plan['behavior'] and
             same_process(ready['process'],expected_child),'BEHAVIOR_NOT_REACHED_OR_WRONG_IDENTITY')
        snap=ready['policy']['snapshot']
        need(snap['installed'] is True and snap['latched'] is False and snap['denial_count']==0 and
             snap['journal_error'] is None,'READY_AUDIT_FAILED')
        need(read_bytes(run.path+'/audit_journal.jsonl',lim['max_record_bytes'])==b'',
             'PHYSICAL_AUDIT_JOURNAL_NONEMPTY')
        # Compare symbolic names: no numeric Linux ABI constants are assumed.
        need(ready['limits_by_name']=={'RLIMIT_AS':[lim['address_space_bytes']]*2,
             'RLIMIT_CPU':[lim['cpu_seconds']]*2,'RLIMIT_FSIZE':[lim['file_size_bytes']]*2,
             'RLIMIT_NOFILE':[lim['open_files']]*2,'RLIMIT_CORE':[0,0]},'CHILD_RLIMIT_RECEIPT')
        run.publish('child_ready.json',ready_raw,lim['max_record_bytes'])
        need(outcome == plan['expected_outcome'],'UNEXPECTED_FROZEN_OUTCOME')
        status='QUALIFICATION_CASE_MATCHED_EXPECTATION'
    except BaseException as exc:
        error=bounded_error(exc)
    finally:
        if process is not None and not reaped:
            try:
                if process.poll() is None:
                    need(pidfd is not None and expected_child is not None,'UNBOUND_CHILD_CLEANUP_UNCERTAIN')
                    kill_exact(pidfd,expected_child);killed=True
                remaining=total-time.monotonic()
                need(remaining>0,'REAP_BUDGET_EXHAUSTED')
                process.wait(timeout=remaining);reaped=True
            except BaseException as exc:
                status='PROCESS_STATE_UNCERTAIN_NO_RETRY';error=bounded_error(exc)
        if pidfd is not None:
            os.close(pidfd)
        if process is not None:
            for name in ('stdin','stdout','stderr'):
                stream=getattr(process,name)
                if stream is not None and not stream.closed:
                    stream.close()
    if not reaped or time.monotonic() >= total:
        status='PROCESS_OR_FINALIZATION_INCOMPLETE_NO_RETRY'
    record={'schema':'F9_POSIX_SUPERVISION_RESULT_V1','execution_unit_id':unit,'nonce':nonce,
        'status':status,'expected_outcome':plan['expected_outcome'],'observed_outcome':outcome,
        'parent':parent,'child':expected_child,'returncode':None if process is None else process.returncode,
        'child_reaped':reaped,'kill_requested':killed,'plan_sha256':plan_sha256,'decision_sha256':decision_sha256,
        'stdout_sha256':None if streams is None else sha(bytes(streams['stdout'])),
        'stderr_sha256':None if streams is None else sha(bytes(streams['stderr'])),
        'retained_bytes':None if streams is None else {k:len(v) for k,v in streams.items()},
        'error':error,'wall_before_terminal_persistence':time.monotonic()-started,
        'nominal_total_seconds':lim['total_seconds'],'total_deadline_monotonic':total,'OS_deadline_guarantee':False,
        'native_IO_isolation':False,'descendant_OS_containment':False,'automatic_retry':False,
        'scientific_execution':False,'pending_external_exit_and_receipt_check':True}
    try:
        run.publish('terminal.json',canonical(record),lim['max_record_bytes'])
        if time.monotonic() >= total:
            run.publish('finalization_failure.json',canonical({'reason':'AFTER_TERMINAL_DEADLINE','nonce':nonce}),lim['max_record_bytes'])
            raise Refusal('TERMINAL_DEADLINE_EXCEEDED')
        return record
    finally:
        run.close();root.close()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute-reviewed-once',action='store_true')
    parser.add_argument('--plan');parser.add_argument('--decision')
    parser.add_argument('--plan-sha256');parser.add_argument('--decision-sha256')
    args=parser.parse_args()
    need(args.execute_reviewed_once,'PREPARATION_ONLY_NO_EXECUTION_SWITCH')
    need(all((args.plan,args.decision,args.plan_sha256,args.decision_sha256)), 'ALL_EXTERNAL_INPUTS_REQUIRED')
    result=execute_once(read_bytes(args.plan,2*1024*1024),read_bytes(args.decision,65536),
        plan_sha256=args.plan_sha256,decision_sha256=args.decision_sha256)
    print(json.dumps(result,sort_keys=True),flush=True)
    # Terminal print itself remains part of the nominal interval: the external
    # caller must check exit0 and terminal receipt, not infer from a printed PASS.
    need(time.monotonic()<result['total_deadline_monotonic'],'STDOUT_FINALIZATION_DEADLINE_EXCEEDED')
    return 0 if result['status']=='QUALIFICATION_CASE_MATCHED_EXPECTATION' else 1

if __name__=='__main__':
    try:
        sys.exit(main())
    except BaseException as exc:
        if isinstance(exc,SystemExit):
            raise
        print(json.dumps({'status':'REFUSED_OR_FAILED_NO_RETRY','error':bounded_error(exc)}),flush=True)
        sys.exit(2)
