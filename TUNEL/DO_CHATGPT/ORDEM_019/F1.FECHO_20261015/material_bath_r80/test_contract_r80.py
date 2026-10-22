"""Deterministic synthetic algebra checks; no GKLS trajectory or observed data."""
import ast, copy, datetime, hashlib, json, math
from pathlib import Path
from material_contract_r80 import evaluate, ContractError
ROOT = Path(__file__).resolve().parent

def main():
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    plan=json.loads((ROOT/'PREREG_TESTS_R80.json').read_text(encoding='utf-8'))
    for p in plan['pins']:
        assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
    alpha_source=Path(plan['alpha_source'])
    constants={}
    for n in ast.parse(alpha_source.read_text(encoding='utf-8')).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('ALPHA_FINE_CODATA_2018','_SEALED_ALPHA_CODATA_2018'):
            constants[n.targets[0].id]=ast.literal_eval(n.value)
    assert constants['ALPHA_FINE_CODATA_2018']==constants['_SEALED_ALPHA_CODATA_2018']
    alpha=constants['ALPHA_FINE_CODATA_2018']; lam=alpha*math.sqrt(math.e)
    base={'schema':'iald-material-reduced/v1','units':'angular_frequency_s^-1;C_s^-1','origin_kind':'synthetic','source_refs':['PREREG_TESTS_R80.json: invented fixtures; not device data'],
          'alpha_fine':alpha,'gamma_lambda':1.0,'g':[[1,0],[1,0]],'pump':[[2,0],[2,0]],'detunings':[3,3],
          'C11':lam,'C22':lam,'C12':[lam,0],'delta_reduced':0,'window_s':1,
          'tolerances':{'pump_dark':1e-12,'bright_mixing':1e-12,'bath_relative':1e-12,'phase_defect':1e-12}}
    rows=[]
    def case(name,changes,expected):
        d=copy.deepcopy(base);d.update(changes)
        try:r=evaluate(d);status=r['status']
        except ContractError as e:r={'error':str(e)};status='REFUSED'
        rows.append({'name':name,'expected':expected,'actual':status,'pass':status==expected,'result':r})
    case('aligned_common_resonant',{},'MODEL_MATCH_WITHIN_INPUT_TOLERANCES')
    case('dark_pump',{'pump':[[2,0],[-2,0]]},'MODEL_MISMATCH')
    case('inhomogeneous_detuning',{'detunings':[3,4]},'MODEL_MISMATCH')
    case('independent_baths',{'C12':[0,0]},'MODEL_MISMATCH')
    case('rank_one_wrong_phase',{'C12':[-lam,0]},'MODEL_MISMATCH')
    case('full_phase_cycle',{'delta_reduced':2*math.pi},'MODEL_MISMATCH')
    case('nonpositive_C',{'C12':[2*lam,0]},'REFUSED')
    case('zero_bath',{'gamma_lambda':0},'REFUSED')
    case('zero_bright',{'g':[[0,0],[0,0]]},'REFUSED')
    case('missing_field',{'C12':None},'REFUSED')
    for field in ['alpha_fine','gamma_lambda','C11','C22','delta_reduced','window_s']:
        for name,v in [('nan',float('nan')),('inf',float('inf')),('bool',True)]:
            case(field+'_'+name,{field:v},'REFUSED')
    d=copy.deepcopy(base);del d['C12']
    try:evaluate(d);ok=False
    except ContractError:ok=True
    rows.append({'name':'absent_C12','pass':ok})
    assert len(rows)==plan['expected_checks']
    result={'status':'PASS' if all(r['pass'] for r in rows) else 'FAIL','checks':rows,'count':len(rows),
            'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'physical_measurements':0,'trajectories':0,'scope':'Synthetic algebra and fail-closed schema tests only',
            'beta_runtime':alpha*math.sqrt(math.e),'prereg_sha256':hashlib.sha256((ROOT/'PREREG_TESTS_R80.json').read_bytes()).hexdigest()}
    with (ROOT/'RESULT_TESTS_R80.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(result['status'],result['count'])
    if result['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
