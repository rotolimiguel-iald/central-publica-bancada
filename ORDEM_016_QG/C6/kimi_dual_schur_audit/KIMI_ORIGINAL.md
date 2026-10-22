# ORDEM016 · ParteC.C6 — crítica independente (texto somente)

**Estatuto desta resposta.** Verificação algébrica estática sobre os quatro arquivos do motor e o `DERIVACAO.md` fornecidos. **Não executei o motor**; os `rc0`, as contagens (540, 2112, 57 palavras) e as tabelas de contato são lidos do `DERIVACAO.md` como **[CAS declarado]**, não reproduzidos por mim. Os arquivos `tensor_euler_zerojet.py`, `smooth_line_compatibility_check_v2.py`, `balanced_log_pair_engine.py` e `bilocal_scalar_euler_zerojet.py` **não foram fornecidos**; onde a auditoria depende deles, digo qual é a lacuna. Escopo: o auxiliar euclidiano 4D de curvatura constante. **Não concluo Q2, não toco gate/kernel.**

---

## Veredito curto

Nos três eixos pedidos — **sinais, dualização, fatores de traço** — a tradução é **preservada em todos os pontos auditáveis com os artefatos fornecidos**. Não encontrei erro demonstrável de índice, sinal ou fator. Há **seis pontos abertos** (seção E), um dos quais (o termo `+(xx/2)·Cstar S|₀`) não é derivável das fórmulas dadas e depende de convenção não fornecida — classificado como *a esclarecer*, não como erro.

---

## A. Sinais e cancelamentos algébricos

**A1. O termo `ℓ C HD`.** Com `HD = −4κP` e `ℓ = 1/(2κ)`:
`ℓ·C·HD = (1/(2κ))·C·(−4κP) = −2 C P` ✓ — bate com a docstring (`S=−2 C P−HQ Kstar`) e com `mixed_ward`, cuja parte métrica implementa:
- Termo 1: `−2 δ^{ab} ∇_a P_{bν cd} = −2(div_X P)_{ν cd}` (div no slot 0 de X; slots X simétricos, indiferente);
- Termo 2: `+δ^{ab} ∇_ν P_{ab cd} = +(d tr_X P)_{ν cd}`;
- Soma: `−2 div + d tr = −2(div − (1/2) d tr) = −2 C` ✓ — **o fator ½ de C está preservado** (razão −2 : +1).

**A2. O termo `D HD`.** Com `D = −I_tr L_h/(4κ)`:
`D·HD = (−I_tr L_h/(4κ))·(−4κP) = +I_tr L_h P` ✓ — duplo sinal cancela; bate com `PH_hh = I_tr Lh P − Cstar S` (código) e com `PH_hh = D HD − Cstar S` (pedido) ✓. A ordem correta é respeitada: `euler()` primeiro computa `M.euler('metric',…)` (o `L_h P`) e **depois** trace-reverte — "Trace reverse the OUTPUT of Lh P" ✓.

**A3. `L_h` e `Q` no motor batem com o pedido.** Em `labelled_covariant_xy.euler`, para `order ≥ 1`: métrica recebe `−2·(termo sem derivadas)` e `+2 g_{ab} tr` (na base δ) → `□ − 2K + 2K g tr = L_h` ✓ (em unidades K=1, com K restaurado por rótulos, conforme "unidades CE*K" do `DERIVACAO`); ghost recebe `+3·(termo sem derivadas)` → `□ + 3K = Q` ✓.

**A4. Sinal da linha ghost em `mixed_ward`.** Os dois termos ghost com `coefficient = −δ^{νj}` dão `−(∇^{(Y)}_c H^ν_d + ∇^{(Y)}_d H^ν_c) = −(K_Y H)^ν_{cd}`. Conferida a cadeia de sinais do `−HQ Kstar` formal contra um espectador `g_{νcd}`, com `Kstar = −2 div`:
`−H^ν_b(−2∇^{(Y)}_e f^{eb}) g_{νcd} = +2 H^ν_b ∇_e f^{eb} g_{νcd} →(partes)→ −∫(∇_e H^ν_b + ∇_b H^ν_e) g_{νcd} f^{eb} = −∫(K_Y H) g f` ✓.
Ou seja: o miolo de `HQ Kstar` é `+K_Y` (a "derivada Y simetrizada **positiva**" do comentário do código) e o sinal `−` de `S` permanece fora → `−K_Y H` ✓ **consistente com o código**. Nota de escopo: essa equivalência vale **módulo contatos** (integração por partes em bitensores de Hadamard) — e é exatamente aí que `S` é não-nulo (ver D).

