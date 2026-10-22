"""Independent KH-N1 R3 review; memory-only composition, no program import/run."""
from pathlib import Path
import ast, copy, datetime, hashlib, json, re, time
B=Path(__file__).resolve().parent
P=B.parent
F=P/'full_rite'
def pin(p):
 p=Path(p); b=p.read_bytes()
 return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_bytes())
def put(p,x):
 b=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode() if isinstance(x,dict) else x.encode()
 with p.open('xb') as f:f.write(b)
 assert p.read_bytes()==b
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.perf_counter()
builder=F/'build_kh_n1_patch_r3.py';contract=F/'kh_patch_tests_r3/KH_N1_V394_PREAUDIT_CONTRACT_R3.json'
tests=F/'kh_patch_tests_r4/PATCH_TEST_RECEIPT_R4.json';source=P/'candidate_r4/um.py'
before=[pin(x) for x in [builder,contract,tests,source,F/'test_kh_n1_patch_r4.py']]
t=read(tests);c=read(contract)
assert t['passed'] is True and len(t['tests'])==18 and all(x['passed'] for x in t['tests'])
for k,p in [('builder',builder),('contract',contract),('source',source),('test_script',F/'test_kh_n1_patch_r4.py')]:assert t[k]==pin(p)
ns={'__name__':'review_no_main','__file__':str(builder)}
exec(compile(builder.read_bytes(),str(builder),'exec'),ns)
raw=source.read_bytes();tree=ast.parse(raw)
embedded=ns['literal'](tree,'_EMBEDDED_KERNEL_FILES')[1]
checks=[]
def check(name,fn,accept):
 try:fn();actual=True;err=None
 except (ValueError,KeyError,TypeError,AssertionError) as e:actual=False;err=str(e)
 checks.append({'name':name,'accepted':actual,'expected_accept':accept,'passed':actual is accept,'error':err})
 assert actual is accept,(name,err)
def probe(name,mutate,accept=False):
 cc=copy.deepcopy(c);mutate(cc)
 check(name,lambda:ns['validate_contract'](cc,embedded),accept)
probe('actual_pinned_full_audit',lambda x:None,True)
probe('decl_and_entries_plus_one',lambda x:x.update(decl=x['decl']+1,axiom_report_entries=x['axiom_report_entries']+1))
probe('thm_plus_one',lambda x:x.update(thm=x['thm']+1))
probe('regex_gap_changed_coherently',lambda x:x.update(nao_lidas_pelo_regex=x['nao_lidas_pelo_regex']+1,axiom_report_entries=x['axiom_report_entries']-1))
probe('boolean_exit',lambda x:x.update(audit_exit_code=False))
probe('boolean_decl',lambda x:x.update(decl=True))
probe('outside_trio_contract',lambda x:x.update(fora_do_trio=1))
probe('wrong_log_pin',lambda x:x['audit_log'].update(sha256='0'*64))
log=Path(c['audit_log']['path']).read_text(encoding='utf-8')
parsed=ns['parse_audit_log'](log)
total=re.search(r'(?m)^TGL_AXIOM_COVERAGE_TOTAL[^\r\n]*',log).group()
name=next(iter(parsed['reports']['runtime']))
pattern=r"(?m)^'"+re.escape(name)+r"' (?:depends on axioms:\s*\[[^]]*\]|does not depend on any axioms)\s*"
missing,n=re.subn(pattern,'',log)
assert n>0 and name not in ns['parse_audit_log'].__globals__.get('nonexistent',{})
for label,text in [('duplicate_total',log+'\n'+total+'\n'),('missing_all_rows_of_declaration',missing),('outside_axiom',log+"\n'Injected' depends on axioms: [NewAxiom]\n"),('sorry_token',log+'\nsorryAx\n')]:
 check(label,lambda text=text:ns['parse_audit_log'](text),False)
