from pathlib import Path
import os,json,hashlib,datetime,ast,difflib
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_calibration_bound\controls_preparation')
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
backups=[]
def atomic(p,data):
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
  assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
  backups.append({'original':str(p),'backup':pin(bak)})
 t=p.with_name(p.name+'.tmp_'+stamp);assert not t.exists();t.write_bytes(data);assert t.read_bytes()==data;os.replace(t,p)
 assert p.read_bytes()==data
def js(p,obj):atomic(p,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
assert all(not (B/x).exists() for x in ('CLAIM.json','RUN','AUTORIZACAO_ROOT.json'))
oldworker=(B/'controls.py').read_text();oldsuper=(B/'supervisor.py').read_text();oldcontract=json.loads((B/'PROTOCOLO_EXATO.json').read_bytes())
original_parent_pins=oldcontract['source_pins']
old_contract_pin=pin(B/'PROTOCOLO_EXATO.json')
newworker=oldworker.replace('time.monotonic() - START > 28','time.monotonic() - START > 23')
assert newworker!=oldworker and newworker.replace('time.monotonic() - START > 23','time.monotonic() - START > 28')==oldworker
newsuper=(B/'supervisor_v2_candidate.txt').read_text()
for text in (newworker,newsuper):ast.parse(text)
oldfunc={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(oldworker).body if isinstance(n,ast.FunctionDef)}
newfunc={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(newworker).body if isinstance(n,ast.FunctionDef)}
assert set(oldfunc)==set(newfunc)
assert all(oldfunc[k]==newfunc[k] for k in oldfunc if k!='budget')
atomic(B/'controls.py',newworker.encode())
atomic(B/'supervisor.py',newsuper.encode())
c=json.loads(json.dumps(oldcontract))
c['operational_revision']=2
c['limits']['cooperative_worker_seconds']=23
del c['limits']['post_kill_cleanup_seconds_max']
c['limits']['collection_reserve_seconds_within_total']=5
c['limits']['work_deadline_offset_seconds']=25
c['limits']['extra_wait_budget_after_total_seconds']=0
c['identity_policy']['wall']='Single monotonic nominal total deadline30s starts after exclusive CLAIM persistence, before environment setup/Popen; pin/auth prevalidation and identity persistence precede it. Work deadline=total-5s, worker cooperative<=23s. Collection communicates only for remaining total time. No fresh/additional5s. OS scheduling/kill/write timing not guaranteed; terminal uncertainty is persisted immediately even if nominal deadline has elapsed.'
c['identity_policy']['collection_failure']='TimeoutExpired or other collection failure is caught and yields terminal PROCESS_STATE_UNCERTAIN, exit2, no PASS/retry. Receipt write is an immediate persistence attempt, not added wait/computation budget.'
for entry in c['execution_pins']:
 if Path(entry['path']).name in ('controls.py','supervisor.py'):entry.update(pin(Path(entry['path'])))
assert c['cases']==oldcontract['cases'] and c['request_id']==oldcontract['request_id']
js(B/'PROTOCOLO_EXATO.json',c)
identity=json.loads((B/'IDENTIDADE_PREPARADA.json').read_bytes());identity['contract']=pin(B/'PROTOCOLO_EXATO.json');identity['operational_revision']=2
js(B/'IDENTIDADE_PREPARADA.json',identity)
note=(B/'NOTA_PREPARACAO_CONTROLES.md').read_text()
old='Teto de30s de processamento, parada cooperativa aos28s, kill no prazo e até5s adicionais apenas para recolher processo morto.'
new='Orçamento operacional nominal TOTAL de30s, iniciado após persistir CLAIM e antes do ambiente/Popen; pré-validação de pins/autorização e identidade ficam antes. Deadline de trabalho em25s e cooperativo em23s; os5s de recolhimento estão reservados DENTRO dos30s, sem prazo adicional. Timeout/erro de recolhimento persiste PROCESS_STATE_UNCERTAIN, sem PASS/retry. Tempo de agendamento/kill/escrita não é garantia do sistema operacional.'
assert old in note;note=note.replace(old,new)
note+='\n\nAdendo operacional V2: somente deadlines e captura terminal do recolhimento foram alterados, na mesma identidade ainda não consumida. Os oito casos, suas contas e resultados esperados estão intactos. A preparação antiga não foi reexecutada. Diferenças, backups de bytes e AST constam em DELTA_OPERACIONAL_V2.json e RECIBO_DELTA_V2_AST_PINS.json. Zero controles executados.\n'
atomic(B/'NOTA_PREPARACAO_CONTROLES.md',note.encode())
diff=''.join(difflib.unified_diff(oldworker.splitlines(True),newworker.splitlines(True),fromfile='controls.py.pre_v2',tofile='controls.py.v2'))
diff+=''.join(difflib.unified_diff(oldsuper.splitlines(True),newsuper.splitlines(True),fromfile='supervisor.py.pre_v2',tofile='supervisor.py.v2'))
atomic(B/'DELTA_OPERACIONAL_V2.diff',diff.encode())
tree=ast.parse(newsuper)
communicates=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='communicate']
checks=[
 {'check':'exactly2communicate calls both use remaining not fresh timeout','pass':len(communicates)==2 and all(any(k.arg=='timeout' and isinstance(k.value,ast.Name) and k.value.id=='remaining' for k in n.keywords) for n in communicates)},
 {'check':'single total deadline plus30 and work total minus5','pass':'deadline_total=started+30' in newsuper and 'deadline_work=deadline_total-5' in newsuper},
 {'check':'worker cooperative23 only code change','pass':newworker.replace('time.monotonic() - START > 23','time.monotonic() - START > 28')==oldworker},
 {'check':'all8case ASTs unchanged','pass':all(oldfunc[k]==newfunc[k] for k in oldfunc if k.startswith('C0'))},
 {'check':'mathematical helpers unchanged','pass':all(oldfunc[k]==newfunc[k] for k in oldfunc if k!='budget')},
 {'check':'protocol8cases unchanged','pass':c['cases']==oldcontract['cases']},
 {'check':'same request_id','pass':c['request_id']==oldcontract['request_id']},
 {'check':'cleanup TimeoutExpired captured','pass':'except subprocess.TimeoutExpired as exc:' in newsuper and 'COLLECTION_TIMEOUT_PROCESS_STATE_UNCERTAIN' in newsuper},
 {'check':'uncertain terminal status and exit2','pass':'status="PROCESS_STATE_UNCERTAIN"' in newsuper and '2 if status=="PROCESS_STATE_UNCERTAIN"' in newsuper},
 {'check':'no additional cleanup budget','pass':c['limits']['extra_wait_budget_after_total_seconds']==0 and 'timeout=5' not in newsuper},
 {'check':'source parents unchanged','pass':all(pin(Path(r['path']))==r for r in original_parent_pins)},
 {'check':'zero authorization claim or run','pass':all(not (B/x).exists() for x in ('CLAIM.json','RUN','AUTORIZACAO_ROOT.json'))},
 {'check':'two ASTs parse only','pass':True}]
