"""Prepared Q01 extra-prior supervisor; derived from pinned consumed Q01 runner, new scope only. No execution is authorized by this file."""
import argparse
import hashlib
import json
import marshal
import os
from pathlib import Path
import subprocess
import sys
import time
import types
import uuid

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_extra_prior_qualification_preparation")
REQUEST_ID = "4f5a24b4-594d-4c6d-84f6-cd06dc4c6064"
SOURCE_REQUEST_ID = "df482198-56c4-4169-ae5e-3908f5d12f2c"


class Refusal(RuntimeError):
    pass


def need(ok, message):
    if not ok:
        raise Refusal(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True,
                       indent=2, allow_nan=False) + "\n").encode("utf-8")


def read_json(path):
    raw = path.read_bytes()
    return json.loads(raw), raw


def checked_bytes(record):
    path = Path(record["path"])
    raw = path.read_bytes()
    need(len(raw) == record["bytes"] and digest(raw) == record["sha256"],
         "PIN_MISMATCH:" + str(path))
    return raw


def exclusive_json(path, obj):
    """Sticky O_EXCL marker. A partial write also blocks repetition."""
    raw = canonical(obj)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    need(path.read_bytes() == raw, "EXCLUSIVE_WRITE_MISMATCH")
    return digest(raw)


def atomic_new_json(path, obj):
    need(not path.exists(), "REFUSE_OVERWRITE:" + str(path))
    tmp = path.with_name(path.name + ".tmp")
    raw = canonical(obj)
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    need(tmp.read_bytes() == raw, "TEMP_WRITE_MISMATCH")
    need(not path.exists(), "FINAL_ALREADY_EXISTS")
    os.replace(tmp, path)
    need(path.read_bytes() == raw, "FINAL_WRITE_MISMATCH")
    return digest(raw)


def safe_failure(path, kind, exc, extra=None):
    obj = {"status": "FAIL", "request_id": REQUEST_ID, "unit": "Q01_EXTRA_PRIOR_MEASURES",
           "failure_kind": kind, "exception_type": type(exc).__name__,
           "detail": str(exc)[:4000], "extra": extra, "retry_allowed": False}
    try:
        if not path.exists():
            atomic_new_json(path, obj)
    except BaseException:
        # Durable claims remain even if filesystem failure prevents the receipt.
        pass


