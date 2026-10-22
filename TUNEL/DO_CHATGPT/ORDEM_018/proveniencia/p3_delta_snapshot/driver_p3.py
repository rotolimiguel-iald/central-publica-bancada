"""Prepared P3 child. Execution requires the matching coordination receipt and supervisor claim."""
import sys,os,json,hashlib,time,signal,resource,threading,contextlib,math,traceback
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.pycache_prefix=str(ROOT/"UNUSED_BYTECODE_CACHE")
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/"src"))
from prior_transform import FREE,FIXED,PERIODIC,transform,parameters
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fresh(path,raw):
    if path.exists():raise FileExistsError(str(path))
    tmp=path.with_name(path.name+".tmp")
    with tmp.open("xb") as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise OSError("Atomic verification failed")
    os.replace(tmp,path)
def js(path,obj):fresh(path,(json.dumps(obj,indent=2,allow_nan=False)+"\n").encode())
def array_sha(a):
    return hashlib.sha256(a.tobytes(order="C")).hexdigest()
from failure_audit import BudgetStop, FailureAudit
class Counter(list):
    def __init__(self):super().__init__([0,0.,0]);self.lock=threading.RLock()
    def get_lock(self):return self.lock

def main():
    if len(sys.argv)!=3:raise ValueError("Exact contract hash and job id required")
    pin,job_id=sys.argv[1:]
    cp=ROOT/"CONTRATO_P3.json"
    if sha(cp)!=pin:raise ValueError("Contract hash differs")
    c=json.loads(cp.read_text())
    if c["state"]!="PREPARED_NOT_EXECUTED" or job_id not in [j["id"] for j in c["jobs"]]:
        raise ValueError("Unregistered job")
    auth=json.loads((ROOT/"AUTORIZACAO_COORDENACAO.json").read_text())
    if (auth.get("contract_sha256")!=pin or auth.get("action")!="EXECUTE_EXACT_TWO_SYNTHETIC_JOBS"
            or auth.get("jobs")!=[j["id"] for j in c["jobs"]] or auth.get("authorized") is not True):
        raise ValueError("Matching explicit coordination authorization required")
    job=next(j for j in c["jobs"] if j["id"]==job_id)
    out=ROOT/c["execution_directory"]/job_id
    claim=json.loads((out/"CLAIM.json").read_text())
    if claim!={"contract_sha256":pin,"job_id":job_id}:raise ValueError("Supervisor claim differs")
    if (out/"RESULT.json").exists() or (out/"CHILD_STARTED.json").exists():raise FileExistsError("No repeat or resume")
    for rel,p in c["inputs"].items():
        path=(ROOT/rel).resolve()
        if sha(path)!=p["sha256"] or path.stat().st_size!=p["bytes"]:raise ValueError("Input mismatch: "+rel)
    interpreter=json.loads((ROOT/"INTERPRETER_PIN.json").read_text())
    if sha(interpreter["path"])!=interpreter["sha256"]:raise ValueError("Interpreter differs")
    runtime=json.loads((ROOT/"RUNTIME_P3_READONLY.json").read_text())
    for row in runtime["files"]:
        p=Path(row["path"])
        if sha(p)!=row["sha256"] or p.stat().st_size!=row["bytes"]:raise ValueError("Runtime pin mismatch: "+str(p))
    for name in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"):
        if os.environ.get(name)!="1":raise ValueError("One-thread environment required")
    resource.setrlimit(resource.RLIMIT_AS,(c["limits"]["address_space_bytes"],)*2)
    resource.setrlimit(resource.RLIMIT_CPU,(c["limits"]["cpu_soft_s"],c["limits"]["cpu_hard_s"]))
    started=time.perf_counter();cpu0=time.process_time()
    def on_budget(sig,frame):raise BudgetStop("SIGNAL_"+str(sig))
    signal.signal(signal.SIGALRM,on_budget);signal.signal(signal.SIGXCPU,on_budget)
    signal.setitimer(signal.ITIMER_REAL,c["limits"]["wall_soft_s"])
    js(out/"CHILD_STARTED.json",{"at":datetime.now(timezone.utc).isoformat(),"pid":os.getpid(),
                                 "contract_sha256":pin,"job_id":job_id})
    import numpy as np
    import bilby,dynesty
    from dynesty.utils import compute_integrals
    import pseob_source as source
    from synthetic_adapter_v2 import generator
    cfg=json.loads((ROOT/"CONFIG_SYNTHETIC.json").read_text())
    receipt=json.loads((ROOT/c["qualified_result"]).read_text())
    inj=next(x for x in receipt["injections"] if x["label"]==job["label"])
    if inj["truth"]!=job["truth"] or inj["normalization"]!=job["normalization"]:
        raise ValueError("Pinned synthetic target differs")
    archive=ROOT/c["qualified_arrays"]
    allowed_data={str((ROOT/rel).resolve()) for rel in c["inputs"]}
    allowed_data|={str(cp),str(ROOT/"AUTORIZACAO_COORDENACAO.json"),str(out/"CLAIM.json")}
    runtime_paths={str(Path(x["path"]).resolve()) for x in runtime["files"]}
    allowed_data|=runtime_paths
    allowed_data|={str(ROOT/"driver_p3.py"),str(ROOT/"prior_transform.py")}
    audit_paths=set();blocked=[]
    def audit(event,args):
        if event in ("socket.connect","socket.bind","subprocess.Popen","os.system","os.fork","os.forkpty","os.posix_spawn"):
            blocked.append(event);raise PermissionError("P3 forbids network/child execution")
        if event=="open" and not isinstance(args[0],int):
            p=Path(os.fsdecode(args[0])).resolve()
            mode=args[1];flags=args[2] or 0
            write=bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)) or (isinstance(mode,str) and any(x in mode for x in "wax+"))
            inside=p==out or out in p.parents
            if write and not inside:blocked.append(str(p));raise PermissionError("Write outside this synthetic job")
            if not write and not inside and str(p) not in allowed_data:
                blocked.append(str(p));raise PermissionError("Read outside exact synthetic/runtime allowlist")
            audit_paths.add(str(p))
    sys.addaudithook(audit)
    counts=Counter();source.set_cost_counter(counts)
    source.set_deadline(time.time()+c["limits"]["wall_soft_s"]-(time.perf_counter()-started))
    source.set_edom_log(out/"EDOM_LOG.jsonl")
    ll_calls=0;sampler=None;last=None;status="FAILED";error=None;delta=None;ess=None
    failures=FailureAudit();last_parameters=None
    def budget():
        if ll_calls>=c["limits"]["max_likelihood_calls"]:raise BudgetStop("MAXCALL_INCLUDING_INITIALIZATION")
        if time.perf_counter()-started>=c["limits"]["wall_soft_s"]:raise BudgetStop("WALL")
        if time.process_time()>=c["limits"]["cpu_soft_s"]:raise BudgetStop("CPU")
    try:
        with np.load(archive,allow_pickle=False) as a:
            f=np.array(a["frequencies_Hz"]);psd=np.array(a["PSD_analytic_strain2_per_Hz"])
            if f.shape!=(65537,) or not np.array_equal(f,np.fft.rfftfreq(131072,1/4096)):
                raise ValueError("Frequency grid differs")
            mask=(f>=20)&(f<=1024)
            if not np.isfinite(psd[mask]).all() or np.any(psd[mask]<=0) or not np.isinf(psd[~mask]).all():
                raise ValueError("Qualified analytic PSD differs")
            ifos=bilby.gw.detector.InterferometerList(["H1","L1"]);snr2=0.
            for ifo in ifos:
                norm=job["normalization"][ifo.name]
                n=np.array(a[job["label"]+"_"+ifo.name+"_noise_fd"])
                s=np.array(a[job["label"]+"_"+ifo.name+"_signal_fd"]);d=n+s
                for key,arr in (("noise_sha256",n),("signal_sha256",s),("injected_sha256",d)):
                    if array_sha(arr)!=norm[key]:raise ValueError("Synthetic array hash differs: "+key)
                snr2+=4/32*float(np.sum(abs(s[mask])**2/psd[mask]))
                ifo.minimum_frequency=20.;ifo.maximum_frequency=1024.
                ifo.power_spectral_density=bilby.gw.detector.PowerSpectralDensity(frequency_array=f,psd_array=psd)
                ifo.set_strain_data_from_frequency_domain_strain(d,sampling_frequency=4096,duration=32,start_time=999999984.)
            if not np.isclose(math.sqrt(snr2),20.,rtol=1e-8,atol=1e-10):raise ValueError("Qualified SNR differs")
        wf=generator(cfg)
        wf.frequency_domain_source_model=failures.wrap(
            wf.frequency_domain_source_model,lambda:last_parameters,counts)
        likelihood=bilby.gw.likelihood.GravitationalWaveTransient(ifos,wf,
            time_marginalization=False,distance_marginalization=False,phase_marginalization=False,
            calibration_marginalization=False,jitter_time=False,reference_frame="sky",time_reference="geocenter")
        def logl(v):
            nonlocal ll_calls,last_parameters
            last_parameters=parameters(v)
            budget();ll_calls+=1
            value=float(likelihood.log_likelihood_ratio(last_parameters))
            if counts[2]!=0 or not math.isfinite(value) or abs(value)>1e100:
                raise RuntimeError("Native/domain/nonfinite likelihood abort; never a silent prior rejection")
            return value
        rng=np.random.default_rng(job["sampler_seed"])
        sampler=dynesty.NestedSampler(logl,transform,12,nlive=256,bound="multi",sample="rwalk",
            periodic=list(PERIODIC),walks=25,rstate=rng,queue_size=1,pool=None,save_evaluation_history=False)
        for item in sampler.sample(maxcall=c["limits"]["max_likelihood_calls"],dlogz=.1,
                                    add_live=False,save_bounds=False,resume=False):
            last=item
            # Immutable audit record; no checkpoint or resume file.
            if sampler.it%100==0:
                js(out/("PROGRESS_%07d.json"%sampler.it),{"iteration":sampler.it,"calls":ll_calls,
                    "delta_logz":float(item.delta_logz),"native_calls":int(counts[0]),
                    "wall_s":time.perf_counter()-started,"cpu_s":time.process_time()-cpu0})
        if last is None:raise RuntimeError("Sampler returned no dead points")
        delta=float(np.logaddexp(0.,np.max(sampler.live_logl)+last.logvol-last.logz))
        if delta<.1 and np.ptp(sampler.live_logl)>0 and ll_calls<c["limits"]["max_likelihood_calls"]:
            for _ in sampler.add_live_points():pass
            values=compute_integrals(logl=sampler.saved_run["logl"],logvol=sampler.saved_run["logvol"])
            for key,val in zip(("logwt","logz","logzvar","h"),values):sampler.saved_run[key]=val.tolist()
            weights=np.exp(np.array(sampler.saved_run["logwt"])-sampler.saved_run["logz"][-1])
            weights/=sum(weights);ess=float(1/sum(weights**2))
            status="DLOGZ_REACHED_ESS_OK" if ess>=100 else "DLOGZ_REACHED_ESS_LOW"
        else:status="STOPPED_NOT_CONVERGED"
    except BudgetStop as exc:
        status="BUDGET_EXHAUSTED_PARTIAL";error=str(exc)
        failures.external(exc,last_parameters)
    except Exception as exc:
        failures.external(exc,last_parameters)
        status="BUDGET_EXHAUSTED_PARTIAL" if failures.kind_for(exc)=="BUDGET_STOP" else "FAILED"
        error=type(exc).__name__+": "+str(exc)
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        artifact=None
        if sampler is not None and len(sampler.saved_run["logl"]):
            # Partial arrays are diagnostics; no inferred summary is promoted.
            target=out/"SAMPLER_DIAGNOSTICS.npz";tmp=out/"SAMPLER_DIAGNOSTICS.npz.tmp"
            with tmp.open("xb") as fh:
                np.savez(fh,**{k:np.asarray(sampler.saved_run[k]) for k in ("v","logl","logvol","logwt","logz","logzvar")})
            if tmp.stat().st_size<=0:raise OSError("Empty diagnostics")
            os.replace(tmp,target);artifact={"path":target.name,"sha256":sha(target),"bytes":target.stat().st_size}
        result={"status":status,"job_id":job_id,"label":job["label"],"contract_sha256":pin,
                "scope":"Synthetic cost/recovery feasibility only; neither coverage nor a D verdict",
                "error":error,"wall_s":time.perf_counter()-started,"cpu_s":time.process_time()-cpu0,
                "cpu_process_total_s":time.process_time(),"likelihood_calls":ll_calls,
                "native_calls":int(counts[0]),"native_wall_s":float(counts[1]),
                "failure_receipt":failures.summary(counts),
                "delta_logz_before_live_addition":delta,"weighted_ESS":ess,"diagnostics":artifact,
                "filesystem_read_write_paths_after_hook":sorted(audit_paths),"blocked_operations":blocked,
                "audit_scope":"Python open/process/socket hook after fixed imports and pin checks; not OS/native syscall containment",
                "D_read":False,"independent_noise_realizations":False,"coverage_estimated":False,
                "finished_utc":datetime.now(timezone.utc).isoformat()}
        js(out/"RESULT.json",result)
        print(json.dumps({k:result[k] for k in ("status","job_id","likelihood_calls","native_calls","wall_s","cpu_s")}))
    return 2 if status=="FAILED" else 0
if __name__=="__main__":sys.exit(main())
