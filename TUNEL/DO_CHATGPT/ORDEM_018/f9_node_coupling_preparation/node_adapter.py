"""Pure in-memory F9 node coupling. Prepared only; no runtime launched here."""
import math

REQUEST_ID = '1fe78df6-efb2-4c57-93bd-499ad85d8b15'
# BEGIN SOURCE PINS
SOURCE_PINS = {'dependency_board': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\preregistros\\f9_completion_dependencies\\QUADRO_F9_ATE_V1.md', 'bytes': 36718, 'sha256': 'c965992156debd0508eaf2f4afeb937ecca1ceb96b5aba7577881d35d5813d56'}, 'assembler': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_five_model_assembly_preparation\\five_model_assembly.py', 'bytes': 17325, 'sha256': 'd65bc8be6123a0bca8ef6e47db10c85b89ff487d9c2edfd5cc6c465e84c4b87f'}, 'consumer': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_likelihood_consumer_preparation\\likelihood_consumer.py', 'bytes': 24982, 'sha256': '6776bb660f6b8565c7282f937ecdc5239d5b941cce3e257aa6155379c9ccd6a5'}, 'consumer_contract': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_likelihood_consumer_preparation\\CONTRATO_API.json', 'bytes': 8720, 'sha256': '9876fcdd3bdf38b86ca8d693ef3c6e1cdf94bace5276f21fd61d4dcc9389b5cb'}, 'prior': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_physical_prior_preparation\\physical_prior.py', 'bytes': 21629, 'sha256': '4fbae1160282875c4ed61c242361c14db9434416a1886d41905c79f0a4f7a3f6'}, 'prior_contract': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_physical_prior_preparation\\CONTRATO_API.json', 'bytes': 6777, 'sha256': '96dbd03f15ac8614eba760b8775145014d9684d1e51a5f63a1cad9303a0c1a03'}, 'precision': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_precision_services_preparation\\precision_services.py', 'bytes': 13442, 'sha256': '63f6adc987308cb14d986a07a9006610e0a304bb36d7d705f59e8c3874b7f278'}, 'theta': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_theta_integration_preparation\\theta_integrator.py', 'bytes': 27898, 'sha256': '9de620190aaf4987cd1abf00772737721945926054d80d99bb1f540184ca2682'}, 'profile': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_affine_profile_preparation\\affine_profile.py', 'bytes': 17121, 'sha256': '003d118e64a40ef58448b70296a4c25467bbf1fb7650a27ebdb422a419aa3b7f'}, 'layout': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_structural_layout_preparation\\LAYOUT_ESTRUTURAL_3CMB_13BAO.json', 'bytes': 16475, 'sha256': '7581c71fb1a548fc1e20110137a3e3d940e363725096485de837bac56d3a2317'}, 'design': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\h0dn_documentary_review\\linear_design\\ESPECIFICACAO_LINEAR.json', 'bytes': 109887, 'sha256': '9aca9fffe3c7788d3c8ef1411b1dfa5c908c7366ef32ad969b14e59492199a95'}, 'precision_theta_review': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\RECIBO_ROOT_REVISOES_PRECISAO_THETA_F9.json', 'bytes': 12157, 'sha256': '032fe4db047afc11c1d04f0558aead75e85415610c8fbd85fc7813327221a35a'}, 'background_execution_review': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\RECIBO_ROOT_PREDICAO_F9_REPARO_IMPORTS.json', 'bytes': 21845, 'sha256': '9907b4800cd0dd4bb7968fc63ccfd583fb8c86fc36fc62a59f9a97354dca7bb5'}, 'profile_review': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\RECIBO_ROOT_REVISAO_PERFIS_F9.json', 'bytes': 4567, 'sha256': '5cd2edb8192b6db76e6998d8c12f6003db54b0d182b92852f0933a33409e073e'}, 'supplier_receipt_schema_reference': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_engine_import_closure_repair_preparation\\worker.py', 'bytes': 14470, 'sha256': 'f10b972e529cff8d96e2f84d27bbc43c60d89ca82177ced89e43cd0cb283f8f3'}, 'background_engine_reference': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_background_prediction\\background_controls.py', 'bytes': 15896, 'sha256': 'c41aee4bcd1d8a137df8d7541e53738e68e9a77605ec8e51d4051459544265a2'}}
# END SOURCE PINS


