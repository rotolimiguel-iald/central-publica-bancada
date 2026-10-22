"""Small English reproduction package for corrected coherent source candidates."""
from pathlib import Path
import json
import hashlib
import zipfile

ROOT=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    source=ROOT/"cache/nonlinear_intrinsic_peak"
    package=ROOT/"C7_COHERENT_SOURCE_REPRODUCTION"
    if package.exists():raise FileExistsError("Create-once package")
    reg=json.loads((source/"REGISTRO_C5_NONLINEAR_COHERENT.json").read_bytes())
    result=json.loads((source/"C5_NONLINEAR_COHERENT.json").read_bytes())
    if len(result["results"])!=12:raise ValueError("Candidate set is unfinished")
    for n,h in reg["hashes"].items():
        if sha(source/n)!=h:raise ValueError("Registered input changed")
    package.mkdir()
    names=list(reg["hashes"])+["REGISTRO_C5_NONLINEAR_COHERENT.json","C5_NONLINEAR_COHERENT.json",
           "PEAK_CORRECTION_PROVENANCE.json","coherent_imr_likelihood.py","tgl_ringdown_likelihood.py",
           "validate_coherent_model.py","validate_coherent_likelihood.py"]
    for name in names:
        p=package/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((source/name).read_bytes())
    for name in ("verify_nonlinear_coherent.py","C5_COHERENT_PEAK_DIAGNOSTIC.json"):
        (package/name).write_bytes((ROOT/name).read_bytes())
    (package/"expected").mkdir()
    for name in ("C5_COHERENT_MODEL_VALIDATION.json","C5_COHERENT_LIKELIHOOD_VALIDATION.json","C5_NONLINEAR_COHERENT_VALIDATION.json"):
        (package/"expected"/name).write_bytes((source/name).read_bytes())
    text='''# Conditional coherent IMR source controls

Research supplement, not an event significance or full source posterior.
TGL: Luiz Antonio Rotoli Miguel. Public waveform generators: LALSuite/PyCBC.

## What is new

The source varies nonlinearly in total mass, mass ratio, both aligned spins,
inclination, orbital phase and peak time. Distance and one polarization angle
are shared by the entire two-detector network. There are no independent fitted
amplitudes for each harmonic or detector.

Three simulated aligned binaries are dephased under the existing conditional
mass-clock reading B. GR candidates are found in both SEOBNRv4HM and the aligned
limit of IMRPhenomXPHM. These are local constructive mismatch bounds, not global
optimizer guarantees, Bayes ratios or bias/coverage calibration.

The corrected reference is the intrinsic complex-22 amplitude maximum, evaluated
face-on before projecting to the source orientation. The previous projected-norm
reference could jump between carrier peaks as resolution changed. The diagnostic
and provenance are included. Old C6 and all earlier runs remain unchanged.

## Physical and statistical scope

The effective ensemble envelope damps each entire 22/44 harmonic by its fundamental
Gamma; other harmonics are unchanged. This is an explicit conditional readout,
not a derivation of a unique overtone law or a choice of TGL partition/unraveling.
Beta is calculated by the supplied prediction module, never fitted here.

`coherent_imr_likelihood.py` additionally provides an exact two-coefficient
Gaussian marginalization for a supplied nonlinear source. Its prior is stated:
psi is uniform modulo pi and p(D)=403^2/(s^2 D^3) exp[-403^2/(2 s^2 D^2)], with
D in Mpc and s the common-amplitude prior sd. This is a proper input prior, NOT
uniform comoving volume. The intrinsic source still needs integration; no
full-source evidence is claimed by this supplement.

## Reproduce from actual generators

Tested runtime: Python 3.12, PyCBC 2.11.0, LALSimulation 6.2.1, NumPy 2.3.5,
SciPy 1.16.3. No private source, credentials, canonical um.py or event strain is
included. The noise metric was derived from public off-source strain and is
provided as a frozen array; prior public-data packages reproduce that step.

Run `python -B reproduce.py` using a Python that already has PyCBC/LAL/SciPy.
It checks every packaged hash, creates a fresh directory, checks the model and
distance/polarization integral, regenerates the 12 stored physical candidates
at 16384/32768 Hz, and independently verifies their residuals using QR.
It does NOT repeat the costly optimizer searches or claim independent external
review. Results are saved in the new run directory. Failures stay visible.

To repeat the searches themselves, use a separate new copy of the registered
inputs without a pre-existing `C5_NONLINEAR_COHERENT.json` or search checkpoints,
and run `python -B nonlinear_coherent_recovery.py run`. Original candidate seeds,
parameters and evaluation budgets are recorded and hashed. A local optimizer
budget exit is not a scientific acceptance test.

The reported five-sigma power bound is an analytic simple-pair Gaussian bound,
not an empirical tail measurement or a conversion of Bayes factor to sigma.
All hypotheses, onset conventions and limitations accompany the results.
'''
    (package/"README.md").write_bytes(text.encode())
    runner='''"""Fresh-directory generator and candidate replay; never modify packaged results."""
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
(run/"RESULT.json").write_bytes((json.dumps(receipt,indent=2)+"\\n").encode())
print(json.dumps(receipt),flush=True)
'''
    (package/"reproduce.py").write_bytes(runner.encode())
    files=[dict(path=p.relative_to(package).as_posix(),bytes=p.stat().st_size,sha256=sha(p))
           for p in sorted(package.rglob("*")) if p.is_file()]
    (package/"MANIFEST.json").write_bytes((json.dumps(dict(status="FROZEN_PACKAGE",files=files),indent=2)+"\n").encode())
    archive=ROOT/"cache/C7_COHERENT_SOURCE_REPRODUCTION_v1.zip"
    if archive.exists():raise FileExistsError(archive)
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(package.rglob("*")):
            if p.is_file():z.write(p,p.relative_to(package).as_posix())
    receipt=dict(status="PACKAGED_REPLAY_PENDING",package=package.name,archive=archive.relative_to(ROOT).as_posix(),
                 bytes=archive.stat().st_size,sha256=sha(archive),files=len(files),manifest_sha256=sha(package/"MANIFEST.json"))
    target=ROOT/"C7_COHERENT_SOURCE_PACKAGE.json"
    target.write_bytes((json.dumps(receipt,indent=2)+"\n").encode());print(json.dumps(receipt),flush=True)


if __name__=="__main__":main()
