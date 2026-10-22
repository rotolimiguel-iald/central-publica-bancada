"""Authorized software-only tests of AST-extracted additive functions and isolated custody fixtures."""
from pathlib import Path
import ast, hashlib, json, math, os, time
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/"stage/patents/_formula_completa/tgl_formula_completa.py"
raw=SOURCE.read_bytes()
expected=json.loads((ROOT/"VALIDACAO_ESTATICA.json").read_bytes())["shared_layer_candidate"]["sha256"]
assert hashlib.sha256(raw).hexdigest()==expected
tree=ast.parse(raw)
names={"_scale_nonnegative_float","alpha_of_chi_v388","beta_of_chi_v388","scale_reading_v388","beta_of_mu_v388","_adendo_v388_no_cofre","beta"}
nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names]
assert {n.name for n in nodes}==names
alpha_nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="ALPHA_FINE_CODATA_2018" for t in n.targets)]
assert len(alpha_nodes)==1
alpha=ast.literal_eval(alpha_nodes[0].value)
ns={"math":math,"Path":Path,"json":json,"ALPHA_FINE_CODATA_2018":alpha}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SOURCE)+"::selected_AST","exec"),ns)
checks=[]
started=time.perf_counter()
def check(name,fn):
    try:
        result=fn()
        if result is not True: raise AssertionError("Predicate was not exactly True")
    except Exception as e:
        checks.append({"name":name,"pass":False,"type":type(e).__name__,"message":str(e)})
    else: checks.append({"name":name,"pass":True})
def raises(kind,fn):
    try: fn()
    except kind: return True
    except Exception: return False
    return False
scale=ns["_scale_nonnegative_float"]; alpha_fn=ns["alpha_of_chi_v388"]
beta_fn=ns["beta_of_chi_v388"]; reading=ns["scale_reading_v388"]
for label,value in (("bool_true",True),("bool_false",False),("string","1"),("complex",1+0j),("none",None)):
    check("reject_type_"+label,lambda v=value:raises(TypeError,lambda:scale(v,"chi")))
for label,value in (("negative",-1.0),("nan",float("nan")),("positive_inf",float("inf")),("negative_inf",-float("inf")),("huge_integer",10**1000)):
    check("reject_domain_"+label,lambda v=value:raises(ValueError,lambda:scale(v,"chi")))
check("chi_zero_alpha_one",lambda:alpha_fn(0)==1.0)
check("chi_zero_beta_sqrt_e",lambda:beta_fn(0)==math.sqrt(math.e))
check("legacy_beta_runtime_preserved",lambda:ns["beta"]()==alpha*math.sqrt(math.e))
for x in (0.125,1.0,4.0,10.0,100.0):
    check("sech_float_formula_"+str(x),lambda x=x:math.isclose(alpha_fn(x),1/math.cosh(x/2),rel_tol=4e-15,abs_tol=0.0))
for x,u in ((0.0,0.0),(0.0,1.0),(1.0,1.0),(1.0,4.0),(4.0,10.0),(10.0,100.0)):
    def floor_case(x=x,u=u):
        r=reading(x,u)
        return r["beta_chi"]>=r["floor_at_chi_sup"]>0 and r["mu"] is None and r["mu_status"]=="OPEN_NOT_ASSIGNED" and not r["physical_verdict_allowed"]
    check("conditional_floor_"+str(x)+"_"+str(u),floor_case)
check("reject_reversed_interval",lambda:raises(ValueError,lambda:reading(2,1)))
check("reject_chi_sup_bool",lambda:raises(TypeError,lambda:reading(1,True)))
check("positive_underflow_is_error",lambda:raises(ArithmeticError,lambda:alpha_fn(2000)))
check("mu_remains_not_implemented",lambda:raises(NotImplementedError,lambda:ns["beta_of_mu_v388"](1)))
check("chi_zero_not_legacy_beta0",lambda:beta_fn(0)!=ns["beta"]())

FIX=ROOT/"software_fixtures"
if FIX.exists(): raise RuntimeError("Fixtures already exist; no automatic replay")
FIX.mkdir()
um=FIX/"um"; kernel=FIX/"kernel"; um.mkdir();kernel.mkdir()
target=um/"synthetic_payload.txt"; target.write_bytes(b"synthetic local fixture only\n")
meta={"custody_pins":[{"base":"um","relative":target.name,"bytes":target.stat().st_size,"sha256":hashlib.sha256(target.read_bytes()).hexdigest()}],
      "source_um_sha256":"synthetic-fixture-not-scientific-pin",
      "source_statute":"SYNTHETIC_FIXTURE","source_reported_kernel_flags":{}}
