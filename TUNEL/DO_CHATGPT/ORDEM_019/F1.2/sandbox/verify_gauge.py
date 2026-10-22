"""Reproduce the algebraic inner-action gauge proof in the isolated kernel copy."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "MatrixInnerGauge.lean"
KERNEL_COPY = Path(r"C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k")
LAKE = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe")
LOG = HERE / "COMPILE_LOG_MEASURED.txt"
RESULT = HERE / "COMPILE_RESULT.json"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path: Path, data: bytes) -> None:
    if path.exists():
        old = path.read_bytes()
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup = path.with_name(path.name + ".bak_" + stamp)
        with backup.open("xb") as handle:
            handle.write(old)
        if backup.read_bytes() != old:
            raise RuntimeError("backup mismatch")
    temp = path.with_name(path.name + ".tmp_" + str(os.getpid()))
    with temp.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.stat().st_size != len(data):
        raise RuntimeError("temporary size mismatch")
    os.replace(temp, path)
    if path.read_bytes() != data:
        raise RuntimeError("replacement mismatch")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    forbidden = re.findall(r"\b(?:sorry|admit|axiom)\b", source_text)
    packages = sorted((KERNEL_COPY / ".lake" / "packages").iterdir())
    env = os.environ.copy()
    env["GIT_CONFIG_COUNT"] = str(len(packages))
    for index, package in enumerate(packages):
        env[f"GIT_CONFIG_KEY_{index}"] = "safe.directory"
        env[f"GIT_CONFIG_VALUE_{index}"] = package.as_posix()
    command = [str(LAKE), "env", "lean", str(SOURCE)]
    process = subprocess.run(command, cwd=KERNEL_COPY, env=env, capture_output=True, text=True, timeout=600)
    output = process.stdout + process.stderr
    atomic(LOG, output.encode("utf-8"))
    axioms = {}
    for name, values in re.findall(r"'ORDEM019\.F12\.(\w+)' depends on axioms: \[([^]]*)\]", output):
        axioms[name] = [part.strip() for part in values.split(",")]
    expected = {"gauge_matrixRep_ungauge", "gauge_shift_ungauge"}
    valid = process.returncode == 0 and not forbidden and set(axioms) == expected and all(set(values) <= ALLOWED for values in axioms.values())
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "sandbox_kernel_copy": str(KERNEL_COPY),
        "returncode": process.returncode,
        "source_sha256": digest(SOURCE),
        "log_sha256": digest(LOG),
        "forbidden_tokens": forbidden,
        "axioms": axioms,
        "valid": valid,
        "scope": "algebraic_gauge_only_not_continuous_crossed_product_trace",
    }
    atomic(RESULT, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"valid": valid, "returncode": process.returncode, "result_sha256": digest(RESULT)}))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
