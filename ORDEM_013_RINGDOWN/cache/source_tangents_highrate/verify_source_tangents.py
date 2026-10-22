"""Independent full-data-covariance check and numerical stability adjudication.

Does not import the production likelihood or projection helpers. A numerical
PASS concerns integration/custody; source inference remains local and conditional.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.linalg import cholesky, solve_triangular

ROOT=Path(__file__).resolve().parent


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    reg=json.loads((ROOT/"REGISTRO_C5_SOURCE_TANGENTS.json").read_bytes())
    for name,h in reg["hashes"].items():
        if digest(ROOT/name)!=h:raise ValueError("Registry changed: "+name)
    result=json.loads((ROOT/"C5_SOURCE_TANGENTS.json").read_bytes())
    if result["registration_sha256"]!=digest(ROOT/"REGISTRO_C5_SOURCE_TANGENTS.json"):
        raise ValueError("Result registration mismatch")
    manifest=ROOT/"C5_SOURCE_TANGENTS_INPUTS.json"
    if digest(manifest)!=result["input_manifest_sha256"]:raise ValueError("Source manifest changed")
    for row in json.loads(manifest.read_bytes())["rows"]:
        if digest(ROOT/row["path"])!=row["sha256"]:raise ValueError("Source waveform changed")
    path=ROOT/result["draws"]["path"]
    if digest(path)!=result["draws"]["sha256"]:raise ValueError("Draw arrays changed")
    errors=[];means=[]
    with np.load(path) as data:
        for i in range(result["oracle_count"]):
            prefix=f"oracle_{i}_";h0=data[prefix+"h0"];h1=data[prefix+"h1"]
            expected=data[prefix+"expected"];noise=data[prefix+"noise"]
            cs=[]
            for side in (0,1):
                b=data[prefix+f"b{side}"];c=np.eye(len(h0))+b@b.T
                lower=cholesky(c,lower=True)
                cs.append((lower,float(2*np.log(np.diag(lower)).sum())))
            actual=[]
            for truth in (h0,h1):
                values=[]
                for (lower,det),mean in zip(cs,(h0,h1)):
                    z=solve_triangular(lower,(noise+truth-mean).T,lower=True)
                    values.append(-.5*(np.sum(z*z,axis=0)+det))
                actual.append(values[1]-values[0])
            error=float(np.max(np.abs(np.array(actual)-expected)))
            errors.append(dict(label=str(data[prefix+"label"]),max_lnB_difference=error))
        for row in result["surrogate_evidence"]:
            sample=data["draws"][row["draw_index"]]
            if abs(float(sample.mean())-row["empirical_lnB"]["mean"])>1e-12:
                raise ValueError("Saved draw mean mismatch")
    stability=[]
    for family in reg["families"]:
        for psd in reg["psds"]:
            for reading in reg["readings"]:
                for a in (0.,1.):
                    rows=[r for r in result["geometries"] if (r["family"],r["psd"],r["reading"],r["a"] )==(family,psd,reading,a)]
                    primary=[r for r in rows if r["resolution"]=="4_hi" and r["rank_rtol"]==1e-8][0]
                    value=primary["z_local_at_SNR40_free_intrinsics"]
                    diffs={r["resolution"]:abs(r["z_local_at_SNR40_free_intrinsics"]-value)/max(value,1e-100)
                           for r in rows if r["rank_rtol"]==1e-8 and r["resolution"] in ("2","4")}
                    rankdiff=max(abs(r["z_local_at_SNR40_free_intrinsics"]-value)/max(value,1e-100)
                                 for r in rows if r["resolution"]=="4_hi")
                    controls=[r for r in result["derivative_checks"] if (r["family"],r["psd"],r["reading"],r["a"] )==(family,psd,reading,a)]
                    derr=max(r["projected_relative_differences_to_high"]["4"] for r in controls)
                    passed=max(diffs.values())<=.1 and rankdiff<=.1 and derr<=.05
                    stability.append(dict(family=family,psd=psd,reading=reading,a=a,
                         status="STABLE_LOCAL_DIAGNOSTIC" if passed else "NUMERICAL_SENSITIVITY_UNRESOLVED",
                         step_and_resolution_sensitivity=diffs,rank_sensitivity=rankdiff,derivative_resolution_error=derr,
                         z_fixed_SNR40=primary["z_local_at_SNR40_fixed_source"],
                         z_free_SNR40=value,retained_information_fraction=primary["retained_information_fraction"]))
    maxerr=max(r["max_lnB_difference"] for r in errors)
    if maxerr>1e-5:raise ValueError(f"Independent full covariance integration failed: {maxerr}")
    report=dict(status="PASS_NUMERICAL_INTEGRAL_NOT_FULL_SOURCE_INFERENCE",max_lnB_difference=maxerr,
                covariance_controls=errors,stability=stability,stable_cases=sum(r["status"]=="STABLE_LOCAL_DIAGNOSTIC" for r in stability),
                total_stability_cases=len(stability),no_event_significance=True,
                hashes={n:digest(ROOT/n) for n in ("REGISTRO_C5_SOURCE_TANGENTS.json","C5_SOURCE_TANGENTS_INPUTS.json","C5_SOURCE_TANGENTS.json",Path(__file__).name)})
    out=ROOT/"C5_SOURCE_TANGENTS_VALIDATION.json"
    if out.exists():raise FileExistsError(out)
    raw=(json.dumps(report,indent=2)+"\n").encode();tmp=out.with_suffix(".tmp")
    tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError("Short write")
    tmp.replace(out)
    print(json.dumps(dict(status=report["status"],max_lnB_difference=maxerr,
                         stable=report["stable_cases"],total=len(stability),B=[r for r in stability if r["reading"]=="R-B"])),flush=True)


if __name__=="__main__":main()
