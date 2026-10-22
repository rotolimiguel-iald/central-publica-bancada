"""Mutation controls for review B1/B2; mutate memory only."""
from pathlib import Path
import csv, copy, json, hashlib
from c1_evidence_guards import validate_inputs, validate_evidence
ROOT=Path(__file__).resolve().parents[1]
cat=json.loads((ROOT/'C4_CATALOG_220.json').read_bytes())
with (ROOT/'C7_INDEPENDENT/tables/event_reading_predictions.csv').open(encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f))
measured=json.loads((ROOT/'bis/C1_NUMERICAL_CONTROLS_v2.json').read_bytes())
core=json.loads((ROOT/'cache/casa/um_absoluto.json').read_bytes())['core']['clock_test_result_v369']
validate_inputs(rows,cat);validate_evidence(ROOT,measured,core)
tests=[]
def reject(name,fn):
    try:fn()
    except (ValueError,KeyError,TypeError) as exc:
        tests.append(dict(name=name,rejected=True,error=str(exc)))
    else:raise RuntimeError('Invalid evidence accepted: '+name)
r=copy.deepcopy(rows);r.insert(0,dict(r[0],delta_tau='12345'))
reject('conflicting_duplicate_csv',lambda:validate_inputs(r,cat))
r=copy.deepcopy(rows);r[-1]['delta_tau']='NaN'
reject('nan_last_csv_column',lambda:validate_inputs(r,cat))
reject('missing_csv_row',lambda:validate_inputs(rows[:-1],cat))
m=copy.deepcopy(measured);m['csv_checks'][0]['relative_errors']['delta_tau']=float('nan')
reject('nan_recorded_error',lambda:validate_evidence(ROOT,m,core))
m=copy.deepcopy(measured);m['dependencies'].pop('refeito/c1_evidence_guards.py')
reject('missing_dependency',lambda:validate_evidence(ROOT,m,core))
m=copy.deepcopy(measured);m['dependencies']['tgl_ringdown_prediction.py']='0'*64
reject('changed_dependency',lambda:validate_evidence(ROOT,m,core))
m=copy.deepcopy(measured);m['checked']=263
reject('wrong_coverage_count',lambda:validate_evidence(ROOT,m,core))
c=copy.deepcopy(core);c['P1']['verdict']='P1_FALSIFIED_IN_READING'
reject('changed_P1',lambda:validate_evidence(ROOT,measured,c))
c=copy.deepcopy(core);c['all_verified']=False
reject('unsealed_clock',lambda:validate_evidence(ROOT,measured,c))
m=copy.deepcopy(measured);m['P2_tau_star_bound_tP']*=2
reject('changed_bound',lambda:validate_evidence(ROOT,m,core))
out=ROOT/'bis/C1_GUARD_MUTATION_TESTS.json'
if out.exists():raise FileExistsError(out)
raw=(json.dumps(dict(status='PASS',positive_control=True,mutations=tests,
    code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n').encode()
tmp=out.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(raw)
if tmp.read_bytes()!=raw:raise RuntimeError('Write mismatch')
tmp.replace(out)
print('PASS',len(tests),'mutations rejected')
