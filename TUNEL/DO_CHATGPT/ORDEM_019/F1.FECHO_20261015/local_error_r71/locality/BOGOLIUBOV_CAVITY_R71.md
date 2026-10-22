# R71 — referência de cavidade e transporte local exato de R66

**[DERIVED — construção analítica candidata, NOT_LEAN]** Subagente r69_locality_bridge, 18/10/2026. Camada ao lado: não altera os textos/pinos R69, R70 ou ENERGY_ERROR_R71. Fonte de continuidade: despacho da coordenação desta missão, revisão 501. A hipótese anteriormente examinada identificava o vácuo R66 ao vácuo global Ω. Aqui essa identificação é **substituída explicitamente** por um vácuo de osciladores locais Ω_b. O no-go anterior permanece válido para sua hipótese original.

## 1. Dois pares locais existem; um único par não os substitui

Escreva σ(u,v)=Im⟨u,v⟩ no H1 concreto. `OneParticleDualityR2.Jcandidate_image_equals_symplectic` identifica KWR′=J KWR; `WedgeNonisotropicR5.KWR_inter_JKWR_zero` então implica KWR∩KWR′={0}. Logo σ restrita a KWR é não degenerada: qualquer vetor não nulo tem algum parceiro com pareamento não nulo.

KWR é infinito-dimensional sobre ℝ. De fato `FubiniL2.canonicalPartialFourier` é uma equivalência H1≃L²(ℝ;TransverseFiber). A fibra não pode ser nula: isso tornaria esse L² nulo, contrariando `spectralOutput_nonzero`, consumido em `WedgeNonisotropicR5.KWR_not_isotropic`. Indicadores de intervalos disjuntos de comprimento um, multiplicados por um vetor unitário da fibra, dão infinitos vetores ortonormais. Se KWR fosse finito-dimensional real, KWR+iKWR seria finito-dimensional complexo, portanto fechado; sua densidade pela standardness daria H1 finito-dimensional, contradição. Esta é uma derivação em texto a partir dos tipos existentes, não uma nova declaração Lean de dimensão.

Escolha q₁,p₁∈KWR com σ(q₁,p₁)=1. Há w fora do span real desses dois. Defina

\[
w'=w-\sigma(w,p_1)q_1+\sigma(w,q_1)p_1.
\]

