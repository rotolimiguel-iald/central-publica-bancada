# R70 — interação local, vácuo separante e o gerador R66

**[DERIVED — demonstrações analíticas candidatas, NOT_LEAN]** Subagente `r69_locality_bridge`, 18/10/2026. Trabalho sob handoff R5, revisão 496, referência própria `work/memoria_missao_20261016/FECHO_MISSION_REFERENCE.json`, sem alterar estado da missão. Os pinos e linhas das fontes efetivamente lidas estão em `SOURCE_PINS_LOCALITY_R70.json`. Nenhuma execução numérica, provedor ou alteração de produção.

## 1. Reaproveitamento preciso

R69 já compôs a rede Maxwell compacta K(O), a álgebra **FieldWeyl.R(K(O))** e a condição suficiente para canais locais fixarem o comutante. R66 já construiu o semigrupo bosônico de dois modos e OH e sua realização por colisões. Aqui se pergunta se **o mesmo gerador** pode ser instalado numa álgebra estritamente local, não se constrói novamente rede ou Fock.

Fontes centrais:

- `WedgeCyclicR3.lean:47–73`: se A pertence à álgebra da cunha padrão e AΩ=0, então A=0; é separação do **vácuo Fock para a álgebra**, mais forte para este uso que a mera separação real K∩iK=0.
- `PhysicalCompactNetAssemblyR1.lean:18–38`: a rede física compacta tem localidade e a cunha direita é exatamente KWR.
- `FieldWeylR3.lean:30–77`: W(f)=D(if), W(f)†=W(−f), CCR, continuidade e inclusão W(f)∈R(K) para f∈K.
- `CanonicalSegalEssentialR6.lean:16–46`: W(tf) é o grupo de gerador √2 Φ(f), com Φ(f) o fecho auto-adjunto do Segal existente.
- `WedgeNonisotropicR5.lean:56–66`: existem u,v∈KWR com Im⟨u,v⟩≠0. A construção local abaixo não é vazia na cunha; não se afirma daí que todo pequeno O tenha a mesma testemunha.
- R66, `BOSONIC_CONTINUUM_R66.txt:7–19`: os saltos, domínio de partículas finitas e N total concretos.
- R66, `construction/CONSTRUCTION_R66.md`, §§1–4: um único canal para J=A+B, colisões, paridade e entrada coerente no canal OH.

Fixe M=A(O)⊂A(W_R), por exemplo O⊂W_R. O vácuo Ω é separante para M por inclusão. Esse enunciado tem uma instância já construída; não se assume separação de um estado arbitrário, nem separação de Ω⊗g para M⊗M₂.

## 2. Teorema: um canal local que preserva o vácuo puro é trivial

Considere Kraus limitados M_j∈M, finitos ou enumeráveis, com Σ M_j†M_j=I em sentido forte. Seja T(ρ)=Σ M_jρM_j†, soma normal em classe-traço. Se

\[
T(|\Omega\rangle\langle\Omega|)=|\Omega\rangle\langle\Omega|,
\qquad \|\Omega\|=1,
\]

então **T é o canal identidade em todos os estados normais**.

Prova: para todo η⊥Ω,
0=⟨η,T(|Ω⟩⟨Ω|)η⟩=Σ_j|⟨η,M_jΩ⟩|². Cada termo é não negativo, logo M_jΩ=c_jΩ. Como M_j−c_jI∈M, a separação dá M_j=c_jI. A normalização implica Σ|c_j|²=1; portanto T(ρ)=ρ. A prova também mostra que não basta inserir um Kraus de nome “local”: sua pertença à álgebra é a premissa que carrega peso.

**Com auxiliar OH.** Suponha Kraus limitados C_j∈M⊗M₂ e estado inicial Ω⊗g, g fixo. Escreva C_j por blocos C_j^{ab}∈M na base (g,e). Se o canal conjunto preserva o projetor puro |Ω,g⟩⟨Ω,g|, a mesma positividade dá C_j(Ω⊗g)=c_jΩ⊗g. Separação no fator campo implica C_j^{gg}=c_jI e C_j^{eg}=0. Consequentemente, para **todo** ψ,

