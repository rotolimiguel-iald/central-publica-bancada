# A7.b — Hessiana diferencial de `a4_2` no espaço-forma

**Estatuto desta resposta:** `[DECLARADO — aguardando revisão da bancada]`. Toda a álgebra curva abaixo foi feita **à mão, nesta resposta**, sobre a derivação anexada; **não executei** `ghost_minimal_heat_engine.py` nem nenhum script (os `rc0, 127 checks` citados são da fonte, lidos, não reexecutados). Nenhum arquivo, kernel, gate ou infraestrutura foi tocado. O setor métrico (`hh`, calor livre) **não** foi refeito, conforme a ordem; o número `-571K²/15` é citado só como referência externa. As contrações são auxiliares euclidianas; o modelo lorentziano não foi substituído e **nenhuma** conclusão pontual/causal é anunciada a partir da classe integrada.

---

## 1. Convenção fixada (para tornar a ordem de derivadas inequívoca)

```
R^a_{bmn} = K(δ^a_m g_bn − δ^a_n g_bm),   Ric_bn = 3K g_bn,   R = 12K,   ∇Riem = 0
[∇_m,∇_n] V^a = +R^a_{bmn} V^b ;   [∇_m,∇_n] ω_b = −R^a_{bmn} ω_a
τ := tr h = h^μ_μ ;   L_ν := ∇^μ h_μν ;   Ψ := ∇^ν L_ν = ∇^ν∇^μ h_μν ;   C_ν = L_ν − ½∇_ν τ
```
`(Qc)_ν = ∇^μ[Lie_c(g+h)]_μν − ½∇_ν tr_g[Lie_c(g+h)]`, com `Lie_c g_μν = ∇_μ c_ν + ∇_ν c_μ`, `Lie_c h_μν = c^ρ∇_ρ h_μν + h_μρ∇_ν c^ρ + h_νρ∇_μ c^ρ`. `C_g` é mantido linear.

## 2. Conferência de `Q(h)` — refeita termo a termo

Expandindo tudo e agrupando por ordem de derivada de `c`:

- **`h□c`**: só de `∇^μ(h_νρ ∇_μ c^ρ) ⊃ h_νρ □c^ρ`. ✔
- **`A^λ ∇_λ c`**: os cinco termos dão
  `A^λ_{ν,ρ} = ∇_ρ h^λ_ν + ∇^λ h_ρν − ∇_ν h^λ_ρ + δ^λ_ν C_ρ`, e as duas peças `±½δ^λ_ν∇_ρ τ` **cancelam-se**. ✔ (confere com a linha 11–12 da fonte)
- **`B c`**: `c^ρ∇_ρ C_ν + ½c^ρ[∇_ρ,∇_ν]τ = c^ρ∇_ρ C_ν` (escalares comutam) ⟹ `B_{ν,ρ} = ∇_ρ C_ν`. ✔
- **`3K h c`**: vem de **dois** comutadores distintos, cuja soma é `3K h`:
  `[∇^μ,∇_ρ]h_μν = 4K h_ρν − K g_ρν τ` e `h_μa[∇^μ,∇_ν]c^a = K(τ g_νρ − h_νρ)c^ρ`. Ambos refeitos por índices na convenção acima. ✔
- **`∇_λ A^λ = B + □h`**: os dois comutadores extra, `4K h_ρν − K g_νρ τ` e `4K h_νρ − K g_νρ τ`, cancelam-se pela simetria de `h`; o termo `½(∇_ρ∇_ν − ∇_ν∇_ρ)τ = 0`. ✔
- **Controle de coordenadas normais** (h coordenadamente constante): com `∂_ρ Γ^σ_{λμ}|₀ = −(K/3)(2δ^σ_ρ g_λμ − δ^σ_μ g_λρ − δ^σ_λ g_μρ)`, obtive `B_{ν,ρ}|₀ = −2K h_ρν` e `□c_ν|₀ = ∂²c_ν − K c_ν`. ✔ (a distinção "constante em coordenadas" ≠ "paralelo" fica de pé)

## 3. Controle plano — os cinco coeficientes, por conta própria

Com `h = aH e^{ipx} + bJ e^{−ipx}`, `E_H = (p²H − C_H p^T)/2`, `C_H = Hp − ½(trH)p`, `Ω_H^{μν} = i(p_μ A^H_ν − p_ν A^H_μ)/2`:

