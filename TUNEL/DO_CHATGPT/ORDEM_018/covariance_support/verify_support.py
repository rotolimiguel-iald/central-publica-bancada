"""Independent analytic examples for the frozen synthetic support contract."""
from pathlib import Path
import sys, json, math, time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from audit_inputs import save_json, file_info
from singular_gaussian import SupportGaussian, gaussian_prior_marginal


def main():
    here=Path(__file__).resolve().parent
    frozen=json.loads((here/'PROTOCOL_FREEZE.json').read_bytes())['protocol']
    assert file_info(here/'PROTOCOL_V1.json')==frozen
    assert not (here/'RESULT.json').exists(), 'Recover existing result instead of rerun'
    start=time.perf_counter();cpu=time.process_time();checks=[]
    def check(name, condition, **details):
        checks.append(dict(name=name,passed=bool(condition),**details))
        assert condition,name
    c=np.ones((2,2));g=SupportGaussian.from_covariance(c)
    ordinary=g.evaluate([1.,1.]);violating=g.evaluate([2.,0.])
    check('duplicate-rank', ordinary['rank']==1 and ordinary['nullity']==1)
    check('pseudoinverse-cost-alone-misses-violation',abs(ordinary['chi2_pseudoinverse']-violating['chi2_pseudoinverse'])<1e-12)
    check('support-rejects-antisymmetric-shift',not violating['support_ok'] and violating['log_density']==-math.inf)
    check('on-support-cost-is-elementary',ordinary['support_ok'] and abs(ordinary['chi2_pseudoinverse']-1)<1e-12)
    for m1,m2 in [(0.,.3),(-2.,1.5),(.9,1.)]:
        lr=g.evaluate(np.ones(2)*(1-m1))['log_density']-g.evaluate(np.ones(2)*(1-m2))['log_density']
        exact=-.5*((1-m1)**2-(1-m2)**2)
        check('duplicated-likelihood-ratio',abs(lr-exact)<1e-12,error=float(lr-exact))
    # Nonorthogonal, redundant observation map from two elementary dimensions.
    b=np.array([[1.,0.],[0.,1.],[1.,1.],[2.,-1.]])
    s=np.diag([2.,.5]);transformed=SupportGaussian.from_covariance(b@s@b.T)
    z=np.array([.4,-.2]);mu1=np.array([.1,.5]);mu2=np.array([-.3,.1])
    r1=z-mu1;r2=z-mu2
    exact=-.5*(r1@np.linalg.solve(s,r1)-r2@np.linalg.solve(s,r2))
    lr=transformed.evaluate(b@r1)['log_density']-transformed.evaluate(b@r2)['log_density']
    check('elementary-map-preserves-ratio',abs(lr-exact)<1e-12,error=float(lr-exact))
    check('elementary-map-support',transformed.evaluate(b@r1)['support_ok'] and transformed.rank==2)
    theta=.713;q=np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]])
    rotated=SupportGaussian.from_covariance(q@c@q.T)
    check('orthogonal-density-invariance',abs(rotated.evaluate(q@np.ones(2))['log_density']-ordinary['log_density'])<1e-12)
    check('orthogonal-support-invariance',not rotated.evaluate(q@np.array([2.,0.]))['support_ok'])
    for label,invalid in [('negative',[[1.,0.],[0.,-.1]]),('asymmetry',[[1.,.1],[0.,1.]]),('nan',[[float('nan')]])]:
        rejected=False
        try:SupportGaussian.from_covariance(invalid)
        except ValueError:rejected=True
        check('reject-'+label,rejected)
    zero=SupportGaussian.from_covariance(np.zeros((2,2)))
    check('dirac-at-zero',zero.evaluate([0.,0.])['support_ok'] and zero.rank==0)
    check('dirac-away-rejected',not zero.evaluate([1.,0.])['support_ok'])
    # Proper prior x~N(.2,.7), y=x+noise, noise variance .3.
    marginal=gaussian_prior_marginal([1.],[0.],[[.3]],[[1.]],[.2],[[.7]])
    exact=-.5*(math.log(2*math.pi)+(1-.2)**2)
    check('normalized-prior-convolution',abs(marginal['log_density']-exact)<1e-12)
    # Change of numerical rank is exposed, not silently called full rank.
    near=SupportGaussian.from_covariance(np.diag([1.,1e-14]))
    check('declared-cutoff-recorded',near.rank==1 and near.threshold==1e-12)
    save_json(here/'RESULT.json',{'scope':'SYNTHETIC_ONLY_NO_REAL_FIT_OR_VERDICT','protocol':frozen,
              'scripts':[file_info(here/n) for n in ['singular_gaussian.py','verify_support.py']],
              'checks':checks,'passed':len(checks),'numpy_version':np.__version__,
              'elapsed_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
              'counterexample':{'ordinary':ordinary,'off_support':{**violating,'log_density':'-infinity'}},
              'limitations':['prototype cutoff applies to dimensionless examples only',
              'likelihood ratios compare one fixed data space/support; unlike-dimensional support densities are not Bayes factors',
              'no real H0DN matrices assembled, no uniform-prior integration or scientific-contract ratification']})
    print(json.dumps({'passed':len(checks),'result':file_info(here/'RESULT.json')},ensure_ascii=False))


if __name__=='__main__':main()
