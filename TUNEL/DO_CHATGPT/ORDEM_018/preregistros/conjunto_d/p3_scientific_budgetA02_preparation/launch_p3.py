"""Prepared A02 cooperative supervisor; no consumption without the exact external decision."""
import sys, os, json, hashlib, subprocess, time, signal
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from result_acceptance import assess, campaign_exit, paired_numerical
from process_supervision import supervise, Cancellation, SupervisorCancelled


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


def check_deadline(deadline, cancellation):
    if cancellation.requested:
        raise SupervisorCancelled("CANCELLATION_RECORDED_NO_RETRY")
    if time.perf_counter() >= deadline:
        raise TimeoutError("NOMINAL_DEADLINE_INCLUDING_FINALIZATION_EXCEEDED")


def main():
    t0 = time.perf_counter()
    run = None
    cancellation = Cancellation()
    exit_code = 2
    old = {}
    def interrupted(sig, frame):
        cancellation.request(sig)
    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            old[sig] = signal.signal(sig, interrupted)
        # Query only: do not block/unblock anything in parent or child.
        inherited_mask = signal.pthread_sigmask(signal.SIG_BLOCK, set())
        if inherited_mask.intersection({signal.SIGINT, signal.SIGTERM}):
            raise RuntimeError("Preblocked cancellation signals require explicit review")
        if cancellation.requested:
            raise SupervisorCancelled("CANCELLATION_BEFORE_ADMISSION")
        if len(sys.argv) != 3:
            raise ValueError("Exact contract and external decision hashes required")
        pin, decision_pin = sys.argv[1:]
        from science_admission import admit
        c, authorization = admit(ROOT, pin, decision_pin)
        campaign_deadline = t0 + c["limits"]["supervisor_wall_s"] * len(c["jobs"])
        check_deadline(campaign_deadline, cancellation)
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
            check_deadline(wait_deadline, cancellation)
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
                                cancellation=cancellation, wait_quantum=0.25)
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
            # Record a cancellation receipt when possible. No cancelled row can
            # become success or advance to the second case.
            if time.perf_counter() >= total_deadline:
                raise TimeoutError("CASE_FINALIZATION_DEADLINE_EXCEEDED")
            assessments.append(decision)
            results.append(row)
            js(out / "PROCESS_RECEIPT.json", row)
            # A receipt written just before a slow IO overrun is provisional.
            check_deadline(total_deadline, cancellation)
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
        check_deadline(campaign_deadline, cancellation)
        js(run / "CAMPAIGN_RECEIPT.json", terminal)
        receipt_pin = sha(run / "CAMPAIGN_RECEIPT.json")
        check_deadline(campaign_deadline, cancellation)
        print(json.dumps({"status": terminal["status"], "receipt_sha256": receipt_pin,
                          "scientific_qualification": False}), flush=True)
        check_deadline(campaign_deadline, cancellation)
        exit_code = code
    except BaseException as exc:
        # Never change a prior provisional success into silent success after failure.
        if run is not None:
            try:
                js(run / "FINALIZATION_FAILURE.json",
                   {"status": "TERMINAL_FAILURE_NO_RETRY", "type": type(exc).__name__,
                    "message": str(exc), "wall_s": time.perf_counter() - t0,
                    "cancellation_requested": cancellation.requested,
                    "cancellation_signal": cancellation.signal_number})
            except BaseException:
                pass  # Missing failure receipt is not acceptance; external exit stays nonzero.
        exit_code = 2
    finally:
        for s, handler in old.items():
            signal.signal(s, handler)
    # Restoring handlers is also finalization: a delayed restoration cannot
    # preserve provisional exit 0. Nonzero external exit invalidates the receipt.
    if exit_code == 0 and time.perf_counter() >= campaign_deadline:
        exit_code = 2
    # Cancellation during receipt/handler finalization cannot retain exit 0.
    return 2 if cancellation.requested else exit_code


if __name__ == "__main__":
    sys.exit(main())
