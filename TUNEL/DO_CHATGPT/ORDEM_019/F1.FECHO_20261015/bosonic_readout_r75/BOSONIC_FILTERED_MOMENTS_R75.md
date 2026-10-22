# R75 — momentos filtrados no limite bosônico, com erro explícito de corte

**[DERIVED — demonstração analítica candidata, NOT_LEAN]** r69_locality_bridge, 18/10/2026. Reutiliza integralmente o semigrupo bosônico R66 e o instrumento finito R64, transportado em R74. Project/preflight R5 na revisão 517, lease `b8a9d760-c16f-4a8b-8210-07415d2c62ee`, owner codex-gerente-tgl: ready. Não há novo gerador, hipótese de banho físico, construção de unitária HP ilimitada, teste ou dado observado nesta nota.

## 1. Objetos e domínio exatos

H=Γ_s(C²)⊗C²_OH e N=n_i+n_o+n_e são os de R66, não os cortes independentes 0/1. P_m=1_[0,m](N). Tome uma densidade ρ₀=P_{m₀}ρ₀P_{m₀}, m₀ inteiro finito, Trρ₀=1. Em cada corte m≥m₀ usa-se o **mesmo** instrumento R64 para o gerador G_m completo: todos os cinco dissipadores, o jump único J, JC e bomba. A existência/compatibilidade de T₀ e a perturbação pela bomba B(X)=−i[h_d,X], ||B||≤b=2|Ω|, já são resultados R66 e não são refeitos.

Em [0,T], para as duas portas independentes j∈{i,o}, fixe c_j(t)=g_j conjugate(f_j(t))exp(−iθ_j(t)), com ganhos reais conhecidos, f_j∈L²[0,T]. Como T é finito, c_j também pertence a L¹. Defina a inserção ponderada

\[
\mathcal M_j(t)X=\sqrt{\kappa_j/2}\,[c_j(t)a_jX+\overline{c_j(t)}Xa_j^\dagger].
\tag{1}
\]

As versões comprimidas usam a_{j,m}=P_ma_jP_m. A normalização de ruído é a R64: contato diagonal |c_j(t)|²/2, cruzado zero entre portas independentes. Quatro aquisições XX, PP, XP, PX continuam separadas. Aqui não se medem simultaneamente quadraturas incompatíveis do mesmo banho.

## 2. Suporte bilateral e norma da inserção

Se X=P_rXP_r, então a_jX e Xa_j† continuam suportados bilateralmente em P_r. A primeira parcela baixa a excitação do ket; a segunda baixa a do bra. Não se afirma que ambas pertençam a P_{r−1}T₁P_{r−1}: apenas um lado precisa ter baixado. Como ||a_jP_r||=||P_ra_j†||≤√r,

\[
\|\mathcal M_j(t)X\|_1
 \le\sqrt{2\kappa_jr}\,|c_j(t)|\,\|X\|_1.
\tag{2}
\]

Isso usa o produto à direita **Xa_j†**, não a_j†X. As mesmas estimativas valem nos cortes, mesmo para X não positivo. T₀ é contração na norma de traço para matrizes complexas e preserva P_rT₁P_r. B aumenta o limite de suporte no máximo de r para r+1, porque o drive apenas troca a ocupação OH em um dos lados. Essas são as únicas propriedades usadas no argumento.

## 3. Série com uma ou duas inserções — contagem de tempos

Considere k=1 ou 2 inserções, em tempos ordenados 0<t₁<…<t_k<T, com etiquetas j₁,…,j_k. Entre elas e antes/depois delas, expanda a evolução completa pela Dyson–Phillips de R66. Um termo tem n₀,…,n_k inserções B nos k+1 intervalos, com n=Σ_l n_l. Todos os estados auxiliares permanecem em P_{m₀+n}, porque as inserções M não aumentam suporte.

O bound de sua norma, somado sobre a distribuição de n entre os intervalos, é

\[
(m_0+n)^{k/2}\prod_{a=1}^k\sqrt{2\kappa_{j_a}}|c_{j_a}(t_a)|
\frac{(bT)^n}{n!}.
\tag{3}
\]

**Combinatória explícita:** sejam Δ_l os comprimentos dos k+1 intervalos. A integração dos n_l tempos ordenados naquele intervalo dá Δ_l^{n_l}/n_l!. Pelo multinômio,

