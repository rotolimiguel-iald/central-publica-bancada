# A-7.b — Exaustão dos jatos de W no contato da bolha mista singular/suave e na fonte BRST

**Estatuto da entrega:** só análise escrita; nenhum código executado nesta chamada; todos os números citados são **lidos** das fontes anexas. Resultado **DECLARADO** até auditoria local. Prescrição (extensão radial fixada, fatores −1/32, −métrica/2+ghost, C_E) **não modificada**; nenhum estado/horizonte físico escolhido; nenhum W é tratado como bisolução de Hadamard — W é jato suave arbitrário e a análise é ponto a ponto (micro)local. O contexto é o **euclidiano auxiliar plano 4D** do recorte; nada aqui é a construção lorentziana.

**Dados ausentes (declarados, não contornados):** os arquivos-base importados pelos motores anexos — `position_metric_bubble_engine.py` (`empty, lincomb, frob, sandwich, LABELS, BASIS, transpose, vertex_data, potential, green_integer, second_integer`), `position_metric_second_curvature_engine_v2.py`, `radial_covariant_second_jet_engine.py` — **não foram anexados**; suas assinaturas foram inferidas do uso. Os valores numéricos de `logarithmic_contact_engine.contact` para ordens ≥ 1 existem como função na fonte, mas não foram lidos aqui (não executo); o algoritmo abaixo os consome como INPUT da prescrição.

---

## 1. Resposta curta à pergunta única

Neste recorte — linha singular `D = 1/|X−Y|²` com **no máximo uma derivada em cada ponta** (`d_line ≤ 2`), **antes** de integrações por partes (`m_ext = 0`) — o contato de extensão recebe contribuição **apenas do jato de ordem 0 de W**, o valor na diagonal `W(Y,Y)`. Isto é **teorema** (grau de escala + fórmula de multiplicação de derivadas de delta), não truncamento: os jatos de ordem `p ≥ 1` têm coeficiente de contato **identicamente zero**, e há testemunha de que o corte é exato (§2, §8).

Os jatos de W existem e ficam **exaustos** (não "inexistentes"), com destinos nomeados:

1. **tangenciais** `∂_u^q W|diag` — reaparecem na identidade de Ward como derivadas do valor na diagonal (§5), sem subir a ordem de δ;
2. **transversais pares** `∂_v^{2k} W|diag` — entram somente em contatos de ordem `≥ 2`, fora do recorte (alcançados após `k` derivações na separação); o exemplo de §7 mora aqui;
3. **transversais ímpares** `∂_v^{2k+1} W|diag` — anulam **somente** na parte totalmente simétrica pontas×fibra; **não** anulam por componente nem no setor ghost direcionado; não podem ser zeradas por decreto (§4.3, §7);
4. todos os jatos entram na **parte finita** da extensão (que não é o contato).

---

## 2. A contagem mestra: teorema de exaustão dos jatos

**Setup.** `x = X − Y` (separação/transversal), `u = (X+Y)/2` (tangencial/diagonal), `z = |x|²`. A linha singular vive em
`D_jet ∈ { z⁻¹, ∂_{x_i}z⁻¹ = −2x_i z⁻², ∂_{x_i}∂_{x_j}z⁻¹ = −2δ_{ij}z⁻² + 8x_i x_j z⁻³ }`,
com `∂_{X_i} = ∂_{x_i}`, `∂_{Y_j} = −∂_{x_j}` (sinais já absorvidos no contato medido `C_E δij δ/4`, [INPUT]). Grau de escala: `sd(z⁻¹) = 2`, `sd(∂^d z⁻¹) = 2 + d`. Limiar logarítmico em 4D: `sd = 4`.

