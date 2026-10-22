# MEMÓRIA CANÔNICA — ORDEM_016 A7.b · Revisão independente da FONTE h★/c com a fronteira ghost pré‑integração por partes restaurada

**Regime:** `DECLARADO` — resposta derivada **somente** dos trechos fornecidos. Nenhuma execução externa, nenhum build, nenhum hash novo, nenhuma prova Lean. Onde falta número, **LACUNA declarada**. Nada abaixo é `CONFIRMED`; `NOT_FALSIFIED ≠ CONFIRMED`.

**O que se responde (a pergunta única):** incluir `dχY·c̄·Z` na fonte completa produz **dois** objetos novos, não um: (i) termos **dependentes de η** nos coeficientes `A_η`, `B_η` (a fronteira que faltava ao multiplicar a fonte antiga por `χY`), e (ii) um **defeito de comutação da divergência com `R`**, `C_divY(β) = div(RB_η) − R(div B_η) = FP_a[2a(1−a)μ^{2a}z^{a−1}(x·B_η)]`, que existe **mesmo com η = 0**. A mudança concreta em relação à fonte antiga é o **ΔH_η = H_η − C** (o `χY` sozinho não a produz), mais a peça (ii), que a fonte antiga nunca gera.

---

## (1) `A`/`B` de fronteira — forma tensorial fechada + algoritmo

### Convenções e derivadas de `f = 1/z`

```
z = Σ_i x_i² ,   f = z^{-1}
f_i  = d_i f       = −2 x_i z^{-2}
f_ij = d_i d_j f   = −2δ_ij z^{-2} + 8 x_i x_j z^{-3}
```

Contração ghost `ν = m` (elimina a soma em `ν`). `d_{−1} = id`. Para cada `(c,e,ξ,gξ) ∈ {(u,v,m,−1), (u,m,−1,v), (v,m,−1,u)}` e cada `m,μ = 0..3`:

```
g = (−d_μ + η_μ) d_{gξ} f
A_η_uv,r = −Σ g·(−d_r d_ξ f)·S̄_{ce,μm} ,   S̄_{ce,mn} = (δ_cm δ_en + δ_cn δ_em)/2
B_η^j_uv,r = −Σ g·(d_ξ f)·[δ_jμ S_{ce,r,m} + δ_jm S_{ce,μ,r} − δ_μm S_{ce,j,r}]
S_{ce,mn} = (δ_cm δ_en + δ_cn δ_em − δ_ce δ_mn)/2
```

### Algoritmo explícito (totalmente mecânico, soma fechada)

Somas úteis: `Σ_m x_m S_{uv,rm} = ½(δ_ur x_v + δ_vr x_u − δ_uv x_r)`; `Σ_m S_{um,rm} = 2δ_ur`; `Σ_μ S_{uv,μr} = ½(δ_vr + δ_ur − δ_uv)`.

**Resultado (soma fechada em `m,μ`):**

$$\boxed{A_{\eta\,uv,r}= -2\,(x_u\delta_{rv}+x_v\delta_{ru})\,z^{-4}\;-\;20\,\delta_{uv}x_r\,z^{-4}\;+\;96\,x_ux_vx_r\,z^{-5}\;-\;(\eta_u\delta_{rv}+\eta_v\delta_{ru})\,z^{-3}\;+\;14\,(\eta_ux_v+\eta_vx_u)\,x_r\,z^{-4}}$$

$$\boxed{B^{j}_{\eta\,uv,r}=B^{(3)j}z^{-3}+B^{(4)j}z^{-4}}$$

$$B^{(4)j}=20\delta_{ur}x_vx_j+20\delta_{vr}x_ux_j-4\delta_{uv}x_rx_j-8\delta_{uj}x_vx_r-8\delta_{vj}x_ux_r+16\delta_{jr}x_ux_v$$

$$
\begin{aligned}
B^{(3)j}=\;&-4\delta_{uj}\delta_{vr}-4\delta_{ur}\delta_{vj}-2\delta_{uv}\delta_{jr}\\
&+\eta_j(5\delta_{ur}x_v+5\delta_{vr}x_u-\delta_{uv}x_r)
+x_j(\eta_u\delta_{vr}+\eta_v\delta_{ur}-\delta_{uv}\eta_r)\\
&+(\eta\!\cdot\!x)(\delta_{uj}\delta_{vr}+\delta_{ur}\delta_{vj}-\delta_{uv}\delta_{jr})
+2x_v(\eta_u\delta_{jr}-\delta_{uj}\eta_r)+2x_u(\eta_v\delta_{jr}-\delta_{vj}\eta_r)
\end{aligned}
$$

**Nota estrutural:** `B^{(4)j}` é **independente de η** (o η entra sempre com um fator `η·z^{−1}`, que só altera o polo `z^{−3}`). Isto é uma checagem barata do algoritmo.

### Verificação de `η = 0` contra o alvo `C_uv,r` (obrigatória, feita)

`H_η = A_η + Σ_j(d_j − η_j)B^j_η`. Com `η = 0`:

