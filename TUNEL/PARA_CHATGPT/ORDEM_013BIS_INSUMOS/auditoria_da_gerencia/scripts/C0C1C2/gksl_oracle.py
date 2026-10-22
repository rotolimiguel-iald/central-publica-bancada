import numpy as np, math
BETA=7.2973525693e-3*math.sqrt(math.e)
rng=np.random.default_rng(7)
d=5
k=np.array([0.,0.4,1.1,2.5,6.0])
U,_=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
def D(Lj,rho): return Lj@rho@Lj.conj().T-0.5*(Lj.conj().T@Lj@rho+rho@Lj.conj().T@Lj)
def superop(Lj):
    S=np.zeros((d*d,d*d),complex)
    for a in range(d):
        for b in range(d):
            E=np.zeros((d,d),complex);E[a,b]=1
            S[:,a*d+b]=D(Lj,E).reshape(-1)   # row-major vec, differs from bancada's column kron
    return S
L=U@np.diag(np.sqrt(BETA*k))@U.conj().T
ev=np.sort(np.linalg.eigvals(superop(L)).real)
an=np.sort((-0.5*BETA*(np.sqrt(k[:,None])-np.sqrt(k[None,:]))**2).ravel())
print('max|eig-analytic|',np.max(np.abs(ev-an)))
for c in [0.3,1.7,-2.2]:
    Lc=L+c*np.eye(d); print('c',c,'||S(L+c)-S(L)||',np.linalg.norm(superop(Lc)-superop(L)),
      'jump rate rho=I/d', np.trace(Lc.conj().T@Lc).real/d, 'vs', np.trace(L.conj().T@L).real/d)
# complex c breaks invariance (anti-Hermitian part adds Hamiltonian-like term): check
Lc=L+0.5j*np.eye(d); print('imag c: ||S diff||',np.linalg.norm(superop(Lc)-superop(L)))
# signed spectrum choices, coherence rates between +k and -k
sK=np.array([-3.,-1.,0.,1.,3.])
for name,f in [('K+',np.maximum(sK,0)),('|K|',np.abs(sK))]:
    r=0.5*BETA*(np.sqrt(f[:,None])-np.sqrt(f[None,:]))**2
    print(name,'rate(+3,-3)=',r[4,0],'rate(0,1)=',r[2,3])
