[REAL — CAS exato; DERIVED — expansão radial; OPEN — soma Ward]
# A7.b — extrator do coeficiente logarítmico principal a um laço

Abertura sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

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
rc0; 45 checks e 6 negativos;
wall 0.3584657000028528s, CPU 0.3125s, Sympy 1.14.0.
Log one_loop_scale_run.log, plano anterior e hashes no manifesto.

O motor recebe um kernel escalar de momento. Ainda falta fornecer a soma real
de numeradores/índices métricos, formas de fibra, curvatura, ghosts, antifields
e pesos combinatórios, além dos termos finitos e contatos EOM/cutoff. O teste
do triângulo anterior confere uma magnitude comum, sem substituir essas entradas.
Portanto Q2 continua NÃO PAGA. Não é novo módulo do um.py: é CAS de bancada
para o A7.b autorizado. Nenhum item interagente/gate ou original foi alterado.
