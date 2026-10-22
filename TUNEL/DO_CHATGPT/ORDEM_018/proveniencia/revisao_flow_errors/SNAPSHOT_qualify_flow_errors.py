"""Qualify pinned flow covariance and error propagation without means."""
from pathlib import Path
import sys,json,time,hashlib
import numpy as np
from singular_gaussian_v2 import SupportGaussian

ROOT=Path(__file__).resolve().parent

def main():
    pp=ROOT/'FLOW_ERROR_PROTOCOL.json'; protocol=json.loads(pp.read_bytes())
    for item in protocol['inputs']:
        raw=Path(item['path']).read_bytes()
        if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
            raise ValueError('Input changed: '+item['path'])
    out=ROOT/'FLOW_ERROR_RESULT.json'
    if out.exists():raise FileExistsError(str(out))
    start=time.perf_counter();cpu=time.process_time()
    meta=json.loads(Path(protocol['metadata_path']).read_bytes())
    # This pinned file contains only covariance entries, not observation means.
    raw=np.loadtxt(protocol['covariance_path']).reshape(-1)
    n=int(raw[0]);assert raw[0]==n==277 and raw.size==1+n*n
    cmag=raw[1:].reshape(n,n)
    support=SupportGaussian.from_covariance(cmag)
    z=np.array([float(x['zcmb']) for x in meta['SN_flow_error_inputs']])
    vp=np.array([float(x['vpec_2mpp_km_s']) for x in meta['SN_flow_error_inputs']])
    c=299792.458
    zpec=np.sqrt((1+vp/c)/(1-vp/c))-1
    zcorr=(1+z)/(1+zpec)-1
    vcorr=c*((1+zcorr)**2-1)/((1+zcorr)**2+1)
    assert np.all(vcorr>0)
    velocity=np.log10(1+240/vcorr)**2
    v=cmag/25+np.diag(velocity)
    effective=SupportGaussian.from_covariance(v)
    if effective.rank!=n:raise ValueError('Ordinary upstream inverse not qualified')
    chol=np.linalg.cholesky(v)
    one=np.ones(n)
    invone=np.linalg.solve(chol.T,np.linalg.solve(chol,one))
    variance=float(1/np.sum(invone));weights=invone*variance
    residual=float(np.max(np.abs(v@invone-one)))
    assert variance>0 and residual<1e-9 and abs(weights.sum()-1)<1e-12
    sbf=meta['SBF_flow_error_inputs']
    sigma_m=np.array([float(x['sigma_m110_mag']) for x in sbf])
    sigma_M=np.array([float(x['sigma_M110_mag_unused_upstream']) for x in sbf])
    sv=np.array([float(x['v2mpp_km_s']) for x in sbf])
    sbf_velocity=np.log10(1+240/sv)**2
    upstream=(sigma_m/5)**2+sbf_velocity
    # Hypothetical component calculation, not an adopted physical error model.
    independent=(sigma_m/5)**2+(sigma_M/5)**2+sbf_velocity
    assert np.all(independent>=upstream) and np.all(upstream>0)
    result={'scope':'ERRORS_ONLY_NO_INTERCEPT_CENTRES_NO_FIT','protocol_sha256':hashlib.sha256(pp.read_bytes()).hexdigest(),
        'SN':{'rows':n,'raw_covariance_rank':support.rank,'raw_covariance_min_eigenvalue':float(np.linalg.eigvalsh(cmag)[0]),'effective_covariance_rank':effective.rank,'effective_condition_number':float(effective.positive_eigenvalues[-1]/effective.positive_eigenvalues[0]),'variance_alpha_conditional_upstream':variance,'sigma_alpha_conditional_upstream':float(np.sqrt(variance)),'inverse_solve_residual_max':residual,'weight_sum':float(weights.sum()),'weight_min':float(weights.min()),'weight_max':float(weights.max())},
        'SBF':{'rows':len(sbf),'sigma_alpha_upstream_m_only':float(np.sqrt(1/np.sum(1/upstream))),'sigma_alpha_if_independent_M_component_added':float(np.sqrt(1/np.sum(1/independent))),'second_case_status':'CONDITIONAL_ALGEBRA_NOT_ADOPTED; shared/correlated components require separate source-backed treatment'},
        'MM':{'evaluated':False,'reason':'sigma_D/D unavailable within error-only extraction; centres intentionally not used'},
        'scope_limits':['No alpha or H0 central value','No stellar/global covariance or observed fit','Raw covariance PSD does not prove completeness or absence of velocity double counting','Nonstellar cross-block independence remains upstream INPUT'],
        'wall_s':time.perf_counter()-start,'cpu_s':time.process_time()-cpu,'scientific_verdict':None}
    encoded=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    temp=out.with_suffix('.tmp');temp.write_bytes(encoded);assert temp.read_bytes()==encoded;temp.replace(out)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