Então w'≠0 e σ(w',q₁)=σ(w',p₁)=0. Pela não degenerescência, existe z com σ(w',z)≠0. Retire de z suas componentes simpléticas na primeira dupla pela mesma fórmula; isso não muda σ(w',z). Normalize esse segundo par. Assim existem q_r,p_r, r=1,2, em KWR com

\[
\sigma(q_r,q_s)=\sigma(p_r,p_s)=0,\qquad
\sigma(q_r,p_s)=\delta_{rs}.
\tag{S}
\]

### Localização também numa região limitada existente por construção

`PhysicalCompactNetAssemblyR1.compactPhysicalNet_wedge_glue` identifica exatamente KWR com o fecho do span real de `compactSupportedGenerators` da cunha. Cada gerador é `circularSmear f` com f real, compacto e tsupport(f) dentro da cunha (`PhysicalCompactNetCovarianceR1:15–21`).

Aproxime os quatro vetores acima por quatro somas reais finitas desses geradores. A matriz 4×4 dos pareamentos σ varia continuamente; a matriz de (S) tem determinante 1. Aproximações suficientemente próximas conservam determinante não nulo. A união dos **finitos suportes compactos** envolvidos é um compacto contido na cunha aberta. Escolha uma vizinhança aberta limitada O desse compacto, com fecho ainda dentro da cunha. Os quatro aproximantes pertencem a K(O). Eliminação simplética real na sua matriz não degenerada produz dois pares exatamente canônicos em K(O). As combinações são reais, logo não saem do subespaço real localizado.

Isso constrói existência de dois pares numa região limitada da rede concreta, sem assumir quatro quadraturas a partir de uma só dupla. Não identifica O com a geometria, dimensões, modos ou materiais de uma cavidade patenteada específica. Nenhum tamanho ou energia foi otimizado.

## 2. Implementação Bogoliubov finita e referência nova

Seja E o span **complexo** dos quatro vetores locais e dos dois modos ortonormais f_i,f_o já escolhidos em R63/R66, dimensão finita d≤6. Incluí-los evita trocar silenciosamente os modos de partida; se fossem escolhidos agora dentro do span dos quatro vetores, bastaria d≤4. Seu espaço real subjacente tem forma simplética não degenerada Im⟨·,·⟩. O span real dos quatro vetores de (S) é um subespaço simplético de dimensão quatro. Complete essa base simplética para E e obtenha S∈Sp(E_ℝ), levando os pares (f_i,if_i),(f_o,if_o) aos pares locais. Estenda S por identidade em E⊥. A parte antilinear dessa transformação tem posto finito; não se supõe um squeezing arbitrário em infinitos modos.

**Construção explícita da implementação finita.** Identifique Γ_s(E) com L²(ℝ^d) pela base de ocupação/Hermite. Uma matriz simplética finita se decompõe por eliminação simplética em:

- mudanças lineares de coordenadas, implementadas por ψ(x)↦|det A|^(−1/2)ψ(A⁻¹x);
- cisalhamentos simpléticos, implementados por multiplicação e^{i xᵀBx/2}, B real simétrica;
- trocas coordenada/momento, implementadas por Fourier nos eixos necessários.

Todos são unitários por mudança de variável, módulo um ou Plancherel, respectivamente. A conjugação dos operadores q_j,p_j verifica cada bloco; seus produtos implementam S. Quando o bloco A é invertível, a fatoração em três blocos usa CA⁻¹ e A⁻¹B simétricas; quando singular, escolhem-se trocas Fourier de pivôs antes da eliminação. O sinal global da implementação não importa. Tensorizando com identidade em Γ_s(E⊥), obtém-se uma unitária U no Fock existente. Esta é uma construção analítica finita; a identificação Hermite e o algoritmo simplético não foram formalizados em Lean nesta camada.

Escolha a orientação de U de modo que os dois aniquiladores originais c₁,c₂ sejam transportados para

\[
b_r=Uc_rU^\dagger=\frac{\Phi(q_r)+i\Phi(p_r)}{\sqrt2},
\quad [b_r,b_s^\dagger]=\delta_{rs},\quad[b_r,b_s]=0.
\tag{B}
\]

O vácuo novo é Ω_b=UΩ; logo b_rΩ_b=0. Para uma completude gaussiana concreta nos d modos, escreva o vetor de aniquiladores transformados como b=Ua a+Va a†, usando **Ua,Va como matrizes**, sem confundir Ua com a unitária de Fock U. As CCR completas dão Ua Ua†−Va Va†=I e Ua Vaᵀ=Va Uaᵀ. Ua é invertível,

\[
Z=-Ua^{-1}Va=Z^T,\quad \|Z\|<1,\qquad
\Omega_b=\det(I-Z^\dagger Z)^{1/4}
\exp\!\left(\tfrac12\sum_{jk}Z_{jk}a_j^\dagger a_k^\dagger\right)\Omega.
\]

A relação aΩ_b=Za†Ω_b comprova bΩ_b=0. A normalização vem da diagonalização de Takagi de Z e da série de cada modo, Σ_n(2n)!|z|^{2n}/(2^{2n}(n!)²)=(1−|z|²)^(−1/2). A completude dos modos espectadores seleciona um Ω_b, não um vácuo único apenas pelas duas equações b₁ψ=b₂ψ=0.

O número médio global nessa referência é finito, Tr(Va†Va). Energia física finita exige também que os perfis de E tenham momentos do Hamiltoniano de uma partícula adequados; número finito não implica energia finita. Esses momentos e o custo de preparar Ω_b não foram medidos nem dispensados.

## 3. O subfator de osciladores é local e seus cortes são diferentes

Na representação (B), as quatro famílias Weyl dos pares locais geram

\[
\mathcal N_b=U\bigl(B(\Gamma_s(\mathbb C^2))\otimes I_{\rm spec}\bigr)U^\dagger
\subset\mathcal A(O).
\]

A identificação do fator usa a representação Schrödinger explícita dos dois pares: operadores que comutam com todas as multiplicações e translações são escalares nesse fator, e o bicomutante é B(L²(ℝ²)). O espectador é mantido; não se afirma que A(O) inteira seja um fator tipo I.

N_b=b₁†b₁+b₂†b₂ é auto-adjunto positivo, afiliado a N_b (álgebra), pelo transporte unitário do número dos dois osciladores. Os dois números fortemente comutam porque seus originais canônicos o fazem. Com OH local, use N_tot,b=N_b+n_e. As projeções

\[
P_m^b=1_{[0,m]}(N_{tot,b})\in\mathcal A(O)\bar\otimes M_2
\]

são agora **cortes locais**, não as projeções do número global utilizadas no erro R71. Têm posto finito no fator de osciladores+OH, mas podem ter posto infinito no espaço inteiro por causa do espectador. Convergem fortemente à identidade.

Ω_b não é separante para A(O): a projeção local que exclui o vácuo dos dois osciladores é não nula e anula Ω_b. Portanto preservar Ω_b puro não satisfaz a premissa “preservar o vácuo global separante” do teorema R70. O obstáculo não foi contornado; sua hipótese foi identificada e modificada.

## 4. Transporte exato do gerador completo, incluindo reservatório e bomba

Amplifique o semigrupo conservativo R66 pelo canal identidade do espectador. Essa amplificação age também em estados entrelaçados, não só produtos: os canais são normais e completamente positivos; a extensão é obtida inicialmente em matrizes de posto finito no espectador e por densidade em classe-traço, mantendo contração. Conjugue por U⊗I_OH:

\[
T_b(t)=\operatorname{Ad}_{U\otimes I}\circ
\bigl(T_{R66}(t)\otimes\operatorname{Id}_{spec}\bigr)
\circ\operatorname{Ad}_{U^\dagger\otimes I}.
\tag{T}
\]

Esse é um semigrupo CPTP fortemente contínuo. Seu gerador fechado é a conjugação do gerador R66 amplificado, com domínio transportado. No core transportado, a fórmula é **exatamente** R66 com a_r substituído por b_r, mesmos coeficientes, mesmo OH, mesmo J=b_o†σ₋+σ₊b_i e mesma bomba. Não se apagam os termos cruzados de J. A realização de colisões também é conjugada pelo mesmo U; os estados das ancillas, o canal OH coerente e a ordem dos limites permanecem os de R66.

A referência física mudou, embora a dinâmica abstrata seja unitariamente equivalente. A isometria do sistema R66 na rede passa a ser ψ↦U(ψ⊗Ω_spec), em vez da inclusão em modos que levava o vácuo diretamente a Ω. A bomba mantém o alcance de R66: sem bomba, Ω_b⊗g é estacionário; com bomba, não se presume isso.

### Causalidade da dinâmica transportada

O fator N_b⊗M₂ é local em O. Comprimir os coeficientes pelo P_m^b dá operadores limitados pertencentes à álgebra local. Fora do corte, tome os coeficientes comprimidos como zero no mesmo espaço; os semigrupos GKLS limitados correspondentes são CPTP, não canais de pós-seleção. Eles fixam A(O)′⊗I_OH pelo lema R69.

Há também uma prova direta que elimina qualquer dependência lógica de cortes: na fatorização transportada, T_b(t) age no fator dos dois osciladores+OH e é identidade no espectador. Seu dual fixa ponto a ponto o comutante de N_b⊗M₂. Como A(O)′⊗I_OH está contido nesse comutante, já resulta a causalidade abaixo. A aproximação por cortes que segue fornece ainda a ligação construtiva com os limites R66.

Na entrada de suporte P_{m₀}^b, a compatibilidade sem bomba e a cota Dyson com bomba de R66 passam por conjugação e amplificação. A cota independe da dimensão do espectador: prova-se primeiro em blocos finitos do espectador usando contrações CPTP e ||[h_drive,·]||≤2|Ω_pump|, depois estende-se por densidade. Os cortes completos aproximam em norma-traço todas as entradas porque P_m^b→I fortemente. Logo T_m^b(t)ρ→T_b(t)ρ em norma-traço e o lema de limite R69 implica

\[
T_b(t)^*(B\otimes I_{OH})=B\otimes I_{OH}
\quad\text{para }B\in\mathcal A(O)'.
\]

Assim há uma **realização matemática local exata** do gerador de osciladores R66 em uma referência de cavidade Ω_b construída, em alguma região limitada O, mantendo todos os termos. Não é a identificação antiga de modos globais positivos/vácuo global. A evolução aqui é intervenção local no parâmetro do aparelho; não se identifica com a evolução livre global nem com o grupo modular da cunha.

## 5. O que mudou e o que continua obrigatório

- O custo C de R71 mede a discrepância quando a entrada preparada é o **vácuo global Ω**. Para a entrada Ω_b e os b como osciladores do aparelho, a perda escura é restaurada. Não se troca a preparação depois de olhar dados: o contrato precisa nomear qual estado foi preparado e como foi reconhecido.
- A existência de O e de uma implementação finita não determina os modos de uma cavidade patenteada, o suporte material, a geometria do receptor ou a preparação gaussiana exigida. O estado e o custo energético fazem parte da realização, não desaparecem por equivalência unitária.
- A família pode ser transportada pela representação de Poincaré: transformam-se região, testes, U e Ω_b conjuntamente. Isso não torna Ω_b invariante nem deriva a transformação relativística do relógio de R66.
- Comparações R65/R69 continuam exigindo taxas, ganho, fase e filtros; λ=βγ_Λ não se separa por esta mudança de representação.
- Os argumentos acima são prova analítica candidata por composição e construção finita; não são uma nova compilação Lean nem instalação no programa. A realização material, a calibração e a identificação da cavidade continuam abertas. Os critérios integrais R4/R5 não são reduzidos à existência abstrata aqui demonstrada.

**Conclusão:** insistir em ancorar uma cavidade dissipativa no vácuo global separante impunha uma condição adicional. Nomear e construir a referência Ω_b permite transportar R66, incluindo seus cortes e reservatório, para um subfator local. Essa passagem agora tem conteúdo matemático; sua identificação com o aparelho real continua exigindo o contrato físico correspondente.
