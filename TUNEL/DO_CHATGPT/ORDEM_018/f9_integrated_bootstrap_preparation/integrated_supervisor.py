"""Concrete cooperative successor: live identities, exact admission, native ACKs."""
import os
import resource
import time
import types
from posix_protocol import canonical, document, need, proc_identity, same_process, sha
from supervisor_port import QualifiedSupervisor, EVIDENCE_SCOPE, AUDITED_OPERATIONS, KNOWN_GAPS
from native_progress import PHASES, exchange

class IntegratedSupervisor(QualifiedSupervisor):
    def __init__(self, *, policy, registry, decision_raw, recipe_raw, runtime_raw,
                 guard_raw, loaded_raw, launch_raw, roots, request_fd, ack_fd,
                 supervisor_pin, journal_fd):
        self.policy=policy;self.registry=registry;self.decision_raw=decision_raw
        self.recipe_raw=recipe_raw;self.runtime_raw=runtime_raw;self.guard_raw=guard_raw;self.loaded_raw=loaded_raw
        self.launch_raw=launch_raw;self.launch=document(launch_raw);self.roots=roots
        self.recipe=document(recipe_raw);self.decision=document(decision_raw)
        self.req_fd=request_fd;self.ack_fd=ack_fd;self.pin=supervisor_pin;self.journal_fd=journal_fd
        self.identity=proc_identity(os.getpid());need(same_process(self.identity,self.launch['child_identity']),'LAUNCH_PROCESS_IDENTITY')
        self.unit=self.decision['execution_unit_id'];self.prepared=None;self.admitted=False
        self.sequence=0;self.acks=[];self.active=None;self.attempts=self.returns=0;self.terminal_emitted=False

    def bind_prepared(self,request_raw,artifacts):
        need(self.prepared is None,'PREPARED_REQUEST_REBIND')
        self.prepared=(request_raw,artifacts)

    def admit(self, *, request_json, decision_json, guard_contract_json,
              resources_json, runtime_inventory_json, artifacts, bindings):
        need(not self.admitted and self.prepared is not None,'SINGLE_ADMISSION')
        need(decision_json==self.decision_raw and request_json==self.prepared[0] and artifacts is self.prepared[1],'ORIGINAL_AUTHORITY_AND_ACTUAL_BUILD')
        request=document(request_json)
        need(request['input_recipe_sha256']==sha(self.recipe_raw)==self.decision['input_recipe_sha256'],'FROZEN_RECIPE_LINK')
        need(guard_contract_json==self.guard_raw and runtime_inventory_json==self.runtime_raw and
             resources_json==canonical(self.recipe['resources']),'ACTUAL_RUNTIME_GUARD_RESOURCES')
        need(request['store_root']==self.roots['nodes'] and request['run_store_root']==self.roots['runs'],'STABLE_PROTECTED_ROOTS')
        need(self.decision['may_read_observations'] is False and self.decision['scope']=='F9_FULL_PRIOR_SYNTHETIC_ENGINEERING_ONLY','SYNTHETIC_SCOPE')
        need(len(request['scenarios'])==600 and self.recipe['first_level']==1 and self.recipe['last_level']==2,'FULL_FROZEN_RECIPE')
        for name,pin in request['artifact_pins'].items():
            raw=artifacts[name];need(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'ACTUAL_ARTIFACT_PIN')
        for spec in request['scenarios']:
            need(document(artifacts[spec['consumer_admission']])['data_kind']=='SYNTHETIC','NO_OBSERVED_INPUT')
        need(bindings['numpy'] is self.registry.modules['numpy'] and bindings['camb'] is self.registry.modules['camb'],'NATIVE_MODULE_INSTANCES')
        self.registry.check(deep=True);self.admitted=True;self.policy.checkpoint('ADMITTED')

    def checkpoint(self,phase,context):
        self.policy.checkpoint(phase);self.registry.check()
        camb=self.registry.modules.get('camb')
        if hasattr(self,'native_background') and phase in ('BEFORE_BACKGROUND_ENGINE','AFTER_BACKGROUND_ENGINE'):
            need(camb.get_background is self.native_background,'ACTUAL_NATIVE_BACKGROUND_OBJECT_CHANGED')
        if phase in PHASES:
            wrapper=camb.get_background
            cls=self.registry.modules['supplier'].ExistingEngineSupplier
            code=next(c for c in cls.__call__.__code__.co_consts if isinstance(c,types.CodeType) and c.co_name=='counted')
            need(isinstance(wrapper,types.FunctionType) and wrapper.__code__ is code,'PINNED_SUPPLIER_WRAPPER_CODE')
            closure=dict(zip(wrapper.__code__.co_freevars,(c.cell_contents for c in wrapper.__closure__)))
            owner=closure.get('self')
            need(isinstance(owner,cls) and owner.supervisor is self and owner.camb is camb and owner.original_get_background is self.native_background,'ACTUAL_SUPPLIER_WRAPPER_BINDING')
            need(self.admitted,'NATIVE_BEFORE_ADMISSION');nonce=context['nonce']
            if phase=='BEFORE_NATIVE_BACKGROUND':
                need(self.active is None,'NATIVE_OVERLAP');self.active=nonce;self.attempts+=1
            else:
                need(self.active==nonce,'NATIVE_NONCE_MISMATCH')
            self.sequence+=1
            ack=exchange(request_fd=self.req_fd,ack_fd=self.ack_fd,execution_unit_id=self.unit,
                launch_nonce=self.launch['launch_nonce'],sequence=self.sequence,phase=phase,call_nonce=nonce,
                deadline=self.policy.deadline,max_frame_bytes=self.recipe['process_limits']['max_progress_frame_bytes'])
            self.acks.append(ack)
            if phase=='AFTER_NATIVE_BACKGROUND':self.returns+=1;self.active=None
        self.policy.checkpoint('AFTER_'+phase)

    def process_identity(self):
        current=proc_identity(os.getpid());need(same_process(current,self.identity),'PROCESS_IDENTITY_CHANGED')
        return {'pid':current['pid'],'start_ticks':current['start_ticks']}

    def terminal_audit(self, *, context):
        need(self.admitted and not self.terminal_emitted,'SINGLE_ADMITTED_TERMINAL')
        self.registry.check(deep=True);self.policy.checkpoint('TERMINAL_AUDIT')
        need(self.active is None and self.attempts==self.returns==context['new_solver_attempts']==context['new_solver_returns']==125,'EXACT_COMPLETE_BACKGROUND_COUNTS')
        need(os.fstat(self.journal_fd).st_size==0 and not self.policy.latch.snapshot()['latched'],'PHYSICAL_JOURNAL_NOT_EMPTY')
        r=resource.getrusage(resource.RUSAGE_SELF)
        measures={**self.policy.measurements(),'user_cpu_s':r.ru_utime,'system_cpu_s':r.ru_stime,
                  'max_rss_kib_linux':r.ru_maxrss,'elapsed_from_command_entry_s':time.monotonic()-self.launch['entry_monotonic'],
                  'scope':'snapshot before run-store final commit; child final snapshot and external validator remain mandatory'}
        raw=canonical({'schema':'F9_CONTROLLER_COOPERATIVE_TERMINAL_V1','execution_unit_id':self.unit,
            'request_sha256':sha(self.prepared[0]),'execution_decision_sha256':sha(self.decision_raw),
            'runtime_sha256':sha(self.runtime_raw),'status':'PYTHON_AUDIT_ACCEPTED_SCOPED','evidence_scope':EVIDENCE_SCOPE,
            'audited_operations':list(AUDITED_OPERATIONS),'known_gaps':list(KNOWN_GAPS),'observed_reads':False,'latched':False,
            'python_unexpected_read_denials':0,'python_network_denials':0,
            'native_network_operations':None,'native_file_operations':None,'native_IO_isolation':False,
            'audit_journal_reference':{'id':self.unit+':audit-journal','sha256':sha(b'')},
            'supervisor_reference':{'id':self.unit+':supervisor','sha256':self.pin['sha256']},
            'watchdog_reference':{'id':self.unit+':parent-launch','sha256':sha(self.launch_raw)},
            'nonce':self.launch['launch_nonce'],'process_identity':self.process_identity(),'resource_measurements':measures,
            'new_solver_attempts':self.attempts,'new_solver_returns':self.returns,'external_exit_cleanup_verified':False})
        self.terminal_emitted=True;return raw