**Fatos de distribuições [KNOWN]** (Gel'fand–Shilov; grau de escala à la Brunetti–Fredenhagen): para núcleo quase-homogêneo de grau `s` em ℝ⁴,
- `s < 4`: extensão **única** (localmente integrável) — sem ambiguidade, **contato nulo**;
- `s = 4`: ambiguidade `∝ δ⁴` (ordem 0);
- `s > 4` inteiro: ambiguidade `= Σ_{|β| ≤ s−4} c_β ∂^β δ`.

**Fórmula de multiplicação de derivadas de delta [KNOWN]:** para φ suave,
`φ · ∂^β δ = Σ_{0≤α≤β} (−1)^{|β|−|α|} C(β,α) (∂^{β−α}φ)(0) · ∂^α δ`,
e o caso polinomial: `x^γ ∂^β δ = (−1)^{|γ|} β!/(β−γ)! · ∂^{β−γ}δ` se `γ ≤ β` componentwise, **0 caso contrário**.

**Teorema (exaustão) [DERIVED nesta unidade].** Seja o contato da linha pura `Σ_{β′} c_{β′} ∂^{β′}δ` (|β′| ≤ s−4). Então o contato de `W·D` (operações (i) e (ii) abaixo) é
`Σ_{β′} c_{β′} Σ_{α≤β′} (−1)^{|β′−α|} C(β′,α) (∂^{β′−α}W)|diag · ∂^α δ`,
e o **grau máximo exato de jato de W é `s − 4 = d_line + m_ext − 2`** (`m_ext` = derivações na separação aplicadas ao diagrama).

*Prova.* (a) *Cota superior:* Taylor `W(Y+x,Y) = Σ_p (∂_v^p W)(0,Y) x^p/p!`; o termo `p` tem grau efetivo `s − p`; para `p > s−4` é localmente integrável ⇒ extensão única ⇒ coeficiente de contato zero. (b) *Atingido:* `W = x^γ`, `|γ| = s−4`, dá `x^γ D` de grau 4, cuja ambiguidade `δ` tem coeficiente `∝ γ! c_γ ≠ 0` sempre que `c_γ ≠ 0`. ∎

**Consequência no recorte:** a linha pura medida tem só `c_0` (ordem 0): contato com W é `c_0 · W(Y,Y) · δ` — **jato máximo 0, exato**.

### Tabela de operações (grau máximo exato de jato de W)

| operação | sd efetivo | ordem máx de δ | **jato máx de W** | status no recorte |
|---|---|---|---|---|
| (i) `R(W·z⁻¹)` | 2 | — | nenhum (extensão única) | sem contato |
| (i) `R(W·∂_{x}z⁻¹)` | 3 | — | nenhum (extensão única) | sem contato |
| (i)/(ii) `W·(∂∂z⁻¹)` | 4 | 0 | **0** | contato medido; só `W(diag)` |
| (iii) `∂_v(W·∂∂z⁻¹)` | 5 | 1 | **1** | após 1 IBP / divergência de ponta |
| (iii) `∂²_v(W·∂∂z⁻¹)` | 6 | 2 | **2** | fora do recorte; §7 mora aqui |
| geral `d_line + m_ext` | `2+d+m` | `d+m−2` | **`d+m−2`** | exato (teorema acima) |

Nota: derivações **tangenciais** `∂_u` não aumentam `sd` (não tocam a linha); elas derivam os coeficientes — é por elas que derivadas de W reaparecem na Ward **sem** subir a ordem de δ (§5).

---

## 3. As três operações não são intercambiáveis — quantificado

- **(i) extensão do produto `R(W·D_jet)`** vs **(ii) produto com a extensão `W·R(D_jet)`**: neste recorte (`kmax = 0`) **coincidem**, porque o único jato admitido é o valor na diagonal, comum aos dois lados. Fora do recorte (`s > 4`), se a prescrição de extensão não preservar multiplicação por suaves, a diferença (i)−(ii) é ela mesma um contato com jatos até ordem `s−4` — a **medir**, jamais a assumir; a prescrição radial fixada do DERIVACAO é a referência e não foi alterada.
- **(iii) derivar a extensão do produto completo** `∂^m[W·R(D)]`: difere de (i)/(ii) pelo comutador `[∂^m, R]`, que é o contato de ordem superior — exatamente o objeto que `logarithmic_contact_engine.contact(n, ℓ, indices)` computa como `(R(D f) − D R(f))/C` para `f = z⁻ⁿ L^ℓ`. **É só por (iii) que jatos de W de ordem > 0 entram em contatos** (via a fórmula de multiplicação aplicada aos `c_{β′}`, `|β′| ≥ 1`, lidos dessa função).

---

## 4. Demonstração: o contato da bolha depende só de W na diagonal antes da divergência

**Afirmação.** Antes da extensão (antes da divergência), a diferença `R(W·D_jet) − W·D_jet` e a contração da bolha `<Jᵀ A_X W + Wᵀ A_X J, B_Y>` têm contato igual a `W(Y,Y) · (C_E δij/4) δ` — só o valor na diagonal.

**Prova (duas pernas).** (1) *Escala:* cada termo de Taylor `x^p`, `p ≥ 1`, reduz o grau para `4 − p < 4` ⇒ localmente integrável ⇒ extensão única ⇒ nenhuma ambiguidade/contato. (2) *Suporte:* o contato é suportado na diagonal (`∂^β δ`, aqui `β = 0`), e `x^p δ = 0` para `p ≥ 1`. Logo todo jato positivo de W tem coeficiente zero exato. ∎

**Escopo honesto (o que NÃO se afirma):** a **extensão completa** (parte finita incluída) depende de **todos** os jatos de W; só o **contato** (a anomalia local) é diagonal. Os coeficientes medidos do DERIVACAO (`W_I = (23/8, −13/16, 1, −2)`, `W_T = (3/4, −3/8, 1/2, −1)`, `W_G = (0,0,0,0)`; resíduo `N_bolha G + E R_W`; primitiva `N_eff`) são **[INPUT]** e permanecem intactos — a exaustão **não os toca** e nenhum coeficiente será escolhido para anulá-los.

### 4.3 Sobre "derivadas transversais ímpares" — a regra correta

Para W hh com simetria total pontas×fibra (`W_{ab,cd}(X,Y) = W_{cd,ab}(Y,X)`):
`∂_v^{2k+1} W_{ab,cd}|diag = −∂_v^{2k+1} W_{cd,ab}|diag` — anula **somente** na parte simétrica sob `(ab)↔(cd)`. Componentes com assimetria de fibra **podem ser não nulas**. No ghost (direcionado, transposição da segunda ponta — `ghost_direct_position_engine.direct_node`, `transpose(BY)`), a regra de pontas conjuga com a transposição de fibra (e o sinal grassmanniano); `∂_v W_G|diag` **não anula** por componente. **Conclusão operacional:** jatos transversais ímpares são **retidos** na exaustão e zerados — quando for o caso — por **projeção de simetria explícita e medida**, nunca por pressuposição.

---

## 5. Como as derivadas de W reaparecem na identidade de Ward

Escreva `c := C_E δij/4` (constante) e o funcional de contato `C[W](u) = c·W(u,u)`. Divergência na ponta X, direção k — os dois lados:

**Lado "derivar a extensão"** (Leibniz na ponta):
`∂_{X_k}[c W(diag) δ] = c[(∂_{v_k} + ½∂_{u_k})W](diag)·δ + c·W(diag)·∂_{v_k}δ`.

**Lado "estender a divergência"** `∂_{X_k}(W·D) = (∂_{X_k}W)·D + W·(∂_{x_k}D)`:
- contato de `(∂_{X_k}W)D` = `c·[(∂_{v_k}+½∂_{u_k})W](diag)·δ`;
- contato de `W·∂_{x_k}D`: a linha derivada tem contato `c·∂_{v_k}δ` (lido da prescrição via `contact`), e a fórmula de multiplicação dá `W·c∂_{v_k}δ = c·W(diag)∂_{v_k}δ − c·(∂_{v_k}W)(diag)·δ`.

Soma: `c[½∂_{u_k}W](diag)δ + c·W(diag)∂_{v_k}δ + c(∂_{v_k}W)(diag)δ − c(∂_{v_k}W)(diag)δ` — **idêntico ao outro lado**.

**Leitura:** as derivadas de W reaparecem **duas vezes com sinais opostos** — a `(∂_v W)δ` da Leibniz na ponta contra a `−(∂_v W)δ` da fórmula de multiplicação no contato da linha derivada — e esse cancelamento exato **é** a identidade de Ward no nível dos jatos. Para W hh simétrico o cancelamento é `0 − 0`; **no ghost direcionado os dois termos são não nulos e o cancelamento é conteúdo**, não tautologia. O remanescente físico é a derivada **tangencial** `½∂_u(W na diagonal)` — a derivada do valor na diagonal ao longo da diagonal. Em ordens superiores, o mesmo mecanismo com `c_{β′}`, `|β′| ≥ 1`, faz entrarem `∂^{β′−α}W|diag` pela fórmula.

---

## 6. Tabela finita de setores

Convenção: **D0** = valor na diagonal `W(Y,Y)`; **Tq** = `∂_u^q W|diag` (tangencial); **Rk** = `∂_v^k W|diag` (transversal). "Entra no contato?" refere-se a **este recorte** (`kmax = 0`).

| setor | bloco de fibra | simetria de pontas×fibra | D0 [INPUT] | T1 | R1 | R2 | entra no contato? |
|---|---|---|---|---|---|---|---|
| hh identidade | `W_I = (δacδbd+δadδbc)/2` | total | `(23/8, −13/16, 1, −2)` | Ward-1 (derivada da diagonal) | = 0 (projeção medida) | ordem-2, **fora do recorte** | **só D0** |
| hh traço | `W_T = δabδcd` | total | `(3/4, −3/8, 1/2, −1)` | idem | = 0 | fora | **só D0** |
| ghost `h†c` | `W_G = δab` (direcionado; `transpose` na 2ª ponta) | grassmann × transposição | `(0,0,0,0)` | 0 (diagonal nula) | **permitido ≠ 0** — fora do recorte | fora | D0 nulo medido; R1 só em ordem-1 |
| campo externo h (vértice) | jatos `∂^w A`, `\|w\| = 0,1,2` (`external_jets`) | — | `\|w\|=0`: matriz mista zero [INPUT] | — | — | — | `\|w\| ≥ 1`: **sem contato** (sd < 4) |
| derivações externas | `m_ext` na separação (Ward/IBP) | — | — | — | — | — | elevam ordem: ver tabela de operações, §2 |

---

## 7. Exemplo polinomial: o termo perdido ao substituir W por W(Y,Y) cedo demais

**Setor hh (simétrico):**
`W(X,Y) = W_0 + λ·[(X−Y)·V]²`, `λ, V` constantes, `W_0` escalar de fibra constante.
Simetrias: par em `v` ✓; fibra escalar ✓ (compatível com `W_I`, `W_T`). Jatos na diagonal: `W|diag = W_0`; `∂_{v_i}∂_{v_j}W|diag = 2λ V_iV_j`; ímpares e tangenciais nulos.
- Neste recorte: o termo `λ(v·V)²·∂∂z⁻¹` tem grau `4−2 = 2 < 4` ⇒ **coeficiente de contato zero exato** — substituir por `W_0` não erra o contato de ordem 0.
- **Onde se perde:** (a) na parte finita da extensão; (b) no contato de **ordem 2** (após duas derivações na separação), onde a fórmula dá coeficiente de δ `= 2λ·c_{ij} V_iV_j` (com `c_{ij}` o coeficiente de ordem 2 da linha, lido da prescrição). Um pipeline que substituiu `W → W(Y,Y)` reporta `0` aí — errado por `2λ c_{ij}V_iV_j`. Este é o controle C2 (§8).

**Setor ghost (transversal ímpar permitido):**
`W_G(X,Y) = γ·[(X−Y)·N]·δab`, com a regra ghost `W_G(X,Y) = −W_G(Y,X)^T` ✓ (ímpar em `v`, antissimétrico com transposição). Jato `∂_{v_i}W_G|diag = γ N_i ≠ 0`. Entra no contato de ordem 1 como `−γ N_i·δ` via fórmula — um pipeline que zerasse transversais ímpares "por simetria" o mataria. Este é o controle C3.

---

## 8. Algoritmo finito (pseudocódigo) — sem escolher coeficientes para anular resíduo

```text
função JATOS_W_QUE_CONTRIBUEM(d_line, m_ext, setor, W_jatos):
    # W_jatos: jatos de W na diagonal, como tensores de fibra, indexados por (γ_v, γ_u)
    # d_line ≤ 2 neste recorte (uma derivada por ponta); m_ext = derivações na separação
    s    ← 2 + d_line + m_ext
    kmax ← s − 4
    se kmax < 0: retornar EXAUSTO_VAZIO        # extensão única; contato ≡ 0 (teorema §2)

    C ← CONTACT_LINE(d_line + m_ext)           # {β ↦ c_β}: LIDO da prescrição fixada
                                               # (logarithmic_contact_engine.contact;
                                               #  âncora de ordem 0: C_E δij/4 [INPUT])
    contrib ← mapa_vazio
    para β com |β| ≤ kmax e c_β ≠ 0:
        para α ≤ β (componentwise):            # fórmula de multiplicação [KNOWN]
            γ ← β − α                          # jato de W que multiplica ∂^α δ
            contrib[γ][α] += (−1)^(|β|−|α|) · binom(β,α) · c_β

    contrib ← PROJEÇÃO_DE_SIMETRIA(contrib, setor)   # MEDIDA, nunca pré-zero:
        # hh: projeta na parte simétrica pontas×fibra (mata |γ_v| ímpar na projeção)
        # ghost: RETÉM |γ_v| ímpar; aplica transposição da 2ª ponta e sinal grassmanniano
    retornar contrib                            # jatos até |γ| = kmax: EXAUSTO (§2)

CONTROLES (fail-closed; qualquer falha ⇒ REFUSED, nada emitido):
  C1: W ≡ W_I constante, kmax=0 ⇒ reproduz (23/8, −13/16, 1, −2) [INPUT; âncora]
      (e W_T ⇒ (3/4, −3/8, 1/2, −1); W_G ⇒ (0,0,0,0))
  C2: W = W_0 + λ(v·V)²:  kmax=2 ⇒ coef. de δ = 2λ·c_{ij}V_iV_j;  kmax ≤ 1 ⇒ 0 exato
  C3: ghost W_G = γ(v·N)δab, kmax=1 ⇒ coef. de δ = −γN (transversal ímpar RETIDO)
  C4: W com jato puro de ordem kmax+1 ⇒ todos os coeficientes 0 (testemunha da exaustão)
  C5: troca de pontas × fibra ⇒ relação de sinal do setor (hh simétrico; ghost transposto)

PROIBIÇÕES: nunca editar c_β nem o resíduo medido (N_bolha G + E R_W) para forçar
anulação; nunca truncar jatos "por simetria" fora da PROJEÇÃO_DE_SIMETRIA; nunca
exigir de W equação de onda/bisolução de Hadamard.
```

Ancoragem nos anexos (sem execução alegada): a mecânica de jatos com denominadores fatoriais (`external_jets`, `ordered_node`, `direct_node`) é a mesma estrutura de Taylor aqui exigida para W; `differentiated`/`residue`/`contact` fornecem os `c_β` de ordem superior como INPUT da prescrição.

---

## 9. Estatutos e pendências

- **[KNOWN]:** teoria de extensão de distribuições homogêneas e a fórmula de multiplicação de derivadas de delta.
- **[DERIVED — nesta unidade]:** o teorema de exaustão (jato máximo exato `= d_line + m_ext − 2`; **0 neste recorte**), a diagonalidade do contato (§4), a conta de Ward que fecha (§5), as tabelas (§2, §6), os exemplos (§7), o algoritmo (§8).
- **[INPUT]:** prescrição fixada e todos os coeficientes medidos do DERIVACAO; os `c_β` de ordem ≥ 1 são função dos anexos, não recomputei.
- **[DECLARADO]:** toda a entrega, até auditoria local com os arquivos-base.
- **[OPEN — fora desta unidade]:** contatos de ordem ≥ 1 com vértices concretos após IBP; curvatura; Q2 completa; continuação lorentziana; a identidade de Ward completa da bolha nos vértices (aqui fixada no nível dos jatos). Nada aqui seleciona estado físico, move gate, ou fecha a QME.

**A linha de uma frase:** neste recorte o único jato de W com coeficiente de contato não nulo é `W(Y,Y)` — por teorema, não por truncamento; os demais jatos ficam exaustos e nomeados: tangenciais voltam na Ward como derivada da diagonal, transversais pares esperam contatos de ordem ≥ 2 fora do recorte, e transversais ímpares são retidos (o ghost os admite) até que a projeção de simetria medida decida.