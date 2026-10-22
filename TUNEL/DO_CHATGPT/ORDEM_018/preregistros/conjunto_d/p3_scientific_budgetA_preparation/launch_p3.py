"""Prepared A supervisor; no consumption without the exact external decision."""
import sys, os, json, hashlib, subprocess, time, signal, contextlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from result_acceptance import assess, campaign_exit, paired_numerical
from process_supervision import supervise, SupervisorInterrupted


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fresh(path, raw):
    if path.exists():
        raise FileExistsError(str(path))
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    if temp.read_bytes() != raw:
        raise OSError("Atomic verification failed")
    os.replace(temp, path)
    if path.read_bytes() != raw:
        raise OSError("Final byte verification failed")


def js(path, obj):
    fresh(path, (json.dumps(obj, indent=2, allow_nan=False) + "\n").encode())


def check_deadline(deadline):
    if time.perf_counter() >= deadline:
        raise TimeoutError("NOMINAL_DEADLINE_INCLUDING_FINALIZATION_EXCEEDED")


@contextlib.contextmanager
def ownership_context():
    previous = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM})
    try:
        yield
    finally:
        # Pending interruption arrives after supervise owns the returned handle.
        signal.pthread_sigmask(signal.SIG_SETMASK, previous)


@contextlib.contextmanager
def cleanup_context():
    old = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        for s in old:
            signal.signal(s, signal.SIG_IGN)
        yield
    finally:
        for s, handler in old.items():
            signal.signal(s, handler)


