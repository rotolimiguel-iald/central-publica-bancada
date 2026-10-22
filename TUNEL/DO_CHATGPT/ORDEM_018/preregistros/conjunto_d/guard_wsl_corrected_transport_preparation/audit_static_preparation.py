"""Static preparation audit only: reads source/AST/JSON; never imports a candidate."""
from pathlib import Path
import ast, json, hashlib, os, copy
from datetime import datetime, timezone

BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\preregistros\conjunto_d\guard_wsl_corrected_transport_preparation")
OLD=BASE.parent/"guard_wsl_integration_preparation_v2"
checks=[]
def check(name,value,detail=None):
    if not value: raise AssertionError(name)
    checks.append({"name":name,"passed":True,"detail":detail})
def pin(path):
    b=path.read_bytes()
    return {"path":str(path),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def dump(code): return ast.dump(ast.parse(code),include_attributes=False)
def fresh(name,value):
    p=BASE/name
    check("fresh:"+name,not p.exists())
    b=(json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    t=p.with_name(p.name+".tmp")
    with t.open("xb") as f:f.write(b)
    check("temporary:"+name,t.read_bytes()==b)
    os.replace(t,p)
    return pin(p)

ident=json.loads((BASE/"IDENTIDADE_PREPARADA.json").read_bytes())
old_ident=json.loads((OLD/"IDENTIDADE_PREPARADA.json").read_bytes())
contract=json.loads((BASE/"CONTRATO_WSL.json").read_bytes())
old_contract=json.loads((OLD/"CONTRATO_WSL.json").read_bytes())
check("new_request",ident["request_id"]!=old_ident["request_id"])
check("new_case",ident["case_id"]!=old_ident["case_id"])
check("coherent_identity",contract["request_id"]==ident["request_id"] and contract["case_id"]==ident["case_id"])
for field in ["limits","runtime","single_control","identity_and_claims","windows_pins","linux_pins"]:
    check("unchanged_contract:"+field,contract[field]==old_contract[field])
for k in ["failure","not_proved"]:
    check("unchanged_acceptance:"+k,contract["acceptance"][k]==old_contract["acceptance"][k])
check("old_acceptance_preserved",contract["acceptance"]["required"][:len(old_contract["acceptance"]["required"])]==old_contract["acceptance"]["required"])
check("argv_required",len(contract["acceptance"]["required"])==len(old_contract["acceptance"]["required"])+2)
check("old_guard_bytes",(BASE/"sources/audit_guard.py").read_bytes()==(OLD/"sources/audit_guard.py").read_bytes())
for row in contract["local_pins"]:
    actual=pin(BASE/row["relative_path"])
    check("local_pin:"+row["relative_path"],all(actual[k]==row[k] for k in ["bytes","sha256"]))
for row in json.loads((BASE/"SOURCE_CUSTODY_BEFORE.json").read_bytes())["pins"]:
    check("old_unchanged:"+Path(row["path"]).name,pin(Path(row["path"]))==row)
runtime=json.loads((BASE/"RUNTIME_READONLY_RECEIPT.json").read_bytes())
check("fresh_runtime_17",runtime["checks"]==17 and all(x["matches"] for x in runtime["rows"]))
for key in ["linux_pins","windows_pins"]:
    check("runtime_rows:"+key,[r["actual"] for r in runtime["rows"] if r["kind"]==key]==contract[key])
for filename in ["AUTORIZACAO_ROOT.json","CLAIM.json","RUN","RESULT.json","REVISAO_ROOT.json"]:
    check("not_consumed:"+filename,not (BASE/filename).exists())
texts={n:(BASE/n).read_text(encoding="utf-8") for n in ["common.py","worker.py","linux_control.py","launch_windows.py"]}
old_texts={n:(OLD/n).read_text(encoding="utf-8").replace(OLD.name,BASE.name).replace(old_ident["request_id"],ident["request_id"]).replace(old_ident["case_id"],ident["case_id"]) for n in texts}
trees={}
for name,code in texts.items():
    trees[name]=ast.parse(code,filename=name)
    check("AST:"+name,True)
    check("no_old_operational_root:"+name,OLD.name not in code)
    check("no_old_operational_request:"+name,old_ident["request_id"] not in code)
    imports=[]
    for node in ast.walk(trees[name]):
        if isinstance(node,ast.Import):imports.extend(x.name for x in node.names)
        elif isinstance(node,ast.ImportFrom):imports.append(node.module)
    check("stdlib_imports:"+name,set(imports)<=set("os sys json hashlib time pathlib signal types importlib.util importlib.machinery threading copy subprocess selectors fcntl uuid".split()))

def functions(code):
    return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(code).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
original_functions=functions(old_texts["common.py"])
new_functions=functions(texts["common.py"])
for name,value in original_functions.items():
    if name!="argv_for":check("common_preserved:"+name,new_functions[name]==value)
check("only_two_helpers",set(new_functions)-set(original_functions)=={"observed_argv","validate_observed_argv"})
candidate=(BASE.parent/"guard_wsl_path_repair_preparation/common.py.candidate.txt").read_text(encoding="utf-8").replace(OLD.name,BASE.name).replace(old_ident["request_id"],ident["request_id"]).replace(old_ident["case_id"],ident["case_id"])
check("reviewed_POSIX_exact",dump(texts["common.py"].split("\ndef observed_argv",1)[0])==dump(candidate))
check("full_process_observed",'process = serial_identity(proc_identity(os.getpid()))' in texts["common.py"])
check("sysargv_observed",'script_received = list(sys.argv)' in texts["common.py"])
check("full_expectation_recomputed",'expected = argv_for(role, nonce)' in texts["common.py"])
check("not_flags_only",'row["received_process_argv"] == expected' in texts["common.py"] and 'row["received_script_argv"] == expected[6:]' in texts["common.py"])
check("fixed_expected_process_exe",'row["process"]["exe"] == "/usr/bin/python3.12"' in texts["common.py"])
check("no_shell_or_split_in_helpers",not any(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr in {"split","Popen","system"} for x in ast.walk(ast.parse(texts["common.py"].split("\ndef observed_argv",1)[1].join(["def observed_argv",""])))))

class StripTransport(ast.NodeTransformer):
    """Remove ONLY receipt additions to compare complete old control AST."""
    def __init__(self,old):
        self.assignments={}
        for n in ast.walk(ast.parse(old)):
            if isinstance(n,ast.Assign):
                for t in n.targets:
                    if isinstance(t,ast.Name) and t.id in {"self_id","me"}:self.assignments[t.id]=n
        self.cleanup_process=ast.parse("g.serial_identity(g.proc_identity(os.getpid()))",mode="eval").body
    def visit_FunctionDef(self,n):
        n=self.generic_visit(n)
        n.args.args=[a for a in n.args.args if a.arg!="transport"]
        return n
    def visit_Assign(self,n):
        names={t.id for t in n.targets if isinstance(t,ast.Name)}
        if names & {"transport","receipt_name"}:return None
        if names & {"self_id","me"}:
            key=next(iter(names&{"self_id","me"}))
            return copy.deepcopy(self.assignments[key])
        return self.generic_visit(n)
    def visit_Expr(self,n):
        rendered=ast.unparse(n)
        if "validate_observed_argv" in rendered:return None
        if "g.fresh" in rendered and ("ARGV_CHILD.json" in rendered or "receipt_name" in rendered):return None
        if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=="need" and "argv_transport" in rendered:return None
        return self.generic_visit(n)
    def visit_Dict(self,n):
        pairs=[(k,v) for k,v in zip(n.keys,n.values) if not (isinstance(k,ast.Constant) and k.value=="argv_transport")]
        n.keys=[k for k,v in pairs];n.values=[v for k,v in pairs]
        for index,(k,v) in enumerate(zip(n.keys,n.values)):
            if isinstance(k,ast.Constant) and k.value=="process" and ast.unparse(v)=="transport['process']":
                n.values[index]=copy.deepcopy(self.cleanup_process)
        return self.generic_visit(n)
    def visit_Call(self,n):
        if isinstance(n.func,ast.Name) and n.func.id in {"supervise","cleanup"} and n.args and isinstance(n.args[-1],ast.Name) and n.args[-1].id=="transport":n.args.pop()
        return self.generic_visit(n)
for name in ["worker.py","linux_control.py","launch_windows.py"]:
    stripped=StripTransport(old_texts[name]).visit(copy.deepcopy(trees[name]))
    check("whole_AST_preserved_except_receipts:"+name,ast.dump(stripped,include_attributes=False)==dump(old_texts[name]))
check("receiver_before_hook",texts["worker.py"].index('g.observed_argv("--child",nonce)') < texts["worker.py"].index('sys.addaudithook(audit)'))
check("receiver_before_guard_source",texts["worker.py"].index('g.observed_argv("--child",nonce)') < texts["worker.py"].index('raw=(BASE/"sources/audit_guard.py")'))
check("Linux_receiver_before_pidfd",texts["linux_control.py"].index('transport=g.observed_argv(sys.argv[1],nonce)') < texts["linux_control.py"].index('ownfd=os.pidfd_open'))
check("Linux_role_receipt_before_validation",'g.fresh(BASE/"RUN"/receipt_name,transport);g.validate_observed_argv' in texts["linux_control.py"])
check("child_role_receipt_before_validation",'g.fresh(BASE/"RUN/ARGV_CHILD.json",transport);g.validate_observed_argv' in texts["worker.py"])
check("Linux_parent_validates_child",'g.validate_observed_argv(child["argv_transport"],"--child",nonce)' in texts["linux_control.py"])
for role in ["--supervisor","--child","--cleanup"]:
    check("Windows_parent_validates:"+role,any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="validate_observed_argv" and any(isinstance(x,ast.Constant) and x.value==role for x in n.args) for n in ast.walk(trees["launch_windows.py"])))
check("no_extra_process_constructor",sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="Popen" for t in trees.values() for n in ast.walk(t))==2)
check("launch_function_preserved",functions(texts["launch_windows.py"])["launch"]==functions(old_texts["launch_windows.py"])["launch"])
check("capture_class_preserved",functions(texts["launch_windows.py"])["Capture"]==functions(old_texts["launch_windows.py"])["Capture"])
for n in ["gate","stop_child","capture"]:
    check("Linux_unchanged:"+n,functions(texts["linux_control.py"])[n]==functions(old_texts["linux_control.py"])[n])
