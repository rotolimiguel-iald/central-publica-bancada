"""Create a new fail-closed F3.4 gate and synthetic runner from pinned R4 bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
F31 = HERE.parent / "F3.1"
SCALAR = F31 / "PREREGISTRO_FASE9_V2_R4_F34_DUAS_TESTEMUNHAS_20261008.json"
R4_BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R4_20261008.json"
R4_GATE = HERE / "f9_reader_gate_v1x_r4.py"
R4_PRE = HERE / "f9_runner_v1x_preflight_r4.py"
R4_STAGE = HERE / "f9_runner_v1x_staged_r4.py"
F34_SCALAR_SHA = "ca59870c4e840bf6c87b7b5051cc1b4e6ff25a88d026fca38893291fdd14153f"
F34_SPEC_SHA = "dbe01f4cef9e6d155d51cbf2930014289144761bb8b948a3b3195615bc609e1b"
ORIGINAL_R4_SHA = "3f4017bf3229903106d2c85388bde9ebfd57e076428e48af5be33c873d5c2d00"
VERDICT_SHA = "98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d"
RESOLUTION_SHA = "01b6a50e6d1fe3a2531b6400880f028b603f22f787c05dacb563d715d2db535d"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pretty(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def replace_one(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"Expected one occurrence, found {text.count(old)}: {old[:70]}")
    return text.replace(old, new, 1)


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    with path.open("xb") as out:
        out.write(data)
        out.flush()
    if path.read_bytes() != data:
        raise OSError(f"Round-trip differs: {path}")


def main() -> None:
    raw_scalar = SCALAR.read_bytes()
    if sha(raw_scalar) != F34_SCALAR_SHA:
        raise ValueError("F3.4 scalar projection changed")
    scalar = json.loads(raw_scalar)
    if scalar["state"] != "RASCUNHO_DOCUMENTAL_F34_NAO_CONGELADO":
        raise ValueError("F3.4 scalar projection state changed")
    if scalar["spec_sha256"] != F34_SPEC_SHA or scalar["derived_from"]["sha256"] != ORIGINAL_R4_SHA:
        raise ValueError("F3.4 scalar projection pin changed")
    if scalar["spec"]["funcao_de_veredito"]["sha256"] != VERDICT_SHA:
        raise ValueError("R4 verdict function changed")

    raw_binding = R4_BINDING.read_bytes()
    binding = json.loads(raw_binding)
    if binding["draft_v2"]["sha256"] != ORIGINAL_R4_SHA:
        raise ValueError("R4 binding basis changed")
    binding["draft_v2"] = {"path": str(SCALAR), "bytes": len(raw_scalar), "sha256": F34_SCALAR_SHA}
    binding["spec_sha256"] = F34_SPEC_SHA
    binding["scope"] = (
        "F3.4 documentary gate: two independent witnesses; V2 R4+F3.4 draft; "
        "historical R4 reader source bytes unchanged; no admission, freeze or opening"
    )
    binding["f34_decision"] = {
        "quadro_event": 462,
        "resolution_sha256": RESOLUTION_SHA,
        "scalar_original_r4_sha256": ORIGINAL_R4_SHA,
        "scalar_projection_sha256": F34_SCALAR_SHA,
        "joint_witness_separate": True,
        "no_pooling": True,
        "opening": False,
    }

    gate = R4_GATE.read_text(encoding="utf-8")
    gate = replace_one(
        gate,
        'if draft.get("state") != "RASCUNHO_NAO_CONGELADO":\n',
        'if draft_pin["sha256"] != F34_DRAFT_SHA256:\n'
        '        raise ReaderGateError("F3.4 projection pin differs")\n'
        '    if draft.get("state") != "RASCUNHO_DOCUMENTAL_F34_NAO_CONGELADO":\n',
    )
    gate = replace_one(
        gate,
        '    spec = _object(draft.get("spec"), "draft spec")\n',
        '    if draft.get("derived_from", {}).get("sha256") != ORIGINAL_R4_SHA256:\n'
        '        raise ReaderGateError("F3.4 projection is not derived from pinned R4")\n'
        '    decision = _object(binding.get("f34_decision"), "F3.4 decision")\n'
        '    if decision != {"quadro_event": 462, "resolution_sha256": F34_RESOLUTION_SHA256,\n'
        '                    "scalar_original_r4_sha256": ORIGINAL_R4_SHA256,\n'
        '                    "scalar_projection_sha256": F34_DRAFT_SHA256,\n'
        '                    "joint_witness_separate": True, "no_pooling": True, "opening": False}:\n'
        '        raise ReaderGateError("F3.4 decision binding differs")\n'
        '    spec = _object(draft.get("spec"), "draft spec")\n'
        '    witness = _object(spec.get("f34_duas_testemunhas"), "F3.4 witness")\n'
        '    if (witness.get("quadro_f34") != {"status": "FECHADA", "evento": 462}\n'
        '            or witness.get("congelamento") is not False or witness.get("abertura") is not False\n'
        '            or witness.get("fonte_ratificacao", {}).get("sha256") != F34_RESOLUTION_SHA256\n'
        '            or any(str(x).startswith("F3.4 ") for x in spec.get("pending_operator_decisions", []))):\n'
        '        raise ReaderGateError("F3.4 witness contract differs")\n',
    )
    gate = replace_one(
        gate,
        '    if expected_spec_sha256 is not None and expected_spec_sha256 != spec_sha256:\n',
        '    if spec_sha256 != F34_SPEC_SHA256:\n'
        '        raise ReaderGateError("F3.4 spec pin differs")\n'
        '    if expected_spec_sha256 is not None and expected_spec_sha256 != spec_sha256:\n',
    )
    gate = replace_one(
        gate,
        'BINDING_SCHEMA = "F9_SCALAR_V1X_DOCUMENTARY_BINDING_V2_DRAFT"\n',
        'BINDING_SCHEMA = "F9_SCALAR_V1X_DOCUMENTARY_BINDING_V2_DRAFT"\n'
        f'F34_DRAFT_SHA256 = "{F34_SCALAR_SHA}"\n'
        f'F34_SPEC_SHA256 = "{F34_SPEC_SHA}"\n'
        f'ORIGINAL_R4_SHA256 = "{ORIGINAL_R4_SHA}"\n'
        f'F34_RESOLUTION_SHA256 = "{RESOLUTION_SHA}"\n',
    )
    gate = replace_one(
        gate,
        '"""R4 fail-closed documentary gate for the Fase 9 V2 draft and V1.x readers.',
        '"""F3.4 fail-closed documentary gate for the two-witness V2 draft and V1.x readers.',
    )

    pre = R4_PRE.read_text(encoding="utf-8")
    pre = replace_one(pre, 'from f9_reader_gate_v1x_r4 import', 'from f9_reader_gate_v1x_f34 import')
    pre = replace_one(pre, 'source admission, F3.4 and X13.', 'source admission and X13.')
    pre = replace_one(pre, '"spec_governance": "PENDING_F3_4"', '"spec_governance": "F3_4_RESOLVED_TWO_WITNESSES"')

    stage = R4_STAGE.read_text(encoding="utf-8")
    stage = replace_one(stage, 'from f9_reader_gate_v1x_r4 import', 'from f9_reader_gate_v1x_f34 import')
    stage = replace_one(stage, 'from f9_runner_v1x_preflight_r4 import', 'from f9_runner_v1x_preflight_f34 import')
    stage = replace_one(stage, '"spec_governance": "PENDING_F3_4"', '"spec_governance": "F3_4_RESOLVED_TWO_WITNESSES"')

    files = {
        "VINCULO_DOCUMENTAL_V1X_F34_20261008.json": pretty(binding),
        "f9_reader_gate_v1x_f34.py": gate.encode("utf-8"),
        "f9_runner_v1x_preflight_f34.py": pre.encode("utf-8"),
        "f9_runner_v1x_staged_f34.py": stage.encode("utf-8"),
    }
    for name in files:
        if (HERE / name).exists():
            raise FileExistsError(HERE / name)
    for name, data in files.items():
        write_new(HERE / name, data)
    print(json.dumps({"created": {name: sha(data) for name, data in files.items()}}, indent=2))


if __name__ == "__main__":
    main()
