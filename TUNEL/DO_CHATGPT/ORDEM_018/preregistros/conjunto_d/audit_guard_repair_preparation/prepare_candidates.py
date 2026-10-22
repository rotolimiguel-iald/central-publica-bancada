"""Build candidate copies by asserted textual deltas. Never imports scientific code."""
from pathlib import Path
import sys,json,difflib
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'proveniencia'))
from audit_provenance import atomic,metadata
OUT=Path(__file__).resolve().parent
OLD=OUT.parent/'p3_init_qualified_003'
DST=OUT/'candidate'
def one(text,old,new):
    assert text.count(old)==1,(old[:90],text.count(old))
    return text.replace(old,new,1)
def save(rel,text):
    old=(OLD/rel).read_text(encoding='utf-8')
    atomic(DST/rel,text)
    atomic(OUT/('DELTA_'+rel.replace('/','_')+'.patch'),''.join(difflib.unified_diff(old.splitlines(True),text.splitlines(True),fromfile='INIT003/'+rel,tofile='candidate/'+rel)))
s=(OLD/'src/pseob_source.py').read_text(encoding='utf-8')
s=one(s,'EDOM_LOG = None','''EDOM_LOG = None
AUDIT_CHECKPOINT = None

def set_audit_checkpoint(callback):
    global AUDIT_CHECKPOINT
    if AUDIT_CHECKPOINT is not None:raise RuntimeError("Audit checkpoint already bound")
    if not callable(callback):raise TypeError("Audit callback required")
    AUDIT_CHECKPOINT=callback

def audit_checkpoint(phase):
    if AUDIT_CHECKPOINT is None:raise RuntimeError("Audit callback not configured")
    AUDIT_CHECKPOINT(phase)
''')
s=one(s,'    import lal\n','    audit_checkpoint("source_entry")\n    import lal\n')
s=one(s,'    from bilby.gw.source import lal_binary_black_hole\n','    from bilby.gw.source import lal_binary_black_hole\n    audit_checkpoint("source_after_imports")\n')
s=one(s,'    from temporal_contract import validate_time_contract\n','    from temporal_contract import validate_time_contract\n    audit_checkpoint("source_before_temporal")\n')
s=one(s,'    dictionary=lal.CreateDict()','    audit_checkpoint("source_before_dictionary")\n    dictionary=lal.CreateDict()')
s=one(s,'    started=time.perf_counter()\n    try:','    audit_checkpoint("source_before_waveform")\n    started=time.perf_counter()\n    try:')
s=one(s,'                COST_COUNTER[0]+=1;COST_COUNTER[1]+=time.perf_counter()-started\n','                COST_COUNTER[0]+=1;COST_COUNTER[1]+=time.perf_counter()-started\n        audit_checkpoint("source_after_waveform")\n')
save('src/pseob_source.py',s)
d=(OLD/'driver_p3.py').read_text(encoding='utf-8')
d=one(d,'from failure_audit import BudgetStop, FailureAudit','from failure_audit import BudgetStop, FailureAudit\nfrom audit_guard import AuditLatch, AuditViolation, PreopenedJournal')
d=one(d,'def main():\n','def main():\n    raise RuntimeError("PREPARATION_ONLY: no runnable campaign contract or execution permission")\n')
d=one(d,'    audit_paths=set();blocked=[]','''    audit_paths=set();blocked=[]
    counts=Counter();ll_calls=0
    journal_path=out/"AUDIT_EVENTS.jsonl"
    guard=AuditLatch(PreopenedJournal(journal_path))
    def checkpoint(phase):
        guard.context(phase,ll_calls,counts[0])
        guard.checkpoint(phase, cause=sys.exc_info()[1])
    source.set_audit_checkpoint(checkpoint)
    def deny(event,target,reason,mode=None,flags=None):
        blocked.append(str(target))
        guard.refresh_counts(ll_calls,counts[0])
        guard.deny(event,target,mode=mode,flags=flags,reason=reason)''')
