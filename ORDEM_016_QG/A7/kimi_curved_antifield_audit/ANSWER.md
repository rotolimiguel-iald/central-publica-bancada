# A7.b — a bolha h†(X)c(Y) a primeira ordem em K: kernel indexado, separação universal/W e o contato da extensão fixa

**Estatuto da entrega.** [DERIVED] montagem sobre os vértices e propagadores já medidos nas fontes; [INPUT] perfis radiais, coeficientes de calor e mapas de contato lidos das fontes (não recalculados); [DERIVED — checado por construção interna] os jatos dos bitensores que derivei abaixo da métrica de coordenadas normais dada; [DECLARADO] o CAS entregue como texto — **não executado nesta etapa** (ações externas indisponíveis; pendência registrada no §7); [OPEN] a soma final dos símbolos direcionais. Sem alteração de originais, gate ou infraestrutura; sem novo fundo físico; **Q2 não está paga** e nenhum coeficiente de anomalia é calculado aqui.

---

## 0. Convenções e a conferência de sinais pedida

Do modelo087 e das fontes: `R_abcd = K(g_ac g_bd − g_ad g_bc)`, `Ric_ab = 3K g_ab`, `R = 12K`, K>0; Λ=3K on-shell; κ real não nulo; **K (curvatura) ≠ κ (acoplamento) ≠ gerador modular**.

Conferência pedida, feita por substituição: a fórmula de coordenadas normais `g_ab = η_ab − (1/3) R_acbd x^c x^d + O(x³)` com `R_acbd = K(η_ab η_cd − η_ad η_cb)` dá `R_acbd x^c x^d = K(η_ab x² − x_a x_b)`, logo

```
g_ab = η_ab − (K/3)(η_ab x² − x_a x_b) + O(K x³, K² x⁴)   ✓
```

exatamente a forma dada no pedido. A convenção de R das fontes é portanto a que uso; nenhum sinal é invertido. Da mesma métrica, derivadas que a bolha consome [DERIVED das fontes, checagem interna]:

```
∂_c g_ab = −(K/3)(2 η_ab x_c − η_ca x_b − x_a η_cb)
Γ^a_bc = −(K/3)(δ^a_c x_b + δ^a_b x_c − 2 x^a η_bc) + O(K x²),   Γ^a_bc x^b x^c = 0  ✓ (carta normal)
```

**Aviso registrado (não resolvido aqui):** `u0 = Δ^{1/2} = 1 + Kz/4` é [INPUT] da unidade `curvature_log_terms`. A conferência cruzada contra o Δ de van Vleck do espaço-forma (`(√K r/sin √K r)³ ≈ 1 + K r²/2`) casa em sinal e fator apenas com uma definição operacional de `z` (e.g. `z = −σ/2` lorentziano ou `z = r²`); essa definição vive naquela unidade, que o pedido manda **não refazer**. Onde isso importa, aponto.

---

## 1. O kernel da bolha — forma indexada completa

**Pernas externas:** antifield `h*_{ab}(X)` (polarização simétrica T) e ghost `c^{r'}(Y)` (polarização v), este saindo **do vértice ghost** (conforme a fonte: "bolha externa h*(−p), c(p)=v contém h(q), c(p−q) e vértice ghost V(H,−q,p)"). **Internos:** h (propaga G_H) e o par c–b̄ (propaga G_Q). Antifields não propagam.

**Vértices (convenção já medida, lidos do pedido e da fonte):**

```
V1(X) = T^{ab}[ c^m ∇_m h_ab + 2 h_am ∇_b c^m ]            (antifield; = T·L_c h)
V2(Y) = −(∇^{μ'} b̄^{ν'}) (I_tr L_v h)_{μ'ν'}               (ghost, após integração por partes)
(I_tr)_{μν}^{ρσ} = δ_μ^{(ρ} δ_ν^{σ)} − ½ g_{μν} g^{ρσ},   I_tr² = id (4D) ✓
L_v h_{μ'ν'} = v^{r'} ∇_{r'} h_{μ'ν'} + 2 h_{r'(ν'} ∇_{μ')} v^{r'}
```

