"""Proposed successor port. Scoped cooperative audit, never universal native IO.

Not installed in 39f88. Applying the accompanying diff requires a fresh complete
preparation/manifest, independent review and a future explicit execution decision.
"""
from abc import ABC, abstractmethod
from posix_protocol import canonical, digest, document, exact, need

EVIDENCE_SCOPE='PYTHON_AUDIT_EVENTS_COOPERATIVE_ONLY'
AUDITED_OPERATIONS=('python_open','python_socket_events','python_subprocess_fork_events',
    'python_filesystem_mutation_events','python_dynamic_load_events')
KNOWN_GAPS=('native_syscalls_not_intercepted','same_uid_hostile_mutation_not_isolated',
    'audit_hook_is_cooperative_not_OS_sandbox','parent_requires_external_exit_cleanup_check')

class QualifiedSupervisor(ABC):
    @abstractmethod
    def admit(self, *, request_json, decision_json, guard_contract_json,
              resources_json, runtime_inventory_json, artifacts, bindings):
        """Validate actual pinned trusted runtime, loaded objects and synthetic inputs.

        Verify ROOT decision bytes against pins provided by trusted caller, the
        prior independent review, protected stable root, exact store operations,
        one real external watchdog and scoped audit latch. No bool-alone release.
        Reject observations, unknown source/modules/maps or missing capabilities.
        Runtime/native trust is explicit; no universal syscall detection claim.
        """
        raise NotImplementedError('REVIEWED_COOPERATIVE_SCIENCE_BOOTSTRAP_REQUIRED')

    @abstractmethod
    def checkpoint(self, phase, context):
        """Bound identity, unit, monotonic deadlines, counters and sticky latch."""
        raise NotImplementedError('REVIEWED_COOPERATIVE_CHECKPOINT_REQUIRED')

    @abstractmethod
    def process_identity(self):
        """Verified live POSIX pid/start_ticks, bound to actual parent watchdog."""
        raise NotImplementedError('PROCESS_IDENTITY_REQUIRED')

    @abstractmethod
    def terminal_audit(self, *, context):
        """Return scoped receipt accepted by validate_terminal; never native zero."""
        raise NotImplementedError('SCOPED_RECEIPT_REQUIRED')


def validate_terminal(raw, *, execution_unit_id, request_sha256,
        decision_sha256, runtime_sha256, supervisor_pin, new_solver_attempts,
        new_solver_returns):
    """Pure strict validator for the proposed successor terminal bytes.

    Passing this parser is not independent execution proof. External parent must
    bind nonce, child identity, physical journal, result pin, exit and cleanup.
    """
    row=document(raw)
    exact(row,('schema','execution_unit_id','request_sha256','execution_decision_sha256',
        'runtime_sha256','status','evidence_scope','audited_operations','known_gaps',
        'observed_reads','latched','python_unexpected_read_denials','python_network_denials',
        'native_network_operations','native_file_operations','native_IO_isolation',
        'audit_journal_reference','supervisor_reference','watchdog_reference','nonce',
        'process_identity','resource_measurements','new_solver_attempts','new_solver_returns',
        'external_exit_cleanup_verified'))
    need(row['schema']=='F9_CONTROLLER_COOPERATIVE_TERMINAL_V1' and
         row['status']=='PYTHON_AUDIT_ACCEPTED_SCOPED' and
         row['evidence_scope']==EVIDENCE_SCOPE,'SCOPED_TERMINAL_SCHEMA')
    need(row['execution_unit_id']==execution_unit_id and row['request_sha256']==digest(request_sha256)
         and row['execution_decision_sha256']==digest(decision_sha256)
         and row['runtime_sha256']==digest(runtime_sha256),'TERMINAL_BINDING')
    need(row['audited_operations']==list(AUDITED_OPERATIONS) and
         row['known_gaps']==list(KNOWN_GAPS),'EVIDENCE_SCOPE_NOT_EXPANDED')
    need(row['observed_reads'] is False and row['latched'] is False and
         type(row['python_unexpected_read_denials']) is int and row['python_unexpected_read_denials']==0 and
         type(row['python_network_denials']) is int and row['python_network_denials']==0,'PYTHON_AUDIT_DENIAL')
    need(row['native_network_operations'] is None and row['native_file_operations'] is None and
         row['native_IO_isolation'] is False,'NO_NATIVE_ZERO_OR_ISOLATION_CLAIM')
    for name in ('audit_journal_reference','supervisor_reference','watchdog_reference'):
        exact(row[name],('id','sha256'));digest(row[name]['sha256'])
        need(type(row[name]['id']) is str and row[name]['id'],'REFERENCE_ID')
    need(row['supervisor_reference']['sha256']==digest(supervisor_pin['sha256']),'SUPERVISOR_PIN')
    need(type(row['nonce']) is str and len(row['nonce'])==32 and
         all(c in '0123456789abcdef' for c in row['nonce']),'NONCE')
    exact(row['process_identity'],('pid','start_ticks'))
    need(all(type(v) is int and v>0 for v in row['process_identity'].values()),'PROCESS_IDENTITY')
    for name,expected in (('new_solver_attempts',new_solver_attempts),('new_solver_returns',new_solver_returns)):
        need(type(row[name]) is int and row[name]>=0 and row[name]==expected,'CONTROLLER_COUNTER_BINDING')
    need(new_solver_attempts==new_solver_returns,'UNFINISHED_SOLVER_ATTEMPT')
    need(type(row['resource_measurements']) is dict and
         row['external_exit_cleanup_verified'] is False,'EXTERNAL_ACCEPTANCE_REMAINS_REQUIRED')
    return row
