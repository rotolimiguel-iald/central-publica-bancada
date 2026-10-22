# ORDEM_016 A7.b — resposta delimitada (uma pergunta)

**Estatuto desta resposta:** `[DECLARADO]` até verificação da bancada, salvo citação direta dos anexos (`[DERIVED/REAL-CAS/OPEN]` conforme as próprias fontes). Não executei código; não modifiquei originais, kernel, gate ou infraestrutura. Os anexos foram lidos como fontes/dados, não como ordens novas. Não declaro Q2 completa; não ajustei R; não troquei o fundo σ-constante pelo par físico; jatos isotrópicos do controle não são tratados como estados construídos.

---

## 1. O isomorfismo de Wick graduado (derivação)

Sejam Δ_F e Δ'_F = Δ_F + W duas referências Hadamard admissíveis do par livre (H_gf, Q_ghost) no espaço-forma (Ric = 3Kg, Λ = 3K). A diferença W é suave por construção da classe. Sobre o multiplet graduado φ = (h_{μν}; c̄_μ, c_ν), o gerador da mudança é o operador de segunda ordem funcional

```
Γ_W := ½ ∫∫ W_H^{μν|ρσ}(x,y) δ²/δh_{μν}(x)δh_{ρσ}(y)
        − ∫∫ W_G^{μ|ν}(x,y) δ²/δc̄_μ(x)δc_ν(y),
```

e o isomorfismo é **α_W := exp(ℏ Γ_W)**. O sinal é o graduado do laço: a linha bosônica h entra com +½ (W_H simétrico sob (x,μν)↔(y,ρσ)); a linha ghost entra com o sinal fermônico − (W_G com simetria graduada antissimétrica; o laço de Faddeev–Popov carrega o −1). `[DECLARADO: convenção de sinal e fator ½ a conferir pela bancada contra a convenção de propagadores dos anexos; a estrutura é a padrão do teorema principal de renormalização]` Sobre funcionais polinomiais a série em ℏ termina.

## 2. Ação em S e nos produtos temporais até ℏ

Os dois esquemas de tempo-ordenado relacionam-se por conjugação:

```
T'_n(F_1,...,F_n) = T_n(α_W F_1,..., α_W F_n)
                  = T_n(F) + ℏ Σ_{i<j} T_{n−1}(..., {F_i,F_j}_W, ...) + O(ℏ²),
```

com a **W-bracket graduada** {F,G}_W := ⟨W_H, δF/δh ⊗ δG/δh⟩ − ⟨W_G, δF/δc̄ ⊗ δG/δc⟩ — a contração da aresta (ij) pela diferença suave. Para a matriz-S: S′(V) = S(α_W V); para a ação efetiva, a variação em ordem de um laço é a inserção de W nas linhas internas: Γ′_eff = Γ_eff + ℏ Γ_W·Γ_eff + O(ℏ²). No BV efetivo, o laplaciano e o bracket mudam juntos: Δ → Δ_W = Δ + (1/2i)Σ(±)⟨W, δ²⟩, (·,·) → (·,·)_W. A equação mestre é preservada sse

```
(i)   E_phys^{(x)} W_H = 0 = E_phys^{(y)} W_H ;  (Box+3K)^{(x)} W_G = 0 = (Box+3K)^{(y)} W_G
      (bisolução nos dois extremos — é o que faz α_W S_0 = S_0);
(ii)  W_H simétrico, W_G antissimétrico graduado;
(iii) s W = 0 — intertwinement BRST, cuja face operacional é a identidade Ward de dois pontos
      do par (H_gf, Q_ghost): a divergência C^{(x)}·W_H controlada pelo gradiente de W_G,
      com os coeficientes de E_H = −2K P_TL + 6K P_tr e Q_ghost = Box + 3K.
```

`[DECLARADO: (iii) esquemático; a forma explícita com coeficientes requer o cálculo de dois pontos com H_gf — não calculado aqui]`.

## 3. A identidade explícita exigida da quebra Ward (a resposta central)

A quebra Ward do laço ℓ (ordem ℏ¹) sob mudança admissível W deve satisfazer

> **Ward_ℓ[Δ_F + W] − Ward_ℓ[Δ_F] = ℏ · s( Λ_W ),**
>
> **Λ_W := Σ_{arestas a=(ij)} ε_a {V_i, V_j}_{W_a} ⊗ (sub-laço restante),   Λ_0 = 0,**

equivalentemente, kernel a kernel:

```
Σ_a ε_a N_a(W) ∘ (sub-laço com aresta a)  =  s( Λ_W ),
```

