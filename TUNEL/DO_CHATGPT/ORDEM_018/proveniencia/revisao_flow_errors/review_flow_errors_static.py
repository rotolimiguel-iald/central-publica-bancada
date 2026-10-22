"""Static integrity/order review. Does not execute/import the qualification or upstream."""
from pathlib import Path
import ast,datetime,hashlib,json,math,sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from audit_provenance import metadata,atomic
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
C=ROOT/'covariance_support'
checks=[];sources=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)})
    if not value:raise AssertionError(name)
def src(p):
    m,b=metadata(p);sources.append(m);return m,b
pm,pb=src(C/'FLOW_ERROR_PROTOCOL.json')
protocol=json.loads(pb)
rm,rb=src(C/'FLOW_ERROR_RESULT.json');res=json.loads(rb)
check('result_protocol_sha256',res['protocol_sha256']==pm['sha256'])
map454=json.loads((OUT/'MAPA_PRE_REGISTRO_454.json').read_bytes())
pin=map454[0]['artefatos'][0]
check('map454_protocol_pin',pin['bytes']==pm['bytes'] and pin['sha256']==pm['sha256'])
for x in protocol['inputs']:
    m,b=src(Path(x['path']))
    check('input_pin:'+Path(x['path']).name,m['sha256']==x['sha256'] and m['bytes']==x['bytes'])
meta=json.loads(Path(protocol['metadata_path']).read_bytes())
sn=meta['SN_flow_error_inputs'];sbf=meta['SBF_flow_error_inputs']
check('SN277_rows',len(sn)==protocol['SN_rows']==res['SN']['rows']==277)
check('SBF61_rows',len(sbf)==protocol['SBF_rows']==res['SBF']['rows']==61)
check('SN_original_order_and_row_identity',[x['row_id'] for x in sn]==[f'data/sn1a_hf_pp.dat:L{i}' for i in range(2,279)])
check('SBF_original_order_and_row_identity',[x['row_id'] for x in sbf]==[f'data/sbf_hf.dat:L{i}' for i in range(2,63)])
check('SN_repeated_names_preserved',len(set(x['sn'] for x in sn))==238 and len(sn)==277)
check('SN_whitelisted_keys',all(set(x)=={'sn','sigma_mb_mag_not_used_with_cov','zcmb','vpec_2mpp_km_s','line','row_id'} for x in sn))
check('SBF_whitelisted_keys',all(set(x)=={'host','sigma_M110_mag_unused_upstream','sigma_m110_mag','v2mpp_km_s','line','row_id'} for x in sbf))
for key,expected in [('sn1a_IR',False),('sn1a_ignore_offdiag',False),('z_range_sn1a',False),('z_range_sbf',False),('sn1a_intrinsic',0.0),('sn1a_vp','2m++'),('sbf_v','2m++')]:
    check('fixed_config:'+key,meta['config'][key]['value']==expected)
for key in ['vpec_error','sbf_vpec_error']:
    check('fixed_config:'+key,float(meta['config'][key]['value'])==240.0)
check('result_MM_not_evaluated',res['MM']['evaluated'] is False)
check('result_no_verdict',res['scientific_verdict'] is None)
check('conditional_SBF_label','NOT_ADOPTED' in res['SBF']['second_case_status'])
check('stored_SN_rank_and_residual',res['SN']['raw_covariance_rank']==res['SN']['effective_covariance_rank']==277 and res['SN']['raw_covariance_min_eigenvalue']>0 and res['SN']['inverse_solve_residual_max']<1e-9)
check('stored_result_monotonic_case',res['SBF']['sigma_alpha_if_independent_M_component_added']>=res['SBF']['sigma_alpha_upstream_m_only']>0)
sm,sb=src(C/'qualify_flow_errors.py');tree=ast.parse(sb)
imports=[ast.unparse(x) for x in ast.walk(tree) if isinstance(x,(ast.Import,ast.ImportFrom))]
check('no_upstream_import',not any('h0_constrainer' in x or 'um'==x for x in imports))
for name in ['qualify_flow_errors.py','FLOW_ERROR_PROTOCOL.json','FLOW_ERROR_RESULT.json']:
    atomic(OUT/('SNAPSHOT_'+name),(C/name).read_bytes())
u=ROOT/'h0dn_documentary_review/upstream'
um=json.loads((u.parent/'UPSTREAM_MANIFEST.json').read_bytes());pins={x['path']:x['sha256'] for x in um['files']}
for rel in ['h0_constrainer/h0_constrainer/intercept.py','h0_constrainer/h0_constrainer/equations.py','h0_constrainer/h0_constrainer/data_loader.py','h0_constrainer/h0_constrainer/main.py']:
    m,b=src(u/rel);check('upstream_pin:'+rel,m['sha256']==pins[rel])
for path in [
ROOT/'proveniencia/sbf_error_components/PARECER_NS01_COMPONENTES_SBF.md',
ROOT/'proveniencia/sbf_error_components/MANIFESTO_NS01_COMPONENTES_SBF.json',
ROOT/'proveniencia/h0dn_nonstellar_errors/CONTRATO_ERROS_NAO_ESTELARES_V01.json',
ROOT/'proveniencia/h0dn_nonstellar_errors/extract_nonstellar_errors.py']:
    src(path)
receipt={
'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'scope':'STATIC_INTEGRITY_FORMULA_AND_ROW_ORDER_REVIEW_NO_RECOMPUTATION',
'checks':checks,'checks_passed':sum(x['passed'] for x in checks),'checks_total':len(checks),
'sources':sources,'imports_in_reviewed_script':imports,
'result_status':'EXISTING_COORDINATION_RESULT_REVIEWED_NOT_INDEPENDENTLY_REPRODUCED',
'no_actionable_findings_in_bounded_numerical_prescription':True,
'limits':['Exact fixed-snapshot upstream prescription only, not a general input API',
'SBF independent addition remains conditional algebra, not physical adoption',
'NS01 composition and shared calibration covariance unresolved',
'No covariance completeness or velocity-noise-double-counting proof',
'No numerical fit, evidence, significance or H0 uncertainty inferred',
'No hard-run-budget requalification: wall/CPU reported from existing result; external supervision is outside this static review'],
'new_numerical_propagation_executions':0,'upstream_imports_or_executions':0,
'catalogue_centres_opened':False,'MM_distance_centre_used':False}
atomic(OUT/'REVISAO_FLOW_ERRORS_RECIBO.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks_passed':receipt['checks_passed'],'checks_total':len(checks),'receipt':metadata(OUT/'REVISAO_FLOW_ERRORS_RECIBO.json')[0]},ensure_ascii=False))
