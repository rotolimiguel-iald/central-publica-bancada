"""Review KH-N1 patch in memory; no um.py import, main run, or candidate write."""
from pathlib import Path
import ast, copy, datetime, hashlib, json, re
B=Path(__file__).resolve().parent
P=B.parent
F=P/'full_rite'
def pin(p):
 p=Path(p);b=p.read_bytes()
 return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def put(p,x):
 b=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8') if isinstance(x,dict) else x.encode('utf-8')
 with p.open('xb') as f:f.write(b)
 assert p.read_bytes()==b
builder=F/'build_kh_n1_patch_r1.py';tests=F/'kh_patch_tests_r1/PATCH_TEST_RECEIPT_R1.json'
fixture=F/'kh_patch_tests_r1/FIXTURE_ONLY_R3_PRIOR_RITE_CONTRACT.json';source=P/'candidate_r3/um.py'
before=[pin(p) for p in [builder,tests,fixture,source]]
t=read(tests);c=read(fixture)
assert t['all_passed'] and all(x['passed'] for x in t['checks'])
assert pin(builder)['sha256']==t['builder_sha256']
assert pin(source)['sha256']==t['source_sha256']
assert pin(fixture)['sha256']==t['fixture_contract_sha256']
ns={'__name__':'kh_patch_review_no_main','__file__':str(builder)}
exec(compile(builder.read_text(encoding='utf-8'),str(builder),'exec'),ns)
raw=source.read_bytes();tree=ast.parse(raw)
embedded=ns['literal'](tree,'_EMBEDDED_KERNEL_FILES')[1]
for key in ['audit_log','audit_receipt']:
 assert pin(c[key]['path'])['sha256']==c[key]['sha256']
log=Path(c['audit_log']['path']).read_text(encoding='utf-8')
totals=re.findall(r'(?m)^TGL_AXIOM_COVERAGE_TOTAL decl=([0-9]+) thm=([0-9]+) fora_do_trio=([0-9]+)\s*$',log)
assert len(totals)==1
actual=dict(zip(['decl','thm','fora_do_trio'],map(int,totals[0])))
assert all(actual[k]==c[k] for k in actual)
checks=[]
def probe(name,mutate,should_accept):
 x=copy.deepcopy(c);mutate(x)
 try:ns['validate_contract'](x,embedded);accepted=True
 except (ValueError,KeyError,TypeError):accepted=False
 checks.append({'name':name,'accepted':accepted,'expected_correct_behavior_accept':should_accept,'passes_required_behavior':accepted is should_accept,'decl':x['decl'],'thm':x['thm'],'entries':x['axiom_report_entries'],'unread':x['nao_lidas_pelo_regex'],'audit_exit_code':x['audit_exit_code']})
