"""One-shot Linux supervisor. Do not run until coordination authorizes the pinned contract."""
import sys,os,json,hashlib,subprocess,time,signal
from pathlib import Path
from datetime import datetime,timezone
from result_acceptance import assess, campaign_exit
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fresh(path,raw):
    if path.exists():raise FileExistsError(str(path))
    temp=path.with_name(path.name+".tmp")
    with temp.open("xb") as f:f.write(raw)
    if temp.read_bytes()!=raw:raise OSError("Atomic verification failed")
    os.replace(temp,path)
def js(path,obj):fresh(path,(json.dumps(obj,indent=2,allow_nan=False)+"\n").encode())
def main():
    raise RuntimeError("PREPARATION_ONLY: no runnable campaign contract or execution permission")
    if len(sys.argv)!=2:raise ValueError("Exact contract SHA256 required")
    cp=ROOT/"CONTRATO_P3.json";pin=sys.argv[1]
    if sha(cp)!=pin:raise ValueError("Contract mismatch")
    c=json.loads(cp.read_text());auth_path=ROOT/"AUTORIZACAO_COORDENACAO.json"
    auth=json.loads(auth_path.read_text())
    if (auth.get("authorized") is not True or auth.get("contract_sha256")!=pin
        or auth.get("action")!="EXECUTE_EXACT_TWO_SYNTHETIC_JOBS"
        or auth.get("jobs")!=[j["id"] for j in c["jobs"]]):raise ValueError("Matching coordination receipt required")
    if Path(sys.executable).absolute()!=Path("/opt/lal_env/bin/python").absolute():
        raise ValueError("Pinned WSL environment required")
    for rel,p in c["inputs"].items():
        path=(ROOT/rel).resolve()
        if sha(path)!=p["sha256"] or path.stat().st_size!=p["bytes"]:raise ValueError("Input mismatch: "+rel)
    run=ROOT/c["execution_directory"];run.mkdir(exist_ok=False)
    js(run/"LAUNCH_STARTED.json",{"contract_sha256":pin,"authorization_sha256":sha(auth_path),
                                  "at":datetime.now(timezone.utc).isoformat(),"pid":os.getpid()})
    env=dict(os.environ,OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1",PYTHONDONTWRITEBYTECODE="1")
    results=[];assessments=[];t0=time.perf_counter()
    for job in c["jobs"]:
        out=run/job["id"];out.mkdir(exist_ok=False)
        js(out/"CLAIM.json",{"contract_sha256":pin,"job_id":job["id"]})
        cmd=["/opt/lal_env/bin/python","-I","-B",str(ROOT/"driver_p3.py"),pin,job["id"]]
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
                                    "coverage_claim":False,"D_read_authorized":False})
    print(json.dumps(results))
    return campaign_exit(assessments,len(c["jobs"]))
if __name__=="__main__":sys.exit(main())
