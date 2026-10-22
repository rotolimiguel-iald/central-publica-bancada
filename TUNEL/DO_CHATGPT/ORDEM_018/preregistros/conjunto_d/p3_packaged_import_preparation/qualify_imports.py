"""Candidate one-use Linux runtime/import inspection; no scientific calls.
No permission is embedded. A future exact ROOT decision is mandatory.
"""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent
PREPARATION_ID = "2bfd4665-a7e7-410a-aeb3-0406f90a596f"
RUN = ROOT / "IMPORT_QUALIFICATION"
TOTAL_SECONDS = 120.0
WORK_SECONDS = 110.0


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_bytes())


def write_once(path, value):
    raw = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    with Path(path).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if Path(path).read_bytes() != raw:
        raise OSError("Durable write verification failed")


def verify_admission(decision_hash):
    if sys.platform != "linux" or not sys.flags.isolated or not sys.dont_write_bytecode:
        raise RuntimeError("Pinned isolated Linux interpreter with -I -B required")
    if len(decision_hash) != 64 or any(c not in "0123456789abcdef" for c in decision_hash):
        raise ValueError("Canonical decision hash required")
    dp = ROOT / "ROOT_DECISION.json"
    if digest(dp) != decision_hash:
        raise ValueError("ROOT decision bytes differ")
    decision = read_json(dp)
    required = {"approved", "action", "preparation_id", "qualification_id",
                "manifest_sha256", "contract_sha256"}
    if set(decision) != required:
        raise ValueError("Unexpected decision schema")
    if (decision["approved"] is not True
            or decision["action"] != "QUALIFY_PINNED_IMPORTS_ONLY"
            or decision["preparation_id"] != PREPARATION_ID
            or str(uuid.UUID(decision["qualification_id"])) != decision["qualification_id"]):
        raise ValueError("Matching future imports-only decision required")
    for name, key in (("MANIFESTO_PREPARACAO.json", "manifest_sha256"),
                      ("CONTRATO_CANDIDATO.json", "contract_sha256")):
        if digest(ROOT / name) != decision[key]:
            raise ValueError("Admission pin differs: " + name)
    manifest = read_json(ROOT / "MANIFESTO_PREPARACAO.json")
    if manifest["preparation_id"] != PREPARATION_ID:
        raise ValueError("Manifest identity differs")
    seen = set()
    for row in manifest["files"]:
        path = (ROOT / row["relative_path"]).resolve()
        if ROOT not in path.parents or path in seen:
            raise ValueError("Manifest path is duplicate/outside package")
        seen.add(path)
        if path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            raise ValueError("Package bytes differ: " + row["relative_path"])
    contract = read_json(ROOT / "CONTRATO_CANDIDATO.json")
    if (contract["preparation_id"] != PREPARATION_ID or contract["science_enabled"] is not False
            or contract["imports_qualification"]["total_nominal_seconds"] != TOTAL_SECONDS):
        raise ValueError("Scope/limits differ")
    pin = read_json(ROOT / "INTERPRETER_PIN.json")
    if (Path(sys.executable).resolve() != Path(pin["path"]).resolve()
            or Path(sys.executable).resolve().stat().st_size != pin["bytes"]
            or digest(sys.executable) != pin["sha256"]):
        raise ValueError("Interpreter differs from historical candidate pin")
    return decision


def worker(decision_hash):
    decision = verify_admission(decision_hash)
    claim = read_json(RUN / "CLAIM.json")
    if claim != {"decision_sha256": decision_hash,
                 "qualification_id": decision["qualification_id"],
                 "contract_sha256": decision["contract_sha256"]}:
        raise ValueError("One-use supervisor claim required")
    # An interruption leaves this reservation. No new name or direct invocation
    # can reuse the same consumed package/contract.
    write_once(RUN / "CHILD_STARTED.json", {"pid": os.getpid(), "claim": claim})
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (8 * 1024**3,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (100, 105))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2 * 1024**2,) * 2)
    sys.pycache_prefix = str(ROOT / "UNUSED_BYTECODE_CACHE")
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))
    runtime = read_json(ROOT / "RUNTIME_P3_READONLY.json")
    plan = read_json(ROOT / "PREHOOK_PLAN.json")
    import prehook_imports
    for row in runtime["files"]:
        prehook_imports.require_pin(row["path"], row)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        if os.environ.get(name) != "1":
            raise ValueError("One-thread environment required")
    # Mirrors the existing driver's import closure, without invoking its main,
    # generator, geometry, detector initialization or any scientific function.
    import prior_transform
    import failure_audit
    import audit_guard
    import result_acceptance
    import numpy
    import bilby
    import dynesty
    from dynesty.utils import compute_integrals
    import pseob_source as source
    import synthetic_adapter_v2 as adapter
    from preload_npz_codec import preload_npz_codec
    import init_detectors
    preload_npz_codec(read_json(ROOT / "CODEC_CP437_PIN.json"))
    receipt = prehook_imports.preload_known_imports(ROOT, runtime, plan, source, adapter)
    receipt.update(qualification_id=decision["qualification_id"],
                   preparation_id=PREPARATION_ID,
                   decision_sha256=decision_hash, pid=os.getpid(),
                   runtime_snapshot_sha256=digest(ROOT / "RUNTIME_P3_READONLY.json"),
                   scientific_function_calls=0, PE_jobs=0, observed_data_opened_by_driver=False,
                   import_side_effect_scope="Python/native module initialization is not syscall-contained")
    write_once(RUN / "IMPORT_RECEIPT.json", receipt)
    return 0