**Propagadores internos (preservados como mandado):** `G_H = G_P B^{−1}`, `B = −I_tr/(4κ)`, `P h = □h − 2K h + 2K g tr h`; `G_cbarc = G_Q`, `Q v = □v + 3K v`. Fatores `i`, `4κ`, sinais Grassmann: **fora do kernel** (convenção da fonte); o fator composto é `+4 i κ ℏ` [INPUT, `finite_relative_normalization_v2`].

**Kernel (sem peso global), com bitensores e derivadas dos dois extremos explícitos:**

```
𝓑(X,Y)[T,v] = − T_{ab} ∇^{μ'}_Y G_Q(X,Y)^{m ν'} ⎧ ∇^X_m 𝓜^{ab}{}_{μ'ν'}(X,Y;v) + 2 ∇^X_b 𝓜^{am}{}_{μ'ν'}(X,Y;v) ⎫
```

onde o propagador métrico **vestido pelo vértice ghost** é

```
𝓜^{αβ}{}_{μ'ν'}(X,Y;v) := (I_tr)^{ρ'σ'}{}_{μ'ν'}(Y) ⎡ v^{r'}(Y) ∇^Y_{r'} G_H(X,Y)^{αβ}{}_{ρ'σ'} + 2 G_H(X,Y)^{αβ}{}_{r'(ρ'} ∇^Y_{σ')} v^{r'}(Y) ⎤
```

e `Γ₁ ⊃ (+4 i κ ℏ) ∫_X ∫_Y h*(X)·𝓑(X,Y)·[v(Y), ∇v(Y)]`.

**Quatro estruturas de derivada** (U1/U2 no extremo X × V-i/V-ii no extremo Y):

| estrutura | sobre G_H | sobre G_Q | ghost externo |
|---|---|---|---|
| (U1, V-i) | `∇^X_m ∇^Y_{r'}` | `∇^{μ'}_Y` | v sem derivada |
| (U1, V-ii) | `∇^X_m` | `∇^{μ'}_Y` | `∇^Y v` |
| (U2, V-i) | `∇^Y_{r'}` | `∇^X_b ∇^{μ'}_Y` | v sem derivada |
| (U2, V-ii) | — | `∇^X_b ∇^{μ'}_Y` | `∇^Y v` |

**Verificação plana da forma [DERIVED — a montagem; REAL-CAS da fonte — o resultado]:** em fundo plano (`G_H = S0·(1/z)`, `G_Q = η/z`, `∇^X→ i q`, `∇^Y→ −i q` no propagador e `→ i p` em v), o kernel reduz a `Σ U_m(T,E_i,q,p−q) S0_ij V_mρ(E_j,−q,p) vρ` com denominadores `q²(q−p)²` — `U_m(T,H,k,l) = k_m tr(TH) + 2(HTl)_m`: o termo `tr(TH) q_m` é U1 (`T_{ab} ∇^X_m G_H^{ab..}`) e `2(HTl)_m` é U2 (`2 T_{ab} G_H^{am..} ∇^X_b G_Q^m`, com l = p−q o momento do ghost interno). ✓ A fonte mediu sobre `A0 = 1/(8π²)`: `R(p)v = K_p F(p)v`, `F(p)v = −3/8 p² v + 1/4 p(p·v)`, coeficiente de `p² I(p·v)` **zero sem ajuste**; a Hessiana de Einstein sem gauge anula R e `Σ_log` anula `K_p` — a bolha plana é puro gauge, **sem que Ward=0 tenha sido imposto** (e não o imponho na curva).

---

## 2. Propagadores a O(K) e os diferenciais dos dois extremos

**Referência local admissível (não parametrix de estado):** a série de Hadamard **local e formal** — singularidades e o log são universais (Seeley–DeWitt do operador); `W_A` é o resto suave mantido como **símbolo com jatos nomeados na diagonal** (`w0_A = W_A|diag`, `w1_A = [∇W_A]`, `w2_A = [∇∇W_A]` simetrizado). Nenhuma positividade, espectro ou estado global é invocado. [Conforme o pedido; a existência distributiva é insumo analítico, não prova do CAS — como já declarado na fonte.]

