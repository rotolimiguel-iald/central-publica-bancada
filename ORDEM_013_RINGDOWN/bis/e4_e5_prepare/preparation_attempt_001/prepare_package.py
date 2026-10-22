"""Metadata and static preparation only. Never call the science executor."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import re
import sys
import time
from pypdf import PdfReader

O = Path(__file__).resolve().parent
B = O.parents[1]
I = B.parent / 'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS'
D = I / 'medicao_da_ampliacao/B_catalogos'
START = time.perf_counter()
FILES = {}


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def pin(path, role='EXISTING_DOCUMENT_OR_METADATA'):
    path = path.resolve()
    import os
    relative = Path(os.path.relpath(path, B)).as_posix()
    FILES[relative] = {'path': relative, 'sha256': sha(path), 'bytes': path.stat().st_size, 'role': role}
    return FILES[relative]


def load(relative):
    p = B / relative
    pin(p)
    return json.loads(p.read_text(encoding='utf-8-sig'))


def write(name, obj):
    raw = obj.encode('utf-8') if isinstance(obj, str) else (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8')
    with (O / name).open('xb') as stream:
        stream.write(raw)


def old_gr():
    """Only Table1 old-run columns: SNR, remnant detector mass, spin, errors."""
    pdf = D / 'arxiv_2603.19021_gwtc4_tgr3.pdf'
    txt = D / 'gwtc4_tgr3.txt'
    pin(pdf, 'PRIMARY_METADATA_TABLE1_PDF_PAGES_2_3_ONLY')
    pin(txt, 'ARCHIVED_PRIMARY_TEXT_TABLE1_CROSSCHECK')
    reader = PdfReader(pdf)
    pattern = r'(GW\d{6}(?:[ _]\d{6})?)'
    def parse(text, page):
        parts = re.split(pattern, text)
        rows = {}
        for k in range(1, len(parts), 2):
            event = parts[k].replace(' ', '_')
            if event[2:4] not in ['15', '17', '19', '20']:
                continue
            numbers = [float(v.replace('−', '-')) for v in re.findall(r'[−-]?\d+(?:\.\d+)?', parts[k+1])][:9]
            require(len(numbers) == 9 and numbers[3] > 0 and 0 <= numbers[6] < 1, 'GR row '+event)
            require(numbers[4] >= 0 and numbers[5] <= 0 and numbers[7] >= 0 and numbers[8] <= 0, 'GR errors '+event)
            require(event not in rows, 'Duplicate table event')
            rows[event] = {'event': event, 'table_snr_not_used_for_selection': numbers[0],
                'final_mass_detector': numbers[3], 'final_mass_upper_error': numbers[4], 'final_mass_lower_error': numbers[5],
                'final_spin': numbers[6], 'final_spin_upper_error': numbers[7], 'final_spin_lower_error': numbers[8],
                'pdf_page': page, 'source_pdf_sha256': sha(pdf), 'source': 'GWTC4 TGR III Table1 historical GR catalog baseline',
                'statute': 'KNOWN_PUBLISHED_BASELINE_NOT_NEW_MEASUREMENT', 'mass_frame': 'detector (1+z)Mf',
                'centrality_scope': 'Published catalog central values; table2 overlap corroborates median convention for O4a. Original old-run median convention inherited from catalog, not individually rederived.',
                'physical_remnant_caveat': 'Table value is not certification of a black-hole remnant for BNS/NSBH. GW170817 fails mass INPUT.',
                'old_release_not_updated_GR_PE': True}
        return rows
    rows = {}
    for page in [2, 3]:
        new = parse(reader.pages[page-1].extract_text(), page)
        require(not set(rows) & set(new), 'Duplicate across pages')
        rows.update(new)
    text = txt.read_text(encoding='utf-8')
    section = text[text.index('Table 1. Event selection table'):text.index('NOTE—Event selection table')]
    control = parse(section, None)
    require(rows.keys() == control.keys(), 'PDF/text table coverage')
    fields = ['final_mass_detector', 'final_mass_upper_error', 'final_mass_lower_error', 'final_spin', 'final_spin_upper_error', 'final_spin_lower_error']
    for event in rows:
        require(all(rows[event][f] == control[event][f] for f in fields), 'PDF/text disagreement '+event)
    return rows, {'old_table_rows': len(rows), 'PDF_text_fields_agree': 6*len(rows), 'pages_read': [2, 3], 'whole_PDF_read': False}


def metadata():
    inventory = load('bis/e0_metadata/GWOSC_INVENTORY.json')
    gr_o4 = load('bis/e1_selection/GR_O4A_ADENDO.json')
    census = load('bis/e1_selection/CALIBRATION_AND_CANDIDATE_CENSUS.json')
    by_o4 = {r['event']: r for r in gr_o4['O4_snapshot_rows']}
    old, validation = old_gr()
    aliases = {'GW150914_095045': 'GW150914', 'GW170104_101158': 'GW170104', 'GW190521_030229': 'GW190521'}
    exposed = {aliases.get(e, e) for e in census['corpus']['deduplicated_event_list']}
    rows = []
    for r in inventory['events']:
        if r['network_matched_filter_snr'] is None or r['network_matched_filter_snr'] < 12:
            continue
        meta = by_o4[r['event']]['GR_metadata'] if r['event'] in by_o4 else old.get(r['event'])
        eligible = None if meta is None else meta['final_mass_detector'] >= 40 and 0 <= meta['final_spin'] < .98
        rows.append({'event': r['event'], 'run': r['run'], 'network_snr_GWOSC': r['network_matched_filter_snr'],
            'version_key': r['version_key'], 'metadata_url': r['event_metadata_url'], 'GR_metadata': meta,
            'eligibility_INPUT': eligible, 'status': 'AWAITING_GR_METADATA' if eligible is None else ('PASS_INPUT' if eligible else 'FAIL_KNOWN_INPUT'),
            'priority_snr_ge30': r['network_matched_filter_snr'] >= 30,
            'in_audited_39_event_pSEOB_corpus': r['event'] in exposed, 'blindness_certified': False,
            'absence_means_never_published': False, 'new_posterior_or_strain_accessed': False})
    by_run = {}
    for run in inventory['by_run']:
        rr = [r for r in rows if r['run'] == run or run == 'all_public_selected' or
              (run == 'O4_public_total' and r['run'].startswith('O4'))]
        by_run[run] = {'SNR_ge12': len(rr), 'eligible': [r['event'] for r in rr if r['eligibility_INPUT'] is True],
            'known_fail': [r['event'] for r in rr if r['eligibility_INPUT'] is False],
            'awaiting_GR': [r['event'] for r in rr if r['eligibility_INPUT'] is None],
            'priority_eligible': [r['event'] for r in rr if r['eligibility_INPUT'] is True and r['priority_snr_ge30']],
            'all_SNR_threshold_lists': {str(t): [r['event'] for r in rr if r['network_snr_GWOSC'] >= t] for t in [12, 30, 53, 78, 95]}}
        for threshold, values in by_run[run]['all_SNR_threshold_lists'].items():
            require(set(values) == set(inventory['by_run'][run]['thresholds'][threshold]['events']), 'Snapshot threshold mismatch')
    special = next(r for r in rows if r['event'] == 'GW250207_115645')
    return {'status': 'REAL_METADATA_JOIN_AND_INPUT_APPLICATION__NOT_E2_TEST_REGISTRATION',
        'observation_snapshot': inventory['observation_snapshot'], 'SNR_convention': inventory['convention'],
        'criteria': gr_o4['criteria'], 'by_run': by_run, 'rows': rows, 'added_old_GR_rows': list(old.values()),
        'old_GR_validation': validation,
        'GW250207_status': {**special, 'prospective_role': 'INPUT_ORDER_FUTURE_TEST_CANDIDATE_WHEN_DATA_RELEASED_AND_REGISTERED',
            'current_eligible_test_event': False, 'availability_scope': 'Frozen E0 metadata snapshot only; no new API query or strain-link validation; no test posterior inspected'},
        'caveats': ['Selection uses median/central values, not probability of cuts or posterior widths.',
            'Historical GR medians are not reestimated for the currently preferred GWOSC version.',
            'O4c is one discovery window, not a complete observing-run catalog.',
            'Catalog CBC includes BNS/NSBH; network SNR is not isolated 440 SNR.',
            'Missing metadata is unknown, not failed or accepted. Absence in audited corpus does not certify blindness.']}


def main():
    targets = ['METADATA_AND_HIGH_SNR.json', 'SCHEMA.json', 'INPUT_MANIFEST.json', 'PLAN.json', 'PREPARATION.md', 'STATIC_RECEIPT.json']
    require(not any((O/n).exists() for n in targets), 'Output exists; preserve by new directory/version')
    code = O / 'deterministic_e4_e5.py'
    parsed = ast.parse(code.read_text(encoding='utf-8'))
    compile(parsed, str(code), 'exec', optimize=1)
    compile(ast.parse(Path(__file__).read_text(encoding='utf-8')), str(__file__), 'exec', optimize=1)
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(parsed)), 'Safety must survive -O')
    require(not any(isinstance(n, (ast.Import, ast.ImportFrom)) and
            any(token in ast.unparse(n) for token in ['subprocess', 'requests', 'urllib', 'lalsimulation', 'bilby', 'dynesty']) for n in ast.walk(parsed)), 'Forbidden executor dependency')
    c1 = load('C1_LEITURAS_v4.json')
    readings = [r['reading'] for r in c1['rows']]
    require(len(readings) == len(set(readings)) == 10, 'Ten readings')
    c4 = load('C4_JOINT_MODES.json')
    schema_c4 = load('C4_SCHEMA.json')
    fisher = load('FISHER_INPUTS.json')
    require({p['key'] for p in fisher['psds']} == {'O4', 'O5', 'ET', 'CE'}, 'Four PSDs')
    posterior = 'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
    source = pin(B/posterior, 'EXISTING_AUDITED_CALIBRATION_HDF_HASH_ONLY_NO_VALUES_READ')
    require(source['sha256'] == c4['source_sha256'] == schema_c4['h5_sha256'], 'Archived 440 source pin')
    for psd in fisher['psds']:
        info = pin(B/'cache/psd'/psd['filename'], 'REFERENCE_SENSITIVITY_CURVE_NOT_EVENT_PSD')
        require(info['sha256'] == psd['sha256'], 'PSD pin')
    reference = [
        'tgl_ringdown_prediction.py', 'tgl_ringdown_unravelings.py', 'joint_modes_posterior.py', 'fisher_forecast.py',
        'QNM_GRID.json', 'C5_FISHER_v3.json', 'PORTAO_DO_PODER_013_v2.json', 'C4_CATALOG_SCHEMA.json',
        'bis/F2_INDEPENDENT_GAUSSIAN_DENSITY.json', 'bis/F2_INJECTION_INDEPENDENT_REVIEW.md',
        'bis/F2_RD_APPLICABILITY_REVIEW.json', 'bis/e1_selection/SELECTION_AND_CONTROLS.json',
        'bis/e0_core/DATASET.json', 'bis/E0_ROUTE_IV_POWER_v2.json', 'NUISANCE_V1.json',
        'PORTAO_DA_AMPLIACAO_V1.json', 'bis/PART_B_BUDGET_START.json']
    for name in reference:
        pin(B/name)
    order = B.parent / 'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
    pin(order, 'ORDER_E4_E5_AND_EXECUTION_SEQUENCE')
    pin(code, 'PREPARED_SCIENTIFIC_CODE_NOT_EXECUTED')
    pin(Path(__file__), 'METADATA_AND_STATIC_PREPARATION_CODE')
    meta = metadata()
    schema = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'title': 'E4 E5 preparation plan v1', 'type': 'object', 'additionalProperties': False,
        'required': ['schema_version', 'status', 'created_utc', 'input_manifest_sha256', 'readings', 'variants', 'E4', 'E5', 'activation', 'not_executed'],
        'properties': {
            'schema_version': {'const': 1}, 'status': {'const': 'PREPARED_NOT_SCIENTIFICALLY_EXECUTED_AWAITING_E2'},
            'created_utc': {'type': 'string'}, 'input_manifest_sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
            'readings': {'type': 'array', 'minItems': 10, 'maxItems': 10, 'uniqueItems': True, 'items': {'enum': readings}},
            'variants': {'const': ['ONLY_220_DEFORMED', 'BOTH_220_440_DEFORMED']},
            'E4': {'type': 'object', 'required': ['fisher', 'posterior', 'fixed_free_robustness', 'output_scope']},
            'E5': {'type': 'object', 'required': ['models', 'statistic', 'full_posterior', 'information', 'secondary', 'jitter_transfer', 'sigma_sys', 'archived_information_populations']},
            'activation': {'type': 'object'}, 'not_executed': {'type': 'array', 'items': {'type': 'string'}}},
        '$defs': {'future_result': {'type': 'object',
            'required': ['schema_version', 'status', 'plan_sha256', 'input_manifest_sha256', 'E4_fisher', 'E4_archived_marginals', 'E5_information', 'E5_contract', 'performance'],
            'properties': {'schema_version': {'const': 1}, 'status': {'const': 'NONBLIND_CONDITIONAL_DETERMINISTIC_DIAGNOSTICS'},
                'new_PE': {'const': False}, 'new_waveforms': {'const': False}, 'new_test_data': {'const': False},
                'population_fit_executed': {'const': False}, 'null_calibration_executed': {'const': False},
                'performance': {'type': 'object', 'required': ['wall_seconds_through_computation', 'process_CPU_seconds_through_computation']}}}}}
    write('METADATA_AND_HIGH_SNR.json', meta)
    write('SCHEMA.json', schema)
    pin(O/'METADATA_AND_HIGH_SNR.json', 'METADATA_RESULT_TO_FREEZE_WITH_PLAN')
    pin(O/'SCHEMA.json', 'PLAN_AND_RESULT_SCHEMA')
    manifest = {'status': 'ACTUAL_BYTES_HASHED_PREPARATION_ONLY', 'files': list(FILES.values()),
        'HDF_values_read': False, 'scientific_runtime_tested': False,
        'path_root': str(B), 'hash_method': 'SHA256 streamed from actual bytes'}
    write('INPUT_MANIFEST.json', manifest)
    plan = {'schema_version': 1, 'status': 'PREPARED_NOT_SCIENTIFICALLY_EXECUTED_AWAITING_E2',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'input_manifest_sha256': sha(O/'INPUT_MANIFEST.json'),
        'readings': readings, 'variants': ['ONLY_220_DEFORMED', 'BOTH_220_440_DEFORMED'],
        'E4': {
            'fisher': {'reference_source': {'mass_detector_Msun': 68.1, 'spin': .68, 'redshift': 0.0,
                    'statute': 'INPUT_FIXED_REFERENCE_NOT_GW250114_MEDIAN'},
                'f_min_Hz': 20., 'f_max_Hz': 2048., 'df_Hz': .125,
                'isolated_440_snr_grid': [10, 20, 40, 80, 200, 600],
                'snr_routes': ['ISOLATED_440_GRID', 'AMPLITUDE_FIXA_INPUT'],
                'normal_90_quantile': 1.2815515655446004, 'operational_delta_min': 1e-12,
                'QNM': 'Pinned 440 cubic spline, no extrapolation; CODATA2018_IAU2015; beta=alpha_CODATA2018*sqrt(e) runtime',
                'profiles': ['FIXED_SOURCE_FREQUENCY', 'FREE_FREQUENCY_FIXED_TAU_GR'],
                'amplitude_phase': 'Marginalized with Schur complement in analytical causal damped-mode Fourier Fisher',
                'mass_spin': 'Fixed; no claim to remove single-mode free-M/chi degeneracy',
                'snr_transport': 'Two INPUT routes: equal isolated rho440 per PSD compares shapes; same reference source with amplitude A=rho440_O4_INPUT/||h||_O4 propagates rho440_PSD=rho440_O4_INPUT*||h||_PSD/||h||_O4. No network IMR conversion.',
                'counts': 'N50=25/z_local^2 [INPUT E(Z)=5]; N90conditional=(5+1.2815515655446004)^2/z_local^2 for known unit-variance one-sided Gaussian Z. Neither is calibrated significance or realistic yield. Zero or |delta|<1e-12 => null operational targets with OPEN reason.',
                'same_source_detector_gain': 'Computed future from analytical GR440 norm in each reference PSD, fixed source and amplitude across PSDs',
                'same_source_gain_status': 'INPUT_O4_MODE_SNR_ANCHOR_NOT_MEASURED_ASTROPHYSICAL_AMPLITUDE',
                'R_PROP_and_COHERENT': 'Explicit OPEN rows, no universal exponential rate; R-GLOBAL zero by construction',
                'R_MOD_scope': 'CONJECTURE_RESTRICTED_KMS_AND_MODULAR_CLOCK__NO_GLOBAL_KERR_HARTLE_HAWKING'},
            'posterior': {'path': posterior, 'sha256': source['sha256'], 'label': 'pSEOBNRv5PHM', 'N': c4['N'],
                'event': 'GW250114', 'statute': 'NONBLIND_CALIBRATION_ALREADY_AUDITED',
                'mass_frame': 'final_mass_non_evolved detector frame, as audited C4; redshift retained sample by sample',
                'prior_strings': {k: v[1] for k, v in c4['priors'].items()}, 'bounds': {k: v[0] for k, v in c4['priors'].items()},
                'bandwidth_multipliers': [.7, 1., 1.3], 'ESS_min': 100,
                'estimators': ['Paired-residual 2D Scott KDE with three bandwidths, full sample', 'Independent 2D Gaussian full moments, no KDE bandwidth'],
                'estimand': 'log p_residual(0)-log p_free_sector(0); same paired sample, other mode marginalized identically',
                'range_scope': 'Estimator sensitivity, not CI or frequentist coverage. Gaussian moments do not solve hard-prior boundaries.',
                'boundaries': 'Report marginal quantiles, edge fractions and unbounded KDE mass outside each original prior; no silent boundary renormalization.',
                'global_prior_and_nuisance_normalization': 'OPEN; uniform tested-coordinate ratio=1 does not by itself prove global evidence contract',
                'lnB': None, 'KDE4D_evidence': False, 'joint_220_440_lnB': None,
                'double_count': 'Do not multiply 220 and 440 marginal diagnostics from the same event',
                'sample_selection': 'All 40776 paired draws; no thinning, seed, bandwidth selection or sample filtering'},
            'fixed_free_robustness': {'status': 'OPEN_NO_MATCHED_FIXED440_PRODUCT_IDENTIFIED_IN_AUDITED_C4_SCHEMA',
                'available': 'GW250114 single archived pSEOBNRv5PHM posterior with both 220 and 440 free; 32/33 catalog products fix higher-mode deviations in other events',
                'not_comparable': ['Different events do not isolate the fixed/free440 effect', 'Conditioning the free440 posterior near zero is not an independent fixed440 recovery', 'The one LVK injection compares injected mode content, while both recovery products have free440'],
                'comparison_executed': False, 'new_PE_required_for_matched_fixed_free': 'OPEN; no such PE authorized here'},
            'output_scope': 'All ten readings and both physical variants in forecasts. 220 and 440 sector diagnostics explicitly separate. Joint220+440 evidence and matched fixed/free comparison remain OPEN when unsupported.'},
        'E5': {
            'models': [
                {'name': 'BROWNIAN_PHASE', 'statute': 'INPUT_ORDER_ROUTE_IV_UNRAVELING', 'law': 'dphi=sqrt(2*Gamma) dW; E exp(i phi)=exp(-Gamma*t)', 'recovered_frequency_scatter': None, 'limitation': 'White frequency noise has no finite pointwise frequency variance; finite-window estimator transfer required'},
                {'name': 'CAUCHY_PHASE', 'statute': 'ALTERNATIVE_CONDITIONAL_UNRAVELING_CONTROL', 'law': 'Symmetric stable increments with scale Gamma*dt; same first-harmonic ensemble decay', 'variance': None, 'limitation': 'No finite increment variance; cannot reuse Gaussian sigma_pop or Brownian transfer'},
                {'name': 'POISSON_COHERENT_OCCUPATION', 'statute': 'CONJECTURE_EFFECTIVE_OSCILLATOR', 'law': 'F(t)=sum_n Pois(n;N) exp[-beta*omega*t/(2*(sqrt(n+1)+sqrt(n))^2)]', 'limitation': 'Poisson is occupation weights here, not a Poisson time-jump process. N/amplitude mapping and fitting window OPEN; not single exponential'},
                {'name': 'COMPOUND_POISSON_TIME_JUMPS', 'statute': 'OPEN_MODEL_NOT_DEFINED_BY_OCCUPATION_SUM', 'law': 'Characteristic exponent lambda*(E exp(iJ)-1) if chosen', 'limitation': 'Jump law/intensity and estimator transfer not supplied; no sigma or event rate assigned'},
                {'name': 'DETERMINISTIC_ENSEMBLE', 'statute': 'DERIVED_CONDITIONAL_MEAN', 'law': 'h_GR*exp(-Gamma*t); ensemble delta_f=0', 'intrinsic_phase_jitter': 0, 'limitation': 'Zero intrinsic jitter in this deterministic model does not imply zero recovered scatter or bias'}],
            'statistic': {'name': 'HETEROSCEDASTIC_GAUSSIAN_PROFILE_LRT_SYNTHETIC_INPUT',
                'variance': 'v_i=sigma_i^2+sigma_sys^2+q, q=sigma_jit_rec^2>=0; total intrinsic sigma_pop^2=sigma_sys^2+q',
                'null': 'q=0 i.e. sigma_pop=sigma_sys; not null total width zero unless sigma_sys=0 lower-bound scenario',
                'alternative': 'q>0; common mean mu profiled under both hypotheses',
                'loglike': '-0.5 sum_i[log(2*pi*v_i)+(y_i-mu)^2/v_i]',
                'threshold': 25.0, 'crossing': 'LRT>25.0', 'p_value': None,
                'calibration': 'Separate heterogeneous route-IV null using registered real sigma_i and empirical tail/upper limit; not scalar matched-filter null',
                'five_sigma_claim': False, 'odds_not_LRT': 'Bayes odds additionally require model/prior normalization; no equivalence assumed'},
            'full_posterior': {'observable': 'sigma_pop of delta_f220, all full paired posterior samples, never population of medians',
                'prepared_identity': 'logscore=sum_i log(mean_s Normal(df_is|mu,sigma_pop)/pi_i(df_is))',
                'uniform_prior': 'pi_i=1/W_i; factor W_i retained per event. Ratio=1 only where identical constant tested priors cancel in a specified comparison.',
                'global_contract': 'OPEN nuisance-prior compatibility, complete support, selection alpha(Lambda) and calibration; not a calibrated hierarchical likelihood',
                'point_null': 'sigma_pop=0 is not approximated by a silently chosen small Gaussian; needs separately registered density/delta-null method',
                'execution': 'Utility prepared; no full-posterior population fit in this package; principal owns nuisance'},
            'information': {'formula': 'I(q=0)=0.5*sum_i(sigma_i^2+sigma_sys^2)^(-2) in Gaussian model; relative weight=1/sigma_i^4 only when sigma_sys=0',
                'known_mean_scope': 'Local expected information; fitted-mean finite-N effects and tails need calibration',
                'sigma_input': 'Archived full posterior std_ddof1 of df, a planning proxy for measurement error',
                'no_double_weight': 'Do not multiply an already heteroscedastic log likelihood by sigma^-4 again',
                'sample_policy': 'All E0.3 eligible events; no posterior-width cut. Archived31/33/10/18 are calibration scenarios, not E2 test selection.'},
            'secondary': {'statute': 'PROPOSED_INPUT_FOR_E2_TO_PIN', 'statistic': 'Fraction |delta_f_hat_i-mu_hat|>3*sigma_i; report uncentered |delta_f_hat_i|>3*sigma_i alongside as order wording',
                'center': 'Profile common mean; its fit and estimator must also be reproduced under null',
                'event_estimator': 'Posterior mean proposed diagnostic; not substitute for primary full-posterior inference',
                'interpretation': 'Sensitivity to heavy tails/jumps, not unique evidence of Poisson/Cauchy law',
                'multiplicity': 'Secondary only; separately calibrated after fixed selection, with false-alarm allocation decided in E2; no sigma claim'},
            'jitter_transfer': {'status': 'OPEN', 'sigma_jit_rec': None, 'needed': 'Brownian injections through registered recovery pipeline, finite window, source convention and seeds; future E3 owner, not executed here'},
            'sigma_sys': {'status': 'OPEN', 'delta_f_floor': None, 'needed': 'GR two-family calibration in delta_f channel; C5 a/dtau bias is not delta_f sigma_sys'},
            'N_targets': 'LOWER_BOUND_SCENARIOS_UNTIL_TRANSFER_AND_SYSTEMATICS; no physical detection promise',
            'historical_sigma_limit': {'value': .0243, 'level': .90, 'MLE': 0, 'statute': 'DECLARADO_IN_ORDER_NONBLIND_EXPLORATORY_NOT_RECOMPUTED_HERE'},
            'archived_information_populations': ['GWTC5_31', 'GWTC5_33', 'GWTC3_10', 'GWTC3_18'],
            'scientific_reading_selected': False},
        'activation': {'required_status': 'AUTHORIZED_BY_PRINCIPAL_AFTER_E2',
            'allowed_task': 'E4_E5_DETERMINISTIC_ARCHIVED_CALIBRATION_ONLY',
            'pins': ['PLAN.json', 'INPUT_MANIFEST.json', 'SCHEMA.json', 'deterministic_e4_e5.py'],
            'E2_field': 'e4_e5_preparation_pins must equal activation package_sha256 map',
            'witness': 'Existing outgoing tunnel note includes actual E2 registration SHA256; registration and witness separately hashed',
            'run': 'python -B -O deterministic_e4_e5.py --execute --authorization <principal_activation.json>',
            'authorization_is_not_generated_here': True, 'new_test_data_allowed': False,
            'dependencies': 'Existing WSL /opt/lal_env numpy/scipy/h5py; not imported/tested scientifically during preparation',
            'output': 'Only own runs/<new_run_id>/DETERMINISTIC_DIAGNOSTICS.json plus RESULT_RECEIPT.json; wall and process CPU recorded; require no existing directory; source pins rechecked before and after'},
        'not_executed': ['Fisher440', 'QNM predictions', 'posterior value access', 'density fitting', 'population inference', 'MC/null', 'PE', 'waveform generation', 'test strain', 'E2 registration']}
    write('PLAN.json', plan)
    doc = ['# Preparação E4/E5 — somente documental, metadados e código', '',
        '**[REAL] Preparação concluída; cálculos científicos novos não executados. [INPUT] Plano para o principal fixar antes do registro E2.**', '',
        'A ordem foi relida nas seções E4/E5 e na sequência E0→E1→E2→E5/E4. O executável exige ativação expressa do principal, os hashes deste pacote dentro do registro E2 e a testemunha no túnel. Não foi criado registro nem autorização. A trava roda antes de scipy/h5py, leitura de valores HDF, previsão e mkdir. Execução anterior dos artefatos de referência é do agente principal autorizado, não atribuída ao humano.', '',
        '## E4 preparado', '',
        'Fisher analítico local do440, fonte INPUT fixa Mdet=68,1M☉, chi=0,68, z=0; quatro PSDs O4/O5/ET/CE, dez leituras, duas variantes físicas, dois perfis de frequência e duas rotas SNR. Derivada dH/d(delta_tau)=+.5*d*(1/zm²+1/zp²) em GR. Amplitude/fase marginalizadas. SNR é do **440 isolado**, sem conversão IMR/rede. A rota de rho igual por PSD compara formas; AMPLITUDE_FIXA_INPUT ancora A=rho440_O4_INPUT/||h||_O4 e transporta rho_PSD por ||h||_PSD/||h||_O4. A âncora é INPUT, não amplitude medida deGW250114.', '',
        'N50=25/z² [INPUT E(Z)=5]; N90condicional=(5+1,2815515655446004)²/z², para Z gaussiano unilateral de variância conhecida1 e fontes idênticas independentes sem sistemáticas. Não são significância calibrada nem promessa de taxa física. Para efeito zero, ausente ou |delta|<1e−12, os alvos operacionais são null/OPEN; previsões sub-resolução não viram números astronômicos de eventos. Massa/spin livres permanecem degenerados no modo isolado.', '',
        'O GW250114 já auditado fornece o produto livre com 40776 amostras pareadas. Preparados KDE residual 2D em três bandas e gaussiana 2D de momentos, para 220 e 440 separadamente. Faixa entre estimadores, ESS local, quantis, fração próxima da borda e massa KDE fora do prior serão reportadas; a faixa não é IC. Não há KDE4D novo, produto de marginais ou promoção a evidência. **lnB calibrado/global fica null:** razão unitária nos priors uniformes de deformação não fecha o contrato dos nuisances, seleção e suporte. O código entrega log-razões de densidade condicionais com seu nome exato.', '',
        'As variantes só-220 e 220+440 aparecem nas previsões. Deformar440 é INPUT; nenhuma leitura é escolhida. O diagnóstico marginal220 conserva440 livre como nuisance: não equivale a recuperação com440 fixo. Não foi identificado no schema auditado um segundo produto da mesma fonte/configuração com440 fixo. Comparar outros32 eventos comGW250114 ou condicionar fatia do posterior livre não paga essa robustez. A comparação conjunta e o efeito fixo/livre permanecem OPEN.', '',
        'R-PROP e R-RAIZ-COHERENT têm linhas OPEN sem um único amortecimento exponencial. R-GLOBAL tem efeito relativo zero por construção. R-MOD mantém o escopo KMS restrito, sem estado global Hartle–Hawking de Kerr.', '',
        '## E4.4 metadados já executados', '',
        'Snapshot GWOSC do E0, sem nova consulta de disponibilidade: '+str(meta['observation_snapshot'])+'. Tabela1 histórica TGR4 pp2–3 acrescenta GR O1–O3; PDF/texto conferidos campo a campo. Mescla declarada: propriedades GR antigas e versão GWOSC preferida do E0, não nova PE. Nenhum chi_eff usado como chi_f. Medianas/centrais seguem a convenção catalogal herdada; não são inspiral isolada nem dados independentes do strain.', '',
        '| corrida | SNR≥12 | passa INPUT | falha conhecida | aguarda GR | prioridade elegível ≥30 |',
        '|---|---:|---:|---:|---:|---:|']
    for run, r in meta['by_run'].items():
        doc.append(f"| {run} | {r['SNR_ge12']} | {len(r['eligible'])} | {len(r['known_fail'])} | {len(r['awaiting_GR'])} | {len(r['priority_eligible'])} |")
    doc += ['', 'Listas nominais completas por corrida (JSON também inclui os cortes≥12/30/53/78/95):', '']
    for run, r in meta['by_run'].items():
        doc += [f"- **{run}, elegíveis:** {', '.join(r['eligible']) or 'nenhum com GR disponível'}.",
                f"- **{run}, aguardando GR:** {', '.join(r['awaiting_GR']) or 'nenhum'}."]
    doc += ['', 'GW250207_115645: candidato futuro de teste previsto pela ordem, SNR '+str(meta['GW250207_status']['network_snr_GWOSC'])+' no snapshot; GR ausente, elegibilidade null e cegueira não certificada. O4c é janela de um evento de descoberta, não censo completo. Não foi aberto posterior/strain de teste, e ausência no corpus39 não significa ausência universal de publicação.', '',
        '## E5 preparado', '',
        'O plano distingue fase browniana, fase Cauchy, soma coerente com ocupações Poisson, saltos temporais Poisson ainda não especificados e sinal determinístico. Cauchy não tem variância finita. Ocupações Poisson não são processo temporal de saltos. Ensemble delta_f=0 não fixa a dispersão do estimador numa realização.', '',
        'Mantidos OPEN sigma_jit,rec (transferência por injeção na pipeline) e sigma_sys do canal delta_f (duas famílias GR). N físico continua cenário de limite inferior. C2/C5 e a única injeção LVK/RD são controles com seus próprios observáveis/janelas, não curva de transferência universal nem cobertura inferida de um ponto.', '',
        'LRT sintético: v_i=sigma_i²+sigma_sys²+q, q≥0, mu livre nos dois modelos, nuloq=0. Limiar25 não vira5sigma sem calibração própria do nulo heterogêneo. A informação local em variância é 1/(2v_i²); 1/sigma_i⁴ vale no cenário sigma_sys=0, sem reponderar duas vezes o log likelihood. Todos os elegíveis entram, sem corte por largura;31/33/10/18 são somente cenários de calibração arquivados.', '',
        'Preparada identidade de integração sobre todas as amostras, conservando as constantes W_i dos priors uniformes; não ajusta nuisance nem executa fit populacional. O limite pontual sigma_pop=0 não recebe largura arbitrária escondida. Seleção/normalização/suporte global permanecem OPEN: nunca chamar KDE ajustado de likelihood populacional hierárquica calibrada. Estatística secundária de outliers centrada, com a forma não centrada da ordem ao lado, foi proposta como INPUT para E2 fixar e calibrar separadamente.', '',
        '## Custódia e próximos passos do principal', '',
        'Fixar PLAN.json, INPUT_MANIFEST.json, SCHEMA.json e deterministic_e4_e5.py no campo e4_e5_preparation_pins do E2. Registrar nota testemunha no túnel; somente depois emitir ativação no formato descrito em PLAN.activation. O executor recusa pins divergentes e grava apenas runs/<id_novo> nesta pasta. Resultado e recibo registram wall e CPU de processo, com alcance do relógio explícito. Nenhum produtor, manifesto anterior, memória ou canônico foi alterado.', '',
        'Verificação feita nesta etapa: parsing/compilação em memória sob optimize1, inspeção de imports/guardas, hashes reais dos arquivos, extração/junção documental. **Não há validação numérica do executável ainda**; pequenos controles determinísticos independentes das fórmulas e comparação com220 devem ser feitos pelo principal após ativação antes de interpretar saídas. As funções de inferência populacional são utilitários preparados, não tarefas acionadas pelo CLI deste pacote.', '',
        'Hashes para registro:', '']
    for name in ['PLAN.json', 'INPUT_MANIFEST.json', 'SCHEMA.json', 'deterministic_e4_e5.py']:
        doc.append(f'- `{name}`: `{sha(O/name)}`.')
    doc += ['']
    write('PREPARATION.md', '\n'.join(doc))
    # Real schema validation if library exists, not a scientific import/run.
    import jsonschema
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(plan, schema)
    require(all(sha(B/r['path']) == r['sha256'] for r in FILES.values()), 'Inputs changed during preparation')
    receipt = {'status': 'PASS_METADATA_AND_STATIC_PREPARATION_ONLY', 'utc': datetime.now(timezone.utc).isoformat(),
        'python_optimize': sys.flags.optimize, 'scientific_code_executed': False, 'HDF_values_read': False,
        'new_network_access': False, 'registration_created': False, 'activation_created': False,
        'static_AST_compiled': True, 'schema_validated': True, 'production_bytes_unchanged': True,
        'input_count': len(FILES), 'old_GR_validation': meta['old_GR_validation'],
        'elapsed_s': time.perf_counter()-START,
        'outputs': {n: {'sha256': sha(O/n), 'bytes': (O/n).stat().st_size} for n in targets if n != 'STATIC_RECEIPT.json'},
        'scripts': {p.name: sha(p) for p in [code, Path(__file__)]}}
    write('STATIC_RECEIPT.json', receipt)
    print(json.dumps({'status': receipt['status'], 'plan_sha256': sha(O/'PLAN.json'), 'by_run': meta['by_run'], 'seconds': receipt['elapsed_s']}))


if __name__ == '__main__':
    main()
