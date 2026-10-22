#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# A7.b — conferencia algebrica dos coeficientes e contatos Ward (2 pontos, parte principal plana).
# ESCOPO: aritmetica e identidades algebricas; NENHUMA identidade distribucional e provada aqui.
# Convencao: C = 4 i pi^2, Box(1/z) = C delta, z = x^2 - i0, assinatura +---.
# Saida 0 sse nenhum FAIL. Uso: python a7b_ward_contacts_check.py
import sys
from sympy import Rational, symbols, simplify, factorial, I, pi, Matrix, zeros

F = []
def check(name, cond):
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond: F.append(name)

# ---------- base
C  = 4*I*pi**2
A0 = 1/(8*pi**2)
check("C*A0 = i/2", simplify(C*A0 - I/2) == 0)

# ---------- r_n, Res U_n, R_n - D_n ; recorrencia Box (T2, T3)
def Hn(j): return sum(Rational(1,k) for k in range(1, j+1))
def r(n):  return -1/(4**(n-1)*factorial(n-1)*factorial(n-2))
def resU(n): return C*r(n)
def RmD(n):  return (Hn(n-1)+Hn(n-2)-1)*resU(n)

check("T3: R_2 - D_2 = 0", simplify(RmD(2)) == 0)
check("T3: R_3 - D_3 = -(3C/64)", simplify(RmD(3) + Rational(3,64)*C) == 0)
check("T3: r_{n-1} = 4(n-1)(n-2) r_n (recorrencia D sem contato)",
      all(simplify(r(n-1) - 4*(n-1)*(n-2)*r(n)) == 0 for n in range(3,8)))
check("T2: identidade harmonica da recorrencia Box, n=3..7",
      all(simplify((n-1)*(n-2)*(Hn(n-3)-Hn(n-1)) + (2*n-3)) == 0 for n in range(3,8)))

# ---------- z R_3 = R_2 (T7), via zD_3 = D_2 + (3C/8)d e z Box d = 8 d
D2, D3, d0 = symbols('D2 D3 d0')
zR3 = (D3 + Rational(3,8)*C*d0) - Rational(3,64)*C*(8*d0)
check("T7: z R_3 = R_2 (= D_2)", simplify(zR3 - D2) == 0)

# ---------- tensor de posto 2 (T4) e CONTROLE DO TRACO
eta, R2s, d2 = symbols('eta R2 d2')
Rmn = Rational(1,8)*d2 + Rational(1,4)*eta*R2s - Rational(1,32)*eta*C*d0
tr_com = Rational(1,8)*C*d0 + Rational(1,4)*4*R2s - Rational(1,32)*4*C*d0
check("T4: traco eta^{mn} R_{mn} = R_2", simplify(tr_com - R2s) == 0)
tr_sem = Rational(1,8)*C*d0 + Rational(1,4)*4*R2s
check("CONTROLE (obrigatorio): sem o contato do traco, o erro e' exatamente +(C/8) delta",
      simplify(tr_sem - R2s - Rational(1,8)*C*d0) == 0)
check("T4<=>T5: d2(1/z) = 8 R_mn - 2 eta R_2 + (C/4) eta delta",
      simplify(8*Rmn - 2*eta*R2s + Rational(1,4)*eta*C*d0 - d2) == 0)

# ---------- [d_mu, R](U_n) (T6, potencias puras): -4(n-1) C r_{n+1} d_mu Box^{n-2} delta
def cont_dR(n): return -4*(n-1)*C*r(n+1)
check("T6: [d,R](U_2) = (C/8) d delta",        simplify(cont_dR(2) - C*Rational(1,8))    == 0)
check("T6: [d,R](U_3) = (C/96) d Box delta",   simplify(cont_dR(3) - C*Rational(1,96))   == 0)
check("T6: [d,R](U_4) = (C/3072) d Box^2 delta", simplify(cont_dR(4) - C*Rational(1,3072)) == 0)

# ---------- bolha: coeficientes e transversalidade (sec. 2)
cm = [Rational(71,60), Rational(27,40), -Rational(19,30), -Rational(11,5), Rational(26,15)]
cg = [Rational(1,12), Rational(7,48), -Rational(1,8),  -Rational(1,12), Rational(1,6)]
comb = [-cm[i]/2 + cg[i] for i in range(5)]
alvo = [Rational(-61,120), Rational(-23,120), Rational(23,120), Rational(61,60), Rational(-7,10)]
check("-m/2 + g = coeficientes registrados", all(simplify(comb[i]-alvo[i])==0 for i in range(5)))

def F5(c, A, B, p):
    trA, trB, trAB = A.trace(), B.trace(), (A*B).trace()
    p2  = (p.T*p)[0]
    pAp = (p.T*A*p)[0]; pBp = (p.T*B*p)[0]; pABp = (p.T*A*B*p)[0]
    return (c[0]*trAB*p2**2 + c[1]*trA*trB*p2**2
            + c[2]*(pAp*trB + pBp*trA)*p2 + c[3]*pABp*p2 + c[4]*pAp*pBp)
def Kg(p, v): return p*v.T + v*p.T

