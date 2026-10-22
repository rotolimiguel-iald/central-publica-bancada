"""Pure finalization coordinator with injected I/O and clock operations.

A provisional persisted receipt is never sufficient for acceptance. The caller
must observe supervisor exit0 after the final post-output clock check. On any
late I/O/failure the coordinator returns nonzero and attempts a separate
invalidation receipt. No operation after a successful final check is performed
here except returning the integer exit status.
"""
import math


def finalize_unit(receipt, controls_status, deadline, clock,
                  persist, read_digest, emit, invalidate):
    candidate = dict(receipt)
    candidate["status"] = (
        "PENDING_FINAL_DEADLINE_CHECK" if controls_status == "PASS" else controls_status)
    candidate["controls_status"] = controls_status
    candidate["acceptance_rule"] = (
        "Acceptance requires external supervisor exit0, this pinned provisional "
        "receipt with controls_status PASS, and no FINALIZATION_FAILURE.json. "
        "A provisional receipt or stdout message alone is never terminal PASS.")
    candidate["supervisor_exit_required"] = 0
    candidate_sha = None

    def failure(reason, observed=None, exception=None):
        record = {
            "request_id": candidate.get("request_id"),
            "status": reason,
            "invalidates_provisional_receipt_sha256": candidate_sha,
            "provisional_receipt_is_accepted": False,
            "controls_status": controls_status,
            "supervisor_exit_will_be_nonzero": True,
            "observed_monotonic": observed,
            "nominal_deadline_monotonic": deadline,
            "observed_wall_seconds": (
                observed - candidate["execution_started_monotonic"]
                if observed is not None and candidate.get("execution_started_monotonic") is not None
                else None),
            "exception": exception,
            "retry_allowed": False,
        }
        persistence_error = None
        try:
            invalidate(record)
        except Exception as error:
            persistence_error = type(error).__name__ + ":" + str(error)[:1000]
        report = dict(record)
        report["invalidation_persistence_error"] = persistence_error
        try:
            emit(report)
        except Exception:
            pass
        # Failure reporting may also block or fail. Never return0 afterward.
        return 1 if persistence_error is None else 4

    def timestamp():
        value = clock()
        if type(value) not in (int, float) or not math.isfinite(value):
            raise RuntimeError("FINALIZATION_CLOCK_INVALID")
        return value

    try:
        if type(deadline) not in (int, float) or not math.isfinite(deadline):
            raise RuntimeError("FINALIZATION_DEADLINE_INVALID")
        persist(candidate)
        candidate_sha = read_digest()
        if (type(candidate_sha) is not str or len(candidate_sha) != 64 or
                any(c not in "0123456789abcdef" for c in candidate_sha)):
            raise RuntimeError("PROVISIONAL_RECEIPT_DIGEST_INVALID")
        after_persistence = timestamp()
        if after_persistence >= deadline:
            return failure("FAILED_NOMINAL_TOTAL_LIMIT_AFTER_PERSISTENCE", after_persistence)
        report = {
            "request_id": candidate.get("request_id"),
            "status": candidate["status"],
            "provisional_receipt_sha256": candidate_sha,
            "controls_status": controls_status,
            "observed_wall_through_persistence_seconds": (
                after_persistence - candidate["execution_started_monotonic"]
                if candidate.get("execution_started_monotonic") is not None else None),
            "external_supervisor_exit0_required": True,
            "message_is_not_terminal_acceptance": True,
        }
        # The real emit must perform its flush before returning.
        emit(report)
        after_output = timestamp()
        if after_output >= deadline:
            return failure("FAILED_NOMINAL_TOTAL_LIMIT_AFTER_OUTPUT", after_output)
        if controls_status != "PASS":
            return 1
        # No further persistence, output, hash or callback on this successful path.
        return 0
    except Exception as error:
        return failure("FINALIZATION_FAILED_NOT_ACCEPTED", exception={
            "type": type(error).__name__, "message": str(error)[:2000]})
