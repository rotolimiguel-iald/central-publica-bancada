# A7.b — Transposição exata entre a referência diferencial harmônica e a referência principal P4(∂)R(U2)

**[DECLARADO até verificação da bancada · derivação manual sobre as duas entregas e os motores anexos · nenhuma execução alegada · nenhum original, kernel, gate ou infraestrutura modificado]**

Fontes lidas: `ENTREGA_016_A7b_contato_finito_curvo_da_fonte.md` (sha256 `acd1b98bbf52c1…`), `ENTREGA_016_A7b_contato_finito_principal.md` (sha256 `fc47164b1c8b1b…`), `finite_harmonic_extension_engine_v2.py`, `logarithmic_contact_engine.py`, `position_metric_ordered_operator_engine.py`. Prescrição única preservada: `R(u) = FP_a[(1−a)μ^{2a} z^a u]`, z = x·x, L = log(μ²z), μ > 0 fixa; `C_E = −4π²` (realização euclidiana auxiliar), `C = 4iπ²` (lorentziana, assinatura +−−−); `Res[z^{a−n}]/C = −□^{n−2}δ/[4^{n−1}(n−1)!(n−2)!]`. Fundo preservado: Model087, forma-espacial 4D, Ric = 3Kg, Λ = 3K, σ constante; **K é curvatura**, não κ nem gerador modular.

---

## 1. Resposta direta (o enunciado central)

As duas referências são **duas escritas da mesma extensão R(F)**, dentro da **mesma** R — e é só porque há uma só R que a transposição é exata. A relação é a identidade-mestra em três linhas:

```
R(F) = D_H + C·N_H(∂)δ                          (bloco harmônico)
     = X_P + D_rem + C·(N_P + N_rem)(∂)δ        (bloco dividido)
logo  D_H = X_P + D_rem      e      N_H = N_P + N_rem
```

com os objetos definidos na seção 2. A **lei da soma de Ward** que daí segue:

> **Para cada kernel, some os contatos UMA vez, numa única cisão: `Ward_par = C·(N_P + N_rem)(∂)δ = C·N_H(∂)δ`. É proibido somar `N_P + N_H` (dupla contagem da parte principal); é proibido apagar `D_rem` (apaga conteúdo não local fora da diagonal — em particular os numeradores de log anisotrópicos com média esférica nula, como o `6x0²−2x1²−2x2²−2x3²` do controle de B).**

A transposição (trocar de referência) **não** é a soma completa de Ward (seção 8): os contatos das outras bolhas, a inserção h*c, os jatos W e a fonte K² seguem pendentes e não entram nesta identidade.

---

## 2. Objetos, numa só R (convenção única de contato)

**Convenção de contato (a das duas entregas):** para todo operador D e kernel elementar f,
`R(D f) − D R(f) = C·N_D(f)(∂)δ`.

| objeto | definição | tipo |
|---|---|---|
| F = (F_A, F_B) | kernels reais da bolha antifield–ghost na 1ª ordem em K, com δT transportado e jatos covariantes ordenados | função com suporte singular em {0} |
| X_P := P4(∂) R(U2), U2 = z^{−2} | referência principal (não local, transversal: P(T,K_qv)=0); representa o log medido (ħP(∂)U2/(16π⁴), até termos locais; A0 = 1/(8π²)) | **[NL]** não local |
| N_P := N_{P4}(U2) | contato principal: `N[P] = −77P/240 − q²Lap_q(P)/80 + (q²)²Lap_q²(P)/5120` (coeficientes medidos: `['16039/57600','377/3600','-2371/28800','-6617/14400','539/2400']` [INPUT da entrega principal]) | **[L]** local |
| D_H, N_H | referência diferencial harmônica: `R(F) = D_H + C·N_H(∂)δ`, com `D_H = Σ_rows H_l(∂) R(z^{−b}L^r)` e `N_H = Σ_r v_r·harmonic_contact(H,b,r)` (motor v2) | D_H: **[NL]**; N_H: **[L]** |
| F_rem := F − P4(∂)U2 | resto fora da diagonal (função) | **[NL]** |
| D_rem, N_rem | representação harmônica do resto: `R(F_rem) = D_rem + C·N_rem(∂)δ` | **[NL]** / **[L]** |

Note a tipagem honesta: **"não local" = suporte fora de {0}** (carrega z^{−n}, L); **"local" = suporte em {0}** (derivadas de δ). `D_H` e `X_P` são **ambos** não locais; a cisão local/não local não é "harmônico versus principal" — cada referência tem as duas partes.

**Derivação da identidade-mestra (duas linhas):** pela linearidade de R (uma só R — um segundo regulador introduziria aqui um termo local não controlado, o que está proibido),

