# R71 — erro energético e custo observável da localização

**[DERIVED — demonstração analítica candidata, NOT_LEAN]** Subagente r69_locality_bridge, 18/10/2026. Handoff R5 e project da referência própria FECHO_MISSION_REFERENCE conferidos na revisão 501. Project recusou teto de 400000 caracteres; o teto de 1000000 recuperou a mesma referência, sem truncamento. Nenhuma campanha, provedor ou escrita em memória/produção.

## 1. Espaço comum e domínio

Reutilizam-se o Fock espacial existente, os aniquiladores de R66 e os campos locais de R70. Os alvos são a_r=a(e_r), com e_i,e_o ortonormais. Os candidatos são b_r=a(f_r)+a†(g_r), r=i,o. f_r,g_r vêm de testes reais u_r,v_r localizados pela fórmula R70; **g_r não é posto em zero**. Os pares locais não são presumidos modos independentes: as relações cruzadas exigem uma matriz simplética própria.

Aqui N=dΓ(I) é o **número total de fótons do Fock espacial inteiro**, sem contar OH. P_m=1_[0,m](N)⊗I_OH. Essa convenção difere do número N_R66=n_i+n_o+n_e: para estados do setor de dois modos, um corte N_R66≤m implica este corte fotônico ≤m, mas não reciprocamente. Não substituir as projeções em uma prova de invariância.

Sobre P_m, para qualquer h∈H1, as identidades CCR e a decomposição em setores dão

\[
\|a(h)P_m\|\le\sqrt m\|h\|,\qquad
\|a^\dagger(h)P_m\|\le\sqrt{m+1}\|h\|.
\]

Justificativa: a†(h)a(h)≤||h||²N em cada setor, e aa†=a†a+||h||²I. a e a† mudam o número em −1 e +1. Todas as composições abaixo são inicialmente no domínio de partículas finitas e suas restrições indicadas são operadores limitados.

Defina, para cada r,

\[
d_r(m)=\sqrt m\|f_r-e_r\|+\sqrt{m+1}\|g_r\|,
\quad \widetilde d_r(m)=\sqrt{m+1}\|f_r-e_r\|+\sqrt m\|g_r\|,
\]
\[
B_r(m)=\sqrt m\|f_r\|+\sqrt{m+1}\|g_r\|,
\quad \widetilde B_r(m)=\sqrt{m+1}\|f_r\|+\sqrt m\|g_r\|.
\]

Então ||(b_r−a_r)P_m||≤d_r(m), ||(b_r†−a_r†)P_m||≤d̃_r(m), ||b_rP_m||≤B_r(m) e ||b_r†P_m||≤B̃_r(m). São cotas, não igualdades universais.

## 2. Produtos: o setor intermediário não pode ser descartado

Se E_r=b_r−a_r,

\[
b_r^\dagger b_r-a_r^\dagger a_r=b_r^\dagger E_r+E_r^\dagger a_r.
\]

E_rP_m tem imagem em P_{m+1}; a_rP_m também está em P_{m+1} (cota conservadora). Portanto

\[
\|(b_r^\dagger b_r-a_r^\dagger a_r)P_m\|
\le q_r(m):=\widetilde B_r(m+1)d_r(m)
+\widetilde d_r(m+1)\sqrt m.
\tag{1}
\]

Usar apenas normas no mesmo P_m perderia a excursão para m+1. A imagem do produto completo pode atingir P_{m+2}. Não se faz compressão prematura P_m b P_m.

Para h_b obtido do h_R66 substituindo a_r por b_r e n_r por b_r†b_r, mantendo todos os coeficientes e o mesmo OH,

\[
\|(h_b-h_a)P_m\|\le h_m:=|\omega_c|[q_i(m)+q_o(m)]
+|g_{JC}|[\widetilde d_i(m)+d_i(m)].
\tag{2}
\]

O termo ω_OH n_e e a bomba Ω_pump σ_x são idênticos e cancelam. A estimativa não identifica frequência óptica, taxa dissipativa e escala β; cada uma conserva as unidades de R65/R66.

## 3. O único salto composto J e o gerador completo