**A5. Jets métricos com sinais opostos, corretos.** Na parte métrica, as contrações usam a métrica **inversa** `gX^{ab} = δ^{ab} − gX1^{ab}` → jet com sinal `−` (`coefficient = −T.B.gX1[a,b]`) ✓. Na parte ghost, o índice X é **abaixado** com a métrica **covariante** `gX_{νj} = δ_{νj} + gX1_{νj}` → jet com sinal `+` (`coefficient = +T.B.gX1[nu,j]`) ✓ — é exatamente o "Lower its X vector index" do comentário. Os dois sinais são os corretos para os respectivos objetos.

## B. Dualização

**B1. Adjunto de C.** De `C = div − (1/2) d tr`, por definição `⟨C h, v⟩ = ⟨h, C* v⟩`:
`∫(∇^b h_{ba} − ½∇_a h) v^a = ∫ h^{ab}[−(∇_a v_b + ∇_b v_a)/2 + ½ g_{ab} ∇·v]`
logo `(C* v)_{ab} = −sym∇v + g div(v)/2` ✓ — **exatamente** o `Cstar` do pedido e o implementado em `cstar_mixed`: `−½∇_a S_b − ½∇_b S_a + ½ g^{ab}∇^i S_i` ✓ (convenção `sym` com fator ½, coerente com `K = 2 sym∇`).

**B2. Adjunto de K.** `⟨h, K c⟩ = ∫ h^{ab}(∇_a c_b + ∇_b c_a) = −2∫(∇_a h^{ab}) c_b` → `K* h = −2 div h` ✓.

**B3. Identidade de consistência `C K = Q` (verificada à mão).**
`(C K c)^a = ∇_b(∇^b c^a + ∇^a c^b) − ∇^a ∇·c = □c^a + [∇_b,∇^a]c^b = □c^a + Ric^a_b c^b = (Q c)^a` em curvatura constante (`Ric = 3K`) ✓. Isto ancora por que a linha antighost **tem** de entrar na mesma montagem: o operador do ghost é o `Q` do pedido, e a estrutura de Ward fecha através de `C K = Q`.

**B4. Dualização do ghost (`labelled_ghost_dual.py`).** `H_a^b = gX_{ac} H^c_d gY^{db}` com `gX = δ + gX1` e `gY^{−1} = δ − gY1`:
`H_a^b = H^a_b + gX1_{aj} H^j_b − H^a_j gY1^{jb} + O(jet²)` — **exatamente** os dois termos do código (`+gX1[a,j]`, `−gY1[j,b]`) ✓. Ordem de operações declarada e correta: dualizar **depois** da diferenciação covariante (compatibilidade métrica), **antes** do pareamento/extensão ✓. Teto `order ∈ {0,1}` declarado (primeira curvatura) ✓.

**B5. Wick.** Nesta ligação nenhum sinal de Grassmann é devido: dualização métrica e integração por partes não permutam campos de ghost ✓ (coerente com "Não há sinal de Wick atribuído nesta ligação"). Ressalva para a montagem completa em E3.

## C. Fatores de traço

**C1. `I_tr` com fator ½ — forçado, não convencional.** Em n=4, `I_tr X = X − ½ g tr X` é o **único** fator que torna a inversão involutiva: `I_tr²X = X − ½g trX − ½g(trX − ½·4·trX) = X` ✓. O código implementa `−½ δ^{ab} Σ_i euler(…(i,i,c,d))` ✓, com o jet correto `−½ g_{ab}(x) g^{ij}(x)` (`gX1^{ab}δ^{ij} − δ^{ab}gX1^{ij}`, sinal `/−2`) ✓.

**C2. Comutação `I_tr ∘ L_h` em curvatura constante.** Verifiquei: `[I_tr, □] = 0` (compatibilidade métrica: `tr(□X) = □ tr X` exato) e `[I_tr, −2K + 2K g tr] = 0` (conta explícita: ambos os lados dão `−2K X − K g trX`). Logo `I_tr L_h I_tr H_h = I_tr L_h H_h` e a possível ambiguidade de ordem entre `P = H_h I_tr` e o "trace reverse do output" **não produz discrepância** em curvatura constante ✓.

**C3. Fator ½ em C e em C\*.** Ambos preservados (A1, B1) ✓.

## D. Estrutura de Ward e contatos

