"""Regenerate candidate waveforms and verify by a QR projection, at two rates.

This checks constructive candidates, not the global optimum of a nonlinear fit.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1",OMP_NUM_THREADS="1")
from pathlib import Path
import argparse
import hashlib
import json
import sys
import math
import numpy as np


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--run",required=True);args=parser.parse_args()
    root=Path(args.run).resolve();sys.path.insert(0,str(root))
    from coherent_imr_model import network_basis,remnant
    from nonlinear_coherent_recovery import source_vector
    from tgl_ringdown_prediction import scales
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    regpath=root/"REGISTRO_C5_NONLINEAR_COHERENT.json";reg=json.loads(regpath.read_bytes())
    for name,h in reg["hashes"].items():
        if sha(root/name)!=h:raise ValueError("Registered input changed: "+name)
    result=json.loads((root/"C5_NONLINEAR_COHERENT.json").read_bytes())
    if result["registration_sha256"]!=sha(regpath) or len(result["results"])!=12:
        raise ValueError("Unfinished or wrong run")
    white={}
    for psd in ("O4","O5"):
        with np.load(root/f"cache/recolored_noise/{psd}_noise.npz") as f:white[psd]=f["whitener_scaled"].copy()
    checks=[];maxerr=0.
    for row in result["results"]:
        s=row["source"];x0=source_vector(s);x=np.array(row["best"]["x"])
        mf,_=remnant(row["injection_family"],s["mass"]*s["q"]/(1+s["q"]),s["mass"]/(1+s["q"]),s["s1"],s["s2"])
        times=np.arange(410)/2048+10*scales(mf,"CODATA2018_IAU2015")[0]
        orientation=np.array([np.cos(2*s["psi"]),np.sin(2*s["psi"])])
        for psd,w in white.items():
            values=[]
            for rate in (16384,32768):
                inj,_=network_basis(row["injection_family"],x0,times,"R-B",1.,w,rate)
                target=inj@orientation;target*=40/np.linalg.norm(target)
                b,meta=network_basis(row["recovery_family"],x,times,"R-B",0.,w,rate)
                q,r=np.linalg.qr(b,mode="reduced")
                coef=np.linalg.solve(r,q.T@target);residual=target-b@coef
                norm=float(np.linalg.norm(residual));values.append(norm)
                if rate==16384:
                    expected=[c for c in row["controls"] if c["psd"]==psd and c["sample_rate"]==rate][0]["residual_norm"]
                    error=abs(norm-expected);maxerr=max(maxerr,error)
                    if error>1e-7:raise ValueError(f"Candidate QR replay differs: {row['label']} {error}")
                if not np.all(np.isfinite(coef)):raise ValueError("Nonfinite common polarization")
            # This is a Gaussian simple-pair power bound, not a Bayes-to-sigma conversion.
            r=values[-1]
            power=.5*math.erfc((5-r)/math.sqrt(2))
            checks.append(dict(label=row["label"],psd=psd,same_family=row["injection_family"]==row["recovery_family"],
                               residual_16384=values[0],residual_32768=r,rate_difference=abs(r-values[0]),
                               relative_rate_difference=abs(r-values[0])/max(r,1e-100),both_residuals_below_one=max(values)<1.,
                               gaussian_power_upper_bound_at_one_sided_5sigma=power,
                               nominal_SNR_lower_bound_for_half_power_at_5sigma=200/r if r>0 else None,
                               power_scope="Conditional unit-Gaussian noise, supplied templates and a size-controlled composite GR null containing this candidate; not empirical power"))
        print(json.dumps(dict(verified=row["label"])),flush=True)
    output=dict(status="PASS_CANDIDATE_REPLAY_NOT_FULL_INFERENCE",checks=checks,max_QR_difference=maxerr,
                gaussian_false_alarm_probability=.5*math.erfc(5/math.sqrt(2)),
                derivation="For means h0,h1 and unit covariance, S=<h1-h0,Y-h0>/r is N(0,1) under h0 and N(r,1) under h1. Any test controlling the composite-null size at Phi(-5) also controls it at this h0; the best simple-pair power is Phi(r-5).",
                unresolved="Calibration of non-Gaussian noise, nonlinear posterior integration and source-population forecasts remain open",
                hashes={p.name:sha(p) for p in (regpath,root/"C5_NONLINEAR_COHERENT.json")},verifier_sha256=sha(Path(__file__)))
    out=root/"C5_NONLINEAR_COHERENT_VALIDATION.json"
    if out.exists():raise FileExistsError(out)
    raw=(json.dumps(output,indent=2)+"\n").encode();tmp=out.with_suffix(".tmp");tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError("Short write")
    tmp.replace(out)
    print(json.dumps(dict(status=output["status"],max_QR_difference=maxerr,
                         same_family=[r for r in checks if r["same_family"]])),flush=True)


if __name__=="__main__":main()
