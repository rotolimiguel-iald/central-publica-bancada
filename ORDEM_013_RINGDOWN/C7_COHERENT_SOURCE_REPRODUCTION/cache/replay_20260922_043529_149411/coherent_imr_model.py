"""Direct nonlinear aligned-binary IMR model with coherent network polarizations.

No independent per-detector or per-harmonic fitting amplitudes. The two columns
are precisely the common distance/polarization rotation, not unrelated modes.
Whole-harmonic TGL damping remains an explicit conditional readout.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from functools import lru_cache
from pathlib import Path
import json
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
from pycbc.waveform import get_td_waveform
import lalsimulation as ls
from tgl_ringdown_prediction import prediction, scales

ROOT=Path(__file__).resolve().parent
RESPONSES=((.7,.2),(-.3,.8))


@lru_cache(maxsize=1)
def qnm_splines():
    modes=json.loads((ROOT/"QNM_GRID.json").read_bytes())["modes"]
    return {ell:CubicSpline(modes[str(ell)*2+"0"]["spins"],
                           np.array(modes[str(ell)*2+"0"]["real"])+1j*np.array(modes[str(ell)*2+"0"]["imag"])) for ell in (2,4)}


def remnant(family,m1,m2,s1,s2):
    if family=="SEOBNRv4HM":
        code,fraction,chi=ls.SimIMREOBFinalMassSpin(m1,m2,[0.,0.,s1],[0.,0.,s2],ls.SEOBNRv4)
        if code!=0:raise ValueError("EOB remnant failure")
    elif family=="IMRPhenomXPHM":
        eta=m1*m2/(m1+m2)**2
        fraction=ls.SimIMRPhenomXFinalMass2017(eta,s1,s2)
        chi=ls.SimIMRPhenomXFinalSpin2017(eta,s1,s2)
    else:raise ValueError("Unsupported registered family")
    return float((m1+m2)*fraction),float(chi)


@lru_cache(maxsize=32)
def source_curves(family,coordinates,sample_rate,include44):
    lm,lq,s1,s2,inclination,phase=coordinates
    mass=np.exp(lm);q=np.exp(lq);m1=mass*q/(1+q);m2=mass/(1+q)
    if not 1<=q<=4 or max(abs(s1),abs(s2))>.8 or not 0<inclination<np.pi:
        raise ValueError("Unphysical source coordinates")
    pars=dict(mass1=m1,mass2=m2,spin1z=s1,spin2z=s2,spin1x=0.,spin1y=0.,spin2x=0.,spin2y=0.,
              inclination=inclination,coa_phase=phase,distance=403.,delta_t=1/sample_rate,f_lower=20.,f_ref=20.,approximant=family)
    products={}
    modes=[("all",None)]+([("22",[(2,2)]),("44",[(4,4)])] if include44 else [])
    for label,selection in modes:
        args=dict(pars)
        if selection:args["mode_array"]=selection
        hp,hc=get_td_waveform(**args)
        t=np.asarray(hp.sample_times);p=np.asarray(hp)*1e21;c=np.asarray(hc)*1e21
        products[label]=(t,p,c)
    # The intrinsic complex 22 amplitude is measured face-on. Its norm is
    # independent of inclination and orbital phase, unlike the projected norm.
    face_args=dict(pars,inclination=0.,mode_array=[(2,2)])
    face_p,face_c=get_td_waveform(**face_args)
    t=np.asarray(face_p.sample_times);p=np.asarray(face_p)*1e21;c=np.asarray(face_c)*1e21
    index=int(np.argmax(p*p+c*c));amplitude=p[index]**2+c[index]**2
    sp=CubicSpline(t,p);sc=CubicSpline(t,c)
    peak=minimize_scalar(lambda x:-(float(sp(x))**2+float(sc(x))**2)/amplitude,
                         bounds=(t[index-2],t[index+2]),method="bounded",options={"xatol":1e-13})
    if not peak.success:raise ValueError("Peak alignment failed")
    curves={}
    for label,(t,p,c) in products.items():
        ratio=float(np.hypot(p[-1],c[-1])/max(np.hypot(p,c)))
        curves[label]=(CubicSpline(t-peak.x,p,extrapolate=False),CubicSpline(t-peak.x,c,extrapolate=False),
                       float(t[0]-peak.x),float(t[-1]-peak.x),ratio)
    mf,spin=remnant(family,m1,m2,s1,s2)
    return curves,mf,spin,float(peak.x)


def polarizations(family,x,times,reading,a,sample_rate=8192):
    x=np.asarray(x,dtype=float)
    if x.shape!=(7,):raise ValueError("Expected six intrinsic/orientation coordinates and time in milliseconds")
    curves,mf,spin,peak=source_curves(family,tuple(x[:6]),sample_rate,a!=0.)
    t=np.asarray(times)-x[6]*1e-3
    if min(t)<0:raise ValueError("The entire ringdown interval must lie after the trial peak")
    def evaluate(name):
        p,c,start,end,ratio=curves[name]
        if min(t)<start or (max(t)>end and ratio>1e-5):raise ValueError("Missing finite waveform interval")
        hp=np.asarray(p(t));hc=np.asarray(c(t));hp[t>end]=0.;hc[t>end]=0.
        if not np.all(np.isfinite(hp)) or not np.all(np.isfinite(hc)):raise ValueError("Nonfinite waveform")
        return hp,hc
    hp,hc=evaluate("all")
    if a!=0.:
        for ell in (2,4):
            gamma=prediction(mf,spin,reading,mode=(ell,ell,0),qnm_dimensionless=complex(qnm_splines()[ell](spin)))["gamma_per_s"]
            delta=np.expm1(-a*gamma*t);p,c=evaluate(str(ell)*2)
            hp=hp+delta*p;hc=hc+delta*c
    return hp,hc,dict(remnant_mass=mf,remnant_spin=spin,peak_generator_s=peak)


def network_basis(family,x,times,reading,a,white,sample_rate=8192):
    hp,hc,meta=polarizations(family,x,times,reading,a,sample_rate)
    first=[];second=[]
    for fp,fc in RESPONSES:
        first.append(white@(fp*hp+fc*hc))
        second.append(white@(fc*hp-fp*hc))
    return np.column_stack([np.concatenate(first),np.concatenate(second)]),meta


def profile_fit(basis,target):
    coefficients=np.linalg.lstsq(basis,target,rcond=None)[0]
    residual=target-basis@coefficients
    return float(residual@residual),coefficients,residual
