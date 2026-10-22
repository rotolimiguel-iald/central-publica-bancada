"""Independent historical P/F4 and P/F5 deterministic reproduction only."""
import os
for k in ("OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","OMP_NUM_THREADS","NUMEXPR_NUM_THREADS"): os.environ[k]="1"
import time,sys,json,math,hashlib,platform,traceback,importlib.util
from pathlib import Path
T0=time.perf_counter(); CPU0=time.process_time()
import numpy as np
import scipy
from scipy.linalg import solve_triangular
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_bytes())
def put(name,d):
 p=ROOT/name;assert not p.exists(),str(p)
 b=(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()
 t=p.with_suffix(p.suffix+".tmp");t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
class SupernovaBlock:
 def __init__(self,table,covariance):
  names=("zHD","zHEL","m_b_corr","IS_CALIBRATOR","CEPH_DIST")
  a=np.genfromtxt(table,names=True,usecols=names,dtype=float,encoding="utf-8")
  cal=a["IS_CALIBRATOR"]==1;mask=(a["zHD"]>.01)|cal
  with covariance.open() as stream:
   n=int(stream.readline());cov=np.loadtxt(stream).reshape(n,n)
  require(len(a)==n==1701,"Pantheon row count")
  selected=cov[np.ix_(mask,mask)];self.asym=float(np.max(abs(selected-selected.T)))
  selected=(selected+selected.T)/2
  self.L=np.linalg.cholesky(selected);self.n=int(mask.sum())
  self.one=solve_triangular(self.L,np.ones(self.n),lower=True)
  self.norm=float(self.one@self.one)
  self.z=a["zHD"][mask];self.hel=a["zHEL"][mask];self.mb=a["m_b_corr"][mask]
  self.cal=cal[mask];self.ceph=a["CEPH_DIST"][mask];self.non=~self.cal
  self.counts={"total":n,"selected":self.n,"calibrators":int(self.cal.sum()),"cosmological":int(self.non.sum())}
  require(self.counts==dict(total=1701,selected=1657,calibrators=77,cosmological=1580),"Pantheon selection mismatch")
 def residual(self,dm_non):
  mu=self.ceph.copy()
  mu[self.non]=5*np.log10((1+self.hel[self.non])*dm_non)+25
  white=solve_triangular(self.L,self.mb-mu,lower=True)
  mh=float(self.one@white/self.norm)
  r=white-mh*self.one
  return r,mh,mu
class Likelihood:
 def __init__(self,inputs,table,sn,phase,reading,nq,proto):
  self.data=inputs;self.table=table;self.sn=sn;self.phase=phase;self.reading=reading;self.nq=nq;self.proto=proto
  self.beta=float(inputs["alpha_codata2018"])*math.sqrt(math.e);self.limits=inputs["limits_declared"];self.count=0
  self.Lp=np.linalg.cholesky(inputs["planck_cov_chen2019"]);self.meanp=np.array(inputs["planck_mean"])
  rows=[line.split() for line in (ROOT/"T4_desi_mean.txt").read_text().splitlines() if line.strip() and not line.lstrip().startswith("#")]
  self.zbao=np.array([float(x[0]) for x in rows]);self.bao=np.array([float(x[1]) for x in rows]);self.kinds=[x[2] for x in rows]
  require(len(self.zbao)==13,"DESI row count")
  self.Lbao=np.linalg.cholesky(np.loadtxt(ROOT/"T4_desi_cov.txt"))
  self.x,self.w=np.polynomial.legendre.leggauss(nq)
  self.radh2=4.4814e-7*2.7255**4*(1+3.046*(7/8)*(4/11)**(4/3))
 def evaluate(self,t):
  self.count+=1;require(time.perf_counter()-T0<self.proto["resources"]["wall_seconds_max"],"wall limit")
  H,wb,wc,beta=t
  for value,k in zip(t,("H0","ombh2","omch2","beta")):
   low,high=self.limits[k];require(low<value<high,"prior support")
  cam=self.table(t);om=(wb+wc+.06/93.14)/(H/100)**2;rad=self.radh2/(H/100)**2;ol=1-om-rad
  def E(z):return np.sqrt(rad*(1+z)**4+om*(1+z)**3+ol)
  istar=(2/3)*math.log(float(E(self.proto["z_star_law"])));K=math.exp(beta*istar)
  def distance(z,boost=False):
   zz=.5*z[:,None]*(self.x+1);e=E(zz)
   factor=np.exp(beta*(istar-(2/3)*np.log(e))) if boost else 1
   return 299792.458/H*.5*z*np.sum(self.w/(e*factor),axis=1)
  dm=distance(self.zbao);dh=299792.458/(H*E(self.zbao));dv=(self.zbao*dm*dm*dh)**(1/3)
  obs=dict(DM_over_rs=dm,DH_over_rs=dh,DV_over_rs=dv)
  bao=np.array([obs[k][i] for i,k in enumerate(self.kinds)])/cam["r_drag"]
  pl=np.array([math.sqrt(om)*H/299792.458*cam["DM_star"],math.pi*cam["DM_star"]/cam["r_star"],wb])
  rs={"planck_comp":solve_triangular(self.Lp,pl-self.meanp,lower=True),"desi_dr2":solve_triangular(self.Lbao,bao-self.bao,lower=True)}
  point={"H0":float(H),"K":K,"I":istar,"H0_local":float(H)*K,"Omega_m":float(om)}
  if self.phase=="fase4":
   x=self.data["sh0es_local"];rs["sh0es_local"]=np.array([(H*K-x["mean"])/x["sigma"]]);point["pull"]=float(rs["sh0es_local"][0])
  else:
   dm_sn=distance(self.sn.z[self.sn.non],boost=self.reading=="acumulada")
   if self.reading=="sombra":dm_sn/=K
   resid,mh,mu=self.sn.residual(dm_sn);rs["pantheon_sh0es"]=resid;point["M_hat"]=mh
  point["chi2"]={k:float(v@v) for k,v in rs.items()}
  return np.concatenate(list(rs.values())),point
def main():
 proto=read("P45_PROTOCOLO.json");freeze=read("P45_PREEXEC_HASHES.json")
 require(sha(ROOT/"P45_PROTOCOLO.json")==freeze["protocol_sha256"],"protocol pin")
 require(sha(Path(__file__))==freeze["code_sha256"],"code pin")
 for name,h in proto["file_pins"].items():require(sha(ROOT/name)==h,"source pin: "+name)
 spec=importlib.util.spec_from_file_location("independent_t4_core",ROOT/"T4_reproduzir.py")
 core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
 core.PROTO=proto;core.T0=T0
 inputs=read("ENTRADAS_HISTORICAS_E_COVARIANCIAS.json");target=read("P45_ALVOS_HISTORICOS.json")
 previous=read("T4_RESULTADO.json");require(previous["status"]=="HISTORICAL_NUMERICAL_REPRODUCTION_WITHIN_FROZEN_TOLERANCES","T4 receipt status")
 snreceipt=read("../reproducao_fase5/RESULT.json");require(snreceipt["status"]=="REAL_INDEPENDENT_ARCHIVED_VALIDATION_REPRODUCTION_NO_NEW_VERDICT","SN-only receipt status")
 out={"scope":proto["scope"],"started_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
 "protocol_sha256":freeze["protocol_sha256"],"code_sha256":freeze["code_sha256"],"file_pins":proto["file_pins"],
 "environment":{"python":sys.version,"executable":sys.executable,"platform":platform.platform(),"numpy":np.__version__,"scipy":scipy.__version__,
 "threads":{k:os.environ[k] for k in ("OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","OMP_NUM_THREADS","NUMEXPR_NUM_THREADS")}},
 "reused_receipts":{"T4":"source pins and table validation only, not rerun","SN_only":"previous independent validation only, not rerun"},
 "fixed_archived_points":{},"families":{},"scientific_verdict":None,"evidence_computed":False,"monte_carlo_computed":False}
 try:
  table=core.FrozenTable(ROOT/"T4_camb_lcdm_v1.npz")
  sn=SupernovaBlock(ROOT/"../reproducao_fase5/Pantheon+SH0ES.dat",ROOT/"../reproducao_fase5/pantheon_covariance.dat")
  require(float(np.max(sn.z[sn.non]))<proto["z_star_law"],"SN support crosses z_star; clamp required")
  require(core.peak_working_set()<=proto["resources"]["peak_working_set_budget_bytes"],"memory budget exceeded before fits")
  out["sample"]=sn.counts;out["covariance_asym_before_symmetrization"]=sn.asym
  out["covariance_scope"]="Planck3x3 and DESI13x13 full; SN1657x1657 from full1701x1701; no cross-block covariance provided; CC absent"
  likes={};tol=proto["tolerances"]
  configurations=[("P4_d1b","fase4","nenhuma"),("P5_sombra","fase5","sombra"),("P5_acumulada","fase5","acumulada")]
  for key,phase,reading in configurations:
   lo=Likelihood(inputs,table,sn,phase,reading,64,proto);hi=Likelihood(inputs,table,sn,phase,reading,128,proto);likes[key]=(lo,hi)
   out["fixed_archived_points"][key]={}
   for model in ("lcdm","tgl","livre"):
    if "theta_"+model not in target[key]:continue
    theta=[target[key]["theta_"+model][k] for k in ("H0","ombh2","omch2","beta")]
    if model=="tgl":theta[3]=lo.beta
    r,p=lo.evaluate(theta);rh,ph=hi.evaluate(theta)
    diff={k:p["chi2"][k]-target[key]["pontos"][model]["chi2"][k] for k in p["chi2"]}
    item={"point":p,"archive_chi2_differences":diff,"residual_GL64_GL128_max":float(max(abs(r-rh)))}
    if phase=="fase5":item["M_hat_difference"]=p["M_hat"]-target[key]["pontos"][model]["M_hat"];item["M_hat_GL128_minus_GL64"]=ph["M_hat"]-p["M_hat"]
    out["fixed_archived_points"][key][model]=item
    require(max(map(abs,diff.values()))<=tol["chi2_block_abs"],key+" fixed point chi2")
    require(item["residual_GL64_GL128_max"]<=tol["quadrature_residual_abs"],key+" quadrature")
    if phase=="fase5":require(abs(item["M_hat_difference"])<=tol["M_abs"],key+" fixed M")
  reused_lcdm=None
  for key,phase,reading in configurations:
   lo,hi=likes[key];a=target[key];out["families"][key]={"fits":{}}
   initial=None
   for model in ("lcdm","tgl","livre"):
    if key=="P5_acumulada" and model=="lcdm":
     f=json.loads(json.dumps(reused_lcdm));f["reused_from"]="P5_sombra/lcdm"
    else:f=core.fit(model,lo,initial)
    out["families"][key]["fits"][model]=f
    require(f["success"],key+"/"+model+" optimizer failed")
    if model=="lcdm":
     initial=[f["theta"][k] for k in ("H0","ombh2","omch2","beta")]
     if key=="P5_sombra":reused_lcdm=f
    diffs={"chi2":f["chi2"]-a["chi2"][model],
           "chi2_blocks":{k:f["point"]["chi2"][k]-a["pontos"][model]["chi2"][k] for k in f["point"]["chi2"]},
           "H0":f["theta"]["H0"]-a["pontos"][model]["H0"],"K":f["point"]["K"]-a["pontos"][model]["K"]}
    if "theta_"+model in a:diffs["theta"]={k:f["theta"][k]-a["theta_"+model][k] for k in f["theta"]}
    if phase=="fase5":diffs["M_hat"]=f["point"]["M_hat"]-a["pontos"][model]["M_hat"]
    f["differences"]=diffs
    t=[f["theta"][k] for k in ("H0","ombh2","omch2","beta")]
    r,p=lo.evaluate(t);rh,ph=hi.evaluate(t)
    f["GL128_minus_GL64_chi2"]=float(rh@rh-r@r)
    f["GL64_GL128_residual_max"]=float(max(abs(r-rh)))
    require(abs(diffs["chi2"])<=tol["chi2_total_abs"] and max(map(abs,diffs["chi2_blocks"].values()))<=tol["chi2_block_abs"],key+"/"+model+" chi2 minimum")
    require(f["GL64_GL128_residual_max"]<=tol["quadrature_residual_abs"],key+"/"+model+" quadrature")
    require(abs(diffs["H0"])<=tol["H0_abs"],key+"/"+model+" H0")
    for name in ("ombh2","omch2"):
     if "theta" in diffs:require(abs(diffs["theta"][name])<=tol["density_abs"],key+"/"+model+" density")
    if phase=="fase5":require(abs(diffs["M_hat"])<=tol["M_abs"],key+"/"+model+" M")
   l,t,f=[out["families"][key]["fits"][m] for m in ("lcdm","tgl","livre")]
   bh=f["theta"]["beta"];sb=f["sigma_JtJ"]["beta"];delta=bh-lo.beta
   statistics={"beta_tgl_runtime":lo.beta,"beta_livre":bh,"sigma_beta_JtJ":sb,"delta":delta,"z_delta":delta/sb,
   "z_perfil_beta_tgl":math.sqrt(max(t["chi2"]-f["chi2"],0)),
   ("z_ganho_da_lei" if phase=="fase4" else "z_tensao"):math.copysign(math.sqrt(abs(l["chi2"]-t["chi2"])),l["chi2"]-t["chi2"])}
   differences={k:v-a[k] for k,v in statistics.items() if k in a}
   out["families"][key]["statistics"]=statistics;out["families"][key]["statistics_differences"]=differences
   require(abs(bh-a["beta_livre"])<=tol["beta_abs"],key+" beta")
   require(abs(sb/a["sigma_beta_JtJ"]-1)<=tol["sigma_beta_relative"],key+" sigma beta")
   for name,val in differences.items():
    if name.startswith("z_"):require(abs(val)<=tol["z_abs"],key+" "+name)
  out["checks"]={"all_source_pins":True,"all_fixed_points_before_any_fit":True,"quadrature_convergence":True,"all_optimizers_success":True,
 "archived_statistics_tolerances":True,"shared_F5_LCDM_fitted_once":True,"T4_and_SN_only_not_rerun":True}
  out["likelihood_evaluations"]=sum(lo.count+hi.count for lo,hi in likes.values())
  out["fits_executed"]=8;out["status"]="HISTORICAL_P4_P5_NUMERICAL_REPRODUCTION_WITHIN_FROZEN_TOLERANCES"
 except Exception as e:
  out["status"]="CRITICAL_DIVERGENCE_STOP_NO_EXTENSION";out["error"]=repr(e);out["traceback"]=traceback.format_exc()
 out["resources"]={"wall_seconds":time.perf_counter()-T0,"cpu_seconds":time.process_time()-CPU0,"peak_working_set_bytes":core.peak_working_set(),"limits":proto["resources"]}
 put("P45_RESULTADO.json",out)
 print(json.dumps({"status":out["status"],"resources":out["resources"],"checks":out.get("checks"),"error":out.get("error"),
 "families":{k:{"chi2":{m:f["chi2"] for m,f in v["fits"].items()},"statistics":v.get("statistics")} for k,v in out["families"].items()}},ensure_ascii=False))
 return 0 if out["status"].startswith("HISTORICAL_P4") else 2
if __name__=="__main__":
 if sys.argv[1:]!=["--run"]:raise SystemExit("Only explicit --run is accepted")
 raise SystemExit(main())
