"""Separate registered quarter-step repetition; preserve all first-run evidence."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    run=ROOT/"cache/source_tangents_refinement"
    if run.exists():raise FileExistsError("Create-once refinement runner")
    run.mkdir()
    files=["prepare_source_tangents.py","analyze_source_tangents.py","verify_source_tangents.py",
           "tgl_ringdown_prediction.py","QNM_GRID.json","C5_IMR_CONTROLS.json","C5_RECOLORED_NOISE.json","REGISTRO_C6.json"]
    meta=json.loads((ROOT/"C5_RECOLORED_NOISE.json").read_bytes())
    files += [s["cache_path"] for s in meta["scenarios"] if s["psd"] in ("O4","O5")]
    for name in files:
        target=run/name;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((ROOT/name).read_bytes())
        if sha(target)!=sha(ROOT/name):raise ValueError("Copy differs")
    script=run/"prepare_source_tangents.py"
    original=script.read_bytes()
    before=b'AXES = {"log_total_mass": .01, "log_mass_ratio": .02,\n        "common_aligned_spin": .02, "difference_aligned_spin": .02}'
    after=b'AXES = {"log_total_mass": .0025, "log_mass_ratio": .005,\n        "common_aligned_spin": .005, "difference_aligned_spin": .005}'
    if original.count(before)!=1:raise ValueError("Unexpected generator structure")
    script.with_suffix(".py.original_bytes").write_bytes(original)
    temp=script.with_suffix(".tmp");temp.write_bytes(original.replace(before,after));temp.replace(script)
    provenance=dict(status="REGISTERED_REFINEMENT_PREPARATION",reason="SEOB projected derivatives fail initial step-size convergence; thresholds unchanged",
                    operation="All finite-difference steps divided by four; physical parameters, rates, noise, priors and all analysis/verifier code unchanged",
                    initial_result_sha256=sha(ROOT/"C5_SOURCE_TANGENTS.json"),
                    initial_validation_sha256=sha(ROOT/"C5_SOURCE_TANGENTS_VALIDATION.json"),
                    parent_inputs={name:sha(ROOT/name) for name in files},
                    amended_generator_sha256=sha(script))
    (run/"REFINEMENT_PROVENANCE.json").write_bytes((json.dumps(provenance,indent=2)+"\n").encode())
    commands=[("register",[sys.executable,"-B","prepare_source_tangents.py","register"]),
              ("generate",["/opt/pycbc_env/bin/python","-B","prepare_source_tangents.py","run"]),
              ("analyze",[sys.executable,"-B","analyze_source_tangents.py"]),
              ("verify",[sys.executable,"-B","verify_source_tangents.py"])]
    for stage,command in commands:
        with (run/(stage+".log")).open("xb") as log:
            process=subprocess.run(command,cwd=run,stdout=log,stderr=subprocess.STDOUT)
        print(json.dumps(dict(stage=stage,returncode=process.returncode)),flush=True)
        if process.returncode:raise RuntimeError("Refinement stage failed: "+stage)
    val=json.loads((run/"C5_SOURCE_TANGENTS_VALIDATION.json").read_bytes())
    print(json.dumps(dict(status=val["status"],stable=val["stable_cases"],total=val["total_stability_cases"],
                         B=[r for r in val["stability"] if r["reading"]=="R-B"])),flush=True)


if __name__=="__main__":main()
