"""Independent synthetic adversarial review; never imports or executes um.py."""
from pathlib import Path
import ast, copy, hashlib, json, math, os, sys, time
from datetime import datetime, timezone
import numpy as np
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent
UNIT=HERE.parent
ROOT=UNIT.parents[4]
INTEGRATOR=ROOT/'work/rede_quantica_20261013/integrate_time_v394.py'
SOURCES=[UNIT/'runtime/time_runtime_v394.py', UNIT/'physical_contract/physical_parameters.py', INTEGRATOR]
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
pins=[pin(p) for p in SOURCES]
ns={}
for p in SOURCES[:2]:exec(compile(p.read_bytes(),str(p),'exec'),ns)
tree=ast.parse(INTEGRATOR.read_text(encoding='utf-8'))
article=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ARTICLE' for t in n.targets))
article_ns={'_V394_INSCRIPTIONS':{'test':{'text':r'a_b {c} % $ & # ~ ^ \end{document}'}}}
exec(compile(article,'ARTICLE extracted from integrator','exec'),article_ns)

def audit(event,args):
    if event in {'subprocess.Popen','os.system','socket.connect','socket.bind'}:
        raise RuntimeError('review forbids process/network action: '+event)
    if event=='open':
        path,mode,flags=args
        writing=isinstance(mode,str) and any(ch in mode for ch in 'wax+')
        writing=writing or isinstance(flags,int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and isinstance(path,(str,bytes)):
            p=Path(os.fsdecode(path)).resolve()
            if not p.is_relative_to(HERE):raise RuntimeError('review write outside new folder: '+str(p))
sys.addaudithook(audit)

rows=[]
def case(name,fn,expected='return'):
    try:
        value=fn()
        if isinstance(value,np.generic):value=value.item()
        row={'name':name,'outcome':'return','value':value,'expected':expected}
    except Exception as exc:
        row={'name':name,'outcome':'exception','type':type(exc).__name__,'error':str(exc),'expected':expected}
    rows.append(row);return row

started=datetime.now(timezone.utc).isoformat();t0=time.perf_counter()
alpha=7.2973525693e-3;hb=6.62607015e-34/(2*math.pi)
synthetic=ns['v394_time_frequency_checks'](ns['v394_physical_parameters'],alpha,hb)
g=ns['_v394_geometry']()
for f,args in [('_v394_clock_phase',(1e308,1e308)),('_v394_clock_phase',(1.,5e-324)),
               ('_v394_clock_phase',(0.,1.)),('_v394_clock_modulus',(.1j,.100000000000001j,.1))]:
    case(f+repr(args),lambda f=f,args=args:ns[f](*args), 'finite_reliable_time_or_visible_refusal')
for name,fn in [
    ('nonfinite_matrix',lambda:ns['_v394_read']([[math.nan,0],[0,1]])),
    ('indefinite_density',lambda:ns['_v394_rule']([[2,0],[0,-1]],g['I']/2)),
    ('negative_energy',lambda:ns['v394_physical_parameters'](1,.9,1,alpha)),
    ('boolean_energy',lambda:ns['v394_physical_parameters'](True,2,1,alpha)),
    ('overflow_energy',lambda:ns['v394_physical_parameters'](1e308,1e308,1,alpha)),
    ('underflow_rate',lambda:ns['v394_physical_parameters'](5e-324,1,1,alpha)),
    ('contractive_echo_boundary',lambda:ns['v394_physical_parameters'](1,1,1,.5/math.sqrt(math.e))),
    ('kms_underflow_faithfulness',lambda:ns['v394_kms_clock'](ns['v394_physical_parameters'](1,1,1,alpha),.001)),
]:case(name,fn,'exception')

rootlaw=[]
for ratio in (1.,1.0000000001,2.,100.,1e10):
    p=ns['v394_physical_parameters'](hb,ratio*hb,hb,alpha)
    direct=(p['beta']/(2*hb))*(math.sqrt(p['energies_J'][1])-math.sqrt(p['energies_J'][0]))**2
    quadratic=p['beta']*p['tau_eff_s']*(2*p['Omega_rad_s'])**2/2
    rootlaw.append({'Eref_over_V0':ratio,'gamma':p['gamma_s_inv'],'root_direct':direct,
        'direct_relative_error':abs(direct-p['gamma_s_inv'])/p['gamma_s_inv'],
        'quadratic_relative_error':abs(quadratic-p['gamma_s_inv'])/p['gamma_s_inv']})

# Test ARTICLE after executing the exact extracted Python string, not its spelling.
tex=article_ns['_v394_article_tex']('BEGIN\n\\end{document}',{'tempo_frequencia_v394':{'verdict':'X_Y'}},'pt')
article_results={'real_section': '\n\\section*{' in tex, 'literal_newline_escape': r'\n' in tex,
                 'escaped_verdict':'X\\_Y' in tex,'document_end_count':tex.count(r'\end{document}'),
                 'escaped_inscription':r'\textbackslash{}end\{document\}' in tex,
                 'output':tex}

# Structural mocks below test admission only. They are not formal evidence.
actual_checks=ns['v394_time_frequency_checks']
ns['v394_time_frequency_checks']=lambda *args:{'passed':True,'scope':'mock admission-only test'}
body='theorem mock : True := True.intro\n'
ns['_V394_FORMAL_CONTRACT']={'theorems':['Mock.theorem'],'source_sha256':{'Mock.lean':hashlib.sha256(body.encode()).hexdigest()},'expected_ladder':100}
ns['_V394_INSCRIPTIONS']={'mock':{'text':'authorized fixture','sha256':hashlib.sha256(b'authorized fixture').hexdigest()}}
ns['_EMBEDDED_KERNEL_FILES']={'Mock.lean':body}
ns['SEALED_CODATA_ALPHA']=alpha;ns['HBAR_EXACT']=hb
base={'kernel_formalization':{'all_verified':True,'axiom_report':{'Mock.theorem':['propext']}}}
for label,core in [
    ('formal_valid_mock',copy.deepcopy(base)),
    ('formal_missing',{}),
    ('formal_axiom_missing',{'kernel_formalization':{'all_verified':True,'axiom_report':{}}}),
    ('formal_custom_axiom',{'kernel_formalization':{'all_verified':True,'axiom_report':{'Mock.theorem':['sorryAx']}}}),
    ('formal_malformed_axiom',{'kernel_formalization':{'all_verified':True,'axiom_report':{'Mock.theorem':[['propext']]}}}),
    ('formal_ladder_missing',copy.deepcopy(base)),
    ('formal_ladder_wrong',dict(copy.deepcopy(base),external_ladder={'n_closed':1,'n_expected':1})),
]:
    case(label,lambda core=core:ns['tempo_frequencia_v394'](core),
         'refused' if label!='formal_valid_mock' else 'accepted_mock')
ns['_EMBEDDED_KERNEL_FILES']['Mock.lean']=body+'-- mutation\n'
case('formal_source_mutation',lambda:ns['tempo_frequencia_v394'](copy.deepcopy(base)),'refused')
ns['_EMBEDDED_KERNEL_FILES']['Mock.lean']=body
ns['_V394_INSCRIPTIONS']['mock']['text']+='changed'
case('formal_inscription_mutation',lambda:ns['tempo_frequencia_v394'](copy.deepcopy(base)),'refused')
ns['v394_time_frequency_checks']=actual_checks

result={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
    'seconds':time.perf_counter()-t0,'reviewer':'atrator_lean independent of runtime builder',
    'sources':pins,'source_unchanged':[pin(p)==old for p,old in zip(SOURCES,pins)],
    'full_synthetic':synthetic,'adversarial':rows,'rootlaw':rootlaw,'article':article_results,
    'scope':'Only explicit synthetic model/functions and mocked admission; no production, canonical um, observed data, network or subprocess.'}
with (HERE/'RESULTADO_RUNTIME_REVIEW_R1.json').open('x',encoding='utf-8') as f:
    json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False,default=str)
print(json.dumps({'path':str(HERE/'RESULTADO_RUNTIME_REVIEW_R1.json'),'runtime_passed':synthetic['passed'],
    'check_count':synthetic['check_count'],'failed':synthetic['failed'],'adversarial':rows,
    'article':{k:v for k,v in article_results.items() if k!='output'},'rootlaw':rootlaw},ensure_ascii=False,default=str))
