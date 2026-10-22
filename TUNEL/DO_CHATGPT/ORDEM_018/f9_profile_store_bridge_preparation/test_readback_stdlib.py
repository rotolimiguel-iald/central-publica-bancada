"""Prepared focused stdlib tests; NOT executed in this preparation.

Only store_bridge/recovery/store_contract are real imported candidates, after
future authorization. All science modules, bridge, stores, process receipts and
registry are explicit doubles. The original registry source is read by hash
only for one custody fixture, never imported. No scientific suite is repeated.
"""
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import store_bridge as s
import recovery as r
from store_contract import SOURCE_PINS


def pinned(raw):
    return {'bytes':len(raw),'sha256':s.sha(raw)}


def context_fixture():
    blobs = {n:n.encode() for n in ('y','C','rows','origin','structure','support')}
    adm = {'schema':'F9_CONSUMER_ADMISSION_V1','scope':'ENGINEERING_POINTWISE_ONLY',
        'scenario_id':'fixture-scenario','data_kind':'SYNTHETIC',
        'input_sha256':{k:s.sha(blobs[v]) for k,v in
            (('y_native_f64le','y'),('C_native_f64le','C'),('row_ids_canonical_json','rows'),
             ('affine_origin_native_f64le','origin'))},
        'structure_sha256':s.sha(blobs['structure']),
        'references':{'fixed_affine_support':{'id':'fixture','sha256':s.sha(blobs['support'])}}}
    blobs['admission'] = s.canonical(adm)
    blobs['plan'] = s.canonical({'consumer_admission_sha256':s.sha(blobs['admission']),
                                'engine_configuration_sha256':'1'*64})
    req = {'artifact_pins':{k:pinned(v) for k,v in blobs.items()}}
    spec = {'scenario_id':'fixture-scenario','consumer_admission':'admission','theta_plan':'plan',
            'y_native':'y','C_native':'C','row_ids':'rows','affine_origin_native':'origin','structure':'structure'}
    return blobs,req,spec


def derive(blobs,req,spec):
    return s.derive_context(consumer_raw=blobs['admission'],plan_raw=blobs['plan'],
        request=req,spec=spec,support_raw=blobs['support'])


def completion_fixture():
    unit='SYNTHETIC_FIXTURE_NOT_AN_EXECUTION'
    admission={'schema':'F9_INTEGRATED_UNIT_CONSUMPTION_V1','execution_unit_id':unit,
        'launch_nonce':'a'*32,'decision_sha256':'b'*64,'entry_monotonic':10,'deadline':20}
    child={'schema':'F9_INTEGRATED_CHILD_COMPLETE_V1','execution_unit_id':unit,
        'launch_nonce':'a'*32,'decision_sha256':'b'*64,'process_identity':{'pid':10,'start_ticks':20}}
    cb=s.canonical(child)
    terminal={'schema':'F9_INTEGRATED_EXTERNAL_TERMINAL_V1','execution_unit_id':unit,
        'status':'SYNTHETIC_INTEGRATED_ENGINEERING_ACCEPTED','launch_nonce':'a'*32,'decision_sha256':'b'*64,
        'child_exit_code':0,'direct_child_reaped':True,'cleanup_uncertain':False,
        'stdout_pin':pinned(cb),'child_identity':{'pid':10,'start_ticks':20},
        'physical_opening_authorized':False,'automatic_retry':False,
        'native_file_operations':None,'native_network_operations':None,'p':None,'sigma':None,'verdict':None}
    tb=s.canonical(terminal)
    seal={'schema':'F9_INTEGRATED_COMPLETION_SEAL_V1','terminal_sha256':s.sha(tb),
        'direct_child_reaped':True,'cleanup_uncertain':False,
        'acceptance_requires_parent_exit_zero_and_absent_failure':True,'entry_monotonic':10,'deadline':20}
    sb=s.canonical(seal)
    parent={'status':'SYNTHETIC_INTEGRATED_ENGINEERING_ACCEPTED','execution_unit_id':unit,
        'completion_seal_sha256':s.sha(sb),'wall_after_seal_persistence_s':5,'p':None,'sigma':None,'verdict':None}
    pb=s.canonical(parent)
    outer={'execution_unit_id':unit,'completion_seal_sha256':s.sha(sb),
           'parent_stdout_sha256':s.sha(pb),'exit_code':0,'reaped':True}
    evidence={'admission':s.canonical(admission),'terminal':tb,'seal':sb,'child_stdout':cb,
              'parent_stdout':pb,'parent_exit':s.canonical(outer)}
    return evidence,{k:pinned(v) for k,v in evidence.items()},{k:'/'+k for k in outer},unit


def complete(f):
    evidence,expected,pointers,unit=f
    return s.external_completion(evidence=evidence,expected=expected,parent_exit_pointers=pointers,unit=unit)


