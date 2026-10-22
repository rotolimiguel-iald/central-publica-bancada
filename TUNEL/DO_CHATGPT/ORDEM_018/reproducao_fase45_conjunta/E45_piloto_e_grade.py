"""Historical evidence pilot and unexecuted streaming-grid unit; no original imports."""
import os
for key in ("OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","OMP_NUM_THREADS","NUMEXPR_NUM_THREADS"):os.environ[key]="1"
import argparse,json,math,time,hashlib,sys,platform,importlib.util,itertools,traceback
from pathlib import Path
T0=time.perf_counter();CPU0=time.process_time()
import numpy as np
import scipy
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_bytes())
def save(n,d):
 p=ROOT/n;assert not p.exists(),str(p)
 b=(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()
 t=p.with_suffix(p.suffix+".tmp");t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def load_module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def setup(max_seconds):
 cfg=read("E45_PROTOCOLO_PILOTO_E_GRADE.json");pins=read("E45_PREEXEC_HASHES.json")
 require(sha(ROOT/"E45_PROTOCOLO_PILOTO_E_GRADE.json")==pins["protocol_sha256"],"protocol hash")
 require(sha(Path(__file__))==pins["code_sha256"],"code hash")
 for n,h in cfg["file_pins"].items():require(sha(ROOT/n)==h,"input hash: "+n)
 core=load_module("independent_t4_evidence",ROOT/"T4_reproduzir.py")
 p45=load_module("independent_p45_evidence",ROOT/"P45_reproduzir.py")
 runtime=read("P45_PROTOCOLO.json")
 runtime["resources"]["wall_seconds_max"]=max_seconds;core.PROTO=runtime;core.T0=T0;p45.T0=T0
 table=core.FrozenTable(ROOT/"T4_camb_lcdm_v1.npz")
 sn=p45.SupernovaBlock(ROOT/"../reproducao_fase5/Pantheon+SH0ES.dat",ROOT/"../reproducao_fase5/pantheon_covariance.dat")
 inp=read("ENTRADAS_HISTORICAS_E_COVARIANCIAS.json")
 likes={k:p45.Likelihood(inp,table,sn,ph,re,64,runtime) for k,ph,re in
 [("P4_d1b","fase4","nenhuma"),("P5_sombra","fase5","sombra"),("P5_acumulada","fase5","acumulada")]}
 fits=read("P45_RESULTADO.json")
 require(fits["status"]=="HISTORICAL_P4_P5_NUMERICAL_REPRODUCTION_WITHIN_FROZEN_TOLERANCES","P45 status")
 require(core.peak_working_set()<cfg["pilot_limits"]["peak_bytes_max"],"RAM limit")
 return cfg,pins,core,table,likes,fits
def metadata(cfg,pins):
 return {"identity":cfg["identity"],"created_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
 "protocol_sha256":pins["protocol_sha256"],"code_sha256":pins["code_sha256"],
 "environment":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"executable":sys.executable,"platform":platform.platform(),"threads":1},
 "scientific_verdict":None,"fits_rerun":False,"originals_executed":False,"monte_carlo":False}
def axes_for(fit,limits,n):
 axes=[]
 for name in fit["free"]:
  sig=fit["sigma_JtJ"].get(name) or .05*(limits[name][1]-limits[name][0])
  low=max(limits[name][0],fit["theta"][name]-6*sig);high=min(limits[name][1],fit["theta"][name]+6*sig)
  if name=="beta":low,high=limits["beta"]
  axes.append(np.linspace(low,high,n))
 return axes
def domain(t,like,table):
 if any(not (like.limits[k][0]<v<like.limits[k][1]) for v,k in zip(t,("H0","ombh2","omch2","beta"))):return False
 for v,ax in zip(t[:3],table.axes):
  pos=(v-ax[0])/(ax[1]-ax[0])
  if not 1<=pos<=len(ax)-2:return False
 return True