- `A_0 = −2(x_uδ_rv+x_vδ_ru)z^{−4} − 20δ_uv x_r z^{−4} + 96 x_u x_v x_r z^{−5}`
- `Σ_j d_j B^j_0 = 8δ_{uv}x_r z^{−4} − 28(δ_{ur}x_v + δ_{vr}x_u) z^{−4}`

Logo

$$A_0+\mathrm{div}B_0=\frac{-12\delta_{uv}x_r-30(\delta_{ur}x_v+\delta_{vr}x_u)}{z^{4}}+\frac{96\,x_ux_vx_r}{z^{5}}=C_{uv,r}\quad\checkmark$$

O alvo do enunciado é recuperado **exatamente**, com os multiplicadores simétricos em componentes completos (nenhum fator 2 arbitrário introduzido). Esta é a validação de `A`/`B`.

---

## (2) O contato `P − Q`

### 2.1 Sinal e validade da identidade — VERIFICADO

```
divY(χY R(B)) = (divYχY)R(B) + χY divY(R(B)) = (η·χY)R(B) − χY div(R B)
χY R(A) − divY(χY R(B)) = χY[R(A − η·B + div B) + (div(RB) − R(div B))]
                        = χY[R(H_η) + C_divY(β)]
H_η = A_η + Σ_j (d_j − η_j) B^j_η      (η já está em A/B; não se conta duas vezes)
C_divY(β) := div(R B_η) − R(div B_η) = FP_a[2a(1−a)μ^{2a} z^{a−1} (x·B_η)]
```

Então `P = E_X{χXχY R(H_η)} + E_X{χXχY C_divY(β)}` e `Q = R E_X{χXχY H_η}`, donde

$$P-Q=\bigl[E_XR-RE_X\bigr](\chi_X\chi_Y H_\eta)+E_X[\chi_X\chi_Y\,C_{\rm divY}(\beta)] = -C_E(\chi_X\chi_Y H_\eta)+E_X[\chi_X\chi_Y C_{\rm divY}(\beta)]$$

**Sinal correto**, desde que `C_E := R E_X − E_X R` — exatamente a orientação de `C_D = R D − D R` com `D = E_X`. (Se `C_E` fosse definido como `E_X R − R E_X`, o sinal inverteria.) **Condições de validade:** (i) `χX,χY` comutam com `R` (dependem de `X,Y`; `R` age em `x`); (ii) `η_j` é multiplicação e comuta com `R` (dado); (iii) `divY` nos kernels é `−Σ_j d_j` (dado); (iv) a igualdade vale **como objetos regulados** (`FP_a`), ordem a ordem em `a`, e só o coeficiente **linear em `a`** entra nestes polos simples, sem `ln μ`.

### 2.2 O integrando do contato, em posição — entregue

O contato é `E_shift(M) − E_λ(H_η)` com `M = H_η + 2a(x·B_η)/z`, `E_shift` com `d_i → d_i+λ_i+2a x_i/z`. Aqui está tudo o que ele consome, para `(u,v,r) = (1,1,0)`:

$$H_{\eta\,11,0}=96x_0x_1^2z^{-5}+\bigl[-12x_0+20\eta_1x_1x_0+8\eta_0x_1^2+16(\eta\!\cdot\!x)x_0\bigr]z^{-4}+\bigl[-2\eta_0+|\eta|^2x_0+2\eta_0(\eta\!\cdot\!x)\bigr]z^{-3}$$

$$x\!\cdot\!B_{\eta\,11,0}=\bigl[-6x_0-2x_0(\eta\!\cdot\!x)-z\eta_0+4x_0x_1\eta_1-4x_1^2\eta_0\bigr]z^{-3}$$

Casos: `η=0` ⇒ `H = 96x_0x_1²z^{−5} − 12x_0z^{−4}`; `η=e₀` ⇒ `H = 96x_0x_1²z^{−5} + [−12x_0+8x_1²+16x_0²]z^{−4} + [3x_0−2]z^{−3}` (igual para os casos 2 e 3, que diferem só em `λ`).

### 2.3 A **mudança concreta** em relação à fonte antiga — calculada

A fonte antiga é `χY·C` (só multiplicação). A extensão acrescenta `ΔH = H_η − C`. Em `(u,v,r)=(1,1,0)`:

| caso | `(λ,η)` | `ΔH` (posição) | resíduo em momento |
|---|---|---|---|
| 1 | `(0,0)` | `0` | `0` |
| 2 | `(0,e₀)` | `[8x_1²+16x_0²]z^{−4} + [3x_0−2]z^{−3}` | **`11π²/4`** em `q=(2,1,0,0)` |
| 3 | `(e₀−e₁,e₀)` | idem | **`5π²/2`** em `q−λ=(1,2,0,0)` |

