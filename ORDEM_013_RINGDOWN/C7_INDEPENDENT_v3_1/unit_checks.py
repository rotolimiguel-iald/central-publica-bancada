"""Portable regression and refusal tests; no target data, no scientific promotion."""
from pathlib import Path
import json,math
import numpy as np
from tgl_ringdown_prediction import prediction,kerr_mode,beta_tgl
from tgl_ringdown_template import ringdown
ROOT=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise ValueError(message)
def refuses(call):
    try:call()
    except (ValueError,NotImplementedError):return
    raise ValueError('Invalid scientific input was accepted')
def main():
    fixture=json.loads((ROOT/'fixtures/legacy_per_series_2.json').read_bytes())['value']
    errors={}
    for r in ('A','B'):
        actual=prediction(fixture['Mf_det'],fixture['a_f'],'R-'+r,profile='LEGACY_V346')['delta_tau_linear']
        expected=fixture['delta_pred_'+r];errors[r]=abs(actual-expected)/abs(expected)
        require(errors[r]<1e-12,'Legacy convention regression')
    require(math.isclose(beta_tgl(),7.2973525693e-3*math.sqrt(math.e),rel_tol=1e-15),'Runtime beta')
    p=prediction(68.1,.68,'R-B');x=p['x']
    require(math.isclose(p['delta_tau_ensemble_exact'],-x/(1+x),rel_tol=1e-14),'Exact rate conversion')
    refuses(lambda:kerr_mode(68.1,-.1))
    refuses(lambda:kerr_mode(68.1,.68,mode=(4,4,0)))
    refuses(lambda:prediction(68.1,.68,'R-MOD'))
    refuses(lambda:prediction(68.1,.68,'R-B',profile='UNKNOWN'))
    times=np.arange(128)/4096
    args=dict(mass_detector_solar=68.1,spin=.68,strain_amplitude=1e-21,t_start=.003,phase=.4,inclination=.3)
    gr=ringdown(times,reading='R-GLOBAL',**args)
    zero=ringdown(times,reading='R-B',deformation=0,**args)
    full=ringdown(times,reading='R-B',deformation=1,**args)
    for key in ('plus','cross'):
        require(np.array_equal(gr[key],zero[key]),'a=0 not GR')
        require(np.all(full[key][times<args['t_start']]==0),'Pre-onset leakage')
    require(not np.array_equal(full['plus'],zero['plus']),'a=1 ineffective')
    refuses(lambda:ringdown(times,reading='R-B',deformation=-1,**args))
    print(json.dumps(dict(status='PASS',legacy_relative_errors=errors,guard_controls=5,scope='Numerical regression and input refusal; no calibration or physical conclusion')))
if __name__=='__main__':main()
