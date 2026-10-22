"""Inspect the resolution-sensitive candidate's orientation-dependent peak."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
from pathlib import Path
import json
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
from pycbc.waveform import get_td_waveform
from coherent_imr_model import source_curves
from nonlinear_coherent_recovery import write

ROOT=Path(__file__).resolve().parent


def main():
    row=json.loads((ROOT/"cache/nonlinear_coherent/source_64_IMRPhenomXPHM_to_SEOBNRv4HM.json").read_bytes())
    x=np.array(row["best"]["x"]);mass=np.exp(x[0]);q=np.exp(x[1]);rows=[]
    for rate in (4096,8192,16384,32768):
        curves,mf,spin,ordinary=source_curves("SEOBNRv4HM",tuple(x[:6]),rate,False)
        pars=dict(mass1=mass*q/(1+q),mass2=mass/(1+q),spin1z=x[2],spin2z=x[3],
                  spin1x=0.,spin1y=0.,spin2x=0.,spin2y=0.,inclination=0.,coa_phase=x[5],distance=403.,
                  delta_t=1/rate,f_lower=20.,f_ref=20.,approximant="SEOBNRv4HM",mode_array=[(2,2)])
        hp,hc=get_td_waveform(**pars);t=np.asarray(hp.sample_times);p=np.asarray(hp)*1e21;c=np.asarray(hc)*1e21
        k=np.argmax(p*p+c*c);sp=CubicSpline(t,p);sc=CubicSpline(t,c);norm=p[k]**2+c[k]**2
        opt=minimize_scalar(lambda tt:-(sp(tt)**2+sc(tt)**2)/norm,bounds=(t[k-2],t[k+2]),method="bounded",options={"xatol":1e-13})
        intrinsic=float(opt.x)
        # For a nonprecessing +/-22 pair hp=A_i Re(h22), hc=-B_i Im(h22).
        # The observed polarization norm is not the intrinsic complex-mode norm.
        a=(1+np.cos(x[4])**2)/2;b=np.cos(x[4])
        p22,c22,lo,hi,_=curves["22"];tt=np.arange(max(lo,-.03),min(hi,.01),1/32768)
        amplitude=(p22(tt)/a)**2+(c22(tt)/b)**2;j=np.argmax(amplitude)
        fixed=minimize_scalar(lambda u:-((p22(u)/a)**2+(c22(u)/b)**2)/amplitude[j],
                              bounds=(tt[j-2],tt[j+2]),method="bounded",options={"xatol":1e-13})
        rows.append(dict(sample_rate=rate,polarization_norm_peak_s=ordinary,intrinsic_faceon_peak_s=intrinsic,
                         deellipticized_peak_s=float(fixed.x+ordinary),orientation_phase_shift_s=intrinsic-ordinary))
    result=dict(status="PEAK_CONVENTION_DIAGNOSTIC",case=row["label"],coordinates=x.tolist(),rows=rows,
                polarization_peak_range_s=float(np.ptp([r["polarization_norm_peak_s"] for r in rows])),
                intrinsic_peak_range_s=float(np.ptp([r["intrinsic_faceon_peak_s"] for r in rows])),
                scope="Comparison of intrinsic 22 amplitude with inclination-weighted polarization norm; no old registration changed")
    write(ROOT/"C5_COHERENT_PEAK_DIAGNOSTIC.json",result);print(json.dumps(result),flush=True)


if __name__=="__main__":main()