```
R(F) = R(P4(∂)U2) + R(F_rem) = X_P + C·N_P δ + D_rem + C·N_rem δ
     = D_H + C·N_H δ
```

e a decomposição de uma distribuição desta classe em "parte regular fora de {0}" + "parte suportada em {0}" é única, donde as **duas identidades de auditoria**:

- **(A-nd, fora da diagonal):** `D_H = X_P + D_rem` (vale como distribuições, portanto como funções fora de {0});
- **(A-loc, não-dupla-contagem):** `N_H = N_P + N_rem` (polinômios em q agindo sobre δ).

**Forma de transposição (T), com termos tipados:**

```
D_H − X_P = R(F_rem) + C·(N_P − N_H)(∂)δ
 [NL]       [NL]        [L: defeito local de transposição]
```

e, usando (A-loc), `N_P − N_H = −N_rem`, donde `D_H − X_P = D_rem` — a transposição fecha sem resto. No caso de concordância dos kernels (F_rem = 0), (T) reduz-se à identidade de contato puro `D_H − X_P = C·(N_P − N_H)(∂)δ`.

**Instanciação nos kernels reais (dados da entrega curva, não re-executados):**
`N_{H,A} = K[−13(q.T.v)/48 − 19 trT(q.v)/96]` (q = derivadas de δ; grau 1), `N_{H,B} = 0` **relativo à representação harmônica exibida** — o que não zera B nem seus logaritmos (ver seção 5). A atribuição de qual parte de P4 corresponde a A e a B é **dado a ler dos manifestos** — não se presume; o grau de cada bloco de contato (homogeneidade em q) é em si um teste de atribuição correta.

---

## 3. A lei da soma de Ward (sem dupla contagem, sem apagar o não local)

1. **Uma cisão por kernel.** Ou o bloco harmônico inteiro (`N_H`), ou a cisão principal+resto (`N_P + N_rem`). As duas são equivalentes por (A-loc); misturar as duas (`N_P + N_H`) conta a parte principal duas vezes.
2. **O não local fica inteiro.** O conteúdo não local do par é `X_P + D_rem`. `D_rem` carrega os canais que o símbolo não vê (seção 5) — apagá-lo muda o kernel fora da diagonal e quebra (A-nd); não é "termo local descartável".
3. **O defeito de transposição viaja junto.** Quem escreve R(F) primeiro numa referência e depois noutra deve carregar `C·(N_P − N_H)(∂)δ` (que é `−C·N_rem(∂)δ`); trocar de referência sem esse termo é uma terceira referência, não a mesma conta.
4. **Soma setorial:** `Ward_antifield-ghost = C·(N_P + N_rem)(∂)δ + C·N_{h*c} + C·N_{outras bolhas} + C·N_{jatos W} + O(K²)` — todas as parcelas após a primeira **pendentes** (preservadas como tal; ver seção 8).

---

## 4. Critério necessário para os dois kernels serem iguais fora da diagonal

Os kernels da classe (somas finitas de `z^{−n} L^r P(x)`, P polinomial) são iguais fora da diagonal **se e somente se** cada numerador polinomial coincide como polinômio — equivalentemente, pela decomposição de Fischer (a `harmonic_split` do motor):

> **(C1, necessário e suficiente):** para todo (n, r) e todo grau harmônico l, `H_l[num_{n,r}(F − F')] = 0`. Em particular, é **necessário** que se anulem todos os canais l ≥ 1 — que o símbolo não vê.
>
> **(C2):** a anulação do canal l = 0 (média esférica / símbolo logUV) é **necessária mas não suficiente** — contraexemplo na seção 5.
>
> **(C3):** a igualdade como distribuições exige ainda o casamento do termo local via (T): `N_H − N'_H = N_P − N'_P + …` conforme a cisão; e o espectro radial (expoentes n), o espectro de logaritmos (potências r — os canais ∂_a) e o numerador δT-transportado devem coincidir (sem δT, o controle T00=1, v=e0 desloca o contato por `47 q0/96` [INPUT da entrega]).

Controle cruzado já entregue e compatível: a rota esférica l=1, `ΔA/C = (K/8) Σ_i ⟨A_geom(n) n_i⟩_{S³} q_i`, reproduz os mesmos coeficientes — sinal de que o contato de A é exatamente o canal l=1 do seu numerador.

---

## 5. O que o símbolo P4 não determina: o dado que falta, e um contraexemplo explícito

