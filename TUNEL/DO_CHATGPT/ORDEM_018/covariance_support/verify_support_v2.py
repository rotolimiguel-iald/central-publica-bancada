"""Focused synthetic regressions for two independently reported P2 defects."""
from pathlib import Path
import json
import math
import sys
import time
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from audit_inputs import file_info, save_json
from singular_gaussian_v2 import SupportGaussian as Gaussian, gaussian_prior_marginal


def main():
    assert not (HERE/'RESULT_V2.json').exists(), 'Do not repeat completed unit'
    protocol = json.loads((HERE/'PROTOCOL_V2_REPAIR.json').read_bytes())
    freeze = json.loads((HERE/'FREEZE_V2.json').read_bytes())
    for item in freeze['files']:
        assert file_info(item['path']) == item
    assert file_info(HERE/'singular_gaussian.py') == protocol['original']
    checks=[]
    start=time.perf_counter()

    def check(name, condition, **details):
        checks.append({'name':name, 'passed':bool(condition), **details})
        assert condition, name

    def rejected(name, function):
        try:
            function()
        except ValueError:
            check(name, True)
        else:
            check(name, False)

    for field in ['relative_cutoff','absolute_cutoff','support_tolerance']:
        for label, value in [('nan',float('nan')),('inf',float('inf')),
                             ('negative_inf',float('-inf')),('negative',-1.),
                             ('vector',[0.])]:
            rejected(field+'_'+label, lambda field=field,value=value:
                     Gaussian.from_covariance(np.ones((2,2)), **{field:value}))
    rejected('threshold_overflow', lambda:Gaussian.from_covariance([[1e308]], relative_cutoff=1e308))
    valid={'data':np.ones(2),'mean':np.zeros(2),'covariance':np.eye(2),
           'design':np.eye(2),'prior_mean':np.zeros(2),'prior_covariance':np.eye(2)}
    for field, bad in [('data',[1.]),('mean',[0.]),('prior_mean',[0.]),
                       ('design',[1.,1.]),('covariance',[[1.]]),
                       ('prior_covariance',[[1.]])]:
        rejected(field+'_dimension',lambda field=field,bad=bad:
                 gaussian_prior_marginal(**{**valid,field:bad}))
    for field in valid:
        bad=np.array(valid[field],copy=True);bad.flat[0]=np.nan
        rejected(field+'_nonfinite',lambda field=field,bad=bad:
                 gaussian_prior_marginal(**{**valid,field:bad}))
    rejected('column_vector_data',lambda:gaussian_prior_marginal(**{**valid,'data':np.ones((2,1))}))
    rejected('row_vector_mean',lambda:gaussian_prior_marginal(**{**valid,'mean':np.zeros((1,2))}))
    c=np.ones((2,2));g=Gaussian.from_covariance(c)
    a=g.evaluate([1.,1.]);b=g.evaluate([2.,0.])
    check('singular_support',a['support_ok'] and not b['support_ok'] and b['log_density']==-math.inf)
    check('pseudoinverse_cost_preserved',abs(a['chi2_pseudoinverse']-b['chi2_pseudoinverse'])<1e-12)
    conv=gaussian_prior_marginal([1.],[0.],[[.3]],[[1.]],[.2],[[.7]])
    exact=-.5*(math.log(2*math.pi)+.8**2)
    check('proper_prior_convolution',abs(conv['log_density']-exact)<1e-12)
    mult=gaussian_prior_marginal(**valid)
    exact2=-.5*(2*math.log(2*math.pi)+2*math.log(2)+1)
    check('multivariate_convolution',abs(mult['log_density']-exact2)<1e-12)
    transform=np.array([[1.,0.],[0.,1.],[1.,1.],[2.,-1.]])
    elementary=np.diag([2.,.5]);mapped=Gaussian.from_covariance(transform@elementary@transform.T)
    r1=np.array([.3,-.7]);r2=np.array([.7,-.3])
    ratio=mapped.evaluate(transform@r1)['log_density']-mapped.evaluate(transform@r2)['log_density']
    target=-.5*(r1@np.linalg.solve(elementary,r1)-r2@np.linalg.solve(elementary,r2))
    check('elementary_map_ratio',abs(ratio-target)<1e-12)
    zero=Gaussian.from_covariance(np.zeros((2,2)))
    check('dirac_support',zero.evaluate([0.,0.])['support_ok'] and not zero.evaluate([1.,0.])['support_ok'])
    theta=.713;rot=np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]])
    rotated=Gaussian.from_covariance(rot@c@rot.T).evaluate(rot@np.ones(2))
    check('rotated_density',abs(rotated['log_density']-a['log_density'])<1e-12)
    assert file_info(HERE/'singular_gaussian.py') == protocol['original']
    save_json(HERE/'RESULT_V2.json',{'scope':'SYNTHETIC_REPAIR_ONLY','passed':len(checks),
        'checks':checks,'seconds':time.perf_counter()-start,'freeze':freeze,
        'original_preserved':True,'numpy':np.__version__})
    print(json.dumps({'passed':len(checks),'result':file_info(HERE/'RESULT_V2.json')}))


if __name__=='__main__':
    main()
