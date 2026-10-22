# -*- coding: utf-8 -*-
"""
V1 - verificador matematico independente da «equacao da verdade» (texto do canal ChatGPT,
colado pelo operador em 23/09/2026). Aritmetica EXATA (sympy Rational + simbolo s).
T_s = exp(-sH) e construido por DIAGONALIZACAO EXATA (autovalores inteiros, projetores
espectrais racionais) e conferido (a) pela EDO dT/ds = -H T, T_0 = I (unicidade => T = exp(-sH))
e (b) pela serie de Taylor em s, coeficiente a coeficiente, ate ordem 12 (igualdade exata).
Num segundo exemplo generico (espectro irracional) usa-se a serie TRUNCADA: P*S_N = P vale
EXATAMENTE para todo N (o resto nao importa para P T_s, porque P H = 0).
Nao executa um.py, nao toca kernel Lean. Escreve so nesta pasta.
"""
import json, sys, itertools, random, hashlib, os
import sympy as sp
from sympy import Rational as R, Matrix, eye, zeros, exp, log, sqrt, symbols, simplify, diff, limit, oo

OUT = os.path.dirname(os.path.abspath(__file__))
checks, controls = [], []

def ck(name, ok, detail=""):
    checks.append({"id": len(checks) + 1, "nome": name, "ok": bool(ok), "detalhe": str(detail)})
    print(("PASS " if ok else "FAIL ") + f"[C{len(checks):02d}] {name} {detail}")

def ctrl(name, must_fail_property_holds, detail=""):
    # must_fail_property_holds = valor da propriedade que o controle TEM de violar.
    detected = not bool(must_fail_property_holds)
    controls.append({"id": len(controls) + 1, "nome": name, "propriedade_vale": bool(must_fail_property_holds),
                     "falha_detectada": detected, "detalhe": str(detail)})
    print(("DETECTADO " if detected else "NAO DETECTADO ") + f"[N{len(controls):02d}] {name} {detail}")

s, t = symbols('s t', real=True, nonnegative=True)
X = Matrix(symbols('x1:6'))  # vetor simbolico generico em Q^5 (real)

# ---------------- Secao 1: V(b, bh) = 1 - (b - bh)^2 ----------------
V = lambda b, bh: 1 - (b - bh) ** 2
tab = {(b, bh): V(b, bh) for b in (0, 1) for bh in (0, 1)}
ck("S1 tabela V(1,1)=V(0,0)=1, V(1,0)=V(0,1)=0", tab == {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 1}, tab)
ck("S1 V(b,bh) == [b == bh] em {0,1}^2 (coincide com o indicador V_r)",
   all(V(b, bh) == (1 if b == bh else 0) for b in (0, 1) for bh in (0, 1)))

# ---------------- Secao 2: exemplo exato em dimensao 5 ----------------
def gs(vs):  # Gram-Schmidt racional sem normalizar
    out = []
    for v in vs:
        w = Matrix(v)
        for u in out:
            w = w - (u.dot(w) / u.dot(u)) * u
        out.append(w)
    return out

u1, u2, u3 = gs([[1, 2, 0, -1, 1], [2, -1, 1, 0, 0], [0, 1, 1, 1, 2]])
u3 = u3 * sp.ilcm(*[sp.fraction(e)[1] for e in u3])  # inteiro
assert u1.dot(u2) == 0 and u1.dot(u3) == 0 and u2.dot(u3) == 0
D1 = Matrix.vstack(u1.T, 2 * u1.T)             # 2x5, posto 1
D2 = u2.T                                      # 1x5
D3 = Matrix.vstack(u3.T, u3.T, zeros(1, 5))    # 3x5, posto 1
Ds = [D1, D2, D3]
H = sum((D.T * D for D in Ds), zeros(5, 5))
AC = -H
E = [u * u.T / u.dot(u) for u in (u1, u2, u3)]
lam = [5 * u1.dot(u1), u2.dot(u2), 2 * u3.dot(u3)]
print("u1,u2,u3 =", list(u1), list(u2), list(u3), " lambdas =", lam)

kers = [Matrix.hstack(*D.nullspace()) for D in Ds]
ck("S2 cada ker D_j sozinho tem dimensao 4 (nenhum vinculo isolado fixa a familia)",
   all(k.shape[1] == 4 for k in kers), [k.shape[1] for k in kers])
