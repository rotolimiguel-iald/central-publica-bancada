[DERIVED — identidade polinomial principal completa h*cc; REAL — CAS exato; OPEN — anomalia causal finita]
# A7.b — do teste de exemplos à identidade tensorial

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T23:23:17.580934+00:00.

A entrega anterior mediu oito exemplos; esta retira a restrição a exemplos
para o MESMO componente logarítmico principal, não para a QME inteira.
Mantêm-se h*hc=G-M/4, a fonte ghost, os fatores4iκA0, o modelo087 e o gauge
de fundo linear. Nenhuma nova hipótese dinâmica ou camada de kernel entrou.

## Teorema no escopo principal

Se B1 é o triângulo c*cc calculado, R1 as duas inserções h*hc e
R0(p)v=-3/8 p²K_pv+1/2 pp^T(p·v), então, como polinômio nos momentos e
polarizações do espaço Euclidiano tangente4D,

    K_(p+r) B1(v,w)+R0(p+r)B(v,w)-L_vR0(r)w+L_wR0(p)v
                       -R1(K_rw,v)+R1(K_pv,w)=0.

Aqui K_pv=p⊗v+v⊗p e B=(v·r)w-(w·p)v. A0=1/(8π²) foi retirado de
todos os coeficientes; é logΛ, não logΛ². As fases globais Lorentzianas
e a prescrição de contatos finitos não são fixadas por esta identidade.

## Completude da demonstração CAS

1. Todas as operações usam somente a métrica Euclidiana, contrações tensoriais
e momentos angulares O(4). Qualquer par p,r pode ser levado ao plano
p=a e0,r=b e0+c e1 por uma transformação O(4). a,b,c permanecem variáveis
ALGÉBRICAS independentes; não foram interpolados em valores numéricos.
Casos degenerados estão incluídos por continuidade polinomial.
2. O resíduo é linear na fonte simétrica T e bilinear em v,w. As10matrizes
simétricas e4vetores de cada ghost constituem uma base completa:10×4×4=160.
O programa calculou cada resíduo no anel QQ[q0,q1,q2,q3,a,b,c] e todos
ficaram exatamente zero. Em48polarizações há parcelas não nulas antes da soma.
3. A soma de fibras foi refeita por Σ Sij Ei⊗Ej=I_tr, não pelo código de
matrizes10×10 usado nos exemplos. Fonte U e vértice ghost foram comparados
com seus índices diretos (400 e160checagens); completude da fibra,100pares.
4. A redução do cúbico usa a Ward clássica W(Kv,A,B)=-4[H2(L_vA,B)+
H2(A,L_vB)], com H2(A,B;k)=k²<A,I_trB>-2C_kA·C_kB. Conferimos a identidade
contra a expansão GammaGamma ORIGINAL em todos400pares A,B,v, com k=a e0
e q arbitrário simbólico. São189casos não nulos. A covariância e linearidade
completam a identidade clássica sem exigir concordância só nos oito exemplos.
5. O extrator UV foi confrontado com um método independente: parâmetros de
Feynman no simplex, integração exata por fatoriais e momentos isotrópicos.
Todos126monômios q^α de grau≤5 foram verificados para cada uma das3famílias
de denominadores dos diagramas:378identidades simbólicas. Esse grau abrange
todos os numeradores presentes, e coeficientes externos saem da integração.

O primeiro programa passou168checks (inclui160componentes). A auditoria
independente passou1439checks e6controles negativos: omitir triângulo,
inserção métrica ou ghost, trocar sinal/fator e confundir os dois logaritmos.
CPU 8.890625s; wall das duas execuções
8.981434800080024s. Fontes, planos anteriores, resultados e
logs estão nos manifestos. Não é uma compilação Lean; A7 admite derivação+CAS.

Houve uma falha de implementação preservada: PolyElement recusou0**0 ao
montar monômios. A versão_v2 apenas pula fatores de expoente zero, que são
a unidade do anel. Nenhum coeficiente físico ou resultado-alvo mudou.

## O que ainda não foi demonstrado

Esta identidade é o componente h*cc do coeficiente LOGARÍTMICO principal da
ação1PI. Não calcula A(e^V) finita, o termo de curvatura da identidade, os
cutoffs, outros componentes de campo/antifield ou a hierarquia inteira de
contratermos. Portanto A7.b/Q2 ainda não está paga; o gate não mudou.
O Kimi revisará completude e hipóteses desta prova já executada, sem recriar
o cálculo. Seu parecer permanece DECLARADO até cotejo local.
