"""Independent documentary/AST/pin audit; no candidate imports or numerical tests."""
from pathlib import Path
import ast
import json
import hashlib
import os
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SUBJECT=ROOT/"f9_theta_integration_preparation"
def readj(p): return json.loads(p.read_text(encoding="utf-8"))
def pin(p):
    b=p.read_bytes()
    return {"path":str(p.resolve()),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def create(name,obj):
    p=HERE/name
    if p.exists(): raise RuntimeError("REVIEW_OUTPUT_EXISTS:"+name)
    b=obj if isinstance(obj,bytes) else obj.encode("utf-8") if isinstance(obj,str) else (json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    tmp=HERE/(name+".tmp")
    with tmp.open("xb") as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    if tmp.read_bytes()!=b: raise RuntimeError("TEMP_MISMATCH")
    os.replace(tmp,p)
    if p.read_bytes()!=b: raise RuntimeError("FINAL_MISMATCH")
    return pin(p)
def literals(tree):
    result={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            result[node.targets[0].id]=ast.literal_eval(node.value)
    return result
input_data=readj(HERE/"REVIEW_INPUT.json")
manifest_path=SUBJECT/"MANIFESTO_PREPARACAO.json"
manifest_bytes=manifest_path.read_bytes()
manifest_pin=pin(manifest_path)
manifest=json.loads(manifest_bytes)
pin_comparisons=[]
all_paths={}
def verify(expected,context):
    p=Path(expected["path"]).resolve()
    if not p.is_relative_to(ROOT): raise RuntimeError("OUT_OF_REVIEW_SOURCE_SCOPE:"+str(p))
    actual=pin(p)
    ok=actual["bytes"]==expected["bytes"] and actual["sha256"]==expected["sha256"]
    pin_comparisons.append({"context":context,"declared":expected,"actual":actual,"passed":ok})
    if not ok: raise RuntimeError("PIN_MISMATCH:"+str(p))
    all_paths[str(p)]=actual
for item in manifest["artifacts"]:
    if (SUBJECT/item["relative"]).resolve()!=Path(item["path"]).resolve():
        raise RuntimeError("MANIFEST_RELATIVE_IDENTITY")
    verify(item,"subject_manifest")
sources=readj(SUBJECT/"PIN_FONTES.json")["sources"]
for key,item in sources.items(): verify(item,"subject_source:"+key)
source_text=(SUBJECT/"theta_integrator.py").read_text(encoding="utf-8")
tree=ast.parse(source_text)
const=literals(tree)
for key,item in const["SOURCE_PINS"].items(): verify(item,"source_literal:"+key)
for key,item in const["PRIOR_SOURCE_PINS"].items(): verify(item,"conditional_source_literal:"+key)
upstream_source=ROOT/"f9_physical_prior_preparation/physical_prior.py"
prior_const=literals(ast.parse(upstream_source.read_text(encoding="utf-8")))
checks=[]
def check(label,ok):
    checks.append({"id":label,"passed":bool(ok),"scope":"AST_OR_METADATA_ONLY"})
    if not ok: raise RuntimeError("STATIC_CHECK_FAILED:"+label)
check("request_manifest",manifest["request_id"]==input_data["subject_request_id"])
check("request_source",const["REQUEST_ID"]==manifest["request_id"])
check("conditional_request",const["PRIOR_REQUEST_ID"]==prior_const["REQUEST_ID"])
check("exact_conditional_lineage",const["PRIOR_SOURCE_PINS"]==prior_const["SOURCE_PINS"])
check("five_model_ids_match",const["MODELS"]==prior_const["MODELS"])
check("three_theta_names",const["THETA_NAMES"]==("H0","ombh2","omch2"))
check("original_bounds_literals",const["BOUNDS"]==((50.0,90.0),(0.015,0.030),(0.08,0.18)))
check("levels_schema_cap",const["MAX_LEVEL"]==6)
check("callback_schema_cap",const["MAX_CALLBACKS"]==300000)
imports=[]
for node in ast.walk(tree):
    if isinstance(node,ast.Import): imports.extend(a.name for a in node.names)
    elif isinstance(node,ast.ImportFrom): imports.append(node.module)
check("stdlib_imports_only",set(imports)=={"hashlib","itertools","json","math"})
check("no_top_level_executable_calls",not any(isinstance(n,(ast.Expr,ast.Assign,ast.AnnAssign)) and any(isinstance(x,ast.Call) for x in ast.walk(n)) for n in tree.body))
functions={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
check("public_entry_present","ThetaIntegrator" in functions)
check("canonical_encoder_present","canonical_conditional_sha256" in functions)
contract=readj(SUBJECT/"CONTRATO_API.json")
check("contract_request",contract["request_id"]==manifest["request_id"])
check("contract_no_execution",contract["execution_authorization"] is False and contract["claim"] is False)
check("contract_positive_rule",contract["algorithm"]["positive_weights"] is True)
check("contract_prior",contract["prior"]["density_exact"]=="50/3" and contract["prior"]["box_jacobian_exact"]=="3/50")
check("contract_no_uniform_convergence",contract["output"]["global_convergence"] is None and contract["output"]["unresolved_peak_mass_bound"] is None)
check("contract_no_observed_verdict",all(contract["output"][k] is None for k in ("absolute_evidence","p","sigma","verdict")))
check("no_campaign_created",contract["global_configuration"]["campaign_generated"] is False and contract["global_configuration"]["configuration_generated"] is False)
static=readj(SUBJECT/"RECIBO_ESTATICO.json")
check("subject_claims_static_only",static["candidate_imports"]==0 and static["callbacks"]==0 and static["scientific_controls"]==0 and static["observed_reads"]==0)
extras=[
"preregistros/f9_completion_dependencies/QUADRO_DEPENDENCIAS_F9.json",
"preregistros/f9_completion_dependencies/QUADRO_F9_ATE_V1.md",
"preregistros/f9_completion_dependencies/MANIFESTO_ENTREGA.json",
"f9_likelihood_consumer_preparation/API_CONTRATO.md",
"derivacoes/revisao_f9_physical_prior/PARECER_PRIORS_FISICOS_F9.md"
]
for rel in extras: all_paths[str((ROOT/rel).resolve())]=pin(ROOT/rel)
all_paths[str(manifest_path.resolve())]=manifest_pin
# The review creates only its own documentation after checking every declared pin.
create("MANIFESTO_ORIGEM_SNAPSHOT.json",manifest_bytes)
create("MAPA_ANTES.json",input_data["map_before"])
create("PARECER_INTEGRADOR_THETA.md",input_data["note"])
findings={"status":"NO_MATERIAL_BLOCKER_FOUND_WITHIN_TRUSTED_CALLBACK_SCOPE",
          "blocking_findings":[],
          "nonblocking_notes":[{"id":"TH-DOC-01","path":str(SUBJECT/"DERIVACAO.md"),"line":3,
             "issue":"J_i denotes a positive integral; callback transports log J_i. Wording says log-callback while equation is J.",
             "impact":"Following equations and implementation are coherent. No numerical change or rerun requested."}],
          "engineering_not_certification":True,"execution_authorized":False}
create("ACHADOS_ESTATICOS.json",findings)
create("PIN_FONTES_REVISAO.json",{"scope":"Source/docs/AST only, no raw data or candidate execution","paths":list(all_paths.values())})
for item in all_paths.values():
    if pin(Path(item["path"]))!=item: raise RuntimeError("SOURCE_CHANGED_DURING_REVIEW")
check("manifest_unchanged",manifest_path.read_bytes()==manifest_bytes)
now=datetime.now(timezone.utc).isoformat()
receipt={"schema":"F9_THETA_INDEPENDENT_STATIC_REVIEW","at":now,
    "subject_request_id":manifest["request_id"],"map_before":580,"status":findings["status"],
    "manifest_start":manifest_pin,"manifest_end":pin(manifest_path),
    "subject_artifacts_checked":len(manifest["artifacts"]),"declared_source_entries":len(sources),
    "pin_comparisons":pin_comparisons,"pin_comparison_count":len(pin_comparisons),
    "unique_paths_read_and_hashed":len(all_paths),"metadata_AST_checks":checks,
    "metadata_AST_checks_count":len(checks),"manual_static_judgments":input_data["judgments"],
    "manual_static_judgment_count":len(input_data["judgments"]),
    "candidate_imports":0,"numerical_controls":0,"callbacks":0,"scientific_execution":False,
    "solver_calls":0,"observed_data_read":False,"network":False,"WSL":False,"new_AUTH_or_CLAIM":False,
    "upstream_modified":False,"shared_memory_or_ledger_modified":False,
    "scope":"Custody, AST and source reasoning only. No module imported, rule evaluated, theta generated, callback, integral or solver executed."}
create("RECIBO_REVISAO_ESTATICA.json",receipt)
members={p.name:pin(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.suffix!=".tmp"}
review_manifest={"schema":"F9_THETA_REVIEW_MANIFEST","at":now,"subject_request_id":manifest["request_id"],
    "status":findings["status"],"members":members,"subject_manifest_pin":manifest_pin,
    "zero_execution":True,"map_after_separate_supplement":True}
out=create("MANIFESTO_REVISAO.json",review_manifest)
for item in members.values():
    if pin(Path(item["path"]))!=item: raise RuntimeError("REVIEW_MEMBER_CHANGED")
print(json.dumps({"manifest":out,"review_note":pin(HERE/"PARECER_INTEGRADOR_THETA.md"),
    "members":len(members),"artifacts_checked":len(manifest["artifacts"]),
    "source_entries":len(sources),"pin_comparisons":len(pin_comparisons),
    "unique_paths":len(all_paths),"AST_metadata_checks":len(checks),
    "static_judgments":len(input_data["judgments"]),"blocking_findings":0},ensure_ascii=False))
