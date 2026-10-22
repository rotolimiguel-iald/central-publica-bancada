"""Repeat the pyRing implementation oracle in a fresh research directory.

Lives in C1_C6_ADDENDUM alongside the original four-package delivery. No target
strain is required. --vendor-cache reuses an already prepared, checked binary;
otherwise the upstream source is built locally with explicit task dependencies.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-archive", type=Path)
    parser.add_argument("--vendor-cache", type=Path)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    if bool(args.source_archive) == bool(args.download):
        parser.error("Choose --source-archive or --download")
    prep = json.loads((root / "PREPARATION.json").read_bytes())
    expected = json.loads((root / "C6_PYRING_IMPLEMENTATION_ORACLE.json").read_bytes())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    run = root / "cache" / ("oracle_" + stamp)
    base = root.parent / "C7_INDEPENDENT/reproduction"
    if not base.is_dir():
        raise ValueError("Place the addendum next to the original C7_INDEPENDENT package")
    shutil.copytree(base, run)
    work = run / "ORDEM_013_RINGDOWN"
    for name in ("prepare_pyring_oracle.py", "verify_pyring_likelihood.py"):
        shutil.copyfile(root / name, work / name)
    archive = work / "cache/source_distributions/pyRingGW-2.7.0.tar.gz"
    archive.parent.mkdir(parents=True, exist_ok=True)
    if args.source_archive:
        if sha(args.source_archive) != prep["source_sha256"]:
            raise ValueError("Supplied source archive differs")
        shutil.copyfile(args.source_archive, archive)
    else:
        partial = archive.with_suffix(".partial")
        with urllib.request.urlopen(prep["source_origin"], timeout=60) as response, partial.open("xb") as stream:
            shutil.copyfileobj(response, stream)
        if sha(partial) != prep["source_sha256"]:
            raise ValueError("Upstream archive differs; partial retained")
        partial.replace(archive)
    manifest = dict(files=[dict(path=archive.relative_to(work).as_posix(),
                               sha256=prep["source_sha256"], origin=prep["source_origin"])])
    mpath = work / "cache/MANIFESTO_DOWNLOADS.json"
    if mpath.exists():
        raise FileExistsError("Unexpected copied download manifest")
    mpath.write_bytes(json.dumps(manifest, indent=2).encode())
    reuse = bool(args.vendor_cache)
    if reuse:
        # Binary identity alone is not enough for the original source; the oracle
        # independently compares installed .pyx bytes with the upstream tarball.
        candidates = list((args.vendor_cache / "pyRing").glob("likelihood*.so"))
        if len(candidates) != 1 or sha(candidates[0]) != expected["compiled_extension_sha256"]:
            raise ValueError("Supplied compiled likelihood differs")
        destination = work / "cache/pyring_oracle"
        destination.mkdir()
        shutil.copytree(args.vendor_cache, destination / "vendor")
        (destination / "mpl_cache").mkdir()
        (destination / "PREPARATION.json").write_bytes((root / "PREPARATION.json").read_bytes())
    else:
        subprocess.run([sys.executable, "-B", str(work / "prepare_pyring_oracle.py")], check=True)
    subprocess.run([sys.executable, "-B", str(work / "verify_pyring_likelihood.py")], check=True)
    actual = json.loads((work / "C6_PYRING_IMPLEMENTATION_ORACLE.json").read_bytes())
    if actual["status"] != "PASS_IMPLEMENTATION_ONLY":
        raise ValueError("Implementation oracle did not pass")
    for field in ("toeplitz_controls", "projected_noise_checks", "marginalized_checks"):
        if actual["stats"][field] != expected["stats"][field]:
            raise ValueError("Oracle coverage changed")
    report = dict(status="PASS", directory=run.relative_to(root).as_posix(),
                  reused_compiled_extension=reuse,
                  source_archive_sha256=sha(archive),
                  scientific_status="IMPLEMENTATION_ONLY__C5_CALIBRATION_NOT_PASSED",
                  numeric_stats=actual["stats"],
                  actual_result_sha256=sha(work / "C6_PYRING_IMPLEMENTATION_ORACLE.json"))
    (run / "RESULT.json").write_bytes((json.dumps(report, indent=2)+"\n").encode())
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
