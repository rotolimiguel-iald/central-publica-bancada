"""Independent metadata/arithmetic audit. No author helper import or execution."""
from pathlib import Path
from datetime import datetime, timezone
from statistics import NormalDist
import csv
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
R = B.parent
PACKAGE = B / 'bis/e3_budget_wall'
CHECKS = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def unique(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('Duplicate key: ' + k)
        out[k] = v
    return out


def read(p):
    return json.loads(Path(p).read_bytes(), object_pairs_hook=unique,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def check(name, value):
    CHECKS.append({'name': name, 'passed': bool(value)})


def close(name, actual, wanted):
    check(name, type(actual) in (float, int) and math.isfinite(actual)
          and math.isclose(actual, wanted, rel_tol=2e-11, abs_tol=1e-12))


def main():
    candidate_path = PACKAGE / 'ORCAMENTO_40H_CANDIDATE.json'
    initial_sha = sha(candidate_path)
    d = read(candidate_path)
    reg = read(B / 'RINGDOWN_5SIGMA_V1.json')
    original = read(B / 'bis/PART_B_BUDGET_START.json')
    manifest = read(PACKAGE / 'MANIFEST.json')
    entries = manifest['files']
    check('manifest unique paths', len(entries) == len({r['relative_path'] for r in entries}))
    for row in entries:
        p = PACKAGE / row['relative_path']
        check('manifest hash ' + row['relative_path'], p.resolve().is_relative_to(PACKAGE.resolve()) and sha(p) == row['sha256'] and p.stat().st_size == row['bytes'])
    for row in read(PACKAGE / 'FROZEN_INPUTS.json')['files']:
        check('frozen/live bytes ' + row['source_relative_to_Chatgpt'],
              sha(R / row['source_relative_to_Chatgpt']) == sha(PACKAGE / row['frozen_relative_path']) == row['sha256'])
    check('parent registration pin', d['parent_registration_sha256'] == sha(B / 'RINGDOWN_5SIGMA_V1.json'))
    check('full frozen E2 own tree', {p.relative_to(B/'bis/e2_code').as_posix(): sha(p)
        for p in (B/'bis/e2_code').rglob('*.py')} == reg['own_code_tree_sha256'])
    jobs = read(R / d['jobs_relative_to_Chatgpt'])
    check('zero jobs pin', sha(R / d['jobs_relative_to_Chatgpt']) == d['jobs_sha256'])
    check('zero jobs metadata', jobs['schema_version'] == 'E2_PE_JOBS_V2' and jobs['jobs'] == {} and jobs['downloads'] == {} and jobs['parent_registration_sha256'] == d['parent_registration_sha256'])
    check('inactive candidate', d['registered_utc'] is None and d['witness_relative_to_Chatgpt'] is None)
    for key in ('new_PE_count','new_injection_count','new_download_count','new_science_wall_seconds','pipeline_repair_seconds'):
        check('zero allocation ' + key, type(d['allocation'][key]) is int and d['allocation'][key] == 0)
    check('unknown converged cost', d['cost_per_converged_IMR_posterior_seconds'] is None)
    check('five alternatives explicit', [x['id'] for x in d['alternatives']] == ['i','ii','iii','iv','v'])
    for a in d['alternatives']:
        check('alternative unpaid ' + a['id'], a['allocated_wall_seconds'] == 0 and a['estimated_wall_seconds_for_qualified_program'] is None and bool(a['reason']))
    w = d['wall_accounting']
    t = {k: datetime.fromisoformat(w[k]) for k in ('started_utc','measured_utc','hard_deadline_utc','finalization_stop_utc')}
    check('original envelope unchanged', w['started_utc'] == original['started_utc'] and w['hard_deadline_utc'] == original['hard_deadline_utc'])
    close('40 hour envelope', (t['hard_deadline_utc']-t['started_utc']).total_seconds(), 144000)
    close('elapsed clock', w['elapsed_seconds'], (t['measured_utc']-t['started_utc']).total_seconds())
    close('remaining clock', w['remaining_seconds'], (t['hard_deadline_utc']-t['measured_utc']).total_seconds())
    close('fixed reserve', (t['finalization_stop_utc']-t['measured_utc']).total_seconds(), 7200)
    check('reserve inside global deadline', t['finalization_stop_utc'] <= t['hard_deadline_utc'])
    close('released hours not spent', w['unused_science_seconds_released_not_spent'], w['remaining_seconds']-7200)
    for hours, seconds in [('elapsed_hours','elapsed_seconds'),('remaining_hours','remaining_seconds'),('unused_science_hours_released_not_spent','unused_science_seconds_released_not_spent')]:
        close(hours, w[hours], w[seconds]/3600)
    costs = d['measured_costs']
    for label, path in [('Kerr_V1','cache/E3_KERR220_CALIBRATION_V1/COST.json'),('Kerr_V2','cache/E3_KERR220_CALIBRATION_V2/COST.json'),('IMR_pilot_failed_controller','cache/E3_PSEOB_PILOT_V1/CONTROLLER.json')]:
        check('cost exact receipt ' + label, costs[label] == read(B / path))
    close('Kerr wall sum', costs['Kerr_V1_V2_controller_sum_seconds'], math.fsum(costs[k]['wall_seconds'] for k in ('Kerr_V1','Kerr_V2')))
    close('Kerr CPU sum', costs['Kerr_V1_V2_CPU_sum_seconds'], math.fsum(costs[k]['children_cpu_seconds'] for k in ('Kerr_V1','Kerr_V2')))
    check('Kerr inequivalence preserved', costs['Kerr_equivalent_reproduction_paid'] is False)
    diagnostic = read(B/'bis/e3_pilot_failure_diagnostic/DIAGNOSIS.json')
    # Locate the exact accounting object without depending on author's helper.
    def dictionaries(x):
        if isinstance(x, dict):
            yield x
            for value in x.values():
                yield from dictionaries(value)
        elif isinstance(x, list):
            for value in x:
                yield from dictionaries(value)
    check('diagnostic accounting transported exactly', costs['IMR_native_diagnostic'] in list(dictionaries(diagnostic)))
    fits = {f['population']: f for f in read(B/'bis/E0_SNR_INFORMATION_FIT.json')['fits']}
    for fit in d['information_model']['fits_preserved']:
        check('fit parameters retained ' + fit['population'], all(v == fits[fit['population']][k] for k,v in fit.items()))
    csv_path = B/'bis/e0_metadata/GWOSC_EVENTS.csv'
    csv_rows = list(csv.DictReader(csv_path.read_text(encoding='utf-8-sig').splitlines()))
    events = d['events']
    check('all fourteen unique registered candidates', len(events) == len({e['event'] for e in events}) == 14 and {e['event'] for e in events} == set(reg['test_candidates']))
    check('10 unheld 4 held', sum(e['data_quality_hold'] is True for e in events) == 4 and sum(e['data_quality_hold'] is False for e in events) == 10)
    outside = []
    for e in events:
        event = e['event']; r = reg['test_candidates'][event]
        for field, target in [('data_quality_hold','data_quality_hold'),('registered_eligible','eligible'),('published_deformation_at_registration','published_deformation_at_registration')]:
            check(event+' '+field, type(e[field]) is bool and e[field] == r[target])
        check(event+' no admission', e['admission'] is None and e['allocated_PE_jobs'] == 0 and e['information_per_hour'] is None)
        src = e['SNR_source']; row = csv_rows[src['line']-2]
        check(event+' source pin and exact line', sha(R/src['relative_to_Chatgpt']) == src['sha256'] and row['event'] == event and row['version_key'] == src['version_key'] and row['event_metadata_url'] == src['primary_url'])
        close(event+' SNR CSV', e['SNR_network'], float(row[src['field']]))
        close(event+' SNR E2', e['SNR_network'], r['SNR_network_GWOSC'])
        mr = e['metadata_review']; review_path = R / mr['relative_to_Chatgpt']
        check(event+' publication review pin', sha(review_path) == mr['sha256'] and mr['review_passed'] is True)
        read(review_path)  # Strict metadata only; no external lookup or posterior.
        check(event+' two fits', {q['fit_population'] for q in e['conditional_expected_weights']} == {'GWTC5_31','GWTC5_33'} and len(e['conditional_expected_weights']) == 2)
        for q in e['conditional_expected_weights']:
            label = event + '/' + q['fit_population']; f = fits[q['fit_population']]
            a,b = f['coefficients_log_intercept_slope']; s = f['residual_sigma_ln_ddof_Nminus2']
            x = math.log(e['SNR_network']); mu = a+b*x; cov = f['covariance']
            variance = math.fsum([cov[0][0],x*cov[0][1],x*cov[1][0],x*x*cov[1][1]])
            expected = math.exp(-2*mu+2*s*s)
            for field, value in [('ln_sigma_mean_mu',mu),('mu_variance_from_full_coefficient_covariance',variance),('sigma_conditional_median',math.exp(mu)),('inverse_squared_conditional_median_proxy',math.exp(-2*mu)),('expected_inverse_variance_lognormal_s_fixed',expected),('parameter_gaussian_integrated_information_s_fixed',expected*math.exp(2*variance)),('ratio_expectation_to_proxy',math.exp(2*s*s))]:
                close(label+' '+field, q[field], value)
            tc = f['coefficient_95_t_halfwidth'][0] / math.sqrt(cov[0][0])
            half = tc*math.sqrt(variance)
            intervals = {'sigma_residual_conditional_05_50_95': [math.exp(mu+NormalDist().inv_cdf(p)*s) for p in (.05,.5,.95)],
                'sigma_median_coefficient_only_95_t_interval': [math.exp(mu-half),math.exp(mu+half)],
                'expected_I_coefficient_only_95_t_interval_s_fixed': [math.exp(-2*(mu+half)+2*s*s),math.exp(-2*(mu-half)+2*s*s)]}
            for field, values in intervals.items():
                for j,value in enumerate(values):
                    close(label+'/'+field+'/'+str(j), q[field][j], value)
            out = not f['SNR_domain'][0] <= e['SNR_network'] <= f['SNR_domain'][1]
            check(label+' domain', q['outside_fit_SNR_domain'] is out)
            check(label+' no realized information', q['information_for_actual_new_PE'] is None)
            if out: outside.append(label)
    core = read(B/'bis/e0_core/E0_CORE.json')
    for summary in d['information_summaries']:
        pop = summary['fit_population']
        for group, selected in [('all14',events),('held4',[e for e in events if e['data_quality_hold']]),('unheld10',[e for e in events if not e['data_quality_hold']])]:
            weights = [next(q for q in e['conditional_expected_weights'] if q['fit_population'] == pop) for e in selected]
            check(pop+group+' N', summary['sums'][group]['N'] == len(weights))
            for field in ('inverse_squared_conditional_median_proxy','expected_inverse_variance_lognormal_s_fixed'):
                close(pop+group+field, summary['sums'][group]['sum_'+field], math.fsum(q[field] for q in weights))
        for row in summary['conditional_target_context']:
            source = core['combinations'][pop]['std_ddof1'][row['reading']]
            if row['I_target90_conditional'] is not None:
                close(pop+row['reading']+' target', row['I_target90_conditional'], source['I_tau_target90'])
                close(pop+row['reading']+' fraction', row['fraction_unheld10_of_conditional_target'], summary['sums']['unheld10']['sum_expected_inverse_variance_lognormal_s_fixed']/source['I_tau_target90'])
            check(pop+row['reading']+' no operational N', row['N_target_operational'] is None)
    check('ten readings', len(d['Ncalib']['readings']) == 10 and {r['reading'] for r in d['Ncalib']['readings']} == {r['reading'] for r in core['systematics']})
    for row in d['Ncalib']['readings']:
        source = next(r for r in core['systematics'] if r['reading'] == row['reading'])
        delta = row['delta_reference_GW250114']
        check(row['reading']+' delta input', delta == source['delta_reference_fresh_GW250114'])
        check(row['reading']+' no allocated injections', row['allocated_injections'] == 0 and row['N_target_operational'] is None)
        for sample in row['illustrative_sigma_INPUT_from_order']:
            n = (5*sample['sigma_inj']/abs(delta))**2
            close(row['reading']+' illustrative N '+str(sample['sigma_inj']), sample['N_per_cell_floor5_continuous'], n)
            check(row['reading']+' illustrative ceilings '+str(sample['sigma_inj']), sample['N_per_cell_floor5_ceiling'] == math.ceil(n) and sample['N_ten_cells_floor5_ceiling'] == 10*math.ceil(n) and sample['wall_cost_seconds'] is None)
    check('E3.3 unpaid', d['E3_3_status']['calibration_paid'] is False and d['E3_3_status']['gate_green'] is False and all(d['E3_3_status'][k] is None for k in ('sigma_c','sigma_sys_df','coverage')))
    check('candidate unchanged during review', sha(candidate_path) == initial_sha)
    failed = [c for c in CHECKS if not c['passed']]
    result = dict(status='APPROVED_DOCUMENTARY_ZERO_NEW_SCIENCE_ALLOCATION' if not failed else 'BUDGET_REVIEW_FINDINGS',
        approved=not failed, candidate_sha256=initial_sha, created_utc=datetime.now(timezone.utc).isoformat(),
        blocking_findings=failed, checks=CHECKS, check_count=len(CHECKS),
        review_source_sha256=sha(__file__), manifest_sha256=sha(PACKAGE/'MANIFEST.json'),
        finalization_stop_utc=w['finalization_stop_utc'], global_stop_utc=w['hard_deadline_utc'],
        candidate_events=14, held_events=4, unheld_events=10, weight_rows=28,
        extrapolation_flags=outside, expected_information=d['information_summaries'],
        activation_approval=False, activation_review='Separate E3_WALL_BUDGET_ACTIVATION_REVIEW.json; this boolean approves the candidate only.',
        scope='Independent metadata, hashes and lightweight scalar arithmetic only. No helper rerun, OLS/bootstrap, science, waveform, PE, strain or candidate posterior reads. Existing whole-package metadata receipts transported and checked; publication review hashes are not a new universal publication search.',
        limitations=['Zero allocation is a decision; unknown qualified science cost remains null.',
                    'Fixed preparation-time two-hour reserve is not restarted by approval.',
                    'Empty jobs cannot remove original E2 jobs; no runtime override or pilot relaunch authorized.',
                    'Weights forecast published-width information under fixed residual scatter, not calibrated likelihood/power or realized event gain.'])
    target = HERE/'E3_WALL_BUDGET_CANDIDATE_REVIEW.json'
    with target.open('xb') as f:
        f.write((json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode())
    print(json.dumps({'approved': not failed, 'checks': len(CHECKS), 'failed': failed, 'candidate_sha256': initial_sha, 'receipt_sha256': sha(target)}))


if __name__ == '__main__':
    main()