```
G_A(X,Y) = (1/4π²) Π_A(X,Y) ⎡ u0/z − (E_A + 2K I) L/4 ⎤ + W_A,
u0 = 1 + Kz/4  [INPUT];  L = log(μ² z) (mesma μ da extensão);
E_H: autovalores −2K (sem traço, mult. 9), +6K (traço, mult. 1) [INPUT];  E_Q = 3K [INPUT].
```

**Jatos dos bitensores** [DERIVED da métrica das fontes; checados por construção]: em coordenadas normais centradas em Y, com x = X−Y,

```
transporte paralelo (da equação radial dv/dt + Γ(tx)v x = 0, exata nesta ordem):
   Π^a_{b'}(x) = δ^a_b + (K/6)(x² δ^a_b − x^a x_b) + O(K² x⁴)      ← Π = id + (K/6)·x²·(projetor transversal)
   ∂_c Π^a_{b'} = (K/6)(2 x_c δ^a_b − δ^a_c x_b − x^a η_bc) + O(K² x³)   [O(K·x): subdominante]
   [∂_c ∂_d Π^a_{b'}]_diag = (K/6)(2 η_cd δ^a_b − δ^a_c η_bd − δ^a_d η_bc)   [jato = curvatura]
função mundo (gradiente exato na carta):  σ_a = ∇^X_a σ = g_ab(x) x^b
segunda mista:  σ_{a b'} := ∇^X_a ∇^Y_{b'} σ = −g_ab(x) + O(K x³)   [pois ∂_b g_ac·x^c = 0 nesta ordem]
eikonal:  (∇z)² = z para z = σ/2;  □z = 2 − Kz/2 + …  (relação de van Vleck [KNOWN] + u0 [INPUT])
tensor: Π_H^{ab}{}_{μ'ν'} = Π^a_{μ'} Π^b_{ν'};  vetor: Π_Q^m_{ν'}.
```

**Diferenciais consumidos pelo kernel** (escrevo com z_a := ∇^X_a z, z_{a b'} := ∇^X_a ∇^Y_{b'} z):

```
∇^X_a G_A = (1/4π²)⎧ Π_A ⎡ −z_a/z² − (E_A+2K) z_a/(4z) ⎤ + (∇^X_a Π_A)⎡ 1/z + K/4 − (E_A+2K)L/4 ⎤ ⎨ + ∇^X_a W_A
              (a peça u0 é constante: sua derivada de perfil morre; só ∇Π a carrega)

∇^X_a ∇^Y_{b'} G_A = (1/4π²)⎧ Π_A ⎡ −z_{ab'}/z² + 2 z_a z_{b'}/z³ − (E_A+2K)( z_{ab'}/(4z) − z_a z_{b'}/(4z²) ) ⎤
                              + (∇^X_a Π_A)(∇^Y_{b'} perfil) + (∇^Y_{b'} Π_A)(∇^X_a perfil) + (∇^X_a∇^Y_{b'}Π_A)(perfil) ⎨ + ∇^X_a∇^Y_{b'} W_A
```

**Leitura que a pergunta exige:** diferenciar **não** é derivar só o perfil radial. Cada ∇ age em quatro objetos distintos — o perfil (`z`, `L`), o transporte paralelo `Π` (O(K·x) fora da diagonal, curvatura na diagonal), a métrica dos extremos (contrações de índices em X e em Y) e `W_A`. É por isso que **o contato de curvatura não se infere da "massa"** (os autovalores de E_A): E_A entra só no termo `−(E_A+2K)L/4`; os símbolos completos carregam `z_a`, `z_{ab'}`, os jatos de Π e os jatos de W — como mandado.

---

## 3. A bolha a O(K): separação universal-K × jatos de W

Substituindo os diferenciais no kernel, `𝓑 = 𝓑⁽⁰⁾ + δ_K𝓑 + δ_W𝓑`:

- **`𝓑⁽⁰⁾`** (plana): Π = I, u0 = 1, E = 0, W = 0 → `R0 = K_gauge F` [REAL da fonte].
- **`δ_K𝓑` (universal em K):** três origens, todas nomeadas —
  (i) **u0:** peça `K/4` por propagador → produto: `(K/2)` no núcleo `1/z`;
  (ii) **calor:** `−(E_A+2K)L/4` por propagador → produto: `−(E_H⊗I + I⊗E_Q + 4K I) L/(4z)`;
  (iii) **jatos de bitensores:** `∇Π = O(K x)`, `[∇∇Π] = O(K)`, correções O(K) de `z_{ab'}` e de `g` nos extremos.
- **`δ_W𝓑` (jatos de W):** todo termo com `W_A`, `∇W_A`, `∇∇W_A` e seus produtos com os perfis — a fonte já os soma como `W_A⊗I + I⊗W_B` em `1/z`; aqui eles entram **também** dentro dos símbolos diferenciados.

**Coeficientes universais dos pares da bolha** [INPUT, lidos dos perfis]: a bolha h†c carrega um G_H e um G_Q, logo só os pares `(métrico, ghost)`:

```
(E_m autovalores: m0 = −2K, mtr = +6K;  E_g = 3K)  →  −(E_H + E_Q + 4K)/4:
   (m0,g):  −5K/4      (mtr,g):  −13K/4
```

Os núcleos singulares O(K) do produto são **`z^{−1}` (u0, W) e `z^{−1}L` (calor)** — uma potência de z menos singulares que a peça plana `z^{−2}`, como na fonte. As derivadas dos extremos (`∇L = z_a/z`, `∇∇L ~ z_{ab}/z − z_a z_b/z²`, `∇(1/z) = −z_a/z²`) re-elevam o grau: é assim que `L` e `L²` com ordem 4 voltam ao limiar — exatamente o conjunto coberto pela tabela de contatos.

---

## 4. O contato que a extensão fixa produz

**Prescrição conservada:** `R(u) = FP[(1−a) μ^{2a} z^a u]`, mesma μ>0; fórmula da fonte para derivadas:

```
R(D[z^{−n} L^ℓ]) − D R(z^{−n} L^ℓ) = − Σ_j ρ_j [ c_j^{(ℓ+1)}(0)/(ℓ+1) + 1_{ℓ≥1} c_j^{(ℓ)}(0) ]
```

**Resposta concentrada.** Aplicada ao kernel do §1 com os diferenciais do §2, a extensão fixa produz um contato (suporte na diagonal) que se lê **núcleo a núcleo, linearmente no símbolo**, pelos mapas [INPUT]:

| núcleo O(K) | símbolo | contato produzido | origem do coeficiente |
|---|---|---|---|
| `z^{−1}` | P3 | `−Δ_q P3/12` | u0-produto `K/2`; jatos Π; W-peças |
| `z^{−1}L` | P3 | `+Δ_q P3/24` | calor-produto: `(m0,g): −5K/4`; `(mtr,g): −13K/4` |
| `z^{−1}` | P4 | `−Δ_q P4/16 + q²Δ_q²P4/384` | derivadas extras sobre as mesmas peças |
| `z^{−1}L` | P4 | `5Δ_q P4/96 + q²Δ_q²P4/768` | idem |
| `L` | P4 | `−Δ_q²P4/48` | `∇∇L` re-singularizado |
| `L²` | P4 | `−Δ_q²P4/24` | produto calor×calor com derivadas |

Controles distributivos da prescrição [INPUT]: `contato(□, z^{−1}) = −C δ`, `contato(□, z^{−1}L) = 0`, `contato(□², z^{−1}L) = (3/2) C □δ`, `contato(□², L) = −4C δ`, `contato(□², L²) = −8C δ`. Em x-espaço, `Δ_q P_m(q)` ↔ derivadas de δ (m-ésimas), i.e. termos locais em X=Y. Ponte ao setor medido: `C_E/(16π⁴) = −2A0`, peso total `+4 i κ ℏ` [INPUT].

