# ORDEM016 · Parte C · C6 — Auditoria da ligação: contato escalar medido → primitiva

**Regime desta resposta** (declarado antes de tudo): texto somente. Nada foi executado, compilado, escrito ou alterado nesta etapa; os números, coeficientes e *checks* citados são **lidos dos artefatos fornecidos** (hashes como constam nas fontes), não reproduzidos por mim. A minha verificação é estrutural e algébrica sobre os trechos carregados. Estatutos preservados; gate intocado (`gate_changed: false` declarado nos próprios artefatos); `full_Q2: false`; nada aqui é CONFIRMED; NOT_FALSIFIED ≠ CONFIRMED. O fundo é o **auxiliar euclidiano 4D espaço-forma com K constante** — nenhuma escolha de horizonte ou de estado físico é feita. Os resultados locais foram tratados como objeto de crítica, não como premissa aceita.

---

## 1. O que os artefatos estabelecem (lido, não reexecutado)

- **`oneform_second_curvature_engine_v2.py`** (sha256 `98359838…`): motor de jatos covariantes de 1-formas em espaço-forma 4D, palavras de derivadas de comprimento 1, 3, 5 e ordens de curvatura `o = 0, 1, 2`; dupla simetrização — `symmetric` (média sobre permutações da palavra) e `gauge` (simetrização `(a,b)`); remove o fator de Fourier comum `i`. É a implementação literal da **ordem simetrizada**.
- **`scalar_measured_primitive.py`** (sha256 `3ab846cf…`): casa, em `p` simbólico e 4 polarizações (`o = 0, 1`), a família `flat` (5 coeficientes) + `first` (4 + t) com o contato escalar REAL lido de `balanced_scalar_euler_v2` e `scalar_parallel`. Solução única por Gauss–Jordan (`assert len(free)==0`), verificação simbólica posterior; o contato integrado fatora como **"−i CE × polinônio avaliado em exp(i p.x)"**; escopo declarado: *"Local normal-jet matching through K, scalar hc sector, constant cutoff; no naturality theorem for the full prescription"*; `full_Q2=false`.
- **`scalar_second_parallel_primitive.py`** (sha256 `5a7626c8…`) + **`results.json`** (sha256 `4bdd0e1f…`): estende a K² — monta o readout paralelo `par = second + P1·first + P2·flat` (com `P1=N/6`, `P2=7xx·N/360`, `g1=−N/3`, `g2=2xx·N/45` e as duas identidades algébricas de fechamento verificadas), resolve `aa = 1289/5760`, `bb = −17/1152`, e casa o O(K²) com a família via `N0` (2 coeficientes). **296 checks**, 46,8 s CPU (declarados). Check independente de ação de distribuição nos jatos de teste de primeiro grau. Veredito declarado: *"Local normal parallel-wave jets: N4+K N2+K² N0 acting on G(c) matches actual scalar contact readout at all derivative degrees 5,3,1"*; `limited_to`: três sabores escalares sem massa, jato singular de Hadamard fixo local, cutoff constante, espaço-forma auxiliar; `full_causal_family=false`, `global_naturality_proved=false`.

**[REAL lido]** o matching, os coeficientes e as identidades exatas em racionais. Os `assert` são declarações dos artefatos; não os reexecutei.

---

## 2. A definição de N com ordem simetrizada

Com `□ = ∇^μ∇_μ`, `(∇·h) = ∇^μh_μ`, e "sym" denotando a média sobre permutações das palavras de derivadas (a `symmetric` do motor) com `(a,b)` simetrizados (a `gauge`), o operador lido é:

**N = N4 + K·N2 + K²·N0**

com os monômios (estrutura conforme `loop_gauge`; os fatores e posições finas de índices são os do código) e coeficientes **lidos** de `results.json`:

**N4** (ordem 4, O(K⁰)) — `(c1,…,c5)`:
```
c1 = 13/10240 − c/2        →  □² h_a
c2 = 163/20480 − b         →  ∇_a □² (∇·h)
c3 = b                     →  ∇_a∇_b □ (∇·h)   e   δ_ab ∇^i∇^k □ (∇_i h_k + ∇_k h_i)
c4 = c                     →  ½[ ∇_a∇^i □ (∇_i h_b + ∇_b h_i) + (a↔b) ]      (par)
c5 = −b − c/2 − 57/5120    →  ∇_a∇_b ∇^i∇^k (∇_i h_k + ∇_k h_i)              (sym (i,k))
```