@dataclass(frozen=True)
class ReceiptDouble:
    role:str
    payload_sha256:str
    evidence_sha256:tuple
    verifier_sha256:str
    scope:str


def registry_fixture():
    roles=('profile','theta','tail','reducer','bridge','threshold','store_bridge','registry')
    bindings={k:{'path':SOURCE_PINS[k]['path'],'bytes':SOURCE_PINS[k]['bytes'],
                  'sha256':SOURCE_PINS[k]['sha256']} for k in roles if k != 'store_bridge'}
    bindings['store_bridge']={'path':'/fixture/store_bridge.py','bytes':1,'sha256':'c'*64}
    contract_path=s.store_contract.__file__;contract_raw=Path(contract_path).read_bytes()
    bindings['store_contract']={'path':contract_path,**pinned(contract_raw)}
    modules={k:SimpleNamespace(__file__=v['path']) for k,v in bindings.items() if k!='registry'}
    modules['store_contract']=s.store_contract
    bridge=modules['bridge'];bridge.threshold_audit=modules['threshold']
    bridge.SOURCE_PINS={k:SOURCE_PINS[k] for k in ('profile','theta','tail','reducer')}
    bridge.Receipt=ReceiptDouble;bridge.digest=s.digest
    class RegistryDouble:
        def check(self,deep=False):
            assert deep is True
            self.checks+=1
    registry=RegistryDouble();registry.checks=0;registry.modules=modules
    registry.sources={k:{'file':v.__file__,'sha256':bindings[k]['sha256']} for k,v in modules.items()}
    registry.policy=SimpleNamespace(read_pins={v['path']:{k:v[k] for k in ('bytes','sha256')} for v in bindings.values()})
    # Bytes-only fixture from the permitted source; no exec/import.
    raw=Path(SOURCE_PINS['registry']['path']).read_bytes()
    s.pin(raw,{k:SOURCE_PINS['registry'][k] for k in ('bytes','sha256')})
    def read_pinned(path,expected,maximum):
        assert path==SOURCE_PINS['registry']['path'] and maximum==len(raw)
        return s.pin(raw,expected)
    registry_module=SimpleNamespace(__file__=SOURCE_PINS['registry']['path'],LoadedRegistry=RegistryDouble,pinned=read_pinned)
    verifier=s.RegistryVerifier(registry,bindings,bridge,lambda:None,registry_module)
    return verifier,{k:modules[k] for k in ('profile','theta','tail','reducer')},bridge.SOURCE_PINS