\[
C_j(\psi\otimes g)=c_j\psi\otimes g,
\quad T(\rho\otimes|g\rangle\langle g|)
=\rho\otimes|g\rangle\langle g|.
\]

Não se conclui T=Id em entradas com OH excitado. Essa distinção evita a inferência falsa de que Ω⊗g seria separante para o produto.

**Aplicação sem bomba.** R66 com Ω_pump=0 preserva |0_i,0_o,g⟩: a_i,a_o,σ₋ e J o anulam; Z atua como escalar e h₀ também. Se κ_i+λ>0, com λ=βγ_Λ, o estado |1_i,0_o,g⟩ sofre perda/transição. Portanto esse canal R66 não admite uma extensão que simultaneamente (a) tenha Kraus estritamente locais em M⊗M₂, (b) identifique o zero de dois modos com o vácuo espacial Ω e (c) reproduza R66 em todo o setor campo⊗g. Não é uma proibição de detector efetivo, nem de acoplamentos com suporte temporal crescente.

## 3. Teorema tangente: a obstrução persiste COM bomba para GKLS local limitado

Para um GKLS com h=h† e saltos limitados L_j, a derivada de pureza de um estado puro ρ_χ=|χ⟩⟨χ|, normalizado, é

\[
\left.\frac{d}{dt}\mathrm{Tr}(\rho_t^2)\right|_0
=2\mathrm{Tr}(\rho_\chi\mathcal G\rho_\chi)
=-2\sum_j\left(\|L_j\chi\|^2-|\langle\chi,L_j\chi\rangle|^2\right).
\tag{P}
\]

O comutador de h tem traço zero nessa expressão. A última igualdade vem de expandir cada dissipador; os termos são variâncias não negativas. Em particular, derivada zero implica L_jχ=c_jχ para cada j, por igualdade em Cauchy–Schwarz.

Suponha agora L_j∈M⊗M₂ e χ₀=Ω⊗g. Se a derivada de pureza em χ₀ é zero, a prova por blocos do §2 força L_j(ψ⊗g)=c_jψ⊗g para qualquer ψ do campo. Assim (P) deve ser zero em **toda** entrada pura ψ⊗g. Isso independe do Hamiltoniano e não presume que χ₀ fique estacionário.

No gerador R66, sobre os vetores de partículas finitas:

\[
\dot{\mathcal P}(0;\chi_0)=0,
\qquad
\dot{\mathcal P}(0;\chi_i)=-2(\kappa_i+\lambda),
\quad\chi_i=|1_i,0_o,g\rangle.
\tag{R}
\]

Conferência algébrica: em χ₀ apenas L₄=√γφ Z tem valor não nulo, mas é autovetor, variância zero. Em χ_i, √κ_i a_i leva a |0_i,0_o,g⟩ e √λ J leva a |0_i,0_o,e⟩, ambos ortogonais à entrada; suas variâncias são κ_i e λ. Os demais saltos têm variância zero. A bomba e o acoplamento Jaynes–Cummings são Hamiltonianos e não entram em (P). Para χ_o=|0_i,1_o,g⟩ a derivada é −2κ_o.

Portanto, se κ_i+λ>0 (ou κ_o>0), **nenhum GKLS de saltos limitados estritamente locais nessa álgebra, com a mesma identificação do vácuo e do OH, coincide com R66 já nessas duas tangentes de pureza**, mesmo com bombeamento.

O gerador R66 é ilimitado; (R) é legítima no seu core finito e não aplica a fórmula a todo estado de energia infinita. A conclusão exclui realizadores locais **limitados** com essa igualdade de tangentes. Não prova impossibilidade universal de realizadores ilimitados, cuja afiliação/domínios e derivadas exigiriam tratamento próprio. Tampouco cobre evolução não-Markoviana reduzida ou aproximação com erro não nulo.

## 4. Interação local concreta por campos reais, sem destruir o termo cruzado

Há uma construção local genuína reaproveitando W e Φ. Para f∈K(O), ε>0, defina

\[
Q_\varepsilon(f)=
\frac{W(\varepsilon f)-W(-\varepsilon f)}{2i\sqrt2\,\varepsilon}
=\frac{\sin(\sqrt2\varepsilon\Phi(f))}{\sqrt2\varepsilon}.
\]

