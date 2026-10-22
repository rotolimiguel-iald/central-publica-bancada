# Parecer A7.b — auditoria da fórmula meromórfica de Fourier para pares curvos

**Estatuto deste parecer:** DECLARADO até auditoria da bancada. Nenhum código foi executado nesta unidade; todas as contas abaixo são fechadas, analíticas e reproduzíveis à mão. A derivação vem **antes** de qualquer comparação com o código, conforme ordenado. Não conheço a saída numérica do par. A concordância interna `coefficients ↔ direct_meromorphic` **não** é usada como prova em nenhum ponto. Contexto reconhecido: controle euclidiano auxiliar em espaço-forma 4D (Ric = 3Kg, Λ = 3K, σ constante), K = curvatura (não gerador modular); a fórmula meromórfica em si é a do plano euclidiano — o espaço-forma entra pelos dados de Green/vértice, fora dos trechos fornecidos. Nenhuma constante ajustada; a exclusão de W não é escolha de estado — anotado, sem efeito na fórmula.

**Lacunas de acesso (declaradas, não contornadas):** os trechos carregados são só `curved_harmonic_fourier_engine.py` e `curved_pair_fourier_engine.py` (~100 linhas). Faltam: a definição interna de harmônico `H_l`/`Z_l` do pacote (decide a fase — item crítico abaixo), `first_curvature_gauge_generating_engine`, `position_metric_ordered_operator_engine`, `ghost_direct_position_engine`, a avaliação final do "raw kernel" (o que elimina `z` da resposta, se elimina), e a ORDEM 016 completa. Onde o parecer depende disso, digo.

---

## 1. Derivação direta, da integral de Schwinger/Gamma (antes do código)

**Convenções fixadas pelo enunciado:** Fourier `exp(−ip·x)`, `p² > 0`, `z = x·x`, esquema de parte finita `R(u) = FP_a[(1−a) μ^{2a} z^a u]`, `C_E = −4π²`, `L := FourierLog = log(4μ²/p²) − 2γ_E`.

**Passo 1 — Schwinger em d=4.** Com `z^{−λ} = Γ(λ)^{−1} ∫₀^∞ dt\, t^{λ−1} e^{−tz}` e `∫d⁴x\, e^{−ip·x} e^{−tx²} = (π/t)² e^{−p²/4t}`:

$$\int d^4x\, e^{-ip\cdot x}\, z^{-\lambda} = \frac{\pi^2\,\Gamma(2-\lambda)}{\Gamma(\lambda)}\, 4^{2-\lambda}\, (p²)^{\lambda-2}.$$

Cheque: λ=1 dá `4π²/p²` ✓ (o propagador euclidiano 4D conhecido).

**Passo 2 — o harmônico.** Com `e^{−ip·x}`, tem-se `x_j ↦ i∂_{p_j}`, logo `H_l(x)e^{−ip·x} = i^l H_l(∂_p)e^{−ip·x}`. A fórmula de Rodrigues para harmônico sólido (verificada por mim em l=1,2, incluindo o cancelamento do termo de traço que **exige** ΔH=0):

$$H_l(\partial_p)\, e^{-p²/4t} = (-2t)^{-l}\, H_l(p)\, e^{-p²/4t}.$$

**Passo 3 — fórmula mestre.** Substituindo u = p²/4t:

$$\boxed{\; \int d^4x\, e^{-ip\cdot x} H_l(x)\, z^{-\lambda} = (-i)^l\, \pi²\, 2^{\,4-2\lambda+l}\, \frac{\Gamma(2+l-\lambda)}{\Gamma(\lambda)}\, (p²)^{\lambda-l-2}\, H_l(p) \;}$$

**Passo 4 — a família do enunciado.** `f = H_l(x)\, z^{-(m+l+4)/2} (\log\mu²z)^\ell`, m−l par, ℓ∈{0,1}. A paridade m−l par é o que torna **inteiros** `k = (m−l)/2` e `N = (m+l+4)/2`. Com λ = ν−a, ν = N:

$$F(a) = (-i)^l \pi²\, 2^{-m}\, e^{a(L+2\gamma_E)}\, \frac{\Gamma(a-k)}{\Gamma(N-a)}\, (p²)^{k-a}\, H_l(p),$$

pois `2^{−m+2a} μ^{2a} (p²)^{−a} = 2^{−m} e^{a\ln(4μ²/p²)}` e `L+2γ_E = ln(4μ²/p²)`. Notar: `Γ(2+l−(ν−a)) = Γ(a−k)` — **o polo em k≥0 inteiro é o Γ(−k)**, e é ele que obriga a continuação analítica; em k<0 não há polo e a transformada direta é finita. Isto confirma, pela estrutura e não pela preferência, que **os dois ramos são genuinamente distintos**.

