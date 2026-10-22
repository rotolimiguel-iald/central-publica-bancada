"""One prepared NC02 unit. No execution during preparation."""
import sys
sys.dont_write_bytecode = True
import argparse
import copy
import ctypes
from ctypes import wintypes
import dataclasses
import fractions
import hashlib
import json
import math
import os
from pathlib import Path
import time
import types

PACKAGE = Path(__file__).resolve().parent
DENIED = []
DEADLINE = None
IDS = ["NC02-RAT-01-POSITIVE", "NC02-RAT-01-NEGATIVE-ANNIHILATION"]


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    require(path.stat().st_size <= 1024 * 1024, "INPUT_SIZE")
    return json.loads(path.read_bytes())


def budget():
    require(not DENIED, "AUDIT_DENIAL_LATCHED")
    require(time.monotonic() < DEADLINE, "COOPERATIVE_WORKER_DEADLINE")


def norm(path):
    return os.path.normcase(os.path.abspath(path))


def install_audit(allowed):
    def audit(event, args):
        reason = None
        if event == "open":
            path, mode, flags = args
            writing = ((isinstance(mode, str) and any(c in mode for c in "wax+")) or
                       (isinstance(flags, int) and bool(flags &
                        (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))))
            if writing or not isinstance(path, (str, bytes, os.PathLike)) or norm(os.fsdecode(path)) not in allowed:
                reason = "UNADMITTED_FILE_ACCESS"
        elif event.startswith(("socket.", "subprocess.", "os.system", "os.spawn", "os.exec", "os.fork")):
            reason = "FORBIDDEN_EXTERNAL_OPERATION"
        elif event in {"os.remove", "os.rename", "os.mkdir", "os.rmdir", "os.chmod", "os.link", "os.symlink"}:
            reason = "FORBIDDEN_FILESYSTEM_MUTATION"
        if reason:
            if len(DENIED) < 16:
                DENIED.append({"event": event, "reason": reason})
            raise PermissionError(reason)
    sys.addaudithook(audit)


def load_source(name, path):
    # Explicit source loading avoids probing a pyc cache before an allowed source.
    budget()
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    budget()
    return module


class MemoryCounters(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
        (name, ctypes.c_size_t) for name in (
            "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
            "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
            "PagefileUsage", "PeakPagefileUsage")]


def memory_reader():
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    current = kernel.GetCurrentProcess
    current.argtypes = []
    current.restype = wintypes.HANDLE
    get_memory = psapi.GetProcessMemoryInfo
    get_memory.argtypes = [wintypes.HANDLE, ctypes.POINTER(MemoryCounters), wintypes.DWORD]
    get_memory.restype = wintypes.BOOL
    handle = current()
    def read():
        value = MemoryCounters()
        value.cb = ctypes.sizeof(value)
        require(bool(get_memory(handle, ctypes.byref(value), value.cb)), "MEMORY_COUNTER_UNAVAILABLE")
        return int(value.PeakWorkingSetSize)
    return read


