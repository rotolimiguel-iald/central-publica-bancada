"""Publish the useful recurrence and reject a spurious kernel correction."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'kimi_transvection_review';O=H.parents[1]/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2).encode()
def append(p,t):write(p,p.read_bytes()+t.encode())
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
r=json.loads((D/'results.json').read_bytes());assert r['checks']==1136
receipt=json.loads((D/'RECEIPT.json').read_bytes());job=receipt['job'];execution=job['execution'];res=execution['result']
payload=H/'orchestration_bilocal_completion_v2/kimi_spaceform_transvection_endpoint_recurrence_submit.json';p=json.loads(payload.read_bytes());assert job['request_id']==p['request_id']
ys=s.symbols('y0:4');controls=[]
for c in r['controls']:
 a=s.sympify(c['recurrence'],locals={str(y):y for y in ys}).subs(dict.fromkeys(ys,0));assert a==s.Rational(c['actual'])
 controls.append(dict(component=c['component'],actual=c['actual'],anchored_recurrence=str(a),claimed_extra=c['claimed_extra']))
write(D/'ANCHORED_CONTROLS.json',dump(dict(note='Original results display recurrence before final y=0; eq checks already anchored. These display values now anchored; no rerun or engine edit.',controls=controls)))
proof=r'''[DERIVED — recorrência de Killing conferida; resto do parecer refutado]

Resposta Kimi9c1 foi lida integralmente,238 linhas. A máquina não tomou
VERIFICADO escrito pelo modelo como verificação local. O parecer explicita
que não executou código; aqui1136 verificações exatas terminaram rc0.

Aceito neste escopo: k_i^a=delta_i^a-K(xx delta_i^a-x^a x_i)/3
satisfaz Lie_k g=0 até primeira ordemK, para
g_ab=delta_ab-K(xx delta_ab-x_a x_b)/3.
A conexão derivada dessa métrica confere com o motor existente.
O operador D_i=k_i.partialX+rho_X, com rho_X atuando nos índices X,
fornece partial_Yi G|0=-D_i G|0. A segunda derivada parcial é
partial_Yj partial_Yi G|0=D_i D_j G|0-sum_{slotsY} Q_jB,i^c G_(B->c),
Q_jB,i^c=partial_Yj partial_YB k_i^c(0).
Para índices covariantesY, -Q_jB,i^c=partial_Yi Gamma^c_jB(0).
Essas correções não podem ser descartadas ao repetir a derivada.

Conferidos:64 componentes de primeira derivada ghost;256 de segunda;
400 primeiras derivadas métricas (10x10x4); mais identidades de Killing,
conexão, distância e termo Q. Não se verificaram aqui todas as segundas
derivadas métricas, nem se alegou precisão em K² ou um estado completo.

Refutado: a §5.3 do parecer afirma falta de2K deltaij deltaAB/(3w)
no kernel. A recorrência e o kernel concordam exatamente em todas256
segundas derivadas ghost. A origem do erro é localizável:
distance1=-(xx yy-(X.Y)^2)/3,
partial_Yi partial_Yj distance1|0=-2(xx deltaij-XiXj)/3.
O parecer reteve2XiXj/3 e omitiu-2xx deltaij/3. Como o propagador tem
-distance1 deltaAB/w², o termo omitido fornece justamente
+2xx deltaij deltaAB/(3w²). Ele já existe no kernel; nada deve ser somado.

Controle X=(1,2,-1,1),w=7,i=j=0,A=B=1:
derivada e recorrência dão-473/2058; o extra alegado seria2/21.
No controle i=0,j=1,A=1,B=2, ambos37/1029.
O resto reivindicado é não nulo em16 componentes de índices; falha nas16.
Isso não é suporte na diagonal X=Y:1/w, mesmo se estivesse presente,
seria singular fora dela, não automaticamente um contato de delta.

Errata menor: a primeira fórmula de Gamma na §1.1 está com sinal
oposto ao motor (36 componentes não nulas). Fórmulas posteriores do
parecer usam o sinal correto. Não foi necessária alteração do motor.
Também os exemplos individuais de primeira derivada no parecer omitem
derivadas logarítmicas que cancelam na diferença; nossa conferência usa
a função completa, inclusive log, e não essa abreviação como igualdade.

Resultado útil: a recorrência é um verificador independente dos jatos,
mantido sem dY=-dX ingênuo. Não é autorização para reparar o propagador
com o termo espúrio, nem conclusão sobre Q2, W suave ou estado físico.
O kernel e a prescrição de extensão permanecem inalterados.
'''
write(D/'DERIVACAO.md',proof.encode())
acceptance=H.parents[1]/'IALD_ORQUESTRACAO_20260923/state/handoffs/a7_source_boundary_pending_submissions.json'
write(H/'orchestration_source_boundary/coordinator_acceptance.json',acceptance.read_bytes())
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md');manifest=D/'delivery_manifest.json';assert not manifest.exists()
write(manifest,dump(dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds=r['cpu_seconds'],full_Q2=False,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in [D/'manifest.json',D/'DERIVACAO.md',D/'ANCHORED_CONTROLS.json',D/'EXTRACTION_NOTE.json',H/'audit_kimi_transvection_run.log',payload,Path(__file__),H/'orchestration_source_boundary/coordinator_acceptance.json']])))
ledger=O/'LEDGER_016.jsonl';entries=[json.loads(t) for t in ledger.read_text('utf-8-sig').splitlines() if t.strip()]
assert not any(e.get('execution_task_id')==execution['id'] for e in entries)
ev=dict(at=now.isoformat(),event='KIMI_TRANSVECTION_REVIEW_RECEIVED_AND_AUDITED',target='A7.b',provider='kimi',job_id=job['id'],request_id=job['request_id'],execution_task_id=execution['id'],
 usage=res['usage'],cost_estimate_usd=None,cost_status='SUBSCRIPTION_UNKNOWN_NOT_ZERO',provider_elapsed_seconds=res['elapsed_seconds'],
 prompt_sha256=hashlib.sha256(p['prompt'].encode()).hexdigest(),payload_sha256=sha(payload),response_sha256=sha(D/'RESPONSE.md'),provider_response_sha256=hashlib.sha256(res['text'].encode()).hexdigest(),
 manifest_sha256=sha(manifest),checks=r['checks'],cpu_seconds=r['cpu_seconds'],scientific_status='RECURRENCE_ACCEPTED_FIRST_K_CLAIMED_RESIDUAL_REFUTED',remote_call_by_this_script=False)
append(ledger,json.dumps(ev)+'\n');entries.append(ev);total=Decimal(0);seen=set()
for e in entries:
 k=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('cost_usd'))
 if v is not None and (k is None or k not in seen):
  total+=Decimal(str(v))
  if k:seen.add(k)
note=f'''[DERIVED — Kimi: recorrência aceita no escopo conferido; resto espúrio refutado]

{now.isoformat()}. Abertura SHA256 {opening}.

1136 verificações exatas, CPU{r['cpu_seconds']}s, rc0. A recorrência de
Killing reproduz64 primeiras e256 segundas derivadas ghost, e400 primeiras
derivadas métricas. O extra2K deltaij deltaAB/(3w) alegado pelo Kimi não
existe: foi omitido -2xx deltaij/3 ao diferenciar distance1. O kernel
já contém esse termo. Controle: ambos lados-473/2058, sem o extra2/21.
Derivação, erratas de sinal e controles estão preservados ao lado.

Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/audit_kimi_transvection.py.
Manifesto {manifest}; SHA256 {sha(manifest)}. Logs/hashes no manifesto.
Kimi K3:{res['usage']['prompt_tokens']} tokens entrada,
{res['usage']['completion_tokens']} saída;{res['elapsed_seconds']}s de
execução informados pelo recibo. Custo da assinatura não informado;
parcial monetário conhecido US${total}. Nenhuma nova chamada nesta auditoria.

Coordenação confirmou MiMo4d (jobc7633694-26f1-47b6-9bf2-f035bf5f834c)
e próximo Kimi fb5b38c3 em execução paralela. Nova revisão MiMo93432896
aceita em staging após4d. PreservadosIDs, perguntas e fila única.
Q2 completo segue OPEN; próximo: inserções de corrente clássica e
montagem de curvatura, sem alterar o kernel para satisfazer o parecer.
'''
for name in ['ENTREGA_016_A7b_auditoria_Kimi_transveccao.md','ENTREGA_016_MEDIDA_Kimi_resto_transveccao.md']:
 p=O/name;assert not p.exists();write(p,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b MEDIDA/PROGRESS: Kimi Killing,1136checks CPU{r["cpu_seconds"]}s; recorrência aceita,resto refutado;436638tokens de assinatura custo desconhecido;parcialUS${total};Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=c.get('completed_this_turn',[])+['Kimi transvection reviewed,1136 exact checks; spurious residual rejected'],
 kimi_transvection_review_manifest=str(manifest),own_live_processes=[],partial_metered_cost_usd=str(total),
 pending_orchestration='MiMo4d jobc7633694 and Kimi fb5b38c3 running;934328 accepted staging after4d;Kimi f3 next admission;DeepSeek70e9 authorized secondary',
 next=['Classical-current insertions in same extension; source+pair alone not Q2','Curvature and higher arities within A7b timebox; use verified recurrence without altering kernel',
 'Await/audit Kimi external-first-jet and MiMo loop-localization results, no duplicate calls','A7b deadline20:32Z;A7c/d,A8,PartB and final audit remain'])
write(p,dump(c));print(json.dumps(dict(manifest=str(manifest),checks=r['checks'],partial_cost=str(total))))
