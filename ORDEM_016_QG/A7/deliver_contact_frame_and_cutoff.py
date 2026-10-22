"""Record new bridge evidence without promoting it to full Q2."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid
H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT'
D=H/'contact_frame_cutoff_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,update=False):
    if isinstance(b,str):b=b.encode('utf-8')
    if p.exists():
        assert update,p;old=p.read_bytes()
        bak=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:8])
        bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert b and t.read_bytes()==b;t.replace(p);assert p.read_bytes()==b
def put(p,v,update=False):write(p,json.dumps(v,ensure_ascii=False,indent=2),update)
names=['contact_frame_naturality','fourth_order_cutoff_bridge']
rs={n:json.loads((H/n/'results.json').read_bytes()) for n in names}
files=[Path(__file__),H/'contact_frame_naturality/DERIVACAO.md']
for n in names:
    mp=H/n/'manifest.json';files.append(mp)
    for row in json.loads(mp.read_bytes())['artifacts']:
        p=Path(row['path']);assert sha(p)==row['sha256'];files.append(p)
    files.append(H/(n+'_run.log'))
count=sum(r['checks'] for r in rs.values());cpu=sum(r['cpu_seconds'] for r in rs.values())
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
report=O/'ENTREGA_016_A7b_frame_naturalidade_e_corte_quarta_ordem.md'
write(report,f'''[DERIVED — naturalidade bilocal e localização da primitiva até O(K); Q2 completa OPEN]

Data {now}. Abertura SHA256 {opening}.

Os dois propagadores singulares e a distância geodésica passam no teste
de derivada de Lie simultânea nos extremos X/Y, para todas as componentes
e quatro transvecções do espaço-forma auxiliar. A verificação conserva
X e Y simbólicos. A distância coordenada w não passa: seus quatro
resíduos estão registrados. Não se escolheu regulador pelo resultado.

O transporte radial do frame e a regra de duas integrações por partes
justificam a leitura local por jatos completamente simétricos, com sinal
positivo no operador sobre c para as ordens ímpares3/5. O teste não
certifica novamente todos os vértices/diagramas; essa aplicação continua
ligada à montagem tensorial declarada no cálculo anterior. A completação
coordenada preserva sua ressalva de naturalidade global.

A localização da nova Hessiana de quarta ordem exige

    M_chi=(chi*N+N*chi)/2=chi*N+[N,chi]/2.

A derivação covariante direta de chi*h coincide com a soma de todos os
subconjuntos ordenados de derivadas, incluindo conexões nos índices
derivados. Os coeficientes paralelos foram conferidos sob transposição
das dez fibras simétricas, com b,c,t e momentos simbólicos. Omitir o
comutador ou duplicar sua metade produz resíduos explícitos.

A demonstração escrita inclui a corrente de Green da quarta ordem e
s0 B_chi=-C_E integral h[chi*A_cov c+[N,chi]Gc/2]+O(K²). Ao transferir
também G para o outro lado, suas derivadas de chi devem ser conservadas.
BRST-exatidão dessa variação não identifica sozinha todo o contato
quântico localizado. Nenhum contratermo foi adotado.

## Evidência e próximo passo

- Naturalidade/frame/sinais: {rs['contact_frame_naturality']['checks']} verificações,
  CPU {rs['contact_frame_naturality']['cpu_seconds']}s, oito controles negativos.
- Corte/adjunção: {rs['fourth_order_cutoff_bridge']['checks']} verificações,
  CPU {rs['fourth_order_cutoff_bridge']['cpu_seconds']}s, quatro pares de resíduos.
- Total desta entrega: {count} verificações; CPU {cpu}s. Ambos os comandos
  com A4/symbolic_runtime/Scripts/python.exe -X utf8 -B terminaram rc0.

Fontes, scripts, logs e demonstração: manifesto em {D/'manifest.json'}.
Ainda faltam os outros diagramas locais, W geral, K², aridades superiores
e valores de contorno lorentzianos. Próximo trabalho: essas parcelas e
a comparação das revisões independentes pendentes, dentro do A7.b.
O turno anterior foi PROGRESS (resultado local e staging custodiados).
Nenhum processo próprio continua vivo; nenhuma nova chamada externa
foi iniciada neste turno. Originais, kernel e gate permanecem intactos.
''')
measure=O/'ENTREGA_016_MEDIDA_naturalidade_bilocal_e_corte.md'
write(measure,f'''[REAL — identidades e defeitos locais medidos]

Data {now}; abertura SHA256 {opening}.

Tentativa1: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/contact_frame_naturality_check.py; rc0;
log SHA256 {sha(H/'contact_frame_naturality_run.log')}.
Identidade (L_kX+L_kY)G=O(K²), para ghost/métrico, antes da ancoragem;
distância geodésica também. A distância coordenada tem defeito não nulo,
registrado por eixo em results.json. Sem escolha de prescrição.

Tentativa2: mesmo interpretador, A7/fourth_order_cutoff_bridge_check.py;
rc0; log SHA256 {sha(H/'fourth_order_cutoff_bridge_run.log')}.
Identidade M_chi=chi*N+[N,chi]/2. Exemplo componente01 no setor plano:
omitir a metade do comutador perde -9b-12c-1337/1920.
Parâmetros livres, não escolhidos para anular o resíduo.

CPU total {cpu}s. Chamadas externas novas: zero. Próximo ramo dentro
A7.b: termos locais restantes e W/revisões. Q2 completa não inferida.
''')
files+= [report,measure];files=list(dict.fromkeys(files))
put(D/'manifest.json',dict(at=now,opening_sha256=opening,checks=count,cpu_seconds=cpu,
    full_Q2=False,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
ledger=O/'LEDGER_016.jsonl'
event=dict(at=now,event='A7_CONTACT_FRAME_NATURALITY_AND_FOURTH_ORDER_CUTOFF',
    target='A7.b',checks=count,cpu_seconds=cpu,remote_call=False,
    manifest_sha256=sha(D/'manifest.json'),full_Q2=False)
write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
rows=[json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()]
for r in rows:
    keys=ids(r)
    for k in keys[1:]:parents[root(k)]=root(keys[0])
known={}
for r in rows:
    keys=ids(r);cost=r.get('cost_estimate_usd',r.get('cost_usd',r.get('custo_usd')))
    if keys and cost is not None:known[root(keys[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(known_partial_usd=str(total),unknown_not_zero=True,ledger_sha256=sha(ledger)))
p=O/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n- {now} A7.b PROGRESS: naturalidade/frame e corte quarta ordem; {count}checks,CPU{cpu}s. Comutador do corte preservado. Q2 OPEN; custo parcial US${total}, desconhecidosnãozero; zero chamadas externas novas.\n'.encode(),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',own_live_processes=[],
    contact_frame_cutoff_manifest=str(D/'manifest.json'),partial_metered_cost_usd=str(total),
    completed_this_turn=['1496 naturality/frame/sign checks',
        '528 fourth-order covariant cutoff and fiber-adjoint checks',
        'Written Green-current and distribution/frame bridge with limited scope'],
    quantum_anomaly_computed=False,
    next=['Remaining local diagrams/W and higher arities under A7.b fixed prescription',
          'Audit new Kimi harmonic/smooth responses without assuming uniqueness of local/nonlocal split',
          'A7.b deadline2026-09-25T20:32Z; then A7.c/d,A8,PartB,full final audit'])
put(p,v,True)
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:
    assert sha(Path(row['path']))==row['sha256']
print(json.dumps(dict(checks=count,cpu_seconds=cpu,artifacts=len(files),
    known_partial_usd=str(total),report=str(report),goal='ACTIVE',full_Q2=False)))