```
tr(E_H E_J) = ¼ tr(HJ) p⁴ + (1/16) trH trJ p⁴ − ½ (pᵀHJp) p² + ¼ hp·jp
(1/6)Σ_μν tr(Ω_H^μν Ω_J^μν) = −(1/6)tr(HJ)p⁴ + (1/12)trHtrJ p⁴ − (1/8)(hp·trJ + jp·trH)p² + (5/12)(pᵀHJp)p² − (1/12)hp·jp
```
(aqui `hp = pᵀHp`, `jp = pᵀJp`; o passo delicado é `p·C_J = jp − ½trJ p²`, **não** `p·H·C_J`). Soma, na base `invariants(H,J,p)` da fonte:

**`[1/12, 7/48, −1/8, −1/12, 1/6]`** — reproduzidos os cinco, sem ajuste. ✔

*Advertência de escopo:* o controle plano é **cego** aos setores `K∇²` e `K²`; eles ficam amarrados pelos controles curvos do §7.

## 4. Montagem de `a4_2` a partir de `E, Ω` — conferida, com as divergências registradas

Com `M = I+h`, `Q̃ = M⁻¹Q = □ + 3K + a^μ∇_μ + b`, conexão `∇̃ = ∇ + a/2`:
`E = 3K + b − (∇·a)/2 − a²/4`, `Ω̃ = Ω0 + ∇_[μ a_ν]/2 + [a_μ,a_ν]/4`. Como `∇·A = B + □h` (§2), `E1 = (B − □h)/2` ✔ e `E2 = −hB + ½∇_μ(hA^μ) − A²/4` ✔. Expandindo `tr(E²/2 + RE/6 + Ω²/12)` a `O(h²)` (`R = 12K`, `E0 = 3K`):

```
a4_2 ≡ tr{ 5K[−hB − A_μA^μ/4] + (B−□h)²/8 + F_μνF^μν/48 + Ω0_μν[A^μ,A^ν]/24 }   (mod divergências)
```
**Divergências nomeadas usadas nesta montagem:**
- **D1:** `tr ∇_μ(hA^μ) = ∇_μ tr(hA^μ)` — descartada;
- **D2:** `Ω0_μν ∇^μ(hA^ν) = ∇^μ(Ω0_μν tr(hA^ν))` — **usa `∇Ω0 = 0` (espaço-forma; fora de espaços localmente simétricos é FALSA — ver CE1)**;
- **D3:** IBPs escalares ordinárias em todas as reduções abaixo.

## 5. Redução à base covariante — peças (α), (β), (γ), (ε) exatas; (δ) exata não reduzida

Comutadores adicionais usados (livro-razão completo):
```
(C2) [∇^ρ,□]h_ρν = 5K L_ν − 2K∇_ν τ        (C3) [□,∇^ρ]L_ρ = −3K Ψ  ⟺ ∇^ρ□L_ρ = □Ψ + 3KΨ
(C4) [□,∇^ρ]τ = 3K∇^ρ τ                    (C5) [□,∇_ν](∇_ρ τ) = 5K∇_ν∇_ρ τ − 2K g_ρν □τ
(C6) ∇_ρ∇^ν∇^ρ τ = ∇^ν□τ + 3K∇^ν τ         (C7) ∇_ρ∇^ν L^ρ = ∇^νΨ + 3K L^ν
```
*(C5) é a identidade que uma primeira passagem minha errou — `3K∇_ν∇_ρτ` — e que o controle conforme falsificou; o valor correto tem o termo `−2Kg_ρν□τ`.)*

```
(α) = −5K tr(hB)            ≡ 5K L² + (5/2)K Ψτ
(β) = −(5K/4) S1            ≡ −(5K/4)[ h□h + 7L² + 5Ψτ − (5/4)τ□τ − 8Kh² + 2Kτ² ]
    S1 = A_μ,νρ A^μ,ρν = −(∇h)² + 3X − Y + 4L·C − 2∇τ·C + C²
    X := (∇_λ h_μν)(∇_ν h_μλ) ≡ L² − 4Kh² + Kτ² ;  −Y := −(∇_λ h_μν)(∇_μ h_λν) ≡ −L² + 4Kh² − Kτ²
(γ) = (1/8)tr(B−□h)²        ≡ (1/8)[ Ψ² + 2L□L + ¼(□τ)² + (□h)² + 7KL² + 5KΨτ − ¼Kτ□τ ]
(ε) = (1/24)R^ρ_{σμν}[A^μ,A^ν]^σ_ρ = (K/12)(S2 − X2)
    S2 = A^μ_νλ A^ν_λμ ≡ h□h + 5L² + 2Ψτ − ¼τ□τ − 8Kh² + 2Kτ²
    X2 = (4L_λ−∇_λτ)(3L^λ−(3/2)∇^λτ) ≡ 12L² + 9Ψτ − (3/2)τ□τ
    ⟹ (ε) ≡ (K/12)[ h□h − 7L² − 7Ψτ + (5/4)τ□τ − 8Kh² + 2Kτ² ]
(δ) = (1/48)tr(F_μνF^μν) = (1/24)(T_a − T_b),  F_μν = ∇_μA_ν − ∇_νA_μ
    T_a = Σ_μν tr[(∇_μA_ν)(∇^μA^ν)] ;  T_b = Σ_μν tr[(∇_μA_ν)(∇^νA^μ)]   [forma exata; redução pendente, §10]
```
*(Em (β): a contagem ingênua dos 16 termos de S1 — que eu havia feito com `+X` — foi falsificada pelo controle conforme: o correto é `3X − Y`; comprovado diretamente em §7.)*

