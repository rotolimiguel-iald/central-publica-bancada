"""Exact beta acceleration for historical P4/P5 shadow. Validation only until coordinator continuation."""
import os
for key in ("OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","OMP_NUM_THREADS","NUMEXPR_NUM_THREADS"):os.environ[key]="1"
import argparse,json,math,time,hashlib,sys,importlib.util,itertools,traceback
from pathlib import Path
T0=time.perf_counter();CPU0=time.process_time()
import numpy as np
from scipy.linalg import solve_triangular
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def save(n,d):
 p=ROOT/n;assert not p.exists(),str(p)
 b=(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode();t=p.with_suffix(p.suffix+".tmp");t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def setup(seconds):
 cfg=read("E45A_PROTOCOLO.json");pins=read("E45A_PREEXEC_HASHES.json")
 require(sha(ROOT/"E45A_PROTOCOLO.json")==pins["protocol_sha256"],"protocol hash")
 require(sha(Path(__file__))==pins["code_sha256"],"code hash")
 for n,h in cfg["pins"].items():require(sha(ROOT/n)==h,"pin "+n)
 common=load("independent_e45_for_acceleration",ROOT/"E45_piloto_e_grade.py");common.T0=T0
 old,p,core,table,likes,fits=common.setup(seconds)
 return cfg,pins,common,core,table,likes,fits
class ExactBeta:
 def __init__(self,family,like):
  require(family in ("P4_d1b","P5_sombra"),"accumulated reading is not supported")
  self.family=family;self.like=like;self.calls=0
  if family=="P5_sombra":
   sn=like.sn;qw=solve_triangular(sn.L,sn.non.astype(float),lower=True)
   self.qM=float(sn.one@qw/sn.norm);self.qperp=qw-sn.one*self.qM;self.qnorm=float(self.qperp@self.qperp)
 def coefficients(self,background):
  self.calls+=1;t=list(background)+[0.0];r,p=self.like.evaluate(t)
  if self.family=="P4_d1b":
   return dict(background_chi2=float(r[:-1]@r[:-1]),H=float(background[0]),I=p["I"])
  # First16 residuals are Planck3 + DR213, then full profiled SN1657.
  rs=r[16:];v=5/math.log(10)*p["I"]
  require(len(rs)==1657,"residual layout")
  return dict(background_chi2=float(r[:16]@r[:16]),A=v*v*self.qnorm,B=2*v*float(rs@self.qperp),C=float(rs@rs),M0=p["M_hat"],M1=v*self.qM,I=p["I"])
 def evaluate(self,c,beta):
  beta=np.asarray(beta,dtype=float)
  if self.family=="P4_d1b":
   sh=self.like.data["sh0es_local"];obs=(c["H"]*np.exp(beta*c["I"])-sh["mean"])/sh["sigma"]
   chi=c["background_chi2"]+obs*obs;m=None
  else:
   chi=c["background_chi2"]+c["C"]+beta*(c["B"]+beta*c["A"]);m=c["M0"]+beta*c["M1"]
  lo,hi=self.like.limits["beta"];valid=(beta>lo)&(beta<hi)
  return np.where(valid,chi,np.inf),m
def validate():
 cfg,pins,common,core,table,likes,fits=setup(cfg_seconds:=120)
 out=common.metadata(cfg,pins);out.update(scope="EXACT_ACCELERATION_VALIDATION_ONLY_NO_OBSERVATIONAL_INTEGRAL",controls={},benchmarks={},source_result_sha256=sha(ROOT/"P45_RESULTADO.json"))
 try:
  beta_fixed=np.array(cfg["validation"]["beta_points"]+[likes["P4_d1b"].beta])
  for family in ("P4_d1b","P5_sombra"):
   like=likes[family];fast=ExactBeta(family,like);out["controls"][family]={}
   backgrounds=[]
   for model,f in fits["families"][family]["fits"].items():
    bg=[f["theta"][k] for k in ("H0","ombh2","omch2")];backgrounds.append(bg)
    c=fast.coefficients(bg)
    values,m=fast.evaluate(c,beta_fixed);delta=[];mdelta=[]
    for j,beta in enumerate(beta_fixed):
     scalar,p=like.evaluate(bg+[float(beta)]);delta.append(float(values[j]-scalar@scalar))
     if m is not None:mdelta.append(float(m[j]-p["M_hat"]))
    oldbeta=f["theta"]["beta"];vv,mm=fast.evaluate(c,[oldbeta])
    item={"background_source":"P45 "+family+"/"+model,"beta_points":beta_fixed.tolist(),"max_chi2_fast_minus_scalar":max(map(abs,delta)),
     "signed_chi2_differences":delta,"max_M_fast_minus_scalar":max(map(abs,mdelta)) if mdelta else None,
     "known_P45_chi2_difference":float(vv[0]-f["chi2"]),
     "known_P45_M_difference":float(mm[0]-f["point"]["M_hat"]) if mm is not None else None,
     "coefficients":c}
    out["controls"][family][model]=item
    require(item["max_chi2_fast_minus_scalar"]<=cfg["validation"]["chi2_abs_tolerance"],"chi2 mismatch")
    if mdelta:require(item["max_M_fast_minus_scalar"]<=cfg["validation"]["M_abs_tolerance"],"M mismatch")
    edge,_=fast.evaluate(c,[-.05,.05]);require(np.isinf(edge).all(),"strict prior endpoint mask")
   rounds=[]
   # The vector beta payload repeats control betas to35 components; no integration or new beta points.
   payload=np.resize(beta_fixed,35)
   for j in range(cfg["benchmark"]["rounds"]):
    start=time.perf_counter();cpu=time.process_time()
    for k in range(cfg["benchmark"]["cycles"]):
     for bg in backgrounds:
      c=fast.coefficients(bg);v,m=fast.evaluate(c,payload)
    count=cfg["benchmark"]["cycles"]*len(backgrounds)
    rounds.append({"wall":time.perf_counter()-start,"cpu":time.process_time()-cpu,"background_calls":count})
   rates=[x["wall"]/x["background_calls"] for x in rounds]
   out["benchmarks"][family]={"rounds":rounds,"seconds_per_background_with_beta35_median":float(np.median(rates)),
    "seconds_per_background_with_beta35_max":max(rates),"seconds_per_background_with_beta35_min":min(rates),"coefficient_calls_total":fast.calls,
    "cost_projected_for_three_models_n25_n35":3*(25**3+35**3)*float(np.median(rates)),
    "design_budget_2x_seconds":2*3*(25**3+35**3)*max(rates)}
  out["status"]="EXACT_BETA_ACCELERATION_VALIDATED_GRID_NOT_STARTED"
 except Exception as e:out.update(status="VALIDATION_FAILED_NO_GRID",error=repr(e),traceback=traceback.format_exc())
 out["resources"]={"wall":time.perf_counter()-T0,"cpu":time.process_time()-CPU0,"peak_bytes":core.peak_working_set()}
 save("E45A_VALIDACAO.json",out)
 print(json.dumps({k:out.get(k) for k in ("status","benchmarks","resources","error")}))
 return 0 if out["status"].startswith("EXACT") else 2
def grid(family,model,n,max_seconds):
 cfg,pins,common,core,table,likes,fits=setup(max_seconds)
 validation=read("E45A_VALIDACAO.json");require(validation["status"]=="EXACT_BETA_ACCELERATION_VALIDATED_GRID_NOT_STARTED","validation not passed")
 require(max_seconds<=600,"unit exceeds ceiling")
 like=likes[family];fast=ExactBeta(family,like);fit=fits["families"][family]["fits"][model]
 ax=common.axes_for(fit,like.limits,n);steps=[float(a[1]-a[0]) for a in ax]
 beta=ax[-1] if model=="livre" else np.array([0.0 if model=="lcdm" else like.beta])
 out=common.metadata(cfg,pins);out.update(scope="SINGLE_EXACT_HISTORICAL_GRID_UNIT",family=family,model=model,n=n,theta=fit["theta"],sigma=fit["sigma_JtJ"],
 free=fit["free"],bounds=[[float(a[0]),float(a[-1])] for a in ax],steps=steps,total_nodes=n**len(ax),processed_nodes=0,finite_nodes=0,backgrounds_evaluated=0,
 lnZ=None,observational_integral_completed=False,validation_sha256=sha(ROOT/"E45A_VALIDACAO.json"))
 lsum=-math.inf;lmax=-math.inf;marg=np.full(n,-np.inf) if model=="livre" else None
 try:
  for ix in itertools.product(range(n),repeat=3):
   if out["backgrounds_evaluated"]%128==0:
    require(time.perf_counter()-T0<max_seconds,"time budget")
    require(core.peak_working_set()<cfg["resources"]["peak_bytes_max"],"memory budget")
   bg=[float(ax[j][ix[j]]) for j in range(3)];out["processed_nodes"]+=len(beta)
   if not common.domain(bg+[0.0],like,table):continue
   c=fast.coefficients(bg);chi,m=fast.evaluate(c,beta);logl=-.5*chi;finite=np.isfinite(logl)
   require(np.isfinite(logl[(beta>-.05)&(beta<.05)]).all(),"unexpected nonfinite")
   vals=logl[finite];subtotal=float(np.logaddexp.reduce(vals))
   lsum=float(np.logaddexp(lsum,subtotal));lmax=max(lmax,float(max(vals)));out["finite_nodes"]+=int(finite.sum());out["backgrounds_evaluated"]+=1
   if marg is not None:marg=np.logaddexp(marg,logl)
  require(out["finite_nodes"]>0,"no finite values")
  lnint=lsum+sum(map(math.log,steps));lnprior=sum(math.log(like.limits[k][1]-like.limits[k][0]) for k in fit["free"])
  out.update(status="EXACT_SINGLE_GRID_COMPLETE_NO_VERDICT",ln_integral=lnint,lnZ=lnint-lnprior,ln_prior_volume=lnprior,lnL_max=lmax,observational_integral_completed=True)
  out["laplace_diag_lnZ"]=-.5*fit["chi2"]+.5*len(ax)*math.log(2*math.pi)+sum(math.log(fit["sigma_JtJ"][k]) for k in fit["free"])-lnprior
  if marg is not None:
   dens=np.exp(marg-lsum)/steps[-1];cdf=np.cumsum(dens);cdf/=cdf[-1];pi=1/(like.limits["beta"][1]-like.limits["beta"][0])
   out["beta_marginal"]={"grid":beta.tolist(),"density":dens.tolist(),"quantiles_nodeCDF":{str(q):float(np.interp(q,cdf,beta)) for q in (.025,.16,.5,.84,.975)},
    "fraction_above_beta_tgl":float(dens[beta>=like.beta].sum()/dens.sum()),"fraction_above_zero":float(dens[beta>=0].sum()/dens.sum())}
   out["savage_dickey"]={k:math.log(max(float(np.interp(v,beta,dens)),1e-300)/pi) for k,v in (("tgl_vs_livre",like.beta),("lcdm_vs_livre",0))}
 except Exception as e:out.update(status="STOPPED_PARTIAL_NO_EVIDENCE_CLAIM",error=repr(e),traceback=traceback.format_exc())
 out["resources"]={"wall":time.perf_counter()-T0,"cpu":time.process_time()-CPU0,"peak_bytes":core.peak_working_set()}
 save(f"E45A_GRID_{family}_{model}_n{n}.json",out)
 print(json.dumps({k:out[k] for k in ("status","family","model","n","lnZ","finite_nodes","backgrounds_evaluated","resources")}))
 return 0 if out["observational_integral_completed"] else 2
if __name__=="__main__":
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest="command",required=True);sub.add_parser("validate")
 g=sub.add_parser("grid");g.add_argument("family",choices=("P4_d1b","P5_sombra"));g.add_argument("model",choices=("lcdm","tgl","livre"));g.add_argument("n",type=int,choices=(25,35));g.add_argument("--max-seconds",type=int,default=600)
 a=p.parse_args()
 if a.command=="validate":raise SystemExit(validate())
 raise SystemExit(grid(a.family,a.model,a.n,a.max_seconds))
