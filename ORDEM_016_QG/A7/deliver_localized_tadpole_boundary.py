"""Record the localized current calculation and a blocked review dispatch."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;D=H/'localized_tadpole_boundary_jets_v2';O=H.parents[1]/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(o):return json.dumps(o,ensure_ascii=False,indent=2).encode()
def append(p,s):write(p,p.read_bytes()+s.encode())
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
r=json.loads((D/'results.json').read_bytes());prior=json.loads((H/'localized_tadpole_boundary_jets/results.json').read_bytes());opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
log=H/'localized_tadpole_boundary_jets_v2_run.log';oldlog=H/'localized_tadpole_boundary_jets_run.log'
catalog=H/'orchestration_localized_boundary/prepared_units.json';blocked=H/'orchestration_localized_boundary/AUTO_REVIEW_BLOCK.json'
m=D/'delivery_manifest.json';assert not m.exists()
write(m,dump(dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds_exact=r['cpu_seconds'],cpu_seconds_prior_float=prior['cpu_seconds'],rc=0,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in [D/'manifest.json',D/'DERIVACAO.md',log,oldlog,catalog,blocked,Path(__file__)]],full_Q2=False,gate_changed=False)))
ledger=O/'LEDGER_016.jsonl';rows=[json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()]
append(ledger,json.dumps(dict(at=now.isoformat(),event='LOCALIZED_EH_TADPOLE_BOUNDARY_JETS',target='A7.b',checks=r['checks'],cpu_seconds=r['cpu_seconds'],prior_float_run_cpu_seconds=prior['cpu_seconds'],manifest_sha256=sha(m),remote_call=False))+'\n')
append(ledger,json.dumps(dict(at=now.isoformat(),event='REVIEW_DISPATCH_AUTO_REVIEW_BLOCKED',provider='deepseek',target='A7.b',request_id='70e9e188-471f-412d-848f-bf0ecc7d51c4',remote_call=False,job_id=None,status='AWAITING_SPECIFIC_USER_APPROVAL',evidence_sha256=sha(blocked)))+'\n')
seen=set();total=Decimal(0)
for e in rows:
 key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');val=e.get('cost_estimate_usd',e.get('cost_usd'))
 if val is not None and (key is None or key not in seen):
  total+=Decimal(str(val))
  if key:seen.add(key)
note=f'''[DERIVED — tadpole suave localizado com corrente EH completa]

{now.isoformat()}. Abertura SHA256 {opening}.

Composto T_boundary=Q.b4. A partição em momentos internos identifica
W20,W02 antes da integração por partes, ausentes na parcela GammaGamma.
A mesma ação escreve -ell.b4 com ell=-Q, isto é, derivada de chi vezes
corrente; não se apagam jatos nem se presume cutoff constante.
Controle A=e00,B=e11,U=V=e00: parcela W02=-15/8 e soma de fronteira=-9/8.

1321 controles racionais,48 fibras com segunda derivada na mesma perna,
CPU {r['cpu_seconds']}s, rc0. A primeira execução usou divisão int/int
e produziu floats; preservada, CPU{prior['cpu_seconds']}s. v2 força
Fraction e rejeita floats; é a evidência exata.
Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/localized_tadpole_boundary_jets_check_v2.py.
Log SHA256 {sha(log)}. Derivação {D/'DERIVACAO.md'}.
Manifesto {m}; SHA256 {sha(m)}.

Revisão DeepSeek preparada com memória comum e três motores. Prévia
selected=deepseek. Despacho bloqueado pela revisão automática por exigir
autorização específica de envio de código; pergunta ao operador pendente.
Não houve submissão, chamada remota nem contorno do bloqueio.
Catálogo {catalog}. Kimi permanece bloqueado por cota; última nova
unidade MiMo falhou no cofre antes da rede, conforme diagnóstico da coordenação.

Parcial monetário conhecido US${total}; assinaturas/despesas desconhecidas
não convertidas em zero. Kernel e gate intactos. Q2 integral OPEN.
Próximo: conferir contatos localizados do produto singular na prescrição
fixada, preservando a separação deste tadpole de um vértice.
'''
p=O/'ENTREGA_016_A7b_jatos_fronteira_tadpole_localizado.md';assert not p.exists();write(p,note.encode())
p=O/'ENTREGA_016_MEDIDA_divisao_float_tadpole_fronteira.md';assert not p.exists();write(p,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: corrente EH+tadpole localizado,1321checks exatos CPU{r["cpu_seconds"]}s; rodada float preservada CPU{prior["cpu_seconds"]}s; revisão DeepSeek preparada e bloqueada; parcial US${total}.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['Kimi endpoint review104checks','MiMo frame/connection review1116checks','Full EH localized smooth tadpole second jets1321checks'],
 localized_tadpole_boundary_manifest=str(m),partial_metered_cost_usd=str(total),
 pending_specific_egress_approval=dict(request_id='70e9e188-471f-412d-848f-bf0ecc7d51c4',catalog=str(catalog),remote_sent=False),
 next=['Await explicit egress reply for DeepSeek unit; no submission before approval',
       'Continue localized singular two-vertex contacts, using full EH boundary; do not repeat smooth tadpole',
       'Unread Kimi9118 nonlocal source adjoint review remains',
       'A7b deadline20:32Z; A7c/d,A8,PartB and final remain'],own_live_processes=[])
write(p,dump(c));print(json.dumps(dict(delivery=str(m),checks=r['checks'],partial_cost=str(total))))