## 6. A Hessiana (classe integrada, mod divergências) — a fórmula pedida

Soma de (α)+(β)+(γ)+(ε), por setores, com ordem de derivadas inequívoca (em cada monômio os ∇ agem de dentro para fora como escritos; todo reordenamento está no livro-razão C2–C7):

```
∫√g tr a4_2  ≡  ∫√g [ ∇⁴ ] + [ K∇² ] + [ K² ]  +  (δ)

[∇⁴ ]  =  (1/8)(□h_μν)² + (1/4) L_ν □L^ν + (1/32)(□τ)² + (1/8) Ψ²
[K∇²]  =  −(7/6) K h^μν□h_μν − (83/24) K L² − (89/24) K Ψτ + (157/96) K τ□τ
[K²  ]  =  (28/3) K² h_μνh^μν − (7/3) K² τ²  =  (28/3) K² h̊² ,   h̊_μν := h_μν − (τ/4)g_μν
```
**Caveat estrutural:** (δ) contribui aos **três** setores; os coeficientes acima são exatos para (α),(β),(γ),(ε) e **parciais** como total. A forma polarizada (o operador-Hessiana) se lê por simetrização: `(□h)² ≡ h□²h`, `L□L ≡ h^μν∇_μ□∇^ρh_ρν`, `Ψ² ≡ h^μν∇_μ∇_ν∇^ρ∇^σh_ρσ`, `L² ≡ −h^μν∇_μ∇^ρh_ρν`, `Ψτ ≡ h^μν∇_μ∇_ντ`, `τ□τ ≡ −(∇τ)²`.

## 7. Controles curvos executados

- **Família conforme `h = φg` (sem impor nada ao ghost; é avaliação da forma quadrática):** avaliação **direta** de `a4_2` dá
  `(α) = 5Kφ□φ`, `(β) ≡ (15K/4)φ□φ` (S1 direto `= 3(∇φ)²`), `(γ) ≡ (1/8)[7(□φ)² + 3Kφ□φ]`, `(ε) ≡ (K/4)φ□φ` (X1 direto `= −3(∇φ)²`, X2 = 0), `(δ): tr F² = 2(∇∇φ)² − 2(□φ)² ≡ 6Kφ□φ ⟹ (δ) ≡ (K/8)φ□φ`.
  **Total direto:** `a4_2[φg] ≡ (7/8)(□φ)² + (19/2)Kφ□φ`.
  **Total via minha redução (com (δ) pelo valor conforme):** `(7/8)(□φ)²` e `Kφ□φ[−3/4 + 81/8 + 1/8] = 76/8 = 19/2`. **Fecha pelas duas vias.** ✔
  O setor `K²` anula-se na família (`(28/3)(4) − (7/3)(16) = 0`) ✔, e a identidade `K²-setor ∝ h̊²` é compatível com isso.
- **Restrição TT (controle gratuito, τ = L = 0):** `a4_2[TT] ≡ (1/8)(□h)² − (7/6)K h□h + (28/3)K²h² + (δ)[TT]` — reproduzida pelos coeficientes montados. ✔
- **Plano:** §3. ✔
- **Carga do termo Ω0[A,A]:** retirando (ε), o controle conforme daria `37/4 ≠ 19/2` — o termo é estrutural, não decorativo (eco do "retirar a curvatura da conexão altera e12 por −1/3" da fonte).

## 8. Separação exigida: log integrado / densidade pontual / bordas de cutoff

