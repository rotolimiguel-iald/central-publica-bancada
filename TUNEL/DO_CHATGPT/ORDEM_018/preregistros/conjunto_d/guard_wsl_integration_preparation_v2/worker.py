"""One new WSL-only cache/latch control, never a scientific driver."""
import sys, os, json, hashlib, types, time
from pathlib import Path
import importlib.util, importlib.machinery, threading, copy
BASE=Path("/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/guard_wsl_integration_preparation_v2")
def load_common():
    c=json.loads((BASE/"CONTRATO_WSL.json").read_bytes()); raw=(BASE/"common.py").read_bytes()
    item=next(x for x in c["local_pins"] if x["relative_path"]=="common.py")
    if hashlib.sha256(raw).hexdigest()!=item["sha256"] or len(raw)!=item["bytes"]: raise RuntimeError("Common pin")
    m=types.ModuleType("prepared_protocol");exec(compile(raw,str(BASE/"common.py"),"exec"),m.__dict__)
    return m,c
def main():
    g,c=load_common();g.need(len(sys.argv)==4 and sys.argv[1:3]==["--child",g.REQUEST],"Exact child argv")
    nonce=sys.argv[3];g.check_pins(c,linux=True);_,ah=g.authorization(c)
    w=g.read(BASE/"CLAIM.json");s=g.read(BASE/"RUN/LINUX_CLAIM.json")
    g.need(w["nonce"]==s["nonce"]==nonce and w["request_id"]==s["request_id"]==g.REQUEST,"Nonce/request")
    g.need(w["authorization_sha256"]==ah and s["contract_sha256"]==g.pin(BASE/"CONTRATO_WSL.json")["sha256"],"Pinned dispatch")
    parent=g.proc_identity(os.getppid());g.need(g.matches(parent,g.argv_for("--supervisor",nonce)),"Exact parent")
    g.need(parent["start_ticks"]==s["process"]["start_ticks"] and parent["pid"]==s["process"]["pid"],"Parent incarnation")
    g.need(time.time()<w["work_deadline_epoch"] and not (BASE/"RUN/STOP.json").exists(),"Launch expired/stopped")
    out=BASE/"RUN/CASE";out.mkdir(exist_ok=False)
    self_id=g.serial_identity(g.proc_identity(os.getpid()))
    g.fresh(out/"CASE_CLAIM.json",{"request_id":g.REQUEST,"nonce":nonce,"case_id":g.CASE,"process":self_id,
            "parent_pid":os.getppid(),"contract_sha256":g.pin(BASE/"CONTRATO_WSL.json")["sha256"],"retry_allowed":False})
    raw=(BASE/"sources/audit_guard.py").read_bytes();m=types.ModuleType("qualified_audit_guard")
    m.__file__=str(BASE/"sources/audit_guard.py");exec(compile(raw,m.__file__,"exec"),m.__dict__)
    journal_path=out/"journal.jsonl";journal=m.PreopenedJournal(str(journal_path));latch=m.AuditLatch(journal)
    resultfd=os.open(out/"CASE_RESULT.json",os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    fixture=out/"probe_fixture.py";fixture.write_bytes(b"VALUE = 42\n")
    cache=Path(importlib.util.cache_from_source(str(fixture)));cache.parent.mkdir()
    allowed={str(fixture),str(journal_path)};unexpected=[];seen=[];pings=[0];callbacks=[0]
    calls={n:{e:0 for e in ("c_call","c_return","c_exception")} for n in ("write","fsync")}
    def profile(frame,event,arg):
        if event in ("c_call","c_return","c_exception"):
            if arg is os.write: calls["write"][event]+=1
            if arg is os.fsync: calls["fsync"][event]+=1
    def audit(event,args):
        if event=="iald.guard.wsl.ping":
            g.need(args==(g.CASE,),"Ping identity");pings[0]+=1;return
        forbidden=event.startswith(("socket.","subprocess.","os.spawn")) or event in (
            "os.system","os.posix_spawn","os.fork","os.forkpty","ctypes.dlopen","ctypes.dlsym",
            "os.remove","os.rmdir","os.rename","os.mkdir","os.link","os.symlink","sys.addaudithook")
        target=str(args[:1])[:200];mode=None;flags=None;expected=False
        if event=="import":forbidden=forbidden or args[0]!="probe_fixture"
        if event=="compile":forbidden=forbidden or args[1]!=str(fixture)
        if event=="exec":forbidden=forbidden or args[0].co_filename!=str(fixture)
        if event=="open":
            target,mode,flags=args
            writing=(isinstance(mode,str) and any(x in mode for x in "wax+")) or (isinstance(flags,int) and bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
            expected=str(target)==str(cache) and not writing;forbidden=writing or str(target) not in allowed
        if forbidden:
            row={"event":event,"target":str(target),"expected":expected};seen.append(row)
            if not expected:unexpected.append(row)
            latch.deny(event,target,mode=mode,flags=flags,reason="EXPECTED_CACHE_PROBE" if expected else "UNEXPECTED_SCOPE_DENIAL")
    def checkpoint(phase):
        try:
            latch.checkpoint(phase);callbacks[0]+=1
        except m.AuditViolation:return True
        return False
    status="FAILED";error=None;returned=False;next_blocked=False;final_blocked=False
    try:
        latch.context("WSL_CACHE_PROBE",0,0);audit.__cantrace__=True
        sys.setprofile(profile);sys.addaudithook(audit);latch.installed();sys.audit("iald.guard.wsl.ping",g.CASE)
        g.need(pings[0]==1 and sys.dont_write_bytecode is True,"Hook/-B")
        spec=importlib.util.spec_from_file_location("probe_fixture",str(fixture))
        g.need(isinstance(spec.loader,importlib.machinery.SourceFileLoader),"Real source loader")
        toy=importlib.util.module_from_spec(spec);spec.loader.exec_module(toy)
        returned=toy.VALUE==42;g.need(returned,"Source did not return normally")
        next_blocked=checkpoint("after_import_before_callback");final_blocked=checkpoint("final")
        snap=latch.snapshot();g.need(next_blocked and final_blocked and callbacks[0]==0,"Persistent checkpoints")
        g.need(snap["installed"] and snap["latched"] and snap["denial_count"]==1,"One expected denial")
        g.need(snap["first_event"]==snap["events"][0] and snap["events"][0]["sequence"]==1,"First event preserved")
        g.need(not unexpected and len(seen)==1 and seen[0]["expected"],"Unexpected audit event")
        g.need(snap["journal_error"] is None and calls["write"]["c_return"]>=1 and calls["fsync"]["c_return"]==1,"Physical write/fsync")
        g.no_science();status="PASS_EXPECTED_LATCHED"
    except BaseException as exc:error={"type":type(exc).__name__,"message":str(exc)[:2000]}
    finally:sys.setprofile(None)
    snap=latch.snapshot();jraw=journal_path.read_bytes();rows=[json.loads(x) for x in jraw.splitlines()]
    if rows!=snap["events"] or len(rows)!=1:status="FAILED";error={"type":"JournalMismatch"}
    result={"status":status,"request_id":g.REQUEST,"case_id":g.CASE,"nonce":nonce,"process":self_id,"parent_pid":os.getppid(),
        "error":error,"import_returned_normally":returned,"next_blocked":next_blocked,"final_blocked":final_blocked,
        "callbacks":callbacks[0],"audit_snapshot":snap,"unexpected_operations":unexpected,"hook_seen":seen,
        "profile_real_os_calls":calls,"journal":{"path":str(journal_path),"bytes":len(jraw),"sha256":g.digest(jraw)},
        "runtime":{"version":sys.version,"executable":sys.executable,"loader_code":importlib.machinery.SourceFileLoader.get_code.__code__.co_filename},
        "scientific_imports":0,"scientific_calls":0,"D_read":False,"new_children":0,"retry_allowed":False}
    raw=(json.dumps(result,sort_keys=True)+"\n").encode();g.writefd(resultfd,raw);os.close(resultfd);print(raw.decode(),end="",flush=True)
    return 0 if status=="PASS_EXPECTED_LATCHED" else 1
if __name__=="__main__":
    try:sys.exit(main())
    except Exception as e:print(json.dumps({"status":"FAILED_PREFLIGHT","error":type(e).__name__,"message":str(e)[:1000]}));sys.exit(1)