def main():
    global DEADLINE
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--request-id", required=True)
    args_parser.add_argument("--claim-token", required=True)
    args_parser.add_argument("--deadline-monotonic", required=True, type=float)
    args = args_parser.parse_args()
    DEADLINE = args.deadline_monotonic
    started = time.monotonic()
    require(math.isfinite(DEADLINE), "INVALID_DEADLINE")
    budget()
    claim = read_json(PACKAGE / "CLAIM.json")
    raw_inputs = (PACKAGE / "EXECUTION_INPUTS.json").read_bytes()
    inputs = json.loads(raw_inputs)
    require(sha(raw_inputs) == claim["inputs_sha256"], "INPUTS_BINDING")
    contract_raw = (PACKAGE / "CONTROL_CONTRACT.json").read_bytes()
    require(sha(contract_raw) == claim["contract_sha256"], "CONTRACT_BINDING")
    require(args.request_id == claim["request_id"] == inputs["request_id"], "REQUEST_BINDING")
    require(args.claim_token == claim["claim_token"] and os.getppid() == claim["supervisor_pid"], "PROCESS_BINDING")
    require(norm(sys.executable) == norm(inputs["python_executable"]), "RUNTIME_IDENTITY")
    allowed = set()
    for item in inputs["pins"]:
        path = Path(item["path"])
        data = path.read_bytes()
        require(len(data) == item["bytes"] and sha(data) == item["sha256"], "DEPENDENCY_PIN:" + path.name)
        allowed.add(norm(path))
        budget()
    payload_path = Path(inputs["payload_path"])
    payload_raw = payload_path.read_bytes()
    require(sha(payload_raw) == inputs["payload_sha256"], "PAYLOAD_BINDING")
    payload = json.loads(payload_raw)
    require([case["id"] for case in payload["cases"]] == IDS, "COMPLETE_CASE_ORDER")
    expected = [copy.deepcopy(case["expected_analytic_not_run"]) for case in payload["cases"]]
    for case in payload["cases"]:
        del case["expected_analytic_not_run"]
    # Do not offer expected symbolic answers or prose formulas to either implementation.
    payload.pop("arithmetic_proof_reference", None)
    peak_reader = memory_reader()
    install_audit(allowed)
    codec = load_source("nc02_pinned_tail_codec", Path(inputs["codec_source_path"]))
    load_source("codec_adapter", PACKAGE / "codec_adapter.py")
    builder = load_source("nc02_builder", PACKAGE / "builder.py")
    verifier = load_source("nc02_verifier", PACKAGE / "verifier.py")
    results = []
    for case, expectation in zip(payload["cases"], expected):
        budget()
        certificate = builder.build_case(copy.deepcopy(payload), copy.deepcopy(case), codec._rational)
        budget()
        verification = verifier.verify_case(copy.deepcopy(payload), copy.deepcopy(case), certificate, codec._rational)
        budget()
        require(verification["verified"] is True, "INDEPENDENT_VERIFICATION")
        require(certificate["status"] == expectation["status"], "EXPECTED_STATUS")
        for key in ("lower", "upper"):
            require(certificate[key] == expectation[key], "EXPECTED_BOUND:" + key)
        if "annihilation_residual" in expectation:
            require(certificate["annihilation_residual"] == expectation["annihilation_residual"], "EXPECTED_ANNIHILATION")
        results.append({"id": case["id"], "status": "PASS", "certificate": certificate,
                        "independent_verification": verification})
    # Pin all Python-module file origins actually loaded; OS DLL dependency closure
    # is not claimed. Files loaded implicitly outside this set invalidate the unit.
    origins = sorted({norm(module.__file__) for module in list(sys.modules.values())
                      if getattr(module, "__file__", None) and Path(module.__file__).is_absolute()})
    require(all(origin in allowed for origin in origins), "UNPINNED_IMPORTED_MODULE")
    budget()
    peak = peak_reader()
    require(peak <= 256 * 1024 * 1024, "OBSERVED_PEAK_MEMORY_ACCEPTANCE_LIMIT")
    report = {"status": "PASS", "request_id": args.request_id, "claim_token": args.claim_token,
              "worker_pid": os.getpid(), "supervisor_pid": os.getppid(),
              "execution_inputs_sha256": sha(raw_inputs), "contract_sha256": sha(contract_raw),
              "payload_sha256": sha(payload_raw), "results": results,
              "controls_seconds": time.monotonic() - started,
              "peak_working_set_bytes": peak,
              "memory_scope": "Peak working set observed before report serialization; acceptance check, not OS enforcement or full process-lifetime ceiling.",
              "loaded_module_origins": origins, "audit_denied": DENIED,
              "synthetic_only": True, "physical_certification": False, "observed_data": False,
              "remote_calls": 0, "solver_calls": 0, "automatic_retry": False}
    raw_output = json.dumps(report, ensure_ascii=True, allow_nan=False)
    require(len(raw_output.encode("ascii")) + 1 <= 128 * 1024, "OUTPUT_SIZE")
    budget()
    print(raw_output, flush=True)
    budget()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps({"status": "FAILED", "error_type": type(error).__name__,
                          "error": str(error)[:1000], "audit_denied": DENIED,
                          "automatic_retry": False}), flush=True)
        sys.exit(1)