**O que já está fechado e o que falta.** Fechado: os coeficientes universais dos perfis (`K/2`; `−5K/4`; `−13K/4`) e o **referencial do que o perfil radial sozinho dá** — a fonte tabulou para (m0,g), só parte geométrica: ordem 3 `−(3K/32)Δ_q P3`, ordem 4 `−(37K/384)Δ_q P4 − (K/3072) q²Δ_q²P4` [INPUT]. **Esse número é o perfil, não a amplitude:** os símbolos `P3/P4` da bolha incluem as quatro estruturas de derivada dos extremos e os jatos de Π/W do §2–§3; a diferença entre o contato do perfil e o contato da amplitude é **exatamente** o objeto desta pergunta, e sua soma explícita é a pendência de execução do CAS (§5). Nada foi ajustado para Ward=0; a anulação plana (R puro gauge, `H_EH R = 0`, `Σ_log K_p = 0`) fica registrada como referência, não como vínculo imposto à O(K).

---

## 5. O CAS pequeno (texto; gate plano primeiro)

[DECLARADO — não executado nesta etapa; pendência no §7.] Desenho fail-closed: a Etapa 0 **tem** de reproduzir `(−3/8, 1/2, 0)·A0` e os dois negativos (coef. de `p² I(p·v)` nulo; `H_EH·R = 0`); se não reproduzir, a Etapa 1 não é lida.

```python
# a7b_bubble.py — A7.b: bolha h†c. Etapa 0: plano (gate). Etapa 1: O(K) (contato).
import sympy as sp
from sympy import Rational as R_
N = 4
delta = sp.eye(N)                       # extração euclidiana da fonte
A0 = 1/(8*sp.pi**2)

# ---------- vértices por índices (convenção medida) ----------
def sym_mat(s):                         # T^{ab} simétrico, 10 componentes
    c = sp.symbols(s+'0:10'); M = sp.zeros(N)
    for a in range(N):
        for b in range(a, N): M[a,b] = M[b,a] = c[(a*(7-a))//2 + b]
    return M
def U(T,H,k,l):                         # U_m = k_m tr(TH) + 2 (H T l)_m
    return sp.Matrix([k[m]*sp.trace(T*H) + sum(2*H[m,a]*T[a,b]*l[b]
                      for a in range(N) for b in range(N)) for m in range(N)])
def Itr(F): return F - delta*sp.trace(F)/R_(2)
def Lv(H,k,v,l):                        # L_v H com H~e^{ikx}, v~e^{ilx} (i retirado)
    return (l.dot(k))*H + sum(delta[:, :], ()) # placeholder estrutural:
    # implementação real: (v·k) H_{μν} + 2 H_{r(ν} l_{μ)} v^r, por índices
# ---------- Etapa 0: plano ----------
# numerador N(q,p) = U_m(T,S0,q,p−q)·G·V_m(S0,−q,p;v), denominadores q²(q−p)²
# integração: Feynman x∈[0,1], ℓ = q − x p, Δ = x(1−x)p²; regras EXATAS de log:
#   ∫d⁴ℓ (ℓ²+Δ)⁻² → −log Δ ;  ∫ ℓ_aℓ_b/(ℓ²+Δ)² → δ_ab Δ logΔ / 2 [peça log];
#   ∫ ℓ_aℓ_bℓ_cℓ_d/(ℓ²+Δ)² → (δδ+δδ+δδ) Δ² logΔ / 24 [peça log]
# gate: ler coeficientes de p²(p⊗v+v⊗p), (p⊗p)(p·v), p² I(p·v) → (−3/8, 1/2, 0)·A0
# negativos: H_EH(p)·R = 0 ; Σ_log·K_p = 0  (reprovam montagens erradas)
# ---------- Etapa 1: O(K) ----------
# núcleos {z^n L^ℓ} com multiplicação e ∇^X, ∇^Y por regras:
#   dz → z_a ; dz_a → z_ab' ; dL → z_a/z ; eikonal z_a z^a = z ;
#   Π^a_b' = δ + (K/6)(x²δ − x x) e seus jatos (§2) ; W_A com jatos nomeados
# coleta por (núcleo, ordem) → mapas: z⁻¹→−Δ_q P3/12 ; z⁻¹L→+Δ_q P3/24 ; (ordem 4, L, L² conforme §4)
# coeficientes universais: K/2 (u0) ; −5K/4 (m0,g) ; −13K/4 (mtr,g) ; jatos W explícitos
# saída: δ_K𝓑 (universal) ⊕ δ_W𝓑 (jatos) ⊕ contato total; SEM impor Ward
```