d=one(d,'            blocked.append(event);raise PermissionError("P3 forbids network/child execution")','            deny(event,event,"P3 forbids network/child execution")')
d=one(d,'            if write and not inside:blocked.append(str(p));raise PermissionError("Write outside this synthetic job")','            if write and not inside:deny(event,str(p),"Write outside this synthetic job",mode,flags)')
d=one(d,'                blocked.append(str(p));raise PermissionError("Read outside exact synthetic/runtime allowlist")','                deny(event,str(p),"Read outside exact synthetic/runtime allowlist",mode,flags)')
d=one(d,'    sys.addaudithook(audit)\n    counts=Counter();source.set_cost_counter(counts)','    sys.addaudithook(audit);guard.installed()\n    checkpoint("hook_installed")\n    source.set_cost_counter(counts)')
d=one(d,'    def budget():\n','    def budget():\n        checkpoint("budget")\n')
d=one(d,'        if blocked:raise ValueError("Initialization swallowed a blocked operation")','        checkpoint("initialization_ready")')
d=one(d,'            last_parameters=parameters(v)\n','            checkpoint("pre_likelihood")\n            last_parameters=parameters(v)\n')
d=one(d,'            value=float(likelihood.log_likelihood_ratio(last_parameters))','            guard.refresh_counts(ll_calls,counts[0])\n            value=guard.evaluate(lambda:float(likelihood.log_likelihood_ratio(last_parameters)))')
d=one(d,'        if last is None:raise RuntimeError("Sampler returned no dead points")','        checkpoint("sampler_returned")\n        if last is None:raise RuntimeError("Sampler returned no dead points")')
d=one(d,'            for _ in sampler.add_live_points():pass','            for _ in sampler.add_live_points():checkpoint("live_point_added")')
d=one(d,'    except BudgetStop as exc:','    except AuditViolation as exc:\n        status="AUDIT_VIOLATION";error=type(exc).__name__+": "+str(exc)\n        failures.external(exc,last_parameters)\n    except BudgetStop as exc:')
start=d.index('        artifact=None\n');end=d.index('        result={',start)
body=d[start:end][len('        artifact=None\n'):]
d=d[:start]+'''        artifact=None
        try:
            checkpoint("final_before_diagnostics")
'''+''.join('    '+line if line.strip() else line for line in body.splitlines(True))+'''            checkpoint("final_before_result")
        except AuditViolation as exc:
            status="AUDIT_VIOLATION";error=type(exc).__name__+": "+str(exc)
            failures.external(exc,last_parameters)
        except Exception as exc:
            status="FAILED";error=type(exc).__name__+": "+str(exc)
            failures.external(exc,last_parameters)
        if guard.snapshot()["latched"]:
            status="AUDIT_VIOLATION"
'''+d[end:]
d=one(d,'        result={"status":status,"job_id":job_id,','        result={"status":status,"pid":os.getpid(),"job_id":job_id,')
d=one(d,'                "audit_scope":','                "audit_latch":guard.snapshot(),"audit_journal_sha256":sha(journal_path),\n                "audit_scope":')
d=one(d,'        js(out/"RESULT.json",result)\n','        js(out/"RESULT.json",result)\n        checkpoint("final_after_result")\n')
d=one(d,'    return 2 if status=="FAILED" else 0','    return 2 if status in ("FAILED","AUDIT_VIOLATION") else 0')
save('driver_p3.py',d)
l=(OLD/'launch_p3.py').read_text(encoding='utf-8')
l=one(l,'from datetime import datetime,timezone','from datetime import datetime,timezone\nfrom result_acceptance import assess, campaign_exit')
l=one(l,'def main():\n','def main():\n    raise RuntimeError("PREPARATION_ONLY: no runnable campaign contract or execution permission")\n')
l=one(l,'    results=[];t0=time.perf_counter()','    results=[];assessments=[];t0=time.perf_counter()')
l=one(l,'        row={"job_id":job["id"],','        row={"pid":p.pid,"job_id":job["id"],')
start=l.index('        if rp.exists():');end=l.index('    js(run/"CAMPAIGN_RECEIPT.json"',start)
l=l[:start]+'''        result=None;journal=None
        try:
            if rp.exists():
                raw=rp.read_bytes();result=json.loads(raw)
                row.update(result_sha256=hashlib.sha256(raw).hexdigest(),result_status=result.get("status"))
            jp=out/"AUDIT_EVENTS.jsonl"
            if jp.exists():
                journal=jp.read_bytes()
                row.update(audit_journal_sha256=hashlib.sha256(journal).hexdigest(),audit_journal_bytes=len(journal))
            decision=assess(result,journal,returncode=rc,process_state=state,
                expected_job=job["id"],expected_label=job["label"],expected_contract=pin,
                expected_pid=p.pid,max_calls=c["limits"]["max_likelihood_calls"])
        except Exception as exc:
            decision={"accepted":False,"disposition":"TERMINAL_FAILURE",
                      "reasons":["RECEIPT_READ_OR_VALIDATION_ERROR"],"error":type(exc).__name__+": "+str(exc)}
        row["acceptance"]=decision;assessments.append(decision)
        results.append(row);js(out/"PROCESS_RECEIPT.json",row)
        if not decision["accepted"]:
            break # Terminal even for a partial label; no retry/resume/replacement.
'''+l[end:]
l=one(l,'                                    "started_jobs":len(results),"planned_jobs":2,"no_retry":True,','                                    "started_jobs":len(results),"planned_jobs":len(c["jobs"]),"no_retry":True,\n                                    "exit_code":campaign_exit(assessments,len(c["jobs"])),\n                                    "status":"CLEAN_PROTOCOL_COMPLETION" if campaign_exit(assessments,len(c["jobs"]))==0 else "TERMINAL_FAILURE_OR_INCOMPLETE",')
l=one(l,'    print(json.dumps(results))\nif __name__=="__main__":main()','    print(json.dumps(results))\n    return campaign_exit(assessments,len(c["jobs"]))\nif __name__=="__main__":sys.exit(main())')
save('launch_p3.py',l)
rels=['driver_p3.py','launch_p3.py','src/pseob_source.py','CONTRATO_P3.json','MANIFESTO_PACOTE_INIT003.json','failure_audit.py','prior_transform.py','src/synthetic_adapter_v2.py','src/temporal_contract.py']
atomic(OUT/'SOURCES_BASELINE.json',json.dumps({'originals':[metadata(OLD/x)[0] for x in rels]},ensure_ascii=False,indent=2)+'\n')
print('Candidates/diffs prepared; no import or execution.')
