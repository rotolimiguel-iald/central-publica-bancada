"""New callable adapter over the unchanged prediction_worker; no solver here.

The historic worker main/CLAIM/scope is never invoked. Imports are stdlib only.
A real qualified supervisor and explicit future ROOT decision remain required.
"""
import hashlib
import json
import math
import sys
import time


def canonical(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(',', ':'),allow_nan=False).encode()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def need(ok, reason):
    if not ok: raise RuntimeError(reason)


class ExistingEngineSupplier:
    def __init__(self, *, configuration_json, runtime_sha256, scope_id,
                 engine_module, camb_module, assembler_module, supervisor,
                 required_references, max_solver_calls, nominal_call_seconds, checkpoint):
        self.raw=configuration_json
        self.configuration=json.loads(configuration_json)
        self.configuration_sha256=sha(configuration_json)
        self.runtime_sha256,self.scope_id=runtime_sha256,scope_id
        self.engine,self.camb,self.assembler=engine_module,camb_module,assembler_module
        self.supervisor,self.checkpoint=supervisor,checkpoint
        self.references=required_references
        self.max_calls=max_solver_calls
        self.nominal_call_seconds=nominal_call_seconds
        self.attempts=self.returns=self.entries=0
        self.nonces=set(); self.active=False
        self.points={tuple(p['theta']):p['id'] for p in self.configuration['points']}
        need(len(self.points)==len(self.configuration['points']),'DUPLICATE_THETA')
        self.original_get_background=camb_module.get_background
        self.original_worker=engine_module.prediction_worker

    def __call__(self, request):
        need(not self.active,'SUPPLIER_REENTRY')
        need(type(request) is dict and set(request)=={'identity','claim_nonce',
             'external_execution_authorization_reference','resource_limits_reference',
             'loaded_objects_reference'},'SUPPLIER_REQUEST_SCHEMA')
        identity=request['identity']; nonce=request['claim_nonce']
        need(type(nonce) is str and len(nonce)==32 and all(c in '0123456789abcdef' for c in nonce),
             'SUPPLIER_NONCE')
        need(nonce not in self.nonces,'SUPPLIER_NONCE_CONSUMED')
        theta=tuple(identity['theta'])
        expected={'schema':'F9_SHARED_BACKGROUND_IDENTITY_V1','scope_id':self.scope_id,
            'theta':list(theta),'engine_configuration_sha256':self.configuration_sha256,
            'runtime_sha256':self.runtime_sha256,
            'engine_sha256':self.assembler.SOURCE_PINS['background_engine']['sha256'],
            'protocol_sha256':self.assembler.SOURCE_PINS['background_protocol']['sha256'],
            'supplier_reference':self.references['supplier_reference']}
        need(identity==expected and theta in self.points,'SUPPLIER_SCOPE_OR_POINT')
        for name in ('external_execution_authorization_reference','resource_limits_reference','loaded_objects_reference'):
            need(request[name]==self.references[name],'SUPPLIER_REFERENCE_BINDING')
        need(self.entries<self.max_calls and self.attempts<self.max_calls,'SUPPLIER_BUDGET')
        need(self.engine.prediction_worker is self.original_worker and
             self.camb.get_background is self.original_get_background and
             sys.modules.get('camb') is self.camb,'SUPPLIER_LOADED_OBJECT_CHANGED')
        need(sha(canonical(self.configuration))==sha(canonical(json.loads(self.raw))),
             'SUPPLIER_CONFIGURATION_CHANGED')
        self.nonces.add(nonce);self.entries+=1;self.active=True
        local_attempts=local_returns=0
        started=time.monotonic()
        self.checkpoint('BEFORE_BACKGROUND_ENGINE',{'theta':list(theta),'nonce':nonce})
        def counted(*args,**kwargs):
            nonlocal local_attempts,local_returns
            self.checkpoint('BEFORE_NATIVE_BACKGROUND',{'theta':list(theta),'nonce':nonce})
            need(local_attempts==0 and self.attempts<self.max_calls,'SECOND_NATIVE_CALL_FORBIDDEN')
            local_attempts+=1;self.attempts+=1
            result=self.original_get_background(*args,**kwargs)
            local_returns+=1;self.returns+=1
            self.checkpoint('AFTER_NATIVE_BACKGROUND',{'theta':list(theta),'nonce':nonce})
            return result
        self.camb.get_background=counted
        try:
            # Exact existing API. No main(), execute_worker_once(), or old claims.
            result=self.original_worker(self.configuration,self.points[theta],'reference')
            need(self.camb.get_background is counted,'CAMB_WRAPPER_CHANGED')
        finally:
            self.camb.get_background=self.original_get_background
            self.active=False
        self.checkpoint('AFTER_BACKGROUND_ENGINE',{'theta':list(theta),'nonce':nonce})
        need(time.monotonic()-started<=self.nominal_call_seconds,'NOMINAL_BACKGROUND_CALL_TIME_EXCEEDED')
        need(local_attempts==local_returns==1,'EXACTLY_ONE_NATIVE_RETURN_REQUIRED')
        need(result['theta']==list(theta) and result['point_id']==self.points[theta] and
             result['profile']=='reference','BACKGROUND_RESULT_POINT')
        result_raw=canonical(result)
        process=self.supervisor.process_identity()
        need(type(process) is dict and set(process)=={'pid','start_ticks'} and
             all(type(process[x]) is int and process[x]>0 for x in process),'PROCESS_IDENTITY')
        receipt={'status':'ENGINEERING_BACKGROUND_RETURNED','request_id':self.scope_id,
            'nonce':nonce,'process':process,'configuration_sha256':self.configuration_sha256,
            'runtime_sha256':self.runtime_sha256,'background_result_sha256':sha(result_raw),
            'solver_calls_attempted':local_attempts,'solver_calls_returned':local_returns,
            'wall_s':time.monotonic()-started,'uniform_error_bound':None,'observed_reads':False}
        receipt_raw=canonical(receipt)
        packet={'schema':'F9_BACKGROUND_PACKET_V1','status':'ENGINEERING_RESULT','error':None,
            'result':result,'identity':{'engine_sha256':expected['engine_sha256'],
            'protocol_sha256':expected['protocol_sha256'],
            'engine_configuration_sha256':self.configuration_sha256,'runtime_sha256':self.runtime_sha256,
            'theta':list(theta),'z_law':self.configuration['redshifts']['z_star_law'],
            'units':self.assembler.BACKGROUND_UNITS,'execution_receipt_sha256':sha(receipt_raw)}}
        return {'packet_json':canonical(packet),'result_json':result_raw,'receipt_json':receipt_raw}