class NodeContext:
    """Trusted pinned dependencies; filesystem/controller live in durable_nodes."""
    def __init__(self, joint, *, admission_json, admission_sha256,
                 theta_plan_json, theta_plan_sha256, assembly_admission_json,
                 design_json, layout_json, assembler_module, consumer_module,
                 prior_module, precision_module, theta_module, profile_module=None):
        self.a, self.c, self.p, self.s, self.t = (assembler_module, consumer_module,
                                                prior_module, precision_module, theta_module)
        c, a, p, t = self.c, self.a, self.p, self.t
        doc = c._json(admission_json, admission_sha256, 'node coupling admission')
        c._keys(doc, ('schema', 'preparation_request_id', 'source_pins', 'theta_plan_sha256',
                      'anchors', 'precision', 'runtime_sha256', 'background_scope_id',
                      'supplier_reference', 'loaded_objects_reference',
                      'external_execution_authorization_reference', 'resource_limits_reference',
                      'profile_enabled'), 'node admission')
        c._require(doc['schema'] == 'F9_NODE_COUPLING_ADMISSION_V1' and
                   doc['preparation_request_id'] == REQUEST_ID and doc['source_pins'] == SOURCE_PINS,
                   'NODE_ADMISSION', 'frozen coupling identity')
        c._require(c.REQUEST_ID == 'a9874f79-9d71-48f5-824c-d51d6d819534' and
                   p.REQUEST_ID == 'df482198-56c4-4169-ae5e-3908f5d12f2c' and
                   t.REQUEST_ID == 'ad02511d-1536-4a1b-a6c4-fb3e5eb26550' and
                   isinstance(joint, c.PreparedJoint), 'NODE_DEPENDENCIES', 'pinned injected modules')
        for name in ('supplier_reference', 'loaded_objects_reference',
                     'external_execution_authorization_reference', 'resource_limits_reference'):
            c._reference(doc[name], name)
        c._digest(doc['runtime_sha256'], 'runtime')
        c._text(doc['background_scope_id'], 'background execution scope')
        c._require(doc['background_scope_id'] not in (REQUEST_ID,
                   'c4359a48-bf7c-4dd5-a753-8c3413774cdf', 'ffd6ccba-cd70-4747-aceb-a10003dfb7f4'),
                   'CONSUMED_SCOPE', 'preparation/consumed single-point unit cannot authorize a grid')
        c._require(doc['theta_plan_sha256'] == theta_plan_sha256, 'NODE_PLAN', 'same theta plan')
        self.plan_raw, self.plan_sha = theta_plan_json, theta_plan_sha256
        probe = self._validator()
        plan = probe._plan
        c._require(plan['consumer_admission_sha256'] == joint._admission_sha256 and
                   plan['common_measure_id'] == joint._admission['common_measure_id'],
                   'NODE_CONTEXT_CHANGED', 'fixed joint/context/measure')
        ad = c._json(assembly_admission_json, plan['assembly_admission_sha256'], 'grid structural admission')
        c._keys(ad, ('schema', 'status', 'layout_sha256', 'sources',
                     'engine_configuration_sha256', 'runtime_sha256'), 'assembly admission')
        c._require(ad['schema'] == 'F9_ASSEMBLY_ADMISSION_V1' and
                   ad['status'] == 'ENGINEERING_STRUCTURAL_ADMISSION' and
                   ad['sources'] == a.SOURCE_PINS and ad['engine_configuration_sha256'] == plan['engine_configuration_sha256']
                   and ad['runtime_sha256'] == doc['runtime_sha256'], 'NODE_ASSEMBLY_ADMISSION', 'global configuration')
        c._require(c._sha(layout_json) == SOURCE_PINS['layout']['sha256'] == ad['layout_sha256']
                   and c._sha(design_json) == SOURCE_PINS['design']['sha256'], 'NODE_STRUCTURAL_PINS', 'layout/design bytes')
        c._keys(doc['anchors'], ('beta', 's', 'rd_Mpc'), 'explicit physical reference anchors')
        anchors = {key: c._number(value, key) for key, value in doc['anchors'].items()}
        c._require(all(a.BOUNDS[k][0] <= value <= a.BOUNDS[k][1] for k, value in anchors.items()),
                   'NODE_ANCHOR_DOMAIN', 'no default/inferred anchors')
        c._keys(doc['precision'], ('services', 'max_quadrature_evaluations', 'max_window_evaluations',
                                   'absolute_log_error_target', 'absolute_scaled_error_target',
                                   'relative_scaled_error_target', 'caller_verification_reference'), 'precision template')
        # Only template fields exist before assembly; never invent an assembly hash.
        for name in ('max_quadrature_evaluations', 'max_window_evaluations'):
            value = doc['precision'][name]
            c._require(type(value) is int and 1 <= value <= 1000000, 'NODE_PRECISION_BUDGET', name)
        for name in ('absolute_log_error_target', 'absolute_scaled_error_target', 'relative_scaled_error_target'):
            c._require(c._number(doc['precision'][name], name) > 0, 'NODE_PRECISION_TARGET', name)
        c._reference(doc['precision']['caller_verification_reference'], 'loaded precision services')
        c._keys(doc['precision']['services'], ('log_exp_quad_interval', 'positive_quad_1d'), 'precision services')
        expected_services = {'log_exp_quad_interval': self.s.LOG_SERVICE_ID,
                             'positive_quad_1d': self.s.QUAD_SERVICE_ID}
        for name, service_id in expected_services.items():
            c._require(doc['precision']['services'][name] ==
                       {'id': service_id, 'sha256': SOURCE_PINS['precision']['sha256']},
                       'NODE_SERVICE_IDENTITY', 'same verified precision module')
        c._require(type(doc['profile_enabled']) is bool, 'NODE_PROFILE_OPTION', 'explicit boolean required')
        c._require(not doc['profile_enabled'] or getattr(profile_module, 'REQUEST_ID', None) ==
                   '4eea0cfb-0a3e-4b38-abcd-37bddbf5bbe3', 'NODE_PROFILE_IDENTITY', 'reviewed pinned I05')
        self.profile = profile_module
        self.joint, self.doc, self.doc_sha, self.plan = joint, doc, admission_sha256, plan
        self.assembly_admission_raw = assembly_admission_json
        self.design, self.layout, self.anchors = design_json, layout_json, anchors
        self.services = {name: getattr(self.s, name) for name in expected_services}

    def _validator(self):
        # A real, fresh instance solely reuses its pinned admission/_accept checks.
        # Its run() and numerical grid are never called by this adapter.
        def forbidden(_):
            raise RuntimeError('validation instance cannot execute a node')
        return self.t.ThetaIntegrator(self.plan_raw, plan_sha256=self.plan_sha, evaluate_node=forbidden)

    def _precision_doc(self, doc, joint, assembly_sha):
        return {'schema': 'F9_PHYSICAL_PRIOR_PRECISION_V1', 'source_pins': self.p.SOURCE_PINS,
                'consumer_admission_sha256': joint._admission_sha256, 'assembly_sha256': assembly_sha,
                **doc['precision']}

    def descriptor(self, descriptor):
        c, t = self.c, self.t
        c._keys(descriptor, ('execution_unit_id', 'consumer_admission_sha256', 'callback_reference',
                            'assembly_admission_sha256', 'engine_configuration_sha256',
                            'dyadic_numerators', 'dyadic_denominator', 'node_id', 'theta',
                            'theta_names', 'five_models'), 'theta node descriptor')
        n, nums = descriptor['dyadic_denominator'], descriptor['dyadic_numerators']
        c._require(type(n) is int and 1 <= n <= 1 << self.plan['last_level'] and n & (n-1) == 0
                   and type(nums) is list and len(nums) == 3 and
                   all(type(x) is int and 0 <= x <= n for x in nums), 'NODE_GRID', 'canonical dyadic coordinate')
        key = t._node_key(tuple(nums), n)
        c._require(key == (*nums, n), 'NODE_GRID', 'descriptor must use reduced node identity')
        expected = self._validator()._descriptor(key)
        c._require(c._canonical(descriptor) == c._canonical(expected), 'NODE_IDENTITY', 'exact plan descriptor')
        return expected

    def node_identity(self, descriptor):
        return {'descriptor': descriptor, 'coupling_admission_sha256': self.doc_sha,
                'theta_plan_sha256': self.plan_sha}

    def background_identity(self, descriptor):
        return {'schema': 'F9_SHARED_BACKGROUND_IDENTITY_V1',
                'scope_id': self.doc['background_scope_id'], 'theta': descriptor['theta'],
                'engine_configuration_sha256': self.plan['engine_configuration_sha256'],
                'runtime_sha256': self.doc['runtime_sha256'],
                'engine_sha256': self.a.SOURCE_PINS['background_engine']['sha256'],
                'protocol_sha256': self.a.SOURCE_PINS['background_protocol']['sha256'],
                'supplier_reference': self.doc['supplier_reference']}

    def background_request(self, identity, claim):
        return {'identity': identity, 'claim_nonce': claim['token'],
                'external_execution_authorization_reference': self.doc['external_execution_authorization_reference'],
                'resource_limits_reference': self.doc['resource_limits_reference'],
                'loaded_objects_reference': self.doc['loaded_objects_reference']}

    def background(self, payload, identity, claim):
        c = self.c
        c._keys(payload, ('packet_json', 'result_json', 'receipt_json'), 'original background bytes')
        docs, hashes = {}, {}
        for name, raw in payload.items():
            hashes[name] = c._sha(raw)
            docs[name] = c._json(raw, hashes[name], name)
        packet, result, receipt = docs['packet_json'], docs['result_json'], docs['receipt_json']
        c._keys(packet, ('schema', 'status', 'identity', 'result', 'error'), 'background packet')
        c._require(packet['schema'] == 'F9_BACKGROUND_PACKET_V1' and packet['status'] == 'ENGINEERING_RESULT'
                   and packet['error'] is None and c._canonical(packet['result']) == c._canonical(result),
                   'BACKGROUND_PACKET_MISMATCH', 'original result retained')
        ident = packet['identity']
        for name in ('theta', 'runtime_sha256', 'engine_configuration_sha256', 'engine_sha256', 'protocol_sha256'):
            c._require(ident[name] == identity[name], 'BACKGROUND_BINDING', name)
        c._require(ident['execution_receipt_sha256'] == hashes['receipt_json']
                   and receipt['background_result_sha256'] == hashes['result_json']
                   and result['theta'] == identity['theta'], 'BACKGROUND_HASH_CHAIN', 'original byte bindings')
        c._require(receipt['status'] == 'ENGINEERING_BACKGROUND_RETURNED'
                   and receipt['request_id'] == identity['scope_id'] and receipt['nonce'] == claim['token']
                   and receipt['configuration_sha256'] == identity['engine_configuration_sha256']
                   and receipt['runtime_sha256'] == identity['runtime_sha256']
                   and receipt['observed_reads'] is False and receipt['uniform_error_bound'] is None,
                   'BACKGROUND_RECEIPT_MISMATCH', 'scope/nonce/runtime/configuration/engineering status')
        for name in ('solver_calls_attempted', 'solver_calls_returned'):
            c._require(type(receipt[name]) is int and receipt[name] == 1, 'BACKGROUND_COUNT', name)
        return {'id': identity['scope_id'] + ':' + claim['token'], 'sha256': hashes['receipt_json']}

    def compute(self, descriptor, background_payload, background_reference, *, origin):
        c = self.c
        common = dict(zip(self.a.THETA_NAMES, descriptor['theta']))
        parameters = {model: {**common, **{key: self.anchors[key] for key in self.a.EXTRAS[model]}}
                      for model in self.a.MODELS}
        assembled = self.a.assemble_five(parameters, design_json=self.design, layout_json=self.layout,
                        background_json=background_payload['packet_json'],
                        admission_json=self.assembly_admission_raw,
                        admission_sha256=self.plan['assembly_admission_sha256'])
        assembly_raw = c._canonical(assembled)
        assembly_sha = c._sha(assembly_raw)
        precision_raw = c._canonical(self._precision_doc(self.doc, self.joint, assembly_sha))
        conditional = self.p.integrate_at_fixed_theta(self.joint, assembly_raw, assembly_sha256=assembly_sha,
                        background_json=background_payload['packet_json'], consumer_module=c,
                        precision_json=precision_raw, precision_sha256=c._sha(precision_raw), services=self.services)
        receipt = {'node_id': descriptor['node_id'], 'execution_unit_id': descriptor['execution_unit_id'],
                   'callback_reference': descriptor['callback_reference'],
                   'conditional_result_reference': {'id': descriptor['node_id'] + ':conditional',
                        'sha256': self.t.canonical_conditional_sha256(conditional)},
                   'background_execution_reference': background_reference,
                   'background_attempts': 1, 'background_successes': 1, 'background_origin': origin,
                   'background_calls_this_callback': 1 if origin == 'NEW_EXECUTION' else 0,
                   'assembly_admission_sha256': self.plan['assembly_admission_sha256'],
                   'engine_configuration_sha256': self.plan['engine_configuration_sha256']}
        envelope = {'conditional_result': conditional, 'receipt': receipt}
        self.validate(envelope, descriptor, assembly_raw, precision_raw, background_payload, background_reference)
        encoded = {'conditional_result': self.t._json_ready(conditional), 'receipt': receipt}
        artifacts = {'envelope_json': c._canonical(encoded), 'assembly_json': assembly_raw,
                     'precision_json': precision_raw}
        if self.doc['profile_enabled']:
            prof = self.profile.profile_at_fixed_theta(self.joint, assembly_raw,
                     assembly_sha256=assembly_sha, background_json=background_payload['packet_json'],
                     consumer_module=c, physical_prior_module=self.p,
                     caller_verification_reference=self.doc['loaded_objects_reference'])
            # Separate typed artifact; never add fields to the theta callback envelope.
            for model in self.t.MODELS:
                rec = prof['models'][model]
                if type(rec['log_profile_deta']) is float and rec['log_profile_deta'] == float('-inf'):
                    rec['log_profile_deta'] = {'$float': '-inf'}
            artifacts['profile_json'] = c._canonical(prof)
            self.validate_profile(artifacts['profile_json'], descriptor, assembly_sha)
        return envelope, artifacts

    def validate_profile(self, raw, descriptor, assembly_sha):
        c = self.c
        prof = c._json(raw, c._sha(raw), 'separate conditional profile artifact')
        c._require(prof['schema'] == 'F9_CONDITIONAL_AFFINE_PROFILE_RESULT_V1'
                   and prof['request_id'] == self.profile.REQUEST_ID and prof['status'] == 'ENGINEERING_ONLY'
                   and prof['theta'] == descriptor['theta']
                   and prof['provenance']['assembly_sha256'] == assembly_sha
                   and prof['provenance']['consumer_admission_sha256'] == self.joint._admission_sha256
                   and prof['provenance']['source_pins'] == self.profile.SOURCE_PINS
                   and prof['global_theta_search_performed'] is False
                   and prof['physical_extra_priors_applied'] is False
                   and prof['MM_status'] == 'CONDITIONAL_UNRATIFIED'
                   and all(prof[k] is None for k in ('global_minima','relative_evidence','lnB','p','sigma','verdict')),
                   'NODE_PROFILE_ARTIFACT', 'profile is separate, conditional and uncertified')
        c._keys(prof['models'], self.t.MODELS, 'complete profile family')

    def validate(self, envelope, descriptor, assembly_raw, precision_raw, background_payload, background_reference):
        c = self.c
        assembled = c._json(assembly_raw, c._sha(assembly_raw), 'stored assembly')
        precision = self.p._precision(c, precision_raw, c._sha(precision_raw))
        provenance = envelope['conditional_result']['provenance']
        c._require(provenance['assembly_sha256'] == c._sha(assembly_raw)
                   and provenance['precision_sha256'] == c._sha(precision_raw)
                   and provenance['background_sha256'] == c._sha(background_payload['packet_json'])
                   and precision == self._precision_doc(self.doc, self.joint, c._sha(assembly_raw)),
                   'NODE_ARTIFACT_CHAIN', 'conditional/assembly/precision/background bytes')
        c._require(assembled['identity']['admission_sha256'] == self.plan['assembly_admission_sha256']
                   and assembled['identity']['background_packet_sha256'] == provenance['background_sha256']
                   and envelope['receipt']['background_execution_reference'] == background_reference,
                   'NODE_ARTIFACT_CHAIN', 'stored original receipt/context')
        self._validator()._accept(envelope, descriptor)

    def decode_envelope(self, raw):
        doc = self.c._json(raw, self.c._sha(raw), 'cached typed envelope')
        self.c._keys(doc, ('conditional_result', 'receipt'), 'cached envelope')
        result = doc['conditional_result']
        for model in self.t.MODELS:
            value = result['models'][model]['log_conditional_integral']
            if type(value) is dict:
                self.c._require(value == {'$float': '-inf'}, 'NODE_TYPED_FLOAT', 'only legitimate tagged minus infinity')
                result['models'][model]['log_conditional_integral'] = float('-inf')
        # The existing typed encoder/_accept reject tags/nonfinite fields elsewhere.
        return doc
