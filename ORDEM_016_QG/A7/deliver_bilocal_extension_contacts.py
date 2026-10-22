"""Record the X/Y contact calculation, restricted primitive and provider audits."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT'
BASE=C/'IALD_ORQUESTRACAO_20260923';D=H/'bilocal_extension_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,update=False):
    if isinstance(b,str):b=b.encode('utf-8')
    if p.exists():
        assert update,p;old=p.read_bytes()
        backup=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:8])
        backup.write_bytes(old);assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b
    t.replace(p);assert p.read_bytes()==b
def put(p,v,update=False):write(p,json.dumps(v,ensure_ascii=False,indent=2),update)
names=['bilocal_X_extension_contact','bilocal_Y_regulator','bilocal_XY_extension_contact',
 'bilocal_regulator_controls_v2','kimi_curved_ward_review','bilocal_flat_contact_primitive','deepseek_adjoint_review']
rs={n:json.loads((H/n/'results.json').read_bytes()) for n in names};files=[Path(__file__)]
for name in names:
    p=H/name/'manifest.json';m=json.loads(p.read_bytes());files.append(p)
    for row in m['artifacts']:
        q=Path(row['path']);assert sha(q)==row['sha256'],q;files.append(q)
    files.extend(q for q in (H/name).iterdir() if q.is_file() and '.tmp_' not in q.name)
    files.append(H/(name+'_run.log'))
checks=sum(r['checks'] for r in rs.values());cpu=sum(r['cpu_seconds'] for r in rs.values())
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
failure=BASE/'state/handoffs/7f606d88-ac59-4940-9bb0-d7be6ba306ea_delivery.json'
failed=json.loads(failure.read_bytes());assert failed['stage']=='failed'
write(D/'MIMO_ANGULAR_FAILURE_RECEIPT.json',failure.read_bytes())
diagnostic=BASE/'state/handoffs/mimo_transport_diagnostic_followup_20260925.json'
write(D/'MIMO_TRANSPORT_DIAGNOSTIC.json',diagnostic.read_bytes())
put(D/'ORCHESTRATION_SNAPSHOT.json',dict(at=now,source='Official coordinator reports this turn',
    kimi_harmonic_running='d0fd9aa9-1d09-451e-867b-a9e34ed775bb',
    mimo_allorder_running='bf606625-201a-41ee-adb1-462bc72d0cdc',
    deepseek_completed='25292039-6bed-4b01-a788-cef4e7bfe55e',
    kimi_meromorphic_registered='6c210ea9-cc1e-4c09-a039-3d469ae4f090',
    mimo_future_dispatch='HOLD_PENDING_TRANSPORT_REVIEW_AFTER_CURRENT_JOB; current job not interrupted',
    separate_queue_created=False,old_calls_repeated=False))
put(D/'FAILED_CONTROL_RECORD.json',dict(at=now,script=str(H/'bilocal_regulator_controls_check.py'),
    exit_code=1,log_sha256=sha(H/'bilocal_regulator_controls_run.log'),
    exact_residual='2/3*(1-X²/w)',reason='Auxiliary-radius relation omitted from test simplifier',
    resolved_by='v2 enforces w=X² after differentiation; no coefficient or engine changed',
    failed_cpu_unknown_not_zero=True,
    failed_preparer='One inline PowerShell/Python quoting attempt produced SyntaxError before file creation; standalone preparer succeeded'))
c=rs['bilocal_XY_extension_contact']['coefficients_over_C_E']
report=O/'ENTREGA_016_A7b_contatos_bilocais_XY_e_primitiva_plana.md'
write(report,f'''[DERIVED — contato do par singular hc até O(K); primitiva plana restrita; Q2 completa OPEN]

# Contatos nos dois extremos da identidade bilocal

Data: {now}. Abertura SHA256: {opening}.

A identidade não coincidente foi estendida com derivadas explícitas do
regulador em X e Y. A soma conserva a fonte Einstein, o frame, a medida
curva e os termos a² log que contribuem à parte finita. As duas
completações rho² (geodésica) e w=(X-Y)² foram medidas lado a lado, sem
escolha posterior para impor anulação.

Em unidades C_E=-4pi², com fatores comuns dos propagadores removidos:

| ordem/base | geodésica | coordenada |
|---|---|---|
| K0: delta_ab qr(q²)²; (delta_ar qb+delta_br qa)(q²)²; qa qb qr q² | {', '.join(c['geodesic'][0])} | {', '.join(c['coordinate'][0])} |
| K1: delta_ab qr q²; (delta_ar qb+delta_br qa)q²; qa qb qr | {', '.join(c['geodesic'][1])} | {', '.join(c['coordinate'][1])} |

q denota derivadas de delta em coordenadas normais, com testes em frame
e volume incluído. A diferença curva é local:
{', '.join(rs['bilocal_XY_extension_contact']['geodesic_minus_coordinate'][1])}.
Ela não altera a identidade fora da diagonal. O contato não nulo deste
par não é, por si só, uma anomalia não removível.

O componente plano admite explicitamente uma família de primitivas
quadráticas locais: N G=A_hc, B=-C_E/2 integral h.Nh. Todos os momentos e
componentes foram verificados simbolicamente (180 verificações), com
duas constantes livres preservadas. Nenhum contratermo foi adotado.
A extensão curva/não linear dessa nova família ainda não foi paga.

## Verificação e correções

X:256 verificações; Y:320; soma:512; controles:27. A regra de parte finita
e 280 pares de monômio/potência na soma foram conferidos por momentos de
S³ e resíduo radial. Fonte testada fora do eixo. Descartar logaritmos
muda o contato, como mostra o controle negativo. O primeiro teste do
raio falhou por comparar w livre com X²; v2 corrige apenas o teste.

Kimi98e09: 213 verificações de consistência, adjunção do símbolo e sinal
graduado. Mantida a família quadrática anterior. Corrigida a sua próxima
condição: para A1=-s0B, WZ implica s0(A2+s1B)=0. O sinal menos proposto
na revisão falha num contraexemplo exato. Não houve cálculo de A2.

DeepSeek252920: 34 verificações da densidade; preservado como parecer
limitado. Ancorar Y=0 não torna um kernel em X um contato. [E0,E1] já
representa ordens em K e não precisa de um segundo K. A derivação da
autoadjunção pedida ao executor não foi fornecida; não se usa o parecer
como certificado do operador completo.

## Escopo e continuidade

Ainda faltam W suave geral, contribuições locais/tadpoles restantes,
K², aridades não lineares, valores de contorno lorentzianos e WZ/classe
da Q2 completa. O próximo passo é confrontar o contato curvo com a
completação covariante da primitiva e com os termos locais faltantes.

Total local: {checks} verificações reportadas, CPU {cpu}s; CPU da tentativa
falha não medido, sem assumir zero. MiMo acumulou três IncompleteRead;
coordenação registrou padrão próximo de15min, sem causa comprovada, e
reterá novos despachos após a chamada já em curso. Kimi segue ativo.
DeepSeek informou US${json.loads((H/'deepseek_adjoint_review/RECEIPT.json').read_bytes())['cost_estimate_usd']}
como estimativa superior desta chamada, não fatura. Nenhum original,
kernel, gate ou parâmetro físico foi alterado.
''')
measure=O/'ENTREGA_016_MEDIDA_contato_bilocal_e_controle_do_raio.md'
write(measure,f'''[REAL — contato não nulo medido; tentativa falha preservada]

Data {now}; abertura SHA256 {opening}.

Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/bilocal_XY_extension_contact_check.py; rc0;
log SHA256 {sha(H/'bilocal_XY_extension_contact_run.log')}.
Identidade não coincidente até O(K) permanece; o contato do par singular
é a tabela no results.json, não a Q2 completa. Próximo ramo: primitiva
covariante/contactos locais restantes. A parte plana já tem família
quadrática explícita, sem escolha de representante.

Controle do raio: bilocal_regulator_controls_check.py rc1;
log SHA256 {sha(H/'bilocal_regulator_controls_run.log')}.
Resíduo (2/3)(1-X²/w); a regra w=X² foi omitida no simplificador do teste.
V2, rc0,27checks,CPU{rs['bilocal_regulator_controls_v2']['cpu_seconds']}s;
log SHA256 {sha(H/'bilocal_regulator_controls_v2_run.log')}.
Original, tentativa e preparação falha de shell preservados/registrados.
Nenhum coeficiente foi ajustado para fazer o controle passar.
''')
files += [report,measure,H/'bilocal_XY_extension_contact/DERIVACAO.md',
 H/'bilocal_regulator_controls_check.py',H/'bilocal_regulator_controls/PRE_REGISTER.json',
 H/'bilocal_regulator_controls_run.log',H/'prepare_regulator_controls_v2.py',
 H/'bilocal_regulator_controls_v2_generation.json',D/'FAILED_CONTROL_RECORD.json',
 D/'MIMO_ANGULAR_FAILURE_RECEIPT.json',D/'MIMO_TRANSPORT_DIAGNOSTIC.json',D/'ORCHESTRATION_SNAPSHOT.json']
files=list(dict.fromkeys(files))
put(D/'manifest.json',dict(at=now,opening_sha256=opening,checks=checks,cpu_seconds=cpu,
    failed_attempt_cpu_unknown=True,full_Q2=False,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
dr=json.loads((H/'deepseek_adjoint_review/RECEIPT.json').read_bytes())
ledger=O/'LEDGER_016.jsonl'
events=[dict(at=now,event='A7_BILOCAL_XY_CONTACTS_AND_FLAT_PRIMITIVE_DELIVERED',target='A7.b',
      checks=checks,cpu_seconds=cpu,full_Q2=False,delivery_manifest_sha256=sha(D/'manifest.json')),
 dict(at=now,event='KIMI_CURVED_WARD_LOCAL_SIGN_AUDIT_COMPLETED',target='A7.b',provider='kimi',
      job_id='98e09d38-848b-4ca1-914e-4a714becd561',remote_call=False,
      audit_manifest_sha256=sha(H/'kimi_curved_ward_review/manifest.json')),
 dict(at=now,event='DEEPSEEK_ADJOINT_RECEIVED_AND_SELECTED_AUDIT',target='A7.b',provider='deepseek',
      job_id=dr['job_id'],request_id='a9bd18bf-b178-46f6-b87e-b061eed1484f',execution_task_id=dr['execution_task_id'],
      tokens=dr['usage'],cost_estimate_usd=dr['cost_estimate_usd'],cost_status=dr['cost_status'],
      response_sha256=dr['response_sha256'],audit_manifest_sha256=sha(H/'deepseek_adjoint_review/manifest.json')),
 dict(at=now,event='MIMO_ANGULAR_TERMINAL_FAILURE_RECEIVED',target='A7.b',provider='mimo',
      job_id=failed['job_id'],execution_task_id=failed['execution_task_id'],error=failed['error'],
      tokens=None,cost_estimate_usd=None,cost_status='UNKNOWN_NOT_ZERO',retried=False,receipt_sha256=sha(failure))]
write(ledger,ledger.read_bytes()+''.join(json.dumps(e)+'\n' for e in events).encode(),True)
parents={}
def root(k):
    parents.setdefault(k,k)
    if parents[k]!=k:parents[k]=root(parents[k])
    return parents[k]
def ids(r):return [str(r[k]) for k in ('execution_id','execution_task_id','job_id','request_id') if r.get(k)]
rows=[json.loads(l) for l in ledger.read_text('utf-8-sig').splitlines() if l.strip()]
for r in rows:
    keys=ids(r)
    for k in keys[1:]:parents[root(k)]=root(keys[0])
known={}
for r in rows:
    keys=ids(r);cost=r.get('cost_estimate_usd',r.get('cost_usd',r.get('custo_usd')))
    if keys and cost is not None:known[root(keys[0])]=Decimal(str(cost))
total=sum(known.values(),Decimal())
put(D/'COST_SUM.json',dict(at=now,known_partial_usd=str(total),unknown_not_zero=True,ledger_sha256=sha(ledger)))
p=O/'ENTREGA_016_PROGRESSO.md'
write(p,p.read_bytes()+f'\n- {now} A7.b PROGRESS: contato singular par+fonte O(K) calculado em X/Y, duas completações; componente plano tem primitiva explícita. {checks}checks,CPU{cpu}s; tentativa falha CPUdesconhecido. Kimi/DeepSeek auditados; MiMo diagnóstico/HOLD após chamada corrente. Custo parcial US${total}; Q2 completa OPEN.\n'.encode(),True)
p=H/'CONTINUIDADE.json';v=json.loads(p.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',own_live_processes=[],
    bilocal_XY_contact_manifest=str(D/'manifest.json'),partial_metered_cost_usd=str(total),
    quantum_anomaly_computed=False,singular_pair_contact_first_curvature=True,
    completed_this_turn=['X/Y regulated singular hc pair+source contact through O(K), both distance completions',
       'Restricted flat hc contact has explicit selfadjoint quadratic primitive family; no subtraction adopted',
       'Kimi nonlinear descent sign corrected; DeepSeek series/density/scope reviewed',
       'Regulator controls passed after enforcing radius relation; failed test retained'],
    next=['Complete curved covariant primitive/contact matching, retaining order of derivatives and frame-to-covariant conversion',
       'Include remaining local diagrams/W/K2 and higher arity/WZ within A7.b deadline',
       'A7.b ends approx2026-09-25T20:32Z; then A7.c/d,A8,PartB and final full audit'],
    pending_orchestration='Kimi harmonic d0fd and MiMo all-order bf606 running per coordinator. Kimi meromorphic6c210 registered. DeepSeek252920 completed/audited. HOLD newMiMo after active unit pending transport diagnosis.',
    latest_live_execution=dict(status='COORDINATOR_OWNED_NO_OWN_PROCESS',
       kimi_job='d0fd9aa9-1d09-451e-867b-a9e34ed775bb',mimo_job='bf606625-201a-41ee-adb1-462bc72d0cdc',
       source=str(D/'ORCHESTRATION_SNAPSHOT.json')),
    local_primitive_contact_manifest=str(H/'bilocal_flat_contact_primitive/manifest.json'),
    corrected_nonlinear_descent='For A1=-s0B: O2=A2+s1B; cancellation O2=-s0B3 modulo d. No nonlinear A2 calculated.')
put(p,v,True)
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256'],row['path']
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,artifacts=len(files),known_partial_usd=str(total),goal='ACTIVE',full_Q2=False)))
