"""Independent byte/AST custody checks only; no candidate evaluation."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
P=ROOT/"f9_affine_profile_preparation"
OUT=ROOT/"proveniencia/revisao_f9_affine_profile"
checks=[];sources={}
def pin(p):
 b=p.read_bytes();v={"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()};sources[str(p)]=v;return v
def read(p):pin(p);return p.read_bytes()
def check(name,value):
 checks.append({"name":name,"pass":bool(value)})
 if not value:raise AssertionError(name)
def literal(tree,name):
 n=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id==name for x in n.targets))
 return ast.literal_eval(n.value)
initial=json.loads(read(OUT/"SNAPSHOT_INICIAL.json"))
for x in initial["pins"]:check("snapshot:"+Path(x["path"]).name,pin(Path(x["path"]))==x)
manifest=json.loads(read(P/"MANIFESTO_PREPARACAO.json"))
contract=json.loads(read(P/"CONTRATO_API.json"))
lineage=json.loads(read(P/"SOURCE_LINEAGE.json"))
for key,x in lineage["sources_verified_now"].items():check("source:"+key,pin(Path(x["path"]))==x)
check("request_source_pin",pin(Path(lineage["request"]["path"]))==lineage["request"])
tree=ast.parse(read(P/"affine_profile.py"))
ast.parse(read(P/"prepare_static.py"))
c=ast.parse(read(Path(lineage["sources_verified_now"]["consumer"]["path"])))
p=ast.parse(read(Path(lineage["sources_verified_now"]["physical_prior"]["path"])))
check("request_id",literal(tree,"REQUEST_ID")==manifest["request_id"]==contract["request_id"]==lineage["request_id"])
check("source_pins",literal(tree,"SOURCE_PINS")==lineage["sources_verified_now"]==contract["source_pins"])
check("actual_module_pin",pin(P/"affine_profile.py")==contract["module"])
check("MODEL_order_and_dependencies",literal(tree,"MODELS")==literal(c,"MODELS")==literal(p,"MODELS")==tuple(contract["models"]))
cp=literal(c,"SOURCE_PINS");pp=literal(p,"SOURCE_PINS")
check("prior_consumer_pin",pp["f9_likelihood_consumer_preparation/likelihood_consumer.py"]==lineage["sources_verified_now"]["consumer"])
check("consumer_linear_pin",cp["linear_gaussian"]==lineage["sources_verified_now"]["linear_gaussian"])
check("consumer_support_pin",cp["support"]==lineage["sources_verified_now"]["singular_gaussian"])
check("consumer_identity",literal(c,"REQUEST_ID")=="a9874f79-9d71-48f5-824c-d51d6d819534")
check("prior_identity",literal(p,"REQUEST_ID")=="df482198-56c4-4169-ae5e-3908f5d12f2c")
for name,expected in (("BETA_LIMITS",(-0.05,0.05)),("S_LIMITS",(-0.15,0.15)),("RD_LIMITS",(130.0,160.0))):
 check("prior_domain:"+name,literal(p,name)==expected)
functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
entry=functions["profile_at_fixed_theta"]
check("signature", [x.arg for x in entry.args.args]==contract["positional"] and [x.arg for x in entry.args.kwonlyargs]==contract["keyword_only_required"] and not entry.args.defaults and all(x is None for x in entry.args.kw_defaults) and not entry.args.vararg and not entry.args.kwarg)
imports=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
check("only_math_import",imports==["import math"])
calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
names=[ast.unparse(n.func) for n in calls]
check("one_existing_evaluate_five",names.count("joint.evaluate_five")==1)
check("three_existing_curves",names.count("p._Curve")==3)
peaks=[n for n in calls if isinstance(n.func,ast.Attribute) and n.func.attr=="peak"]
check("peak_no_prior_shift",len(peaks)==1 and not peaks[0].args and not peaks[0].keywords)
check("no_hidden_retry_or_search",not any(isinstance(n,(ast.Try,ast.While)) for n in ast.walk(tree)))
for forbidden in ("open","eval","exec","compile","__import__","minimize","svd","pinv","inv","solve","integrate_at_fixed_theta","assemble_five","get_background"):
 check("no_call:"+forbidden,not any(isinstance(n.func,ast.Name) and n.func.id==forbidden or isinstance(n.func,ast.Attribute) and n.func.attr==forbidden for n in calls))
cert=ast.literal_eval(functions["_unavailable_certificates"].body[0].value)
check("certificate_defaults",cert==contract["certificate_defaults"])
ret=entry.body[-1].value
out={ast.literal_eval(k):v for k,v in zip(ret.keys,ret.values)}
for name in ("global_minima","relative_evidence","lnB","p","sigma","verdict"):check("unavailable:"+name,ast.literal_eval(out[name]) is None)
for name in ("physical_extra_priors_applied","global_theta_search_performed"):check("false:"+name,ast.literal_eval(out[name]) is False)
prepared=next(n for n in c.body if isinstance(n,ast.ClassDef) and n.name=="PreparedJoint")
curve=next(n for n in p.body if isinstance(n,ast.ClassDef) and n.name=="_Curve")
curve_methods={n.name:n for n in curve.body if isinstance(n,ast.FunctionDef)}
check("existing_curve_methods",{"__init__","mean","log_likelihood","peak"}<=set(curve_methods))
check("peak_default_zero",len(curve_methods["peak"].args.defaults)==1 and ast.literal_eval(curve_methods["peak"].args.defaults[0])==0.0)
check("consumer_evaluate_five_exists",any(isinstance(n,ast.FunctionDef) and n.name=="evaluate_five" for n in prepared.body))
check("no_authorization_or_claim",not any(q.name.startswith(("AUTH","AUTORIZACAO","CLAIM")) for q in P.iterdir()))
for x in initial["pins"]:check("final_snapshot:"+Path(x["path"]).name,pin(Path(x["path"]))==x)
for key,x in lineage["sources_verified_now"].items():check("final_source:"+key,pin(Path(x["path"]))==x)
data={"at_utc":datetime.now(timezone.utc).isoformat(),"reviewer":"chatgpt-codex/ordem-018/proveniencia","request_id":manifest["request_id"],"status":"STATIC_METADATA_ONLY_NO_NUMERICAL_CONTROL","checks":checks,"source_pins":list(sources.values()),"candidate_imports":0,"candidate_or_backend_calls":0,"controls_executed":0,"solver_calls":0,"WSL":0,"observed_reads":False,"call_sites":names,"source_ranges_reviewed":{"affine_profile.py":"1-239","physical_prior.py":"_Curve83-151 and integration252-356","likelihood_consumer.py":"PreparedJoint319-414 and admission helpers","linear_gaussian.py":"1-79","singular_gaussian_v2.py":"1-97"}}
b=(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode();f=OUT/"EVIDENCIA_ESTATICA.json";assert not f.exists();t=f.with_name(f.name+".tmp");t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,f)
print(json.dumps({"checks":len(checks),"all_pass":all(x["pass"] for x in checks),"source_paths":len(sources),"evidence":pin(f)}))
