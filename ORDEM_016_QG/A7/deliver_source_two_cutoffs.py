"""Publish the two-endpoint source assembly and orchestration receipt."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'source_two_cutoff_assembly';O=H.parents[1]/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(o):return json.dumps(o,ensure_ascii=False,indent=2).encode()
def append(p,s):write(p,p.read_bytes()+s.encode())
for folder in [D,H/'source_Y_cutoff_v2']:
 for row in json.loads((folder/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
r=json.loads((D/'results.json').read_bytes());y=json.loads((H/'source_Y_cutoff_v2/results.json').read_bytes())
q=s.symbols('q0:4');lam=s.Symbol('lam');loc={'lam':lam,**{str(t):t for t in q}}
vals=[]
for row in r['controls']:
 f=s.sympify(row['polynomial'],locals=loc);vals.append(s.expand(f.subs(dict(zip(q,(2,1,0,0)))).subs(lam,1))
assert vals==[-s.Rational(29,32),-s.Rational(17,120),-s.Rational(79,160)]
assert vals[1]-vals[0]==s.Rational(367,480) and vals[2]-vals[0]==s.Rational(33,80)
neg=D/'NEGATIVE_CONTROLS.json';assert not neg.exists();write(neg,dump(dict(q=[2,1,0,0],lambda_value=1,values=[str(v) for v in vals],omit_Y_differences=[str(v-vals[0]) for v in vals[1:]],checks=3)))
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
receipt=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/worker_resumed_kimi_mimo_20260925.json'
rp=D/'ORCHESTRATION_RECEIPT.json';assert not rp.exists();write(rp,receipt.read_bytes())
catalog=H/'orchestration_two_endpoint_source/prepared_units.json'
artifacts=[D/'manifest.json',D/'DERIVACAO.md',D/'NEGATIVE_CONTROLS.json',rp,H/'source_Y_cutoff_v2/manifest.json',
 H/'source_Y_cutoff_run.log',H/'source_Y_cutoff_v2_run.log',H/'source_two_cutoff_assembly_run.log',catalog,Path(__file__)]
m=D/'delivery_manifest.json';assert not m.exists();write(m,dump(dict(at=now.isoformat(),opening_sha256=opening,checks=y['checks']+r['checks']+3,
 cpu_seconds=y['cpu_seconds']+r['cpu_seconds'],failed_v1_cpu_seconds_total=None,failed_v1_checkpoint_cpu_seconds=json.loads((H/'source_Y_cutoff/B_COEFFICIENTS.json').read_bytes())['cpu_seconds'],
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in artifacts],full_Q2=False)))
ledger=O/'LEDGER_016.jsonl';rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
append(ledger,json.dumps(dict(at=now.isoformat(),event='SOURCE_TWO_ENDPOINT_CUTOFF_ASSEMBLY',target='A7.b',checks=y['checks']+r['checks']+3,cpu_seconds=y['cpu_seconds']+r['cpu_seconds'],failed_attempt=dict(rc=1,cpu_seconds_total=None,log_sha256=sha(H/'source_Y_cutoff_run.log')),manifest_sha256=sha(m),remote_call=False))+'\n')
append(ledger,json.dumps(dict(at=now.isoformat(),event='SCIENTIFIC_REVIEW_DISPATCH_ACCEPTED',target='A7.b',provider='mimo',request_id='d946bf96-9eaf-4263-bffb-fc8e1f7e688f',job_id='f7f59797-7201-44a1-a4e5-25c7e748a01f',status='RUNNING_PER_COORDINATOR_RECEIPT',cost_estimate_usd=None,receipt_sha256=sha(rp),prompt_catalog_sha256=sha(catalog),execution_owner='coordinator',remote_call_by_this_script=False))+'\n')
total=Decimal(0);seen=set()
for e in rows:
 key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');val=e.get('cost_estimate_usd',e.get('cost_usd'))
 if val is not None and (key is None or key not in seen):
  total+=Decimal(str(val))
  if key:seen.add(key)
start=datetime.fromisoformat(json.loads((H/'source_Y_cutoff/PRE_REGISTER.json').read_bytes())['at']);wall=(now-start).total_seconds()
note=f'''[DERIVED — fonte plana localizada nos dois extremos; soma Q2 ainda OPEN]

{now.isoformat()}. Abertura SHA256 {opening}.

Reconstruído B no acoplamento A.c+B.Dc: coeficientes
(-2,-4,-4,16,-8,20,0) na base explicitada na derivação.
Recupera C=A-divY B e os jatos do motor original.
O contato de Y tem coeficientes (-1/16,1/6,0) na base rank3.

Com H=chiY C-(dchiY).B, a identidade exata do comparador é
P-Q=-C_E(chiX H)+E_X[chiX chiY D], onde D=C_divY(B).
Adjunção permanece exata; todos os contatos pertencem à extensão.
Omitir dchiY.B altera os dois controles em367/480 e33/80.

370+240+3 controles, CPU dos dois runners aprovados
{y['cpu_seconds']+r['cpu_seconds']}s, rc0. Intervalo de bancada registrado
{wall/3600:.6f}h entre pré-registro inicial e entrega; não é CPU.
v1 falhou por namespace AST incompleto, preservado; CPU total não medida.
Comandos: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/source_Y_cutoff_check_v2.py e A7/source_two_cutoff_assembly_check.py.
Manifesto {m}; SHA256 {sha(m)}. Logs e hashes no manifesto.
Derivação: {D/'DERIVACAO.md'}.

MiMo d946bf96 admitido como f7f59797, execução iniciada pela coordenação.
Kimi9c1fe22c retomado após diagnóstico oficial de limite de5horas;
não era saldo mensal. Recibo de processo84025 copiado, responsabilidade
da coordenação; não houve duplicação. DeepSeek70e9 permanece bloqueado.

Parcial conhecido US${total}, sem contabilizar como zero os usos pendentes.
Faltam a localização completa dos laços, curvatura/aridades e Q2 causal.
Nenhum original, kernel ou gate alterado. Próximo: aplicar a mesma regra
de dois cutoffs aos coeficientes h/Dh dos laços sem descartar B ou a
corrente EH já construída. Não refazer a extração da fonte.
'''
p=O/'ENTREGA_016_A7b_fonte_dois_cutoffs.md';assert not p.exists();write(p,note.encode())
p=O/'ENTREGA_016_MEDIDA_namespace_fonte_cutoffY.md';assert not p.exists();write(p,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: fonte plana dois cutoffs,613checks,CPU{y["cpu_seconds"]+r["cpu_seconds"]}s,bancada registrada{wall/3600:.6f}h; MiMo novo em execução e Kimi retomado; parcialUS${total}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['Unreduced flat source B reconstructed and verified','Both cutoff source contact P-Q assembled with613checks','Distinct MiMo review admitted;Kimi existing FIFO resumed'],
 source_two_cutoff_manifest=str(m),partial_metered_cost_usd=str(total),own_live_processes=[],
 pending_orchestration='MiMo f7f59797 and Kimi9c1fe22c running per coordinator receipt; DeepSeek70e9 remains BLOCKED pending specific approval.',
 orchestration_update='Kimi5hour limit diagnosed; public K3max recheck succeeded, block reconciled by coordinator; terminal efbb not retried. MiMo context recovered, new unit dispatched, terminal3e998 untouched.',
 latest_live_execution=dict(owner='coordinator',session_id=84025,receipt=str(rp)),
 next=['Keep DeepSeek70e9 blocked until explicit approval','Wait through coordinator for MiMo d946 and Kimi9c1fe22c; do not poll its exec session directly',
       'Localize metric/ghost loop h/Dh coefficients with two cutoffs and EH current, not source alone',
       'A7b deadline20:32Z; A7c/d,A8,PartB and full final remain'])
write(p,dump(c));print(json.dumps(dict(delivery=str(m),checks=613,partial_cost=str(total))))
