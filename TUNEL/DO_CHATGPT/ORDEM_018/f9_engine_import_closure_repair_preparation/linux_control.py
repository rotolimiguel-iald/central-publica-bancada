"""WSL supervisor or identity-bound cleanup; neither role imports science."""
import time
ENTRY=time.monotonic()
import sys,os,json,hashlib,types,subprocess,selectors,fcntl,signal
from pathlib import Path
BASE=Path("/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_engine_import_closure_repair_preparation")
def load():
    c=json.loads((BASE/"CONTRATO_WSL.json").read_bytes());raw=(BASE/"common.py").read_bytes()
    q=next(x for x in c["local_pins"] if x["relative_path"]=="common.py")
    if hashlib.sha256(raw).hexdigest()!=q["sha256"] or len(raw)!=q["bytes"]:raise RuntimeError("Common pin")
    g=types.ModuleType("protocol");exec(compile(raw,str(BASE/"common.py"),"exec"),g.__dict__);return g,c

def gate(g,deadline):
    fd=os.open(BASE/"RUN/LAUNCH_GATE.lock",os.O_RDWR)
    try:
        while True:
            try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);return fd
            except BlockingIOError:
                g.need(time.monotonic()<deadline,"Launch gate timeout");time.sleep(.02)
    except BaseException:os.close(fd);raise

def stop_child(g,proc,argv,deadline):
    if proc.poll() is None:
        try:g.exact_signal(proc.pid,argv)
        except ProcessLookupError:pass
    proc.wait(timeout=max(.001,min(2,deadline-time.monotonic())))
    return proc.returncode

def capture(g,proc,argv,deadline):
    sel=selectors.DefaultSelector();buffers={"stdout":bytearray(),"stderr":bytearray()}
    for name in buffers:
        stream=getattr(proc,name);os.set_blocking(stream.fileno(),False);sel.register(stream,selectors.EVENT_READ,name)
    try:
        while sel.get_map() or proc.poll() is None:
            g.need(time.monotonic()<deadline,"Linux child work deadline")
            for key,_ in sel.select(min(.05,max(0,deadline-time.monotonic()))):
                chunk=os.read(key.fileobj.fileno(),4096)
                if not chunk:sel.unregister(key.fileobj);continue
                room=32768-len(buffers[key.data])
                buffers[key.data].extend(chunk[:room])
                g.need(len(chunk)<=room,"Child output overflow")
        proc.wait(timeout=.1)
        return {k:bytes(v) for k,v in buffers.items()}
    finally:sel.close()

def validate_case(g,child,nonce,proc):
    g.need(child["status"]=="ENGINEERING_PREDICTIONS_WRITTEN" and child["request_id"]==g.REQUEST and child["case_id"]==g.CASE,"Case identity/status")
    g.need(child["nonce"]==nonce and child["process"]["pid"]==proc.pid and child["parent_pid"]==os.getpid(),"Case PID/nonce")
    g.need(child["solver_calls_attempted"]==child["solver_calls_returned"]==1 and child["new_children"]==0,"Solver/child budget")
    g.need(child["observed_reads"] is False and child["D_read"] is False and child["module_errors"]==[],"Scope/dependencies")
    snap=child["audit_snapshot"]
    g.need(snap["installed"] and not snap["latched"] and snap["denial_count"]==0 and snap["journal_error"] is None,"Sticky audit")
    journal=BASE/"RUN/CASE/journal.jsonl"
    g.need([json.loads(x) for x in journal.read_bytes().splitlines()]==snap["events"]==[],"Physical journal")
    for name,record in child["artifacts"].items():
        p=BASE/"RUN/CASE"/name
        g.need(record=={"path":str(p),**g.pin(p)},"Output pin: "+name)
    g.need(set(child["artifacts"])=={"BACKGROUND_RESULT.json","ENGINE_EXECUTION_RECEIPT.json","BACKGROUND_PACKET.json","FIVE_MODEL_OUTPUT.json"},"Output completeness")
    result=g.read(BASE/"RUN/CASE/FIVE_MODEL_OUTPUT.json")
    g.need(result["status"]=="ENGINEERING_ONLY" and result["certification"]["certified"] is False,"No certificate promotion")
    g.need(len(result["row_ids"])==283 and result["nuisance"]["dimension"]==63,"Assembly dimensions")
    g.need(set(result["models"])=={"H1_TGL","H2_LCDM","H3_beta_free","H4_Cepheid","H5_rd_free"},"Five models")
    g.need(all(len(v["mean_without_nuisance"])==283 for v in result["models"].values()),"Five prediction lengths")
    claim=g.read(BASE/"RUN/CASE/CASE_CLAIM.json")
    g.need(claim["nonce"]==nonce and claim["process"]==child["process"],"Case claim")


