"""Read-only custody helpers. No loader, supervisor, solver or execution entrypoint."""
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace, MethodType
import store_contract
from store_contract import SOURCE_PINS

class ReadbackError(ValueError):
    pass

def need(ok, code):
    if not ok:
        raise ReadbackError(code)

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(',', ':'), allow_nan=False).encode('ascii')

def sha(raw):
    need(type(raw) is bytes, 'BYTES_REQUIRED')
    return hashlib.sha256(raw).hexdigest()

def digest(value):
    return sha(canonical(value))

def decode(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, 'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def bad(_):
        raise ReadbackError('NONFINITE_JSON')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)

def pin(raw, expected):
    need(type(expected) is dict and set(expected) == {'bytes', 'sha256'}, 'PIN_FIELDS')
    need(type(expected['bytes']) is int and expected['bytes'] >= 0, 'PIN_BYTES')
    need(len(raw) == expected['bytes'] and sha(raw) == expected['sha256'], 'PIN_MISMATCH')
    return raw

def pointer(doc, path):
    need(type(path) is str and path.startswith('/'), 'EXTERNAL_RECORD_POINTER_REQUIRED')
    for part in path[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        doc = doc[int(part)] if type(doc) is list else doc[part]
    return doc

def read_budget(level, cap, maximum):
    need(type(level) is int and 1 <= level <= maximum, 'ADMITTED_LEVEL_RANGE')
    required = 600*((1 << level)+1)**3
    need(type(cap) is int and cap == required, 'EXPLICIT_FINEST_READ_BUDGET')
    return required

class RegistryVerifier:
    """Checks the READER's actual objects; never claims producer objects survived.

    The supplied registry and admitted reader bindings are a trusted bootstrap
    boundary. Existing registry checks identity/code plus sampled native maps,
    not arbitrary globals, closures, native syscalls or hostile same-UID writes.
    """
    def __init__(self, registry, bindings, bridge_module, checkpoint, registry_module):
        self.registry, self.bindings = registry, json.loads(canonical(bindings))
        self.registry_module = registry_module
        self.registry_type = registry_module.LoadedRegistry
        self.registry_check = self.registry_type.check
        self.registry_check_code = self.registry_check.__code__
        need(type(registry) is self.registry_type, "TRUSTED_BOOTSTRAP_REGISTRY_TYPE")
        self.bridge, self.checkpoint = bridge_module, checkpoint
        self.check()

    def check(self):
        self.checkpoint()
        need(self.registry_type.check is self.registry_check and self.registry_check.__code__ is self.registry_check_code, 'REGISTRY_CHECK_REPLACED')
        self.registry_check(self.registry, deep=True)
        for role, binding in self.bindings.items():
            if role == 'registry':
                module = self.registry_module
                raw = module.pinned(module.__file__, {k:binding[k] for k in ('bytes','sha256')}, binding['bytes'])
                source = {'file':module.__file__, 'sha256':sha(raw)}
            else:
                source = self.registry.sources[role]
                module = self.registry.modules[role]
            need(source['file'] == binding['path'] == module.__file__, 'READER_PATH_BINDING')
            need(source['sha256'] == binding['sha256'], 'READER_BYTES_BINDING')
            admitted = self.registry.policy.read_pins[binding['path']]
            need(admitted == {k:binding[k] for k in ('bytes', 'sha256')}, 'READER_POLICY_PIN')
            if role in SOURCE_PINS:
                need(all(binding[k] == SOURCE_PINS[role][k] for k in ('bytes', 'sha256')),
                     'NON_EQUIVALENT_READER_SOURCE')
        need(type(self.registry) is self.registry_type and self.registry_module.LoadedRegistry is self.registry_type,
             'EXACT_REGISTRY_CLASS')
        need(self.registry.modules['store_contract'] is store_contract and SOURCE_PINS is store_contract.SOURCE_PINS, 'STORE_CONTRACT_MODULE_BINDING')
        need(self.registry.modules['bridge'] is self.bridge, 'BRIDGE_OBJECT_REPLACED')
        need(self.bridge.threshold_audit is self.registry.modules['threshold'], 'THRESHOLD_GLOBAL_MODULE')
        self.checkpoint()

    def __call__(self, modules, pins):
        self.check()
        need(set(modules) == {'profile', 'theta', 'tail', 'reducer'}, 'BRIDGE_MODULE_ROLES')
        for role, module in modules.items():
            need(self.registry.modules[role] is module, 'MODULE_SWAPPED')
            # Canonical provenance paths may differ from the executed copy.
            need(pins[role] == self.bridge.SOURCE_PINS[role], 'CANONICAL_SOURCE_BINDING')
            need(all(self.bindings[role][k] == pins[role][k] for k in ('bytes', 'sha256')),
                 'COPY_BYTES_NOT_EQUIVALENT')
        return self.bridge.Receipt('LOADED_OBJECTS', self.bridge.digest(pins),
            tuple(sorted(p['sha256'] for p in pins.values())),
            self.bindings['store_bridge']['sha256'], 'LOADED_OBJECTS_ONLY')

class StoreView:
    """Existing DurableStore.lookup only: it fsyncs but never publishes files.

    No Windows emulation and no acquire/commit/fail/repair exposed here.
    The caller owns and closes the existing protected handle and store.
    """
    def __init__(self, store, protected, *, durable_module, protocol_module,
                 expected_path, expected_identity, checkpoint):
        need(os.name == 'posix', 'READBACK_REQUIRES_REAL_POSIX')
        need(type(store) is durable_module.DurableStore, 'EXACT_DURABLE_CLASS')
        need(type(protected) is protocol_module.ProtectedDirectory, 'EXACT_PROTECTED_CLASS')
        need(set(vars(store)) == {'root', 'cap'}, 'STORE_INSTANCE_OVERRIDES')
        need(set(vars(protected)) == {'path', 'identity', 'fd'}, 'DIRECTORY_INSTANCE_OVERRIDES')
        self.store, self.protected = store, protected
        self.durable, self.protocol, self.checkpoint = durable_module, protocol_module, checkpoint
        self.expected_path, self.expected_identity = expected_path, tuple(expected_identity)
        self.check()

    def check(self):
        self.checkpoint()
        self.protocol.ProtectedDirectory.check(self.protected)
        need(str(self.store.root) == self.protected.path == self.expected_path, 'STORE_PATH_BINDING')
        need(tuple(self.protected.identity) == self.expected_identity, 'STORE_DEVICE_INODE_UID_MODE')
        need(set(vars(self.store)) == {'root', 'cap'} and set(vars(self.protected)) == {'path','identity','fd'}, 'STORE_INSTANCE_OVERRIDES')
        self.checkpoint()

    def lookup(self, kind, key, identity):
        self.check()
        row = self.durable.DurableStore.lookup(self.store, kind, key, identity)
        self.check()
        need(row['created'] is False, 'READBACK_MUST_NOT_CREATE')
        return row

class ReadContext:
    """Metadata-only facade using existing NodeContext validation methods.

    joint is NOT a PreparedJoint, contains no arrays, and cannot evaluate.
    No constructor of NodeContext or prepare_joint is invoked.
    """
    ALLOWED = frozenset(('_validator', '_precision_doc', 'descriptor', 'node_identity',
        'background_identity', 'background', 'validate_profile', 'validate', 'decode_envelope'))

    def __init__(self, *, modules, coupling_raw, plan_raw, consumer_raw):
        self.node = modules['node']
        self.a, self.c, self.p, self.s, self.t = (modules[k] for k in
            ('assembler', 'consumer', 'prior', 'precision', 'theta'))
        self.profile = modules['profile']
        self.doc, self.doc_sha = decode(coupling_raw), sha(coupling_raw)
        self.plan_raw, self.plan_sha = plan_raw, sha(plan_raw)
        self.plan = decode(plan_raw)
        self.joint = SimpleNamespace(_admission=decode(consumer_raw), _admission_sha256=sha(consumer_raw))
        need(self.doc['schema'] == 'F9_NODE_COUPLING_ADMISSION_V1'
             and self.doc['preparation_request_id'] == self.node.REQUEST_ID
             and self.doc['source_pins'] == self.node.SOURCE_PINS
             and self.doc['theta_plan_sha256'] == self.plan_sha
             and self.doc['profile_enabled'] is True, 'ORIGINAL_PROFILE_COUPLING_REQUIRED')
        need(self.plan['consumer_admission_sha256'] == sha(consumer_raw)
             and self.joint._admission['prediction_admission_sha256'] == self.plan['assembly_admission_sha256'],
             'READ_CONTEXT_ORIGINAL_ADMISSIONS')
        self._validator()  # Constructor validates plan; callback always forbidden.

    def __getattr__(self, name):
        need(name in self.ALLOWED, 'READ_CONTEXT_OPERATION_FORBIDDEN')
        return MethodType(getattr(self.node.NodeContext, name), self)


def derive_context(*, consumer_raw, plan_raw, request, spec, support_raw):
    """All identities originate in authenticated request/admission, never profiles."""
    adm, plan = decode(consumer_raw), decode(plan_raw)
    pin(consumer_raw, request['artifact_pins'][spec['consumer_admission']])
    pin(plan_raw, request['artifact_pins'][spec['theta_plan']])
    need(adm['schema'] == 'F9_CONSUMER_ADMISSION_V1' and adm['data_kind'] == 'SYNTHETIC'
         and adm['scope'] == 'ENGINEERING_POINTWISE_ONLY'
         and adm['scenario_id'] == spec['scenario_id'], 'SYNTHETIC_ADMISSION_ONLY')
    need(plan['consumer_admission_sha256'] == sha(consumer_raw), 'PLAN_CONSUMER_BINDING')
    support_sha = adm['references']['fixed_affine_support']['sha256']
    need(sha(support_raw) == support_sha and any(p['sha256'] == support_sha
         and p['bytes'] == len(support_raw) for p in request['artifact_pins'].values()), 'SUPPORT_REFERENCE_BYTES')
    for field, source in (('y_native','y_native_f64le'),('C_native','C_native_f64le'),
                          ('row_ids','row_ids_canonical_json'),('affine_origin_native','affine_origin_native_f64le')):
        need(request['artifact_pins'][spec[field]]['sha256'] == adm['input_sha256'][source],
             'ADMISSION_REQUEST_INPUT_LINEAGE')
    need(request['artifact_pins'][spec['structure']]['sha256'] == adm['structure_sha256'], 'STRUCTURE_REQUEST_BINDING')
    return {'data_sha256':adm['input_sha256']['y_native_f64le'],
            'covariance_sha256':adm['input_sha256']['C_native_f64le'],
            'X_response_sha256':adm['structure_sha256'], 'support_sha256':support_sha,
            'engine_config_sha256':plan['engine_configuration_sha256'],
            'consumer_admission_sha256':sha(consumer_raw)}


def external_completion(*, evidence, expected, parent_exit_pointers, unit):
    """Pins are externally admitted. No receipt or authorization is issued here.

    The original parent has no persisted schema for its own process exit.
    JSON pointers map an independently retained outer observation; absent fields
    are a real missing integration dependency, never a generated success.
    """
    need(set(evidence) == {'admission','terminal','seal','child_stdout','parent_stdout','parent_exit'},
         'COMPLETE_EXTERNAL_EVIDENCE_REQUIRED')
    need(set(expected) == set(evidence), 'EXTERNALLY_ADMITTED_PINS_REQUIRED')
    docs = {k:decode(pin(v, expected[k])) for k,v in evidence.items()}
    admission, terminal, seal, child, parent = (docs[k] for k in
        ('admission','terminal','seal','child_stdout','parent_stdout'))
    need(admission['schema'] == 'F9_INTEGRATED_UNIT_CONSUMPTION_V1'
         and terminal['schema'] == 'F9_INTEGRATED_EXTERNAL_TERMINAL_V1'
         and seal['schema'] == 'F9_INTEGRATED_COMPLETION_SEAL_V1'
         and child['schema'] == 'F9_INTEGRATED_CHILD_COMPLETE_V1', 'ORIGINAL_EXTERNAL_SCHEMAS')
    need(all(x['execution_unit_id'] == unit for x in (admission,terminal,child,parent)), 'EXTERNAL_UNIT')
    need(terminal['status'] == parent['status'] == 'SYNTHETIC_INTEGRATED_ENGINEERING_ACCEPTED', 'EXTERNAL_STATUS')
    need(terminal['child_exit_code'] == 0 and type(terminal['child_exit_code']) is int
         and terminal['direct_child_reaped'] is True and terminal['cleanup_uncertain'] is False
         and seal['direct_child_reaped'] is True and seal['cleanup_uncertain'] is False, 'CHILD_EXIT_CLEANUP')
    need(seal['acceptance_requires_parent_exit_zero_and_absent_failure'] is True, 'PARENT_EXIT_NOT_OPTIONAL')
    need(seal['terminal_sha256'] == sha(evidence['terminal'])
         and parent['completion_seal_sha256'] == sha(evidence['seal'])
         and terminal['stdout_pin'] == expected['child_stdout'], 'EXTERNAL_SEAL_BYTE_CHAIN')
    need(admission['launch_nonce'] == terminal['launch_nonce'] == child['launch_nonce']
         and admission['decision_sha256'] == terminal['decision_sha256'] == child['decision_sha256'], 'NONCE_DECISION_CHAIN')
    need(child['process_identity'] == {k:terminal['child_identity'][k] for k in ('pid','start_ticks')}, 'CHILD_PROCESS_CHAIN')
    need(terminal['physical_opening_authorized'] is False and terminal['automatic_retry'] is False
         and terminal['native_file_operations'] is None and terminal['native_network_operations'] is None,
         'EXTERNAL_SCOPE')
    for doc in (terminal,parent):
        need(all(doc[k] is None for k in ('p','sigma','verdict')), 'NO_SCIENTIFIC_TERMINAL')
    values = {'execution_unit_id':unit, 'completion_seal_sha256':sha(evidence['seal']),
              'parent_stdout_sha256':sha(evidence['parent_stdout']), 'exit_code':0, 'reaped':True}
    need(set(parent_exit_pointers) == set(values), 'OUTER_EXIT_MAPPING_REQUIRED')
    for key,value in values.items():
        actual = pointer(docs['parent_exit'], parent_exit_pointers[key])
        need(type(actual) is type(value) and actual == value, 'OUTER_PARENT_EXIT_BINDING:'+key)
    need(seal['entry_monotonic'] == admission['entry_monotonic']
         and seal['deadline'] == admission['deadline']
         and parent['wall_after_seal_persistence_s'] < admission['deadline']-admission['entry_monotonic'], 'ORIGINAL_FINISH_DEADLINE')
    return docs

if __name__ == '__main__':
    raise SystemExit('PREPARATION_ONLY_NO_EXECUTION_COMMAND')
