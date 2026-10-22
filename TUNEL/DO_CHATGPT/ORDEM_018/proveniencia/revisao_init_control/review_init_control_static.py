"""Static, read/hash/AST-only review; does not import or execute the author package."""
from pathlib import Path
import ast, hashlib, json, sys
from datetime import datetime, timezone
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent))
from audit_provenance import atomic, metadata
ROOT=OUT.parents[1]
PKG=ROOT/'preregistros/conjunto_d/p3_init_preparation'
checks=[]; sources={}
def read(path):
    path=Path(path).resolve();m,b=metadata(path);sources[str(path)]=m;return b
def jsread(path):return json.loads(read(path))
def check(name,ok,detail=None):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
    if not ok: raise AssertionError(name)
def pin(path,row,label):
    b=read(path);check(label,len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'])
manifest=jsread(PKG/'MANIFESTO_PREPARACAO_INIT.json')
contract=jsread(PKG/'CONTRATO_CONTROLE_INIT.json')
for row in manifest['files']:
    pin(row['path'],row,'manifest:'+row['relative_path'])
check('manifest_count',len(manifest['files'])==manifest['file_count']==31)
for rel,row in contract['inputs'].items():pin(PKG/rel,row,'input:'+rel)
check('inputs_count',len(contract['inputs'])==24)
runtime=jsread(PKG/'../p3_codec_002/RUNTIME_P3_READONLY.json')
runtime_index={r['path']:r for r in runtime['files']}
check('runtime_manifest_count',len(runtime_index)==len(runtime['files'])==1162)
extra=[]
for row in contract['runtime_initialization_dependencies']:
    pin(PKG/row['local_path'],row,'snapshot:'+row['local_path'])
    if row['runtime_path'] not in runtime_index:extra.append(row)
    else:
        old=runtime_index[row['runtime_path']]
        check('runtime_overlap:'+row['local_path'],(old['sha256'],old['bytes'])==(row['sha256'],row['bytes']))
check('exact_one_extra_dependency',extra==contract['new_exact_runtime_read'] and len(extra)==1)
check('extra_is_ASD',extra[0]['runtime_path'].endswith('/noise_curves/aLIGO_O4_high_asd.txt'))
check('source_snapshot_count',len(contract['runtime_initialization_dependencies'])==16)
dependency=jsread(PKG/'DEPENDENCIA_FACTORY_PIN.json')
check('dependency_pin_matches_contract',dependency==extra[0])
for key in ['base_scientific_contract','base_failure']:pin(contract[key]['path'],contract[key],key)
command=jsread(PKG/'COMANDO_CONTROLE_NAO_EXECUTADO.json')
check('command_contract_hash',command['argv'][-1]==hashlib.sha256(read(PKG/'CONTRATO_CONTROLE_INIT.json')).hexdigest())
check('contract_is_B_preparation',contract['selected_alternative']=='B' and contract['state']=='PREPARED_NOT_EXECUTED' and contract['execution_permission'] is False)
for n in ['CONTROL_INIT_001','DECISAO_CONTROLE_INIT.json','CLAIM.json','AUTORIZACAO_COORDENACAO.json']:
    check('absent:'+n,not (PKG/n).exists())
control=read(PKG/'control_init.py').decode('utf-8')
helper=read(PKG/'init_detectors.py').decode('utf-8')
tree=ast.parse(control);ast.parse(helper)
check('static_syntax',True,'AST parse only; no compile/exec/import of author package.')
scientific_classes={}
for name,cls,methods in [
 ('sources/gw/waveform_generator.py','WaveformGenerator',('frequency_domain_strain','time_domain_strain','_calculate_strain','_strain_from_model','_strain_from_transformed_model')),
 ('sources/gw/likelihood/base.py','GravitationalWaveTransient',('log_likelihood','log_likelihood_ratio','noise_log_likelihood','_calculate_noise_log_likelihood','calculate_snrs'))]:
    t=ast.parse(read(PKG/name).decode('utf-8'))
    c=next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name==cls)
    found={n.name:n.lineno for n in c.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    for m in methods:check('guard_target_exists:'+cls+'.'+m,m in found)
    scientific_classes[cls]={m:found[m] for m in methods}
imports=[]
for n in ast.walk(tree):
    if isinstance(n,ast.Import):imports += [a.name for a in n.names]
    if isinstance(n,ast.ImportFrom):imports.append(n.module)
check('no_direct_dynesty_import',not any(x and x.split('.')[0]=='dynesty' for x in imports))
# Save selected source slices; this is documentary evidence, not executing expressions.
ranges={
 'control_init.py':[(24,63),(78,106),(108,171)],
 'init_detectors.py':[(24,69)],
 'COMANDO_CONTROLE_NAO_EXECUTADO.json':[(1,20)],
 'sources/gw/likelihood/base.py':[(145,222)],
 'sources/gw/waveform_generator.py':[(62,79),(244,262)],
 'sources/gw/detector/networks.py':[(27,39),(440,474)],
 'sources/gw/detector/psd.py':[(49,63),(210,226),(234,247),(297,332)]
}
excerpts=[]
for name,rs in ranges.items():
    lines=read(PKG/name).decode('utf-8').splitlines()
    excerpts.extend({'path':str(PKG/name),'first':lo,'last':min(hi,len(lines)),
                     'text':'\n'.join(lines[lo-1:hi])} for lo,hi in rs)
# Immutable snapshots of central material being reviewed.
snap=OUT/'snapshot_457';snap.mkdir(exist_ok=True)
for name in ['MANIFESTO_PREPARACAO_INIT.json','CONTRATO_CONTROLE_INIT.json','control_init.py','init_detectors.py','COMANDO_CONTROLE_NAO_EXECUTADO.json','NOTA_ALTERNATIVAS_E_CONTROLE_INIT.md']:
    dest=snap/name
    raw=read(PKG/name)
    if dest.exists():check('snapshot_preserved:'+name,dest.read_bytes()==raw)
    else:atomic(dest,raw)
finding={
 'id':'INIT-01','priority':'P2','status':'OPEN_BEFORE_EXECUTION',
 'title':'Comando direto sem supervisor externo não garante teto de parede e recibo terminal',
 'locations':[{'file':'COMANDO_CONTROLE_NAO_EXECUTADO.json','lines':[3,16]},
              {'file':'control_init.py','lines':[37,53]},
              {'file':'control_init.py','lines':[162,170]}],
 'evidence':'argv inicia diretamente control_init.py. Os pins e STARTED precedem setitimer; o handler Python não é watchdog externo. RLIMIT_CPU hard protege CPU, não espera/I/O. Um encerramento duro também pode impedir RESULT no finally.',
 'impact':'Os 60 s não abrangem todo o processo e podem ser ultrapassados em bloqueio sem CPU; inexistência de RESULT precisa de recibo externo e não autoriza retry.',
 'correction':'Supervisor aditivo próprio, pinado e sujeito a decisão específica: deadline desde entrada/launch, timeout monotônico externo, kill do grupo de processos e recibo externo de exit/signal/timeout inclusive pré-RESULT. Sem CLAIM científico ou novo P3; preservar pacote457.'}
receipt={
 'status':'STATIC_REVIEW_ONE_P2_NO_CONTROL_EXECUTED',
 'created_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'chatgpt-codex/ordem-018/proveniencia',
 'scope':'Documentary/hash/AST only. No execution/import of control, no WSL process, no network, no array deserialization, real D, waveform, likelihood or PE.',
 'checks_count':len(checks),'checks':checks,'findings':[finding],
 'exact_new_runtime_dependency':extra,'overlap_with_runtime_manifest':15,
 'runtime_installed_files_rehashed_in_this_review':False,
 'runtime_limit':'Local snapshots rehashed and compared to frozen runtime manifest. Actual installed WSL paths are to be rehashed by an authorized control; no fresh installation verification claimed.',
 'guard_targets_in_pinned_sources':scientific_classes,
 'execution_evidence':'No control output, decision or CLAIM present at static check. Future zero counters are required conditions, not observed dynamic qualification.',
 'sources':list(sources.values()),'excerpts':excerpts,
 'originals_modified':False,'upstream_executed':False,'control_executed':False,'D_read':False}
atomic(OUT/'REVISAO_INIT_CONTROL_RECIBO.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'checks':len(checks),'sources':len(sources),'new_runtime_paths':[x['runtime_path'] for x in extra],'finding':finding},ensure_ascii=False,indent=2))