def synthetic():
 # Proper scalar normal likelihood over an explicit uniform prior: not observational data.
 mean=.01;sig=.0022;lo=-.05;hi=.05;beta_point=read("ENTRADAS_HISTORICAS_E_COVARIANCIAS.json")["alpha_codata2018"]*math.sqrt(math.e)
 norm=math.sqrt(2*math.pi)*sig
 exact_int=norm*.5*(math.erf((hi-mean)/(math.sqrt(2)*sig))-math.erf((lo-mean)/(math.sqrt(2)*sig)))
 rows={}
 for n in (25,35):
  x=np.linspace(lo,hi,n);dx=x[1]-x[0];w=np.exp(-.5*((x-mean)/sig)**2);w[[0,-1]]=0
  approx=w.sum()*dx;dens=w/approx;cdf=np.cumsum(w);cdf/=cdf[-1]
  pt=float(np.interp(beta_point,x,dens));exact_pt=math.exp(-.5*((beta_point-mean)/sig)**2)/exact_int
  # Constant-L diagnostic makes endpoint weights and masked endpoints visible exactly.
  rows[str(n)]={"lnZ":math.log(approx/(hi-lo)),"lnZ_error":math.log(approx/exact_int),
  "interpolated_log_point_density_error":math.log(pt/exact_pt),"left_node_cdf_median":float(np.interp(.5,cdf,x)),
  "cdf_median_error":float(np.interp(.5,cdf,x))-mean,
  "constant_L_inclusive_relative_error":n/(n-1)-1,
  "constant_L_strict_prior_endpoints_relative_error":(n-2)/(n-1)-1}
 return {"status":"SYNTHETIC_ONLY_NOT_OBSERVATIONAL_INTEGRAL","mean":mean,"sigma":sig,"prior":[lo,hi],"beta_point_runtime":beta_point,
 "exact_lnZ":math.log(exact_int/(hi-lo)),"rows":rows,
 "meaning":"Small grid25/35 log-integral error alone does not certify interpolated point density or node-CDF quantiles; rectangular endpoint effects remain."}
def benchmark():
 cfg,pins,core,table,likes,fits=setup(120)
 out=metadata(cfg,pins);out["scope"]="PILOT_AT_ALREADY_EVALUATED_THETA_NO_OBSERVATIONAL_INTEGRAL"
 out["synthetic"]=synthetic();out["benchmarks"]={};out["grid_geometry"]={}
 rounds=cfg["pilot_limits"]["rounds"];repeat=cfg["pilot_limits"]["repeat_cycle_per_round"]
 for key,like in likes.items():
  ff=fits["families"][key]["fits"]
  samples=[(m,[f["theta"][k] for k in ("H0","ombh2","omch2","beta")],f["chi2"]) for m,f in ff.items()]
  maxerr=0.0
  for m,t,old in samples:
   r,p=like.evaluate(t);maxerr=max(maxerr,abs(float(r@r)-old))
  rows=[]
  for rep in range(rounds):
   w0=time.perf_counter();c0=time.process_time()
   for j in range(repeat):
    for m,t,old in samples:
     r,p=like.evaluate(t);maxerr=max(maxerr,abs(float(r@r)-old))
   rows.append({"wall":time.perf_counter()-w0,"cpu":time.process_time()-c0,"calls":repeat*len(samples)})
  require(maxerr<=cfg["tolerances"]["repeat_chi2_abs"],"unchanged point failed: "+key)
  rates=[v["wall"]/v["calls"] for v in rows]
  out["benchmarks"][key]={"samples":"P45 receipt theta, no new parameter points","rounds":rows,"seconds_per_call_median":float(np.median(rates)),
  "seconds_per_call_min":min(rates),"seconds_per_call_max":max(rates),"max_chi2_difference":maxerr}
  out["grid_geometry"][key]={}
  for model,f in ff.items():
   out["grid_geometry"][key][model]={}
   for n in (25,35):
    ax=axes_for(f,like.limits,n)
    out["grid_geometry"][key][model][str(n)]={"total_nodes":n**len(f["free"]),"free":f["free"],"bounds":[[float(a[0]),float(a[-1])] for a in ax],
    "steps":[float(a[1]-a[0]) for a in ax],
    "declared_log_prior_volume":sum(math.log(like.limits[k][1]-like.limits[k][0]) for k in f["free"])}
 out["cost_projection"]={};total=0.0;totalnodes=0
 for key in likes:
  nodes=(2 if key!="P5_acumulada" else 1)*(25**3+35**3)+(25**4+35**4)
  median=out["benchmarks"][key]["seconds_per_call_median"];duration=nodes*median
  out["cost_projection"][key]={"nodes_upper_bound":nodes,"seconds_serial_estimate":duration,"hours_serial_estimate":duration/3600,
  "seconds_design_budget_2x":2*nodes*out["benchmarks"][key]["seconds_per_call_max"]}
  total+=duration;totalnodes+=nodes
 out["cost_projection"]["total"]={"nodes":totalnodes,"seconds":total,"hours":total/3600,"note":"Linear extrapolation on this CPU, not measured full-run time; ignores skipped invalid points; no automatic batch."}
 out["resources"]={"wall_seconds":time.perf_counter()-T0,"cpu_seconds":time.process_time()-CPU0,"peak_bytes":core.peak_working_set()}
 out["status"]="PILOT_COMPLETE_GRID_NOT_STARTED"
 save("E45_PILOTO_RESULTADO.json",out)
 print(json.dumps({"status":out["status"],"cost":out["cost_projection"],"resources":out["resources"],"synthetic":out["synthetic"]}))