O motor implementa `S = −2(C_X P + ½ K_Y H)` (com o `gX` abaixando o índice do ghost). Se a identidade de Ward da parametrix é `C_X P = −½ K_Y H`, então `S = 0` fora de contatos — **coerente** com o relatado: "bloco misto zero fora da diagonal até K" e "22 dos 100 contatos ganham contribuição". Ou seja: `S` vive precisamente nos contatos da prescrição parcial, e a exatidão dos sinais/fatores acima é a condição para o cancelamento fora da diagonal. As tabelas `contato_misto = (18 Id_sym − g⊗g)/128` e `contato_completo = (10 Id_sym + 31 g⊗g)/128` (unidades CE·K) **não são deriváveis com os arquivos fornecidos** — permanecem [CAS declarado] (ver E5). A instrução metodológica do pedido está honrada: não exigi cancelamento de palavras rotuladas antes da extensão, nem declarei erro pelo não-cancelamento.

## E. Pontos abertos (não são erros demonstrados)

- **E1 — o termo `+(xx/2)·cstar_mixed(0,ind)` para `order ≥ 1`.** Não é derivável da fórmula `I_tr Lh P − Cstar S` com o material dado. É **plausível** como termo de densidade ("density is applied once at X"): `Δ_VV` ou `g^{−1/2}` em K=1 dão `+xx/2` ✓; mas `Δ_VV^{1/2}` dá `+xx/4` — **se a densidade da prescrição parcial for a raiz de Van Vleck, o fator estaria errado por 2**. Adicionalmente: se `T.xx = |x|²` sem K, o termo é `O(x²)·K⁰` e a pertinência a `order ≥ 1` (ordem de curvatura) depende da convenção de contagem de "order" — **lacuna**: faltam `tensor_euler_zerojet.py` (definição de `T.xx`) e a documentação da densidade. Também não vejo o termo análogo multiplicando `I_tr Lh P`: se a densidade age no bitensor inteiro, a assimetria precisa de justificativa (provavelmente: P já é densificado por construção e S não).
- **E2 — `w = |x−y|²` imposto só na realização ordinária; o motor rotulado não mudou** (falha preservada, `rc1` do primeiro verificador mantido). O "zero fora da diagonal em ordem K" deve ser re-confirmado garantindo que nenhuma palavra rotulada carrega `w` independente escondido — senão o zero pode ser falso zero ou falso não-zero. O `DERIVACAO` declara isto honestamente; registro como risco residual.
- **E3 — Wick na montagem completa.** Quando a linha antighost for pareada com o bloco hh e houver **permutação** dos dois campos de ghost, o sinal de Grassmann entra; está fora do escopo desta ligação (e o `DERIVACAO` o diz), mas deve ser verificado na montagem, não presumido.
- **E4 — teto de ordem.** `dualize` exige `order ∈ {0,1}`: a dualização está verificada apenas em primeira curvatura; `O(K²)` é descartado por construção.
- **E5 — coeficientes de contato.** `(18, −1)/128` e `(10, 31)/128` não foram derivados aqui; seguem [CAS declarado], à espera de derivação independente ou do plano completo. (Sanidade parcial possível: `Id_sym = (δ_{ac}δ_{bd}+δ_{ad}δ_{bc})/2`, dimensão 10 em 4D — não fecha a normalização `1/128` sozinha.)
- **E6 — dupla dualização.** Em `mixed_ward` o abaixamento do índice X do ghost é feito **inline** (`δ^{νj} + gX1^{νj}`); `labelled_ghost_dual.py` faz a dualização completa `H^a_b → H_a^b` para o uso como espectador. As duas vias estão corretas separadamente, mas **não podem ser aplicadas ao mesmo fator** (dupla dualização). No material fornecido não vejo uso simultâneo; fica como cuidado de montagem.
- **E7 — κ ≠ K.** `κ` (de `HD, ℓ, D`) e `K` (de `L_h, Q`) são símbolos distintos no pedido. Todos os cancelamentos verificados (`ℓ·HD = −2P`, `D·HD = I_tr L_h P`) são **independentes da identidade de κ** ✓ — mas a identidade física de κ deve ser declarada em algum ponto da derivação-fonte; não é auditável aqui.

## O que não se conclui

Não concluo Q2, não concluo a soma de vértices, não concluo os pesos temporais nem a montagem completa — o próprio `DERIVACAO` os mantém **OPEN**. Nada aqui move gate, kernel, Atlas ou qualquer bandeira; nenhum arquivo foi escrito ou alterado. A pergunta respondida é a estreita: **a ligação Schur/dual tipada preserva sinais, dualização e fatores de traço nos pontos auditáveis — com E1 (convenção de densidade/`T.xx`) como o único item que exige documento adicional antes de qualquer selo.**