"""Conditional shape forecast from redshifts/covariances only; no data likelihood fit."""
from pathlib import Path
import datetime, hashlib, json, math, os, time
import numpy as np
import scipy
from scipy.linalg import cholesky, solve_triangular
ROOT=Path(__file__).resolve().parent
START=time.perf_counter()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write_json(name,obj):
 p=ROOT/name;assert not p.exists(),str(p)
 b=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf-8")
 t=p.with_name(p.name+".tmp");t.write_bytes(b);assert t.stat().st_size==len(b)
 os.replace(t,p);assert p.read_bytes()==b
def load(name):return json.loads((ROOT/name).read_bytes())
alpha_source=load("alpha_source.json")
ALPHA_FINE_CODATA_2018=alpha_source["alpha"]
beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
H0=70.; OM=.3; OR=9e-5; C_LIGHT=299792.458; RD=147.
plan_paths=["PLANO_ANTES_DO_PODER.md","ADENDO_FONTES_ANTES_DO_PODER.md"]
plan_proof=[{"path":str(ROOT/x),"sha256":sha(ROOT/x),"mtime_ns":(ROOT/x).stat().st_mtime_ns} for x in plan_paths]
assert all(x["mtime_ns"]<time.time_ns() for x in plan_proof)
checks=[]
def check(name,condition,detail=None):
 checks.append({"name":name,"passed":bool(condition),"detail":detail})
 assert condition,name
def expansion(z,om=OM):return np.sqrt(om*(1+z)**3+OR*(1+z)**4+1-om-OR)
def distance_integrals(z,om=OM,b=beta,n=128):
 z=np.asarray(z)
 nodes,w=np.polynomial.legendre.leggauss(n)
 x=z[:,None]*(nodes[None,:]+1)/2
 e=expansion(x,om)
 ordinary=z/2*((1/e)@w)
 transported=z/2*((e**(2*b/3)/e)@w)
 return ordinary,transported
def covariance(matrix,label):
 check(label+"_square",matrix.ndim==2 and matrix.shape[0]==matrix.shape[1])
 check(label+"_finite",np.isfinite(matrix).all())
 asym=float(np.max(np.abs(matrix-matrix.T)))
 check(label+"_symmetry",asym<=1e-6,asym)
 check(label+"_positive_diagonal",np.all(np.diag(matrix)>0))
 symmetric=(matrix+matrix.T)/2
 L=cholesky(symmetric,lower=True,check_finite=True)
 check(label+"_cholesky",np.all(np.diag(L)>0))
 return L,{"n":len(matrix),"max_absolute_asymmetry":asym,
           "min_diagonal":float(np.min(np.diag(matrix))),
           "min_cholesky_diagonal":float(np.min(np.diag(L))),
           "treatment":"(C+C.T)/2; no eigenvalue repair"}
def white(L,x):return solve_triangular(L,x,lower=True,check_finite=True)
def projected(a,j,names):
 a=np.asarray(a);raw=float(a@a)
 if len(names):
  U,s,v=np.linalg.svd(j,full_matrices=False)
  threshold=np.finfo(float).eps*max(j.shape)*s[0]
  rank=int(np.sum(s>threshold))
  check("full_nuisance_rank_"+str(names),rank==len(names))
  U=U[:,:rank];r=a-U@(U.T@a)
  orth=float(np.linalg.norm(U.T@r))
  check("projection_orthogonal_"+str(names),orth<1e-10)
  singular=s.tolist()
 else:r=a;rank=0;orth=0.;singular=[]
 d2=float(r@r)
 check("projection_nonincrease_"+str(names),d2<=raw+1e-9)
 d=math.sqrt(max(d2,0))
 return {"D_expected":d,"D_squared":d2,"nuisance_rank":rank,"nuisances":names,
         "retained_fraction_vs_fixed_amplitude":None if raw==0 else d2/raw,
         "nuisance_singular_values":singular,"orthogonality_residual":orth,
         "ideal_uniform_sigma_improvement_for_D5":None if d<=1e-12 else 5/d}
snmeta=load("pantheon_metadata_only.json")
zfull=np.array([r["zHD"] for r in snmeta])
zhfull=np.array([r["zHEL"] for r in snmeta])
cal=np.array([r["IS_CALIBRATOR"] for r in snmeta])
mask=(zfull>.01)&(cal==0)
z=zfull[mask];zh=zhfull[mask]
with (ROOT/"pantheon_STAT_SYS.cov").open(encoding="utf-8") as f:
 N=int(f.readline());covsn=np.loadtxt(f).reshape(N,N)
