"""Compile the F1.2 completion only against the current Nos kernel caches."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


SANDBOX = Path(__file__).resolve().parent
MODULES = SANDBOX / "F12Completion"
BUILD = SANDBOX / "build" / "F12Completion"
BUILD.mkdir(parents=True, exist_ok=True)
LEAN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
PKG = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\tgl_kernel\.lake\packages")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")

dependency_paths = [
    PKG / name / ".lake" / "build" / "lib" / "lean"
    for name in (
        "Cli", "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
]
dependency_paths.extend([NOS / ".lake" / "build" / "lib" / "lean", LEAN.parent.parent / "lib" / "lean", BUILD.parent])
missing = [str(path) for path in dependency_paths if not path.is_dir()]
if missing:
    print(json.dumps({"missing_cache_directories": missing}, ensure_ascii=False))
    dependency_paths = [path for path in dependency_paths if path.is_dir()]
if not LEAN.is_file():
    raise FileNotFoundError(LEAN)

env = os.environ.copy()
env["LEAN_PATH"] = os.pathsep.join(str(path) for path in dependency_paths)
results = []
for stem in ("V351DualScalingBridge", "AgapeNonVacuity"):
    source = MODULES / f"{stem}.lean"
    olean = BUILD / f"{stem}.olean"
    log = SANDBOX / f"BUILD_{stem}.log"
    command = [str(LEAN), "-o", str(olean), f"--root={SANDBOX}", str(source)]
    completed = subprocess.run(command, cwd=SANDBOX, env=env, capture_output=True, check=False)
    output = completed.stdout + completed.stderr
    with log.open("xb") as stream:
        stream.write(output)
        stream.flush()
        os.fsync(stream.fileno())
    result = {
        "module": stem,
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "olean": str(olean),
        "olean_sha256": hashlib.sha256(olean.read_bytes()).hexdigest() if olean.exists() else None,
        "log": str(log),
        "log_sha256": hashlib.sha256(output).hexdigest(),
        "exit_code": completed.returncode,
        "command": command,
        "lean_path": env["LEAN_PATH"],
    }
    results.append(result)
    print(json.dumps(result, ensure_ascii=False))
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)

result_path = SANDBOX / "BUILD_COMPLETION_RESULT.json"
result_raw = (json.dumps({"steps": results}, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
if result_path.exists():
    raise FileExistsError(f"Existing evidence must not be replaced: {result_path}")
with tempfile.NamedTemporaryFile(
    dir=result_path.parent, prefix=result_path.name + ".", suffix=".tmp", delete=False
) as stream:
    stream.write(result_raw)
    stream.flush()
    os.fsync(stream.fileno())
    temp = Path(stream.name)
try:
    if temp.stat().st_size != len(result_raw):
        raise OSError(f"Temporary result truncated: {temp}")
    os.link(temp, result_path)
finally:
    temp.unlink(missing_ok=True)
if result_path.read_bytes() != result_raw:
    raise OSError(f"Result byte mismatch: {result_path}")
