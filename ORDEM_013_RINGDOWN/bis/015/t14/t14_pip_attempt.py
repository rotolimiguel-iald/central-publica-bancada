"""T14-A: isolated pyseobnr install attempt; never changes /opt or system Python."""
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHAT = RING.parent
CACHE = RING / "cache" / "t14_pyseobnr_venv"


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for part in iter(lambda: f.read(1 << 20), b""):
            h.update(part)
    return h.hexdigest()


def write_new(path, value):
    raw = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    with Path(path).open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())


def run_command(args, log, seconds):
    begin = time.monotonic()
    with log.open("xb") as stream:
        proc = subprocess.Popen(args, stdout=stream, stderr=subprocess.STDOUT,
                                start_new_session=True, env=dict(os.environ,
                                PIP_DISABLE_PIP_VERSION_CHECK="1", PYTHONDONTWRITEBYTECODE="1"))
        try:
            rc = proc.wait(timeout=seconds)
            timed_out = False
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
            rc = proc.returncode
            timed_out = True
    return dict(rc=rc, timed_out=timed_out, wall_seconds=time.monotonic()-begin,
                log_sha256=digest(log), log_bytes=log.stat().st_size,
                command=args)


def main():
    stamp = datetime.now(timezone.utc).isoformat()
    pre = HERE / "T14_A_PRE_REG.json"
    write_new(pre, dict(status="PRE_REGISTERED_BEFORE_ATTEMPT", registered_utc=stamp,
                        package="pyseobnr==0.3.7", install="pip in own venv only",
                        venv_relative_to_Chatgpt=str(CACHE.relative_to(CHAT)).replace("\\", "/"),
                        deadline_seconds=7200, branch_A_cap_seconds=1800,
                        source="https://pypi.org/project/pyseobnr/0.3.7/",
                        source_sdist_sha256="a3125f4b7ba680bb0f0c64f6fc644e1ccb663805d78052b40803f30fd6bbb581",
                        prerequisites_observed="swig, gsl-config, conda, micromamba, cmake absent from WSL PATH",
                        scope="installation and API timing only, no scientific gate"))
    result = dict(status="T14_A_ATTEMPT", created_utc=datetime.now(timezone.utc).isoformat(),
                  prereg_sha256=digest(pre), venv=None, pip=None, installed=False)
    CACHE.parent.mkdir(exist_ok=True)
    try:
        result["venv"] = run_command([sys.executable, "-m", "venv", "--system-site-packages", str(CACHE)],
                                     HERE / "T14_A_VENV.log", 120)
        if result["venv"]["rc"] == 0:
            result["pip"] = run_command([str(CACHE / "bin" / "python"), "-m", "pip", "install",
                                         "--no-input", "--no-cache-dir", "pyseobnr==0.3.7"],
                                        HERE / "T14_A_PIP.log", 1800)
            if result["pip"]["rc"] == 0:
                check = run_command([str(CACHE / "bin" / "python"), "-c",
                                     "import pyseobnr; print(pyseobnr.__version__)"],
                                    HERE / "T14_A_IMPORT.log", 30)
                result["import"] = check
                result["installed"] = check["rc"] == 0
    except Exception as exc:
        result["error"] = repr(exc)
    result["finished_utc"] = datetime.now(timezone.utc).isoformat()
    result["gate_changed"] = False
    write_new(HERE / "T14_A_RESULT.json", result)
    print(json.dumps({"status": result["status"], "installed": result["installed"],
                      "venv_rc": None if result["venv"] is None else result["venv"]["rc"],
                      "pip_rc": None if result["pip"] is None else result["pip"]["rc"],
                      "error": result.get("error")}))


if __name__ == "__main__":
    main()
