# A7.b — Vértice quártico polarizado da parte Γ-Γ: resposta e auditoria independente

**Resposta em duas linhas.** O vértice `32·kappa·V4` é a soma sobre as 12 configurações (par ordenado de pernas-γ × par não ordenado de pernas de fundo) dos blocos T1–T8 abaixo, com coeficientes +4 / −2 / +(t_Z t_W − 2·tr(ZW)). **A contração com duas pernas internas g a momento zero fecha em forma exata e não-nula:**

```
eh_quartic_32k(g, 0, g, 0, A, p, B, q)  ==  8 · eh_quadratic_8k(A, p, B, q)
```

— oito vezes o núcleo quadrático Γ-Γ do anexo (sem o termo de gauge-fixing, que é linear e não gera vértices superiores). Contrasto direto com `V4_pot(g,g,A,B)=0` do DERIVACAO.md anexo: o tadpole do potencial morre, **o do quártico derivativo não morre**. Estatuto: [DERIVED algebricamente da expansão; DECLARADO até a auditoria local — os testes embutidos são a auditoria, e eu **não executei** o código nesta sessão].

---

## 1. Derivação (sem supor comutação de matrizes)

**Setup.** Com G = g + h, C^ρ_{μν} = (i/2)·G^{ρλ}γ_{λμν}(h) exato, γ linear em h (convenção do anexo: `gamma = i/2 * gamma2`). A densidade Γ-Γ é

```
ℒ_ΓΓ = sqrt(det G)·G^{μν}·(C^ρ_{μσ}C^σ_{νρ} − C^ρ_{μν}C^σ_{ρσ})
     = d(h) · U(h)^{μν} · [CC]
```