def main():
    t0 = time.perf_counter()
    run = None
    def interrupted(sig, frame):
        raise SupervisorInterrupted("SIGNAL_" + str(sig))
    old = {s: signal.signal(s, interrupted) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        if len(sys.argv) != 3:
            raise ValueError("Exact contract and external decision hashes required")
        pin, decision_pin = sys.argv[1:]
        from science_admission import admit
        c, authorization = admit(ROOT, pin, decision_pin)
        campaign_deadline = t0 + c["limits"]["supervisor_wall_s"] * len(c["jobs"])
        fd = os.open(ROOT / "CAMPAIGN_CLAIM.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write((json.dumps({"contract_sha256": pin, "decision_sha256": decision_pin,
                                "preparation_id": c["preparation_id"],
                                "execution_id": authorization["execution_id"],
                                "pid": os.getpid()}) + "\n").encode())
            f.flush()
            os.fsync(f.fileno())
        run = ROOT / c["execution_directory"]
        run.mkdir(exist_ok=False)
        js(run / "LAUNCH_STARTED.json",
           {"contract_sha256": pin, "decision_sha256": decision_pin,
            "preparation_id": c["preparation_id"], "execution_id": authorization["execution_id"],
            "at": datetime.now(timezone.utc).isoformat(), "pid": os.getpid()})
        env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
                   MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
        results, assessments = [], []
        for job in c["jobs"]:
            start = time.perf_counter()
            total_deadline = min(start + c["limits"]["supervisor_wall_s"], campaign_deadline)
            # 14400 work; 5 child-finalization grace; 4 kill/reap; 1 receipt reserve.
            wait_deadline = min(start + c["limits"]["wall_soft_s"] + 5, total_deadline - 5)
            cleanup_deadline = total_deadline - 1
            check_deadline(wait_deadline)
            out = run / job["id"]
            out.mkdir(exist_ok=False)
            js(out / "CLAIM.json", {"contract_sha256": pin, "decision_sha256": decision_pin,
                                   "execution_id": authorization["execution_id"],
                                   "job_id": job["id"], "supervisor_pid": os.getpid()})
            cmd = ["/opt/lal_env/bin/python", "-I", "-B", str(ROOT / "driver_p3.py"),
                   pin, job["id"], decision_pin]
            with (out / "stdout.log").open("xb") as fo, (out / "stderr.log").open("xb") as fe:
                def spawn():
                    return subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=fo, stderr=fe,
                                            env=env, cwd=str(ROOT), start_new_session=True)
                row = supervise(spawn, wait_deadline=wait_deadline,
                                cleanup_deadline=cleanup_deadline, clock=time.perf_counter,
                                kill_owned_group=lambda pid: os.killpg(pid, signal.SIGKILL),
                                cleanup_context=cleanup_context, ownership_context=ownership_context)
            row.update(job_id=job["id"], wall_s=time.perf_counter() - start,
                       stdout_sha256=sha(out / "stdout.log"), stderr_sha256=sha(out / "stderr.log"))
            result, journal = None, None
            try:
                rp, jp = out / "RESULT.json", out / "AUDIT_EVENTS.jsonl"
                if rp.exists():
                    raw = rp.read_bytes()
                    result = json.loads(raw)
                    row.update(result_sha256=hashlib.sha256(raw).hexdigest(),
                               result_status=result.get("status"))
                if jp.exists():
                    journal = jp.read_bytes()
                    row.update(audit_journal_sha256=hashlib.sha256(journal).hexdigest(),
                               audit_journal_bytes=len(journal))
                decision = assess(result, journal, returncode=row["returncode"],
                    process_state=row["supervisor_status"], expected_job=job["id"],
                    expected_label=job["label"], expected_contract=pin,
                    expected_pid=row["pid"], max_calls=c["limits"]["max_likelihood_calls"],
                    expected_preparation=c["preparation_id"],
                    expected_execution=authorization["execution_id"],
                    expected_decision=decision_pin,
                    max_native=c["limits"]["native_waveform_calls_at_most"],
                    dlogz=c["numeric_thresholds"]["dlogz"],
                    ess_min=c["numeric_thresholds"]["weighted_ESS_min"])
                if row["process_accepted"] is not True:
                    decision = {"accepted": False, "disposition": "TERMINAL_FAILURE",
                                "numerical_criteria_met": False,
                                "reasons": ["SUPERVISION_OR_TERMINATION_UNCERTAIN"]}
            except Exception as exc:
                decision = {"accepted": False, "disposition": "TERMINAL_FAILURE",
                            "numerical_criteria_met": False,
                            "reasons": ["RECEIPT_READ_OR_VALIDATION_ERROR"],
                            "error": type(exc).__name__ + ": " + str(exc)}
            row["acceptance"] = decision
            check_deadline(total_deadline)
            assessments.append(decision)
            results.append(row)
            js(out / "PROCESS_RECEIPT.json", row)
            # A receipt written just before a slow IO overrun is provisional.
            check_deadline(total_deadline)
            if decision["accepted"] is not True:
                break
        code = campaign_exit(assessments, len(c["jobs"]))
        terminal = {"contract_sha256": pin, "jobs": results, "wall_s": time.perf_counter() - t0,
                    "started_jobs": len(results), "planned_jobs": len(c["jobs"]),
                    "no_retry": True, "exit_code_provisional": code,
                    "status": "CLEAN_PROTOCOL_COMPLETION" if code == 0 else "TERMINAL_FAILURE_OR_INCOMPLETE",
                    "paired_numerical_criteria_met": paired_numerical(assessments),
                    "scientific_qualification": False, "coverage_claim": False,
                    "D_read_authorized": False, "preparation_id": c["preparation_id"],
                    "execution_id": authorization["execution_id"], "decision_sha256": decision_pin,
                    "acceptance_requires": "External exit 0, exact receipt pins and no FINALIZATION_FAILURE.json"}
        check_deadline(campaign_deadline)
        js(run / "CAMPAIGN_RECEIPT.json", terminal)
        receipt_pin = sha(run / "CAMPAIGN_RECEIPT.json")
        check_deadline(campaign_deadline)
        print(json.dumps({"status": terminal["status"], "receipt_sha256": receipt_pin,
                          "scientific_qualification": False}), flush=True)
        check_deadline(campaign_deadline)
        return code
    except BaseException as exc:
        # Never change a prior provisional success into silent success after failure.
        if run is not None:
            try:
                js(run / "FINALIZATION_FAILURE.json",
                   {"status": "TERMINAL_FAILURE_NO_RETRY", "type": type(exc).__name__,
                    "message": str(exc), "wall_s": time.perf_counter() - t0})
            except BaseException:
                pass  # Missing failure receipt is not acceptance; external exit stays nonzero.
        return 2
    finally:
        for s, handler in old.items():
            signal.signal(s, handler)


if __name__ == "__main__":
    sys.exit(main())
