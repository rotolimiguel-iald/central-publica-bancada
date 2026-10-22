"""Independent SVD oracle and coverage audit for the IMR recovery extension."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.special import logsumexp
from tgl_ringdown_prediction import prediction, scales

ROOT=Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    target=ROOT/"C5_IMR_RECOVERY_VALIDATION.json"
    if target.exists():raise FileExistsError(target)
    output=json.loads((ROOT/"C5_IMR_RECOVERY.json").read_bytes())
    reg=json.loads((ROOT/"REGISTRO_C5_IMR_RECOVERY.json").read_bytes())
    if sha(ROOT/"REGISTRO_C5_IMR_RECOVERY.json")!=output["registration_sha256"]:
        raise ValueError("Registry mismatch")
    for name,digest in reg["hashes"].items():
        if sha(ROOT/name)!=digest:raise ValueError("Registered input changed")
    families=json.loads((ROOT/"C5_IMR_CONTROLS.json").read_bytes())["families"]
    scenarios=json.loads((ROOT/"C5_RECOLORED_NOISE.json").read_bytes())["scenarios"]
    qs=json.loads((ROOT/"QNM_GRID.json").read_bytes())["modes"]
    spline={ell:CubicSpline(qs[str(ell)*2+"0"]["spins"],np.asarray(qs[str(ell)*2+"0"]["real"])+1j*np.asarray(qs[str(ell)*2+"0"]["imag"])) for ell in (2,4)}
    caches={}
    for item in output["draws"]:
        if sha(ROOT/item["path"])!=item["sha256"]:raise ValueError("Draws changed")
        p=np.load(ROOT/item["path"])
        caches[Path(item["path"]).stem.split("_")[0]]=p
    # Recount criteria from saved draws, not status strings.
    recomputed=0
    for row in output["results"]:
        values=caches[row["psd"]]["draws"][row["draws_index"]]
        if values.shape!=(206,4):raise ValueError("Missing injections")
        if not np.all(np.isfinite(values[:,0])):raise ValueError("Nonfinite Bayes ratio")
        if row["absolute_bias"] is None:
            if not np.all(np.isnan(values[:,1:])):raise ValueError("Unexpected unidentified estimates")
            continue
        bias=abs(float(np.median(values[:,1]))-row["injected_a"])
        coverage=float(np.mean((values[:,2]<=row["injected_a"])&(row["injected_a"]<=values[:,3])))
        if abs(bias-row["absolute_bias"])>1e-12 or coverage!=row["coverage_90"]:
            raise ValueError("Bias/coverage summary differs from draws")
        passed=bias<=.2 and .8<=coverage<=.97 and row["boundary_hits"]==0
        if passed!=(row["status"]=="CALIBRATED_CONDITIONAL_CELL"):
            raise ValueError("Cell criteria silently changed")
        recomputed+=1
    # Direct SVD integration of amplitude coefficients, bypassing the production
    # Gram-matrix solves and independently reconstructing all waveform columns.
    checks=[];scales_in_test=[]
    responses={"H1":(.7,.2),"L1":(-.3,.8)}
    for scenario in scenarios:
        if scenario["psd"] not in reg["computed_psds"]:continue
        with np.load(ROOT/scenario["cache_path"]) as data:
            white=data["whitener_scaled"].copy()
            noise={d:data[d+"_strain_scaled"][[50,153,255]]@white.T for d in responses}
        t=np.arange(410)/2048.
        raw=[]
        for family in families:
            peak_time=t+10*scales(family["remnant_mass_detector_solar"],"CODATA2018_IAU2015")[0]
            with np.load(ROOT/f"cache/imr_controls/{family['family']}.npz") as wave:
                v={k:np.interp(peak_time,wave["time_from_peak_s"],wave[k])*1e21 for k in
                   ("22_plus","22_cross","44_plus","44_cross","other_plus","other_cross")}
            norm={h:np.max(np.hypot(v[h+"_plus"],v[h+"_cross"])) for h in ("22","44","other")}
            raw.append((peak_time,v,norm))
        for reading in ("R-B","R-MOD"):
            svds=[];rates=[]
            for family,(time,v,norm) in zip(families,raw):
                rate={ell:prediction(family["remnant_mass_detector_solar"],family["remnant_spin"],reading,
                       mode=(ell,ell,0),qnm_dimensionless=complex(spline[ell](family["remnant_spin"])))['gamma_per_s'] for ell in (2,4)}
                rates.append(rate);perpoint=[]
                for a in (0.,1.):
                    matrix=np.column_stack([v[h+"_"+pol]/norm[h]*np.exp(-a*(rate[ell] if ell else 0)*time)
                           for h,ell in (("22",2),("44",4),("other",None)) for pol in ("plus","cross")])
                    u,s,_=np.linalg.svd(white@matrix,full_matrices=False)
                    perpoint.append((u,s))
                svds.append(perpoint)
            for famindex,family in enumerate(families):
                time,v,norm=raw[famindex]
                for a in (0.,1.):
                    signal={d:white@sum((fp*v[h+"_plus"]+fc*v[h+"_cross"])*np.exp(-a*(rates[famindex][ell] if ell else 0)*time)
                                        for h,ell in (("22",2),("44",4),("other",None))) for d,(fp,fc) in responses.items()}
                    source_norm=np.sqrt(sum(y@y for y in signal.values()))
                    for snr in (40.,600.):
                        observations={d:noise[d]+signal[d][None,:]*snr/source_norm for d in responses}
                        evidence=[]
                        for perpoint in svds:
                            atpoint=[]
                            for u,s in perpoint:
                                inv_fraction=s*s/(s*s+1/100.)
                                lnz=sum(.5*np.sum((observations[d]@u)**2*inv_fraction,axis=1)-.5*np.sum(np.log1p(100*s*s)) for d in observations)
                                atpoint.append(lnz)
                            evidence.append(np.array(atpoint))
                        mixture=logsumexp(np.array(evidence),axis=0)-np.log(2.)
                        for name,e in [(families[0]["family"],evidence[0]),(families[1]["family"],evidence[1]),("EQUAL_FAMILY_MIXTURE",mixture)]:
                            rows=[r for r in output["results"] if r["psd"]==scenario["psd"] and r["reading"]==reading and r["SNR"]==snr
                                  and r["injected_a"]==a and r["injection_family"]==family["family"] and r["recovery"]==name]
                            if len(rows)!=1:raise ValueError("Ambiguous oracle row")
                            row=rows[0];published=caches[row["psd"]]["draws"][row["draws_index"],[0,103,205],0]
                            difference=e[1]-e[0]-published
                            checks.append(dict(psd=row["psd"],reading=reading,SNR=snr,truth=a,
                                               injection_family=family["family"],recovery=name,
                                               max_abs_difference=float(np.max(abs(difference)))))
    max_error=max(c["max_abs_difference"] for c in checks)
    # The same-family/noiseless control must include the injected waveform in
    # its basis. That property alone is not cross-family physical calibration.
    same=[r for r in output["results"] if r["recovery"]==r["injection_family"] and r["absolute_bias"] is not None]
    residual=max(abs(r["noiseless_residual_norm_squared"]) for r in same)
    passed=max_error<1e-6 and residual<1e-6
    result=dict(status="PASS" if passed else "FAILED",registered_inputs_unchanged=True,
                criteria_recomputed_cells=recomputed,independent_SVD_cells=len(checks),
                independent_SVD_draws=3*len(checks),max_lnB_abs_difference=max_error,
                max_same_family_noiseless_residual_squared=residual,
                checks=checks,production_sha256=sha(ROOT/"calibrate_imr_recovery.py"),
                result_sha256=sha(ROOT/"C5_IMR_RECOVERY.json"),verifier_sha256=sha(Path(__file__)),
                scope="Numerical and criteria audit, not acceptance of the model outside its two-family fixed-source set")
    tmp=target.with_suffix(".json.tmp");tmp.write_bytes((json.dumps(result,indent=2)+"\n").encode());tmp.replace(target)
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}),flush=True)
    if not passed:raise SystemExit(1)


if __name__=="__main__":main()
