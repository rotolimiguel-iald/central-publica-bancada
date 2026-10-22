"""Independent covariance integral and physical prior normalization checks."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.integrate import quad
from scipy.linalg import cholesky,solve_triangular
from coherent_imr_model import network_basis,remnant
from coherent_imr_likelihood import marginalized_source_log_likelihood,distance_prior_density
from nonlinear_coherent_recovery import source_vector,SOURCES,write
from tgl_ringdown_prediction import scales

ROOT=Path(__file__).resolve().parent


def main():
    rows=[];norms=[]
    with np.load(ROOT/"cache/recolored_noise/O5_noise.npz") as f:
        white=f["whitener_scaled"].copy()
        noise=np.hstack([f[d+"_strain_scaled"][50:53]@white.T for d in ("H1","L1")])
    for s in (1.,3.,10.):
        # Independent direct numerical integration in distance, including the tail.
        value,error=quad(lambda d:float(distance_prior_density(d,s)),0.,np.inf,epsabs=1e-10,epsrel=1e-10)
        if abs(value-1)>1e-8:raise ValueError("Distance prior is not normalized")
        norms.append(dict(sd=s,integral=value,error_estimate=error))
    for family in ("SEOBNRv4HM","IMRPhenomXPHM"):
        source=SOURCES[0];x=source_vector(source);m1=source["mass"]*source["q"]/(1+source["q"]);m2=source["mass"]/(1+source["q"])
        mf,spin=remnant(family,m1,m2,x[2],x[3]);times=np.arange(410)/2048+10*scales(mf,"CODATA2018_IAU2015")[0]
        true,_=network_basis(family,x,times,"R-B",1.,white)
        signal=true[:,0]*40/np.linalg.norm(true[:,0]);targets=signal[None,:]+noise
        for a in (0.,1.):
            basis,_=network_basis(family,x,times,"R-B",a,white)
            for s in (1.,3.,10.):
                got,metadata=marginalized_source_log_likelihood(family=family,coordinates=x,times=times,white=white,
                                targets=targets,reading="R-B",a=a,amplitude_prior_sd=s)
                covariance=np.eye(len(signal))+s*s*basis@basis.T
                lower=cholesky(covariance,lower=True);solved=solve_triangular(lower,targets.T,lower=True)
                expected=-.5*np.sum(solved*solved,axis=0)-np.log(np.diag(lower)).sum()+.5*np.sum(targets*targets,axis=1)
                error=float(np.max(np.abs(got-expected)))
                if error>1e-7:raise ValueError("Physical amplitude integral mismatch")
                rows.append(dict(family=family,a=a,sd=s,N=len(targets),max_logz_difference=error))
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    out=dict(status="PASS_EXACT_COMMON_DISTANCE_POLARIZATION_INTEGRAL",prior_checks=norms,integral_checks=rows,
             max_logz_difference=max(r["max_logz_difference"] for r in rows),source_integration_complete=False,
             scope="An available nonlinear source likelihood; physical partition remains conditional. Proper prior is stated explicitly and is not uniform in comoving volume.",
             hashes={n:digest(ROOT/n) for n in ("coherent_imr_model.py","coherent_imr_likelihood.py","tgl_ringdown_likelihood.py",Path(__file__).name)})
    write(ROOT/"C5_COHERENT_LIKELIHOOD_VALIDATION.json",out);print(json.dumps(out),flush=True)


if __name__=="__main__":main()
