"""P3-01 pure exception/forwarding controls. No scientific imports or native calls."""
from pathlib import Path
from datetime import datetime,timezone
import ast,errno,hashlib,inspect,json,os,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from failure_audit import FailureAudit,BudgetStop,SourceReturnedNone
checks=[]
def check(name,condition):
    checks.append({"name":name,"passed":bool(condition)})
    if not condition:raise AssertionError(name)
p={"mass_1":50.,"mass_2":35.,"dtau220":0.,"dtau440":0.,"domega220":0.,"domega440":0.}
def simulate(name,exc=None,value=None,native=True,none_counter=False,expected=None):
    audit=FailureAudit();counter=[0,0.,0];captured=None
    def call():
        if native:counter[0]+=1
        if none_counter:counter[2]+=1
        if exc is not None:raise exc
        return value
    try:audit.guard(call,p,counter)
    except Exception as caught:
        captured=caught;audit.external(caught,p)
    check(name+":propagates",captured is not None)
    check(name+":single_event",len(audit.events)==1)
    check(name+":recorded_kind_keeps_stage",audit.kind_for(captured)==expected)
    check(name+":classification",audit.events[0]["kind"]==expected)
    check(name+":parameters",audit.events[0]["parameters"]==p)
    check(name+":type_message",audit.events[0]["exception_type"]==type(captured).__module__+"."+type(captured).__qualname__ and audit.events[0]["message"]==str(captured))
    if exc is not None:check(name+":same_exception_identity",captured is exc)
    result=audit.summary(counter)
    check(name+":no_inferred_domain_total",result["domain_error_total"] is None)
    return result
reports={}
reports["none"]=simulate("None",native=True,none_counter=True,expected="SOURCE_RETURNED_NONE_UNCLASSIFIED")
check("None:separate_raw_counter",reports["none"]["source_returned_none_count"]==1 and reports["none"]["source_returned_none_counter_raw"]==1 and reports["none"]["recognized_domain_exception_count"]==0)
reports["domain_text"]=simulate("explicit_domain",RuntimeError("Input domain error"),native=True,expected="DOMAIN_ERROR_RECOGNIZED_AFTER_NATIVE_ATTEMPT")
check("explicit_domain:recognized_without_None",reports["domain_text"]["recognized_domain_exception_count"]==1 and reports["domain_text"]["source_returned_none_counter_raw"]==0)
reports["domain_errno"]=simulate("errno_EDOM",OSError(errno.EDOM,"native error"),native=True,expected="DOMAIN_ERROR_RECOGNIZED_AFTER_NATIVE_ATTEMPT")
reports["generic_native"]=simulate("generic_native",RuntimeError("unknown native failure"),native=True,expected="EXCEPTION_INDETERMINATE_AFTER_NATIVE_ATTEMPT")
check("generic_native:not_zero_EDOM_claim",reports["generic_native"]["indeterminate_exception_after_native_attempt_count"]==1 and reports["generic_native"]["domain_error_total"] is None)
reports["before_native"]=simulate("pre_native",ValueError("Input domain error"),native=False,expected="EXCEPTION_BEFORE_NATIVE_ATTEMPT")
reports["temporal"]=simulate("temporal",RuntimeError("WINDOW_BOUND_VIOLATION_ABORT_NOT_PRIOR_REJECTION"),native=False,expected="TEMPORAL_GUARD_BEFORE_NATIVE")
reports["budget"]=simulate("budget",BudgetStop("MAXCALL_INCLUDING_INITIALIZATION"),native=False,expected="BUDGET_STOP")
reports["deadline"]=simulate("source_deadline",TimeoutError("Source deadline reached"),native=False,expected="BUDGET_STOP")
reports["deadline_text_after_native"]=simulate("deadline_text_after_native",TimeoutError("Source deadline reached"),native=True,expected="EXCEPTION_INDETERMINATE_AFTER_NATIVE_ATTEMPT")
reports["unknown_timeout"]=simulate("unknown_timeout",TimeoutError("unclassified timeout"),native=True,expected="EXCEPTION_INDETERMINATE_AFTER_NATIVE_ATTEMPT")
audit=FailureAudit();obj={"plus":object(),"cross":object()};counter=[0,0.,0]
check("success:identity",audit.guard(lambda:obj,p,counter) is obj)
check("success:no_failure_event",not audit.events)
external=RuntimeError("likelihood application failure");audit.external(external,p);audit.external(external,p)
check("external:deduplicated",len(audit.events)==1 and audit.events[0]["kind"]=="APPLICATION_EXCEPTION")
seen={}
def source(frequency_array,mass_1,dtau220,dtau440=0.,domega220=0.,domega440=0.,**kwargs):
    seen.update(args=(frequency_array,mass_1,dtau220),fixed=(dtau440,domega220,domega440),kwargs=kwargs)
    return obj
a=FailureAudit();wrapped=a.wrap(source,lambda:p,[0,0.,0]);frequencies=object();extra=object()
check("wrapper:signature_preserved",inspect.signature(wrapped)==inspect.signature(source))
check("wrapper:bound_callable_preserved",wrapped.__wrapped__ is source)
result=wrapped(frequencies,mass_1=50.,dtau220=0.,dtau440=0.,domega220=0.,domega440=0.,extra=extra)
check("wrapper:return_identity",result is obj)
check("wrapper:forward_identity_and_fixed_zeros",seen["args"]==(frequencies,50.,0.) and seen["fixed"]==(0.,0.,0.) and seen["kwargs"]["extra"] is extra)
check("wrapper:success_no_events",not a.events)
src=(ROOT/"driver_p3.py").read_text();tree=ast.parse(src)
check("driver:wraps_bound_waveform_source","wf.frequency_domain_source_model=failures.wrap(" in src and "wf.frequency_domain_source_model,lambda:last_parameters,counts" in src)
check("driver:no_ambiguous_EDOM_result_key",'"EDOM":int(counts[2])' not in src and '"failure_receipt":failures.summary(counts)' in src)
check("driver:keeps_fail_closed",'"FAILED"' in src and 'never a silent prior rejection' in src)
check("helper:no_infinite_rejection","-inf" not in (ROOT/"failure_audit.py").read_text())
for rel in ("src/pseob_source.py","src/temporal_contract.py","src/synthetic_adapter_v2.py","CONFIG_SYNTHETIC.json"):
    check("P0P2_unchanged:"+rel,(ROOT/rel).read_bytes()==(ROOT.parent/"piloto_sintetico"/rel).read_bytes())
check("no_scientific_modules",not any(x in sys.modules for x in ("numpy","bilby","lal","lalsimulation","dynesty")))
check("no_execution_or_authorization",not (ROOT/"EXECUTION_001").exists() and not (ROOT/"AUTORIZACAO_COORDENACAO.json").exists())
result={"status":"PURE_EXCEPTION_CONTROLS_PASS","created_utc":datetime.now(timezone.utc).isoformat(),"count":len(checks),"checks":checks,"stub_receipts":reports,
 "input_pins":{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in ("driver_p3.py","failure_audit.py","check_exceptions_p3_v2.py")},
 "PE_jobs":0,"native_waveforms":0,"D_read":False,"scope":"Pure Python stubs, propagation, identity, classification, signature/forwarding and static driver checks. Does not execute waveform or likelihood."}
path=ROOT/"CONTROLES_EXCECOES_P3_V2_FINAL.json";assert not path.exists()
raw=(json.dumps(result,indent=2)+"\n").encode();tmp=path.with_name(path.name+".tmp");tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,path)
print(json.dumps({k:v for k,v in result.items() if k not in ("checks","stub_receipts")}))
