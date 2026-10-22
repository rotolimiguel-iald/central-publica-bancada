from pathlib import Path
import json,hashlib,ast,datetime,os,copy
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018')
BASE=ROOT/'preregistros/conjunto_d/audit_guard_repair_preparation'
OLD=ROOT/'preregistros/conjunto_d/p3_init_qualified_003'
OUT=ROOT/'preregistros/conjunto_d/revisao_audit_guard_repair'
OUT.mkdir(exist_ok=True)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(name,obj):
 p=OUT/name;assert not p.exists()
 b=obj.encode() if isinstance(obj,str) else (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
 t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def dump(n):return ast.dump(n,include_attributes=False)
def tree(p):return ast.parse(p.read_text(),filename=str(p))
def funcs(t):return {n.name:n for n in ast.walk(t) if isinstance(n,ast.FunctionDef)}
checks=[]
def check(name,condition,evidence=None):checks.append(dict(name=name,pass_check=bool(condition),evidence=evidence))
m=json.loads((BASE/'MANIFESTO_PREPARACAO.json').read_bytes())
for r in m['files']:
 q=Path(r['path']);d=pin(q);check('manifest pin '+str(q.relative_to(BASE)),d['bytes']==r['bytes'] and d['sha256']==r['sha256'],d)
source=json.loads((BASE/'SOURCES_BASELINE.json').read_bytes())
for r in source['originals']:
 q=Path(r['path']);d=pin(q);check('INIT003 preserved '+str(q.relative_to(OLD)),d['bytes']==r['bytes'] and d['sha256']==r['sha256'],d)
check('manifest exactly26files',len(m['files'])==26)
protocol=json.loads((BASE/'PROTOCOL_PREPARATION.json').read_bytes())
contract=json.loads((OLD/'CONTRATO_P3.json').read_bytes())
check('protocol pure preparation',protocol['suite_execution_authorized_by_this_protocol'] is False and protocol['new_scientific_contract_created'] is False and protocol['new_authorization_created'] is False and protocol['new_claim_created'] is False)
asts={}
for rel in ['candidate/audit_guard.py','candidate/result_acceptance.py','candidate/driver_p3.py','candidate/launch_p3.py','candidate/src/pseob_source.py','tests/test_audit_guard_doubles.py']:
 asts[rel]=tree(BASE/rel);check('AST parses '+rel,True)
origsource=tree(OLD/'src/pseob_source.py');newsource=copy.deepcopy(asts['candidate/src/pseob_source.py'])
class RemoveAudit(ast.NodeTransformer):
 def visit_FunctionDef(self,node):
  if node.name in ('set_audit_checkpoint','audit_checkpoint'):return None
  return self.generic_visit(node)
 def visit_Assign(self,node):
  if any(isinstance(t,ast.Name) and t.id=='AUDIT_CHECKPOINT' for t in node.targets):return None
  return self.generic_visit(node)
 def visit_Expr(self,node):
  if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='audit_checkpoint':return None
  return self.generic_visit(node)
normalized=RemoveAudit().visit(newsource)
check('whole scientific source AST unchanged after ONLY audit removal',dump(normalized)==dump(origsource))
newf=funcs(asts['candidate/src/pseob_source.py']);oldf=funcs(origsource)
for name in oldf:check('source signature '+name,dump(oldf[name].args)==dump(newf[name].args))
driver=asts['candidate/driver_p3.py'];olddriver=tree(OLD/'driver_p3.py')
def fncalls(t,name):
 return sorted(dump(n) for n in ast.walk(t) if isinstance(n,ast.Call) and ast.unparse(n.func)==name)
scientific=['np.load','np.array','np.fft.rfftfreq','np.isfinite','np.isinf','np.any','np.sum','np.array_equal','np.isclose','math.sqrt','build_B','verify_analytic_state','generator','failures.wrap','bilby.gw.likelihood.GravitationalWaveTransient','parameters','likelihood.log_likelihood_ratio','np.random.default_rng','dynesty.NestedSampler','sampler.sample','sampler.add_live_points','compute_integrals','np.logaddexp','np.max','np.ptp','np.exp','np.asarray','np.savez','resource.setrlimit','signal.setitimer']
for name in scientific:check('driver call AST unchanged '+name,fncalls(driver,name)==fncalls(olddriver,name),{'occurrences':len(fncalls(driver,name))})
dfa,ofa=funcs(driver),funcs(olddriver)
for name in ('audit',):
 tests=lambda n:[dump(x.test) for x in ast.walk(n) if isinstance(x,ast.If)]
 check('all hook allow/deny predicates unchanged',tests(dfa[name])==tests(ofa[name]))
def allow_nodes(t):
 ans=[]
 for n in ast.walk(t):
  if isinstance(n,(ast.Assign,ast.AugAssign)):
   targets=n.targets if isinstance(n,ast.Assign) else [n.target]
   if any(isinstance(x,ast.Name) and x.id in ('allowed_data','runtime_paths','init_dependency') for x in targets):ans.append(dump(n))
  if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='allowed_data.add':ans.append(dump(n))
 return ans
check('full allowlist construction unchanged',allow_nodes(driver)==allow_nodes(olddriver))
for name in ('main',):
 for t,label in [(driver,'driver'),(asts['candidate/launch_p3.py'],'supervisor')]:
  first=funcs(t)[name].body[0]
  check(label+' refuses preparation before main work',isinstance(first,ast.Raise) and 'PREPARATION_ONLY' in ast.unparse(first))
oldlaunch=tree(OLD/'launch_p3.py');newlaunch=asts['candidate/launch_p3.py']
for name in ('subprocess.Popen','p.wait','os.killpg'):
 check('supervisor inherited process/limit call unchanged '+name,fncalls(oldlaunch,name)==fncalls(newlaunch,name))
for key,value in protocol['baseline_limits_preserved'].items():
 if key in contract['limits']:check('limit preserved '+key,contract['limits'][key]==value,{'value':value})
testnames=[n.name for n in ast.walk(asts['tests/test_audit_guard_doubles.py']) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
check('21test names exact protocol order',len(testnames)==21 and testnames==protocol['prepared_only_test_names'])
for rel,allowed in [('candidate/audit_guard.py',{'copy','json','os','threading','time'}),('candidate/result_acceptance.py',{'hashlib'}),('tests/test_audit_guard_doubles.py',{'pathlib','copy','hashlib','json','sys','unittest','audit_guard','result_acceptance'})]:
 imports=[]
 for n in ast.walk(asts[rel]):
  if isinstance(n,ast.Import):imports.extend(x.name for x in n.names)
  elif isinstance(n,ast.ImportFrom):imports.append(n.module)
 check(rel+' pure imports only',set(imports)<=allowed,imports)
guard=(BASE/'candidate/audit_guard.py').read_text()
check('latch set before event serialization',guard.index('self._latched = True')<guard.index('self._writer((json.dumps(row'))
check('denial counter before journal',guard.index('self._denial_count += 1')<guard.index('self._writer((json.dumps(row'))
check('exclusive preopened journal with full-write loop/fsync','os.O_EXCL' in guard and 'while view:' in guard and 'view = view[n:]' in guard and 'os.fsync(self.fd)' in guard)
check('snapshot copied and no reset API','return copy.deepcopy' in guard and not any(n.name in ('reset','clear','truncate') for n in ast.walk(asts['candidate/audit_guard.py']) if isinstance(n,ast.FunctionDef)))
dr=(BASE/'candidate/driver_p3.py').read_text();src=(BASE/'candidate/src/pseob_source.py').read_text();launch=(BASE/'candidate/launch_p3.py').read_text();accept=(BASE/'candidate/result_acceptance.py').read_text()
for phase in ('pre_likelihood','initialization_ready','sampler_returned','final_before_diagnostics','final_before_result','final_after_result'):
 check('driver checkpoint '+phase,'checkpoint("'+phase+'")' in dr)
check('source after imports before temporal and waveform',src.index('audit_checkpoint("source_after_imports")')<src.index('validate_time_contract(mass_1')<src.index('audit_checkpoint("source_before_waveform")')<src.index('result=lal_binary_black_hole'))
check('source waveform finally checkpoint after counter',src.index('COST_COUNTER[0]+=1')<src.index('audit_checkpoint("source_after_waveform")'))
check('source callback bound once','if AUDIT_CHECKPOINT is not None:raise' in src and 'source.set_audit_checkpoint(checkpoint)' in dr)
check('supervisor independent journal bytes','journal=jp.read_bytes()' in launch and 'assess(result,journal' in launch)
check('supervisor stops before next job after rejection','if not decision["accepted"]:' in launch and 'break # Terminal' in launch)
check('supervisor returns failure exit','return campaign_exit(assessments,len(c["jobs"]))' in launch and 'sys.exit(main())' in launch)
check('accept requires actual clean journal and clean receipt','isinstance(journal,bytes) and len(journal)==0' in accept and 'result.get("blocked_operations") == []' in accept and 'audit.get("latched") is False' in accept)
check('accept rejects bool counters','return type(value) is int and value >= 0' in accept)
check('accept clean partial distinguished','CLEAN_PARTIAL' in accept and 'CLEAN_CONVERGED' in accept)
check('no candidate run permission/files',not any(p.name in ('AUTORIZACAO_COORDENACAO.json','CONTRATO_P3.json','CLAIM.json') for p in BASE.rglob('*')))
scope={'tests_run':0,'candidate_imports':0,'waveform_calls':0,'likelihood_calls':0,'sampler_calls':0,'D_reads':0,'scientific_array_reads':0,'shared_memory_edits':0,'authorization_edits':0}
manual=[
 {'topic':'Latch and journal','conclusion':'State latched before serialization/IO; first/all events and interrupted original exceptions retained; journal FD exclusive and kept open, full writes/fsync; missing or dirty journal terminal at supervisor. Not immutable against hostile in-process code or native syscalls.'},
 {'topic':'Checkpoints','conclusion':'Pre/post evaluation encloses float conversion and exception paths. Source checkpoint after imports occurs before temporal helper/dict/waveform; finally after native counter ensures denial inside waveform aborts returned value. Cannot interrupt already running C; auxiliary LAL calls are not the waveform counter.'},
 {'topic':'Finalization','conclusion':'AuditViolation overrides budget/partial status; checkpoint before diagnostics/result and after result. A late denied event after receipt invalidates external journal/returncode; no successful continuation solely from stale status.'},
 {'topic':'Supervisor','conclusion':'Validates identity, process return, audit states/journal pin/checkpoint counts, initialization consistency and failure counters; rejects missing/malformed receipts and stops next job; campaign incomplete/nonaccepted returns2.'},
 {'topic':'Limits','conclusion':'Scientific resource/sampler/source calls and declared limits preserved. Inherited3610s initial child wait plus unbounded post-kill wait/IO remains explicitly OPEN, not a new hard wall guarantee.'},
 {'topic':'21 doubles','conclusion':'Nine latch/checkpoint/exception tests, ten result-acceptance tests and two campaign-flow tests are logically aligned with intended defect. Source/native and supervisor process integration are modeled doubles, not invoked. PreopenedJournal actual short-write/fsync and real sys.addaudithook integration are not dynamically exercised; no execution claimed.'}
]
receipt={'status':'DOCUMENTARY_REVIEW_NO_BLOCKING_P2_FOUND_WITHIN_SCOPE','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':scope,
 'checks':checks,'checks_total':len(checks),'checks_passed':sum(q['pass_check'] for q in checks),'prepared_tests_count':len(testnames),'prepared_test_names':testnames,
 'manual_review':manual,'findings':[],'source_manifest':pin(BASE/'MANIFESTO_PREPARACAO.json'),'source_files':m['files'],'baseline_pins':source['originals'],
 'limits':'Static review is not dynamic qualification or execution permission. Integration/testing remains OPEN.'}
assert all(q['pass_check'] for q in checks),[(q['name']) for q in checks if not q['pass_check']]
write('RECIBO_REVISAO_DOCUMENTAL.json',receipt)
note="""# Revisão independente — reparo de audit, preparação

[REAL documental] Revisão estática do pacote audit_guard_repair_preparation, sem executar os 21 testes, importar candidatos ou abrir séries/arrays. Nenhum defeito bloqueante P2+ foi localizado no recorte examinado. Este parecer admite o pacote à decisão posterior da ROOT; não autoriza testes, integração ou PE.

O latch torna a recusa persistente antes da serialização e IO. Preserva primeiro evento, sequência, modo/flags, fase, tempos, contadores e exceção original interrompida. O journal é criado com exclusividade antes do hook, escreve pelo descritor já aberto, trata escritas parciais e faz fsync. Falha de IO conserva o estado sujo; snapshot é cópia. Isso não torna a memória/arquivo imutável contra código hostil, nem confina FDs/syscalls nativas.

A revisão do fluxo confirma checkpoints antes/depois da avaliação e conversão numérica, inclusive exceção; após imports da fonte; antes do helper temporal, dict e waveform; depois da tentativa principal; e na finalização. O callback mantém a assinatura original. Uma recusa absorvida no import não alcança o despacho principal seguinte. Uma recusa ocorrida dentro de C pode ser percebida somente ao retorno; o contador de waveform não inventaria todos os helpers LAL.

A finalização dá prioridade ao audit sobre um rótulo parcial. O supervisor confere o journal real após o retorno do filho, identidade job/label/contrato/PID, exit/status, chamadas, checkpoints, estado de inicialização e falhas de fonte. Recibo limpo anterior não encobre journal sujo posterior. Resultado ausente/malformado, journal ausente/sujo ou filho falho impedem o próximo job e resultam em saída não zero. Parcial limpo permanece CLEAN_PARTIAL, sem afirmar convergência ou cobertura.

[REAL estrutural] Todos os26 arquivos do manifesto e os9 originais INIT003 foram conferidos por tamanho/hash. Removidas exclusivamente as instruções/definições novas de audit, o AST inteiro da fonte científica coincide com INIT003. Assinaturas, chamadas científicas selecionadas, construção completa da allowlist, predicados do hook, chamadas de resource/timer e limites declarados foram comparados independentemente. Priors/adapter/helper temporal permanecem nas referências originais pinadas. Os entrypoints candidatos recusam PREPARATION_ONLY; não foi criado contrato executável, autorização ou CLAIM.

[OPEN] Os21 testes escritos cobrem os casos pretendidos de latch, absorção de exceção, prioridade da recusa, aceitação de parcial limpo, inconsistências e parada da campanha. Nove examinam latch/checkpoints/exceções, dez aceitação de resultado, dois o fluxo da campanha. Testes de integração do source/driver/supervisor reais não foram executados; as simulações não demonstram captura de um import nativo real. O caminho físico de journal/short-write/fsync e a instalação de sys.addaudithook não têm validação dinâmica nesta suíte de doubles. A conclusão estática não supre esses controles futuros.

A espera inicial herdada de3610s por filho é preservada, assim como o wait após kill sem timeout. Essa limitação está declarada; não se converte em garantia de prazo total do SO. Não houve flexibilização da allowlist, preload para ocultar recusa ou ampliação de limites científicos neste delta.

O recibo enumera todas as verificações e seus pins. Zero testes/candidatos/init/waveform/likelihood/sampler/PE executados, zero leitura D ou NPZ/HDF5, zero alteração de autorização ou memória compartilhada. INIT003 e IDs consumidos permanecem intactos; próximos passos dependem de decisão específica da ROOT.
"""
write('PARECER_REVISAO_DOCUMENTAL.md',note)
write('MANIFESTO_REVISAO.json',{'status':receipt['status'],'files':[pin(p) for p in sorted(OUT.iterdir()) if p.is_file()],'source_manifest':pin(BASE/'MANIFESTO_PREPARACAO.json'),'executions':0})
print(json.dumps({'checks_total':len(checks),'passed':sum(q['pass_check'] for q in checks),'manifest':pin(OUT/'MANIFESTO_REVISAO.json'),'note':pin(OUT/'PARECER_REVISAO_DOCUMENTAL.md')},ensure_ascii=False))
