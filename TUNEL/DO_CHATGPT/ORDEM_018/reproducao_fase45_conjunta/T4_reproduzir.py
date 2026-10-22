"""Independent deterministic reproduction of archived F4/T D1b only."""
import os
for _name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"
import sys, json, math, time, hashlib, platform, traceback, ctypes
from pathlib import Path
T0 = time.perf_counter()
CPU0 = time.process_time()
import numpy as np
import scipy
from scipy.linalg import solve_triangular
from scipy.optimize import least_squares
ROOT = Path(__file__).resolve().parent
PROTO = None
class CriticalDivergence(RuntimeError): pass
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tick():
    if time.perf_counter() - T0 > PROTO["resources"]["wall_seconds_max"]:
        raise CriticalDivergence("wall time limit reached")
def save_new(path, obj):
    assert not path.exists(), str(path)
    data=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()
    tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_bytes(data)
    assert tmp.read_bytes()==data; os.replace(tmp,path)
def peak_working_set():
    if os.name!="nt": return None
    from ctypes import wintypes
    class PMC(ctypes.Structure):
        _fields_=[("cb",wintypes.DWORD),("PageFaultCount",wintypes.DWORD)]+[(k,ctypes.c_size_t) for k in
        ("PeakWorkingSetSize","WorkingSetSize","QuotaPeakPagedPoolUsage","QuotaPagedPoolUsage","QuotaPeakNonPagedPoolUsage","QuotaNonPagedPoolUsage","PagefileUsage","PeakPagefileUsage")]
    p=PMC(); p.cb=ctypes.sizeof(p)
    ctypes.windll.kernel32.GetCurrentProcess.restype=wintypes.HANDLE
    h=ctypes.windll.kernel32.GetCurrentProcess()
    f=ctypes.windll.psapi.GetProcessMemoryInfo; f.argtypes=[wintypes.HANDLE,ctypes.POINTER(PMC),wintypes.DWORD]
    ok=f(h,ctypes.byref(p),p.cb)
    return int(p.PeakWorkingSetSize) if ok else None
def require(condition, message):
    if not condition: raise CriticalDivergence(message)
class FrozenTable:
    names=("z_star","z_drag","r_star","r_drag","DM_star")
    def __init__(self,path):
        self.data=np.load(path,allow_pickle=False)
        self.axes=[self.data["grade_"+n] for n in ("H0","ombh2","omch2")]
        self.values=np.stack([self.data[n] for n in self.names],axis=-1)
    def __call__(self,t):
        weights=[]; indices=[]
        for value,axis in zip(t[:3],self.axes):
            pos=(value-axis[0])/(axis[1]-axis[0])
            require(1<=pos<=len(axis)-2,"CAMB table support exceeded")
            start=int(np.clip(math.floor(pos)-2,0,len(axis)-6))
            nodes=np.arange(6,dtype=float); rel=pos-start
            w=np.ones(6)
            for j in range(6):
                for m in range(6):
                    if m!=j: w[j]*=(rel-nodes[m])/(nodes[j]-nodes[m])
            weights.append(w); indices.append(np.arange(start,start+6))
        vals=self.values[np.ix_(*indices)]
        ans=np.einsum("i,j,k,ijkv->v",*weights,vals,optimize=False)
        return dict(zip(self.names,ans))
    def check(self):
        points=self.data["teste_pontos"]; errors={n:[] for n in self.names}; count=0; outside=0
        for t in points:
            try: out=self(t)
            except CriticalDivergence: outside+=1; continue
            for name in self.names:
                expected=self.data["teste_"+name][count+outside]
                errors[name].append(abs(out[name]/expected-1))
            count+=1
        require(count>0,"no valid table test points")
        return {"n_interior":count,"n_outside":outside,"relative_max":{n:float(max(x)) for n,x in errors.items()}}
