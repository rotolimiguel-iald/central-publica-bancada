"""Leaver (1985) independente: raiz radial + angular por fracao continua (2M=1), s=-2, l=m=2, n=0."""
import numpy as np, json, math
from scipy.optimize import fsolve

def cf(alpha, beta, gamma, N):
    # beta_0 - alpha_0 gamma_1/(beta_1 - alpha_1 gamma_2/(beta_2 - ...)) avaliada de tras para frente
    val = beta(N)
    for n in range(N-1, -1, -1):
        val = beta(n) - alpha(n)*gamma(n+1)/val
    return val

def angular(A, c, s=-2, m=2, N=300):
    k1 = abs(m - s)/2; k2 = abs(m + s)/2
    al = lambda n: -2*(n+1)*(n+2*k1+1)
    be = lambda n: n*(n-1) + 2*n*(k1+k2+1-2*c) - (2*c*(2*k1+s+1) - (k1+k2)*(k1+k2+1)) - (c*c + s*(s+1) + A)
    ga = lambda n: 2*c*(n + k1 + k2 + s)
    return cf(al, be, ga, N)

def radial(w, a, A, s=-2, m=2, N=2000):
    b = np.sqrt(1 - 4*a*a)
    t = (w/2 - a*m)
    c0 = 1 - s - 1j*w - 2j/b*t
    c1 = -4 + 2j*w*(2+b) + 4j/b*t
    c2 = s + 3 - 3j*w - 2j/b*t
    c3 = w*w*(4 + 2*b - a*a) - 2*a*m*w - s - 1 + (2+b)*1j*w - A + (4*w + 2j)/b*t
    c4 = s + 1 - 2*w*w - (2*s+3)*1j*w - (4*w + 2j)/b*t
    al = lambda n: n*n + (c0+1)*n + c0
    be = lambda n: -2*n*n + (c1+2)*n + c3
    ga = lambda n: n*n + (c2-3)*n + c4 - c2 + 2
    return cf(al, be, ga, N)

def solveA(c, A0):
    f = lambda v: [angular(complex(v[0],v[1]), c).real, angular(complex(v[0],v[1]), c).imag]
    v = fsolve(f, [A0.real, A0.imag], xtol=1e-14)
    return complex(v[0], v[1])

def qnm(chi, w0M, A0=4+0j):
    a = chi/2  # 2M=1
    state = {'A': A0}
    def F(v):
        wL = complex(v[0], v[1])
        c = a*wL
        A = solveA(c, state['A']); state['A'] = A
        r = radial(wL, a, A)
        return [r.real, r.imag]
    w0L = 2*w0M
    v = fsolve(F, [w0L.real, w0L.imag], xtol=1e-13)
    wL = complex(v[0], v[1])
    return wL/2, state['A']

B = r'C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/'
ref = json.load(open(B+'C7_INDEPENDENT/tables/reference_QNM.json'))
grid = json.load(open(B+'QNM_GRID.json', encoding='utf-8'))
spins = np.array(grid['spins']); re = np.array(grid['modes']['220']['real']); im = np.array(grid['modes']['220']['imag'])
out = []
A = 4+0j; wguess = 0.3737-0.0890j
for chi in [0.0, 0.3, 0.5, 0.68, 0.9, 0.98]:
    # continuação em spin
    w, A = qnm(chi, wguess, A); wguess = w
    k = int(np.argmin(abs(spins-chi)))
    gridv = complex(re[k], im[k]) if abs(spins[k]-chi) < 1e-12 else None
    row = dict(chi=chi, leaver_indep=[w.real, w.imag], grid=None if gridv is None else [gridv.real, gridv.imag],
               absdiff_grid=None if gridv is None else abs(w-gridv))
    if abs(chi-ref['spin'])<1e-12:
        refv = complex(ref['omega_real'], ref['omega_imag']); row['reference_QNM_json'] = [refv.real, refv.imag]; row['absdiff_ref'] = abs(w-refv)
    # BCW
    mw = 1.5251-1.1568*(1-chi)**0.1292; q = 0.7+1.4187*(1-chi)**(-0.4990)
    row['bcw'] = [mw, -mw/(2*q)]; row['bcw_reldiff_real'] = (mw-w.real)/w.real; row['bcw_reldiff_imag'] = (-mw/(2*q)-w.imag)/w.imag
    out.append(row); print(json.dumps(row))
json.dump(out, open(r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote/leaver_indep_result.json','w'), indent=1)