O ponto de honestidade do desenho: as regras de log da Etapa 0 são **exatas** (teorema de integração euclidiana), não ajustadas; a prova de que a montagem (vértices, propagadores, sinais de momento) está certa é a reprodução dos três números medidos — check que **pode falhar**, como manda a casa.

---

## 6. Omissão exata (o que esta entrega não pagou)

1. **A soma explícita do contato da amplitude** com os símbolos direcionais completos (as quatro estruturas × os núcleos × os jatos de Π e W): montada, não executada — pendência de execução do CAS.
2. **Os vértices de curvatura dos extremos** (o Γ do fundo dentro dos ∇ dos vértices, O(K·x) fora do ponto): nomeados e contados como subdominantes, não incluídos na soma.
3. **Tadpoles e a soma de inserções da hierarquia causal** — fora do escopo desta unidade, como na fonte.
4. **Ward/identidade BV** (`sa_N + d_H b_N = 0`) a O(K): não verificada e não imposta.
5. A normalização final em `A0`/`C_E` da peça curva segue a ponte [INPUT] `C_E/(16π⁴) = −2A0`, mas só se fecha com o item 1.

**Q2 não está paga.** Nenhuma alteração em originais, kernel, gate, orçamento; nenhuma escolha de novo fundo; nenhuma confirmação declarada.

---

## 7. Lacunas e remissões (sem fingir acesso)

- **Definição operacional de `z`** (e com ela o sinal/fator de `u0 = 1 + Kz/4` contra o Δ de van Vleck): vive na unidade `curvature_log_terms`, que o pedido manda não refazer — remissão registrada; meus jatos usam `z = σ/2` de forma provisória e o CAS parametriza essa escolha.
- **Fontes de leitura primária** (Hollands §§3.4–3.6; Fröb 1803.10235 Teoremas 3/6/7): permanecem remissões das fontes locais, conforme a própria `DERIVACAO_OPERADORES.md` declara — não reli nesta chamada.
- **Execução do CAS** (Etapa 0 de verificação e Etapa 1 de extração): indisponível nesta etapa; o artefato-texto acima é o entregável, e a rodada que o executar deve reportar primeiro o gate plano.
- **Estatuto dos jatos de Π e z_{ab'}** que derivei: [DERIVED das fontes, com checagens internas declaradas (`Γ^a_bc x^b x^c = 0`, `Π→δ`, `∂_b g_ac x^c = 0` na ordem)]; uma conferência independente contra a literatura de bitensores (e.g. expansões de Synge/van Vleck) é bem-vinda e não foi feita aqui.

**Síntese da resposta à pergunta única:** o kernel da bolha a O(K) é o do §1 (quatro estruturas de derivada sobre `G_H = G_P B^{−1}` e `G_Q`, vestido por `I_tr L_v`); os termos universais em K são `K/2` (u0), `−5K/4` no par (m0,g) e `−13K/4` no par (mtr,g) (calor), mais os jatos de curvatura de Π e de `z_{ab'}` que derivei — tudo separado dos jatos de `W` no §3; e a extensão fixa produz, sobre esses núcleos, os contatos da tabela do §4 — cujo fechamento numérico completo (amplitude, não perfil) é a execução pendente do CAS do §5, com o gate plano `(−3/8, 1/2, 0)` como prova de fogo.