def validate(decision_sha):
    need(Path(__file__).resolve() == (ROOT / "driver.py").resolve(), "FIXED_ROOT_REQUIRED")
    need(sys.version_info[:2] == (3, 14), "PYTHON_314_REQUIRED")
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "REQUIRED_FLAGS_-I_-S_-B")
    need(type(decision_sha) is str and len(decision_sha) == 64
         and all(c in "0123456789abcdef" for c in decision_sha), "DECISION_DIGEST")
    manifest, mbytes = read_json(ROOT / "MANIFESTO_PREPARACAO.json")
    need(manifest["request_id"] == REQUEST_ID and manifest["unit"] == "Q01_EXTRA_PRIOR_MEASURES",
         "MANIFEST_IDENTITY")
    need(manifest["status"] == "PREPARATION_ONLY_PENDING_INDEPENDENT_REVIEW_AND_ROOT_DECISION",
         "PREPARATION_STATUS")
    decision, dbytes = read_json(ROOT / "ROOT_DECISION.json")
    need(digest(dbytes) == decision_sha, "ROOT_DECISION_PIN")
    need(set(decision) == {"schema", "request_id", "unit", "authorize_single_execution",
                          "manifest_sha256", "review_reference", "scope"}, "DECISION_FIELDS")
    need(decision["schema"] == "F9_Q01_EXTRA_PRIORS_ROOT_DECISION_V1"
         and decision["request_id"] == REQUEST_ID and decision["unit"] == "Q01_EXTRA_PRIOR_MEASURES"
         and decision["authorize_single_execution"] is True
         and decision["manifest_sha256"] == digest(mbytes)
         and decision["scope"] == "ONLY_ELEVEN_SCALAR_PRIOR_JOIN_CASES_NO_OBSERVED",
         "ROOT_SINGLE_EXECUTION_DECISION")
    ref = decision["review_reference"]
    need(type(ref) is dict and set(ref) == {"id", "sha256"}
         and type(ref["id"]) is str and bool(ref["id"])
         and type(ref["sha256"]) is str and len(ref["sha256"]) == 64
         and all(c in "0123456789abcdef" for c in ref["sha256"]), "INDEPENDENT_REVIEW_REFERENCE")
    paths = []
    for rec in manifest["members"]:
        member = Path(rec["path"]).resolve()
        need(member.parent == ROOT.resolve(), "MEMBER_OUTSIDE_FIXED_ROOT")
        need(member.name not in paths, "DUPLICATE_MEMBER")
        checked_bytes(rec)
        paths.append(member.name)
    need({"IDENTIDADE_PREPARACAO.json", "CONTROL_CONTRACT.json", "driver.py",
          "cases.py", "REFERENCIAS_E_COMANDO.md", "STATIC_PREPARATION_RECEIPT.json"}
         <= set(paths), "REQUIRED_MEMBERS")
    contract, _ = read_json(ROOT / "CONTROL_CONTRACT.json")
    need(contract["request_id"] == REQUEST_ID and contract["source_request"] == SOURCE_REQUEST_ID,
         "CONTRACT_IDENTITY")
    need(contract["case_order"] == ['B01', 'B02', 'S01', 'R01', 'F01', 'F02', 'F03', 'Z01', 'N01', 'N02', 'N03']
         and [c["id"] for c in contract["cases"]] == contract["case_order"]
         and contract["case_count"] == 11 and contract["maximum_service_calls"] == 7
         and contract["maximum_total_evaluations"] == 16393, "FIXED_CASES")
    expected_source = ROOT.parent / "f9_physical_prior_preparation" / "physical_prior.py"
    need(Path(contract["candidate"]["path"]).resolve() == expected_source.resolve(),
         "CANDIDATE_SOURCE_PATH")
    checked_bytes(contract["candidate"])
    interpreter = contract["runtime"]["interpreter"]
    need(Path(sys.executable).resolve() == Path(interpreter["path"]).resolve(), "INTERPRETER_PATH")
    checked_bytes(interpreter)
    for rec in contract["sources"]:
        checked_bytes(rec)
    for name in ("CLAIM.json", "AUTH.json", "AUTHORIZATION.json"):
        need(not (ROOT / name).exists(), "UNEXPECTED_LEGACY_AUTH_OR_CLAIM")
    return contract, manifest, digest(mbytes), decision_sha


def load_bytes(path, raw, name):
    """Executed only inside consumed worker; compiled object comes from pinned bytes."""
    code = compile(raw, str(path), "exec", dont_inherit=True, optimize=0)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    exec(code, module.__dict__)
    need(path.read_bytes() == raw, "SOURCE_CHANGED_DURING_LOAD")
    return module, {"path": str(path), "source_sha256": digest(raw),
                    "compiled_module_sha256": digest(marshal.dumps(code)),
                    "co_filename": code.co_filename,
                    "loader": "exec of exact pinned byte compilation, optimize=0; no pycache"}