**Passo 5 — separação de Gamma (a peça que o código parametriza).** Usando Γ(z+1)=zΓ(z) repetidamente:

- **k ≥ 0:** `Γ(a−k) = Γ(1+a) / [a ∏_{j=1}^{k}(a−j)]`;
- **k < 0:** `Γ(a−k) = Γ(a+|k|) = Γ(1+a) ∏_{j=1}^{|k|−1}(j+a)` — **sem polo**;
- sempre: `Γ(N−a) = Γ(1−a) ∏_{j=1}^{N−1}(j−a)`.

Logo `Γ(a−k)/Γ(N−a) = [Γ(1+a)/Γ(1−a)] × ratio(a)` com

$$\text{ratio} = \frac{1}{a\prod_{j=1}^k(a-j)\prod_{j=1}^{N-1}(j-a)} \;(k\ge 0), \qquad \text{ratio} = \frac{\prod_{j=1}^{-k-1}(j+a)}{\prod_{j=1}^{N-1}(j-a)} \;(k<0),$$

**exatamente** as formas das linhas 48–49 do código. E por Weierstrass, `log[Γ(1+a)/Γ(1−a)] = −2γ_E a + (2ζ(3)/3)a³ + …` — **sem termo quadrático** — de modo que `e^{a(L+2γ)}Γ(1+a)/Γ(1−a) = e^{aL}(1+O(a³))`. Como o ratio tem no máximo polo simples, o `O(a³)` só contaminaria coeficientes de ordem ≥ a², fora do alcance de ℓ≤1. O comentário das linhas 50–51 do código é **exato**.

**Passo 6 — a parte finita no esquema (1−a), na ordem ordenada.** O log nasce de `∂_a[μ^{2a}z^a] = μ^{2a}z^a \log(\mu²z)` atuando **na família não regulada**; só depois ×(1−a) e FP. Com `P(a) := e^{aL}\,\text{ratio}(a) = Σ c_j a^j`:

- **ℓ=0:** `FP = [a⁰]((1−a)P) = c₀ − c_{−1}`;
- **ℓ=1:** `FP = [a⁰]((1−a)\,∂_a P) = c₁` (o termo `−a·∂_a` mata o `c₀`).

A linha 53 do código (`(1−a)*(s.diff(expansion,a) if ell else expansion)`, depois `.coeff(a,0)`) implementa **precisamente** esta ordem, e **não** diferencia o (1−a) — se o fizesse, sobraria um fantasma `−c₀`. Conforme a instrução.

**Passo 7 — expansões explícitas (as fórmulas fechadas, derivadas).** Com `h := H_k + H_{N−1}`, `h₂ := H_k^{(2)} + H_{N−1}^{(2)}` (harmônicos generalizados), `R := (−1)^k/(k!(N−1)!)`, `R' := (−k−1)!/(N−1)!`:

`∏(1−a/j)^{-1} = 1 + a h + a²(h²+h₂)/2 + …` (o coeficiente de a² é `h² − e₂ = (h²+h₂)/2`, verificado pela expansão da inversa), de modo que:

| caso | ratio(a) | value(ℓ=0) = c₀−c_{−1} | value(ℓ=1) = c₁ |
|---|---|---|---|
| k ≥ 0 | `R[a⁻¹ + h + a(h²+h₂)/2 + …]` | **`R(h − 1 + L)`** | **`R[(h²+h₂)/2 + hL + L²/2]`** |
| k < 0 | `R'[1 + a h + …]` | **`R'`** (sem log) | **`R'(h + L)`** |

O **`−1`** no ℓ=0 é a assinatura do peso (1−a) do esquema (sem ele, a parte finita ingênua seria `h+L`); a estrutura quadrática em L do ℓ=1 vem de `e^{aL}` contra o polo simples. Transformada final derivada:

$$\int d^4x\, e^{-ip\cdot x} f = (-i)^l\, \pi²\, 2^{-m}\, (p²)^k\, H_l(p) \times \text{value}(m,l,\ell).$$

---

## 2. Comparação com o código (depois da derivação)

Os quatro ramos de `coefficients(m,l,ell)` são, termo a termo, **idênticos em magnitude** aos derivados acima: `pref = −1/(2^{m+2}k!(N−1)!)` (k≥0) e `pref = −(−1)^{−k}(−k−1)!/(2^{m+2}(N−1)!)` (k<0); os tuplos `(c₀,c₁,c₂)` = `(pref(h−1), pref, 0)`, `(pref(h²+h₂)/2, pref·h, pref/2)`, `(pref,0,0)`, `(pref·h, pref, 0)` batem com os values da tabela — fatoriais, harmônicos, o `−1` do esquema, os graus em L. ✓

