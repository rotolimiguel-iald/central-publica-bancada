"""Double the generation/sample-interpolation rate after measured resolution failure.

Keeps quarter-step priors/criteria unchanged and preserves both previous runs.
"""
from pathlib import Path
import json
import hashlib
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    previous=ROOT/"cache/source_tangents_refinement"
    run=ROOT/"cache/source_tangents_highrate"
    if run.exists():raise FileExistsError("Create-once high-resolution control")
    run.mkdir()
    reg=json.loads((previous/"REGISTRO_C5_SOURCE_TANGENTS.json").read_bytes())
    names=list(reg["hashes"])+["verify_source_tangents.py"]
    for name in names:
        p=run/name;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes((previous/name).read_bytes())
        if sha(p)!=sha(previous/name):raise ValueError("Source copy changed")
    generator=run/"prepare_source_tangents.py";old=generator.read_bytes()
    generator.with_suffix(".py.original_bytes").write_bytes(old)
    replacements={b"8192":b"16384",b"16384":b"32768"}
    new=re.sub(rb"\b(?:8192|16384)\b",lambda m:replacements[m[0]],old)
    if new==old:raise ValueError("Missing rate settings")
    tmp=generator.with_suffix(".tmp");tmp.write_bytes(new);tmp.replace(generator)
    provenance=dict(reason="Quarter-step SEOB mass-ratio and spin-difference derivatives still depend on generation rate; double both rates, without changing criteria",
                    previous_validation_sha256=sha(previous/"C5_SOURCE_TANGENTS_VALIDATION.json"),
                    previous_generator_sha256=hashlib.sha256(old).hexdigest(),new_generator_sha256=sha(generator),
                    code_change="Only integer rate tokens 8192->16384 and 16384->32768 in the copied generator, including interpolation grid")
    (run/"REFINEMENT_PROVENANCE.json").write_bytes((json.dumps(provenance,indent=2)+"\n").encode())
    for label,command in (("register",[sys.executable,"-B","prepare_source_tangents.py","register"]),
                          ("generate",["/opt/pycbc_env/bin/python","-B","prepare_source_tangents.py","run"]),
                          ("analyze",[sys.executable,"-B","analyze_source_tangents.py"]),
                          ("verify",[sys.executable,"-B","verify_source_tangents.py"])):
        with (run/(label+".log")).open("xb") as log:
            proc=subprocess.run(command,cwd=run,stdout=log,stderr=subprocess.STDOUT)
        print(json.dumps(dict(stage=label,returncode=proc.returncode)),flush=True)
        if proc.returncode:raise RuntimeError(label)
    val=json.loads((run/"C5_SOURCE_TANGENTS_VALIDATION.json").read_bytes())
    print(json.dumps(dict(stable=val["stable_cases"],total=val["total_stability_cases"],
                         B=[r for r in val["stability"] if r["reading"]=="R-B"])),flush=True)


if __name__=="__main__":main()