Ela é auto-adjunta, limitada, pertence a M e tem norma ≤1/(√2 ε). A segunda igualdade usa precisamente a normalização FieldWeyl; com a convenção de deslocamento sem rotação estaria errada. Pelo cálculo espectral, para ψ∈D(Φ(f)³),

\[
\|(Q_\varepsilon(f)-\Phi(f))\psi\|
\le\frac{\varepsilon^2}{3}\|\Phi(f)^3\psi\|.
\tag{Q}
\]

Prova: |sin z−z|≤|z|³/6 para z real, integrada contra a medida espectral de ψ. Logo há aproximação controlada de cada quadratura sobre domínio explícito. Esta cota **não** fornece por si convergência de geradores GKLS ilimitados ou de seus semigrupos.

Escolha pares u_r,v_r∈K(O), r=i,o, com s_r=Im⟨u_r,v_r⟩>0. A existência de ao menos um par na cunha vem de `KWR_not_isotropic` (inverter v se necessário). Duas duplas com CCR cruzadas independentes exigem sua matriz simplética; **não se presume que a fonte de um par já forneça dois modos independentes**. Para a interação limitada seguinte, essa independência não é necessária.

\[
b_{r,\varepsilon}=\frac{Q_\varepsilon(u_r)+iQ_\varepsilon(v_r)}{\sqrt{2s_r}},
\qquad
J_\varepsilon=b_{o,\varepsilon}^\dagger\sigma_-+
\sigma_+b_{i,\varepsilon}=:A_\varepsilon+B_\varepsilon.
\]

Todos são limitados em M⊗M₂. Defina h_{0,ε} substituindo a_i,a_o por b_{i,ε},b_{o,ε} no h₀ R66 e n_r por b_{r,ε}†b_{r,ε}; acrescente a mesma bomba Ω_pump σ_x. Use os cinco saltos com os mesmos coeficientes R66 e J_ε como **um só salto**. Obtém-se um GKLS limitado estritamente local que fixa o comutante por R69. Isso é uma **realização local candidata distinta**, explicitamente indexada por ε e pelos testes reais. Não recebe o nome de gerador R66.

A soma no salto é preservada exatamente:

\[
\mathcal D[A_\varepsilon+B_\varepsilon](\rho)
=\mathcal D[A_\varepsilon](\rho)+\mathcal D[B_\varepsilon](\rho)
+A_\varepsilon\rho B_\varepsilon^\dagger+B_\varepsilon\rho A_\varepsilon^\dagger
-\tfrac12\{A_\varepsilon^\dagger B_\varepsilon+
B_\varepsilon^\dagger A_\varepsilon,\rho\}.
\]

Neste caso os produtos A_ε†B_ε=B_ε†A_ε=0 por σ₊²=σ₋²=0, independentemente de CCR entre os campos. **Os termos cruzados de reciclagem permanecem**. Separar duas ancillas eliminaria precisamente esses termos.

## 5. Reservatório local e redução controlada para cada ε fixo

Para o salto J_ε sozinho, absorva √λ em L e use uma ancilla de dois níveis em |0⟩:

\[
V=L\otimes|1\rangle\langle0|-L^\dagger\otimes|0\rangle\langle1|,
\quad U_\delta=e^{\sqrt\delta V},
\quad\Phi_\delta(\rho)=\mathrm{Tr}_E[U_\delta(\rho\otimes|0\rangle\langle0|)U_\delta^\dagger].
\]

V†=−V e ||V||=||L||=:a. U pertence à álgebra local com ancilla; seus dois blocos Kraus estão na álgebra local. A paridade da ancilla anula termos ímpares. Expandindo a conjugação em ad_V, obtém-se Φδ=I+δD[L]+resto. Em norma induzida 1→1, ||ad_V||≤2a e o traço parcial tem norma ≤1. Assim, para 0≤δ≤δ₀,

\[
\|\Phi_\delta-e^{\delta\mathcal D[L]}\|_{1\to1}
\le C\delta^2,\quad
C=\frac{(2a)^4e^{2a\sqrt{\delta_0}}}{24}
+\frac{(2a^2)^2e^{2a^2\delta_0}}{2}.
\tag{C}
\]

