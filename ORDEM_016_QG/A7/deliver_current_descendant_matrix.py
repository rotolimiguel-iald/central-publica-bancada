"""Publish the full fixed-cutoff matrix result and independent residue audit."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, uuid

H = Path(__file__).resolve().parent
OUT = H.parents[1] / 'TUNEL/DO_CHATGPT'
D = H / 'current_descendant_matrix_delivery'
now = datetime.now(timezone.utc)
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, b, replace=False):
    assert b
    if p.exists():
        assert replace, p
        old = p.read_bytes()
        bak = p.with_name(p.name + '.bak_' + stamp)
        assert not bak.exists()
        bak.write_bytes(old)
        assert bak.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(b)
    assert tmp.read_bytes() == b
    tmp.replace(p)
def put(p, v, replace=False):
    write(p, json.dumps(v, ensure_ascii=False, indent=2).encode('utf-8'), replace)
def append(p, t): write(p, p.read_bytes() + t.encode('utf-8'), True)

m = json.loads((H/'current_distributional_descendant_matrix/results.json').read_bytes())
a = json.loads((H/'current_descendant_matrix_independent_audit/results.json').read_bytes())
assert m['bilocal_nonzero_components'] == m['nonzero_difference_components'] == 0
assert a['independent_residue_route_matches_all16']
assert a['omitted_contact_nonzero_components'] == a['reversed_sign_nonzero_components'] == 16
D.mkdir(exist_ok=False)
opening = sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
checks = m['checks'] + a['checks']
cpu = m['cpu_seconds'] + a['cpu_seconds']
report = f'''# A7.b — descida distribucional da corrente: matriz completa no recorte medido

[REAL — cálculo simbólico exato; DERIVED — interpretação restrita; Q2 integral OPEN]

As 16 componentes de dois ghosts do resíduo anteriormente medido coincidem
exatamente com a descida distribucional da corrente já construída. Nenhum
coeficiente foi ajustado e nenhuma normalização nova foi escolhida.

Escopo: espaço plano regularizado, lambda=(1,-1,0,0), eta=(1,0,0,0), ambas
as orientações, 40 componentes h/c por orientação. Foram reutilizados oito
núcleos e calculados outros 72. O resto bilocal antissimetrizado é zero nas
16 componentes como expressão racional em x; a diferença entre o resíduo
local anterior e o descendente é zero nos 16 polinômios completos em D.
Não se trata de igualdade apenas no momento zero.

A operação relevante é C_i(F)=R(d_i F)-d_i R(F). Portanto
-(d_i+lambda_i)R(F)=R(-(d_i+lambda_i)F)+C_i(F).
Variar apenas o contato local da corrente omitia essa última parcela.
Mantidos Ymetric/2+Ymixed+Yghost+Xmetric+Xmixed, os fatores da base simétrica,
q->q-lambda, q->D+lambda+eta e a adjunção ponderada D->-D-L.

Auditoria por segunda fórmula: C_i(F)/CE=-2 Res[x_i F/z]/CE, derivada do
regulador analítico. Ela usa os núcleos racionais salvos e a rotina de resíduo,
sem chamar contact() nem recalcular os loops. Reproduz as 16 componentes.
Omitir o contato ou inverter seu sinal deixa diferenças nas 16 componentes.
No controle00 em D=0: omissão=-2743/3840; sinal invertido=-2743/1920.
Esta auditoria usa uma rota algébrica independente, mas compartilha a rotina
básica de resíduos; não equivale a revisão externa de todo o cálculo.

Matriz: {m['checks']} verificações, CPU {m['cpu_seconds']}s, session19789 rc0.
Auditoria: {a['checks']} verificações, CPU {a['cpu_seconds']}s, rc0.
Total desta entrega: {checks} verificações, CPU {cpu}s.
Comandos: runtime SymPy A4, -X utf8 -B, current_distributional_descendant_matrix.py
e audit_current_descendant_matrix.py. Códigos de saída observados nas ferramentas;
sem captura independente de stdout em arquivo. JSONs e manifestos preservados.

Consequência: o resíduo isolado desse recorte não pode ser tratado como
obstrução homogênea sem incluir a inserção de corrente. Continua pendente
identificar integralmente as inserções da identidade quântica, tratar as
hipóteses de ordem um e estender o resultado para cutoffs gerais/curvatura.
Não foi estabelecido Q2 integral, nem anulação de classe de cohomologia.
O resultado não move o gate e não altera originais científicos/kernel.

A nota FR0B_CONSISTENCIA_LOCALIZADA_ORDEM2.md registra separadamente a condição
localizada da fonte primária e a expansão de ordem dois; não substitui a
identificação dos núcleos da bancada com suas inserções.

Orquestração: Kimi/MiMo prioritários na fila única. DeepSeek6309f0bf aceito
em STAGING_PRIORITY_CAPACITY, sem job nem execução, conforme mensagem oficial
da coordenação. Não duplicar unidades em andamento. Prazo A7.b20:32UTC.

Abertura SHA256={opening}.
'''
write(D/'DERIVACAO.md', report.encode('utf-8'))
write(OUT/'ENTREGA_016_MEDIDA_descida_distribucional_matriz16.md', report.encode('utf-8'))
put(D/'EXECUTION_RECEIPT.json', dict(at=now.isoformat(), completed=[
    dict(script='current_distributional_descendant_matrix.py',session_id=19789,rc=0,source='write_stdin terminal result'),
    dict(script='audit_current_descendant_matrix.py',rc=0,source='exec_command terminal result')],
    independent_stdout_file=False))
paths = [Path(__file__), D/'DERIVACAO.md', D/'EXECUTION_RECEIPT.json'] + [H/p for p in [
    'current_distributional_descendant_matrix.py', 'current_distributional_descendant_matrix/results.json',
    'current_distributional_descendant_matrix/manifest.json',
    'audit_current_descendant_matrix.py','current_descendant_matrix_independent_audit/results.json',
    'current_descendant_matrix_independent_audit/manifest.json',
    'FR0B_CONSISTENCIA_LOCALIZADA_ORDEM2.md',
    'orchestration_descendant_adjoint_skeptic/prepared_units.json']]
put(D/'manifest.json', dict(at=now.isoformat(),checks=checks,cpu_seconds=cpu,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False,gate_changed=False))
ledger = OUT/'LEDGER_016.jsonl'
append(ledger, json.dumps(dict(at=now.isoformat(),event='CURRENT_DESCENT_MATRIX16_AND_RESIDUE_AUDIT',
    target='A7.b',checks=checks,cpu_seconds=cpu,remote_call=False,
    manifest_sha256=sha(D/'manifest.json'))) + '\n')
cost = Decimal(0); seen=set()
for line in ledger.read_text('utf-8').splitlines():
    e=json.loads(line); v=e.get('cost_estimate_usd',e.get('cost_usd'))
    if v is None: continue
    key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
    if key and key in seen: continue
    if key: seen.add(key)
    cost += Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b:16/16 componentes da descida igualam o resíduo, resto bilocal zero; auditoria independente de contato e controles de omissão/sinal;{checks}checks CPU{cpu}s. Q2 integral OPEN. Custo conhecido parcial USD{cost}. Abertura SHA256={opening}.\n')
p=H/'CONTINUIDADE.json'; state=json.loads(p.read_bytes())
keys=['at','previous_goal_turn','completed_this_turn','next','pending_orchestration','partial_metered_cost_usd']
state.setdefault('head_history',[]).append({k:state.get(k) for k in keys})
state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
    completed_this_turn=['Full fixed-cutoff current descendant matches all16 measured hc defect components',
        'Independent regulator residue audit matches all16; omission and sign reversal rejected',
        'Localized primary-source consistency expanded to order2 with remaining identification explicit'],
    next=['Do not restart completed session19789; inspect this delivery',
        'Identify composite localized insertion and order1 normalization using pending Kimi/MiMo/DeepSeek reviews',
        'No new A7b dispatch after20:32UTC; A7c/d,A8,PartB/final remain'],
    pending_orchestration='Single coordinator owns transitions; Kimi/MiMo priority; DeepSeek6309 accepted STAGING_PRIORITY_CAPACITY with no job/execution',
    partial_metered_cost_usd=str(cost))
state['current_descendant_matrix_update']=dict(at=now.isoformat(),manifest=str(D/'manifest.json'),
    session_id=19789,status='COMPLETED_RC0',checks=checks,all16_match=True,
    general_cutoff_not_established=True,full_Q2=False,gate_changed=False)
state['current_descendant_probe_update']['own_processes'][0]['status']='COMPLETED_RC0'
state['current_descendant_probe_update']['full_matrix_not_yet_measured']=False
put(p,state,True)
for entry in json.loads((D/'manifest.json').read_bytes())['artifacts']:
    assert sha(Path(entry['path']))==entry['sha256']
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=checks,cpu_seconds=cpu,
    artifacts_verified=len(paths),partial_known_cost_usd=str(cost))))