**A fase.** A fase completa da fórmula mestre é `(−i)^l`. O pacote declara separar `i^m`. Como `i^m = i^{l+2k} = i^l(−1)^k`, o resíduo real é `(−1)^{l+k}`. O código embute o `(−1)^k` (nos fatoriais `∏(a−j)|₀ = (−1)^k k!` do ramo k≥0, cancelado pelo `pref` do `direct_meromorphic` dando líquido `−1/(2^{m+2}k!(N−1)!)`; e no `(−1)^{−k}` do ramo k<0) — **mas não o `(−1)^l`**. Algebricamente, nas quatro fórmulas:

$$F_{\text{derivada}} \;=\; (-1)^l \times F_{\text{ código}} \qquad(\text{uniforme, todos os ramos}).$$

**Achado central sobre fases [DECLARADO — depende de convenção não fornecida]:** se o harmônico do pacote é o harmônico sólido padrão com a transformada `e^{−ip·x}` (e o `C_l^1` mostrado é o padrão, argumento `+xp/√(zp2)`, paridade `(−1)^l`), **falta o fator `(−1)^l` no pref** — ou, equivalentemente, a fase a separar é `(−i)^l`, não `i^m`. Se a definição interna de `H_l`/`Z_l` do pacote (não incluída nos trechos) embute `(−1)^l`, o código está correto como está. A decisão exige um documento que não me foi dado; a discrepância é **uniforme** e **isolada** — ver os controles.

---

## 3. Os dois controles independentes pedidos

**Controle A — ramo k<0 (sem série, Γ finito).** Dois casos:

- **(m,l,ℓ)=(0,2,0):** `f = H_2 z^{−3}`. Direto pela fórmula mestre: `(−i)²π²·2^{4−6+2}·Γ(1)/Γ(3)·(p²)^{−1}H_2(p) = −π²/(2p²)·H_2(p)`. Pacote: `P = (−1)⁰2^{−2}·0!/2! = 1/8`; reconstruído: `(1/8)(−4π²)(1)(p²)^{-1}H_2 = −π²/(2p²)H_2` ✓ **exato** (magnitude, fatorial, potência de p).
- **(m,l,ℓ)=(1,3,0):** `f = H_3 z^{−4}`. Direto: `(−i)³π²·2^{4−8+3}·Γ(1)/Γ(4)·(p²)^{−1}H_3 = i·π²·(1/2)(1/6)·H_3/p² = +iπ²/12·H_3/p²`. Pacote: `P = 1/48`; reconstruído: `(1/48)(−4π²i)(p²)^{-1}H_3 = −iπ²/12·H_3/p²`. **Razão −1 = (−1)^l** — este é o controle que isola a fase: para l ímpar o sinal difere, e a diferença é exatamente o fator discutido no §2.

**Controle B — log com polo (k=0, ℓ=1), (m,l)=(0,0).** Família: `F(a) = π² e^{aL}/[a(1−a)]` (após absorção do −2γ em L). `P(a) = 1/a + (1+L) + a(1+L+L²/2) + …`. Esquema:
- ℓ=0: `value = c₀ − c_{−1} = L` → `F[z^{−2}] = π²L` ✓ (a forma conhecida `∫e^{−ipx}/x⁴ = −π² ln p² + const`);
- ℓ=1: `value = c₁ = 1+L+L²/2` → `F = π²(1+L+L²/2)`, e o pacote `(−1/4, −1/4, −1/8)` reconstruído via C_E dá `−4π²·(−1/4 − L/4 − L²/8) = π²(1+L+L²/2)` ✓ **exato nos três coeficientes**.

**Cruzada 1 (derivada na escala):** `∂F(ℓ=1)/∂lnμ² = π²(1+L) ≠ π²L = F(ℓ=0)`. A diferença `π²` é o resíduo do polo: o esquema (1−a) **não comuta** com `∂_{ln μ}` (`∂_μ∘FP ≠ FP∘∂_μ`). Esperado, declarado, não é erro — mas a bancada deve saber que o "−1" e esta não-comutação são o mesmo objeto.

