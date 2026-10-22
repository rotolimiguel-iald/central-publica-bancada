"""Prepare NumPy-consumable not-a-knot coefficients from the T05 pinned grid."""
from pathlib import Path
import sys, hashlib, json, os
sys.dont_write_bytecode=True
import numpy as np
from scipy.interpolate import CubicSpline
D=Path(__file__).resolve().parent;B=D.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    reg=json.loads((B/'RINGDOWN_5SIGMA_V1_1.json').read_bytes());grid=B/'QNM_GRID.json'
    assert sha(grid)==reg['input_pins_relative_to_Chatgpt']['ORDEM_013_RINGDOWN/QNM_GRID.json']
    g=json.loads(grid.read_bytes());result=dict(schema='T12_QNM_CUBIC_V1',grid_sha256=sha(grid),method='scipy.CubicSpline not-a-knot; extrapolate=False',modes={})
    for mode in ('220','440'):
        v=g['modes'][mode];cs=CubicSpline(v['spins'],np.asarray(v['real'])+1j*np.asarray(v['imag']),extrapolate=False)
        result['modes'][mode]=dict(x=cs.x.tolist(),c_real=cs.c.real.tolist(),c_imag=cs.c.imag.tolist())
        assert np.allclose(cs(v['spins']),np.asarray(v['real'])+1j*np.asarray(v['imag']),rtol=1e-14,atol=1e-15)
    p=D/'QNM_CUBIC_COEFFICIENTS.json';tmp=p.with_suffix('.pending')
    raw=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode()
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;os.link(tmp,p);tmp.unlink()
    print(json.dumps(dict(path=str(p),sha256=sha(p))))
if __name__=='__main__':main()
