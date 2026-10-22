"""Build documentary contracts and source custody only; no scientific execution."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUEST = '6273a822-5880-4742-a82c-b7cf93f7c128'


def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


def write_new(path, value):
    data = value if isinstance(value, bytes) else (
        json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if path.exists():
        if path.read_bytes() == data:
            return
        raise FileExistsError(str(path))
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(data)
    if temp.read_bytes() != data:
        raise OSError('Incomplete temporary file')
    os.rename(temp, path)  # Windows refuses to replace an existing destination.
    if path.read_bytes() != data:
        raise OSError('Final file differs')


def main():
    checks = []
    def check(name, condition):
        checks.append({'name': name, 'pass': bool(condition)})
        if not condition:
            raise ValueError(name)

    request_path = ROOT / 'F9_CALIBRATION_BOUND_REQUEST.json'
    request = json.loads(request_path.read_text(encoding='utf-8-sig'))
    check('same_request', request['request_id'] == REQUEST)
    original = ROOT / 'f9_verdict_contract/F9_VERDICT_CONTRACT_CANDIDATE.json'
    original_pin = pin(original)
    check('requested_original_hash', original_pin['sha256'] == request['contract']['sha256'])
    check('requested_original_size', original_pin['bytes'] == request['contract']['bytes'])
    check('observed_opening_not_authorized', request['opening_authorized'] is False)

    source_names = [
        'F9_CALIBRATION_BOUND_REQUEST.json',
        'f9_verdict_contract/F9_VERDICT_CONTRACT_CANDIDATE.json',
        'f9_verdict_contract/F9_VERDICT_CONTRACT_CANDIDATE_V2.json',
        'f9_verdict_contract/ROOT_VC01_DELTA.md',
        'f9_verdict_contract/MANIFESTO_VC01_DELTA.json',
        'h0dn_documentary_review/linear_design/PROJETO_LINEAR_E_MEDIDA.md',
        'h0dn_documentary_review/linear_design/ESPECIFICACAO_LINEAR.json',
        'h0dn_documentary_review/linear_design/VALIDACAO_ESTRUTURAL.json',
        'derivacoes/preflight_262/PROTOCOLO_PREFLIGHT_262.json',
        'derivacoes/preflight_262/PREFLIGHT_262_RESULT.json',
        'reproducao_fase45_conjunta/T4_PROTOCOLO.json',
        'covariance_support/linear_gaussian.py',
        'covariance_support/singular_gaussian_v2.py',
    ]
    snapshots = HERE / 'source_snapshots'
    snapshots.mkdir(exist_ok=True)
    sources = []
    for index, name in enumerate(source_names, 1):
        path = ROOT / name
        before = pin(path)
        target = snapshots / f'{index:02d}_{path.name}'
        write_new(target, path.read_bytes())
        after = pin(path)
        check(f'source_{index}_stable', before == after)
        target_pin = pin(target)
        check(f'snapshot_{index}_identical', before['sha256'] == target_pin['sha256'])
        sources.append({'original': before, 'snapshot': target_pin})
    write_new(HERE / 'SOURCES.json', {'request_id': REQUEST, 'sources': sources,
        'policy': 'Immutable byte snapshots; original scientific sources not executed or modified'})

    v2 = json.loads((ROOT / source_names[2]).read_text(encoding='utf-8-sig'))
    structure = json.loads((ROOT / source_names[7]).read_text(encoding='utf-8-sig'))
    historical = json.loads((ROOT / source_names[10]).read_text(encoding='utf-8-sig'))
    check('V2_has_explicit_predicates', bool(v2['verdict'].get('decision_predicates')))
    check('primary_family_five', v2['primary_family']['m'] == 5)
    check('five_models', len(v2['models']) == 5)
    check('eta_63_source_metadata', structure['counts']['eta_dimension'] == 63)
    check('local_267_source_metadata', structure['counts']['rows'] == 267)
    check('cycles_72_source_metadata', structure['counts']['host_cycle_constraints'] == 72)
    check('Planck_compression_three', '3x3' in historical['likelihood']['planck'])
    check('BAO_compression_thirteen', '13x13' in historical['likelihood']['desi_dr2'])
    check('no_observed_outputs_in_V2', all(x is None for x in v2['outputs_now'].values()))

    prerequisites = [
        'Fixed known Gaussian joint covariance per frozen scenario, common to all compared models',
        'Same affine support, observation units and density normalizations',
        'True mean and nuisance contained in declared null domains',
        'Fixed X of supported full column rank63, eta in R^63',
        'All actual model means globally contained in declared response span for refined bound',
        'Whitening, quotient and global span recomputed or certified for each scenario',
        'Exact inherited72 covariance constraints if residual df upper148 is used',
        'Certified lower bounds for true global minima, feasible certified upper bounds for competitors',
        'Certified upper numerical SF including theory/rounding errors; no numerical zero tail',
        'Entire frozen scenario family available or proved equivalent coverage, with label mapping',
        'Selection and multiplicity contract held fixed, no new data-dependent route selection',
        'Conditional interpretation of reported or plug-in errors explicitly ratified',
    ]
    contract = {
        'request_id': REQUEST, 'version': 1,
        'status': 'DOCUMENTARY_CONDITIONAL_PROOF_CANDIDATE_NOT_ADOPTED',
        'scope': 'F9 compressed Planck3+BAO13+V01local267, shared eta63',
        'source_verdict_original': original_pin,
        'source_verdict_V2': pin(ROOT / source_names[2]),
        'changes_consumed_contract': False, 'opening_authorized': False,
        'new_science_executed': False, 'models_remote_called': 0,
        'proof': 'PROVA_COTA_CALIBRACAO_F9.md',
        'classification': 'DERIVED conditional finite-sample stochastic upper envelopes; not exact tail laws',
        'prerequisites': [{'requirement': x, 'application_status': 'REQUIRES_CASE_VERIFICATION'} for x in prerequisites],
        'base_theorem': {
            'quotient': 'R_s X=0; R_s C_s R_s^T=I_(r_s-63)',
            'true_parameter_pivot': 'q_null(xi0)=||R_s(Y-mu_null(xi0))||^2 ~ chi2_(r_s-63)',
            'inequality': 'G_null<=q_true; Q1<=G1; T_j1<=G_j',
            'uniformity': 'all admitted true physical parameters and eta; no improper sampling prior',
            'no_extra_physical_df_subtraction': True,
            'degree_upper_bound_allowed': True,
        },
        'gain_theorem': {
            'inclusion': 'Every R_s[mu_comp(xi)-mu_null(xi0)] belongs to fixed V_s for every pair of allowed parameters',
            'lower_competitor_residual': 'g_comp >= ||(I-Pi_V)Z||^2',
            'upper_gain': 'g_null-g_comp <= ||Pi_V Z||^2 ~ chi2_dim(V)',
            'B17_columns': '16 background coordinate columns plus extended local a_h',
            'B18_columns': 'B17 plus extended local c_C',
            'V_s': 'Range(R_s B17) or Range(R_s B18), with scenario-specific R_s',
            'actual_span_rank_measured': False,
            'tangent_space_substitution_allowed': False,
        },
        'structural_dimensions': {
            'local_rows': 267, 'background_compressed_rows': 16, 'joint_rows': 283,
            'inherited_constraints_conditional': 72, 'joint_rank_upper_conditional': 211,
            'nuisance_rank_required': 63, 'residual_degree_upper_conditional': 148,
            'actual_joint_rank': None, 'actual_quotient_dimension': None,
            'degree_148_guard': 'Exact72 covariance kernel constraints and supported rank63 X in actual joint matrix',
            'subset_262': {'scope': 'Historical conditional engineering subset, not full experiment',
                'local_rank_from_receipt': 190, 'joint_rank_if_independent_positive_background': 206,
                'quotient_dimension_if_same_conditions': 143, 'substitution_for_full_267': False},
        },
        'test_envelopes': [
            {'id': 'COMPAT_H1', 'null': 'H1', 'statistic': 'G1=g1',
             'df_upper_candidate': 148, 'df_status': 'CONDITIONAL_RESIDUAL_DIMENSION_UPPER_BOUND',
             'statistic_lower': 'max(0,L1)'},
            {'id': 'LAW_H1_VS_FREE', 'null': 'H1', 'statistic': 'Q1=g1-g3',
             'df_upper_candidate': 17, 'df_status': 'STRUCTURAL_SPAN_UPPER_BOUND_NOT_MEASURED_RANK',
             'statistic_lower': 'max(0,L1-U3), only with qualified H1 subset H3'},
            {'id': 'H2_TO_H1', 'null': 'H2', 'statistic': 'T21=g2-g1',
             'df_upper_candidate': 17, 'df_status': 'STRUCTURAL_SPAN_UPPER_BOUND_NOT_MEASURED_RANK',
             'statistic_lower': 'L2-U1'},
            {'id': 'H4_TO_H1', 'null': 'H4', 'statistic': 'T41=g4-g1',
             'df_upper_candidate': 18, 'df_status': 'STRUCTURAL_SPAN_UPPER_BOUND_NOT_MEASURED_RANK',
             'statistic_lower': 'L4-U1'},
            {'id': 'H5_TO_H1', 'null': 'H5', 'statistic': 'T51=g5-g1',
             'df_upper_candidate': 17, 'df_status': 'STRUCTURAL_SPAN_UPPER_BOUND_NOT_MEASURED_RANK',
             'statistic_lower': 'L5-U1'},
        ],
        'certificates': {
            'minima': 'For every required model, deterministic L_i<=global_inf_RSS_i<=U_i',
            'local_optimizer_returns': 'feasible upper U only; never global lower L',
            'global_lower_option': 'minimum distance to certified outer enclosures over complete null-domain cell cover',
            'theory': 'include entire-domain prediction/support/whitening/roundoff errors, not five-point agreement only',
            'tail': 'upper numerical SF, stable at small p; exact/interval error bounds',
            'probabilistic_certification': 'Any failure probability must be allocated inside total alpha budget',
        },
        'p_value': {
            'nonpositive_lower': 1,
            'positive_lower': 'certified_upper_SF_chi2(df_upper,statistic_lower)',
            'zero_dimension': 'point mass0 with inclusive tail, no generic chi2(df=0)',
            'robust': 'max_s p_upper over complete frozen family or certified equivalent coverage',
            'familywise': 'min(1,5*max_s p_upper)',
            'alpha5': '0.5*erfc(5/sqrt(2)), upper-tail convention',
            'Z_equivalent_lower': 'Phi^-1(1-p_familywise_upper), optional, not positive evidence for large p',
            'directed_sign': 'statistic_lower>0 in every admitted scenario',
            'no_exact_p_claim': True, 'no_Wilks': True, 'no_Bayes_conversion': True,
        },
        'V2_interoperation': {
            'valid_status': 'VALID_UNIFORM_NULL_OR_CONSERVATIVE_BOUND',
            'weak_bound': 'Valid but non-rejecting conservative test, not missing calibration',
            'weak_bound_limit': 'Does not show exact p exceeds alpha; does not validate the model',
            'not_falsified': 'Only both complete valid H1 tests non-reject under V2; power separate',
            'incomplete': 'No robust p/non-rejection from subset of available scenarios',
            'bayes': 'All relative evidence remains separately computed under its own measure contract',
        },
        'extensions_not_adopted': {
            'covariance_inflation': 'If true fixed Gaussian Sigma <= a C_work uniformly, use a*chi2, with justified a and same support',
            'unknown_or_parameter_dependent_covariance': 'No automatic likelihood-ratio extension; fresh proof required',
            'estimated_covariance': 'No automatic chi-square pivot even if independent estimate',
            'full_spectral_CMB': 'New dimension and theory/likelihood contract needed',
        },
        'alternatives': [
            {'id': 'A', 'name': 'Residual chi-square envelope for all five tests', 'recommended': False},
            {'id': 'B', 'name': 'Residual envelope for G and global-span envelopes for Q/T', 'recommended': True},
            {'id': 'C', 'name': 'Sharper uniformly calibrated tails in a separate future unit', 'recommended': False},
        ],
        'outputs_now': {k: None for k in ('observed_statistics', 'minima_certificates', 'p_upper',
            'sigma', 'global_power', 'lnB', 'observed_centres', 'y', 'S', 'g')},
    }
    write_new(HERE / 'CALIBRATION_BOUND_CANDIDATE.json', contract)

    cases = [
        ('C01_FIXED_QUOTIENT', 'Tiny rational fixed Gaussian geometry, supported full-rank X; verify RX=0, RCRt=I and pointwise base inequality; no reused integral test'),
        ('C02_GLOBAL_NONLINEAR_SPAN', 'Curved mean family entirely inside prescribed V; verify distance relaxation and gain bound with deterministic vectors'),
        ('C03_TANGENT_IS_NOT_GLOBAL_SPAN', 'Nonlinear curve with one-dimensional tangent but larger affine span; reject tangent-only certificate'),
        ('C04_DIRECTED_SIGN_AND_ZERO_DF', 'Negative/zero gain maps to p1; rank-zero pivot handled as atom0; no scipy df0 call'),
        ('C05_MINIMUM_CERTIFICATE_DIRECTION', 'Fabricated local residual upper value must not be accepted as lower bound; Lnull-Ucomp ordering required'),
        ('C06_DIFFERENT_COVARIANCE', 'Analytic epsilon covariance counterexample must block reuse of RSS-based likelihood envelope'),
        ('C07_COMPLETE_SCENARIOS', 'Missing scenario leaves robust unavailable, but another complete valid rejection survives; no silent best-case selection'),
        ('C08_TAIL_CERTIFICATE', 'Integer/half-integer SF recurrences compared with certified enclosures, no underflow-zero or unbudgeted certificate failure'),
    ]
    protocol = {
        'request_id': REQUEST, 'status': 'PROTOCOL_ONLY_NOT_EXECUTED_NOT_AUTHORIZED_TO_RUN',
        'purpose': 'Implementation guards specific to new analytic envelopes; not proof by Monte Carlo',
        'scope': 'At most8 deterministic tiny synthetic controls after separate authorization',
        'max_cases': 8, 'matrix_dimension_max': 8, 'max_wall_seconds': 30,
        'worker_threads': 1, 'max_execution_count_per_identity': 1,
        'random_simulation_count': 0, 'scientific_catalogues': [],
        'CAMB_runs': 0, 'observed_data_allowed': False, 'remote_calls': 0,
        'controls': [{'id': a, 'requirement': b} for a, b in cases],
        'failure_policy': 'Visible terminal failure, no repeated uncertain unit and no covariance/model repair',
        'does_not_validate': ['physical Gaussian errors', 'complete-domain CAMB prediction bounds',
            'actual F9 optimizer minima', 'actual5sigma power', 'observed hypothesis'],
        'do_not_repeat': ['qualified flat-nuisance integral controls', 'preflight262', 'five paired background controls'],
    }
    write_new(HERE / 'PROTOCOLO_CONTROLES_FUTUROS.json', protocol)
    check('no_new_science_flag', contract['new_science_executed'] is False)
    check('no_observed_outputs', all(x is None for x in contract['outputs_now'].values()))
    check('test_ids_match_consumed_V2', [x['id'] for x in contract['test_envelopes']] ==
          [x['id'] for x in v2['primary_family']['claims']])
    check('all_require_application_checks', all(x['application_status'] == 'REQUIRES_CASE_VERIFICATION'
          for x in contract['prerequisites']))
    check('actual_joint_rank_unmeasured', contract['structural_dimensions']['actual_joint_rank'] is None)
    check('span_ranks_unmeasured', contract['gain_theorem']['actual_span_rank_measured'] is False)
    check('future_protocol_only', protocol['status'] == 'PROTOCOL_ONLY_NOT_EXECUTED_NOT_AUTHORIZED_TO_RUN')
    check('no_simulation_protocol', protocol['random_simulation_count'] == 0)
    check('future_no_CAMB', protocol['CAMB_runs'] == 0)
    check('proof_exists_nonempty', (HERE / contract['proof']).stat().st_size > 10000)
    for item in sources:
        check('original_still_' + Path(item['original']['path']).name,
              pin(Path(item['original']['path'])) == item['original'])
    write_new(HERE / 'VALIDACAO_DOCUMENTAL.json', {
        'request_id': REQUEST, 'status': 'PASS_DOCUMENTARY_SCHEMA_AND_CUSTODY_ONLY',
        'checks': checks, 'passed': len(checks),
        'not_a_mathematical_or_scientific_execution_test': True,
        'imported_scientific_modules': [], 'new_science_runs': 0,
        'created_utc': datetime.now(timezone.utc).isoformat()})
    print(json.dumps({'status': 'DOCUMENTARY_ARTIFACTS_PREPARED', 'checks': len(checks),
                      'sources': len(sources), 'candidate': pin(HERE / 'CALIBRATION_BOUND_CANDIDATE.json')},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
