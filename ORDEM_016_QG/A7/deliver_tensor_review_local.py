"""Record the received review, local corrections and staged provider tasks."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    b=v if isinstance(v,bytes) else (v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)).encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bak=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
job='9eefec6b-74ed-41c0-a50f-d5098179eba0'
receipt=json.loads((H/f'received_reviews/{job}.json').read_bytes())
assert sha(H/f'received_reviews/{job}.md')==receipt['response_sha256']
audit=json.loads((H/'tensor_review_local/results.json').read_bytes())
units=json.loads((H/'orchestration_curved_source/prepared_units.json').read_bytes())
for u in units:assert sha(Path(u['payload']))==u['payload_sha256']
text=f'''[REAL — leitura integral e CAS exato; DERIVED — condicionado às famílias meromorfas; OPEN — Q2 curva]
# A7.b — revisão Kimi dos contatos, incorporada com correções
Abertura SHA256 `{opening}`. UTC {now}.

Recebido Kimi K3 máximo, job {job}, execução {receipt['execution_id']}.
Resposta SHA256 `{receipt['response_sha256']}`. A resposta é DECLARADO até auditoria;
seu parecer favorável não substitui prova distribucional ou a soma causal completa.
Uso: {receipt['result_metadata']['usage']}. Custo não informado; não é zero.

**O que permanece.** A recorrência meromorfa, os resíduos, o tensor de posto dois
e o contato que corrige seu traço continuam compatíveis com os cálculos existentes.
O relatório original já declarava os insumos analíticos e o escopo de um par plano.
As 41 assertivas originais têm dependências comuns; não são 41 provas independentes.

**Correções ao parecer.**
1. Cancelar log(z)delta não é uma prova: o produto não foi definido. Não adotamos
essa rota nem os limites epsilon/z^k alegados sem demonstração. Basta a rota
meromorfa: zR_n=R_(n-1) e R_n=D_n+h_n Res U_n implicam
zD_n-D_(n-1)=(h_(n-1)-h_n)Res U_(n-1). Para n=3:3Cdelta/8.
2. Preservar R2=D2 determina g1=-1 em g(a)=1+g1 a+g2 a²+…;
não determina g(a) inteiro. Se U=r/a+v0+v1 a+…, FP(gU)=v0+g1r,
mas FP(gU')=v1-g2r. Portanto 1-a e 1-a+a² concordam na primitiva e
diferem no log por -r. A prescrição 1-a continua a já escolhida, sem ajuste novo.
3. A fórmula literal da seção2.2 do parecer duplica z^a. Corrigida, usa
mu^(2a)z^(-1+a); a duplicação altera a derivada por log(z)/z.

**Instância adicional.** Diferenciar U2(a) antes da parte finita dá
partial_mu U2=(-4+2a)x_mu U3. Logo

    partial_mu R2 - R(partial_mu z^-2)
      =2x_mu Res U3 =-(C/16)x_mu box delta =(C/8)partial_mu delta.

Não se usou multiplicação log(z)delta. CAS: {audit['checks']} assertivas formais,
rc0, CPU {audit['cpu_seconds']}s; não prova existência das distribuições.
Log e manifestação em A7/tensor_review_local. Nenhum original/gate alterado.

**Distribuição.** Coordenadora confirmou MiMo contact_bookkeeping iniciado;
Kimi marked_tensor_identity v2 registrado no job7af2e0e2-f377-4d51-87d3-db09350b51e4.
Os dois novos pacotes, Kimi curved_antifield_source e DeepSeek
logarithmic_contact_skeptic, tiveram rota prévia correta e staging confirmado.
Estão aguardando a ordem da fila; preparação não é execução. Um worker,
cinco pedidos não terminais e oito em staging no último status recebido.
Não repetimos falhas nem contaminamos revisões pendentes com o resultado desejado.
'''
report=O/'ENTREGA_016_A7b_revisao_Kimi_contatos.md';save(report,text)
files=[H/'tensor_review_local.py',H/'tensor_review_local_run.log',
 H/'tensor_review_local/PRE_REGISTER.json',H/'tensor_review_local/results.json',
 H/'tensor_review_local/manifest.json',H/f'received_reviews/{job}.md',
 H/f'received_reviews/{job}.json',report]
save(H/'tensor_review_local/delivery_manifest.json',dict(at=now,opening_sha256=opening,
 artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]))
ledger=O/'LEDGER_016.jsonl'
def event(e):
    rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
    if any(r.get('event')==e['event'] for r in rows):return
    save(ledger,ledger.read_bytes()+(json.dumps(e,ensure_ascii=False)+'\n').encode())
event(dict(event='A7_KIMI_TENSOR_CONTACT_RECEIVED_AND_REVIEWED',at=now,target='A-7.b',
 provider='kimi',job_id=job,request_id=receipt['request_id'],execution_id=receipt['execution_id'],
 prompt_sha256=receipt['prompt_sha256'],response_sha256=receipt['response_sha256'],
 usage=receipt['result_metadata']['usage'],cost_estimate_usd=None,new_external_execution=False,
 local_audit_checks=audit['checks'],local_cpu_seconds=audit['cpu_seconds'],report_sha256=sha(report)))
for u in units:
    payload=json.loads(Path(u['payload']).read_bytes())
    event(dict(event='A7_CURVED_SOURCE_STAGED_'+u['request_id'],at=now,target='A-7.b',
       provider=u['provider'],request_id=u['request_id'],status='PREVIEWED_COORDINATOR_STAGING_CONFIRMED',
       payload_sha256=sha(Path(u['payload'])),prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
       cost_estimate_usd=None,new_external_execution=False))
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()];parent={}
def root(k):
    parent.setdefault(k,k)
    if parent[k]!=k:parent[k]=root(parent[k])
    return parent[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
for r in rows:
    ix=ids(r)
    for k in ix[1:]:parent[root(k)]=root(ix[0])
known={}
for r in rows:
    ix=ids(r);v=r.get('cost_estimate_usd',r.get('cost_usd',r.get('custo_usd')))
    if ix and v is not None:known[root(ix[0])]=Decimal(str(v))
total=sum(known.values(),Decimal(0))
save(H/'tensor_review_local/COST_SNAPSHOT.json',dict(at=now,ledger_sha256=sha(ledger),
 total_known_partial=str(total),unknown_cost_not_zero=True,billing_not_verified=True))
cont=H/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d.update(at=now,status='ACTIVE',previous_goal_turn='PROGRESS',
 tensor_contact_review_manifest=str(H/'tensor_review_local/delivery_manifest.json'),
 pending_orchestration='Coordinator:5registered,8staging;MiMo contact_bookkeeping running;Kimi tensor review received',
 curved_source_catalog=str(H/'orchestration_curved_source/prepared_units.json'),
 partial_metered_cost_usd=str(total))
d['latest_orchestration']=dict(at=now,source='Official coordinator message,not a new provider poll',
 currently_executing='MiMo contact_bookkeeping',execution_job='fb3587cd-5807-4dab-9aa0-3ac178bc4deb',
 registered=5,staging=8,new_kimi_registered='7af2e0e2-f377-4d51-87d3-db09350b51e4')
d.setdefault('completed_this_turn',[]).append('Kimi tensor review fully read;21 conditional CAS assertions and invalid proof routes rejected;two new units staged')
save(cont,d)
p=O/'ENTREGA_016_PROGRESSO.md'
save(p,p.read_bytes()+f'\n- {now} — A7.b PROGRESSO: revisão Kimi completa,21assertivas locais,CPU{audit["cpu_seconds"]}s;dois novos pacotes Kimi/DeepSeek em staging,sem duplicação. Custo parcial conhecidoUS${total};custos ausentes desconhecidos. LedgerSHA256{sha(ledger)};abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(report),audit_checks=audit['checks'],cost_partial=str(total),status='ACTIVE')))
