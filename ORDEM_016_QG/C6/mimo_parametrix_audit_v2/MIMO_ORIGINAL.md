# MEMÓRIA CIENTÍFICA — UNIDADE C6 (ORDEM_016, Parte C)
## Operador de Euler densitizado sobre a PRIMEIRA linha métrica `H_ab,cd(x,y)` de `bilocal_first_curvature_engine.metric`, ordem‑K nas duas pontas

*(Nova unidade C6, iniciada após a falha terminal de MiMo46f `transverse_cocycle`. Não é retry dela. Uma pergunta por unidade: esta unidade responde só à pergunta do operador de Euler sobre a primeira linha.)*

---

## 0. Regime, fontes e proibições observadas

- **Texto somente. Sem execução alegada.** Nada foi rodado, compilado, medido ou casado por CAS nesta unidade. O que segue é **derivação analítica** a partir dos três arquivos‑fonte entregues: `bilocal_first_curvature_engine.py`, `bilocal_covariant_jet_engine.py`, `bilocal_vector_euler_zerojet.py`. [DERIVED]
- **Sem originais, sem gate.** Nenhum arquivo foi tocado; nenhum original reescrito; nenhum gate movido.
- **H0 e H1 intocados.** `metric(0,·)` e `metric(1,·)` são a fonte; **nenhum coeficiente foi ajustado** (S1, o `d1`, o `1/4` e o `1/2·L` permanecem como publicados). [SOURCE]
- **Convenções:** auxiliar **euclidiano 4‑D, espaço‑forma, K constante**; carta RNC centrada em O; **y mantido até o fim de todas as derivadas**; **assinatura física não inferida**. Sem ghostWick novo, sem vértice novo, sem loop completo.
- **Q2 não é completada** e **nenhuma partição é escolhida** (a partição “qual H” segue em aberto). A prescrição parcial corrente segue sendo **R_bal + sua correção de compatibilidade com linha suave**; **não misturo com Rraw** e **não presumo família causal completa**.

---

## 1. Convenções e objetos [SOURCE]

Numa carta RNC em O, para espaço‑forma de curvatura constante K:

```
R_abcd = K(g_ac g_bd − g_ad g_bc);   R_ab = 3K g_ab;   R = 12K      (curvatura escalar)
Γ^c_ab(x) = −(K/3)(x_a δ^c_b + x_b δ^c_a − 2δ_ab x^c)
g_ab(x) = δ_ab − (K/3)(xx δ_ab − x_a x_b)  ⇒  g^ab(x) = δ^ab + (K/3)(xx δ^ab − x^a x^b)
√g(x) = 1 − (K/2)xx + O(K²)
```

Bilocal: `z = x − y`, `w = z·z`, `L = log w`; `xx = x·x`, `yy = y·y`, `xy = x·y`.
Os coeficientes geométricos do engine estão escritos com **K = 1**; repor K significa multiplicar `gX1`, `gY1`, `P1`, `distance1` por K, e o potencial do operador carrega K explicitamente. A verificação é **homogênea de primeira ordem em K**.

Linha métrica publicada (índices (a,b) na ponta X, (c,d) na ponta Y):

```
H⁰_ab,cd = S_ab,cd / w ,            S = ½(δ_ac δ_bd + δ_ad δ_bc − δ_ab δ_cd)
H¹_ab,cd = S1/w − d1·S/w² + ¼ S + ½ L δ_ab δ_cd
S1 = ½[lower1_ac δ_bd + δ_ac lower1_bd + lower1_ad δ_bc + δ_ad lower1_bc − gX1_ab δ_cd − δ_ab gY1_cd]
lower1 = gX1 + P1;   d1 = −(K/3)(xx·yy − xy²)
```

---

## 2. O candidato, escrito por inteiro (X‑end, linha (a,b))

O candidato do operador é `√g[□h_ab − 2K h_ab + 2K g_ab tr(h)]`, **com duas conexões covariantes em cada ponta**. Expanso em coordenadas, ele lê:

```
E_cand[h]_ab = √g(x) {  □ h_ab
   + (K/3)(xx δ^ij − x^i x^j) ∂_i ∂_j h_ab          ← inversa métrica (correção de O(K))
   − (2K/3) x·∂ h_ab                                 ← Γ^k_ij ∂_k (slot de DERIVADA)
   + (2K/3)( x_a ∂^m h_mb + x_b ∂^m h_am )          ← Γ nos slots de ÍNDICE
   − (4K/3) x^m( ∂_a h_mb + ∂_b h_am )               ← Γ nos slots de índice (2ª parte)
   + (4K/3) h_ab                                     ← ∂_j Γ^m_ia h_mb + ∂_j Γ^m_ib h_am
   − 2K h_ab + 2K g_ab g^ef h_ef }                   ← POTENCIAL
```

**Duas conexões em cada ponta** = (i) a cadeia de derivadas (`Γ^k_ij ∂_k` e o `∂Γ` da segunda derivada), (ii) os slots tensoriais (`Γ^m_ia h_mb`). Na ponta Y o mesmo vale com a regra da cadeia `∂/∂y_j = ∂/∂y_j − 2z_j(∂_w + ∂_L/w)` (sinal −).

**Termos de conexão (explícitos):**

```
δ^ij Γ^k_ij = 2K x^k                     → −2K x·∂
δ^ij Γ^m_iμ = −(K/3)(x^j δ^m_μ + x_μ δ^mj − 2δ^j_μ x^m)
δ^ij ∂_jΓ^m_iμ = −(2K/3) δ^m_μ           → +(2K/3)h_μν por slot, +(4K/3) no total
```

**Curvatura e potencial:** `R = 12K`, `R_ab = 3K g_ab`. O potencial do candidato é **exatamente** `2 R_{a c b d} h^{cd} = 2K(g_ab tr h − h_ab) = −2K h_ab + 2K g_ab tr h`. Não é o Lichnerowicz (que daria `−8K h_ab + 2K g_ab tr h`).

---

## 3. A ordem correta: **derivar e depois ancorar**

1. `w` e `L` são auxiliares: `∂/∂x_j → ∂/∂x_j + 2z_j(∂_w + ∂_L/w)`, `∂/∂y_j → ∂/∂y_j − 2z_j(∂_w + ∂_L/w)` (é o que `B.derivative` implementa).
2. **Todos** os jets (X e Y) saem com y independente.
3. Só depois se ancora: `y → 0`, `w → xx`, `L → log xx`.
Ancorar antes é o erro: perde‑se o setor `x∧y` (de `P1` e `lower1`) e o setor `d1`, e o resíduo deixa de ser o mesmo. Esta unidade fez **derivar → ancorar**.

---

## 4. A verificação, em quatro blocos [DERIVED]

Com `□H⁰ = 0` fora da diagonal (`□(1/w) = 0` em 4‑D), a equação de O(K) é `□H¹ + [operador O(K)]H⁰ = 0`.

Identidades‑chave usadas:

```
□S1 = −2S                                     (exato: □lower1 = −δ, □gX1 = −2δ, □gY1 = 0)
□d1 = −2yy ;  z·∂d1 = 2d1 ;  □(1/w²) = 8/w³ ;  □(log w) = 4/w
xx·w − (x·z)² = xx·yy − (x·y)² = −3d1
```

**(a) `□H¹`:** `= −2S/w − 4(z·∂S1)/w² + 2yy S/w² + 8 d1 S/w³ + 2 δ_ab δ_cd /w`.
**(b) estruturas bilocais** (inversa métrica + conexões): os termos `1/w³` **cancelam identicamente** (`8d1 + (8/3)(xx w − xz²) = 0`); os termos `1/w²` dão `2yy − 2xx + 4xz = 2w` ⇒ `+2S/w`; **todas as estruturas `x∧y` cancelam exatamente** entre as conexões de índice e `z·∂S1` (usa `z∧x = x∧y`).
**(c) conexões de índice (termo constante):** `+(4/3)S/w`.
**(d) potencial:** `−2δ_ab δ_cd /w − 2S/w`; **`−2δδ/w` cancela exatamente `+2δδ/w` vindo do log `½L δ_ab δ_cd`.**

Saldo da estrutura `S/w`: `−2 (□S1) + 2 (estruturas) + 4/3 (índices) − 2 (potencial) = −2/3`.

---

## 5. Veredito: **o candidato diverge**. Resíduo

> **`E_cand[H]_ab,cd(x,y) = −(2/3) K S_ab,cd / w = −(2/3) K H⁰_ab,cd`, para todo `x ≠ y`, em O(K).**