probe('valid_historical_fixture',lambda x:None,True)
probe('joint_counts_plus_one_same_pinned_log',lambda x:x.update(decl=x['decl']+1,axiom_report_entries=x['axiom_report_entries']+1),False)
probe('theorem_count_plus_one_same_pinned_log',lambda x:x.update(thm=x['thm']+1),False)
probe('changed_regex_gap_same_pinned_log',lambda x:x.update(nao_lidas_pelo_regex=x['nao_lidas_pelo_regex']+1,axiom_report_entries=x['axiom_report_entries']-1),False)
probe('boolean_exit_false',lambda x:x.update(audit_exit_code=False),False)
probe('boolean_decl',lambda x:x.update(decl=True),False)
probe('wrong_log_hash',lambda x:x['audit_log'].update(sha256='0'*64),False)
probe('outside_trio_contract',lambda x:x.update(fora_do_trio=1),False)
result,detail=ns['compose'](raw.decode('utf-8'),c,fixture,fixture.read_bytes())
newtree=ast.parse(result)
allowed={'_V393_SPECS','_V393_FONTES','_V393_NOMES_REGISTROS'}
def unchanged(t):return [ast.dump(n,include_attributes=False) for n in t.body if not(isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id in allowed for v in n.targets))]
assert unchanged(tree)==unchanged(newtree)
oldspecs=ns['literal'](tree,'_V393_SPECS')[1];newspecs=ns['literal'](newtree,'_V393_SPECS')[1]
historical=next(s for s in newspecs if s['nome']=='kh_n1_cobertura_v393')
old=next(s for s in oldspecs if s['nome']=='kh_n1_cobertura_v393')
assert historical['extras']['v393_original_spec_preserved']==old
new=next(s for s in newspecs if s['nome']=='kh_n1_cobertura_v394')
assert all(x['op']=='igual' for x in new['checks'] if x['id'] in ['h_decl','h_thm','h_sources_exact'])
for p in before:assert pin(p['path'])==p
out={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'codex-atrator-skeptic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'REQUER_CORRECAO_VINCULO_CONTAGENS_LOG_RECIBO','material_findings':[{'id':'KH-R1','severity':'MEDIUM','anchor':'build_kh_n1_patch_r1.py:41-74','observation':'Hashes conferem, mas contagens do contrato não são reconstruídas nem comparadas ao conteúdo do log. Três mutações coerentes internamente foram aceitas com o mesmo log pinado, incluindo decl/report+1, thm+1 e lacuna de regex alterada. O recibo também só é lido para calcular hash; seu exit, ligação ao log e conjunto de fontes não são consumidos.','fix':'Validar uma única linha TOTAL, reconstruir entradas de axiomas e nomes não lidos com a mesma semântica do consumidor, conferir axiomas/sorry e comparar todos os totais; ler recibo de auditoria integral tipado e exigir exit inteiro zero, vínculo ao log e ao conjunto de fontes. Nada de expectativa derivada do futuro rito.'}],
 'low_findings':[{'id':'KH-R2','observation':'audit_exit_code=False passa porque False==0. Exigir type(value) is int, como nas demais contagens.'}],
 'checks':checks,'actual_fixture_totals_from_log':actual,'existing_structural_checks':len(t['checks']),
 'positive_results':['As mutações do programa ficam somente nas três atribuições de dados; nenhuma função ou outro AST muda.','Especificação v393 original preservada em extras; h2/h3 históricos passam a pisos e a spec v394 cobra valores exatos.','Booleano em decl, hash do log alterado e fora_do_trio não zero foram recusados.','A expectativa não é lida do próximo rito, mas a origem prévia ainda precisa do vínculo semântico comprovado.'],
 'scope':'Revisão em memória do gerador e dos predicados; fixture histórica explicitamente marcada. Não rodou main, Lean, rito integral ou geração de candidato.',
 'sources':before+[pin(c['audit_log']['path']),pin(c['audit_receipt']['path'])],'script':pin(__file__),'production_memory_gate_changed':False}
put(B/'REVISAO_KH_PATCH_R1.json',out)
md='''# Revisão KH-N1 R1

**REQUER CORREÇÃO — vínculo entre contrato e evidência.**

[REAL] A validação aceita três alterações de contagem com o mesmo log pinado: decl e axiom_report_entries +1; thm +1; lacuna de regex +1 e entradas −1. O hash conserva bytes, mas o código não lê os totais desses bytes. O recibo de auditoria também é apenas pinado; seu conteúdo não é vinculado ao log, às fontes e ao exit informado no contrato. `audit_exit_code=False` passa por igualdade com zero.

Exigir uma linha TOTAL única, reconstrução de entradas/lacuna/axiomas a partir do log, comparação integral e recibo tipado ligando exit inteiro zero, log e conjunto exato de fontes. A pré-medição deve continuar anterior ao rito.

[REAL] A estrutura do patch passa: só três atribuições AST mudam; a spec v393 original permanece em extras; os pisos históricos e as igualdades v394 estão separados. Recusas de hash adulterado, booleano em decl e axioma externo continuam funcionando. Nenhum main, candidato ou produção foi executado/escrito.

Detalhes, fontes, hashes e oito sondas em REVISAO_KH_PATCH_R1.json.
'''
put(B/'REVISAO_KH_PATCH_R1.md',md)
print(json.dumps({'json':pin(B/'REVISAO_KH_PATCH_R1.json'),'md':pin(B/'REVISAO_KH_PATCH_R1.md'),'checks':checks},ensure_ascii=False))