Defina J_b=b_o†σ₋+σ₊b_i e J_a=a_o†σ₋+σ₊a_i. Com normas dos operadores de spin ≤1:

\[
j_m=\widetilde B_o(m)+B_i(m),\quad
\widetilde j_m=B_o(m)+\widetilde B_i(m),\quad
j_m^0=\sqrt{m+1}+\sqrt m,
\]
\[
d_m^J=\widetilde d_o(m)+d_i(m),\qquad
\widetilde d_m^J=d_o(m)+\widetilde d_i(m),
\]
\[
\|(J_b^\dagger J_b-J_a^\dagger J_a)P_m\|
\le q_J(m):=\widetilde j_{m+1}d_m^J
+\widetilde d_{m+1}^Jj_m^0.
\tag{3}
\]

A prova é a mesma fatoração de (1), usando que cada J muda o número fotônico no máximo em um. Não pressupõe comutação entre os modos locais. Mantém-se D[J_b] inteiro: seus termos cruzados não são separados em dois dissipadores.

Para X=P_mXP_m de classe-traço, os produtos da fórmula GKLS definem operadores de classe-traço. Para um salto L versus A, com diferenças d_m, normas l_m,a_m e cota q_m para (L†L−A†A)P_m,

\[
\|[\mathcal D[L]-\mathcal D[A]]X\|_1
\le[(l_m+a_m)d_m+q_m]\|X\|_1.
\tag{4}
\]

Prova: LXL†−AXA†=(L−A)XL†+AX(L†−A†), controlado pelas três restrições a P_m. Para o anticomutador, a diferença L†L−A†A é simétrica no core, e suas restrições esquerda/direita adjuntas têm a mesma norma q_m; o fator 1/2 cancela as duas parcelas. Isso vale para X complexo, não só estados positivos.

Se λ=βγ_Λ, β calculado pela regra da casa, resulta a cota de gerador:

\[
\|(\mathcal G_b-\mathcal G_a)X\|_1\le E_m\|X\|_1,
\]
\[
E_m=2h_m+
\sum_{r=i,o}\kappa_r[(B_r(m)+\sqrt m)d_r(m)+q_r(m)]
+\lambda[(j_m+j_m^0)d_m^J+q_J(m)].
\tag{5}
\]

Os dissipadores OH e Z cancelam por serem iguais. A cota é finita para m finito e depende de erros concretos de perfis de modo. Não foi escolhido valor para f_r,g_r, pois a geometria instrumental ainda não foi entregue.

Para qualquer observável limitado O, |Tr(O(G_b−G_a)X)|≤||O||E_m||X||₁. É erro de **tangente** ou de gerador restrito; não se anuncia automaticamente erro finito no tempo.

## 4. Vazamento e alcance dinâmico

O termo criador a†(g) leva P_m a P_{m+1}; b†b pode criar pares e chegar a P_{m+2}. Mesmo sem bomba OH, o novo gerador não herda a compatibilidade triangular dos cortes R66. A prova R66 de conservação de N por J e de invariância sem bomba dependia dos aniquiladores originais. Portanto não se reutiliza sua cota Dyson de corte com a mera troca a→b.

Uma estimativa Duhamel no tempo requer semigrupos conservativos previamente construídos, domínios comuns e controle integrável de ||(G_b−G_a)T_a(s)ρ||₁. Se a trajetória T_a(s) permanecer no corte e (5) se aplicar, a contração daria erro ≤tE_m; porém essa hipótese geralmente falha com bomba. Para trajetórias de suporte variável, é necessário controle de cauda/momentos; (5) sozinha não o fornece. Os candidatos limitados b_{r,ε} de R70 têm semigrupo, mas a passagem ε→0 continua própria. Nada nesta nota prova sua existência por decreto.

## 5. Custo no vácuo: fórmula exata e acessível em princípio

Seja χ₀=Ω_Fock⊗g e ρ₀=|χ₀⟩⟨χ₀|. Como b_rΩ=a†(g_r)Ω e os primeiros momentos de b_r no vácuo são zero,

\[
\boxed{C=(\kappa_i+\lambda)\|g_i\|^2+\kappa_o\|g_o\|^2.}
\tag{6}
\]

