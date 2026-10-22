"""Independent stdlib-only review; no scientific module imports or execution."""
from pathlib import Path
from collections import Counter
import ast
import datetime
import hashlib
import json
import math
import sys
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
TARGET = ROOT / "derivacoes/preflight_262"
CHECKS, READS = [], {}
START, CPU = time.perf_counter(), time.process_time()

def read(path):
    path = Path(path)
    data = path.read_bytes()
    READS[str(path)] = {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    return data

def obj(path):
    return json.loads(read(path))

def check(name, condition):
    CHECKS.append({"name": name, "passed": bool(condition)})

def tree(path):
    return ast.parse(read(path).decode("utf-8-sig"))

def dump(node):
    return ast.dump(node, include_attributes=False)

def statement(parsed, text):
    expected = dump(ast.parse(text).body[0])
    return any(dump(n) == expected for n in ast.walk(parsed) if isinstance(n, ast.stmt))

def atomic_new(path, value):
    assert not path.exists(), "Preserve existing review receipt"
    data = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(data)
    assert temp.read_bytes() == data
    temp.replace(path)
    assert path.read_bytes() == data

manifest = obj(TARGET / "MANIFESTO_PREFLIGHT_262.json")
proto = obj(TARGET / "PROTOCOLO_PREFLIGHT_262.json")
claim = obj(TARGET / "CLAIM.json")
result = obj(TARGET / "PREFLIGHT_262_RESULT.json")
launch = obj(TARGET / "PREFLIGHT_262_LAUNCH.json")
own_audit = obj(TARGET / "AUDITORIA_PREFLIGHT_262.json")
note = read(TARGET / "NOTA_PREFLIGHT_262.md").decode("utf-8")
for group, entries in [("manifest", manifest["files"]), ("protocol", proto["inputs"])]:
    for entry in entries:
        read(entry["path"])
        check(group + "_pin:" + Path(entry["path"]).name, READS[entry["path"]] == entry)
src = {Path(e["path"]).name: Path(e["path"]) for e in proto["inputs"]}
check("protocol_claim_result_identity", proto["id"] == claim["id"] == result["id"])
check("claim_protocol_pin", claim["protocol_sha256"] == READS[str(TARGET / "PROTOCOLO_PREFLIGHT_262.json")]["sha256"])
check("result_protocol_pin", result["protocol"] == READS[str(TARGET / "PROTOCOLO_PREFLIGHT_262.json")])
check("result_inputs", result["inputs"] == proto["inputs"])
check("protocol_predates_claim", datetime.datetime.fromisoformat(proto["created_utc"]) < datetime.datetime.fromisoformat(claim["claimed_utc"]))
check("launch_success", launch["status"] == "COMPLETED" and launch["returncode"] == 0 and launch["stderr"] == "")
stdout = json.loads(launch["stdout"])
check("launch_stdout_matches_result", stdout == {k: result[k] for k in stdout})
check("wall_budget", 0 < result["wall_seconds"] <= launch["wall_seconds"] < proto["max_wall_seconds"] == launch["hard_timeout_seconds"] == 120)
check("single_execution_frozen", proto["max_execution_count"] == 1)
check("thread_env", result["runtime"]["thread_environment"] == {k: "1" for k in proto["threads_env"]})
check("own_audit_consistent", own_audit["n_checks"] == len(own_audit["checks"]) == 27 and all(c["passed"] for c in own_audit["checks"]) and own_audit["second_numerical_execution"] is False)
check("no_failure_receipt", not (TARGET / "PREFLIGHT_262_FAILURE.json").exists())

spec = obj(src["ESPECIFICACAO_LINEAR.json"])
meta = obj(src["METADADOS_ERROS_NAO_ESTELARES_V01.json"])
errors = obj(src["ERROR_COMPONENTS.json"])
flow = obj(src["FLOW_ERROR_RESULT.json"])
check("flow_protocol_pin", flow["protocol_sha256"] == READS[str(src["FLOW_ERROR_PROTOCOL.json"])]["sha256"])
for owner, value in [("flow", obj(src["FLOW_ERROR_PROTOCOL.json"])), ("stellar", obj(src["STELLAR_FAMILY_PROTOCOL.json"]))]:
    for entry in value["inputs"]:
        name = Path(entry["path"]).name
        if name in src:
            actual = READS[str(src[name])]
            check(owner + "_shared_pin:" + name, actual["bytes"] == entry["bytes"] and actual["sha256"] == entry["sha256"])
rows, excluded = spec["rows"][:262], spec["rows"][262:]
check("counts_262_267_5", len(rows) == result["row_count"] == 262 and len(spec["rows"]) == result["full_V01_row_count"] == 267 and len(excluded) == 5)
check("unique_row_identity", len({r["row_id"] for r in spec["rows"]}) == 267)
check("excluded_all_and_only_MM", all(r["family"] == "megamaser" for r in excluded) and not any(r["family"] == "megamaser" for r in rows))
check("excluded_ids_match", [r["row_id"] for r in excluded] == result["excluded_row_ids"] == ["data/megamaser.dat:L" + str(n) for n in range(5, 10)])
check("centres_absent", all(v is None for v in spec["values"].values()))
families = dict(Counter(r["family"] for r in rows))
check("row_family_counts", families == {"host": 178, "group": 13, "SN_calibrator": 55, "SBF_calibrator": 14, "SN_HF": 1, "SBF_HF": 1})
check("eta_63_unique", len(spec["eta_columns"]) == len({e["key"] for e in spec["eta_columns"]}) == 63)
host_ids = [r["row_id"] for r in rows if r["family"] == "host"]
check("host_prefix", host_ids == [r["row_id"] for r in rows[:178]])
graph = {g["row_id"]: g for g in spec["mas_hms_graph"]}
primitive = {rid: g["key"] for g in errors["primitive_hms_groups"] for rid in g["row_ids"]}
check("host_graph_primitive_identity", set(host_ids) == set(graph) == set(primitive))
check("host_graph_HMS_keys", all(graph[rid]["HMS"] == primitive[rid] for rid in host_ids))
check("host_graph_anchor_keys", all(graph[rid]["MAS"].split("&")[1] == graph[rid]["anchor"] for rid in host_ids))
nonstellar = [r for key in ["SN_calibrators", "SBF_calibrators", "group_equations"] for r in meta[key]]
check("nonstellar_82_unique", len(nonstellar) == len({r["row_id"] for r in nonstellar}) == 82)
check("nonstellar_ids_match", {r["row_id"] for r in nonstellar} == {r["row_id"] for r in rows if r["family"] in {"group", "SN_calibrator", "SBF_calibrator"}})
check("nonstellar_positive_errors", all(math.isfinite(float(r["variance_mag2_upstream"])) and float(r["variance_mag2_upstream"]) > 0 for r in nonstellar))
flows = [r for r in rows if r["family"] in {"SN_HF", "SBF_HF"}]
check("transport_row_ids", [r["row_id"] for r in flows] == result["transformed_rows"])
check("flow_coefficients", all(list(r["X"].values()) == ["-1/5"] and r["a_h"] == "1" and r["c_C"] == "0" for r in flows))

worker = tree(TARGET / "preflight_262.py")
launcher = tree(TARGET / "launch_preflight_262.py")
baseline = tree(TARGET / "baseline_stellar.py")
original = tree(src["qualify_stellar_family.py"])
helper_fn = next(n for n in baseline.body if isinstance(n, ast.FunctionDef))
original_fn = next(n for n in original.body if isinstance(n, ast.FunctionDef) and n.name == "main")
start, end = proto["baseline_extraction"]["start_line"], proto["baseline_extraction"]["end_line"]
selected = [n for n in original_fn.body if start <= n.lineno and n.end_lineno <= end]
check("baseline_exact_AST_extraction", [dump(n) for n in selected] == [dump(n) for n in helper_fn.body[:-1]] and len(selected) == 15)
check("baseline_returns_only_baseline", dump(helper_fn.body[-1]) == dump(ast.parse("return baseline").body[0]))
statements = {
    "subset_prefix": "rows=spec['rows'][:262]",
    "transport_init": "scale=np.ones(262)",
    "transport_exact_families": "if r['family'] in ('SN_HF','SBF_HF'): scale[i]=5.",
    "transport_two_rows": "assert np.count_nonzero(scale==5)==2",
    "transport_X": "Xt=scale[:,None]*X",
    "transport_A": "At=scale[:,None]*A",
    "transport_C": "Ct=scale[:,None]*C*scale[None,:]",
    "baseline_block": "common[:178,:178]=baseline",
    "common_zero_offblock": "common=np.zeros((262,262))",
    "nonstellar_diagonal": "if r['row_id'] in variances: common[i,i]=variances[r['row_id']]\nelif r['family']=='SN_HF': common[i,i]=flow['SN']['variance_alpha_conditional_upstream']\nelse: assert r['family']=='SBF_HF'",
    "SBF_error_square": "C[sbfi,sbfi]=sigma*sigma",
    "same_CX_module": "model=FlatNuisanceGaussian(Ct,Xt,**proto['module_tolerances'])",
    "information_only": "I=model.response_information(At)",
    "joint_covariance": "cov=np.linalg.solve(I,np.eye(2))",
    "joint_sigmas": "errors_ideal=np.sqrt(np.diag(cov))",
}
for label, text in statements.items():
    check("AST:" + label, statement(worker, text))
calls = [ast.unparse(n.func) for n in ast.walk(worker) if isinstance(n, ast.Call)]
check("no_log_integral_evaluate_calls", not any(c.endswith((".log_integral", ".evaluate")) for c in calls))
check("no_original_main_call", not any("qualify_stellar_family" in c for c in calls))
check("one_subprocess_call_in_launcher", sum(isinstance(n, ast.Call) and ast.unparse(n.func) == "subprocess.run" for n in ast.walk(launcher)) == 1)
check("launcher_refuses_terminal_or_claim", "Existing or uncertain unit" in ast.unparse(launcher) and all(n in ast.unparse(launcher) for n in ["CLAIM.json", "PREFLIGHT_262_RESULT.json", "PREFLIGHT_262_FAILURE.json", "PREFLIGHT_262_LAUNCH.json"]))
check("launcher_timeout_frozen", "timeout=protocol['max_wall_seconds']" in ast.unparse(launcher))
flat = tree(src["linear_gaussian.py"])
for label, text in {
    "flat_whitener": "self.whitener=(self.support.positive_vectors/np.sqrt(self.support.positive_eigenvalues)).T",
    "flat_design_SVD": "u,s,_=np.linalg.svd(xw,full_matrices=False)",
    "flat_projection": "return aw-self.q@(self.q.T@aw)",
    "flat_response_support": "self._check_supported_columns(a)",
    "flat_design_support": "self._check_supported_columns(x)",
    "flat_information": "result=t.T@t",
}.items():
    check("AST:" + label, statement(flat, text))
check("recorded_exact_ranks_not_recomputed", result["exact_coefficient_ranks_without_MM"] == {"X": 63, "X_a_h": 64, "X_a_h_c_C": 65})
check("variants_match_protocol", [v["id"] for v in result["variants"]] == [v["id"] for v in proto["variants"]])
for v, p in zip(result["variants"], proto["variants"]):
    label = v["id"]
    check(label + ":flow_sigma_matches", v["SBF_sigma_alpha_used"] == flow["SBF"][p["flow_sigma_field"]])
    check(label + ":recorded_support", v["covariance_rank"] == 190 and v["nullity"] == 72 and v["X_rank_whitened"] == 63 and max(v["support_null_column_norms"].values()) <= proto["module_tolerances"]["support_tolerance"])
    check(label + ":recorded_positive_information", v["information_eigenvalues_in_stated_parameter_coordinates"][0] > 0)
    check(label + ":conditional_labels", v["conditional"] is True and v["data_residual_supplied"] is False and v["information_parameter_order"] == ["h_log10", "delta_C_mag"])
    check(label + ":joint_separate_fixed", all(k in v for k in ["ideal_joint_sigma_h_dex", "ideal_joint_sigma_delta_C_mag", "ideal_joint_covariance_2x2", "ideal_sigma_other_response_fixed"]))
check("no_verdict_or_power", result["no_centres_y_S_g_fit_H0_lnB"] is True and result["scientific_verdict"] is None and result["global_power_or_detection"] is None)
check("assumptions_preserved", result["conditional_assumptions"] == proto["conditional_assumptions"])
check("note_distinguishes_joint_errors", "sqrt(diag(I⁻¹))" in note and "outra resposta fixa" in note)
check("note_conditional_independence", "INPUT upstream" in note and "não são afirmações de independência física medida" in note)
check("note_not_observed_H0", "Não são posterior ajustada nem erro de H0 observado" in note)
check("note_C_hash_not_independent_validation", "não uma validação independente" in note)
check("no_scientific_import_in_review", not any(k in sys.modules for k in ["numpy", "scipy", "preflight_262", "linear_gaussian", "singular_gaussian_v2", "baseline_stellar"]))
read(Path(__file__))
receipt = {
    "identity": "chatgpt-codex/ordem-018/preregistros",
    "scope": "Independent static/hash/structural review only; no numerical rerun",
    "review_correction": "V1 reviewer check expected numeric JSON values; all 82 upstream variances are decimal strings. V2 validates the explicit finite positive float conversion used by the worker. Original failed receipt retained; no scientific change or execution.",
    "previous_receipt_sha256": hashlib.sha256((OUT / "RECIBO_REVISAO_PREFLIGHT_262.json").read_bytes()).hexdigest(),
    "reviewed_map_sequences": [458, 459],
    "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS_STATIC_SCOPED_REVIEW" if all(c["passed"] for c in CHECKS) else "STATIC_REVIEW_CHECK_FAILED",
    "n_checks": len(CHECKS), "passed_checks": sum(c["passed"] for c in CHECKS),
    "checks": CHECKS, "read_artifacts": list(READS.values()), "row_family_counts": families,
    "limits": ["No reconstruction/rank/eigenvalues/inverse of C or information", "Matrix hashes preserved as recorded, not independently regenerated", "No numerical proof of upstream physical covariance", "No centers/y/b, fitted H0, S/g, lnB, D or network", "No source or old package mutation"],
    "scientific_numerical_executions": 0, "remote_calls": 0,
    "wall_seconds": time.perf_counter() - START, "cpu_seconds": time.process_time() - CPU,
}
atomic_new(OUT / "RECIBO_REVISAO_PREFLIGHT_262_V2.json", receipt)
print(json.dumps({"status": receipt["status"], "checks": len(CHECKS), "passed": receipt["passed_checks"], "failed": [c for c in CHECKS if not c["passed"]], "files_read": len(READS)}, ensure_ascii=False))
raise SystemExit(0 if receipt["passed_checks"] == len(CHECKS) else 1)
