"""Full covariance Cholesky check of B at all SNRs, priors and both injections.

Reconstruct higher-SNR design matrices from the stored SNR40 controls by
scaling physical time/source derivatives while keeping amplitude priors fixed.
This does not use the production SVD or evidence function.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
import json
import hashlib
import numpy as np
from scipy.linalg import cholesky,solve_triangular

ROOT=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    reports=[]
    for relative in (".","cache/source_tangents_refinement","cache/source_tangents_highrate"):
        base=ROOT/relative
        output=json.loads((base/"C5_SOURCE_TANGENTS.json").read_bytes())
        archive=base/output["draws"]["path"]
        if sha(archive)!=output["draws"]["sha256"]:raise ValueError("Changed draws")
        lookup={(r["family"],r["psd"],r["prior"],r["SNR"],r["injected_a"]):r["draw_index"]
                for r in output["surrogate_evidence"] if r["reading"]=="R-B"}
        differences=[]
        with np.load(archive) as data:
            for i in range(output["oracle_count"]):
                prefix=f"oracle_{i}_";label=str(data[prefix+"label"])
                family,tail=label.split("_O");digit,prior=tail.split("_",1);psd="O"+digit
                noise=data[prefix+"noise"]
                for snr in (40.,200.,600.):
                    scale=snr/40.;h=[data[prefix+f"h{j}"]*scale for j in (0,1)]
                    integrals=[]
                    for j in (0,1):
                        b=data[prefix+f"b{j}"].copy();b[:,12:]*=scale
                        c=np.eye(len(h[0]))+b@b.T;lower=cholesky(c,lower=True)
                        det=2*np.log(np.diag(lower)).sum();values=[]
                        for truth in h:
                            w=solve_triangular(lower,(noise+truth-h[j]).T,lower=True)
                            values.append(-.5*(np.sum(w*w,axis=0)+det))
                        integrals.append(np.array(values))
                    diff=integrals[1]-integrals[0]
                    for j in (0,1):
                        expected=data["draws"][lookup[(family,psd,prior,snr,float(j))],:3]
                        differences.extend(np.abs(diff[j]-expected).tolist())
        maximum=max(differences)
        if maximum>1e-5:raise ValueError(f"Integral discrepancy {relative}: {maximum}")
        reports.append(dict(run=relative,comparisons=len(differences),max_lnB_difference=maximum,
                            result_sha256=sha(base/"C5_SOURCE_TANGENTS.json"),draws_sha256=sha(archive)))
    result=dict(status="PASS",scope="R-B all three SNRs, both PSDs/families, all priors, both truths, first three fixed-source noise draws; no nonlinear inference claim",
                reports=reports,source_sha256=sha(Path(__file__)))
    out=ROOT/"C5_SOURCE_TANGENTS_EXTENDED_VALIDATION.json"
    if out.exists():raise FileExistsError(out)
    raw=(json.dumps(result,indent=2)+"\n").encode();tmp=out.with_suffix(".tmp");tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError("Short write")
    tmp.replace(out);print(json.dumps(result),flush=True)


if __name__=="__main__":main()