Dstack = Matrix.vstack(*Ds)
Fb = Matrix.hstack(*Dstack.nullspace())
ck("S2 dim (ker D1 ∩ ker D2 ∩ ker D3) = 2", Fb.shape[1] == 2, Fb.shape)
KH = Matrix.hstack(*H.nullspace())
same = (KH.shape[1] == 2 and Matrix.hstack(KH, Fb).rank() == 2)
ck("S2 ker H_3L = ∩ ker D_j (mesmo subespaco)", same)
qf = sp.expand((X.T * H * X)[0] - sum(((D * X).T * (D * X))[0] for D in Ds))
ck("S2 <x,Hx> = Σ||D_j x||^2 identicamente (x simbolico)", qf == 0)
ck("S2 H simetrico (auto-adjunto real)", H == H.T)
evH = H.eigenvals()
ck("S2 espectro de H exato, >= 0: {0^2, 35, 6, 2|u3|^2}", all(k >= 0 for k in evH) and evH.get(0, 0) == 2, evH)
ck("S2 A_C = -H <= 0 (todos autovalores <= 0)", all(k <= 0 for k in AC.eigenvals()))
P = Fb * (Fb.T * Fb).inv() * Fb.T
Q = eye(5) - P
ck("S2 P^2=P, P^T=P, posto 2, Im P = F", P * P == P and P.T == P and P.rank() == 2 and Matrix.hstack(P, Fb).rank() == 2)
ck("S2 0 != P != I", P != zeros(5, 5) and P != eye(5))
ck("S2 H P = 0 e P H = 0", H * P == zeros(5, 5) and P * H == zeros(5, 5))
ck("S2 P + ΣE_k = I e H = Σ λ_k E_k (diagonalizacao exata)",
   P + E[0] + E[1] + E[2] == eye(5) and H == sum((l * e for l, e in zip(lam, E)), zeros(5, 5)))
T = lambda ss: P + sum((exp(-ss * l) * e for l, e in zip(lam, E)), zeros(5, 5))
Ts = T(s)
ck("S2 T_0 = I", sp.simplify(T(0) - eye(5)) == zeros(5, 5))
ck("S2 dT/ds = -H T_s = A_C T_s (EDO => T_s = exp(-sH) por unicidade)",
   sp.simplify(diff(Ts, s) + H * Ts) == zeros(5, 5))
N = 12
ser_ok = True
for n in range(N + 1):
    cn = sp.simplify(diff(Ts, s, n).subs(s, 0) / sp.factorial(n))
    if cn != ((-H) ** n) / sp.factorial(n):
        ser_ok = False; break
ck(f"S2 serie de Taylor de T_s em s = Σ(-sH)^n/n! coeficiente a coeficiente ate n={N}", ser_ok)
ck("S2 semigrupo T_s T_t = T_{s+t}", sp.simplify(T(s) * T(t) - T(s + t)) == zeros(5, 5))
ck("S2 P T_s = P (s simbolico)", sp.simplify(P * Ts - P) == zeros(5, 5))
ck("S2 T_s P = P e T_s Q = Q T_s", sp.simplify(Ts * P - P) == zeros(5, 5) and sp.simplify(Ts * Q - Q * Ts) == zeros(5, 5))
ck("S2 I(T_s x) = I(x) com I = P, x simbolico", sp.simplify(P * Ts * X - P * X) == zeros(5, 1))
x0 = Matrix([1, 0, 0, 0, 0])
ck("S2 T_s x = Px + T_s Q x", sp.simplify(Ts * X - (P * X + Ts * Q * X)) == zeros(5, 1))
ck("S2 T_1 x0 != x0 para x0 = e1 (Q x0 != 0) mas P T_1 x0 = P x0",
   Q * x0 != zeros(5, 1) and sp.simplify(T(1) * x0 - x0) != zeros(5, 1) and sp.simplify(P * T(1) * x0 - P * x0) == zeros(5, 1))

# exemplo generico (espectro irracional): serie truncada exata
random.seed(20260923)
C = Matrix([list(u1), list(u2), list(u3)])  # linhas = base de F^perp
Dg = [Matrix(2, 3, lambda i, j: random.randint(-3, 3)) * C for _ in range(3)]
Hg = sum((D.T * D for D in Dg), zeros(5, 5))
Fg = Matrix.hstack(*Matrix.vstack(*Dg).nullspace())
Pg = Fg * (Fg.T * Fg).inv() * Fg.T
cp = Hg.charpoly().as_expr()
okS = all(Pg * sum((((-s * Hg) ** n) / sp.factorial(n) for n in range(Nn + 1)), zeros(5, 5)) - Pg == zeros(5, 5)
          for Nn in range(0, 16))
