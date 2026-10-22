"""Registered, source-pinned local constructive fits for ORDEM015 T07(a)."""
import os
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
import hashlib, json, math, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/"C7_COHERENT_SOURCE_REPRODUCTION_v3"
REG=HERE/"T07_REGISTRATION.json"
OUT=HERE/"results"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def fresh(p, obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    with p.open("xb") as f: f.write(data)
    assert p.stat().st_size==len(data)

def custody():
    reg=json.loads(REG.read_bytes())
    for rel,h in reg["source_sha256"].items():
        p=ROOT/rel
        if sha(p)!=h: raise RuntimeError("SOURCE_CHANGED:"+rel)
    return reg

def run():
    reg=custody()
    sys.path.insert(0,str(SOURCE))
    from coherent_imr_model import network_basis,profile_fit,remnant
    from tgl_ringdown_prediction import scales
    from nonlinear_coherent_recovery import source_vector,STEPS,WIDTH
    source=reg["source"]
    x0=source_vector(source)
    q=source["q"]
    m1=source["mass"]*q/(1+q); m2=source["mass"]/(1+q)
    mf,spin=remnant("SEOBNRv4HM",m1,m2,source["s1"],source["s2"])
    times=np.arange(reg["n_samples"])/reg["sample_rate"]+10*scales(mf,"CODATA2018_IAU2015")[0]
    with np.load(SOURCE/"cache/recolored_noise/O4_noise.npz") as f:
        white=f["whitener_scaled"].copy()
    orientation=np.array([np.cos(2*source["psi"]),np.sin(2*source["psi"])])
    lower=-WIDTH.copy(); upper=WIDTH.copy()
    lower[1]=max(lower[1],-x0[1]); upper[1]=min(upper[1],np.log(4)-x0[1])
    for k in (2,3):
        lower[k]=max(lower[k],-.8-x0[k]); upper[k]=min(upper[k],.8-x0[k])
    lower[4]=max(lower[4],.03-x0[4]); upper[4]=min(upper[4],np.pi-.03-x0[4])
    bounds=list(zip(lower/STEPS,upper/STEPS))
    OUT.mkdir(exist_ok=True)
    for reading in reg["readings"]:
        begun=time.monotonic()
        label=reading.replace("-","_")
        target_basis,_=network_basis("SEOBNRv4HM",x0,times,reading,1.,white,8192)
        raw=target_basis@orientation
        target=raw*(40/np.linalg.norm(raw))
        gr_basis,_=network_basis("SEOBNRv4HM",x0,times,reading,0.,white,8192)
        control0=profile_fit(gr_basis,gr_basis@orientation*40/np.linalg.norm(gr_basis@orientation))[0]
        best={"squared_residual":float("inf")}
        calls=0; invalid=0; stages=[]
        def objective(y):
            nonlocal calls,invalid,best
            calls+=1
            x=x0+np.asarray(y)*STEPS
            try:
                basis,_=network_basis("SEOBNRv4HM",x,times,reading,0.,white,8192)
                val,coef,_=profile_fit(basis,target)
                if not math.isfinite(val): raise ValueError("nonfinite")
            except (ValueError, RuntimeError, FloatingPointError):
                invalid+=1
                return 1e12
            if val<best["squared_residual"]:
                best={"squared_residual":float(val),"coordinates":x.tolist(),"coefficients":coef.tolist(),"call":calls}
            return float(val)
        objective(np.zeros(7))
        for cap in reg["maxfev_stages"]:
            if not math.isfinite(best["squared_residual"]): break
            seed=np.clip((np.array(best["coordinates"])-x0)/STEPS,lower/STEPS,upper/STEPS)
            res=minimize(objective,seed,method="Powell",bounds=bounds,options=dict(maxfev=cap,ftol=1e-7,xtol=1e-4))
            stages.append({"maxfev":cap,"success":bool(res.success),"message":str(res.message),"nfev":int(res.nfev)})
        controls=[]
        if math.isfinite(best["squared_residual"]):
            x=np.array(best["coordinates"])
            for rate in (8192,16384):
                injected,_=network_basis("SEOBNRv4HM",x0,times,reading,1.,white,rate)
                raw=injected@orientation
                t=raw*(40/np.linalg.norm(raw))
                basis,_=network_basis("SEOBNRv4HM",x,times,reading,0.,white,rate)
                v,_,_=profile_fit(basis,t)
                controls.append({"sample_rate":rate,"candidate_residual_norm":float(np.sqrt(v)),"finite":bool(np.isfinite(v))})
        row={"reading":reading,"family":"SEOBNRv4HM","psd":"O4","reference_snr":40,"a0_same_source_squared_residual":float(control0),"a1_best_local_constructive_upper_bound":float(np.sqrt(best["squared_residual"])) if math.isfinite(best["squared_residual"]) else None,"best":best if math.isfinite(best["squared_residual"]) else None,"stages":stages,"evaluations":calls,"invalid_evaluations":invalid,"controls":controls,"wall_seconds":time.monotonic()-begun,"status":"LOCAL_CANDIDATE_NOT_GLOBAL_Z_OR_SIGMA","registered_sha256":sha(REG),"scope":"Finite local GR source candidate gives upper bound on best mismatch. maxfev is not convergence; no calibrated detection, gate or Bayes factor."}
        fresh(OUT/(label+".json"),row)
        print(json.dumps({"reading":reading,"status":row["status"],"calls":calls,"wall_seconds":row["wall_seconds"],"candidate":row["a1_best_local_constructive_upper_bound"]}),flush=True)

if __name__=="__main__":run()
