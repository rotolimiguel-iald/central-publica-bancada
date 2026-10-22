"""Build the branch C docstring-only F2.3 source without overwriting evidence."""

from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
KERNEL = HERE / "kernel"
SOURCE = HERE / "LiganteLeiCampoCurvoRamoCAuditoriaC1.lean"
SANDBOX_SOURCE = KERNEL / "TGLExt/LiganteLeiCampoCurvoRamoCAuditoriaC1.lean"
OUTPUT = HERE / "LiganteLeiCampoCurvoRamoCAuditoriaC1.olean"
LOG = HERE / "BUILD_RAMOC_AUDITORIAC1_V4_20261008.log"
ORIGINAL_KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
LEAN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
ATTEMPTS = [
    ("first_audited_stone_error", HERE / "BUILD_FIRST_ATTEMPT.log"),
    ("branch_c_error_and_sorryAx", HERE / "BUILD_RAMOC.log"),
    ("branch_c_warnings_only", HERE / "BUILD_RAMOC_2.log"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path: Path, payload: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite {path}")
    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=".f23_build_receipt_", suffix=".tmp", delete=False
    ) as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.read_bytes() != payload:
        raise RuntimeError("Temporary receipt differs from intended bytes")
    os.rename(temporary, path)
    if path.read_bytes() != payload:
        raise RuntimeError("Written receipt differs from intended bytes")


def main() -> None:
    if OUTPUT.exists() or LOG.exists():
        raise RuntimeError("A build output for this act already exists")
    required = [SOURCE, SANDBOX_SOURCE, LEAN, *[path for _, path in ATTEMPTS]]
    if not all(path.is_file() for path in required):
        raise RuntimeError("Required audited source, toolchain, or historical log is absent")
    if SOURCE.read_bytes() != SANDBOX_SOURCE.read_bytes():
        raise RuntimeError("Audited source differs from its sandbox copy")
    original_lib = ORIGINAL_KERNEL / ".lake/build/lib/lean"
    package_root = ORIGINAL_KERNEL / ".lake/packages"
    package_libs = sorted(
        path / ".lake/build/lib/lean" for path in package_root.iterdir() if path.is_dir()
    )
    paths = [original_lib, *[path for path in package_libs if path.is_dir()]]
    if not original_lib.is_dir() or not any("mathlib" in str(path).lower() for path in paths):
        raise RuntimeError("Original kernel or Mathlib cache unavailable")
    lean_path = os.pathsep.join(str(path) for path in paths)
    env = os.environ.copy()
    env["LEAN_PATH"] = lean_path
    version = subprocess.run(
        [str(LEAN), "--version"], cwd=KERNEL, env=env,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        encoding="utf-8", errors="replace", check=True,
    ).stdout.strip()
    command = [str(LEAN), "-o", str(OUTPUT), "TGLExt/LiganteLeiCampoCurvoRamoCAuditoriaC1.lean"]
    started = datetime.now(timezone.utc)
    clock = time.perf_counter()
    run = subprocess.run(
        command, cwd=KERNEL, env=env, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        encoding="utf-8", errors="replace",
    )
    elapsed = time.perf_counter() - clock
    ended = datetime.now(timezone.utc)
    lines = [
        "F2.3 branch C c1 docstring-only source: direct Lean build, fresh act",
        f"started_utc={started.isoformat()}",
        f"ended_utc={ended.isoformat()}",
        f"elapsed_seconds={elapsed:.6f}",
        f"source={SOURCE}",
        f"source_bytes={SOURCE.stat().st_size}",
        f"source_sha256={digest(SOURCE)}",
        f"sandbox_source={SANDBOX_SOURCE}",
        f"sandbox_source_sha256={digest(SANDBOX_SOURCE)}",
        f"toolchain_executable={LEAN}",
        f"toolchain_version={version}",
        f"cwd={KERNEL}",
        f"LEAN_PATH={lean_path}",
        f"command={subprocess.list2cmdline(command)}",
        f"exit_code={run.returncode}",
        f"olean_exists={OUTPUT.exists()}",
        f"olean_bytes={OUTPUT.stat().st_size if OUTPUT.exists() else 0}",
        f"olean_sha256={digest(OUTPUT) if OUTPUT.exists() else 'NONE'}",
    ]
    for label, path in ATTEMPTS:
        lines.extend(
            [f"historical_attempt_{label}={path}",
             f"historical_attempt_{label}_bytes={path.stat().st_size}",
             f"historical_attempt_{label}_sha256={digest(path)}"]
        )
    lines.append("compiler_transcript_begin")
    transcript = run.stdout.rstrip("\n")
    receipt = "\n".join(lines) + "\n" + transcript + "\ncompiler_transcript_end\n"
    write_new(LOG, receipt.encode("utf-8"))
    print(f"log={LOG}\nlog_sha256={digest(LOG)}\nexit_code={run.returncode}")
    if run.returncode != 0:
        raise RuntimeError("Lean build failed; the new log records the failure")


if __name__ == "__main__":
    main()
