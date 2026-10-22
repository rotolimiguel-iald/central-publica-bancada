"""Prepared supervisor: one pure child, no authorization supplied by this file."""
from pathlib import Path
import os, sys, json, time, hashlib, subprocess, datetime, threading, uuid
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\preregistros\conjunto_d\guard_doubles_run_preparation")
REQUEST = "83bed917-9a88-4505-a26c-0bb75e2f7c86"
LIMIT = 65536
def require(ok, message):
    if not ok: raise RuntimeError(message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read_json(p): return json.loads(p.read_bytes())
def exclusive_json(p, obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode()
    with p.open("xb") as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    require(p.read_bytes()==data,"durable write verification")
def atomic_new(p,obj):
    require(not p.exists(),"Existing output: "+str(p))
    tmp=p.with_name(p.name+".new")
    exclusive_json(tmp,obj)
    os.replace(tmp,p)
class Capture:
    def __init__(self, pipe, overflow):
        self.pipe=pipe; self.buf=bytearray(); self.total=0
        self.overflow=overflow; self.error=None
        self.thread=threading.Thread(target=self.read,daemon=True)
    def read(self):
        try:
            while True:
                b=os.read(self.pipe.fileno(),4096)
                if not b: break
                self.total+=len(b)
                self.buf.extend(b[:max(0,LIMIT-len(self.buf))])
                if self.total>LIMIT: self.overflow.set()
        except BaseException as exc:
            self.error=type(exc).__name__+": "+str(exc)
    def snapshot(self):
        return {"text":bytes(self.buf).decode("utf-8",errors="replace"),
                "bytes_seen":self.total,"retained_bytes":len(self.buf),
                "truncated":self.total>LIMIT,"reader_error":self.error,
                "reader_alive":self.thread.is_alive()}
def main():
    require(sys.argv[1:]==["--run-once"],"Only --run-once")
    require(Path(__file__).resolve()==BASE/"supervisor.py","Fixed path identity")
    cp=BASE/"CONTRATO_DOUBLES.json"; c=read_json(cp)
    auth=read_json(BASE/"AUTORIZACAO_ROOT.json")
    require(auth["authorized"] is True and auth["request_id"]==REQUEST,"Authorization identity")
    require(auth["scope"]=="AUDIT_GUARD_21_PURE_DOUBLES_ONLY_ONCE","Authorization scope")
    require(auth["contract_sha256"]==digest(cp),"Authorization contract pin")
    require(auth["max_execution_count"]==1 and auth["max_wall_seconds"]==30 and auth["worker_threads"]==1,"Authorization limits")
    rev=auth["independent_review"]; rp=Path(rev["path"]).resolve()
    require(rp.is_relative_to(BASE.parents[2]) and rp.suffix in (".md",".json"),"Review path")
    require(rev["accepted_for_this_execution"] is True and digest(rp)==rev["sha256"],"Pinned review")
    require(c["request_id"]==REQUEST and len(c["test_names"])==21,"Prepared identity")
    require(Path(sys.executable).resolve()==Path(c["interpreter"]).resolve(),"Interpreter identity")
    for pin in c["execution_pins"]:
        p=Path(pin["path"])
        require(p.stat().st_size==pin["bytes"] and digest(p)==pin["sha256"],"Pin mismatch: "+str(p))
    require(not (BASE/"CLAIM.json").exists() and not (BASE/"RUN").exists(),"Consumed/uncertain identity; no retry")
    run=BASE/"RUN"; run.mkdir()
    claim={"request_id":REQUEST,"pid_supervisor":os.getpid(),"nonce":str(uuid.uuid4()),
           "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "contract_sha256":digest(cp),"authorization_sha256":digest(BASE/"AUTORIZACAO_ROOT.json"),
           "scope":c["scope"],"retry_allowed":False}
    exclusive_json(BASE/"CLAIM.json",claim)
    # Preflight/CLAIM precede this one nominal clock; startup and collection share it.
    started=time.monotonic(); total_deadline=started+30; work_deadline=started+25
    child=None; captures=[]; status="FAILED"; detail={}; overflow=threading.Event()
    try:
        env=os.environ.copy()
        for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
            env[k]="1"
        env["PYTHONDONTWRITEBYTECODE"]="1"
        argv=[sys.executable,"-I","-S","-B","-X","utf8",str(BASE/"worker.py"),"--supervised-stdin"]
        child=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                               env=env,cwd=str(BASE),creationflags=subprocess.CREATE_NO_WINDOW)
        captures=[Capture(child.stdout,overflow),Capture(child.stderr,overflow)]
        for cap in captures: cap.thread.start()
        atomic_new(run/"PROCESS.json",dict(claim,pid_worker=child.pid,argv=argv,
                    deadline_work_monotonic=work_deadline,deadline_total_monotonic=total_deadline))
        child.stdin.write((json.dumps({"request_id":REQUEST,"nonce":claim["nonce"]})+"\n").encode())
        child.stdin.close()
        while child.poll() is None:
            require(not overflow.is_set(),"OUTPUT_LIMIT")
            remaining=work_deadline-time.monotonic()
            require(remaining>0,"WORK_DEADLINE_TIMEOUT_NO_RETRY")
            try: child.wait(timeout=min(0.05,remaining))
            except subprocess.TimeoutExpired: pass
        detail["returncode"]=child.returncode
    except BaseException as exc:
        detail["failure"]={"type":type(exc).__name__,"message":str(exc)}
    # No new cleanup budget. Never communicate()/wait() without the common deadline.
    if child is not None and child.poll() is None:
        try: child.kill(); detail["kill_requested"]=True
        except BaseException as exc: detail["kill_error"]=str(exc)
    if child is not None and child.poll() is None:
        remain=max(0,total_deadline-time.monotonic())
        if remain:
            try: child.wait(timeout=remain)
            except BaseException as exc: detail["collection_error"]=str(exc)
    for cap in captures: cap.thread.join(timeout=max(0,total_deadline-time.monotonic()))
    snapshots=[cap.snapshot() for cap in captures]
    if child is None:
        detail.setdefault("failure",{"message":"NO_WORKER_CREATED"})
    elif child.poll() is None or any(x["reader_alive"] for x in snapshots):
        status="PROCESS_STATE_UNCERTAIN"
    elif "failure" not in detail:
        try:
            require(not overflow.is_set() and all(not x["reader_error"] for x in snapshots),"Capture error/overflow")
            require(child.returncode==0,"Worker nonzero")
            result=json.loads(snapshots[0]["text"])
            require(result["request_id"]==REQUEST and result["status"]=="PASS","Worker failure/identity")
            require(result["tests_run"]==21 and result["test_names"]==c["test_names"],"Exact21 tests")
            require(result["guard_denials"]==[] and result["unexpected_or_skipped"]==0,"Guard/test status")
            require(time.monotonic()<=total_deadline,"TOTAL_NOMINAL_DEADLINE")
            status="PASS";detail["worker"]=result
        except BaseException as exc: detail["failure"]={"type":type(exc).__name__,"message":str(exc)}
    elapsed=time.monotonic()-started
    if elapsed>30 and status=="PASS": status="FAILED";detail["failure"]={"message":"TOTAL_NOMINAL_DEADLINE"}
    atomic_new(run/"RESULT.json",{"request_id":REQUEST,"status":status,"wall_including_collection_s":elapsed,
        "nominal_total_s":30,"work_s":25,"collection_reserve_inside_total_s":5,
        "clock_start":"after durable CLAIM, before environment/Popen",
        "OS_hard_realtime_guarantee":False,"pid_supervisor":os.getpid(),
        "pid_worker":child.pid if child else None,"returncode":child.poll() if child else None,
        "stdout":snapshots[0] if snapshots else None,"stderr":snapshots[1] if snapshots else None,
        "detail":detail,"retry_allowed":False,"science_executed":False})
    return 0 if status=="PASS" else (2 if status=="PROCESS_STATE_UNCERTAIN" else 1)
if __name__=="__main__": sys.exit(main())
