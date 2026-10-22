"""Independent I03 audit: bytes, JSON identifiers and AST only; no candidate import."""
from pathlib import Path
import ast
import hashlib
import json
import os
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
PACKAGE = ROOT / "f9_joint_covariance_preparation"
OUT = ROOT / "derivacoes/revisao_f9_joint_covariance"

def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def load(path):
    return json.loads(path.read_bytes())

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")

def write_new(path, value):
    assert not path.exists(), str(path)
    data = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == data
    os.replace(temp, path)
    assert path.read_bytes() == data

identity = load(OUT / "IDENTIDADE_REVISAO.json")
manifest_initial = pin(PACKAGE / "MANIFESTO_PREPARACAO.json")
manifest = load(PACKAGE / "MANIFESTO_PREPARACAO.json")
checks = []
def check(name, passed, detail=None):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})

check("manifest matches task pin",
      manifest_initial["bytes"] == 4236 and manifest_initial["sha256"] ==
      "2e331bc91b2c727498363738b1da27ba25b4094dbad7bd88ffd63e48e3493cdc")
members = []
for item in manifest["members"]:
    actual = pin(Path(item["path"]))
    ok = all(actual[k] == item[k] for k in ("bytes", "sha256"))
    check("member: " + item["name"], ok)
    members.append({"expected": item, "actual": actual, "matches": ok})
sources = load(PACKAGE / "FONTES_PINADAS.json")
source_results = []
for name, item in sources.items():
    actual = pin(Path(item["path"]))
    ok = all(actual[k] == item[k] for k in ("bytes", "sha256"))
    check("source: " + name, ok)
    source_results.append({"name": name, "expected": item, "actual": actual, "matches": ok})
check("source/member declared counts", len(members) == manifest["member_count"] == 10 and
      len(sources) == manifest["source_count"] == 22)

metadata = load(PACKAGE / "METADATA_ESTRUTURA_FAMILIA.json")
structure = load(ROOT / "f9_likelihood_consumer_preparation/IDENTIDADE_ESTRUTURAL_METADATA.json")
linear = load(ROOT / "h0dn_documentary_review/linear_design/ESPECIFICACAO_LINEAR.json")
psd = load(ROOT / "h0dn_documentary_review/jagb_extension/residual_systematics/CONTRATO_PSD_CANDIDATO.json")
errors = load(ROOT / "h0dn_documentary_review/jagb_extension/residual_systematics/ERROR_COMPONENTS.json")
preflight = load(ROOT / "derivacoes/preflight_262/PROTOCOLO_PREFLIGHT_262.json")
resolver = load(ROOT / "f9_consolidated_draft/RESOLUTOR_F9.json")
mm = load(ROOT / "f9_mm_model_preparation/CONTRATO_MM_CANDIDATO.json")

check("projection exactly equals consumer metadata", metadata["projection"] == structure["projection"])
check("projection hashes regenerated from metadata", all(
    hashlib.sha256(canonical(value)).hexdigest() == metadata["projection_canonical_sha256"][key]
    for key, value in metadata["projection"].items()))
check("native local design exactly source", metadata["local_design"] == linear["rows"])
check("stellar graph exactly source", metadata["stellar_graph"] == linear["mas_hms_graph"])
check("eta columns exactly source", metadata["projection"]["eta_columns"] == linear["eta_columns"])
check("correlation groups exactly source", metadata["groups"] == psd["groups"])
expected_keys = {
    "anchor": [x["anchor"] for x in errors["anchor_errors"]],
    "MAS": [x["mas_key"] for x in errors["mas_reference_errors"]],
    "HMS": [x["key"] for x in errors["primitive_hms_groups"]],
}
check("primitive key orders match pinned errors metadata", metadata["primitive_keys"] == expected_keys)
check("all stellar incidences refer to admitted keys", all(
    row[kind] in expected_keys[kind] for row in metadata["stellar_graph"] for kind in ("anchor", "MAS", "HMS")))
row_hms = {rid: x["key"] for x in errors["primitive_hms_groups"] for rid in x["row_ids"]}
check("HMS row identity matches error metadata", all(row["HMS"] == row_hms[row["row_id"]]
      for row in metadata["stellar_graph"]))
check("graph row order equals first178 local rows",
      [x["row_id"] for x in metadata["stellar_graph"]] == [x["row_id"] for x in linear["rows"][:178]])

blocks = metadata["blocks"]
block_names = [x["name"] for x in blocks]
expected_names = ["PLANCK","DESI","STELLAR","GROUP","SN_CAL","SBF_CAL","SN_HF","SBF_HF","MM"]
check("nine block names and sizes", block_names == expected_names and
      [len(x["row_ids"]) for x in blocks] == [3,13,178,13,55,14,1,1,5])
flattened = [rid for b in blocks for rid in b["row_ids"]]
check("block flattening equals consumer row order", flattened == metadata["projection"]["row_ids"])
check("no repeated row identities", len(flattened) == len(set(flattened)) == 283)
cursor = 0
slices_ok = True
for b in blocks:
    slices_ok = slices_ok and b["start"] == cursor and b["stop"] == cursor + len(b["row_ids"])
    cursor = b["stop"]
