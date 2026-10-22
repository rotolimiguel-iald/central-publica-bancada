"""One initialization-only child; external deadline and durable terminal receipt."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent


def pin(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def fresh(path, value):
    data = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    if path.exists():
        raise FileExistsError(path)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(data)
    if temporary.read_bytes() != data:
        raise OSError("Incomplete receipt")
    os.replace(temporary, path)


def main():
    started = time.monotonic()
    protocol_path = ROOT / "SUPERVISION_PROTOCOL.json"
    if len(sys.argv) != 2 or pin(protocol_path)["sha256"] != sys.argv[1]:
        raise ValueError("Exact supervision protocol hash required")
    protocol = json.loads(protocol_path.read_bytes())
    for name, expected in protocol["inputs"].items():
        if pin(ROOT / name) != expected:
            raise ValueError("Input pin mismatch: " + name)
    decision_path = ROOT / "DECISAO_CONTROLE_INIT.json"
    decision = json.loads(decision_path.read_bytes())
    if (decision.get("authorized") is not True
        or decision.get("action") != "QUALIFY_INITIALIZATION_ONLY"
        or decision.get("contract_sha256") != protocol["control_contract_sha256"]
        or decision.get("supervision_protocol_sha256") != sys.argv[1]
        or decision.get("supervised_only") is not True):
        raise ValueError("Specific supervised initialization decision required")
    if str(Path(sys.executable).absolute()) != "/opt/lal_env/bin/python":
        raise ValueError("Fixed WSL interpreter required")
    if (ROOT / "CONTROL_INIT_001").exists():
        raise FileExistsError("Initialization already claimed; no retry")
    out = ROOT / protocol["output_directory"]
    out.mkdir(exist_ok=False)
    receipt = {
        "status": "STARTED_INITIALIZATION_ONLY",
        "supervisor_pid": os.getpid(),
        "protocol_sha256": sys.argv[1],
        "decision_sha256": pin(decision_path)["sha256"],
        "start_utc": datetime.now(timezone.utc).isoformat(),
        "child_calls": 0,
        "no_retry": True,
        "PE_authorized": False,
    }
    fresh(out / "STARTED.json", receipt)
    proc = None
    deadline = started + protocol["wall_seconds_from_entry"]
    env = dict(os.environ)
    env.update({name: "1" for name in
                ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")})
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = ["/opt/lal_env/bin/python", "-I", "-B", str(ROOT / "control_init.py"),
            protocol["control_contract_sha256"]]
    try:
        if time.monotonic() >= deadline:
            raise TimeoutError("Deadline exhausted before child launch")
        with (out / "stdout.txt").open("xb") as stdout, (out / "stderr.txt").open("xb") as stderr:
            proc = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=stdout, stderr=stderr,
                                    stdin=subprocess.DEVNULL, start_new_session=True)
            receipt.update(child_pid=proc.pid, child_calls=1)
            fresh(out / "CHILD.json", {"pid": proc.pid, "argv": argv, "new_process_group": True})
            remaining = max(0.001, deadline - time.monotonic())
            try:
                receipt["returncode"] = proc.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                receipt["deadline_exceeded"] = True
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=protocol["termination_grace_seconds"])
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait(timeout=protocol["kill_reap_seconds"])
                receipt["returncode"] = proc.returncode
                raise TimeoutError("External initialization deadline exceeded; process group terminated")
        result_path = ROOT / "CONTROL_INIT_001" / "RESULT.json"
        if not result_path.is_file():
            raise RuntimeError("Child ended without terminal result")
        result = json.loads(result_path.read_bytes())
        receipt["child_result"] = {"path": str(result_path), **pin(result_path)}
        receipt["child_status"] = result.get("status")
        counters = result.get("counters", {})
        expected_counters = {"waveform_attempts", "likelihood_evaluation_attempts", "sampler_attempts", "source_attempts"}
        if (receipt["returncode"] != 0 or result.get("status") != "INITIALIZATION_ONLY_PASS"
            or result.get("contract_sha256") != protocol["control_contract_sha256"]
            or set(counters) != expected_counters or any(counters.values())
            or result.get("source_native_counter") != [0, 0.0, 0]
            or result.get("blocked_operations") != [] or result.get("scientific_PE_jobs") != 0
            or result.get("D_read") is not False or result.get("permission_for_P3") is not False
            or len(result.get("rows", [])) != 2):
            raise RuntimeError("Initialization receipt did not pass the frozen boundary")
        receipt["status"] = "SUPERVISED_INITIALIZATION_ONLY_PASS"
    except Exception as exc:
        receipt["status"] = "TERMINAL_INITIALIZATION_CONTROL_FAILURE_NO_RETRY"
        receipt["error"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        if proc is not None and proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait(timeout=protocol["kill_reap_seconds"])
            except (ProcessLookupError, subprocess.TimeoutExpired) as exc:
                receipt["cleanup_issue"] = type(exc).__name__
            receipt["status"] = "TERMINAL_INITIALIZATION_CONTROL_FAILURE_NO_RETRY"
        receipt["elapsed_wall_seconds_from_entry"] = time.monotonic() - started
        receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
        receipt["stdout"] = pin(out / "stdout.txt") if (out / "stdout.txt").exists() else None
        receipt["stderr"] = pin(out / "stderr.txt") if (out / "stderr.txt").exists() else None
        fresh(out / "SUPERVISION_RESULT.json", receipt)
    print(json.dumps({"status": receipt["status"], "receipt": str(out / "SUPERVISION_RESULT.json")}))
    return 0 if receipt["status"] == "SUPERVISED_INITIALIZATION_ONLY_PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
