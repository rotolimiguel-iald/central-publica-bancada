"""Pure fail-closed supervisor acceptance; no scientific imports or file opening."""
import hashlib

ACCEPTABLE = {"DLOGZ_REACHED_ESS_OK", "DLOGZ_REACHED_ESS_LOW",
              "STOPPED_NOT_CONVERGED", "BUDGET_EXHAUSTED_PARTIAL"}

def integer(value):
    return type(value) is int and value >= 0

def assess(result, journal, *, returncode, process_state, expected_job,
           expected_label, expected_contract, expected_pid, max_calls):
    reasons = []
    def require(ok, reason):
        if not ok:
            reasons.append(reason)
    require(type(returncode) is int and returncode == 0, "CHILD_PROCESS_FAILURE")
    require(process_state == "PROCESS_RETURNED", "SUPERVISOR_NONRETURN")
    if not isinstance(result, dict):
        return {"accepted": False, "disposition": "TERMINAL_FAILURE",
                "reasons": reasons + ["RESULT_MISSING_OR_MALFORMED"]}
    require(result.get("job_id") == expected_job, "JOB_IDENTITY")
    require(result.get("label") == expected_label, "LABEL_IDENTITY")
    require(result.get("contract_sha256") == expected_contract, "CONTRACT_IDENTITY")
    require(type(result.get("pid")) is int and result.get("pid") == expected_pid, "PID_IDENTITY")
    status = result.get("status")
    require(isinstance(status, str) and status in ACCEPTABLE, "RESULT_STATUS")
    ll, native = result.get("likelihood_calls"), result.get("native_calls")
    require(integer(ll) and integer(native) and integer(max_calls)
            and native <= ll <= max_calls, "CALL_LIMIT_OR_TYPE")
    require(result.get("blocked_operations") == [], "BLOCKED_OPERATIONS")
    require(result.get("initialization_qualified") is True, "INITIALIZATION_NOT_QUALIFIED")
    before, after = result.get("initialization_analytic_before_likelihood"), result.get("initialization_analytic_after_likelihood")
    require(isinstance(before,list) and len(before)==2 and before==after, "ANALYTIC_PSD_STATE")
    for name in ("D_read", "coverage_estimated", "independent_noise_realizations"):
        require(result.get(name) is False, "SCOPE_" + name)
    audit = result.get("audit_latch")
    if not isinstance(audit,dict):
        audit = {}
    require({"schema","installed","latched","denial_count","first_event","events","journal_error","checkpoint_counts","interrupted_exceptions"} <= set(audit), "AUDIT_REQUIRED_FIELDS")
    require(audit.get("schema") == "AUDIT_LATCH_V1" and audit.get("installed") is True, "HOOK_RECEIPT")
    require(audit.get("latched") is False and type(audit.get("denial_count")) is int
            and audit.get("denial_count") == 0, "AUDIT_LATCH_DIRTY")
    require(audit.get("first_event") is None and audit.get("events") == []
            and audit.get("journal_error") is None and audit.get("interrupted_exceptions")==[], "AUDIT_EVENTS_OR_IO_ERROR")
    require(isinstance(journal,bytes) and len(journal)==0, "AUDIT_JOURNAL_NONEMPTY_OR_MISSING")
    actual_pin = hashlib.sha256(journal).hexdigest() if isinstance(journal,bytes) else None
    require(isinstance(actual_pin,str) and result.get("audit_journal_sha256")==actual_pin, "AUDIT_JOURNAL_PIN")
    checks = audit.get("checkpoint_counts", {})
    if not isinstance(checks,dict):
        checks = {}
    require(all(integer(v) for v in checks.values()), "CHECKPOINT_TYPES")
    for phase in ("initialization_ready", "final_before_diagnostics", "final_before_result"):
        require(integer(checks.get(phase)) and checks.get(phase,0)>=1, "MISSING_CHECKPOINT_" + phase)
    if integer(ll) and ll:
        require(integer(checks.get("pre_likelihood")) and checks.get("pre_likelihood",0)>=ll, "PRE_LL_COUNT")
        require(checks.get("post_likelihood")==ll and type(checks.get("post_likelihood")) is int, "POST_LL_COUNT")
    if integer(native) and native:
        for phase in ("source_after_imports", "source_before_temporal", "source_before_dictionary", "source_before_waveform", "source_after_waveform"):
            require(integer(checks.get(phase)) and checks.get(phase,0)>=native, "NATIVE_CHECKPOINT_" + phase)
    failures = result.get("failure_receipt")
    if not isinstance(failures,dict):
        failures = {}
    require(failures.get("domain_error_total", "missing") is None, "EDOM_TOTAL_NOT_INFERRED")
    events = failures.get("events")
    require(isinstance(events,list) and all(isinstance(e,dict) and e.get("kind")=="BUDGET_STOP" for e in events), "FAILURE_EVENTS")
    require(type(failures.get("budget_abort_count")) is int and isinstance(events,list)
            and failures.get("budget_abort_count")==len(events), "BUDGET_COUNTER")
    if isinstance(events,list) and events:
        require(status == "BUDGET_EXHAUSTED_PARTIAL", "BUDGET_EVENT_STATUS")
    for name in ("source_returned_none_count", "source_returned_none_counter_raw", "recognized_domain_exception_count", "indeterminate_exception_after_native_attempt_count", "pre_native_exception_count", "temporal_guard_count", "application_exception_count"):
        require(type(failures.get(name)) is int and failures.get(name)==0, "FAILURE_COUNTER_"+name)
    accepted = not reasons
    return {"accepted": accepted, "disposition": ("CLEAN_PARTIAL" if status in {"STOPPED_NOT_CONVERGED", "BUDGET_EXHAUSTED_PARTIAL", "DLOGZ_REACHED_ESS_LOW"} else "CLEAN_CONVERGED") if accepted else "TERMINAL_FAILURE", "reasons": reasons}

def campaign_exit(assessments, planned):
    """Nonzero for incomplete/failed campaigns, even if the parent reached its end."""
    return 0 if len(assessments)==planned and all(x.get("accepted") is True for x in assessments) else 2
