"""Persist measured partial results and orchestration; never promote to QME."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib,json

HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,value):
    raw=value.encode('utf-8') if isinstance(value,str) else value
    if p.exists():
        old=p.read_bytes()
        if old==raw:return
        backup=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and raw;tmp.replace(p)
def js(p,value):save(p,json.dumps(value,ensure_ascii=False,indent=2))

now=datetime.now(timezone.utc).isoformat()
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
vr=json.loads((HERE/'metric_vertices/results.json').read_bytes())
br=json.loads((HERE/'metric_bubble/results.json').read_bytes())
catalog=json.loads((HERE/'orchestration_metric/prepared_units.json').read_bytes())
assert vr['checks_passed']==81 and br['checks_passed']==65
assert br['double_gauge_zero'] is False
for unit in catalog:
    assert sha(Path(unit['payload']))==unit['payload_sha256']
    receipt=json.loads((HERE/'orchestration_metric'/(unit['slug']+'_receipt.json')).read_bytes())
    for source in receipt['sources']:assert sha(Path(source['path']))==source['sha256']

js(HERE/'orchestration_metric/coordinator_acknowledgment.json',dict(
    at=now, source_thread_id='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    source='official send_message_to_thread incoming message',
    status='ACKNOWLEDGED_STAGED_NOT_SUBMITTED',
    units=3, order='after A7 contacts and all preceding catalogs',
    request_ids=[u['request_id'] for u in catalog],
    note='Coordinator confirmed three payload hashes and absence in queue; no new call yet'))

js(HERE/'metric_bubble/CONTROL_SCOPE_ERRATUM.json',dict(
    at=now,corrects='negative_controls.wrong_relative_determinant_sign',
    issue='Both proposed and opposite signs have nonzero e00 contraction. Nonzero alone cannot discriminate the relative sign.',
    accepted_scope='Arithmetic nonzero check only, not a successful sign-error detector.',
    other_control='metric_longitudinal_piece_discarded only rejects erasure of a measured nonzero piece',
    no_erasure_of_original_result=True))

vertex_report=f'''[DERIVED — vértice principal; REAL — CAS exato; OPEN — contribuição quântica completa]
# A7.b — Hessiana e vértice cúbico métricos

Abertura SHA256 `{opening}`. Data UTC {now}.

Usamos g=delta+h com h covariante, Fourier exp(+ipx), contrações euclidianas
do símbolo principal. A ação -sqrt(g)R/(2κ) é escrita em Gamma-Gamma módulo
divergência SOMENTE com cutoff constante. C=div(h)-d tr(h)/2 é linear e a
fixação +C²/(4κ) não acrescenta vértice cúbico. A transferência dos sinais
ao problema Lorentziano e contatos de derivadas do cutoff permanece separada.

O motor metric_principal_vertices.py retorna 16κ vezes a derivada cúbica da
ação, sem divisão adicional por3!. A conferência quadrática recupera
H_gf=p² I_tr/(4κ), inclusive a multiplicidade2 das componentes fora da diagonal.
Oito exemplos da identidade clássica cúbica verificam V3(Kv,H,J)+
V2(L_v H,J)+V2(H,L_v J)=0; quatro são não triviais. Isto é verificação exata
desses exemplos, não certificação automática de toda identidade polinomial.
Também foram conferidas seis permutações de Bose, dez direções de gauge na
Hessiana sem gauge e a família conforme, 16κ V3(I,I,I)=12Σp_i².

Comando Python314 -X utf8 -B A7/metric_vertex_check.py; rc0.
81 verificações e dois controles negativos; wall {vr['wall_seconds']}s,
CPU {vr['cpu_seconds']}s. Resultados, plano anterior e log no manifesto.
Nenhum dado de curvatura, coeficiente ghost1 ou QME foi certificado aqui.
'''
save(HERE/'metric_vertices/DERIVACAO_VERTICES.md',vertex_report)

bubble_report=f'''[REAL — coeficientes principais exatos; MEDIDA — cancelamento pretendido não obtido; OPEN — Ward completa]
# A7.b — bolha métrica e diferença longitudinal medida

Abertura SHA256 `{opening}`. Data UTC {now}.

Prescrição anterior ao cálculo: mesmo extrator radial log Λ_UV, denominadores
q²(q+p)², símbolo principal euclidiano. W_A=16κ V3(A,p,E_i,q,E_j,-p-q).
Na base simétrica de dez componentes, S0 é a inversa da forma I_tr: bloco
diagonal I4-ones4/2, seis entradas1/2 fora dele. Logo G_h=4κ S0/q² e
N_m=Tr(S0 W_A S0 W_B)/16. W é reconstruído por quinze avaliações inteiras
de um polinômio quadrático; uma avaliação fora dos nós confere cada matriz.

Na ordem trAB*p4, trA*trB*p4, (pAp*trB+pBp*trA)*p2, pABp*p2, pAp*pBp,
os coeficientes sobre A0=1/(8π²) foram:

    métrica: {br['metric_coefficients_over_A0']}
    ghosts:  {br['ghost_coefficients_over_A0']}
    -métrica/2+ghosts: {br['combined_Hessian_coefficients_over_hbar_A0']}

A combinação é a hipótese de normalização da Hessiana derivada formalmente de
Gamma1=(ħ/2)Trlog H-ħTrlog Q, antes da fase Lorentz. Não foi ajustada após o teste.
Para p=e0, A=B=E00, a peça métrica vale A0/4 e a ghost A0/16: a soma vale
-ħ A0/16. Usando K(e0)=2E00, a contração dupla vale -ħ A0/4; as outras nove
contrações de base são zero. Portanto o critério pretendido de cancelamento
duplo NÃO foi satisfeito por esta soma. Não é legítimo declarar anomalia:
faltam conferir identidade adequada, normalizações, termos/inserções BV e
contatos da prescrição. O resultado não contém cálculo de ghost1/forma4.

Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/metric_bubble_check.py;
rc0 significa que o cálculo e seus 65 checks terminaram, NÃO que o cancelamento
passou. Foram conferidos 55 pares tensoriais e dez interpolações fora dos nós.
Wall {br['wall_seconds']}s, CPU {br['cpu_seconds']}s.

Correção ao lado: o negativo wrong_relative_determinant_sign testa apenas
não nulidade, que também ocorre com o sinal proposto; não discrimina o erro.
O outro negativo apenas impede apagar a peça métrica não nula. Não anunciar
dois detectores de erro físico independentes. Errata preservada no manifesto.

Próximo passo: verificação independente do vértice/integração e da identidade
longitudinal com fontes BV; só então combinar curvatura, cutoff e normalizações
finitas. O Kimi recebeu uma unidade preparada especificamente para a identidade
e fatores, anterior a este resultado, sem ajustar seu payload depois da medida.
Nenhuma mudança no um.py, kernel, gate ou no modelo físico canônico.
'''
save(HERE/'metric_bubble/DERIVACAO_BOLHA_METRICA.md',bubble_report)
for folder,files in [
    ('metric_vertices',[HERE/'metric_principal_vertices.py',HERE/'metric_vertex_check.py',
      HERE/'metric_vertex_run.log',HERE/'metric_vertices/PRE_REGISTER.json',
      HERE/'metric_vertices/results.json',HERE/'metric_vertices/DERIVACAO_VERTICES.md']),
    ('metric_bubble',[HERE/'metric_bubble_check.py',HERE/'metric_bubble_run.log',
      HERE/'metric_bubble/PRE_REGISTER.json',HERE/'metric_bubble/results.json',
      HERE/'metric_bubble/CONTROL_SCOPE_ERRATUM.json',HERE/'metric_bubble/DERIVACAO_BOLHA_METRICA.md'])]:
    js(HERE/folder/'manifest.json',dict(at=now,opening_sha256=opening,
       artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files],
       full_ward_coefficient_computed=False,gate_changed=False))

save(OUT/'ENTREGA_016_A7b_vertices_e_bolha_metrica.md',vertex_report+'\n'+bubble_report)
save(OUT/'ENTREGA_016_MEDIDA_contracao_longitudinal_principal.md',bubble_report)

ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes()
marker='A7_METRIC_BUBBLE_AND_THREE_REVIEWS_20260924'
if marker.encode() not in raw:
    events=[dict(event=marker,at=now,target='A-7.b',provider='local',rc=0,
        metric_checks=81,bubble_checks=65,double_gauge_zero=False,
        quantum_anomaly_computed=False,opening_sha256=opening,
        metric_log_sha256=sha(HERE/'metric_vertex_run.log'),
        bubble_log_sha256=sha(HERE/'metric_bubble_run.log'),
        machine_cpu_seconds=vr['cpu_seconds']+br['cpu_seconds'])]
    events += [dict(event=marker,at=now,target='A-7.b',provider=u['provider'],
        request_id=u['request_id'],payload_sha256=u['payload_sha256'],
        phase='ACKNOWLEDGED_STAGED_NOT_SUBMITTED',external_execution=False,
        tokens=None,cost_usd=None,opening_sha256=opening) for u in catalog]
    save(ledger,raw+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line)
    cost=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))

rows='\n'.join(f"- {u['provider']}: {u['slug']} — `{u['request_id']}`." for u in catalog)
save(OUT/'ENTREGA_016_A7_orquestracao_metrica.md',f'''[REAL — prévias e recebimento conferidos; INPUT — três unidades preparadas]
# Mais tarefas A7.b para Kimi e MiMo

Abertura SHA256 `{opening}`; UTC {now}.

{rows}

Prévias selecionaram os provedores exigidos, com memória comum máxima e uma
chamada por unidade. A coordenação oficial confirmou hashes e staging após o
catálogo contacts. Estas três unidades AINDA NÃO têm job_id nem execução.
Não foi duplicada fila/worker. Catálogo: {HERE/'orchestration_metric/prepared_units.json'}.
Kimi concentra duas tarefas matemáticas; MiMo verifica o cálculo por outra via.
Os cinco jobs existentes permanecem preservados. Consumo destes novos pedidos
não informado; soma histórica de estimativas deduplicadas US${total}, parcial,
não equivalente à fatura nem ao custo da assinatura. O objetivo não é consumir
modelos por volume, mas obter verificações complementares utilizáveis no A7.b.
''')

continuity=HERE/'CONTINUIDADE.json';data=json.loads(continuity.read_bytes())
data.update(at=now,previous_goal_turn='PROGRESS',completed_this_turn=[
    'Metric principal cubic normalization:81checks/2controls',
    'Metric bubble:five coefficients and55basis pairs; double longitudinal cancellation failed',
    'Two Kimi and one MiMo new units previewed and acknowledged staged'],
    next=['Diagnose nonzero double-longitudinal sum without forcing cancellation',
          'Review independent metric/ghost signs and Slavnov/BV identity',
          'Continue curved and marked Ward contributions within A7.b timebox'],
    metric_vertices_manifest=str(HERE/'metric_vertices/manifest.json'),
    metric_bubble_manifest=str(HERE/'metric_bubble/manifest.json'),
    partial_metered_cost_usd=str(total),
    latest_orchestration=dict(catalog=str(HERE/'orchestration_metric/prepared_units.json'),
        status='ACKNOWLEDGED_STAGED_NOT_SUBMITTED',request_ids=[u['request_id'] for u in catalog]))
js(continuity,data)
progress=OUT/'ENTREGA_016_PROGRESSO.md';raw=progress.read_bytes()
if marker.encode() not in raw:
    save(progress,raw+f'\n- {now} — A7.b EM ANDAMENTO/MEDIDA:81checks vertices,65checks bolha; soma dupla longitudinal -hbar*A0/4, nao zero, nao anomalia demonstrada; Kimi2/MiMo1 preparados e recebidos, sem novos job_ids. CPU local {vr["cpu_seconds"]+br["cpu_seconds"]}s; bancada desta etapa ~0,23h (intervalo observado22:08–22:22UTC, sem repetir horas anteriores). Custo externo parcial registrado US${total}. Abertura {opening}. [{marker}]\n'.encode())
print(json.dumps(dict(status='DELIVERED_PARTIAL_WITH_FAILED_CANCELLATION',
    units_staged=3,full_ward=False,gate_changed=False,cost_partial=str(total)),ensure_ascii=False))
