"""Reproduce the conditional IMR recovery experiment from frozen derived inputs."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(actual,expected,where="root"):
    if isinstance(expected,dict):
        if not isinstance(actual,dict) or actual.keys()!=expected.keys():raise ValueError("Keys differ: "+where)
        return sum(compare(actual[k],v,where+"."+k) for k,v in expected.items())
    if isinstance(expected,list):
        if not isinstance(actual,list) or len(actual)!=len(expected):raise ValueError("Lists differ: "+where)
        return sum(compare(a,b,where+f"[{i}]") for i,(a,b) in enumerate(zip(actual,expected)))
    if isinstance(expected,(float,int)) and not isinstance(expected,bool):
        if not isinstance(actual,(float,int)) or isinstance(actual,bool):raise ValueError("Type differs: "+where)
        if not np.isclose(actual,expected,rtol=1e-10,atol=1e-7):raise ValueError("Number differs: "+where)
        return 1
    if actual!=expected:raise ValueError("Identity/statute differs: "+where)
    return 0


def main():
    manifest=json.loads((ROOT/"MANIFEST.json").read_bytes())
    for r in manifest["files"]:
        rel=PurePosixPath(r["path"])
        if rel.is_absolute() or ".." in rel.parts or "\\" in r["path"]:raise ValueError("Unsafe path")
        p=(ROOT/r["path"]).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file() or digest(p)!=r["sha256"]:raise ValueError("Missing or altered package file")
    run=ROOT/"cache"/("run_"+datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    shutil.copytree(ROOT/"assets",run)
    for name,args in [("calibrate_imr_recovery.py",["run"]),("verify_imr_recovery.py",[])]:
        subprocess.run([sys.executable,"-B",str(run/name),*args],check=True)
    actual=json.loads((run/"C5_IMR_RECOVERY.json").read_bytes())
    expected=json.loads((ROOT/"evidence/C5_IMR_RECOVERY.json").read_bytes())
    # Container hashes of regenerated NPZ archives are checked against each
    # computation's receipt below; numerical arrays are the portable invariant.
    for item in actual["draws"]:
        if digest(run/item["path"])!=item["sha256"]:raise ValueError("Regenerated draws changed")
    masked_a={k:v for k,v in actual.items() if k!="draws"}
    masked_e={k:v for k,v in expected.items() if k!="draws"}
    numeric=compare(masked_a,masked_e)
    array_checks=[]
    for old,new in zip(expected["draws"],actual["draws"]):
        if old["path"]!=new["path"]:raise ValueError("Draw identity differs")
        with np.load(ROOT/"evidence"/old["path"]) as a, np.load(run/new["path"]) as b:
            if a.files!=b.files:raise ValueError("Array keys differ")
            for key in a.files:
                if a[key].dtype.kind in "fiu":
                    if not np.allclose(a[key],b[key],rtol=1e-10,atol=1e-7,equal_nan=True):raise ValueError("Draw values differ")
                    values=abs(a[key]-b[key]); finite=values[np.isfinite(values)]
                    array_checks.append(dict(archive=new["path"],key=key,max_absolute_difference=float(finite.max()) if finite.size else 0))
                elif not np.array_equal(a[key],b[key]):raise ValueError("Array identity differs")
    validation=json.loads((run/"C5_IMR_RECOVERY_VALIDATION.json").read_bytes())
    if validation["status"]!="PASS":raise ValueError("Fresh SVD oracle failed")
    result=dict(status="PASS",numeric_fields=numeric,arrays=array_checks,
                cells=len(actual["results"]),joint_mixture_groups=sum(r["pass_all_four"] for r in actual["joint_mixture_criteria"]),
                raw_waveforms_or_noise_regenerated=False,
                scope="Fresh fit/oracle from hash-checked derived IMR and recolored-noise arrays; raw-input production is in the earlier C7_INJECTION_REPRODUCTION",
                run_directory=run.relative_to(ROOT).as_posix())
    path=run/"RESULT.json";path.write_bytes((json.dumps(result,indent=2)+"\n").encode())
    print(json.dumps(result),flush=True)


if __name__=="__main__":main()
