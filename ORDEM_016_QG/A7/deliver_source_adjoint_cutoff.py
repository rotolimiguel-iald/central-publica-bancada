"""Deliver one bounded source-contact calculation and audit receipt."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;D=H/'source_adjoint_cutoff';O=H.parents[1]/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def append(p,s):write(p,p.read_bytes()+s.encode())
def dump(o):return json.dumps(o,ensure_ascii=False,indent=2).encode()
for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
r=json.loads((D/'results.json').read_bytes());rec=json.loads((D/'RECEIPT.json').read_bytes())
p=H/'orchestration_nonlocal_followup/kimi_a7_nonlocal_source_adjoint_orientation_submit.json';payload=json.loads(p.read_bytes())
assert payload['request_id']=='98f65f67-75c3-478d-935b-00edf1f7baa8'
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md');log=H/'source_adjoint_cutoff_run.log'
m=D/'delivery_manifest.json';assert not m.exists();write(m,dump(dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds=r['cpu_seconds'],rc=0,
 artifacts=[dict(path=str(q),sha256=sha(q)) for q in [D/'manifest.json',D/'DERIVACAO.md',log,p,Path(__file__)]],full_Q2=False)))
ledger=O/'LEDGER_016.jsonl';rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
assert not any(x.get('execution_task_id')==rec['execution_task_id'] for x in rows)
e=dict(at=now.isoformat(),event='MODEL_REVIEW_RECEIVED_AND_AUDITED',provider='kimi',target='A7.b',branch='nonlocal_source_adjoint_orientation',
 request_id=payload['request_id'],job_id=rec['job_id'],execution_task_id=rec['execution_task_id'],usage=rec['result']['usage'],cost_estimate_usd=None,
 cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO',prompt_sha256=hashlib.sha256(payload['prompt'].encode()).hexdigest(),payload_sha256=sha(p),
 response_sha256=sha(D/'RESPONSE.md'),receipt_sha256=sha(D/'RECEIPT.json'),scientific_status='ADJOINT_CONTACT_CONFUSION_AND_SOURCE_DENSITY_CORRECTED',remote_call_by_this_script=False)
append(ledger,json.dumps(e,ensure_ascii=False)+'\n');rows.append(e)
append(ledger,json.dumps(dict(at=now.isoformat(),event='SOURCE_ADJOINT_CUTOFF_FIRST_JET',target='A7.b',checks=r['checks'],cpu_seconds=r['cpu_seconds'],manifest_sha256=sha(m),remote_call=False))+'\n')
seen=set();total=Decimal(0)
for e in rows:
 key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('cost_usd'))
 if v is not None and (key is None or key not in seen):
  total+=Decimal(str(v))
  if key:seen.add(key)
note=f'''[DERIVED — contato de primeiro jato do cutoff na fonte plana; auditoria de orientação]

{now.isoformat()}. Abertura SHA256 {opening}.

Adjunção distribucional é exata: <E U,T>=<U,E T>. O contato adicional
pertence à diferença R(Ef)-E R(f), não à adjunção de U já estendido.
O parecer Kimi9118 confundia essas duas comparações. A fórmula de
densidade externa que apontava como ausente já estava na bancada.
Os contatos de log z podem ser não nulos na quarta derivada.

Calculado o novo termo de primeiro jato do cutoff para a fonte plana
efetiva C_ab,r. A extração por regulador e a regra de Leibniz com
contatos de primeira derivada coincidem. Para r=0,b=e0,ab=11,q=e0,
o coeficiente de contato é -5/128 em unidades C_E=-4pi².
São28 componentes não nulas nas duas direções de cutoff verificadas.

674 controles exatos, CPU{r['cpu_seconds']}s, rc0.
Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/source_adjoint_cutoff_check.py.
Log SHA256 {sha(log)}. Derivação {D/'DERIVACAO.md'}.
Manifesto {m}; SHA256 {sha(m)}.

Escopo: estágio X da fonte, K0. Faltam a contribuição do cutoff em Y
antes de reduzir B.Dc, a composição completa dos vértices e as aridades
restantes. Q2 integral OPEN. Nenhum original, kernel ou gate alterado.
Próxima operação: K_chiY=chiY(A-divY B)-(dchiY).B; conservar os dois
termos antes de aplicar E_X e R. Não substituir pelo primeiro sozinho.

Nenhuma chamada remota nova. Parcial conhecido do ledger US${total};
assinatura Kimi sem valor monetário informado. Envio DeepSeek70e9 ainda
aguarda autorização específica após bloqueio automático, sem despacho.
'''
target=O/'ENTREGA_016_A7b_adjunto_fonte_e_primeiro_jato_cutoff.md';assert not target.exists();write(target,note.encode())
measure=O/'ENTREGA_016_MEDIDA_adjunto_nao_e_comutacao.md';assert not measure.exists();write(measure,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: adjunção corrigida e contato do primeiro jato de cutoff na fonte plana,674checks CPU{r["cpu_seconds"]}s; parcial conhecido US${total}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['Kimi9118 adjoint review audited','Source X cutoff first-jet contact independently extracted;674checks'],
 source_adjoint_cutoff_manifest=str(m),partial_metered_cost_usd=str(total),
 next=['Keep DeepSeek70e9 blocked until explicit specific egress approval',
       'Compute Y cutoff source term -(dchiY).B before E_X and R, using existing bilocal source engine',
       'Compose localized singular pair with full EH boundary; retain actual two-vertex cutoff factors',
       'A7b deadline20:32Z; A7c/d,A8,PartB and full final audit remain'],own_live_processes=[])
write(p,dump(c));print(json.dumps(dict(delivery=str(target),checks=r['checks'],partial_cost=str(total))))
