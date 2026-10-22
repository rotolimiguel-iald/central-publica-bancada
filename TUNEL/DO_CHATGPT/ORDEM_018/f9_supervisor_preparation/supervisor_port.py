"""Mandatory external supervisory boundary, deliberately unimplemented.

No bool/flag grants execution. A future pinned reviewed implementation must
perform the documented checks and raise on failure. This is not an OS sandbox.
"""
from abc import ABC, abstractmethod

class QualifiedSupervisor(ABC):
    @abstractmethod
    def admit(self, *, request_json, decision_json, guard_contract_json,
              resources_json, runtime_inventory_json, artifacts, bindings):
        """Verify real ROOT authority, scope, runtime/loaded code, inputs and FS.

        Validate the actual process supervisor/watchdog, single science thread,
        BLAS/CAMB thread settings, read allowlist, native mappings, audit latch,
        descriptor ownership, no network and exact pinned runtime/metadata.
        For observations verify operator release and frozen V1, not a flag.
        Install/verify real enforcement before returning None. No default.
        """
        raise NotImplementedError('QUALIFIED_SUPERVISOR_NOT_IMPLEMENTED')

    @abstractmethod
    def checkpoint(self, phase, context):
        """Enforce bound deadlines/limits and latched audit; None or raise.

        Native calls may not return: independent process supervision is required.
        Persisted run claim must survive termination. Do not retry child/process.
        """
        raise NotImplementedError('QUALIFIED_SUPERVISOR_NOT_IMPLEMENTED')

    @abstractmethod
    def process_identity(self):
        """Return verified live POSIX {pid,start_ticks}, bound to supervisor."""
        raise NotImplementedError('PROCESS_IDENTITY_NOT_IMPLEMENTED')

    @abstractmethod
    def terminal_audit(self, *, context):
        """Return original bytes of audited terminal receipt, not inferred success.

        Required: schema F9_CONTROLLER_SUPERVISOR_TERMINAL_V1, execution_unit_id,
        status AUDIT_ACCEPTED, latched false, observed_reads matching request,
        unexpected_reads zero, network_operations zero, runtime_sha256,
        execution_decision_sha256, new_solver_attempts/returns equal counters,
        supervisor_reference, and actual resource measurements or explicit null.
        External exit/cleanup acceptance remains caller responsibility.
        """
        raise NotImplementedError('TERMINAL_AUDIT_NOT_IMPLEMENTED')
