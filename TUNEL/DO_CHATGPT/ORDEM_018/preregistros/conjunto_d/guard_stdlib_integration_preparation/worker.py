"""Prepared stdlib integration child. No scientific imports or arbitrary case paths."""
from pathlib import Path
import sys, os, json, hashlib, types, time, errno, datetime
import copy, threading, importlib.util, importlib.machinery
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\preregistros\conjunto_d\guard_stdlib_integration_preparation")
REQUEST = "278b56a3-36e0-4adc-9708-af49f094d1df"
SCOPE = "AUDIT_GUARD_STDLIB_INTEGRATION_THREE_CHILDREN_ONLY_ONCE"

def require(ok, message):
    if not ok: raise RuntimeError(message)

def digest(raw): return hashlib.sha256(raw).hexdigest()

def read_json(path): return json.loads(path.read_bytes())

def exclusive(path, payload):
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    require(path.read_bytes() == raw, "Durable reservation readback")

def write_fd(fd, raw):
    view = memoryview(raw)
    while view:
        n = os.write(fd, view)
        require(n > 0, "Short output write")
        view = view[n:]
    os.fsync(fd)

def norm(path): return os.path.normcase(os.path.abspath(os.fsdecode(path)))

def execute_case(case_id, case_dir, guard_bytes):
    # Called only after parent identity, contract pins and durable CASE_CLAIM.
    module = types.ModuleType("qualified_audit_guard")
    module.__file__ = str(BASE / "sources" / "audit_guard.py")
    exec(compile(guard_bytes, module.__file__, "exec"), module.__dict__)
    guard = module
    journal_path = case_dir / "journal.jsonl"
    journal = guard.PreopenedJournal(str(journal_path))
    latch = guard.AuditLatch(journal)
    result_fd = os.open(case_dir / "CASE_RESULT.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    fixture = case_dir / "probe_fixture.py"
    fixture.write_bytes(b"VALUE = 42\n")
    cache_path = Path(importlib.util.cache_from_source(str(fixture)))
    cache_path.parent.mkdir()
    denied_paths = [case_dir / "blocked_a.txt", case_dir / "blocked_b.txt"]
    for p in denied_paths: p.write_bytes(b"synthetic-fixture-only\n")
    source_norm, journal_norm, cache_norm = map(norm, [fixture, journal_path, cache_path])
    blocked_norms = {norm(p) for p in denied_paths}
    expected_targets = {cache_norm} if case_id == "I02_IMPORT_CACHE_SWALLOWED" else blocked_norms
    hook_seen = []; unexpected = []; ping = [0]; callback_calls = [0]
    profile_counts = {name: {event: 0 for event in ("c_call", "c_return", "c_exception")}
                      for name in ("write", "fsync")}
    def profile(frame, event, arg):
        if event in ("c_call", "c_return", "c_exception"):
            if arg is os.write: profile_counts["write"][event] += 1
            if arg is os.fsync: profile_counts["fsync"][event] += 1
    def audit(event, args):
        if event == "iald.guard.integration.ping":
            require(args == (case_id,), "Hook ping identity"); ping[0] += 1; return
        forbidden = event.startswith(("subprocess.", "socket.", "os.spawn")) or event in (
            "os.system", "os.posix_spawn", "os.fork", "os.forkpty", "ctypes.dlopen", "ctypes.dlsym",
            "os.remove", "os.rmdir", "os.rename", "os.mkdir", "os.link", "os.symlink", "sys.addaudithook")
        target = str(args[:1])[:200]; mode = None; flags = None; expected = False
        if event == "import":
            forbidden = forbidden or args[0] != "probe_fixture"
        if event == "compile":
            forbidden = forbidden or norm(args[1]) != source_norm
        if event == "exec":
            forbidden = forbidden or norm(args[0].co_filename) != source_norm
        if event == "open":
            target, mode, flags = args
            writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (
                isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)))
            name = None if isinstance(target, int) else norm(target)
            expected = name in expected_targets and not writing
            forbidden = writing or name not in {source_norm, journal_norm}
        if forbidden:
            row = {"event": event, "target": str(target), "expected": expected}
            hook_seen.append(row)
            if not expected: unexpected.append(row)
            latch.deny(event, target, mode=mode, flags=flags,
                       reason="EXPECTED_PROBE_DENIAL" if expected else "UNEXPECTED_SCOPE_DENIAL")
    def callback():
        callback_calls[0] += 1
        return "MUST_NOT_RUN"
    def blocked_checkpoint(phase):
        try:
            latch.checkpoint(phase)
            callback()
        except guard.AuditViolation:
            return True
        return False
    if case_id == "I03_PHYSICAL_JOURNAL_FAILURE":
        os.close(journal.fd)  # Real EBADF on the next write, not a simulated writer.
    status = "FAILED"; error = None; detail = {}; snapshot = None
    try:
        latch.context("real_hook_setup", 0, 0)
        sys.setprofile(profile)  # Observer only: os.write/fsync are not replaced.
        # CPython suppresses tracing in audit hooks unless this opt-in is true.
        # Observation only: preserve the real hook, original guard and allowlist.
        audit.__cantrace__ = True
        sys.addaudithook(audit)
        latch.installed()
        sys.audit("iald.guard.integration.ping", case_id)
        require(ping[0] == 1, "Real audit hook did not observe ping")
        if case_id == "I01_REAL_HOOK_JOURNAL":
            for i, path in enumerate(denied_paths, 1):
                latch.context("physical_denial_" + str(i), 0, 0)
                try:
                    path.read_bytes()
                except PermissionError:
                    pass
                else:
                    raise AssertionError("Expected open denial was not raised")
            require(blocked_checkpoint("before_next_callback"), "Latch did not block callback")
            require(blocked_checkpoint("final"), "Final checkpoint did not remain latched")
            detail["expected_denials"] = 2
        elif case_id == "I02_IMPORT_CACHE_SWALLOWED":
            latch.context("real_cache_import", 0, 0)
            require(sys.dont_write_bytecode is True, "-B required")
            spec = importlib.util.spec_from_file_location("probe_fixture", str(fixture))
            require(isinstance(spec.loader, importlib.machinery.SourceFileLoader), "Exact source loader")
            toy = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(toy)  # CPython catches OSError when probing the .pyc.
            require(toy.VALUE == 42, "Source fallback did not finish")
            detail["import_returned_normally"] = True
            detail["cache_probe_path"] = str(cache_path)
            require(blocked_checkpoint("after_import_before_callback"), "Callback was allowed after swallowed denial")
            require(blocked_checkpoint("final"), "Final latch lost")
            detail["expected_denials"] = 1
        elif case_id == "I03_PHYSICAL_JOURNAL_FAILURE":
            latch.context("closed_journal_fd", 0, 0)
            try:
                denied_paths[0].read_bytes()
            except OSError as exc:
                detail["physical_error"] = {"type": type(exc).__name__, "errno": exc.errno}
                require(exc.errno == errno.EBADF, "Expected real bad file descriptor")
            else:
                raise AssertionError("Closed journal write did not fail")
            require(blocked_checkpoint("after_journal_error_before_callback"), "Journal failure lost latch")
            require(blocked_checkpoint("final"), "Final latch lost")
            detail["expected_denials"] = 1
        else:
            raise RuntimeError("Unknown exact case")
        snapshot = latch.snapshot()
        require(snapshot["installed"] and snapshot["latched"], "Expected latched hook state")
        require(snapshot["denial_count"] == detail["expected_denials"], "Denial count")
        require(snapshot["first_event"] == snapshot["events"][0], "First event overwritten")
        require([x["sequence"] for x in snapshot["events"]] == list(range(1, detail["expected_denials"] + 1)), "Sequence")
        require(callback_calls[0] == 0 and not unexpected, "Unexpected callback or operation")
        require(len(hook_seen) == detail["expected_denials"] and all(x["expected"] for x in hook_seen), "Hook identity")
        if case_id == "I03_PHYSICAL_JOURNAL_FAILURE":
            require(snapshot["journal_error"] is not None and profile_counts["write"]["c_exception"] == 1,
                    "Real journal error not retained")
            require(profile_counts["fsync"]["c_call"] == 0, "Unexpected fsync after failed write")
        else:
            require(snapshot["journal_error"] is None, "Unexpected physical journal failure")
            require(profile_counts["write"]["c_return"] >= detail["expected_denials"], "No real write return")
            require(profile_counts["fsync"]["c_return"] == detail["expected_denials"], "Real fsync count")
        status = "PASS_EXPECTED_LATCHED"
    except BaseException as exc:
        error = {"type": type(exc).__name__, "message": str(exc)[:2000]}
    finally:
        sys.setprofile(None)
    if snapshot is None: snapshot = latch.snapshot()
    raw_journal = journal_path.read_bytes()
    rows = [json.loads(line) for line in raw_journal.splitlines()]
    expected_rows = [] if case_id == "I03_PHYSICAL_JOURNAL_FAILURE" else snapshot["events"]
    if rows != expected_rows:
        status = "FAILED"; error = {"type": "JournalReadbackMismatch", "message": "Physical rows differ from retained events"}
    payload = {"request_id": REQUEST, "case_id": case_id, "pid": os.getpid(), "parent_pid": os.getppid(),
               "status": status, "error": error, "detail": detail, "callback_calls": callback_calls[0],
               "hook_seen": hook_seen, "unexpected_operations": unexpected, "audit_snapshot": snapshot,
               "profile_real_os_calls": profile_counts, "journal": {"path": str(journal_path),
               "bytes": len(raw_journal), "sha256": digest(raw_journal), "rows": len(rows)},
               "source_loader_runtime": {"module": importlib.machinery.SourceFileLoader.__module__,
               "get_code_filename": importlib.machinery.SourceFileLoader.get_code.__code__.co_filename},
               "scientific_imports": 0, "scientific_calls": 0, "new_children": 0,
               "retry_allowed": False, "OS_isolation_claim": False}
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode()
    write_fd(result_fd, raw); os.close(result_fd)
    print(raw.decode(), end="", flush=True)
    return 0 if status == "PASS_EXPECTED_LATCHED" else 1

