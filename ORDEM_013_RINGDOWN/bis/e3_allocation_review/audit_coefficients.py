"""Independent finite rational-arithmetic check of published planning metadata."""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
LIMIT=25_000_000


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def publish(name,value):
    raw=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    if len(raw)>LIMIT:raise ValueError('Size cap')
    path=HERE/name;temp=path.with_name(path.name+'.pending')
    with temp.open('xb') as f:f.write(raw)
    if temp.stat().st_size!=len(raw):raise ValueError('Short write')
    os.link(temp,path);temp.unlink()


def main():
    paths=dict(coefficients=BASE/'bis/E3_CALIBRATION_BUDGET_COEFFICIENTS_V1.json',
        producer_code=BASE/'refeito/calibration_budget_coefficients_013bis.py',
        E0=BASE/'PORTAO_DA_AMPLIACAO_V1.json',
        order=BASE.parent/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md')
    pins={k:dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for k,p in paths.items()}
    if pins['coefficients']['sha256']!='f984ebe58ae2b788b97762e1ba9b64917d58c74c09f93742ec80bca55a302649':
        raise ValueError('Operator coefficient pin differs')
    data=json.loads(paths['coefficients'].read_bytes());e0=json.loads(paths['E0'].read_bytes())
    for field,alias in [('code_sha256','producer_code'),('gate_sha256','E0'),('order_sha256','order')]:
        if data[field]!=pins[alias]['sha256']:raise ValueError('Published source pin differs: '+field)
    snap=HERE/'coefficient_snapshot_001';snap.mkdir(exist_ok=False)
    for alias in ('coefficients','producer_code'):
        (snap/paths[alias].name).write_bytes(paths[alias].read_bytes())
    floors={r['reading']:r for r in e0['systematic_conditions']}
    expected={(reading,sigma,field) for reading in floors for sigma in (.0497,.058,.24)
              for field in ('floor5_INPUT','floor15_INPUT')}
    seen=set();checks=[]
    tolerance=8*math.ulp(1.0)
    for i,row in enumerate(data['rows']):
        key=(row['reading'],row['sigma_injection_INPUT'],row['floor_source'])
        c=dict(index=i,reading=key[0],sigma_INPUT=key[1],floor_source=key[2])
        c['unique_expected_key']=key in expected and key not in seen;seen.add(key)
        floor=floors[key[0]][key[2]];n=row['N_per_cell_continuous_conditional'];ceil=row['N_per_cell_ceiling_conditional']
        c['floor_exactly_copied']=row['floor']==floor
        c['scope_null_cost_no_allocation']=(row['cost_per_converged_injection_hours'] is None and
             row['allocated_hours'] is None and row['actual_injections_completed']==0 and row['cells_INPUT']==10)
        if floor is None or floor<=0:
            c['null_target_preserved']=n is None and ceil is None and row['N_ten_cells_conditional'] is None
            c['status_correct']=row['status']=='NO_FINITE_TARGET_FROM_ZERO_OR_OPEN_EFFECT'
        else:
            # Exact rational arithmetic on published binary64 inputs, no producer import.
            ratio=Fraction.from_float(key[1])/Fraction.from_float(floor)
            exact=ratio*ratio
            residual=abs(Fraction.from_float(n)-exact)/exact
            c['relative_error_against_exact_binary_inputs']=float(residual)
            c['continuous_within_eight_ulp_relative']=residual<=Fraction.from_float(tolerance)
            binary_value=Fraction.from_float(n)
            expected_ceil=-(-binary_value.numerator//binary_value.denominator)
            c['ceiling_of_published_binary64_correct']=type(ceil) is int and ceil==expected_ceil
            c['ten_cells_exact_integer_product']=row['N_ten_cells_conditional']==10*ceil
            c['status_correct']=row['status']=='DERIVED_CONDITIONAL_PLANNING'
            c['above_binary64_exact_integer_range']=n>2**53
            exact_input_ceil=-(-exact.numerator//exact.denominator)
            c['exact_input_rational_ceiling_matches']=ceil==exact_input_ceil
            c['ceiling_precision_scope']='ASTRONOMICAL_SCALE_NOT_EXACT_DESIGN' if n>2**53 else 'FINITE_RESOLVED_INTEGER_CHECK'
            if n<=2**53:c['resolved_ceiling_correct']=ceil==exact_input_ceil
        required=[k for k,v in c.items() if isinstance(v,bool) and k not in
                  ('above_binary64_exact_integer_range','exact_input_rational_ceiling_matches')]
        c['passed']=all(c[k] for k in required);checks.append(c)
    coverage=seen==expected and len(checks)==len(expected)
    for alias,p in paths.items():
        if sha(p)!=pins[alias]['sha256']:raise ValueError('Source changed during coefficient review')
    result=dict(status='FINITE_CONDITIONAL_ARITHMETIC_REVIEW',created_utc=datetime.now(timezone.utc).isoformat(),
        source_pins=pins,review_script_sha256=sha(Path(__file__)),rows=len(checks),coverage_complete=coverage,
        passed=sum(c['passed'] for c in checks),failed=[c['index'] for c in checks if not c['passed']],
        tolerance_relative=tolerance,method='Exact Fraction ratio-squared on published binary64 inputs, separate ceil and integer x10 checks; producer not imported/executed',
        maximum_relative_error=max(c.get('relative_error_against_exact_binary_inputs',0) for c in checks),
        astronomical_rows=sum(c.get('above_binary64_exact_integer_range',False) for c in checks),
        rows_with_null_target=sum(c.get('null_target_preserved',False) for c in checks),
        illustrative_R_B_primary=[r for r in data['rows'] if r['reading']=='R-B' and r['floor_source']=='floor5_INPUT'],
        scope='INPUT sigmas .0497/.058/.24 and common-sigma ten-cell scenario; no measured injection accuracy, cost, walltime or actual allocation; secondary floor15 does not replace floor5',
        scientific_campaign_executed=False,originals_changed=False,checks=checks)
    publish('COEFFICIENT_REVIEW_001.json',result)
    print(json.dumps({k:result[k] for k in ('rows','coverage_complete','passed','failed','maximum_relative_error','astronomical_rows','rows_with_null_target')}))


if __name__=='__main__':main()