class Likelihood:
    def __init__(self,inputs,table,dr2mean,dr2cov,nq):
        self.table=table; self.data=inputs; self.nq=nq; self.count=0
        self.beta=float(inputs["alpha_codata2018"])*math.sqrt(math.e)
        self.limits=inputs["limits_declared"]
        self.planck=np.array(inputs["planck_mean"]); self.Lplanck=np.linalg.cholesky(inputs["planck_cov_chen2019"])
        rows=[ln.split() for ln in dr2mean.read_text().splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
        self.zbao=np.array([float(r[0]) for r in rows]); self.bao=np.array([float(r[1]) for r in rows])
        self.kinds=[r[2] for r in rows]; self.Lbao=np.linalg.cholesky(np.loadtxt(dr2cov))
        self.cc=np.array(inputs["cc_data_z_H_sigma"])
        require(self.cc.shape==(32,3),"CC shape mismatch")
        require(len(self.zbao)==13,"DR2 length mismatch")
        self.x,self.w=np.polynomial.legendre.leggauss(nq)
        self.omega_r_h2=4.4814e-7*2.7255**4*(1+3.046*(7/8)*(4/11)**(4/3))
        self.c=299792.458
    def evaluate(self,t):
        tick(); self.count+=1
        H,wb,wc,beta=t
        for value,key in zip(t,("H0","ombh2","omch2","beta")):
            low,high=self.limits[key]; require(low<value<high,"declared prior exceeded")
        cam=self.table(t)
        om=(wb+wc+.06/93.14)/(H/100)**2
        orad=self.omega_r_h2/(H/100)**2
        ol=1-om-orad
        def E(z): return np.sqrt(orad*(1+z)**4+om*(1+z)**3+ol)
        zz=.5*self.zbao[:,None]*(self.x+1)
        dm=self.c/H*.5*self.zbao*np.sum(self.w/E(zz),axis=1)
        dh=self.c/(H*E(self.zbao)); dv=(self.zbao*dm**2*dh)**(1/3)
        obs={"DM_over_rs":dm,"DH_over_rs":dh,"DV_over_rs":dv}
        bao=np.array([obs[k][i] for i,k in enumerate(self.kinds)])/cam["r_drag"]
        pl=np.array([math.sqrt(om)*H/self.c*cam["DM_star"],math.pi*cam["DM_star"]/cam["r_star"],wb])
        istar=(2/3)*math.log(float(E(PROTO["z_star_law"])))
        icc=(2/3)*np.log(E(self.cc[:,0]))
        cc=H*E(self.cc[:,0])*np.exp(beta*(istar-icc))
        residuals={"planck_comp":solve_triangular(self.Lplanck,pl-self.planck,lower=True),
                   "desi_dr2":solve_triangular(self.Lbao,bao-self.bao,lower=True),
                   "cc_moresco":(cc-self.cc[:,1])/self.cc[:,2]}
        r=np.concatenate(list(residuals.values()))
        return r,{"chi2":{k:float(v@v) for k,v in residuals.items()},"H0":float(H),"K":math.exp(beta*istar),"I":istar,
                  "H0_local":float(H)*math.exp(beta*istar),"Omega_m":float(om)}
def fit(model,like,x0=None):
    base=np.array([67.5,.02237,.1200,0.0])
    free=model=="livre"; n=4 if free else 3
    base[3]=0 if model=="lcdm" else like.beta if model=="tgl" else 0
    scales=np.array([1,.0005,.005,.005])[:n]
    names=["H0","ombh2","omch2","beta"][:n]
    lo=np.array([(like.limits[k][0]-base[i])/scales[i] for i,k in enumerate(names)])*.999
    hi=np.array([(like.limits[k][1]-base[i])/scales[i] for i,k in enumerate(names)])*.999
    ini=np.zeros(n) if x0 is None else (np.array(x0)[:n]-base[:n])/scales
    cache={}
    def unpack(y):
        t=base.copy(); t[:n]=base[:n]+y*scales; return t
    def rj(y):
        key=tuple(np.round(y,14))
        if key not in cache:
            h=.001; r=like.evaluate(unpack(y))[0]; jac=[]
            for i in range(n):
                dy=np.eye(n)[i]*h
                jac.append((like.evaluate(unpack(y+dy))[0]-like.evaluate(unpack(y-dy))[0])/(2*h))
            cache.clear(); cache[key]=(r,np.array(jac).T)
        return cache[key]
    wall=time.perf_counter(); cpu=time.process_time()
    res=least_squares(lambda y:rj(y)[0],ini,jac=lambda y:rj(y)[1],bounds=(lo,hi),method="trf",
                      x_scale=1,xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=200)
    theta=unpack(res.x); r,jac=rj(res.x); cov=np.linalg.inv(jac.T@jac)*np.outer(scales,scales)
    sig=np.sqrt(np.diag(cov)); point=like.evaluate(theta)[1]
    return {"model":model,"theta":dict(zip(["H0","ombh2","omch2","beta"],map(float,theta))),
            "chi2":float(r@r),"point":point,"free":names,"sigma_JtJ":dict(zip(names,map(float,sig))),
            "cov_JtJ":cov.tolist(),"success":bool(res.success),"status":int(res.status),"message":res.message,
            "nfev":int(res.nfev),"njev":int(res.njev),"optimality":float(res.optimality),
            "active_mask":res.active_mask.tolist(),"jac_condition":float(np.linalg.cond(jac)),
            "wall_seconds":time.perf_counter()-wall,"cpu_seconds":time.process_time()-cpu}
def main():
    global PROTO
    PROTO=json.loads((ROOT/"T4_PROTOCOLO.json").read_bytes())
    freeze=json.loads((ROOT/"T4_PREEXEC_HASHES.json").read_bytes())
    require(sha(ROOT/"T4_PROTOCOLO.json")==freeze["protocol_sha256"],"protocol hash mismatch")
    require(sha(Path(__file__))==freeze["code_sha256"],"code hash mismatch")
    for name,h in PROTO["file_pins"].items(): require(sha(ROOT/name)==h,"source pin mismatch: "+name)
    inputs=json.loads((ROOT/"ENTRADAS_HISTORICAS_E_COVARIANCIAS.json").read_bytes())
    archive=json.loads((ROOT/"T4_ALVO_HISTORICO.json").read_bytes())
    table=FrozenTable(ROOT/"T4_camb_lcdm_v1.npz")
    out={"scope":PROTO["scope"],"started_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
         "protocol_sha256":freeze["protocol_sha256"],"code_sha256":freeze["code_sha256"],"file_pins":PROTO["file_pins"],
         "environment":{"python":sys.version,"executable":sys.executable,"platform":platform.platform(),"numpy":np.__version__,"scipy":scipy.__version__,
         "threads":{k:os.environ[k] for k in ("OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","OMP_NUM_THREADS","NUMEXPR_NUM_THREADS")}},
         "fits":{},"checks":{},"scientific_verdict":None,"evidence_computed":False,"other_families_executed":False}
    try:
        tt=table.check(); out["table_test"]=tt
        require(max(tt["relative_max"].values())<=PROTO["tolerances"]["table_relative"],"table test divergence")
        like=Likelihood(inputs,table,ROOT/"T4_desi_mean.txt",ROOT/"T4_desi_cov.txt",64)
        high=Likelihood(inputs,table,ROOT/"T4_desi_mean.txt",ROOT/"T4_desi_cov.txt",128)
        fixed={}; out["fixed_archived_points"]=fixed
        for model in ("tgl","livre"):
            th=archive["theta_"+model]; t=[th[k] for k in ("H0","ombh2","omch2","beta")]
            if model=="tgl": t[3]=like.beta
            r,p=like.evaluate(t); rh,ph=high.evaluate(t)
            diff={k:p["chi2"][k]-archive["pontos"][model]["chi2"][k] for k in p["chi2"]}
            qdiff=float(max(abs(r-rh)))
            fixed[model]={"point":p,"archive_chi2_differences":diff,"residual_GL64_GL128_max":qdiff}
            require(max(map(abs,diff.values()))<=PROTO["tolerances"]["chi2_block_abs"],"fixed archived theta mismatch")
            require(qdiff<=PROTO["tolerances"]["quadrature_residual_abs"],"distance quadrature not converged")
        out["fixed_archived_points"]=fixed
        initial=None
        for model in ("lcdm","tgl","livre"):
            f=fit(model,like,initial); out["fits"][model]=f
            require(f["success"],model+" optimizer failed")
            require(abs(f["chi2"]-archive["chi2"][model])<=PROTO["tolerances"]["chi2_total_abs"],model+" minimum mismatch")
            diffs={k:f["point"]["chi2"][k]-archive["pontos"][model]["chi2"][k] for k in f["point"]["chi2"]}
            require(max(map(abs,diffs.values()))<=PROTO["tolerances"]["chi2_block_abs"],model+" block minima mismatch")
            f["differences"]={"chi2":f["chi2"]-archive["chi2"][model],"chi2_blocks":diffs,
                 "H0":f["theta"]["H0"]-archive["pontos"][model]["H0"],
                 "K":f["point"]["K"]-archive["pontos"][model]["K"]}
            if model in ("tgl","livre"):
                f["differences"]["theta"]={k:f["theta"][k]-archive["theta_"+model][k] for k in f["theta"]}
            if model=="lcdm": initial=[f["theta"][k] for k in ("H0","ombh2","omch2","beta")]
            t=[f["theta"][k] for k in ("H0","ombh2","omch2","beta")]
            rh,ph=high.evaluate(t); r,p=like.evaluate(t)
            f["GL128_minus_GL64_chi2"]=float(rh@rh-r@r)
            require(max(abs(rh-r))<=PROTO["tolerances"]["quadrature_residual_abs"],model+" quadrature mismatch")
            require(abs(f["differences"]["H0"])<=PROTO["tolerances"]["H0_abs"],model+" H0 mismatch")
            for key in ("ombh2","omch2"):
                if model in ("tgl","livre"):
                    require(abs(f["differences"]["theta"][key])<=PROTO["tolerances"]["density_abs"],model+" density mismatch")
        l,t,f=[out["fits"][k] for k in ("lcdm","tgl","livre")]
        sb=f["sigma_JtJ"]["beta"]; bh=f["theta"]["beta"]; delta=bh-like.beta
        stat={"beta_tgl_runtime":like.beta,"beta_livre":bh,"sigma_beta_JtJ":sb,"delta":delta,
              "z_delta":delta/sb,"z_perfil_beta_tgl":math.sqrt(max(t["chi2"]-f["chi2"],0)),
              "z_ganho_da_lei":math.copysign(math.sqrt(abs(l["chi2"]-t["chi2"])),l["chi2"]-t["chi2"]),
              "custo_por_nat_medido":bh*f["point"]["I"]/math.log1p(PROTO["z_star_law"])}
        out["statistics"]=stat
        out["statistics_differences"]={k:stat[k]-archive[k] for k in stat if k in archive}
        require(abs(bh-archive["beta_livre"])<=PROTO["tolerances"]["beta_abs"],"free beta mismatch")
        require(abs(sb/archive["sigma_beta_JtJ"]-1)<=PROTO["tolerances"]["sigma_beta_relative"],"beta sigma mismatch")
        for key in ("z_delta","z_perfil_beta_tgl","z_ganho_da_lei"):
            require(abs(out["statistics_differences"][key])<=PROTO["tolerances"]["z_abs"],key+" mismatch")
        out["checks"]={"source_pins":True,"table_holdout_tolerance":True,"fixed_points_before_fit":True,
                       "quadrature_convergence":True,"all_optimizers_success":True,"archived_statistics_tolerances":True}
        out["status"]="HISTORICAL_NUMERICAL_REPRODUCTION_WITHIN_FROZEN_TOLERANCES"
        out["likelihood_calls"]=like.count+high.count
    except Exception as e:
        out["status"]="CRITICAL_DIVERGENCE_STOP_NO_EXTENSION"
        out["error"]=repr(e); out["traceback"]=traceback.format_exc()
    out["resources"]={"wall_seconds":time.perf_counter()-T0,"cpu_seconds":time.process_time()-CPU0,
                      "peak_working_set_bytes":peak_working_set(),"limits":PROTO["resources"]}
    save_new(ROOT/"T4_RESULTADO.json",out)
    print(json.dumps({"status":out["status"],"resources":out["resources"],"checks":out["checks"],
                      "chi2":{k:v["chi2"] for k,v in out["fits"].items()},"statistics":out.get("statistics"),"error":out.get("error")},ensure_ascii=False))
    return 0 if out["status"].startswith("HISTORICAL_NUMERICAL") else 2
if __name__=="__main__":
    if sys.argv[1:]!=["--run"]: raise SystemExit("Only explicit --run is accepted")
    raise SystemExit(main())
