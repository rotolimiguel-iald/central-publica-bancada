"""Preserve the model-derived principal ghost numerator and its exact limitations."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
DEST=HERE/'ghost_bubble'
BV=HERE.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
    if isinstance(b,str):b=b.encode('utf-8')
    assert not p.exists() and b,str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
def replace(p,b):
    if isinstance(b,str):b=b.encode('utf-8')
    old=p.read_bytes();stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(p.with_name(p.name+'.bak_'+stamp),old)
    t=p.with_name(p.name+'.replacement_'+stamp);new(t,b);t.replace(p)
    assert p.read_bytes()==b
def append(p,s):replace(p,p.read_bytes()+s.encode('utf-8'))
r=json.loads((DEST/'results.json').read_bytes())
assert r['source_sha256']==sha(HERE/'ghost_bubble_check.py')
assert r['engine_sha256']==sha(HERE/'one_loop_scale_engine.py')
assert r['plan_sha256']==sha(DEST/'PRE_REGISTER.json')
plan=json.loads((DEST/'PRE_REGISTER.json').read_bytes())
assert plan['bv_source_sha256']==sha(BV)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[REAL — CAS de contribuição ghost; DERIVED — vértice principal; OPEN — soma Ward]
# A7.b — coeficientes tensoriais da bolha ghost do modelo

Abertura sha256 `{opening}`. Fonte BV069 sha256 `{sha(BV)}`.

## Vértice extraído da ação existente

A fonte069 §4 fixa C linear no campo métrico e interação +barc C(L_c h).
Não há vértice h²barc c nessa escolha de gauge linear. Antifields não são
propagadores. Aqui se calcula apenas o símbolo principal no espaço tangente,
em álgebra angular euclidiana, com Fourier exp(+ikx); termos com K/curvatura
ficam separados. O espaço-forma Lorentziano087 não foi trocado por outro fundo.

Para polarização simétrica H, momento métrico p, momento ghost de entrada k,
r=k+p e saída antighost −r, primeiro se escreve

    (L_c h)_ab,ρ = i[p_ρ H_ab+k_a H_ρb+k_b H_aρ],
    C_ν(L_c h)=i r^a(L_c h)_aν−(i r_ν/2)tr(L_c h).

O vértice resultante, com o sinal positivo da interação da fonte, é

    V_νρ(H,p,k)=−[p_ρ(Hr)_ν+(r·k)H_ρν+k_ν(Hr)_ρ
                    −r_ν p_ρ trH/2−r_ν(Hk)_ρ].

O CAS deriva V também por índices, compondo Lie e C sem usar a fórmula reduzida.
Em p=0 dá V=−k²H. A bolha usa o traço sobre os QUATRO índices vetoriais,

    N(A,B,p,q)=tr[V(B,−p,q+p)V(A,p,q)],
    I(A,B;p)=∫ d⁴q/(2π)^4 N/[q²(q+p)²].

O objeto I é o kernel numerador sem o sinal de laço ghost fechado, sem fator
de simetria/normalização da ação efetiva e sem fatores Wick iħ. Essa separação
foi registrada ANTES do cálculo. Portanto os números abaixo não devem ser
inseridos como amplitude física ou quebra Ward sem os fatores restantes.

## Os cinco coeficientes calculados

Com A0=1/(8π²) e notação pAp=pᵀAp, o coeficiente logarítmico é

    I_log/A0 = (1/12)tr(AB)(p²)² +(7/48)trA trB (p²)²
        −(1/8)(pAp trB+pBp trA)p²
        −(1/12)(pᵀABp)p² +(1/6)(pAp)(pBp).

A e B são polarizações, não o coeficiente angular A0. Esta é a base tensorial
par de grau4 em p, bilinear nas polarizações simétricas. Cinco escolhas
independentes determinam os coeficientes. A conta então verifica TODOS os55
pares não ordenados da base de10 matrizes simétricas em p=(1,0,0,0). Covariância
O(4), homogeneidade de grau4 e troca das pernas estendem essa determinação;
uma direção externa (1,2,−1,1) com duas matrizes não diagonais verifica novamente
a fórmula, sem ser usada no ajuste. O ponto p=0 segue por polinomialidade.

Outra derivação combina os denominadores por x∈[0,1], desloca q=l−xp e usa
Δ=x(1−x)p². Para um monômio de grau par j em l, o coeficiente log é
(-1)^(j/2)(j/2+1)Δ^(j/2) vezes sua média angular. Integrar x reproduz
os cinco casos independentes sem usar a expansão radial original.

Para A=B=e00 e p=e0, I_log=A0/16=1/(128π²), não zero. Isso refuta apenas
a transversalidade da peça isolada; não demonstra quebra da teoria completa.
Não se confunde ghost loop de número fantasma0 com a anomalia de número1.

## Evidência e correção de um rótulo de controle

rc0; {r['checks_passed']} checks e {r['negative_controls_detected']} negativos,
wall {r['wall_seconds']}s, CPU {r['cpu_seconds']}s, Sympy {r['sympy_version']}.
Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/ghost_bubble_check.py`.
Log ghost_bubble_run.log; plano anterior, fontes e resultados no manifesto.

Correção ao lado: o negativo chamado ghosts_treated_as_four_independent_scalar_vertices
apenas verifica que a contribuição da polarização e12 não pode ser zerada.
Não implementa nem compara quatro vértices escalares alternativos. Seu nome
é excessivo; o alcance medido fica registrado em CONTROL_LABEL_ERRATUM.json.
Os demais controles recusam o zero longitudinal e troca do termo de traço.

Faltam o sinal/normalização globais, as contribuições métricas, os termos de
curvatura, antifields e contatos de normalização/EOM/cutoff, e a soma de ghost1.
Este resultado já fornece um numerador REAL do modelo ao extrator, mas não
fixa todos os produtos temporais. Q2 continua NÃO PAGA; gate e originais intactos.
'''
new(DEST/'DERIVACAO_BOLHA_GHOST.md',report)
new(DEST/'CONTROL_LABEL_ERRATUM.json',json.dumps(dict(
    original='ghosts_treated_as_four_independent_scalar_vertices',
    actual_test='nonzero e12 polarization contribution rejects dropping this contribution',
    alternative_scalar_vertex_model_constructed=False,
    results_preserved=True),ensure_ascii=False,indent=2))
arts=[HERE/'ghost_bubble_check.py',HERE/'one_loop_scale_engine.py',DEST/'PRE_REGISTER.json',
    DEST/'results.json',DEST/'DERIVACAO_BOLHA_GHOST.md',DEST/'CONTROL_LABEL_ERRATUM.json',
    HERE/'ghost_bubble_run.log']
new(DEST/'manifest.json',json.dumps(dict(opening_sha256=opening,bv_source_sha256=sha(BV),
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in arts],observed_rc=0,
    full_Ward_coefficient=False,gate_changed=False),ensure_ascii=False,indent=2))
new(OUT/'ENTREGA_016_A7b_bolha_ghost_principal.md',report)
now=datetime.now(timezone.utc)
bench_start=datetime.fromisoformat('2026-09-24T21:46:38+00:00')
event=dict(event='A7B_PRINCIPAL_GHOST_BUBBLE_20260924',at=now.isoformat(),target='A7.b',
    provider='local_CAS',external_calls=0,manifest_sha256=sha(DEST/'manifest.json'),
    log_sha256=sha(HERE/'ghost_bubble_run.log'),rc=0,
    checks=r['checks_passed'],negative_controls=r['negative_controls_detected'],
    wall_seconds=r['wall_seconds'],cpu_seconds=r['cpu_seconds'],
    observed_continuation_interval_seconds=(now-bench_start).total_seconds(),
    interval_includes='reading, coordination, derivation, CAS and documentation; not CPU',
    quantum_anomaly_computed=False)
ledger=OUT/'LEDGER_016.jsonl'
assert event['event'] not in ledger.read_text('utf-8-sig')
append(ledger,json.dumps(event,ensure_ascii=False)+'\n')
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n- {event["at"]} — A7.b BOLHA_GHOST: cinco coeficientes principais, 65 checks/3 negativos rc0 (rótulo de um negativo corrigido ao lado). Máquina {r["wall_seconds"]/3600:.9f}h; intervalo observado desta continuação {event["observed_continuation_interval_seconds"]/3600:.6f}h, inclui os três cálculos/documentação/coordenação, não somar novamente como CPU. Quebra completa NÃO PAGA; zero chamada nova.\n')
cp=HERE/'CONTINUIDADE.json'
c=json.loads(cp.read_bytes())
c.update(at=event['at'],previous_goal_turn='PROGRESS',
    completed_this_turn=c.get('completed_this_turn',[])+['Principal model ghost bubble: five tensor coefficients, all55 basis pairs checked'],
    ghost_bubble_manifest=str(DEST/'manifest.json'),
    next=['Apply and verify complete loop signs/normalizations and metric vertices',
        'Add curvature, BV-marked vertices, local finite terms and contacts',
        'Compute full ghost1/form4 Ward coefficient before claiming A7.b paid',
        'Review Kimi B3a newly completed; avoid duplicating already compiled lemmas'],
    full_ward_coefficient_computed=False,
    A7b_timebox_exhausted=False)
replace(cp,json.dumps(c,ensure_ascii=False,indent=2))
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7b_bolha_ghost_principal.md'),
    manifest_sha256=sha(DEST/'manifest.json'),observed_bench_hours=event['observed_continuation_interval_seconds']/3600),ensure_ascii=False))