command=json.loads((BASE/"COMANDO_PROPOSTO_NAO_EXECUTADO.json").read_bytes())
check("command_contract",command["contract"]==pin(BASE/"CONTRATO_WSL.json"))
check("command_identity",command["request_id"]==ident["request_id"])
check("exact_outer_entry",command["argv"]==[r"C:\Python314\python.exe","-I","-S","-B","-X","utf8",str(BASE/"launch_windows.py"),"--run-once"])
check("auth_requires_new_id",contract["future_authorization_schema_not_an_authorization"]["request_id"]==ident["request_id"])
check("no_retry_resume",contract["limits"]["retry"] is False and contract["limits"]["resume"] is False)
r={"created_utc":datetime.now(timezone.utc).isoformat(),"status":"STATIC_PREPARATION_CHECKED_NOT_EXECUTED","request_id":ident["request_id"],"check_count":len(checks),"checks":copy.deepcopy(checks),"candidate_imports":0,"candidate_executions":0,"controls":0,"WSL_invocations":0,"claim_created":False,"authorization_created":False,"scientific_imports":0,"method":"Source/JSON/AST inspection only. Whole old AST after root/identity rebase is restored by deleting only observed-argv receipt additions. No candidate function, path builder or stub is evaluated.","code_pins":[pin(BASE/n) for n in texts]}
p=fresh("RECIBO_ANALISE_ESTATICA.json",r)
print(json.dumps({"receipt":p,"checks":r["check_count"]},indent=2))
