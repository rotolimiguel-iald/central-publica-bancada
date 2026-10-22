"""Deliver the principal-symbol calculator and update bench progress."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
DEST=HERE/'one_loop_scale'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
    if isinstance(b,str):b=b.encode('utf-8')
    assert not p.exists() and b,str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
def replace(p,b):
    if isinstance(b,str):b=b.encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    old=p.read_bytes();new(p.with_name(p.name+'.bak_'+stamp),old)
    t=p.with_name(p.name+'.replacement_'+stamp);new(t,b);t.replace(p)
    assert p.read_bytes()==b
def append(p,s):replace(p,p.read_bytes()+s.encode('utf-8'))
r=json.loads((DEST/'results.json').read_bytes())
assert r['engine_sha256']==sha(HERE/'one_loop_scale_engine.py')
assert r['source_sha256']==sha(HERE/'one_loop_scale_check.py')
assert r['plan_sha256']==sha(DEST/'PRE_REGISTER.json')
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[REAL — CAS exato; DERIVED — expansão radial; OPEN — soma Ward]
# A7.b — extrator do coeficiente logarítmico principal a um laço

Abertura sha256 `{opening}`.

## Objeto e algoritmo

one_loop_scale_engine.py extrai o coeficiente de log Λ_UV de

    ∫ d⁴q/(2π)⁴ N(q) / ∏_e [(q+p_e)²+m_e²],

em assinatura EUCLIDIANA, para numerador polinomial e denominadores escalares
comutantes. É a álgebra angular do símbolo principal. O fundo Lorentziano087
continua o mesmo: o mapa para seus kernels causais exige fases de Fourier/Green,
fatores de fibra e Wick. Essa continuação não é executada automaticamente.

Escreva q=r n, n∈S³, t=1/r. Cada denominador tem série

    D_e^−1=r^−2 Σ d_(e,k)t^k,
    d_0=1, d_1=−2n·p_e,
    d_k=−2(n·p_e)d_(k−1)−(p_e²+m_e²)d_(k−2).

Para um monômio de grau j em q e m denominadores, só se extrai
k=j+4−2m da série produto. Se k<0, não há termo logarítmico desse monômio.
A média angular é

    <∏ n_i^(2a_i)> = ∏(2a_i−1)!!/[4·6·…·(4+2Σa_i−2)],

zero se algum expoente for ímpar; o fator area(S³)/(2π)^4 é1/(8π²).
O algoritmo termina e produz polinômio nos momentos externos e massas. Não
calcula parte finita ou divergências de potência.

Num ciclo ordinário de m vértices com no máximo duas derivadas por vértice,
j<=2m e k<=4. Inserções Ward marcadas e árvores anexas exigem conferir sua
própria contagem; a cota não é aplicada automaticamente. O código usa a ordem
efetivamente requerida pelo numerador que recebeu.

## Coeficientes e controles independentes

Defina A=1/(8π²), D0=q²+m0² e D1=(q+p)²+m1². Incluindo d⁴q/(2π)^4,

    [∫1/(D0D1)]log=A,
    [∫q_μ/(D0D1)]log=−A p_μ/2,
    [∫q_μq_ν/(D0D1)]log
      =A[p_μp_ν/3−δ_μν(p²/12+(m0²+m1²)/4)].

O tadpole tem coeficiente −A m², independente do deslocamento. A identidade
2p·q=D1−D0−p²−m1²+m0² é respeitada pelos coeficientes: combinar dois tadpoles
e a bolha escalar dá −A p². É identidade de numeradores, não a Ward BRST inteira.

O controle por parâmetros de Feynman calcula, por uma segunda fórmula,

    A∫_0^1 [−δ_μν Δ(x)/2+x²p_μp_ν]dx,
    Δ=(1−x)m0²+x m1²+x(1−x)p²,

e reproduz o tensor. Outro controle desloca q→q+a no numerador E denominadores:
o coeficiente permanece. Deslocar só denominadores é recusado. Descartar um
numerador ímpar antes de expandir denominadores também é erro: a bolha vetorial
é não nula. Momentos angulares foram conferidos ainda pela fórmula Dirichlet.

Nos ciclos m=2,…,6, os numeradores críticos q0^(2m−4), com deslocamentos/massas
zero, dão respectivamente1/(8π²),1/(32π²),1/(64π²),5/(512π²),7/(1024π²).
São coeficientes UV formais. Integral sem escala pode conter problema IR e
cancelamento UV/IR em outra regularização; não foi declarado seu valor integrado.
Não usamos integral sem escala zero para apagar um coeficiente UV.

## Evidência e limite

Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/one_loop_scale_check.py`.
rc0; {r['checks_passed']} checks e {r['negative_controls_detected']} negativos;
wall {r['wall_seconds']}s, CPU {r['cpu_seconds']}s, Sympy {r['sympy_version']}.
Log one_loop_scale_run.log, plano anterior e hashes no manifesto.

O motor recebe um kernel escalar de momento. Ainda falta fornecer a soma real
de numeradores/índices métricos, formas de fibra, curvatura, ghosts, antifields
e pesos combinatórios, além dos termos finitos e contatos EOM/cutoff. O teste
do triângulo anterior confere uma magnitude comum, sem substituir essas entradas.
Portanto Q2 continua NÃO PAGA. Não é novo módulo do um.py: é CAS de bancada
para o A7.b autorizado. Nenhum item interagente/gate ou original foi alterado.
'''
new(DEST/'DERIVACAO_EXTRATOR.md',report)
artifacts=[HERE/'one_loop_scale_engine.py',HERE/'one_loop_scale_check.py',DEST/'PRE_REGISTER.json',
    DEST/'results.json',DEST/'DERIVACAO_EXTRATOR.md',HERE/'one_loop_scale_run.log']
new(DEST/'manifest.json',json.dumps(dict(opening_sha256=opening,observed_rc=0,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in artifacts],
    quantum_anomaly_computed=False,gate_changed=False),ensure_ascii=False,indent=2))
new(OUT/'ENTREGA_016_A7b_extrator_um_laco.md',report)
now=datetime.now(timezone.utc).isoformat()
event=dict(event='A7B_EXACT_ONE_LOOP_SCALE_ENGINE_20260924',at=now,target='A7.b',
    provider='local_CAS',external_calls=0,manifest_sha256=sha(DEST/'manifest.json'),
    log_sha256=sha(HERE/'one_loop_scale_run.log'),rc=0,
    checks=r['checks_passed'],negative_controls=r['negative_controls_detected'],
    wall_seconds=r['wall_seconds'],cpu_seconds=r['cpu_seconds'],quantum_anomaly_computed=False)
ledger=OUT/'LEDGER_016.jsonl'
assert event['event'] not in ledger.read_text('utf-8-sig')
append(ledger,json.dumps(event,ensure_ascii=False)+'\n')
rows=[json.loads(x) for x in ledger.read_text('utf-8-sig').splitlines() if x.strip()]
costs={}
for row in rows:
    cost=row.get('cost_estimate_usd',row.get('cost_usd',row.get('custo_usd')))
    key=row.get('execution_id') or row.get('job_id') or row.get('request_id') or row.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n- {now} — A7.b EXTRATOR_UM_LACO: CAS parcial 45 checks/6 negativos rc0; máquina {r["wall_seconds"]/3600:.9f}h; bancada não instrumentada separadamente. Quebra NÃO PAGA. Zero chamada nova, custo parcial deduplicado US${total}.\n')
cp=HERE/'CONTINUIDADE.json'
c=json.loads(cp.read_bytes())
c.update(at=now,previous_goal_turn='PROGRESS',
    completed_this_turn=['Three-point differentiated triangle scale residue: 26 checks/7 controls',
        'Exact one-loop principal log-coefficient engine: 45 checks/6 controls',
        'Independent Feynman-parameter and routing checks'],
    triangle_manifest=str(HERE/'triangle_contacts_v2/manifest.json'),
    one_loop_engine_manifest=str(DEST/'manifest.json'),
    next=['Build actual metric/ghost/antifield contractions and finite normalization',
        'Compute ghost1/form4 Ward coefficient; scale residues alone do not pay it',
        'Receive queued prescriptions/reviews without changing or duplicating IDs'],
    quantum_anomaly_computed=False,partial_metered_cost_usd=str(total),
    previous_turn_failure='Triangle v1 JSON serialization failed; v2 only fixes integer export')
replace(cp,json.dumps(c,ensure_ascii=False,indent=2))
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7b_extrator_um_laco.md'),
    manifest_sha256=sha(DEST/'manifest.json'),partial_metered_cost_usd=str(total)),ensure_ascii=False))
