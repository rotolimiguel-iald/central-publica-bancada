"""Record partial BV calculations and use the existing finite-gap proof."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
A6=HERE.parent/'A6_EQUACAO_DA_VERDADE'
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
def js(p,obj):save(p,json.dumps(obj,ensure_ascii=False,indent=2))
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
ar=json.loads((HERE/'antifield_vertex/results.json').read_bytes())
pr=json.loads((HERE/'principal_bv_identity/results.json').read_bytes())
tr=json.loads((HERE/'ghost_antifield_triangle/results.json').read_bytes())
assert ar['einstein_Hessian_of_source_zero']
assert tr['constant_multiple_of_coordinate_candidate_on_tested_cases'] is False
report=f'''[DERIVED — setor logarítmico principal BV; REAL — CAS exato; OPEN — anomalia causal finita]
# A7.b — primeira inserção antifield–ghost e identidade hc

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.

Fonte BV069: h* L_c h e +barc C(L_c h), com C de fundo linear. Antifields
são fontes externas sem propagador. Escrevemos o vértice da fonte como iU:

    U_m(T,H,k,l)=k_m tr(T H)+2(H T l)_m.

T é a polarização simétrica de h*, H a métrica, k o momento métrico e l o
momento ghost. Derivação por índices confere U com a derivada de Lie. A bolha
externa h*(-p),c(p)=v contém h(q),c(p-q) e vértice ghost V(H,-q,p). Seu
numerador sem peso global é Σ U_m(T,E_i,q,p-q) S0_ij V_mρ(E_j,-q,p)vρ.
Denominadores q²(q-p)²; mesma extração log Λ_UV euclidiana. O fator fonte i,
4κ métrico, sinal do inverso ghost e convenções Grassmann globais ficam
explicitamente fora dos números abaixo. Eles não afetam as anulações que
ocorrem separadamente.

## Resultado medido

Sobre A0=1/(8π²), a correção é <T,R(p)v>, com

    R(p)v= -3/8 p²(p⊗v+v⊗p)+1/2(p⊗p)(p·v).
    F(p)v= -3/8 p²v+1/4 p(p·v),     R=K_p F.

Não apareceu o terceiro tensor permitido p² I(p·v): seu coeficiente foi zero,
sem ser imposto no ajuste. Logo a Hessiana de Einstein SEM gauge anula R.
Já a parte métrica Σ_log calculada na entrega precedente anula K_p. No setor
hc de referência plana principal, o coeficiente logarítmico de

    Σ_log K_p + H_EH R_log

é zero, inclusive antes de fixar a fase relativa, porque ambas as parcelas
anulam separadamente. Mantemos b na identidade BV; eliminar b do propagador
interno não permite trocar H_EH por H_gf nessa equação com b=0.

O vértice antighost é obtido do mesmo U aplicando C: V=-U(C_p^T e,H,k,l)
depois de retirar os fatores i. A linearidade da integral dá o kernel ghost
sem peso -C_p R=+3/8 p4 I-1/4 p² pp^T, compatível com Q(p)F(p), Q=-p²I.
Isto é uma identidade entre os kernels marcados, não uma nova contribuição
de ghost duplicada na soma.

Uma mudança LOCAL c_old=(I+εF)c, com transformação cotangente inversa do
antifield, reproduz essa estrutura livre. Sua extensão algébrica do colchete é
δ_F B=B(Fv,w)+B(v,Fw)-F B(v,w). Ela satisfaz Jacobi por transporte da operação,
e64exemplos Fourier verificam também o termo de primeira ordem. Isso é uma
construção de mudança de coordenadas, NÃO o cálculo do triângulo quântico.

## Evidência e alcance

antifield_vertex_check.py: rc0,47checks,2negativos; wall {ar['wall_seconds']}s,
CPU {ar['cpu_seconds']}s. Quarenta pares da base, direção não axial,
vértice de Lie por índices, antighost e parâmetros de Feynman independentes.
principal_bv_identity_check.py: rc0,134checks,2negativos; wall
{pr['wall_seconds']}s,CPU {pr['cpu_seconds']}s. As identidades hc são polinomiais
em momento/polarização arbitrários; Jacobi foi checada nos64trios escolhidos,
além do argumento algébrico de transporte.

É o cancelamento LOGARÍTMICO principal do componente hc. Não foi calculada a
parte finita da anomalia causal A(e^V), nem o mapa completo entre a 1PI e a
prescrição causal com cutoffs. Curvatura, contatos, pesos globais completos e
vértices marcados superiores continuam obrigações distintas. Q2 não está paga;
nenhuma alteração de kernel/um.py/gate.
'''
save(HERE/'antifield_vertex/DERIVACAO_FONTE.md',report)
save(OUT/'ENTREGA_016_A7b_fonte_antifield_e_Ward_hc.md',report)
triangle_report=f'''[REAL — triângulo principal sem peso global; MEDIDA — redefinição bilinear não basta]
# A7.b — c* c c: próximo vértice marcado calculado

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.

A fonte é c*_ρ c^μ∂_μc^ρ. Seu vértice de duas pernas ghost, retirando i,
é T_ab=(l_a Y_b-k_b Y_a), onde Y é a polarização de c* e k,l são os dois
momentos ghost. O diagrama1PI usa essa fonte e dois vértices barc C(L_c h).
Uma linha métrica une esses dois vértices; duas linhas ghost os ligam à fonte.
Para externos c(p)=v,c(r)=w,c*(-p-r)=Y, fixamos k=q+p,l=r-q. O numerador é

    Σ S0_ij [ (l·V(E_i,q,p)v)(Y·V(E_j,-q,r)w)
             -(Y·V(E_i,q,p)v)(k·V(E_j,-q,r)w) ],

com denominadores q²(q+p)²(q-r)². Fatores globais4κ,i e pesos Grassmann/ação
estão separados: o resultado é um kernel numérico sem peso global completo.

Controles: troca das duas pernas ghost inverte o sinal depois de q→-q,
diretamente no numerador e após a extração. Uma integração independente por
Feynman usa x,y>=0,x+y<=1, shift=xp-yr e Δ=x p²+y r²-(xp-yr)². Para termo
l^(2a) em três denominadores, a≥1, seu log UV tem fator
2(-1)^(a-1) binomial(a+1,2) Δ^(a-1), incluindo o peso simplex2; momentos
angulares Dirichlet reproduzem seis casos de eixo e um caso não axial.

## Medida que limita a simplificação

Com p=e0,r=e1,Y=e0,v=e0,w=e1, o coeficiente sobreA0 é7/24. A extensão por
coordenadas δ_F B derivada da bolha h*c dá ZERO no mesmo caso. Logo nem um
fator global resolve a diferença. No teste não axial o triângulo deu1165/24
e a candidata de coordenadas -27/4. As sete componentes estão em results.json.

Não é uma anomalia demonstrada. A bolha h*c sozinha não determina as correções
quânticas de todos os vértices da álgebra de gauge. A Ward superior envolve
também fontes dependentes de h; impô-la a c*cc isoladamente é truncá-la.
Próximo elo do A7.b: h*hc e suas relações com estes termos, mantendo curvatura,
cutoff e contatos finitos visíveis. O triângulo não foi apagado nem ajustado
para concordar com a candidata bilinear.

Comando A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/ghost_antifield_triangle_check.py; rc0,20checks,1controle não nulo;
wall {tr['wall_seconds']}s,CPU {tr['cpu_seconds']}s. Plano anterior, código,
resultados e log no manifesto. Não há QME/gate novo nem prova da teoria física.
'''
save(HERE/'ghost_antifield_triangle/DERIVACAO_TRIANGULO_GHOST.md',triangle_report)
save(OUT/'ENTREGA_016_A7b_triangulo_ghost_antifield.md',triangle_report)
save(OUT/'ENTREGA_016_MEDIDA_redefinicao_ghost_bilinear_insuficiente.md',triangle_report)

groups=[('antifield_vertex','antifield_vertex_check.py','antifield_vertex_run.log',['DERIVACAO_FONTE.md']),
        ('principal_bv_identity','principal_bv_identity_check.py','principal_bv_identity_run.log',[]),
        ('ghost_antifield_triangle','ghost_antifield_triangle_check.py','ghost_antifield_triangle_run.log',['DERIVACAO_TRIANGULO_GHOST.md'])]
for folder,script,log,extra in groups:
    files=[HERE/script,HERE/log,HERE/folder/'PRE_REGISTER.json',HERE/folder/'results.json']+[HERE/folder/x for x in extra]
    js(HERE/folder/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,
        artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files],full_Q2=False,gate_changed=False))

# Compare the returned Kimi review to the actual already-compiled finite-gap source.
job='46bc7f7d-0b2c-4238-892e-e9280a95cfd3';response=A6/'received_reviews'/(job+'.md')
receipt=json.loads((A6/'received_reviews'/(job+'.json')).read_bytes())
assert sha(response)==receipt['response_sha256']
src=A6/'B_fechamentos/FiniteGapRate_v2.lean';log=A6/'B_fechamentos/finite_gap_02.log'
comp=json.loads((A6/'B_fechamentos/finite_gap_02.json').read_bytes())
audit=json.loads((A6/'B_fechamentos/finite_gap_02_audit.json').read_bytes())
assert comp['rc']==0 and sha(src)==comp['source_sha256'] and sha(log)==comp['log_sha256']
assert audit['n_declaracoes_auditadas']==3 and not audit['sorry'] and not audit['fora_do_trio']
review=f'''[REAL — comparação com prova compilada existente; DECLARADO — esqueleto do Kimi]
# Revisão local Kimi A6.B1b

Abertura SHA256 `{opening}`. UTC {now.isoformat()}.
Resposta integral lida: `{response}`, SHA256 `{sha(response)}`.
Execução única `{receipt['execution_id']}`; uso informado no recibo, sem nova chamada.

O argumento por base ortonormal e Parseval preserva a constante1 e coincide
com finite_gap_norm_rate em FiniteGapRate_v2.lean. Ali o gap pertence aos mesmos
eigenvalues da base; projeta fora o kernel, inclui H=0/dimensão0, e exige s>=0,
γ>0. A positividade extra do parecer é redundante com a hipótese do gap.
Igualdade de norma para todos s requer gap atingido e complemento não nulo;
em s=0 isolado ela não identifica o gap. O fluxo dissipativo não é modular unitário.

Recibo local existente rc0; fonte `{sha(src)}`, log `{sha(log)}`, auditoria3/3,
somente propext/Classical.choice/Quot.sound, zero sorry. Conferidos em disco,
sem nova compilação nesta rodada. Reutilizar essa prova, não criar novo módulo.

O esqueleto Kimi não está compilado, lista APIs candidatas e tem sorry explícito
na extensão opcional. No ramo hF1, após reescrever b_i=0, h1 fica0=1; o uso
one_ne_zero h1 tem orientação incorreta. A contradição seria zero_ne_one h1,
ou one_ne_zero h1.symm. Não transplantei esse código nem substituí a prova pronta.
Parecer útil como conferência independente escrita, não certificado de kernel.
'''
save(A6/'received_reviews/REVISAO_KIMI_A6_B1b.md',review)

ledger=OUT/'LEDGER_016.jsonl';raw=ledger.read_bytes();marker='A7_PRINCIPAL_BV_SOURCE_AND_TRIANGLE_20260924'
cpu=ar['cpu_seconds']+pr['cpu_seconds']+tr['cpu_seconds']
if marker.encode() not in raw:
    events=[dict(event=marker,at=now.isoformat(),provider='local',target='A-7.b',
        opening_sha256=opening,rc=0,antifield_checks=47,BV_checks=134,triangle_checks=20,
        source_manifest_sha256=sha(HERE/'antifield_vertex/manifest.json'),
        triangle_manifest_sha256=sha(HERE/'ghost_antifield_triangle/manifest.json'),
        bilinear_log_hc_zero=True,ghost_coordinate_change_insufficient=True,cpu_seconds=cpu,full_Q2=False),
      dict(event='A6_KIMI_FINITE_GAP_REVIEWED_REUSING_COMPILED_SOURCE',at=now.isoformat(),
        provider='kimi',job_id=job,execution_id=receipt['execution_id'],
        response_sha256=sha(response),review_sha256=sha(A6/'received_reviews/REVISAO_KIMI_A6_B1b.md'),
        new_external_execution=False,new_compilation=False,opening_sha256=opening)]
    save(ledger,raw+''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events).encode())
costs={}
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);cost=e.get('cost_estimate_usd',e.get('cost_usd',e.get('custo_usd')))
    key=e.get('execution_id') or e.get('job_id') or e.get('request_id') or e.get('execution_task_id')
    if cost is not None and key:costs[key]=Decimal(str(cost))
total=sum(costs.values(),Decimal(0))
first=datetime.fromisoformat(json.loads((HERE/'antifield_vertex/PRE_REGISTER.json').read_bytes())['at'])
elapsed=(now-first).total_seconds()/3600
p=HERE/'CONTINUIDADE.json';d=json.loads(p.read_bytes())
d.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
    'h*c principal one-loop source:47checks, pure gauge R=K F',
    'Logarithmic hc BV identity:134checks, independent of relative global factor',
    'c*cc triangle:20checks; local ghost-coordinate change alone fails tested components',
    'Kimi B1b recovered and reviewed; reuse existing3theorem audited module'],
    next=['Compute h*hc marked vertex and higher Ward relations, not c*cc in isolation',
          'Curvature, cutoff and finite causal anomaly remain OPEN',
          'Recover A7 reviews in existing queue; do not duplicate provider calls'],
    antifield_manifest=str(HERE/'antifield_vertex/manifest.json'),
    principal_BV_manifest=str(HERE/'principal_bv_identity/manifest.json'),
    ghost_triangle_manifest=str(HERE/'ghost_antifield_triangle/manifest.json'),
    partial_metered_cost_usd=str(total),full_ward_coefficient_computed=False,A7b_timebox_exhausted=False)
d['pending_orchestration']='Kimi temporal_prescription registered jobba337b71-5345-44e7-8481-04a24ba1569e; MiMo C1 executing single call; rest staged'
js(p,d)
progress=OUT/'ENTREGA_016_PROGRESSO.md';raw=progress.read_bytes()
if marker.encode() not in raw:
    save(progress,raw+f'\n- {now.isoformat()} — A7.b PROGRESSO: h*c47checks, BV principal134checks, c*cc20checks. Loghc anula; redefinicao bilinear nao explica triangulo, proximo h*hc. KimiB1b revisado sem modulo/recompilacao novos. CPU local {cpu}s; intervalo instrumentado primeiro plano→entrega {elapsed:.6f}h, preparacao anterior nao cronometrada. Custo externo parcial US${total}. Abertura {opening}. [{marker}]\n'.encode())
count=0
for folder,_,_,_ in groups:
    for a in json.loads((HERE/folder/'manifest.json').read_bytes())['artifacts']:
        assert sha(Path(a['path']))==a['sha256'];count+=1
print(json.dumps(dict(delivered=True,artifacts_verified=count,new_provider_calls=0,new_Lean_modules=0,
    instrumented_hours=elapsed,cpu_seconds=cpu,full_Q2=False,gate_changed=False),ensure_ascii=False))
