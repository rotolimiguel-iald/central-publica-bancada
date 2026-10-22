from __future__ import annotations
import hashlib
import json
from pathlib import Path

HERE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2")
F31 = HERE.parent / "F3.1"
OLD_GATE = HERE / "f9_reader_gate_v1x_r52.py"
OLD_PRE = HERE / "f9_runner_v1x_preflight_r52.py"
OLD_STAGE = HERE / "f9_runner_v1x_staged_r52.py"
OLD_BIND = HERE / "VINCULO_DOCUMENTAL_V1X_R52_20261008.json"
PINS = {
    OLD_GATE: "779b20872b309f3078ae14b86c94c796cbaa6fd432cd80dc91ced606e4f522f2",
    OLD_PRE: "9a6b625d5a3f1682e25de7b5c92badcdfb762867a2b7779bc781cf88542548f6",
    OLD_STAGE: "1d5f0abffe0630057341cb2e4fd320ea2940fa967ddc95684a455a063fa97008",
    OLD_BIND: "a0c098763d305308e47b40196263416b63d6b7893d555bd9618072915c3f6316",
}
for p, digest in PINS.items():
    assert hashlib.sha256(p.read_bytes()).hexdigest() == digest, p
names = [
    ("F3.4", "PREREGISTRO_FASE9_V2_R4_F34_DUAS_TESTEMUNHAS_20261008.json", "ca59870c4e840bf6c87b7b5051cc1b4e6ff25a88d026fca38893291fdd14153f"),
    ("R5", "PREREGISTRO_FASE9_V2_R5_F31_20261008.json", "ab84d493c9ac54083eb78495e19e9da93782392ca5ffa5981e5ac7c83ce76f09"),
    ("R5.1", "PREREGISTRO_FASE9_V2_R5_1_F31_20261008.json", "f73bee1d8b45c43575e73bea8f4adf10724d039f1b96a50542cd7e70ae100c60"),
    ("R5.2", "PREREGISTRO_FASE9_V2_R5_2_F31_20261008.json", "6b6769da821b03dd96728202b478d3c0920b51f68cb6ca013916899390c517cd"),
]
pins = []
for role, name, digest in names:
    p = F31 / name
    raw = p.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == digest
    pins.append({"role": role, "path": str(p), "bytes": len(raw), "sha256": digest})
