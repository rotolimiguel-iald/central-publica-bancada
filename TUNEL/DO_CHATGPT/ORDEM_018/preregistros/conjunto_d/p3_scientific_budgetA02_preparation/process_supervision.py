"""Cooperative cancellation and bounded cleanup of one owned child.

Pure stdlib, injectable process doubles. No child is created at import time.
Nominal deadlines cannot contain blocking OS calls, SIGKILL, or host loss.
"""
import subprocess


class SupervisorCancelled(Exception):
    """Raised synchronously outside owned-child cleanup, never by a handler."""


class Cancellation:
    def __init__(self):
        self.requested = False
        self.signal_number = None

    def request(self, signum):
        # A handler only records state; it never raises, does IO, or changes masks.
        self.requested = True
        self.signal_number = signum


def supervise(spawn, *, wait_deadline, cleanup_deadline, clock,
              kill_owned_group, cancellation, wait_quantum=0.25):
    """Spawn at most once; retain ownership through every controllable exit.

    SIGINT/SIGTERM must use the caller's non-raising recorder throughout.
    Sending SIGKILL is not evidence of termination: a successful wait/poll is
    required. Errors, cancellation, and late cleanup always refuse acceptance.
    """
    proc = None
    rc = None
    state = "SPAWN_NOT_COMPLETED"
    errors = []
    spawn_attempted = False
    cleanup_attempted = False
    try:
        if type(wait_quantum) not in (int, float) or not 0 < wait_quantum <= 1:
            raise ValueError("Finite wait quantum in (0, 1] required")
        if cancellation.requested:
            raise SupervisorCancelled("Cancellation before spawn")
        if clock() >= wait_deadline:
            raise subprocess.TimeoutExpired("before spawn", 0)
        # Cancellation during spawn only sets a flag. The returned handle is
        # assigned before that flag is interpreted; there is no mask inheritance.
        spawn_attempted = True
        proc = spawn()
        while True:
            if cancellation.requested:
                raise SupervisorCancelled("Cancellation after spawn or during wait")
            remaining = wait_deadline - clock()
            if remaining <= 0:
                raise subprocess.TimeoutExpired("owned child", 0)
            try:
                rc = proc.wait(timeout=min(wait_quantum, remaining))
            except subprocess.TimeoutExpired:
                continue
            if type(rc) is not int:
                raise TypeError("Owned child returned a non-integer exit status")
            state = "PROCESS_RETURNED"
            break
    except SupervisorCancelled as exc:
        state = "SUPERVISOR_CANCELLED"
        errors.append(str(exc))
    except subprocess.TimeoutExpired as exc:
        state = "SUPERVISOR_TIMEOUT"
        errors.append(type(exc).__name__ + ": " + str(exc))
    except BaseException as exc:
        state = "SUPERVISOR_INTERRUPTED_OR_ERROR"
        errors.append(type(exc).__name__ + ": " + str(exc))
    finally:
        if proc is not None:
            # No context-manager entry or handler transition can escape here.
            # Recorder remains active during poll, kill and bounded reaping.
            try:
                observed = proc.poll()
                if observed is None:
                    cleanup_attempted = True
                    kill_owned_group(proc.pid)
                elif type(observed) is int:
                    rc = observed
                else:
                    raise TypeError("Owned child poll returned a non-integer status")
            except BaseException as exc:
                errors.append("KILL_OR_POLL:" + type(exc).__name__ + ": " + str(exc))
            try:
                while True:
                    remaining = cleanup_deadline - clock()
                    if remaining <= 0:
                        rc = proc.poll()
                        errors.append("CLEANUP_DEADLINE_EXHAUSTED")
                        break
                    try:
                        rc = proc.wait(timeout=min(wait_quantum, remaining))
                        if type(rc) is not int:
                            raise TypeError("Reap returned a non-integer exit status")
                        break
                    except subprocess.TimeoutExpired:
                        continue
            except BaseException as exc:
                rc = None
                errors.append("REAP:" + type(exc).__name__ + ": " + str(exc))
    # Includes a cancellation recorded during cleanup, even if exit status is 0.
    if cancellation.requested:
        state = "SUPERVISOR_CANCELLED"
        errors.append("CANCEL_REQUESTED")
    certain = proc is not None and type(rc) is int
    within = clock() < cleanup_deadline
    if not within:
        errors.append("CLEANUP_OR_RETURN_LATE")
    return {
        "pid": None if proc is None else proc.pid,
        "returncode": rc,
        "supervisor_status": state,
        "spawn_attempted": spawn_attempted,
        "no_child_started": proc is None and not spawn_attempted,
        "spawn_result_uncertain": proc is None and spawn_attempted,
        "termination_certain": certain,
        "within_cleanup_deadline": within,
        "cleanup_attempted": cleanup_attempted,
        "cancellation_requested": cancellation.requested,
        "cancellation_signal": cancellation.signal_number,
        "supervision_errors": errors,
        "process_accepted": certain and within and not errors
                            and state == "PROCESS_RETURNED" and rc == 0,
    }
