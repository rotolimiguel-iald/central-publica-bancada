# R72 — dos perfis reconhecidos do dispositivo aos osciladores locais

**[DERIVED — candidato analítico, NOT_LEAN]** r69_locality_bridge, 18/10/2026. Reuso de R71; missão projetada e preflight R5 `ready` na revisão 506, lease `ec98434f-b7cf-4bfb-b311-a6810dda408b`, dono codex-gerente-tgl. Não há nova campanha, leitura de dado observado, provedor, implantação ou mudança de critério. As fontes/linhas e os hashes são fornecidos pelo script vizinho. A existência abstrata de dois pares locais de R71 não é refeita.

## 1. A entrada é uma resposta eletromagnética, não apenas um desenho de modo

O objeto necessário são quatro funcionais reais de acoplamento/leitura, com suas unidades, fase, posição, janela temporal e resposta instrumental. No modelo livre, representamo-los por quatro tensores reais `f_α∈C_c^∞(O;R^{4×4})`, α=1,…,4. Como o acoplamento é com a intensidade de campo antissimétrica, só a parte antissimétrica contribui. Podem ser dados diretamente como kernels de integração do sensor/atuador; se vierem de perfis de cavidade, precisam resultar de um mapa de resposta explicitado, que inclua materiais e portas.

Um perfil clássico F_{μν}(x) e um kernel de leitura f^{μν}(x) têm papéis diferentes. Multiplicar um perfil por uma janela suave compacta produz um **candidato matemático a teste**; não prova que o aparelho mede a operação ∫f^{μν} F_{μν}. Essa identidade deve ser aferida pela resposta a excitações de referência, com ganho e fase guardados. Não escolher os kernels depois para obter a Gram ou o β desejados.

Para um perfil harmônico complexo E_r(x), duas leituras reais podem usar envelopes fixados w_r(t,x) e fases cos(ω_rt+φ_r), sin(ω_rt+φ_r), com a estrutura tensorial E/B do acoplamento. A frequência, o tensor, a janela, o tempo próprio e o sinal da quadratura são dados. A defasagem de π/2 no laboratório **não implica automaticamente** h_2=ih_1 na rede; a restrição à casca e o suporte temporal entram no cálculo. Isso é coerente com K(O) real e evita o erro de transformar uma região local num subespaço complexo.

### Mapa livre já disponível, incluindo normalização

Use a mesma convenção do acervo:

\[
\widehat f_{\rm phys}(p)=({\cal F}^{-1}f)((2\pi)^{-1}\,\mathrm{metricFlip}(p)),
\]
\[
c_j(y)=\frac12\sum_{\mu\nu}\mathrm{cartesianStrength}_{j\mu\nu}(y)
                      \widehat f_{\rm phys}(\mathrm{shellEmbedding}(y))_{\mu\nu}.
\tag{1}
\]

`physicalSmearCLM` é exatamente esse coeficiente em H1; `circularSmear` aplica a inversa da base circular unitária. O adaptador de campo físico normalizado já existe: `normalizedCircularSmearCLM = A_F circularSmearCLM`, com A_F positivo, `A_F²=unitaryFourierStressScale`. Portanto fixamos h_α=normalizedCircularSmearCLM(f_α), sem substituir A_F por um ganho ajustado. Um ganho do detector é outro objeto, com unidade e calibração próprias.

Para f_α real e suporte compacto em O, h_α pertence ao K(O) existente: a normalização A_F é real e positiva. As famílias `W(th_α)` e as quadraturas Φ(h_α) fechadas são locais na álgebra `FieldWeyl.R(K(O))`. A localização vem do suporte e do mapa (1), **não do valor da matriz de Gram**. Vetores em outra região podem ter a mesma Gram.

## 2. Dados que determinam a construção, sem perder os canais originais

Calcule, com a medida `orbitalMeasure 0` e a base circular da fonte,

\[
G_{\alpha\beta}=\langle h_\alpha,h_\beta\rangle,
\quad S=\operatorname{Re}G,
\quad \Xi=\operatorname{Im}G,
\quad [\Phi(h_\alpha),\Phi(h_\beta)]=i\Xi_{\alpha\beta}I.
\tag{2}
\]

Os dados mínimos são os próprios quatro kernels e o mapa/normalização, além de G. A Gram verifica CCR, não recupera os kernels, a região, a energia nem a identidade do dispositivo. `det Xi≠0` é o critério de existência de **duas** duplas nos quatro canais fornecidos. Se rank Xi<4, o conjunto do aparelho não fornece dois modos canônicos por essa construção, ainda que R71 prove existência em alguma outra escolha de testes.

Fixe uma eliminação simplética **real**, com ordem de pivôs registrada, e obtenha C real tal que

\[
C^T\Xi C=J_4=\operatorname{diag}\!\left(
\begin{pmatrix}0&1\\-1&0\end{pmatrix},
\begin{pmatrix}0&1\\-1&0\end{pmatrix}\right).
\tag{3}
\]

