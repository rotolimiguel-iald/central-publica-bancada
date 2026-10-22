"""Independent NumPy/SciPy reproduction of the archived SN-only validation. No verdict."""
from pathlib import Path
import sys, json, time, math
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize
from numpy.polynomial.legendre import leggauss
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from audit_inputs import file_info,save_json
ROOT=Path(__file__).resolve().parent
start=time.perf_counter()
protocol=json.loads((ROOT/'PROTOCOL_V1.json').read_bytes())
manifest=json.loads((ROOT/'SOURCES.json').read_bytes())
for f in manifest['copied']:
    assert file_info(f['path'])['sha256']==f['sha256'],f['path']
data=np.genfromtxt(ROOT/'Pantheon+SH0ES.dat',names=True,dtype=None,encoding='utf-8')
with (ROOT/'pantheon_covariance.dat').open() as f:
    n=int(f.readline()); cov=np.loadtxt(f).reshape(n,n)
assert n==len(data)
mask=(data['zHD']>0.01)|(data['IS_CALIBRATOR']==1)
cov=cov[np.ix_(mask,mask)]; asym=float(np.max(np.abs(cov-cov.T))); cov=(cov+cov.T)/2
x=data[mask]; cal=x['IS_CALIBRATOR']==1; z=x['zHD']; zhel=x['zHEL']
chol=cho_factor(cov,lower=True,check_finite=True); one=np.ones(len(x)); ci1=cho_solve(chol,one); norm=float(one@ci1)
# Independent Gauss-Legendre quadrature, not the benchmark's log-a interpolation.
grid={}
for count in [64,128]:
    nodes,weights=leggauss(count); grid[count]=(z[:,None]*(nodes+1)/2, z[:,None]*weights/2)
def mu(par,count=64):
    H0,Om=par; Or=4.4814e-7*2.7255**4*(1+3.046*7/8*(4/11)**(4/3))/(H0/100)**2
    zz,ww=grid[count]; E=np.sqrt(Or*(1+zz)**4+Om*(1+zz)**3+1-Om-Or)
    dist=(299792.458/H0)*np.sum(ww/E,axis=1)
    out=np.empty(len(z)); out[cal]=x['CEPH_DIST'][cal]
    out[~cal]=5*np.log10((1+zhel[~cal])*dist[~cal])+25
    return out
def objective(par,detail=False):
    if not(50<par[0]<90 and .05<par[1]<.6): return 1e12
    residual=x['m_b_corr']-mu(par); mh=float(residual@ci1/norm); rr=residual-mh
    value=float(rr@cho_solve(chol,rr))
    return (value,mh) if detail else value
fits=[]
for init in [[73,.33],[68,.25]]:
    opt=minimize(objective,init,method='Nelder-Mead',options={'xatol':1e-7,'fatol':1e-9,'maxiter':600})
    fits.append({'initial':init,'x':opt.x.tolist(),'chi2':float(opt.fun),'success':bool(opt.success),'nfev':int(opt.nfev)})
assert all(f['success'] for f in fits)
p=np.array(fits[0]['x']); matrices=[]
for steps in [[.2,.01],[.1,.005],[.02,.001]]:
    hess=np.zeros((2,2))
    for i in range(2):
        for j in range(2):
            ei=np.zeros(2);ej=np.zeros(2);ei[i]=steps[i];ej[j]=steps[j]
            hess[i,j]=(objective(p+ei+ej)-objective(p+ei-ej)-objective(p-ei+ej)+objective(p-ei-ej))/(4*steps[i]*steps[j])
    c=np.linalg.inv(hess/2); sig=np.sqrt(np.diag(c))
    matrices.append({'steps':steps,'covariance':c.tolist(),'sigma':sig.tolist(),'correlation':float(c[0,1]/np.prod(sig))})
value,mh=objective(p,True)
# Compare only after independent estimates exist; historical result is not an input to the optimizer.
old=json.loads((ROOT/'RESULTADO_FASE5_SH0ES_20261001.json').read_bytes())['familias']['V_sh0es_so']['validacao']
checks={'quadrature_mu_max_delta':float(np.max(np.abs(mu(p,64)-mu(p,128)))),
        'two_starts_parameter_max_delta':float(np.max(np.abs(np.array(fits[1]['x'])-p))),
        'delta_from_archived':{'H0':float(p[0]-old['H0']),'Omega_m':float(p[1]-old['Omega_m']),'chi2':value-old['chi2'],'M_hat':mh-old['M_hat'],'sigma_H0_same_steps':matrices[0]['sigma'][0]-old['sigma_H0']}}
result={'status':'REAL_INDEPENDENT_ARCHIVED_VALIDATION_REPRODUCTION_NO_NEW_VERDICT',
    'scope':'SN-only LCDM validation; NOT complete phase4/5 joint fits, NOT five-hypothesis evidence, NOT the phase9 composite',
    'protocol':file_info(ROOT/'PROTOCOL_V1.json'),'script':file_info(Path(__file__)), 'sources':manifest,
    'sample':{'total':n,'selected':len(x),'calibrators':int(cal.sum()),'hosts_by_ceph_distance':len(np.unique(np.round(x['CEPH_DIST'][cal],4))),'cosmological':int((~cal).sum()),'covariance_shape':list(cov.shape),'asymmetry_before_symmetrizing':asym},
    'model':'flat LCDM with radiation convention from archived benchmark; mnu included in Om, no duplicate addition; calibrators use CEPH_DIST, M analytically profiled',
    'H0':float(p[0]),'Omega_m':float(p[1]),'M_hat':mh,'chi2':value,'dof':len(x)-3,'fits':fits,'hessian_convergence':matrices,'checks':checks,'archived_comparison':old,'elapsed_seconds':time.perf_counter()-start}
save_json(ROOT/'RESULT.json',result)
print(json.dumps({k:result[k] for k in ['status','sample','H0','Omega_m','M_hat','chi2','hessian_convergence','checks','elapsed_seconds']},ensure_ascii=False))
