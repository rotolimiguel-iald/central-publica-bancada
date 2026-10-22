"""Check physical network rotation, dephasing construction and conventions."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
import hashlib
import json
import numpy as np
import pycbc
import lalsimulation
import scipy
from coherent_imr_model import network_basis,polarizations,source_curves,qnm_splines,RESPONSES,profile_fit
from nonlinear_coherent_recovery import check,source_vector,SOURCES,write
from tgl_ringdown_prediction import scales,prediction

ROOT=Path(__file__).resolve().parent


def main():
    reg=check();results=[]
    with np.load(ROOT/"cache/recolored_noise/O5_noise.npz") as f:white=f["whitener_scaled"].copy()
    for family in reg["families"]:
        x=source_vector(SOURCES[0]);curves,mass,spin,peak=source_curves(family,tuple(x[:6]),8192,True)
        times=np.arange(410)/2048+10*scales(mass,"CODATA2018_IAU2015")[0]
        for a in (0.,1.):
            basis,_=network_basis(family,x,times,"R-B",a,white)
            hp,hc,_=polarizations(family,x,times,"R-B",a)
            angle=.371;amplitude=2.17
            coefficients=amplitude*np.array([np.cos(2*angle),np.sin(2*angle)])
            pp=amplitude*(np.cos(2*angle)*hp-np.sin(2*angle)*hc)
            cc=amplitude*(np.sin(2*angle)*hp+np.cos(2*angle)*hc)
            independently_rotated=np.concatenate([white@(fp*pp+fc*cc) for fp,fc in RESPONSES])
            residual=np.linalg.norm(basis@coefficients-independently_rotated)/np.linalg.norm(independently_rotated)
            if residual>1e-12:raise ValueError("Coherent rotation differs")
            value,fit,_=profile_fit(basis,independently_rotated)
            if np.linalg.norm(fit-coefficients)>1e-10:raise ValueError("Shared amplitude/polarization fit differs")
            results.append(dict(family=family,a=a,rotation_relative_error=float(residual),fit_squared_residual=value))
        gr=np.array([curves["all"][pol](times) for pol in (0,1)])
        expected=gr.copy()
        for ell in (2,4):
            gamma=prediction(mass,spin,"R-B",mode=(ell,ell,0),qnm_dimensionless=complex(qnm_splines()[ell](spin)))["gamma_per_s"]
            # Separate explicit sum; production uses expm1 correction.
            component=np.array([curves[str(ell)*2][pol](times) for pol in (0,1)])
            expected=expected-component+component*np.exp(-gamma*times)
        actual=np.array(polarizations(family,x,times,"R-B",1.)[:2])
        finite=np.isfinite(expected)
        err=np.linalg.norm((expected-actual)[finite])/np.linalg.norm(actual[finite])
        if err>1e-12:raise ValueError("Conditional damping differs")
        results.append(dict(family=family,damping_relative_error=float(err)))
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    output=dict(status="PASS_CONDITIONAL_MODEL_IMPLEMENTATION",checks=results,
                versions=dict(pycbc=pycbc.__version__,lalsimulation=lalsimulation.__version__,numpy=np.__version__,scipy=scipy.__version__),
                source_hashes={n:sha(ROOT/n) for n in ("coherent_imr_model.py","nonlinear_coherent_recovery.py",Path(__file__).name)},
                not_a_physical_mapping_proof=True)
    write(ROOT/"C5_COHERENT_MODEL_VALIDATION.json",output);print(json.dumps(output),flush=True)


if __name__=="__main__":main()
