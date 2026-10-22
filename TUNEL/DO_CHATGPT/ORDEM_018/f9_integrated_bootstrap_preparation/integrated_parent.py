"""Prepared fixed POSIX parent for ONE full-family integrated qualification.

Default invocation refuses. Requires separately produced, explicitly pinned ROOT
execution decision, independent review, current inventory and stable root binding.
No runtime, approval or claim is generated during preparation.
"""
import time
ENTRY_MONOTONIC=time.monotonic()  # Before argparse, bundle reads, preflight and imports below.
import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import base64
import selectors
import signal
import subprocess
import uuid
from posix_protocol import canonical, document, exact, need, pinned, read_bytes, sha, ProtectedDirectory, proc_identity, same_process, bounded_error
from deployment_contract import bundle
from native_progress import NativeProgressWindow
from supervisor_port import validate_terminal
from integrated_reference import verify, unpack, store_measurements

NOMINAL_TOTAL_SECONDS=87000
CLEANUP_RESERVE_SECONDS=30


def main(argv):
    need(len(argv)==3,'PREPARATION_ONLY: future deployment path, original ROOT decision path and its exact SHA256 are mandatory')
    deployment_path,decision_path,decision_sha=argv
    deadline=ENTRY_MONOTONIC+NOMINAL_TOTAL_SECONDS;work_deadline=deadline-CLEANUP_RESERVE_SECONDS
    def check():need(time.monotonic()<deadline,'WHOLE_COMMAND_NOMINAL_DEADLINE')
    b=bundle(deployment_path,decision_path,decision_sha,check)
    recipe=b['recipe'];limits=recipe['process_limits'];res=recipe['resources'];unit=b['decision']['execution_unit_id']
    need(limits['total_seconds']==NOMINAL_TOTAL_SECONDS,'FROZEN_WHOLE_COMMAND_BUDGET')
    need(time.monotonic()<work_deadline,'PREFLIGHT_EXHAUSTED_BUDGET')
    stable=ProtectedDirectory(b['binding']['stable_consumption_root'])
    # This permanent reservation is the single-consumption boundary. No retry,
    # resume-as-new, alternate root or automatic removal after any later failure.
    run=stable.reserve(unit);nodes=run.reserve('nodes');runs=run.reserve('runs')
    roots={'nodes':nodes.path,'runs':runs.path};nodes.close();runs.close()
    nonce=uuid.uuid4().hex
    child=None;pidfd=None;expected=None;reaped=False;exit_code=None;rusage=None
    owned=[];selector=None;failure=None;terminal=None;launch_raw=None
    captures={'stdout':bytearray(),'stderr':bytearray()};progress_buffer=bytearray();ack_buffer=bytearray()
    try:
        run.publish('admission.json',canonical({'schema':'F9_INTEGRATED_UNIT_CONSUMPTION_V1','execution_unit_id':unit,
            'decision_sha256':sha(b['decision_raw']),'deployment_sha256':sha(b['deployment_raw']),
            'recipe_sha256':sha(b['recipe_raw']),'launch_nonce':nonce,'entry_monotonic':ENTRY_MONOTONIC,
            'deadline':deadline,'automatic_retry':False}),1024*1024)
        read_fd,request_fd=os.pipe2(os.O_NONBLOCK|os.O_CLOEXEC)
        ack_fd,write_fd=os.pipe2(os.O_NONBLOCK|os.O_CLOEXEC);owned.extend((read_fd,request_fd,ack_fd,write_fd))
        env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','PYTHONHASHSEED':'0',
             'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1',
             'OMP_DYNAMIC':'FALSE','MKL_DYNAMIC':'FALSE','PYTHONDONTWRITEBYTECODE':'1'}
        command=[b['runtime']['python_executable'],'-I','-S','-B','-X','utf8',str(b['package']/'bootstrap.py'),
            deployment_path,decision_path,decision_sha,run.path,str(request_fd),str(ack_fd),str(ENTRY_MONOTONIC),str(work_deadline)]
        check();child=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            cwd=str(b['package']),env=env,close_fds=True,pass_fds=(request_fd,ack_fd),start_new_session=True)
        # A not-yet-reaped direct child cannot have its PID reused. pidfd binds
        # the kernel task; no signal is ever sent via an unbound numeric PID.
        pidfd=os.pidfd_open(child.pid,0);expected=proc_identity(child.pid)
        need(expected['argv']==command and expected['ppid']==os.getpid() and expected['exe']==b['runtime']['python_executable'],'ACTUAL_CHILD_COMMAND_IDENTITY')
        os.close(request_fd);owned.remove(request_fd);os.close(ack_fd);owned.remove(ack_fd)
        launch_raw=canonical({'schema':'F9_INTEGRATED_PARENT_LAUNCH_V1','execution_unit_id':unit,
            'decision_sha256':sha(b['decision_raw']),'launch_nonce':nonce,'entry_monotonic':ENTRY_MONOTONIC,
            'deadline':work_deadline,'child_identity':expected,'parent_identity':proc_identity(os.getpid()),
            'parent_source_pin':b['pins']['integrated_parent.py']})+b'\n'
        run.publish('launch.json',launch_raw,1024*1024)
        need(time.monotonic()<work_deadline,'EXPIRED_BEFORE_GO')
        child.stdin.write(launch_raw);child.stdin.flush();child.stdin.close()
        window=NativeProgressWindow(run_directory=run,execution_unit_id=unit,launch_nonce=nonce,
            work_deadline=work_deadline,nominal_native_seconds=res['nominal_native_call_seconds'],
            max_attempts=res['max_solver_calls'],record_cap=limits['max_progress_frame_bytes'])
        selector=selectors.DefaultSelector()
        for stream,role in ((child.stdout,'stdout'),(child.stderr,'stderr')):
            os.set_blocking(stream.fileno(),False);selector.register(stream.fileno(),selectors.EVENT_READ,role)
        selector.register(read_fd,selectors.EVENT_READ,'progress');pipes_open=3
        while pipes_open or ack_buffer:
            remaining=window.next_deadline()-time.monotonic();need(remaining>0,'PARENT_WATCHDOG_EXPIRED')
            if ack_buffer:
                try:selector.get_key(write_fd)
                except KeyError:selector.register(write_fd,selectors.EVENT_WRITE,'ack')
            for key,mask in selector.select(min(.25,remaining)):
                role=key.data
                if role=='ack':
                    try:count=os.write(write_fd,ack_buffer)
                    except BlockingIOError:continue
                    need(count>0,'ACK_SHORT_WRITE');del ack_buffer[:count]
                    if not ack_buffer:selector.unregister(write_fd)
                    continue
                try:chunk=os.read(key.fd,65536)
                except BlockingIOError:continue
                if not chunk:
                    selector.unregister(key.fd);pipes_open-=1
                    if role=='progress':need(not progress_buffer and window.active is None,'PROGRESS_EOF_INCOMPLETE')
                    continue
                if role in captures:
                    captures[role].extend(chunk);need(len(captures[role])<=limits['max_'+role+'_bytes'],'CAPTURE_LIMIT:'+role)
                else:
                    progress_buffer.extend(chunk);need(len(progress_buffer)<=limits['max_progress_frame_bytes'],'PROGRESS_BUFFER_CAP')
                    while b'\n' in progress_buffer:
                        raw,_,rest=progress_buffer.partition(b'\n');progress_buffer[:]=rest
                        need(not ack_buffer,'OVERLAPPING_UNACKNOWLEDGED_PROGRESS')
                        ack_buffer.extend(window.receive(bytes(raw))+b'\n')
            if not reaped:
                pid,status,usage=os.wait4(child.pid,os.WNOHANG)
                if pid:
                    reaped=True;exit_code=os.waitstatus_to_exitcode(status);rusage=usage;child.returncode=exit_code
                    need(exit_code==0,'CHILD_FAILED_NO_RETRY')
        while not reaped:
            need(time.monotonic()<work_deadline,'REAP_NOMINAL_DEADLINE')
            pid,status,usage=os.wait4(child.pid,os.WNOHANG)
            if pid:
                reaped=True;exit_code=os.waitstatus_to_exitcode(status);rusage=usage;child.returncode=exit_code
            else:time.sleep(.01)
        need(exit_code==0 and reaped and not captures['stderr'],'EXTERNAL_EXIT_OR_STDERR_FAILURE')
        progress=window.terminal();need(progress['attempts']==progress['returns']==125 and progress['sequence']==250,'COMPLETE_PROGRESS_COUNTS')
        check();output_raw=bytes(captures['stdout']);output=document(output_raw)
        need(output['schema']=='F9_INTEGRATED_CHILD_COMPLETE_V1' and output['execution_unit_id']==unit and output['launch_nonce']==nonce,'CHILD_OUTPUT_IDENTITY')
        need(output['process_identity']=={k:expected[k] for k in ('pid','start_ticks')} and output['launch_sha256']==sha(launch_raw)
             and output['decision_sha256']==sha(b['decision_raw']),'CHILD_OUTPUT_ACTUAL_BINDING')
        need(output['native_file_operations'] is None and output['native_network_operations'] is None and output['external_exit_cleanup_verified'] is False,'CHILD_SCOPE')
        journal=read_bytes(run.path+'/audit_journal.jsonl',limits['max_stderr_bytes']);need(journal==b'','PHYSICAL_AUDIT_JOURNAL_NOT_EMPTY')
        need(output['audit_latch']['installed'] is True and output['audit_latch']['latched'] is False and output['audit_latch']['denial_count']==0 and output['audit_latch']['journal_error'] is None,'AUDIT_LATCH_STATUS')
        ack_rows=output['progress_acknowledgements'];need(len(ack_rows)==250,'CHILD_ACK_COUNT')
        before_nonces=[]
        for seq,ack in enumerate(ack_rows,1):
            check();raw=read_bytes(run.path+'/progress_'+str(seq).zfill(12)+'.json',limits['max_progress_frame_bytes']);record=document(raw)
            need(ack['sequence']==record['sequence']==seq and ack['progress_record_sha256']==sha(raw),'ACK_PHYSICAL_RECORD_PIN')
            need(all(ack[k]==record[k] for k in ('execution_unit_id','launch_nonce','phase','call_nonce')),'ACK_RECORD_IDENTITY')
            if record['phase']=='BEFORE_NATIVE_BACKGROUND':before_nonces.append(record['call_nonce'])
        runclaims=list(Path(roots['runs']).glob('node_*.claim.json'));need(len(runclaims)==1,'ONE_GLOBAL_RUN_CLAIM')
        claim,files,_=unpack(Path(roots['runs']),runclaims[0],res['max_run_record_bytes'])
        result=output['result'];need(document(files['controller_result.json'])==result and files['decision.json']==b['decision_raw'],'ACTUAL_RUN_COMMIT')
        need(sha(files['request.json'])==output['request_sha256']==result['request_sha256'],'RUN_REQUEST_PIN')
        need(result['counts']=={'callback_attempts':75000,'callback_returns':75000,'new_solver_attempts':125,'new_solver_returns':125,'new_supplier_entries':125}
             and result['status']=='ENGINEERING_ONLY' and result['complete_declared_family'] is True,'ACTUAL_CONTROLLER_COUNTS')
        audit=validate_terminal(files['supervisor_terminal.json'],execution_unit_id=unit,request_sha256=output['request_sha256'],
            decision_sha256=sha(b['decision_raw']),runtime_sha256=sha(b['runtime_raw']),supervisor_pin=b['pins']['integrated_supervisor.py'],
            new_solver_attempts=125,new_solver_returns=125);need(sha(files['supervisor_terminal.json'])==result['supervisor_terminal_sha256'],'TERMINAL_FILE_PIN')
        need(audit['nonce']==nonce and audit['process_identity']==output['process_identity'] and audit['watchdog_reference']['sha256']==sha(launch_raw)
             and audit['audit_journal_reference']['sha256']==sha(journal) and audit['supervisor_reference']['sha256']==b['pins']['integrated_supervisor.py']['sha256'],'ACTUAL_TERMINAL_NONCE_PROCESS_REFERENCES')
        need(audit['execution_decision_sha256']==sha(b['decision_raw']) and audit['runtime_sha256']==sha(b['runtime_raw']) and audit['request_sha256']==output['request_sha256'],'TERMINAL_ROOT_BINDINGS')
        loaded=output['loaded_receipt'];need(loaded['runtime_sha256']==sha(b['runtime_raw']) and loaded['native_file_operations'] is None and loaded['native_network_operations'] is None,'ACTUAL_LOADER_RUNTIME_SCOPE')
        for role,source in loaded['modules'].items():
            path=Path(source['file']);pin=b['runtime']['files'].get(str(path)) if role in ('numpy','camb') else b['pins'].get(path.name)
            need(pin is not None and pin['sha256']==source['sha256'],'ACTUAL_LOADED_SOURCE_PIN')
        measure=output['final_resources'];early=audit['resource_measurements']
        required=('store_reserved_bytes','store_exclusive_creations','store_quota_bytes','max_threads_observed','native_map_samples','native_map_pins','user_cpu_s','system_cpu_s','max_rss_kib_linux','elapsed_from_command_entry_s')
        need(all(k in measure and k in early for k in required),'RESOURCE_MEASUREMENTS_NOT_EMPTY')
        need(measure['max_threads_observed']==early['max_threads_observed']==1 and measure['native_map_samples']>=early['native_map_samples']>=1,'ACTUAL_RUNTIME_SAMPLING')
        need(measure['store_quota_bytes']==res['nominal_store_bytes'] and 0<early['store_reserved_bytes']<=measure['store_reserved_bytes']<=res['nominal_store_bytes'],'STORE_QUOTA_RECORD')
        need(measure['user_cpu_s']<=rusage.ru_utime+.05 and measure['system_cpu_s']<=rusage.ru_stime+.05 and measure['max_rss_kib_linux']<=rusage.ru_maxrss,'GETRUSAGE_EXTERNAL_COMPARISON')
        need(0<measure['elapsed_from_command_entry_s']<=time.monotonic()-ENTRY_MONOTONIC and rusage.ru_utime+rusage.ru_stime<=limits['cpu_seconds']+1 and rusage.ru_maxrss*1024<=res['nominal_memory_bytes'],'ACTUAL_RESOURCE_LIMITS')
        for path,pin in measure['native_map_pins'].items():need(b['runtime']['native_map_pins'].get(path)==pin,'ACTUAL_NATIVE_MAP_PIN')
        family=document((b['package']/'family_metadata.json').read_bytes());family_ids=[x['label'] for x in family['family_labels']]
        reference=verify(roots=roots,result=result,recipe=recipe,family_ids=family_ids,checkpoint=check)
        need(sorted(before_nonces)==reference['background_nonces'],'PROGRESS_NONCES_MATCH_REAL_BACKGROUND_CLAIMS')
        measured=reference['store'];need(measured['exclusive_creation_inodes']==measure['store_exclusive_creations']==150252
             and measured['unique_inodes']==150252 and measured['paths']==225378
             and measured['physical_unique_inode_bytes']<=measure['store_reserved_bytes']
             and measured['allocated_unique_inode_bytes']<=res['nominal_store_bytes'],'EXTERNAL_STORE_QUOTA_ACCOUNTING')
        # Recheck package/runtime after the child and reference; no second science call.
        bundle(deployment_path,decision_path,decision_sha,check)
        terminal={'schema':'F9_INTEGRATED_EXTERNAL_TERMINAL_V1','status':'SYNTHETIC_INTEGRATED_ENGINEERING_ACCEPTED',
            'execution_unit_id':unit,'launch_nonce':nonce,'decision_sha256':sha(b['decision_raw']),
            'stdout_pin':{'bytes':len(output_raw),'sha256':sha(output_raw)},'child_identity':expected,
            'child_exit_code':exit_code,'direct_child_reaped':reaped,'cleanup_uncertain':False,
            'resource_measurements':{'child_wait4_user_cpu_s':rusage.ru_utime,'child_wait4_system_cpu_s':rusage.ru_stime,
                'child_wait4_max_rss_kib_linux':rusage.ru_maxrss,'store':measured,'wall_before_terminal_persistence_s':time.monotonic()-ENTRY_MONOTONIC},
            'progress':progress,'integrated_reference':reference,'evidence_scope':'COOPERATIVE_PYTHON_AND_TRUSTED_PINNED_NATIVE',
            'OS_deadline_guarantee':False,'native_IO_isolation':False,'descendant_OS_containment':False,
            'native_file_operations':None,'native_network_operations':None,'p':None,'sigma':None,'verdict':None,
            'automatic_retry':False,'physical_opening_authorized':False}
        run.publish('child_stdout.json',output_raw,limits['max_stdout_bytes']);check()
        run.publish('terminal_candidate.json',canonical(terminal),8*1024*1024);check()
        # Acceptance is a separate final seal *after* terminal readback/fsync and
        # clock check. A terminal candidate alone is never accepted.
        seal={'schema':'F9_INTEGRATED_COMPLETION_SEAL_V1','terminal_sha256':sha(canonical(terminal)),
              'wall_before_seal_persistence_s':time.monotonic()-ENTRY_MONOTONIC,'entry_monotonic':ENTRY_MONOTONIC,
              'deadline':deadline,'direct_child_reaped':True,'cleanup_uncertain':False,
              'acceptance_requires_parent_exit_zero_and_absent_failure':True}
        run.publish('completion_seal.json',canonical(seal),65536);check()
        print(canonical({'status':'SYNTHETIC_INTEGRATED_ENGINEERING_ACCEPTED','execution_unit_id':unit,
            'completion_seal_sha256':sha(canonical(seal)),'wall_after_seal_persistence_s':time.monotonic()-ENTRY_MONOTONIC,
            'native_IO_isolation':False,'p':None,'sigma':None,'verdict':None}).decode())
    except BaseException as exc:
        failure=exc
        raise
    finally:
        cleanup_error=None
        if child is not None and not reaped:
            try:
                if pidfd is None:pidfd=os.pidfd_open(child.pid,0)
                try:signal.pidfd_send_signal(pidfd,signal.SIGKILL,None,0)
                except ProcessLookupError:pass
                end=min(deadline,time.monotonic()+5)
                while time.monotonic()<end:
                    pid,status,usage=os.wait4(child.pid,os.WNOHANG)
                    if pid:
                        reaped=True;exit_code=os.waitstatus_to_exitcode(status);child.returncode=exit_code;break
                    time.sleep(.01)
                need(reaped,'CLEANUP_REAP_UNCERTAIN')
            except BaseException as exc:cleanup_error=bounded_error(exc)
        if failure is not None:
            for label,captured in captures.items():
                if captured:
                    try:run.publish('partial_'+label+'.bin',bytes(captured),limits['max_'+label+'_bytes'])
                    except BaseException:pass
            try:run.publish('failure.json',canonical({'schema':'F9_INTEGRATED_FAILED_OR_UNCERTAIN_V1','error':bounded_error(failure),
                'direct_child_reaped':reaped,'cleanup_uncertain':not reaped if child is not None else False,'cleanup_error':cleanup_error,
                'wall_at_failure_persistence_s':time.monotonic()-ENTRY_MONOTONIC,'automatic_retry':False}),65536)
            except BaseException:pass  # Permanent consumed unit directory still forbids retry; never success.
        if selector is not None:selector.close()
        for fd in owned:
            try:os.close(fd)
            except OSError:pass
        if pidfd is not None:os.close(pidfd)
        for stream in (() if child is None else (child.stdin,child.stdout,child.stderr)):
            if stream is not None:stream.close()
        run.close();stable.close()
        if cleanup_error is not None:raise RuntimeError('CLEANUP_UNCERTAIN_NO_SUCCESS:'+str(cleanup_error))

if __name__=='__main__':
    main(sys.argv[1:])
