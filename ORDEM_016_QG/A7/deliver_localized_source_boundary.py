"""Publish source boundary and assemble previously computed flat pair contacts."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
import sympy as s
from full_loop_extension_engine import Q
H=Path(__file__).resolve().parent;D=H/'localized_source_boundary_delivery';D.mkdir(exist_ok=False)
O=H.parents[1]/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2).encode()
def append(p,t):write(p,p.read_bytes()+t.encode())
artifacts=[]
for name in ['localized_source_boundary_v2','full_loop_extension_basis']:
 m=H/name/'manifest.json'
 for row in json.loads(m.read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256'],row['path']
 artifacts.append(m)
r=json.loads((H/'localized_source_boundary_v2/results.json').read_bytes());assert r['checks']==488
pair=json.loads((H/'full_loop_extension_basis/results.json').read_bytes())['rows']
lookup={(a['case'],a['r']):a for a in r['rows']};parse=lambda t:s.sympify(t,locals={str(q):q for q in Q})
rows=[];controls=[]
for a in pair:
 src=parse(lookup[a['case'],a['r']]['components'][str((a['a'],a['b']))]);pol=s.expand(parse(a['combined'])+src)
 v=str(pol.subs(dict(zip(Q,(2,1,0,0)))))
 row=dict(case=a['case'],a=a['a'],b=a['b'],r=a['r'],pair=a['combined'],source=str(src),sum=str(pol),at2100=v)
 rows.append(row)
 if (a['a'],a['b'],a['r'])==(1,1,0):controls.append(dict(case=a['case'],pair=a['value2100'],source=str(src.subs(dict(zip(Q,(2,1,0,0))))),sum=v))
write(D/'assembled_pair_source.json',dump(dict(components=len(rows),controls=controls,rows=rows,full_Q2=False,missing=['classical-current insertions','curvature','smooth remainder','tadpoles','higher arities','Lorentzian continuation'])))
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
proof=r'''[DERIVED — fonte plana com fronteira ghost; montagem parcial de contatos]

O vértice Y é o mesmo que agora entra no par ghost:
integral chiY barc divZ=-integral(chiY dbarc+dchiY barc)Z.
Assim não basta multiplicar por chiY os coeficientes antigos A e B.
Aeta e Beta incorporam a substituição, na linha ghost interna,
partial_Ymu f -> (-d_mu+eta_mu)f, com d=partial_(X-Y).
As derivadas no outro extremo da linha são mantidas. Os sinais e a
contração dirigida são os do vértice já existente. O código explicita
os três termos de Lie_c h, o propagador métrico e seu traço revertido.

Depois da adjunção do ghost externo, a fonte é
Heta=Aeta+sum_j(d_j-eta_j)Beta^j.
Por isso existem termos quadráticos em eta, embora o vértice só tenha
uma derivada de cutoff. Eles vêm da adjunção sobre o coeficiente.
O operador em X continua o Einstein linear não fixado por gauge.

P=E_X{chiX[chiY R(Aeta)-divY(chiY R(Beta))]},
Q=R E_X{chiX chiY Heta}, C_D=R D-D R:
P-Q=-C_E(chiX chiY Heta)+E_X[chiX chiY C_divY(Beta)].
Não há termo de contato autônomo na adjunção das distribuições; ele está
na diferença entre aplicar derivadas antes e depois da extensão R.

Duas rotas calculam esse contato. A primeira usa a tabela C_D, Leibniz
completo e q->q-lambda para multiplicar chiX sobre derivadas de delta.
A segunda extrai o resíduo da expressão regulada
E_(d+lambda+2a*x/z)(Heta+a*2sum x_j Beta^j/z)-E_(d+lambda)Heta.
Só o coeficiente linear em a contribui para esses kernels racionais com
polos simples. Essa simplificação não é exportada a kernels logarítmicos.

488 verificações exatas:320 comparações com B antigo e C reduzido,
80 contrações de fronteira contra jatos de bitensores independentes,
40 recuperações do contato constante e48 comparações entre os dois
cálculos da extensão. Geradas120 componentes fonte (10x4x3 cutoffs).
Os dois métodos de extensão foram comparados para r=0; não declarar
que todas120 receberam a mesma comparação independente.

Falha preservada: v1 comparou polinômios tratando z independente de x.
Por exemplo,34x0²/z4-2(x1²+x2²+x3²)/z4-8/z3 versus36x0²/z4-10/z3
diferem por2(z-sum x²)/z4. No domínio z=sum x² são iguais. v2 usa
redução nesse ideal SOMENTE na comparação de kernels fora da diagonal;
o motor e o esquema de extensão não foram alterados. Logs/predecessor
estão preservados. Não se substituiu um desacordo numérico por tolerância.

Somados os contatos aos pares completos já calculados, na mesma
normalização CE=-4pi², obtém-se a tabela do JSON de montagem. Esta soma
é fonte+pares, ainda não a quebra Q2: as inserções da corrente BRST
clássica precisam ser calculadas na mesma prescrição. São igualmente
pendentes curvatura, partes suaves/tadpoles, aridades e causalidade.
Nenhum contato isolado não nulo demonstra obstrução cohomológica.
'''
write(D/'DERIVACAO.md',proof.encode())
artifacts += [D/'DERIVACAO.md',D/'assembled_pair_source.json',H/'localized_source_boundary_run.log',H/'localized_source_boundary_run_v2.log',H/'localized_source_boundary_check.py',H/'localized_source_boundary_check_v2.py',Path(__file__),H/'orchestration_source_boundary/prepared_units.json',H/'orchestration_source_boundary/preview.json']
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds=r['cpu_seconds'],full_Q2=False,
 supersedes=dict(path=str(H/'localized_source_boundary_check.py'),sha256=sha(H/'localized_source_boundary_check.py'),reason='Comparator must impose z=sum x²; v1 failure preserved'),
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in artifacts])
write(D/'manifest.json',dump(manifest))
ledger=O/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='LOCALIZED_SOURCE_COMPARATOR_V1_FAILURE',target='A7.b',rc=1,cpu_seconds=None,reason='z independent in comparator despite radial constraint',log_sha256=sha(H/'localized_source_boundary_run.log'),remote_call=False))+'\n')
append(ledger,json.dumps(dict(at=now.isoformat(),event='LOCALIZED_SOURCE_GHOST_BOUNDARY_AND_PAIR_ASSEMBLY',target='A7.b',checks=r['checks'],cpu_seconds=r['cpu_seconds'],rc=0,manifest_sha256=sha(D/'manifest.json'),remote_call=False))+'\n')
catalog=json.loads((H/'orchestration_source_boundary/prepared_units.json').read_bytes())[0]
append(ledger,json.dumps(dict(at=now.isoformat(),event='MIMO_SOURCE_BOUNDARY_PREPARED_SENT_TO_COORDINATOR',target='A7.b',request_id=catalog['request_id'],prompt_sha256=sha(Path(catalog['payload'])),status='PREVIEW_SELECTED_MIMO_PENDING_COORDINATOR_STAGING',provider_calls=0))+'\n')
total=Decimal(0);seen=set()
for line in ledger.read_text('utf-8-sig').splitlines():
 if not line.strip():continue
 e=json.loads(line);k=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('cost_usd'))
 if v is not None and (k is None or k not in seen):
  total+=Decimal(str(v))
  if k:seen.add(k)
start=datetime.fromisoformat(json.loads((H/'localized_source_boundary/PRE_REGISTER.json').read_bytes())['at']);wall=(now-start).total_seconds()/3600
table='\n'.join(f"|{a['case']}|{a['pair']}|{a['source']}|{a['sum']}|" for a in controls)
out=O/'ENTREGA_016_A7b_fonte_fronteira_ghost_e_pares.md';assert not out.exists()
write(out,f'''[DERIVED — fonte localizada com fronteira ghost e montagem plana parcial]

{now.isoformat()}. Abertura SHA256 {opening}.

Incluído dchiY.bar c.Z nos próprios coeficientes A/B da fonte, além dos
multiplicadores externos. {r['checks']} verificações, CPU{r['cpu_seconds']}s,
rc0 na v2. v1 preservada: comparador ignorava z=sum x²; sem mudança do
motor. Dois cálculos independentes de extensão concordam nos48 controles.
Registradas120 componentes e sua soma aos pares da entrega anterior.

Para h11,c0,q=(2,1,0,0), normalizados por CE=-4pi²:

|Jatos locais|Par ghost-métrica/2|Fonte|Soma parcial|
|---|---|---|---|
{table}

Esta soma ainda não é Q2: falta incorporar as inserções da corrente
clássica na mesma extensão, além de curvatura, partes suaves, aridades
e continuação causal. Não há alteração do gate.

Manifesto {D/'manifest.json'}; SHA256 {sha(D/'manifest.json')}.
Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/localized_source_boundary_check_v2.py. Logs e hashes no manifesto.
Bancada registrada{wall:.6f}h; custo da tentativa falha não medido.
Parcial externo conhecido US${total}, sem chamada paga nesta entrega.
Nova revisão independente MiMo {catalog['request_id']} preparada e
encaminhada à coordenação, após4d e sem alterar consultas já em execução.
'''.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: fonte pré-IBP completa,488checks,CPU{r["cpu_seconds"]}s,bancada{wall:.6f}h,v1falha preservada;120componentes somadas aos pares; parcialUS${total};Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=c.get('completed_this_turn',[])+['Full source ghost boundary,488 exact checks','120 source+pair contacts assembled'],
 localized_source_boundary_manifest=str(D/'manifest.json'),own_live_processes=[],
 source_boundary_review_catalog=str(H/'orchestration_source_boundary/prepared_units.json'),
 next=['Compute actual classical-current insertions in same extension; source+pair alone is not Q2','Curvature,smooth pieces,tadpoles,arities and causal prescription remain',
 'Audit pending Kimi/MiMo through coordinator; new MiMo934328 staged after4d','A7b deadline20:32Z; A7c/d,A8,PartB and final audit remain'])
write(p,dump(c));print(json.dumps(dict(delivery=str(out),controls=controls,checks=r['checks'],cpu_seconds=r['cpu_seconds'],partial_cost=str(total))))
