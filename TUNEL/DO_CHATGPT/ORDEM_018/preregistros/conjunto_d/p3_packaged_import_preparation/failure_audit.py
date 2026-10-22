"""Pure receipt classification for the P3 source wrapper; no scientific imports."""
import errno
import re
from functools import wraps

class BudgetStop(RuntimeError):
    pass

class SourceReturnedNone(RuntimeError):
    pass

class FailureAudit:
    def __init__(self):
        self.events=[]
        self._seen_exceptions=[]

    def _record(self,kind,exc,parameters,before=None,after=None):
        if any(exc is seen for seen in self._seen_exceptions):
            return
        self._seen_exceptions.append(exc)
        self.events.append({
            "kind":kind,
            "exception_type":type(exc).__module__+"."+type(exc).__qualname__,
            "message":str(exc),
            "errno":getattr(exc,"errno",None),
            "parameters":dict(parameters) if parameters is not None else None,
            "native_attempts_before":None if before is None else int(before[0]),
            "native_attempts_after":None if after is None else int(after[0]),
            "source_none_counter_before":None if before is None else int(before[2]),
            "source_none_counter_after":None if after is None else int(after[2]),
            "origin_limit":"After-native-attempt does not by itself locate the exception inside C."
        })

    def classify(self,exc,before=None,after=None):
        attempted=before is not None and after is not None and after[0]>before[0]
        message=str(exc)
        if isinstance(exc,BudgetStop):
            return "BUDGET_STOP"
        if not attempted and isinstance(exc,TimeoutError) and message=="Source deadline reached":
            return "BUDGET_STOP"
        if not attempted and "WINDOW_BOUND_VIOLATION_ABORT_NOT_PRIOR_REJECTION" in message:
            return "TEMPORAL_GUARD_BEFORE_NATIVE"
        if attempted:
            if getattr(exc,"errno",None)==errno.EDOM or re.search(r"\binput\s+domain\s+error\b",message,re.IGNORECASE):
                return "DOMAIN_ERROR_RECOGNIZED_AFTER_NATIVE_ATTEMPT"
            return "EXCEPTION_INDETERMINATE_AFTER_NATIVE_ATTEMPT"
        return "EXCEPTION_BEFORE_NATIVE_ATTEMPT" if before is not None else "APPLICATION_EXCEPTION"

    def guard(self,call,parameters,counter):
        before=tuple(counter)
        try:
            value=call()
        except Exception as exc:
            self._record(self.classify(exc,before,tuple(counter)),exc,parameters,before,tuple(counter))
            raise
        if value is None:
            exc=SourceReturnedNone("SOURCE_RETURNED_NONE_ABORT_NOT_PRIOR_REJECTION")
            self._record("SOURCE_RETURNED_NONE_UNCLASSIFIED",exc,parameters,before,tuple(counter))
            raise exc
        return value

    def kind_for(self,exc):
        for seen,event in zip(self._seen_exceptions,self.events):
            if exc is seen:return event["kind"]
        raise LookupError("Exception has not been recorded")

    def external(self,exc,parameters=None):
        self._record(self.classify(exc),exc,parameters)

    def wrap(self,bound_source,get_parameters,counter):
        # Wrap the actual callable bound in WaveformGenerator, not an imported alias.
        @wraps(bound_source)
        def audited(*args,**kwargs):
            return self.guard(lambda:bound_source(*args,**kwargs),get_parameters(),counter)
        return audited

    def summary(self,source_counter):
        kinds=[e["kind"] for e in self.events]
        return {
            "source_returned_none_count":kinds.count("SOURCE_RETURNED_NONE_UNCLASSIFIED"),
            "source_returned_none_counter_raw":int(source_counter[2]),
            "recognized_domain_exception_count":kinds.count("DOMAIN_ERROR_RECOGNIZED_AFTER_NATIVE_ATTEMPT"),
            "indeterminate_exception_after_native_attempt_count":kinds.count("EXCEPTION_INDETERMINATE_AFTER_NATIVE_ATTEMPT"),
            "pre_native_exception_count":kinds.count("EXCEPTION_BEFORE_NATIVE_ATTEMPT"),
            "temporal_guard_count":kinds.count("TEMPORAL_GUARD_BEFORE_NATIVE"),
            "budget_abort_count":kinds.count("BUDGET_STOP"),
            "application_exception_count":kinds.count("APPLICATION_EXCEPTION"),
            "events":self.events,
            "domain_error_total":None,
            "domain_error_total_scope":"Not inferred: None and generic exceptions are not certified EDOM; explicit recognized count is reported separately."
        }
