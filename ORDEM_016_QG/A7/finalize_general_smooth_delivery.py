"""Verify and deliver general smooth fiber and first-curvature contact scope."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'general_smooth_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,replace=False):
 if p.exists():
  assert replace,p
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);assert not bak.exists()
  bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b and b;t.replace(p)
def obj(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode())
def append(p,text):
 b=p.read_bytes();write(p,b+text.encode(),True);assert p.stat().st_size>len(b)
artifacts={};data=[];logs=[]
for name in ['smooth_general_fiber','mixed_curvature_scaling']:
 m=H/name/'manifest.json'
 for row in json.loads(m.read_bytes())['artifacts']:
  p=Path(row['path']);assert sha(p)==row['sha256'];artifacts[str(p)]=sha(p)
 artifacts[str(m)]=sha(m)
 log=H/(name+'_run.log');r=json.loads((H/name/'results.json').read_bytes())
 assert json.loads(log.read_text('utf-8-sig').splitlines()[-1])==r
 data.append(r);artifacts[str(log)]=sha(log)
 logs.append(dict(command=f'A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/{name}_check.py',rc=0,log=str(log),sha256=sha(log)))
for p in [Path(__file__),H/'smooth_general_fiber/DERIVACAO.md']:artifacts[str(p)]=sha(p)
checks=sum(r['checks'] for r in data);cpu=sum(r['cpu_seconds'] for r in data)
opening=OUT/'ENTREGA_016_ABERTURA_operador.md'
obj(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=sha(opening),
 artifacts=[dict(path=p,sha256=h) for p,h in sorted(artifacts.items())],
 logs=logs,checks=checks,cpu_seconds=cpu,full_Q2=False,gate_changed=False))
note=f'''[DERIVED — primitiva BV com referência geral; primeira curvatura do contato misto]

{now.isoformat()}. Abertura SHA256 {sha(opening)}.

Retirada a hipótese de isotropia: os55 componentes reais simétricos da
referência métrica foram contraídos nos vértices existentes. Todos os
tensores resultantes obedecem à transposição conjunta de fibra/derivada.
Por linearidade, o operador N_W=-div(T(W)grad) é autoadjunto para
referência diagonal variável geral. O ghost é zero nesse contato,
conferido nas16 fibras. As fontes de primeiro jato e rotação permanecem.

O mesmo objeto já construído cobre essa generalização:

    B_W=-C_E integral(h.N_W h/2+hdagger.R_W c),
    s0B_W=-C_E integral h.(N_W G+E R_W)c.

Não é necessário R_W=L_WG. Controle anisotrópico: c=(-x1,x0,0,0)
tem Gc=0, mas, para W_00|00=x0²-x2² na coordenada central,
(E R_Wc)01=(E R_Wc)10=1/2. O antifield conserva essa contribuição.

Separadamente,2900 componentes bilocais à primeira curvatura foram
derivados antes de ancorar Y. Os6122 monômios têm grau de escala≤2,
sem contato adicional da linha mista antes de Ward. Isso NÃO elimina
curvatura das composições covariantes nem logaritmos em geral: a quarta
derivada de logz tem contato/C_E=-1/2, contra zero na segunda.

Evidência: {checks} verificações, CPU{cpu}s, dois comandos rc0.
Nota: {H/'smooth_general_fiber/DERIVACAO.md'}.
Manifesto conferido: {D/'manifest.json'}; SHA256 {sha(D/'manifest.json')}.
As contagens são igualdades algébricas, não experiências independentes.

Alcance: contato relativo singular/suave dos vértices estudados. Não
foi escolhido estado admissível, aplicado contratermo ou fechada Q2.
Restam outros locais/aridades, compatibilidade física e normalização
causal. Originais, kernel e gate intactos. Próximo: auditar as revisões
independentes e completar a soma na prescrição dentro do teto A7.b.
'''
write(OUT/'ENTREGA_016_A7b_referencia_geral_e_contato_curvo.md',note.encode())
measure=f'''[REAL — MEDIDA do limite da fatoração por G e do descarte de log]

{now.isoformat()}. Abertura SHA256 {sha(opening)}.
Rota simplificada: R_W=L_WG e log sempre sem contato.
Resultados: controle anisotrópico com Gc=0 tem (ER_Wc)01=1/2;
contato da quarta derivada temporal euclidiana de logz/C_E=-1/2.
Essas simplificações não podem ser usadas. A primitiva BV geral
preserva R_W; a análise de escala deve respeitar a ordem de derivada.
Comandos/rc/logs: {json.dumps(logs,ensure_ascii=False)}.
CPU{cpu}s; zero chamadas remotas novas. Próxima rota: soma dos termos
locais/curvos já calculados, mantendo os dados gerais acima.
'''
write(OUT/'ENTREGA_016_MEDIDA_referencia_geral_e_log.md',measure.encode())
ledger=OUT/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='A7_GENERAL_SMOOTH_FIBER_AND_CURVATURE_SCALING',
 target='A7.b',checks=checks,cpu_seconds=cpu,remote_call=False,
 manifest_sha256=sha(D/'manifest.json'),full_Q2=False),ensure_ascii=False)+'\n')
seen=set();cost=Decimal(0)
for line in ledger.read_text('utf-8-sig').splitlines():
 if not line.strip():continue
 r=json.loads(line);v=r.get('cost_estimate_usd')
 if v is None:v=r.get('cost_usd')
 if v is None:continue
 key=r.get('execution_task_id') or r.get('job_id') or r.get('request_id')
 if key and key in seen:continue
 if key:seen.add(key)
 cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS:55fibras da referência geral; primitivaBV mantém rotação; K1 misto subcrítico antes deWard. {checks}checks CPU{cpu}s; custo parcialUS${cost}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes())
c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['All55 real symmetric metric reference fibers contracted',
 'General BV primitive retains rotational source',
 'All2900 explicit K1 single-line jets subcritical under endpoint derivative cap'],
 general_smooth_manifest=str(D/'manifest.json'),
 next=['Audit received Kimi reviews without contaminating pending independent prompts',
       'Assemble remaining local/curved Ward contributions within A7b timebox',
       'A7.b deadline2026-09-25T20:32Z; then A7.c/d,A8,PartB,final audit'],
 partial_metered_cost_usd=str(cost),own_live_processes=[])
write(p,json.dumps(c,ensure_ascii=False,indent=2).encode(),True)
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,artifacts=len(artifacts),cost_partial=str(cost),manifest_sha256=sha(D/'manifest.json'))))
