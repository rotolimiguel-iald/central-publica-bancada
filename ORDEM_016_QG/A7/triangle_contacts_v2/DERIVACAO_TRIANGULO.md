[DERIVED — resíduo de escala de três pontos; REAL — CAS; OPEN — coeficiente Ward completo]
# A7.b — triângulo principal com duas derivadas

Abertura sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

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
JSON e declara o predecessor. Ela terminou rc0: 26 checks,
7 controles negativos; wall 0.15553530002944171s,
CPU 0.15625s; Sympy 1.14.0.
Comando: `A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/triangle_contact_check_v2.py`.
Log: triangle_contacts_v2_run.log; hashes no manifesto.

É um coeficiente local de um subkernel de três pontos. Não foi construída toda
a parte finita de T3, não foram somados os vértices métricos/ghost/antifields,
termos curvos, inserções marcadas ou contatos de cutoff. Logo a primeira quebra
Q2 continua NÃO PAGA. A conta fornece um dado necessário à montagem, sem mudar
o item interagente da QG, o kernel, um.py ou o gate.
