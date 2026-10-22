"""Exact QNMs for independent off-source IMR-model adequacy diagnostics."""
from pathlib import Path
import os
import sys
import hashlib
import json
ROOT=Path(__file__).resolve().parent
os.environ['NUMBA_CACHE_DIR']=str(ROOT/'cache/numba')
os.environ['QNMCACHEDIR']=str(ROOT/'cache/qnm')
os.environ['OPENBLAS_NUM_THREADS']='1'
sys.path.insert(0,str(ROOT/'cache/vendor'))
import qnm
from fetch_public import atomic_json

def main():
    controls=json.loads((ROOT/'C5_IMR_CONTROLS.json').read_bytes())
    modes=[(2,2,1),(2,2,2),(2,1,0),(3,3,0),(4,4,1),(5,5,0)]
    rows=[]
    for mode in modes:
        seq=qnm.modes_cache(s=-2,l=mode[0],m=mode[1],n=mode[2])
        for family in controls['families']:
            spin=family['remnant_spin'];freq,A,coeff=seq(a=spin)
            rows.append(dict(family=family['family'],spin=spin,mode=mode,
                omega_real=float(freq.real),omega_imag=float(freq.imag),
                angular_separation_real=float(A.real),angular_separation_imag=float(A.imag)))
        print(json.dumps(dict(mode=mode,computed=len(rows))),flush=True)
    atomic_json(ROOT/'C5_EXTRA_QNMS.json',dict(status='EXTRA_QNMS_CALCULATED_FOR_IMR_CONTROLS',rows=rows,
        qnm_version=qnm.__version__,source_sha256=hashlib.sha256((ROOT/'C5_IMR_CONTROLS.json').read_bytes()).hexdigest(),
        scope='Exact package solutions at control-source spins; no interpolation and no claim of an independent overtone solver proof'))

if __name__=='__main__':main()
