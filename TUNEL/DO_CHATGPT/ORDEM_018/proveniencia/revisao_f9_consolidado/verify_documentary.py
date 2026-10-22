"""Read/hash documentary sources only. No scientific imports or execution."""
from pathlib import Path
import datetime,hashlib,json,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'proveniencia'))
from audit_provenance import atomic,metadata
DRAFT=ROOT/'f9_consolidated_draft'
resolver=json.loads((DRAFT/'RESOLUTOR_F9.json').read_text(encoding='utf-8'))
manifest=json.loads((DRAFT/'MANIFESTO_ENTREGA.json').read_text(encoding='utf-8'))
checks=[];sources=[]
def check(name,ok,detail=None):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
def pinned(name,row):
    p=Path(row['path'])
    assert p.resolve().is_relative_to(ROOT.resolve())
    now,_=metadata(p)
    check('pin:'+name,now['sha256']==row['sha256'] and now['bytes']==row['bytes'],
          {'expected':row['sha256'],'read':now['sha256']})
    sources.append(dict(source_id=name,**now))
    return p
for row in manifest['artifacts']:
    pinned('delivery:'+row['relative_path'],row)
for name,row in resolver['sources'].items():
    pinned(name,row)
    if 'snapshot' in row:
        p=pinned(name+':snapshot',row['snapshot'])
        check('snapshot_identical:'+name,p.read_bytes()==Path(row['path']).read_bytes())
def read(source):
    return json.loads(Path(resolver['sources'][source]['path']).read_text(encoding='utf-8'))
resolved=resolver['resolved_contract'];v2=read('verdict_v2');bound=read('calibration')
for key in ['models','definitions','physical_priors']:
    check('exact_V2:'+key,resolved[key]==v2[key])
for dest,src in [('primary_family','primary_family'),('definition_of_calibrated_tail','calibration'),('decision','verdict')]:
    check('exact_V2:'+dest,resolved['frequentist'][dest]==v2[src])
for key in ['classification','prerequisites','base_theorem','gain_theorem','structural_dimensions','test_envelopes','certificates','p_value','V2_interoperation']:
    check('exact_bound:'+key,resolved['frequentist']['recommended_calibration'][key]==bound[key])
measure=read('nuisance_measure');linear=read('linear_design');bg=read('background_protocol')
check('nuisance_formula_exact',resolved['nuisance']['formula']==measure['flat_measure_ratio'])
check('nuisance_columns_exact',resolved['nuisance']['eta_columns']==measure['eta_columns']==linear['eta_columns'])
check('network_counts_exact',resolved['data']['local_counts']==linear['counts'])
for dest,src in [('protocol_configuration','background'),('redshift_conventions','redshifts'),('prior','prior'),('H5','h5_candidate')]:
    check('background_exact:'+dest,resolved['background'][dest]==bg[src])
check('clause_count',len(resolver['clauses'])==13)
clauseids={x['id'] for x in resolver['clauses']}
for row in resolver['clauses']:
    check('clause_refs:'+row['id'],all(x in resolver['sources'] for x in row['source_ids']))
    check('clause_conditions_and_gaps:'+row['id'],all(row.get(x) for x in ['proposal','application_condition','implementation_gap']))
acc=json.loads(Path(resolver['sources']['historical_accumulator']['snapshot']['path']).read_text())
supersessions=[]
for row in resolver['superseded_legacy_fields']:
    value=acc
    for token in row['json_pointer'].strip('/').split('/'):
        token=token.replace('~1','/').replace('~0','~')
        value=value[int(token)] if isinstance(value,list) else value[token]
    supersessions.append({'pointer':row['json_pointer'],'historical_value':value,'status':row['status']})
    check('supersession_pointer:'+row['json_pointer'],True)
    check('supersession_refs:'+row['json_pointer'],all(x in clauseids for x in row['replacement_clause_ids']) and all(x in resolver['sources'] for x in row['replacement_source_ids']))
for row in resolver['alternatives_for_real_obstacles']:
    check('alternatives:'+row['id'],len(row['options'])>=2 and all(all(s in resolver['sources'] for s in q['source_ids']) for q in row['options']))
for name in ['frozen_V1','F1_complete','opening_authorized','adopted_scientific_choices']:
    check('scope:'+name,resolver[name] is False)
check('all_observed_outputs_null',all(v is None for v in resolver['observed_outputs_now'].values()))
check('all_forbidden_operations_false',all(v is False for v in resolver['forbidden_operations_performed'].values()))
check('MM_symbolic_and_retained',resolved['MM']['numerical_variances'] is None and resolved['MM']['selection_removed'] is False)
check('universal_R_A_indicator_scope_explicit','indicador' in next(q for q in resolver['clauses'] if q['id']=='C02')['application_condition'])
check('no_global_power_claim',resolved['information_power']['global_power'] is None and resolved['information_power']['preflight262_is_global_power'] is False)
check('E45_not_new_output',resolved['chronology_and_reproduction']['historical_numbers_copied_as_F9_outputs'] is False)
order=ROOT.parents[1]/'PARA_CHATGPT'/'ORDEM_018_o_discriminante.md'
sources.append(dict(source_id='ORDEM018',**metadata(order)[0]))
sources.append(dict(source_id='reviewed_manifest',**metadata(DRAFT/'MANIFESTO_ENTREGA.json')[0]))
report={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'DOCUMENTARY_VERIFICATION_COMPLETE' if all(x['passed'] for x in checks) else 'DOCUMENTARY_DIFFERENCES_FOUND',
        'sources':sources,'source_pins_in_draft':len(resolver['sources']),
        'delivery_manifest_entries':len(manifest['artifacts']),
        'checks':checks,'check_count':len(checks),'failed':[x for x in checks if not x['passed']],
        'supersessions_resolved_to_actual_pointer':supersessions,
        'scope':'Hash/bytes/JSON field identity and documentary review; no raw catalogue or centers, no source execution, solver, rank, covariance, CDF, fit, posterior or scientific verdict',
        'models_remote_called':False,'science_executed':False,'new_centers_opened':False,'author_files_modified':False}
atomic(OUT/'DOCUMENTARY_VERIFICATION.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','source_pins_in_draft','delivery_manifest_entries','check_count','failed']},ensure_ascii=False))
