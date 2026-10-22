"""Register the assembly without elevating a partial sum to full quantum anomaly."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;D=H/'assembled_contact_wz';O=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,new=False):
 if new:assert not p.exists(),p
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex)
  bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def append(p,v):write(p,p.read_bytes()+v.encode())
m=D/'manifest.json'
for row in json.loads(m.read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
r=json.loads((D/'results.json').read_bytes());log=H/'assembled_contact_wz_run.log'
assert json.loads(log.read_text('utf-8-sig').splitlines()[-1])==r
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds=r['cpu_seconds'],
 command='A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/assembled_contact_wz_check.py',rc=0,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in [m,log,D/'DERIVACAO.md',Path(__file__)]],full_Q2=False)
dm=D/'delivery_manifest.json';write(dm,json.dumps(manifest,ensure_ascii=False,indent=2).encode(),True)
ledger=O/'LEDGER_016.jsonl';append(ledger,json.dumps(dict(at=now.isoformat(),event='ASSEMBLED_CONTACT_FREE_BRST_CONSISTENCY',
 target='A7.b',checks=r['checks'],cpu_seconds=r['cpu_seconds'],remote_call=False,manifest_sha256=sha(dm)))+'\n')
seen=set();cost=Decimal(0)
for line in ledger.read_text('utf-8-sig').splitlines():
 if not line.strip():continue
 v=json.loads(line);z=v.get('cost_estimate_usd')
 if z is None:z=v.get('cost_usd')
 if z is None:continue
 k=v.get('execution_task_id') or v.get('job_id') or v.get('request_id')
 if k and k in seen:continue
 if k:seen.add(k)
 cost+=Decimal(str(z))
note=f'''[DERIVED — soma de contatos consistente sob BRST livre; Q2 integral OPEN]

{now.isoformat()}. Abertura SHA256 {opening}.

Reunidos os operadores já derivados: N=N_s+N_W e a fonte R_W.
A primitiva localizada é Bchi=-C_E[<chi h,Nh>/2+<chi hdagger,R_Wc>].
Sua variação mantém todos os termos do cutoff:

    Achi=-s0Bchi=C_E<h,Mchi Gc+E(chi R_Wc)>,
    Mchi=(chiN+Nchi)/2; s0Achi=0.

A última identidade usa adjunto formal, EG=0 e a paridade ímpar dos
ghosts. Não pressupõe R_W=L_WG. No interior chi=1 recupera a soma dos
contatos medidos. A igualdade com a quebra integral dos produtos
temporais, incluindo todos os locais e aridades, não foi demonstrada.

Controle com operadores diferenciais existentes, referência anisotrópica
variável e três pares de ghosts:52verificações, CPU21.015625s, rc0.
Omitir [N,chi]/2 quebra os três controles. Não são novos diagramas.

Derivação: {D/'DERIVACAO.md'}.
Manifesto: {dm}; SHA256 {sha(dm)}.
Log: {log}; SHA256 {sha(log)}.
Comando: {manifest['command']}.

Próximo: restante efetivo de Q2 e sua classe, dentro do teto A7.b.
Original, kernel e gate intactos. Custo parcial US${cost}; nenhuma
chamada externa nova nesta composição.
'''
write(O/'ENTREGA_016_A7b_soma_contatos_consistencia_livre.md',note.encode(),True)
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: soma dos contatos com cutoff é s0-exata no escopo construído;52checks CPU21.015625s; custo parcial US${cost}; Q2 integral OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 assembled_contact_wz_manifest=str(dm),partial_metered_cost_usd=str(cost),own_live_processes=[],
 next=['Compute remaining actual quantum contributions, distinguish A2 from primitive variation','A7b deadline2026-09-25T20:32Z; then A7c/d,A8,PartB,final'],
 completed_this_turn=['Reconciled existing Fourier phases','DeepSeek cutoff counterexample','Assembled contact free-BRST consistency with negative controls'])
write(p,json.dumps(c,ensure_ascii=False,indent=2).encode())
print(json.dumps(dict(checks=r['checks'],cpu_seconds=r['cpu_seconds'],cost_partial=str(cost),manifest_sha256=sha(dm))))