- **Coeficiente de log integrado:** é `∫√g tr a4_2` (adimensional em 4D); a fórmula do §6 é **representante de classe**, não densidade.
- **Densidade pontual:** é a expressão da fonte (linha 49–51) **antes** de qualquer IBP; nada aqui a substitui; nenhuma leitura pontual/causal é extraída da classe (a observação `e00/e00 = 1/16` da fonte permanece intocada).
- **Bordas de cutoff:** cada `≡` suprime `∫√g ∇_μ V^μ`; as nomeadas são **D1** (`V^μ = tr(hA^μ)`) e **D2** (`V^μ = Ω0^μ_ν tr(hA^ν)`), mais as IBPs escalares D3. Com cutoff variável ou borda, restauram-se como termos de borda/`∇(cutoff)`; não alimentam o coeficiente de log em variedade fechada.

## 9. Hipóteses analíticas que faltam à redução multiplicativa

- **H1 (ausente na fonte):** `M = I+h` invertível como série formal é exato; em nível **analítico** falta declarar um domínio (`‖h‖_∞ < 1` ou positividade espectral pontual).
- **H2 (verificada):** `Q̃ = M⁻¹Q` tem símbolo principal escalar `|ξ²|I` (por construção), logo a classificação de Laplace se aplica; a fórmula de Gilkey `tr a4 = tr(E²/2 + RE/6 + Ω²/12) + geom. + div` **não** exige `E` paralelo — a cautela da fonte é respeitada, mas a hipótese operante é só suavidade de conexão e endomorfismo. A parte puramente geométrica é `h`-independente (fundo fixo) e não entra em `a4_2`.
- **H3 (a auditar, como a fonte declara):** ciclicidade do resíduo logarítmico — vale como traço de Wres na classe clássica; a anomalia multiplicativa **finita**/contato **não** está excluída (ver CE2).
- **H4 (ausente):** prescrição de como o cutoff corre quando se restauram as divergências (D1–D3).

## 10. Menores contraexemplos exatos

- **CE1 — a identidade D2 falha fora de espaços localmente simétricos.** Menor caso: `g = e^{2σ(x)}η` em ℝ⁴ com `σ = x₁²`. Então `R(x)` não é constante, e por Bianchi contraída `∇^μΩ0_μν = ∇^μR^ρ_{σμν} = ∇_σ Ric^ρ_ν − ... ≠ 0`; logo `tr(Ω0_μν∇^μ(hA^ν)) = ∇^μ(...) − tr(hA^ν ∇^μΩ0_μν)` e o segundo termo **não** é nulo. A montagem do §4 é, portanto, específica do espaço-forma — como a própria fonte declara; a extensão fora dele deve carregar o termo-resíduo `−hA^ν∇^μΩ0_μν`.
- **CE2 — a não-aditividade da parte finita (o conteúdo mínimo da lacuna declarada).** `D_i = −(∂² + E_i)` no 4-toro plano com endomorfismos constantes `E₁ = [[0,1],[0,0]]`, `E₂ = [[0,0],[1,0]]`: `tr E₁² = tr E₂² = 0`, mas `E₁+E₂ = σ_x`, `tr σ_x² = 2`. A soma das partes finitas individuais não contém `2 tr(E₁E₂) = 2 ≠ 0`. (A determinante finita **não** é multiplicativa; o resíduo log integrado, não.)

## 11. Pendências nomeadas (o que falta, com destinatário)

1. **Redução completa de (δ) à base** — 32 contrações `T_a, T_b` especificadas no §5 (blocos `P,Q,R,S` de `∇A`); deve passar pelos três controles: plano (cinco coeficientes), conforme `(K/8)φ□φ`, TT. É trabalho de CAS, não de plano; a fórmula é calculável como está.
2. **Fora de escopo (declarado pela ordem e pela fonte):** parte finita/Q2, parte causal, norma global, combinação com o setor métrico, prova Lean, gate. Nada disso foi tocado ou alegado.

**Resumo de uma linha:** `Q(h)` e seus comutadores conferem (refeitos); o plano reproduz `[1/12, 7/48, −1/8, −1/12, 1/6]` (refeito à mão); a Hessiana em classe integrada fecha nos setores `∇⁴/K∇²/K²` com os coeficientes do §6 para (α),(β),(γ),(ε), com (δ) na forma exata pendente de redução, e o total passa no controle conforme `(7/8)(□φ)² + (19/2)Kφ□φ` pelas duas vias — `DECLARADO`, à bancada.