def grid(family,model,n,max_seconds):
 # Prepared only. The coordinator must authorize a later bounded unit before this mode is invoked.
 cfg,pins,core,table,likes,fits=setup(max_seconds)
 require(max_seconds<=cfg["future_grid_limits"]["wall_seconds_per_unit_max"],"requested time exceeds frozen limit")
 like=likes[family];fit=fits["families"][family]["fits"][model]
 ax=axes_for(fit,like.limits,n);steps=[float(a[1]-a[0]) for a in ax]
 out=metadata(cfg,pins);out.update(scope="ONE_HISTORICAL_GRID_UNIT",family=family,model=model,n=n,center_source="P45 verified fit receipt; no refit",
 theta=fit["theta"],sigma=fit["sigma_JtJ"],free=fit["free"],steps=steps,bounds=[[float(a[0]),float(a[-1])] for a in ax],
 grid_total_nodes=n**len(ax),finite_nodes=0,processed_nodes=0,lnZ=None,observational_integral_completed=False)
 lsum=-math.inf;lmax=-math.inf;bmarg=np.full(n,-np.inf) if model=="livre" else None
 try:
  for ix in itertools.product(range(n),repeat=len(ax)):
   if out["processed_nodes"]%512==0:
    require(time.perf_counter()-T0<max_seconds,"time budget; preserve partial and stop")
    require(core.peak_working_set()<cfg["future_grid_limits"]["peak_bytes_max"],"RAM budget; stop")
   t=[fit["theta"][k] for k in ("H0","ombh2","omch2","beta")]
   for j,k in enumerate(fit["free"]):t[("H0","ombh2","omch2","beta").index(k)]=float(ax[j][ix[j]])
   out["processed_nodes"]+=1
   if not domain(t,like,table):continue
   r,point=like.evaluate(t);v=-.5*float(r@r);require(math.isfinite(v),"unexpected nonfinite in valid support")
   lsum=float(np.logaddexp(lsum,v));lmax=max(lmax,v);out["finite_nodes"]+=1
   if bmarg is not None:bmarg[ix[-1]]=np.logaddexp(bmarg[ix[-1]],v)
  require(out["finite_nodes"]>0,"no finite nodes")
  lnint=lsum+sum(map(math.log,steps));lnprior=sum(math.log(like.limits[k][1]-like.limits[k][0]) for k in fit["free"])
  out.update(ln_integral=lnint,lnZ=lnint-lnprior,lnL_max=lmax,ln_prior_volume=lnprior,observational_integral_completed=True,status="SINGLE_GRID_COMPLETE_NO_VERDICT")
  out["laplace_diag_lnZ"]=-.5*fit["chi2"]+.5*len(ax)*math.log(2*math.pi)+sum(math.log(fit["sigma_JtJ"][k]) for k in fit["free"])-lnprior
  if bmarg is not None:
   dens=np.exp(bmarg-lsum)/steps[-1];b=ax[-1];pi=1/(like.limits["beta"][1]-like.limits["beta"][0]);cdf=np.cumsum(dens);cdf/=cdf[-1]
   out["beta_marginal"]={"grid":b.tolist(),"density":dens.tolist(),"quantiles_nodeCDF":{str(q):float(np.interp(q,cdf,b)) for q in (.025,.16,.5,.84,.975)},
    "fraction_above_beta_tgl":float(dens[b>=like.beta].sum()/dens.sum()),"fraction_above_zero":float(dens[b>=0].sum()/dens.sum())}
   out["savage_dickey"]={k:math.log(max(float(np.interp(v,b,dens)),1e-300)/pi) for k,v in (("tgl_vs_livre",like.beta),("lcdm_vs_livre",0))}
 except Exception as e:out.update(status="STOPPED_PARTIAL_NO_EVIDENCE_CLAIM",error=repr(e),traceback=traceback.format_exc())
 out["resources"]={"wall_seconds":time.perf_counter()-T0,"cpu_seconds":time.process_time()-CPU0,"peak_bytes":core.peak_working_set()}
 save(f"E45_GRID_{family}_{model}_n{n}.json",out)
 print(json.dumps({k:out[k] for k in ("status","family","model","n","processed_nodes","finite_nodes","lnZ","resources")}))
 return 0 if out["observational_integral_completed"] else 2
if __name__=="__main__":
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest="command",required=True);sub.add_parser("benchmark")
 g=sub.add_parser("grid");g.add_argument("family",choices=("P4_d1b","P5_sombra","P5_acumulada"));g.add_argument("model",choices=("lcdm","tgl","livre"));g.add_argument("n",type=int,choices=(25,35));g.add_argument("--max-seconds",type=int,default=600)
 a=p.parse_args()
 if a.command=="benchmark":benchmark()
 else:raise SystemExit(grid(a.family,a.model,a.n,a.max_seconds))