key=next(k for k in embedded if k not in ('TGLExt.lean','TGL/Audit.lean'))
ee=dict(embedded);ee[key]+='\n-- coherent source mutation\n'
cc=copy.deepcopy(c);cc['formal_files_sha256'][key]=hashlib.sha256(ee[key].encode()).hexdigest()
check('coherent_embedded_and_contract_change',lambda:ns['validate_contract'](cc,ee),False)
audit=read(c['audit_receipt']['path']);audit['exit_code']=False
mock=B/'AUDIT_BOOL_EXIT_FIXTURE_R3.json';put(mock,audit)
cc=copy.deepcopy(c);cc['audit_receipt']=pin(mock)
check('audit_receipt_bool_exit',lambda:ns['validate_contract'](cc,embedded),False)
result,detail=ns['compose'](raw.decode(),c,contract,contract.read_bytes())
updated=ast.parse(result)
allowed={'_V393_SPECS','_V393_FONTES','_V393_NOMES_REGISTROS'}
def filtered(t):return [ast.dump(n,include_attributes=False) for n in t.body if not(isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id in allowed for v in n.targets))]
assert filtered(tree)==filtered(updated)
old=ns['literal'](tree,'_V393_SPECS')[1];new=ns['literal'](updated,'_V393_SPECS')[1]
historical=next(s for s in new if s['nome']=='kh_n1_cobertura_v393')
assert historical['extras']['v393_original_spec_preserved']==next(s for s in old if s['nome']=='kh_n1_cobertura_v393')
current=next(s for s in new if s['nome']=='kh_n1_cobertura_v394')
assert len(new)==len(old)+1
assert all(x['op']=='igual' for x in current['checks'] if x['id'] in ('h_decl','h_thm','h_sources_exact'))
for x in before:assert pin(x['path'])==x
out={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'codex-atrator-skeptic','start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-t0,
 'verdict':'PASSA_COM_ESCOPO_PREAUDITORIA_PINADA','material_findings':[],'resolved':['R1: contagens agora reconstruídas do log e vinculadas ao recibo real e ao conjunto de fontes recompiladas.','R1: exit booleano recusado tanto no contrato quanto no recibo.'],
 'independent_checks':checks,'structural_checks':['Somente três atribuições de dados mudam; todos os outros nós AST ficam iguais.','Spec v393 integral preservada em extras; pisos históricos e igualdade exata v394 explícitos.','Conjunto de fontes reconstruído da baseline, dos 50 módulos realmente compilados e das duas raízes.'],
 'counts':{k:v for k,v in parsed.items() if k!='reports'},'parser_lengths':{k:len(v) for k,v in parsed['reports'].items()},'builder_tests_passed':18,
 'fixture_erratum':'A tentativa de teste R3 removia só a primeira ocorrência de declaração com linhas duplicadas legítimas. R4 remove todas; essa recusa e as demais 18 verificações foram conferidas. Não é recusa ao recibo real.',
 'sources':before+[pin(c[k]['path']) for k in ('audit_log','audit_receipt','measured_coverage_receipt')], 'script':pin(__file__),
 'scope':'Validação real e composição em memória; não executa/importa um.py, não materializa candidato nem roda main. É pré-auditoria local de componentes matemáticos, não autorização de produção ou confirmação física.','production_memory_gate_changed':False}
put(B/'REVISAO_KH_PATCH_R3.json',out)
put(B/'REVISAO_KH_PATCH_R3.md','# Revisão KH-N1 R3\n\n**PASSA no escopo de pré-auditoria pinada.**\n\n[REAL] Validação independente reconstrói 26.797 declarações e 21.209 teoremas do log, com zero fora do trio. Os parsers runtime/recibo/completo leem 26.793/26.783/26.797 nomes; quatro nomes não lidos pelo regex legado ficam explícitos. As contagens, raízes e fontes são ligadas aos recibos reais e ao conjunto baseline + módulos recompilados.\n\n[REAL] As mutações coerentes de contagem/fonte, booleanos, declaração ausente, total duplicado e axioma externo são recusadas. Só três atribuições AST mudam na composição em memória, e a spec histórica permanece integral. Os 18 testes R4 do construtor passaram; a fixture R3 inadequada foi preservada.\n\nNenhum main ou produção foi executado. O parecer não substitui o rito posterior nem autoriza implantação. Detalhes e pins em REVISAO_KH_PATCH_R3.json.\n')
print(json.dumps({'review':pin(B/'REVISAO_KH_PATCH_R3.json'),'md':pin(B/'REVISAO_KH_PATCH_R3.md'),'independent_checks':len(checks),'verdict':out['verdict']},ensure_ascii=False))