binding = json.loads(OLD_BIND.read_bytes())
binding["r52_ancestor_files"] = pins
binding["relocation_rule"] = {
    "historic_root": str(HERE.parents[1]),
    "mapped_root": "binding_parent/../..",
    "source_subtree": "ORDEM_018",
    "ancestor_subtree": "ORDEM_019/F3.1",
    "original_documentary_paths_remain_in_metadata": True,
}
new_binding = HERE / "VINCULO_DOCUMENTAL_V1X_R52_BYTES_20261008.json"
with new_binding.open("x", encoding="utf-8", newline="\n") as f:
    json.dump(binding, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write("\n")
source = OLD_GATE.read_text(encoding="utf-8")
source = source.replace(
    '"""R5.2 fail-closed documentary gate for the two-witness V2 draft and V1.x readers.\n\nIt reuses the audited byte reader and does not call official_archive_check(),\nwhose pin and metadata belong to historical V1. No admission or verdict.\n"""',
    '"""R5.2 byte-lineage documentary gate for a relocated two-witness package.\n\nRe-read F3.4, R5, R5.1 and R5.2 bytes at each invocation. Historic paths\nin pinned metadata remain documentary strings; actual reads map under the\nbundle containing this binding. No admission, opening, freeze or verdict.\n"""'
)
marker = '_SHA256 = re.compile(r"[0-9a-f]{64}\\Z")\n'
addon = r'''
HISTORIC_ARCHIVE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT")
ANCESTOR_NAMES = (
    ("F3.4", "PREREGISTRO_FASE9_V2_R4_F34_DUAS_TESTEMUNHAS_20261008.json", F34_DRAFT_SHA256),
    ("R5", "PREREGISTRO_FASE9_V2_R5_F31_20261008.json", R5_SHA256),
    ("R5.1", "PREREGISTRO_FASE9_V2_R5_1_F31_20261008.json", R51_SHA256),
    ("R5.2", "PREREGISTRO_FASE9_V2_R5_2_F31_20261008.json", R52_DRAFT_SHA256),
)


def _bundle_root(binding_path: Path) -> Path:
    path = base._resolve_existing(binding_path)
    if path.parent.name != "F3.2" or path.parent.parent.name != "ORDEM_019":
        raise ReaderGateError("binding outside portable F3.2 package")
    return path.parents[2]


def _relocated_path(documentary_path: str, bundle_root: Path, subtree: str) -> Path:
    original = Path(documentary_path)
    try:
        relative = original.relative_to(HISTORIC_ARCHIVE_ROOT)
    except ValueError as exc:
        raise ReaderGateError("documentary path outside historic package") from exc
    expected = Path(subtree)
    if relative != expected and not relative.is_relative_to(expected):
        raise ReaderGateError("documentary path outside expected subtree")
    destination = base._resolve_existing(bundle_root / relative)
    allowed = base._resolve_existing(bundle_root / expected)
    if not destination.is_relative_to(allowed):
        raise ReaderGateError("relocated path escaped expected subtree")
    return destination


def _verify_ancestor_bytes(binding: dict, draft_pin: dict, draft: dict,
                           draft_raw: bytes, bundle_root: Path) -> list[dict]:
    records = binding.get("r52_ancestor_files")
    if not isinstance(records, list) or len(records) != 4:
        raise ReaderGateError("four ancestor file pins required")
    actual = []
    previous = None
    for index, (role, name, expected_sha) in enumerate(ANCESTOR_NAMES):
        pin = _pin(records[index], f"ancestor[{index}]")
        documentary = HISTORIC_ARCHIVE_ROOT / "ORDEM_019" / "F3.1" / name
        if pin.get("role") != role or pin["path"] != str(documentary) or pin["sha256"] != expected_sha:
            raise ReaderGateError(f"ancestor identity differs: {role}")
        if index == 3:
            if pin != {**draft_pin, "role": role}:
                raise ReaderGateError("R5.2 ancestor pin differs from draft pin")
            obj, raw = draft, draft_raw
        else:
            path = _relocated_path(pin["path"], bundle_root, "ORDEM_019/F3.1")
            obj, raw = base._read_json(path)
        digest = base._digest(raw)
        if len(raw) != pin["bytes"] or digest != expected_sha:
            raise ReaderGateError(f"ancestor bytes/hash mismatch: {role}")
        if previous is not None and obj.get("derived_from") != previous:
            raise ReaderGateError(f"ancestor parent does not bind bytes: {role}")
        actual.append({"role": role, "sha256": digest, "bytes": len(raw)})
        previous = {"path": pin["path"], "bytes": pin["bytes"], "sha256": pin["sha256"]}
    return actual
'''
assert source.count(marker) == 1
source = source.replace(marker, marker + addon, 1)
source = source.replace(
    'def _pinned_file(value: object, name: str, root: Path | None = None) -> tuple[dict, Path, bytes]:\n    pin = _pin(value, name)\n    path = base._resolve_existing(Path(pin["path"]))',
    'def _pinned_file(value: object, name: str, root: Path, bundle_root: Path) -> tuple[dict, Path, bytes]:\n    pin = _pin(value, name)\n    path = _relocated_path(pin["path"], bundle_root, "ORDEM_018")'
)
source = source.replace(
    'def _source_text(record: dict, reader_id: str, root: Path) -> tuple[bytes, bytes]:',
    'def _source_text(record: dict, reader_id: str, root: Path, bundle_root: Path) -> tuple[bytes, bytes]:'
)
source = source.replace('f"{reader_id}.source", root)', 'f"{reader_id}.source", root, bundle_root)')
source = source.replace('f"{reader_id}.text_projection", root\n', 'f"{reader_id}.text_projection", root, bundle_root\n')
source = source.replace('f"{reader_id}.projection_receipt", root\n', 'f"{reader_id}.projection_receipt", root, bundle_root\n')
source = source.replace(
    '    binding_path = base._resolve_existing(binding_path)\n    binding, binding_raw = base._read_json(binding_path)',
    '    binding_path = base._resolve_existing(binding_path)\n    bundle_root = _bundle_root(binding_path)\n    binding, binding_raw = base._read_json(binding_path)'
)
source = source.replace(
    '    draft_path = base._resolve_existing(Path(draft_pin["path"]))',
    '    draft_path = _relocated_path(draft_pin["path"], bundle_root, "ORDEM_019/F3.1")'
)
needle = '    spec = _object(draft.get("spec"), "draft spec")\n'
assert source.count(needle) == 1
source = source.replace(needle,
    '    ancestor_receipt = _verify_ancestor_bytes(binding, draft_pin, draft, draft_raw, bundle_root)\n' + needle)
source = source.replace(
    '    root = base._resolve_existing(allowed_source_root)\n    verified = {}',
    '    root = base._resolve_existing(allowed_source_root)\n    if root != base._resolve_existing(bundle_root / "ORDEM_018"):\n        raise ReaderGateError("source root differs from relocated ORDEM_018")\n    verified = {}'
)
source = source.replace('_source_text(record, reader_id, root)', '_source_text(record, reader_id, root, bundle_root)')
source = source.replace('        "draft_v2_sha256": base._digest(draft_raw),',
                        '        "draft_v2_sha256": base._digest(draft_raw),\n        "ancestor_bytes_rechecked": ancestor_receipt,')
assert '_relocated_path' in source and 'ancestor_bytes_rechecked' in source
new_gate = HERE / "f9_reader_gate_v1x_r52_bytes.py"
new_gate.write_text(source, encoding="utf-8", newline="\n")
pre = OLD_PRE.read_text(encoding="utf-8").replace("f9_reader_gate_v1x_r52 import", "f9_reader_gate_v1x_r52_bytes import")
(HERE / "f9_runner_v1x_preflight_r52_bytes.py").write_text(pre, encoding="utf-8", newline="\n")
stage = OLD_STAGE.read_text(encoding="utf-8").replace("f9_reader_gate_v1x_r52 import", "f9_reader_gate_v1x_r52_bytes import").replace("f9_runner_v1x_preflight_r52 import", "f9_runner_v1x_preflight_r52_bytes import")
(HERE / "f9_runner_v1x_staged_r52_bytes.py").write_text(stage, encoding="utf-8", newline="\n")
print(json.dumps({"binding_sha256": hashlib.sha256(new_binding.read_bytes()).hexdigest(),
                  "files": [str(new_binding), str(new_gate)]}, ensure_ascii=False))