def supervise(g,c,w,nonce):
    deadline=ENTRY+125;work=min(ENTRY+110,time.monotonic()+max(0,w["work_deadline_epoch"]-time.time()))
    me=g.serial_identity(g.proc_identity(os.getpid()))
    g.fresh(BASE/"RUN/LINUX_CLAIM.json",{"request_id":g.REQUEST,"nonce":nonce,"process":me,
        "contract_sha256":g.pin(BASE/"CONTRATO_WSL.json")["sha256"],"retry_allowed":False})
    proc=None;argv=g.argv_for("--child",nonce);status="FAILED";error=None;streams=None;child=None;clean=False
    try:
        g.need(time.monotonic()<work and not (BASE/"RUN/STOP.json").exists(),"Expired/stopped before launch")
        fd=gate(g,work)
        try:
            g.need(not (BASE/"RUN/STOP.json").exists() and time.monotonic()<work,"Fenced before Popen")
            proc=subprocess.Popen(argv,cwd=BASE,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                env={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1", **{n:"1" for n in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS")}},start_new_session=True)
            childid=g.serial_identity(g.proc_identity(proc.pid))
            g.need(g.matches(g.proc_identity(proc.pid),argv),"Child identity after Popen")
            g.fresh(BASE/"RUN/CHILD_PROCESS.json",{"request_id":g.REQUEST,"nonce":nonce,"process":childid,"argv":argv})
        finally:os.close(fd)
        streams=capture(g,proc,argv,work)
        g.need(proc.returncode==0 and not streams["stderr"],"Child returncode/stderr")
        child=json.loads(streams["stdout"]);g.need(child==g.read(BASE/"RUN/CASE/CASE_RESULT.json"),"Stdout/physical result mismatch")
        validate_case(g,child,nonce,proc);status="F9_BACKGROUND_ASSEMBLY_PASS_PENDING_EXTERNAL_CLEANUP"
    except BaseException as exc:error={"type":type(exc).__name__,"message":str(exc)[:2000]}
    finally:
        if proc is not None:
            try:
                if proc.poll() is None:stop_child(g,proc,argv,deadline);status="FAILED"
                clean=proc.poll() is not None
            except BaseException as exc:status="UNCERTAIN_CHILD_STATE";error={"type":type(exc).__name__,"message":str(exc)[:2000]}
    if streams:
        for name,raw in streams.items():
            with (BASE/"RUN"/(name+".bin")).open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    receipt={"status":status,"request_id":g.REQUEST,"nonce":nonce,"process":me,"child":child,"child_reaped":clean,
        "child_returncode":None if proc is None else proc.returncode,"error":error,"wall_before_receipt_s":time.monotonic()-ENTRY,
        "scientific_calls":None if child is None else child["solver_calls_attempted"],"retry_allowed":False,"requires_external_cleanup_receipt":True}
    g.fresh(BASE/"RUN/LINUX_RESULT.json",receipt)
    g.need(time.monotonic()<deadline,"Linux final IO exceeded nominal deadline")
    print(json.dumps(receipt,sort_keys=True),flush=True)
    g.need(time.monotonic()<deadline,"Terminal stdout exceeded Linux deadline")
    return 0 if status=="F9_BACKGROUND_ASSEMBLY_PASS_PENDING_EXTERNAL_CLEANUP" and clean else 1