def worker(decision_sha, nonce):
    started = time.monotonic()
    output = ROOT / "execution_once"
    consumed = False
    try:
        contract, manifest, msha, dsha = validate(decision_sha)
        claim, _ = read_json(ROOT / "RUN_CLAIM.json")
        need(claim["request_id"] == REQUEST_ID and claim["manifest_sha256"] == msha
             and claim["decision_sha256"] == dsha and claim["nonce"] == nonce
             and claim["supervisor_pid"] == os.getppid(), "WORKER_PARENT_CLAIM")
        need(output.is_dir(), "OUTPUT_NOT_RESERVED")
        deadline = claim["cooperative_deadline"]
        need(time.monotonic() < deadline, "WORKER_START_TOO_LATE")
        exclusive_json(output / "WORKER_STARTED.json", {
            "request_id": REQUEST_ID, "pid": os.getpid(), "parent_pid": os.getppid(),
            "nonce": nonce, "manifest_sha256": msha, "decision_sha256": dsha,
            "consumption": "before candidate loading", "retry_allowed": False})
        consumed = True
        # Preload standard-library dependencies only, before observing candidate calls.
        import math
        import heapq
        import fractions
        need("numpy" not in sys.modules and "scipy" not in sys.modules and "camb" not in sys.modules,
             "FORBIDDEN_NUMERICAL_IMPORT")
        source = Path(contract["candidate"]["path"])
        raw = checked_bytes(contract["candidate"])
        candidate, candidate_attest = load_bytes(source, raw, "q01_df482_pinned_candidate")
        precision_path = Path(contract["precision_service"]["path"])
        precision, precision_attest = load_bytes(precision_path, checked_bytes(contract["precision_service"]), "q01_f820_service_dependency")
        need(precision.LOG_SERVICE_ID == contract["precision_service_ids"]["LOG_SERVICE_ID"] and precision.QUAD_SERVICE_ID == contract["precision_service_ids"]["QUAD_SERVICE_ID"], "PRECISION_DEPENDENCY_IDENTITY")
        precision_functions = {}
        for service_name in ("log_exp_quad_interval", "positive_quad_1d"):
            service_fn = getattr(precision, service_name)
            need(service_fn.__globals__ is precision.__dict__ and service_fn.__code__.co_filename == str(precision_path), "LOADED_PRECISION_BINDING")
            precision_functions[service_name] = {"co_filename": service_fn.__code__.co_filename,
                "code_sha256": digest(marshal.dumps(service_fn.__code__))}
        case_record = next(x for x in manifest["members"] if Path(x["path"]).name == "cases.py")
        cases_path = ROOT / "cases.py"
        cases, cases_attest = load_bytes(cases_path, checked_bytes(case_record), "q01_extra_prior_cases_pinned")
        need(list(cases.CASE_IDS) == contract["case_order"], "CASE_CODE_ORDER")
        functions = {}
        for name in ("_analytic", "_rd_quadrature", "_Curve.peak"):
            fn = candidate._Curve.peak if name == "_Curve.peak" else getattr(candidate, name)
            need(fn.__globals__ is candidate.__dict__ and fn.__code__.co_filename == str(source),
                 "LOADED_FUNCTION_BINDING")
            functions[name] = {"co_filename": fn.__code__.co_filename,
                               "code_sha256": digest(marshal.dumps(fn.__code__))}
        atomic_new_json(output / "LOADED_CODE_ATTESTATION.json", {
            "request_id": REQUEST_ID, "candidate": candidate_attest, "cases": cases_attest,
            "functions": functions, "precision_module": precision_attest, "precision_functions": precision_functions, "python_version": sys.version,
            "executable": sys.executable, "dont_write_bytecode": sys.dont_write_bytecode,
            "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site},
            "pid": os.getpid(), "parent_pid": os.getppid(),
            "candidate_monkeypatched": False, "scientific_imports": False})
        results, total_evaluations, total_invocations = [], 0, 0
        for case in contract["cases"]:
            need(time.monotonic() < deadline, "COOPERATIVE_DEADLINE_BEFORE_CASE")
            cid = case["id"]
            exclusive_json(output / (cid + "_STARTED.json"), {
                "request_id": REQUEST_ID, "case_id": cid, "retry_allowed": False})
            result = cases.run_case(candidate, case, str(source), deadline, precision)
            atomic_new_json(output / (cid + "_RESULT.json"), result)
            results.append(result)
            total_evaluations += result["observed"]["calls"]
            total_invocations += result["service_invocations"]
            need(result["status"] == "PASS", "CASE_FAILED:" + cid)
            need(total_evaluations <= contract["maximum_total_evaluations"], "TOTAL_EVALUATION_CAP")
            need(total_invocations <= contract["maximum_service_calls"], "TOTAL_INVOCATION_CAP")
            need(time.monotonic() < deadline, "COOPERATIVE_DEADLINE_AFTER_CASE_IO")
        need(len(results) == 11 and total_invocations == 7, "COMPLETE_CASE_COLLECTION")
        checked_bytes(contract["candidate"])
        checked_bytes(case_record)
        checked_bytes(contract["precision_service"])
        need(sum(x["candidate_invocations"] for x in results) == 11, "PRIOR_ENTRY_COUNT")
        need(sum(x["real_service_invocations"] for x in results) == 4 and sum(x["synthetic_service_invocations"] for x in results) == 3, "REAL_VS_NEGATIVE_SERVICE_COUNTS")
        need(sum(x["curve_log_calls"] for x in results) <= 4105, "CURVE_WORK_CAP")
        need(sum((x["reference"] or {}).get("evaluations", 0) for x in results) == 257, "REFERENCE_WORK_COUNT")
        result = {"request_id": REQUEST_ID, "unit": "Q01_EXTRA_PRIOR_MEASURES", "status": "PASS",
                  "scope": "ENGINEERING_QUALIFICATION_OF_ELEVEN_SCALAR_PRIOR_JOINS_ONLY",
                  "case_ids": [x["case_id"] for x in results], "case_count": len(results),
                  "observed_total_evaluations": total_evaluations,
                  "service_invocations": total_invocations, "prior_entry_calls": 11, "real_f820_calls": 4, "synthetic_service_calls": 3,
                  "curve_log_calls": sum(x["curve_log_calls"] for x in results), "reference_evaluations": 257,
                  "worker_wall_seconds": time.monotonic() - started,
                  "manifest_sha256": msha, "decision_sha256": dsha,
                  "uniform_accuracy_certificate": False, "observed_data": False,
                  "provisional_until_supervisor_exit_zero": True}
        atomic_new_json(output / "RESULT.json", result)
        need(time.monotonic() < deadline, "COOPERATIVE_DEADLINE_AFTER_RESULT_IO")
        return 0
    except BaseException as exc:
        if consumed:
            safe_failure(output / "WORKER_FAILURE.json", "WORKER_TERMINAL_FAILURE", exc)
        else:
            print(json.dumps({"status": "WORKER_REFUSED_BEFORE_CONSUMPTION",
                              "detail": str(exc)[:1000]}), file=sys.stderr, flush=True)
        return 1


