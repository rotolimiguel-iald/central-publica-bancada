"""Static custody/schema audit. Does not import or run reviewed candidates."""
from pathlib import Path
from collections import Counter
import ast, datetime, hashlib, json, os
ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
OUT = Path(__file__).resolve().parent
PACKAGE = ROOT / "f9_five_model_assembly_preparation"
def meta(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}, raw
def atomic(path, data):
    raw = data.encode("utf-8")
    if path.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        path.with_name(path.name + ".bak_" + stamp).write_bytes(path.read_bytes())
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and raw
    os.replace(temp, path)
    assert path.read_bytes() == raw
checks = []
sources = {}
def check_pin(pin, base=None):
    path = Path(pin["path"]) if base is None else base / pin["path"]
    measured, _ = meta(path)
    sources[str(path)] = measured
    ok = measured["bytes"] == pin["bytes"] and measured["sha256"] == pin["sha256"]
    checks.append({"path": str(path), "expected_bytes": pin["bytes"], "expected_sha256": pin["sha256"], "match": ok})
    return ok
manifest_meta, raw = meta(PACKAGE / "MANIFESTO_ENTREGA.json")
manifest = json.loads(raw)
sources[manifest_meta["path"]] = manifest_meta
for pin in manifest["files"]:
    check_pin(pin, PACKAGE)
f = json.loads((PACKAGE / "FONTES_PINADAS.json").read_bytes())
for pin in [f["request"], *f["direct_sources"], f["additional_documentary_source"], f["layout_manifest"], *f["layout_members"]]:
    check_pin(pin)
module = (PACKAGE / "five_model_assembly.py").read_bytes()
tree = ast.parse(module.decode("utf-8-sig"))
constants = {}
for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                constants[target.id] = ast.literal_eval(node.value)
embedded_equal = constants["SOURCE_PINS"] == f["embedded_sources"]
for pin in constants["SOURCE_PINS"].values():
    check_pin(pin)
imports = sorted({alias.name for node in ast.walk(tree) if isinstance(node,ast.Import) for alias in node.names} |
                 {node.module for node in ast.walk(tree) if isinstance(node,ast.ImportFrom)})
toplevel_calls = [{"line": n.lineno, "kind": type(n).__name__} for n in tree.body
                  if not isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.Import,ast.ImportFrom)) and any(isinstance(x,ast.Call) for x in ast.walk(n))]
d = json.loads((ROOT / "h0dn_documentary_review/linear_design/ESPECIFICACAO_LINEAR.json").read_bytes())
l = json.loads((ROOT / "f9_structural_layout_preparation/LAYOUT_ESTRUTURAL_3CMB_13BAO.json").read_bytes())
rows = d["rows"]
columns = d["eta_columns"]
native_response = Counter((row["family"], row["a_h"], row["c_C"]) for row in rows)
five_rows = [{"row_id": row["row_id"], "family": row["family"], "X": row["X"], "a_h": row["a_h"], "c_C": row["c_C"]} for row in rows if row["family"] in ("SN_HF","SBF_HF","megamaser")]
background_ids = [c["source_path"] + ":L" + str(c["source_line"]) + "#" + c["observable"] for c in l["components"]]
structural = {
 "local_rows": len(rows), "background_rows": len(l["components"]), "total_rows": len(rows)+len(l["components"]),
 "nuisance_columns": len(columns), "nuisance_keys_unique": len({c["key"] for c in columns})==len(columns),
 "nuisance_all_mag": all(c["unit"]=="mag" for c in columns),
 "row_ids_joint_unique": len(set(background_ids + [row["row_id"] for row in rows])) == len(rows)+len(l["components"]),
 "family_counts": dict(Counter(row["family"] for row in rows)),
 "native_response_counts": [{"family": k[0], "a_h": k[1], "c_C": k[2], "count": v} for k,v in native_response.items()],
 "a_h_nonzero_rows": sum(row["a_h"]!="0" for row in rows), "c_C_nonzero_rows": sum(row["c_C"]!="0" for row in rows),
 "five_scaled_rows": five_rows, "scale5_row_count": len(five_rows),
 "background_components": [{k:c[k] for k in ("index_1based","block","observable","redshift_decimal","units")} for c in l["components"]],
 "ordered_unique_BAO_redshift_decimals": l["ordered_unique_BAO_redshift_decimals"],
 "alpha": {k:l["alpha"][k] for k in ("symbol","decimal_token","units","origin","source_line")},
 "rank_recomputed": False, "observed_centres_projected": False,
}
followup_path = ROOT / "F9_ENGINE_ASSEMBLY_INTEGRATION_REQUEST.json"
followup_meta, raw = meta(followup_path)
sources[str(followup_path)] = followup_meta
followup = json.loads(raw)
result = {
 "schema":"F9_FIVE_MODEL_INDEPENDENT_STATIC_REVIEW_RECEIPT_V1",
 "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "reviewer":"chatgpt-codex/ordem-018/proveniencia", "reviewed_request_id":manifest["request_id"],
 "scope":"Read-only candidate/source review, hashes and structural AST/JSON metadata; no candidate import or arithmetic execution",
 "map_before_refs":[542,545], "manifest":manifest_meta, "pin_checks":checks,
 "pin_check_count":len(checks), "all_pins_match":all(c["match"] for c in checks), "unique_files_hashed":len(sources), "unique_files_verified_against_pin":len({c["path"] for c in checks}),
 "sources":list(sources.values()),
 "AST":{"parsed":True,"imports":imports,"top_level_calls":toplevel_calls,"embedded_sources_match":embedded_equal,
        "constant_metadata":{k:constants[k] for k in ("MODELS","THETA_NAMES","BOUNDS","EXTRAS","BACKGROUND_UNITS")},
        "limitation":"Syntax and literal metadata inspection, not execution or proof of runtime dependency closure"},
 "structural_metadata":structural,
 "findings":[{"id":"F9A-I01","classification":"INTEGRATION_OBLIGATION_ALREADY_FORWARDED_NOT_PURE_ADAPTER_BLOCKER",
    "source":"f9_background_prediction/background_controls.py:182-185",
    "finding":"Engine uses index0 as z0 and requires increasing distances. Effective grid must retain zero first plus seven ordered unique BAO redshifts.",
    "adapter_support":"five_model_assembly.py:235-244 accepts extra low_z entries including zero.",
    "forwarded_in_request":followup["request_id"],"forwarded_source":followup_meta,
    "source_instruction":[x for x in followup["deliverables"] if "redshifts" in x],
    "future_execution_authorized_here":False}],
 "assessment":"LIMITED_STATIC_ACCEPTANCE_NO_NEW_BLOCKER_FOUND; integration and runtime remain unqualified",
 "limits":{"candidate_imports":0,"candidate_calls":0,"Fraction_calls":0,"controls_executed":0,"solver_calls":0,
  "observed_data_files_opened":[],"observed_centres_read":False,"scientific_rank_or_covariance_computed":False,
  "remote_or_network_calls":0,"new_execution_request_claim_authorization":False,"candidate_or_shared_memories_modified":False,
  "upstream_origin_pins_only_transcribed_not_reopened":True,"scientific_certificate":False},
}
assert result["all_pins_match"] and embedded_equal
atomic(OUT/"RECIBO_REVISAO_ESTATICA.json",json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ("all_pins_match","pin_check_count","unique_files_hashed","unique_files_verified_against_pin","assessment")},ensure_ascii=False))
print(json.dumps({"receipt":meta(OUT/"RECIBO_REVISAO_ESTATICA.json")[0],"structural_metadata":structural,"AST":result["AST"]},ensure_ascii=False))