**N2** (ordem 2, O(K¹)) — `(d1,…,d4,t)`, todos com sinal − na combinação:
```
d1 = −11b/3 − 7c/6 − t/2 − 31/3072   →  □ h_b
d2 = 19b/3 + c/2 + t/2 − 103/768     →  δ_ab □ (∇·h)
d3 = −4b/3 + c/3 − t/2 + 83/1536     →  ∇_a∇_b (∇·h)   e   δ_ab ∇^i∇^k (∇_i h_k + ∇_k h_i)
d4 = t                               →  ½[ ∇_a∇^i (∇_i h_b) + (a↔b) ]      (par)
```

**N0** (ordem 0, O(K²)) — `(second[0], second[1])`, sinal +:
```
second[0] = 4b/3 − 2c + t − 2599/11520    →  h_b
second[1] = −89b/6 − c/4 − t + 45491/92160 →  δ_ab (∇·h)
```

**Ponto decisivo:** `free_parameters = [b, c, t]`, `parameters_chosen: false`. O matching é satisfeito **com b, c, t simbólicos** — o contato não os vê. E o padrão é revelador: cada parâmetro aparece **espalhado pelos três níveis K⁰/K¹/K² com sinais compensadores** (t: `−t/2, +t/2, −t/2, +t` em N2 e `+t, −t` em N0; b e c analogamente). Essa é a assinatura característica de **redistribuição por identidades de comutação** — em espaço-forma, `[∇_i,∇_j]h_k = K(g_{ik}h_j − g_{jk}h_i)`, e reordenar palavras de N4 produz correções em K·(monômios de N2) e K²·(monômios de N0). **[DERIVED — diagnóstico estrutural; não provado nos artefatos.]**

---

## 3. Autoadjuncidade formal no produto natural de tensores

Produto natural de 1-formas: `⟨h,k⟩ = ∫ g^{ab} h_a k_b dvol_g`. A condição é `⟨h,Nk⟩ = ⟨Nh,k⟩`.

**Verificação formal (no papel, não por máquina):**

- **Classes puras, autoadjuntas termo a termo:** potências `□^m` (pois `□ = ∇*∇` com o sinal da conexão); a classe `dd*` — `∇_a(∇·h)` e iterados, pois `d` e `d*` são adjuntos formais, logo `∇_a□²(∇·h)` (`= −d□²d*`) é autoadjunto; multiplicação por constante (`second[0]`).
- **Classes mistas:** entram **aos pares explicitamente simetrizados** — `c4` e `d4` como `½[· + (a↔b)]`; `c5` e os segundos `c3`/`d3` com simetrização `(i,k)` interna e `(a,b)` externa (é exatamente o que a função `gauge` implementa).
- **Leitura pelo símbolo:** em ordem simetrizada (Weyl) com coeficientes constantes sobre espaço localmente simétrico, autoadjuncidade formal ⟺ **símbolo total real simétrico nos índices de campo** (ordens pares). O `measured` e o `wanted` são simétricos em `(i,j)` por construção, e o matching é uma identidade polinomial em `p` simbólico — logo o símbolo total da família é simétrico.

**Veredito:** a família N é **formalmente autoadjunta para todo (b,c,t)** — **[DERIVED da estrutura do ansatz + simetria do símbolo casado]**. Duas honestidades: (i) nenhum artefato contém uma verificação *explícita* de autoadjuncidade (a identidade `⟨h,Nk⟩ − ⟨Nh,k⟩ = ∇·V` não está computada em módulo algum) — **[OPEN como verificação formal independente; estruturalmente esperada verdadeira]**; (ii) justamente por ser automática na classe do ansatz, **a autoadjuncidade não restringe (b,c,t)** — ela não pode ser invocada para fixar os parâmetros livres.

---

## 4. O funcional quadrático B e o sinal

Com `s₀h = G(c)` (h par, c ímpar, s₀ derivação ímpar) e N formalmente autoadjunto:

```
B[h] = ½ ⟨h, N h⟩ = ½ ∫ dvol_g  g^{ab} h_a (Nh)_b
s₀B  = ½( ⟨G(c), Nh⟩ + ⟨h, NG(c)⟩ )  =  ⟨h, NG(c)⟩  =  contato
```

O sinal é **+**: h par faz a derivação passar sem sinal de Kirchhoff, a autoadjuncidade troca os dois termos, e o ½ cancela o 2. O sinal *relativo* entre N e o contato já foi fixado pelo próprio matching (`R(p) = A_flat − K·A_parallel`, com N4 em +, N2 em −, N0 em +); o fator global `−i CE` do contato integrado entra como fator global de B. **A existência de uma primitiva quadrática local é equivalente à autoadjuncidade formal de N** — é a condição de integrabilidade; satisfeita estruturalmente (§3). **[DERIVED formal.]** Unicidade: módulo termos `s₀`-exatos e `d`-exatos; e **B herda a liberdade (b,c,t)** salvo prova de redundância — §5.

---

## 5. A pergunta da unidade: a igualdade em 4 polarizações com p simbólico e transporte paralelo é suficiente?

