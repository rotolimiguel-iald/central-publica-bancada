"""Independent Leaver (1985) continued-fraction solver, Kerr s=-2, l=m=2, n=0.
Units 2M=1 internally; returns M*omega (M=1). Auditor's own code, no house/bancada import."""
import numpy as np, math, json

def cf(alpha, beta, gamma, N=400):
    # value of beta0 - alpha0*gamma1/(beta1 - alpha1*gamma2/(beta2 - ...)) evaluated bottom-up
    val = beta(N)
    for n in range(N-1, -1, -1):
        val = beta(n) - alpha(n)*gamma(n+1)/val
    return val

def angular_A(c, s=-2, m=2, A0=4.0+0j):
    k1 = abs(m-s)/2; k2 = abs(m+s)/2
    def F(A):
        a_ = lambda n: -2*(n+1)*(n+2*k1+1)
        b_ = lambda n: n*(n-1) + 2*n*(k1+k2+1-2*c) - (2*c*(2*k1+s+1) - (k1+k2)*(k1+k2+1)) - (c*c + s*(s+1) + A)
        g_ = lambda n: 2*c*(n+k1+k2+s)
        return cf(a_, b_, g_, 200)
    A = A0
    for _ in range(100):
        h = 1e-7*(1+abs(A))
        f = F(A); df = (F(A+h)-f)/h
        dA = f/df; A -= dA
        if abs(dA) < 1e-14*(1+abs(A)): break
    return A

def radial(w, a, s=-2, m=2, A0=4.0+0j):
    # a in 2M=1 units (0<=a<1/2), w Leaver frequency
    A = angular_A(a*w, s, m, A0)
    b = math.sqrt(1-4*a*a)
    t = (w/2 - a*m)
    c0 = 1 - s - 1j*w - (2j/b)*t
    c1 = -4 + 2j*w*(2+b) + (4j/b)*t
    c2 = s + 3 - 3j*w - (2j/b)*t
    c3 = w*w*(4+2*b-a*a) - 2*a*m*w - s - 1 + (2+b)*1j*w - A + ((4*w+2j)/b)*t
    c4 = s + 1 - 2*w*w - (2*s+3)*1j*w - ((4*w+2j)/b)*t
    al = lambda n: n*n + (c0+1)*n + c0
    be = lambda n: -2*n*n + (c1+2)*n + c3
    ga = lambda n: n*n + (c2-3)*n + c4 - c2 + 2
    return cf(al, be, ga, 600), A

def qnm220(chi, guess=None):
    a = chi/2.0
    w = guess if guess is not None else 2*(0.3737-0.0890j)
    A0 = 4.0+0j
    for _ in range(200):
        f, A = radial(w, a, A0=A0); A0 = A
        h = 1e-7
        f2, _ = radial(w+h, a, A0=A0)
        dw = f/((f2-f)/h); w -= dw
        if abs(dw) < 1e-13: break
    return w/2.0  # M*omega with M=1

if __name__ == '__main__':
    out = {}
    g = None
    # march in spin from 0 for continuity
    targets = [0.0, 0.67122, 0.6712194217379245, 0.68, 0.6784704444609746, 0.7, 0.9]
    grid = np.linspace(0, 0.9, 91).tolist()
    pts = sorted(set(grid + targets))
    for chi in pts:
        Mw = qnm220(chi, None if g is None else 2*g)
        g = Mw
        if any(abs(chi-t) < 1e-15 for t in targets):
            out[repr(chi)] = [Mw.real, Mw.imag]
            print(chi, Mw)
    json.dump(out, open(__file__.replace('leaver.py', 'leaver_out.json'), 'w'), indent=1)
