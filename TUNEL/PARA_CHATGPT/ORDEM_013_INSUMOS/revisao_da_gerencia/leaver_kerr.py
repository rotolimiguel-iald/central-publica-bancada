# Leaver (1985) continued fractions for Kerr QNM, s=-2, l=m=2, n=0 -- independent oracle for BCW fit accuracy.
import numpy as np, sys, json
from scipy.optimize import fsolve
sys.stdout.reconfigure(encoding='utf-8')
s, l, m = -2, 2, 2
def cf(alpha, beta, gamma, N=400):
    # returns beta0 - alpha0*gamma1/(beta1 - alpha1*gamma2/(beta2 - ...))
    val = beta(N)
    for n in range(N-1, -1, -1):
        val = beta(n) - alpha(n)*gamma(n+1)/val
    return val
def angular(A, w, a):
    k1 = abs(m - s)/2; k2 = abs(m + s)/2
    al = lambda n: -2*(n+1)*(n+2*k1+1)
    be = lambda n: n*(n-1) + 2*n*(k1+k2+1-2*a*w) - (2*a*w*(2*k1+s+1) - (k1+k2)*(k1+k2+1)) - (a*a*w*w + s*(s+1) + A)
    ga = lambda n: 2*a*w*(n + k1 + k2 + s)
    return cf(al, be, ga)
def radial(w, A, a):
    b = np.sqrt(1 - 4*a*a)
    X = (w/2 - a*m)
    c0 = 1 - s - 1j*w - (2j/b)*X
    c1 = -4 + 2j*w*(2+b) + (4j/b)*X
    c2 = s + 3 - 3j*w - (2j/b)*X
    c3 = w*w*(4 + 2*b - a*a) - 2*a*m*w - s - 1 + (2+b)*1j*w - A + ((4*w + 2j)/b)*X
    c4 = s + 1 - 2*w*w - (2*s+3)*1j*w - ((4*w + 2j)/b)*X
    al = lambda n: n*n + (c0+1)*n + c0
    be = lambda n: -2*n*n + (c1+2)*n + c3
    ga = lambda n: n*n + (c2-3)*n + c4 - c2 + 2
    return cf(al, be, ga)
def solve(a, w0, A0):
    def F(x):
        w = x[0] + 1j*x[1]; A = x[2] + 1j*x[3]
        r = radial(w, A, a); t = angular(A, w, a)
        return [r.real, r.imag, t.real, t.imag]
    x = fsolve(F, [w0.real, w0.imag, A0.real, A0.imag], xtol=1e-13)
    return x[0]+1j*x[1], x[2]+1j*x[3], np.max(np.abs(F(x)))
out = {}
w = 2*(0.37367 - 0.08896j); A = 4.0 + 0j
targets = [0.0, 0.5, 0.6, 0.65, 0.671219, 0.68, 0.7, 0.8, 0.9, 0.95, 0.99]
jgrid = np.unique(np.concatenate([np.linspace(0, 0.99, 199), targets]))
for j in jgrid:
    aL = j/2
    w, A, res = solve(aL, w, A)
    if any(abs(j - t) < 1e-9 for t in targets):
        Mw = w/2   # 2M=1 units -> M*omega
        out[f'{j:.6f}'] = dict(M_omega_R=float(Mw.real), M_omega_I=float(Mw.imag), Q=float(Mw.real/(2*abs(Mw.imag))), resid=float(res))
        print(f'j={j:.6f}  M*omega = {Mw.real:.6f} {Mw.imag:+.6f}i  Q={Mw.real/(2*abs(Mw.imag)):.5f}  resid={res:.1e}')
json.dump(out, open('leaver_kerr_result.json','w'), indent=1)