\[
\sum_{n_0+\cdots+n_k=n}\prod_{l=0}^k\frac{\Delta_l^{n_l}}{n_l!}
=\frac{(\sum_l\Delta_l)^n}{n!}=\frac{T^n}{n!}.
\tag{4}
\]

Portanto não aparece um fator adicional (k+1)^n ou uma escolha extra dos tempos de medida. As medidas já têm seus tempos fixados; a soma das posições da bomba entre elas é exatamente (4). O bound usa (m₀+n)^{k/2} em todos os fatores M; é conservador e não exige que os n aumentos de suporte aconteçam de fato.

A série de (3) é absolutamente convergente para T finito. Se m≥m₀+n, cada termo no corte m coincide com o termo sem corte, incluindo todos os operadores auxiliares fora do cone positivo, pela compatibilidade R66 e por (1). Logo as duas séries coincidem até n=m−m₀. Acima dessa ordem, cada cauda é majorada por (3); a diferença traz fator **2**, uma cauda de cada expressão.

## 4. Limites funcionais e cotas prontas

Escreva

\[
q=2|\Omega|T,\quad d=m-m_0\ge0,\quad
A_j=\sqrt{2\kappa_j}\int_0^T|c_j(t)|dt,
\]
\[
E_d(q)=\sum_{n>d}\frac{q^n}{n!},\qquad
T_k(d)=\sum_{n>d}(m_0+n)^{k/2}\frac{q^n}{n!}\quad(k=1,2).
\tag{5}
\]

As somas começam em n=d+1. Quando q=0, são zero; o termo n=0 das somas completas usa q⁰=1, inclusive em q=0. Não há potência 0⁰ nos pesos k/2 porque k≥1.

### Primeiro momento

Defina μ_j pela série absolutamente convergente de uma inserção integrada em t. É o limite dos primeiros momentos μ_j^{(m)} dos instrumentos finitos. Da equação (3),

\[
\boxed{|\mu_j-\mu_j^{(m)}|\le\varepsilon_j(m)=2A_jT_1(d).}
\tag{6}
\]

A mesma cota vale para |μ_j^{(M)}−μ_j^{(m)}| com qualquer M>m≥m₀. Não se usa aqui somente convergência em norma-traço de estados para passar um observável ilimitado: a passagem é controlada diretamente pela série ponderada.

### Segundo momento bruto

O segundo momento r_{jk}=E[Q_jQ_k] tem duas contribuições regulares, nos triângulos t>s e s>t, com as etiquetas trocadas, e o contato diagonal. As integrais dos majorantes regulares satisfazem

\[
\int_{t>s}|c_j(t)c_k(s)|\,dt\,ds+
\int_{s>t}|c_j(t)c_k(s)|\,dt\,ds
=\|c_j\|_1\|c_k\|_1.
\tag{7}
\]

Para j=k, os dois termos são iguais, e sua soma ainda é ||c_j||₁². Portanto não há outro fator 2 além das duas caudas do §3. Como Trρ^{(m)}(t)=1 em todo corte, o contato é exatamente
`δ_jk (1/2)∫|c_j(t)|²dt`, independente de m. Seu **erro de corte é zero**. Assim

\[
\boxed{|r_{jk}-r_{jk}^{(m)}|\le\varepsilon_{jk}(m)=2A_jA_kT_2(d).}
\tag{8}
\]

Novamente a mesma cota compara quaisquer dois cortes M>m. O limite r é definido pelas duas séries e pelo contato, e coincide com o limite dos instrumentos finitos. Omitir o ruído alteraria o segundo momento, embora não a cauda de corte regular.

### Fórmulas para computar as caudas sem nova hipótese

Com E_{−1}(q)=e^q,

\[
T_2(d)=m_0E_d(q)+qE_{d-1}(q),\qquad
T_1(d)\le\sqrt{E_d(q)T_2(d)}.
\tag{9}
\]

A primeira igualdade separa m₀+n e desloca n q^n/n! para q q^{n−1}/(n−1)!. A segunda é Cauchy–Schwarz das sequências √(q^n/n!) e √((m₀+n)q^n/n!). Pode-se usar a cota da direita diretamente nos testes; não apresentá-la como igualdade. Subtrações de números quase iguais para calcular E_d exigem cuidado numérico; a fórmula é analítica, não prescribe uma avaliação por cancelamento.

