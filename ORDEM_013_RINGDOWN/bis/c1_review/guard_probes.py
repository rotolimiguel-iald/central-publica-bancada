"""Lightweight in-memory adversarial probes of the audit's validation logic.

No production function is imported or executed. Synthetic variants never leave
this directory and never replace the audited inputs.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import math

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def predicate(errors):
    # The actual production predicate at measure_c1_013bis.py:91.
    return max(errors.values()) < 1e-12


def main():
    out=HERE/'guard_probe_results.json'
    if out.exists():
        raise FileExistsError(out)
    with (ROOT/'C7_INDEPENDENT/tables/event_reading_predictions.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    # Production dict comprehension silently loses duplicate keys.
    duplicated=rows+[dict(rows[0])]
    saved={(r['event'],r['reading']):r for r in duplicated}
    # A bad duplicate before the good row is silently replaced by the good row.
    bad=dict(rows[0]);bad['delta_tau']='12345'
    saved_conflict={(r['event'],r['reading']):r for r in [bad]+rows}
    current={(r['event'],r['reading']):r for r in rows}
    finite_errors={'gamma_per_s':0.0,'gamma_over_omega':0.0,'delta_tau':0.0}
    nan_errors=dict(finite_errors);nan_errors['delta_tau']=float('nan')
    num=json.loads((ROOT/'bis/C1_NUMERICAL_CONTROLS.json').read_bytes())
    v2=json.loads((ROOT/'C1_LEITURAS_v2.json').read_bytes())
    paths=['refeito/measure_c1_013bis.py','refeito/record_c1_013bis.py',
           'C1_LEITURAS_v2.json','complete_c1_contract.py',
           'C7_INDEPENDENT/tables/event_reading_predictions.csv']
    source_checks=[]
    for name,item in v2['source_references'].items():
        path=ROOT/item['path']; lines=path.read_text(encoding='utf-8-sig').splitlines()
        source_checks.append({'reference':name,'hash_matches':sha(path)==item['sha256'],
            'matching_text_at_declared_line':any(item['matching_text'] in lines[n-1] for n in item['lines'])})
    results={
        'status':'CURRENT_DATA_PASS__VALIDATOR_HAS_FAIL_OPEN_CASES',
        'utc':datetime.now(timezone.utc).isoformat(),
        'scope':'In-memory reproduction of validation expressions only; no audited script executed.',
        'inputs':{p:sha(ROOT/p) for p in paths},
        'script_sha256':sha(Path(__file__)),
        'current_csv_rows':len(rows),
        'all_current_target_values_finite':all(math.isfinite(float(r[k])) for r in rows for k in ('Gamma_per_second','Gamma_over_omega','delta_tau')),
        'duplicate_probe':{'raw_rows':len(duplicated),'dictionary_rows':len(saved),'dictionary_equals_current':saved==current},
        'conflicting_duplicate_probe':{'raw_rows':len(rows)+1,'bad_delta_tau':'12345','dictionary_equals_current':saved_conflict==current},
        'nan_delta_probe':{'predicate_accepts_nan_delta_tau':predicate(nan_errors),
                           'explanation':'max([0.0,0.0,nan]) == 0.0 in this field order; validate every finite input and error first.'},
        'coverage_guard_static':'No assertion of unique/raw row count, equality of catalog/CSV key sets, or expected 99+33 counts before PASS.',
        'recorder_guard_static':'Recorder emits fixed 264/264 and threshold claims without validating measured.checked, csv_checks, status or dependencies.',
        'generator_provenance':{'v2_generator_field':v2['generator_sha256'],
             'matches_v1_generator':v2['generator_sha256']==sha(ROOT/'complete_c1_contract.py'),
             'matches_v2_recorder':v2['generator_sha256']==sha(ROOT/'refeito/record_c1_013bis.py')},
        'source_checks':source_checks,
        'current_measured_count':num['checked'],
        'current_recorded_max_error':max(max(x['relative_errors'].values()) for x in num['csv_checks']),
        'limits':'Synthetic failure cases invalidate general fail-closed claims, not the independently verified current numerical table.'
    }
    raw=(json.dumps(results,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    tmp=out.with_suffix('.json.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw
    if out.exists():raise FileExistsError(out)
    tmp.rename(out)
    print(json.dumps(results,ensure_ascii=False,indent=2))
    print('SHA256',sha(out))


if __name__=='__main__':main()