A primeira parcela limita a cauda da série de conjugação a partir da quarta ordem em √δ; a segunda limita a cauda exponencial de D[L], cuja norma é ≤2a². Não é uma constante ajustada nem medida. Telescopagem entre contrações CPTP dá erro ≤Ct²/n em n passos δ=t/n.

Para os cinco saltos e o Hamiltoniano limitado, reaproveita-se a ancilla C⁶ e a expansão R66: a exponencial de operadores **limitados** converge em norma mesmo em Hilbert infinita; a prova não depende da dimensão finita do sistema. Há erro O(δ²) com constante finita dependente de ε. O canal OH admite a mesma entrada coerente α=iΩ_pump/√γ_OH quando γ_OH>0; se γ_OH=0, a bomba fica no Hamiltoniano. Todos os blocos Kraus permanecem locais. Essa construção fornece o semigrupo **local candidato ε**, mantendo o índice único de J e sua interferência.

As normas de Q_ε crescem quando ε→0. Nenhuma uniformidade da constante C em ε é afirmada. A cota (Q), isolada, não permite trocar o limite de colisões pelo limite ε→0. Esta entrega entrega o limite reduzido de colisões para **cada ε fixo** e a aproximação de quadraturas em domínio; não um limite GKLS ilimitado local já construído.

## 6. Diferença calculada entre o modo local e o modo de perda R66

Para um par u,v local com s=Im⟨u,v⟩>0, no domínio exponencial comum o limite formal das quadraturas é

\[
b=\frac{\Phi(u)+i\Phi(v)}{\sqrt{2s}}
=a(f)+a^\dagger(g),
\quad f=\frac{u-iv}{2\sqrt s},\quad g=\frac{u+iv}{2\sqrt s}.
\tag{B}
\]

Aqui a é antilinear no argumento, a† é linear, conforme a convenção do produto interno. A identidade vem de expandir Φ=(a+a†)/√2. Vale ||f||²−||g||²=1 e [b,b†]=I no core, mas bΩ=a†(g)Ω. Se u,v∈K(O)⊂KWR e s>0, g não pode ser zero: g=0 daria v=iu com u,iu∈KWR, contradizendo separação. Portanto

\[
\boxed{\|b\Omega\|^2=\|g\|^2>0.}
\]

O campo local admite um par canônico de quadraturas, porém seu aniquilador efetivo contém componente criadora relativa ao vácuo global. Essa é a diferença concreta que evita o teorema de trivialidade: ele não é um canal de perda que mantém aquele vácuo puro. Em um dissipador D[b] formalmente definido no core, a contribuição inicial à perda de pureza do vácuo é −2||g||²; a construção de um semigrupo ilimitado com esse b permanece separada.

É possível estudar detecção sobre estados de energia limitada, banho não-vácuo, aproximações de frequência positiva ou regiões de interação que crescem no tempo. Mas igualar o candidato local a R66 sem contabilizar g e os termos adicionais eliminaria uma diferença derivada, não uma escolha de notação.

## Resultado material e alcance

1. **PROVADO EM TEXTO:** canal de Kraus locais preservando vácuo separante puro é trivial; versão correta com OH.
2. **PROVADO EM TEXTO:** a tangente de pureza impede um GKLS limitado estritamente local de reproduzir os dois estados de referência de R66 quando κ_i+λ>0, mesmo com bomba.
3. **CONSTRUÍDO EM TEXTO:** interação local limitada por Weyl, cinco saltos e reservatório coerente, com um único J e redução de colisões controlada para ε fixo.
4. **DIFERENÇA EXIBIDA:** o modo local tem criação g≠0 no vácuo; não é o aniquilador R66. A redução causal não foi promovida a igualdade falsa.

R5 não fecha globalmente com estes resultados. A classe “ligar exatamente R66, com perdas escuras de vácuo, a coeficientes limitados de uma única álgebra local” foi agora delimitada por um obstáculo matemático. A rota seguinte deve escolher e justificar uma aproximação física ou um contrato local ampliado que carregue os termos adicionais. Nenhuma conclusão histórica, teológica, experimental ou de gate decorre disso.
