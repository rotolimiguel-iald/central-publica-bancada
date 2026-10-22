"""Publish the already-run endpoint audit without a remote call."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid

H=Path(__file__).resolve().parent
O=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'kimi_bilocal_pair_review'
now=datetime.now(timezone.utc)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
    if p.exists():
        old=p.read_bytes(); bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex)
        bak.write_bytes(old); assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(b); assert b and tmp.read_bytes()==b; tmp.replace(p)
def append(p,s): write(p,p.read_bytes()+s.encode('utf-8'))
def dump(d): return json.dumps(d,ensure_ascii=False,indent=2).encode('utf-8')

for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:
    assert sha(Path(a['path']))==a['sha256']
r=json.loads((D/'results.json').read_bytes())
assert r['checks']==104
receipt=json.loads((D/'RECEIPT.json').read_bytes())
payload_path=H/'orchestration_bilocal/kimi_a7_bilocal_pair_endpoint_ward_submit.json'
payload=json.loads(payload_path.read_bytes())
assert payload['request_id']=='542808c3-9cec-4f27-ba09-993ced9d6f98'
log=H/'kimi_bilocal_pair_review_run.log'
assert '104' in log.read_text('utf-8-sig')
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
delivery=D/'delivery_manifest.json'; assert not delivery.exists()
write(delivery,dump(dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds=r['cpu_seconds'],rc=0,
    full_Q2=False,gate_changed=False,artifacts=[dict(path=str(p),sha256=sha(p)) for p in
    [D/'manifest.json',D/'DERIVACAO.md',log,payload_path,Path(__file__)]])))
ledger=O/'LEDGER_016.jsonl'
rows=[json.loads(s) for s in ledger.read_text('utf-8-sig').splitlines() if s.strip()]
assert not any(a.get('execution_task_id')==receipt['execution_task_id'] for a in rows)
event=dict(at=now.isoformat(),event='MODEL_REVIEW_RECEIVED_AND_AUDITED',provider='kimi',target='A7.b',
    branch='bilocal_pair_endpoint_ward',request_id=payload['request_id'],job_id=receipt['job_id'],
    execution_task_id=receipt['execution_task_id'],usage=receipt['result']['usage'],cost_estimate_usd=None,
    cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO',prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),
    payload_sha256=sha(payload_path),response_sha256=sha(D/'RESPONSE.md'),receipt_sha256=sha(D/'RECEIPT.json'),
    scientific_status='PARTIAL_REVIEW_ENDPOINT_INDEX_AND_CONTACT_SCOPE_CORRECTED',remote_call_by_this_script=False)
append(ledger,json.dumps(event,ensure_ascii=False)+'\n');rows.append(event)
append(ledger,json.dumps(dict(at=now.isoformat(),event='BILOCAL_ENDPOINT_REVIEW_LOCAL_AUDIT',target='A7.b',
    checks=r['checks'],cpu_seconds=r['cpu_seconds'],manifest_sha256=sha(delivery),remote_call=False))+'\n')
seen=set(); total=Decimal(0)
for e in rows:
    key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
    val=e.get('cost_estimate_usd',e.get('cost_usd'))
    if val is not None and (key is None or key not in seen):
        total+=Decimal(str(val))
        if key:seen.add(key)
note=f'''[DERIVED — auditoria parcial, com correção de índice e alcance]

{now.isoformat()}. Abertura SHA256 {opening}.

O parecer Kimi soma a derivada em Y sobre o índice pertencente a X.
No objeto ghost(a,b)=G^a_b'(X,Y), a divergência correta em Y contrai b.
Em Y=0, o coeficiente de primeira curvatura é 4X_a/z; o comparador
ingênuo -partial_X dá 3X_a/z. Defeito +X_a/z. O exemplo original
calculou outra soma e seu coeficiente não vale para essa divergência.

O aviso contra substituir partial_Y por -partial_X permanece válido.
A tabela de contato de 1/z também não encerra a extensão do produto:
(R(partial_i z^-2)-partial_i R(z^-2))/C_E=-partial_i delta/8.
Uma derivada já produz contato nesse produto mais singular.

104 verificações exatas, CPU {r['cpu_seconds']}s, rc0.
Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/kimi_bilocal_pair_review_check.py.
Log SHA256 {sha(log)}. Manifesto {delivery}; SHA256 {sha(delivery)}.
Derivação completa: {D/'DERIVACAO.md'}.

O parecer não entregou a Ward completa do par; o resultado não coincidente
já demonstrado em bilocal_bulk_ward_closure permanece separado.
Próximo ramo: produtos localizados e seus contatos, incluindo fronteira EH.
Q2 integral OPEN. Sem mudança de originais ou gate, sem chamada repetida.
Custo da assinatura não informado; parcial monetário conhecido do ledger
US$ {total}, sem converter desconhecidos em zero.
'''
p=O/'ENTREGA_016_A7b_auditoria_Kimi_endpoint_bilocal.md';assert not p.exists();write(p,note.encode())
p=O/'ENTREGA_016_MEDIDA_Kimi_endpoint_e_contato_produto.md';assert not p.exists();write(p,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b MEDIDA/PROGRESS: Kimi endpoint corrigido,104checks CPU{r["cpu_seconds"]}s; contato de produto explicitado; Q2 OPEN; parcial conhecido US${total}.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),
    completed_this_turn=['Kimi bilocal endpoint review audited,104 exact checks'],
    kimi_bilocal_pair_review_manifest=str(delivery),partial_metered_cost_usd=str(total),
    pending_orchestration='MiMo c763 completed; next MiMo3e998 failed DPAPI, terminal. Kimi provider quota blocked; no retries.',
    next=['Audit MiMo c763 frame/index response; preserve cost discrepancy',
          'Compose local contacts with full EH boundary vertices',
          'A7b deadline20:32Z; A7c/d,A8,PartB and final remain'])
write(p,dump(c))
print(json.dumps(dict(delivery=str(delivery),checks=r['checks'],partial_known_cost=str(total))))
