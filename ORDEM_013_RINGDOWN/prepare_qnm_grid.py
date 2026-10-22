"""Exact Kerr grid with held-out interpolation validation, not a BCW replacement by decree."""
from pathlib import Path
import sys
import os
import json
ROOT=Path(__file__).resolve().parent
os.environ['NUMBA_CACHE_DIR']=str(ROOT/'cache/numba')
os.environ['QNMCACHEDIR']=str(ROOT/'cache/qnm')
os.environ['OPENBLAS_NUM_THREADS']='1'
sys.path.insert(0,str(ROOT/'cache/vendor'))
import numpy as np
import qnm
from scipy.interpolate import CubicSpline
from fetch_public import atomic_json

def main():
    grid=np.linspace(0,.98,491)
    schema=json.loads((ROOT/'C4_CATALOG_SCHEMA.json').read_bytes())
    assert min(r['summary']['final_spin_non_evolved']['min'] for r in schema['rows'])>=grid[0]
    assert max(r['summary']['final_spin_non_evolved']['max'] for r in schema['rows'])<=grid[-1]
    rng=np.random.default_rng(1304220);check=rng.uniform(0,.98,150)
    modes={}
    for ell in (2,4):
        mode=qnm.modes_cache(s=-2,l=ell,m=ell,n=0)
        exact=np.array([mode(a=float(a))[0] for a in check])
        root=np.sqrt(1-check**2);gap=exact.real-ell*check/(2*(1+root))
        attempts=[]
        for size in (491,981,1961):
            grid=np.linspace(0,.98,size)
            values=np.array([mode(a=float(a))[0] for a in grid])
            spline=CubicSpline(grid,values,extrapolate=False)
            err=np.abs(spline(check)-exact)/np.abs(exact)
            gap_error=np.abs((spline(check).real-exact.real)/gap)
            attempt=dict(grid_size=size,complex_error=float(max(err)),gap_error=float(max(gap_error)))
            attempts.append(attempt);print(json.dumps(dict(mode=ell,attempt=attempt)),flush=True)
            if max(err)<=1e-7 and max(gap_error)<=1e-6:break
        else:
            atomic_json(ROOT/'QNM_GRID_REJECTED.json',dict(mode=ell,attempts=attempts))
            raise ValueError('Interpolation insufficient')
        modes[str(ell)*2+'0']=dict(real=values.real.tolist(),imag=values.imag.tolist(),
           spins=grid.tolist(),attempts=attempts,
           max_relative_complex_error=float(max(err)),max_relative_corotation_gap_error=float(max(gap_error)),
           validation_spins=check.tolist())
        print(json.dumps(dict(mode=ell,max_relative_error=float(max(err)),gap_error=float(max(gap_error)))),flush=True)
    atomic_json(ROOT/'QNM_GRID.json',dict(status='EXACT_QNM_GRID_VALIDATED',spins=grid.tolist(),modes=modes,
               qnm_version=qnm.__version__,interpolation='CubicSpline; extrapolation forbidden',
               seed=1304220,n_validation=150,independent_solver_check='C4_VALIDATION.json (220 only)'))

if __name__=='__main__':main()
