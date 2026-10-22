"""Deliver a three-point scale coefficient, not a BRST anomaly claim."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
DEST=HERE/'triangle_contacts_v2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
    if isinstance(b,str):b=b.encode('utf-8')
    assert not p.exists() and b,str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.replace(p)
def append(p,s):
    old=p.read_bytes();stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    new(p.with_name(p.name+'.bak_'+stamp),old)
    t=p.with_name(p.name+'.replacement_'+stamp)
    new(t,old+s.encode('utf-8'));t.replace(p)
    assert p.read_bytes()==old+s.encode('utf-8')
r=json.loads((DEST/'results.json').read_bytes())
assert r['source_sha256']==sha(HERE/'triangle_contact_check_v2.py')
assert r['plan_sha256']==sha(DEST/'PRE_REGISTER.json')
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — resíduo de escala de três pontos; REAL — CAS; OPEN — coeficiente Ward completo]
# A7.b — triângulo principal com duas derivadas

Abertura sha256 `{opening}`.

## Objeto e prescrição

Fixe η=diag(1,−1,−1,−1), f(x)=1/(x²−i0), □f=Cδ, C=4iπ².
No espaço de duas coordenadas relativas, de dimensão8, tome

    a=x, b=y, c=x−y,       F(x,y)=f(a)f(b)f(c).

Os produtos fora da diagonal total são os causais, incluindo derivadas
distribucionais nas diagonais parciais. Não se usa só a função fora do cone.
F tem grau de escala6<8, logo sua extensão é única e homogênea.
Aplicar duas derivadas numa mesma aresta define A_e,μν de grau8.
A derivação exige existência dos produtos causais fora da origem, como no069.

[KNOWN] Hollands, Lema6/Proposição1, garante extensão Lorentz-covariante quase
homogênea para distribuições tensoriais. Na igualdade grau=dimensão, a liberdade
e o resíduo de Euler são coeficientes invariantes vezes δ, sem derivadas.
Isso não é um teorema de cancelamento de anomalias gravitacionais.
Fonte conferida: https://arxiv.org/html/0705.3340v4, §3.3, eq173–174/205–208.

Antes do CAS, fixou-se: estender a parte simétrica sem traço de A_e de modo
homogêneo e Lorentz-covariante; fixar seu traço pelo contato EOM e pelo R2 já
escolhido. Por exemplo,

    tr A_a = C δ(x) R2(y).

Isso fixa a extensão deste tensor, pois o único tensor constante simétrico
Lorentz-invariante de posto2 é múltiplo de η, e nenhum é sem traço não nulo.
O CAS confere essa última afirmação resolvendo as seis equações infinitesimais
de boosts/rotações. A existência distribucional vem do teorema importado, não
dessa matriz finita. O mesmo argumento mostra que a extensão sem traço é
homogênea: seu possível resíduo de escala seria um tensor invariante sem traço.

## Coeficiente exato e orientação das arestas

Escreva S8=x·∂x+y·∂y+8. A conta primitiva deu S4 R2=−Cδ/2.
Portanto a identidade do traço implica

    tr(S8 R(A_a)) = −C² δ(x)δ(y)/2,
    S8 R(A_a,μν) = −(C²/8)η_μν δ(x)δ(y).

O mesmo coeficiente vale nas arestas b,c: as mudanças de coordenadas relativas
têm módulo de determinante1. A parte sem traço não contribui a esse resíduo.
Com escala de referência μ_R e sem novos termos locais correndo arbitrariamente,
esse também é o coeficiente de μ_R∂_(μ_R). Não é valor da parte finita inteira.

Para derivadas em arestas diferentes, B_ef,μν, tome A=−C²/8. As derivadas
coordenadas de F têm resíduo zero, pois S8∂i∂j F=∂i∂j S6F=0. Com

    J = [[1,0],[0,1],[1,−1]],

isso exige Jᵀ M J=0 para a matriz M dos coeficientes entre arestas, com
diagonal (A,A,A). A solução é única:

    M = A [[ 1,−1,−1],
           [−1, 1, 1],
           [−1, 1, 1]] = A (1,−1,−1)ᵀ(1,−1,−1).

Assim os cruzamentos ab e ac têm −A, enquanto bc tem +A. Todos os sinais
dependem dos argumentos declarados a=x,b=y,c=x−y. Inverter uma aresta muda
a atribuição das derivadas. A parte antissimétrica não tem resíduo constante
Lorentz-invariante. Estas relações usam resíduos de Euler: diferenças finitas
locais entre extensões têm S8δ8=0 e não modificam a conta.

Para G0=−if/(4π²), inverso principal de □ na convenção já fixada,

    μ_R∂_(μ_R) R[(∂μ∂ν G0)(x) G0(y) G0(x−y)]
      = i/(32π²) η_μν δ(x)δ(y).

Ainda faltam fatores Wick iħ, formas de fibra, vértices, pesos de simetria e
sinais ghost. Um controle independente da magnitude usa a integral angular
euclidiana ∫S³ n0² dΩ=π²/2: dividida por (2π)^4 dá1/(32π²), o coeficiente
logarítmico radial de qμqν/(q²)^3. Esse controle não prova a continuação
Lorentziana nem seu sinal; esses dependem da convenção de Green fixada acima.

## Evidência e alcance

Primeira execução rc1 na serialização de inteiros Sympy; código/plano/falha
preservados em triangle_contacts. A versão v2 só converte esses inteiros para
JSON e declara o predecessor. Ela terminou rc0: {r['checks_passed']} checks,
{r['negative_controls_detected']} controles negativos; wall {r['wall_seconds']}s,
CPU {r['cpu_seconds']}s; Sympy {r['sympy_version']}.
Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/triangle_contact_check_v2.py`.
Log: triangle_contacts_v2_run.log; hashes no manifesto.

É um coeficiente local de um subkernel de três pontos. Não foi construída toda
a parte finita de T3, não foram somados os vértices métricos/ghost/antifields,
termos curvos, inserções marcadas ou contatos de cutoff. Logo a primeira quebra
Q2 continua NÃO PAGA. A conta fornece um dado necessário à montagem, sem mudar
o item interagente da QG, o kernel, um.py ou o gate.
'''
new(DEST/'DERIVACAO_TRIANGULO.md',report)
artifacts=[HERE/'triangle_contact_check_v2.py',DEST/'PRE_REGISTER.json',
    DEST/'results.json',DEST/'DERIVACAO_TRIANGULO.md',HERE/'triangle_contacts_v2_run.log',
    HERE/'triangle_contacts/failure.json',HERE/'triangle_contact_check.py']
new(DEST/'manifest.json',json.dumps(dict(opening_sha256=opening,observed_rc=0,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in artifacts],
    quantum_anomaly_computed=False,full_finite_T3_constructed=False),ensure_ascii=False,indent=2))
new(OUT/'ENTREGA_016_A7b_contato_triangular.md',report)
event=dict(event='A7B_TRIANGLE_SCALE_CONTACT_20260924',at=datetime.now(timezone.utc).isoformat(),
    target='A7.b',provider='local_CAS',external_calls=0,
    manifest_sha256=sha(DEST/'manifest.json'),rc=0,prior_rc=1,
    log_sha256=sha(HERE/'triangle_contacts_v2_run.log'),
    wall_seconds=r['wall_seconds'],cpu_seconds=r['cpu_seconds'],
    checks=r['checks_passed'],negative_controls=r['negative_controls_detected'],
    quantum_anomaly_computed=False)
ledger=OUT/'LEDGER_016.jsonl'
assert event['event'] not in ledger.read_text('utf-8-sig')
append(ledger,json.dumps(event,ensure_ascii=False)+'\n')
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n- {event["at"]} — A7.b TRIANGULO: resíduo de escala de subkernel, 26 checks/7 negativos rc0; v1 rc1 serialização preservado. Máquina v2 {r["wall_seconds"]/3600:.9f}h; bancada não instrumentada. Quebra Ward NÃO PAGA, zero chamadas novas.\n')
print(json.dumps(dict(delivery=str(OUT/'ENTREGA_016_A7b_contato_triangular.md'),manifest_sha256=sha(DEST/'manifest.json')),ensure_ascii=False))
