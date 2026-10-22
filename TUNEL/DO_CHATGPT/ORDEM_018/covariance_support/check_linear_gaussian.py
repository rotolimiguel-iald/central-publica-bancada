"""Bounded dimensionless synthetic controls; no scientific catalogue input."""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, multivariate_normal
from linear_gaussian import FlatNuisanceGaussian

ROOT = Path(__file__).resolve().parent


def main():
    protocol_path = ROOT/'LINEAR_GAUSSIAN_PROTOCOL.json'
    protocol = json.loads(protocol_path.read_bytes())
    for record in protocol['inputs']:
        raw = Path(record['path']).read_bytes()
        assert len(raw) == record['bytes']
        assert hashlib.sha256(raw).hexdigest() == record['sha256']
    output = ROOT/'LINEAR_GAUSSIAN_RESULT.json'
    if output.exists():
        raise FileExistsError('Synthetic control result already exists')
    started = time.perf_counter()
    checks = []
    def close(name, actual, expected, tolerance=1e-10):
        error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, error=error, tolerance=tolerance, passed=error <= tolerance))
    def rejects(name, operation):
        try:
            operation()
        except ValueError:
            checks.append(dict(name=name, passed=True))
        else:
            checks.append(dict(name=name, passed=False))
    c=np.diag([0.04,0.09]); x=np.ones((2,1)); b=np.array([0.7,-0.3])
    model=FlatNuisanceGaussian(c,x)
    expected=norm.logpdf(b[0]-b[1],scale=math.sqrt(0.13))
    close('analytic_difference_density',model.log_integral(b),expected)
    numeric,error=quad(lambda eta: multivariate_normal.pdf(b-x[:,0]*eta,cov=c),-np.inf,np.inf,epsabs=1e-12)
    close('independent_scalar_quadrature',model.log_integral(b),math.log(numeric))
    singular=FlatNuisanceGaussian(np.diag([0.04,0.09,0]),np.array([[1.],[1.],[0.]]))
    close('singular_embedding',singular.log_integral(np.r_[b,0]),expected)
    checks.append(dict(name='inconsistent_deterministic_observation',passed=singular.log_integral(np.r_[b,0.1])==float('-inf')))
    rejects('unsupported_nuisance',lambda:FlatNuisanceGaussian(np.diag([1.,0.]),np.ones((2,1))))
    rejects('rank_deficient_flat_prior',lambda:FlatNuisanceGaussian(np.eye(2),np.ones((2,2))))
    rejects('nonfinite_response',lambda:model.response_information(np.array([[np.nan],[0.]])))
    rejects('unsupported_response',lambda:singular.response_information(np.array([[0.],[0.],[1.]])))
    parameter_changed=FlatNuisanceGaussian(c,x/2)
    close('parameter_measure_jacobian',parameter_changed.log_integral(b),expected+math.log(2))
    b2=np.array([0.2,0.4])
    close('relative_ratio_common_measure',parameter_changed.log_integral(b)-parameter_changed.log_integral(b2),model.log_integral(b)-model.log_integral(b2))
    t=np.diag([2.,3.]); transported=FlatNuisanceGaussian(t@c@t.T,t@x)
    close('fixed_observation_units_jacobian',transported.log_integral(t@b),expected-math.log(6))
    close('fixed_units_relative_ratio',transported.log_integral(t@b)-transported.log_integral(t@b2),model.log_integral(b)-model.log_integral(b2))
    information=model.response_information(np.array([[1.],[0.]]))
    close('projected_information_analytic',information,np.array([[1/0.13]]))
    close('nuisance_response_is_unidentified',model.response_information(x),np.zeros((1,1)))
    # Independent full-rank dense algebra checks normalization and two responses.
    c3=np.array([[2.,.2,.1],[.2,1.,.15],[.1,.15,.7]])
    x3=np.array([[1.],[.5],[-.25]])
    a3=np.array([[1.,0.],[0.,1.],[1.,-1.]])
    m3=FlatNuisanceGaussian(c3,x3)
    ci=np.linalg.inv(c3); f=x3.T@ci@x3
    p=ci-ci@x3@np.linalg.solve(f,x3.T@ci)
    close('two_response_schur_information',m3.response_information(a3),a3.T@p@a3)
    b3=np.array([.1,-.2,.3])
    direct=-.5*(2*math.log(2*math.pi)+np.linalg.slogdet(c3)[1]+np.linalg.slogdet(f)[1]+b3@p@b3)
    close('dense_flat_integral',m3.log_integral(b3),direct)
    result={'scope':'DIMENSIONLESS_SYNTHETIC_ONLY_NO_CATALOGUES_OR_CENTRES','protocol_sha256':hashlib.sha256(protocol_path.read_bytes()).hexdigest(),'checks':checks,'passed':all(x['passed'] for x in checks),'quadrature_error':error,'wall_s':time.perf_counter()-started,'scientific_verdict':None}
    raw=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    tmp=output.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(output)
    print(json.dumps({'passed':result['passed'],'checks':len(checks),'wall_s':result['wall_s']}))
    assert result['passed']


if __name__=='__main__':
    main()