**Cruzada 2 (Laplaciano, família (m,l)=(2,0)):** fora de contatos, `z^{−3} = ∇²z^{−2}/8`, logo `F[z^{−3}] = −p²F[z^{−2}]/8 = −π²p²L/8`. Pacote: `(−3/64 − L/32)×(C_E·i²) = (−3/64 − L/32)(+4π²)(p²) = −π²(3+2L)p²/16` — o termo `L` bate **exatamente** (`−π²p²L/8`); a constante `−3π²p²/16` é contato/esquema (↔ `□δ⁴(x)`), ver §5. Com log (`ℓ=1` nesse par): pela via ∇² os coeficientes de `L²` e `L` batem exatos; a constante difere por contato. Classificado, não erro.

---

## 4. Auditoria estrutural de `node_weights` e da troca m→m−j

**Potência de z (nós não unitários).** `radial = z^{(m+4−l)/2} · p2^k · (l+1) · cheb[l]`. Sob a paridade m−l par, o expoente `(m+4−l)/2` é **inteiro e ≥ 2** — nenhuma raiz residual de z. O balanço de graus é internamente coerente: peso de grau `x^{m+4}` (com o C_l^1 de grau l em x) contra um kernel de grau `−(m+4)`, produzindo integrando de grau `−l` — a forma zonal cuja transformada é a fórmula mestre. ✓ Estruturalmente exato; a composição final peso×kernel-avaliado (o que elimina z, se elimina) **não está nos trechos** — lacuna nomeada.

**Projetor `(l+1)C_l^1`.** Em d=4 o Gegenbauer correto é λ = (d−2)/2 = **1**, e `C_l^1(1) = l+1` é a normalização diagonal do núcleo reproduzinte de S³ (dimensão dos harmônicos `(l+1)²`). Correto — **e exclusivo de d=4**: em outra dimensão o λ mudaria. A recorrência implementada (`cheb[l] = 2xp·cheb[l−1] − z·p2·cheb[l−2]`) é a de `C_l^1` escalada: verifiquei à mão `cheb[1] = 2xp = (zp2)^{1/2}C_1^1(t)` e `cheb[2] = 4xp² − zp2 = zp2·C_2^1(t)` com `t = xp/√(zp2)`. ✓

**Troca m→m−j (gerador externo de grau j).** O comentário ("Multiplication by an external polynomial of degree j requires m−j", linha 32) e o uso (`mh = m−j`, linha 37 do engine de pares) são **corretos em homogeneidade** (grau total `−(m−j)−4`) e **exatos quando o fator externo é radial** (potência de z: `z^{j/2}·H_l z^{−ν} = H_l z^{−(ν−j/2)}`, que é precisamente a fórmula com m→m−j). **Para um polinômio externo angular genérico, a troca não é exata**: o produto re-expande-se em harmônicos `l′ = l+j, l+j−2, …, |l−j|` (Clebsch–Gordan de S³), e cada peça exige `m′ = m+l−l′`, não `m−j`; só a peça maximal `l′ = l+j` obedece à regra. **[OPEN — a demonstrar]:** que os polinômios de `gauge_generator` sejam radiais/zoneficados na direção de p após as contrações `M.weighted`/`G.weighted`. Controle decisivo recomendado (uma linha de sympy, não executado aqui): comparar `i∂_{p_i} F[H_l z^{−ν}]` — que mistura `l±1` — contra `coefficients(m−1, l±1, ℓ)`; se o pacote não reproduzir a mistura, a troca m→m−j está fora do seu escopo para aquele gerador.

---

## 5. Termos suportados em p=0 (não cobertos por p²>0)

- **k ≥ 0:** a fórmula é regular em p=0 (polinômio × log). Como **distribuição**, a continuação analítica de Gel'fand–Shilov é definida **módulo contatos em x**: acrescentar `const×(p²)^j` (j ≤ k) ↔ `□^j δ⁴(x)` não é visto em p²>0 na derivação, e a constante dentro de `L⁰` é precisamente essa liberdade. O pacote fixa a normalização **meromórfica com o peso (1−a)** — coerente com "nenhuma constante ajustada para impor Ward zero": eventuais violações de Ward moram nesses contatos, e o esquema não os esconde nem os fabrica. (Ilustrado na cruzada 2 do §3: a constante `p²×(−3π²/16)` é contato; o log é físico.)
- **k < 0:** `(p²)^k` é **singular em p=0 e não-polinomial** — por isso mesmo **não é resíduo local e não pode ser apagado**, como o enunciado ordena. O pacote os retém com coeficientes próprios (ramo separado, Γ finito) ✓. Como distribuição em p exigiriam prescrição de Hadamard em p=0 — fora do domínio p²>0, declarado.
- **δ⁴(p) puro** (polinômio em x): não ocorre na família homogênea (grau ≤ −4). O integrando efetivo de l=0 é constante em x e sua "transformada" seria `δ⁴(p)` — fora do domínio p²>0 por construção (`assert p2>0`, linha 35 ✓); anotado como o único lugar onde um suporte-em-zero estrito espreitaria.

