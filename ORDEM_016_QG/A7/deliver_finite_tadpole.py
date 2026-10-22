"""Deliver zero-jet tadpole and preserve the rejected anisotropy hypothesis."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT';D=H/'finite_tadpole_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,new=False):
 if new:assert not p.exists(),p
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex)
  bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def append(p,v):write(p,p.read_bytes()+v.encode())
arts={};rows=[];logs=[]
for name,logname in [('finite_smooth_tadpole','finite_smooth_tadpole_run.log'),('finite_smooth_tadpole_transport_v2','finite_smooth_tadpole_transport_v2_run.log')]:
 m=H/name/'manifest.json'
 for item in json.loads(m.read_bytes())['artifacts']:
  p=Path(item['path']);assert sha(p)==item['sha256'];arts[str(p)]=sha(p)
 arts[str(m)]=sha(m);r=json.loads((H/name/'results.json').read_bytes());rows.append(r)
 log=H/logname;assert json.loads(log.read_text('utf-8-sig').splitlines()[-1])==r;arts[str(log)]=sha(log)
 logs.append(dict(log=str(log),sha256=sha(log),rc=0))
for p in [H/'finite_smooth_tadpole/DERIVACAO.md',H/'finite_smooth_tadpole_transport_check.py',H/'finite_smooth_tadpole_transport/PRE_REGISTER.json',Path(__file__)]:arts[str(p)]=sha(p)
checks=sum(r['checks'] for r in rows);cpu=sum(r['cpu_seconds'] for r in rows)
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,
 artifacts=[dict(path=p,sha256=h) for p,h in sorted(arts.items())],logs=logs,
 failed_v1='rc1 at assert nonzero: every anisotropic zero-jet gauge contraction was zero; CPU not captured',
 full_Q2=False,gate_changed=False)
m=D/'manifest.json';write(m,json.dumps(manifest,ensure_ascii=False,indent=2).encode(),True)
ledger=O/'LEDGER_016.jsonl';append(ledger,json.dumps(dict(at=now.isoformat(),event='FINITE_SMOOTH_TADPOLE_ZERO_JET',target='A7.b',checks=checks,cpu_seconds=cpu,remote_call=False,manifest_sha256=sha(m)))+'\n')
cost=Decimal(0);seen=set()
for line in ledger.read_text('utf-8-sig').splitlines():
 if not line.strip():continue
 r=json.loads(line);v=r.get('cost_estimate_usd')
 if v is None:v=r.get('cost_usd')
 if v is None:continue
 k=r.get('execution_task_id') or r.get('job_id') or r.get('request_id')
 if k and k in seen:continue
 if k:seen.add(k)
 cost+=Decimal(str(v))
note=f'''[DERIVED — tadpole finito calculado; jato constante não altera a contração Ward]

{now.isoformat()}. Abertura SHA256 {opening}.

Contraído o vértice quártico existente com a parte suave constante do
propagador. Na base de quatro invariantes já usada, os coeficientes são
W_I:(5/2,-5/2,5/2,-5) e W_T:(1,-1,1,-2), com os prefatores explícitos
na derivação. São Hessianas não nulas, mas sua contração com Gc é zero.

A nulidade vale para qualquer fibra W constante: a Hessiana EH é
degenerada na mesma imagem de gauge em toda métrica constante M.
Duas derivadas em M dão V4(A,Gc,Ea,Eb)=0 para as duas pernas internas
de momento zero. O controle cobriu55fibras, inclusive anisotrópicas.
Assim esse tadpole não cancela o resíduo hc da bolha+fonte já medido.

{checks}verificações exatas; CPU{cpu}s nas execuções bem-sucedidas;
dois comandos rc0. Falha anterior da hipótese de anisotropia preservada.
Nota: {H/'finite_smooth_tadpole/DERIVACAO.md'}.
Manifesto: {m}; SHA256 {sha(m)}.
Comandos: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/finite_smooth_tadpole_check.py e A7/finite_smooth_tadpole_transport_check_v2.py.

Não escolhidos estado ou normalização T1. Jatos derivados, curvatura,
aridades restantes e continuação causal seguem pendentes. Q2 integral
OPEN; gate intacto. Custo parcial US${cost}; zero chamadas externas novas.
'''
write(O/'ENTREGA_016_A7b_tadpole_suave_finito_jato_zero.md',note.encode(),True)
measure=f'''[REAL — MEDIDA: anisotropia constante não produz o resíduo esperado]

{now.isoformat()}. Abertura SHA256 {opening}.
Tentativa: obter contração de gauge não nula ao tornar W anisotrópico.
Comando A7/finite_smooth_tadpole_transport_check.py, rc1 em assert nonzero;
55fibras x3controles deram zero. Fonte SHA256 {sha(H/'finite_smooth_tadpole_transport_check.py')}.
Plano preservado; CPU da falha não capturada, não registrada como zero.
Versãov2 confirma nulidade e identidade cúbica/quártica, rc0;
logs e hashes: {json.dumps(logs,ensure_ascii=False)}.
Próximo: jatos derivados de W, que não são pernas internas de momento
zero. Não ampliar esta nulidade a eles. Nenhuma chamada remota nova.
'''
write(O/'ENTREGA_016_MEDIDA_tadpole_anisotropico_constante.md',measure.encode(),True)
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: tadpole finitoW0 calculado, Ward zero em toda fibra constante por identidade EH;{checks}checks CPU{cpu}s; custo parcialUS${cost}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 finite_tadpole_manifest=str(m),partial_metered_cost_usd=str(cost),own_live_processes=[],
 completed_this_turn=['Finite smooth zero-jet tadpole extracted','General constant-fiber gauge degeneracy proved; anisotropic expectation corrected'],
 next=['Compute derivative jets of finite W tadpole, preserving density and cutoff','Continue remaining Q2 contributions before A7b deadline20:32Z','A7c/d,A8,PartB,final still required'])
write(p,json.dumps(c,ensure_ascii=False,indent=2).encode())
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,cost_partial=str(cost),manifest_sha256=sha(m))))
