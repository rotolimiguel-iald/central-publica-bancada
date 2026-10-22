"""Cross-check the objective against actual artifacts without promoting gates."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict
import hashlib
import json
import math
from fetch_public import atomic_json

ROOT = Path(__file__).resolve().parent


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(8*1024*1024):
            h.update(block)
    return h.hexdigest()


def write_new(path, text):
    if path.exists():
        raise FileExistsError('Preserve prior audit: ' + str(path))
    raw = text.encode('utf-8')
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_bytes(raw)
    if tmp.stat().st_size != len(raw):
        raise ValueError('Short write')
    tmp.replace(path)


def main():
    target = ROOT / 'C7_REQUIREMENTS_AUDIT.json'
    if target.exists():
        raise FileExistsError('Preserve prior audit')
    evidence = {}

    def load(name):
        path = ROOT / name
        evidence[name] = dict(bytes=path.stat().st_size, sha256=sha(path))
        return json.loads(path.read_bytes())

    def cite(*names):
        for name in names:
            path = ROOT / name
            evidence[name] = dict(bytes=path.stat().st_size, sha256=sha(path))
        return list(names)

    checks = []

    def row(identifier, requirement, outcome, files, finding):
        checks.append(dict(id=identifier, requirement=requirement, outcome=outcome,
                           evidence=cite(*files), finding=finding))

    c0 = load('C0_AUDITORIA.json')
    original = ROOT.parent / 'TUNEL/PARA_CHATGPT/ORDEM_013_INSUMOS/TEXTO_CONFRONTACAO_OPERADOR_21SET_VERBATIM.md'
    if sha(original) != c0['input_sha256']:
        raise ValueError('Audited user text changed')
    lines = original.read_text(encoding='utf-8-sig').splitlines()
    required = {i for i in range(3, 66) if lines[i-1].strip()}
    covered = {i for claim in c0['claims'] for i in claim['lines']}
    if required - covered:
        raise ValueError('User claim absent from audit')
    if not all(c['evidence'] and c['what_the_text_gets_right'] and c['corrected_public_sentence'] for c in c0['claims']):
        raise ValueError('Incomplete claim audit')
    row('C0.a,e', 'Atomic claims, nonempty lines 3-65, sources and corrected sentences', 'VERIFIED_ARTIFACT',
        ['C0_AUDITORIA.json', 'C0_AUDITORIA.md'],
        f'{len(c0["claims"])} claims; {len(required)} required lines covered. Literature access scope remains explicit, not upgraded.')
    algebra = load('C0_C3_checks.json')
    if algebra['liouvillian_eigenvalue_residual'] >= 1e-12 or algebra['jump_shift_generator_residual'] >= 1e-12:
        raise ValueError('Algebra control failed')
    if algebra['units']['GM_over_c3_SI_exponents'] != [0,0,1]:
        raise ValueError('Dimensional correction missing')
    if algebra['signed_modular_extensions']['positive_part_rates_per_clock'] == algebra['signed_modular_extensions']['absolute_value_rates_per_clock']:
        raise ValueError('Distinct positive extensions lost')
    row('C0.b,c,d', 'Units, independent Liouvillian, jump-count distinction, signed-generator choices', 'VERIFIED_CONDITIONAL_RESULT',
        ['verify_c0_c3.py','C0_C3_checks.json','C2_MAPEAMENTO_ANALITICO.md'],
        'Independent Kronecker Liouvillian and spectral gaps agree; K+ and |K| differ. GM/c^3 is a time. No physical extension selected.')

    c1 = load('C1_TABLES.json')
    for item in c1['rows']:
        pred = item['prediction']
        if pred.get('gamma_per_s') is not None:
            if not math.isclose(pred['gamma_per_s']/pred['omega_rad_s'], pred['gamma_over_omega'], rel_tol=1e-12, abs_tol=1e-100):
                raise ValueError('Rate/frequency inconsistency')
        if pred.get('delta_tau_ensemble_exact') is not None:
            x = pred['x']
            if not math.isclose(-x/(1+x), pred['delta_tau_ensemble_exact'], rel_tol=1e-12, abs_tol=1e-100):
                raise ValueError('Damping-time convention inconsistency')
    row('G1/C1', 'Gamma(M,spin,D), clocks, FP-5, root/quadratic/linear/global/propagation alternatives', 'VERIFIED_CONDITIONAL_RESULT',
        ['C1_TABLES.json','C1_LEITURAS_E_RELOGIOS.md','C2_MAPEAMENTO_ANALITICO.md','tgl_ringdown_prediction.py'],
        'C1_LEITURAS_E_RELOGIOS.md + C1_TABLES.json implement the requested C1 table under descriptive filenames. Local source rate does not depend directly on distance; propagation is a separate spectral model. Physical clock/partition remain unselected as ordered.')
    row('G2/C1', 'Evaluate Gamma/omega, rather than assert it is small for every interpretation', 'VERIFIED_CONDITIONAL_RESULT',
        ['C1_TABLES.json','C7_GWTC3_EVENT_READINGS.csv','C7_INDEPENDENT/tables/event_reading_predictions.csv'],
        'Dimensionless ratios are evaluated by reading and event. Small Gamma/omega does not itself establish detectability or exclusion; source/clock and QNM domain restrictions apply.')
    row('C1.MOD', 'Corotation, modular/Killing clock and Kerr state hypotheses', 'CONDITIONAL_WITH_SOURCE_LIMIT',
        ['C1_TABLES.json','C1_LEITURAS_E_RELOGIOS.md','C0_ADENDO_ESCOPO_LITERATURA.md','QNM_GRID.json'],
        'Positive finite KMS oscillator checked; exact Kerr QNM used for the corotating gap. It is not a construction of the physical Kerr state. Kay-Wald and Milburn were read only at abstract scope; broader claims are not supported here.')

    trajectory = load('C2_TRAJECTORY_RECOVERY.json')
    cells = [c for r in trajectory['rows'] for c in r['comparisons']]
    if min(c['N'] for c in cells) < 50 or any(c['optimizer_failures'] or c['boundary_count'] for c in cells):
        raise ValueError('Trajectory recovery control requires inspection')
    row('C2', 'Ensemble, single trajectories, energy/power, finite occupation and colored noise', 'VERIFIED_CONDITIONAL_RESULT',
        ['C2_MAPEAMENTO_ANALITICO.md','C2_TRAJECTORY_RECOVERY.json','C3_UNRAVELING_API.json','trajectory_recovery.py'],
        f'{len(cells)} estimator/noise cells, {sum(c["N"] for c in cells)} fits. Colored noise here is declared synthetic OU+white; later C5 uses actual off-source intervals. Large N~10^78 is an analytic initial-slope extrapolation, not an exact finite computation or measured occupation.')
    if max(v['relative_error'] for v in algebra['legacy_regression'].values()) > 1e-12:
        raise ValueError('Legacy numerical regression failed')
    compatibility = load('C3_PREDICTION_COMPATIBILITY.json')
    api = load('C3_UNRAVELING_API.json')
    if compatibility['current_prediction_sha256'] != sha(ROOT/'tgl_ringdown_prediction.py') or api['source_sha256'] != sha(ROOT/'tgl_ringdown_unravelings.py'):
        raise ValueError('API reports do not match delivered sources')
    row('G4/C3', 'Public prediction and waveform modules; a=0/1, constants regression and actual consumer', 'VERIFIED_CONDITIONAL_RESULT',
        ['tgl_ringdown_prediction.py','tgl_ringdown_template.py','tgl_ringdown_unravelings.py',
         'C3_PREDICTION_COMPATIBILITY.json','C3_MULTIMODE_TEMPLATE.json','C3_UNRAVELING_API.json'],
        'Legacy A/B within 1e-12; 264 later predictions unchanged; actual Bilby consumers checked. Higher modes need explicit exact QNM and angular projection. Not a full inspiral-merger modified-gravity waveform or pyRing plugin.')

    current = load('C4_CATALOG_220.json')
    old = load('C4_GWTC3_220.json')
    joint = load('C4_CATALOG_COMBINATION.json')
    oldjoint = load('C4_GWTC3_PUBLISHED_COMBINATION.json')
    if len({r['event'] for r in old['rows']}) != 18 or len({r['event'] for r in current['rows']}) != 33:
        raise ValueError('Duplicate/missing event in release')
    overlap = {r['event'] for r in old['rows']} & {r['event'] for r in current['rows']}
    if overlap != set(old['duplicate_reconciliation']['overlap']):
        raise ValueError('Cross-release identity audit differs')
    row('C4.sources', 'Actual released samples, prior semantics, file custody and no repeated event evidence', 'VERIFIED_WITH_PROVENANCE_LIMIT',
        ['C4_CATALOG_220.json','C4_GWTC3_220.json','C4_GWTC3_SCHEMA.json','C4_GWTC3_CONVENTIONS.json',
         'C4_GWTC3_SELECTION.json','C4_CATALOG_PRIOR_AUDIT.json'],
        f'33 newer and 18 older products, {len(overlap)} overlaps. Release-specific combinations are alternatives, never multiplied. Legacy executable/remnant fit and some pyRing merge provenance remain unavailable.')
    row('C4.statistics', 'Joint densities, sample-dependent predictions, marginals, prior alternatives and GR-relative decisions', 'VERIFIED_CONDITIONAL_RESULT',
        ['C4_220_INITIAL.json','C4_JOINT_MODES.json','C4_FREE_CLOCK.json','C4_CATALOG_COMBINATION.json',
         'C4_GWTC3_PUBLISHED_COMBINATION.json','REGISTRO_C4.json','posterior_220_readout.py','free_clock_posterior.py'],
        'Joint KDE/conditional-curve results, bootstrap/bandwidth controls and two free-clock priors are explicit. Catalog verdict remains INCONCLUSIVE_SYSTEMATICS, including GR-region and local-density qualifications. No ln B-to-sigma conversion.')

    forecast = load('C5_RECOLORED_FORECAST.json')
    numeric = load('C5_RECOLORED_VALIDATION.json')
    if len(forecast['results']) != forecast['number_of_cells'] or any(r['N'] < 50 for r in forecast['results']):
        raise ValueError('Incomplete forecast matrix')
    grouping = defaultdict(list)
    for r in forecast['results']:
        if r['absolute_bias'] is not None:
            criterion = r['absolute_bias'] <= .2 and .8 <= r['coverage_90'] <= .97
            if criterion != r['original_numeric_criteria_pass']:
                raise ValueError('Calibration label inconsistent with measured criteria')
        if r['content'] == 'FULL_IMR':
            grouping[(r['psd'],r['recovery'],r['reading'],r['SNR'])].append(r)
    both = [k for k,v in grouping.items() if len(v)==4 and all(r.get('original_numeric_criteria_pass',False) for r in v)]
    row('G3/C5.compute', 'O4/O5 distributions under both hypotheses, PSD controls and full injection matrix', 'VERIFIED_CONDITIONAL_RESULT',
        ['C5_FISHER_EMPIRICAL.json','PSD_CONTROLS.json','C5_RECOLORED_FORECAST.json',
         'C5_RECOLORED_VALIDATION.json','forecast_recolored_imr.py','verify_recolored_forecast.py'],
        f'{len(forecast["results"])} cells with 50 paired intervals each, actual off-source O4 noise recolored to design PSDs, two IMR families and six SNRs. Reused intervals are not independent observations; remnant is fixed in this forecast. O5 is a sensitivity scenario, not a promise.')
    row('C5.acceptance', 'Bias <=0.2 and 90% coverage in [0.80,0.97] across both IMR families', 'FAILED_SCIENTIFIC_ACCEPTANCE',
        ['C5_RECOLORED_FORECAST.json','C5_RECOLORED_VALIDATION.json'],
        f'{len(both)} FULL_IMR groups pass both families and both injected amplitudes. Negative result retained. Passing numerical reproduction or a selected cell cannot replace this gate.')

    c6 = load('C6_RESULTS.json')
    registration = load('REGISTRO_C6.json')
    if c6['registration_sha256'] != sha(ROOT/'REGISTRO_C6.json'):
        raise ValueError('C6 registration changed')
    for name, digest in registration['code_and_input_hashes'].items():
        if sha(ROOT/name) != digest:
            raise ValueError('Frozen C6 source changed: '+name)
    if not all(x['passed'] for x in c6['convergence']):
        raise ValueError('Unconverged C6 quadrature')
    row('C6.registration', 'Nonblind pre-read registration, guards, actual strain and all five starts', 'VERIFIED_MEASUREMENT',
        ['REGISTRO_C6.json','C6_RESULTS.json','C6_GUARD_TEST.json','C7_INDEPENDENT/C6_REPRODUCTION_RESULT.json'],
        'Frozen input hashes still match; all starts converge; full registered strain result reproduced in a fresh copy. Code/input/registration mutations are refused. Physical interpretation remains INCONCLUSIVE_SYSTEMATICS.')
    row('C6.external_comparison', 'Comparison with released pyRing analyses at corresponding starts', 'PARTIAL_NOT_IDENTICAL_REPRODUCTION',
        ['C6_PYRING_START_COMPARISON.json'],
        'Eight released products at 6/8/10/12 tM compared. No 10.5 tM product exists in the inspected release. PSD, trigger, modes and priors differ; identical pyRing inference was not reproduced. This cannot validate model adequacy by itself.')

    package = load('C7_PACKAGE_VALIDATION.json')
    supplements = load('C7_SUPPLEMENTS_VALIDATION.json')
    gwpackage = load('C7_GWTC3_REPRODUCTION_VALIDATION.json')
    if any(x['status'] != 'PASS' for x in [package, supplements, gwpackage]):
        raise ValueError('Unverified reproduction package')
    row('C7', 'English package, event/readout tables, modules and fresh-directory regeneration', 'VERIFIED_WITH_EXPLICIT_SCOPE',
        ['C7_INDEPENDENT/README.md','C7_POSTERIOR_REPRODUCTION/README.md',
         'C7_INJECTION_REPRODUCTION/README.md','C7_GWTC3_REPRODUCTION/README.md',
         'C7_PACKAGE_VALIDATION.json','C7_SUPPLEMENTS_VALIDATION.json','C7_GWTC3_REPRODUCTION_VALIDATION.json'],
        'Waveform demo and registered strain reproduced; posterior stages, injection chain and GWTC-3 replay verified. Public URLs/hashes permit download, but this round used local verified archives. Original LVK samplers and independent external review are not claimed.')

    stamp = datetime.now(timezone.utc).isoformat()
    report = dict(status='REQUIREMENTS_INSPECTED__NO_PHYSICAL_ACCEPTANCE_PROMOTION', date_utc=stamp,
        goal_completion_claimed=False, requirements=checks, evidence=evidence,
        mathematical_scope='Conditional implications from specified generators/clocks; not a unique physical identification',
        C5_full_IMR_groups_passing_all=len(both),
        unresolved_acceptance=['C5 two-family bias/coverage gate failed',
            'C6 pyRing comparison differs in model/priors and lacks a released 10.5 tM product',
            'Physical partition, clock and observed unraveling were intentionally not selected'],
        source_access_limits=['Kay-Wald and Milburn full texts not read here',
            'Legacy executable/remnant and pyRing merging provenance unavailable'],
        remaining_delivery_review='Inspect this consolidated audit and English overview against original objective before any goal completion decision')
    atomic_json(target, report)
    text = ['[REAL — artefatos inspecionados; DERIVED condicional; não declara conclusão do objetivo]\n',
            '# Auditoria de requisitos da Ordem 013\n', stamp+'\n',
            'Os resultados numéricos e os critérios científicos têm colunas distintas. Uma reprodução correta pode reproduzir um resultado inconclusivo ou uma calibração reprovada.\n',
            '| Item | Requisito | Resultado da auditoria | Evidência |',
            '|---|---|---|---|']
    for item in checks:
        links = ', '.join(f'[{name}]({name})' for name in item['evidence'])
        finding = item['finding'].replace('|', '&#124;')
        requirement = item['requirement'].replace('|', '&#124;')
        text.append(f'| {item["id"]} | {requirement} | {item["outcome"]}: {finding} | {links} |')
    text += ['\nOs hashes e tamanhos medidos estão no JSON companheiro. N/A — sem Lean novo.',
        '\nA auditoria não aceita o requisito de calibração como pago: nenhuma combinação testada passou simultaneamente nas duas famílias. A comparação com pyRing é parcial, com diferenças expressas. As tabelas e formas de onda são entregas condicionais, sem escolha de partição física.',
        '\nOs campos `remaining`, `pending` e textos de trabalho dos primeiros artefatos são históricos. A reprodução dos posteriores, injeções, strain e GWTC-3 está documentada nos suplementos posteriores; não deve ser refeita por causa desses campos antigos.']
    write_new(ROOT/'C7_REQUIREMENTS_AUDIT.md', '\n'.join(text)+'\n')

    event_rows = [r['prediction'] for r in c1['rows'] if r['event']=='GW250114_public_posterior_medians']
    new_b = next(r for r in joint['catalog']['release_figure_selection_31'] if r['reading']=='R-B')
    old_b = next(r for r in oldjoint['catalog'] if r['reading']=='R-B')
    strain_b = next(r for r in c6['results'] if r['reading']=='R-B' and r['primary_start'] and r['amplitude_prior_sd_strain']==1e-20)
    scenario = [r for r in forecast['results'] if r['family']=='SEOBNRv4HM' and r['psd']=='O5_Aplus'
                and r['recovery']=='220_440' and r['reading']=='R-B' and r['SNR']==40. and r['content']=='FULL_IMR']
    # Validate PSD label from the measured matrix rather than silently choosing a row.
    if not scenario:
        scenario = [r for r in forecast['results'] if r['family']=='SEOBNRv4HM' and r['psd']=='O5'
                    and r['recovery']=='220_440' and r['reading']=='R-B' and r['SNR']==40. and r['content']=='FULL_IMR']
    if len(scenario)!=2 or {r['injected_a'] for r in scenario}!={0.,1.}:
        raise ValueError('Inspect O5 scenario labels')
    overview = ['# Conditional TGL ringdown: consolidated delivery',
        '\nInternal research handoff for independent review. TGL: Luiz Antonio Rotoli Miguel. This addendum consolidates the delivered packages; earlier files remain dated records. It does not select a physical clock, partition or strain unraveling. It does not change a mathematical gate or claim physical confirmation.\n',
        '## Four requested results\n',
        '1. **Functional law.** For a self-adjoint jump L=f(H), Gamma_ij=(f(E_i)-f(E_j))^2/2. For the conditional oscillator with the quadratic energy generator, Gamma=beta*tau_star*omega^2/2. For the existing mass-clock reading B, tM=G*M_detector/c^3 and Gamma=beta*w(spin)^2/(2*tM). Distance affects amplitude/SNR and cosmological frame conversion, not the local source rate. Propagation over D is a separate, explicitly conditional spectral model.',
        '2. **Size relative to QNM frequency.** The following entries are evaluated at the released GW250114 posterior medians. They are conditional examples, not fitted beta or proof of the clock identification. Beta is computed at runtime as ALPHA_FINE_CODATA_2018*sqrt(e).\n',
        '| Reading | Gamma [1/s] | Gamma/omega | Exact ensemble delta_tau |',
        '|---|---:|---:|---:|']
    for p in event_rows:
        if p.get('delta_tau_ensemble_exact') is not None:
            overview.append(f'| {p["reading"]} | {p["gamma_per_s"]:.9g} | {p["gamma_over_omega"]:.9g} | {p["delta_tau_ensemble_exact"]:.9g} |')
    overview += [
        '\nGamma is an amplitude/coherence rate. The ensemble waveform is A exp[-(1/tau_GR+Gamma)t] cos(omega*t+phi), with delta_tau=-x/(1+x), x=Gamma*tau_GR. Energy dephasing conserves oscillator populations. Single stochastic phase realizations need not have that deterministic envelope. A coherent root-generator field is generally a Poisson mixture, not one exponential. A bare signed -log Delta cannot be square-rooted as a positive operator without specifying a positive extension.',
        '\n3. **Expected Bayes ratios.** O4/O5 forecasts are distributions conditioned on sensitivity, SNR, waveform family, mode content, readout and priors. For the illustrative SEOBNRv4HM, O5 A+ curve, SNR40, 220+440 FULL_IMR experiment:',
        '\n| Injection | Mean ln B(B/GR) | Standard deviation |',
        '|---|---:|---:|']
    for r in sorted(scenario,key=lambda r:r['injected_a']):
        overview.append(f'| a={r["injected_a"]:g} | {r["lnB"]["mean"]:.9g} | {r["lnB"]["standard_deviation"]:.9g} |')
    overview += [
        f'\nThe full matrix has {len(forecast["results"])} cells, 50 paired off-source intervals each, two IMR families, three recovery mode sets and six SNRs. Noise intervals are reused across cells. Remnant mass/spin are fixed in this forecast: it is optimistic. **{len(both)} FULL_IMR groups passed the requested bias/coverage criteria for both families and both injected amplitudes.** Numerical SVD checks passed; scientific calibration did not. No selected positive log ratio is promoted to detection. O5/ET/CE use design scenarios, not measured future noise or a schedule.',
        '\n4. **Waveforms for independent fits.** C7_INDEPENDENT contains the NumPy prediction, waveform and optional stochastic/finite-occupation APIs, explicit phase/polarization/onset conventions and a working Bilby consumer example. It is a ringdown model, not a complete modified-gravity inspiral-merger template. Other modes require exact QNMs and supplied angular projections.\n',
        '## Actual-data confrontation\n',
        '| Dataset / scope | ln B(B/GR) | Interpretation |',
        '|---|---:|---|',
        f'| GW250114 H1/L1 strain, registered primary start 10 tM | {strain_b["lnB_vs_GR"]:.12g} | INCONCLUSIVE_SYSTEMATICS; amplitude prior sd 1e-20 |',
        f'| Newer catalog, published 31-event selection, conditional 220 sector | {new_b["lnB"]:.12g} | {new_b["verdict"]} |',
        f'| GWTC-3, paper Table 13 minus author exclusions, 10 events | {old_b["lnB"]:.12g} | {old_b["verdict"]} |',
        '\nThese rows are **not independent measurements to multiply**. The catalogs share events and GW250114 is in the newer catalog. Thirty-three newer and eighteen older posterior products were inspected, with twelve overlaps. The all-eighteen older combination remains an auxiliary control, not the publication selection. Joint frequency/damping densities, sample-dependent spin predictions, bandwidth/bootstraps, marginal diagnostics and two free-clock priors are recorded. Common-deformation catalog GR checks fail the registered acceptance condition, so the catalog status remains inconclusive. Some newer-event tail densities also lack sufficient local support.',
        '\nThe registered strain experiment marginalizes remnant mass/spin and detector amplitudes. All five starts and three amplitude priors are retained. Comparison with eight released pyRing products is a model comparison, not exact reproduction: no 10.5 tM product was released and trigger, PSD, mode and prior conventions differ. Original sampler/remnant-postprocessing and some pyRing merging provenance are unavailable. Bayes factors are not frequentist sigma.\n',
        '## Reproduction entry points\n',
        '| Package | Command after unpacking | Scope |',
        '|---|---|---|',
        '| C7_INDEPENDENT | `python run_demo.py --output`; `python reproduce_c6.py --run --download` | Waveform demo and frozen actual-strain measurement |',
        '| C7_POSTERIOR_REPRODUCTION | `python reproduce.py primary --download` (also joint, free_clock, catalog) | Recompute posterior analyses from public samples |',
        '| C7_INJECTION_REPRODUCTION | `python reproduce.py full --download --imr-python /path/to/pycbc/python` | Regenerate IMR, off-source PSD/noise and injection forecast |',
        '| C7_GWTC3_REPRODUCTION | `python reproduce.py full --download` | Older release, literal paper selection and separate joint diagnostic |',
        '\nEach package README gives tested dependencies, source/archive-cache alternatives and file hashes. Use fresh directories. Reproduction receipts are checks of the implemented calculations, not independent physical confirmation. The original LVK samplers are not rerun. This round exercised verified local sources/archives; it did not re-fetch every download URL. No canonical um.py, private stack or credentials are distributed.',
        '\n## Corrections to historical remaining-work notes\n',
        'The original v1 README and early C1/C2 JSON notes predate the posterior/injection/GWTC-3 supplements. Colored-noise trajectories, higher-mode APIs, actual strain, cross-release reconciliation and the supplementary reproductions now exist. Do not repeat them because an old `pending` field survives. The three failed literature fetches were one GW250114 LaTeX archive and two abstract pages, not three unread full articles; the separate C0 addendum states the actual access. Kay-Wald and Milburn remain abstract-only citations here. The conditional finite KMS construction is not their full theorem or a physical Kerr-state construction.',
        '\nThe accompanying C7_REQUIREMENTS_AUDIT.json/.md maps each requested task to measured evidence and explicitly records failed or partial acceptance. The unresolved physical identification and failed calibration are not concealed as packaging work. Further goal-completion review must preserve those distinctions. N/A: no new Lean proof.']
    write_new(ROOT/'C7_DELIVERY_OVERVIEW.md','\n'.join(overview)+'\n')
    print(json.dumps(dict(status=report['status'],requirements=len(checks),evidence_files=len(evidence),
        C5_groups_passing=len(both),overview='C7_DELIVERY_OVERVIEW.md')))


if __name__ == '__main__':
    main()