check("contiguous exact block slices", slices_ok and cursor == 283)
check("row scale exactly 276ones then7fives",
      metadata["projection"]["native_to_output_row_scale"] == [1]*276 + [5]*7)
check("local267 and eta63", len(linear["rows"]) == 267 and len(linear["eta_columns"]) == 63)
check("five MM IDs match source order", blocks[-1]["row_ids"] == [x["row_id"] for x in mm["rows"]])
check("metadata source pins equal source manifest", metadata["source_pins"] == sources)

expected_family = []
for si, sign in enumerate(psd["candidate_grid"]["sign_scenarios"]):
    for ti, fractions in enumerate(psd["candidate_grid"]["fraction_tuples_order_u_v_p_q"]):
        for vi, variant in enumerate(preflight["variants"]):
            expected_family.append({
                "label": f"STELLAR_{si}_{ti:03d}__" + variant["id"],
                "stellar_index": si*len(psd["candidate_grid"]["fraction_tuples_order_u_v_p_q"])+ti,
                "sign_scenario": sign["id"], "fraction_strings": fractions,
                "sbf_id": variant["id"], "sbf_sigma_field": variant["flow_sigma_field"],
                "resolver_sbf_label": resolver["resolved_contract"]["systematics"]["SBF_labels"][vi]})
check("600 complete labels exact source product/order/mapping", metadata["family_labels"] == expected_family and len(expected_family) == 600)
check("600 distinct labels and300stellar indices", len({x["label"] for x in expected_family}) == 600
      and len({x["stellar_index"] for x in expected_family}) == 300)

ast_receipts = []
for rel in ["f9_joint_covariance_preparation/joint_covariance.py",
            "f9_likelihood_consumer_preparation/likelihood_consumer.py",
            "covariance_support/qualify_stellar_family.py",
            "covariance_support/qualify_flow_errors.py",
            "covariance_support/linear_gaussian.py",
            "covariance_support/singular_gaussian_v2.py"]:
    path = ROOT / rel
    tree = ast.parse(path.read_bytes(), filename=str(path))
    ast_receipts.append({"source": pin(path), "parsed_only": True, "top_level_node_count": len(tree.body)})
tree = ast.parse((PACKAGE / "joint_covariance.py").read_bytes())
imports = [n.module if isinstance(n, ast.ImportFrom) else a.name
           for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
           for a in (n.names if isinstance(n, ast.Import) else [None])]
check("candidate imports only stdlib declared modules", imports == ["hashlib","json","math","fractions"])
assignments = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
check("candidate metadata byte binding", assignments["METADATA_SHA256"] == pin(PACKAGE/"METADATA_ESTRUTURA_FAMILIA.json")["sha256"])
check("candidate exact block order", list(assignments["BLOCKS"]) == expected_names)
check("candidate six common blocks", list(assignments["COMMON"]) == ["PLANCK","DESI","GROUP","SN_CAL","SBF_CAL","SN_HF"])
check("candidate request binding", assignments["REQUEST_ID"] == manifest["request_id"] == identity["request_id"])
check("all36 unordered cross pairs defined by9block metadata",
      len([a+"|"+b for i,a in enumerate(assignments["BLOCKS"]) for b in assignments["BLOCKS"][i+1:]]) == 36)
manifest_final = pin(PACKAGE / "MANIFESTO_PREPARACAO.json")
check("manifest unchanged during documentary audit", manifest_initial == manifest_final)
receipt = {
 "schema": "I03_INDEPENDENT_DOCUMENTARY_AUDIT_V1",
 "review_id": identity["review_id"], "request_id": identity["request_id"],
 "at_utc": datetime.now(timezone.utc).isoformat(),
 "scope": "BYTES_JSON_IDENTIFIERS_AST_ONLY_NO_CANDIDATE_OR_MATRIX_EXECUTION",
 "reviewer": "chatgpt-codex/ordem-018/derivacoes",
 "identity_pin": pin(OUT/"IDENTIDADE_REVISAO.json"),
 "audit_script_pin": pin(Path(__file__)),
 "manifest_initial": manifest_initial, "manifest_final": manifest_final,
 "member_pin_comparisons": members, "source_pin_comparisons": source_results,
 "checks": checks, "check_count": len(checks),
 "passed": sum(x["passed"] for x in checks), "failed": [x["name"] for x in checks if not x["passed"]],
 "AST_only": ast_receipts,
 "candidate_imports": 0, "candidate_calls": 0, "matrix_operations": 0,
 "numpy_scipy_imports": 0, "controls_executed": 0, "observed_centres_read": False,
 "WSL_solver_remote_calls": 0, "AUTH_CLAIM_created": False,
 "physical_ratification": False, "new_scientific_results": None,
 "map_before_seq": 601,
 "note": "Checks are documentary consistency checks, not numerical qualification or proof of physical covariance."
}
write_new(OUT/"RECIBO_AUDITORIA_DOCUMENTAL.json", receipt)
print(json.dumps({"checks":len(checks),"passed":receipt["passed"],"failed":receipt["failed"],
                 "receipt":pin(OUT/"RECIBO_AUDITORIA_DOCUMENTAL.json")}))
