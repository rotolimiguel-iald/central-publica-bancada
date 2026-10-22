"""I02 persisted profiles -> qualified V2 estimates; no numerical recomputation."""
from itertools import product
import math
import os
from pathlib import Path
import time
from store_bridge import (ReadbackError, need, canonical, sha, digest, decode, pin,
    RegistryVerifier, StoreView, ReadContext, derive_context, external_completion, read_budget)

class Recovery:
    """Trusted intake pins are supplied by the external admission, not this store.

    No file is created. Caller opens/closes existing ProtectedDirectory and
    DurableStore instances and owns the already loaded reader registry.
    """
    def __init__(self, *, intake_raw, intake_sha256, registry, reader_bindings,
                 stores, protected_roots, metadata, external_evidence,
                 bridge_module, registry_module, deadline, clock=time.monotonic):
        need(sha(intake_raw) == intake_sha256, 'ADMITTED_INTAKE_PIN')
        self.intake, self.registry, self.bridge = decode(intake_raw), registry, bridge_module
        self.intake_sha256 = intake_sha256
        self.clock, self.deadline = clock, deadline
        self.checkpoint()
        a = self.intake
        need(a['schema'] == 'F9_PROFILE_READBACK_INTAKE_V1'
             and a['scope'] == 'SYNTHETIC_ENGINEERING_READBACK_ONLY', 'READBACK_SCOPE')
        need(type(a['level']) is int and type(a['max_records']) is int, 'EXPLICIT_LEVEL_AND_READ_CAP')
        self.live = RegistryVerifier(registry, reader_bindings, bridge_module, self.checkpoint, registry_module)
        m = registry.modules
        required = {'profile','theta','tail','reducer','node','assembler','consumer','prior',
                    'precision','durable','protocol','supervisor_port','bridge','frozen',
                    'threshold','store_bridge','store_contract','recovery','registry'}
        need(required <= set(reader_bindings), 'ALL_READER_DEPENDENCIES_BOUND')
        need(reader_bindings == a['reader_bindings'], 'ADMITTED_READER_BINDINGS')
        self.modules = m
        need(set(stores) == {'nodes','runs'} and set(protected_roots) == {'nodes','runs','unit'}, 'EXACT_STORES')
        self.root = protected_roots['unit']
        need(type(self.root) is m['protocol'].ProtectedDirectory, 'EXACT_UNIT_ROOT_CLASS')
        self.roots = protected_roots
        self.views = {role:StoreView(stores[role], protected_roots[role],
            durable_module=m['durable'], protocol_module=m['protocol'],
            expected_path=a['roots'][role]['path'], expected_identity=a['roots'][role]['identity'],
            checkpoint=self.checkpoint) for role in stores}
        self.root_check()
        self.documents = external_completion(evidence=external_evidence, expected=a['external_pins'],
            parent_exit_pointers=a['parent_exit_pointers'], unit=a['execution_unit_id'])
        # Actual protected store files must match the externally admitted bytes.
        for role,name in (('admission','admission.json'),('terminal','terminal_candidate.json'),
                          ('seal','completion_seal.json'),('child_stdout','child_stdout.json')):
            observed=m['protocol'].read_bytes(self.root.path+'/'+name, a['external_pins'][role]['bytes'])
            need(observed == external_evidence[role], 'EXTERNAL_RECORD_NOT_FROM_PROTECTED_RUN')
        self.external_evidence = dict(external_evidence)
        self.metadata = dict(metadata)
        self._read_run()
        self.live.check()

    def checkpoint(self):
        now = self.clock()
        need(type(now) in (int,float) and math.isfinite(now)
             and type(self.deadline) in (int,float) and math.isfinite(self.deadline)
             and now < self.deadline, 'READBACK_DEADLINE')

    def root_check(self):
        self.checkpoint()
        need(set(vars(self.root)) == {'path','identity','fd'}, 'UNIT_ROOT_INSTANCE_OVERRIDES')
        self.modules['protocol'].ProtectedDirectory.check(self.root)
        expected = self.intake['roots']['unit']
        need(self.root.path == expected['path'] and tuple(self.root.identity) == tuple(expected['identity']), 'UNIT_ROOT_IDENTITY')
        need(not os.path.lexists(self.root.path+'/failure.json'), 'ORIGINAL_PARENT_FAILURE')
        unit = self.intake['execution_unit_id']
        need(Path(self.root.path).name == unit, 'ORIGINAL_UNIT_PATH')
        for role in ('nodes','runs'):
            need(self.views[role].expected_path == self.root.path+'/'+role, 'NO_ALTERNATE_STORE_ROOT')
            self.views[role].check()
        self.checkpoint()

    def artifact(self, name):
        need(name in self.request['artifact_pins'] and name in self.metadata, 'ORIGINAL_METADATA_NOT_RETAINED:'+name)
        return pin(self.metadata[name], self.request['artifact_pins'][name])

    def _read_run(self):
        a, docs = self.intake, self.documents
        child, terminal = docs['child_stdout'], docs['terminal']
        identity = {'schema':'F9_CONTROLLER_RUN_IDENTITY_V1','execution_unit_id':a['execution_unit_id'],
                    'request_sha256':child['request_sha256'],'decision_sha256':child['decision_sha256']}
        key = digest({'controller_execution_unit_id':a['execution_unit_id']})
        ticket = self.views['runs'].lookup('node', key, identity)
        need(ticket['claim_sha256'] == a['run_claim_sha256'] and ticket['result_sha256'] == a['run_result_sha256'],
             'ADMITTED_GLOBAL_COMMIT_PINS')
        files = ticket['payload']
        expected = {'controller_result.json','supervisor_terminal.json','request.json','decision.json'}
        expected.update('coupling_'+str(i)+'.json' for i in range(600))
        need(set(files) == expected, 'EXACT_GLOBAL_COMMITTED_FILES')
        request, decision, result = (decode(files[n]) for n in ('request.json','decision.json','controller_result.json'))
        need(sha(files['request.json']) == identity['request_sha256'] == result['request_sha256']
             and sha(files['decision.json']) == identity['decision_sha256'] == result['decision_sha256'], 'GLOBAL_REQUEST_DECISION')
        need(result == child['result'] and result['status'] == 'ENGINEERING_ONLY'
             and result['schema'] == 'F9_CONTROLLER_ENGINEERING_RESULT_V1'
             and result['execution_unit_id'] == a['execution_unit_id']
             and result['complete_declared_family'] is True
             and result['acceptance'] == 'REQUIRES_EXTERNAL_EXIT_AND_CLEANUP_VERIFICATION', 'GLOBAL_RESULT_EXTERNAL_BINDING')
        need(decision['schema'] == 'F9_INTEGRATED_ROOT_DECISION_V1'
             and decision['scope'] == 'F9_FULL_PRIOR_SYNTHETIC_ENGINEERING_ONLY'
             and decision['may_read_observations'] is False
             and decision['execution_unit_id'] == a['execution_unit_id'], 'ORIGINAL_SYNTHETIC_DECISION')
        need(request['schema'] == 'F9_CONTROLLER_REQUEST_V1' and request['execution_unit_id'] == a['execution_unit_id']
             and request['store_root'] == self.views['nodes'].expected_path
             and request['run_store_root'] == self.views['runs'].expected_path, 'ORIGINAL_REQUEST_STORE_PATHS')
        need([r['scenario_id'] for r in request['scenarios']] == list(self.bridge.SCENARIOS)
             and [r['scenario_id'] for r in result['scenarios']] == list(self.bridge.SCENARIOS), 'EXACT_600_ORDER')
        self.request, self.result, self.run_files = request, result, files
        count = read_budget(a['level'],a['max_records'],self.modules['theta'].MAX_LEVEL)
        ref = terminal['integrated_reference']
        need(ref['schema'] == 'F9_INTEGRATED_EXTERNAL_REFERENCE_V1' and ref['node_count'] == count, 'EXTERNAL_FULL_NODE_COUNT')
        need(result['counts']['callback_attempts'] == result['counts']['callback_returns'] == count, 'ORIGINAL_CALLBACK_COUNTS')
        self.audit = self.modules['supervisor_port'].validate_terminal(files['supervisor_terminal.json'],
            execution_unit_id=a['execution_unit_id'], request_sha256=identity['request_sha256'],
            decision_sha256=identity['decision_sha256'], runtime_sha256=result['runtime_sha256'],
            supervisor_pin=decision['supervisor_adapter_pin'],
            new_solver_attempts=result['counts']['new_solver_attempts'], new_solver_returns=result['counts']['new_solver_returns'])
        need(sha(files['supervisor_terminal.json']) == result['supervisor_terminal_sha256']
             and self.audit['nonce'] == terminal['launch_nonce']
             and self.audit['process_identity'] == child['process_identity'], 'ACTUAL_SUPERVISOR_TERMINAL')
        need(decision['runtime_inventory_sha256'] == result['runtime_sha256'], 'ORIGINAL_RUNTIME_IDENTITY')
        self.contexts, self.read_contexts = {}, {}
        self._prepare_contexts()

    def _prepare_contexts(self):
        for index,spec in enumerate(self.request['scenarios']):
            self.checkpoint()
            sid = spec['scenario_id']
            consumer_raw, plan_raw = self.artifact(spec['consumer_admission']), self.artifact(spec['theta_plan'])
            adm, plan = decode(consumer_raw), decode(plan_raw)
            need(adm['source_pins'] == self.modules['consumer'].SOURCE_PINS, 'CONSUMER_SOURCE_LINEAGE')
            need(plan['execution_unit_id'] == self.intake['execution_unit_id']+':'+sid
                 and plan['last_level'] == self.intake['level'], 'ADMITTED_FINEST_LEVEL_ONLY')
            support_sha = adm['references']['fixed_affine_support']['sha256']
            candidates = [name for name,p in self.request['artifact_pins'].items() if p['sha256'] == support_sha]
            need(candidates, 'ORIGINAL_SUPPORT_REFERENCE_NOT_PINNED')
            support_raw = self.artifact(candidates[0])
            ctx = derive_context(consumer_raw=consumer_raw,plan_raw=plan_raw,request=self.request,spec=spec,support_raw=support_raw)
            structure_raw = self.artifact(spec['structure'])
            need(sha(structure_raw) == ctx['X_response_sha256'], 'ADMITTED_STRUCTURE_BYTES')
            self.modules['consumer']._structure(decode(structure_raw))
            coupling = self.run_files['coupling_'+str(index)+'.json']
            expected = {**decode(self.artifact(spec['coupling_template'])),
                'external_execution_authorization_reference':{'id':self.intake['execution_unit_id']+':root-decision',
                    'sha256':sha(self.run_files['decision.json'])}}
            need(decode(coupling) == expected and sha(coupling) == self.result['scenarios'][index]['coupling_admission_sha256'], 'EXACT_ORIGINAL_COUPLING')
            need(expected['runtime_sha256'] == self.result['runtime_sha256']
                 and expected['background_scope_id'] == self.intake['execution_unit_id']+':background', 'COUPLING_RUNTIME_SCOPE')
            configuration = self.request['artifact_pins'][self.request['global_artifacts']['engine_configuration']]['sha256']
            need(plan['engine_configuration_sha256'] == configuration
                 and plan['assembly_admission_sha256'] == self.request['artifact_pins'][self.request['global_artifacts']['assembly_admission']]['sha256'], 'GLOBAL_PLAN_PINS')
            self.contexts[sid] = ctx
            self.read_contexts[sid] = ReadContext(modules=self.modules,coupling_raw=coupling,plan_raw=plan_raw,consumer_raw=consumer_raw)
        need(tuple(self.contexts) == self.bridge.SCENARIOS, 'FULL_CONTEXT_ORDER')

    def _records(self):
        """Deterministic full finest plan; final next() authenticates entire chain."""
        self.root_check(); self.live.check()
        n = 1 << self.intake['level']
        chain, seen = {}, set()
        for index,sid in enumerate(self.bridge.SCENARIOS):
            ctx = self.read_contexts[sid]
            validator = ctx._validator()
            for indices in product(range(n+1), repeat=3):
                self.checkpoint()
                key = self.modules['theta']._node_key(indices,n)
                desc = ctx.descriptor(validator._descriptor(key))
                identity = ctx.node_identity(desc)
                node = self.views['nodes'].lookup('node', desc['node_id'], identity)
                name = 'node_'+desc['node_id']+'.claim.json'
                need(name not in seen, 'DUPLICATE_EXPECTED_NODE')
                seen.add(name);chain[name] = node['result_sha256']
                bg_identity = ctx.background_identity(desc)
                bg = self.views['nodes'].lookup('background', digest(bg_identity), bg_identity)
                reference = ctx.background(bg['payload'], bg_identity, bg['claim'])
                files = node['payload']
                need(set(files) == {'profile_json','assembly_json','precision_json','envelope_json'}, 'EXACT_PROFILE_NODE_PAYLOAD')
                envelope = ctx.decode_envelope(files['envelope_json'])
                ctx.validate(envelope,desc,files['assembly_json'],files['precision_json'],bg['payload'],reference)
                # Reuse one validator per scenario to retain normalization/duplicate checks.
                validator._accept(envelope,desc)
                ctx.validate_profile(files['profile_json'],desc,sha(files['assembly_json']))
                need(self.modules['consumer'].extract_structure(files['assembly_json'],assembly_sha256=sha(files['assembly_json']))
                     == self.artifact(self.request['scenarios'][index]['structure']), 'ASSEMBLY_STRUCTURE_IDENTITY')
                need(decode(files['profile_json'])['provenance']['background_sha256'] == sha(bg['payload']['packet_json']), 'PROFILE_BACKGROUND_CHAIN')
                yield sid,key,files['profile_json'],sha(files['profile_json']),sha(files['assembly_json']),sha(bg['payload']['packet_json'])
        expected = self.documents['terminal']['integrated_reference']
        need(len(chain) == expected['node_count'] and digest([chain[name] for name in sorted(chain)])
             == expected['node_result_chain_sha256'], 'ORIGINAL_EXTERNAL_NODE_CHAIN')
        self.root_check(); self.live.check()

    def estimate(self):
        self.root_check();self.live.check()
        # No semantic verifier is supplied: this API cannot request a verdict.
        bridge = self.bridge.Bridge(modules={k:self.modules[k] for k in ('profile','theta','tail','reducer')},
            object_verifier=self.live,object_verifier_sha256=self.live.bindings['store_bridge']['sha256'],
            deadline=self.deadline,clock=self.clock)
        result = bridge.estimate_family(self._records(), contexts=self.contexts,
            level=self.intake['level'],max_records=self.intake['max_records'])
        self.root_check();self.live.check();self.checkpoint()
        need(result['status'] == 'ENGINEERING_ONLY' and result['verdict'] is None
             and result['certified_bounds'] is None, 'ESTIMATE_SCOPE')
        return {'schema':'F9_PROFILE_READBACK_RESULT_V1','status':'SYNTHETIC_ENGINEERING_ONLY',
            'intake_sha256':self.intake_sha256,'original_unit':self.intake['execution_unit_id'],
            'original_completion_seal_sha256':sha(self.external_evidence['seal']),
            'original_node_result_chain_sha256':self.documents['terminal']['integrated_reference']['node_result_chain_sha256'],
            'reader_objects_scope':'CURRENT_READER_OBJECTS_NOT_TERMINATED_PRODUCER_OBJECTS',
            'contexts':self.contexts,'estimates':result,
            'solver_calls':0,'numerical_recomputation':False,'observed_access':False,
            'certified_bounds':None,'p':None,'sigma':None,'verdict':None}

if __name__ == '__main__':
    raise SystemExit('PREPARATION_ONLY_NO_LAUNCH')
