"""Registered, non-blind local source-uncertainty experiment with actual IMR generators.

Nothing here reads event strain or changes C6. The output supports a local
identifiability diagnostic, not an astrophysical posterior or physical partition.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
REG = ROOT / "REGISTRO_C5_SOURCE_TANGENTS.json"
AXES = {"log_total_mass": .0025, "log_mass_ratio": .005,
        "common_aligned_spin": .005, "difference_aligned_spin": .005}
FAMILIES = ("SEOBNRv4HM", "IMRPhenomXPHM")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def create(p, value):
    if p.exists():
        raise FileExistsError(p)
    raw = (json.dumps(value, ensure_ascii=False, indent=2)+"\n").encode()
    tmp = p.with_name(p.name+".tmp")
    tmp.write_bytes(raw)
    if tmp.stat().st_size != len(raw):
        raise ValueError("Short write")
    tmp.replace(p)


def register():
    files = [Path(__file__).name, "analyze_source_tangents.py", "tgl_ringdown_prediction.py",
             "QNM_GRID.json", "C5_IMR_CONTROLS.json", "C5_RECOLORED_NOISE.json", "REGISTRO_C6.json"]
    scenarios = json.loads((ROOT/"C5_RECOLORED_NOISE.json").read_bytes())["scenarios"]
    files += [s["cache_path"] for s in scenarios if s["psd"] in ("O4", "O5")]
    reg = dict(status="REGISTERED_NONBLIND_LOCAL_SOURCE_DIAGNOSTIC",
               created_utc=datetime.now(timezone.utc).isoformat(),
               primary_parameters=json.loads((ROOT/"C5_IMR_CONTROLS.json").read_bytes())["parameters"],
               families=FAMILIES, axes=AXES, finite_difference_divisors=[1,2,4],
               primary_generation_rate_hz=16384, high_generation_rate_hz=32768,
               high_resolution_control="Central source and finest-step +/- for all four intrinsic axes",
               peak="Continuous maximum of isolated-22 polarization amplitude from a cubic spline within two samples of its discrete maximum",
               epoch="All harmonics share the original generator epoch; align to the same 22 peak, not their individual peaks",
               analysis_window="410 samples at 2048 Hz, fixed start 10 tM of the nominal family remnant; do not move data window as source mass changes",
               readings=["R-B","R-RAIZ-0","R-LIN","R-MOD"], psds=["O4","O5"], snrs=[40.,200.,600.],
               nuisance="12 independent harmonic-polarization amplitude columns, then shared peak time, then four physical source derivatives",
               rank_relative_thresholds=[1e-6,1e-8,1e-10], primary_rank_threshold=1e-8,
               stability_criterion="Compare step-halving and doubled generation rate. Relative projected-sensitivity change >10% or normalized tangent change >5% is NUMERICAL_SENSITIVITY_UNRESOLVED, not a physical conclusion",
               gaussian_surrogate="Means are exact a=0/1 at nominal source; covariance integrates centered Gaussian fluctuations in the local source and amplitude tangent. This is exact for the affine surrogate only, not nonlinear astrophysical PE.",
               source_prior_scenarios={"SOURCE_FIXED":0., "LOCAL_SIGMA_0_002":.002, "LOCAL_SIGMA_0_02":.02},
               prior_coordinates="Independent equal sd in log total mass, log mass ratio, common spin shift and difference spin shift; chosen diagnostic priors, not event information. Time sd=1e-4 s; each normalized harmonic amplitude sd=10 in 1e-21 strain units, centered on the nominal signal.",
               noise_indices=[50,256], no_target_strain_read=True,
               not_claimed=["nonlinear source marginalization", "calibrated source recovery", "blind forecast", "event significance", "unique physical TGL mapping"],
               hashes={f:sha(ROOT/f) for f in files})
    create(REG, reg)
    print(json.dumps(dict(status=reg["status"],sha256=sha(REG))),flush=True)


def parameters(base, axis, offset, sample_rate):
    p = dict(base, delta_t=1/sample_rate)
    mass=base["mass1"]+base["mass2"]; q=base["mass1"]/base["mass2"]
    if axis=="log_total_mass": mass *= np.exp(offset)
    if axis=="log_mass_ratio": q *= np.exp(offset)
    p["mass1"]=mass*q/(1+q); p["mass2"]=mass/(1+q)
    if axis=="common_aligned_spin":
        p["spin1z"]+=offset; p["spin2z"]+=offset
    if axis=="difference_aligned_spin":
        p["spin1z"]+=offset; p["spin2z"]-=offset
    return p


def run():
    import pycbc
    import lalsimulation as ls
    from pycbc.waveform import get_td_waveform
    from scipy.interpolate import CubicSpline
    from scipy.optimize import minimize_scalar
    reg=json.loads(REG.read_bytes())
    for name,h in reg["hashes"].items():
        if sha(ROOT/name)!=h: raise ValueError("Registered input changed: "+name)
    out=ROOT/"cache/source_tangents";out.mkdir(exist_ok=True)
    grid=np.arange(-.002,.210,1/32768)
    rows=[]
    for family in FAMILIES:
        specs=[("center",None,0.,16384),("center_hi",None,0.,32768)]
        for axis,step in AXES.items():
            for divisor in (1,2,4):
                for sign in (-1,1):
                    specs.append((f"{axis}_{divisor}_{'minus' if sign<0 else 'plus'}",axis,sign*step/divisor,16384))
            for sign in (-1,1):
                specs.append((f"{axis}_4_{'minus' if sign<0 else 'plus'}_hi",axis,sign*step/4,32768))
        for label,axis,offset,rate in specs:
            path=out/f"{family}_{label}.npz"; receipt=path.with_suffix(".json")
            if receipt.exists():
                row=json.loads(receipt.read_bytes())
                if row["registration_sha256"]!=sha(REG) or sha(path)!=row["sha256"]:
                    raise ValueError("Changed source checkpoint")
                rows.append(row);continue
            if path.exists():raise FileExistsError("Unreceipted source: "+str(path))
            pars=parameters(reg["primary_parameters"],axis,offset,rate)
            products={}
            for name,modes in (("all",None),("22",[(2,2)]),("44",[(4,4)])):
                opts=dict(pars,approximant=family)
                if modes:opts["mode_array"]=modes
                hp,hc=get_td_waveform(**opts)
                products[name]=(np.asarray(hp.sample_times),np.asarray(hp),np.asarray(hc))
            t,hp,hc=products["22"]; index=int(np.argmax(hp*hp+hc*hc))
            splp=CubicSpline(t,hp);splc=CubicSpline(t,hc)
            amplitude=float(hp[index]**2+hc[index]**2)
            opt=minimize_scalar(lambda x: -(float(splp(x))**2+float(splc(x))**2)/amplitude,
                                bounds=(t[index-2],t[index+2]),method="bounded",options={"xatol":1e-13})
            if not opt.success:raise ValueError("Continuous peak failed")
            peak=float(opt.x)
            arrays={"time_from_peak_s":grid}
            for name,(t,hp,hc) in products.items():
                if grid[0]+peak<t[0]:raise ValueError("Missing waveform start")
                if grid[-1]+peak>t[-1] and np.hypot(hp[-1],hc[-1])/max(np.hypot(hp,hc))>1e-5:
                    raise ValueError("Non-negligible missing waveform tail")
                for pol,values in (("plus",hp),("cross",hc)):
                    curve=CubicSpline(t,values,extrapolate=False)(grid+peak)
                    curve[grid+peak>t[-1]]=0.
                    if not np.all(np.isfinite(curve)):raise ValueError("Nonfinite waveform")
                    arrays[name+"_"+pol]=curve
            for pol in ("plus","cross"):
                arrays["other_"+pol]=arrays["all_"+pol]-arrays["22_"+pol]-arrays["44_"+pol]
            total=pars["mass1"]+pars["mass2"]
            if family=="SEOBNRv4HM":
                code,fraction,spin=ls.SimIMREOBFinalMassSpin(pars["mass1"],pars["mass2"],
                    [0.,0.,pars["spin1z"]],[0.,0.,pars["spin2z"]],ls.SEOBNRv4)
                if code!=0:raise ValueError("EOB remnant error")
            else:
                eta=pars["mass1"]*pars["mass2"]/total**2
                fraction=ls.SimIMRPhenomXFinalMass2017(eta,pars["spin1z"],pars["spin2z"])
                spin=ls.SimIMRPhenomXFinalSpin2017(eta,pars["spin1z"],pars["spin2z"])
            np.savez_compressed(path,**arrays)
            row=dict(family=family,label=label,axis=axis,offset=offset,sample_rate=rate,parameters=pars,
                     peak_s=peak,discrete_peak_s=float(products["22"][0][index]),
                     remnant_mass_detector_solar=float(total*fraction),remnant_spin=float(spin),
                     path=path.relative_to(ROOT).as_posix(),sha256=sha(path),registration_sha256=sha(REG))
            create(receipt,row);rows.append(row)
            print(json.dumps(dict(family=family,label=label,count=len(rows))),flush=True)
    create(ROOT/"C5_SOURCE_TANGENTS_INPUTS.json",dict(status="GENERATED",registration_sha256=sha(REG),
           pycbc_version=pycbc.__version__,lalsimulation_version=ls.__version__,rows=rows))


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("command",choices=["register","run"])
    args=parser.parse_args()
    register() if args.command=="register" else run()