def cleanup(g,c,w,nonce):
    deadline=ENTRY+25;stopped=[];lockfd=None
    g.need((BASE/"RUN/STOP.json").exists(),"Windows durable stop fence required")
    fence=g.read(BASE/"RUN/STOP.json");g.need(fence["nonce"]==nonce and fence["request_id"]==g.REQUEST,"Stop fence identity")
    g.fresh(BASE/"RUN/CLEANUP_CLAIM.json",{"request_id":g.REQUEST,"nonce":nonce,"process":g.serial_identity(g.proc_identity(os.getpid()))})
    status="UNCERTAIN_ORPHAN_STATE";error=None
    try:
        # First terminate only exact known commands. pidfd prevents PID-reuse signaling.
        for x,argv in g.scoped_processes(nonce):
            g.need(time.monotonic()<deadline,"Cleanup deadline")
            try:stopped.append(g.exact_signal(x["pid"],argv))
            except ProcessLookupError:pass
        # Any delayed supervisor must acquire this same gate and then see STOP.
        lockfd=gate(g,deadline)
        while True:
            live=g.scoped_processes(nonce)
            if not live:break
            g.need(time.monotonic()<deadline,"Controlled processes still present")
            for x,argv in live:
                try:stopped.append(g.exact_signal(x["pid"],argv))
                except ProcessLookupError:pass
            time.sleep(.02)
        status="NO_LIVE_CONTROLLED_PROCESSES_VERIFIED"
    except BaseException as exc:error={"type":type(exc).__name__,"message":str(exc)[:2000]}
    finally:
        if lockfd is not None:os.close(lockfd)
    result={"status":status,"request_id":g.REQUEST,"nonce":nonce,"stopped":stopped,"error":error,
        "launch_fence_persistent":True,"wall_before_receipt_s":time.monotonic()-ENTRY,"control_runs":0,"scientific_calls":0}
    g.fresh(BASE/"RUN/CLEANUP_RESULT.json",result);g.need(time.monotonic()<deadline,"Cleanup final IO deadline")
    print(json.dumps(result,sort_keys=True),flush=True)
    g.need(time.monotonic()<deadline,"Terminal stdout exceeded cleanup deadline")
    return 0 if status=="NO_LIVE_CONTROLLED_PROCESSES_VERIFIED" else 2

def main():
    g,c=load();g.need(len(sys.argv)==4 and sys.argv[1] in ("--supervisor","--cleanup") and sys.argv[2]==g.REQUEST,"Exact mode/identity")
    nonce=sys.argv[3];g.check_pins(c,linux=True);_,ah=g.authorization(c);w=g.read(BASE/"CLAIM.json")
    g.need(w["request_id"]==g.REQUEST and w["nonce"]==nonce and w["authorization_sha256"]==ah,"Windows claim")
    g.need(w["contract_sha256"]==g.pin(BASE/"CONTRATO_WSL.json")["sha256"],"Claim pin")
    g.need(hasattr(os,"pidfd_open") and hasattr(signal,"pidfd_send_signal"),"pidfd capability required before control")
    ownfd=os.pidfd_open(os.getpid(),0);os.close(ownfd)  # Capability preflight, no signal.
    if sys.argv[1]=="--supervisor":return supervise(g,c,w,nonce)
    return cleanup(g,c,w,nonce)
if __name__=="__main__":
    try:sys.exit(main())
    except Exception as e:print(json.dumps({"status":"FAILED_PREFLIGHT_OR_RECEIPT","error":type(e).__name__,"message":str(e)[:1200]}));sys.exit(1)
