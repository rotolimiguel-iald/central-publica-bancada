"""Local source geometry and proper affine-surrogate Gaussian evidence.

The Gaussian integral is exact for its explicitly linearized model only.
Source priors are diagnostic inputs, not estimates from the observed event.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
import json
import numpy as np
from scipy.interpolate import CubicSpline
from prepare_source_tangents import ROOT, REG, AXES, sha, create
from tgl_ringdown_prediction import prediction, scales

RESPONSES=((.7,.2),(-.3,.8))


def projection(columns, vectors, rtol=1e-8):
    norms=np.linalg.norm(columns,axis=0)
    keep=norms>0
    u,s,_=np.linalg.svd(columns[:,keep]/norms[keep],full_matrices=False)
    rank=int(np.sum(s>s[0]*rtol))
    q=u[:,:rank]
    return vectors-q@(q.T@vectors),rank,s


def covariance(columns):
    u,s,_=np.linalg.svd(columns,full_matrices=False)
    weight=s*s/(1+s*s)
    return u,weight,float(np.log1p(s*s).sum())


def inverse(cov, x):
    u,w,_=cov
    return x-u@(w*(u.T@x)) if x.ndim==1 else x-(x@u*w)@u.T


def evidence(cov, residual):
    u,w,logdet=cov
    return -.5*(np.sum(residual*residual,axis=-1)-np.sum((residual@u)**2*w,axis=-1)+logdet)


def gaussian_moments(c0,c1,h0,h1,true):
    # Exact moments for unit-Gaussian detector noise at a fixed source, not
    # a source drawn from the prior and not an empirical-Gaussian assertion.
    u0,w0,l0=c0;u1,w1,l1=c1
    trA=float(w1.sum()-w0.sum())
    trA2=float(w1@w1+w0@w0-2*np.sum((u0.T@u1)**2*w0[:,None]*w1[None,:]))
    r0=true-h0;r1=true-h1
    lin=inverse(c0,r0)-inverse(c1,r1)
    const=.5*(r0@inverse(c0,r0)-r1@inverse(c1,r1))-.5*(l1-l0)
    return dict(mean=float(const+.5*trA),sd=float(np.sqrt(max(0.,.5*trA2+lin@lin))))


def main():
    reg=json.loads(REG.read_bytes())
    for name,h in reg["hashes"].items():
        if sha(ROOT/name)!=h:raise ValueError("Registered input changed: "+name)
    manifest=json.loads((ROOT/"C5_SOURCE_TANGENTS_INPUTS.json").read_bytes())
    if manifest["registration_sha256"]!=sha(REG):raise ValueError("Different source registry")
    grid=json.loads((ROOT/"QNM_GRID.json").read_bytes())["modes"]
    qm={ell:CubicSpline(grid[str(ell)*2+"0"]["spins"],np.array(grid[str(ell)*2+"0"]["real"])+1j*np.array(grid[str(ell)*2+"0"]["imag"])) for ell in (2,4)}
    scenarios=json.loads((ROOT/"C5_RECOLORED_NOISE.json").read_bytes())["scenarios"]
    geometries=[];derivative_checks=[];evidences=[];draws=[];oracles=[]
    for family in reg["families"]:
        source={r["label"]:r for r in manifest["rows"] if r["family"]==family}
        curves={}
        for name,row in source.items():
            if sha(ROOT/row["path"])!=row["sha256"]:raise ValueError("Source waveform changed")
            with np.load(ROOT/row["path"]) as f:
                curves[name]={key:CubicSpline(f["time_from_peak_s"],f[key]*1e21) for key in
                              ("22_plus","22_cross","44_plus","44_cross","other_plus","other_cross")}
        start=10*scales(source["center_hi"]["remnant_mass_detector_solar"],"CODATA2018_IAU2015")[0]
        times=np.arange(410)/2048.+start
        for scenario in scenarios:
            if scenario["psd"] not in reg["psds"]:continue
            with np.load(ROOT/scenario["cache_path"]) as f:
                white=f["whitener_scaled"].copy()
                noise=np.hstack([f[d+"_strain_scaled"][50:256]@white.T for d in ("H1","L1")])
            n=white.shape[0]
            for reading in reg["readings"]:
                def evaluate(label,a):
                    row=source[label];cs=curves[label]
                    raw=[];d_amp=[];d_time=[]
                    for name,ell in (("22",2),("44",4),("other",None)):
                        gamma=0. if ell is None else prediction(row["remnant_mass_detector_solar"],row["remnant_spin"],reading,
                                     mode=(ell,ell,0),qnm_dimensionless=complex(qm[ell](row["remnant_spin"]))) ["gamma_per_s"]
                        for pol in ("plus","cross"):
                            v=cs[name+"_"+pol](times); envelope=np.exp(-a*gamma*times)
                            raw.append(v*envelope)
                            d_amp.append(-gamma*times*v*envelope)
                            d_time.append((cs[name+"_"+pol](times,1)-a*gamma*v)*envelope)
                    raw=np.column_stack(raw);da=np.column_stack(d_amp);dt=np.column_stack(d_time)
                    physical=np.array([[fp,fc]*3 for fp,fc in RESPONSES])
                    h=np.concatenate([white@(raw@p) for p in physical])
                    deriv=np.concatenate([white@(da@p) for p in physical])
                    timing=np.concatenate([white@(dt@p) for p in physical])
                    # Freeze amplitude coordinates across hypotheses at nominal a=0.
                    nom=curves["center_hi"]
                    norm=np.repeat([max(np.hypot(nom[name+"_plus"](times),nom[name+"_cross"](times))) for name in ("22","44","other")],2)
                    basis=np.zeros((2*n,12))
                    for k in range(2):basis[k*n:(k+1)*n,6*k:6*(k+1)]=white@(raw/norm)
                    return dict(h=h,da=deriv,time=timing,basis=basis)
                prepared={}
                for a in (0.,1.):
                    central=evaluate("center_hi",a);normalization=np.linalg.norm(evaluate("center_hi",0.)["h"])
                    amplitude_timing=np.column_stack([central["basis"],central["time"]])
                    derivatives={}
                    for resolution in ("1","2","4","4_hi"):
                        divisor=int(resolution.split("_")[0]);suffix="_hi" if resolution.endswith("hi") else ""
                        cols=[]
                        for axis,step in AXES.items():
                            plus=evaluate(f"{axis}_{divisor}_plus{suffix}",a)["h"]
                            minus=evaluate(f"{axis}_{divisor}_minus{suffix}",a)["h"]
                            cols.append((plus-minus)/(2*step/divisor))
                        derivatives[resolution]=np.column_stack(cols)
                        columns=np.column_stack([amplitude_timing,derivatives[resolution]])
                        for rtol in reg["rank_relative_thresholds"]:
                            ortho,rank,s=projection(columns,central["da"],rtol)
                            amp,_rank,_s=projection(central["basis"],central["da"],rtol)
                            timed,_rank,_s=projection(amplitude_timing,central["da"],rtol)
                            geometries.append(dict(family=family,psd=scenario["psd"],reading=reading,a=a,
                                  resolution=resolution,rank_rtol=rtol,rank=rank,singular_values=s.tolist(),
                                  z_local_at_SNR40_fixed_source=float(40*np.linalg.norm(amp)/normalization),
                                  z_local_at_SNR40_free_time=float(40*np.linalg.norm(timed)/normalization),
                                  z_local_at_SNR40_free_intrinsics=float(40*np.linalg.norm(ortho)/normalization),
                                  retained_information_fraction=float(ortho@ortho/(amp@amp))))
                    for axis_index,axis in enumerate(AXES):
                        base=projection(amplitude_timing,derivatives["4_hi"][:,axis_index])[0]
                        checks={}
                        for name in ("1","2","4"):
                            diff=projection(amplitude_timing,derivatives[name][:,axis_index]-derivatives["4_hi"][:,axis_index])[0]
                            checks[name]=float(np.linalg.norm(diff)/np.linalg.norm(base))
                        derivative_checks.append(dict(family=family,psd=scenario["psd"],reading=reading,a=a,axis=axis,
                                                      projected_relative_differences_to_high=checks))
                    central["source"]=derivatives["4_hi"];prepared[a]=central
                for snr in reg["snrs"]:
                    scale=snr/np.linalg.norm(prepared[0.]["h"])
                    h0=prepared[0.]["h"]*scale;h1=prepared[1.]["h"]*scale
                    for prior,sd in reg["source_prior_scenarios"].items():
                        bases=[];covs=[]
                        for a in (0.,1.):
                            p=prepared[a]
                            b=np.column_stack([10*p["basis"],p["time"]*scale*1e-4,p["source"]*scale*sd])
                            bases.append(b);covs.append(covariance(b))
                        for a in (0.,1.):
                            true=h0 if a==0 else h1
                            lnb=evidence(covs[1],noise+true-h1)-evidence(covs[0],noise+true-h0)
                            row=dict(family=family,psd=scenario["psd"],reading=reading,SNR=snr,prior=prior,injected_a=a,N=len(noise),
                                     status="AFFINE_SURROGATE_ONLY_NOT_ASTROPHYSICAL_EVIDENCE",draw_index=len(draws),
                                     empirical_lnB=dict(mean=float(np.mean(lnb)),sd=float(np.std(lnb,ddof=1)),q05_50_95=np.quantile(lnb,[.05,.5,.95]).tolist()),
                                     gaussian_fixed_source_lnB=gaussian_moments(*covs,h0,h1,true))
                            evidences.append(row);draws.append(lnb)
                        if reading=="R-B" and snr==40.:
                            oracles.append(dict(label=f"{family}_{scenario['psd']}_{prior}",
                                                h0=h0,h1=h1,b0=bases[0],b1=bases[1],noise=noise[:3],
                                                expected=np.array([[evidence(covs[1],noise[:3]+h-h1)-evidence(covs[0],noise[:3]+h-h0)] for h in (h0,h1)]).reshape(2,3)))
                print(json.dumps(dict(family=family,psd=scenario["psd"],reading=reading,cells=len(evidences))),flush=True)
    cache=ROOT/"cache/source_tangents/analysis_draws.npz"
    if cache.exists():raise FileExistsError(cache)
    values={"draws":np.array(draws)}
    for i,case in enumerate(oracles):
        for key,value in case.items():values[f"oracle_{i}_{key}"]=value
    np.savez_compressed(cache,**values)
    create(ROOT/"C5_SOURCE_TANGENTS.json",dict(status="LOCAL_SOURCE_DIAGNOSTIC_NOT_FULL_PE",registration_sha256=sha(REG),
           input_manifest_sha256=sha(ROOT/"C5_SOURCE_TANGENTS_INPUTS.json"),geometries=geometries,
           derivative_checks=derivative_checks,surrogate_evidence=evidences,oracle_count=len(oracles),
           draws=dict(path=cache.relative_to(ROOT).as_posix(),sha256=sha(cache)),
           scientific_scope=reg["not_claimed"],original_C6_unchanged=True,no_target_strain_read=True))


if __name__=="__main__":main()
