"""Build the additive F2.3 source and record the actual Lean invocation."""

from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "LiganteLeiCampoCurvoAuditoriaC1.lean"
OUTPUT = HERE / "LiganteLeiCampoCurvoAuditoriaC1.olean"
LOG = HERE / "BUILD_AUDITORIA_C1_20261008.log"
FIRST_ATTEMPT = HERE / "BUILD_FIRST_ATTEMPT.log"
COPY = HERE / "kernel"
ORIGINAL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
LEAN = Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_new(path: Path, payload: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite {path}")
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".f23_c1_build_", suffix=".tmp", delete=False) as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.read_bytes() != payload:
        raise RuntimeError("Temporary build log differs from intended bytes")
    os.rename(temporary, path)


def main() -> None:
    if LOG.exists() or OUTPUT.exists():
        raise RuntimeError("Build evidence output already exists")
    if not SOURCE.is_file() or not FIRST_ATTEMPT.is_file() or not LEAN.is_file():
        raise RuntimeError("Required source, first attempt, or toolchain is absent")
    original_lib = ORIGINAL / ".lake/build/lib/lean"
    package_root = ORIGINAL / ".lake/packages"
    package_libs = sorted(p / ".lake/build/lib/lean" for p in package_root.iterdir() if p.is_dir())
    paths = [original_lib, *[p for p in package_libs if p.is_dir()]]
    if not original_lib.is_dir() or not any("mathlib" in str(p).lower() for p in paths):
        raise RuntimeError("Original kernel or Mathlib cache unavailable")
    lean_path = os.pathsep.join(str(p) for p in paths)
    env = os.environ.copy()
    env["LEAN_PATH"] = lean_path
    version_run = subprocess.run([str(LEAN), "--version"], cwd=COPY, env=env,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 encoding="utf-8", errors="replace", check=True)
    command = [str(LEAN), "-o", str(OUTPUT), str(SOURCE)]
    started_utc = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    run = subprocess.run(command, cwd=COPY, env=env, stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         encoding="utf-8", errors="replace")
    elapsed = time.perf_counter() - start
    header = (
        "F2.3 c1 additive source: actual direct Lean build\n"
        f"started_utc={started_utc}\n"
        f"source={SOURCE}\nsource_bytes={SOURCE.stat().st_size}\nsource_sha256={sha256(SOURCE)}\n"
        f"first_attempt={FIRST_ATTEMPT}\nfirst_attempt_bytes={FIRST_ATTEMPT.stat().st_size}\n"
        f"first_attempt_sha256={sha256(FIRST_ATTEMPT)}\n"
        f"toolchain_executable={LEAN}\ntoolchain_version={version_run.stdout.strip()}\n"
        f"cwd={COPY}\nLEAN_PATH={lean_path}\n"
        f"command={' '.join('"' + arg + '"' if ' ' in arg else arg for arg in command)}\n"
        f"exit_code={run.returncode}\nelapsed_seconds={elapsed:.6f}\n"
        f"olean_exists={OUTPUT.exists()}\n"
        f"olean_bytes={OUTPUT.stat().st_size if OUTPUT.exists() else 0}\n"
        f"olean_sha256={sha256(OUTPUT) if OUTPUT.exists() else 'NONE'}\n"
        "compiler_transcript_begin\n"
    )
    transcript = run.stdout
    if transcript and not transcript.endswith("\n"):
        transcript += "\n"
    create_new(LOG, (header + transcript + "compiler_transcript_end\n").encode("utf-8"))
    print(f"log={LOG}\nlog_sha256={sha256(LOG)}\nexit_code={run.returncode}\n"
          f"elapsed_seconds={elapsed:.6f}\nolean_sha256={sha256(OUTPUT) if OUTPUT.exists() else 'NONE'}")
    if run.returncode != 0:
        raise RuntimeError("Lean build failed; see recorded log")


if __name__ == "__main__":
    main()
