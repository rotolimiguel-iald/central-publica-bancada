"""Install the pinned public pyRing in a task-only target, without /opt edits.

This prepares a numerical implementation comparison, not a repeat of the LVK
posterior.  Dependencies and generated binaries stay below the task cache.
"""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache" / "pyring_oracle"
TARGET = CACHE / "vendor"
SOURCE = ROOT / "cache/source_distributions/pyRingGW-2.7.0.tar.gz"


def main():
    manifest = json.loads((ROOT / "cache/MANIFESTO_DOWNLOADS.json").read_bytes())
    entries = manifest if isinstance(manifest, list) else manifest.get("files", [])
    matching = [r for r in entries if str(r.get("path", "")).replace("\\", "/")
                == SOURCE.relative_to(ROOT).as_posix()]
    if len(matching) != 1:
        raise ValueError("Ambiguous source distribution in the custody manifest")
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if matching[0]["sha256"] != digest:
        raise ValueError("pyRing source custody mismatch")
    CACHE.mkdir(exist_ok=True)
    for name in ("tmp", "pip_cache", "mpl_cache"):
        (CACHE / name).mkdir(exist_ok=True)
    if TARGET.exists():
        raise FileExistsError("Preserve existing oracle target; do not reinstall blindly")
    env = os.environ.copy()
    env.update(PYTHONPATH=str(TARGET), TMPDIR=str(CACHE / "tmp"),
               PIP_CACHE_DIR=str(CACHE / "pip_cache"),
               MPLCONFIGDIR=str(CACHE / "mpl_cache"), PYTHONDONTWRITEBYTECODE="1",
               OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    commands = [
        [sys.executable, "-B", "-m", "pip", "install", "--disable-pip-version-check",
         "--no-deps", "--target", str(TARGET), "Cython==3.0.12",
         "setuptools==80.9.0", "wheel==0.45.1", "seaborn==0.13.2"],
        [sys.executable, "-B", "-m", "pip", "install", "--disable-pip-version-check",
         "--no-deps", "--no-build-isolation", "--target", str(TARGET), str(SOURCE)],
        [sys.executable, "-B", "-c",
         "import pyRing,pyRing.likelihood as l; "
         "print('PYRING_LOADED',pyRing.__version__,l.__file__)"]
    ]
    steps = []
    for index, command in enumerate(commands):
        log = CACHE / f"step_{index}.txt"
        if log.exists():
            raise FileExistsError(log)
        print(f"step={index} running", flush=True)
        with log.open("xb") as stream:
            result = subprocess.run(command, env=env, cwd=CACHE, stdout=stream,
                                    stderr=subprocess.STDOUT)
        steps.append(dict(command=command, exit_code=result.returncode,
                          log=log.relative_to(ROOT).as_posix(),
                          sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
        print(f"step={index} exit={result.returncode}", flush=True)
        if result.returncode:
            break
    status = "PYRING_IMPORTED" if len(steps) == 3 and steps[-1]["exit_code"] == 0 else "PREPARATION_FAILED"
    receipt = dict(status=status, source_sha256=digest, source_origin=matching[0]["origin"],
                   target=TARGET.relative_to(ROOT).as_posix(), steps=steps,
                   system_environment_modified=False,
                   scope="Upstream functions available for a likelihood oracle; no LVK posterior reproduction claimed")
    out = CACHE / "PREPARATION.json"
    temp = out.with_suffix(".json.tmp")
    temp.write_bytes((json.dumps(receipt, indent=2) + "\n").encode())
    temp.replace(out)
    print(status, flush=True)
    if status != "PYRING_IMPORTED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
