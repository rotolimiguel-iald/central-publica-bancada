"""AST and isolated fake-metadata checks; never execute generator main or real report."""
from pathlib import Path
import ast,hashlib,json,os,copy

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'prepare_final_report_v5_013bis.py'
OUT=HERE/'final_report_v5_checks_001'
cases=[]

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    raw=obj if isinstance(obj,bytes) else json.dumps(obj).encode()
    with path.open('xb') as f:f.write(raw)
    return path

def probe(name,fn,reject=False):
    error=None
    try:fn()
    except Exception as e:error=type(e).__name__+': '+str(e)
    cases.append(dict(name=name,expected_rejection=reject,passed=(error is not None)==reject,error=error))

def require(x):
    if not x:raise ValueError('Fixture expectation')

def main():
    if OUT.exists():raise FileExistsError('Preserve fixtures')
    OUT.mkdir()
    raw=SOURCE.read_bytes();tree=ast.parse(raw);compile(tree,str(SOURCE),'exec')
    nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)) or isinstance(n,ast.FunctionDef) and n.name!='main']
    n={'__file__':str(SOURCE),'__name__':'ast_isolated_metadata_only','R':OUT,'B':OUT/'PACKAGE',
       'LIMIT':25_000_000,'READ_SNAPSHOTS':{}}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SOURCE),'exec'),n)
    sha=n['sha'];p=write(OUT/'note.json',{'dummy':True})
    entry={'sha256':sha(p),'bytes':p.stat().st_size}
    extra=dict(status='DELIVERED_B3_B4_TEST_B5_HASHES_RECHECKED',checks=[{'matches':True}],files={'note.json':entry})
    execution={'products':{}}
    probe('valid_extra_pin',lambda:n['verify_extra'](extra,execution))
    for label,change in [('bad_hash',lambda x:x['files']['note.json'].update(sha256='0'*64)),
        ('bad_bytes',lambda x:x['files']['note.json'].update(bytes=0)),
        ('failed_check',lambda x:x['checks'][0].update(matches=False)),
        ('bad_status',lambda x:x.update(status='FAILED'))]:
        bad=copy.deepcopy(extra);change(bad);probe(label,lambda bad=bad:n['verify_extra'](bad,execution),True)
    payload=write(OUT/'POSTERIORES_PSEOB_DUMMY.json',b'FAKE_NO_ARRAYS')
    ep={'sha256':sha(payload),'bytes':payload.stat().st_size}
    ex=copy.deepcopy(extra);ex['files'][payload.name]=ep
    exe={'products':{payload.name:ep}}
    def guarded_sha(path):
        if Path(path)==payload:raise ValueError('Forbidden payload open')
        return sha(path)
    n['sha']=guarded_sha
    probe('payload_not_opened_supported_by_execution_pin',lambda:require(n['verify_extra'](ex,exe)[payload]['verification'].endswith('NO_SAMPLE_READ')))
    probe('unsupported_payload_rejected',lambda:n['verify_extra'](ex,execution),True)
    n['sha']=sha
    digest='a'*64;part='b'*64
    baseline={'inputs':[{'path':'dummy_input','sha256':digest}],'sources':[{'path':'dummy_source','sha256':digest}]}
    bp=write(n['B']/'bis/INPUT_INTEGRITY_013BIS_retry.json',baseline)
    write(n['B']/'bis/M6_MA_DELIVERY_MANIFEST.json',{'files':{'dummy_part_A':part}})
    rows=[dict(category=c,path=p,expected_sha256=h,actual_sha256=h,matches=True) for c,p,h in
        [('inputs','dummy_input',digest),('sources','dummy_source',digest),('delivered_part_A','dummy_part_A',part)]]
    integrity=dict(status='PASS_FROZEN_INPUTS_DELIVERED_A_AND_SIZE_LAYOUT',checks=rows,baseline_sha256=sha(bp),
        oversized_outside_cache=[],metadata_exceptions=[{'path':'dummy_link','scope':'METADATA_ONLY'}])
    probe('integrity_complete_with_explicit_exception',lambda:require(n['validate_integrity'](integrity)==dict(inputs=1,sources=1,delivered_part_A=1)))
    for label,change in [('integrity_false_match',lambda x:x['checks'][0].update(matches=False)),
        ('integrity_hash_disagrees',lambda x:x['checks'][0].update(actual_sha256='c'*64)),
        ('integrity_missing_source',lambda x:x['checks'].pop(1)),
        ('integrity_duplicate_source',lambda x:x['checks'].append(copy.deepcopy(x['checks'][1]))),
        ('integrity_oversize',lambda x:x['oversized_outside_cache'].append({'path':'dummy'})),
        ('integrity_failed_status',lambda x:x.update(status='VISIBLE_INTEGRITY_OR_LAYOUT_DIFFERENCE'))]:
        bad=copy.deepcopy(integrity);change(bad);probe(label,lambda bad=bad:n['validate_integrity'](bad),True)
    for label,data in [('duplicate',b'{"a":1,"a":2}'),('nonfinite',b'{"a":1e999}')]:
        pp=write(OUT/(label+'.json'),data);probe('reject_'+label,lambda pp=pp:n['load'](pp),True)
    probe('outside_reference',lambda:n['artifact_path']('../outside.json'),True)
    probe('private_reference',lambda:n['artifact_path']('E2_PRIVATE/seed.json'),True)
    destination=OUT/'exclusive.md';n['new'](destination,b'preserved')
    probe('refuse_output_replacement',lambda:n['new'](destination,b'new'),True)
    probe('old_output_intact',lambda:require(destination.read_bytes()==b'preserved'))
    # Structural assertions: CLI compatibility, no main execution, explicit source paths.
    text=raw.decode('utf-8')
    probe('CLI_preserved_and_additions_documented',lambda:require(all(x in text for x in
        ('--e6-result','--e7-review','--integrity-receipt','--extra-manifest','--e6-review','--output-dir','--replay'))))
    probe('E6_section_wired_not_unused',lambda:require('lines+=extra_lines' in text and 'documentary_sections(e6,' in text))
    for label,prediction in [('null',None),('text','OPEN'),('bool',False),('nan',float('nan')),('infinity',float('inf'))]:
        probe('ratio_OPEN_'+label,lambda prediction=prediction:require(n['historical_ratio_cell'](prediction,0)=='OPEN'))
    probe('R_GLOBAL_numeric_zero_preserved',lambda:require(n['historical_ratio_cell'](-0.0,0)=='0'))
    probe('numeric_prediction_historical_ratio_preserved',lambda:require(n['historical_ratio_cell'](-0.02,0.3)=='0.3'))
    probe('undefined_prediction_nonzero_history_still_OPEN',lambda:require(n['historical_ratio_cell'](None,0.3)=='OPEN'))
    receipts={
        'bis/RESULT_E2_NULL_CAMPAIGN.json':{'wall_seconds':4.25},
        'bis/e4_e5_prepare/runs/authorized_001/RESULT_RECEIPT.json':{'wall_seconds_through_result_hash':2.5,'process_CPU_seconds_through_result_hash':1.5},
        'bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json':{'wall_seconds':1.25},
        'bis/E4_E5_EXECUTION_V1.json':{'wall_seconds':2.75}}
    inventory={}
    for relative,obj in receipts.items():
        pp=write(n['B']/relative,obj);inventory[relative]={'sha256':sha(pp),'bytes':pp.stat().st_size}
    mp=write(n['B']/'bis/B2_DELIVERY_MANIFEST.json',{'files':inventory})
    probe('B2_four_observed_times_exactly_copied',lambda:require([x['wall_seconds'] for x in n['load_b2_costs']()]==[4.25,2.5,1.25,2.75]))
    probe('B2_CPU_unknown_not_zero',lambda:require([x['cpu_seconds'] for x in n['load_b2_costs']()]==[None,1.5,None,None]))
    fake_sha=n['sha'];n['sha']=lambda p:'0'*64 if Path(p)==n['B']/'bis/RESULT_E2_NULL_CAMPAIGN.json' else fake_sha(p)
    probe('B2_bad_receipt_pin_refused',lambda:n['load_b2_costs'](),True)
    n['sha']=fake_sha
    probe('successor_default_is_new_normal_directory',lambda:require("default=B/'bis/final_report_v5_001'" in text))
    b1files={'bis/e1_nuisance_v2/runs/authorized_001/RECEIPT.json':{'wall_seconds':4.1,'cpu_seconds':2.4},
        'bis/E1_DIRECT_KDE_REVIEW.json':{'wall_seconds':1.3}}
    note=[]
    for rel,obj in b1files.items():
        pp=write(n['B']/rel,obj);note.append('- `'+rel+'` — `'+sha(pp)+'`')
    np=write(OUT/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_B1_portao_e_nuisance.md',('\n'.join(note)+'\n').encode())
    write(n['B']/'bis/B1_DELIVERY_MANIFEST.json',{'delivery_sha256':sha(np)})
    probe('B1_exact_receipt_fields_copied',lambda:require([(x['wall_seconds'],x['cpu_seconds']) for x in n['load_b1_costs']()]==[(4.1,2.4),(1.3,None)]))
    real_sha=n['sha'];n['sha']=lambda p:'0'*64 if Path(p)==np else real_sha(p)
    probe('B1_note_hash_mismatch_refused',lambda:n['load_b1_costs'](),True)
    n['sha']=lambda p:'0'*64 if Path(p)==n['B']/'bis/E1_DIRECT_KDE_REVIEW.json' else real_sha(p)
    probe('B1_review_receipt_hash_mismatch_refused',lambda:n['load_b1_costs'](),True)
    n['sha']=real_sha
    probe('effective_deadline_printed_beside_nominal_balance',lambda:require('Prazo efetivo da alocação' in text and 'não prorroga essa reserva' in text))
    result=dict(scope='AST_AND_FAKE_METADATA_ONLY_NO_GENERATOR_EXECUTION',total=len(cases),passed=sum(c['passed'] for c in cases),
        source_sha256=hashlib.sha256(raw).hexdigest(),cases=cases,real_draft_created=False,science_executed=False,
        posterior_arrays_read=False,E6_rerun=False)
    target=HERE/'FINAL_REPORT_V5_CHECKS_001.json';write(target,result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
    if result['passed']!=result['total']:raise SystemExit(1)

if __name__=='__main__':main()