check("SN_covariance_rows_match_metadata",N==len(snmeta)==1701)
covsn=covsn[np.ix_(mask,mask)]
Lsn,sn_cov_info=covariance(covsn,"Pantheon_STAT_SYS_selected")
I,Iac=distance_integrals(z)
Q=Iac/I;k=expansion(z)**(2*beta/3)
s_sn=5*np.log10(Q)
I64,Iac64=distance_integrals(z,n=64)
qref=float(np.max(np.abs(Q-Iac64/I64)))
check("Q_quadrature_64_128",qref<1e-12,qref)
check("Q_bounds",np.all(Q>=1-1e-13) and np.all(Q<=k+1e-13))
i0,ia0=distance_integrals(z,b=0)
check("beta_zero_signal",float(np.max(abs(ia0/i0-1)))<1e-14)
h=1e-4
def sn_derivative(step):
 ip,_=distance_integrals(z,om=OM+step);im,_=distance_integrals(z,om=OM-step)
 return (5*np.log10(ip)-5*np.log10(im))/(2*step)
ds=sn_derivative(h/2);ds_coarse=sn_derivative(h)
dref=float(np.max(abs(ds-ds_coarse)))
check("sn_Om_derivative_convergence",dref<1e-6,dref)
swhite=white(Lsn,s_sn);onewhite=white(Lsn,np.ones(len(z)));dswhite=white(Lsn,ds)
sn_fixed=projected(swhite,np.empty((len(z),0)),[])
sn_amp=projected(swhite,onewhite[:,None],["SN_intercept_M_H0_Kstar"])
sn_om=projected(swhite,np.column_stack([onewhite,dswhite]),["SN_intercept_M_H0_Kstar","Omega_m_tangent"])
sn_const_control=projected(onewhite,onewhite[:,None],["SN_constant_control"])
check("SN_constant_erased",sn_const_control["D_expected"]<1e-10)
meta=load("desi_metadata_only.json")
zb=np.array([r["z"] for r in meta]);typ=[r["type"] for r in meta]
covb=np.loadtxt(ROOT/"desi_DR2.cov")
check("BAO_covariance_rows_match_metadata",covb.shape==(len(meta),len(meta)))
Lb,bao_cov_info=covariance(covb,"DESI_DR2")
def bao_prediction(om=OM):
 ib,iab=distance_integrals(zb,om=om)
 dm=C_LIGHT/H0*ib;dh=C_LIGHT/H0/expansion(zb,om);dv=(dm**2*zb*dh)**(1/3)
 values={"DM_over_rs":dm/RD,"DH_over_rs":dh/RD,"DV_over_rs":dv/RD}
 return np.array([values[t][i] for i,t in enumerate(typ)])
y=bao_prediction()
ib,iab=distance_integrals(zb);qb=iab/ib;kb=expansion(zb)**(2*beta/3)
ratios={"DM_over_rs":qb,"DH_over_rs":kb,"DV_over_rs":qb**(2/3)*kb**(1/3)}
ratio=np.array([ratios[t][i] for i,t in enumerate(typ)])
s_b=y*(ratio-1)
def bao_derivative(step):return (bao_prediction(OM+step)-bao_prediction(OM-step))/(2*step)
db=bao_derivative(h/2);db_coarse=bao_derivative(h)
bref=float(np.max(abs(db-db_coarse)))
check("BAO_Om_derivative_convergence",bref<1e-5,bref)
bwhite=white(Lb,s_b);ywhite=white(Lb,y);dbwhite=white(Lb,db)
bao_fixed=projected(bwhite,np.empty((len(zb),0)),[])
bao_amp=projected(bwhite,ywhite[:,None],["BAO_common_inverse_H0_rd_Kstar"])
bao_om=projected(bwhite,np.column_stack([ywhite,dbwhite]),["BAO_common_inverse_H0_rd_Kstar","Omega_m_tangent"])
bao_const_control=projected(ywhite,ywhite[:,None],["BAO_common_scale_control"])
check("BAO_common_scale_erased",bao_const_control["D_expected"]<1e-10)
na=len(z);nb=len(zb)
ja=np.concatenate([onewhite,np.zeros(nb)])
jb=np.concatenate([np.zeros(na),ywhite])
jom=np.concatenate([dswhite,dbwhite])
jointJ=np.column_stack([ja,jb])
jointJom=np.column_stack([ja,jb,jom])
joint={}
for name,bsg in [("A_luminosity_only",np.zeros(nb)),("B_universal_geometry_extra_assumption",bwhite)]:
 a=np.concatenate([swhite,bsg])
 joint[name]={"fixed_amplitudes":projected(a,np.empty((na+nb,0)),[]),
 "independent_amplitudes":projected(a,jointJ,["SN_intercept","BAO_common_scale"]),
 "independent_amplitudes_shared_Om":projected(a,jointJom,["SN_intercept","BAO_common_scale","shared_Omega_m_tangent"])}
