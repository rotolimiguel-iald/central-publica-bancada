import sys, json, math
sys.path.insert(0, r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote/mod')
import numpy as np
from scipy import integrate
from tgl_ringdown_likelihood import linear_statistics
rng = np.random.default_rng(7)
T = 60
t = np.arange(T)/T
basis = np.stack([np.exp(-3*t)*np.cos(20*t), np.exp(-3*t)*np.sin(20*t)], axis=1)  # (time, 2)
target = 0.8*basis[:,0] - 0.3*basis[:,1] + rng.normal(size=T)
sd = 1.7
prof, marg = linear_statistics(basis, target, sd)
# brute force: log int N(c;0,sd^2 I) exp(-|d-Bc|^2/2 + |d|^2/2) dc
def integrand(c1, c0):
    c = np.array([c0, c1]); r = target - basis@c
    return math.exp(-0.5*(r@r) + 0.5*(target@target)) * math.exp(-0.5*(c@c)/sd**2)/(2*math.pi*sd**2)
val, err = integrate.dblquad(integrand, -12, 12, -12, 12, epsabs=1e-12, epsrel=1e-10)
cols = np.linalg.lstsq(basis, target, rcond=None)[0]
prof_bf = 0.5*(target@target) - 0.5*np.sum((target-basis@cols)**2)
print(json.dumps(dict(marginal_module=float(marg[0,0]), marginal_bruteforce=math.log(val), diff=float(marg[0,0])-math.log(val),
                      profile_module=float(prof[0,0]), profile_bf=float(prof_bf))))