Defina (q₁,p₁,q₂,p₂)_j=Σ_α h_α C_{αj}. Estas são combinações reais dos **mesmos** testes, permanecem em K(O), e dão b_r=(Φ(q_r)+iΦ(p_r))/√2 com CCR exatas no modelo. O relatório deve guardar C e C⁻¹: se a eliminação mistura a porta de entrada com a de saída, misturou efetivamente os observáveis. Não basta chamar os modos resultantes novamente de “entrada” e “saída”.

A leitura dos canais é transportada por X_j=Σ_α C_{αj} Φ(h_α). Hamiltoniano, jump J, filtros e decoder de R63–R66 devem usar essa mesma mudança. Se se exige preservar cada porta, restrinja C previamente à forma de blocos correspondente; nesse caso os cruzamentos entre portas podem impedir (3). Não se anulam correlações com uma mudança proibida pelo aparelho.

### Reconhecimento com incerteza

Se os vetores calibrados têm erros ||δh_α||≤ε_α, então

\[
|\delta G_{\alpha\beta}|\le
\|h_\alpha\|\varepsilon_\beta+
\|h_\beta\|\varepsilon_\alpha+
\varepsilon_\alpha\varepsilon_\beta.
\tag{4}
\]

Uma cota espectral ||δXi||₂<s_min(Xi_estimado) certifica não degenerescência da Xi verdadeira. O erro numérico de integração deve entrar nessa cota. Com C fixada no estimado, o defeito CCR verdadeiro é CᵀδXi C, de norma ≤||C||₂²||δXi||₂. É um erro a declarar; não vira igualdade exata por arredondamento. Uma matriz mal condicionada amplifica erro e ganho: os limiares operacionais devem ser fixados antes do teste. Nenhum limiar novo foi escolhido nesta nota.

## 3. Cavidade aberta, material e reservatório

Um modo ressonante com frequência complexa é um polo de resposta. Sem condição adicional não é vetor normalizado de H1, nem possui a norma positiva da rede livre. O Hamiltoniano de uma partícula da rede livre é auto-adjunto, com frequências reais: inserir nele diretamente uma frequência complexa não preserva essa estrutura. A normalização por Q, volume ou amplitude máxima do modo não substitui ∫||h(y)||²dμ(y)=1.

O vínculo operacional possível usa **pacotes de saída/entrada livres** da região exterior: resolver ou aferir a resposta material às excitações de referência, obter os campos radiativos, convertê-los para amplitudes na casca positiva e aplicar a norma de H1. Envelopes temporais, banda e polarizações são fixados como parte do pacote. Para um pacote h≠0 com norma finita, e=h/||h|| é um vetor; a potência e o ganho retirados nessa normalização continuam registrados. Se dois pacotes não são ortogonais, sua Gram complexa registra isso; ortogonalização deve ser transportada à leitura e à dinâmica, como em (3).

Uma parametrização admissível é uma resposta linear causal R_D que leva as excitações conhecidas às quatro funções de acoplamento/leitura, seguida de j=f↦h pela (1). O diagrama é `excitação → R_D → f_α → j → h_α → (G,Xi,C) → b_r`; R_D inclui interfaces, dispersão, perdas, portas, fase e calibração. A resposta efetivamente obtida deve ser comparada à prevista **antes** de se aceitar o dispositivo como realizador de R66. Essa construção não identifica o campo dentro de um dielétrico dissipativo com o campo livre do kernel.

O banho é necessário também algebricamente. Se um modelo de perda escrevesse apenas a(t)=exp[−(κ/2+iω)t]a(0), teria [a(t),a(t)†]=exp(−κt), quebrando CCR para κ>0. Com um canal branco independente, a solução

\[
a(t)=e^{-(\kappa/2+i\omega)t}a(0)
 +\sqrt\kappa\int_0^t e^{-(\kappa/2+i\omega)(t-s)}b_{in}(s)ds
\]

dá comutador exp(−κt)+κ∫₀ᵗexp[−κ(t−s)]ds=1. Esta é a especialização Markov escolhida, não uma dedução de qualquer dielétrico. Em frequência, para uma resposta passiva `a_out=S a_in+B c_in`, a preservação CCR exige SS†+BB†=I. Se S é contração, B=(I−SS†)^{1/2} dá uma extensão algébrica em cada frequência; causalidade, regularidade e estado do ruído ainda precisam ser fornecidos, não seguem dessa raiz ponto a ponto.

R66 já fornece um banho de colisões construído e o canal coerente OH; a resposta material deve demonstrar sua equivalência no regime adotado, com erros declarados. Não substituir o jump único J por perdas independentes: seus termos cruzados permanecem parte do alvo. Uma caracterização clássica de S ou de uma largura espectral sozinha não determina a textura de ruído, o estado do banho ou γ_Λ.

## 4. Finitude da energia de Ω_b: a peça faltante é fechável por reuso

