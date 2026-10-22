"""Prepared single-use supervisor. No authorization is supplied by preparation."""
from pathlib import Path
import os,sys,json,time,hashlib,subprocess,datetime

BASE=Path(__file__).resolve().parent
REQUEST="8b53f7c0-9f5f-49e1-87bc-cf73a7e1f79d"
def read_json(p):return json.loads(p.read_bytes())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def atomic_new(p,obj):
    require(not p.exists(),"Existing output must not be replaced: "+str(p))
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode()
    tmp=p.with_suffix(p.suffix+".tmp")
    with tmp.open("xb") as f:f.write(data)
    require(tmp.read_bytes()==data,"write verification")
    os.replace(tmp,p)
def partial_text(value):
    if value is None:return ""
    return value.decode("utf-8",errors="replace") if isinstance(value,bytes) else value
def collect_within_deadline(child,deadline_total):
    """Never allocate a fresh cleanup budget. Every failure is returned as evidence."""
    evidence={"kill_requested":False,"reaped":False,"state":"PROCESS_STATE_UNCERTAIN"}
    stdout="";stderr=""
    try:
        if child.poll() is None:
            evidence["kill_requested"]=True
            child.kill()
        remaining=deadline_total-time.monotonic()
        evidence["remaining_s_before_collect"]=max(0,remaining)
        if remaining<=0:
            evidence["failure"]="NO_TOTAL_DEADLINE_REMAINING_FOR_COLLECTION"
            evidence["returncode"]=child.poll()
            return evidence,stdout,stderr
        try:
            stdout,stderr=child.communicate(timeout=remaining)
        except subprocess.TimeoutExpired as exc:
            evidence["failure"]="COLLECTION_TIMEOUT_PROCESS_STATE_UNCERTAIN"
            evidence["returncode"]=child.poll()
            return evidence,partial_text(exc.output),partial_text(exc.stderr)
        evidence["returncode"]=child.poll()
        evidence["reaped"]=evidence["returncode"] is not None
        evidence["state"]="COLLECTED" if evidence["reaped"] else "PROCESS_STATE_UNCERTAIN"
        return evidence,stdout,stderr
    except Exception as exc:
        evidence["failure"]={"type":type(exc).__name__,"message":str(exc)}
        return evidence,stdout,stderr
def main():
    require(sys.argv[1:]==["--run-once"],"Only exact --run-once command")
    contract_path=BASE/"PROTOCOLO_EXATO.json"
    contract=read_json(contract_path)
    auth=read_json(BASE/"AUTORIZACAO_ROOT.json")
    require(auth["request_id"]==REQUEST and auth["contract_sha256"]==digest(contract_path),"Identity mismatch")
    require(auth["authorized"] is True and auth["scope"]=="C01_C08_SYNTHETIC_ONLY_ONCE","Missing explicit scope")
    require(auth["max_execution_count"]==1 and auth["max_wall_seconds"]==30 and auth["worker_threads"]==1,"Limits mismatch")
    review=auth["independent_proof_review"]
    rp=Path(review["path"]).resolve()
    review_root=BASE.parent.parent/"derivacoes"
    require(rp.is_relative_to(review_root.resolve()) and rp.suffix in (".json",".md"),"Review path outside admitted review area")
    require(review["accepted_for_these_controls"] is True and digest(rp)==review["sha256"],"Proof review not accepted/pinned")
    for pin in contract["execution_pins"]:
        p=Path(pin["path"])
        require(p.is_file() and p.stat().st_size==pin["bytes"] and digest(p)==pin["sha256"],"Pin mismatch: "+str(p))
    require(contract["request_id"]==REQUEST and len(contract["cases"])==8,"Prepared contract mismatch")
    run=BASE/"RUN"
    require(not run.exists(),"RUN already exists; never retry uncertain identity")
    run.mkdir()
    # Prevalidation and exclusive identity persistence precede the nominal run budget.
    claim={"request_id":REQUEST,"pid_supervisor":os.getpid(),"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"contract_sha256":digest(contract_path)}
    atomic_new(BASE/"CLAIM.json",claim)
    # One monotonic deadline begins here, before environment setup/Popen.
    # Five seconds for collection are reserved INSIDE these thirty seconds.
    started=time.monotonic()
    deadline_total=started+30
    deadline_work=deadline_total-5
    child=None;collected=False
    env=os.environ.copy()
    for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
        env[key]="1"
    env["PYTHONDONTWRITEBYTECODE"]="1"
    status="FAILED";detail={};stdout="";stderr=""
    try:
        child=subprocess.Popen([sys.executable,"-I","-B",str(BASE/"controls.py"),"--supervised-stdin"],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8",env=env,
            creationflags=subprocess.CREATE_NO_WINDOW)
        atomic_new(run/"PROCESS.json",dict(claim,pid_worker=child.pid,argv=[sys.executable,"-I","-B",str(BASE/"controls.py"),"--supervised-stdin"],
            deadline_total_monotonic=deadline_total,deadline_work_monotonic=deadline_work))
        remaining=deadline_work-time.monotonic()
        require(remaining>0,"startup consumed work deadline")
        stdout,stderr=child.communicate(json.dumps({"request_id":REQUEST,"authorized":True}),timeout=remaining)
        collected=True
        require(len(stdout.encode())<=4*1024*1024 and len(stderr.encode())<=65536,"output budget")
        data=json.loads(stdout)
        require(child.returncode==0 and data["status"]=="PASS","worker terminal failure")
        require(data["request_id"]==REQUEST and [r.get("id") for r in data["results"]]==[c["id"] for c in contract["cases"]],"result case identities")
        require(time.monotonic()<=deadline_total,"total wall deadline exceeded")
        status="PASS";detail={"worker":data}
    except Exception as exc:
        detail={"failure":{"type":type(exc).__name__,"message":str(exc)}}
        if isinstance(exc,subprocess.TimeoutExpired):
            stdout=partial_text(exc.output);stderr=partial_text(exc.stderr)
            detail["failure"]["classification"]="WORK_DEADLINE_TIMEOUT_NO_RETRY"
        if child is not None and not collected:
            cleanup,new_stdout,new_stderr=collect_within_deadline(child,deadline_total)
            detail["collection"]=cleanup
            stdout=new_stdout or stdout;stderr=new_stderr or stderr
            if cleanup["state"]=="PROCESS_STATE_UNCERTAIN":
                status="PROCESS_STATE_UNCERTAIN"
    # Persist terminal uncertainty even if OS scheduling/collection overshot the nominal deadline.
    # Receipt writing is attempted immediately; no additional wait/retry budget is granted.
    elapsed=time.monotonic()-started
    if elapsed>30 and status=="PASS":
        status="FAILED";detail["failure"]="TOTAL_NOMINAL_DEADLINE_EXCEEDED"
    atomic_new(run/"RESULT.json",{"request_id":REQUEST,"status":status,"wall_including_cleanup_s":elapsed,
        "nominal_total_budget_s":30,"budget_start":"after exclusive CLAIM persistence, before environment setup/Popen",
        "deadline_total_monotonic":deadline_total,"deadline_work_monotonic":deadline_work,"OS_timing_guarantee":False,
        "pid_supervisor":os.getpid(),"pid_worker":child.pid if child else None,"returncode":child.returncode if child else None,
        "stdout":stdout,"stderr":stderr,"detail":detail,"scientific_observed_data":False,"retry_allowed":False})
    return 0 if status=="PASS" else (2 if status=="PROCESS_STATE_UNCERTAIN" else 1)
if __name__=="__main__":
    sys.exit(main())
