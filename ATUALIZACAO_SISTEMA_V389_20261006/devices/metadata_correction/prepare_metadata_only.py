"""Prepare only the 16 FINAL metadata corrections, no imports/device execution."""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
C=Path(r'C:\IALD\Central de Patentes')
W=C/'Chatgpt/ATUALIZACAO_SISTEMA_V389_20261006/devices'
D=W/'metadata_correction'
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists(): raise FileExistsError(p)
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
 assert t.read_bytes()==b
 os.replace(t,p); assert p.read_bytes()==b
 return pin(p)
def js(p,d): return write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
identity=json.loads((W/'IDENTIDADE_ESTAGIO.json').read_bytes())
recon=json.loads((W/'RECONCILIACAO_PRODUCAO_V389.json').read_bytes())
assert len(recon['devices'])==16
entries=[]; checks=[]
for row in recon['devices']:
 target=Path(row['manifest']['path']); final=Path(row['FINAL']['path'])
 raw=target.read_bytes(); fb=final.read_bytes()
 assert sha(raw)==row['manifest']['sha256'] and sha(fb)==row['FINAL']['sha256']
 before=json.loads(raw); assert 'final_sha256' not in before
 pattern=rb'(?P<indent>[ \t]*)"final_bytes"[ \t]*:[ \t]*(?P<n>[0-9]+)(?P<comma>,)(?P<eol>\r*\n)'
 matches=list(re.finditer(pattern,raw)); assert len(matches)==1
 m=matches[0]; assert int(m['n'])==before['final_bytes']
 replacement=(m['indent']+b'"final_bytes": '+str(len(fb)).encode()+b','+m['eol']+m['indent']+b'"final_sha256": "'+sha(fb).encode()+b'",'+m['eol'])
 new=raw[:m.start()]+replacement+raw[m.end():]
 after=json.loads(new); assert after==dict(before,final_bytes=len(fb),final_sha256=sha(fb))
 # Preserve all other bytes, including the existing CRCRLF serialization.
 assert new.replace(replacement,raw[m.start():m.end()],1)==raw
 rel=target.relative_to(C/'patents'); base=D/'baseline'/rel; stage=D/'stage'/rel
 bp=write(base,raw); ap=write(stage,new)
 entries.append({'target':str(target),'baseline':str(base.relative_to(D)),'stage':str(stage.relative_to(D)),'before':pin(target),'after':ap,'final':pin(final),'backup_on_apply':str(target.with_name(target.name+'.bak_v389_metadata_'+identity['stage_id'])),'field_delta':{'final_bytes':{'before':before['final_bytes'],'after':len(fb)},'final_sha256':{'before':'ABSENT','after':sha(fb)}}})
 checks.append({'device':row['device'],'only_two_fields_changed':True,'other_bytes_identical':True,'FINAL_unchanged_since_reconciliation':True,'size_difference':len(fb)-before['final_bytes']})
V=C/'vault/originals_copy/um_unificado_v389'; sealpath=V/'um_absoluto_selo.json'; seal=json.loads(sealpath.read_bytes())
exam=[]
for role,source in seal['text_label_errata_v389']['files'].items():
 name=Path(source['path']).name
 archived=V/'cadeia_de_selo_v387_v389/v389_exame_v388'/name
 staged=W/'stage/vault/originals_copy/um_unificado_v389/exame_v388'/name
 a=pin(archived); b=pin(staged)
 assert a['sha256']==b['sha256']==source['sha256']
 exam.append({'role':role,'seal_declared_original_path':source['path'],'seal_expected_sha256':source['sha256'],'existing_custody':a,'own_stage':b,'equal':True,'classification':'PRESENT_AT_EXISTING_CHAIN_PATH_NOT_MISSING'})
audit=W.parent/'science_audit/controller_static_20261006/MANIFESTO_AUDITORIA.json'
auditdata=json.loads(audit.read_bytes()); auditchecks=[]
for item in auditdata['files']:
 observed=pin(Path(item['path'])); assert observed['bytes']==item['bytes'] and observed['sha256']==item['sha256']; auditchecks.append(observed)
js(D/'RECONCILIACAO_EXAME_ERRATA.json',{'status':'THREE_PRESENT_IN_EXISTING_CUSTODY','seal':pin(sealpath),'items':exam,'scope':'Bytes/hash only; no scientific execution or new custody copy required','independent_audit_manifest':pin(audit),'audit_members_verified':auditchecks})
guards=[pin(V/'CUSTODY_MANIFEST.json'),pin(sealpath),pin(C/'patents/_formula_completa/tgl_formula_completa.py')]+[x['existing_custody'] for x in exam]
plan={'schema':'V389_FINAL_METADATA_CORRECTION_PLAN_V1','stage_id':identity['stage_id'],'action':'CORRECT_16_FINAL_METADATA_ONLY','status':'PREPARED_NOT_APPLIED','scope':'Only final_bytes and final_sha256; no FINAL, ZIP, layer, runner, custody or publication mutation','entries':entries,'installer':pin(D/'apply_metadata_only.py'),'read_only_guards':guards,'authority':'Separate ROOT decision required; this plan supplies no approval','concurrency':'Preflight plus immediate CAS; no global filesystem transaction. A concurrent uncooperative writer can race after the final check. Failure leaves lock/receipt/backups; do not auto-retry.','aggregate_manifest_followup':'No hash hit in inspected current v389 seal-work/custody JSONs. Historical receipts retain before-pins. New applied receipt provides after-pins without changing sealed history. Inspection scope explicitly bounded.'}
js(D/'PLAN.json',plan)
ast.parse((D/'apply_metadata_only.py').read_bytes())
js(D/'STATIC_CHECKS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'16_DELTAS_AND_THREE_ARCHIVE_PINS_VERIFIED','checks':checks,'installer_AST':'PASS','installer_executed':False,'science_executed':False,'production_modified':False,'tests_added':False})
js(W/'DISPOSICAO_ESTAGIO_CONCORRENTE.json',{'status':'EARLIER_CUSTODY_AND_LAYER_STAGE_SUPERSEDED_DO_NOT_INSTALL','stage_id':identity['stage_id'],'reason':'Concurrent v389 production custody/layer/FINALs already installed. Reconciliation preserves all live additional opaque members. Only metadata_correction/PLAN.json is the current proposed change.','retained_for_history':['stage','baseline','prepare_custody_layer.py','repackage_stage.py','RECIBO_DRIFT_BASELINE.json','RECONCILIACAO_PRODUCAO_V389.json'],'production_modified_by_this_task':False,'full_reinstallation_forbidden_by_this_disposition':True})
print(json.dumps({'status':'PREPARED','plan':pin(D/'PLAN.json'),'reconciled_exam':len(exam),'metadata_entries':len(entries),'production_modified':False}))
