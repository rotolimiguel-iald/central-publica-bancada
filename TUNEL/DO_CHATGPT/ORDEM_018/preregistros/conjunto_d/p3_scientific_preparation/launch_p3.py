"""One-shot Linux supervisor. Do not run until coordination authorizes the pinned contract."""
import sys,os,json,hashlib,subprocess,time,signal
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
from result_acceptance import assess, campaign_exit
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fresh(path,raw):
    if path.exists():raise FileExistsError(str(path))
    temp=path.with_name(path.name+".tmp")
    with temp.open("xb") as f:f.write(raw)
    if temp.read_bytes()!=raw:raise OSError("Atomic verification failed")
    os.replace(temp,path)
def js(path,obj):fresh(path,(json.dumps(obj,indent=2,allow_nan=False)+"\n").encode())
def main():
    if len(sys.argv)!=3:raise ValueError("Exact contract and external ROOT decision hashes required")
    pin,decision_pin=sys.argv[1:]
    from science_admission import admit
    c,authorization=admit(ROOT,pin,decision_pin)
    auth_path=ROOT/"ROOT_DECISION.json"
    # No automatic retry: reserve the entire collection before any child.
    fd=os.open(ROOT/"CAMPAIGN_CLAIM.json",os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,"wb") as f:
        f.write((json.dumps({"contract_sha256":pin,"decision_sha256":decision_pin,
                            "execution_id":authorization["execution_id"],"pid":os.getpid()})+"\n").encode())
        f.flush();os.fsync(f.fileno())
    run=ROOT/c["execution_directory"];run.mkdir(exist_ok=False)
    js(run/"LAUNCH_STARTED.json",{"contract_sha256":pin,"authorization_sha256":sha(auth_path),
                                  "at":datetime.now(timezone.utc).isoformat(),"pid":os.getpid()})
    env=dict(os.environ,OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1",PYTHONDONTWRITEBYTECODE="1")
    results=[];assessments=[];t0=time.perf_counter()
    for job in c["jobs"]:
        out=run/job["id"];out.mkdir(exist_ok=False)
        js(out/"CLAIM.json",{"contract_sha256":pin,"decision_sha256":decision_pin,
                             "execution_id":authorization["execution_id"],
                             "job_id":job["id"],"supervisor_pid":os.getpid()})
        cmd=["/opt/lal_env/bin/python","-I","-B",str(ROOT/"driver_p3.py"),pin,job["id"],decision_pin]
        start=time.perf_counter()
        with (out/"stdout.log").open("xb") as fo,(out/"stderr.log").open("xb") as fe:
            p=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=fo,stderr=fe,env=env,
                               cwd=str(ROOT),start_new_session=True)
            try:
                rc=p.wait(timeout=c["limits"]["supervisor_wall_s"]);state="PROCESS_RETURNED"
            except subprocess.TimeoutExpired:
                os.killpg(p.pid,signal.SIGKILL);rc=p.wait();state="SUPERVISOR_TIMEOUT_UNCERTAIN_PARTIAL"
        row={"pid":p.pid,"job_id":job["id"],"returncode":rc,"supervisor_status":state,"wall_s":time.perf_counter()-start,
             "stdout_sha256":sha(out/"stdout.log"),"stderr_sha256":sha(out/"stderr.log")}
        rp=out/"RESULT.json"
        result=None;journal=None
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
    js(run/"CAMPAIGN_RECEIPT.json",{"contract_sha256":pin,"jobs":results,"wall_s":time.perf_counter()-t0,
                                    "started_jobs":len(results),"planned_jobs":len(c["jobs"]),"no_retry":True,
                                    "exit_code":campaign_exit(assessments,len(c["jobs"])),
                                    "status":"CLEAN_PROTOCOL_COMPLETION" if campaign_exit(assessments,len(c["jobs"]))==0 else "TERMINAL_FAILURE_OR_INCOMPLETE",
                                    "coverage_claim":False,"D_read_authorized":False,
                                    "scientific_qualification":False,
                                    "scope":"Operational completion may accept clean partials; not F3 qualification",
                                    "preparation_id":c["preparation_id"],
                                    "execution_id":authorization["execution_id"],"decision_sha256":decision_pin})
    print(json.dumps(results))
    return campaign_exit(assessments,len(c["jobs"]))
if __name__=="__main__":sys.exit(main())
