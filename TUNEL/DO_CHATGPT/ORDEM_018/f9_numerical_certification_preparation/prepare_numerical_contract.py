"""Documentary custody only. Never import a scientific engine or evaluate formulas."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
REQUEST = ROOT / 'F9_NUMERICAL_CERTIFICATION_REQUEST.json'
RID = 'b5fe6406-4430-48a0-bc59-e58f68917c12'
checks = []
sources = []


def check(name, condition):
    if not condition:
        raise RuntimeError(name)
    checks.append({'name': name, 'passed': True})


def pin(path, expected=None, length=None, role='documentary_source'):
    path = Path(path)
    check('allowed documentary extension ' + path.name, path.suffix in {'.md', '.json'})
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if expected is not None:
        check('source SHA ' + path.name, digest == expected)
    if length is not None:
        check('source bytes ' + path.name, len(raw) == length)
    if not any(s['path'] == str(path) for s in sources):
        sources.append({'path': str(path), 'bytes': len(raw), 'sha256': digest, 'role': role})
    return raw


def read_structure(raw):
    # Numeric fields of the resolver are not observed inputs to this preparation.
    return json.loads(raw, parse_float=lambda _: None, parse_int=lambda _: None)


def write_new(name, value):
    path = BASE / name
    check('new output ' + name, not path.exists())
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    check('temporary bytes ' + name, tmp.read_bytes() == raw and len(raw) > 0)
    os.replace(tmp, path)
    check('written bytes ' + name, path.read_bytes() == raw)
    json.loads(path.read_bytes())


request = json.loads(pin(REQUEST, role='official_request'))
check('request identity', request['request_id'] == RID)
check('output folder', Path(request['output_folder']).resolve() == BASE)
check('all execution limits zero', all(v == 0 for v in request['limits'].values()))
check('opening preserved', request['operator_section6_preserved'] is True)
top = {}
for source in request['source_pins']:
    top[Path(source['path']).name] = pin(source['path'], source['sha256'], source['bytes'], 'request_pin')
resolver = read_structure(top['RESOLUTOR_F9.json'])
check('resolver observed outputs absent', all(v is None for v in resolver['observed_outputs_now'].values()))
selected = ['assembly', 'linear_note', 'nuisance_measure', 'background_protocol',
            'background_metadata', 'h5_note', 'calibration_proof', 'background_review', 'root_recommendation']
admitted = {}
for key in selected:
    item = resolver['sources'][key]
    admitted[key] = pin(item['path'], item['sha256'], role='resolver:' + key)
calibration = json.loads(top['CALIBRATION_BOUND_CANDIDATE.json'])
check('calibration not adopted', calibration['opening_authorized'] is False)
check('calibration execution absent', calibration['new_science_executed'] is False)
receipt = json.loads(top['THEORY_CONTROL_ROOT_RECEIPT.json'])
check('pilot not full prior', receipt['full_prior_qualified'] is False)
check('pilot no observed inputs', receipt['observed_inputs'] is False)
check('pilot not scientific ratification', receipt['scientific_ratification'] is False)

search = []
pattern = re.compile(r'interval|quadratur|certif.*min|L_i|U_i|otimiz|branch|parti[cç]', re.I)
for key, raw in admitted.items():
    if key == 'background_metadata':
        continue
    matches = [{'line': i + 1, 'text': line} for i, line in enumerate(raw.decode('utf-8').splitlines()) if pattern.search(line)]
    search.append({'source_id': key, 'matches': matches})

domain = {
    'base_coordinates': ['H0', 'omega_b_h2', 'omega_c_h2'],
    'base_bounds_exact_strings': [['50', '90'], ['0.015', '0.030'], ['0.08', '0.18']],
    'base_density': '50/3',
    'additional_uniform_priors': {'H3': {'coordinate': 'beta', 'bounds': ['-0.05', '0.05'], 'density': '10'},
        'H4': {'coordinate': 's', 'bounds': ['-0.15', '0.15'], 'density': '10/3'},
        'H5': {'coordinate': 'rd_free_Mpc', 'bounds': ['130', '160'], 'density': '1/30'}},
    'unit_cube': 'Exact affine map of original prior coordinates. pi_i(xi) dxi = du; no fitted boxes.',
    'minimum_boundary': 'All closed-domain boundaries included',
    'integration_partition': 'Disjoint interiors, boundaries counted once or zero prior measure, exact rational cell mass',
    'H4_reparameterization': 'delta=-5 log10(1+s); pi_delta=(ln10/1.5)*10^(-delta/5), transformed endpoints',
    'H5_reparameterization': 'q=rd/rd_CAMB(theta); bounds [130/rd_CAMB,160/rd_CAMB], pi_q=rd_CAMB/30',
    'domain_change_allowed': False,
}
model_rows = [
    {'id': 'H1', 'dimension': 3, 'local_h': 'log10(H0/H_unit)+I(theta)*ALPHA_FINE_CODATA_2018*sqrt(e)/ln10', 'delta_C': '0', 'background': 'standard'},
    {'id': 'H2', 'dimension': 3, 'local_h': 'log10(H0/H_unit)', 'delta_C': '0', 'background': 'standard'},
    {'id': 'H3', 'dimension': 4, 'local_h': 'log10(H0/H_unit)+I(theta)*beta/ln10', 'delta_C': '0', 'background': 'standard'},
    {'id': 'H4', 'dimension': 4, 'local_h': 'log10(H0/H_unit)', 'delta_C': '-5 log10(1+s) through c_C', 'background': 'standard'},
    {'id': 'H5', 'dimension': 4, 'local_h': 'log10(H0/H_unit)', 'delta_C': '0', 'background': 'BAO denominator rd_free; CMB rstar standard'},
]
dependencies = ['request_id', 'unit_id', 'model_id', 'scenario_id', 'entire_scenario_list_sha256',
    'target_definition_sha256', 'engine_and_config_sha256', 'domain_and_prior_sha256',
    'data_future_sha256', 'covariance_sha256', 'X_and_response_sha256', 'support_certificate_sha256',
    'arithmetic_backend_and_precision', 'upstream_certificate_hashes', 'coverage_hash', 'method', 'status']
contract = {
    'schema': 'F9_NUMERICAL_CERTIFICATION_DOCUMENTARY_CANDIDATE_V1', 'request_id': RID,
    'status': 'PREPARED_NOT_RATIFIED_NOT_IMPLEMENTED', 'scope_statutes': ['DERIVED_CONDITIONAL', 'INPUT_PROPOSED', 'OPEN_IMPLEMENTATION'],
    'recommendation': 'B engineering first, A certificate interface and independent verifier. No automatic promotion of estimates.',
    'alternatives': {'A': 'Validated outer enclosures over full domain, feasible upper witnesses and interval prior integration',
                     'B': 'Adaptive engineering, estimates and diagnostics only where error unbounded; certified trivial bounds kept separately'},
    'adoption': False, 'scientific_execution_authorized': False, 'opening_under_section6': False,
    'fixed_models': model_rows, 'domain_and_priors': domain,
    'fixed_shared_model': {'local_rows': 267, 'background_rows': 16, 'nuisance_dimension': 63,
        'nuisance_measure': 'same kappa d_eta on R^63, relative only', 'I_theta': '(2/3)*ln(E_standard(1089.95;theta))',
        'scenario_family': 'Entire frozen list from adopted contract;600 candidate labels are not yet600 qualified joint matrices',
        'no_new_scenarios_or_weights': True, 'alpha': '0.5*erfc(5/sqrt(2))', 'alpha_changed': False},
    'target': {'q': 'inf_eta (y-mu_i(xi)-X eta)^T C_s^+ (y-mu_i(xi)-X eta) = ||R_s(y-mu_i(xi))||^2',
        'g': 'inf over the entire D_i of q', 'geometry': 'Common affine support, X in support with rank63, R_s X=0 and R_s C_s R_s^T=I',
        'physical_sampling_adequacy_is_separate': True},
    'interfaces': {
        'qualify_geometry': {'input': 's,pinned stipulated C,X,response,units,structural constraints', 'output': 'GeometryCertificate or invalid'},
        'enclose_prediction': {'input': 'model,entire cell,geometry,engine/config', 'output': 'CertifiedMeanEnclosure | UnboundedTheoryError | ComputationalFailure'},
        'bound_profile': {'input': 'cell,geometry,mean enclosure', 'output': 'CellBounds valid for every point, plus dependencies'},
        'certify_witness': {'input': 'feasible physical point,evaluation error bound', 'output': 'finite upper on actual q or UncertifiedEstimate'},
        'verify_cover': {'input': 'full domain,cell tree,prune ledger', 'output': 'CoverageCertificate or coverage gap'},
        'assemble_minimum': {'input': 'cover,cell lower bounds,witness upper bounds', 'output': 'L<=g<=U'},
        'integrate_prior_bounds': {'input': 'full partition,cell prior masses,q ranges', 'output': 'I_lower<=I<=I_upper'},
        'compare_models': {'input': 'verified minimum/integral intervals', 'output': 'existing statistic and pairwise evidence intervals'}},
    'certificate_common_fields': dependencies,
    'cell_certificate_fields': ['exact_cell_endpoints','prior_mass_exact','q_lower','q_upper','upper_bound_kind',
        'enclosure_scope','cover_parent','proof_method','witness_refs','unresolved_errors'],
    'minimum_assembly': {'lower': 'max(0,min_all_covered_cells lower_k)', 'upper': 'min_certified_feasible_points upper_j',
        'no_upper_witness': 'positive_infinity; numeric field null', 'unknown_cell_lower': '0 from q nonnegativity, retain cell',
        'prune': 'Only certified cell lower>=current certified upper, with retained coverage/prune ledger',
        'numeric_estimate_is_certified_upper': False,
        'outer_ball_lower': 'max(0,||x-c_B||-rho_B)^2 with outward arithmetic',
        'dual_lower': 'max(0, interval_lower(2 v^T (y-mu(B))-v^T C v)); exact X^T v=0 required',
        'full_domain_mandatory': True},
    'error_propagation': {
        'covariance_distinction': 'stipulated covariance, numerical representation error and physical inadequacy are separate',
        'inverse_bound': 'On fixed support: ||Cinv-Chatinv|| <= e_C/[lambda*(lambda-e_C)] with verified lambda>e_C',
        'metric_sandwich': '(1-eps)C0<=C<=(1+eps)C0 => q0/(1+eps)<=qC<=q0/(1-eps), same b/X/support',
        'residual_error': 'delta=e_R*||bhat||+(||Rhat||+e_R)*e_b',
        'point_q_interval': '[max(0,n-delta)^2,(n+delta)^2], n=||Rhat*bhat||, external rounding',
        'forbidden_repairs': ['jitter','drop small positive eigenvalues','erase off-support residual','truncate nuisance domain','replace X within tolerance'],
        'engine_error': 'Uniform on each entire cell and required fields; resolution agreement is diagnostic only',
        'beta_fixed': 'ALPHA_FINE_CODATA_2018*sqrt(e) in runtime with representation certificate',
        'physical_approximation': 'Declared CAMB/RECFAST target separate from numerical solution error and physical sampling adequacy'},
    'evidence': {
        'physical_priors_normalized': True, 'absolute_evidence_with_improper_eta': False,
        'I': 'integral_Di exp(-q/2)*pi_i dxi = integral_unit_cube exp(-q(T_i(u))/2) du',
        'J': 'kappa*A_s*I_i', 'A_s': '(2pi)^(-(r_s-63)/2)/sqrt(pdet(C_s)*det(X^T C_s^+ X))',
        'common_factor_cancellation': 'Only same C,X,support,units,nuisance measure and parameter-independent factor per scenario',
        'logJ_certificate': 'Requires interval log(A_s) plus log(I_i); omit log(kappa) as explicit common unknown. Ratios may cancel A_s symbolically.',
        'quadrature_lower': 'sum_k w_k*exp(-q_upper_k/2), rounded down',
        'quadrature_upper': 'sum_k w_k*exp(-q_lower_k/2), rounded up',
        'unknown_cell': '[0,w_k] contribution, NOT likelihood zero; preserve failure flag',
        'minimum_pruning_removes_integral_mass': False,
        'uniform_q_error': '|q-qhat|<=eps => exp(-eps/2)*Ihat<=I<=exp(eps/2)*Ihat, plus certified quadrature error',
        'ratio_interval': '[I_i_lower/I_j_upper,I_i_upper/I_j_lower] for strictly positive lower endpoints',
        'log_ratio_interval': '[ln(I_i_lower)-ln(I_j_upper),ln(I_i_upper)-ln(I_j_lower)]',
        'zero_lower_bound': 'insufficient_lower_bound, extended interval; not measured log zero',
        'report': 'five relative logJ and ten pairwise ratios per scenario; ranges over scenarios not posterior intervals',
        'no_conversion_to_sigma': True},
    'decision_integration': {
        'statistic_lowers': {'G1':'max(0,L1)','Q1':'max(0,L1-U3) only if H1 subset H3 qualified',
            'T21':'L2-U1','T41':'L4-U1','T51':'L5-U1'},
        'tail_consumer': 'Existing qualified upper-tail contract, including df0 and complete scenario list; no new tail algorithm here',
        'FWER': 'min(1,5*max_s p_upper_s), subject to existing V2 completeness',
        'probabilistic_error_budget': 'No positive failure probability proposed; any future one allocated inside unchanged alpha',
        'weak_certificate': 'L=0 may imply valid loose p=1, not missing calibration if all other hypotheses are qualified',
        'incomplete_scenario': 'No automatic complete non-rejection from placeholder p=1 or partial list'},
    'statuses': ['PREPARED_NOT_RATIFIED','ENGINEERING_ONLY','CERTIFIED_BOUND', 'CERTIFIED_BOUND_LOOSE',
        'UNBOUNDED_THEORY_ERROR','INCOMPLETE_COVERAGE','INVALID_SUPPORT','INVALID_TARGET','BUDGET_EXHAUSTED',
        'COMPUTATIONAL_FAILURE','INVALID_CERTIFICATE','INCONCLUSIVE'],
    'runtime': {'target_runtime_source': 'background_metadata admitted snapshot, not new availability test',
        'validated_backend_availability': 'NOT_CHECKED', 'initial_threads_proposed': 1,
        'required': ['exact domain/coverage arithmetic','directed-rounding elementary functions','validated supported linear algebra',
                     'independent certificate checker','content-addressed cell/prediction cache','persistent claims before calls',
                     'deadline checks through terminal persistence','bounded output and actual memory enforcement'],
        'scientific_campaign_limits': None, 'scientific_tolerances': None,
        'scientific_new_calls_authorized': 0,
        'uncertain_unit': 'Recover identity/receipt; never automatic rerun or rename'},
    'observed_outputs_now': dict.fromkeys(['y','C','R','minimum_intervals','evidence_intervals','logJ','logBayes_factors','F9','sigma']),
    'scientific_tests_executed': False, 'remote_calls': 0, 'downloads': 0,
    'originals_gate_shared_memories_changed': False,
}

cases = [
    ('NC01','Global lower versus local optimizer','Rational polynomial on [0,1] with boundary optimum and separated wells; exact known minima', 'Local proposals never become lower bound; full cover encloses each minimum'),
    ('NC02','Certified dual lower','Small rational PSD matrix and exact null-space vectors for X; one intentionally near-null invalid vector', 'Valid vectors give lower bounds; approximate annihilation is refused without nuisance bound'),
    ('NC03','Prior preservation','Affine cube maps for inherited physical coordinates; analytic toy means for H4/H5 reparameterizations', 'Mass exactly one and transformed Jacobians retained; no real model/centres used'),
    ('NC04','Minimization pruning versus integration','Positive analytic integrand with sizeable mass outside minimum cell; certified cell bounds', 'Pruned minimum cells remain in evidence interval'),
    ('NC05','Failed or unknown cell','Mock oracle reports failure in a positive-prior-mass cell of a completely defined toy target', 'Integral includes [0,w], minimum includes lower0, failure visible; no renormalization or zero likelihood'),
    ('NC06','Metric and support uncertainty','Exact rational support and covariance sandwiches, then rank-changing/jitter mutation', 'Bounds contain analytic toy profile; changed support refused; no physical covariance claim'),
    ('NC07','Forward uncertainty versus agreement','Two deliberately identical biased mock solvers and an independently supplied valid enclosure', 'Agreement alone remains ENGINEERING_ONLY; only the enclosure supports certificate'),
    ('NC08','Relative normalization','Analytically integrable low-dimensional Gaussian nuisance with common flat measure and normalized compact physical prior', 'Common factor cancels only when conditions hold; changed nuisance measure or prefactor retained/refused'),
    ('NC09','Integral and ratio containment','Positive toy integrands with analytic integral; deliberately wide bounds including zero and extreme log scale', 'Analytic value contained; no finite ratio claim from zero denominator lower bound or underflow'),
    ('NC10','Coverage and resource contract','Document-only toy cell tree and scenario manifest; shortened list, gap, budget exhaustion and certificate hash mutation', 'Missing coverage/hash cannot count as complete; valid wide bounds retained; no new execution of existing guard/tail controls'),
]
plan = {'request_id':RID,'status':'PLAN_ONLY_NOT_EXECUTED','execution_authorized':False,
    'controls':[{'id':x[0],'target':x[1],'fixture':x[2],'expected':x[3]} for x in cases],
    'scope':'New numerical certificate interfaces only; no CAMB, observed data or tail Monte Carlo',
    'limits_proposed_not_measured':{'total_wall_seconds':180,'per_control_wall_seconds':10,'threads':1,
        'RSS_MiB':512,'cells_per_case':4096,'precision_bits':[128,256],'output_MiB':16,'stdout_MiB':1},
    'before_execution':['Independent review and separate concrete authorization/unit IDs',
        'Select and pin interval backend; if unavailable BLOCKED_DEPENDENCY, no install by this plan',
        'Confirm arithmetic and actual resource enforcement through final persistence',
        'Reference existing controls C01-C08 and guard/tail receipts without replay'],
    'excluded':['consumed C01-C08','CAMB five-point pilot','INIT003','old Claude generation/pin blockage','observed F9'],
    'scientific_campaign_created':False,'real_values_allowed':False}

check('five unchanged model IDs', [x['id'] for x in model_rows]==['H1','H2','H3','H4','H5'])
check('prior dimensions preserved', [x['dimension'] for x in model_rows]==[3,3,4,4,4])
check('outputs all null', all(x is None for x in contract['observed_outputs_now'].values()))
check('plan only', plan['execution_authorized'] is False and len(plan['controls'])==10)
check('current unit no science', contract['scientific_tests_executed'] is False)
check('flat nuisance is not absolute evidence', contract['evidence']['absolute_evidence_with_improper_eta'] is False)
check('failure is not zero likelihood', 'NOT likelihood zero' in contract['evidence']['unknown_cell'])
check('full scenario list bound', 'entire_scenario_list_sha256' in dependencies)
check('note exists nonempty', (BASE/'CONTRATO_NUMERICO_F9.md').stat().st_size > 0)

write_new('INTERFACE_CERTIFICADOS_F9.json', contract)
write_new('PLANO_SINTETICO_NUMERICO.json', plan)
write_new('FONTES_E_REUSO.json', {'request_id':RID,'sources':sources,'bounded_contract_search':search,
    'reuse_decision':'Reuse existing Gaussian quotient, marginalization, calibration, background and no-retry contracts. Add numerical certificate interface only.',
    'scope_of_absence':'No equivalent complete numerical contract located in searched admitted documents; not whole-acervo claim',
    'pilot_metadata_only':{k:receipt[k] for k in ['status','observed_inputs','logical_solver_units','wall_controller_s','max_RSS_KiB','solver_seconds_total','full_prior_qualified','scientific_ratification']},
    'read_policy':'No raw data files, no scientific code imports, no observed targets; resolver numeric tokens suppressed; prior/runtime metadata allowed',
    'initial_navigation_error':'Resolver.sources is a mapping; initial list iteration failed with TypeError before remaining reads. Corrected dictionary navigation and all request pins subsequently verified; no mutation/science from failure.'})
validation = {'request_id':RID,'status':'PASS_DOCUMENTARY_CUSTODY_ONLY','checks_passed':len(checks),
    'checks':list(checks),'formulas_executed':False,'synthetic_controls_executed':False,
    'scientific_solver_calls':0,'integration_calls':0,'observed_values_accessed':False,
    'model_calls':0,'shared_memories_changed':False}
write_new('VALIDACAO_DOCUMENTAL.json', validation)
files=[]
for p in sorted(BASE.iterdir()):
    if p.is_file() and p.name not in ['MANIFESTO_ENTREGA.json','RECIBO_COORDENACAO.json']:
        b=p.read_bytes();files.append({'path':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'request_id':RID,'created_utc':datetime.now(timezone.utc).isoformat(),
    'status':'DOCUMENTARY_PREPARATION_COMPLETE_NOT_SCIENTIFIC_CERTIFICATION',
    'files':files,'observed_data_access':False,'scientific_execution':False,'remote_calls':0,'downloads':0,
    'does_not_authorize_execution':True}
write_new('MANIFESTO_ENTREGA.json', manifest)
for name in ['CONTRATO_NUMERICO_F9.md','INTERFACE_CERTIFICADOS_F9.json','MANIFESTO_ENTREGA.json']:
    b=(BASE/name).read_bytes();print(json.dumps({'file':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}))
print(json.dumps({'documentary_checks':validation['checks_passed'],'sources':len(sources),
    'manifest_files':len(files),'controls_planned_only':len(cases),'science_calls':0}))
