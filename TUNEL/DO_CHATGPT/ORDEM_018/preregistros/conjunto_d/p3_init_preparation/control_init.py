"""Initialization-only control, PREPARED. No waveform/likelihood evaluation or sampler."""
import sys,os,json,hashlib,time,signal,resource,functools,inspect,math
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BASE=(ROOT/"../p3_codec_002").resolve()
sys.dont_write_bytecode=True
sys.pycache_prefix=str(ROOT/"UNUSED_BYTECODE_CACHE")
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/"src"));sys.path.insert(0,str(ROOT))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def fresh(path,raw):
    if path.exists():raise FileExistsError(str(path))
    tmp=path.with_name(path.name+".tmp")
    with tmp.open("xb") as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise OSError("Atomic write differs")
    os.replace(tmp,path)
def js(path,obj):fresh(path,(json.dumps(obj,indent=2,allow_nan=False)+"\n").encode())
def pincheck(path,row):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=row["sha256"] or len(raw)!=row["bytes"]:
        raise ValueError("Pin mismatch: "+str(path))
def digest(array):return hashlib.sha256(array.tobytes(order="C")).hexdigest()

def main():
    if len(sys.argv)!=2:raise ValueError("Exact control contract hash required")
    os.chdir(ROOT)
    cp=ROOT/"CONTRATO_CONTROLE_INIT.json";contract_hash=sys.argv[1]
    if sha(cp)!=contract_hash:raise ValueError("Contract pin mismatch")
    c=json.loads(cp.read_text())
    decision_path=ROOT/"DECISAO_CONTROLE_INIT.json"
    decision=json.loads(decision_path.read_text())
    if (decision.get("authorized") is not True or decision.get("action")!="QUALIFY_INITIALIZATION_ONLY"
        or decision.get("contract_sha256")!=contract_hash or decision.get("alternative")!=c["selected_alternative"]):
        raise ValueError("Specific ROOT decision for this non-PE control required")
    if c["state"]!="PREPARED_NOT_EXECUTED" or c["selected_alternative"]!="B":raise ValueError("Unregistered alternative")
    if Path(sys.executable).absolute()!=Path("/opt/lal_env/bin/python"):raise ValueError("Fixed interpreter invocation")
    for rel,row in c["inputs"].items():pincheck((ROOT/rel).resolve(),row)
    runtime=json.loads((BASE/"RUNTIME_P3_READONLY.json").read_text())
    for row in runtime["files"]:pincheck(row["path"],row)
    for row in c["runtime_initialization_dependencies"]:pincheck(row["runtime_path"],row)
    interpreter=json.loads((BASE/"INTERPRETER_PIN.json").read_text());pincheck(interpreter["path"],interpreter)
    for name in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"):
        if os.environ.get(name)!="1":raise ValueError("One-thread environment required")
    # No scientific job, campaign, CLAIM or authorization file is created here.
    out=ROOT/c["output_directory"];out.mkdir(exist_ok=False)
    js(out/"STARTED.json",{"pid":os.getpid(),"contract_sha256":contract_hash,
        "decision_sha256":sha(decision_path),"at":datetime.now(timezone.utc).isoformat(),"kind":"INITIALIZATION_ONLY"})
    resource.setrlimit(resource.RLIMIT_AS,(c["limits"]["address_space_bytes"],)*2)
    resource.setrlimit(resource.RLIMIT_CPU,(c["limits"]["cpu_soft_s"],c["limits"]["cpu_hard_s"]))
    started=time.perf_counter();cpu0=time.process_time()
    def on_limit(sig,frame):raise RuntimeError("INITIALIZATION_CONTROL_LIMIT_"+str(sig))
    signal.signal(signal.SIGALRM,on_limit);signal.signal(signal.SIGXCPU,on_limit)
    signal.setitimer(signal.ITIMER_REAL,c["limits"]["wall_s"])
    counters={"waveform_attempts":0,"likelihood_evaluation_attempts":0,"sampler_attempts":0,"source_attempts":0}
    native_counts=[0,0.,0];paths=set();blocked=[];rows=[];stage="fixed_imports";status="FAILED";error=None
    def deny(kind,original):
        @functools.wraps(original)
        def forbidden(*args,**kwargs):
            counters[kind]+=1
            raise RuntimeError("Forbidden scientific evaluation in initialization control: "+kind)
        forbidden.__signature__=inspect.signature(original)
        return forbidden
    try:
        # Same fixed bootstrap as the P3 driver, omitting Dynesty import/use.
        import numpy as np
        import bilby
        import pseob_source as source
        import synthetic_adapter_v2 as adapter
        from init_detectors import build_B,verify_analytic_state
        from preload_npz_codec import preload_npz_codec
        preload_npz_codec(json.loads((BASE/"CODEC_CP437_PIN.json").read_text()))
        cfg=json.loads((BASE/"CONFIG_SYNTHETIC.json").read_text())
        science=json.loads((BASE/"CONTRATO_P3.json").read_text())
        receipt=json.loads((BASE/science["qualified_result"]).read_text())
        geometry=json.loads((ROOT/"GEOMETRIA_PINADA.json").read_text())
        dependency=json.loads((ROOT/"DEPENDENCIA_FACTORY_PIN.json").read_text())
        archive=(BASE/science["qualified_arrays"]).resolve()
        source.set_cost_counter(native_counts)
        # Guard the actual imported source references and model signature.
        source.pseob_frequency_domain=deny("source_attempts",source.pseob_frequency_domain)
        adapter.pseob_frequency_domain=deny("source_attempts",adapter.pseob_frequency_domain)
        source_signature=str(inspect.signature(adapter.synthetic_only220))
        source_args=inspect.getfullargspec(adapter.synthetic_only220).args
        adapter.synthetic_only220=deny("source_attempts",adapter.synthetic_only220)
        W=bilby.gw.WaveformGenerator
        for name in ("frequency_domain_strain","time_domain_strain","_calculate_strain","_strain_from_model","_strain_from_transformed_model"):
            setattr(W,name,deny("waveform_attempts",getattr(W,name)))
        L=bilby.gw.likelihood.GravitationalWaveTransient
        for name in ("log_likelihood","log_likelihood_ratio","noise_log_likelihood","_calculate_noise_log_likelihood","calculate_snrs"):
            setattr(L,name,deny("likelihood_evaluation_attempts",getattr(L,name)))
        bilby.run_sampler=deny("sampler_attempts",bilby.run_sampler)
        allowed={str((ROOT/rel).resolve()) for rel in c["inputs"]}
        allowed|={str(Path(row["path"]).resolve()) for row in runtime["files"]}
        allowed|={str(Path(row["runtime_path"]).resolve()) for row in c["runtime_initialization_dependencies"]}
        # Only the one named installed ASD is additional; no directory grant.
        writable={str(out/name) for name in ("RESULT.json","RESULT.json.tmp","EDOM_LOG.jsonl")}
        def audit(event,args):
            if event in ("socket.connect","socket.bind","subprocess.Popen","os.system","os.fork","os.forkpty","os.posix_spawn"):
                blocked.append(event);raise PermissionError("Control forbids network/child process")
            if event=="open" and not isinstance(args[0],int):
                p=str(Path(os.fsdecode(args[0])).resolve());mode=args[1];flags=args[2] or 0
                write=bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)) or (isinstance(mode,str) and any(x in mode for x in "wax+"))
                if (write and p not in writable) or (not write and p not in allowed and p not in writable):
                    blocked.append(p);raise PermissionError("Outside exact initialization allowlist")
                paths.add(p)
        sys.addaudithook(audit)
        stage="NPZ_and_detectors"
        source.set_edom_log(out/"EDOM_LOG.jsonl")
        with np.load(archive,allow_pickle=False) as a:
            f=np.array(a["frequencies_Hz"]);psd=np.array(a["PSD_analytic_strain2_per_Hz"])
            if f.shape!=(65537,) or not np.array_equal(f,np.fft.rfftfreq(131072,1/4096)):
                raise ValueError("Qualified frequency grid differs")
            mask=(f>=20)&(f<=1024)
            if not np.isfinite(psd[mask]).all() or np.any(psd[mask]<=0) or not np.isinf(psd[~mask]).all():
                raise ValueError("Qualified analytic PSD differs")
            for job in science["jobs"]:
                stage="detectors_"+job["label"]
                inj=next(x for x in receipt["injections"] if x["label"]==job["label"])
                if inj["truth"]!=job["truth"] or inj["normalization"]!=job["normalization"]:
                    raise ValueError("Synthetic identity differs")
                ifos,before=build_B(bilby,f,psd,geometry,dependency);snr2=0.;detector_rows=[]
                for ifo in ifos:
                    norm=job["normalization"][ifo.name]
                    n=np.array(a[job["label"]+"_"+ifo.name+"_noise_fd"])
                    s=np.array(a[job["label"]+"_"+ifo.name+"_signal_fd"]);d=n+s
                    for key,arr in (("noise_sha256",n),("signal_sha256",s),("injected_sha256",d)):
                        if digest(arr)!=norm[key]:raise ValueError("Qualified synthetic array changed: "+key)
                    snr2+=4/32*float(np.sum(abs(s[mask])**2/psd[mask]))
                    ifo.set_strain_data_from_frequency_domain_strain(d,sampling_frequency=4096,duration=32,start_time=999999984.)
                    detector_rows.append(verify_analytic_state(np,ifo,f,psd,geometry))
                    if not np.array_equal(ifo.strain_data.frequency_domain_strain,d):
                        raise ValueError("Stored synthetic strain differs")
                if not np.isclose(math.sqrt(snr2),20.,rtol=1e-8,atol=1e-10):raise ValueError("Qualified SNR changed")
                stage="construct_generator_and_likelihood_"+job["label"]
                wf=adapter.generator(cfg)
                if inspect.getfullargspec(wf.frequency_domain_source_model).args!=source_args:
                    raise ValueError("Bilby getfullargspec source arguments changed")
                if wf.source_parameter_keys!=set(source_args[1:]):raise ValueError("Source parameter keys changed")
                if str(inspect.signature(wf.frequency_domain_source_model))!=source_signature:
                    raise ValueError("Source signature changed")
                if not np.array_equal(wf.frequency_array,f):raise ValueError("Generator grid differs")
                likelihood=L(ifos,wf,time_marginalization=False,distance_marginalization=False,
                    phase_marginalization=False,calibration_marginalization=False,jitter_time=False,
                    reference_frame="sky",time_reference="geocenter")
                if likelihood.waveform_generator is not wf or likelihood.reference_ifo is not None:
                    raise ValueError("Unexpected likelihood constructor state")
                for ifo in likelihood.interferometers:verify_analytic_state(np,ifo,f,psd,geometry)
                if likelihood._noise_log_likelihood_value is not None:raise ValueError("Noise likelihood evaluated")
                if any((likelihood.time_marginalization,likelihood.distance_marginalization,
                        likelihood.phase_marginalization,likelihood.calibration_marginalization,likelihood.jitter_time)):
                    raise ValueError("Marginalization changed")
                if wf._cache["waveform"] is not None:raise ValueError("Waveform cache was populated")
                rows.append({"synthetic_label":job["label"],"detectors":detector_rows,
                    "default_initialization_only":before,"SNR_from_pinned_arrays":math.sqrt(snr2),
                    "generator_created_no_waveform":True,"likelihood_created_no_evaluation":True,
                    "source_signature_preserved":True,"PSD_rechecked_after_likelihood_constructor":True})
        if any(counters.values()) or native_counts!=[0,0.,0]:raise ValueError("Scientific evaluation attempted")
        if blocked:raise ValueError("A blocked read was swallowed by the library")
        status="INITIALIZATION_ONLY_PASS";stage="boundary_before_first_evaluation"
    except Exception as exc:
        error={"type":type(exc).__module__+"."+type(exc).__qualname__,"message":str(exc)}
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        js(out/"RESULT.json",{"status":status,"stage":stage,"error":error,"contract_sha256":contract_hash,
            "wall_s":time.perf_counter()-started,"CPU_s":time.process_time()-cpu0,"CPU_process_total_s":time.process_time(),
            "counters":counters,"source_native_counter":native_counts,"rows":rows,
            "filesystem_paths_after_hook":sorted(paths),"blocked_operations":blocked,
            "scientific_PE_jobs":0,"D_read":False,"coverage_claim":False,"permission_for_P3":False,
            "audit_scope":"Fixed imports precede exact-file hook; not OS/native syscall containment.",
            "finished_utc":datetime.now(timezone.utc).isoformat()})
    return 0 if status=="INITIALIZATION_ONLY_PASS" else 2
if __name__=="__main__":sys.exit(main())