Aqui há avanço positivo além do contrato de medição. `RegularMaxwellEnergyR2.physicalSmear_strongRegular` já prova todos os momentos quadráticos de energia do smear Schwartz; `RegularCoefficientBoundaryR3.circularSmear_energySquare` transporta-os à base circular. A constante A_F não altera a finitude. Para cada h_α e todo inteiro m≥0,

\[
I_m(h_\alpha)=\int |p|^m\|h_\alpha(p)\|^2d\mu(p)<\infty.
\tag{5}
\]

A estimativa explícita reutilizada é

\[
I_m(h_\alpha)\le128 A_F^2\int |p|^{m+1}
\|\widehat f_{\alpha,phys}(|p|,p)\|^2d^3p.
\tag{6}
\]

A medida orbital da fonte tem densidade 1/|p| em relação à medida de momentos; não se insere um 1/2 ausente. O bound da força Maxwell é `||globalCoefficient||²≤128|p|²||f(shell)||²`. A expressão à direita é integrável por `energy_moment_square_restriction_integrable`; o Fourier físico leva Schwartz a Schwartz. (6) usa a norma tensorial específica das fontes, não uma constante universal para qualquer convenção SI.

Combinações reais ou complexas finitas preservam (5), pela desigualdade ||Σc_jh_j||²≤(Σ|c_j|²)(Σ||h_j||²). Portanto o espaço complexo E_loc gerado pelos quatro vetores está no domínio de todas as potências de h^{1/2}, h=|p|. A base ortonormal e o complemento simplético finito da construção R71 podem ser feitos dentro de E_loc; não introduzem caudas energéticas externas.

Seja e₁,…,e_d uma base ortonormal de E_loc e H_E a matriz de forma positiva H_{jk}=⟨h^{1/2}e_j,h^{1/2}e_k⟩. Ela tem entradas finitas; não se exige que E_loc seja invariante por h. Para a implementação gaussiana finita b=Aa+Va† de R71, com vácuo Ω_b e ocupação total ν=Tr(V†V)<∞,

\[
\langle\Omega_b,d\Gamma(h)\Omega_b\rangle
 =\sum_{jk} H_{jk}\langle\Omega_b,a_j^\dagger a_k\Omega_b\rangle
 \le \|H_E\|\,\nu <\infty.
\tag{7}
\]

Prova: a matriz de densidade de uma partícula de Ω_b é positiva, tem suporte em E_loc e traço ν. A energia é o pareamento dessa matriz com a forma H_E. Primeiro vale para h truncado espectralmente; convergência monótona das formas positivas permite o limite e dá (7). Logo Ω_b pertence ao domínio de forma de dΓ(h); não se reivindica aqui seu domínio de operador nem energia mínima.

### Preservar os modos de partida, sem supor energia deles

R71 incluiu os modos antigos f_i,f_o no espaço finito E. Sua mera ortonormalidade não garantia energia finita. Para garantir (7) sem alterar b₁,b₂ nem o gerador abstrato, escolha primeiro um unitário **passivo** V₀ de H1 que leve f_i,f_o a dois modos ortonormais de E_loc. Uma extensão unitária pode ser feita no span finito das duas duplas e ser identidade no ortogonal. Depois aplique o implementador U_loc cuja parte ativa está toda em E_loc. Defina U_total=U_loc Γ(V₀). Como Γ(V₀)Ω=Ω, o vácuo final é U_locΩ e satisfaz (7), mesmo se os antigos modos não tinham momento de energia finito. Ainda assim U_total a(f_r)U_total†=b_r e R66 é transportado inteiro. A finitude energética de **outras entradas físicas** antigas permanece obrigação própria.

Assim a finitude energética do vácuo construído deixa de exigir um perfil arbitrário adicional: decorre dos testes compactos suaves já usados para construir os pares. O valor da energia requer os perfis efetivos, H_E e V; a preparação e seu custo dissipativo podem ser maiores e não foram medidos. Conversão para joules exige a convenção do momento: se p é número de onda, h_físico=ℏc|p|; não substituir esse fator por uma taxa Γ do aparelho.

## 5. Saída desta ponte e resíduo físico

Uma entrega operacional completa deve portar `O`, os quatro kernels reais (bytes/mesh/unidades/interpolação), a resposta R_D e seu intervalo de validade, a convenção Fourier/A_F, a Gram complexa com erro, Xi, C e limites de condicionamento, a transformação dos canais originais, a implementação gaussiana/complemento escolhido e H_E. O reservatório e sua preparação são parte do mesmo contrato. Essa lista é a entrada necessária ao mapa explicitamente construído acima, não uma nova teoria.

**Fechado nesta componente [DERIVED]:** a aplicação dos dados de quatro respostas compactas suaves reconhecidas aos pares canônicos, os erros de Gram/CCR e uma condição já satisfeita por esses testes que garante energia finita para Ω_b. **Ainda [OPEN]:** obter/reconhecer esses quatro kernels no dispositivo concreto, demonstrar sua resposta material/banho e calibrar o relógio e γ_Λ. Os números, suportes e perfis não foram inventados. R4/R5 integrais permanecem com os critérios originais.
