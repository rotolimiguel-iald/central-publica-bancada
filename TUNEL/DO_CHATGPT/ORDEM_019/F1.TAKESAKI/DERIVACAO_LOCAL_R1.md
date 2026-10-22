# F1.TAKESAKI — primeira derivação e contrato de alcance

Autor: codex-gerente-tgl, 13/10/2026, reivindicação 733. Base de raciocínio: v392, autorizada pelo operador, com ratificação do rito ainda distinta da validade condicional dos enunciados. Esta nota é [DERIVED] sobre resultados [KNOWN]; não anuncia construção geral compilada no kernel.

## 1. Enunciado preciso

Seja M uma álgebra de von Neumann e ω um estado fiel normal. Use **o grupo modular de ω**, σ^ω, e forme N = M ⋊_{σ^ω} ℝ. Fixe a convenção θ_s(λ(t)) = exp(−ist)λ(t), com θ_s(π(x)) = π(x). A conclusão é a existência de um traço fiel normal semifinito τ em N, com τ∘θ_s = exp(−s)τ.

A hipótese é a estrutura modular completa, incluindo a caracterização KMS. A normalização ω(I)=1 e a preservação de ω por um fluxo arbitrário não identificam, sozinhas, esse grupo. A normalização fixa a massa do estado; a lei exponencial é uma covariância do traço no core, não a afirmação τ∘θ_s=τ.

Fonte conferida: Fumio Hiai, *Concise lectures on selected topics of von Neumann algebras*, arXiv:2004.02383v1, teorema 10.15, pp. 99–100, e observação 10.16. PDF custodiado em sources, hash em CUSTODY_R1.json. Takesaki 1973 foi custodiado como fonte original; a conferência semântica local desta nota usou a exposição de Hiai.

## 2. Onde a invariância entra

1. O peso dual φ = ω̃ é construído pela integração da ação dual. Por invariância de Haar, φ∘θ_s = φ.
2. Seu grupo modular satisfaz σ_t^φ(π(x)) = π(σ_t^ω(x)). A fórmula sobre λ(u) contém o cociclo de Radon–Nikodym de ω∘σ_u^ω em relação a ω.
3. **É neste ponto que ω∘σ_u^ω = ω é consumida:** o cociclo é 1, logo σ_t^φ(λ(u)) = λ(u). Nos geradores, σ_t^φ = Ad λ(t).
4. Escrevendo λ(t) = h^{it}, com h positivo, não singular e afiliado, a construção de Pedersen–Takesaki retira essa densidade modular: τ = φ_{h^{-1}} é um traço fiel normal semifinito.
5. A convenção dual dá θ_s(h)=exp(−s)h. Assim, para B=h^{-1}, θ_s(B)=exp(s)B.

A invariância é um ingrediente efetivo da construção. O resultado depende também da identificação do fluxo como modular, do produto cruzado, da existência dos pesos e do cálculo dos operadores afiliados.

## 3. A conta da escala, com domínio

Não interpretar φ(B^{1/2}xB^{1/2}) como produto de operadores limitados se B for ilimitado. Use B_ε=B(1+εB)^{-1} e a definição do peso perturbado por limite crescente, para x≥0:

τ(x)=lim_{ε↓0} φ(B_ε^{1/2}xB_ε^{1/2}).

Como φ∘θ_{−s}=φ e θ_{−s}(B_ε)=exp(−s)B_{exp(−s)ε}, segue

τ(θ_s(x))
= lim_{ε↓0} φ(θ_{−s}(B_ε)^{1/2} x θ_{−s}(B_ε)^{1/2})
= exp(−s) lim_{ε↓0} φ(B_{exp(−s)ε}^{1/2} x B_{exp(−s)ε}^{1/2})
= exp(−s)τ(x).

O limite e as igualdades são no cone positivo estendido; valores infinitos são permitidos. A restrição a traço finito é necessária para passar a uma interface real como DualScalingData. A F1.2 já faz essa restrição e prova sua não vacuidade no modelo regular V351.

## 4. Controles que delimitam a afirmação

**Controle A — fluxo preservante arbitrário.** Em M₂, tome ρ=diag(p,1−p), 0<p<1, p≠1/2, e o fluxo identidade. Ele preserva ω(x)=Tr(ρx), mas não é σ^ω. No produto cruzado desse fluxo trivial, λ é central, enquanto o peso dual ainda tem grupo modular Ad ρ^{it} na parte matricial. Portanto σ^φ=Ad λ falha. A perturbação pela densidade de λ permanece ponderada por ρ e não é traço: com uma função positiva de suporte compacto na parte real, as avaliações nos produtos E₁₂E₂₁ e E₂₁E₁₂ são proporcionais a p e 1−p. Isso não impede que esse produto cruzado tenha outro traço com escala; impede inferir a construção pretendida da mera invariância por um fluxo qualquer.

**Controle B — álgebra finita.** Se θ_s é unital e 0<τ(1)<∞, então a lei aplicada à unidade dá τ(1)=exp(−s)τ(1), logo s=0. Não há análogo finito não trivial dessa mesma lei para um traço finito sobre toda a álgebra. A família τ_s=exp(−s)τ₀ verifica uma reescala por definição, mas não fornece a ação dual solicitada.

**Modelo concreto útil.** Para a base matricial, o core é isomorfo a M_n ⊗ L∞(ℝ), sob identificação que precisa entrelaçar as ações e os pesos. A parte contínua permite θ_s f(r)=f(r+s) e τ(A)=∫exp(r)Tr(A(r))dr. Mudança de variável produz a escala. Esse modelo tem τ(1)=∞ e elementos positivos de traço finito. Escrever a integral não formaliza automaticamente o produto cruzado ou sua equivalência; essa identificação é a obrigação que permanece.

**Não há contraexemplo ao teorema da invariância pelo próprio fluxo modular** mantendo as suas hipóteses. Um controle honesto troca o fluxo ou enfraquece outra hipótese e identifica qual etapa deixa de valer.

## 5. Reaproveitamento e próximo trabalho

- [REAL — fonte e evidência existente] V351DualScalingBridge e AgapeNonVacuity, agora no pacote v392: escala concreta do modelo regular, domínio de traço finito, testemunha positiva e aplicação de Fundacao.agape.
- [OPEN — construção local] identificar fielmente esse modelo com o produto cruzado pretendido, por equivalência que entrelace π, λ, θ e τ; provar a construção geral no ferramental Lean disponível.
- [OPEN — QG mais ampla] Takesaki não fornece por si só o habitante da rede BGL/Fock, nem deriva H3 do estado, nem constrói o tensor de Maxwell e a métrica globais.
- [EM_CURSO] pedido Kimi existente, com contrato completado. Uma resposta do provedor será candidata [DECLARADO], submetida à conferência local; não é automaticamente prova.

As cunhagens ficam nos originais verbatim pinados pelo contrato. As explicações desta nota são paráfrase matemática, não citações do operador. Nenhum gate é alterado.
