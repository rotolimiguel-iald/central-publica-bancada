"""Review actual candidate R4 and isolated evidence consumer; never import main."""
from pathlib import Path
import ast,copy,datetime,hashlib,json,time
B=Path(__file__).resolve().parent;P=B.parent
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_bytes())
def put(p,v):
 raw=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode() if isinstance(v,dict) else v.encode()
 with p.open('xb') as f:f.write(raw)
 assert p.read_bytes()==raw
def literal(t,name):
 rows=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(k,ast.Name) and k.id==name for k in n.targets)]
 assert len(rows)==1,name
 return ast.literal_eval(rows[0].value)
def functions(t):return {n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
def dump(n):return ast.dump(n,include_attributes=False)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.perf_counter()
receipt=P/'INTEGRATION_NETWORK_R4.json';r=read(receipt)
for k,v in r.items():
 if isinstance(v,dict) and {'path','sha256','bytes'}<=set(v):assert pin(v['path'])==v,k
before=[pin(receipt)]+[v for v in r.values() if isinstance(v,dict) and {'path','sha256','bytes'}<=set(v)]
baseline=ast.parse(Path(r['baseline']['path']).read_bytes());candidate=ast.parse(Path(r['candidate']['path']).read_bytes())
oldf,newf=functions(baseline),functions(candidate)
changed=sorted(k for k in oldf if dump(oldf[k])!=dump(newf[k]))
assert changed==['_v394_article_tex','compile_pdf','main','prove_external_ladder']
assert set(newf)-set(oldf)=={'rede_fock_v394'}
allowed_assign={'_EMBEDDED_KERNEL_FILES','_LEAN_THEOREM_FLAGS','_V394_FORMAL_CONTRACT','_V394_QUADRATIC_CONTRACT','_V394_NETWORK_CONTRACT'}
runtime=ast.parse(Path(r['runtime']['path']).read_bytes())
runtime_doc=next(n for n in runtime.body if isinstance(n,ast.Expr))
def filter_ast(t):
 out=[]
 for n in t.body:
  if isinstance(n,ast.FunctionDef) and n.name in changed+['rede_fock_v394']:continue
  if isinstance(n,ast.Assign) and any(isinstance(k,ast.Name) and k.id in allowed_assign for k in n.targets):continue
  if dump(n)==dump(runtime_doc):continue
  out.append(dump(n))
 return out
assert filter_ast(baseline)==filter_ast(candidate),'unexpected non-function changes'
assert dump(newf['rede_fock_v394'])==dump(functions(runtime)['rede_fock_v394'])
pdf=read(r['pdf_patch']['path']);pdf_ast=ast.parse(Path(pdf['replacement']['path']).read_bytes())
assert dump(newf['compile_pdf'])==dump(functions(pdf_ast)['compile_pdf'])
old_embedded=literal(baseline,'_EMBEDDED_KERNEL_FILES');embedded=literal(candidate,'_EMBEDDED_KERNEL_FILES')
old_flags=literal(baseline,'_LEAN_THEOREM_FLAGS');flags=literal(candidate,'_LEAN_THEOREM_FLAGS')
plan=read(r['bundle_plan']['path']);compiled=read(r['compiled_bundle']['path'])
assert compiled['passed'] is True and compiled['plan']==r['bundle_plan']
modules={row['module']:row for row in compiled['modules']}
expected={row['module']:row['transposed_source'] for row in plan['modules']};expected[plan['audit_module']]=plan['audit']
assert len(modules)==len(compiled['modules'])==50 and set(modules)==set(expected)
for name,row in modules.items():
 assert row['source']==expected[name] and row['passed'] is True and type(row['exit_code']) is int and row['exit_code']==0
 for k in ('source','object','stdout','stderr'):assert pin(row[k]['path'])==row[k]
 assert all(isinstance(v,list) and set(v)<={'propext','Classical.choice','Quot.sound'} for v in row['axiom_report'].values())
report=modules[plan['audit_module']]['axiom_report']
assert set(report)==set(plan['theorems']) and len(report)==936
contract=literal(candidate,'_V394_NETWORK_CONTRACT')
assert contract['declarations']==sorted(set(plan['theorems'])-set(old_flags.values()))
assert flags==dict(old_flags,**r['new_flags']) and len(r['new_flags'])==936
added={row['relative']:Path(row['transposed_source']['path']).read_bytes() for row in plan['modules']}
added[plan['audit_relative']]=Path(plan['audit']['path']).read_bytes()
assert set(embedded)-set(old_embedded)==set(added)
assert all(embedded[k].encode()==v for k,v in added.items())
roots={'TGLExt.lean','TGL/Audit.lean'}
assert {k for k in old_embedded if old_embedded[k]!=embedded[k]}==roots
glue='import '+plan['audit_module']+'\n'
assert embedded['TGLExt.lean']==old_embedded['TGLExt.lean']+'\n'+glue
assert embedded['TGL/Audit.lean']==glue+'\n'+old_embedded['TGL/Audit.lean']
assert contract['source_sha256']=={k:hashlib.sha256(v).hexdigest() for k,v in added.items()}
kernel=Path(r['candidate']['path']).parent/'tgl_kernel'
assert all((kernel/k).read_bytes()==v.encode() for k,v in embedded.items())
for name in ['_V394_FORMAL_CONTRACT','_V394_QUADRATIC_CONTRACT']:
 before_contract=literal(baseline,name);after_contract=literal(candidate,name)
 assert before_contract['expected_ladder']==7171
 before_contract['expected_ladder']=8107
 assert before_contract==after_contract
def ladder(t):
 return ast.literal_eval(next(n.value for n in functions(t)['prove_external_ladder'].body if isinstance(n,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='ext_flags' for k in n.targets)))
lad=ladder(candidate);oldlad=ladder(baseline)
assert lad==oldlad+list(r['new_flags']) and len(lad)==len(set(lad))==8107
assert contract['expected_ladder']==8107
maintext=ast.unparse(newf['main']);articletext=ast.unparse(newf['_v394_article_tex'])
assert maintext.index('_network_result = rede_fock_v394(core)')>maintext.index('regra_quadratica_v394(core)')
assert maintext.index('_network_result = rede_fock_v394(core)')<maintext.index('_figs = emit_figures(core)')
assert "os.path.abspath(__file__) if f == 'um.py' else os.path.join(OUT, f)" in maintext
assert 'whole_certificate_inhabited' in maintext and 'rede_fock_v394' in articletext
# Real pre-audit, already bound to complete source set by independent KH-N1 R3 review.
kh_path=P/'full_rite/kh_patch_tests_r3/KH_N1_V394_PREAUDIT_CONTRACT_R3.json';kh=read(kh_path)
builder=P/'full_rite/build_kh_n1_patch_r3.py';bs={'__name__':'review_no_main','__file__':str(builder)}
exec(compile(builder.read_bytes(),str(builder),'exec'),bs)
bs['validate_contract'](kh,embedded)
parsed=bs['parse_audit_log'](Path(kh['audit_log']['path']).read_text(encoding='utf-8'))
actual_axioms=parsed['reports']['runtime']
clean=sum(isinstance(actual_axioms.get(flags[k]),list) and set(actual_axioms[flags[k]])<={'propext','Classical.choice','Quot.sound'} for k in lad)
assert clean==8107
ns={'_V394_NETWORK_CONTRACT':contract,'_EMBEDDED_KERNEL_FILES':embedded}
exec(compile(ast.Module(body=[newf['rede_fock_v394']],type_ignores=[]),'<extracted-real-candidate-consumer>','exec'),ns)
core={'kernel_formalization':{'all_verified':True,'axiom_report':actual_axioms},'external_ladder':{'n_theorems_clean':clean,'n_theorems_expected':len(lad)},'regra_quadratica_v394':{'all_verified':True},'gate':'UNCHANGED_REVIEW_SENTINEL'}
original=copy.deepcopy(core);result=ns['rede_fock_v394'](core)
assert result['all_verified'] is True and result['whole_certificate_inhabited'] is False and result['does_not_gate_core'] is True
del core['rede_fock_v394'];assert core==original
controls=[]
for name,mut in [('one_declaration_missing',lambda c:c['kernel_formalization']['axiom_report'].pop(contract['declarations'][0])),('quadratic_dependency_false',lambda c:c['regra_quadratica_v394'].update(all_verified=False)),('formal_status_false',lambda c:c['kernel_formalization'].update(all_verified=False))]:
 c=copy.deepcopy(original);mut(c);q=ns['rede_fock_v394'](c);assert q['all_verified'] is False
 controls.append({'name':name,'refused':True})
for x in before:assert pin(x['path'])==x
out={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'codex-atrator-skeptic','start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-t0,'verdict':'PASSA_CANDIDATA_R4_COMPONENTES','material_findings':[],
 'changed_existing_functions':changed,'added_function':'rede_fock_v394','unchanged_other_top_level_ast':True,'embedded_files':len(embedded),'new_modules_including_audit':len(added),'compiled_modules':len(modules),'new_declarations':len(report),'actual_full_audit_clean_ladder':clean,'expected_ladder':8107,
 'consumer':{'actual_compiled_report':pin(kh['audit_log']['path']),'all_verified':result['all_verified'],'verdict':result['verdict'],'declared_coverage':len(result['formal_declarations']),'source_coverage':len(result['embedded_sources']),'controls':controls,'scope':'Execução real da função extraída da candidata, usando relatório de axiomas efetivamente compilado e contagem reconstruída da escada. Harness isolado fornece all_verified do kernel a partir da pré-auditoria validada e fornece a dependência regra_quadratica=True como fixture explícita. Essa função quadrática e main não foram executados nesta chamada; isto não é o resultado do rito integral.'},
 'scope':['Apenas quatro funções existentes alteradas; todas as demais funções/classes/expressões/atribuições fora da lista permitida têm AST idêntica.','50 novas fontes iguais byte a byte ao plano recompilado; 1.287 fontes materializadas iguais ao conteúdo embutido. Somente duas raízes históricas ganham o import.','PDF R2 coincide por AST com a substituição revista; identidade do selo usa arquivo realmente executado.','Whole certificate continua sem habitante e polar/KMS/contrato conjunto permanecem OPEN.','Nenhum main, import de um.py, produção, memória ou gate executado/alterado.'],
 'sources':before+[pin(kh_path),pin(P/'kh_patch_review/REVISAO_KH_PATCH_R3.json')],'script':pin(__file__)}
put(B/'REVISAO_CANDIDATA_R4_R1.json',out)
put(B/'REVISAO_CANDIDATA_R4_R1.md','# Revisão da candidata R4\n\n**PASSA no escopo de componentes e integração aditiva.**\n\n[REAL] A comparação independente confirma quatro funções modificadas, uma função nova, 50 módulos novos (incluindo auditor), 936 declarações novas e 8.107 posições da escada satisfeitas pelo relatório real. As 1.287 fontes materializadas conferem byte a byte com o programa. Fora das atribuições e funções previstas, o AST é idêntico.\n\n[REAL] O consumidor real extraído da candidata aceitou o relatório compilado, preservou o gate sentinela e recusou declaração ausente ou dependências falsas. O harness fornece explicitamente as duas marcas agregadas de validação; a dependência quadrática não foi reexecutada. Isto não é um rito integral.\n\n[OPEN] Habitante do contrato conjunto, identificação polar/KMS e realização física conjunta não são anunciados. Nenhum main ou produção foi executado. Pins e detalhes em REVISAO_CANDIDATA_R4_R1.json.\n')
print(json.dumps({'review':pin(B/'REVISAO_CANDIDATA_R4_R1.json'),'md':pin(B/'REVISAO_CANDIDATA_R4_R1.md'),'verdict':out['verdict']},ensure_ascii=False))
