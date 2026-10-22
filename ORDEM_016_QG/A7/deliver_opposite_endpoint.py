"""Publish measured current placement and orchestration receipts, append-only."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
OUT=ROOT/'TUNEL/DO_CHATGPT';BASE=ROOT/'IALD_ORQUESTRACAO_20260923'
D=H/'opposite_endpoint_delivery';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,raw,existing=False):
    if p.exists():
        assert existing
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);assert not bak.exists()
        bak.write_bytes(old);assert bak.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);temp.write_bytes(raw)
    assert raw and temp.read_bytes()==raw;temp.replace(p)
def put(p,value,existing=False):write(p,json.dumps(value,ensure_ascii=False,indent=2).encode('utf-8'),existing)
def text(p,value):write(p,value.encode('utf-8'))
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
receipt=BASE/'state/handoffs/a7_opposite_endpoint_pending_submissions.json'
accepted=json.loads(receipt.read_bytes())
for unit in accepted['units']:
    assert sha(Path(unit['payload']))==unit['payload_sha256']
write(H/'orchestration_opposite_endpoint/coordinator_acceptance.json',receipt.read_bytes())
results=json.loads((H/'opposite_endpoint_current/results.json').read_bytes())
ledger=OUT/'LEDGER_016.jsonl'
oldrows=[json.loads(line) for line in ledger.read_text('utf-8').splitlines()]
new_events=[]
received=BASE/'state/handoffs/46168c27-1701-4329-9073-b908ffa51fd5_delivery.json'
raw=json.loads(received.read_bytes());job=raw['job'];execution=job['execution'];result=execution['result']
intake=H/'kimi_smooth_twojet_review';intake.mkdir(exist_ok=False)
write(intake/'RECEIPT.json',received.read_bytes())
text(intake/'RESPONSE.md',result['text'])
put(intake/'INTAKE.json',dict(at=now.isoformat(),scientific_status='DECLARADO_PENDING_LOCAL_REVIEW',
    job_id=job['id'],request_id=job['request_id'],execution_task_id=execution['id'],
    receipt_sha256=sha(intake/'RECEIPT.json'),response_sha256=sha(intake/'RESPONSE.md'),usage=result['usage']))
if not any(row.get('execution_task_id')==execution['id'] for row in oldrows):
    new_events.append(dict(at=now.isoformat(),event='KIMI_SMOOTH_TWOJET_RECEIVED_PENDING_REVIEW',
        target='A7.b',provider='kimi',job_id=job['id'],request_id=job['request_id'],
        execution_task_id=execution['id'],usage=result['usage'],provider_elapsed_seconds=result['elapsed_seconds'],
        cost_estimate_usd=None,cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO',
        prompt_sha256=hashlib.sha256(job['prompt'].encode('utf-8')).hexdigest(),
        response_sha256=sha(intake/'RESPONSE.md'),receipt_sha256=sha(intake/'RECEIPT.json'),
        scientific_status='DECLARADO_PENDING_LOCAL_REVIEW',remote_call_by_this_script=False))
cost=Decimal(0);seen=set()
for row in oldrows+new_events:
    value=row.get('cost_estimate_usd')
    if value is None:value=row.get('cost_usd')
    if value is None:continue
    key=row.get('execution_task_id') or row.get('job_id') or row.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(value))
report=f'''[DERIVED — controles exatos da corrente no extremoX; identidade geral/Q2 OPEN]

A montagem anterior incluía correntes emY e tinha resíduo-14928/117649 no
controle h11,c0,x=(1,2,-1,1),lambda=e0-e1,eta=e0, jatos exponenciais completos.
Construímos as duas inserções que faltavam nessa distribuição de pernas:
corrente métrica h_X h_X c_X e corrente b_X h_X c_X, contra Vghost_Y.
O h externo fica emX; o c externo fica emY. Não é uma troca dos rótulos
do cálculo antigo: o ghost da corrente agora contrai com barc_Y.

Convenções fixadas antes da execução:
Cmetric_real=+dchiX.Jraw/(16kappa); GD=-4kappa S f;
Gbh=-G^T(d)f; <c_X barc_Y>=f. O1/2 da Hessiana é cancelado pelas
duas escolhas do h externo. A adjunção dos jatos externos é
prod_i[-(d_i+lambda_i)] prod_j[d_j-eta_j]. Retidos h'' e todos
os fatores de Leibniz; nenhuma normalização escolhida para zerar resíduo.

Resultados exatos no controle não trivial:
* corrente métrica emX:15194/117649;
* corrente mista emX:-38/16807;
* soma:-14928/117649+15194/117649-38/16807=0.
Os dois controles com lambda0 também permanecem zero.
Há350 termos métricos e132 mistos após agregação;46 termos métricos
contêm segunda derivada EXTERNA de h, omitida por um leitor limitado a h,h'.

{results['checks']} verificações:75 identidades do operador adjunto até
h''/c',6 avaliações por dois métodos (Leibniz em linhas versus derivar
produto explícito),2 controles de dchiX0. CPU{results['cpu_seconds']}s,rc0.
Isso demonstra os valores e a consistência da adjunção nesses controles;
não prova cancelamento em todos os tensores/pontos, nem extensão diagonal,
curvatura, parte suave, ordens superiores ou QME completa. Gate inalterado.
Próximo: variar componentes/pontos e calcular os contatos da montagem completa.

Orquestração: novas unidades Kimi bd8796b3 e MiMo24ad1812 aceitas em staging
pela coordenação única, após FIFO existente; ambas prévias selecionam o
provedor exigido. Staging não é execução. Kimi218c concluiu; resposta integral
preservada em kimi_smooth_twojet_review, ainda DECLARADO, sem auditoria local.
Consumo desse resultado registrado uma vez no ledger; custo de assinatura
desconhecido, não zero. Custo monetário conhecido parcial recontadoUS${cost}.

Comando:A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/opposite_endpoint_current_check.py.
Log:{H/'opposite_endpoint_current_run.log'};sha256={sha(H/'opposite_endpoint_current_run.log')}.
Abertura sha256:{opening}.
'''
text(D/'DERIVACAO.md',report)
text(OUT/'ENTREGA_016_A7b_corrente_no_extremo_X.md',report)
artifacts=[Path(__file__),D/'DERIVACAO.md',OUT/'ENTREGA_016_A7b_corrente_no_extremo_X.md',
 H/'opposite_endpoint_current_engine.py',H/'opposite_endpoint_current_check.py',
 H/'opposite_endpoint_current_run.log',H/'opposite_endpoint_current/manifest.json',
 H/'opposite_endpoint_current/results.json',H/'opposite_endpoint_current/PRE_REGISTER.json',
 H/'prepare_opposite_endpoint_reviews.py',H/'orchestration_opposite_endpoint/manifest.json',
 H/'orchestration_opposite_endpoint/coordinator_acceptance.json',intake/'INTAKE.json']
put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,checks=results['checks'],
 cpu_seconds=results['cpu_seconds'],known_partial_usd=str(cost),Q2=False,gate_changed=False,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in artifacts]))
new_events.append(dict(at=now.isoformat(),event='OPPOSITE_ENDPOINT_CURRENT_CONTROL_ZERO',target='A7.b',
 checks=results['checks'],cpu_seconds=results['cpu_seconds'],manifest_sha256=sha(D/'manifest.json'),remote_call=False))
write(ledger,ledger.read_bytes()+b''.join((json.dumps(row,ensure_ascii=False)+'\n').encode('utf-8') for row in new_events),True)
cont=H/'CONTINUIDADE.json';value=json.loads(cont.read_bytes());elapsed=(now-datetime.fromisoformat(value['at'])).total_seconds()/3600
value.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_processes=[],
 opposite_endpoint_manifest=str(D/'manifest.json'),opposite_endpoint_review_catalog=str(H/'orchestration_opposite_endpoint/prepared_units.json'),
 pending_scientific_review=str(intake/'RESPONSE.md'),pending_scientific_review_intake=str(intake/'INTAKE.json'),
 completed_this_turn=['Two new complementary model units accepted in staging; provider routes verified',
 'Constructed metric and b currents at X against ghost vertex Y',
 'All three sampled full-current assembly residuals zero without fitting;83 exact checks'],
 next=['Check additional tensor/ghost components and nonaxial points in full-current assembly',
 'Compute extension contacts including opposite-endpoint currents; do not infer fullQ2 from sampled zeros',
 'Audit Kimi smooth_twojet response; preserve blind FIFO reviews and MiMo running',
 'A7b deadline20:32UTC;A7c/d,A8,ORDEM015PartB and final audit remain'])
put(cont,value,True)
progress=OUT/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\r\n- {now.isoformat()} A7.b PROGRESS:83checks,correnteX cancela resíduo do controle XY sem ajuste;CPU{results["cpu_seconds"]}s;bancada{elapsed:.6f}h;2novas unidades em staging;parcialUS${cost};Q2 OPEN.\r\n'.encode('utf-8'),True)
for entry in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(entry['path']))==entry['sha256']
print(json.dumps(dict(manifest=str(D/'manifest.json'),verified_artifacts=len(artifacts),checks=results['checks'],
 cpu_seconds=results['cpu_seconds'],known_partial_usd=str(cost),kimi_usage=result['usage'])))
