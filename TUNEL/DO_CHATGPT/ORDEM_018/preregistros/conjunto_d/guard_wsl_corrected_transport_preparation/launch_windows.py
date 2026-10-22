"""Windows outer deadline includes WSL startup and identity-bound cleanup."""
import time
ENTRY=time.monotonic()
import sys,os,json,hashlib,types,uuid,subprocess,threading
from pathlib import Path
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\preregistros\conjunto_d\guard_wsl_corrected_transport_preparation")
WSL=r"C:\Windows\System32\wsl.exe"
def load():
    c=json.loads((BASE/"CONTRATO_WSL.json").read_bytes());raw=(BASE/"common.py").read_bytes()
    q=next(x for x in c["local_pins"] if x["relative_path"]=="common.py")
    if hashlib.sha256(raw).hexdigest()!=q["sha256"] or len(raw)!=q["bytes"]:raise RuntimeError("Common pin")
    g=types.ModuleType("protocol");exec(compile(raw,str(BASE/"common.py"),"exec"),g.__dict__);return g,c
class Capture:
    def __init__(self,proc):
        self.buffers={"stdout":bytearray(),"stderr":bytearray()};self.overflow=False;self.threads=[]
        self.errors={key:None for key in self.buffers}
        self.eof={key:False for key in self.buffers}
        for key in self.buffers:
            t=threading.Thread(target=self.read,args=(key,getattr(proc,key)),daemon=True);t.start();self.threads.append(t)
    def read(self,key,stream):
        try:
            while True:
                raw=stream.read(4096)
                if raw==b"":
                    self.eof[key]=True
                    return
                if not isinstance(raw,bytes):raise TypeError("Capture read did not return bytes")
                room=32768-len(self.buffers[key]);self.buffers[key].extend(raw[:room])
                if len(raw)>room:self.overflow=True
        except BaseException as exc:
            # A terminated reader is not evidence of EOF or a complete stream.
            self.errors[key]={"type":type(exc).__name__,"message":str(exc)[:1000]}
    def require_no_errors(self):
        if any(error is not None for error in self.errors.values()):
            raise RuntimeError("WSL capture read failure: "+json.dumps(self.errors,sort_keys=True))
    def join(self,deadline):
        for t in self.threads:t.join(timeout=max(0,min(1,deadline-time.monotonic())))
        self.require_no_errors()
        if any(t.is_alive() for t in self.threads):return False
        if not all(self.eof.values()):raise RuntimeError("Capture reader ended without normal EOF")
        if self.overflow:raise RuntimeError("WSL output overflow")
        return True
    def snapshot(self):
        return {"errors":dict(self.errors),"eof":dict(self.eof),"overflow":self.overflow,
                "retained_bytes":{key:len(value) for key,value in self.buffers.items()},
                "all_readers_terminated":not any(t.is_alive() for t in self.threads)}
    def text(self,key):return bytes(self.buffers[key])

