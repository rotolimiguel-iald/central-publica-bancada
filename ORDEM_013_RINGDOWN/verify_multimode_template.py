"""Independent LAL angular harmonics verify the explicit mode interface."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
import lal
from scipy.interpolate import CubicSpline
from tgl_ringdown_template import ringdown
from tgl_ringdown_prediction import prediction
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']
    times=np.arange(400)/8192.;rows=[]
    for ell in (2,4):
        mode=(ell,ell,0);k=f'{ell}{ell}0';g=grid[k]
        q=complex(CubicSpline(g['spins'],np.array(g['real'])+1j*np.array(g['imag']))(.68))
        for inclination in (0.,.3,1.2,math.pi/2,math.pi):
            yp=lal.SpinWeightedSphericalHarmonic(inclination,0.,-2,ell,ell).real
            ym=lal.SpinWeightedSphericalHarmonic(inclination,0.,-2,ell,-ell).real
            norm=math.sqrt(5/(4*math.pi))
            factors=((yp+(-1)**ell*ym)/norm,(yp-(-1)**ell*ym)/norm)
            out=ringdown(times,68.1,.68,'R-MOD',1.,phase=.37,
                qnm_dimensionless=q,mode=mode,polarization_factors=factors)
            pred=prediction(68.1,.68,'R-MOD',qnm_dimensionless=q,mode=mode)
            phase=pred['omega_rad_s']*times+.37
            reference=np.exp(-(1/pred['tau_gr_s']+pred['gamma_per_s'])*times)*(yp*np.exp(-1j*phase)+(-1)**ell*ym*np.exp(1j*phase))/norm
            residual=float(np.max(abs(out['plus']-1j*out['cross']-reference)))
            if residual>1e-12:raise ValueError('LAL harmonic convention differs')
            if ell==2:
                original=ringdown(times,68.1,.68,'R-MOD',1.,phase=.37,inclination=inclination,qnm_dimensionless=q)
                if np.max(abs(original['plus']-out['plus']))>1e-12:raise ValueError('Default 220 projection changed')
            rows.append(dict(mode=mode,inclination=inclination,absolute_residual=residual))
    refusal=False
    try:ringdown(times,68.1,.68,'R-B',1.,mode=(4,4,0),qnm_dimensionless=q)
    except ValueError:refusal=True
    if not refusal:raise ValueError('Missing higher-mode projection was silently accepted')
    result=dict(status='LAL_MULTIMODE_ANGULAR_ORACLE_PASS',rows=rows,missing_projection_refused=refusal,
        scope='Spherical-harmonic convention verified, not Kerr spheroidal-to-spherical mixing or full IMR dynamics',
        template_sha256=hashlib.sha256((ROOT/'tgl_ringdown_template.py').read_bytes()).hexdigest())
    atomic_json(ROOT/'C3_MULTIMODE_TEMPLATE.json',result);print(json.dumps(result),flush=True)

if __name__=='__main__':main()
