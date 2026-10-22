from pathlib import Path
import ast, datetime, hashlib, json

B=Path(__file__).resolve().parent
P=B.parent
def pin(p):
    p=Path(p);raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def put(p,s):
    raw=s.encode('utf-8')
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def functions(p):
    return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(Path(p).read_text(encoding='utf-8')).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
r3=P/'sitecustomize_rite_r3.py';r4=P/'sitecustomize_rite_r4.py';r2=P/'sitecustomize_rite_r2.py'
assert r3.read_bytes()==(B/'sitecustomize_rite_r3.py').read_bytes()==(B/'replay_elevated/sitecustomize_rite_r3.py').read_bytes()
assert r4.read_bytes()==(B/'replay_r4_sentinel/sitecustomize_rite_r4.py').read_bytes()
f2,f3,f4=functions(r2),functions(r3),functions(r4)
changed23=[n for n in f2 if f2[n]!=f3[n]];changed34=[n for n in f3 if f3[n]!=f4[n]]
assert changed23==['_path'] and changed34==['_audit']
s3=r3.read_text(encoding='utf-8');s4=r4.read_text(encoding='utf-8')
assert s4.replace(', "socket.getnameinfo", "socket.sendto", "socket.sendmsg"','')==s3
o3=load(P/'GUARD_PATHS_R3B_RESULT.json');i3=load(B/'replay_elevated/GUARD_PATHS_R3B_RESULT.json')
o4=load(P/'GUARD_PATHS_R4_RESULT.json');i4=load(B/'replay_r4_sentinel/GUARD_PATHS_R4_RESULT.json')
for result,count,guard in [(o3,13,r3),(i3,13,r3),(o4,16,r4),(i4,17,r4)]:
    assert result['passed'] and result['exit_code']==0
    assert result['junction_removed'] and result['outside_unchanged_empty']
    assert len(result['result']['checks'])==count and all(x['passed'] for x in result['result']['checks'])
    assert result['guard_sha256']==pin(guard)['sha256']
assert i4['result']['checks'][-1]=={'name':'independent_safety_not_needed','passed':True}
events=load(B/'NETWORK_EVENT_PROBE_R1.json')
assert events['actual_network_calls']==0
assert [x['refused'] for x in events['results'][0]['checks']]==[True,False,False,False]
assert all(x['refused'] for x in events['results'][1]['checks'])
checks=[
    {'id':'differential_scope','verdict':'PASSA','finding':'R2→R3 altera somente _path. A lista de executáveis, permissões de subprocessos, regra de GPU e callbacks restantes permanecem iguais. R3→R4 acrescenta somente três eventos à lista de recusas de rede.'},
    {'id':'normal_extended_containment','verdict':'PASSA','finding':'Caminhos DOS ordinários e estendidos legítimos dentro da fixture são aceitos. Parent traversal ordinário/estendido, prefixo irmão e gravação fora são recusados. A comparação é por parentesco de Path, não prefixo textual.'},
    {'id':'junction','verdict':'PASSA','finding':'A resolução do caminho local detectou a junção escapando da raiz, inclusive com prefixo DOS estendido. A única junção de cada fixture foi validada e removida sem recursão; o alvo de fora, ainda dentro da revisão autorizada, permaneceu vazio.'},
    {'id':'unc_device','verdict':'PASSA_NO_TESTE_DE_CLASSIFICACAO','finding':'A função de contenção rejeita as representações UNC e NT device testadas sem resolver esses caminhos remotos. O ensaio não abre caminhos UNC nem afirma isolar chamadas nativas.'},
    {'id':'r3_network_gap','verdict':'RESSALVA_MATERIAL_CORRIGIDA_EM_R4','finding':'R3 ignorava socket.sendto/sendmsg/getnameinfo; sys.audit reproduziu essa omissão sem tráfego. Por isso seus 13 testes não justificavam uma afirmação irrestrita de bloqueio de rede. R4 passou as recusas dos eventos e os testes efetivos sendto/getnameinfo antes da operação.'},
    {'id':'independent_network_safety','verdict':'PASSA','finding':'O teste R4 recebeu um segundo hook sentinela, posterior ao guard, que lançaria RuntimeError para qualquer evento de rede coberto que passasse pelo primeiro. As 16 verificações e a 17ª de sentinela ociosa passaram: o guard recusou antes dela. Nenhum tráfego foi autorizado ou enviado pela revisão.'},
]
scope=['Revisão técnica da mitigação de I/O Python para o programa fixado; não é garantia de sandbox do sistema operacional ou isolamento contra código hostil.',
       'Processos nativos Lean/Lake/MiKTeX permanecem fora da contenção dos audit hooks, conforme a própria docstring. Esta revisão não iniciou o rito científico nem esses processos.',
       'A primeira tentativa independente em ambiente restrito recusou a criação da junção antes dos testes. Foi preservada; uma fixture nova foi executada com permissão própria apenas para criar/remover a junção local controlada.',
       'Originais R2/R3/R4 e resultados anteriores permaneceram intactos. Escritas apenas na revisão; nenhuma memória, ACOM, produção, dado observado, provedor ou gate foi alterado.',
       'O aceite refere-se ao guard R4 com SHA pinado neste recibo. Não autoriza outro executável, rede, recarga ou implantação.']
