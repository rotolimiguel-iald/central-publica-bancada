"""Static packaging only. Does not import any prepared instrument or solver."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from fractions import Fraction
import ast, hashlib, json, os, uuid

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
SOURCE = ROOT/'preregistros/conjunto_d/guard_wsl_integration_preparation_v2'
POSIX = '/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/' + BASE.name
PREPARATION = 'f07e4aba-e976-4d78-be1c-449968d4a305'


def pin(p):
    raw=p.read_bytes();return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def put(p, data):
    if isinstance(data,dict):data=(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if isinstance(data,str):data=data.encode('utf-8')
    p.parent.mkdir(parents=True,exist_ok=True)
    old=p.read_bytes() if p.exists() else None
    if old==data:return
    if old is not None:
        bak=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(old);assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(data);assert tmp.read_bytes()==data and (p.read_bytes() if p.exists() else None)==old
    os.replace(tmp,p);assert p.read_bytes()==data


def main():
    assert not any((BASE/x).exists() for x in ('RUN','CLAIM.json','AUTORIZACAO_ROOT.json','RESULT.json'))
    req=json.loads((ROOT/'F9_ENGINE_ASSEMBLY_INTEGRATION_REQUEST.json').read_bytes())
    assert req['request_id']==PREPARATION
    sources=[]
    for item in req['sources']:
        actual=pin(Path(item['path']));assert actual==item;sources.append(actual)
    identity_file=BASE/'UNIT_IDENTITY.json'
    if identity_file.exists():identity=json.loads(identity_file.read_bytes())
    else:
        identity={'preparation_request_id':PREPARATION,'proposed_run_request_id':str(uuid.uuid4()),
                  'status':'PROPOSED_NOT_AUTHORIZED_NOT_CLAIMED','created_utc':datetime.now(timezone.utc).isoformat()}
        put(identity_file,identity)
    runid=identity['proposed_run_request_id']
    copies={
        'background_controls.py':ROOT/'f9_background_prediction/background_controls.py',
        'RUNTIME_METADATA.json':ROOT/'f9_background_prediction/RUNTIME_METADATA.json',
        'PROTOCOL_ORIGIN.json':ROOT/'f9_background_prediction/PROTOCOL.json',
        'five_model_assembly.py':ROOT/'f9_five_model_assembly_preparation/five_model_assembly.py',
        'ESPECIFICACAO_LINEAR.json':ROOT/'h0dn_documentary_review/linear_design/ESPECIFICACAO_LINEAR.json',
        'LAYOUT_ESTRUTURAL_3CMB_13BAO.json':ROOT/'f9_structural_layout_preparation/LAYOUT_ESTRUTURAL_3CMB_13BAO.json',
        'audit_guard.py':SOURCE/'sources/audit_guard.py'}
    for name,path in copies.items():
        sources.append(pin(path));put(BASE/'sources'/name,path.read_bytes())
    reviews={'REVISAO_MONTADOR.json':ROOT/'RECIBO_ROOT_REVISAO_FIVE_MODEL_ASSEMBLY.json',
             'REVISAO_TRANSPORTE.json':ROOT/'RECIBO_ROOT_WSL_CORRIGIDO_PASS.json'}
    for name,path in reviews.items():sources.append(pin(path));put(BASE/name,path.read_bytes())
    proto=json.loads(copies['PROTOCOL_ORIGIN.json'].read_bytes())
    effective=json.loads(copies['PROTOCOL_ORIGIN.json'].read_bytes())
    quantiles=[Fraction(1,3),Fraction(1,2),Fraction(2,3)]
    theta=[]
    for name,q in zip(proto['prior']['coordinates'],quantiles):
        lo,hi=map(lambda x:Fraction(str(x)),proto['prior']['bounds'][name]);theta.append(float(lo+q*(hi-lo)))
    layout=json.loads(copies['LAYOUT_ESTRUTURAL_3CMB_13BAO.json'].read_bytes())
    z=[0.0]+[float(v) for v in layout['ordered_unique_BAO_redshift_decimals']]
    assert len(z)==8 and z==sorted(set(z)) and theta not in [p['theta'] for p in proto['points']]
    effective.update(request_id=runid,status='PROPOSED_SINGLE_ENGINEERING_PREDICTION_NOT_AUTHORIZED',
        points=[{'id':'prior_quantiles_1_3_1_2_2_3','theta':theta}],
        point_selection='Independent prior quantiles (1/3,1/2,2/3); no observed centres or fitted parameters.',
        accuracy_profiles={'reference':proto['accuracy_profiles']['reference']})
    effective['redshifts']['low_z_controls']=z
    effective['resources'].update(points=1,profiles=1,max_solver_calls=1,timeout_seconds_per_worker=100,total_timeout_seconds=180)
    effective['next_authority']='Specific ROOT integration review and authorization required; original control main/validate/claims are not invoked.'
    put(BASE/'EFFECTIVE_CONFIGURATION.json',effective)
    common_parameters=dict(zip(proto['prior']['coordinates'],theta))
    params={name:dict(common_parameters) for name in ('H1_TGL','H2_LCDM','H3_beta_free','H4_Cepheid','H5_rd_free')}
    params['H3_beta_free']['beta']=float(Fraction(1,40))
    params['H4_Cepheid']['s']=float(Fraction(3,40))
    params['H5_rd_free']['rd_Mpc']=float(Fraction(275,2))
    put(BASE/'MODEL_PARAMETERS.json',params)
    tree=ast.parse(copies['five_model_assembly.py'].read_bytes())
    pins=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id=='SOURCE_PINS' for t in n.targets)))
    put(BASE/'ASSEMBLY_ADMISSION.json',{'schema':'F9_ASSEMBLY_ADMISSION_V1','status':'ENGINEERING_STRUCTURAL_ADMISSION',
        'layout_sha256':pin(copies['LAYOUT_ESTRUTURAL_3CMB_13BAO.json'])['sha256'],'sources':pins,
        'engine_configuration_sha256':pin(BASE/'EFFECTIVE_CONFIGURATION.json')['sha256'],
        'runtime_sha256':pin(BASE/'RUNTIME_INVENTORY.json')['sha256']})
    corrected=ROOT/'preregistros/conjunto_d/guard_wsl_path_repair_preparation/common.py.candidate.txt'
    common=corrected.read_text(encoding='utf-8');sources.append(pin(corrected))
    oldid='4f5d0b21-e1d2-4906-a6ce-eb70e60bc6cf'
    oldwin=str(SOURCE);oldposix='/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/guard_wsl_integration_preparation_v2'
    common=common.replace(oldid,runid).replace(oldwin,str(BASE)).replace(oldposix,POSIX)
    common=common.replace('WSL312_ONE_STDLIB_CACHE_LATCH_CONTROL','F9_ONE_THEORY_BACKGROUND_AND_FIVE_MODEL_ASSEMBLY')
    common=common.replace('WSL_CACHE_LATCH_001','F9_ENGINE_ASSEMBLY_001')
    common=common.replace('a.get("nominal_total_s")==60','a.get("nominal_total_s")==180')
    common=common.replace('    return a,ah',
        '    need(a.get("max_solver_calls")==1 and a.get("no_observed_data") is True, "One theory-only call")\n'
        '    for key,name in (("assembler_review_sha256","REVISAO_MONTADOR.json"),("transport_review_sha256","REVISAO_TRANSPORTE.json")):\n'
        '        need(pin(BASE/name)["sha256"]==a.get(key), "Dependency review absent: "+name)\n'
        '    return a,ah')
    assert 'PurePosixPath' in common and oldid not in common and oldposix not in common
    put(BASE/'common.py',common)
    linux=(SOURCE/'linux_control.py').read_text(encoding='utf-8');sources.append(pin(SOURCE/'linux_control.py'))
    linux=linux.replace(oldposix,POSIX).replace('deadline=ENTRY+15;work=min(ENTRY+9,','deadline=ENTRY+125;work=min(ENTRY+110,')
    linux=linux.replace('deadline=ENTRY+12;stopped=[]','deadline=ENTRY+25;stopped=[]')
    linux=linux.replace('WSL_CONTROL_PASS_PENDING_EXTERNAL_CLEANUP','F9_BACKGROUND_ASSEMBLY_PASS_PENDING_EXTERNAL_CLEANUP')
    linux=linux.replace('"scientific_calls":0,"retry_allowed":False',
        '"scientific_calls":None if child is None else child["solver_calls_attempted"],"retry_allowed":False')
    linux=linux.replace('env={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1"}',
        'env={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1", **{n:"1" for n in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS")}}')
    a=linux.index('def validate_case(');b=linux.index('\ndef supervise(',a)
    linux=linux[:a]+'''def validate_case(g,child,nonce,proc):
    g.need(child["status"]=="ENGINEERING_PREDICTIONS_WRITTEN" and child["request_id"]==g.REQUEST and child["case_id"]==g.CASE,"Case identity/status")
    g.need(child["nonce"]==nonce and child["process"]["pid"]==proc.pid and child["parent_pid"]==os.getpid(),"Case PID/nonce")
    g.need(child["solver_calls_attempted"]==child["solver_calls_returned"]==1 and child["new_children"]==0,"Solver/child budget")
    g.need(child["observed_reads"] is False and child["D_read"] is False and child["module_errors"]==[],"Scope/dependencies")
    snap=child["audit_snapshot"]
    g.need(snap["installed"] and not snap["latched"] and snap["denial_count"]==0 and snap["journal_error"] is None,"Sticky audit")
    journal=BASE/"RUN/CASE/journal.jsonl"
    g.need([json.loads(x) for x in journal.read_bytes().splitlines()]==snap["events"]==[],"Physical journal")
    for name,record in child["artifacts"].items():
        p=BASE/"RUN/CASE"/name
        g.need(record=={"path":str(p),**g.pin(p)},"Output pin: "+name)
    g.need(set(child["artifacts"])=={"BACKGROUND_RESULT.json","ENGINE_EXECUTION_RECEIPT.json","BACKGROUND_PACKET.json","FIVE_MODEL_OUTPUT.json"},"Output completeness")
    result=g.read(BASE/"RUN/CASE/FIVE_MODEL_OUTPUT.json")
    g.need(result["status"]=="ENGINEERING_ONLY" and result["certification"]["certified"] is False,"No certificate promotion")
    g.need(len(result["row_ids"])==283 and result["nuisance"]["dimension"]==63,"Assembly dimensions")
    g.need(set(result["models"])=={"H1_TGL","H2_LCDM","H3_beta_free","H4_Cepheid","H5_rd_free"},"Five models")
    g.need(all(len(v["mean_without_nuisance"])==283 for v in result["models"].values()),"Five prediction lengths")
    claim=g.read(BASE/"RUN/CASE/CASE_CLAIM.json")
    g.need(claim["nonce"]==nonce and claim["process"]==child["process"],"Case claim")

''' +linux[b:]
    put(BASE/'linux_control.py',linux)
    launch=(SOURCE/'launch_windows.py').read_text(encoding='utf-8');sources.append(pin(SOURCE/'launch_windows.py'))
    launch=launch.replace(oldwin,str(BASE)).replace('deadline=ENTRY+60;work=ENTRY+40','deadline=ENTRY+180;work=ENTRY+140')
    launch=launch.replace('WSL_CONTROL_PASS_PENDING_EXTERNAL_CLEANUP','F9_BACKGROUND_ASSEMBLY_PASS_PENDING_EXTERNAL_CLEANUP')
    launch=launch.replace('PASS_WSL_STDLIB_INTEGRATION_ONCE','ENGINEERING_F9_PREDICTION_ONCE')
    launch=launch.replace('linux["scientific_calls"]==0','linux["scientific_calls"]==1')
    launch=launch.replace('"scientific_calls":0,"D_read":False',
        '"scientific_calls":None if linux is None else linux["scientific_calls"],"D_read":False')
    launch=launch.replace('nominal60s','nominal180s')
    put(BASE/'launch_windows.py',launch)
    inherited=json.loads((SOURCE/'CONTRATO_WSL.json').read_bytes());sources.append(pin(SOURCE/'CONTRATO_WSL.json'))
    inv=json.loads((BASE/'RUNTIME_INVENTORY.json').read_bytes())
    indexed={x['path']:x for x in inv['pins']}
    linux_pins=[]
    for item in inherited['linux_pins']:
        actual=indexed.get(item['path']);assert actual==item, item['path'];linux_pins.append(actual)
    windows_pins=[]
    for item in inherited['windows_pins']:
        actual=pin(Path(item['path']));assert actual==item;windows_pins.append(actual)
    local_names=['common.py','worker.py','linux_control.py','launch_windows.py','UNIT_IDENTITY.json',
        'EFFECTIVE_CONFIGURATION.json','MODEL_PARAMETERS.json','ASSEMBLY_ADMISSION.json','RUNTIME_INVENTORY.json']
    local_names += ['sources/'+name for name in copies] + list(reviews)
    local_pins=[]
    for name in local_names:
        item=pin(BASE/name);item['relative_path']=name;del item['path'];local_pins.append(item)
    put(BASE/'CONTRATO_WSL.json',{'schema':'F9_ENGINE_ASSEMBLY_INTEGRATION_PREPARATION_V1',
        'preparation_request_id':PREPARATION,'request_id':runid,'scope':'F9_ONE_THEORY_BACKGROUND_AND_FIVE_MODEL_ASSEMBLY',
        'status':'PREPARED_AWAITING_INDEPENDENT_REVIEW_NO_AUTHORIZATION',
        'local_pins':local_pins,'linux_pins':linux_pins,'windows_pins':windows_pins,
        'limits':{'solver_calls':1,'primary_WSL':1,'cleanup_WSL':1,'children':1,'threads':1,
                  'nominal_total_s':180,'primary_work_s':140,'Linux_child_work_s':110,'Linux_cleanup_s':25,'retries':0},
        'future_authority':'AUTORIZACAO_ROOT.json plus pinned integration, assembler and transport reviews; none created here',
        'admission_note':'ASSEMBLY_ADMISSION is data provenance, not execution authorization or scientific certification',
        'read_scope':'Pinned runtime, local copies and exact process identity only; no observed catalogues or network',
        'runtime_scope':'Inventory and Linux alias hash checks; Python audit is cooperative, not OS sandbox/native syscall coverage',
        'memory_cap':'Peak worker RSS reported by existing engine; no OS memory cap claimed',
        'original_control_slots_reused':False,'originals_modified':False})
    checks=[]
    for name in ['common.py','worker.py','linux_control.py','launch_windows.py']+[f'sources/{n}' for n in copies if n.endswith('.py')]:
        ast.parse((BASE/name).read_bytes(),filename=name);checks.append(name)
    for item in local_pins:
        actual=pin(BASE/item['relative_path']);assert all(actual[k]==item[k] for k in ('bytes','sha256'))
    assert not any((BASE/x).exists() for x in ('RUN','CLAIM.json','AUTORIZACAO_ROOT.json','RESULT.json'))
    put(BASE/'SOURCE_LINEAGE.json',{'sources':sources,'request':pin(ROOT/'F9_ENGINE_ASSEMBLY_INTEGRATION_REQUEST.json'),
        'copies_exact':{n:pin(BASE/'sources'/n)['sha256']==pin(p)['sha256'] for n,p in copies.items()},
        'transport_delta':'New identity/paths/scope/deadlines/acceptance; PurePosixPath reviewed candidate; STOP/gate/pidfd/journal/capture retained',
        'engine_delta':'None. Call prediction_worker directly, never historical main/validate/run_controls/execute_worker_once.'})
    put(BASE/'STATIC_PREPARATION_RECEIPT.json',{'preparation_request_id':PREPARATION,'proposed_run_request_id':runid,
        'created_utc':datetime.now(timezone.utc).isoformat(),'status':'AST_AND_METADATA_ONLY',
        'AST_files':checks,'local_pins':len(local_pins),'runtime_files':len(inv['pins']),
        'theta_selection_quantiles':[str(q) for q in quantiles],'theta':theta,'redshifts':z,
        'engine_calls_prepared':1,'candidate_imports':0,'solver_calls_executed':0,'observed_reads':0,
        'claims_created':0,'authorizations_created':0,'Linux_processes_started':0,
        'independent_review_required':True,'numerical_certificate':None})
    files=[]
    for p in sorted(BASE.rglob('*')):
        if p.is_file() and '.bak_' not in p.name and '.tmp_' not in p.name and p.name not in ('MANIFESTO_PREPARACAO.json','RECIBO_COORDENACAO.json'):
            item=pin(p);item['path']=p.relative_to(BASE).as_posix();files.append(item)
    put(BASE/'MANIFESTO_PREPARACAO.json',{'preparation_request_id':PREPARATION,'proposed_run_request_id':runid,
        'status':'PREPARED_NOT_RUN_NOT_AUTHORIZED','files':files,'scientific_execution':False})
    print(json.dumps({'manifest':pin(BASE/'MANIFESTO_PREPARACAO.json'),'request_id':runid,
        'files':len(files),'runtime_files':len(inv['pins']),'local_pins':len(local_pins),'candidate_imports':0,'solver_calls':0}))


if __name__=='__main__':main()