Para somas completas S₁=Σ_{n≥0}√(m₀+n)q^n/n! e S₂=(m₀+q)e^q,

\[
S_1\le e^q\sqrt{m_0+q},\qquad
|\mu_j|,|\mu_j^{(m)}|\le A_jS_1.
\tag{10}
\]

A cota de S₁ é Jensen para os pesos de Poisson normalizados; também resulta de Cauchy–Schwarz. Estes bounds podem ser largos: PASS de uma desigualdade larga verifica o contrato, não demonstra erro próximo do limite superior.

## 5. Covariâncias e decoder, com propagação do erro

Para V_{jk}=r_{jk}−μ_jμ_k, a decomposição do produto de médias e (10) dão

\[
\boxed{|V_{jk}-V_{jk}^{(m)}|
\le2A_jA_kT_2(d)+4A_jA_kS_1T_1(d).}
\tag{11}
\]

Alternativamente, usando as médias do corte medido, vale
`ε_jk+|μ_j^(m)| ε_k+|μ_k^(m)| ε_j+ε_j ε_k`.
Estas estimativas também comparam dois cortes. Cada matriz de covariância finita das correntes compatíveis é positiva semidefinida; o limite entrada a entrada conserva essa propriedade. Isso não prova convergência em norma-traço de um estado de campo de saída, nem fornece uma taxa em tal norma.

Reaproveite literalmente o decoder R64, aplicado aos segundos momentos cruzados de quatro aquisições:

\[
C=\tfrac12[r_{XX}-r_{PP}+i(r_{XP}+r_{PX})],\quad
B=\tfrac12[r_{XX}+r_{PP}+i(r_{XP}-r_{PX})].
\tag{12}
\]

Seu erro em módulo é no máximo metade da soma dos quatro erros cruzados. Se todos os settings têm os mesmos módulos de filtros/ganhos, cada um tem (8), logo
`|ΔC|,|ΔB|≤4 A_iA_o T₂(d)`.
Para o decoder centrado, substitua cada erro por (11). Se o consumidor remove ganhos conhecidos dividindo os segundos momentos por g_i g_o≠0, divida essas cotas por |g_i g_o|. Não se divide a cauda sem também dividir a estatística.

A leitura/reconstrução **linear** de R57 pode consumir uma amplitude de leitura identificada: multiplicar por exp(±iθ_M) conserva o erro absoluto e multiplicar por S(θ_M) transfere-o com norma ||S(θ_M)||=1. Isso não identifica automaticamente C, B ou uma corrente filtrada com a polarização OH z ou o fator documental G_OH. Normalização de uma fase ou razão pelo módulo da amplitude é não linear e exige cota inferior própria para esse módulo; as estimativas lineares não a autorizam perto de zero.

## 6. Fases R74 e o alcance do resultado

R(t)=exp(iΣχ_j(t)n_j) comuta com N e P_r. A conjugação não altera as normas de M, B, nem |c_j|. O T₀ transportado preserva os mesmos suportes; a conexão −Σ dot(χ)n permanece no Hamiltoniano conservador de N. Logo a prova dos §§2–5 e todas as cotas são invariantes sob o transporte conjunto R74, com a fase dentro do filtro. Isso permite comparar o mesmo instrumento nos quadros lab/girante sem criar um cutoff diferente.

**O que fica obtido:** primeiros e segundos momentos, covariâncias e decoder do instrumento bosônico como limites únicos das expressões/instrumentos finitos, com erro controlado para entrada de suporte finito e T finito. A positividade quadrática é herdada. Trata-se de um funcional de momentos, não de uma construção já feita da distribuição completa de trajetórias, da unitária HP ilimitada, do campo de saída global ou de uma identificação da cavidade patenteada.

Não se estende o resultado a estados iniciais arbitrários apenas por densidade em norma-traço: para observáveis ilimitados, isso exige controle de caudas/momentos inicial adicional. Não se afirma uniformidade quando T→∞. As hipóteses instrumentais R64, a realização R66, a calibração física, a escala γ_Λ e os critérios integrais R4/R5 continuam os mesmos. Nenhuma taxa, ganho ou β foi ajustado por esta derivação.
