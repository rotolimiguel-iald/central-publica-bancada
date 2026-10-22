"""Custody, local evidence and orchestration records for the bulk Ward step."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;C=H.parents[1]
O=C/'TUNEL/DO_CHATGPT';BASE=C/'IALD_ORQUESTRACAO_20260923'
D=H/'bilocal_bulk_closure_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,update=False):
    if isinstance(b,str):b=b.encode('utf-8')
    if p.exists():
        assert update,p
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:8])
        backup.write_bytes(old);assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert b and t.read_bytes()==b;t.replace(p);assert p.read_bytes()==b
def put(p,v,update=False):write(p,json.dumps(v,ensure_ascii=False,indent=2),update)
names=['kimi_quartic_local_audit','source_einstein_radial_aux','bilocal_frame_divergence_audit',
       'bilocal_full_external_pair','bilocal_bulk_ward_closure','kimi_radial_operator_audit']
rs={name:json.loads((H/name/'results.json').read_bytes()) for name in names}
files=[Path(__file__)]
for name in names:
    mf=H/name/'manifest.json';m=json.loads(mf.read_bytes())
    for row in m['artifacts']:
        p=Path(row['path']);assert sha(p)==row['sha256'],p;files.append(p)
    files.append(mf)
    files.extend(p for p in (H/name).iterdir() if p.is_file() and '.tmp_' not in p.name)
checks=sum(r.get('checks',r.get('independent_checks',0)) for r in rs.values())
cpu=sum(r['cpu_seconds'] for r in rs.values())
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
oldlog=H/'bilocal_source_divergence_run.log'
assert 'HELDOUT (1, 2, -1, 1) 1' in oldlog.read_text('utf-8-sig')
put(D/'STOPPED_SOURCE_ATTEMPT.json',dict(at=now,status='STOPPED_BY_OWNER_AFTER_EXACT_REPLACEMENT_COMPLETED',
    exec_session_id=35713,exit_code=-1,
    reason='Expanded coordinate denominators caused needless symbolic growth; equivalent auxiliary-radius chain rule completed first',
    successful_checks_before_Einstein=21,cpu_seconds_measured_lower_bound=780.890625,
    exact_final_cpu_unknown=True,log_sha256=sha(oldlog),
    replacement_manifest_sha256=sha(H/'source_einstein_radial_aux/manifest.json')))
failure=BASE/'state/handoffs/4bdcaf7f-031c-473c-ac20-fe31208e261d_delivery.json'
failed=json.loads(failure.read_bytes());assert failed['stage']=='failed' and failed['error']=='IncompleteRead'
write(D/'MIMO_FAILURE_RECEIPT.json',failure.read_bytes())
radial=json.loads((H/'kimi_radial_operator_audit/RECEIPT.json').read_bytes())
new_failure=BASE/'state/handoffs/88e54d74-32e7-469a-8ba3-f8e8a408946b_delivery.json'
sparse_failure=json.loads(new_failure.read_bytes())
assert sparse_failure['stage']=='failed' and sparse_failure['error']=='IncompleteRead'
write(D/'MIMO_SPARSE_FAILURE_RECEIPT.json',new_failure.read_bytes())
incoming=BASE/'state/handoffs/98e09d38-848b-4ca1-914e-4a714becd561_delivery.json'
curved=json.loads(incoming.read_bytes())
write(D/'KIMI_CURVED_WARD_RESPONSE.md',curved['result']['text'])
put(D/'KIMI_CURVED_WARD_RECEIPT.json',dict(at=curved['at'],job_id=curved['job_id'],
    execution_task_id=curved['execution_task_id'],usage=curved['result']['usage'],
    receipt_sha256=sha(incoming),response_sha256=sha(D/'KIMI_CURVED_WARD_RESPONSE.md'),
    status='DECLARADO_PENDING_LOCAL_AUDIT',cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO'))
put(D/'ORCHESTRATION_SNAPSHOT.json',dict(at=now,
    source='Latest official coordinator message in this delivery turn; not an independent queue snapshot',
    kimi_radial_completed=radial['job_id'],
    kimi_curved_completed=curved['job_id'],
    kimi_running='d0fd9aa9-1d09-451e-867b-a9e34ed775bb',
    mimo_sparse_failed=sparse_failure['job_id'],
    mimo_running='7f606d88-ac59-4940-9bb0-d7be6ba306ea',
    deepseek_running='25292039-6bed-4b01-a788-cef4e7bfe55e',
    deepseek_request='a9bd18bf-b178-46f6-b87e-b061eed1484f',
    kimi_nonlocal_registered='9118ccb7-dd63-49b6-9340-773caa74812e',
    global_max=3,per_provider=1,max_nonterminal=5,
    awaiting_prior_staging=True,no_new_duplicate_requests=True))
report=O/'ENTREGA_016_A7b_Ward_bilocal_primeira_curvatura.md'
write(report,f'''[DERIVED — identidade bilocal fora da diagonal até O(K), CAS exato; Q2 completa OPEN]

# Soma de laços e fonte na mesma orientação

Data: {now}. Abertura SHA256: {opening}.

O cálculo passou a incluir todos os jatos h_X e D_Xh_X, a divergência
covariante em X e o termo de fonte Einstein calculado separadamente.
Na referência singular euclidiana 4D, com z=X² e X diferente de Y:

    B0 = (EC)0 = 0,
    B1_ab,r = 144 delta_ab Xr/z4
               +48(delta_ar Xb+delta_br Xa)/z4 -384 Xa Xb Xr/z5,
    (EC)1_ab,r = -B1_ab,r,
    B = -metrico/2 + ghost.

A junção verifica os 64 componentes nas duas ordens (128 identidades
racionais), sem ajuste de coeficiente. Três controles detectam omitir
D_Xh_X, retirar a fonte e inverter seu sinal. A divergência de frame foi
auditada por conversão independente para coordenadas (84 identidades).
Fonte: 128 verificações; reconstrução dos laços: 480 verificações.

**Alcance:** paga a identidade não coincidente deste truncamento. O
resíduo anterior com D_Xh=0 não testava a identidade forte completa.
Faltam contatos da extensão temporal, parte suave geral, ordem K²,
contribuições locais restantes e demais aridades para declarar Q2/WZ e
sua classe. A própria saída dos laços preserva o rótulo de candidato;
a auditoria e a soma posteriores estão em arquivos novos, sem apagar
aquele estado. Gate e originais intactos.

## Auditoria das contribuições Kimi

- Quártico: o vértice concorda exatamente com o existente em 12 exemplos
  densos. Dois autotestes originais falharam: momento usado na ação de
  Lie e métrica total entregue a uma função que esperava perturbação.
  Controles independentes corrigidos passam, inclusive 12 Ward com
  momento ghost não nulo. Foram 35 verificações; nenhum vértice foi
  alterado. O antigo gerador de momentos tornava o ghost zero em todos
  os exemplos. Um controle sqrt(det) antigo era float, registrado como
  tal, sem promovê-lo a identidade racional.
- Dicionário radial: 48 verificações locais, 16 contraexemplos aos
  sinais/fatores mistos e ao exemplo de derivar uma correção constante.
  A sugestão de acrescentar Kp0 a um símbolo homogêneo de quarta ordem
  não foi aceita sem escala adicional. A parte algébrica do operador de
  Lichnerowicz foi conferida; não é prova do matching bilocal inteiro.

## Orquestração e custo

Kimi referência harmônica, MiMo contatos angulares e DeepSeek adjunto
Einstein foram despachados e estão simultaneamente em execução segundo
o recibo da coordenação. Kimi primitiva curva terminou, ainda DECLARADO
até auditoria local; sua resposta foi preservada para o próximo passo.
Preservados os pedidos já existentes, memória comum e uma execução por
unidade. MiMo 4bdcaf7f e 88e54d74 terminaram IncompleteRead: sem resposta/uso medido,
custo desconhecido, não zero; nenhuma repetição. Kimi radial recebido
com 317.871 tokens de entrada e 40.169 de saída (cache 312.064 informado).

Total desta entrega: {checks} verificações reportadas (contagens de
execução, não quantidade de teoremas), CPU {cpu}s. A tentativa antiga de
fonte foi encerrada só depois de a representação compacta equivalente
concluir; preserva 21 testes anteriores, rc-1 e limite inferior medido
de CPU 780,890625s, sem inventar duração final. Demonstração detalhada,
recibos e hashes em bilocal_bulk_closure_delivery/manifest.json.
Próximo ramo: extensão/contatos na prescrição fixada, dentro de A7.b.
''')
measure=O/'ENTREGA_016_MEDIDA_fonte_expandida_e_dicionario_radial.md'
write(measure,f'''[REAL — tentativas preservadas; cálculo seguinte executado sem mudar os coeficientes]

Data {now}; abertura SHA256 {opening}.

Fonte expandida: comando Python A4/symbolic_runtime/Scripts/python.exe
-X utf8 -B A7/bilocal_source_divergence_check.py, sessão35713, rc-1 após
encerramento pelo proprietário. Log SHA256 {sha(oldlog)}. Antes do
operador Einstein expandido passaram 21 verificações da fonte. CPU
medido >=780.890625s; total final desconhecido. Próximo ramo já executado:
source_einstein_radial_aux_check.py, mesma diferenciação com raio auxiliar,
rc0,128 verificações,39.53125CPU s; coeficientes Einstein preservados.

Kimi radial: dicionário não aceito como escrito. Auditoria local comando
Python A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/kimi_radial_operator_audit.py, rc0,48 verificações,16 contraexemplos.
Log SHA256 {sha(H/'kimi_radial_operator_audit_run.log')}. A soma bilocal
foi realizada diretamente por jatos covariantes, evitando a conversão
incorreta sugerida. Nenhuma nova camada baseada nessa sugestão.

MiMo job4bdcaf7f-031c-473c-ac20-fe31208e261d: IncompleteRead terminal.
Recibo SHA256 {sha(failure)}; tokens/custo desconhecidos, não zerados.
Preservado, sem repetição. A fila segue com outras unidades autorizadas.
''')
files += [report,measure,H/'bilocal_bulk_ward_closure/DERIVACAO.md',
 H/'source_einstein_radial_aux/DERIVACAO.md',
 H/'bilocal_source_divergence_check.py',H/'bilocal_source_divergence_engine.py',
 H/'bilocal_source_divergence/PRE_REGISTER.json',oldlog,
 H/'prepare_einstein_radial_aux.py',H/'prepare_full_pair_external_jets.py',
 H/'bilocal_external_jets_generation.json',D/'STOPPED_SOURCE_ATTEMPT.json',
 D/'MIMO_FAILURE_RECEIPT.json',D/'ORCHESTRATION_SNAPSHOT.json',
 D/'MIMO_SPARSE_FAILURE_RECEIPT.json',D/'KIMI_CURVED_WARD_RESPONSE.md',D/'KIMI_CURVED_WARD_RECEIPT.json']
files += [H/(n+'_run.log') for n in names]
files=list(dict.fromkeys(files))
put(D/'manifest.json',dict(at=now,opening_sha256=opening,checks=checks,
    completed_cpu_seconds=cpu,stopped_cpu_lower_bound=780.890625,
    all_local_cpu_lower_bound=cpu+780.890625,
    full_Q2=False,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
ledger=O/'LEDGER_016.jsonl'
events=[dict(at=now,event='A7_BILOCAL_BULK_WARD_THROUGH_FIRST_K_DELIVERED',target='A7.b',
    checks=checks,cpu_seconds=cpu,stopped_cpu_lower_bound=780.890625,full_Q2=False,
    delivery_manifest_sha256=sha(D/'manifest.json')),
 dict(at=now,event='KIMI_QUARTIC_LOCAL_AUDIT_COMPLETED',target='A7.b',provider='kimi',
      job_id='96648157-7424-49ad-b606-6cafe72b9988',remote_call=False,
      audit_manifest_sha256=sha(H/'kimi_quartic_local_audit/manifest.json')),
 dict(at=now,event='KIMI_RADIAL_RECEIVED_AND_LOCAL_AUDIT_COMPLETED',target='A7.b',provider='kimi',
      job_id=radial['job_id'],execution_task_id=radial['execution_task_id'],
      tokens=radial['usage'],cost_estimate_usd=None,cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO',
      response_sha256=radial['response_sha256'],audit_manifest_sha256=sha(H/'kimi_radial_operator_audit/manifest.json')),
 dict(at=now,event='MIMO_COINCIDENT_JETS_TERMINAL_FAILURE_RECEIVED',target='A7.b',provider='mimo',
      job_id=failed['job_id'],execution_task_id=failed['execution_task_id'],error=failed['error'],
      tokens=None,cost_estimate_usd=None,cost_status='UNKNOWN_NOT_ZERO',
      receipt_sha256=sha(failure),retried=False)]
events += [dict(at=now,event='MIMO_SPARSE_WICK_TERMINAL_FAILURE_RECEIVED',target='A7.b',provider='mimo',
    job_id=sparse_failure['job_id'],execution_task_id=sparse_failure['execution_task_id'],
    error=sparse_failure['error'],tokens=None,cost_estimate_usd=None,cost_status='UNKNOWN_NOT_ZERO',
    receipt_sha256=sha(new_failure),retried=False),
 dict(at=now,event='KIMI_CURVED_WARD_RECEIVED_PENDING_LOCAL_AUDIT',target='A7.b',provider='kimi',
    job_id=curved['job_id'],execution_task_id=curved['execution_task_id'],tokens=curved['result']['usage'],
    cost_estimate_usd=None,cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO',
    response_sha256=sha(D/'KIMI_CURVED_WARD_RESPONSE.md'),status='DECLARADO_PENDING_LOCAL_AUDIT')]
write(ledger,ledger.read_bytes()+''.join(json.dumps(e)+'\n' for e in events).encode(),True)
parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
rows=[json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()]
for r in rows:
    ix=ids(r)
    for k in ix[1:]:parents[root(k)]=root(ix[0])
known={}
for r in rows:
    ix=ids(r);cost=r.get('cost_estimate_usd',r.get('cost_usd',r.get('custo_usd')))
    if ix and cost is not None:known[root(ix[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(at=now,known_partial_usd=str(total),unknown_not_zero=True,
    ledger_sha256=sha(ledger),subscription_not_priced_as_zero=True))
p=O/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n- {now} A7.b PROGRESS: identidade Ward bilocal não coincidente até O(K) paga no recorte; 128 igualdades tensoriais/3controles; Q2 completa OPEN. Auditorias e motores: {checks}checks,CPU{cpu}s; tentativa encerrada >=780.890625CPU s adicional. Kimi/MiMo/DeepSeek em execução simultânea relatada. Custo parcial US${total}; desconhecidos não zerados.\n'.encode(),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',own_live_processes=[],
    bilocal_bulk_ward_manifest=str(D/'manifest.json'),partial_metered_cost_usd=str(total),
    off_diagonal_Ward_first_curvature=True,quantum_anomaly_computed=False,
    completed_this_turn=['Full external h/Dh bilocal loop computed; source independently computed',
        '128 symbolic Ward identities modulo z=X² through O(K), three negative controls',
        'Kimi quartic agrees existing vertex; selftest defects isolated without modifying vertex',
        'Kimi radial dictionary selected errors measured; not incorporated',
        'Slow source attempt stopped only after exact compact replacement succeeded'],
    next=['Extend the same bilocal identity with fixed regulator; contact coefficients, smooth W and remaining arities still required',
          'Receive independent Kimi/MiMo/DeepSeek audits; do not append local answers to independent prompts',
          'A7.b deadline approx2026-09-25T20:32Z; then A7.c/d,A8,PartB and final audit'],
    pending_orchestration='Single coordinator; Kimi98e09 completed pending local audit; MiMo88e54 failed; Kimi d0fd/MiMo7f606/DeepSeek2529 running; Kimi9118 registered; staging accepted',
    latest_live_execution=dict(status='COORDINATOR_OWNED_NO_OWN_PROCESS',
        kimi_job='d0fd9aa9-1d09-451e-867b-a9e34ed775bb',mimo_job='7f606d88-ac59-4940-9bb0-d7be6ba306ea',
        deepseek_job='25292039-6bed-4b01-a788-cef4e7bfe55e',
        remote_status_source=str(D/'ORCHESTRATION_SNAPSHOT.json')),
    kimi_radial_local_audit=str(H/'kimi_radial_operator_audit/manifest.json'),
    source_einstein_manifest=str(H/'source_einstein_radial_aux/manifest.json'))
put(p,v,True)
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:
    assert sha(Path(row['path']))==row['sha256'],row['path']
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,stopped_cpu_lower_bound=780.890625,
    artifacts=len(files),known_partial_usd=str(total),goal='ACTIVE',full_Q2=False)))
