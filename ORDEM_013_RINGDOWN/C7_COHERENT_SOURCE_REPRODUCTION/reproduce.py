"""Fresh-directory generator and candidate replay; never modify packaged results."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/"MANIFEST.json").read_bytes())
for row in manifest["files"]:
    p=ROOT/row["path"]
    if hashlib.sha256(p.read_bytes()).hexdigest()!=row["sha256"]:
        raise ValueError("Package file changed: "+row["path"])
run=ROOT/"cache"/("replay_"+datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
run.mkdir(parents=True)
for row in manifest["files"]:
    name=row["path"]
    if name.startswith("expected/") or name in ("README.md","reproduce.py"):continue
    p=run/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/name).read_bytes())
for stage in ("validate_coherent_model.py","validate_coherent_likelihood.py","verify_nonlinear_coherent.py"):
    command=[sys.executable,"-B",stage]
    if stage.startswith("verify_"):command += ["--run",str(run)]
    with (run/(stage+".log")).open("xb") as log:
        proc=subprocess.run(command,cwd=run,stdout=log,stderr=subprocess.STDOUT)
    print(json.dumps(dict(stage=stage,exit_code=proc.returncode,run=str(run))),flush=True)
    if proc.returncode:raise RuntimeError(stage)
actual=json.loads((run/"C5_NONLINEAR_COHERENT_VALIDATION.json").read_bytes())
expected=json.loads((ROOT/"expected/C5_NONLINEAR_COHERENT_VALIDATION.json").read_bytes())
lookup={(r["label"],r["psd"]):r for r in expected["checks"]}
diff=0.
for r in actual["checks"]:
    old=lookup[(r["label"],r["psd"])]
    for key in ("residual_16384","residual_32768"):
        diff=max(diff,abs(r[key]-old[key]))
if diff>1e-7:raise ValueError("Candidate replay drift: "+str(diff))
receipt=dict(status="PASS",candidate_metrics=len(actual["checks"]),max_residual_difference=diff,
             scope="Regenerated source waveforms and QR candidate checks, not repeated optimization or full source PE")
(run/"RESULT.json").write_bytes((json.dumps(receipt,indent=2)+"\n").encode())
print(json.dumps(receipt),flush=True)