ck("S2' exemplo generico (D_j aleatorios racionais, polinomio caract. " + str(sp.factor_list(cp)[1][-1][0].as_poly().degree()) +
   "o grau irredutivel): ker Hg = ∩ker, Pg Hg = 0, e Pg·S_N = Pg EXATO p/ N=0..15",
   Matrix.hstack(*Hg.nullspace()).shape[1] == Fg.shape[1] and Pg * Hg == zeros(5, 5) and okS, sp.factor(cp))

# ---------------- Secao 3: limite e reciproca ----------------
lim = Ts.applyfunc(lambda e: limit(e, s, oo))
ck("S3 lim_{s->oo} T_s = P (entrada a entrada)", sp.simplify(lim - P) == zeros(5, 5))
lmin = min(lam)
# ||T_s - P||_op = max_k e^{-s λ_k} = e^{-s λmin} (T_s-P = Σ e^{-sλ_k}E_k, E_k ortogonais)
ck("S3 ||T_s - P||_op = e^{-s·λ_min+}, λ_min+ = %s (taxa = gap espectral)" % lmin,
   set(sp.simplify(k) for k in (T(1) - P).eigenvals().keys()) == {0, exp(-lam[0]), exp(-lam[1]), exp(-lam[2])})
l1 = lambda v: sp.simplify((P * v).dot(P * v))   # continuo, fatora por P
ck("S3 leitor continuo ℓ(x)=||Px||^2: ℓ(T_s x)=ℓ(x) e ℓ=ℓ∘P", sp.simplify(l1(Ts * X) - l1(X)) == 0 and sp.simplify(l1(P * X) - l1(X)) == 0)
l2 = lambda v: sp.simplify(v.dot(v))              # continuo, NAO fatora
ck("S3 coerencia da reciproca: ℓ(x)=||x||^2 nao fatora por P e NAO e conservado",
   sp.simplify(l2(P * x0) - l2(x0)) != 0 and sp.simplify(l2(T(1) * x0) - l2(x0)) != 0)
s0 = R(1, 3)
l_inv_s0 = sp.simplify(((T(s0) ** 3) - T(1)))
ck("S3 semigrupo discreto T_{s0}^n = T_{n s0} (base do reforco: invariancia num unico s0>0 ja implica ℓ=ℓ∘P)", l_inv_s0 == zeros(5, 5))
nn = symbols('n', positive=True, integer=True)
ck("S3 ∞-dim sem gap (H=diag(1/n) em l2, ker=0, P=0): e^{-s/n}->0 p/ n fixo (forte) mas sup_n e^{-s/n}=1 (norma NAO converge)",
   limit(exp(-R(7)/nn), nn, oo) == 1 and limit(exp(-s / 3), s, oo) == 0)

# ---------------- Secao 4 ----------------
ck("S4 P^n = P para n=1..8", all(P ** n == P for n in range(1, 9)))
fixb = Matrix.hstack(*(P - eye(5)).nullspace())
ck("S4 Fix P = Im P = F", fixb.shape[1] == 2 and Matrix.hstack(fixb, Fb).rank() == 2)
random.seed(7)
ok4 = True
for _ in range(40):
    a = Matrix([R(random.randint(-5, 5), random.randint(1, 4)) for _ in range(5)])
    b = a + (Q * Matrix([random.randint(-3, 3) for _ in range(5)]) if random.random() < .5 else Matrix([random.randint(-3, 3) for _ in range(5)]))
    lhs = (P * a == P * b); rhs = (P * (a - b) == zeros(5, 1))
    ok4 &= (lhs == rhs)
ck("S4 Px = Py <=> x - y ∈ ker P (40 pares racionais)", ok4)
ck("S4 ker P = Q H = F^perp (dim 3)", Matrix.hstack(*P.nullspace()).shape[1] == 3 and Matrix.hstack(*P.nullspace(), u1, u2, u3).rank() == 3)

