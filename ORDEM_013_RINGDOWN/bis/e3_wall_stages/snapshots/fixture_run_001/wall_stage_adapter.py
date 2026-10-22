"""Prepare reviewed wall-stage adapters after explicit budget activation.

Never reads scientific samples or executes E6. Artifact creation and review binding
are separate immutable steps. Preparation alone grants no execution authority.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,re

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
ROOT=BASE.parent
LIMIT=25_000_000
ROUTES=('TAU220_POPULATION','TAU440_FIXED_SOURCE_FISHER','DF220_POPULATION_WIDTH_IV')
GROUPS=('O4_HOJE','O4_CEGO','O4C_GWTC6','O5_BANDA','ET','CE')
METRICS=('z_expected_conditional','N90_information_target','N90_count_scenario','GW250114_equivalents',
         'delta','sigma','correction_over_sigma','rate_per_year','rate_CI','z_physical','lnB')
GATES=('sigma_c_calibrated','floor5_INPUT','floor15_sensitivity','sigma_sys_df','sigma_jit_recovered','correction_over_sigma_physical')
FLAGS=('physical_calibration_paid','null_calibration_paid','selection_paid','normalization_paid','independent_review_passed')


def require(value,message):
    if not value:raise ValueError(message)


def metadata_bytes(p):
    with Path(p).open('rb') as f:raw=f.read(LIMIT+1)
    require(len(raw)<=LIMIT,'Metadata size cap')
    return raw


def sha(p):return hashlib.sha256(metadata_bytes(p)).hexdigest()


def load(p):
    raw=metadata_bytes(p)
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result,'Duplicate key');result[k]=v
        return result
    def finite_float(value):
        result=float(value);require(math.isfinite(result),'Nonfinite metadata number');return result
    return json.loads(raw,object_pairs_hook=pairs,parse_float=finite_float,
        parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))


def pin(p):
    p=Path(p).resolve();require(p.is_relative_to(ROOT.resolve()),'Pin outside Chatgpt')
    return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))


def checked(ref):
    require(isinstance(ref,dict) and set(ref)=={'path','sha256'},'Exact pin object')
    relative=Path(ref['path']);p=(ROOT/relative).resolve()
    require(not relative.is_absolute() and p.is_relative_to(ROOT.resolve()) and p.suffix in ('.json','.md'), 'Metadata path only')
    require(not any('PRIVATE' in x.upper() or 'SECRET' in x.upper() for x in p.parts),'Private data excluded')
    require(re.fullmatch('[0-9a-f]{64}',ref['sha256']) and sha(p)==ref['sha256'],'Pin mismatch')
    return p


def utc(value):
    t=datetime.fromisoformat(value.replace('Z','+00:00'));require(t.utcoffset() is not None,'Timezone required')
    return t.astimezone(timezone.utc)


def pointer(obj,value):
    require(isinstance(value,str) and value.startswith('/'),'JSON Pointer required')
    for key in value[1:].split('/'):
        key=key.replace('~1','/').replace('~0','~');obj=obj[int(key)] if isinstance(obj,list) else obj[key]
    return obj


def publish(p,obj):
    raw=(json.dumps(obj,ensure_ascii=False,allow_nan=False,indent=2)+'\n').encode()
    require(len(raw)<=LIMIT and p.parent.resolve().is_relative_to(HERE.resolve()),'Output path/size')
    t=p.with_name(p.name+'.pending')
    with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    require(t.stat().st_size==len(raw),'Short write')
    os.link(t,p);t.unlink()


def reviewed_predecessor(ref,stage,registration):
    receipt=load(checked(ref));require(receipt['schema']=='E6_REVIEWED_STAGE_V2' and receipt['stage']==stage
        and receipt['registration_sha256']==registration,'Wrong predecessor stage/E2')
    evidence=load(checked(receipt['timeline']['evidence']));checked(receipt['artifact'])
    review=load(checked(receipt['review']))
    require(review['status']=='ACCEPTED_FOR_E6_MAPPING' and review['blocking_findings']==[]
        and review['stage']==stage and review['registration_sha256']==registration
        and review['artifact_sha256']==receipt['artifact']['sha256'],'Predecessor review not accepted')
    require(isinstance(review['reviewer'],str) and review['reviewer'].strip(),'Predecessor reviewer required')
    for k in ('bindings','timeline','predecessor','outcome'):require(review[k]==receipt[k],'Predecessor review differs')
    now=datetime.now(timezone.utc)
    require(utc(receipt['issued_utc'])<=utc(review['reviewed_utc'])<=now,'Predecessor review chronology')
    t=receipt['timeline'];field='recorded_utc_pointer' if t['kind']=='NO_EXECUTION' else 'finished_utc_pointer'
    return receipt,utc(pointer(evidence,t[field]))


def rows_and_bindings(contract,e0,e0_ref,stage):
    """Copy only historical 220 INPUT floors; no calibration or expected-z arithmetic."""
    require(stage in ('E3.2','E3.3','TEST'),'Only allocation/wall stages')
    if stage!='TEST':return [],[]
    readings=contract['readings'];require(len(readings)==10 and len(set(readings))==10,'Ten unique readings')
    floors={x['reading']:(i,x) for i,x in enumerate(e0['systematic_conditions'])}
    require(len(floors)==len(e0['systematic_conditions']),'Duplicate floor reading')
    require(set(readings)<=set(floors),'Missing historical floor metadata')
    rows=[];bindings=[]
    for route in ROUTES:
        units=contract['semantic_units'][route]
        for reading in readings:
            for group in GROUPS:
                gate=dict(color='red',status='NO_EXECUTION_UNCALIBRATED__E0_FLOORS_INPUT_ONLY',decision_reviewed=False,
                    **{k:False for k in FLAGS},**{k:None for k in GATES},
                    units={k:units[k][0] if units[k] else 'INAPPLICABLE_NULL' for k in GATES})
                context=None
                if route=='TAU220_POPULATION':
                    i,floor=floors[reading];gate['floor5_INPUT']=floor['floor5_INPUT'];gate['floor15_sensitivity']=floor['floor15_INPUT']
                    context=dict(source=e0_ref,pointer='/systematic_conditions/'+str(i),statute='INPUT_HISTORICAL_NOT_CALIBRATION')
                row=dict(route=route,reading=reading,data_group=group,reading_statute=contract['reading_statutes'][reading],
                    metrics={k:None for k in METRICS},gate=gate,historical_floor_context=context,
                    summary=dict(test_data_present=False,verdict='AWAITING_DATA'),
                    scope='NO_EXECUTION_NO_TEST_POSTERIOR__COST_AND_PHYSICAL_RESULTS_OPEN')
                idx=len(rows);rows.append(row)
                binding=dict(route=route,reading=reading,data_group=group,scenario_id='wall_no_new_pe',scope=row['scope'],
                    metrics={k:dict(pointer='/rows/'+str(idx)+'/metrics/'+k,unit=units[k][0] if units[k] else 'INAPPLICABLE_NULL') for k in METRICS if stage=='TEST' or k not in ('z_physical','lnB')},
                    gate_pointer='/rows/'+str(idx)+'/gate')
                if stage=='TEST':binding['test_summary_pointer']='/rows/'+str(idx)+'/summary'
                bindings.append(binding)
    require(len(rows)==len(bindings)==180,'Coverage mismatch')
    return rows,bindings


def prepare(args):
    require(args.execute and args.authorization and args.authorization_sha256,'Principal budget activation required; preparation only')
    authorization_ref=pin(args.authorization)
    require(authorization_ref['sha256']==args.authorization_sha256,'Authorization changed')
    checked(authorization_ref)
    auth=load(args.authorization);stage=auth['stage'];require(stage in ('E3.2','E3.3','TEST'),'Allocation/wall stage only')
    require(auth['status']=='AUTHORIZED_WALL_STAGE_CANDIDATE_AFTER_BUDGET','No actual stage authorization')
    require(auth['helper_sha256']==sha(__file__),'Helper pin differs')
    require(auth['test_posterior_available'] is False and auth['new_PE_allowed'] is False
        and auth['new_injections_allowed'] is False and auth['cost_per_converged_PE'] is None,'Wall scope differs')
    require(auth['outcome'] in (('COMPLETED','PARTIAL','BLOCKED','UNAVAILABLE') if stage=='E3.2' else
        ('PARTIAL','BLOCKED','UNAVAILABLE')),'Wall cannot be COMPLETED')
    require(isinstance(auth['reason'],str) and auth['reason'].strip(),'Explicit wall reason')
    regpath=checked(auth['registration']);require(regpath==(BASE/'RINGDOWN_5SIGMA_V1.json').resolve(),'Wrong E2 path')
    reg=load(regpath);require(reg['status']=='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST','Wrong E2 status')
    actpath=checked(auth['E2_activation']);require(actpath==(ROOT/reg['activation']['receipt_relative_to_Chatgpt']).resolve(),'Activation path')
    act=load(actpath);require(act['status']=='E2_ACTIVATION_COMPLETE' and act['registration_sha256']==auth['registration']['sha256'],'Activation differs')
    budgetpath=checked(auth['budget']);require(budgetpath==(ROOT/reg['allocation_policy']['relative_to_Chatgpt']).resolve(),'Not active budget slot')
    budget=load(budgetpath);require(budget['parent_registration_sha256']==auth['registration']['sha256'],'Budget parent')
    witness=checked(auth['budget_witness']);require(witness==(ROOT/budget['witness_relative_to_Chatgpt']).resolve()
        and witness.is_relative_to((ROOT/'TUNEL/DO_CHATGPT').resolve()),'Witness location')
    text=witness.read_text(encoding='utf-8-sig')
    require(re.findall(r'^allocation_sha256: ([0-9a-f]{64})\s*$',text,re.M)==[auth['budget']['sha256']],'Budget not witnessed')
    dates=re.findall(r'^registered_utc: (\S+)\s*$',text,re.M);require(len(dates)==1,'Ambiguous witness date')
    now=datetime.now(timezone.utc)
    require(utc(act['finished_utc'])<=utc(budget['registered_utc'])<=utc(dates[0])<=utc(auth['issued_utc'])<=now,'Budget/activation chronology')
    jobsref=dict(path=budget['jobs_relative_to_Chatgpt'],sha256=budget['jobs_sha256']);jobs=load(checked(jobsref))
    require(jobs['schema_version']=='E2_PE_JOBS_V2' and jobs['parent_registration_sha256']==auth['registration']['sha256']
        and jobs['jobs']=={},'New PE jobs must be absent from wall allocation')
    contract=load(checked(auth['E6_contract']));require(contract['schema']=='E6_PREPARATION_CONTRACT_V2'
        and contract['readings']==reg['readings'],'E6 contract/readings differ')
    e0=load(checked(auth['E0']));require(auth['E0']==load(HERE/'PREPARATION_PINS.json')['E0'],'Historical E0 floor pin differs')
    require(auth['E6_contract']==load(HERE/'PREPARATION_PINS.json')['E6_contract'],'Reviewed E6 contract pin differs')
    for note in auth['principal_notes']:checked(note)
    require(auth['principal_notes'],'Pinned principal B3/B4/TEST note required')
    if stage=='E3.2':
        require(auth['predecessor']==auth['E2_activation'],'E3.2 predecessor must be E2 activation')
        predecessor=None
    else:
        predecessor,last=reviewed_predecessor(auth['predecessor'],'E3.2' if stage=='E3.3' else 'E3.3',auth['registration']['sha256'])
        require(utc(act['finished_utc'])<=last<=now and utc(predecessor['issued_utc'])<=now,'Predecessor chronology')
    if stage=='E3.3':
        require(predecessor['timeline']['kind']=='ALLOCATION_REGISTERED'
            and predecessor['timeline']['evidence']==auth['budget'],'E3.2 must identify actual activated allocation')
    rows,bindings=rows_and_bindings(contract,e0,auth['E0'],stage)
    now=datetime.now(timezone.utc)
    require(re.fullmatch('[a-z][a-z0-9_]{0,63}',auth['run_id']),'Unsafe run id')
    folder=HERE/'candidates'/auth['run_id'];require(not folder.exists() and folder.parent.resolve().is_relative_to(HERE.resolve()),'Existing/escaped candidate')
    source=dict(schema='E3_WALL_SOURCE_V1',status='NO_EXECUTION',stage=stage,recorded_utc=now.isoformat(),reason=auth['reason'],
        predecessor_evidence_sha256=predecessor['timeline']['evidence']['sha256'] if predecessor else auth['E2_activation']['sha256'],
        registration=auth['registration'],budget=auth['budget'],budget_witness=auth['budget_witness'],principal_notes=auth['principal_notes'],
        E0_floor_source=auth['E0'],cost_per_converged_PE=None,test_posterior_available=False,rows=rows)
    for key in ('registration','E2_activation','budget','budget_witness','predecessor','E0','E6_contract'):checked(auth[key])
    checked(jobsref)
    for note in auth['principal_notes']:checked(note)
    require(sha(args.authorization)==args.authorization_sha256,'Authorization changed before writing')
    folder.mkdir(parents=True,exist_ok=False)
    if stage=='E3.2':
        artifact=auth['budget']
        timeline=dict(kind='ALLOCATION_REGISTERED',evidence=artifact,authorized_utc_pointer='/registered_utc',
            started_utc_pointer='/registered_utc',finished_utc_pointer='/registered_utc')
    else:
        publish(folder/'WALL_SOURCE.json',source);artifact=pin(folder/'WALL_SOURCE.json')
        timeline=dict(kind='NO_EXECUTION',evidence=artifact,recorded_utc_pointer='/recorded_utc',reason_pointer='/reason',
                      predecessor_evidence_sha256_pointer='/predecessor_evidence_sha256')
    draft=dict(schema='E6_REVIEWED_STAGE_V2',stage=stage,registration_sha256=auth['registration']['sha256'],outcome=auth['outcome'],
        issued_utc=datetime.now(timezone.utc).isoformat(),artifact=artifact,predecessor=auth['predecessor'],timeline=timeline,bindings=bindings)
    publish(folder/'ADAPTER_REVIEW_REQUEST.json',dict(status='UNREVIEWED_NOT_E6_RECEIPT',draft=draft,
        authorization_sha256=args.authorization_sha256,authorization_path=str(Path(args.authorization).resolve()),helper_sha256=sha(__file__),
        allocation_time_scope='E3.2 timeline fields denote the single actual documentary registration event, not PE/injection execution; later main GO authorizes adapter issuance only',
        first_issuance_scope='Actual first publication of this adapter declaration; review reference will be bound later without altering this request'))


def finalize(args):
    require(args.execute and args.request and args.request_sha256 and args.review and args.review_sha256,'Explicit reviewed draft required')
    request=Path(args.request).resolve();reviewpath=Path(args.review).resolve()
    require(request.is_relative_to(HERE.resolve()) and sha(request)==args.request_sha256,'Draft pin')
    reviewref=pin(reviewpath);require(reviewref['sha256']==args.review_sha256,'Review pin');checked(reviewref)
    obj=load(request);require(obj['status']=='UNREVIEWED_NOT_E6_RECEIPT' and obj['helper_sha256']==sha(__file__),'Unknown draft/helper')
    draft=obj['draft'];review=load(reviewpath);now=datetime.now(timezone.utc)
    require(review['status']=='ACCEPTED_FOR_E6_MAPPING' and review['blocking_findings']==[] and review['request_sha256']==args.request_sha256,'Independent review not closed')
    for k in ('stage','registration_sha256','bindings','timeline','predecessor','outcome'):require(review[k]==draft[k],'Review scope differs')
    require(review['artifact_sha256']==draft['artifact']['sha256'] and isinstance(review['reviewer'],str) and review['reviewer'].strip(),'Reviewer/artifact required')
    require(utc(draft['issued_utc'])<=utc(review['reviewed_utc'])<=now,'Actual first issuance/review chronology')
    checked(draft['artifact'])
    if draft['stage']!='E3.2':
        reviewed_predecessor(draft['predecessor'],'E3.2' if draft['stage']=='E3.3' else 'E3.3',draft['registration_sha256'])
    else:checked(draft['predecessor'])
    authpath=Path(obj['authorization_path']);require(sha(authpath)==obj['authorization_sha256'],'Original main activation changed')
    auth=load(authpath)
    for key in ('registration','E2_activation','budget','budget_witness','E0','E6_contract'):checked(auth[key])
    for note in auth['principal_notes']:checked(note)
    budget=load(checked(auth['budget']))
    checked(dict(path=budget['jobs_relative_to_Chatgpt'],sha256=budget['jobs_sha256']))
    final=dict(draft,review=pin(reviewpath));publish(request.parent/'ADAPTER_REVIEWED.json',final)
    publish(request.parent/'FINALIZATION_RECEIPT.json',dict(status='REVIEW_BOUND_NOT_E6_EXECUTED',first_issuance_request=pin(request),
        final_adapter=pin(request.parent/'ADAPTER_REVIEWED.json'),review=pin(reviewpath),published_utc=now.isoformat(),
        issued_utc_meaning='First adapter declaration actually issued in the preserved request, not this later review-binding publication time',E6_executed=False))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('prepare','finalize'))
    p.add_argument('--execute',action='store_true');p.add_argument('--authorization',type=Path);p.add_argument('--authorization-sha256')
    p.add_argument('--request',type=Path);p.add_argument('--request-sha256');p.add_argument('--review',type=Path);p.add_argument('--review-sha256')
    args=p.parse_args();(prepare if args.action=='prepare' else finalize)(args)


if __name__=='__main__':main()
