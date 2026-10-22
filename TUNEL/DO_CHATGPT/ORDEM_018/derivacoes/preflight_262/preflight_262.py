"""Single bounded error-only preflight of 262 equations, no observed means."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,sys,time,platform,os,traceback
ROOT=Path(__file__).resolve().parent
def info(p):
 b=p.read_bytes();return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def save(name,obj):
 p=ROOT/name
 if p.exists():raise RuntimeError("Refusing overwrite "+str(p))
 b=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf-8");t=p.with_name(p.name+".tmp")
 with t.open("xb") as f:f.write(b)
 assert t.read_bytes()==b;t.replace(p);assert p.read_bytes()==b
def rank(rows):
 basis={}
 for raw in rows:
  row={k:Q(v) for k,v in raw.items() if v}
  while row:
   k=min(row)
   if k not in basis:
    d=row[k];basis[k]={j:v/d for j,v in row.items()};break
   d=row[k]
   for j,v in basis[k].items():
    z=row.get(j,Q(0))-d*v
    if z:row[j]=z
    else:row.pop(j,None)
 return len(basis)
def main():
 started=time.perf_counter();cpu=time.process_time()
 p=ROOT/"PROTOCOLO_PREFLIGHT_262.json";proto=json.loads(p.read_bytes())
 for item in proto["inputs"]:
  assert info(Path(item["path"]))==item,"Input pin changed: "+item["path"]
 src={Path(x["path"]).name:Path(x["path"]) for x in proto["inputs"]}
 for var in proto["threads_env"]:assert os.environ.get(var)=="1","Thread environment differs"
 import numpy as np
 sys.path.insert(0,str(src["linear_gaussian.py"].parent))
 from linear_gaussian import FlatNuisanceGaussian
 from singular_gaussian_v2 import SupportGaussian
 from baseline_stellar import stellar_baseline
 spec=json.loads(src["ESPECIFICACAO_LINEAR.json"].read_bytes())
 errors=json.loads(src["ERROR_COMPONENTS.json"].read_bytes())
 meta=json.loads(src["METADADOS_ERROS_NAO_ESTELARES_V01.json"].read_bytes())
 flow=json.loads(src["FLOW_ERROR_RESULT.json"].read_bytes())
 fp=json.loads(src["FLOW_ERROR_PROTOCOL.json"].read_bytes())
 sp=json.loads(src["STELLAR_FAMILY_PROTOCOL.json"].read_bytes())
 assert flow["protocol_sha256"]==info(src["FLOW_ERROR_PROTOCOL.json"])["sha256"]
 for owner in [fp,sp]:
  for item in owner["inputs"]:
   name=Path(item["path"]).name
   if name in src:
    actual=info(src[name]);assert actual["sha256"]==item["sha256"] and actual["bytes"]==item["bytes"]
 rows=spec["rows"][:262];excluded=spec["rows"][262:]
 assert len(rows)==262 and len(excluded)==5 and all(r["family"]=="megamaser" for r in excluded)
 assert not any(r["family"]=="megamaser" for r in rows)
 assert all(v is None for v in spec["values"].values())
 keys=[r["key"] for r in spec["eta_columns"]];ix={k:i for i,k in enumerate(keys)}
 xr=[{ix[k]:Q(v) for k,v in r["X"].items()} for r in rows]
 xh=[x|({63:Q(r["a_h"])} if Q(r["a_h"]) else {}) for x,r in zip(xr,rows)]
 xhc=[x|({64:Q(r["c_C"])} if Q(r["c_C"]) else {}) for x,r in zip(xh,rows)]
 ranks={"X":rank(xr),"X_a_h":rank(xh),"X_a_h_c_C":rank(xhc)}
 assert ranks=={"X":63,"X_a_h":64,"X_a_h_c_C":65},ranks
 X=np.zeros((262,63));A=np.zeros((262,2))
 for i,r in enumerate(rows):
  for k,v in r["X"].items():X[i,ix[k]]=float(Q(v))
  A[i]=[float(Q(r["a_h"])),float(Q(r["c_C"]))]
 host_ids=[r["row_id"] for r in rows if r["family"]=="host"]
 assert len(host_ids)==178 and host_ids==[r["row_id"] for r in rows[:178]]
 graph={e["row_id"]:e for e in spec["mas_hms_graph"]}
 row_hms={rid:g["key"] for g in errors["primitive_hms_groups"] for rid in g["row_ids"]}
 assert set(host_ids)==set(graph)==set(row_hms)
 host_rows=[]
 for rid in host_ids:
  e=graph[rid];method,anchor,source=e["MAS"].split("&")
  assert anchor==e["anchor"] and row_hms[rid]==e["HMS"]
  host_rows.append({"row_id":rid,"method":method,"anchor":anchor,"source":source})
 baseline=stellar_baseline(errors,host_rows)
 assert baseline.shape==(178,178)
 # Transport both intercept observations and every coefficient by the same map.
 scale=np.ones(262)
 for i,r in enumerate(rows):
  if r["family"] in ("SN_HF","SBF_HF"):scale[i]=5.
 assert np.count_nonzero(scale==5)==2
 Xt=scale[:,None]*X;At=scale[:,None]*A
 variances={}
 for k in ["SN_calibrators","SBF_calibrators","group_equations"]:
  for r in meta[k]:
   assert r["row_id"] not in variances
   v=float(r["variance_mag2_upstream"]);assert np.isfinite(v) and v>0
   variances[r["row_id"]]=v
 assert len(variances)==82
 common=np.zeros((262,262));common[:178,:178]=baseline
 for i,r in enumerate(rows[178:],178):
  if r["row_id"] in variances:common[i,i]=variances[r["row_id"]]
  elif r["family"]=="SN_HF":common[i,i]=flow["SN"]["variance_alpha_conditional_upstream"]
  else:assert r["family"]=="SBF_HF"
 sbfi=next(i for i,r in enumerate(rows) if r["family"]=="SBF_HF")
 variants=[]
 for var in proto["variants"]:
  assert time.perf_counter()-started<proto["max_wall_seconds"]
  C=common.copy();sigma=flow["SBF"][var["flow_sigma_field"]];C[sbfi,sbfi]=sigma*sigma
  Ct=scale[:,None]*C*scale[None,:]
  assert np.isfinite(Ct).all() and np.array_equal(Ct,Ct.T)
  model=FlatNuisanceGaussian(Ct,Xt,**proto["module_tolerances"])
  # The existing module checks both response columns against the same support.
  I=model.response_information(At)
  ev=np.linalg.eigvalsh(I);assert np.isfinite(ev).all() and ev[0]>proto["information_relative_cutoff"]*ev[-1]
  cov=np.linalg.solve(I,np.eye(2));errors_ideal=np.sqrt(np.diag(cov))
  null=model.support.null_vectors
  nullnorms={"X_max_column":float(np.max(np.linalg.norm(null.T@Xt,axis=0))),"a_h":float(np.linalg.norm(null.T@At[:,0])),"c_C":float(np.linalg.norm(null.T@At[:,1]))}
  assert model.support.rank==190 and model.p==63
  assert max(nullnorms.values())<=proto["module_tolerances"]["support_tolerance"]
  variants.append({"id":var["id"],"conditional":True,"SBF_sigma_alpha_used":sigma,"covariance_rank":model.support.rank,"nullity":262-model.support.rank,"X_rank_whitened":len(model.design_singular_values),"X_min_singular_whitened":float(model.design_singular_values[-1]),"X_max_singular_whitened":float(model.design_singular_values[0]),"support_null_column_norms":nullnorms,"covariance_eigen_threshold":model.support.threshold,"covariance_positive_min":float(model.support.positive_eigenvalues[0]),"covariance_positive_max":float(model.support.positive_eigenvalues[-1]),"information_parameter_order":["h_log10","delta_C_mag"],"information_2x2":I.tolist(),"information_eigenvalues_in_stated_parameter_coordinates":ev.tolist(),"ideal_joint_covariance_2x2":cov.tolist(),"ideal_joint_sigma_h_dex":float(errors_ideal[0]),"ideal_joint_sigma_delta_C_mag":float(errors_ideal[1]),"ideal_joint_parameter_correlation":float(cov[0,1]/np.prod(errors_ideal)),"ideal_sigma_other_response_fixed":(1/np.sqrt(np.diag(I))).tolist(),"covariance_transformed_sha256":hashlib.sha256(Ct.astype("<f8").tobytes()).hexdigest(),"data_residual_supplied":False})
 result={"id":proto["id"],"status":"COMPLETED_ERROR_ONLY_CONDITIONAL_PREFLIGHT_262","protocol":info(p),"inputs":proto["inputs"],"row_count":262,"full_V01_row_count":267,"excluded_row_ids":[r["row_id"] for r in excluded],"exclusion_reason":"Five MM variances require central distances; no selection or V1 change","exact_coefficient_ranks_without_MM":ranks,"transformed_rows":[r["row_id"] for r,s in zip(rows,scale) if s!=1],"observation_units":"all rows transformed to mag; h remains log10 H0 and delta_C mag","baseline_formula_source":proto["baseline_extraction"],"variants":variants,"conditional_assumptions":proto["conditional_assumptions"],"runtime":{"python":sys.version,"executable":sys.executable,"numpy":np.__version__,"platform":platform.platform(),"thread_environment":{v:os.environ[v] for v in proto["threads_env"]},"scipy_used":False},"wall_seconds":time.perf_counter()-started,"cpu_seconds":time.process_time()-cpu,"no_centres_y_S_g_fit_H0_lnB":True,"scientific_verdict":None,"global_power_or_detection":None}
 assert result["wall_seconds"]<proto["max_wall_seconds"]
 save("PREFLIGHT_262_RESULT.json",result)
 print(json.dumps({k:result[k] for k in ["status","exact_coefficient_ranks_without_MM","variants","wall_seconds","cpu_seconds"]},allow_nan=False))
if __name__=="__main__":
 try:main()
 except BaseException:
  save("PREFLIGHT_262_FAILURE.json",{"status":"FAILED_NO_RETRY","traceback":traceback.format_exc()})
  raise
