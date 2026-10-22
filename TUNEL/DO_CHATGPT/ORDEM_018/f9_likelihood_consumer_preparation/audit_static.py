"""Own static custodian only. Never import candidate/numpy/solver or run controls."""
from pathlib import Path
import ast
import collections
import datetime
import hashlib
import json
import os
import time

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
OUT = ROOT / "f9_likelihood_consumer_preparation"
START = time.perf_counter()
CHECKS = []
PINS = []
def check(name, ok, detail=None):
    CHECKS.append({"name": name, "passed": bool(ok), "detail": detail})
    if not ok:
        raise RuntimeError("STATIC_CHECK_FAILED: " + name)
def pin(path):
    b = path.read_bytes()
    p = {"path": str(path), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    PINS.append(p)
    return b, p
def canonical(doc):
    return json.dumps(doc, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
def create(name, value):
    path = OUT / name
    check("new receipt path " + name, not path.exists())
    b = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert temporary.read_bytes() == b
    os.replace(temporary, path)
    assert path.read_bytes() == b

raw, code_pin = pin(OUT / "likelihood_consumer.py")
tree = ast.parse(raw)
check("candidate parses as AST only", isinstance(tree, ast.Module))
constants = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ("REQUEST_ID", "SOURCE_PINS", "ASSEMBLY_SOURCE_PINS",
                                 "STRUCTURAL_IDENTITY_PINS", "MODELS"):
            constants[node.targets[0].id] = ast.literal_eval(node.value)
check("persistent request", constants["REQUEST_ID"] == "a9874f79-9d71-48f5-824c-d51d6d819534")
source_doc = json.loads(pin(OUT / "PIN_FONTES.json")[0])
for group in ("sources", "assembly_declared_sources_verified"):
    for key, expected in source_doc[group].items():
        _, actual = pin(Path(expected["path"]))
        check("current source bytes " + group + ":" + key, actual == expected)
for key, expected in constants["SOURCE_PINS"].items():
    check("code embeds current pin " + key, expected == source_doc["sources"][key])
check("assembly source pin mapping", constants["ASSEMBLY_SOURCE_PINS"] ==
      source_doc["assembly_declared_sources_verified"])
identity = json.loads(pin(OUT / "IDENTIDADE_PREPARACAO.json")[0])
check("identity provenance", identity["source_request"] == source_doc["sources"]["request"])
check("identity no authorization/claim", identity["claim"] is False and
      identity["execution_authorization"] is False)
meta = json.loads(pin(OUT / "IDENTIDADE_ESTRUTURAL_METADATA.json")[0])
for key, projection in meta["projection"].items():
    check("structural metadata canonical pin " + key,
          hashlib.sha256(canonical(projection)).hexdigest() == meta["canonical_sha256"][key]
          == constants["STRUCTURAL_IDENTITY_PINS"][key])
check("283 unique ordered metadata rows", len(meta["projection"]["row_ids"]) == 283 and
      len(set(meta["projection"]["row_ids"])) == 283)
check("63 unique eta metadata labels", len(meta["projection"]["eta_columns"]) == 63 and
      len({v["key"] for v in meta["projection"]["eta_columns"]}) == 63)
check("seven metadata scale-five positions", meta["projection"]["native_to_output_row_scale"].count(5) == 7)
check("five exact models", constants["MODELS"] ==
      ("H1_TGL","H2_LCDM","H3_beta_free","H4_Cepheid","H5_rd_free"))
imports = []
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        imports.extend(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom):
        imports.append(node.module)
check("only declared stdlib imports", imports == ["hashlib", "json", "math", "re", "fractions"])
calls = [ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)]
for forbidden in ("open", "eval", "exec", "compile", "__import__", "importlib.import_module",
                  "np.linalg.eigh", "np.linalg.svd", "np.linalg.inv", "np.linalg.pinv",
                  "np.load", "np.save", "assemble_five", "gaussian_prior_marginal"):
    check("candidate has no call " + forbidden, forbidden not in calls)
check("one qualified constructor call site", calls.count("flat_gaussian_class") == 1)
check("one reused log integral call site", calls.count("self._engine.log_integral") == 1)
check("two reused support evaluator call sites", calls.count("self._engine.support.evaluate") == 2)
for i, handler in enumerate(n for n in ast.walk(tree) if isinstance(n, ast.ExceptHandler)):
    check("except handler raises without substitute return " + str(i),
          any(isinstance(n, ast.Raise) for n in ast.walk(handler)) and
          not any(isinstance(n, ast.Return) for n in ast.walk(handler)))
assignments = {}
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        assignments.setdefault(node.targets[0].id, []).append(ast.unparse(node.value))
check("actual Ty expression", "scales * yy" in assignments["y_out"])
check("actual TCTt full covariance expression",
      "scales[:, None] * cc * scales[None, :]" in assignments["covariance_out"])
check("actual affine origin transformation", "scales * oo" in assignments["origin_out"])
check("no second T multiplication of means", "self._np.array(means, dtype='<f8')" in assignments["mu"])
check("pointwise residual expression", "self._y - mu" in assignments["residual"])
classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
check("only adapter/error/context classes", set(classes) == {"ConsumerError", "PreparedJoint"})
check("explicit constructor inputs", [v.arg for v in functions["prepare_joint"].args.args] == ["y","C","row_ids"])
check("required keyword dependencies and admission", [v.arg for v in functions["prepare_joint"].args.kwonlyargs] ==
      ["affine_origin_native","structure_json","admission_json","admission_sha256",
       "backend_receipt_json","numpy_module","flat_gaussian_class"])
check("no keyword defaults silently choose tolerances", all(v is None for v in functions["prepare_joint"].args.kw_defaults))
text = raw.decode("utf-8")
for fragment in ('engine.support.rank == rank', 'packet["models"], MODELS',
                 'mu - self._origin', 'ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT',
                 'value == float("-inf")', 'math.isfinite(value)',
                 'prior_metadata_not_applied', 'common_log_kappa_omitted',
                 '"absolute_evidence": None', '"lnB": None', '"verdict": None',
                 '_canonical(structure) == _canonical(self._structure)',
                 'COORDINATES = "NATIVE_EQUATION_Y_OFFSETS_ALREADY_INCLUDED"',
                 'MM_STATUS = "CONDITIONAL_UNRATIFIED"'):
    check("explicit source invariant " + fragment, fragment in text)
contract = json.loads(pin(OUT / "CONTRATO_API.json")[0])
check("contract same identity/no authority", contract["request_id"] == constants["REQUEST_ID"] and
      contract["claim"] is False and contract["execution_authorization"] is False)
check("contract no numerical candidate exercise", all(contract["delivery_activity"][k] == 0 for k in
      ("candidate_imports","numpy_imports","backend_calls","controls_executed","observed_reads","remote_calls","solver_calls")))
for name in ("API_CONTRATO.md", "ALTERNATIVAS_ANTES_IMPLEMENTACAO.json"):
    pin(OUT / name)
linear = json.loads(Path(source_doc["sources"]["linear_receipt"]["path"]).read_bytes())
support = json.loads(Path(source_doc["sources"]["support_receipt"]["path"]).read_bytes())
# Preserve existing receipt objects as evidence references; do NOT rerun or count as our controls.
receipt = {
    "schema":"F9_CONSUMER_STATIC_PREPARATION_RECEIPT_V1",
    "request_id":constants["REQUEST_ID"],
    "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "statute":"REAL_BYTES_AST_METADATA_ONLY",
    "candidate_executed":False,"numpy_imported":False,"solver_calls":0,
    "observed_reads":0,"controls_executed":0,"authorization":False,"claim":False,
    "candidate_pin":code_pin,"checks":CHECKS,
    "all_static_checks_passed":all(c["passed"] for c in CHECKS),
    "pins_read":PINS,
    "custody_comparisons_are_not_numeric_tests":True,
    "historical_receipts_not_reexecuted":[source_doc["sources"]["linear_receipt"],
                                        source_doc["sources"]["support_receipt"]],
    "own_static_audit_seconds_before_persistence":time.perf_counter()-START,
    "limitation":"AST/pin checks do not execute transforms/support/likelihood or validate data/physics/runtime objects"
}
# create() itself adds a bookkeeping check; the result is still only a static receipt.
create("RECIBO_ESTATICO.json", receipt)
b=(OUT/"RECIBO_ESTATICO.json").read_bytes()
print(json.dumps({"checks":len(CHECKS),"all_static_passed":all(c["passed"] for c in CHECKS),
                  "receipt_bytes":len(b),"receipt_sha256":hashlib.sha256(b).hexdigest(),
                  "candidate_imports":0,"observed_reads":0},ensure_ascii=False))
