"""Copy installed reference PSDs; calculate exact Kerr modes with qnm 0.4.4.

Run with /opt/lal_env/bin/python. Writes only inside this task directory.
"""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import os
import shutil
import sys

ROOT=Path(__file__).resolve().parent
os.environ['NUMBA_CACHE_DIR']=str(ROOT/'cache'/'numba')
os.environ['QNMCACHEDIR']=str(ROOT/'cache'/'qnm')
sys.path.insert(0,str(ROOT/'cache'/'vendor'))
import bilby
import numpy as np
import qnm
from fetch_public import atomic_json

def main():
    dest=ROOT/'cache'/'psd'; dest.mkdir(parents=True,exist_ok=True)
    origin=Path(bilby.__file__).parent/'gw'/'detector'/'noise_curves'
    curves=[]
    for key,filename,kind in [('O4','aLIGO_O4_high_asd.txt','ASD'),('O5','Aplus_asd.txt','ASD'),
                              ('ET','ET_D_psd.txt','PSD'),('CE','CE_psd.txt','PSD')]:
        src=origin/filename; out=dest/filename
        raw=src.read_bytes()
        if out.exists() and out.read_bytes()!=raw:
            raise RuntimeError('Do not overwrite a changed reference curve')
        if not out.exists(): out.write_bytes(raw)
        data=np.loadtxt(out)
        curves.append(dict(key=key,filename=filename,kind=kind,source=str(src),
                           sha256=hashlib.sha256(raw).hexdigest(),rows=len(data),
                           frequency_min=float(data[:,0].min()),frequency_max=float(data[:,0].max())))
    # qnm solves the angular eigenproblem and the radial continued fraction.
    # No download_data() call; construct the spin sequence locally.
    mode=qnm.modes_cache(s=-2,l=2,m=2,n=0)
    modes=[]
    for spin in [0,.5,.6,.65,.6712194217379245,.68,.7,.8,.9,.95,.99]:
        omega,sep,_=mode(a=spin)
        modes.append(dict(spin=spin,omega_real=float(omega.real),omega_imag=float(omega.imag),
                          angular_real=float(sep.real),angular_imag=float(sep.imag)))
    atomic_json(ROOT/'FISHER_INPUTS.json',dict(status='INPUTS_COPIED_AND_QNM_CALCULATED',
                  versions={m:importlib.metadata.version(m) for m in ['numpy','scipy','bilby']},
                  qnm_version=qnm.__version__,psds=curves,mode_220=modes,
                  conventions='M omega = omega_R - i M/tau; detector mass; prograde 220',
                  scope='Reference design curves, not measured O4 event PSD; O5 sensitivity scenario'))
    print(json.dumps({'curves':curves,'qnm_220':modes}),flush=True)

if __name__=='__main__':main()
