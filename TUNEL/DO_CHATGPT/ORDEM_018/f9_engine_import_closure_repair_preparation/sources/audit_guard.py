"""Sticky Python audit state. Pure standard library; cooperative, not OS isolation."""
import copy
import json
import os
import threading
import time

class AuditViolation(RuntimeError):
    pass

class PreopenedJournal:
    """Open exclusively before hook installation. No path opens in the hook."""
    def __init__(self, path):
        self.fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)

    def __call__(self, raw):
        view = memoryview(raw)
        while view:
            n = os.write(self.fd, view)
            if n <= 0:
                raise OSError("Audit journal short write")
            view = view[n:]
        os.fsync(self.fd)

    # Intentionally held open until process exit. No reset/truncate API.

class AuditLatch:
    def __init__(self, writer):
        self._writer = writer
        self._lock = threading.RLock()
        self._latched = False
        self._events = []
        self._first = None
        self._journal_error = None
        self._denial_count = 0
        self._phase = "setup"
        self._ll = 0
        self._native = 0
        self._checkpoints = {}
        self._installed = False
        self._interrupted_exceptions = []

    def installed(self):
        self._installed = True

    def context(self, phase, likelihood_calls, native_calls):
        with self._lock:
            self._phase = str(phase)
            self._ll = int(likelihood_calls)
            self._native = int(native_calls)

    def refresh_counts(self, likelihood_calls, native_calls):
        with self._lock:
            self._ll = int(likelihood_calls)
            self._native = int(native_calls)

    def deny(self, event, target, *, mode=None, flags=None, reason):
        with self._lock:
            # Persist the failure in memory BEFORE serialization or journal IO.
            self._latched = True
            self._denial_count += 1
            row = {"sequence": self._denial_count, "event": str(event),
                   "target": str(target), "mode": mode, "flags": flags,
                   "reason": str(reason), "phase": self._phase,
                   "likelihood_calls_at_event": self._ll,
                   "native_attempts_completed_at_event": self._native,
                   "monotonic_ns": time.monotonic_ns(), "unix_time_ns": time.time_ns()}
            self._events.append(row)
            if self._first is None:
                self._first = row
            try:
                self._writer((json.dumps(row, allow_nan=False, sort_keys=True)+"\n").encode())
            except BaseException as exc:
                # Only to retain IO failure evidence and re-raise it; never success.
                self._journal_error = {"type": type(exc).__name__, "message": str(exc)}
                raise
        raise PermissionError(reason)

    def checkpoint(self, phase, cause=None):
        with self._lock:
            self._phase = str(phase)
            self._checkpoints[phase] = self._checkpoints.get(phase, 0) + 1
            if self._latched or self._journal_error is not None:
                if cause is not None:
                    self._interrupted_exceptions.append({
                        "type": type(cause).__name__, "message": str(cause)})
                raise AuditViolation("Sticky audit failure at " + str(phase))

    def evaluate(self, call):
        """Counts are managed by the caller; catches no BaseException as success."""
        self.checkpoint("pre_likelihood_evaluation")
        try:
            value = call()
        except BaseException as exc:
            self.checkpoint("post_likelihood", cause=exc)
            raise
        self.checkpoint("post_likelihood")
        return value

    def snapshot(self):
        with self._lock:
            return copy.deepcopy({"schema": "AUDIT_LATCH_V1", "installed": self._installed,
                "latched": self._latched, "denial_count": self._denial_count,
                "first_event": self._first, "events": self._events,
                "journal_error": self._journal_error, "checkpoint_counts": self._checkpoints,
                "interrupted_exceptions": self._interrupted_exceptions})