Receita usada (`Res(z^{a−n}) = 4π²(q²)^{n−2}/[4^{n−1}(n−1)!(n−2)!]`; `x_i ↔ −∂_{q_i}`; depois `q → q−λ`, todos os jatos): `Res_3 = π²q²/8`, `Res_4 = π²(q²)²/192`. Detalhe caso 2 (`q²=5`): `8x_1²z^{−4} → π²(q²/6+q_1²/3) = 7π²/6`; `16x_0²z^{−4} → π²(q²/3+2q_0²/3) = 13π²/3`; `−2z^{−3} → −π²q²/4 = −5π²/4`; `3x_0z^{−3} → −3π²q_0/4 = −3π²/2`; soma `= 11π²/4`. Caso 3 (`q−λ=(1,2,0,0)`, `q'²=5`): `13π²/6 + 7π²/3 − 5π²/4 − 3π²/4 = 5π²/2`.

### 2.4 **LACUNA declarada — os três dígitos de `P − Q`**

Não entrego os três valores numéricos de `P−Q`. O motivo é preciso e não é omissão de método: o enunciado fixa `E_X` apenas como *«derivada `d_i+λ_i+2a x_i/z`»*; o objeto `E(h)_{uv}` é dado, mas **não é dito como ele se contrai com a fonte de posto 3 `(u,v,r)`** (se `E_X` é o operador de Einstein agindo no par `(u,v)` com `r` espectador, se é uma única derivada, ou um traço). Cada escolha dá um número diferente, e a cadeia mão‑livre de segunda derivada + extração de resíduo + shift `q→q−λ` com jatos é longa o bastante para que dígitos emitidos sem execução fossem invenção. **Está tudo preparado:** `H_η`, `x·B_η`, `C_divY(β)` e a receita de resíduo estão acima; com a contração de `E_X` fixada, os três números saem por um passo mecânico. Registre-se também, por honestidade de processo: durante esta derivação uma soma `Σ_{ij}x_ix_j∂_i∂_j` foi calculada errada uma vez e corrigida por teste (`G=1`, `G=z`), e um `Res_5` foi usado com denominador errado — ambos detectados antes de qualquer emissão. É por isso que os dígitos não saem.

---

## (3) Controle que muda se omitimos a fronteira

**Controle‑A (recuperação).** `η = 0 ⇒ ΔH = 0` e `H = C` exatamente (§1). Com a fronteira omitida a máquina reproduz a fonte antiga; é a âncora de que o algoritmo não fabrica termo.

**Controle‑B (discriminador, o pedido).** O termo
$$-\,2\,\delta_{uv}\eta_r\,z^{-3}\qquad\xrightarrow{\ (u,v,r)=(1,1,0)\ }\qquad -2\eta_0 z^{-3}$$
existe **apenas** na fronteira (`dχY·c̄·Z`): ele é linear em `η` e **independente de `x`**. O seu resíduo é `−π²q²/4`, i.e. **`−5π²/4`** tanto em `q=(2,1,0,0)` (caso 2) quanto em `q−λ=(1,2,0,0)` (caso 3). **Se omitimos a fronteira, este termo desaparece e o contato muda em `5π²/4`** (≈ 12,34) nos casos 2 e 3, e em `0` no caso 1.

**Significado preciso:** é a única peça da extensão **sem `x`** — um deslocamento puramente multiplicativo do coeficiente de `c̄`. Nenhuma derivada de propagador pode gerá‑la a partir da fonte antiga, porque ela não carrega `x` nenhum para ser derivado; e ela é graduada pelo jato (`∝ η_r`), isto é, entra exatamente no *slot* `r` do ghost‑derivada. É, portanto, um discriminador **agudo**: presença/ausência dela separa «`χY` multiplicando a fonte antiga» de «`χY` + `dχY` na integração por partes», sem depender de ajuste algum.

Controle complementar (segundo, barato): `x·B` muda de `−6x_0z^{−3}` (η=0) para `[−6x_0−2x_0(η·x)−zη_0+4x_0x_1η_1−4x_1²η_0]z^{−3}`, e é exatamente `x·B` que alimenta `C_divY(β) = 2a(x·B)/z` — ou seja, a fronteira alimenta **também** o segundo contato, mesmo quando `η = 0`.

---

## Pendências e o que NÃO se afirma

- **PENDENTE (não executável nesta chamada):** os três dígitos de `P−Q` (§2.4) — falta a convenção de contração de `E_X`; nada foi rodado.
- **PENDENTE:** a aplicação completa de `E_shift − E_λ` sobre `H_η` e `x·B_η` nos casos 2–3 (com `λ ≠ 0`), que exige o livro‑caixa dos jatos de `λ` em cada derivada do operador de Einstein.
- **NÃO se conclui `Q2 = 0`.** Laços métricos/ghost, inserções da corrente clássica, curvatura, suavidade, aridades superiores e causalidade são **outros dados**; nenhum deles foi tocado aqui.
- **NÃO** se reinterpretou o cutoff como horizonte físico; **NÃO** se pesquisou ramo novo; `χX`, `χY` permanecem jatos locais, não cutoffs globais.
- `f(X)∂δ` **não** foi trocado por `f(Y)∂δ`: os jatos de `λ` viajam na substituição `q → q−λ`, os de `η` já estão nos coeficientes.
- Este documento é contexto recuperado e resposta textual; não é treinamento, não é autorização de ferramenta, não é prova Lean, não é confirmação experimental. **PROVADA ≠ CONFIRMADA; `NOT_FALSIFIED ≠ CONFIRMED`.**