"""Compile fresh sandbox evidence; preserve every previous attempt byte for byte."""
from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

BASE = Path(__file__).resolve().parent
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
LEAN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
SOURCE = BASE / "GeometricFiberConjugation.lean"


def save_new(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if path.read_bytes() != data:
        raise OSError(f"Byte verification failed: {path}")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = [BASE / "attempts/20261013T213953_584159Z", KERNEL / ".lake/build/lib/lean"]
    paths += sorted((KERNEL / ".lake/packages").glob("*/.lake/build/lib/lean"))
    paths += [LEAN.parent.parent / "lib/lean"]
    if not LEAN.is_file() or not all(p.is_dir() for p in paths):
        raise FileNotFoundError("Missing compiler or read-only dependency cache")
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    out = BASE / "attempts" / stamp
    out.mkdir(parents=True, exist_ok=False)
    save_new(out / SOURCE.name, SOURCE.read_bytes())
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
    command = [str(LEAN), "-o", str(out / "GeometricFiberConjugation.olean"), str(SOURCE)]
    version = subprocess.check_output([str(LEAN), "--version"], text=True).strip()
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t0 = time.perf_counter()
    result = subprocess.run(command, cwd=BASE, env=env, capture_output=True, check=False)
    seconds = time.perf_counter() - t0
    end = datetime.datetime.now(datetime.timezone.utc).isoformat()
    raw = result.stdout + result.stderr
    metadata = {
        "start_utc": start, "end_utc": end, "seconds": seconds,
        "command": command, "cwd": str(BASE), "toolchain": version,
        "LEAN_PATH": env["LEAN_PATH"], "exit_code": result.returncode,
        "source_sha256": sha(SOURCE), "source_bytes": SOURCE.stat().st_size,
        "attempt": str(out), "read_only_dependency_paths": list(map(str, paths)),
        "no_kernel_writes": True, "no_junction_created": True,
    }
    log = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n\nSTDOUT+STDERR\n").encode() + raw
    save_new(out / "BUILD.log", log)
    save_new(out / "AXIOMS.txt", raw)
    metadata["artifacts"] = [
        {"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)}
        for p in sorted(out.iterdir()) if p.is_file()
    ]
    save_new(out / "RECEIPT.json", (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"attempt": str(out), "exit_code": result.returncode,
                      "seconds": seconds, "receipt_sha256": sha(out / "RECEIPT.json")}, ensure_ascii=False))
    print(raw.decode("utf-8", "replace"))
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