# ---------------- Secao 5 ----------------
ck("S5 d/ds P T_s x = P A_C T_s x = 0", sp.simplify(diff(P * Ts * X, s)) == zeros(5, 1) and sp.simplify(P * AC * Ts * X) == zeros(5, 1))
dT0 = sp.simplify(diff(Ts * x0, s))
ck("S5 d/ds T_s x0 != 0 para x0 ∉ F (dinamica nao nula)", dT0 != zeros(5, 1))
z = Fb[:, 0]
ck("S5 z ∈ F => Pz = z e T_s z = z", P * z == z and sp.simplify(Ts * z - z) == zeros(5, 1))
chi = symbols('chi', real=True)
a = sp.sech(chi / 2); q = sp.tanh(chi / 2)
ck("S5 a' = -(1/2) a q", sp.simplify((diff(a, chi) + a * q / 2).rewrite(sp.exp)) == 0)
ck("S5 q' = (1/2) a^2", sp.simplify((diff(q, chi) - a ** 2 / 2).rewrite(sp.exp)) == 0)
vals = (diff(a, chi).subs(chi, 0), diff(q, chi).subs(chi, 0), sp.simplify(diff(a, chi, 2).subs(chi, 0)))
ck("S5 a'(0)=0, q'(0)=1/2, a''(0)=-1/4", vals == (0, R(1, 2), R(-1, 4)), vals)
ck("S5 a^2 + q^2 = 1 (tanh^2 + sech^2)", sp.simplify((a ** 2 + q ** 2 - 1).rewrite(sp.exp)) == 0)
ck("S5 extremos: P=0 => leitura constante; P=I (H=0) => T_s = I",
   (zeros(5, 5) * X) == zeros(5, 1) and sp.simplify((-s * zeros(5, 5)).exp() - eye(5)) == zeros(5, 5))

# ---------------- Secao 6: qubit ----------------
p = symbols('p', positive=True); k = symbols('k', nonnegative=True)  # k = |c|^2
cr = symbols('c', real=True)  # c real (fase de c nao altera espectro nem entropia)
rho = Matrix([[p, cr * exp(-s)], [cr * exp(-s), 1 - p]])
sig = Matrix([[p, 0], [0, 1 - p]])
Epin = lambda M: Matrix([[M[0, 0], 0], [0, M[1, 1]]])
ck("S6 E ρ_s = σ (constante)", sp.simplify(Epin(rho) - sig) == zeros(2, 2))
ck("S6 dρ/ds = -(id - E)ρ_s", sp.simplify(diff(rho, s) + (rho - Epin(rho))) == zeros(2, 2))
r = sqrt((2 * p - 1) ** 2 + 4 * cr ** 2 * exp(-2 * s))
ev = list(rho.eigenvals().keys())
ck("S6 autovalores = (1 ± r_s)/2", all(sp.simplify(sp.expand((e - R(1, 2)) ** 2 - r ** 2 / 4)) == 0 for e in ev))
# superoperador em vec(ρ) (base E11,E12,E21,E22): E = diag(1,0,0,1)
Esup = sp.diag(1, 0, 0, 1)
ck("S6 E e projecao ORTOGONAL em Hilbert-Schmidt e e^{sL} = E + e^{-s}(id-E) (instancia da secao 2 com H = id-E = D†D)",
   Esup * Esup == Esup and Esup.T == Esup and sp.simplify((-(s) * (eye(4) - Esup)).exp() - (Esup + exp(-s) * (eye(4) - Esup))) == zeros(4, 4))
rr = symbols('r', positive=True)
Sofr = -((1 + rr) / 2 * log((1 + rr) / 2) + (1 - rr) / 2 * log((1 - rr) / 2))
dSds = diff(Sofr, rr).subs(rr, r) * diff(r, s)
claimed = 2 * cr ** 2 * exp(-2 * s) / r * log((1 + r) / (1 - r))
diffexpr = sp.simplify(sp.expand_log(dSds - claimed, force=True))
ck("S6 dS/ds = 2|c|^2 e^{-2s}/r_s · log((1+r_s)/(1-r_s)) (simbolico)", diffexpr == 0, diffexpr)
# positividade e r<1: r^2 < 1 <=> c^2 e^{-2s} < p(1-p)
ck("S6 r_s^2 < 1 <=> |c|^2 e^{-2s} < p(1-p) (logo log((1+r)/(1-r)) >= 0 e dS/ds >= 0)",
   sp.expand((1 - r ** 2) - 4 * (p * (1 - p) - cr ** 2 * exp(-2 * s))) == 0)
