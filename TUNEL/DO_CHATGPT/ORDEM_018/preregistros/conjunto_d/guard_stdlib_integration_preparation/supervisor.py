"""Prepared external supervisor; no authority or claim is supplied by this source."""
import time
ENTRY_MONOTONIC = time.monotonic()
from pathlib import Path
import os, sys, json, hashlib, subprocess, datetime, threading, uuid
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\preregistros\conjunto_d\guard_stdlib_integration_preparation")
REQUEST = "278b56a3-36e0-4adc-9708-af49f094d1df"
SCOPE = "AUDIT_GUARD_STDLIB_INTEGRATION_THREE_CHILDREN_ONLY_ONCE"
CASE_IDS = ["I01_REAL_HOOK_JOURNAL", "I02_IMPORT_CACHE_SWALLOWED", "I03_PHYSICAL_JOURNAL_FAILURE"]
LIMIT = 32768

def require(ok, message):
    if not ok: raise RuntimeError(message)

def digest(raw): return hashlib.sha256(raw).hexdigest()

def read_json(path): return json.loads(path.read_bytes())

def exclusive(path, obj):
    raw = (json.dumps(obj, sort_keys=True) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    require(path.read_bytes() == raw, "Durable write verification")

def new_result(path, obj):
    require(not path.exists(), "Consumed output")
    temp = path.with_name(path.name + ".new")
    exclusive(temp, obj); os.replace(temp, path)

class Capture:
    def __init__(self, pipe, overflow):
        self.pipe = pipe; self.buffer = bytearray(); self.total = 0; self.error = None
        self.overflow = overflow; self.thread = threading.Thread(target=self.read, daemon=True)
    def read(self):
        try:
            while True:
                block = os.read(self.pipe.fileno(), 4096)
                if not block: break
                self.total += len(block)
                self.buffer.extend(block[:max(0, LIMIT - len(self.buffer))])
                if self.total > LIMIT: self.overflow.set()
        except BaseException as exc:
            self.error = {"type": type(exc).__name__, "message": str(exc)[:500]}
    def snapshot(self):
        return {"text": bytes(self.buffer).decode("utf-8", errors="replace"), "bytes_seen": self.total,
                "retained_bytes": len(self.buffer), "overflow": self.total > LIMIT,
                "reader_error": self.error, "reader_alive": self.thread.is_alive()}

def run_case(case_id, contract, claim, work_deadline, total_deadline):
    case_dir = BASE / "RUN" / case_id
    case_dir.mkdir()
    case_nonce = str(uuid.uuid4())
    exclusive(case_dir / "DISPATCH.json", {"request_id": REQUEST, "case_id": case_id,
              "nonce": case_nonce, "pid_supervisor": os.getpid(), "retry_allowed": False})
    child = None; caps = []; detail = {}; status = "FAILED"; overflow = threading.Event()
    began = time.monotonic(); case_deadline = min(work_deadline, began + 6)
    try:
        require(time.monotonic() < case_deadline, "No work time left")
        argv = [sys.executable, "-I", "-S", "-B", "-X", "utf8", str(BASE / "worker.py"), "--supervised-stdin"]
        env = {"SystemRoot": os.environ.get("SystemRoot", r"C:\Windows"), "PYTHONDONTWRITEBYTECODE": "1"}
        child = subprocess.Popen(argv, cwd=str(BASE), env=env, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)
        caps = [Capture(child.stdout, overflow), Capture(child.stderr, overflow)]
        for cap in caps: cap.thread.start()
        exclusive(case_dir / "PROCESS.json", {"request_id": REQUEST, "case_id": case_id,
                  "pid_supervisor": os.getpid(), "pid_worker": child.pid, "argv": argv,
                  "case_work_deadline_monotonic": case_deadline, "total_deadline_monotonic": total_deadline})
        child.stdin.write((json.dumps({"request_id": REQUEST, "nonce": claim["nonce"],
                          "case_id": case_id, "case_nonce": case_nonce}) + "\n").encode())
        child.stdin.close()
        while child.poll() is None:
            require(not overflow.is_set(), "OUTPUT_OVERFLOW")
            remain = case_deadline - time.monotonic()
            require(remain > 0, "CASE_WORK_DEADLINE")
            try: child.wait(timeout=min(0.025, remain))
            except subprocess.TimeoutExpired: pass
    except BaseException as exc:
        detail["failure"] = {"type": type(exc).__name__, "message": str(exc)[:1000]}
    if child is not None and child.poll() is None:
        try: child.kill(); detail["kill_requested"] = True
        except BaseException as exc: detail["kill_error"] = str(exc)[:500]
    if child is not None and child.poll() is None:
        remain = min(2, max(0, total_deadline - time.monotonic()))
        if remain:
            try: child.wait(timeout=remain)
            except BaseException as exc: detail["collection_error"] = str(exc)[:500]
    for cap in caps:
        cap.thread.join(timeout=min(1, max(0, total_deadline - time.monotonic())))
    streams = [cap.snapshot() for cap in caps]
    if child is None:
        detail.setdefault("failure", {"message": "NO_CHILD_CREATED"})
    elif child.poll() is None or any(x["reader_alive"] for x in streams):
        status = "PROCESS_STATE_UNCERTAIN"
    elif "failure" not in detail:
        try:
            require(child.returncode == 0, "Child failure")
            require(not overflow.is_set() and not any(x["reader_error"] for x in streams), "Capture failed")
            require(streams[1]["bytes_seen"] == 0, "Unexpected stderr")
            require(time.monotonic() <= total_deadline, "TOTAL_DEADLINE")
            result = json.loads(streams[0]["text"])
            on_disk = (case_dir / "CASE_RESULT.json").read_bytes()
            require(len(on_disk) <= LIMIT and json.loads(on_disk) == result, "Physical result / stdout mismatch")
            require(result["request_id"] == REQUEST and result["case_id"] == case_id, "Result identity")
            require(result["pid"] == child.pid and result["parent_pid"] == os.getpid(), "Result PID")
            require(result["status"] == "PASS_EXPECTED_LATCHED" and result["error"] is None, "Case did not pass")
            require(result["callback_calls"] == 0 and result["unexpected_operations"] == [], "Unexpected callback / denial")
            require(result["scientific_calls"] == result["scientific_imports"] == result["new_children"] == 0, "Scope")
            snap = result["audit_snapshot"]; expected = 2 if case_id == CASE_IDS[0] else 1
            require(snap["installed"] is True and snap["latched"] is True and snap["denial_count"] == expected,
                    "Expected permanent latch invariant")
            require(snap["first_event"] == snap["events"][0] and snap["checkpoint_counts"].get("final") == 1, "First/final invariant")
            require(len(result["hook_seen"]) == expected and all(x["expected"] is True for x in result["hook_seen"]), "Expected hook acts")
            jpath = case_dir / "journal.jsonl"; jb = jpath.read_bytes()
            require(len(jb) <= LIMIT and result["journal"]["path"] == str(jpath), "Journal path/limit")
            require(digest(jb) == result["journal"]["sha256"] and len(jb) == result["journal"]["bytes"], "Journal physical pin")
            rows = [json.loads(line) for line in jb.splitlines()]
            require(rows == ([] if case_id == CASE_IDS[2] else snap["events"]), "Journal event identity")
            counts = result["profile_real_os_calls"]
            if case_id == CASE_IDS[2]:
                require(snap["journal_error"] is not None and counts["write"]["c_exception"] == 1,
                        "Physical failure not exercised")
                require(result["detail"]["physical_error"]["errno"] == 9, "Expected EBADF")
                require(counts["fsync"]["c_call"] == 0, "No fsync after failed write")
            else:
                require(snap["journal_error"] is None and counts["fsync"]["c_return"] == expected,
                        "Fsync physical returns")
                require(counts["write"]["c_return"] >= expected, "Write physical returns")
            if case_id == CASE_IDS[1]:
                require(result["detail"]["import_returned_normally"] is True, "Cache denial was not swallowed")
            reservation = read_json(case_dir / "CASE_CLAIM.json")
            require(reservation["pid"] == child.pid and reservation["nonce"] == case_nonce and
                    reservation["request_id"] == REQUEST and reservation["case_id"] == case_id and
                    reservation["contract_sha256"] == claim["contract_sha256"], "Child claim identity")
            detail["result_pin"] = {"path": str(case_dir / "CASE_RESULT.json"), "bytes": len(on_disk), "sha256": digest(on_disk)}
            detail["worker"] = result; status = "PASS"
        except BaseException as exc:
            detail["failure"] = {"type": type(exc).__name__, "message": str(exc)[:1000]}
    receipt = {"request_id": REQUEST, "case_id": case_id, "status": status,
               "pid_worker": child.pid if child else None, "returncode": child.poll() if child else None,
               "wall_including_collection_s": time.monotonic() - began, "streams": streams,
               "detail": detail, "retry_allowed": False}
    new_result(case_dir / "SUPERVISOR_RECEIPT.json", receipt)
    return receipt

def main():
    require(sys.argv[1:] == ["--run-once"], "Only reviewed --run-once")
    require(Path(__file__).resolve() == BASE / "supervisor.py", "Fixed supervisor path")
    cp = BASE / "CONTRATO_INTEGRACAO.json"; cb = cp.read_bytes(); c = json.loads(cb)
    auth_path = BASE / "AUTORIZACAO_ROOT.json"; auth_bytes = auth_path.read_bytes(); auth = json.loads(auth_bytes)
    require(auth["authorized"] is True and auth["scope"] == c["scope"] == SCOPE, "Explicit authorization absent")
    require(auth["request_id"] == c["request_id"] == REQUEST and auth["contract_sha256"] == digest(cb), "Contract identity")
    require(type(auth["max_execution_count"]) is int and auth["max_execution_count"] == 1, "Single execution")
    require(type(auth["max_children"]) is int and auth["max_children"] == 3 and auth["max_wall_seconds"] == 30, "Limits")
    review = auth["review"]; rp = Path(review["path"]).resolve()
    require(rp.is_relative_to(BASE.parents[2]) and rp.suffix in (".md", ".json") and review["accepted_for_this_execution"] is True,
            "Pinned ROOT review required")
    require(digest(rp.read_bytes()) == review["sha256"], "Review pin")
    require(c["case_ids"] == CASE_IDS and c["limits"]["max_child_processes"] == 3, "Fixed cases")
    require(Path(sys.executable).resolve() == Path(c["interpreter"]).resolve(), "Interpreter identity")
    for pin in c["execution_pins"]:
        raw = Path(pin["path"]).read_bytes()
        require(len(raw) == pin["bytes"] and digest(raw) == pin["sha256"], "Execution pin changed")
    require(not (BASE / "CLAIM.json").exists() and not (BASE / "RUN").exists() and not (BASE / "RESULT.json").exists(), "Consumed/uncertain identity; no retry")
    total_deadline = ENTRY_MONOTONIC + 30; work_deadline = ENTRY_MONOTONIC + 24
    require(time.monotonic() < work_deadline, "Preflight consumed nominal budget")
    claim = {"request_id": REQUEST, "pid_supervisor": os.getpid(), "nonce": str(uuid.uuid4()),
             "contract_sha256": digest(cb), "authorization_sha256": digest(auth_bytes),
             "entry_monotonic": ENTRY_MONOTONIC, "total_deadline_monotonic": total_deadline,
             "scope": SCOPE, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "retry_allowed": False}
    exclusive(BASE / "CLAIM.json", claim)  # Reserved before RUN, fixture generation, or any Popen.
    results = []; status = "FAILED"; failure = None
    try:
        (BASE / "RUN").mkdir()
        for case_id in CASE_IDS:
            require(time.monotonic() < work_deadline, "No remaining work budget")
            row = run_case(case_id, c, claim, work_deadline, total_deadline)
            results.append(row)
            if row["status"] != "PASS":
                status = row["status"]; break
        else:
            status = "PASS" if time.monotonic() <= total_deadline else "FAILED"
    except BaseException as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:1000]}; status = "FAILED"
    if len(results) != 3 and status == "PASS": status = "FAILED"
    receipt = {"request_id": REQUEST, "status": status, "failure": failure,
               "case_ids_requested": CASE_IDS, "cases_completed": len(results), "cases": results,
               "wall_before_final_receipt_io_s": time.monotonic() - ENTRY_MONOTONIC,
               "nominal_total_s": 30, "work_deadline_inside_total_s": 24, "per_child_work_s": 6,
               "clock_start": "first monotonic read after import time, before remaining supervisor imports and preflight",
               "OS_hard_realtime_guarantee": False, "max_children": 3, "retry_allowed": False,
               "scientific_execution": False, "D_opened": False, "PE_authorized": False}
    # Small local receipt IO is inside the nominal design, not an OS hard guarantee.
    new_result(BASE / "RESULT.json", receipt)
    require(time.monotonic() <= total_deadline, "FINAL_RECEIPT_IO_EXCEEDED_TOTAL_DEADLINE; parent exit invalidates provisional PASS")
    return 0 if status == "PASS" else (2 if status == "PROCESS_STATE_UNCERTAIN" else 1)
if __name__ == "__main__":
    try: sys.exit(main())
    except Exception as exc:
        print(json.dumps({"request_id": REQUEST, "status": "FAILED_PREFLIGHT_OR_RECEIPT",
                          "exception": type(exc).__name__, "message": str(exc)[:1000], "retry_allowed": False}), flush=True)
        sys.exit(1)
