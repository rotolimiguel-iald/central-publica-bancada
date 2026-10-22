"""Independent exact algebra review; consumes pinned documentary design, no data."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter, defaultdict
import json, hashlib, time, datetime

ROOT=Path(__file__).resolve().parent
def digest(p):
 b=p.read_bytes()
 return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def save(name,obj):
 p=ROOT/name
 if p.exists():raise RuntimeError("No overwrite "+str(p))
 b=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
 t=p.with_name(p.name+".tmp")
 with t.open("xb") as f:f.write(b)
 assert t.read_bytes()==b
 t.replace(p)
 assert p.read_bytes()==b
def rank(rows):
 basis={}
 for raw in rows:
  row={k:Q(v) for k,v in raw.items() if v}
  while row:
   col=min(row)
   if col in basis:
    f=row[col]
    for j,v in basis[col].items():
     z=row.get(j,Q(0))-f*v
     if z:row[j]=z
     else:row.pop(j,None)
   else:
    f=row[col];basis[col]={j:v/f for j,v in row.items()}
    break
 return len(basis)
def main():
 t0=time.perf_counter();c0=time.process_time()
 pr=json.loads((ROOT/"PROTOCOLO_REVISAO_LINEAR.json").read_text(encoding="utf-8"))
 for item in pr["inputs"]:assert digest(Path(item["path"]))==item,item["path"]
 files={Path(f["path"]).name:Path(f["path"]) for f in pr["inputs"]}
 spec=json.loads(files["ESPECIFICACAO_LINEAR.json"].read_text(encoding="utf-8"))
 measure=json.loads(files["MEDIDA_NUISANCE_CANDIDATA.json"].read_text(encoding="utf-8"))
 manifest=json.loads(files["MANIFESTO_ENTREGA.json"].read_text(encoding="utf-8"))
 checks=[]
 def check(name,value,details=None):
  checks.append({"name":name,"pass":bool(value),"details":details})
  if not value:raise RuntimeError(name+": "+str(details))
 md={Path(x["path"]).name:x for x in manifest["files"]}
 for name in files:
  if name in md:check("pin:"+name,digest(files[name])==md[name])
 rows=spec["rows"];rm={r["row_id"]:r for r in rows}
 keys=[x["key"] for x in spec["eta_columns"]]
 check("unique_rows",len(rm)==len(rows)==267)
 check("unique_eta",len(set(keys))==len(keys)==63)
 check("eta_common_with_measure",spec["eta_columns"]==measure["eta_columns"])
 check("null_observed_objects",all(v is None for v in spec["values"].values()))
 ix={k:i for i,k in enumerate(keys)}
 matrices=[]
 for r in rows:
  check("valid_columns:"+r["row_id"],set(r["X"])<=set(keys))
  matrices.append({ix[k]:Q(v) for k,v in r["X"].items()})
 Xh=[dict(x,**{})|({63:Q(r["a_h"])} if Q(r["a_h"]) else {}) for x,r in zip(matrices,rows)]
 Xhc=[x|({64:Q(r["c_C"])} if Q(r["c_C"]) else {}) for x,r in zip(Xh,rows)]
 ranks={"X":rank(matrices),"X_h":rank(Xh),"X_h_c_C":rank(Xhc)}
 check("full_ranks",ranks=={"X":63,"X_h":64,"X_h_c_C":65},ranks)
 expected={"host":178,"group":13,"SN_calibrator":55,"SBF_calibrator":14,"SN_HF":1,"SBF_HF":1,"megamaser":5}
 check("families",dict(Counter(r["family"] for r in rows))==expected)
 check("a_h_seven",sum(Q(r["a_h"])!=0 for r in rows)==7)
 check("c_C_119",sum(Q(r["c_C"])!=0 for r in rows)==119)
 for r in rows:
  x={k:Q(v) for k,v in r["X"].items()};f=r["family"];ah=Q(r["a_h"]);cc=Q(r["c_C"])
  if f=="host":ok=len(x)==1 and next(iter(x)).startswith("mu_host:") and list(x.values())==[Q(1)] and ah==0 and cc in (0,1)
  elif f=="group":ok=len(x)==2 and sorted(x.values())==[-1,1] and any(k.startswith("mu_host:") and v==1 for k,v in x.items()) and any(k.startswith("mu_group:") and v==-1 for k,v in x.items()) and ah==cc==0
  elif f in ("SN_calibrator","SBF_calibrator"):
   mag="M_B" if f=="SN_calibrator" else "M110_offset"
   ok=len(x)==2 and x.get(mag)==1 and any(k.startswith("mu_host:") and v==1 for k,v in x.items()) and ah==cc==0
  elif f in ("SN_HF","SBF_HF"):ok=x=={("M_B" if f=="SN_HF" else "M110_offset"):Q(-1,5)} and ah==1 and cc==0
  else:ok=x=={} and ah==1 and cc==0
  check("recipe:"+r["row_id"],ok)
 graph=spec["mas_hms_graph"];gm={e["row_id"]:e for e in graph}
 host_ids=[r["row_id"] for r in rows if r["family"]=="host"]
 check("graph_covers_host_rows",set(gm)==set(host_ids) and len(gm)==len(graph)==178)
 hkeys=sorted({e["HMS"] for e in graph});mkeys=sorted({e["MAS"] for e in graph})
 verts=[("HMS",k) for k in hkeys]+[("MAS",k) for k in mkeys]
 vi={v:i for i,v in enumerate(verts)};parent=list(range(len(verts)))
 def find(i):
  while parent[i]!=i:
   parent[i]=parent[parent[i]];i=parent[i]
  return i
 def union(i,j):parent[find(i)]=find(j)
 B=[]
 for e in graph:
  i=vi["HMS",e["HMS"]];j=vi["MAS",e["MAS"]];union(i,j);B.append({i:Q(1),j:Q(1)})
 groups=defaultdict(list)
 for e in graph:groups[find(vi["HMS",e["HMS"]])].append(e)
 comps=[]
 for es in groups.values():
  hs={e["HMS"] for e in es};ms={e["MAS"] for e in es}
  comps.append({"HMS":len(hs),"MAS":len(ms),"edges":len(es),"rank":len(hs)+len(ms)-1,"cycles":len(es)-len(hs)-len(ms)+1})
 comps.sort(key=lambda x:(-x["edges"],x["HMS"],x["MAS"]))
 check("vertices_components",len(hkeys)==104 and len(mkeys)==11 and len(comps)==9)
 br=rank(B)
 check("incidence_rank",br==106==len(verts)-len(comps),br)
 check("only_R22_cycles",sorted(c["cycles"] for c in comps)==[0]*8+[72],comps)
 order={r["row_id"]:i for i,r in enumerate(rows)}
 cycles=spec["deterministic_cycles"]
 L=[{order[rid]:Q(w) for rid,w in c["coefficients"].items()} for c in cycles]
 lr=rank(L);check("cycle_rank",lr==len(cycles)==72,lr)
 for c in cycles:
  totals=defaultdict(Q)
  for rid,w0 in c["coefficients"].items():
   w=Q(w0);row=rm[rid]
   for k,v in row["X"].items():totals["X:"+k]+=w*Q(v)
   totals["a_h"]+=w*Q(row["a_h"]);totals["c_C"]+=w*Q(row["c_C"])
   e=gm[rid]
   for label in ("HMS","MAS","anchor"):totals[label+":"+e[label]]+=w
  check("cycle_annihilation:"+c["id"],all(v==0 for v in totals.values()))
 check("cycles_complete_kernel",lr+br==len(graph))
 # Explicit range witness: assign host/method coefficients to each HMS primitive.
 primitives={}
 for e in graph:
  r=rm[e["row_id"]];vec=({k:Q(v) for k,v in r["X"].items()},Q(r["a_h"]),Q(r["c_C"]))
  if e["HMS"] in primitives:check("same_HMS_vector:"+e["row_id"],primitives[e["HMS"]]==vec)
  primitives[e["HMS"]]=vec
 check("stellar_h_zero",all(Q(rm[e["row_id"]]["a_h"])==0 for e in graph))
 hostX=[{ix[k]:Q(v) for k,v in rm[e["row_id"]]["X"].items()} for e in graph]
 Bhc=[b|{len(verts)+k:v for k,v in x.items()}|({len(verts)+63:Q(rm[e["row_id"]]["c_C"])} if Q(rm[e["row_id"]]["c_C"]) else {}) for b,x,e in zip(B,hostX,graph)]
 check("incidence_range_by_augmented_rank",rank(Bhc)==br)
 direct={next(iter(r["X"])) for r in rows if r["family"]=="host"}
 allhosts={k for k in keys if k.startswith("mu_host:")}
 extra=sorted(allhosts-direct)
 check("host_counts",len(direct)==53 and len(allhosts)==59)
 witness=spec["rank_certificate"]["mixed_host_witness"];w0,w1=(rm[k] for k in witness)
 check("mixed_host_witness",w0["X"]==w1["X"] and Q(w0["a_h"])==Q(w1["a_h"])==0 and Q(w0["c_C"])!=Q(w1["c_C"]),witness)
 check("five_common_models",len(measure["common_to"])==5)
 check("measure_choice_explicitly_open",measure["adopted_choice"] is None and measure["proper_prior_hyperparameters_selected"] is False)
 result={"identity":pr["identity"],"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"EXACT_DOCUMENTARY_ALGEBRA_PASS","inputs":pr["inputs"],"protocol":digest(ROOT/"PROTOCOLO_REVISAO_LINEAR.json"),"script":digest(Path(__file__)),"checks":checks,"n_checks":len(checks),"all_pass":all(x["pass"] for x in checks),"rank":ranks|{"stellar_incidence":br,"cycles":lr},"components_independent":comps,"extra_host_columns":extra,"full_C_built":False,"data_centres_opened":False,"upstream_executed":False,"S_g_H0_lnB_evaluated":False,"wall_seconds":time.perf_counter()-t0,"cpu_seconds":time.process_time()-c0}
 save("REVISAO_LINEAR_RECIBO.json",result)
 print(json.dumps({k:result[k] for k in ["status","n_checks","all_pass","rank","components_independent","extra_host_columns","wall_seconds","cpu_seconds"]}))
if __name__=="__main__":main()
