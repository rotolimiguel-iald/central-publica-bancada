"""Future fixed scientific child; requires original external ROOT authority.

No historical control main is called. Scientific modules are loaded only after
full authority, byte pins, resource limits and cooperative audit installation.
"""
import time
import os
import sys
from pathlib import Path
# -I removes script-directory discovery; the parent has already pinned this
# bootstrap and complete control closure before execve. No inherited PYTHONPATH.
sys.path.insert(0,str(Path(__file__).resolve().parent))
import json
import resource
import importlib
import importlib.metadata
import importlib.machinery
import uuid
from posix_protocol import canonical, document, need, proc_identity, sha
from deployment_contract import bundle
from audit_guard import PreopenedJournal
from guard_runtime import RuntimePolicy
from loaded_registry import LoadedRegistry
import supervisor_port
from integrated_supervisor import IntegratedSupervisor
import synthetic_inputs


def run(argv):
    need(len(argv)==8,'FIXED_PARENT_ONLY_CHILD_ARGUMENTS')
    deployment_path,decision_path,decision_sha,runroot,reqfd,ackfd,entry,deadline=argv
    request_fd,ack_fd=int(reqfd),int(ackfd);entry=float(entry);deadline=float(deadline)
    def check():need(time.monotonic()<deadline,'WHOLE_COMMAND_DEADLINE')
    check();go=sys.stdin.buffer.readline(1024*1024);launch=document(go)
    need(launch['schema']=='F9_INTEGRATED_PARENT_LAUNCH_V1' and launch['entry_monotonic']==entry and launch['deadline']==deadline,'PARENT_LAUNCH_CLOCK')
    b=bundle(deployment_path,decision_path,decision_sha,check);recipe=b['recipe'];limits=recipe['process_limits'];res=recipe['resources']
    need(launch['decision_sha256']==sha(b['decision_raw']) and launch['execution_unit_id']==b['decision']['execution_unit_id'],'PARENT_AUTHORITY_LINK')
    expected_root=b['binding']['stable_consumption_root']+'/'+b['decision']['execution_unit_id']
    need(runroot==expected_root,'STABLE_RESERVED_RUN_ROOT')
    roots={'nodes':runroot+'/nodes','runs':runroot+'/runs'}
    resource.setrlimit(resource.RLIMIT_AS,(res['nominal_memory_bytes'],res['nominal_memory_bytes']))
    resource.setrlimit(resource.RLIMIT_CPU,(limits['cpu_seconds'],limits['cpu_seconds']))
    resource.setrlimit(resource.RLIMIT_FSIZE,(limits['file_size_bytes'],limits['file_size_bytes']))
    resource.setrlimit(resource.RLIMIT_NOFILE,(limits['open_files'],limits['open_files']))
    need(all(os.environ.get(k)=='1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')),'FIXED_THREAD_ENV')
    # Exact current search paths come from reviewed runtime, never host user-site.
    sys.path[:]=[str(b['package'])]+b['runtime']['python_search_path'];sys.dont_write_bytecode=True
    journal=PreopenedJournal(runroot+'/audit_journal.jsonl')
    policy=RuntimePolicy(package=b['package'],package_pins=b['pins'],runtime=b['runtime'],roots=roots,
        resources=res,deadline=deadline,journal=journal,owned_fds=(0,1,2,request_fd,ack_fd,journal.fd))
    policy.install()
    registry=LoadedRegistry(b['package'],b['pins'],b['runtime'],policy,sha(b['runtime_raw']))
    numpy=importlib.import_module('numpy');camb=importlib.import_module('camb')
    registry.native_module('numpy',numpy);registry.native_module('camb',camb)
    source_map=document((b['package']/'COPIED_SOURCE_MAP.json').read_bytes())
    order=('support','linear','assembler','consumer','prior','precision','theta','profile','node','durable','engine')
    aliases={'support':'singular_gaussian_v2','linear':'linear_gaussian'};bindings={'numpy':numpy,'camb':camb,'supervisor_port':supervisor_port}
    for role in order:
        policy.checkpoint('BEFORE_LOAD_'+role)
        bindings[role]=registry.load(role,source_map[role],aliases.get(role,'f9_integrated_'+role))
    bindings['supplier']=registry.load('supplier','background_supplier.py','f9_integrated_supplier')
    controller=registry.load('controller','controller.py','f9_integrated_controller')
    builder=registry.load('builder','builder.py','f9_integrated_covariance_builder')
    primitive=registry.primitive(source_map['primitive_source'])
    loaded_raw=registry.receipt()
    guard_raw=canonical({'schema':'F9_ACTUAL_SCOPED_GUARD_CONTRACT_V1','runtime_sha256':sha(b['runtime_raw']),
        'roots':roots,'scope':'PYTHON_AUDIT_EVENTS_COOPERATIVE_ONLY','source_pin':b['pins']['guard_runtime.py'],
        'store_operations':'I02 exact exclusive open/fdopen/fsync/same-root pending hardlink/readback',
        'native_file_operations':None,'native_network_operations':None,'native_IO_isolation':False})
    supervisor=IntegratedSupervisor(policy=policy,registry=registry,decision_raw=b['decision_raw'],recipe_raw=b['recipe_raw'],
        runtime_raw=b['runtime_raw'],guard_raw=guard_raw,loaded_raw=loaded_raw,launch_raw=go,roots=roots,
        request_fd=request_fd,ack_fd=ack_fd,supervisor_pin=b['pins']['integrated_supervisor.py'],journal_fd=journal.fd)
    supervisor.native_background=camb.get_background
    request_raw,artifacts,family=synthetic_inputs.build(package=b['package'],source_map=source_map,
        source_pins=document((b['package']/'SOURCE_PINS.json').read_bytes()),modules=bindings,
        auxiliary={'builder':builder,'primitive':primitive},recipe_raw=b['recipe_raw'],decision_raw=b['decision_raw'],
        runtime_raw=b['runtime_raw'],loaded_raw=loaded_raw,guard_raw=guard_raw,review_raw=b['review_raw'],roots=roots,checkpoint=supervisor.checkpoint)
    supervisor.bind_prepared(request_raw,artifacts)
    result=controller.run_once(request_json=request_raw,request_sha256=sha(request_raw),decision_json=b['decision_raw'],
        decision_sha256=sha(b['decision_raw']),artifacts=artifacts,bindings=bindings,supervisor=supervisor)
    registry.check(deep=True);policy.checkpoint('AFTER_RUN_COMMIT');need(os.fstat(journal.fd).st_size==0,'NONEMPTY_AUDIT_JOURNAL')
    r=resource.getrusage(resource.RUSAGE_SELF)
    final={'schema':'F9_INTEGRATED_CHILD_COMPLETE_V1','execution_unit_id':b['decision']['execution_unit_id'],
        'launch_nonce':launch['launch_nonce'],'process_identity':supervisor.process_identity(),
        'launch_sha256':sha(go),'decision_sha256':sha(b['decision_raw']),'request_sha256':sha(request_raw),
        'result':result,'family_summary_sha256':sha(canonical(family)),'loaded_receipt':document(loaded_raw),
        'progress_acknowledgements':supervisor.acks,'audit_latch':policy.latch.snapshot(),
        'final_resources':{**policy.measurements(),'user_cpu_s':r.ru_utime,'system_cpu_s':r.ru_stime,'max_rss_kib_linux':r.ru_maxrss,
                           'elapsed_from_command_entry_s':time.monotonic()-entry},
        'external_exit_cleanup_verified':False,'native_file_operations':None,'native_network_operations':None}
    raw=canonical(final)+b'\n';need(len(raw)<=limits['max_stdout_bytes'],'FINAL_STDOUT_CAP');check()
    view=memoryview(raw)
    while view:
        n=os.write(1,view);need(n>0,'FINAL_STDOUT_SHORT_WRITE');view=view[n:]
    check()

if __name__=='__main__':
    run(sys.argv[1:])