meta_raw=(json.dumps(meta,sort_keys=True)+"\n").encode()
meta_file=FIX/"ADENDO_V388_METADATA.json";meta_file.write_bytes(meta_raw)
ns.update({"__file__":str(FIX/"synthetic_adapter.py"),"VERSAO_DA_CAMADA":"v386","V388_METADATA_SHA256":hashlib.sha256(meta_raw).hexdigest(),
           "_sha":lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(),
           "_cofre_corrente":lambda:(388,um,kernel)})
adendo=ns["_adendo_v388_no_cofre"]
cf={"cofre":"um_unificado_v388"}
check("fixture_valid_pins",lambda:adendo(cf)["physical_scale_mu_status"]=="OPEN_PER_DEVICE_AND_RITE")
check("fixture_wrong_custody_label",lambda:raises(RuntimeError,lambda:adendo({"cofre":"um_unificado_v386"})))
ns["_cofre_corrente"]=lambda:(389,um,kernel)
check("fixture_wrong_version",lambda:raises(RuntimeError,lambda:adendo(cf)))
ns["_cofre_corrente"]=lambda:(388,um,kernel)
ns["V388_METADATA_SHA256"]="0"*64
check("fixture_metadata_pin_mismatch",lambda:raises(RuntimeError,lambda:adendo(cf)))
ns["V388_METADATA_SHA256"]=hashlib.sha256(meta_raw).hexdigest()
target.write_bytes(b"changed fixture bytes\n")
check("fixture_payload_pin_mismatch",lambda:raises(RuntimeError,lambda:adendo(cf)))
target.write_bytes(b"synthetic local fixture only\n")
original_sha=ns["_sha"]
ns["_sha"]=lambda p:meta["custody_pins"][0]["sha256"] if Path(p)==target else original_sha(p)
target.write_bytes(b"x")
check("fixture_size_mismatch_even_with_hash_stub",lambda:raises(RuntimeError,lambda:adendo(cf)))
target.write_bytes(b"synthetic local fixture only\n")
ns["_sha"]=original_sha
missing=FIX/"missing"
ns["_cofre_corrente"]=lambda:(388,missing,kernel)
check("fixture_missing_payload_read_error",lambda:raises(FileNotFoundError,lambda:adendo(cf)))
ns["_cofre_corrente"]=lambda:(388,um,kernel)
check("fixture_restored_valid_pins",lambda:adendo(cf)["base_layer_preserved"]=="v386")
report={"stage_id":"cdbf8b67-0de2-4bde-83db-30ffa9afde6f",
        "status":"PASS" if all(c["pass"] for c in checks) else "FAIL",
        "utc":datetime.now(timezone.utc).isoformat(),"elapsed_seconds":time.perf_counter()-started,
        "candidate":{"path":str(SOURCE),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()},
        "method":"Only the seven named function definitions plus the exact CODATA input literal were extracted through AST; no candidate module imported. Pure function samples and local synthetic custody fixtures only.",
        "extracted_functions":sorted(names),"checks":checks,"passed":sum(c["pass"] for c in checks),"total":len(checks),
        "limitations":["Software checks, not scientific rite or physical validation","No uniform floating-point error certificate","No real custody read through the candidate function","No device or runner executed","No um.py import/execution, Lean, WSL, observed inputs or providers"],
        "fixture_files":[{"relative":str(p.relative_to(FIX)),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(FIX.rglob("*")) if p.is_file()]}
out=ROOT/"RECIBO_TESTES_SOFTWARE_V388.json"
if out.exists():raise RuntimeError("Result already exists")
b=(json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode()
temp=out.with_suffix(".tmp");temp.write_bytes(b);assert temp.read_bytes()==b;os.replace(temp,out)
print(json.dumps({"status":report["status"],"passed":report["passed"],"total":report["total"],"elapsed_seconds":report["elapsed_seconds"],"receipt":{"path":str(out),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}},ensure_ascii=False))
raise SystemExit(0 if report["status"]=="PASS" else 1)
