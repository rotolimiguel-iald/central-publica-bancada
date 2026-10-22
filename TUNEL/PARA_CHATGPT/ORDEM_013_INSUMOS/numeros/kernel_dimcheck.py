import math, numpy as np
# [KNOWN] constants typed here (CODATA 2018 / IAU 2015 nominal) -- not read from casa files
G=6.67430e-11; hbar=1.054571817e-34; c=299792458.0; GMsun=1.3271244e20
ALPHA=7.2973525693e-3
beta=ALPHA*math.sqrt(math.e)
Msun=GMsun/G
MPl=math.sqrt(hbar*c/G); tP=math.sqrt(hbar*G/c**5)
print("beta(runtime)=",beta)
for m in (1,60):
    M=m*Msun
    r=M/MPl
    tg=G*M/c**3
    print(f"M={m} Msun: M/MPl={r:.3e}  (M/MPl)^2={r*r:.3e}  S_BH=4pi(M/MPl)^2={4*math.pi*r*r:.3e}  GM/c^3={tg:.3e} s = {tg/tP:.3e} t_P")
# QNM l=2,n=0 Schwarzschild [KNOWN, typed: M*omega = 0.37367 - 0.08896 i]
wr,wi=0.37367,0.08896
print("K_mode = omega/T_H = 8*pi*M*omega_R =",8*math.pi*wr)
print("illustration beta*Re(omega)/Im(omega) =",beta*wr/wi)
# GKSL checks (numeric): off-diagonal decay rate for three jump choices
rng=np.random.default_rng(0)
k=np.array([0.3,1.7,4.0])   # positive spectrum for sqrt(K)
def dissip(L,rho):
    return L@rho@L.conj().T-0.5*(L.conj().T@L@rho+rho@L.conj().T@L)
E=np.zeros((3,3));E[0,2]=1
b=0.5
for name,L in [("L=sqrt(b)*sqrt(K)",math.sqrt(b)*np.diag(np.sqrt(k))),("L=sqrt(b)*K",math.sqrt(b)*np.diag(k))]:
    r=dissip(L,E)[0,2]
    print(name,"rate_02=",-r)
print("pred (b/2)(sqrt k0 - sqrt k2)^2 =",b/2*(math.sqrt(k[0])-math.sqrt(k[2]))**2)
print("pred (b/2)(k0-k2)^2 =",b/2*(k[0]-k[2])**2)
