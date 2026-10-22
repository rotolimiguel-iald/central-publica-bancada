# F1.2 — assinatura da ponte matricial contínua

07/10/2026 · [DERIVED/OPEN] Esta é a redução matemática que falta tipar no Lean; **não é um teorema compilado**. A fonte de convenções da bancada é `TETELESTAI_V350_KERNEL_20260911/CONVENCOES_DO_TRACO.md`; o fornecedor de escala já existente é `V351InverseLimitScaling.scalarInverseLimitWeight_dual`.

Seja `ρ∈M_n(ℂ)` positiva definida e `u_t=ρ^{it}`. A ação modular interna é `σ_t(a)=u_t a u_t*`. Na representação regular sobre `L²(ℝ,ℂⁿ)`, escolher `π_σ(a)f(r)=σ_{-r}(a)f(r)` e `λ_t f(r)=f(r-t)`. A conjugação pontual `Vf(r)=u_r f(r)` satisfaz, por cálculo direto,

```text
V π_σ(a) V* = a ⊗ 1,
V λ_t V* = u_t ⊗ λ_t.
```

Como `u_t` já pertence ao fator matricial, as álgebras geradas coincidem com `M_n(ℂ)⊗L(ℝ)` sob essa conjugação. Fixar a convenção de Fourier `λ_t ↦ exp(i t x)` e `θ_s(λ_t)=exp(-i s t)λ_t`. Então `θ_s F(x)=F(x-s)`. Para `F≥0` integrável no peso,

```text
τ(F) = ∫ tr_n(F(x)) exp(-x) dx,
τ(θ_s F) = ∫ tr_n(F(x-s)) exp(-x) dx = exp(-s) τ(F).
```

O domínio positivo, a extensão normal/semifinita e a normalização do traço precisam ser construídos antes de chamar isto de `M_n⋊_σℝ` no núcleo. A igualdade formal da última linha é mudança de variável; ela não fornece sozinha os objetos analíticos de produto cruzado e traço. O **peso dual** da representação regular não deve receber o nome `τ` por mera troca de símbolo: sua invariância é distinta da escala do traço canônico.

**Assinatura Lean desejada, sem fingir que já existe:** (i) ação contínua `σ` implementada por `u_t`; (ii) representação covariante fiel e álgebra gerada; (iii) equivalência estelar com `M_n⊗L(ℝ)` que entrelace `θ`; (iv) traço normal semifinito no cone positivo, com fórmula integral e domínio; (v) aplicação do lema de escala, seguida de `#print axioms`, `lake build` no sandbox e revisão independente. A rota B do núcleo regular da v351 pode fornecer o lema de escala, mas a equivalência (iii) ainda deve ser uma construção, nunca uma hipótese escondida dentro do nome.
