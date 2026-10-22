# Package preparation only: stdlib, hashes, text/AST; never import scientific code.
from pathlib import Path
import ast,copy,datetime,difflib,hashlib,json,time
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'p3_codec_002'
INIT=ROOT.parent/'p3_init_preparation'
checks=[];copies=[];start=time.perf_counter();cpu=time.process_time()
def info(path):
    raw=Path(path).read_bytes()
    return {'path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def pin(path):
    row=info(path);return {k:row[k] for k in ('sha256','bytes')}
def ck(name,ok):
    checks.append({'name':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
def put(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    ck('fresh:'+str(path.relative_to(ROOT)),not path.exists())
    if isinstance(data,str):data=data.encode('utf-8')
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('xb') as f:f.write(data)
    assert tmp.read_bytes()==data;tmp.replace(path);assert path.read_bytes()==data
def js(path,obj):
    put(path,json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def cp(source,dest):
    put(dest,source.read_bytes());ck('copy:'+str(dest.relative_to(ROOT)),pin(source)==pin(dest))
    copies.append({'source':info(source),'destination':info(dest)})

old=json.loads((OLD/'CONTRATO_P3.json').read_bytes())
for rel,expected in old['inputs'].items():ck('old_input:'+rel,pin((OLD/rel).resolve())==expected)
qualified=json.loads((INIT/'MANIFESTO_RESULTADO_INIT.json').read_bytes())
for e in qualified['files']:ck('qualified_result_pin:'+str(Path(e['path']).relative_to(INIT)),info(Path(e['path']))==e)
control=json.loads((INIT/'CONTROL_INIT_001/RESULT.json').read_bytes())
ck('qualified_control_pass_zero',control['status']=='INITIALIZATION_ONLY_PASS' and all(x==0 for x in control['counters'].values()) and control['source_native_counter']==[0,0.0,0] and not control['blocked_operations'])
ck('qualified_two_labels',[r['synthetic_label'] for r in control['rows']]==[j['label'] for j in old['jobs']])
runtime=json.loads((ROOT/'VERIFICACAO_RUNTIME_INIT003.json').read_bytes())
ck('runtime_current',runtime['status']=='RUNTIME_CURRENT_READ_ONLY' and len(runtime['checks'])==1165 and all(x['passed'] for x in runtime['checks']))
for rel in old['inputs']:
    if not rel.startswith('../') and rel!='driver_p3.py':cp(OLD/rel,ROOT/rel)
for rel in ['init_detectors.py','GEOMETRIA_PINADA.json','DEPENDENCIA_FACTORY_PIN.json','sources/gw/detector/noise_curves/aLIGO_O4_high_asd.txt']:
    cp(INIT/rel,ROOT/rel)

driver=(OLD/'driver_p3.py').read_bytes().decode('utf-8')
changes=[]
def replace(before,after):
    global driver
    ck('replacement_once:'+before.splitlines()[0],driver.count(before)==1)
    driver=driver.replace(before,after)
    changes.append((before,after))
replace('    audit_paths=set();blocked=[]\n','    from init_detectors import build_B, verify_analytic_state\n    geometry=json.loads((ROOT/"GEOMETRIA_PINADA.json").read_text())\n    init_dependency=json.loads((ROOT/"DEPENDENCIA_FACTORY_PIN.json").read_text())\n    allowed_data.add(init_dependency["runtime_path"])\n    audit_paths=set();blocked=[]\n')
replace('    failures=FailureAudit();last_parameters=None\n','    failures=FailureAudit();last_parameters=None\n    initialization_defaults=[];initialization_before=[];initialization_after=[]\n')
replace('            ifos=bilby.gw.detector.InterferometerList(["H1","L1"]);snr2=0.\n','            ifos,initialization_defaults=build_B(bilby,f,psd,geometry,init_dependency);snr2=0.\n')
replace('                ifo.power_spectral_density=bilby.gw.detector.PowerSpectralDensity(frequency_array=f,psd_array=psd)\n','')
replace('                ifo.set_strain_data_from_frequency_domain_strain(d,sampling_frequency=4096,duration=32,start_time=999999984.)\n','                ifo.set_strain_data_from_frequency_domain_strain(d,sampling_frequency=4096,duration=32,start_time=999999984.)\n                initialization_before.append(verify_analytic_state(np,ifo,f,psd,geometry))\n                if not np.array_equal(ifo.strain_data.frequency_domain_strain,d):\n                    raise ValueError("Stored synthetic strain differs")\n')
replace('        def logl(v):\n','        initialization_after=[verify_analytic_state(np,ifo,f,psd,geometry) for ifo in likelihood.interferometers]\n        if initialization_after!=initialization_before:raise ValueError("Analytic detector state changed in likelihood constructor")\n        if blocked:raise ValueError("Initialization swallowed a blocked operation")\n        def logl(v):\n')
replace('                "failure_receipt":failures.summary(counts),\n','                "failure_receipt":failures.summary(counts),\n                "initialization_defaults":initialization_defaults,\n                "initialization_analytic_before_likelihood":initialization_before,\n                "initialization_analytic_after_likelihood":initialization_after,\n                "initialization_qualified":len(initialization_after)==2 and initialization_after==initialization_before,\n')
ast.parse(driver)
put(ROOT/'driver_p3.py',driver)
reversed_driver=driver
for before,after in reversed(changes):
    if after:
        ck('reverse_unique:'+before.splitlines()[0],reversed_driver.count(after)==1)
        reversed_driver=reversed_driver.replace(after,before)
    else:
        marker='                ifo.set_strain_data_from_frequency_domain_strain(d,sampling_frequency=4096,duration=32,start_time=999999984.)\n'
        ck('reverse_PSD_location',reversed_driver.count(marker)==1)
        reversed_driver=reversed_driver.replace(marker,before+marker)
ck('only_declared_driver_delta',reversed_driver.encode('utf-8')==(OLD/'driver_p3.py').read_bytes())
diff=''.join(difflib.unified_diff((OLD/'driver_p3.py').read_text(encoding='utf-8').splitlines(True),driver.splitlines(True),fromfile='frozen_p3_codec_002/driver_p3.py',tofile='p3_init_qualified_003/driver_p3.py'))
put(ROOT/'DELTA_DRIVER_VS_CODEC002.patch',diff)

c=copy.deepcopy(old)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
c.update(id='ORDEM018_F3_P3_INIT_QUALIFIED_003',created_utc=now,revised_utc=now,
    authorization_scope='ROOT authorized only this separate preparation after initialization-only pass seq465. No execution permission: independent review and matching explicit ROOT receipt still required.',
    execution_directory='EXECUTION_INIT_QUALIFIED_003',
    revision='Only qualified factory B, exact installed ASD dependency, unchanged helper and analytic-PSD checks/receipt; separate job identities; all science and resource limits unchanged.')
for j,newid in zip(c['jobs'],['P3_GR_INIT_QUALIFIED_003','P3_RB_INIT_QUALIFIED_003']):j['id']=newid
c['coordination_receipt_required']['jobs']=[j['id'] for j in c['jobs']]
c['isolation']['python_read_allowlist']='Same exact 1162 runtime files and synthetic/source pins, plus the one hash-pinned installed ASD demanded by official H1/L1 factory. No directory wildcard. Qualification metadata are exact pinned inputs.'
c['isolation']['writes']='This execution/job output tree only after hook; unchanged supervisor only fixed EXECUTION_INIT_QUALIFIED_003 tree.'
c['allowed_status_claim']='REAL preparation, input/runtime hashes and earlier initialization-only pass; OPEN this campaign execution/recovery/cost of PE/coverage/D.'
c['derived_from_failed_CODEC002']={'contract':info(OLD/'CONTRATO_P3.json'),'terminal_receipt':info(OLD/'RECIBO_EXECUCAO_P3_CODEC_002.json'),'old_jobs':[j['id'] for j in old['jobs']],'old_jobs_reopened':False,'old_files_unchanged':True}
c['qualified_initialization']={'map_sequence':465,'alternative':'B','result':info(INIT/'CONTROL_INIT_001/RESULT.json'),'manifest':info(INIT/'MANIFESTO_RESULTADO_INIT.json'),
    'helper':'init_detectors.py','geometry':'GEOMETRIA_PINADA.json','dependency':'DEPENDENCIA_FACTORY_PIN.json',
    'dependency_scope':'Exact default ASD is initialization-only; replaced by qualified analytic NPZ PSD before likelihood construction and rechecked afterward.',
    'control_zero_blocks_transported':False,'no_monkeypatch':True,
    'source_signature_policy':'Unchanged adapter: generator constructor binds original synthetic_only220 and computes source_parameter_keys before the unchanged FailureAudit wrapper is assigned. No compatibility shim.',
    'dynamic_boundary':'Previous control evaluated no waveform/likelihood/sampler. This package has not been executed; initial sampling and prior-dependent waveform validity remain unmeasured.',
    'execution_permission':False}
extra=['init_detectors.py','GEOMETRIA_PINADA.json','DEPENDENCIA_FACTORY_PIN.json','sources/gw/detector/noise_curves/aLIGO_O4_high_asd.txt','../p3_init_preparation/CONTRATO_CONTROLE_INIT.json','../p3_init_preparation/CONTROL_INIT_001/RESULT.json','../p3_init_preparation/MANIFESTO_RESULTADO_INIT.json']
for rel in list(c['inputs'])+extra:c['inputs'][rel]=pin((ROOT/rel).resolve())
js(ROOT/'CONTRATO_P3.json',c)
contract_sha=pin(ROOT/'CONTRATO_P3.json')['sha256']
cmd=json.loads((OLD/'COMANDO_EXATO_NAO_EXECUTADO.json').read_bytes())
cmd['argv'][-2]=cmd['argv'][-2].replace('/p3_codec_002/','/p3_init_qualified_003/')
cmd['argv'][-1]=contract_sha
cmd['requires']='Independent review and explicit matching ROOT authorization, absent. Do not execute this proposed command during preparation.'
js(ROOT/'COMANDO_EXATO_NAO_EXECUTADO.json',cmd)

unchanged_keys=['purpose','hypothesis','free_parameters','fixed_parameters','priors','mass_prior_normalization','grid','geometry','detectors','analytic_psd','qualified_arrays','qualified_result','data_rule','noise','sampler','limits','stop_rules','convergence','cost','failure_receipt_policy','codec_preload']
for key in unchanged_keys:ck('same_science_contract:'+key,c[key]==old[key])
for j,prior in zip(c['jobs'],old['jobs']):ck('same_job_except_id:'+j['id'],{k:v for k,v in j.items() if k!='id'}=={k:v for k,v in prior.items() if k!='id'})
ck('supervisor_bytes_unchanged',(ROOT/'launch_p3.py').read_bytes()==(OLD/'launch_p3.py').read_bytes())
ck('new_ids_disjoint',not ({j['id'] for j in c['jobs']}&{j['id'] for j in old['jobs']}))
ck('all_old_inputs_unchanged',all(pin((OLD/rel).resolve())==expected for rel,expected in old['inputs'].items()))
ck('qualification_all_unchanged',all(info(Path(e['path']))==e for e in qualified['files']))
ck('no_execution_or_permission_artifacts',not any((ROOT/n).exists() for n in ['AUTORIZACAO_COORDENACAO.json','CLAIM.json',c['execution_directory']]))
for f in ROOT.rglob('*.py'):ast.parse(f.read_bytes().decode('utf-8'))
ck('all_code_parses_no_execution',True)
js(ROOT/'COPIAS_EXATAS.json',{'copies':copies})
js(ROOT/'COMPARACAO_ESCOPO.json',{'status':'SCIENCE_AND_LIMITS_IDENTICAL','same_contract_fields':unchanged_keys,'jobs_only_id_changed':True,'driver_change_count':len(changes),'supervisor_byte_identical':True,'qualified_helper_byte_identical':True,'old_source_adapter_priors_failure_codec_byte_identical':True,'initialization_control_blocks_copied':False,'new_ASD_exact_pin':json.loads((ROOT/'DEPENDENCIA_FACTORY_PIN.json').read_bytes()),'differences_not_scientific':['new IDs and provenance','factory B with exact ASD initialization dependency','analytic PSD and stored strain checks','initialization receipt fields']})
put(ROOT/'DELTA_CONTRATO_VS_CODEC002.patch',''.join(difflib.unified_diff((OLD/'CONTRATO_P3.json').read_text(encoding='utf-8').splitlines(True),(ROOT/'CONTRATO_P3.json').read_text(encoding='utf-8').splitlines(True),fromfile='frozen_p3_codec_002/CONTRATO_P3.json',tofile='p3_init_qualified_003/CONTRATO_P3.json')))
js(ROOT/'RECIBO_PREPARACAO_INIT003.json',{'status':'PREPARATION_ONLY_PASS','checks':checks,'n_checks':len(checks),'all_passed':all(x['passed'] for x in checks),'at':now,'wall_s':time.perf_counter()-start,'CPU_s':time.process_time()-cpu,'contract':info(ROOT/'CONTRATO_P3.json'),'scientific_modules_imported':False,'PE_jobs':0,'waveforms':0,'D_read':False,'old_packages_unchanged':True,'execution_authorized':False})
print(json.dumps({'contract':info(ROOT/'CONTRATO_P3.json'),'checks':len(checks),'driver':info(ROOT/'driver_p3.py'),'inputs':len(c['inputs'])}))
