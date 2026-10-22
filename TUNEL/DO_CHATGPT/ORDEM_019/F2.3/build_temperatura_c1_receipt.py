"""Compile the existing F2.3 Temperature sandbox stone and save an immutable receipt."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
KERNEL = ROOT / "kernel"
SOURCE = KERNEL / "TGLExt" / "LiganteLeiCampoCurvoTemperaturaSemBoostOcioso.lean"
ORIGINAL = ROOT / "LiganteLeiCampoCurvoTemperaturaSemBoostOcioso.lean"
REFERENCE_LOG = ROOT / "BUILD_AUDITORIA_C1_FINAL_20261008.log"
OUTPUT = ROOT / "LiganteLeiCampoCurvoTemperaturaSemBoostOcioso_C1_20261008.olean"
RECEIPT = ROOT / "BUILD_TEMPERATURA_C1_ACT_20261008.json"
TRANSCRIPT = ROOT / "BUILD_TEMPERATURA_C1_ACT_20261008.log"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exclusive_bytes(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


if __name__ == "__main__":
    for path in (OUTPUT, RECEIPT, TRANSCRIPT):
        if path.exists():
            raise FileExistsError(path)
    if SOURCE.read_bytes() != ORIGINAL.read_bytes():
        raise RuntimeError("Sandbox source differs from the delivered stone")

    recorded = REFERENCE_LOG.read_text(encoding="utf-8")
    fields = dict(line.split("=", 1) for line in recorded.splitlines() if "=" in line)
    lean_path = fields["LEAN_PATH"]
    executable = Path(fields["toolchain_executable"])
    if not executable.is_file():
        raise FileNotFoundError(executable)
    env = os.environ.copy()
    env["LEAN_PATH"] = lean_path
    command = [str(executable), "-o", str(OUTPUT), "TGLExt/LiganteLeiCampoCurvoTemperaturaSemBoostOcioso.lean"]

    started = datetime.now(timezone.utc)
    tic = time.perf_counter()
    completed = subprocess.run(command, cwd=KERNEL, env=env, text=True, capture_output=True)
    elapsed = time.perf_counter() - tic
    finished = datetime.now(timezone.utc)
    transcript = completed.stdout + completed.stderr
    exclusive_bytes(TRANSCRIPT, transcript.encode("utf-8"))
    receipt = {
        "unit": "F2.3",
        "purpose": "Fresh build receipt for the additive Temperature candidate without unused observer_boost fields; no kernel installation",
        "started_utc": started.isoformat(),
        "finished_utc": finished.isoformat(),
        "elapsed_seconds": elapsed,
        "cwd": str(KERNEL),
        "toolchain_executable": str(executable),
        "command": command,
        "LEAN_PATH_literal": lean_path,
        "exit_code": completed.returncode,
        "source_sha256": sha256(SOURCE),
        "source_bytes": SOURCE.stat().st_size,
        "transcript_sha256": sha256(TRANSCRIPT),
        "transcript_bytes": TRANSCRIPT.stat().st_size,
        "olean_sha256": sha256(OUTPUT) if OUTPUT.is_file() else None,
        "olean_bytes": OUTPUT.stat().st_size if OUTPUT.is_file() else None,
    }
    exclusive_bytes(RECEIPT, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({k: receipt[k] for k in ("started_utc", "finished_utc", "elapsed_seconds", "exit_code", "olean_sha256", "transcript_sha256")}, ensure_ascii=False))
    if completed.returncode:
        raise SystemExit(completed.returncode)
