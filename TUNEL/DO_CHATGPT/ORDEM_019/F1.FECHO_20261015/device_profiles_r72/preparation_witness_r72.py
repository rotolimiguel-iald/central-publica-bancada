"""Synthetic verification of local vacuum witnesses; no apparatus or observed data."""
import json, math
import numpy as np
from support_r72 import new

def run():
    n=6; dim=n*n*2*2
    a=np.diag(np.sqrt(np.arange(1,n,dtype=float)),1).astype(complex)
    eye=np.eye(n); i2=np.eye(2)
    kron=lambda x,y,z,w:np.kron(np.kron(np.kron(x,y),z),w)
    ai=kron(a,eye,i2,i2);ao=kron(eye,a,i2,i2)
    xs=[(v+v.conj().T)/math.sqrt(2) for v in (ai,ao)]
    ps=[(v-v.conj().T)/(1j*math.sqrt(2)) for v in (ai,ao)]
    quadratures=[xs[0],ps[0],xs[1],ps[1]]
    idx=lambda ni,no,oh,sp:((ni*n+no)*2+oh)*2+sp
    def ket(components):
        v=np.zeros(dim,dtype=complex)
        for address,amp in components:v[idx(*address)]=amp
        assert abs(np.vdot(v,v)-1)<1e-12
        return v
    def pure(c):
        v=ket(c);return np.outer(v,v.conj())
    v0=(0,0,0,0)
    cases={
      'vacuum':pure([(v0,1)]),
      'one_photon_no_certificate':pure([((1,0,0,0),1)]),
      'coherent_vacuum_one':pure([(v0,math.sqrt(.96)),((1,0,0,0),math.sqrt(.04))]),
      'entangled_spectator_high_number':pure([(v0,math.sqrt(.98)),((3,0,0,1),math.sqrt(.02))]),
      'means_are_required':pure([(v0,1/math.sqrt(2)),((1,0,0,0),1/math.sqrt(2))]),
      'oh_excitation':pure([(v0,math.sqrt(.9)),((0,0,1,1),math.sqrt(.1))]),
      'pair_excitation':pure([(v0,math.sqrt(.95)),((1,1,0,0),1j*math.sqrt(.05))]),
      'mixed_non_gaussian':.6*pure([(v0,1)])+.4*pure([((2,0,0,1),1)])}
    nf=np.array([ni+no for ni in range(n) for no in range(n) for oh in range(2) for sp in range(2)])
    ne=np.array([oh for ni in range(n) for no in range(n) for oh in range(2) for sp in range(2)])
    pf=np.diag((nf==0).astype(float));pj=np.diag(((nf+ne)==0).astype(float))
    trace_norm=lambda x:float(np.abs(np.linalg.eigvalsh((x+x.conj().T)/2)).sum())
    rows=[]
    for name,rho in cases.items():
        # All support has ni,no<=3. One quadrature reaches <=4<6: no truncation boundary.
        support=np.flatnonzero(np.real(np.diag(rho))>1e-14)
        assert all((k//4)//n<=3 and (k//4)%n<=3 for k in support)
        means=np.array([float(np.trace(rho@q).real) for q in quadratures])
        seconds=np.array([float(np.trace(q@rho@q).real) for q in quadratures])
        variances=seconds-means**2
        ef=float(np.dot(np.diag(rho).real,nf));ej=ef+float(np.dot(np.diag(rho).real,ne))
        from_moments=float((variances.sum()+np.dot(means,means)-2)/2)
        p0=float(np.trace(rho@pf).real);p0j=float(np.trace(rho@pj).real)
        reduced=np.einsum('arbr->ab',rho.reshape(n*n,4,n*n,4))
        target=np.zeros_like(reduced);target[0,0]=1
        df=trace_norm(reduced-target)
        dc=trace_norm(rho-pf@rho@pf/p0) if p0>1e-14 else None
        dj=trace_norm(rho-pj@rho@pj/p0j) if p0j>1e-14 else None
        tol=1e-11
        rows.append({'name':name,'epsilon_field':ef,'epsilon_joint':ej,'from_moments':from_moments,
          'means_squared':float(np.dot(means,means)),'without_means':float((variances.sum()-2)/2),
          'p_vacuum_field':p0,'p_vacuum_joint':p0j,'reduced_trace_distance':df,'conditional_product_distance':dc,
          'joint_conditional_distance':dj,
          'moment_identity':abs(ef-from_moments)<=tol,
          'gap_field':1-p0<=ef+tol,'gap_joint':1-p0j<=ej+tol,
          'distance_field':df<=2*math.sqrt(max(0,1-p0))+tol,
          'distance_conditional':dc is None or dc<=2*math.sqrt(max(0,1-p0))+tol,
          'distance_joint':dj is None or dj<=2*math.sqrt(max(0,1-p0j))+tol})
    checks=[{'name':k,'passed':all(r[k] for r in rows)} for k in ['moment_identity','gap_field','gap_joint','distance_field','distance_conditional','distance_joint']]
    displaced=next(r for r in rows if r['name']=='means_are_required')
    checks.append({'name':'missing_means_negative_control','passed':displaced['epsilon_field']-displaced['without_means']>.2})
    checks.append({'name':'zero_probability_no_false_product_certificate','passed':next(r for r in rows if r['name']=='one_photon_no_certificate')['conditional_product_distance'] is None})
    result={'status':'SYNTHETIC_PREPARATION_WITNESS_ONLY','passed':all(c['passed'] for c in checks),'checks':checks,'rows':rows,
       'new_physical_measurements':0,'no_gaussian_assumption':True,'domain':'finite-support states in infinite Fock; extended cutoff avoids quadrature boundary',
       'limitations':'no calibration, no actual local profile or output-to-cavity inference, no full global vacuum certificate'}
    new('RESULT_PREPARATION_R72.json',result)
    print(json.dumps({'passed':result['passed'],'checks':len(checks),'cases':len(rows)}))
    if not result['passed']:raise SystemExit(1)
if __name__=='__main__':run()
