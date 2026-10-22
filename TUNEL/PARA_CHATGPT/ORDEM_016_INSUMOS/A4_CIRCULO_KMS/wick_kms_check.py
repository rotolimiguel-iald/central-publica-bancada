# Checagem simbolica [KNOWN reproduzido]: a ponte face->leitura (Wick) e a regularidade conica.
import sympy as sp
phi, x, tE, kap, r, c = sp.symbols('phi x t_E kappa r c', real=True)
s = sp.I*phi
B = sp.Matrix([[sp.cosh(s), sp.sinh(s)], [sp.sinh(s), sp.cosh(s)]])   # boost do kernel (BisognanoWichmann.boost), rapidez imaginaria
W = sp.diag(1, -sp.I)                                                   # t = -i t_E  (coordenadas (x,t) -> (x,t_E))
Rot = sp.simplify(W.inv()*B*W)
print("W^-1 boost(i phi) W =", Rot)
G = sp.Matrix([[0,1],[-1,0]])
print("igual a exp(phi*[[0,1],[-1,0]]):", sp.simplify(Rot - (phi*G).exp()) == sp.zeros(2))
print("periodo: Rot(2pi) = 1:", sp.simplify(Rot.subs(phi, 2*sp.pi)) == sp.eye(2))
# Regularidade conica: ds^2 = dr^2 + kappa^2 r^2 dtau^2, tau ~ tau + P. Angulo total = kappa*P; liso sse kappa*P = 2 pi.
P = sp.symbols('P', positive=True)
print("periodo liso P =", sp.solve(sp.Eq(kap*P, 2*sp.pi), P), " => T = 1/P =", sp.simplify(1/sp.solve(sp.Eq(kap*P, 2*sp.pi), P)[0]))
# Covariancia de escala: xi -> c xi  => kappa -> c kappa, T -> c T, E_Killing -> c E ; Boltzmann E/T invariante
E = sp.symbols('E', real=True)
print("E/T invariante sob xi->c xi:", sp.simplify((c*E)/(c*kap/(2*sp.pi)) - E/(kap/(2*sp.pi))) == 0)