Derivação: L₁χ₀=√κ_i a†(g_i)Ω⊗g; L₂χ₀=√κ_o a†(g_o)Ω⊗g; L₅χ₀=√λ a†(g_i)Ω⊗e, pois a parcela b_o†σ₋ anula g. L₃ anula χ₀; L₄ é escalar nele e tem variância zero. As normas dos estados de um fóton são ||g_r||. Os coeficientes pertencem a canais separados; não há termo cruzado entre κ_i e λ. Dentro de J, a parcela de saída é zero nesta entrada particular; sua interferência reaparece em outras entradas.

Pela identidade de pureza de R70, para uma evolução diferenciável que realize essa tangente,

\[
\dot{\mathcal P}(0)=-2C,\qquad
\left.\frac d{dt}\mathrm{Tr}(\rho_0\rho_t)\right|_0=-C.
\tag{7}
\]

O Hamiltoniano, inclusive a bomba, não contribui às duas primeiras derivadas em (7). A probabilidade do **vácuo do campo**, sem condicionar OH, também tem derivada −C nesta entrada. O número fotônico total tem derivada C, porque os saltos em (6) criam exatamente um fóton e o comutador Hamiltoniano tem expectativa inicial zero para NΩ=0. Essa última igualdade é uma afirmação no core, não uma garantia de finitude de momento para todo t.

Para os operadores limitados b_{r,ε} de R70, o custo de pureza correspondente é C_ε=(κ_i+λ)||b_{i,ε}Ω||²+κ_o||b_{o,ε}Ω||²: seus primeiros momentos são zero pela característica real e par do vácuo Weyl. Mas b_{r,ε}Ω contém setores ímpares com mais de um fóton; **a derivada do número não é, em geral, C_ε**. Usam-se os pesos N nesses estados. A igualdade de número em (6) pertence ao b linear.

## 6. Cota inferior: o que ela permite e o que não permite

No alvo R66, C_a=0 para a mesma entrada χ₀, mesmo com bomba. A diferença Δ=(G_b−G_a)ρ₀ é auto-adjunta e tem traço zero, e Tr(ρ₀Δ)=−C. A decomposição de Jordan de um operador de traço zero dá

\[
\boxed{\|\Delta\|_1\ge2C.}
\tag{8}
\]

É uma cota inferior concreta da discrepância de **geradores na entrada**. Se ambas as evoluções existem e são diferenciáveis em norma-traço nessa entrada, então ||T_b(t)ρ₀−T_a(t)ρ₀||₁≥2Ct+o(t). Não se deduz um intervalo de tempos útil sem uma cota do resto. A sensibilidade de um instrumento real ainda depende de eficiência, ruído, preparação e relógio.

R70 prova g_r≠0 para cada par local não degenerado numa cunha separante. Logo C>0 se uma taxa correspondente for positiva. Entretanto **g≠0 não fornece um limite inferior numérico uniforme para ||g||**. A possibilidade de uma família de perfis com custo arbitrariamente pequeno ou de um piso positivo sob restrições de suporte/banda/energia requer uma estimativa geométrica adicional. Nenhum piso universal foi calculado aqui.

Assim (6) sugere um canal: preparação de referência próxima do vácuo + contagem de excitações ou teste de sobrevivência, com verificação da mesma leitura de modo e do mesmo relógio. Não é ainda um experimento do aparelho e não discrimina β sozinho: λ=βγ_Λ continua um produto, C inclui g_i/g_o e κ_i/κ_o, além de fundos instrumentais. Separar esses parâmetros exige os contratos R65/R69. Nenhuma significância ou confirmação física é reivindicada.

## Resultado

Há agora uma cota superior explícita (5), uma diferença inferior (8) e um custo observável (6), todos para objetos no mesmo Fock e com excursões de setor contabilizadas. A questão pendente foi reduzida a perfis, taxas, domínios e geometria reais; ela não foi apagada. R4/R5 mantêm seus critérios integrais. Esta demonstração aguarda revisão distinta; os controles sintéticos da coordenação verificam fórmulas, não realizam o instrumento.