check("SN_Om_reduces_distance",sn_om["D_expected"]<=sn_amp["D_expected"])
check("BAO_Om_reduces_distance",bao_om["D_expected"]<=bao_amp["D_expected"])
check("joint_A_zero_BAO_fixed_matches_SN",abs(joint["A_luminosity_only"]["fixed_amplitudes"]["D_expected"]-sn_fixed["D_expected"])<1e-12)
check("joint_A_amps_matches_SN_amp",abs(joint["A_luminosity_only"]["independent_amplitudes"]["D_expected"]-sn_amp["D_expected"])<1e-12)
arrays={"SN":[{"source_row_zero_based":int(i),"zHD":float(a),"zHEL":float(b),"Q":float(q),"signal_mu_mag":float(s),"dmu_dOmega_m":float(d)} for i,a,b,q,s,d in zip(np.where(mask)[0],z,zh,Q,s_sn,ds)],
 "BAO":[{"z":float(a),"type":t,"fiducial_not_observed":float(v),"ratio_map_B":float(q),"signal_map_B":float(s),"derivative_Om":float(d),"sigma_from_covariance":float(err)} for a,t,v,q,s,d,err in zip(zb,typ,y,ratio,s_b,db,np.sqrt(np.diag(covb)))]}
write_json("TEMPLATES_SEM_CENTROS.json",arrays)
result={"status":"DERIVED_CONDITIONAL_FORECAST_NO_OBSERVED_SIGNIFICANCE_NO_VERDICT",
 "author":"chatgpt-codex/ordem-018/derivacoes",
 "created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "input":{"H0_fid_km_s_Mpc":H0,"Omega_m_fid":OM,"Omega_r_fid":OR,"rd_fid_Mpc":RD,
 "alpha_CODATA_2018":ALPHA_FINE_CODATA_2018,"beta_runtime":beta},
 "method":{"metric":"D=sqrt(s^T W s), covariance-weighted separation of model templates",
 "marginalization":"Analytic common amplitudes; Omega_m linear tangent with flat prior, not data fit",
 "joint_crosscovariance":"ZERO assumed; not measured","observed_means_parsed":False,
 "fiducial_BAO_values_are_not_data":True,"SN_selection":"zHD>0.01 and IS_CALIBRATOR==0",
 "BAO_A_signal":"exactly zero by specified motor mapping",
 "dualities":{"A":"eta_ac/eta_s=Q if angular distance unchanged; normalization not fixed",
 "B":"eta=1 if luminosity/angular share transport; extra hypothesis"}},
 "SN":{"n_selected":len(z),"z_range":[float(min(z)),float(max(z))],
 "max_template_magnitude":float(max(s_sn)),"covariance":sn_cov_info,
 "fixed_amplitude":sn_fixed,"intercept_projected":sn_amp,"intercept_Om_projected":sn_om},
 "BAO_B_extra_hypothesis":{"n":len(zb),"covariance":bao_cov_info,
 "fixed_amplitude":bao_fixed,"common_projected":bao_amp,"common_Om_projected":bao_om},
 "joint":joint,"controls":{"SN_constant":sn_const_control,"BAO_common_scale":bao_const_control},
 "checks":checks,"checks_passed":sum(x["passed"] for x in checks),
 "quadrature_max_delta_Q":qref,"SN_derivative_max_delta":dref,"BAO_derivative_max_delta":bref,
 "precalculation_plan":plan_proof,
 "software":{"python":os.sys.version,"numpy":np.__version__,"scipy":scipy.__version__},
 "source_hashes":[{"file":x,"sha256":sha(ROOT/x),"bytes":(ROOT/x).stat().st_size} for x in [
 "pantheon_metadata_only.json","pantheon_STAT_SYS.cov","desi_metadata_only.json","desi_DR2.cov","alpha_source.json","FONTES_COVARIANCIAS_METADATA.json",Path(__file__).name]],
 "elapsed_seconds":time.perf_counter()-START,"providers_called":[],"request_ids":[]}
write_json("PODER_FORMA.json",result)
print(json.dumps({k:result[k] for k in ["status","SN","BAO_B_extra_hypothesis","joint","checks_passed","elapsed_seconds"]},ensure_ascii=False,indent=2))