---

## 6. Conferência m=0..4 × l=0..6 (paridade compatível)

A prova é a fórmula geral do §1 (não exaustão numérica); amostras calculadas à mão e batendo com o código (módulo o `(−1)^l` do §2):

| (m,l) | k | N | ℓ=0: (c₀,c₁,c₂) | ℓ=1: (c₀,c₁,c₂) |
|---|---|---|---|---|
| (0,0) | 0 | 2 | (0, −1/4, 0) | (−1/4, −1/4, −1/8) |
| (1,1) | 0 | 3 | (−1/32, −1/16, 0) | (−13/…, ver fórmula) |
| (2,0) | 1 | 3 | (−3/64, −1/32, 0) | (−17/128, −5/64, −1/64) |
| (2,2) | 0 | 4 | (−5/576, −1/96, 0) | — |
| (3,1) | 1 | 4 | (−11/1152, −1/192, 0) | — |
| (4,0) | 2 | 4 | (−7/2304, −1/768, 0) | — |
| (0,2) | −1 | 3 | (1/8, 0, 0) | (3/16, 1/8, 0) |
| (1,3) | −1 | 4 | (1/48, 0, 0) | (11/288, 1/48, 0) |
| (2,4) | −1 | 5 | (1/384, 0, 0) | (25/4608, 1/384, 0) |
| (0,4) | −2 | 5 | (−1/384, 0, 0) | — |
| (0,6) | −3 | 7 | (1/23040, 0, 0) | — |

(Os casos "—" seguem de `h = H_k + H_{N−1}`, `h₂ = H_k^{(2)} + H_{N−1}^{(2)}` na fórmula geral; e.g. (1,1,ℓ=1): h = 3/2, h₂ = 5/4 → `(−11/128, −3/32, −1/32)`.)

---

## 7. Veredito, lacunas e script puro opcional

**Veredito (DECLARADO até auditoria):**
1. **Constantes** — corretas: potências de 2, fatoriais `k!(N−1)!` / `(−k−1)!/(N−1)!`, harmônicos, verificadas por derivação independente e pelos controles A1, B, ∇².
2. **Partes finitas** — corretas no esquema declarado `FP[(1−a)·]`: o `−1` do ℓ=0 (assinatura do peso), a estrutura `(h²+h₂)/2 + hL + L²/2` do ℓ=1, a ordem das operações (derivada na família → ×(1−a) → FP; **não** diferenciar (1−a)) e a suficiência de `O(a²)` para ℓ≤1 (o comentário do código é exato).
3. **Fases** — **uma discrepância uniforme `(−1)^l`**, isolada pelo controle A2: com as convenções declaradas (`e^{−ip·x}`, `i^m` separado, `C_E=−4π²`, harmônico sólido padrão), o pref deveria carregar `(−1)^l` a mais. Se a definição interna de harmônico do pacote (não fornecida) absorve esse sinal, o código está correto. **É o único ponto que exige documento fora dos trechos.**
4. **Pesos** — potência de z, projetor `(l+1)C_l^1` e recorrência de Gegenbauer corretos para d=4 (e só d=4).
5. **Troca m→m−j** — exata para fatores radiais; **escopo por demonstrar** para geradores angulares, com o controle `i∂_p` recomendado.
6. **p=0** — termos localizados e classificados: contatos em x (esquema) no ramo k≥0; singularidades não-locais retidas no ramo k<0; nenhum δ⁴(p) estrito na família.

**Lacunas que impedem fechar 3 e parte de 4:** definição interna de `H_l`/`Z_l` do pacote; `gauge_generator` e os engines `M`/`G`; a avaliação final do raw kernel; a ORDEM 016 completa.

**Script puro opcional (esqueleto, não executado; independente do pacote):**
```python
# via 1: expansão em série de e^{aL}*ratio(a) com FP (1-a)  [a derivação do §1]
# via 2: fórmula fechada com h, h2 (digamma/harmônicos)     [a tabela do §1, passo 7]
# via 3 (fase): Rodrigues H_l(d)e^{-p²/4t} = (-2t)^{-l} H_l(p) e^{-p²/4t} em l=1,2,3
# as três são independentes de coefficients/direct_meromorphic;
# a concordância interna do pacote não é usada em nenhuma.
```

Nada aqui toca originais, kernel, gate ou infraestrutura; nenhum ramo fora de A7.b foi proposto. O número corrige a frase; o parecer aguarda a bancada.