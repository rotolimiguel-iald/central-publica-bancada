"""Concrete fail-closed adapter to the exact 39f88 abstract signatures.

It materializes process identity, pin checks and cooperative checkpoints. It
REFUSES scientific admission because the available guard does not fulfill the
port's universal native IO claim. There is no flag overriding that refusal.
This explicit incompatibility is not an implementation of an OS sandbox.
"""
import os
from pathlib import Path
import sys
import time
from supervisor_port import QualifiedSupervisor
from posix_protocol import canonical, digest, document, need, proc_identity, same_process, sha

class NativePolicyUnavailable(RuntimeError):
    pass

class POSIXSupervisor39(QualifiedSupervisor):
    def __init__(self, *, launch_context_json, cooperative_policy):
        self.launch=document(launch_context_json)
        self.policy=cooperative_policy
        self.state='PREPARED_NOT_ADMITTED'
        self.me=proc_identity(os.getpid())
        self.parent=proc_identity(os.getppid())
        need(same_process(self.me,self.launch['child']) and same_process(self.parent,self.launch['parent']),
             'SUPERVISOR_PROCESS_IDENTITY')
        need(type(self.launch['nonce']) is str and len(self.launch['nonce'])==32,'SUPERVISOR_NONCE')

    def admit(self, *, request_json, decision_json, guard_contract_json,
              resources_json, runtime_inventory_json, artifacts, bindings):
        need(self.state=='PREPARED_NOT_ADMITTED','SUPERVISOR_SINGLE_ADMISSION')
        self.state='ADMISSION_ATTEMPTED'
        request,decision,guard,resources,runtime=map(document,
            (request_json,decision_json,guard_contract_json,resources_json,runtime_inventory_json))
        need(sha(request_json)==self.launch['request_sha256'] and
             sha(decision_json)==self.launch['decision_sha256'], 'PINNED_REQUEST_AND_DECISION')
        need(decision['request_sha256']==sha(request_json) and
             request['execution_unit_id']==decision['execution_unit_id']==self.launch['execution_unit_id'],
             'CONTROLLER_UNIT_BINDING')
        need(decision['may_read_observations'] is False,'OBSERVED_RELEASE_VERIFIER_NOT_IMPLEMENTED')
        need(type(artifacts) is dict and set(artifacts)==set(request['artifact_pins']), 'EXACT_ARTIFACTS')
        for name,item in request['artifact_pins'].items():
            raw=artifacts[name]
            need(type(raw) is bytes and len(raw)==item['bytes'] and sha(raw)==digest(item['sha256']),
                 'ARTIFACT_PIN:'+name)
        need(resources['threads']==resources['workers_parallel']==1 and resources['automatic_retries']==0,
             'SERIAL_NO_RETRY')
        need(sha(runtime_inventory_json)==self.launch['runtime_sha256'],'RUNTIME_BINDING')
        need(isinstance(self,bindings['supervisor_port'].QualifiedSupervisor),'SAME_PORT_CLASS')
        self.policy.checkpoint('STRICT_ADMISSION_PREFLIGHT')
        # An audit flag, receipt, source pin or observed zero Python denials is
        # not proof of native IO isolation. No code path can set ADMITTED here.
        self.state='REFUSED_NATIVE_POLICY_SCOPE'
        raise NativePolicyUnavailable('39F88_PORT_NATIVE_READ_NETWORK_ENFORCEMENT_UNAVAILABLE')

    def checkpoint(self, phase, context):
        need(self.state=='ADMITTED','SCIENTIFIC_ADMISSION_NOT_ESTABLISHED')
        need(same_process(proc_identity(os.getpid()),self.me),'CURRENT_PROCESS_CHANGED')
        need(context['execution_unit_id']==self.launch['execution_unit_id'],'CHECKPOINT_UNIT')
        need(time.monotonic()<self.launch['work_deadline'],'SUPERVISOR_WORK_DEADLINE')
        self.policy.checkpoint(phase)

    def process_identity(self):
        actual=proc_identity(os.getpid())
        need(same_process(actual,self.me),'LIVE_PROCESS_IDENTITY_CHANGED')
        return {'pid':actual['pid'],'start_ticks':actual['start_ticks']}

    def terminal_audit(self, *, context):
        # Never manufacture AUDIT_ACCEPTED or numeric native network zero.
        need(self.state=='ADMITTED','TERMINAL_SCIENTIFIC_AUDIT_UNAVAILABLE')
        raise NativePolicyUnavailable('NO_UNIVERSAL_NATIVE_IO_TERMINAL_RECEIPT')