# checagem numerica de alta precisao em pontos racionais
import mpmath as mp
mp.mp.dps = 50
okn = True
for (pp, cc) in [(R(1, 3), R(1, 5)), (R(1, 2), R(1, 4)), (R(9, 10), R(1, 10)), (R(1, 7), R(1, 3))]:
    assert cc ** 2 < pp * (1 - pp)
    for ss in [R(0), R(1, 2), R(2), R(5)]:
        def Snum(x):
            rv = mp.sqrt((2 * mp.mpf(pp) - 1) ** 2 + 4 * mp.mpf(cc) ** 2 * mp.e ** (-2 * x))
            l1_, l2_ = (1 + rv) / 2, (1 - rv) / 2
            return -(l1_ * mp.log(l1_) + l2_ * mp.log(l2_))
        dnum = mp.diff(Snum, mp.mpf(ss))
        cl = claimed.subs({p: pp, cr: cc, s: ss})
        okn &= abs(dnum - mp.mpf(sp.N(cl, 60))) < mp.mpf(10) ** -35 and dnum >= 0
ck("S6 dS/ds numerico (50 dig.) = formula e >= 0 em 16 pontos", okn)
# D(ρ||σ) = S(σ) - S(ρ): -Tr ρ log σ = -Σ ρ_ii log σ_ii = S(σ)
Ssig = -(p * log(p) + (1 - p) * log(1 - p))
ck("S6 -Tr(ρ_s log σ) = S(σ) (log σ diagonal, diag ρ_s = diag σ)",
   sp.simplify(-(rho[0, 0] * log(p) + rho[1, 1] * log(1 - p)) - Ssig) == 0)
# caso p=1/2: r = 2|c|e^{-s}; log((1+r)/(1-r))/r -> 2 quando r->0
ck("S6 p=1/2: limite log((1+r)/(1-r))/r -> 2 quando r->0 (extensao continua; c=0 => dS/ds=0)",
   limit(log((1 + rr) / (1 - rr)) / rr, rr, 0) == 2)
ck("S6 p=1/2, c!=0: dS/ds -> 0 quando s->oo",
   limit(claimed.subs({p: R(1, 2), cr: R(1, 4)}), s, oo) == 0)

# ======================= CONTROLES NEGATIVOS =======================
# N1: T que altera a identidade: H' = H + f f^T com f ∈ F
f = Fb[:, 0]
Hp = H + f * f.T
Tp1 = (-(1) * Hp).exp() if False else None
# exato: P T'_s x para x = f: f e autovetor de H' com autovalor |f|^2
Tpf = exp(-s * f.dot(f)) * f
ctrl("N1 T' = exp(-sH'), H' = H + f f^T (f ∈ F): P T'_s f = P f ?",
     sp.simplify(P * Tpf - P * f) == zeros(5, 1), "P T'_s f = e^{-s|f|^2} f != f")
# N2: leitor constante
l0 = lambda v: 1
y0 = Fb[:, 1]
ctrl("N2 leitor constante ℓ≡1 distingue identidades? (Px != Py mas ℓ(x)=ℓ(y))",
     (P * x0 != P * y0) and (l0(x0) != l0(y0)), "V_x(y)=1 para todo y: falso positivo de verdade")
# N3: poda que corta um modo do nucleo
g = gs([list(Fb[:, 0]), list(Fb[:, 1])])[1]
Hc = H + g * g.T
kc = Matrix.hstack(*Hc.nullspace()).shape[1]
Tcg = exp(-s * g.dot(g)) * g
ctrl("N3 poda que corta o modo g ∈ F: T_cut g = g e dim ker = 2 ?",
     kc == 2 and sp.simplify(Tcg - g) == zeros(5, 1), f"dim ker H_cut = {kc}; T_cut g = e^(-s|g|^2) g")
# N4: P nao ortogonal (obliqua) sobre F ao longo de W = span(u1+f, u2, u3)
W = Matrix.hstack(u1 + f, u2, u3)
B = Matrix.hstack(Fb, W)
Pob = B * sp.diag(1, 1, 0, 0, 0) * B.inv()
okob = (Pob * Pob == Pob) and (H * Pob == zeros(5, 5))
ctrl("N4 P obliqua (P^2=P, HP=0 valem: %s): P H = 0 e P T_s = P ?" % okob,
     (Pob * H == zeros(5, 5)) and sp.simplify(Pob * Ts - Pob) == zeros(5, 5),
     f"Pob^T == Pob: {Pob.T == Pob}; lim T_s = P != Pob: {P != Pob}")
