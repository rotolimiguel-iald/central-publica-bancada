"""Read bytes and AST only; never import or call the prepared reducer/driver."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os
ROOT=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
P=ROOT/"f9_decision_reducer_preparation"
OUT=ROOT/"proveniencia/revisao_f9_decision_reducer"
sources=[];checks=[]
def pin(p):
 b=p.read_bytes();return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def read(p):sources.append(pin(p));return p.read_bytes()
def check(name,ok):
 checks.append({"name":name,"passed":bool(ok)})
 if not ok:raise AssertionError(name)
mraw=read(P/"MANIFESTO_PREPARACAO.json");m=json.loads(mraw)
for e in m["artifacts"]:
 p=Path(e["path"]);check("manifest:"+p.name,pin(p)==e);read(p)
contract_path=Path(m["source_contract"]["path"]);check("contract_pin",pin(contract_path)==m["source_contract"])
contract=json.loads(read(contract_path))
tree=ast.parse(read(P/"decision_reducer.py"));driver=ast.parse(read(P/"logical_checks.py"))
assignments={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
check("contract_literal",assignments["CONTRACT_SHA256"]==m["source_contract"]["sha256"])
check("test_names_order",list(assignments["TESTS"])==[x["id"] for x in contract["primary_family"]["claims"]])
check("multiplicity_5",len(assignments["TESTS"])==contract["primary_family"]["m"]==5)
check("calibration_states",list(assignments["CALIBRATIONS"])==contract["verdict"]["decision_predicates"]["calibration_per_test_per_scenario"]["allowed_calibration_status"])
imports=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
check("reducer_import_math_only",imports==["import math"])
call_names=sorted({ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call)})
check("no_reducer_io_or_dynamic_import_calls",not any(x in call_names for x in ("open","eval","exec","compile","__import__","os.system","importlib.import_module")))
f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="evaluate_decisions")
check("function_interface",len(f.args.args)==1 and f.args.args[0].arg=="records" and [a.arg for a in f.args.kwonlyargs]==["scenario_ids","readiness","contract_sha256"])
check("module_top_level_is_definitions_only",all(isinstance(n,(ast.Expr,ast.Import,ast.Assign,ast.ClassDef,ast.FunctionDef)) for n in tree.body))
main=next(n for n in driver.body if isinstance(n,ast.FunctionDef) and n.name=="main")
cases=[]
for n in main.body:
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id in ("check","rejected"):
  arg=n.value.args[0];check("constant_case_name:"+str(n.lineno),isinstance(arg,ast.Constant) and isinstance(arg.value,str))
  cases.append({"name":arg.value,"line":n.lineno,"kind":n.value.func.id})
 elif isinstance(n,ast.For) and ast.unparse(n.iter)=="module.TESTS[:2]":
  c=next(x for x in n.body if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and getattr(x.value.func,"id","")=="check")
  prefix=c.value.args[0].left.value
  for test in assignments["TESTS"][:2]:cases.append({"name":prefix+test,"line":c.lineno,"kind":"check","expanded_static_loop":True})
check("24_static_case_labels",len(cases)==24==m["logical_checks_planned"])
check("case_names_unique",len({x["name"] for x in cases})==24)
for name in ("REVISAO_ROOT.json","CLAIM_LOGIC.json","RESULT_LOGIC.json"):
 check("not_present:"+name,not(P/name).exists())
end=[pin(Path(x["path"])) for x in m["artifacts"]]
check("final_members_unchanged",end==m["artifacts"])
check("final_manifest_unchanged",pin(P/"MANIFESTO_PREPARACAO.json")==sources[0])
check("final_contract_unchanged",pin(contract_path)==m["source_contract"])
data={"at_utc":datetime.now(timezone.utc).isoformat(),"status":"STATIC_REVIEW_ONLY_NOT_LOGICAL_CHECK_EXECUTION","source_pins":list({x["path"]:x for x in sources}.values()),"checks":checks,"reducer_call_names":call_names,"planned_cases_static":cases,"candidate_imports":0,"candidate_calls":0,"logical_tests_executed":0,"science_calls":0,"data_read":False,"final_members":end}
OUT.mkdir(exist_ok=True)
b=(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode();p=OUT/"EVIDENCIA_ESTATICA.json"
assert not p.exists()
t=p.with_name(p.name+".tmp");t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
print(json.dumps({"metadata_checks":len(checks),"all_passed":all(x["passed"] for x in checks),"planned_cases_count":len(cases),"source_paths":len(data["source_pins"]),"evidence":pin(p)}))
