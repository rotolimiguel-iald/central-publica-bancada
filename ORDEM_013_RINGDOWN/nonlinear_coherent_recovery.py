"""Constructive nonlinear source degeneracy controls, not a Bayes approximation.

Finds explicit GR sources matching conditional dephased IMR injections. A valid
close candidate is an upper bound on best mismatch even if search is incomplete.
Does not interpret optimizer success as posterior coverage or event significance.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
from datetime import datetime,timezone
import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor,as_completed
import numpy as np
from scipy.optimize import minimize
from coherent_imr_model import network_basis,profile_fit,remnant
from tgl_ringdown_prediction import scales

ROOT=Path(__file__).resolve().parent
REG=ROOT/"REGISTRO_C5_NONLINEAR_COHERENT.json"
OUT=ROOT/"cache/nonlinear_coherent"
FAMILIES=("SEOBNRv4HM","IMRPhenomXPHM")
SOURCES=[dict(name="reference",mass=72.,q=39/33,s1=.05,s2=-.03,inclination=.6,phase=.37,psi=0.),
         dict(name="source_64",mass=64.,q=1.5,s1=.15,s2=.05,inclination=1.,phase=.8,psi=.22),
         dict(name="source_90",mass=90.,q=2.,s1=.25,s2=-.15,inclination=.9,phase=1.2,psi=.45)]
STEPS=np.array([.01,.02,.02,.02,.05,.05,.03])
WIDTH=np.array([.12,.3,.3,.3,.5,.5,.5])


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p,value,replace=False):
    if p.exists() and not replace:raise FileExistsError(p)
    raw=(json.dumps(value,indent=2,ensure_ascii=False)+"\n").encode();tmp=p.with_name(p.name+".tmp")
    tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError("Short write")
    tmp.replace(p)


def register():
    names=[Path(__file__).name,"coherent_imr_model.py","tgl_ringdown_prediction.py","QNM_GRID.json",
           "REGISTRO_C6.json","C5_SOURCE_UNCERTAINTY_SUMMARY.json",
           "cache/recolored_noise/O4_noise.npz","cache/recolored_noise/O5_noise.npz"]
    reg=dict(status="REGISTERED_NONBLIND_NONLINEAR_CONSTRUCTIVE_CONTROL",date_utc=datetime.now(timezone.utc).isoformat(),
             sources=SOURCES,families=FAMILIES,reading="R-B",injected_a=1.,recovery_a=0.,reference_SNR=40.,
             primary_PSD="O5",holdout_metric_PSD="O4",generation_sample_rate=8192,verification_sample_rate=16384,
             sample_rate=2048,n_samples=410,start="10 tM of injection-family remnant, fixed throughout each fit",
             unknowns=["log total mass","log mass ratio","spin1z","spin2z","inclination","orbital reference phase","peak shift in ms","distance","common polarization"],
             amplitude_treatment="Two real shared network columns exactly represent distance and one common polarization rotation; coefficients profiled by least squares. No independent harmonic/detector fitting coefficients.",
             search="Derivative-free bounded Powell, mass/common-spin/time stage maxfev150 then all seven nonlinear coordinates maxfev350; initialized at simulated source, local search only",
             local_half_widths=WIDTH.tolist(),conditioning_steps=STEPS.tolist(),
             physical_bounds="q in [1,4], spin1/spin2 in [-.8,.8], inclination in [.03,pi-.03]; intersect with local box",
             stopping="ftol1e-7,xtol1e-4; retain best explicit candidate even on evaluation-budget exit, never call it global optimum",
             acceptance="Report full residual norms and rate-doubling stability. A candidate residual below one at SNR40 is a constructive local degeneracy only if the high-rate residual remains below one. No universal exclusion rule or Bayes factor.",
             source_fidelity="Same whole-harmonic 22/44 damping as prior C5; other modes unchanged. A conditional readout, not a unique TGL overtone law.",
             no_noise_added=True,no_target_strain_read=True,no_C6_change=True,
             result_limits=["no posterior integration", "no varied-source noise coverage", "no blind discovery", "not complete astrophysical inference"],
             hashes={n:sha(ROOT/n) for n in names})
    write(REG,reg);print(json.dumps(dict(status=reg["status"],sha256=sha(REG),jobs=12)),flush=True)


def check():
    reg=json.loads(REG.read_bytes())
    for name,h in reg["hashes"].items():
        if sha(ROOT/name)!=h:raise ValueError("Registered input changed: "+name)
    return reg


def source_vector(source):
    return np.array([np.log(source["mass"]),np.log(source["q"]),source["s1"],source["s2"],source["inclination"],source["phase"],0.])


def fit_job(source,inj_family,rec_family):
    reg=check();label=f"{source['name']}_{inj_family}_to_{rec_family}"
    saved=OUT/(label+".json")
    if saved.exists():
        row=json.loads(saved.read_bytes())
        if row["registration_sha256"]!=sha(REG):raise ValueError("Checkpoint registry mismatch")
        return row
    x0=source_vector(source);q=source["q"];m1=source["mass"]*q/(1+q);m2=source["mass"]/(1+q)
    mf,spin=remnant(inj_family,m1,m2,source["s1"],source["s2"])
    times=np.arange(reg["n_samples"])/reg["sample_rate"]+10*scales(mf,"CODATA2018_IAU2015")[0]
    white={}
    for psd in ("O4","O5"):
        with np.load(ROOT/f"cache/recolored_noise/{psd}_noise.npz") as f:white[psd]=f["whitener_scaled"].copy()
    primary=white["O5"];orientation=np.array([np.cos(2*source["psi"]),np.sin(2*source["psi"])])
    injected,_=network_basis(inj_family,x0,times,"R-B",1.,primary,reg["generation_sample_rate"])
    raw_signal=injected@orientation;normalization=40/np.linalg.norm(raw_signal);target=raw_signal*normalization
    lower=-WIDTH.copy();upper=WIDTH.copy()
    lower[1]=max(lower[1],-x0[1]);upper[1]=min(upper[1],np.log(4)-x0[1])
    for k in (2,3):lower[k]=max(lower[k],-.8-x0[k]);upper[k]=min(upper[k],.8-x0[k])
    lower[4]=max(lower[4],.03-x0[4]);upper[4]=min(upper[4],np.pi-.03-x0[4])
    bounds=list(zip(lower/STEPS,upper/STEPS));best=dict(squared_residual=float("inf"));calls=0
    trace=OUT/(label+"_improvements.jsonl")
    if trace.exists():raise FileExistsError("Incomplete search exists; review before restarting")
    def objective(y):
        nonlocal calls,best
        x=x0+np.asarray(y)*STEPS
        basis,meta=network_basis(rec_family,x,times,"R-B",0.,primary,reg["generation_sample_rate"])
        value,coeff,residual=profile_fit(basis,target);calls+=1
        if not np.isfinite(value):raise ValueError("Nonfinite mismatch")
        if value<best["squared_residual"]:
            best=dict(squared_residual=value,x=x.tolist(),coefficients=coeff.tolist(),remnant=meta,calls=calls)
            with trace.open("ab") as f:f.write((json.dumps(best)+"\n").encode())
        if calls==1 or calls%25==0:
            write(OUT/(label+"_progress.json"),dict(label=label,calls=calls,best=best,date_utc=datetime.now(timezone.utc).isoformat()),replace=True)
        return value
    initial=objective(np.zeros(7))
    # Stage one explicitly changes both component spins equally.
    smallbounds=[bounds[0],(max(bounds[2][0],bounds[3][0]),min(bounds[2][1],bounds[3][1])),bounds[6]]
    def small(v):
        y=np.zeros(7);y[0]=v[0];y[2]=v[1];y[3]=v[1];y[6]=v[2]
        return objective(y)
    first=minimize(small,np.zeros(3),method="Powell",bounds=smallbounds,options=dict(maxfev=150,ftol=1e-7,xtol=1e-4))
    start=(np.array(best["x"])-x0)/STEPS
    second=minimize(objective,start,method="Powell",bounds=bounds,options=dict(maxfev=350,ftol=1e-7,xtol=1e-4))
    x=np.array(best["x"])
    controls=[]
    for psd,w in white.items():
        for rate in (8192,16384):
            inj,_=network_basis(inj_family,x0,times,"R-B",1.,w,rate)
            ref=inj@orientation;ref=ref*(40/np.linalg.norm(ref))
            basis,meta=network_basis(rec_family,x,times,"R-B",0.,w,rate)
            val,coef,resid=profile_fit(basis,ref)
            controls.append(dict(psd=psd,sample_rate=rate,residual_norm=float(np.sqrt(val)),squared_residual=val,
                                 coefficients=coef.tolist(),relative_residual=float(np.sqrt(val)/40),
                                 candidate_at_SNR600_residual=float(np.sqrt(val)*15)))
    a1basis,_=network_basis(inj_family,x0,times,"R-B",1.,primary,16384)
    closure=profile_fit(a1basis,a1basis@orientation)[0]
    near=all(c["residual_norm"]<1 for c in controls)
    row=dict(label=label,status="EXPLICIT_NEARBY_GR_CANDIDATE" if near else "CANDIDATE_NOT_SUBNOISE_IN_ALL_CONTROLS",
             source=source,injection_family=inj_family,recovery_family=rec_family,registration_sha256=sha(REG),
             initial_squared_residual=initial,best=best,evaluations=calls,
             stages=[dict(success=bool(r.success),message=str(r.message),nfev=int(r.nfev)) for r in (first,second)],
             controls=controls,high_rate_true_model_squared_residual=closure,
             boundary_distance_in_conditioned_coordinates=np.minimum((x-x0-lower)/STEPS,(upper-x+x0)/STEPS).tolist(),
             scope="Constructive mismatch upper bound from one local search; not global optimum, Bayes factor, measured significance or calibrated recovery")
    write(saved,row);return row


def run():
    reg=check();OUT.mkdir(exist_ok=True)
    result=ROOT/"C5_NONLINEAR_COHERENT.json"
    if result.exists():raise FileExistsError(result)
    jobs=[(s,a,b) for s in SOURCES for a in FAMILIES for b in FAMILIES]
    rows=[]
    with ProcessPoolExecutor(max_workers=4) as pool:
        pending={pool.submit(fit_job,*j):j for j in jobs}
        for future in as_completed(pending):
            row=future.result();rows.append(row)
            print(json.dumps(dict(label=row["label"],status=row["status"],calls=row["evaluations"],
                 residuals=[c["residual_norm"] for c in row["controls"]])),flush=True)
    rows.sort(key=lambda r:r["label"])
    write(result,dict(status="NONLINEAR_CONSTRUCTIVE_CONTROLS_COMPLETE",registration_sha256=sha(REG),results=rows,
                      subnoise_candidates=sum(r["status"]=="EXPLICIT_NEARBY_GR_CANDIDATE" for r in rows),
                      original_C6_unchanged=True,no_target_strain_read=True,not_completed=reg["result_limits"]))


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("command",choices=["register","run"]);a=p.parse_args()
    register() if a.command=="register" else run()