**Resposta: é suficiente para o símbolo total simetrizado; é suficiente para o operador local linearizado neste fundo somente sob uma hipótese adicional concreta, que nomeio abaixo.**

O que a igualdade entrega, de fato: 4 polarizações = base completa de polarizações em 4D; `p` simbólico = momento genérico; graus 5, 3, 1 = as ordens de derivada que esgotam a ação de N4, N2, N0 sobre jatos de 1-forma; transporte paralelo montado e conferido por um check independente de distribuição; solução **única** dentro do ansatz (Gauss–Jordan sem variáveis livres). Isso determina o **símbolo total em ordem simetrizada** do operador na classe testada.

Para transformar isso em "o operador local linearizado neste fundo", restam:

- **(H1) Naturalidade do ansatz** — que N seja um operador natural covariante da classe `loop_gauge` (monômios em ∇/g/R com ∇R = 0). Em espaço localmente simétrico, símbolo total + naturalidade determinam o operador; sem H1, o mesmo símbolo pode provir de operadores não naturais. O contato não prova H1: ela é a *forma* do código, não um teorema. É a hipótese de forma do programa — aceita, mas **[OPEN como teorema]**.
- **(H2) — a hipótese adicional concreta a nomear:** **classificar a liberdade (b,c,t)**. Ou se prova que a variação em (b,c,t) anula N *como operador* via as identidades de comutação do espaço-forma (**redundância de representação** — o padrão de sinais compensadores entre níveis a torna plausível, mas não está provada), ou, em caso negativo, (b,c,t) são **parâmetros genuínos a fixar por uma condição independente do contato** — e a autoadjuncidade não serve para isso (§3). Enquanto H2 não for paga, "o operador local" é uma **família 3-paramétrica**, e a primitiva B herda a mesma liberdade.

Delimitações já declaradas nos artefatos (restrições de validade, não hipóteses a remover aqui): truncamento **O(K²)** (O(K³) **[OPEN]**); três sabores escalares sem massa; Hadamard fixo local; **cutoff constante**; espaço-forma euclidiano **auxiliar**.

---

## 6. Distinções exigidas pela ordem (o que isto NÃO é)

- **Não é a família causal/natural completa:** `full_causal_family=false`, `global_naturality_proved=false`, `causal_normalization_constructed=false` — falta a normalização causal (prescrição microlocal/Feynman) e a prova de naturalidade da prescrição inteira.
- **Não é cutoff variável:** `limited_to` declara cutoff constante. A prescrição parcial **R_bal rotulada mais linha suave** (não Rraw), referida na ordem, exigiria **novo matching** e análise de contratermos locais — ausente destes artefatos.
- **Não é Q2 completa** (`full_Q2=false`), **não recalcula o setor tensorial** da unidade MiMo (por ordem, não tocado), **não move o gate** (`gate_changed=false`), e **não é confirmação física** — é uma identidade formal num fundo auxiliar, com uma hipótese nomeada pendente.

---

## 7. Lacunas de fonte (declaradas, sem fingir acesso)

Para auditoria completa da convenção fina de índices/fatores e da proveniência do "contato REAL medido", faltam nesta chamada: `scalar_parallel/results.json`, `balanced_scalar_euler_v2/results.json`, `scalar_vertex_v2/MATRICES.json`, `scalar_second_curvature_v2/MATRIX.json`, `balanced_log_pair_engine.py`, `smooth_line_compatibility_check_v2.py`, `spaceform_covariant_jet_engine.py`, `deliver_nonminimal_wick_and_mimo_audit.py`, `scalar_parallel_readout.py`. Sem eles, minha leitura é estrutural sobre os trechos carregados; a mecânica exata dos motores referenciados não foi reaberta.

---

### Síntese em uma frase

A ligação **contato medido → operador** está fechada como identidade exata de símbolo total simetrizado (N = N4 + K N2 + K² N0, coeficientes racionais lidos, matching em 4 polarizações e graus 5/3/1) **[REAL lido]**; a ligação **operador → primitiva** é `B = ½⟨h,Nh⟩` com `s₀B = ⟨h,NG(c)⟩` no sinal correto, **equivalente à autoadjuncidade formal de N — satisfeita estruturalmente para todo (b,c,t)** **[DERIVED]**; e **não é suficiente incondicionalmente**: resta **(H2)** — provar que (b,c,t) são redundâncias de representação por comutação (padrão de sinais compensadores a favor) ou fixá-los por condição independente do contato — além de **(H1)** naturalidade como teorema, O(K³), família causal, naturalidade global e cutoff variável, todos **[OPEN]**. Gate intocado; `full_Q2=false`; NOT_FALSIFIED ≠ CONFIRMED.