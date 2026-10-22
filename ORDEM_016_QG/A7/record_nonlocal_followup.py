"""Record preparation/dispatch only; never promote queued reviews to results."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, uuid
H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT'
D=H/'orchestration_nonlocal_followup'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,update=False):
    if p.exists():
        assert update,p
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b and len(b)>0;t.replace(p);assert p.read_bytes()==b
def put(p,o,update=False):write(p,json.dumps(o,ensure_ascii=False,indent=2).encode(),update)
rows=json.loads((D/'prepared_units.json').read_bytes());now=datetime.now(timezone.utc).isoformat()
for r in rows:
    assert sha(Path(r['payload']))==r['payload_sha256']
    body=json.loads(Path(r['payload']).read_bytes())
    assert body['request_id']==r['request_id']
    assert body['execution_constraints']['required_provider']==r['provider']
    assert r['selected']==r['provider']
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
report=O/'ENTREGA_016_A7b_orquestracao_fonte_Fourier_gerador.md'
write(report,('''[REAL — preparação e prévia locais; OPEN — execução e revisão científicas]
# A7.b — novas unidades independentes para Kimi e MiMo
'''+f'Abertura SHA256 `{opening}`. UTC {now}.\n\n'+'''
O pedido do operador de ampliar a divisão, principalmente Kimi, foi encaminhado
à coordenação existente. Três unidades novas, no fim da ordem já registrada:

- Kimi: adjunção e orientação da imagem Einstein da fonte não local.
- Kimi: continuação meromórfica de Fourier, incluindo harmônicos sem resíduo local.
- MiMo: validade para toda ordem do gerador de Taylor covariante de primeira curvatura.

Os prompts têm fontes científicas explícitas, hashes lidos, uma pergunta cada,
executor obrigatório, memória comum e uma chamada por unidade. A prévia local
selecionou os três executores pedidos. Ela não chamou os modelos. O coordenador
recebeu o catálogo pela ferramenta oficial; só o recibo da fila demonstra registro
ou execução. Não se criou fila/worker nem se repetiu unidade antiga. Mantida a
independência: resultados do novo cálculo numérico não foram enviados aos revisores.

O catálogo guarda os request_id e os hashes de cada payload. A resposta externa
será DECLARADO até a verificação apropriada. Nenhum gate, original ou kernel mudou.
O cálculo local curved_pair_fourier_check.py continua na mesma sessão93180;
resultados parciais não são registrados como conclusão. Custos destas unidades
ainda não medidos, pois não foram executadas por esta preparação.
''').encode())
files=[Path(__file__),H/'prepare_nonlocal_followup_units.py',report]
files += sorted(p for p in D.glob('*.json') if p.name not in ('delivery_manifest.json',))
put(D/'delivery_manifest.json',dict(at=now,opening_sha256=opening,status='PREVIEWED_SENT_TO_COORDINATOR',
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in files],remote_execution_by_this_script=False))
ledger=O/'LEDGER_016.jsonl';raw=ledger.read_bytes()
existing=[json.loads(s) for s in raw.decode('utf-8-sig').splitlines() if s.strip()]
assert not any(e.get('event')=='A7_NONLOCAL_REVIEW_PREPARED' and e.get('request_id') in {r['request_id'] for r in rows} for e in existing)
events=[]
for r in rows:
    body=json.loads(Path(r['payload']).read_bytes())
    events.append(dict(at=now,event='A7_NONLOCAL_REVIEW_PREPARED',provider=r['provider'],target='A7.b',
        request_id=r['request_id'],lemma_id=r['lemma'],prompt_sha256=hashlib.sha256(body['prompt'].encode()).hexdigest(),
        payload_sha256=r['payload_sha256'],status='PREVIEWED_SENT_TO_COORDINATOR',remote_call=False,
        tokens=None,cost_estimate_usd=None))
write(ledger,raw+''.join(json.dumps(e)+'\n' for e in events).encode(),True)
p=O/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n- {now} A7.b: 2 novas unidades Kimi + 1 MiMo preparadas, fontes/hash/prévia conferidos e encaminhadas à fila existente. Sem execução remota nesta preparação; resultado científico pendente. Sessão local93180 preservada.\n'.encode(),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes())
v['at']=now;v['previous_goal_turn']='PROGRESS'
v['nonlocal_followup']=dict(catalog=str(D/'prepared_units.json'),request_ids=[r['request_id'] for r in rows],
    status='PREVIEWED_SENT_TO_COORDINATOR',after='orchestration_harmonic_followup')
v['next'].insert(0,'Confirm coordinator acceptance of three nonlocal_followup units; do not resubmit or reorder')
put(p,v,True)
print(json.dumps(dict(recorded=True,units=len(rows),manifest=str(D/'delivery_manifest.json'))))