def supervisor(decision_hash):
    started = time.monotonic()
    deadline = started + TOTAL_SECONDS
    decision = verify_admission(decision_hash)
    if time.monotonic() >= started + WORK_SECONDS:
        raise TimeoutError("Admission exceeded work budget")
    RUN.mkdir(exist_ok=False)
    write_once(RUN / "CLAIM.json", {
        "decision_sha256": decision_hash, "qualification_id": decision["qualification_id"],
        "contract_sha256": decision["contract_sha256"]})
    result = {"status": "TERMINAL_FAILURE", "decision_sha256": decision_hash,
              "qualification_id": decision["qualification_id"], "scientific_qualification": False}
    child = None
    try:
        env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                   MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
        remaining = started + WORK_SECONDS - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("Work budget expired before child")
        with (RUN / "stdout.log").open("xb") as out, (RUN / "stderr.log").open("xb") as err:
            child = subprocess.Popen(
                [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--worker", decision_hash],
                stdin=subprocess.DEVNULL, stdout=out, stderr=err, cwd=ROOT,
                env=env, start_new_session=True)
            # Popen handle is the newly created direct child; no PID scan/killpg.
            try:
                remaining = started + WORK_SECONDS - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(child.args, 0)
                rc = child.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                child.kill()
                try:
                    child.wait(timeout=max(0.001, deadline - time.monotonic()))
                except subprocess.TimeoutExpired:
                    result["cleanup_unconfirmed"] = True
                raise TimeoutError("Imports child exceeded nominal work deadline")
        result.update(child_pid=child.pid, returncode=rc)
        if rc != 0:
            raise RuntimeError("Imports child failed; no retry")
        receipt = read_json(RUN / "IMPORT_RECEIPT.json")
        if (receipt.get("status") != "EXPLICIT_PREHOOK_IMPORTS_COMPLETE"
                or receipt.get("decision_sha256") != decision_hash
                or receipt.get("qualification_id") != decision["qualification_id"]
                or receipt.get("pid") != child.pid or receipt.get("scientific_function_calls") != 0):
            raise ValueError("Child receipt identity/status differs")
        result.update(status="IMPORTS_ONLY_COMPLETE",
                      receipt_sha256=digest(RUN / "IMPORT_RECEIPT.json"))
    except BaseException as exc:
        result.update(status="TERMINAL_FAILURE", error=type(exc).__name__ + ": " + str(exc))
        if child is not None and child.poll() is None and not result.get("cleanup_unconfirmed"):
            child.kill()
            try:
                child.wait(timeout=max(0.001, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                result["cleanup_unconfirmed"] = True
    result["elapsed_before_receipt_s"] = time.monotonic() - started
    if time.monotonic() >= deadline:
        result["status"] = "DEADLINE_EXCEEDED"
    write_once(RUN / "TERMINAL_RECEIPT.json", result)
    terminal_hash = digest(RUN / "TERMINAL_RECEIPT.json")
    print(json.dumps({"status": result["status"], "terminal_sha256": terminal_hash}), flush=True)
    # Receipt is provisional until this external exit succeeds. A late write,
    # hash, flush or exception invalidates it even if it contains COMPLETE.
    if time.monotonic() >= deadline:
        write_once(RUN / "FINALIZATION_FAILURE.json", {"reason": "NOMINAL_DEADLINE_EXCEEDED"})
        return 2
    return 0 if result["status"] == "IMPORTS_ONLY_COMPLETE" else 2


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        return worker(sys.argv[2])
    if len(sys.argv) == 2:
        return supervisor(sys.argv[1])
    raise RuntimeError("PREPARATION_ONLY: future exact ROOT decision hash required")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException:
        # Missing decision refuses before any scientific library import.
        raise