def supervisor(decision_sha, started):
    output = ROOT / "execution_once"
    claimed, proc = False, None
    deadline = started + 30.0
    try:
        contract, manifest, msha, dsha = validate(decision_sha)
        need(not output.exists() and not (ROOT / "RUN_CLAIM.json").exists(), "ALREADY_CONSUMED_OR_UNCERTAIN")
        need(time.monotonic() < started + 23.0, "PREFLIGHT_TOO_LATE")
        nonce = str(uuid.uuid4())
        exclusive_json(ROOT / "RUN_CLAIM.json", {
            "request_id": REQUEST_ID, "unit": "Q01_EXTRA_PRIOR_MEASURES", "manifest_sha256": msha,
            "decision_sha256": dsha, "supervisor_pid": os.getpid(), "nonce": nonce,
            "started_monotonic": started, "cooperative_deadline": started + 23.0,
            "total_deadline": deadline, "retry_allowed": False})
        claimed = True
        output.mkdir(exist_ok=False)
        command = [contract["runtime"]["interpreter"]["path"], "-I", "-S", "-B", "-X", "utf8",
                   str(ROOT / "driver.py"), "--decision-sha256", dsha, "--worker-nonce", nonce]
        env = os.environ.copy()
        for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
            env[name] = "1"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        with (output / "stdout.log").open("xb") as stdout, (output / "stderr.log").open("xb") as stderr:
            need(time.monotonic() < started + 25.0, "NO_REMAINING_WORK_TIME")
            proc = subprocess.Popen(command, cwd=str(ROOT), env=env, stdin=subprocess.DEVNULL,
                                    stdout=stdout, stderr=stderr, shell=False,
                                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            atomic_new_json(output / "CHILD_IDENTITY.json", {
                "pid": proc.pid, "parent_pid": os.getpid(), "argv": command,
                "request_id": REQUEST_ID, "single_child": True})
            try:
                proc.wait(timeout=max(0.001, started + 25.0 - time.monotonic()))
            except subprocess.TimeoutExpired:
                proc.kill()  # Only the Popen child owned by this supervisor.
                proc.wait(timeout=max(0.001, min(4.0, deadline - time.monotonic())))
                raise Refusal("WORKER_TIMEOUT_NO_RETRY")
        need(proc.returncode == 0, "WORKER_EXIT_NONZERO:" + str(proc.returncode))
        need(not (output / "WORKER_FAILURE.json").exists(), "WORKER_FAILURE_RECORD")
        for name in ("stdout.log", "stderr.log"):
            need((output / name).stat().st_size <= 65536, "OUTPUT_ACCEPTANCE_CAP:" + name)
        result, result_raw = read_json(output / "RESULT.json")
        need(result["status"] == "PASS" and result["request_id"] == REQUEST_ID
             and result["manifest_sha256"] == msha and result["case_ids"] == contract["case_order"]
             and result["case_count"] == 11 and result["service_invocations"] == 7
             and result["observed_total_evaluations"] <= 16393, "WORKER_RESULT_IDENTITY")
        for case in contract["cases"]:
            record, _ = read_json(output / (case["id"] + "_RESULT.json"))
            need(record["case_id"] == case["id"] and record["status"] == "PASS", "INCOMPLETE_CASE_SET")
        need(time.monotonic() < deadline, "TOTAL_DEADLINE_BEFORE_FINAL_IO")
        terminal = {"request_id": REQUEST_ID, "unit": "Q01_EXTRA_PRIOR_MEASURES", "status": "PASS",
                    "worker_exit": proc.returncode, "result_sha256": digest(result_raw),
                    "manifest_sha256": msha, "decision_sha256": dsha,
                    "wall_seconds_before_terminal_io": time.monotonic() - started,
                    "acceptance_requires_external_supervisor_exit_zero": True,
                    "no_failure_record_required": True, "uniform_certificate": False}
        terminal_sha = atomic_new_json(output / "TERMINAL_RECEIPT.json", terminal)
        need(time.monotonic() < deadline, "TOTAL_DEADLINE_AFTER_TERMINAL_IO")
        need(digest((output / "TERMINAL_RECEIPT.json").read_bytes()) == terminal_sha,
             "TERMINAL_READBACK_PIN")
        need(time.monotonic() < deadline, "TOTAL_DEADLINE_AFTER_READBACK")
        print(json.dumps({"status": "PASS", "request_id": REQUEST_ID,
                          "terminal_sha256": terminal_sha}), flush=True)
        need(time.monotonic() < deadline, "TOTAL_DEADLINE_AFTER_STDOUT_FLUSH")
        return 0
    except BaseException as exc:
        if proc is not None and proc.poll() is None:
            try:
                proc.kill()
                proc.wait(timeout=max(0.001, min(4.0, deadline - time.monotonic())))
            except BaseException:
                pass
        if claimed:
            target = output / "FAILURE.json" if output.exists() else ROOT / "FAILURE_BEFORE_OUTPUT.json"
            safe_failure(target, "SUPERVISOR_TERMINAL_FAILURE", exc,
                         {"child_pid": None if proc is None else proc.pid,
                          "child_exit": None if proc is None else proc.poll(),
                          "wall_seconds": time.monotonic() - started})
        print(json.dumps({"status": "FAIL" if claimed else "REFUSED_BEFORE_CLAIM",
                          "request_id": REQUEST_ID, "detail": str(exc)[:1000]}),
              file=sys.stderr, flush=True)
        return 1


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision-sha256", required=True)
    parser.add_argument("--worker-nonce")
    args = parser.parse_args()
    if args.worker_nonce is not None:
        return worker(args.decision_sha256, args.worker_nonce)
    return supervisor(args.decision_sha256, started)


if __name__ == "__main__":
    raise SystemExit(main())
