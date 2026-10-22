"""Mock return-contract audit; no actual LAL fit or cosmological calculation."""
from pathlib import Path
import ast,copy,hashlib,json,sys,types
import numpy as np
O=Path(__file__).resolve().parent
code=O/'integration_snapshot/remnant_conversion.py'
cfg=json.loads((O/'snapshot/E2_DESIGN_DRAFT_002.json').read_text())['pe_jobs']['GW250114_PILOT']
target=O/'REMNANT_MOCKS.json'
if target.exists():raise FileExistsError(target)
pars=cfg['remnant_conversion_INPUT']['cosmology_parameters']
pinfile=O/'SYNTHETIC_COSMOLOGY_BYTES.txt';pinfile.write_text('MOCK ONLY; NOT PLANCK TABLE')
cfg['remnant_conversion_INPUT']['cosmology_source_path']=str(pinfile)
cfg['remnant_conversion_INPUT']['cosmology_source_sha256']=hashlib.sha256(pinfile.read_bytes()).hexdigest()
ns={'Path':Path,'hashlib':hashlib,'np':np}
tree=ast.parse(code.read_text())
fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='derive')
# Replace imports with explicit mocks, leaving every branch and arithmetic unchanged.
fun.body=[n for n in fun.body if not isinstance(n,(ast.Import,ast.ImportFrom))]
ns['lal']=types.SimpleNamespace(MSUN_SI=10.)
ns['ls']=types.SimpleNamespace(SEOBNRv4=4,SimIMREOBFinalMassSpin=lambda m1,m2,s1,s2,a:[0,.9,s1[2]])
ns['u']=types.SimpleNamespace(km=1.,s=1.,Mpc=1.,K=1.,eV=1.)
ns['Planck18']=types.SimpleNamespace(H0=types.SimpleNamespace(value=pars['H0_km_s_Mpc']),Om0=pars['Om0'],
    Tcmb0=types.SimpleNamespace(value=pars['Tcmb0_K']),Neff=pars['Neff'],m_nu=types.SimpleNamespace(value=np.array(pars['m_nu_eV'])),Ob0=pars['Ob0'])
ns['FlatLambdaCDM']=lambda **kwargs:types.SimpleNamespace(luminosity_distance='MOCK_DISTANCE_FUNCTION')
ns['z_at_value']=lambda f,d,**kwargs:d/10000.
exec(compile(ast.Module(body=[fun],type_ignores=[]),str(code),'exec',optimize=1),ns)
rows={'mass_1':[30.,40.],'mass_2':[10.,20.],'chi_1':[-.2,.3],'chi_2':[0.,.1],'luminosity_distance':[100.,200.]}
checks=[]
def good(name,value):
    if not value:raise ValueError(name)
    checks.append({'name':name,'passed':True})
def refuse(name,call):
    try:call()
    except ValueError:good(name,True)
    else:raise RuntimeError('Expected rejection '+name)
out,receipt=ns['derive'](rows,cfg,lambda:None)
good('mass_fraction_times_detector_sum_no_extra_redshift',np.allclose(out['final_mass_detector'],[36,54]))
good('negative_final_spin_retained',out['final_spin'].tolist()==[-.2,.3])
good('paired_order_and_no_thinning',out['redshift'].tolist()==[.01,.02] and receipt['N']==2)
bad=copy.deepcopy(cfg);bad['remnant_conversion_INPUT']['cosmology_parameters']['H0_km_s_Mpc']+=1
refuse('Planck_name_cannot_hide_changed_H0',lambda:ns['derive'](rows,bad,lambda:None))
badrows=copy.deepcopy(rows);badrows['mass_2']=[10.]
refuse('unpaired_rows',lambda:ns['derive'](badrows,cfg,lambda:None))
ns['ls'].SimIMREOBFinalMassSpin=lambda *a:[1,.9,.7]
refuse('nonzero_LAL_return_status',lambda:ns['derive'](rows,cfg,lambda:None))
ns['ls'].SimIMREOBFinalMassSpin=lambda *a:[0,1.1,.7]
refuse('mass_fraction_above_one',lambda:ns['derive'](rows,cfg,lambda:None))
report={'status':'MOCK_CONTRACT_ONLY_NOT_NUMERICAL_REMNANT_VALIDATION','python_optimize':sys.flags.optimize,
    'source_sha256':hashlib.sha256(code.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'checks':checks,'actual_LAL_calls':0,'actual_cosmological_inversions':0,
    'primary_return_contract_source':'https://lscsoft.docs.ligo.org/pesummary/latest/_modules/pesummary/gw/conversions/remnant.html',
    'primary_reading_scope':'SEOBNRv4 branch indices1/2; helper converts mass fraction times component-mass sum; webpage opened during independent review'}
with target.open('x') as f:json.dump(report,f,indent=2)
print(json.dumps({'checks':len(checks),'status':report['status']}))
