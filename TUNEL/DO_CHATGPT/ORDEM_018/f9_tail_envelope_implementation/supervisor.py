"""One-shot external supervisor. Requires a future ROOT authorization file.

No authorization or CLAIM is created by package preparation. Preflight is
outside the nominal execution interval; process start through collection has
one 30-second monotonic deadline. The OS may exceed a nominal deadline.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import time
import uuid

PACKAGE = Path(__file__).resolve().parent
TOTAL_SECONDS = 30.0
WORK_SECONDS = 25.0
COOPERATIVE_SECONDS = 23.0
PRIMARY_IDS = ["T01_ATOM", "T02_THRESHOLD_AND_DOMAIN", "T03_EVEN", "T04_ODD",
               "T05_MONOTONE_D148", "T06_NO_FALSE_UNDERFLOW", "T07_LOWER_ENDPOINT",
               "T08_AGGREGATION_AND_FAILURE"]
NEGATIVE_IDS = ["N01_IDENTITY_AND_BINDING", "N02_CERTIFICATION_NOT_FLAGS",
                "N03_CANONICAL_AND_SIZE", "N04_RESOURCE_AFTER_SEMANTICS",
                "N05_SCRATCH_PREFLIGHT", "N06_FAMILY_DUPLICATES_AND_TAMPERING",
                "N07_ROOT_CERTIFICATE_BOUNDARIES"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_small(path, maximum=2 * 1024 * 1024):
    if path.stat().st_size > maximum:
        raise RuntimeError("PREFLIGHT_FILE_SIZE:" + path.name)
    return path.read_bytes()


def checked_json(path, expected=None):
    data = read_small(path)
    if expected is not None and sha(data) != expected:
        raise RuntimeError("PIN_MISMATCH:" + path.name)
    return json.loads(data)


def create_json(path, value):
    data = (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode("ascii")
    # Exclusive creation: uncertain writes are never retried automatically.
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if path.read_bytes() != data:
        raise RuntimeError("PERSISTENCE_MISMATCH:" + path.name)
    return sha(data)


def create_atomic_json(path, value):
    if path.exists():
        raise RuntimeError("OUTPUT_ALREADY_EXISTS:" + path.name)
    data = (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode("ascii")
    temporary = path.with_name(path.name + ".tmp_" + uuid.uuid4().hex)
    with temporary.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != data:
        raise RuntimeError("TEMPORARY_MISMATCH:" + path.name)
    os.replace(temporary, path)
    if path.read_bytes() != data:
        raise RuntimeError("FINAL_MISMATCH:" + path.name)


def preflight(args):
    if not args.execute_authorized_once:
        raise RuntimeError("EXPLICIT_EXECUTION_SWITCH_REQUIRED")
    inputs_path = PACKAGE / "EXECUTION_INPUTS.json"
    inputs = checked_json(inputs_path, args.inputs_sha256)
    identity = checked_json(PACKAGE / "IDENTITY.json")
    contract = checked_json(PACKAGE / "CONTROL_CONTRACT.json", args.contract_sha256)
    if not inputs["request_id"] == identity["request_id"] == contract["request_id"]:
        raise RuntimeError("REQUEST_ID_MISMATCH")
    for item in inputs["pins"]:
        path = Path(item["path"])
        if not path.is_file() or path.stat().st_size != item["bytes"]:
            raise RuntimeError("PIN_FILE_SIZE:" + path.name)
        with path.open("rb") as stream:
            hasher = hashlib.sha256()
            while block := stream.read(1024 * 1024):
                hasher.update(block)
        if hasher.hexdigest() != item["sha256"]:
            raise RuntimeError("PIN_FILE_HASH:" + path.name)
    if os.path.normcase(os.path.abspath(sys.executable)) != os.path.normcase(inputs["python_executable"]):
        raise RuntimeError("WRONG_PYTHON_EXECUTABLE")
    if contract["limits"]["total_wall_seconds"] != TOTAL_SECONDS:
        raise RuntimeError("CONTRACT_WALL_CHANGED")
    for name in ("CLAIM.json", "RUN", "TERMINAL_RECEIPT.json"):
        if (PACKAGE / name).exists():
            raise RuntimeError("IDENTITY_ALREADY_CONSUMED_OR_OUTPUT_EXISTS:" + name)
    authorization_path = PACKAGE / "AUTORIZACAO_ROOT.json"
    authorization_bytes = read_small(authorization_path, 65536)
    authorization = json.loads(authorization_bytes)
    expected = {
        "request_id": identity["request_id"], "authorized": True, "authorized_by": "ROOT",
        "scope": "F9_SYNTHETIC_TAIL_CONTROLS_ONLY",
        "contract_sha256": args.contract_sha256,
        "execution_inputs_sha256": args.inputs_sha256,
        "one_execution_only": True, "total_wall_seconds": 30,
        "implementation_review_accepted": True,
    }
    if any(type(authorization.get(k)) is not type(v) or authorization[k] != v
           for k, v in expected.items()):
        raise RuntimeError("SPECIFIC_ROOT_AUTHORIZATION_MISSING_OR_MISMATCHED")
    return identity, contract, sha(authorization_bytes)


def remaining(deadline):
    return max(0.0, deadline - time.monotonic())


def terminate_and_collect(process, deadline):
    """Never allocate an extra timeout after the total deadline."""
    detail = {}
    if process.poll() is None:
        try:
            process.kill()
            detail["kill_requested"] = True
        except Exception as error:
            detail["kill_error"] = {"type": type(error).__name__, "message": str(error)[:1000]}
    wait = remaining(deadline)
    if wait <= 0:
        return None, None, "PROCESS_STATE_UNCERTAIN", detail
    try:
        stdout, stderr = process.communicate(timeout=wait)
        return stdout, stderr, "TERMINATED_AFTER_LIMIT", detail
    except subprocess.TimeoutExpired:
        detail["cleanup_deadline_expired"] = True
        detail["poll_returncode"] = process.poll()
        return None, None, "PROCESS_STATE_UNCERTAIN", detail
    except Exception as error:
        detail["cleanup_error"] = {"type": type(error).__name__, "message": str(error)[:1000]}
        return None, None, "PROCESS_STATE_UNCERTAIN", detail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute-authorized-once", action="store_true")
    parser.add_argument("--inputs-sha256", required=True)
    parser.add_argument("--contract-sha256", required=True)
    args = parser.parse_args()
    preflight_started = time.monotonic()
    try:
        identity, contract, authorization_sha = preflight(args)
    except Exception as error:
        print(json.dumps({"status": "PREFLIGHT_REFUSED_NO_CLAIM",
                          "error": {"type": type(error).__name__, "message": str(error)[:2000]},
                          "process_started": False}))
        return 2

    token = secrets.token_hex(16)
    claim = {
        "request_id": identity["request_id"], "claim_token": token,
        "supervisor_pid": os.getpid(), "authorization_sha256": authorization_sha,
        "contract_sha256": args.contract_sha256, "inputs_sha256": args.inputs_sha256,
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "one_execution_only": True, "scope": "SYNTHETIC_CONTROLS_NOT_SCIENTIFIC_APPLICATION",
    }
    try:
        create_json(PACKAGE / "CLAIM.json", claim)
    except Exception as error:
        print(json.dumps({"status": "CLAIM_WRITE_UNCERTAIN_NO_LAUNCH",
                          "request_id": identity["request_id"],
                          "error": {"type": type(error).__name__, "message": str(error)[:1000]}}))
        return 3

    process = None
    stdout = None
    stderr = None
    worker = None
    status = "FAILED"
    detail = {}
    execution_started = None
    total_deadline = None
    try:
        run = PACKAGE / "RUN"
        run.mkdir(exist_ok=False)
        environment = dict(os.environ)
        for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                     "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
            environment[name] = "1"
        # Start immediately before launch; startup is inside the same total budget.
        execution_started = time.monotonic()
        total_deadline = execution_started + TOTAL_SECONDS
        argv = [sys.executable, "-I", "-X", "utf8", str(PACKAGE / "worker_controls.py"),
                "--request-id", identity["request_id"], "--claim-token", token,
                "--deadline-monotonic", repr(execution_started + COOPERATIVE_SECONDS)]
        process = subprocess.Popen(argv, cwd=str(PACKAGE), env=environment,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=False,
                                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        create_atomic_json(run / "PROCESS_IDENTITY.json", {
            "request_id": identity["request_id"], "supervisor_pid": os.getpid(),
            "worker_pid": process.pid, "argv": argv,
            "execution_started_monotonic": execution_started,
            "total_deadline_monotonic": total_deadline,
        })
        try:
            stdout, stderr = process.communicate(
                timeout=remaining(execution_started + WORK_SECONDS))
        except subprocess.TimeoutExpired:
            stdout, stderr, status, cleanup = terminate_and_collect(process, total_deadline)
            detail.update(cleanup)
            detail["reason"] = "WORK_DEADLINE_EXCEEDED"
        else:
            if len(stdout) > 2 * 1024 * 1024 or len(stderr) > 65536:
                status = "FAILED_OUTPUT_LIMIT"
            elif remaining(total_deadline) <= 0:
                status = "FAILED_NOMINAL_TOTAL_LIMIT"
            else:
                worker = json.loads(stdout.decode("utf-8"))
                expected_ids = PRIMARY_IDS + NEGATIVE_IDS
                valid = (
                    process.returncode == 0 and worker.get("status") == "PASS" and
                    worker.get("request_id") == identity["request_id"] and
                    worker.get("worker_pid") == process.pid and
                    worker.get("supervisor_pid") == os.getpid() and
                    [r.get("id") for r in worker.get("results", [])] == expected_ids and
                    all(r.get("status") == "PASS" for r in worker.get("results", [])) and
                    worker.get("audit_denied") == [] and
                    worker.get("synthetic_only") is True and
                    worker.get("physical_certification") is False and
                    worker.get("observed_data") is False)
                status = "PASS" if valid else "FAILED_WORKER_OR_RECEIPT"
                if remaining(total_deadline) <= 0:
                    status = "FAILED_NOMINAL_TOTAL_LIMIT"
    except Exception as error:
        detail["exception"] = {"type": type(error).__name__, "message": str(error)[:2000]}
        status = "FAILED"
        if process is not None and total_deadline is not None:
            stdout, stderr, cleanup_status, cleanup = terminate_and_collect(process, total_deadline)
            detail["cleanup"] = cleanup
            if cleanup_status == "PROCESS_STATE_UNCERTAIN":
                status = cleanup_status
        elif execution_started is not None:
            status = "PROCESS_START_UNCERTAIN"

    if status == "PASS" and remaining(total_deadline) <= 0:
        status = "FAILED_NOMINAL_TOTAL_LIMIT"
    receipt = {
        "request_id": identity["request_id"], "status": status,
        "supervisor_pid": os.getpid(), "worker_pid": process.pid if process else None,
        "worker_returncode": process.poll() if process else None,
        "authorization_sha256": authorization_sha, "contract_sha256": args.contract_sha256,
        "execution_inputs_sha256": args.inputs_sha256,
        "preflight_seconds": (execution_started or time.monotonic()) - preflight_started,
        "execution_wall_seconds": (time.monotonic() - execution_started
                                   if execution_started is not None else None),
        "nominal_total_seconds": TOTAL_SECONDS, "extra_cleanup_seconds": 0,
        "OS_deadline_guarantee": False,
        "stdout_sha256": sha(stdout) if stdout is not None else None,
        "stderr_sha256": sha(stderr) if stderr is not None else None,
        "stderr_excerpt": stderr[:65536].decode("utf-8", "replace") if stderr is not None else None,
        "worker": worker, "detail": detail,
        "synthetic_only": True, "physical_certification": False,
        "automatic_retry": False,
    }
    try:
        create_atomic_json(PACKAGE / "TERMINAL_RECEIPT.json", receipt)
    except Exception as error:
        print(json.dumps({"status": "RECEIPT_PERSISTENCE_UNCERTAIN",
                          "request_id": identity["request_id"],
                          "prior_status": status,
                          "error": {"type": type(error).__name__, "message": str(error)[:1000]},
                          "do_not_retry": True}))
        return 4
    print(json.dumps({"status": status, "request_id": identity["request_id"],
                      "worker_pid": receipt["worker_pid"],
                      "receipt": str(PACKAGE / "TERMINAL_RECEIPT.json"),
                      "receipt_sha256": sha((PACKAGE / "TERMINAL_RECEIPT.json").read_bytes())}))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
