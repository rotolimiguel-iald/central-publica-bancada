"""Static review metadata only: bytes, JSON and AST. Never import reviewed modules."""
from pathlib import Path
import ast, hashlib, json, os
from datetime import datetime, timezone
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
PKG=BASE/"f9_theta_qualification_preparation"
OWN=BASE/"proveniencia"/"revisao_f9_theta_qualification"
REQ="4e9a80ad-dac3-4c6c-8ec5-b7927a9c056d"
checks=[]; pins={}
def check(name,condition):
    checks.append({"name":name,"pass":bool(condition)})
    if not condition: raise AssertionError(name)
def pin(p):
    p=Path(p); b=p.read_bytes()
    r={"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
    pins[str(p)]=r
    return r
def verify(record,label):
    actual=pin(record["path"])
    check(label, actual["bytes"]==record["bytes"] and actual["sha256"]==record["sha256"])
    return actual
def atomic_json(p,value):
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode()
    if p.exists(): raise RuntimeError("REVIEW_OUTPUT_ALREADY_EXISTS:"+str(p))
    tmp=p.with_name(p.name+".tmp")
    with tmp.open("xb") as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes()==raw
    os.replace(tmp,p)
    assert p.read_bytes()==raw
manifest= json.loads((PKG/"MANIFESTO_PREPARACAO.json").read_bytes())
mpin=pin(PKG/"MANIFESTO_PREPARACAO.json")
check("manifest_reported_bytes_and_hash",mpin["bytes"]==2721 and mpin["sha256"]=="c45638cd489aa1739a90d07c9bc8d19a7f0aaab081e4521765d5d5562810b1da")
check("manifest_request",manifest["request_id"]==REQ)
check("eight_members_one_backup",len(manifest["members"])==8 and len(manifest["backups"])==1)
for i,r in enumerate(manifest["members"]+manifest["backups"]): verify(r,"manifest_pin_"+str(i))
contract=json.loads((PKG/"CONTROL_CONTRACT.json").read_bytes())
lineage=json.loads((PKG/"SOURCE_LINEAGE.json").read_bytes())
check("contract_request",contract["request_id"]==REQ)
check("lineage_contract_sources_equal",lineage["sources"]==contract["sources"])
for i,r in enumerate(contract["sources"]): verify(r,"contract_source_"+str(i))
check("fifteen_sources",len(contract["sources"])==15)
verify(contract["runtime"]["interpreter"],"interpreter")
verify(contract["candidate"],"candidate")
for group in ("theta_source_pins","prior_source_pins"):
    for k,r in contract[group].items(): verify(r,group+":"+k)
check("cases_binding",pin(PKG/"cases.py")["sha256"]==contract["case_source_sha256"])
check("driver_binding",pin(PKG/"driver.py")["sha256"]==contract["driver_source_sha256"])
check("case_order_exact",contract["case_order"]==["T01","T02","T03","T04","T05","T06","N01","N02","N03","N04","N05","N06","N07","N08","N09"])
check("cases_match_order",[x["id"] for x in contract["cases"]]==contract["case_order"])
check("fifteen_cases",len(contract["cases"])==contract["case_count"]==15)
check("callback_counts",[x["expected_callbacks"] for x in contract["cases"]]==[125]*6+[0,3,2,2,1,2,2,1,2])
check("metadata_callback_sum",sum(x["expected_callbacks"] for x in contract["cases"])==765==contract["maximum_total_evaluations"]==contract["exact_expected_total_callbacks"])
check("construction_run_node_caps",contract["maximum_constructor_attempts"]==15 and contract["maximum_run_attempts"]==16 and contract["maximum_unique_nodes_per_instance"]==125)
asts={}
for name in ("cases.py","driver.py","build_preparation.py"):
    tree=ast.parse((PKG/name).read_bytes(),filename=str(PKG/name))
    imports=sorted({n.names[0].name if isinstance(n,ast.Import) else n.module for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))})
    asts[name]={"imports":imports,"functions":[{"name":n.name,"line":n.lineno,"end_line":n.end_lineno} for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)]}
    check("ast_parsed:"+name, isinstance(tree,ast.Module))
    check("no_scientific_imports:"+name,not any(str(x).split(".")[0] in {"numpy","scipy","camb","bilby","lal","lalsimulation"} for x in imports))
tree=ast.parse(Path(contract["candidate"]["path"]).read_bytes(),filename=contract["candidate"]["path"])
check("candidate_ast_only",isinstance(tree,ast.Module))
asts["candidate"]={"classes":[n.name for n in ast.walk(tree) if isinstance(n,ast.ClassDef)],"functions":[{"name":n.name,"line":n.lineno,"end_line":n.end_lineno} for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)]}
initial=json.loads((OWN/"SNAPSHOT_INICIAL.json").read_bytes())
for i,r in enumerate(initial["pins"]): verify(r,"unchanged_since_initial_"+str(i))
absence={}
for name in ("ROOT_DECISION.json","RUN_CLAIM.json","CLAIM.json","AUTH.json","AUTHORIZATION.json","execution_once","__pycache__"):
    absence[name]=not(PKG/name).exists()
    check("no_consumption:"+name,absence[name])
receipt={
 "schema":"INDEPENDENT_STATIC_THETA_REVIEW_V1","request_id":REQ,
 "reviewer":"chatgpt-codex/ordem-018/proveniencia","map_before":620,
 "at_utc":datetime.now(timezone.utc).isoformat(),"status":"STATIC_ACCEPTANCE_LIMITED_NOT_EXECUTION",
 "material_blockers":[],"checks":checks,"check_count":len(checks),"all_checks_pass":all(x["pass"] for x in checks),
 "pins":list(pins.values()),"pin_count":len(pins),"asts":asts,"absence_at_read":absence,
 "candidate_imports":0,"controls_executed":0,"numerical_reference_execution":0,"authorization_created":False,"claim_created":False,
 "manual_review":"Full cases, driver, contract, references and pertinent integrator source; analytical reasoning only. See PARECER_Q01_THETA.md.",
 "trust_boundaries":["ROOT validates actual independent review before decision","Pinned trusted harness, not arbitrary hostile-code sandbox","Runtime exe pinned, not full stdlib/DLL closure","Future external supervisor exit0 plus no failure required","I02 equality, actual guard/POSIX cache and Q02 excluded"],
 "report":pin(OWN/"PARECER_Q01_THETA.md")
}
atomic_json(OWN/"RECIBO_REVISAO_E_PINS.json",receipt)
print(json.dumps({"checks":len(checks),"unique_pins":receipt["pin_count"],"all_pass":receipt["all_checks_pass"],"receipt":pin(OWN/"RECIBO_REVISAO_E_PINS.json")},ensure_ascii=False))