class ReadbackTests(unittest.TestCase):
    def test_contexts_come_from_original_admission(self):
        b,q,sp=context_fixture();out=derive(b,q,sp)
        self.assertEqual(out['data_sha256'],q['artifact_pins']['y']['sha256'])
        self.assertEqual(out['covariance_sha256'],q['artifact_pins']['C']['sha256'])
        self.assertEqual(out['X_response_sha256'],q['artifact_pins']['structure']['sha256'])
        self.assertEqual(out['support_sha256'],q['artifact_pins']['support']['sha256'])
        self.assertEqual(out['consumer_admission_sha256'],q['artifact_pins']['admission']['sha256'])

    def test_covariance_lineage_tamper(self):
        b,q,sp=context_fixture();q['artifact_pins']['C']['sha256']='0'*64
        with self.assertRaisesRegex(s.ReadbackError,'ADMISSION_REQUEST_INPUT_LINEAGE'):derive(b,q,sp)

    def test_scenario_swap(self):
        b,q,sp=context_fixture();sp['scenario_id']='other'
        with self.assertRaisesRegex(s.ReadbackError,'SYNTHETIC_ADMISSION_ONLY'):derive(b,q,sp)

    def test_original_admission_bytes_changed(self):
        b,q,sp=context_fixture();b['admission']+=b' '
        with self.assertRaisesRegex(s.ReadbackError,'PIN_MISMATCH'):derive(b,q,sp)

    def test_support_reference_not_self_authenticated(self):
        b,q,sp=context_fixture();b['support']=b'altered'
        with self.assertRaisesRegex(s.ReadbackError,'SUPPORT_REFERENCE_BYTES'):derive(b,q,sp)

    def test_context_structure_tamper(self):
        b,q,sp=context_fixture();q['artifact_pins']['structure']['sha256']='0'*64
        with self.assertRaisesRegex(s.ReadbackError,'STRUCTURE_REQUEST_BINDING'):derive(b,q,sp)

    def test_external_complete_keeps_synthetic_scope(self):
        docs=complete(completion_fixture())
        self.assertFalse(docs['terminal']['physical_opening_authorized'])
        self.assertIsNone(docs['terminal']['verdict'])

    def test_terminal_without_completion_seal_refused(self):
        f=completion_fixture();del f[0]['seal']
        with self.assertRaisesRegex(s.ReadbackError,'COMPLETE_EXTERNAL_EVIDENCE'):complete(f)

    def test_no_outer_exit_observation_refused(self):
        f=completion_fixture();del f[0]['parent_exit']
        with self.assertRaisesRegex(s.ReadbackError,'COMPLETE_EXTERNAL_EVIDENCE'):complete(f)

    def test_parent_exit_nonzero_refused(self):
        f=completion_fixture();doc=s.decode(f[0]['parent_exit']);doc['exit_code']=1
        f[0]['parent_exit']=s.canonical(doc);f[1]['parent_exit']=pinned(f[0]['parent_exit'])
        with self.assertRaisesRegex(s.ReadbackError,'OUTER_PARENT_EXIT_BINDING:exit_code'):complete(f)

    def test_exit_bool_zero_not_integer(self):
        f=completion_fixture();doc=s.decode(f[0]['parent_exit']);doc['exit_code']=False
        f[0]['parent_exit']=s.canonical(doc);f[1]['parent_exit']=pinned(f[0]['parent_exit'])
        with self.assertRaisesRegex(s.ReadbackError,'OUTER_PARENT_EXIT_BINDING:exit_code'):complete(f)

    def test_seal_mutation_fails_independent_pin(self):
        f=completion_fixture();f[0]['seal']+=b' '
        with self.assertRaisesRegex(s.ReadbackError,'PIN_MISMATCH'):complete(f)

    def test_outer_receipt_other_unit(self):
        f=completion_fixture();doc=s.decode(f[0]['parent_exit']);doc['execution_unit_id']='other'
        f[0]['parent_exit']=s.canonical(doc);f[1]['parent_exit']=pinned(f[0]['parent_exit'])
        with self.assertRaisesRegex(s.ReadbackError,'OUTER_PARENT_EXIT_BINDING:execution_unit_id'):complete(f)

    def test_registry_typed_receipt_and_copy_pins(self):
        verifier,modules,pins=registry_fixture();receipt=verifier(modules,pins)
        self.assertIs(type(receipt),ReceiptDouble)
        self.assertEqual(receipt.scope,'LOADED_OBJECTS_ONLY')
        self.assertEqual(receipt.evidence_sha256,tuple(sorted(p['sha256'] for p in pins.values())))

    def test_live_module_swapped(self):
        verifier,modules,pins=registry_fixture();modules['profile']=SimpleNamespace()
        with self.assertRaisesRegex(s.ReadbackError,'MODULE_SWAPPED'):verifier(modules,pins)

    def test_source_copy_not_byte_equivalent(self):
        verifier,modules,pins=registry_fixture();verifier.bindings['profile']['sha256']='0'*64
        with self.assertRaisesRegex(s.ReadbackError,'READER_BYTES_BINDING'):verifier(modules,pins)

    def test_registry_check_override_detected(self):
        verifier,modules,pins=registry_fixture();cls=verifier.registry_type;old=cls.check
        try:
            cls.check=lambda self,deep=False:None
            with self.assertRaisesRegex(s.ReadbackError,'REGISTRY_CHECK_REPLACED'):verifier(modules,pins)
        finally:cls.check=old

    def test_large_level_refused_before_shift(self):
        with self.assertRaisesRegex(s.ReadbackError,'ADMITTED_LEVEL_RANGE'):s.read_budget(10**100,1,6)

    def test_full_600_budget_and_partial_refusal(self):
        self.assertEqual(s.read_budget(2,75000,6),75000)
        with self.assertRaisesRegex(s.ReadbackError,'EXPLICIT_FINEST_READ_BUDGET'):s.read_budget(2,74999,6)

    def test_original_metadata_missing_refused(self):
        obj=object.__new__(r.Recovery);obj.request={'artifact_pins':{'original':pinned(b'x')}};obj.metadata={}
        with self.assertRaisesRegex(s.ReadbackError,'ORIGINAL_METADATA_NOT_RETAINED'):obj.artifact('original')

    def test_physical_failure_marker_refused(self):
        obj=object.__new__(r.Recovery);obj.clock=lambda:0;obj.deadline=1
        obj.root=SimpleNamespace(path='/fixture/unit',identity=(1,2,3,448),fd=5)
        obj.modules={'protocol':SimpleNamespace(ProtectedDirectory=SimpleNamespace(check=lambda root:None))}
        obj.intake={'roots':{'unit':{'path':'/fixture/unit','identity':[1,2,3,448]}}}
        with patch.object(r.os.path,'lexists',return_value=True):
            with self.assertRaisesRegex(s.ReadbackError,'ORIGINAL_PARENT_FAILURE'):obj.root_check()

    def test_estimate_conserves_original_intake_pin_and_scope(self):
        obj=object.__new__(r.Recovery);obj.clock=lambda:0;obj.deadline=1
        obj.intake={'level':1,'max_records':16200,'execution_unit_id':'fixture'}
        obj.intake_sha256=s.sha(b'{ "noncanonical": true }')
        obj.root_check=lambda:None
        obj.live=SimpleNamespace(check=lambda:None,bindings={'store_bridge':{'sha256':'c'*64}})
        obj.modules={k:object() for k in ('profile','theta','tail','reducer')}
        obj.contexts={'sentinel':'context'};obj._records=lambda:iter([('record',)])
        seen={}
        class BridgeDouble:
            def __init__(self,**kwargs):seen.update(kwargs)
            def estimate_family(self,records,**kwargs):
                self_consumed=list(records);seen.update(kwargs);seen['consumed']=self_consumed
                return {'status':'ENGINEERING_ONLY','verdict':None,'certified_bounds':None}
        obj.bridge=SimpleNamespace(Bridge=BridgeDouble)
        obj.external_evidence={'seal':b'synthetic-seal'}
        obj.documents={'terminal':{'integrated_reference':{'node_result_chain_sha256':'d'*64}}}
        out=obj.estimate()
        self.assertEqual(out['intake_sha256'],obj.intake_sha256)
        self.assertEqual(out['status'],'SYNTHETIC_ENGINEERING_ONLY')
        self.assertNotIn('scientific_decision',out)
        self.assertNotIn('semantic_verifier',seen)
        self.assertEqual(seen['consumed'],[('record',)])
        self.assertEqual(seen['level'],1)

    def test_final_iteration_failure_prevents_publication(self):
        obj=object.__new__(r.Recovery);obj.clock=lambda:0;obj.deadline=1
        obj.intake={'level':1,'max_records':16200};obj.root_check=lambda:None
        obj.live=SimpleNamespace(check=lambda:None,bindings={'store_bridge':{'sha256':'c'*64}})
        obj.modules={k:object() for k in ('profile','theta','tail','reducer')};obj.contexts={}
        def records():
            yield ('prefix',)
            raise s.ReadbackError('ORIGINAL_EXTERNAL_NODE_CHAIN')
        obj._records=records
        class BridgeDouble:
            def __init__(self,**kwargs):pass
            def estimate_family(self,records,**kwargs):return list(records)
        obj.bridge=SimpleNamespace(Bridge=BridgeDouble)
        with self.assertRaisesRegex(s.ReadbackError,'ORIGINAL_EXTERNAL_NODE_CHAIN'):obj.estimate()


    def test_store_lookup_once_without_mutation_api(self):
        calls=[]
        class DurableDouble:
            @staticmethod
            def lookup(store,kind,key,identity):
                calls.append((store,kind,key,identity))
                return {'created':False,'payload':{'profile_json':b'fixture'}}
        view=object.__new__(s.StoreView);view.check=lambda:None
        view.store=object();view.durable=SimpleNamespace(DurableStore=DurableDouble)
        out=view.lookup('node','0'*64,{'identity':'fixture'})
        self.assertFalse(out['created']);self.assertEqual(len(calls),1)
        self.assertEqual(calls[0][1:],('node','0'*64,{'identity':'fixture'}))
        self.assertFalse(hasattr(s.StoreView,'acquire'));self.assertFalse(hasattr(s.StoreView,'commit'))

    def test_pending_lookup_error_propagates_without_retry(self):
        calls=[]
        class DurableDouble:
            @staticmethod
            def lookup(*args):
                calls.append(args)
                raise RuntimeError('PENDING_OR_UNCERTAIN_CLAIM_NO_RETRY')
        view=object.__new__(s.StoreView);view.check=lambda:None
        view.store=object();view.durable=SimpleNamespace(DurableStore=DurableDouble)
        with self.assertRaisesRegex(RuntimeError,'PENDING_OR_UNCERTAIN'):view.lookup('node','0'*64,{})
        self.assertEqual(len(calls),1)

    def test_failed_lookup_error_propagates_without_retry(self):
        calls=[]
        class DurableDouble:
            @staticmethod
            def lookup(*args):
                calls.append(args)
                raise RuntimeError('FAILED_OR_UNCERTAIN_CLAIM_NO_RETRY')
        view=object.__new__(s.StoreView);view.check=lambda:None
        view.store=object();view.durable=SimpleNamespace(DurableStore=DurableDouble)
        with self.assertRaisesRegex(RuntimeError,'FAILED_OR_UNCERTAIN'):view.lookup('node','0'*64,{})
        self.assertEqual(len(calls),1)

if __name__ == '__main__':
    raise SystemExit('PREPARED_NOT_AUTHORIZED_TO_RUN_AUTOMATICALLY')