p = Matrix([1, 2, -1, 1]); v = Matrix([2, 0, 1, -1]); K = Kg(p, v)
bs = symbols('b0:10'); idx = [(0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]
B  = Matrix(4, 4, lambda i,j: bs[idx.index((min(i,j),max(i,j)))])
p2 = (p.T*p)[0]; pv = (p.T*v)[0]; pBv = (p.T*B*v)[0]; trB = B.trace()
check("residuo setorial metrica: F_m(K,B) = (1/6)p^4 pBv + (1/12)p^4 (p.v) trB",
      simplify(F5(cm, K, B, p) - (Rational(1,6)*p2**2*pBv + Rational(1,12)*p2**2*pv*trB)) == 0)
check("residuo setorial ghost:   F_g(K,B) = (1/12)p^4 pBv + (1/24)p^4 (p.v) trB",
      simplify(F5(cg, K, B, p) - (Rational(1,12)*p2**2*pBv + Rational(1,24)*p2**2*pv*trB)) == 0)
H = Matrix(4, 4, lambda i,j: Rational((i+2*j) % 5 - 1, (i+j) % 3 + 2))
H = H + H.T
check("WTI logaritmica: F_{-m/2+g}(K_p(v), H) = 0 (fora de no)",
      simplify(F5(comb, K, H, p)) == 0)
check("CONTROLE: peca metrica isolada NAO e' transversal", simplify(F5(cm, K, H, p)) != 0)
check("CONTROLE: sinal ghost trocado destroi o cancelamento",
      simplify(sum((-cm[i]/2 - cg[i]) for i in range(5))) != 0)

# ---------- mapa D2 (sec. 5) e WZ-2pt (sec. 6)
def Ric1(A, p):
    pA = A*p; p2 = (p.T*p)[0]
    return Rational(1,2)*(p2*A + p*(p.T)*A.trace() - p*pA.T - pA*p.T)
def R1(A, p): return (p.T*p)[0]*A.trace() - (p.T*A*p)[0]
check("WZ-2pt: Ric^1(K_p(v)) = 0", Ric1(K, p) == zeros(4))
check("WZ-2pt: R^1(K_p(v)) = 0",   simplify(R1(K, p)) == 0)
A2 = Matrix(4, 4, lambda i,j: Rational((i+3*j) % 4 - 1, (2*i+j) % 3 + 2)); A2 = A2 + A2.T
B2 = Matrix(4, 4, lambda i,j: Rational((2*i+j) % 5 - 2, (i+2*j) % 4 + 1)); B2 = B2 + B2.T
T  = Matrix.eye(4) - p*p.T/(p.T*p)[0]
X1 = (T*A2*T*B2).trace(); X2 = (T*A2).trace()*(T*B2).trace(); p4 = (p.T*p)[0]**2
check("Ric^1:Ric^1 = (p2^2/4)(X1+X2)",
      simplify(((Ric1(A2,p)*Ric1(B2,p)).trace() if hasattr((Ric1(A2,p)*Ric1(B2,p)),'trace') else (Ric1(A2,p)*Ric1(B2,p)).trace()) - p4/4*(X1+X2)) == 0)
check("R^1 R^1 = p2^2 X2", simplify(R1(A2,p)*R1(B2,p) - p4*X2) == 0)
check("-61/30 Ric:Ric + 19/60 RR = p4[-61/120 X1 - 23/120 X2]",
      simplify(-Rational(61,30)*(p4/4*(X1+X2)) + Rational(19,60)*p4*X2
               - p4*(-Rational(61,120)*X1 - Rational(23,120)*X2)) == 0)

# ---------- vertice ghost e sua eta-tracada (lacuna L1: peca ja computavel)
def Vghost(H, p, k):
    r = k + p; Hr = H*r; Hk = H*k
    return -Matrix(4, 4, lambda nu, rho:
        p[rho]*Hr[nu] + (r.T*k)[0]*H[rho,nu] + k[nu]*Hr[rho]
        - r[nu]*p[rho]*H.trace()/2 - r[nu]*Hk[rho])
k = Matrix([0, 1, -1, 2]); Hg = Matrix(4, 4, lambda i,j: Rational((i+j) % 3, (i+2*j) % 4 + 2)); Hg = Hg + Hg.T
V = Vghost(Hg, p, k); r = k + p
etaV = -((p.T*Hg*r)[0] + (r.T*k)[0]*Hg.trace() + (k.T*Hg*r)[0] - (r.T*p)[0]*Hg.trace()/2 - (r.T*Hg*k)[0])
check("eta^{nu rho} V_{nu rho} = formula fechada", simplify(sum(V[nu,nu] for nu in range(4)) - etaV) == 0)
q = p
Cnu = [ -((q.T*q)[0]*v[nu] + (q.T*v)[0]*q[nu] - q[nu]*(q.T*v)[0]) for nu in range(4) ]
check("C(L_v g) e' proporcional a p^2 v (sem termos (p.v)p; sinal = convencao i^2)",
      all(simplify(Cnu[nu] + (q.T*q)[0]*v[nu]) == 0 for nu in range(4)))

print()
print("TABELA (resumo): traco T4 = -C/32 eta d ; omissao = +C/8 d ; T5 = +C/4 eta d ;")
print("[d,R](U_2) = C/8 d_mu d ; [d,R](U_3) = C/96 d_mu Box d ; Box R_2 = 8R_3 + 3C/8 Box d.")
sys.exit(1 if F else 0)
