"""Independent deterministic receipt review; no producer imports, RNG, seed files or MC."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, platform, os
import scipy
from scipy.stats import binom, norm, t
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
CHAT = B.parent
snapshots = {}
checks = []

def read(path):
    path = path.resolve()
    raw = path.read_bytes()
    snapshots[str(path)] = raw
    return raw

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def sha(path):
    return digest(read(path))

def get(path):
    return json.loads(read(path))

def check(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})
    if not condition:
        print('FAILED:', label, flush=True)

def near(a, b, rel=1e-10, absolute=1e-16):
    return math.isclose(a, b, rel_tol=rel, abs_tol=absolute)

def date(value):
    return datetime.fromisoformat(value)

regpath = B/'RINGDOWN_5SIGMA_V1.json'
reg = get(regpath)
rh = digest(snapshots[str(regpath.resolve())])
campaign_path = B/'bis/RESULT_E2_NULL_CAMPAIGN.json'
campaign = get(campaign_path)
audit_path = B/'bis/E2_NULL_RECEIPTS_AUDIT_V1.json'
audit = get(audit_path)
manifest = get(B/'bis/B2_DELIVERY_MANIFEST.json')
delivery_path = CHAT/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_B2_registro_e_440.md'
delivery_raw = read(delivery_path)
# Only parse the null section; no E4 calculations or posterior inputs are used.
delivery_null = delivery_raw.decode('utf-8').split('## Nulos registrados', 1)[1].split('## Modo440', 1)[0]
check('B2 delivery bytes match manifest', digest(delivery_raw) == manifest['delivery_sha256'])
check('registration linked in all receipts', rh == campaign['registration_sha256'] == audit['registration_sha256'] == manifest['registration_sha256'])
check('campaign audit link', sha(campaign_path) == audit['campaign_sha256'])
for rel in ['RINGDOWN_5SIGMA_V1.json', 'bis/RESULT_E2_NULL_CAMPAIGN.json', 'bis/E2_NULL_RECEIPTS_AUDIT_V1.json']:
    raw = read(B/rel)
    check('B2 manifest '+rel, digest(raw) == manifest['files'][rel]['sha256'] and len(raw) == manifest['files'][rel]['bytes'])
for name in ['null_runner.py', 'synthetic_null.py', 'route_iv_null.py', 'null_campaign.py']:
    check('registered source '+name, sha(B/'bis/e2_code'/name) == reg['own_code_tree_sha256'][name])
for name in ['refeito/e0_mc_guarded_013bis.py', 'refeito/e0_route_iv_power_013bis_v2.py']:
    check('registered IV source '+name, sha(B/name) == reg['input_pins_relative_to_Chatgpt']['ORDEM_013_RINGDOWN/'+name])
check('audit script current pin', sha(B/'refeito/audit_e2_null_receipts_013bis.py') == audit['script_sha256'])
check('campaign code current pin', sha(B/'bis/e2_code/null_campaign.py') == campaign['code_sha256'])
check('campaign completion status', campaign['status'] == 'SYNTHETIC_NULLS_COMPLETED_NOT_PHYSICAL_5SIGMA' and campaign['failed'] is None)
check('audit limited status', audit['status'] == 'RECEIPTS_AND_BINOMIAL_ENDPOINTS_VERIFIED__SYNTHETIC_ONLY' and audit['physical_gate'] == 'INCONCLUSIVE_SYSTEMATICS' and audit['physical_5sigma_paid'] is False)
cells = reg['nulls']['cells']
completed = {v['cell']: v for v in campaign['completed']}
arows = {v['cell']: v for v in audit['cells']}
check('exact 25 cell coverage and no duplicates', len(cells) == len(campaign['completed']) == len(audit['cells']) == 25 and set(cells) == set(completed) == set(arows) == set(campaign['requested_cells']) and len(campaign['requested_cells']) == 25)
start, finish = date(campaign['started_utc']), date(campaign['finished_utc'])
check('registration precedes campaign; audit and delivery follow', date(reg['registered_utc']) < start < finish < date(audit['created_utc']) < date(manifest['created_utc']))
check('campaign clock duration', abs((finish-start).total_seconds()-campaign['wall_seconds']) < .01)
p5 = float(norm.sf(5))
check('registered one sided p5', near(reg['statistics']['one_sided_p5'], p5))
rows = []
previous = start
seed_ids = []
for name in campaign['requested_cells']:
    cell = cells[name]
    path = B/'bis'/('RESULT_E2_NULL_'+name+'.json')
    entry = get(path)
    result = entry['result']
    logpath = B/'bis'/('E2_NULL_'+name+'.log')
    log = get(logpath)
    cp = completed[name]
    row = arows[name]
    check(name+' byte links', sha(path) == cp['result_sha256'] == row['result_sha256'] == log['sha256'] and sha(logpath) == cp['log_sha256'])
    check(name+' identity and contract', entry['registration_sha256'] == rh and entry['cell_id'] == name == log['cell'] and entry['cell'] == cell and entry['null_runner_sha256'] == reg['own_code_tree_sha256']['null_runner.py'])
    check(name+' status', entry['status'] == log['status'] == 'SYNTHETIC_NULL_COMPLETED__NOT_PHYSICAL_CALIBRATION' and entry['physical_test_gate'] == 'INCONCLUSIVE_SYSTEMATICS')
    begin, end = date(entry['started_utc']), date(entry['finished_utc'])
    check(name+' timestamp order and wall', previous <= begin < end <= finish and abs((end-begin).total_seconds()-entry['wall_seconds']) < .01 and entry['wall_seconds'] == cp['wall_seconds'] == log['wall_seconds'])
    previous = end
    k, n = result['false_positives'], result['draws']
    check(name+' counts', type(k) is int and type(n) is int and n == cell['draws'] and 0 <= k <= n and result['empirical_p'] == k/n and result['confidence_level'] == .95 and result['seed'] == cell['seed'])
    # Independent inversion of binomial probabilities, not producer beta.ppf.
    root = lambda f: brentq(f, 0., 1., xtol=5e-324, rtol=1e-14)
    upper = root(lambda p: binom.cdf(k, n, p)-.05) if k < n else 1.
    low = root(lambda p: binom.sf(k-1, n, p)-.025) if k else 0.
    high = root(lambda p: binom.cdf(k, n, p)-.025) if k < n else 1.
    check(name+' CP endpoints independent roots', near(upper,result['one_sided_upper']) and near(low,result['central_interval'][0]) and near(high,result['central_interval'][1]))
    mapped = {'kind':cell['kind'], 'population':cell['population'], 'reading':cell.get('reading'), 'model':cell.get('model'), 'draws':n, 'false_positives':k, 'empirical_p':k/n, 'one_sided_upper95':result['one_sided_upper'], 'central95':result['central_interval'], 'mean':result.get('mean'), 'variance_ddof1':result.get('variance_ddof1'), 'components':result.get('components'), 'max_LRT':result.get('max_LRT'), 'wall_seconds':entry['wall_seconds'], 'cpu_seconds':entry['cpu_seconds']}
    check(name+' audit row fields', all(row[key] == val for key,val in mapped.items()))
    check(name+' descriptive normal inverse', near(row['normal_tail_equivalent_of_upper_bound_DESCRIPTIVE'], float(norm.isf(upper))))
    analytical = result.get('analytic_tail_control',{}).get('p')
    check(name+' audit analytical fields', row['analytic_p'] == analytical and row['analytic_inside_pointwise95'] == (None if analytical is None else low <= analytical <= high) and row['analytic_expected_false_positives'] == (None if analytical is None else n*analytical))
    independent = None
    err = None
    if cell['kind'] == 'matched_projection':
        a = result['components']['noise_variance_fraction']
        b = result['components']['nuisance_variance_fraction']
        check(name+' projection declaration', min(a,b) >= 0 and near(a+b,1,1e-7) and result['threshold_one_sided'] == 5 and result['model'] == cell['model'] and result['components']['N'] == cell['N_target_balanced_catalog'])
        if cell['model'] == 'gaussian':
            independent = float(norm.sf(5/math.sqrt(a+b)))
        else:
            # Different integration variable: integrate Gaussian nuisance H,
            # using measurement sqrt(3/5)*T_5, rather than chi-square mixture U.
            independent, err = quad(lambda h: norm.pdf(h)*t.sf((5-math.sqrt(b)*h)/math.sqrt(3*a/5),5), -12,12,epsabs=1e-14,epsrel=1e-11,limit=200)
        check(name+' analytical reference independent convolution', near(independent, analytical, rel=1e-8, absolute=1e-13))
        seed_ids.append(cell['seed'])
    else:
        check(name+' IV contract', result['threshold_LRT'] == reg['statistics']['LRT_IV_threshold_strict_greater'] == 25. and result['N'] == cell['N_target'] and result['population'] == cell['population'] and result['sigma_sys_INPUT'] == cell['sigma_sys_INPUT'] and result['chunk_size'] == cell['chunk'])
        check(name+' max versus count', (result['max_LRT'] > 25) == (k > 0))
        seed_ids.extend(range(cell['seed'],cell['seed']+math.ceil(n/cell['chunk'])))
    line = next((s for s in delivery_null.splitlines() if s.startswith('| '+name+' |')), None)
    values = [s.strip() for s in line.split('|')[1:-1]] if line else []
    check(name+' B2 rounded null table', bool(values) and int(values[1]) == n and int(values[2]) == k and near(float(values[3]),k/n,rel=1e-5) and near(float(values[4]),upper,rel=1e-5) and ((values[5]=='OPEN') if analytical is None else near(float(values[5]),analytical,rel=1e-5)))
    rows.append({'cell':name,'kind':cell['kind'],'draws':n,'k':k,'empirical_p':k/n,'upper95_independent':upper,'central95_independent':[low,high],'analytic_receipt':analytical,'analytic_independent':independent,'convolution_error_estimate':err,'analytic_to_p5':None if independent is None else independent/p5,'upper_to_p5':upper/p5,'analytic_inside_central95':None if analytical is None else low<=analytical<=high,'result_sha256':sha(path),'log_sha256':sha(logpath)})
check('finite RNG identifier range overlap only, no RNG execution',len(set(seed_ids)) == len(seed_ids))
check('total draws exact 1.609 billion',sum(r['draws'] for r in rows) == audit['total_draws'] == 1609000000)
check('audit duration and CPU aggregation',audit['campaign_wall_seconds'] == campaign['wall_seconds'] and near(sum(r['cpu_seconds'] for r in arows.values()),audit['sum_cell_cpu_seconds']))
check('zero-count closed-form UL',all(near(r['upper95_independent'],-math.expm1(math.log(.05)/r['draws'])) for r in rows if r['k']==0))
check('unchanged byte snapshots',all(Path(p).read_bytes() == raw for p,raw in snapshots.items()))
evidence = {'status':'PASS_CONDITIONAL_RECEIPT_REVIEW' if all(c['passed'] for c in checks) else 'FAIL_PRESERVE_AND_ADDENDUM', 'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'No RNG, MC, producer imports, PE, real blind seed/offset, or producer writes. Independent quadrature and binomial inversion only.','python':platform.python_version(),'scipy':scipy.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'rows':rows,'p5':p5,'pure_unit_variance_t5_tail_at5':float(t.sf(5*math.sqrt(5/3),5)),'zero_count_n_required_UL95_le_p5':math.ceil(math.log(.05)/math.log1p(-p5)),'pins':[{'path':p,'bytes':len(raw),'sha256':digest(raw)} for p,raw in snapshots.items()]}
raw = (json.dumps(evidence,indent=2,allow_nan=False)+'\n').encode()
target = HERE/'E2_NULL_CAMPAIGN_REVIEW_EVIDENCE.json'
pending = target.with_suffix('.json.pending')
with pending.open('xb') as f:
    f.write(raw)
assert pending.read_bytes() == raw
os.link(pending,target)
pending.unlink()
print(json.dumps({'status':evidence['status'],'checks':len(checks),'failed':[c['check'] for c in checks if not c['passed']],'evidence_sha256':digest(raw),'rows':rows},indent=2))
