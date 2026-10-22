"""Only metadata/AST checks of changes made during the independent review."""
import ast, hashlib, json, math, sys
from pathlib import Path
from datetime import datetime,timezone,timedelta
O=Path(__file__).resolve().parent
S=O/'closing_snapshot'
rows=[]
def check(name,condition):
    if not condition:raise ValueError(name)
    rows.append({'name':name,'passed':True})
def extract(file,names,ns):
    nodes=[n for n in ast.parse((S/file).read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
    check(file+'_functions_found',len(nodes)==len(names))
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(S/file),'exec',optimize=1),ns)
    return ns
def reject(name,call):
    try:call()
    except (ValueError,KeyError):check(name,True)
    else:raise RuntimeError('Expected refusal '+name)
evidence=O/'MOCK_REVIEW_EVIDENCE.txt';evidence.write_text('SYNTHETIC METADATA RECEIPT ONLY')
digest=hashlib.sha256(evidence.read_bytes()).hexdigest()
now=datetime.now(timezone.utc)
ns={'contained':lambda p:Path(p),'sha':lambda p:hashlib.sha256(p.read_bytes()).hexdigest(),
    'utc':lambda t:datetime.fromisoformat(t),'datetime':datetime,'timezone':timezone}
extract('registration_guard.py',['authorize_event','validate_job_reviews'],ns)
reg={'registered_utc':(now-timedelta(minutes=2)).isoformat(),'calibration_event_ids':[],
     'test_candidates':{'FAKE':{'eligible':True,'published_deformation_at_registration':False,
                              'publication_census_scope':'MOCK CORPUS','data_quality_hold':False}}}
job={'mode':'blind_test','event':'FAKE','publication_metadata_review':{'relative_to_Chatgpt':str(evidence),
    'sha256':digest,'review_passed':True,'scope':'MOCK CORPUS','reviewed_utc':(now-timedelta(minutes=1)).isoformat()}}
ns['validate_job_reviews'](reg,job);check('new_metadata_gate_positive',True)
job['publication_metadata_review']['reviewed_utc']=(now+timedelta(minutes=2)).isoformat()
reject('future_publication_review',lambda:ns['validate_job_reviews'](reg,job))
job['publication_metadata_review']['reviewed_utc']=(now-timedelta(minutes=1)).isoformat()
reg['test_candidates']['FAKE']['data_quality_hold']=True
reject('hold_without_resolution',lambda:ns['validate_job_reviews'](reg,job))
job['data_quality_resolution']={'relative_to_Chatgpt':str(evidence),'sha256':digest,'review_passed':True,
                               'method':'MOCK METHOD','reviewed_utc':(now-timedelta(minutes=1)).isoformat()}
ns['validate_job_reviews'](reg,job);check('resolved_hold_positive',True)
job['data_quality_resolution']['sha256']='f'*64
reject('changed_quality_evidence',lambda:ns['validate_job_reviews'](reg,job))
# Paired remnant integration is inspected without running the PE main.
text=(S/'pe_runner.py').read_text()
check('remnant_called_after_convergence',text.index('derived,remnant_receipt=derive')>text.index("if not state['accepted_for_analysis']"))
check('derived_columns_finite_and_paired',"shape!=(len(result.posterior),)" in text and "not np.isfinite(v).all()" in text)
check('derived_columns_in_blind_payload','for k in PHYSICAL+DERIVED_PHYSICAL' in text)
check('source_has_detector_delay_reserve','detector_delay_bound_s=0.022' in (S/'pseob_source.py').read_text())
report={'status':'PASS_FINITE_METADATA_AND_STATIC_INTEGRATION','python_optimize':sys.flags.optimize,'checks':rows,
        'scientific_execution':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (O/'CLOSING_DELTA_CHECKS.json').open('x') as f:json.dump(report,f,indent=2)
print(json.dumps({'checks':len(rows),'status':report['status']}))
