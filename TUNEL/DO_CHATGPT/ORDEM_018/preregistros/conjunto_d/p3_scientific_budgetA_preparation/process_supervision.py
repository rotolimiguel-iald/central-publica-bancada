"""Bounded wait/cleanup using injected process doubles or owned child handles."""
import subprocess


class SupervisorInterrupted(BaseException):
    pass


def supervise(spawn, *, wait_deadline, cleanup_deadline, clock, kill_owned_group,
              cleanup_context, ownership_context):
    """No retry. Only the child returned by spawn may be signalled/reaped.

    Deadlines are nominal. SIGKILL/host failure cannot run Python cleanup.
    No successful return is inferred from a label or from sending a signal.
    """
    proc = None
    rc = None
    state = "SPAWN_NOT_COMPLETED"
    errors = []
    cleanup_attempted = False
    try:
        if clock() >= wait_deadline:
            raise TimeoutError("No work interval remains before spawn")
        # Defer SIGINT/SIGTERM until the owned handle is assigned.
        with ownership_context():
            proc = spawn()
        remaining = wait_deadline - clock()
        if remaining <= 0:
            raise subprocess.TimeoutExpired("owned child", 0)
        rc = proc.wait(timeout=remaining)
        state = "PROCESS_RETURNED"
    except subprocess.TimeoutExpired as exc:
        state = "SUPERVISOR_TIMEOUT"
        errors.append(type(exc).__name__ + ": " + str(exc))
    except BaseException as exc:
        state = "SUPERVISOR_INTERRUPTED_OR_ERROR"
        errors.append(type(exc).__name__ + ": " + str(exc))
    finally:
        if proc is not None:
            # Temporarily defer controllable interruptions only during cleanup.
            # The caller keeps the failure state and returns nonzero afterward.
            with cleanup_context():
                try:
                    observed = proc.poll()
                    if observed is None:
                        cleanup_attempted = True
                        kill_owned_group(proc.pid)
                    else:
                        rc = observed
                except BaseException as exc:
                    errors.append("KILL_OR_POLL:" + type(exc).__name__ + ": " + str(exc))
                try:
                    remaining = cleanup_deadline - clock()
                    if remaining > 0:
                        rc = proc.wait(timeout=remaining)
                    else:
                        rc = proc.poll()
                        errors.append("CLEANUP_DEADLINE_EXHAUSTED")
                except BaseException as exc:
                    rc = None
                    errors.append("REAP:" + type(exc).__name__ + ": " + str(exc))
    certain = proc is not None and type(rc) is int
    within = clock() < cleanup_deadline
    if not within:
        errors.append("CLEANUP_OR_RETURN_LATE")
    return {"pid": None if proc is None else proc.pid,
            "returncode": rc, "supervisor_status": state,
            "termination_certain": certain, "within_cleanup_deadline": within,
            "cleanup_attempted": cleanup_attempted, "supervision_errors": errors,
            "process_accepted": certain and within and not errors
                                and state == "PROCESS_RETURNED" and rc == 0}