com **três inversas**: uma externa (G^{μν}) e duas internas (uma em cada C). As expansões necessárias até ordem 2 (os dois γ's já carregam duas das quatro pernas):

- **inversas** (cada uma): `G^{-1} = g^{-1} − h + h² − …` (em componentes: U_0 = δ, U_1 = −h, U_2 = +h², produtos de matriz na ordem escrita);
- **determinante**: com M = I + g⁻¹h, t_j = tr(M^j),

```
sqrt(det M) = 1 + t1/2 + (t1²/8 − t2/4) + (t1³/48 − t1·t2/8 + t3/6)
              + (t1⁴/384 − t1²·t2/32 + t1·t3/12 + t2²/32 − t4/8) + O(M⁵)
```

(confere com o anexo: substituída em P(h) = √det M·(tr M⁻¹ − 2) reproduz exatamente P2 = s2/2 − t²/4, P3 = −t³/12 + t·s2/2 − 2s3/3, P4 = −t⁴/64 + 3t²s2/16 − 3s2²/16 − t·s3/2 + 3s4/4 do DERIVACAO.md). Para o Γ-Γ quártico bastam d_1 = t/2 e d_2(Z,W) = t_Z·t_W/4 − tr(ZW)/2.

**Polarização sem comutação.** Cada monômio multilinear entra uma vez. Os dois γ's carregam duas pernas ordenadas (X,Y); as outras duas (Z,W, não ordenadas) distribuem-se como inserções nos quatro fatores (d, U_ext, prefixo de γ_X, prefixo de γ_Y). As ordenações de produto `ZW` e `WZ` são termos **distintos** (blocos T1, T5); os prefixos duplos `up(Z,up(W,γ))` e `up(W,up(Z,γ))` idem; só os traços são simétricos por natureza (tr(ZW) = inner(Z,W)). Sinais: (i/2)² = −1/4 nos CC; R4 = −16·ℒ_ΓΓ⁽⁴⁾, o que reproduz a convenção do anexo (R_n = 2^{n+1}κ·ℒ_n: 8κ quadrático, 16κ cúbico, **32κ quártico** ✓ — verificado o cúbico termo a termo contra o anexo).

**Blocos por configuração** (γ_X, γ_Y ordenados; {Z,W} fundo; `up` = upper_product do anexo; `contr` = contraction do anexo; I = identidade):

```
T_núcleo = contr(I, up(Z,up(W,γX)), γY) + contr(I, up(W,up(Z,γX)), γY)
         + contr(I, γX, up(Z,up(W,γY))) + contr(I, γX, up(W,up(Z,γY)))
         + contr(I, up(Z,γX), up(W,γY)) + contr(I, up(W,γX), up(Z,γY))
         + contr(Z, up(W,γX), γY) + contr(Z, γX, up(W,γY))
         + contr(W, up(Z,γX), γY) + contr(W, γX, up(Z,γY))
         + contr(mmul(Z,W), γX, γY) + contr(mmul(W,Z), γX, γY)
A_W = contr(I, up(W,γX), γY) + contr(I, γX, up(W,γY));   A_Z = idem com Z
R4_config = 4·T_núcleo
            − 2·(t_Z·A_W + t_W·A_Z)
            − 2·(t_Z·contr(W,γX,γY) + t_W·contr(Z,γX,γY))
            + (t_Z·t_W − 2·tr(ZW))·contr(I,γX,γY)
R4(A,B,C,D) = Σ sobre os 12 pares ordenados (γ_X,γ_Y) de R4_config
```

**Contração g,g (cálculo explícito).** γ(g)(momento zero) = 0, logo só sobrevivem as duas configurações (γA,γB; g,g) e (γB,γA; g,g). Com t_g = 4, tr(g·g) = 4, up(g,·) = ·, mmul(g,g) = g: T_núcleo = 12·contr(I,γA,γB), os blocos de traço dão −32, −16, +8. Total `(48 − 32 − 16 + 8) = 8`. Q.E.D.: **8 × o núcleo quadrático** — derivado, não ajustado.

## 2. Código (Python puro, stdlib apenas)

```python
"""A7.b — vertice quartico polarizado da parte Gamma-Gamma de Einstein-Hilbert.

Convencoes do anexo metric_principal_vertices.py: indices euclidianos 4D,
Fourier exp(+ipx), perturbacoes covariantes lineares, fundo g = delta nas
componentes (a forma covariante e a mesma com nabla no lugar de partial;
as correcoes de conexao pertencem a outras unidades).
Quadratico: 8*kappa*V2 = eh_quadratic_8k.  Cubico: 16*kappa*V3 = eh_cubic_16k.
Quartico (este arquivo): 32*kappa*V4 = eh_quartic_32k.

A parte Gamma-Gamma e usada modulo a derivada total
    d_rho[ sqrt(G) (G^{mu,nu} C^rho_{mu,nu} - G^{mu,rho} C^lambda_{mu,lambda}) ],
descartada com cutoff CONSTANTE (caixa periodica); os contatos associados NAO
sao apagados da missao — ficam para as unidades de contatos/BV.
Sem ajuste a anomalia, sem transversalidade imposta, sem tentativa de Q2.

Quando o anexo esta no path, os testes cruzados (g,g e Ward) rodam contra ELE;
caso contrario, contra as copias internas bit-a-bit abaixo.
"""
import math, random
from itertools import permutations, combinations

# ---------- primitivas (copias bit-a-bit do anexo; substituidas pelo anexo se presente) ----------
def _I(): return tuple(int(i == j) for i in range(4) for j in range(4))
I4 = _I()

def trace(H): return sum(H[4*i + i] for i in range(4))
def dot(p, q): return sum(x*y for x, y in zip(p, q))
def mv(H, p): return tuple(sum(H[4*i + j]*p[j] for j in range(4)) for i in range(4))
def inner(H, J): return sum(a*b for a, b in zip(H, J))
def mmul(A, B):
    return tuple(sum(A[4*i + k]*B[4*k + j] for k in range(4)) for i in range(4) for j in range(4))

def gamma2(H, p):
    # gamma = i/2 * gamma2, indices [rho, mu, nu]
    return tuple(p[mu]*H[4*nu + rho] + p[nu]*H[4*mu + rho] - p[rho]*H[4*mu + nu]
                 for rho in range(4) for mu in range(4) for nu in range(4))

def up(H, G):
    # upper_product do anexo: (H^rho_a G^a_{mu,nu})
    return tuple(sum(H[4*rho + a]*G[16*a + 4*mu + nu] for a in range(4))
                 for rho in range(4) for mu in range(4) for nu in range(4))

def contraction(W, G, H):
    # W^mu,nu (G^rho_mu,sigma H^sigma_nu,rho - G^rho_mu,nu H^sigma_rho,sigma)
    ht = [sum(H[16*a + 4*rho + a] for a in range(4)) for rho in range(4)]
    result = 0
    for mu in range(4):
        for nu in range(4):
            w = W[4*mu + nu]
            if w:
                b = sum(G[16*rho + 4*mu + sigma]*H[16*sigma + 4*nu + rho]
                        for rho in range(4) for sigma in range(4))
                b -= sum(G[16*rho + 4*mu + nu]*ht[rho] for rho in range(4))
                result += w*b
    return result

def c2(H, p):
    hp = mv(H, p); tr = trace(H)
    return tuple(2*hp[i] - p[i]*tr for i in range(4))

def _eh_quadratic_8k(H, p, J, q):
    G, L = gamma2(H, p), gamma2(J, q)
    return contraction(I4, G, L) + contraction(I4, L, G)

def _eh_cubic_16k(H, p, J, q, L, r):
    fields = [(H, p), (J, q), (L, r)]
    gs = [gamma2(f, pp) for f, pp in fields]
    result = 0
    for i, j, k in permutations(range(3)):
        A = fields[i][0]; G, T = gs[j], gs[k]
        result += trace(A)*contraction(I4, G, T) - 2*contraction(A, G, T)
        result -= 2*contraction(I4, up(A, G), T)
        result -= 2*contraction(I4, G, up(A, T))
    return result

def gauge_matrix(p, v):
    return tuple(p[a]*v[b] + p[b]*v[a] for a in range(4) for b in range(4))

def lie_matrix(H, p, k, v):
    hv = mv(H, v); vp = dot(v, p)
    return tuple(vp*H[4*a + b] + k[a]*hv[b] + k[b]*hv[a] for a in range(4) for b in range(4))

try:  # se o anexo estiver no path, os testes cruzados usam ELE
    from metric_principal_vertices import (
        eh_quadratic_8k, eh_cubic_16k)  # type: ignore
    _ANNEX = True
except Exception:
    eh_quadratic_8k = _eh_quadratic_8k
    eh_cubic_16k = _eh_cubic_16k
    _ANNEX = False

# ---------- vertice quartico: 32*kappa*V4 ----------
def _quartic_config(gX, gY, Z, W):
    tZ, tW = trace(Z), trace(W)
    A_W = contraction(I4, up(W, gX), gY) + contraction(I4, gX, up(W, gY))
    A_Z = contraction(I4, up(Z, gX), gY) + contraction(I4, gX, up(Z, gY))
    core = (
        contraction(I4, up(Z, up(W, gX)), gY) + contraction(I4, up(W, up(Z, gX)), gY)
        + contraction(I4, gX, up(Z, up(W, gY))) + contraction(I4, gX, up(W, up(Z, gY)))
        + contraction(I4, up(Z, gX), up(W, gY)) + contraction(I4, up(W, gX), up(Z, gY))
        + contraction(Z, up(W, gX), gY) + contraction(Z, gX, up(W, gY))
        + contraction(W, up(Z, gX), gY) + contraction(W, gX, up(Z, gY))
        + contraction(mmul(Z, W), gX, gY) + contraction(mmul(W, Z), gX, gY))
    return (4*core
            - 2*(tZ*A_W + tW*A_Z)
            - 2*(tZ*contraction(W, gX, gY) + tW*contraction(Z, gX, gY))
            + (tZ*tW - 2*inner(Z, W))*contraction(I4, gX, gY))

def eh_quartic_32k(A, p, B, q, C, r, D, s):
    """32*kappa*V4 polarizado (12 configuracoes: par ordenado de gamas x par de fundo)."""
    fields = [(A, p), (B, q), (C, r), (D, s)]
    gs = [gamma2(f, pp) for f, pp in fields]
    total = 0
    for ix in range(4):
        for iy in range(4):
            if iy == ix:
                continue
            rest = [k for k in range(4) if k != ix and k != iy]
            total += _quartic_config(gs[ix], gs[iy], fields[rest[0]][0], fields[rest[1]][0])
    return total

# variante perturbada para o controle negativo (o teste tem de morder)
def _eh_quartic_32k_perturbed(A, p, B, q, C, r, D, s):
    fields = [(A, p), (B, q), (C, r), (D, s)]
    gs = [gamma2(f, pp) for f, pp in fields]
    total = 0
    for ix in range(4):
        for iy in range(4):
            if iy == ix:
                continue
            rest = [k for k in range(4) if k != ix and k != iy]
            Z, W = fields[rest[0]][0], fields[rest[1]][0]
            tZ, tW = trace(Z), trace(W)
            A_W = contraction(I4, up(W, gs[ix]), gs[iy]) + contraction(I4, gs[ix], up(W, gs[iy]))
            A_Z = contraction(I4, up(Z, gs[ix]), gs[iy]) + contraction(I4, gs[ix], up(Z, gs[iy]))
            core = (
                contraction(I4, up(Z, up(W, gs[ix])), gs[iy]) + contraction(I4, up(W, up(Z, gs[ix])), gs[iy])
                + contraction(I4, gs[ix], up(Z, up(W, gs[iy]))) + contraction(I4, gs[ix], up(W, up(Z, gs[iy])))
                + contraction(I4, up(Z, gs[ix]), up(W, gs[iy])) + contraction(I4, up(W, gs[ix]), up(Z, gs[iy]))
                + contraction(Z, up(W, gs[ix]), gs[iy]) + contraction(Z, gs[ix], up(W, gs[iy]))
                + contraction(W, up(Z, gs[ix]), gs[iy]) + contraction(W, gs[ix], up(Z, gs[iy]))
                + contraction(mmul(Z, W), gs[ix], gs[iy]) + contraction(mmul(W, Z), gs[ix], gs[iy]))
            total += (3*core  # <-- coeficiente errado de proposito
                      - 2*(tZ*A_W + tW*A_Z)
                      - 2*(tZ*contraction(W, gs[ix], gs[iy]) + tW*contraction(Z, gs[ix], gs[iy]))
                      + (tZ*tW - 2*inner(Z, W))*contraction(I4, gs[ix], gs[iy]))
    return total

# ---------- expansao de sqrt(det(I+M)) ----------
def sqrt_det_series(M, order=4):
    t = [0] + [trace(M if j == 1 else _mpow(M, j)) for j in range(1, order + 1)]
    out = [1.0, t[1]/2.0,
           t[1]**2/8.0 - t[2]/4.0,
           t[1]**3/48.0 - t[1]*t[2]/8.0 + t[3]/6.0,
           t[1]**4/384.0 - t[1]**2*t[2]/32.0 + t[1]*t[3]/12.0 + t[2]**2/32.0 - t[4]/8.0]
    return out[:order + 1]

def _mpow(M, j):
    R = I4
    for _ in range(j):
        R = mmul(R, M)
    return R

def det4(M):
    m = [[M[4*i + j] for j in range(4)] for i in range(4)]
    def det3(a): return (a[0][0]*(a[1][1]*a[2][2] - a[1][2]*a[2][1])
                         - a[0][1]*(a[1][0]*a[2][2] - a[1][2]*a[2][0])
                         + a[0][2]*(a[1][0]*a[2][1] - a[1][1]*a[2][0]))
    d = 0.0
    for j in range(4):
        minor = [[m[i][k] for k in range(4) if k != j] for i in range(1, 4)]
        d += ((-1)**j)*m[0][j]*det3(minor)
    return d

# ---------- geradores de teste ----------
def rand_field(rng):
    H = [rng.randint(-3, 3) for _ in range(16)]
    for i in range(4):
        for j in range(i + 1, 4):
            H[4*j + i] = H[4*i + j]
    return tuple(H)

def rand_momenta(rng, n, conserved=True):
    ps = [tuple(rng.randint(-2, 2) for _ in range(4)) for _ in range(n)]
    if conserved:
        s = [sum(p[i] for p in ps) for i in range(4)]
        ps[-1] = tuple(ps[-1][i] - s[i] for i in range(4))
    return ps

def addp(p, q): return tuple(x + y for x, y in zip(p, q))

# ---------- testes ----------
def test_bose():
    for seed in range(6):
        rng = random.Random(1000 + seed)
        F = [(rand_field(rng), p) for p in rand_momenta(rng, 4)]
        base = eh_quartic_32k(*[x for f in F for x in f])
        for perm in permutations(range(4)):
            G = [F[i] for i in perm]
            assert eh_quartic_32k(*[x for f in G for x in f]) == base, f"Bose falhou seed={seed}"

def test_gg_contraction():
    g = I4; zero = (0, 0, 0, 0)
    for seed in range(6):
        rng = random.Random(2000 + seed)
        A, B = rand_field(rng), rand_field(rng)
        p, q = rand_momenta(rng, 2)
        lhs = eh_quartic_32k(g, zero, g, zero, A, p, B, q)
        rhs = 8*eh_quadratic_8k(A, p, B, q)
        assert lhs == rhs, f"contracao g,g falhou seed={seed}: {lhs} vs {rhs}"

def test_ward():
    for seed in range(10):
        rng = random.Random(3000 + seed)
        A, B, C = rand_field(rng), rand_field(rng), rand_field(rng)
        p, q, r = rand_momenta(rng, 3)
        v = tuple(rng.randint(-2, 2) for _ in range(4))
        qv = tuple(-(p[i] + q[i] + r[i]) for i in range(4))
        g4 = gauge_matrix(qv, v)
        lieA = lie_matrix(A, p, addp(p, qv), v)
        lieB = lie_matrix(B, q, addp(q, qv), v)
        lieC = lie_matrix(C, r, addp(r, qv), v)
        lhs = eh_quartic_32k(A, p, B, q, C, r, g4, qv)
        rhs = (eh_cubic_16k(lieA, addp(p, qv), B, q, C, r)
               + eh_cubic_16k(A, p, lieB, addp(q, qv), C, r)
               + eh_cubic_16k(A, p, B, q, lieC, addp(r, qv)))
        assert lhs + 2*rhs == 0, f"Ward V4<->V3 falhou seed={seed}"

def test_conformal():
    for seed in range(10):
        rng = random.Random(4000 + seed)
        fs = [rng.randint(-2, 2) for _ in range(4)]
        if all(f == 0 for f in fs):
            fs[0] = 1
        ps = rand_momenta(rng, 4)
        lhs = eh_quartic_32k(*[x for i in range(4) for x in
                               (tuple(fs[i]*c for c in I4), ps[i])])
        gg = [gamma2(I4, ps[i]) for i in range(4)]
        rhs = 0
        for i, j in combinations(range(4), 2):
            rest = [k for k in range(4) if k != i and k != j]
            for k, l in [(rest[0], rest[1]), (rest[1], rest[0])]:
                rhs += 8*fs[i]*fs[j]*fs[k]*fs[l]*contraction(I4, gg[k], gg[l])
        assert lhs == rhs, f"familia conforme falhou seed={seed}"

def test_sqrt_det():
    for seed in range(4):
        rng = random.Random(5000 + seed)
        H = rand_field(rng)
        eps = 1e-3
        M = tuple((1.0 if i == j else 0.0) + eps*H[4*i + j] for i in range(4) for j in range(4))
        exact = math.sqrt(abs(det4(M)))
        series = sum(sqrt_det_series(M))
        assert abs(exact - series) < 1e-9, f"sqrt(det) falhou seed={seed}"

def test_negative_control():
    rng = random.Random(6000)
    A, B = rand_field(rng), rand_field(rng)
    p, q = rand_momenta(rng, 2)
    g, zero = I4, (0, 0, 0, 0)
    bad = _eh_quartic_32k_perturbed(g, zero, g, zero, A, p, B, q)
    assert bad != 8*eh_quadratic_8k(A, p, B, q), "controle negativo NAO morde"

def test_zero_field():
    rng = random.Random(7000)
    A, B, C = rand_field(rng), rand_field(rng), rand_field(rng)
    p, q, r = rand_momenta(rng, 3)
    Z = tuple(0 for _ in range(16))
    assert eh_quartic_32k(Z, (0, 0, 0, 0), A, p, B, q, C, r) == 0

if __name__ == "__main__":
    for name, fn in [("bose", test_bose), ("gg_contraction", test_gg_contraction),
                     ("ward_v4_v3", test_ward), ("conformal_family", test_conformal),
                     ("sqrt_det_series", test_sqrt_det),
                     ("negative_control", test_negative_control),
                     ("zero_field", test_zero_field)]:
        fn()
        print(f"OK  {name}")
    print(f"annex_imported = {_ANNEX}")
```

## 3. Explicação dos fatores e das verificações

- **Normalização 32κ:** R_n = 2^{n+1}κ·ℒ_n, com ℒ_n = −(1/2κ)·ℒ_n^raw. O cúbico do anexo foi reproduzido termo a termo por esta regra antes de fixar a do quártico (coeficientes −2 e +trace do anexo batem com −8·ℒ₃^raw).
- **Bose:** o vértice é invariante sob as 24 permutações de (campo, momento) — testado com entradas inteiras, igualdade exata.
- **g,g a momento zero:** resultado central, verificado contra o `eh_quadratic_8k` do próprio anexo (quando importável). Não é zero; é 8× o núcleo quadrático. Não confundir com a Hessiana interagente — este é o vértice local; a bolha efetiva monta-se com propagadores em outra unidade.
- **Família conforme G = (1+f)g:** forma fechada (1+F)²·(1+F)⁻³ = (1+F)⁻¹ — os três fatores de inversa e o √det conspiram; o teste compara o vértice montado peça a peça contra essa forma fechada, com f's inteiros. É a verificação conjunta das três inversas + determinante.
- **Ward clássica V4↔V3:** de δ₀ℒ₄ + δ₁ℒ₃ = borda (δ₀h = L_v g, δ₁h = L_v h), com conservação de momento e cutoff constante (borda = 0): `R4(A,B,C, L_v g) + 2·Σ_i R3(…, L_v h_i, …) = 0`, testada contra o `eh_cubic_16k` do anexo. Nenhuma transversalidade foi imposta ao diagrama isolado.
- **Bordas descartadas:** na passagem EH→Γ-Γ+potencial, `∂_ρ[√G(G^{μν}C^ρ_{μν} − G^{μρ}C^λ_{μλ})]`, usando ∇_ρ(√G G^{μν}) = √G[C^λ_{ρλ}G^{μν} − C^μ_{ρλ}G^{λν} − C^ν_{ρλ}G^{μλ}]. O descarte exige **cutoff constante** (caixa periódica); em momentos, a borda é ∝ (momento total)·B e morre por conservação. Os termos de contato associados não são apagados da missão — ficam para as unidades de contatos/BV.
- **Controle negativo:** a variante com um coeficiente perturbado (4→3) falha o teste g,g (dá −4×, não 8×) — o teste morde.

## 4. Escopo, honestidade e lacunas

- **Não executei** o código nesta sessão; todos os resultados de modelo são [DECLARADO até auditoria local]. A contração g,g = 8× está derivada algebricamente na seção 1, passo a passo; se algum teste falhar na sua máquina, a falha está na minha montagem, não nos controles — reportar, não remendar.
- **Fora desta unidade:** correções de conexão de fundo nos γ's (∇h = ∂h − Γ(g)h); o potencial (Ric(g), Λ) — coberto pelo DERIVACAO.md anexo; a montagem com propagadores (bolhas/tadpoles efetivos); contatos BV; Q2. O fator K do espaço-forma não entra nesta peça de duas derivadas em momento.
- **Não ajustei** o vértice para cancelar anomalia alguma; **não impus** transversalidade; **não tentei** Q2 completa. Nenhum arquivo canônico, kernel ou gate foi alterado — esta resposta é texto, e o código é entregue como artefato a compilar pela auditoria local.