"""Read A's completed finite diagnostics, never execute their code or native calls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,math

HERE=Path(__file__).resolve().parent
B=HERE.parents[1];D=B/'bis/e3_pilot_failure_diagnostic';C=D/'cases'
pins={};checks=[]
def sha(p):
    value=hashlib.sha256(p.read_bytes()).hexdigest();pins[str(p)]=value;return value
def load(p):sha(p);return json.loads(p.read_bytes())
def check(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    if not ok:raise ValueError(name)
plan=load(D/'PLAN_INPUTS.json');plan_sha=sha(D/'PLAN_INPUTS.json')
for name in ('diagnostic_child.py','run_diagnostics.py','prepare_cases.py','collect_and_plan.py'):sha(D/name)
replay=load(D/'PRIOR_REPLAY.json');matches=load(D/'REPLAY_MATCHES.json')
check('replay_receipt_pin',matches['replay_sha256']==sha(D/'PRIOR_REPLAY.json'))
log=(D/'sources/original_PRIVATE.log').read_text();sha(D/'sources/original_PRIVATE.log')
pairs=[tuple(map(float,x)) for x in re.findall(r"'mass_1': np.float64\(([^)]+)\), 'mass_2': np.float64\(([^)]+)\)",log)]
indices=[]
for pair in pairs:
    found=[r for r in replay['draws'] if (r['mass_1_kg_using_Bilby'],r['mass_2_kg_using_Bilby'])==pair]
    check('unique_log_mass_match:'+str(pair),len(found)==1)
    indices.append(found[0]['draw_index_starting_1'])
check('replay_matches_2_8',indices==matches['draw_indices']==[2,8])
rows=[]
deadline=datetime.fromisoformat(plan['deadline_utc'])
for path in sorted(C.glob('*.CONTROLLER.json')):
    ctl=load(path);label=ctl['label'];lp=C/(label+'.log')
    check('case_log_pin:'+label,sha(lp)==ctl['log_sha256'])
    check('case_before_deadline:'+label,datetime.fromisoformat(ctl['finished_utc'])<=deadline)
    check('case_wall_bound:'+label,0<ctl['wall_seconds']<=plan['per_child_wall_cap_seconds']+5)
    result={'label':label,'controller':ctl,'source_calls':0,'returns':[]}
    if label!='PRIOR_REPLAY':
        case=load(C/(label+'.json'));entered=load(C/(label+'.ENTERED.json'))
        check('case_plan:'+label,case['plan_sha256']==plan_sha)
        check('entered_case_pin:'+label,entered['case_sha256']==sha(C/(label+'.json')))
        planned=case.get('sequence',[case['parameters']]);result['source_calls']=len(planned)
        for i,params in enumerate(planned,1):
            call=load(C/(label+f'.CALL_{i}.json'))
            check('call_parameters:'+label+':'+str(i),call['parameters']==params)
            ret=C/(label+f'.RETURN_{i}.json')
            result['returns'].append(load(ret) if ret.exists() else None)
        rp=C/(label+'.RESULT.json')
        result['result_present']=rp.exists()
        if rp.exists():
            saved=load(rp);check('return_sequence:'+label,saved['calls']==result['returns'])
        result['generation_fmax']=case['generation_fmax']
    rows.append(result)
check('finite_child_count',len(rows)==10 and len(rows)<=plan['max_sequential_waveform_children'])
by={x['label']:x for x in rows}
check('sequence_did_not_reproduce_crash',by['SEQUENCE_8_ORIGINAL']['controller']['returncode']==0)
seq=by['SEQUENCE_8_ORIGINAL']['returns']
check('sequence_none_draws',[i+1 for i,x in enumerate(seq) if x['status']=='DOMAIN_RETURNED_NONE']==[2,8])
check('draw8_2048_native_abort',by['DRAW8_2048']['controller']['returncode']==-6 and by['DRAW8_2048']['returns']==[None])
check('allocator_message','free(): invalid next size' in (C/'DRAW8_2048.log').read_text())
for label in ('DRAW2_2048','DRAW2_8192','LOW_GR_2048','LOW_DEFORMED_8192'):
    check('finite_specific_case:'+label,by[label]['returns'][0]['status']=='FINITE_WAVEFORM')
norm2a=by['DRAW2_2048']['returns'][0]['analysis_band_norm2']
norm2b=by['DRAW2_8192']['returns'][0]['analysis_band_norm2']
source_mapping=[]
for item in plan['source_evidence']:
    if 'primary_url' in item:
        source=D/'sources'/Path(item['copy']).name;html=source.with_name(source.name+'.html')
        source_mapping.append(dict(name=source.name,declared_hash=item['sha256'],text_hash=sha(source),html_hash=sha(html),
                                   declared_copy_matches=sha(source)==item['sha256'],adjacent_html_matches=sha(html)==item['sha256']))
        check('HTML_preserved:'+source.name,sha(html)==item['sha256'])
reg=load(B/'RINGDOWN_5SIGMA_V1.json');code=B/'bis/e2_code'
check('frozen_tree_unchanged',{p.relative_to(code).as_posix():sha(p) for p in code.rglob('*.py')}==reg['own_code_tree_sha256'])
ctx=load(B/'cache/E3_PSEOB_PILOT_V1/LAUNCH_CONTEXT.json')
report=dict(status='FINITE_NATIVE_DIAGNOSIS_REVIEWED_REPAIR_NOT_APPROVED',created_utc=datetime.now(timezone.utc).isoformat(),
    blocking_findings=[
        {'id':'NF-R2','issue':'Simple generation_fmax2048 does not repair native safety: DRAW8_2048 aborts with allocator message. No concrete reviewed adapter yet; keep prior/data/family/band and never map numerical incapacity to prior rejection.'},
        {'id':'NF-R3','issue':'No versioned witnessed amendment/run identity and original absolute-stop guard reviewed yet.'},
        {'id':'NF-R4','issue':'PLAN_INPUTS C-source copy fields point to extracted text while pins match adjacent HTML; requires additive mapping correction, not science rerun.'}],
    original_SIGSEGV_cause='OPEN: original eight-draw source sequence does not reproduce rc-11; observed rc-6 at changed fmax is a distinct native failure.',
    NF_R1_scope_update='Finite diagnosis identifies an EDOM path and a separate unsafe native case. It does not establish the original exact crash. Full native root cause is not asserted as a universal prerequisite if a concrete, reviewed repair can preserve support and fail visibly.',
    checks=checks,check_count=len(checks),input_hashes=pins,diagnostic_cases=rows,
    counts={'child_process_receipts':len(rows),'source_children':len(rows)-1,'source_call_entries':sum(x['source_calls'] for x in rows),
            'source_returns':sum(sum(v is not None for v in x['returns']) for x in rows)},
    minor_numeric_control={'DRAW2_norm2_2048':norm2a,'DRAW2_norm2_8192':norm2b,'relative_norm2_difference':abs(norm2b-norm2a)/norm2a,
                           'scope':'Scalar norm agreement cannot establish complex phase, overlap, epoch or full in-band waveform equality; no arrays were saved/read by this review.'},
    source_mapping=source_mapping,original_pilot_stop_utc=ctx['stop_utc'],
    limitations=['Only completed diagnostic receipts examined; no campaign repeated by this reviewer.',
                 'Diagnostic controller receipts witness wait/return but do not record group_absent; no independent group cleanup survey claimed.',
                 'Passing finite examples at8192 does not establish whole-prior support or safety.',
                 'A changed internal sample rate is computational treatment requiring explicit transport review, not new analysis bandwidth.',
                 'Observer is inactive and not a gate.'],
    waveform_calls_by_reviewer=0,PE_runs_by_reviewer=0,strain_read=False,posterior_read=False,
    script_sha256=sha(Path(__file__)))
out=HERE/'PILOT_NATIVE_DIAGNOSTIC_INDEPENDENT_REVIEW.json'
with out.open('xb') as f:f.write((json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
print(json.dumps({'status':report['status'],'checks':len(checks),'receipt_sha256':sha(out),'counts':report['counts'],'norm_control':report['minor_numeric_control']}))
