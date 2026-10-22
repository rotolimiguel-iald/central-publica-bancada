"""P1/P2 qualification only. No likelihood, sampler, D files or original execution."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,itertools,json,math,os,sys,time,traceback,threading
ROOT=Path(__file__).resolve().parent
CONTRACT=ROOT/"CONTRATO_P0_P2_V2.json"
contract_raw=CONTRACT.read_bytes();contract=json.loads(contract_raw)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for rel,pin in contract["inputs"].items():
    assert digest(ROOT/rel)==pin["sha256"],"Input changed: "+rel
runtime_pins=json.loads((ROOT/"ENVIRONMENT_NATIVE_HASHES.json").read_text())
for row in runtime_pins["files"]:assert digest(row["path"])==row["sha256"],"Runtime changed: "+row["path"]
assert contract["PE_authorized"] is False and contract["D_read_authorized"] is False
assert contract["max_native_calls"]==26 and contract["run_id"]=="RUN_002"
run=ROOT/contract["run_id"];run.mkdir(exist_ok=False)
cfg=json.loads((ROOT/"CONFIG_SYNTHETIC.json").read_text())
sys.path.insert(0,str(ROOT/"src"))
import numpy as np
import lal,lalsimulation as ls,bilby
import synthetic_adapter_v2 as ad
import pseob_source as source
import temporal_contract as temporal
assert Path(source.__file__).resolve()==ROOT/"src/pseob_source.py"
assert Path(temporal.__file__).resolve()==ROOT/"src/temporal_contract.py"
bilby.core.utils.logger.setLevel("ERROR")
started=time.perf_counter();cpu_started=time.process_time()
controls=[];blocked=[];filesystem=[];trace=[];native_dictionaries=[]
class Counter(list):
    def __init__(self):super().__init__([0,0.0,0]);self.lock=threading.Lock()
    def get_lock(self):return self.lock
counter=Counter()
source.set_deadline(time.time()+contract["max_wall_seconds"])
source.set_cost_counter(counter)
source.set_edom_log(run/"EDOM_LOG.jsonl")
runtime_roots=[Path(sys.prefix).resolve(),Path("/usr/lib"),Path("/usr/local/lib"),Path("/lib"),
               Path("/usr/share/zoneinfo")]
def inside(p,root):return p==root or root in p.parents
def audit(event,args):
    if event in ("socket.connect","socket.connect_ex","subprocess.Popen","os.system"):
        blocked.append({"event":event,"reason":"no network/process launch permitted in qualification child"})
        raise PermissionError("Synthetic isolation blocks "+event)
    if event=="open" and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0])).resolve()
        mode=args[1] if len(args)>1 else "r";flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
        writing=(isinstance(mode,str) and any(c in mode for c in "wax+")) or bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        permitted=inside(p,run) if writing else (inside(p,ROOT) or any(inside(p,r) for r in runtime_roots) or p in (Path("/dev/null"),Path("/etc/localtime")))
        if str(p).startswith("/mnt/"):filesystem.append({"path":str(p),"write":writing,"allowed":permitted})
        if not permitted:
            blocked.append({"event":event,"path":str(p),"write":writing})
            raise PermissionError("Synthetic file allowlist blocks "+str(p))
sys.addaudithook(audit)
def atomic_json(path,obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()
    assert inside(path.resolve(),run) and not path.exists()
    tmp=path.with_name(path.name+".tmp");tmp.write_bytes(raw);assert tmp.read_bytes()==raw
    os.replace(tmp,path)
def ahash(a):return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def check(name,fn):
    t=time.perf_counter()
    try:
        detail=fn()
        controls.append({"name":name,"passed":True,"detail":detail,"wall_seconds":time.perf_counter()-t})
    except Exception as exc:
        controls.append({"name":name,"passed":False,"error":type(exc).__name__+": "+str(exc),"wall_seconds":time.perf_counter()-t})
def rejects(fn):
    try:fn()
    except (ValueError,PermissionError,KeyError):return "rejected as required"
    raise AssertionError("Forbidden case was accepted")
def mutated_cfg(key,value):
    x=copy.deepcopy(cfg);x[key]=value;return x
def base_truth(fixture):
    row=contract["fixtures"][fixture]
    return dict(mass_1=row["mass_1"],mass_2=row["mass_2"],chi_1=row["chi_1"],chi_2=row["chi_2"],
                luminosity_distance=1000.0,dtau220=0.0,**ad.FIXED,**cfg["geometry"])
truth=base_truth("SYN_A")
result={"status":"STARTED","at":datetime.now(timezone.utc).isoformat(),"contract_sha256":hashlib.sha256(contract_raw).hexdigest(),
        "scope":"Synthetic P1/P2 qualification only; no PE or D","controls":controls,"native_trace":trace,"PE_calls":0}
old_run_sampler=bilby.run_sampler
def no_pe(*args,**kwargs):result["PE_calls"]+=1;raise PermissionError("PE not authorized in P0-P2")
bilby.run_sampler=no_pe
try:
    print("P1 static/signature/isolation controls started",flush=True)
    check("accept_numeric_fixed_zero_priors",lambda:ad.validate_truth(cfg,truth))
    check("source_signature_has_only220_controlled_deformation",lambda:{"wrapper":str(__import__("inspect").signature(ad.synthetic_only220))})
    for k,val in [("data",{"path":"/mnt/c/NO_SCIENTIFIC_INPUT"}),("event","GW_FORBIDDEN"),
                  ("mode","REAL_OFFSOURCE"),("fixture_ids",["GW_FORBIDDEN"]),("psd_kind","FILE")]:
        check("reject_config_"+k,lambda k=k,val=val:rejects(lambda:ad.validate_config(mutated_cfg(k,val))))
    for k in ad.FIXED:
        bad=dict(truth);bad[k]=0.01
        check("reject_nonzero_"+k,lambda bad=bad:rejects(lambda:ad.validate_truth(cfg,bad)))
        badcfg=copy.deepcopy(cfg);badcfg["priors"][k]={"kind":"Uniform","minimum":-0.1,"maximum":0.1}
        check("reject_free_prior_"+k,lambda badcfg=badcfg:rejects(lambda:ad.validate_config(badcfg)))
    missing=dict(truth);missing.pop("dtau440")
    check("reject_missing_fixed_truth",lambda:rejects(lambda:ad.validate_truth(cfg,missing)))
    badcfg=copy.deepcopy(cfg);badcfg["grid"].pop("generation_sample_rate_hz")
    check("reject_missing_generation_grid",lambda:rejects(lambda:ad.validate_config(badcfg)))
    badcfg2=copy.deepcopy(cfg);badcfg2["grid"]["generation_sample_rate_hz"]=4096
    check("reject_unqualified_generation_grid",lambda:rejects(lambda:ad.validate_config(badcfg2)))
    check("reject_outside_pilot_file_before_read",lambda:rejects(lambda:Path("/mnt/c/NO_SCIENTIFIC_INPUT_SENTINEL").read_bytes()))
    check("reject_nonuniform_grid_without_native_call",lambda:rejects(lambda:source.generation_grid(np.array([0.,1.,2.01]),4096,8192,1024)))
    source_kwargs=ad.generator(cfg).waveform_arguments
    wfpars={k:truth[k] for k in ("mass_1","mass_2","luminosity_distance","chi_1","chi_2","theta_jn","phase","dtau220","dtau440","domega220","domega440","geocent_time")}
    fake_freq=np.array([0.0,0.03125])
    check("reject_lal_dictionary_override_before_native",lambda:rejects(lambda:ad.synthetic_only220(fake_freq,**wfpars,**dict(source_kwargs,lal_waveform_dictionary={}))))
    missing_kw=dict(source_kwargs);missing_kw.pop("generation_sample_rate_hz")
    check("reject_missing_forwarded_generation_before_native",lambda:rejects(lambda:ad.synthetic_only220(fake_freq,**wfpars,**missing_kw)))
    check("reject_silent_waveform_errors",lambda:rejects(lambda:ad.synthetic_only220(fake_freq,**wfpars,**dict(source_kwargs,catch_waveform_errors=True))))
    def time_corners():
        p=cfg["priors"];g=cfg["grid"];n=0;min_margin=float("inf");skipped=0
        for vals in itertools.product(*[(p[k]["minimum"],p[k]["maximum"]) for k in ("mass_1","mass_2","chi_1","chi_2","dtau220","geocent_time")]):
            m1,m2,c1,c2,dt,t=vals;q=m2/m1
            if not p["mass_ratio"]["minimum"]<=q<=p["mass_ratio"]["maximum"]:skipped+=1;continue
            a=temporal.validate_time_contract(m1,m2,c1,c2,g["minimum_frequency_hz"],t,source_kwargs["analysis_time_contract"],dt,0.0)
            n+=1;min_margin=min(min_margin,*a["margins_s"])
        return {"valid_box_corners":n,"excluded_by_registered_mass_ratio":skipped,"minimum_margin_seconds":min_margin,
                "scope":"Conservative time bounds over physical prior corners, not waveform-tail leakage certification"}
    check("registered_prior_corner_time_bounds",time_corners)
    result["P1_status"]="PASS" if all(x["passed"] for x in controls) else "FAIL"
    atomic_json(run/"P1_CONTROLS.json",{"controls":controls,"status":result["P1_status"],"native_calls":counter[0]})
    if result["P1_status"]!="PASS":raise RuntimeError("P1 failure; native stage not started")
    old_create=lal.CreateDict
    def tracked_create():
        obj=old_create()
        if __import__("inspect").currentframe().f_back.f_code.co_filename==source.__file__:native_dictionaries.append(obj)
        return obj
    lal.CreateDict=tracked_create
    old_bbh=bilby.gw.source.lal_binary_black_hole
    def tracked_bbh(*args,**kwargs):
        if counter[0]>=contract["max_native_calls"]:raise RuntimeError("Native call cap reached")
        dictionary=kwargs["lal_waveform_dictionary"]
        params={n:float(getattr(ls,"SimInspiralWaveformParamsLookup"+n)(dictionary)) for n in ("DTau220","DTau440","DOmega220","DOmega440")}
        if any(params[n]!=0.0 for n in ("DTau440","DOmega220","DOmega440")):raise AssertionError("Fixed deformation leaked")
        if kwargs["maximum_frequency"]!=4096 or len(args[0])!=131073:raise AssertionError("Generation grid was not forwarded")
        if kwargs["waveform_approximant"]!="pSEOBNRv4HM_PA":raise AssertionError("Wrong native family")
        if not any(dictionary is x for x in native_dictionaries):raise AssertionError("Dictionary provenance absent")
        trace.append({"ordinal":len(trace)+1,"deformations":params,"generation_bins":len(args[0]),
                      "generation_fmax":kwargs["maximum_frequency"],"family":kwargs["waveform_approximant"]})
        return old_bbh(*args,**kwargs)
    bilby.gw.source.lal_binary_black_hole=tracked_bbh
    print("P1 passed; P2 native synthetic source controls started",flush=True)
    derived=ad.remnant_and_rb_truth(truth["mass_1"],truth["mass_2"],truth["chi_1"],truth["chi_2"])
    rb=dict(truth);rb["dtau220"]=derived["dtau220"]
    f,gr_first=ad.generate(cfg,truth);f2,rb_pol=ad.generate(cfg,rb);f3,gr_again=ad.generate(cfg,truth)
    def gr_repeat():
        rel=max(float(np.linalg.norm(gr_first[k]-gr_again[k])/np.linalg.norm(gr_first[k])) for k in gr_first)
        assert rel<=contract["tolerances"]["GR_repeat_relative"]
        return {"relative_error":rel,"bitwise_equal":all(np.array_equal(gr_first[k],gr_again[k]) for k in gr_first)}
    check("native_GR_RB_GR_repeat",gr_repeat)
    def deformation_is_visible():
        rel=math.sqrt(sum(float(np.vdot(rb_pol[k]-gr_first[k],rb_pol[k]-gr_first[k]).real) for k in gr_first)/sum(float(np.vdot(gr_first[k],gr_first[k]).real) for k in gr_first))
        assert rel>contract["tolerances"]["RB_GR_minimum_relative_difference"]
        return {"relative_norm_difference":rel}
    check("RB_differs_from_GR_source",deformation_is_visible)
    stress=base_truth("SYN_B");stress_rem=ad.remnant_and_rb_truth(stress["mass_1"],stress["mass_2"],stress["chi_1"],stress["chi_2"])
    stress["dtau220"]=stress_rem["dtau220"];_,stress_pol=ad.generate(cfg,stress)
    def stress_valid():
        assert all(np.isfinite(x).all() for x in stress_pol.values()) and any(np.any(x!=0) for x in stress_pol.values())
        return {"finite_nonzero":True,"dtau220":stress["dtau220"]}
    check("stress_fixture_finite_nonzero",stress_valid)
    psd,mask=ad.analytic_psd(f,cfg)
    check("analytic_PSD_positive_finite_on_band",lambda:{"bins":int(mask.sum()),"min":float(psd[mask].min()),"max":float(psd[mask].max()),"sha256":ahash(psd)})
    bad_psd=psd.copy();bad_psd[mask]*=1.01
    check("reject_foreign_PSD_numeric_array",lambda:rejects(lambda:ad.make_ifos(cfg,f,bad_psd,"ZERO")))
    foreign_ifos=bilby.gw.detector.InterferometerList(cfg["detectors"])
    check("reject_foreign_detector_objects",lambda:rejects(lambda:ad.inject(cfg,truth,gr_first,foreign_ifos)))
    own_ifos,_=ad.make_ifos(cfg,f,psd,"ZERO")
    foreign_pol={k:a.copy() for k,a in gr_first.items()}
    check("reject_foreign_polarization_objects",lambda:rejects(lambda:ad.inject(cfg,truth,foreign_pol,own_ifos)))
    changed_noise=own_ifos[0].strain_data.frequency_domain_strain.copy();changed_noise[1000]+=1e-20
    own_ifos[0].set_strain_data_from_frequency_domain_strain(changed_noise,sampling_frequency=cfg["grid"]["sample_rate_hz"],duration=cfg["grid"]["duration_s"],start_time=cfg["geometry"]["geocent_time"]-16)
    check("reject_replaced_in_memory_noise",lambda:rejects(lambda:ad.inject(cfg,truth,gr_first,own_ifos)))
    other_ifos,_=ad.make_ifos(cfg,f,psd,"ZERO")
    other_ifos[0].power_spectral_density=bilby.gw.detector.PowerSpectralDensity(frequency_array=f,psd_array=bad_psd)
    check("reject_replaced_in_memory_PSD",lambda:rejects(lambda:ad.inject(cfg,truth,gr_first,other_ifos)))
    arrays={"frequencies_Hz":f,"PSD_analytic_strain2_per_Hz":psd}
    injections=[]
    for label,t,pol,noise_kind in [("GR_ZERO",truth,gr_first,"ZERO"),("GR_GAUSS",truth,gr_first,"SEEDED_GAUSSIAN"),("RB_GAUSS",rb,rb_pol,"SEEDED_GAUSSIAN")]:
        ifos,noise=ad.make_ifos(cfg,f,psd,noise_kind)
        actual,scaled,signal,receipt=ad.inject(cfg,t,pol,ifos)
        check(label+"_reject_reused_injection_objects",lambda:rejects(lambda:ad.inject(cfg,t,pol,ifos)))
        norm={}
        for i in ifos:
            quad=4/cfg["grid"]["duration_s"]*float(np.sum(np.abs(noise[i.name][mask])**2/psd[mask]))
            dof=2*int(mask.sum());z=(quad-dof)/math.sqrt(2*dof) if noise_kind!="ZERO" else 0.0
            if noise_kind!="ZERO" and abs(z)>contract["tolerances"]["noise_chisquare_z_abs_max"]:raise AssertionError("Synthetic PSD/noise normalization control failed")
            norm[i.name]={"noise_quadratic":quad,"dof":dof,"z":z,"noise_sha256":ahash(noise[i.name]),
                          "signal_sha256":ahash(signal[i.name]),"injected_sha256":ahash(i.strain_data.frequency_domain_strain)}
            arrays[label+"_"+i.name+"_noise_fd"]=noise[i.name]
            arrays[label+"_"+i.name+"_signal_fd"]=signal[i.name]
        injections.append({"label":label,"truth":actual,"receipt":receipt,"normalization":norm})
        if label in ("GR_GAUSS","RB_GAUSS"):
            _,fresh=ad.generate(cfg,actual)
            rel=max(float(np.linalg.norm(fresh[k]-scaled[k])/np.linalg.norm(scaled[k])) for k in scaled)
            assert rel<=contract["tolerances"]["amplitude_rescaling_relative"]
            check(label+"_distance_rescaling_equivalent",lambda rel=rel:{"relative_error":rel})
    check("paired_GR_RB_same_noise",lambda:{"identical":all(np.array_equal(arrays["GR_GAUSS_"+d+"_noise_fd"],arrays["RB_GAUSS_"+d+"_noise_fd"]) for d in cfg["detectors"])})
    assert all(np.array_equal(arrays["GR_GAUSS_"+d+"_noise_fd"],arrays["RB_GAUSS_"+d+"_noise_fd"]) for d in cfg["detectors"])
    assert len(native_dictionaries)==len(trace) and len({id(x) for x in native_dictionaries})==len(trace)
    check("fresh_LAL_dictionary_every_native_generation",lambda:{"dictionaries":len(native_dictionaries),"native_calls":len(trace),"all_unique":True})
    tmp=run/"SYNTHETIC_ARRAYS.npz.tmp"
    with tmp.open("xb") as h:np.savez_compressed(h,**arrays)
    assert tmp.stat().st_size>0
    final=run/"SYNTHETIC_ARRAYS.npz";os.replace(tmp,final)
    result.update({"status":"P0_P1_P2_QUALIFIED_SYNTHETIC_ONLY" if all(x["passed"] for x in controls) else "MEASURED_CONTROL_FAILURE",
                   "source_truth_derivation":derived,"stress_truth_derivation":stress_rem,"injections":injections,
                   "arrays":{"path":str(final),"sha256":digest(final),"bytes":final.stat().st_size},
                   "P3_or_recovery_performed":False,
                   "limits":"No bias/coverage, PE convergence, D power or physical verdict is established."})
except BaseException as exc:
    result["status"]="MEASURED_FAILURE_NO_PE"
    result["error"]=type(exc).__name__+": "+str(exc)
    result["traceback"]=traceback.format_exc()
finally:
    result.update({"finished_utc":datetime.now(timezone.utc).isoformat(),
                   "wall_seconds":time.perf_counter()-started,"CPU_seconds":time.process_time()-cpu_started,
                   "native_calls_counted":counter[0],"native_wall_seconds":counter[1],"EDOM_count":counter[2],
                   "filesystem_audit_mounted_paths":filesystem,"blocked_operations":blocked,
                   "instrument_isolation_scope":"Python-level audited file/process/network restrictions plus path-free adapter. Not a proof that arbitrary native code could never perform unaudited syscalls.",
                   "D_strain_read":False,"D_posterior_read":False,"originals_executed":False,"new_remote_calls":0,
                   "runtime_hashes_verified_before_native_calls":len(runtime_pins["files"]),
                   "original_input_hashes_unchanged":all(digest(ROOT/rel)==pin["sha256"] for rel,pin in contract["inputs"].items())})
    atomic_json(run/"RESULT.json",result)
    print(json.dumps({k:result[k] for k in ("status","wall_seconds","CPU_seconds","native_calls_counted","native_wall_seconds","EDOM_count","PE_calls")},ensure_ascii=False),flush=True)
sys.exit(0 if result["status"]=="P0_P1_P2_QUALIFIED_SYNTHETIC_ONLY" else 2)
