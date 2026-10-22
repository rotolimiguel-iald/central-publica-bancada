"""Build an additive F3.2 E1 projection binding from audited byte-lineage files."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

HERE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2")
F31 = HERE.parent / "F3.1"
OLD = {
    "binding": HERE / "VINCULO_DOCUMENTAL_V1X_R52_BYTES_20261008.json",
    "gate": HERE / "f9_reader_gate_v1x_r52_bytes.py",
    "pre": HERE / "f9_runner_v1x_preflight_r52_bytes.py",
    "stage": HERE / "f9_runner_v1x_staged_r52_bytes.py",
}
EXPECTED = {
    "binding": "f1aae0582e8bc672068476d717efcf5a4de730a23688eb67742abb4d18ac407a",
    "gate": "1fd01720e86ef2dc349ceeb0a839d32bbfa21eedab131fdb0681d1e245247f07",
    "pre": "5cecfb24cc01d396594d4930fb6abb0cf9a5b55e57f47987c8d89293902c2721",
    "stage": "7e3e2af9e456e4459ed77b1c36baf0e5d9b70ade9cb1b6b6185523cf7b641a4b",
}
for key, path in OLD.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED[key], path
E1 = F31 / "PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json"
e1_raw = E1.read_bytes()
e1_sha = hashlib.sha256(e1_raw).hexdigest()
assert e1_sha == "81a970926345832ad34d4963b0fadf70827003086e2876295d07024f83ffcca7"
e1 = json.loads(e1_raw)
assert e1["spec_sha256"] == "406d9d2dde90d6d250d71938ffbaaf3b881fdd459629630770cdc27c0d52bf58"
assert e1["derived_from"]["sha256"] == "6b6769da821b03dd96728202b478d3c0920b51f68cb6ca013916899390c517cd"
assert e1["spec"]["funcao_de_veredito"]["sha256"] == "544f60ef928c32620f2956665618daca4cb4116419d91197a09880c91c5274a5"

binding = json.loads(OLD["binding"].read_bytes())
old_last = binding["r52_ancestor_files"][-1]
assert old_last["role"] == "R5.2" and e1["derived_from"] == {k: old_last[k] for k in ("path", "bytes", "sha256")}
binding["draft_v2"] = {"path": str(E1), "bytes": len(e1_raw), "sha256": e1_sha}
binding["spec_sha256"] = e1["spec_sha256"]
binding["r52_ancestor_files"].append({"role": "F3.1.E1", **binding["draft_v2"]})
binding["e1_projection"] = {
    "parent_sha256": old_last["sha256"],
    "projection_sha256": e1_sha,
    "spec_sha256": e1["spec_sha256"],
    "function_sha256": e1["spec"]["funcao_de_veredito"]["sha256"],
    "freeze": False,
    "opening": False,
}
new_binding = HERE / "VINCULO_DOCUMENTAL_V1X_E1_BYTES_20261008.json"
with new_binding.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(binding, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write("\n")

gate = OLD["gate"].read_text(encoding="utf-8")
def change(before: str, after: str) -> None:
    global gate
    assert gate.count(before) == 1, (before, gate.count(before))
    gate = gate.replace(before, after, 1)
change('"""R5.2 byte-lineage documentary gate for a relocated two-witness package.',
       '"""F3.1.E1 byte-lineage documentary gate for a relocated two-witness package.')
change('R52_STATE = "RASCUNHO_DOCUMENTAL_R5_2_NAO_CONGELADO"',
       'R52_STATE = "RASCUNHO_DOCUMENTAL_R5_2_NAO_CONGELADO"\nE1_DRAFT_SHA256 = "81a970926345832ad34d4963b0fadf70827003086e2876295d07024f83ffcca7"\nE1_SPEC_SHA256 = "406d9d2dde90d6d250d71938ffbaaf3b881fdd459629630770cdc27c0d52bf58"')
change('    ("R5.2", "PREREGISTRO_FASE9_V2_R5_2_F31_20261008.json", R52_DRAFT_SHA256),\n)',
       '    ("R5.2", "PREREGISTRO_FASE9_V2_R5_2_F31_20261008.json", R52_DRAFT_SHA256),\n    ("F3.1.E1", "PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json", E1_DRAFT_SHA256),\n)')
change('len(records) != 4:', 'len(records) != 5:')
change('four ancestor file pins required', 'five lineage file pins required')
change('if index == 3:', 'if index == 4:')
change('R5.2 ancestor pin differs from draft pin', 'F3.1.E1 projection pin differs from draft pin')
change('if draft_pin["sha256"] != R52_DRAFT_SHA256:', 'if draft_pin["sha256"] != E1_DRAFT_SHA256:')
change('raise ReaderGateError("F3.4 projection pin differs")', 'raise ReaderGateError("F3.1.E1 projection pin differs")')
change('if draft.get("derived_from", {}).get("sha256") != R51_SHA256:',
       'if draft.get("derived_from", {}).get("sha256") != R52_DRAFT_SHA256:')
change('raise ReaderGateError("R5.2 draft parent pin differs")',
       'raise ReaderGateError("F3.1.E1 projection parent pin differs")')
needle = '    ancestor_receipt = _verify_ancestor_bytes(binding, draft_pin, draft, draft_raw, bundle_root)\n'
assert gate.count(needle) == 1
gate = gate.replace(needle, '''    if binding.get("e1_projection") != {
            "parent_sha256": R52_DRAFT_SHA256,
            "projection_sha256": E1_DRAFT_SHA256,
            "spec_sha256": E1_SPEC_SHA256,
            "function_sha256": R52_FUNCTION_SHA256,
            "freeze": False, "opening": False}:
        raise ReaderGateError("F3.1.E1 projection binding differs")
''' + needle, 1)
change('if spec_sha256 != R52_SPEC_SHA256:', 'if spec_sha256 != E1_SPEC_SHA256:')
change('raise ReaderGateError("R5.2 spec pin differs")', 'raise ReaderGateError("F3.1.E1 spec pin differs")')
change('        "ancestor_bytes_rechecked": ancestor_receipt,',
       '        "ancestor_bytes_rechecked": ancestor_receipt,\n        "projection": "F3.1.E1",')
new_gate = HERE / "f9_reader_gate_v1x_e1_bytes.py"
with new_gate.open("x", encoding="utf-8", newline="\n") as f:
    f.write(gate)

pre = OLD["pre"].read_text(encoding="utf-8").replace(
    "f9_reader_gate_v1x_r52_bytes import", "f9_reader_gate_v1x_e1_bytes import")
assert "f9_reader_gate_v1x_e1_bytes import" in pre
with (HERE / "f9_runner_v1x_preflight_e1_bytes.py").open("x", encoding="utf-8", newline="\n") as f:
    f.write(pre)

stage = OLD["stage"].read_text(encoding="utf-8").replace(
    "f9_reader_gate_v1x_r52_bytes import", "f9_reader_gate_v1x_e1_bytes import").replace(
    "f9_runner_v1x_preflight_r52_bytes import", "f9_runner_v1x_preflight_e1_bytes import")
assert "f9_reader_gate_v1x_e1_bytes import" in stage
with (HERE / "f9_runner_v1x_staged_e1_bytes.py").open("x", encoding="utf-8", newline="\n") as f:
    f.write(stage)
print(json.dumps({"binding_sha256": hashlib.sha256(new_binding.read_bytes()).hexdigest(),
                  "e1_sha256": e1_sha, "spec_sha256": e1["spec_sha256"]}, ensure_ascii=False))
