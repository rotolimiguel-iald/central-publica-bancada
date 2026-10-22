"""Read/hash/AST only. Never imports candidates, Fraction or controls."""
from pathlib import Path
import ast, datetime, hashlib, json, sys
ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
P = ROOT / "f9_nc02_rational_preparation"
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "proveniencia"))
from audit_provenance import atomic, metadata

def load(path):
    return json.loads(path.read_bytes())

def compare(pin):
    p = Path(pin["path"])
    raw = p.read_bytes()
    return {"path": str(p), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "matches": len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"]}

inputs = load(P / "EXECUTION_INPUTS.json")
runtime = load(P / "RUNTIME_PINS.json")
manifest = load(P / "MANIFESTO_PREPARACAO_NC02.json")
execution_pins = [compare(x) for x in inputs["pins"]]
manifest_pins = [compare(x) for x in manifest["files"]]
assert all(x["matches"] for x in execution_pins + manifest_pins)
assert len(execution_pins) == len({x["path"].casefold() for x in execution_pins}) == 536
assert len(runtime["pins"]) == 506
expected = {x["path"].casefold(): (x["bytes"], x["sha256"]) for x in inputs["pins"]}
assert all(expected[x["path"].casefold()] == (x["bytes"], x["sha256"]) for x in runtime["pins"])
modules = ["builder.py", "codec_adapter.py", "verifier.py", "worker_controls.py", "supervisor.py", "finalization.py"]
snapshots = []
ast_inventory = []
for name in modules:
    path = P/name
    pin, raw = metadata(path)
    tree = ast.parse(raw, filename=str(path))
    target = OUT/(name + ".snapshot.txt")
    atomic(target, raw)
    snapshots.append({"source": pin, "snapshot": metadata(target)[0]})
    ast_inventory.append({"path": str(path), "syntax_parsed": True,
                          "declared_imports": [{"line": n.lineno, "source": ast.get_source_segment(raw.decode("utf-8"), n)} for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]})
codec = Path(inputs["codec_source_path"])
ctree = ast.parse(codec.read_bytes())
codec_top = [{"line": n.lineno, "node": type(n).__name__, "name": getattr(n, "name", None)} for n in ctree.body]
source_names = [P/n for n in ["MANIFESTO_PREPARACAO_NC02.json", "EXECUTION_INPUTS.json", "RUNTIME_PINS.json", "IDENTITY.json", "CONTROL_CONTRACT.json", "NOTA_BUILDER_NC02.md"]]
source_names += [Path(inputs["payload_path"]), codec, ROOT/"f9_numerical_certification_preparation/CONTRATO_NUMERICO_F9.md", ROOT/"f9_numerical_certification_preparation/PLANO_SINTETICO_NUMERICO.json", ROOT/"RECIBO_ROOT_BACKEND_E_PREPARACAO_NC02.json"]
source_names += [Path(r"C:\Python314\Lib")/n for n in ["fractions.py", "dataclasses.py", "annotationlib.py", "inspect.py", "subprocess.py", "ctypes/__init__.py"]]
receipt = {"status": "INDEPENDENT_STATIC_REVIEW_NOT_EXECUTION", "at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "execution_pins": execution_pins, "manifest_pins": manifest_pins,
           "counts": {"execution_pins": len(execution_pins), "runtime_pins": len(runtime["pins"]), "manifest_members": len(manifest_pins), "source_modules_parsed": len(modules)},
           "sources": [metadata(x)[0] for x in source_names], "source_snapshots": snapshots,
           "ast_inventory": ast_inventory, "codec_top_level_ast": codec_top,
           "finalizer_same_bytes_as_tail_v2": (P/"finalization.py").read_bytes() == (ROOT/"f9_tail_envelope_implementation_v2/finalization.py").read_bytes(),
           "state_exists_at_review": {n: (P/n).exists() for n in ["AUTORIZACAO_ROOT.json", "CLAIM.json", "RUN", "TERMINAL_RECEIPT.json", "FINALIZATION_FAILURE.json"]},
           "candidate_imports": 0, "candidate_executions": 0, "Fraction_import_or_control_execution": 0,
           "WSL": 0, "observed_centres_read": False, "new_authorization_claim_request_created": False,
           "limits": "Static custody/AST only; no dynamic import closure, timing, memory, numeric case or physical certificate validated."}
assert receipt["finalizer_same_bytes_as_tail_v2"]
assert not any(receipt["state_exists_at_review"].values())
atomic(OUT/"RECIBO_REVISAO_ESTATICA.json", json.dumps(receipt, ensure_ascii=False, indent=2)+"\n")
print(json.dumps({"counts": receipt["counts"], "pins_all_match": True, "finalizer_same": True, "execution_state_absent": True}, ensure_ascii=False))