assert all(q['pass'] for q in checks)
js(B/'RECIBO_DELTA_V2_AST_PINS.json',{'status':'PASS_STATIC_ONLY','request_id':c['request_id'],'checks':checks,'count':len(checks),'controls_executed':0,'modules_imported_or_executed':[],'contract_pin':pin(B/'PROTOCOLO_EXATO.json'),'runtime_or_scientific_benchmark':False})
js(B/'DELTA_OPERACIONAL_V2.json',{'request_id':c['request_id'],'scope':'Operational deadline only; same unconsumed identity; no scientific execution','old_contract_sha256':old_contract_pin['sha256'],'new_contract':pin(B/'PROTOCOLO_EXATO.json'),'backups':backups,'AST_checks':13,'math_cases_and_numerical_limits_unchanged':True,'authorization_granted':False})
# Back up the existing manifest before calculating the new inventory.
manifest_path=B/'MANIFESTO_PREPARACAO.json';oldmanifest=manifest_path.read_bytes()
bak=manifest_path.with_name(manifest_path.name+'.bak_'+stamp);assert not bak.exists();bak.write_bytes(oldmanifest);assert bak.read_bytes()==oldmanifest
files=[pin(p) for p in sorted(B.iterdir()) if p.is_file() and '.bak_' not in p.name and p.name!='MANIFESTO_PREPARACAO.json']
manifest={'request_id':c['request_id'],'status':'PREPARED_ONLY_ZERO_CONTROL_EXECUTIONS','operational_revision':2,'files':files,'source_pins':original_parent_pins,'backups':backups+[{'original':str(manifest_path),'backup':pin(bak)}],'next':'ROOT review and explicit authorization of exact revised contract; no controls executed.'}
data=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode();temp=manifest_path.with_name(manifest_path.name+'.tmp_'+stamp);temp.write_bytes(data);assert temp.read_bytes()==data;os.replace(temp,manifest_path)
print(json.dumps({'manifest':pin(manifest_path),'contract':pin(B/'PROTOCOLO_EXATO.json'),'worker':pin(B/'controls.py'),'supervisor':pin(B/'supervisor.py'),'checks':len(checks),'backup_count':len(backups)+1},ensure_ascii=False))