# N5a: H INDEFINIDO quebra ker = ∩ker e a identidade da forma quadratica: H_ind = D1†D1 - D2†D2 (+0·D3†D3)
Ha = D1.T * D1 - D2.T * D2
ka = Matrix.hstack(*Ha.nullspace()).shape[1]
eva = Ha.eigenvals()
qfa = sp.expand((X.T * Ha * X)[0] - sum(((D * X).T * (D * X))[0] for D in Ds))
ctrl("N5a H_ind = D1†D1 - D2†D2 (autovalores %s): ker H_ind = ∩ker D_j (dim 2) E <x,Hx> = Σ||D_j x||^2 ?" % dict(eva),
     ka == 2 and qfa == 0 and (D3 * u3 == zeros(3, 1)), f"dim ker H_ind = {ka}; u3 ∈ ker H_ind mas D3 u3 != 0; forma quadratica difere")
# N5b: H indefinido com ker = F: P T_s = P AINDA vale, mas lim nao existe e a reciproca cai
lb = 3
Hb = lb * E[0] - lb * E[1] + 5 * E[2]
Tb = P + exp(-s * lb) * E[0] + exp(s * lb) * E[1] + exp(-5 * s) * E[2]
PTb = sp.simplify(P * Tb - P) == zeros(5, 5)
c1 = lambda v: u1.dot(v) / u1.dot(u1); c2 = lambda v: u2.dot(v) / u2.dot(u2)
lb_ = lambda v: sp.simplify(c1(v) * c2(v))
xb = u1 + u2
inv_b = sp.simplify(lb_(Tb * X) - lb_(X)) == 0
fact_b = sp.simplify(lb_(P * xb) - lb_(xb)) == 0
limb = limit(Tb[0, 0], s, oo)
ctrl("N5b H indefinido (ker=F; P T_s = P vale: %s): lim T_s existe E todo leitor continuo conservado fatora por P ?" % PTb,
     (limb.is_finite is True) and (not inv_b or fact_b),
     f"lim T_s[0,0] = {limb}; ℓ=c1·c2 conservado: {inv_b}; ℓ(Px)=ℓ(x) p/ x=u1+u2: {fact_b}")
# N6: leitor DEScontinuo conservado que nao fatora (1 se Qx != 0)
ld = lambda v, ss: 1 if sp.simplify(Q * v) != zeros(5, 1) else 0
invd = all(ld(T(ss) * x0, ss) == ld(x0, 0) for ss in [R(1, 2), 1, 3, 10])
ctrl("N6 leitor descontinuo ℓ=1_{Qx!=0}: conservado (%s) => ℓ = ℓ∘P ?" % invd,
     (not invd) or (ld(P * x0, 0) == ld(x0, 0)), "ℓ(P e1)=0 != 1=ℓ(e1): a continuidade e hipotese necessaria")
# N7: V fora de {0,1}
ctrl("N7 V(1/2,0) e V(2,0) sao valores de verdade em {0,1} ?", V(R(1, 2), 0) in (0, 1) and V(2, 0) in (0, 1),
     f"V(1/2,0)={V(R(1,2),0)}, V(2,0)={V(2,0)}")
# N8: qubit com |c|^2 > p(1-p): nao e estado
pp, cc = R(1, 2), R(3, 5)
rho0 = Matrix([[pp, cc], [cc, 1 - pp]])
ctrl("N8 qubit com |c|^2 > p(1-p): ρ_0 >= 0 e r_0 < 1 ?",
     all(e >= 0 for e in rho0.eigenvals()) and ((2 * pp - 1) ** 2 + 4 * cc ** 2) < 1, f"eig={list(rho0.eigenvals())}")

res = {"checks": checks, "controles": controls,
       "n_checks": len(checks), "n_pass": sum(c["ok"] for c in checks),
       "n_controles": len(controls), "n_detectados": sum(c["falha_detectada"] for c in controls),
       "u": [list(map(str, u1)), list(map(str, u2)), list(map(str, u3))], "lambdas": [str(l) for l in lam],
       "P": [[str(e) for e in P.row(i)] for i in range(5)],
       "metodo_T_s": "diagonalizacao exata (autovalores inteiros, projetores espectrais racionais) conferida por EDO e por serie ate ordem 12; exemplo generico: serie truncada, P S_N = P exato"}
with open(os.path.join(OUT, "resultados_V1.json"), "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
print(f"\nCHECKS {res['n_pass']}/{res['n_checks']}  CONTROLES DETECTADOS {res['n_detectados']}/{res['n_controles']}")
sys.exit(0 if res['n_pass'] == res['n_checks'] and res['n_detectados'] == res['n_controles'] else 1)
