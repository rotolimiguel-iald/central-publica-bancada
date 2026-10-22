"""Audit C1 and add the upstream implementation oracle to the immutable bundle."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def new(path, raw):
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(raw)
    if temp.stat().st_size != len(raw):
        raise ValueError("Incomplete write")
    temp.replace(path)


def main():
    receipt = ROOT / "C7_C1_C6_ADDENDUM_VALIDATION.json"
    if receipt.exists():
        raise FileExistsError("Preserve additive release")
    contract = json.loads((ROOT / "C1_LEITURAS.json").read_bytes())
    numbers = json.loads((ROOT / "C1_TABLES.json").read_bytes())
    expected = {(r["event"], r["prediction"]["reading"]):r["prediction"] for r in numbers["rows"]}
    refs = [*contract["source_references"].values(), contract["numerical_source"], contract["clock_evidence"]]
    for ref in refs:
        path = ROOT / ref["path"]
        if sha(path) != ref["sha256"]:
            raise ValueError("C1 reference changed: " + ref["path"])
        if "lines" in ref:
            lines = path.read_text(encoding="utf-8").splitlines()
            if not all(ref["matching_text"] in lines[i-1] for i in ref["lines"]):
                raise ValueError("C1 source anchor differs")
    counted = 0
    if contract["hypothesis_selected"] or len(contract["rows"]) != 10:
        raise ValueError("C1 scope changed")
    for row in contract["rows"]:
        reading = row["reading"]
        if row["physical_selection"] is not None or row["relation_to_operator_16Sep"] is not None:
            raise ValueError("Unpermitted interpretation was selected")
        if row["units"]["seconds_power"] != (0 if reading == "R-PROP" else -1):
            raise ValueError("Wrong units")
        for measurement in row["measurements"]:
            p = expected[measurement["event"], reading]
            for key in ("gamma_per_s", "gamma_over_omega"):
                if measurement[key] != p[key]:
                    raise ValueError("Numerical C1 contract differs")
            if reading == "R-RAIZ-COHERENT":
                if measurement["x"] is not None or measurement["delta_tau"] is not None:
                    raise ValueError("Coherent mixture replaced by exponential")
            elif measurement["x"] != p["x"] or measurement["delta_tau"] != p["delta_tau_ensemble_exact"]:
                raise ValueError("Ringdown conversion differs")
            counted += 1
    if counted != 18:
        raise ValueError("Missing numerical rows")
    oracle = json.loads((ROOT / "C6_PYRING_IMPLEMENTATION_ORACLE.json").read_bytes())
    if oracle["status"] != "PASS_IMPLEMENTATION_ONLY":
        raise ValueError("Upstream oracle not passed")
    if oracle["registration_sha256"] != sha(ROOT / "REGISTRO_C6.json"):
        raise ValueError("Frozen registration changed")
    evidence_names = ["C1_LEITURAS.json", "C1_LEITURAS.md", "complete_c1_contract.py",
                      "C6_PYRING_IMPLEMENTATION_ORACLE.json", "prepare_pyring_oracle.py",
                      "verify_pyring_likelihood.py", "package_reproduce_pyring_oracle.py",
                      "cache/pyring_oracle/PREPARATION.json"]
    evidence = {n:dict(sha256=sha(ROOT/n), bytes=(ROOT/n).stat().st_size) for n in evidence_names}
    audit = dict(status="CONDITIONAL_RESEARCH_PROGRESS", created_utc=datetime.now(timezone.utc).isoformat(),
                 C1=dict(status="CONTRACT_VERIFIED", readings=10, numerical_rows=counted,
                         source_anchors=len(contract["source_references"]), units_checked=10,
                         physical_hypothesis_selected=False),
                 C6=dict(implementation="VERIFIED_AGAINST_UNMODIFIED_PYRING_2_7_0", stats=oracle["stats"],
                         identical_published_posterior_reproduction=False,
                         interpretation="INCONCLUSIVE_SYSTEMATICS"),
                 unresolved_acceptance=["C5 two-family calibration still fails; no original scientific gate changed",
                                        "C6 published posterior comparison is not the same model, priors, or preprocessing",
                                        "No released pyRing 10.5 tM product in the inspected archive",
                                        "Physical partition/clock/readout not selected, as ordered",
                                        "Full primary Kay-Wald/Milburn texts not inspected; abstract-only scope persists"],
                 goal_completion_claimed=False, evidence=evidence)
    new(ROOT / "C7_C1_C6_ADDENDUM.json", (json.dumps(audit, indent=2)+"\n").encode())
    stats = oracle["stats"]
    md = f'''[REAL — numerical implementation verification; physical readings remain conditional]

# C1/C6 addendum to the ringdown research delivery

The ten-reading C1 contract is complete and checked against the frozen source
anchors and all 18 saved two-event numerical rows. It distinguishes the supplied
clock, operator, physical bridge, FP-5 scope, distance dependence and atomic
universality condition. Null universal flags are unresolved, not “not excluded”.
The coherent-state initial slope is not an exponential damping rate; propagation
Xi is not a local ringdown shift. No reading was selected.

## Executed upstream implementation comparison

The original pyRing 2.7.0 source distribution was compiled locally, with no source
edits, no system-environment installation and no changes to the frozen C6 code.
Its installed likelihood.pyx was checked byte for byte against the public archive.
The actual compiled loglikelihood and three inverse-covariance functions ran on:

- {stats['toeplitz_controls']} synthetic Toeplitz cases, with independent determinant checks;
- {stats['projected_noise_checks']} held-out off-source noise vectors under the existing quotient covariance;
- {stats['marginalized_checks']} amplitude integrals for the registered five readings, three mass/spin
  points, three amplitude priors, two detectors and three off-source vectors.

Maximum relative inner-product difference: {stats['max_inner_relative_error']:.12g}.
Maximum projected log-density difference: {stats['max_projected_log_density_error']:.12g}.
Maximum log-evidence difference: {stats['max_marginal_lnZ_error']:.12g}.
An intentionally omitted determinant differs by {stats['missing_determinant_control_difference']:.12g}
and is rejected. The independent amplitude oracle convolves a 407-dimensional
data covariance, whereas production solves a 4-dimensional coefficient system.

## What this result does and does not establish

This pays the numerical **implementation** comparison. It does not reproduce the
published posterior under identical priors, modes or preprocessing. Published
pyRing 220/221 posteriors and this 220/440 model remain distinct; the inspected
release has no 10.5 tM posterior. No new on-source strain was read in this test.

The earlier two-family injection calibration still fails its declared bias and
coverage criteria. Its calculations are completed; the required scientific
acceptance is **NOT PASSED**. Agreement between numerical implementations cannot
repair an inadequate waveform model. No frozen measurement, Bayes ratio,
selection, gate, or physical partition was changed. There is no sigma claim.

## Reproduce

From the extracted delivery root, run `python verify_delivery.py`. In
`C1_C6_ADDENDUM`, with the scientific Python environment described by the base
package, execute:

```sh
python -B reproduce.py --download
```

Alternatively supply `--source-archive /path/to/pyRingGW-2.7.0.tar.gz`.
The source is hash-checked. The runner copies frozen inputs to a fresh directory,
builds pyRing and its task-only dependencies there, then runs the oracle without
target strain. An optional `--vendor-cache /path/to/prepared/vendor` reuses the
checked binary; that is explicitly recorded and is not called an independent
compiler run. No original inference sampler is rerun.

The package retains the earlier v1 artifacts and their full scope statements.
This addendum advances C1 documentation and C6 implementation verification; it
does not declare the full research objective or precision requirement complete.
'''
    new(ROOT / "C7_C1_C6_ADDENDUM.md", md.encode())
    old_receipt = json.loads((ROOT / "C7_DELIVERY_BUNDLE_VALIDATION.json").read_bytes())
    old_zip = ROOT / old_receipt["archive"]
    if sha(old_zip) != old_receipt["sha256"]:
        raise ValueError("Original delivery changed")
    contents = {}
    with zipfile.ZipFile(old_zip) as old:
        if old.testzip() is not None:
            raise ValueError("Original archive CRC failed")
        for name in old.namelist():
            rel = PurePosixPath(name)
            if rel.parts[0] != "TGL_RINGDOWN_DELIVERY" or ".." in rel.parts:
                raise ValueError("Invalid old archive path")
            contents[PurePosixPath(*rel.parts[1:]).as_posix()] = old.read(name)
    old_manifest = json.loads(contents["MANIFEST.json"])
    for row in old_manifest["files"]:
        raw = contents[row["path"]]
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError("Old manifest verification failed")
    contents["MANIFEST_v1.json"] = contents.pop("MANIFEST.json")
    contents["README_v1.md"] = contents["README.md"]
    contents["README.md"] = ("# Updated research delivery\n\nRead [the C1/C6 addendum](C1_C6_ADDENDUM/README.md) "
                           "for the latest scope, then [the full v1 overview](README_v1.md). "
                           "Scientific two-family calibration remains NOT PASSED.\n\n"
                           "Run `python verify_delivery.py` to verify shipped files.\n").encode()
    additions = {"README.md":"C7_C1_C6_ADDENDUM.md", "AUDIT.json":"C7_C1_C6_ADDENDUM.json",
                 "reproduce.py":"package_reproduce_pyring_oracle.py", "PREPARATION.json":"cache/pyring_oracle/PREPARATION.json"}
    additions.update({n:n for n in evidence_names if "/" not in n and n != "package_reproduce_pyring_oracle.py"})
    for name, source in additions.items():
        contents["C1_C6_ADDENDUM/"+name] = (ROOT/source).read_bytes()
    manifest = dict(status="CONDITIONAL_RESEARCH_DELIVERY_V2", source_v1_sha256=sha(old_zip),
                    scientific_calibration="NOT_PASSED", physical_confirmation_claimed=False,
                    files=[dict(path=n, bytes=len(v), sha256=hashlib.sha256(v).hexdigest())
                           for n,v in sorted(contents.items())])
    contents["MANIFEST.json"] = (json.dumps(manifest, indent=2)+"\n").encode()
    archive = ROOT / "cache/TGL_RINGDOWN_DELIVERY_v2.zip"
    if archive.exists():
        raise FileExistsError(archive)
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for name, raw in sorted(contents.items()):
            handle.writestr("TGL_RINGDOWN_DELIVERY/"+name, raw)
    fresh = ROOT / "cache" / ("delivery_v2_fresh_"+datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    fresh.mkdir()
    with zipfile.ZipFile(archive) as handle:
        if handle.testzip() is not None:
            raise ValueError("V2 archive CRC failed")
        for name, expected_bytes in contents.items():
            raw = handle.read("TGL_RINGDOWN_DELIVERY/"+name)
            if raw != expected_bytes:
                raise ValueError("Repacking changed bytes")
            path = fresh/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    process = subprocess.run([sys.executable, "-B", str(fresh/"verify_delivery.py")],
                             capture_output=True, text=True, check=True)
    validation = dict(status="PASS", archive=archive.relative_to(ROOT).as_posix(), bytes=archive.stat().st_size,
                      sha256=sha(archive), source_v1_sha256=sha(old_zip), fresh_directory=fresh.relative_to(ROOT).as_posix(),
                      verifier=json.loads(process.stdout), C1=audit["C1"], upstream_oracle=stats,
                      independent_directory_oracle_replay="PENDING", scientific_acceptance="NOT_PASSED",
                      generator_sha256=sha(Path(__file__)))
    new(receipt, (json.dumps(validation, indent=2)+"\n").encode())
    print(json.dumps(validation), flush=True)


if __name__ == "__main__":
    main()