def main():
    require(sys.argv[1:] == ["--supervised-stdin"], "Supervised stdin only")
    require(Path(__file__).resolve() == BASE / "worker.py", "Fixed worker identity")
    cp = BASE / "CONTRATO_INTEGRACAO.json"; cb = cp.read_bytes(); c = json.loads(cb)
    token = json.loads(sys.stdin.buffer.readline(4097))
    claim = read_json(BASE / "CLAIM.json"); auth = read_json(BASE / "AUTORIZACAO_ROOT.json")
    require(c["request_id"] == claim["request_id"] == token["request_id"] == auth["request_id"] == REQUEST, "Request")
    require(token["nonce"] == claim["nonce"] and os.getppid() == claim["pid_supervisor"], "Parent/nonce")
    require(auth["authorized"] is True and auth["scope"] == c["scope"] == SCOPE, "Explicit authorization absent")
    require(claim["contract_sha256"] == auth["contract_sha256"] == digest(cb), "Contract pin")
    require(claim["authorization_sha256"] == digest((BASE / "AUTORIZACAO_ROOT.json").read_bytes()), "Authorization changed")
    require(type(auth["max_children"]) is int and auth["max_children"] == 3 and auth["max_wall_seconds"] == 30, "Limits")
    require(Path(sys.executable).resolve() == Path(c["interpreter"]).resolve(), "Interpreter")
    case = token["case_id"]; require(case in c["case_ids"], "Case allowlist")
    case_dir = BASE / "RUN" / case
    dispatch = read_json(case_dir / "DISPATCH.json")
    require(dispatch["case_id"] == case and dispatch["nonce"] == token["case_nonce"] and dispatch["request_id"] == REQUEST, "Dispatch identity")
    cache = {}
    for pin in c["execution_pins"]:
        raw = Path(pin["path"]).read_bytes()
        require(len(raw) == pin["bytes"] and digest(raw) == pin["sha256"], "Pin mismatch")
        cache[pin["path"]] = raw
    exclusive(case_dir / "CASE_CLAIM.json", {"request_id": REQUEST, "case_id": case, "pid": os.getpid(),
              "parent_pid": os.getppid(), "contract_sha256": digest(cb), "nonce": token["case_nonce"],
              "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "retry_allowed": False})
    return execute_case(case, case_dir, cache[str(BASE / "sources" / "audit_guard.py")])
if __name__ == "__main__":
    try: sys.exit(main())
    except Exception as exc:
        print(json.dumps({"request_id": REQUEST, "status": "FAILED", "exception": type(exc).__name__,
                          "message": str(exc)[:2000], "retry_allowed": False}), flush=True)
        sys.exit(1)