**Dados faltantes (para identificar os dois kernels):**
- **(D1)** os canais harmônicos l ≥ 1 dos numeradores de cada L^r (a dependência angular completa em S³; equivalentemente o polinômio q completo por setor, não sua média angular);
- **(D2)** o numerador transportado δT;
- **(D3)** o espectro de potências de log (canais r, i.e., derivadas em a);
- **(D4)** os expoentes radiais n por canal (que fixam qual mapa Res se aplica);
- **(D5)** o conteúdo de jatos covariantes **ordenados** da perna ancorada — cujo contato **não é** o Taylor radial cru (guarda G3, seção 8).

**Contraexemplo (DECLARADO; contas mostradas para a bancada refazer).** Seja n(x) = 6x0² − 2x1² − 2x2² − 2x3² — o numerador de log do controle T00=1, v=e0 da entrega. É harmônico de grau 2 (Δn = 12 − 12 = 0) e de média esférica nula (⟨n⟩_{S³} = 6−2−2−2 = 0). Tome

`F₂ = F₁ + ε·n(x)·z^{−4}·L⁰`.

Os símbolos l=0 de F₁ e F₂ são idênticos; mas F₂ ≠ F₁ fora da diagonal, **e os contatos Ward diferem**. Pela regra dos motores (sem nova prescrição):

(i) identidade de funções: `∂_i² z^{−2} = −4 z^{−3} + 24 x_i² z^{−4}`, logo `n(∂) z^{−2} = 24·n(x) z^{−4}` (os termos z^{−3} cancelam porque n é harmônico), i.e. `n z^{−4} = (1/24) n(∂) z^{−2}`;

(ii) contato elementar pelas regras `differentiated`/`residue` (cálculo literal: para f = z^{−2}, L⁰, dois índices (i,i), realização euclidiana): `contact(2,0,(i,i)) = −(q² + 5 q_i²)/24` — derivação: termos `(3,(0⁴)): 2(a−2)` e `(4,(2,0³)): 4(a−2)(a−3)`; fatores 2 e −20; resíduos `−q²/32` e `−(q²+2q_i²)/192`; soma `q²/16 − 5(q²+2q_i²)/48 = −(q²+5q_i²)/24`;

(iii) combinando: `6·contact(2,0,(0,0)) − 2·Σ_{i=1..3} contact(2,0,(i,i)) = (5q² − 20 q0²)/12`, e com o coeficiente 1/24 da inversão:

`R(n z^{−4}) = (1/24)·n(∂) R(z^{−2}) + C·[5(q² − 4q0²)/288]·δ`.

Logo `ΔN = N(F₂) − N(F₁) = ε·5(q² − 4q0²)/288` — não nulo (e Lap_q-harmônico, como convém a um canal l=2). **Conclusão:** o símbolo P4 não distingue F₁ de F₂; o dado que falta é, aqui, o coeficiente do canal l=2 (ε) — em geral, todos os canais l ≥ 1, mais δT, os canais r e os expoentes n. E o efeito não é só fora da diagonal: **o contato Ward muda** — o bookkeeping de Ward fica subdeterminado sem os dados D1–D5.

---

## 6. Controle tensorial explícito não escalar (com traços) — forma-espacial 4D

Da entrega: a imagem covariante do contato, com o operador físico E (E G = 0; E(gf) = −2 Hess f + 2g□f + 6Kgf, sem substituição por operador gauge-fixado):

`ΔR(v)/C = −K[13 G(v) + 19 g div v]/96`
⟹ `T_μν(v) := [E ΔR(v)/C]_μν = (19K/48)·[∇_μ∇_ν(div v) − g_μν □(div v) − 3K g_μν div v]`

(consistência da passagem: `−K[0 + 19(−2 Hess + 2g□ + 6Kg)div v]/96 = 19K[Hess − g□ − 3Kg div v]/48` ✓). É um (0,2)-tensor — **não escalar**. **Traço:** `g^{μν}T_μν = −(19K/16)·[□(div v) + 4K div v]`. A parte livre de traço isola o componente Hessiano.

Duas amostras polinomiais (mesma disciplina da entrega; valores derivados à mão, DECLARADO):

| amostra | div v | T_μν | traço | parte livre de traço |
|---|---|---|---|---|
| v = ∇(x0³) | 6x0 | `−(57K²/8)·x0·g_μν` | `−(57/2)K² x0` | 0 |
| v = ∇(x0 x1 z) | 16 x0x1 | `T_01 = 19K/3`; `T_μμ = −19K² x0x1` (cada μ) | `−76K² x0x1` | só o componente 01: `19K/3` |

(Conferências: amostra 1 — `(19K/48)(−18Kx0)g_μν = −(57K²/8)x0 g_μν`, traço `4·(−57K²/8)x0 = −(57/2)K²x0` ✓ pela fórmula do traço; amostra 2 — `Hess_01(16x0x1) = 16`, `□(16x0x1) = 0`, `T_01 = (19K/48)·16 = 19K/3`, traço `−(19K/16)(64Kx0x1) = −76K²x0x1` ✓.)