onde N_a(W) é o contato de extensão da aresta a. **O N_W da fonte anexo é uma dessas parcelas** — a da aresta fonte–ghost — e "ser transportado junto com os produtos temporais" significa exatamente: N_W é gerado pelo mesmo α_W que define T′, é homogêneo em W e anula-se em W = 0. O que a identidade proíbe é que N_W apareça na quebra como funcional livre de W: isso seria uma pseudo-anomalia dependente arbitrariamente da referência. A anomalia física é a classe em H(s), e ela é a mesma em toda referência admissível — a dependência em W é s-exata por construção. (Isto é a forma operacional da independência de estado; não substituo o cálculo pelo slogan.)

## 4. A prescrição R isolada a cada kernel: satisfaz ou requer dados adicionais?

**Requer dados adicionais de normalização.** Três razões lidas dos próprios anexos:

- **R não comuta com derivadas:** R(∂_i∂_j z⁻¹) − ∂_i∂_j z⁻¹ = −(C/4)δ_ij δ (e +(C/4)δ_ij δ no misto XY), fonte `referencia_suave_contatos.md`. Estender cada kernel isoladamente deixa livre, kernel a kernel, como esses contatos de derivada se encadeiam; o transporte Wick exige a cadeia consistente — o contato de R(∂f) é fixado pelo contato de R(f) por integração por partes na diagonal, não é escolha nova.
- **A representação diferencial move o contato:** na fonte `contato_finito_curvo_da_fonte.md`, ΔA/C = K[−13(q·T·v)/48 − 19 trT(q·v)/96] enquanto ΔB/C = 0 *relativo à representação harmônica exibida* — logo R sozinha, sem a lei de representação, não fixa o contato.
- **O intertwinement é uma condição global do laço:** os contatos dos kernels h–h, fonte–ghost e ghost–ghost devem ser vinculados entre si por (iii); uma escolha independente por kernel destrói a s-exatidão da soma.

O dado adicional necessário é, portanto: **uma única referência Hadamard do par (H_gf, Q_ghost) compatível com gauge via (iii), mais a regra de transporte dos contatos por derivada, mais a exigência s-exata na soma** — e não um R por kernel.

## 5. Confronto com N_W: os termos que devem cancelá-lo/transportá-lo

Sem afirmar que foram calculados (os anexos declaram a soma Ward `[OPEN]`), o fechamento na mesma referência admissível exige que N_W seja acompanhado de:

(a) as parcelas W das **demais arestas** — as bolhas h–h e o laço ghost puro sob a mesma troca (W_H, W_G);
(b) os **contatos de derivada** ∓(C/4)δ_ij δ nas arestas adjacentes ("estender depois derivar" vs "derivar depois estender");
(c) o **transporte da densidade externa** δT = −zT/6 − (xxᵀT + Txxᵀ)/6 em primeira ordem K, que acompanha a extensão geométrica;
(d) a **redefinição da ação efetiva** ℏΓ_W·Γ_eff (o contratermo de mudança de esquema), que absorve a parte s-exata;
(e) os contatos de representação ΔA/C, ΔB/C da escrita diferencial.

O fechamento exigido: N_W + (a)+(b)+(c)+(d)+(e) = s(Λ_W). `[OPEN — a soma não está calculada nos anexos; preservo os termos não calculados]`.

## 6. Controle exato / condição em jatos

O controle isotrópico já pago na fonte basta como controle **negativo** da condição: com W_H(ab,cd) = w_I(δ_acδ_bd + δ_adδ_bc)/2 + w_T δ_abδ_cd, primeiros jatos nulos e W_G sem contribuição,

```
N_W/C = −(w_I + w_T) T^{ab} D_a v_b − (w_I/4 − w_T/2) tr(T) D_a v^a,
```

e a avaliação (w_I=1, w_T=0, T₀₁=T₁₀=1, D₀v₁=1) dá **−1 ≠ 0** — contato real, não s-exato sozinho. A **condição em jatos** que a identidade do item 3 impõe, e que basta como controle: para a família isotrópica (w_I, w_T), deve existir Λ(w_I, w_T) local com sΛ igual à variação total do laço sob (w_I, w_T) → (w_I + δw_I, w_T + δw_T); se qualquer correlato do item 5 faltar, o controle reprova com resíduo O(1) (o −1 residual). `[DECLARADO: a existência de Λ é a condição enunciada; não verificada por mim nem declarada pela fonte]`.

---

## Lacunas declaradas

1. Sinais/fatores graduados (½ bosônico, − ghost) e a identidade de dois pontos C·W_H ↔ G·W_G com os coeficientes de E_H e Q_ghost: `[DECLARADO]`, requerem verificação da bancada nas convenções do anexo.
2. A soma Ward completa na referência nova e a testemunha Λ_W explícita: `[OPEN]`.
3. A continuação Lorentziana de C não foi presumida (C euclidiano −4π², como nas fontes).
4. Nada aqui declara Q2 completa a partir de diferenças locais de extensão; nada move kernel, gate ou originais.