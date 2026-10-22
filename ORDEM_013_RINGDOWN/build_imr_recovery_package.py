"""Ship a reproducible, explicitly restricted full-IMR-shape calibration study."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parent


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def new(path,raw):
    if path.exists():raise FileExistsError(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+".tmp");tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError("Incomplete write")
    tmp.replace(path)


def main():
    package=ROOT/"C7_IMR_RECOVERY_REPRODUCTION"
    if package.exists():raise FileExistsError(package)
    reg=json.loads((ROOT/"REGISTRO_C5_IMR_RECOVERY.json").read_bytes())
    measured=json.loads((ROOT/"C5_IMR_RECOVERY.json").read_bytes())
    validation=json.loads((ROOT/"C5_IMR_RECOVERY_VALIDATION.json").read_bytes())
    if validation["status"]!="PASS" or measured["registration_sha256"]!=sha(ROOT/"REGISTRO_C5_IMR_RECOVERY.json"):
        raise ValueError("Scientific numerical checks failed")
    for name,wanted in reg["hashes"].items():
        if sha(ROOT/name)!=wanted:raise ValueError("Registered input differs")
    names=list(reg["hashes"])+["REGISTRO_C5_IMR_RECOVERY.json","verify_imr_recovery.py","fetch_public.py"]
    for name in names:new(package/"assets"/name,(ROOT/name).read_bytes())
    for name in ["C5_IMR_RECOVERY.json","C5_IMR_RECOVERY_VALIDATION.json"]:
        new(package/"evidence"/name,(ROOT/name).read_bytes())
    for item in measured["draws"]:
        if sha(ROOT/item["path"])!=item["sha256"]:raise ValueError("Measured draws changed")
        new(package/"evidence"/item["path"],(ROOT/item["path"]).read_bytes())
    new(package/"reproduce.py",(ROOT/"package_reproduce_imr_recovery.py").read_bytes())
    groups=[r for r in measured["joint_mixture_criteria"] if r["reading"] in ("R-B","R-RAIZ-0","R-LIN","R-MOD")]
    table="\n".join(f"| {r['psd']} | {r['reading']} | {r['SNR']:g} | {'PASS' if r['pass_all_four'] else 'FAIL'} |" for r in groups)
    readme=f'''# Conditional IMR recovery extension

This is a **non-blind model-adequacy study**, not a new analysis of observed
GW250114 strain or a physical confirmation. It extends the previous QNM-basis
recovery using full, precomputed IMR harmonic shapes at the same fixed binary
parameters. Both model families, all eight scalar-rate readings and the original
bias/coverage criteria are retained.

## Measured outcome

576 cells, 206 paired held-out noise intervals per cell, O4 and O5 reference
PSDs, injected dephasing amplitudes 0 and 1, and ringdown network SNRs 40, 200,
600. The noise indices 50:256 were not used in the earlier 50-draw forecast;
the same intervals are reused across configurations, not independent events.

For the four identifiable readings, **19 of 24** PSD/reading/SNR groups pass
jointly for both injected amplitudes and both injection families using one
equal-family-mixture likelihood. There are 78 passing individual mixture cells,
76 passing same-family cells and **zero passing opposite-family cells**.
Half of the total cells are below observable precision and claim no calibration.

| PSD | Reading | Ringdown SNR | All four mixture cells |
|---|---|---:|---|
{table}

## Scope that must accompany these results

The mixture includes the true injection family. Passing within this closed,
two-model set is not evidence that every astrophysical waveform is covered.
Masses, spins, inclination and source phase are fixed to one representative
source. The opposite-family-only failures remain visible. No mass/spin posterior
marginalization or broad source-population validation has been performed here.

Reading B still fails the registered calibration at SNR 40. Its success at SNR
200 or 600 cannot change the frozen C6 verdict at the observed sensitivity.
Positive mean log Bayes ratios also occur for a=0 at low SNR because of the
specified nuisance priors; do not convert them to sigma or claim a detection.

All 22/44 harmonic content receives its fundamental-mode Gamma, and other modes
are unchanged. That deformation, the source mass clock in B, and the ensemble
interpretation remain conditional. Negative amplitudes exist only on a profile
diagnostic grid; the physical point hypotheses are 0 and 1.

## Reproduce

Use Python with NumPy and SciPy. The tested environment is Python 3.12, NumPy
2.5.3 and SciPy 1.18.1. Run:

```sh
python -B reproduce.py
```

The runner verifies every shipped file, creates a fresh directory, recalculates
all 576 cells, and compares identities, statutes and numerical fields plus every
saved draw. It also executes an independent SVD likelihood oracle (96 cells,
288 draw comparisons; measured maximum error {validation['max_lnB_abs_difference']:.12g}).

This package starts from hash-checked **derived** harmonic arrays and recolored
off-source noise. The earlier `C7_INJECTION_REPRODUCTION` package provides their
production from public raw strain and the actual PyCBC/LAL waveform generators.
The original v1/v2 delivery remains unchanged. No canonical um.py, Lean source,
global memory, real-event result or scientific gate is edited by this study.
'''
    new(package/"README.md",readme.encode())
    files=[dict(path=p.relative_to(package).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(package.rglob("*")) if p.is_file()]
    manifest=dict(status="CONDITIONAL_FIXED_SOURCE_TWO_FAMILY_STUDY",files=files,
                  registration_sha256=sha(ROOT/"REGISTRO_C5_IMR_RECOVERY.json"),
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  observations_reanalyzed=False,physical_confirmation_claimed=False)
    new(package/"MANIFEST.json",(json.dumps(manifest,indent=2)+"\n").encode())
    archive=ROOT/"cache/C7_IMR_RECOVERY_REPRODUCTION_v1.zip"
    if archive.exists():raise FileExistsError(archive)
    with zipfile.ZipFile(archive,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as handle:
        for p in sorted(package.rglob("*")):
            if p.is_file():handle.write(p,"C7_IMR_RECOVERY_REPRODUCTION/"+p.relative_to(package).as_posix())
    with zipfile.ZipFile(archive) as handle:
        if handle.testzip() is not None:raise ValueError("Archive CRC failed")
        for row in files:
            data=handle.read("C7_IMR_RECOVERY_REPRODUCTION/"+row["path"])
            if hashlib.sha256(data).hexdigest()!=row["sha256"]:raise ValueError("Archive differs")
    receipt=dict(status="PACKAGED_NUMERICAL_REPLAY_PENDING",archive=archive.relative_to(ROOT).as_posix(),
                 sha256=sha(archive),bytes=archive.stat().st_size,files=len(files),manifest_sha256=sha(package/"MANIFEST.json"),
                 package=package.name,scope="Source-fixed two-family adequacy; no full scientific acceptance claimed")
    new(ROOT/"C7_IMR_RECOVERY_PACKAGE.json",(json.dumps(receipt,indent=2)+"\n").encode())
    print(json.dumps(receipt),flush=True)


if __name__=="__main__":main()