A bancada deve computar o lado esquerdo (contato plano ΔA/C → movimentação funcional das derivadas de δ sobre o jato do ghost → completamento covariante) e o lado direito (álgebra covariante direta), exigindo igualdade **componente a componente** e as duas identidades de traço. Este controle testa, num só objeto não escalar: a transposição (a movimentação funcional), o mapa de covariantização e a ação de E.

---

## 7. Algoritmo simbólico mínimo (para a bancada executar nos motores entregues)

```
ENTRADA: F (kernel real, com δT, jatos ordenados), P4, U2 = z^-2.
 1. F_P  := P4(∂)U2                      # expansão simbólica exata
 2. R0   := F − F_P                      # resto (função), exato
 3. canais := harmonic_split de cada numerador de R0 (e de F, para auditoria)
 4. CRITÉRIO (C1): F == F_P fora da diagonal  ⟺  R0 == 0  ⟺  todos os canais nulos
    (listar os canais NÃO nulos = o dado que faltava, seção 5)
 5. (linhasH, N_H)  := represent(F)     # finite_harmonic_extension_engine_v2
 6. (linhasR, N_rem) := represent(R0)
 7. N_P := fórmula universal (−77/240, −q²Lap/80, +(q²)²Lap²/5120) aplicada a P4
 8. AUDITORIA A-loc: N_H == N_P + N_rem          (polinômios em q, por grau)
 9. AUDITORIA A-nd : D_H == X_P + D_rem fora da diagonal
10. GRAU: decompor por grau de q (N_{H,A} grau 1; N_P grau 4; restos compensam por bloco)
11. ZERO-SIMPLES: registrar toda linha com c(0)=0 em radial_inverse — coeficiente
    anulado fixado em zero APENAS na representação; o defeito local (T) pode morar aí
12. CONTROLE TENSORIAL da seção 6 (duas amostras; componentes + traços)
13. GUARDA G3: o contato da perna ancorada vem de ordered_node (IBP covariante
    ordenada); PROIBIDO substituí-lo pelo Taylor radial cru; registrar, não misturar
CONTROLE NEGATIVO (obrigatório): rodar F' = F + ε·n(x)·z^{−4} e exigir:
    critério REPROVA com canal l=2 reportado e ΔN = ε·5(q²−4q0²)/288.
SAÍDA: identidade (T) instanciada, termos [NL]/[L] tipados, N_P, N_rem, N_H,
       auditorias, flags. Tudo exato (racional), rc0 exigido, sem ajuste a Ward.
```

---

## 8. Guardas e delimitações (o que NÃO se afirma)

- **G1 — uma só R.** Nenhum segundo regulador físico; a transposição só é exata por linearidade da mesma R.
- **G2 — sem ajuste a Ward.** R não foi ajustada para impor Ward = 0; o fator (1−a) é mantido; coeficientes anulados por derivada são fixados em zero apenas na representação.
- **G3 — perna ancorada ordenada.** A IBP dos jatos da perna ancorada é covariante e ordenada; seu contato não é o Taylor radial cru.
- **G4 — fundo preservado.** Model087 (Ric = 3Kg, Λ = 3K, σ constante); não se troca pelo par físico. K é curvatura.
- **G5 — transposição ≠ soma completa de Ward.** Esta identidade organiza **apenas** a bolha do par. Seguem pendentes e preservados: contatos das outras bolhas, inserção h*c, jatos W, fonte K² (o termo K² de EΔR é a imagem deste contato K, **não** inclui uma fonte K² não calculada), curvaturas Kq²/K², aridades superiores, normalização multilinear T10/T11, fases BV lorentzianas (a calibração euclidiana não as fixa), e a atribuição A↔P dos manifestos. **Q2 não é declarada completa** a partir de uma diferença local de extensões.
- **G6 — não repetição.** Esta unidade não repete finite_two_point_ward_contact, curved_antifield_source nem a revisão de contratermo quadrático já enfileiradas.

## 9. Estatuto

**DECLARADO** — identidade, critério, contraexemplo e controles derivados à mão das duas entregas e das regras dos motores anexos, na mesma prescrição R e na mesma convenção de contato. Nenhum código executado nesta resposta; nenhum número novo medido; os coeficientes citados foram lidos das entregas. Veredito suspenso até a verificação da bancada (rc0 nos três motores, controle negativo mordendo, auditorias A-nd/A-loc fechando). Gate, kernel e originais intactos; nenhuma nova normalização adotada; os termos ainda não calculados permanecem de pé com seus nomes.