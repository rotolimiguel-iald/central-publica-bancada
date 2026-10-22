[REAL — CAS de contribuição ghost; DERIVED — vértice principal; OPEN — soma Ward]
# A7.b — coeficientes tensoriais da bolha ghost do modelo

Abertura sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. Fonte BV069 sha256 `5cefd0a1be321e426627d9ad14a5cf1c788b98a4456d2190d1ba5932a7698124`.

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

rc0; 65 checks e 3 negativos,
wall 1.5691309999674559s, CPU 1.390625s, Sympy 1.14.0.
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