O resíduo é **puro e exato**: não há resto `x∧y`, não há resto `δδ`, não há resto `1/w³`. A estrutura é exatamente a linha de ordem zero. Testado por derivação em três componentes independentes, com o mesmo número: `(01;01)`, `(00;00)`, `(11;11)` em `y = 0`, `x = t e₀` dão todos `−K/(3t²)`.

**Origem (sem alterar a fonte):** o desequilíbrio está **no coeficiente do termo `h_ab` do potencial**. O `S1` publicado força `□S1 = −2S`; o log `½L` e o termo de traço `+2K g_ab tr h` fecham **exatamente** entre si (é a evidência interna de que **a parte de traço do candidato e o coeficiente `½` do log estão certos**); sobra `−(2/3)K S/w`, que é a diferença entre `−2K h_ab` (candidato) e o que a linha publicada exige. Equivalentemente: a linha publicada é parametrix de

```
√g[ □ h_ab − (4/3)K h_ab + 2K g_ab tr(h) ]      (candidato + um termo +(2/3)K h_ab)
```

Isto é **afirmação sobre o operador**, não sobre H. **Nenhum coeficiente de H0/H1 foi alterado para zerar o resíduo** — o resíduo fica registrado como está.

---

## 6. Controle não diagonal que rejeita sinal errado

Configuração **fora da diagonal**: `y = 0`, `x = t·e₀`, `t ≠ 0` (`w = t²`). Dois componentes separam os setores:

| componente | `S_ab,cd` | `δ_ab δ_cd` | lê | valor com o candidato | com `-4K/3` | com sinal do TRAÇO trocado | com sinal do LOG trocado |
|---|---|---|---|---|---|---|---|
| `(01;01)` | `½` | `0` | só `S` | `−K/(3t²)` | `0` | `−K/(3t²)` (inalterado) | `−K/(3t²)` |
| `(00;11)` | `0` | `1` | só `δδ` | `0` | `0` | **`+4K/t²`** | **`−4K/t²`** |

- `(00;11)` **isola o setor do traço** (`S = 0` ali): qualquer sinal errado em `+2K g_ab tr(h)` ou em `½L` produz `±4K/t²` — recusa inequívoca.
- `(01;01)` **isola o setor `S`** (`δδ = 0` ali): qualquer sinal errado no termo `h_ab`, nas conexões ou na inversa métrica muda o número.
- **Atenção à cegueira de `y = 0`:** em `y = 0` o setor `x∧y` é invisível. Para rejeitar sinal de **conexão** é obrigatório um controle com `y ≠ 0` (p.ex. `x = t e₀`, `y = s e₁`), onde o resíduo deve continuar **exatamente proporcional a `S/w`** e nada mais. Qualquer sinal errado em `Γ`, `∂Γ` ou nos coeficientes `a₂/a₃` de `lower1` deixa ali estruturas `x∧y` — é o teste que a ancoragem sozinha não faz.

---

## 7. O que esta unidade **não** afirma / lacunas

- **[PENDENTE]** verificação por CAS/pipeline do polinômio expandido; a derivação acima é analítica e não traz execução nem número de máquina.
- O operador **na ponta Y** (segunda linha (c,d), com `∂/∂y` e o sinal da regra da cadeia) **não foi derivado aqui** — uma unidade por pergunta. De qualquer modo, o resíduo da ponta X já impede o fechamento da equação da primeira linha.
- `√g` **não é testável fora da diagonal** nesta ordem: `H⁰` é harmônico, logo `√g·E = E + O(K²)`; a densitização só entra na diagonal/fonte, que esta unidade não toca.
- Não se infere assinatura física, não se mistura com `Rraw`, não se presume família causal completa, não se completa Q2, não se escolhe partição.
- Nenhum gate, selo, original ou arquivo foi alterado. `NOT_FALSIFIED` não é `CONFIRMED`; nada aqui é confirmação.

**Fecho da unidade C6:** *o candidato `√g[□h_ab − 2K h_ab + 2K g_ab tr(h)]` **não** satisfaz o parametrix fora da diagonal com a `S1` e o log publicados; o resíduo é exatamente `−(2/3)K H⁰_ab,cd`, de origem no coeficiente do termo `h_ab` do potencial, com o setor de traço/log fechando exatamente.*