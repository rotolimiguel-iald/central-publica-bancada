"""Independent Q01 review: bytes, hashes, AST and contract metadata only."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import os

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
PKG = ROOT / "f9_precision_qualification_preparation"
OUT = ROOT / "proveniencia/revisao_f9_precision_qualification"
REQUEST = "d8aac6d3-7061-42fb-ae33-6e8b834b3de8"
checks, pins = [], {}

def check(name, ok, detail=None):
    checks.append({"check": name, "passed": bool(ok), "detail": detail})
    if not ok:
        raise AssertionError(name)

def read_pin(path):
    path = Path(path)
    raw = path.read_bytes()
    rec = {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    pins[str(path)] = rec
    return raw, rec

def verify(rec, label):
    _, got = read_pin(rec["path"])
    check(label, all(got[k] == rec[k] for k in ("path", "bytes", "sha256")), got)

def emit(name, obj):
    path = OUT / name
    raw = (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    if path.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        bak = path.with_name(path.name + ".bak_" + stamp)
        old = path.read_bytes()
        with bak.open("xb") as f: f.write(old)
        assert bak.read_bytes() == old
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    os.replace(tmp, path)
    assert path.read_bytes() == raw
    return read_pin(path)[1]

initial = json.loads((OUT / "SNAPSHOT_INICIAL.json").read_bytes())
for i, rec in enumerate(initial["pins"]):
    verify(rec, f"unchanged_initial_{i}")
manifest_bytes, manifest_pin = read_pin(PKG / "MANIFESTO_PREPARACAO.json")
manifest = json.loads(manifest_bytes)
check("manifest_requested_identity", manifest["request_id"] == REQUEST and manifest["unit"] == "Q01")
check("manifest_no_self_member", str(PKG / "MANIFESTO_PREPARACAO.json") not in [r["path"] for r in manifest["members"]])
check("ten_unique_members", len(manifest["members"]) == len({r["path"] for r in manifest["members"]}) == 10)
for i, rec in enumerate(manifest["members"]):
    verify(rec, f"member_{i}")
contract = json.loads((PKG / "CONTROL_CONTRACT.json").read_bytes())
for i, rec in enumerate([contract["candidate"], contract["runtime"]["interpreter"], *contract["sources"]]):
    verify(rec, f"source_or_runtime_{i}")
check("candidate_consistent", contract["candidate"] == manifest["source_candidate"])
check("contract_no_self_pin", str(PKG / "CONTROL_CONTRACT.json") not in [r["path"] for r in contract["sources"]])
check("no_manifest_in_contract_sources", str(PKG / "MANIFESTO_PREPARACAO.json") not in [r["path"] for r in contract["sources"]])
case_ids = ["W01", "W02", "W03", "W04", "W05", "P01", "P02", "N01", "N02"]
check("case_order", [c["id"] for c in contract["cases"]] == contract["case_order"] == case_ids)
check("nine_service_calls_metadata", contract["case_count"] == contract["maximum_service_calls"] == 9)
ceilings = [c["max_evaluations"] if c["expected_evaluations"] is None else c["expected_evaluations"] for c in contract["cases"]]
check("sum_of_accepted_path_ceilings", ceilings == [4098,4097,5,4098,4098,17,17,0,3] and sum(ceilings) == contract["maximum_total_evaluations"] == 16433, ceilings)
trees = {}
for path in [PKG/"driver.py", PKG/"cases.py", Path(contract["candidate"]["path"])]:
    raw, _ = read_pin(path)
    tree = ast.parse(raw, filename=str(path))
    trees[path.name] = tree
    imports = sorted({a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names} | {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module})
    allowed = {"argparse","hashlib","json","marshal","os","pathlib","subprocess","sys","time","types","uuid","math","heapq","fractions"}
    check("stdlib_imports_" + path.name, set(imports) <= allowed, imports)
    check("ast_parsed_" + path.name, True, {"nodes": len(list(ast.walk(tree)))})
driver = (PKG/"driver.py").read_text(encoding="utf-8")
cases = (PKG/"cases.py").read_text(encoding="utf-8")
candidate = Path(contract["candidate"]["path"]).read_text(encoding="utf-8")
check("one_popen_callsite", sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="subprocess" and n.func.attr=="Popen" for n in ast.walk(trees["driver.py"])) == 1)
check("two_service_callsites_disjoint_branches", sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=="candidate" and n.func.attr in {"log_exp_quad_interval","positive_quad_1d"} for n in ast.walk(trees["cases.py"])) == 2)
integrands = [n for n in ast.walk(trees["precision_services.py"]) if isinstance(n,ast.FunctionDef) and n.name=="integrand"]
check("single_pinned_python_integrand", len(integrands)==1 and integrands[0].lineno==252)
check("reference_before_profile", cases.index("reference = window_reference") < cases.index("sys.setprofile(profile)"))
check("profile_filename_and_name", 'frame.f_code.co_filename == source_filename' in cases and 'frame.f_code.co_name == "integrand"' in cases)
check("profile_restored_finally", 'finally:\n                sys.setprofile(None)' in cases)
check("callback_exception_identity", 'captured is sentinel and result is None' in cases)
check("no_candidate_monkeypatch", not any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Attribute) and isinstance(t.value,ast.Name) and t.value.id=="candidate" for t in n.targets) for n in ast.walk(trees["cases.py"])))
check("exact_pinned_compile", 'compile(raw, str(path), "exec", dont_inherit=True, optimize=0)' in driver and 'exec(code, module.__dict__)' in driver)
check("loaded_function_binding", 'fn.__globals__ is candidate.__dict__' in driver and 'fn.__code__.co_filename == str(source)' in driver)
check("preload_stdlib", driver.index("import fractions\n") < driver.index('candidate, candidate_attest = load_bytes'))
check("run_claim_before_popen", driver.index('exclusive_json(ROOT / "RUN_CLAIM.json"') < driver.index('proc = subprocess.Popen'))
check("worker_marker_before_candidate", driver.index('exclusive_json(output / "WORKER_STARTED.json"') < driver.index('candidate, candidate_attest = load_bytes'))
check("exclusive_marker", 'os.O_WRONLY | os.O_CREAT | os.O_EXCL' in driver)
check("fixed_output_and_parent_binding", 'ROOT / "execution_once"' in driver and 'claim["supervisor_pid"] == os.getppid()' in driver)
check("late_pass_guard_after_stdout", driver.index('"TOTAL_DEADLINE_AFTER_STDOUT_FLUSH"') > driver.index('terminal_sha256'))
check("worker_nonzero_required_failure", 'need(proc.returncode == 0' in driver and '"WORKER_FAILURE_RECORD"' in driver)
check("limits_metadata", contract["limits"]["total_nominal_seconds"]==30 and contract["limits"]["worker_cooperative_seconds"]==23 and contract["limits"]["worker_outer_wait_seconds"]==25 and contract["limits"]["maximum_children"]==1)
check("immutable_terminal_no_retry", contract["limits"]["retry"] is False and contract["limits"]["fallback"] is False)
for name in ["ROOT_DECISION.json","RUN_CLAIM.json","CLAIM.json","AUTH.json","AUTHORIZATION.json","execution_once","__pycache__"]:
    check("not_present_"+name, not (PKG/name).exists())
receipt = {
 "schema":"Q01_INDEPENDENT_STATIC_REVIEW_EVIDENCE_V1",
 "reviewer":"chatgpt-codex/ordem-018/proveniencia",
 "request_id":REQUEST,"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "map_before":597,"status":"STATIC_REVIEW_NO_MATERIAL_BLOCKER_IN_PINNED_SCOPE",
 "source_manifest_initial_and_final":manifest_pin,
 "checks_count":len(checks),"checks":checks,"source_pins":list(pins.values()),
 "analytical_review":"Manual algebra and control-flow review in PARECER_Q01.md; not evaluated by this script.",
 "limits":["Pins concern named files, not a complete Python runtime inventory.",
           "16433 sums fixed-source paths/accepted counts; instrumentation is not a universal quota against changed source.",
           "No candidate/reference/driver imports or execution; no numerical or scientific qualification claimed."],
 "candidate_imports":0,"candidate_executions":0,"numeric_reference_evaluations":0,
 "AUTH_created":False,"CLAIM_created":False,"WSL":0,"network":0,"observed_reads":0
}
ev = emit("EVIDENCIA_ESTATICA_Q01.json", receipt)
artifacts = []
for name in ["SNAPSHOT_INICIAL.json","MAPA_ANTES.json","verificar_metadados_q01.py","PARECER_Q01.md","EVIDENCIA_ESTATICA_Q01.json"]:
    artifacts.append(read_pin(OUT/name)[1])
review_manifest = {"schema":"Q01_INDEPENDENT_REVIEW_MANIFEST_V1","request_id":REQUEST,
 "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"STATIC_REVIEW_ONLY_NOT_EXECUTION_AUTHORIZATION",
 "source_manifest":manifest_pin,"checks_count":len(checks),"members":artifacts,
 "map_after":"MAPA_DEPOIS.json saved separately; no cyclic self-hash"}
result = emit("MANIFESTO_REVISAO_Q01.json", review_manifest)
print(json.dumps({"checks_count":len(checks),"all_passed":all(c["passed"] for c in checks),"manifest":result,"report":read_pin(OUT/"PARECER_Q01.md")[1],"source_manifest":manifest_pin}, ensure_ascii=False))
