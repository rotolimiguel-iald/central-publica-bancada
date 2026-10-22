"""Structural tests only: no scientific solver or observed data."""
import ast,copy,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
p=HERE/'background_controls.py'
compile(p.read_text(encoding='utf-8'),str(p),'exec')
spec=importlib.util.spec_from_file_location('prepared_background',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
protocol=m.read('PROTOCOL.json'); checks=[]
checks.append({'name':'valid_protocol','passed':m.validate(protocol)['solver_calls']==0})
for name,change in [
 ('prior_density_changed',lambda x:x['prior'].update(density_exact='1')),
 ('outside_prior',lambda x:x['points'][0].update(theta=[95,.0225,.13])),
 ('nonfinite_point',lambda x:x['points'][0].update(theta=[float('nan'),.0225,.13])),
 ('expanded_run_budget',lambda x:x['resources'].update(max_solver_calls=11)),
 ('H5_changes_CMB',lambda x:x['h5_candidate'].update(CMB='replace rstar by rd')),
 ('BBN_coverage_missing',lambda x:x['background'].update(nnu=20))]:
 x=copy.deepcopy(protocol);change(x)
 try:m.validate(x)
 except ValueError:checks.append({'name':name,'passed':True})
 else:checks.append({'name':name,'passed':False})
require_names=['camb','numpy','scipy']
checks.append({'name':'no_scientific_library_imported','passed':not any(n in sys.modules for n in require_names)})
checks.append({'name':'source_ast_compiles','passed':True})
result={'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','checks':checks,'check_count':len(checks),'science_runs':0,'camb_imported':False,'observed_inputs':False,'engine_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'protocol_sha256':hashlib.sha256((HERE/'PROTOCOL.json').read_bytes()).hexdigest(),'not_validated':'CAMB execution, numerical accuracy/cost, full prior coverage, likelihood and evidence'}
m.write_new(HERE/'VALIDACAO_PREPARACAO.json',result)
print(json.dumps(result,ensure_ascii=False))
assert result['status']=='PASS'