files=[r2,r3,r4,P/'test_guard_paths_r3b.py',P/'test_guard_paths_r4.py',P/'GUARD_PATHS_R3B_RESULT.json',P/'GUARD_PATHS_R4_RESULT.json',P/'PLANO_RITO_REAL_R3.json',B/'SETUP_REFUSAL_R1.json',B/'replay_elevated/GUARD_PATHS_R3B_RESULT.json',B/'replay_r4_sentinel/GUARD_PATHS_R4_RESULT.json',B/'replay_r4_sentinel/test_guard_independent_r1.py',B/'NETWORK_EVENT_PROBE_R1.json',B/'network_event_probe_r1.py']
report={'unit':'F1.FECHO_20261015','claim_event':845,'reviewer':'/root/atrator_skeptic','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'R4_PASSA_COM_ESCOPO__R3_REDE_INCOMPLETA_CORRIGIDA','checks':checks,'scope':scope,'ast_functions_changed_R2_R3':changed23,'ast_functions_changed_R3_R4':changed34,'independent_replays':{'R3':{'exit_code':i3['exit_code'],'seconds':i3['seconds'],'checks':13},'R4_with_sentinel':{'exit_code':i4['exit_code'],'seconds':i4['seconds'],'checks':17}},'guard_R4':pin(r4),'files':[pin(p) for p in files],'generator':pin(__file__)}
put(B/'REVISAO_GUARD_R3_R4_R1.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Revisão independente do guard R3 e correção R4','','[REAL] R4 PASSA com o alcance dos eventos Python testados. A cobertura de rede incompleta do R3 foi corrigida aditivamente.','',
       'Reprodução independente: R3 13/13, R4 17/17 (16 controles + sentinela independente), ambas EXIT 0. Junções removidas, alvos externos da fixture vazios.','']+[f"- **{c['id']} — {c['verdict']}:** {c['finding']}" for c in checks]
lines+=['','## Alcance','']+['- '+s for s in scope]
lines+=['','Hashes, comandos, tempos e recibos: REVISAO_GUARD_R3_R4_R1.json.']
put(B/'REVISAO_GUARD_R3_R4_R1.md','\n'.join(lines)+'\n')
print(json.dumps({'verdict':report['verdict'],'guard_R4':pin(r4),'json':pin(B/'REVISAO_GUARD_R3_R4_R1.json'),'md':pin(B/'REVISAO_GUARD_R3_R4_R1.md')},ensure_ascii=False))