def launch(g,mode,nonce):
    argv=[WSL,"--distribution","Ubuntu-24.04","--exec",*g.argv_for(mode,nonce)]
    proc=subprocess.Popen(argv,cwd=BASE,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
    return proc,Capture(proc),argv

def wait(proc,cap,deadline):
    while proc.poll() is None:
        cap.require_no_errors()
        if cap.overflow:raise RuntimeError("WSL output overflow")
        if time.monotonic()>=deadline:raise TimeoutError("Outer WSL deadline")
        time.sleep(.02)
    if not cap.join(deadline):raise TimeoutError("Stream capture not joined")
    cap.require_no_errors()
    if cap.overflow:raise RuntimeError("WSL output overflow")
    return proc.returncode

def main():
    g,c=load();g.need(os.name=="nt" and sys.argv[1:]==["--run-once"],"Fixed Windows entry")
    g.need(Path(__file__).resolve()==BASE/"launch_windows.py","Fixed script")
    g.check_pins(c);_,ah=g.authorization(c)
    for q in c["windows_pins"]:g.need(g.pin(q["path"])=={k:q[k] for k in ("bytes","sha256")},"Windows pin")
    g.need(not any((BASE/x).exists() for x in ("CLAIM.json","RUN","RESULT.json")),"Consumed or uncertain unit; no replay")
    deadline=ENTRY+60;work=ENTRY+40;nonce=str(uuid.uuid4());g.need(time.monotonic()<work,"Preflight deadline")
    g.fresh(BASE/"CLAIM.json",{"request_id":g.REQUEST,"nonce":nonce,"pid":os.getpid(),"contract_sha256":g.pin(BASE/"CONTRATO_WSL.json")["sha256"],
        "authorization_sha256":ah,"work_deadline_epoch":time.time()+max(0,work-time.monotonic()),"max_control_runs":1,"retry_allowed":False})
    run=BASE/"RUN";run.mkdir(exist_ok=False)
    with (run/"LAUNCH_GATE.lock").open("xb") as f:f.flush();os.fsync(f.fileno())
    primary=None;pcap=None;cleaner=None;ccap=None;error=None;linux=None;cleanup=None;status="FAILED"
    try:
        g.need(time.monotonic()<work,"Expired after claim IO before WSL launch")
        primary,pcap,pargv=launch(g,"--supervisor",nonce)
        g.fresh(run/"WSL_PROCESS.json",{"request_id":g.REQUEST,"nonce":nonce,"pid":primary.pid,"argv":pargv,"handle_owned_by_this_launcher":True})
        wait(primary,pcap,work)
        g.need(primary.returncode==0 and not pcap.text("stderr"),"WSL supervisor returncode/stderr")
        linux=json.loads(pcap.text("stdout"));g.need(linux==g.read(run/"LINUX_RESULT.json"),"Linux result stream mismatch")
        g.need(linux["status"]=="WSL_CONTROL_PASS_PENDING_EXTERNAL_CLEANUP" and linux["request_id"]==g.REQUEST and linux["nonce"]==nonce,
            "Linux result status/identity")
        g.validate_observed_argv(linux["argv_transport"],"--supervisor",nonce)
        g.need(linux["argv_transport"]==g.read(run/"ARGV_SUPERVISOR.json"),"Supervisor argv physical receipt")
        g.need(linux["argv_transport"]["process"]==linux["process"],"Supervisor argv process binding")
        g.validate_observed_argv(linux["child"]["argv_transport"],"--child",nonce)
        g.need(linux["child"]["argv_transport"]==g.read(run/"ARGV_CHILD.json"),"Child argv physical receipt")
        g.need(linux["child"]["argv_transport"]["process"]==linux["child"]["process"],"Child argv process binding")
        g.need(linux["child_reaped"] is True and linux["child_returncode"]==0 and linux["scientific_calls"]==0,"Child not cleanly reaped")
        status="CONTROL_PASS_CLEANUP_PENDING"
    except BaseException as exc:error={"type":type(exc).__name__,"message":str(exc)[:2000]}
    finally:
        # Fence first; any delayed supervisor is forbidden to launch after this point.
        try:
            g.fresh(run/"STOP.json",{"request_id":g.REQUEST,"nonce":nonce,"reason":"TERMINAL_LAUNCH_FENCE"})
            g.need(time.monotonic()<deadline-5,"No nominal cleanup reserve")
            cleaner,ccap,cargv=launch(g,"--cleanup",nonce)
            g.fresh(run/"CLEANUP_WSL_PROCESS.json",{"request_id":g.REQUEST,"nonce":nonce,"pid":cleaner.pid,"argv":cargv})
            wait(cleaner,ccap,deadline-5)
            g.need(cleaner.returncode==0 and not ccap.text("stderr"),"Cleanup process failed")
            cleanup=json.loads(ccap.text("stdout"));g.need(cleanup==g.read(run/"CLEANUP_RESULT.json"),"Cleanup stream mismatch")
            g.need(cleanup["status"]=="NO_LIVE_CONTROLLED_PROCESSES_VERIFIED" and cleanup["nonce"]==nonce and cleanup["request_id"]==g.REQUEST,
                "No proof of controlled process termination")
            g.validate_observed_argv(cleanup["argv_transport"],"--cleanup",nonce)
            g.need(cleanup["argv_transport"]==g.read(run/"ARGV_CLEANUP.json"),"Cleanup argv physical receipt")
            g.need(cleanup["argv_transport"]["process"]==g.read(run/"CLEANUP_CLAIM.json")["process"],"Cleanup argv process binding")
            if status=="CONTROL_PASS_CLEANUP_PENDING" and not cleanup["stopped"]:status="PASS_WSL_STDLIB_INTEGRATION_ONCE"
            else:status="FAILED_TERMINAL_CLEANED"
        except BaseException as exc:
            status="UNCERTAIN_ORPHAN_STATE";error={"type":type(exc).__name__,"message":str(exc)[:2000]}
        # Uses subprocess-owned Windows process handles, never PID-only broad kill.
        for proc,cap in ((primary,pcap),(cleaner,ccap)):
            if proc is None:continue
            try:
                if proc.poll() is None:
                    proc.kill();proc.wait(timeout=max(.001,min(1,deadline-time.monotonic())))
                    if status=="PASS_WSL_STDLIB_INTEGRATION_ONCE":status="FAILED_TERMINAL_CLEANED"
                if cap is not None and not cap.join(deadline):raise RuntimeError("Unjoined WSL streams")
            except BaseException as exc:
                status="UNCERTAIN_ORPHAN_STATE";error={"type":type(exc).__name__,"message":str(exc)[:2000]}
    for label,cap in (("primary",pcap),("cleanup",ccap)):
        if cap:
            for stream in ("stdout","stderr"):
                with (run/(label+"_"+stream+".bin")).open("xb") as f:f.write(cap.text(stream));f.flush();os.fsync(f.fileno())
    receipt={"status":status,"request_id":g.REQUEST,"nonce":nonce,"pid":os.getpid(),"error":error,"linux":linux,"cleanup":cleanup,
        "primary_returncode":None if primary is None else primary.returncode,"cleanup_returncode":None if cleaner is None else cleaner.returncode,
        "wall_before_final_receipt_io_s":time.monotonic()-ENTRY,"scientific_calls":0,"D_read":False,"retry_allowed":False,
        "requires_external_exit0_and_total_deadline":True,
        "capture_state":{"primary":None if pcap is None else pcap.snapshot(),
                         "cleanup":None if ccap is None else ccap.snapshot()}}
    g.fresh(BASE/"RESULT.json",receipt);g.need(time.monotonic()<deadline,"Final IO exceeded nominal60s; invalidate provisional PASS")
    print(json.dumps(receipt,sort_keys=True),flush=True)
    g.need(time.monotonic()<deadline,"Terminal stdout IO exceeded nominal60s")
    return 0 if status=="PASS_WSL_STDLIB_INTEGRATION_ONCE" else 2
if __name__=="__main__":
    try:sys.exit(main())
    except Exception as e:print(json.dumps({"status":"FAILED_PREFLIGHT_OR_RECEIPT","error":type(e).__name__,"message":str(e)[:1200]}));sys.exit(1)
