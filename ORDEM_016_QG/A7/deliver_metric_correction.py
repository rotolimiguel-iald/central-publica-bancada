"""Append correction/evidence without overwriting cited predecessor artifacts."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):
    raw=data.encode('utf-8') if isinstance(data,str) else data
    if p.exists():
        old=p.read_bytes()
        if old==raw:return
        backup=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and raw;tmp.replace(p)
def js(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2))
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
old=HERE/'metric_bubble/results.json'
v2=json.loads((HERE/'metric_bubble_v2/results.json').read_bytes())
audit=json.loads((HERE/'metric_bubble_independent/results.json').read_bytes())
classical=json.loads((HERE/'metric_diagnostic/classical_results.json').read_bytes())
assert v2['double_gauge_zero'] and not classical['failures']
report=f'''[DERIVED — cancelamento principal quadrático; REAL — CAS exato independente; OPEN — Ward curva completa]
# A7.b — correção da contração e cancelamento métrico–ghost

Abertura SHA256 `{opening}`. UTC {now}.
Supersede os coeficientes métricos de metric_bubble/results.json, SHA256
`{sha(old)}`. A tentativa anterior e sua MEDIDA permanecem intactas.

## Erro identificado antes do novo cálculo

Os vértices são W_A(i,j;q)=16κ V3(A,p,E_i,q,E_j,-p-q) e W_B(k,l;q),
depois de inverter simultaneamente os momentos do segundo vértice. As linhas
conectam i a k e j a l. Portanto a soma é

    N_m = Σ W_A(i,j) W_B(k,l) S0(i,k) S0(j,l)/16
        = Tr(S0 W_A S0 W_B^T)/16.

O cálculo anterior omitiu a transposição. W não é simétrica a q fixado: a
simetria de Bose também troca q e -p-q. A soma explícita de quatro índices
confere a fórmula corrigida e recusa a anterior num caso não degenerado.
A inversa S0 foi também recalculada diretamente da forma da base, sem presumir
seus blocos. Nem vértice, gauge, ghost, peso de laço ou extrator foi ajustado.

## Coeficientes corrigidos e identidade

Com A0=1/(8π²), na ordem
trAB*p4, trA*trB*p4, (pAp*trB+pBp*trA)*p2, pABp*p2, pAp*pBp:

    métrica/A0 = [71/60, 27/40, -19/30, -11/5, 26/15]
    ghosts/A0  = [1/12, 7/48, -1/8, -1/12, 1/6]
    (-métrica/2+ghosts)/A0
                = [-61/120, -23/120, 23/120, 61/60, -7/10].

A ponderação é a Hessiana formal de (ħ/2)Trlog H-ħTrlog Q; fases Lorentz
permanecem separadas. Para p=e0, E00/E00, a métrica vale A0/8 e o ghost A0/16,
logo a soma é zero. As dez contrações duplas de base anulam. Mais forte:
para p,v,H simbólicos arbitrários, K_p(v)=p⊗v+v⊗p,

    F_log(K_p(v),H)=0.

Se T=I-pp^T/p², o polinômio bilinear pode ser escrito para p²≠0 como

    F_log(A,B)/(ħ A0) = (p²)²[-61/120 tr(T A T B)
                                      -23/120 tr(T A)tr(T B)].

A identidade polinomial não exige dividir por p² e inclui p=0.
Em termos das curvaturas LINEARIZADAS em espaço tangente plano,

    F_log/(ħ A0) = -61/30 Ric^(1)(A):Ric^(1)(B)
                         +19/60 R^(1)(A)R^(1)(B).

Essa expressão é a Hessiana quadrática calculada. Ela não determina por si
uma ação covariante não linear única nem os coeficientes curvos Kp² e K².
Não há termo log p4 do tadpole massless principal com vértice quartico de
somente duas derivadas: sua contagem não chega a q^-4 com quatro derivadas
externas. Isso NÃO descarta tadpoles com curvatura ou outras ordens.

## Verificações e próximo elo

metric_bubble_check_v2.py: rc0,68checks,3controles; wall {v2['wall_seconds']}s,
CPU {v2['cpu_seconds']}s. Inclui55pares da base e dez interpolações fora dos nós.
metric_bubble_independent_check.py: rc0,9checks,3controles; wall
{audit['wall_seconds']}s,CPU {audit['cpu_seconds']}s. Os cinco coeficientes foram
reproduzidos por parâmetros de Feynman e momentos Dirichlet, sem recorrência
radial; direção p=(1,2,-1,1) e polarizações densas deram20489/30 sobreA0 por
ambas as vias. A identidade longitudinal simples e a expressão em Ric/R foram
conferidas simbolicamente. Peças isoladas e troca do sinal relativo falham.
diagnose_metric_ward.py:440exemplos clássicos,276não triviais,zerofalhas.

O cancelamento é do termo logarítmico principal quadrático, no modelo truncado.
Não é a primeira quebra Q2 completa: faltam inserções BV, contatos e termos
finitos da prescrição, contribuições curvas e identidades de ordens superiores.
Não foi executada continuação Lorentziana de toda amplitude. Gate inalterado.
Próximo ramo do A7.b: termos curvos e marcados, preservando este resultado.
'''
save(HERE/'metric_bubble_v2/DERIVACAO_CORRIGIDA.md',report)
save(OUT/'ENTREGA_016_A7b_cancelamento_principal_corrigido.md',report)
for folder,files in [
 ('metric_diagnostic',[HERE/'diagnose_metric_ward.py',HERE/'metric_diagnostic_run.log',
     HERE/'metric_diagnostic/PRE_REGISTER.json',HERE/'metric_diagnostic/classical_results.json']),
 ('metric_bubble_v2',[HERE/'prepare_metric_bubble_v2.py',HERE/'metric_bubble_check_v2.py',
     HERE/'metric_bubble_v2_run.log',HERE/'metric_bubble_v2/PRE_REGISTER.json',
     HERE/'metric_bubble_v2/results.json',HERE/'metric_bubble_v2/DERIVACAO_CORRIGIDA.md']),
 ('metric_bubble_independent',[HERE/'metric_bubble_independent_check.py',HERE/'metric_bubble_independent_run.log',
     HERE/'metric_bubble_independent/PRE_REGISTER.json',HERE/'metric_bubble_independent/results.json'])]:
    js(HERE/folder/'manifest.json',dict(at=now,opening_sha256=opening,
       artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files],
       full_Q2=False,gate_changed=False))
ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_METRIC_WICK_SLOT_CORRECTION_20260924'
if marker.encode() not in raw:
    e=dict(event=marker,at=now,provider='local',target='A-7.b',phase='MEASURED_CORRECTION',
        opening_sha256=opening,superseded_result_sha256=sha(old),
        corrected_manifest_sha256=sha(HERE/'metric_bubble_v2/manifest.json'),
        independent_manifest_sha256=sha(HERE/'metric_bubble_independent/manifest.json'),
        rc=0,double_longitudinal_zero=True,single_longitudinal_zero=True,
        classical_checks=440,metric_checks=68,independent_checks=9,
        cpu_seconds=v2['cpu_seconds']+audit['cpu_seconds']+classical['cpu_seconds'],
        full_Q2=False,gate_changed=False)
    save(ledger,raw+(json.dumps(e,ensure_ascii=False)+'\n').encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);value=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if value is not None and key:costs[key]=Decimal(str(value))
total=sum(costs.values(),Decimal(0))
p=HERE/'CONTINUIDADE.json';d=json.loads(p.read_bytes())
d.update(at=now,previous_goal_turn='PROGRESS',
    completed_this_turn=['Missing transpose in metric Wick contraction diagnosed, corrected in v2',
        '68metric checks +9independent checks; polynomial single Ward zero',
        '440classical Ward examples; principal quadratic curvature bilinear'],
    next=['Curvature and marked BV contributions in same A7.b prescription',
        'Replace unsubmitted Kimi metric payload by additive correction only if not yet registered',
        'Full ghost1/form4 coefficient and finite contacts remain OPEN'],
    metric_bubble_corrected_manifest=str(HERE/'metric_bubble_v2/manifest.json'),
    metric_bubble_independent_manifest=str(HERE/'metric_bubble_independent/manifest.json'),
    prior_failure_diagnosed='Missing transpose W_B in fixed momentum routing; no gate or source vertex change',
    full_ward_coefficient_computed=False,A7b_timebox_exhausted=False,
    partial_metered_cost_usd=str(total))
js(p,d)
progress=OUT/'ENTREGA_016_PROGRESSO.md';raw=progress.read_bytes()
if marker.encode() not in raw:
    save(progress,raw+f'\n- {now} — A7.b PROGRESSO: transposicao Wick corrigida;68checks metricos,9independentes,440classicos; Ward principal quadratica simples anula exatamente. Q2 completa continua NAO PAGA. CPU {v2["cpu_seconds"]+audit["cpu_seconds"]+classical["cpu_seconds"]}s; bancada observada22:25–22:33UTC ~0,13h, sem horas anteriores. Custo externo parcial US${total}. Abertura {opening}. [{marker}]\n'.encode())
print(json.dumps(dict(report=str(OUT/'ENTREGA_016_A7b_cancelamento_principal_corrigido.md'),
    verified_single_longitudinal=True,full_Q2=False,gate_changed=False),ensure_ascii=False))
