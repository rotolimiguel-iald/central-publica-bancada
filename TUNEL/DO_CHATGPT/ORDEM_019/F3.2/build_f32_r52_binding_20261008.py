"""Create an additive F3.2 documentary binding for the F3.1 R5.2 draft.

The output remains synthetic-only and does not admit sources or freeze either witness.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
F31 = HERE.parent / "F3.1"
BASE_BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_F34_20261008.json"
BASE_GATE = HERE / "f9_reader_gate_v1x_f34.py"
BASE_PRE = HERE / "f9_runner_v1x_preflight_f34.py"
BASE_STAGE = HERE / "f9_runner_v1x_staged_f34.py"
R5 = F31 / "PREREGISTRO_FASE9_V2_R5_F31_20261008.json"
R51 = F31 / "PREREGISTRO_FASE9_V2_R5_1_F31_20261008.json"
BASE_BINDING_SHA256 = "19d03542ae8839d4856a44eb2291397a4c26f7760881345762d1de5e7c0854cc"
R5_SHA256 = "ab84d493c9ac54083eb78495e19e9da93782392ca5ffa5981e5ac7c83ce76f09"
R51_SHA256 = "f73bee1d8b45c43575e73bea8f4adf10724d039f1b96a50542cd7e70ae100c60"
F34_DRAFT_SHA256 = "ca59870c4e840bf6c87b7b5051cc1b4e6ff25a88d026fca38893291fdd14153f"
F34_SPEC_SHA256 = "dbe01f4cef9e6d155d51cbf2930014289144761bb8b948a3b3195615bc609e1b"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def replace_one(source: str, old: str, new: str) -> str:
    count = source.count(old)
    if count != 1:
        raise ValueError(f"expected exactly one occurrence ({count}): {old[:100]}")
    return source.replace(old, new, 1)


def pretty(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    draft_path = args.draft.resolve(strict=True)
    if draft_path.parent != F31.resolve() or "R5_2" not in draft_path.name:
        raise ValueError("draft must be the F3.1 R5.2 artifact")
    draft_raw = draft_path.read_bytes()
    draft = json.loads(draft_raw)
    draft_sha = sha(draft_raw)
    r5_raw = R5.read_bytes()
    parent_raw = R51.read_bytes()
    if sha(r5_raw) != R5_SHA256 or sha(parent_raw) != R51_SHA256:
        raise ValueError("R5/R5.1 parent changed")
    if json.loads(r5_raw).get("derived_from", {}).get("sha256") != F34_DRAFT_SHA256:
        raise ValueError("R5 is not derived from the F3.4 projection")
    if json.loads(parent_raw).get("derived_from", {}).get("sha256") != R5_SHA256:
        raise ValueError("R5.1 is not derived from pinned R5")
    if draft.get("derived_from", {}).get("sha256") != R51_SHA256:
        raise ValueError("R5.2 parent pin differs")
    state = draft.get("state")
    if not isinstance(state, str) or "R5_2" not in state or "NAO_CONGELADO" not in state:
        raise ValueError("R5.2 state is not an explicit unfrozen draft")
    spec = draft["spec"]
    spec_raw = json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    spec_sha = sha(spec_raw)
    if spec_sha != draft.get("spec_sha256"):
        raise ValueError("R5.2 spec hash differs")
    function = spec["funcao_de_veredito"]
    function_name = function["nome"]
    function_sha = sha(function["fonte"].encode("utf-8"))
    if function_sha != function.get("sha256") or function_name != "veredito_fase9_v2_r5_2_proposta":
        raise ValueError("R5.2 function pin or name differs")
    witness = spec["f34_duas_testemunhas"]
    if (witness.get("quadro_f34") != {"evento": 462, "status": "FECHADA"}
            or witness.get("congelamento") is not False
            or witness.get("abertura") is not False):
        raise ValueError("two-witness decision changed")
    binding_raw = BASE_BINDING.read_bytes()
    if sha(binding_raw) != BASE_BINDING_SHA256:
        raise ValueError("audited F3.4 binding changed")
    binding = copy.deepcopy(json.loads(binding_raw))
    if binding["draft_v2"]["sha256"] != F34_DRAFT_SHA256 or binding["spec_sha256"] != F34_SPEC_SHA256:
        raise ValueError("F3.4 binding basis differs")
    binding["draft_v2"] = {"path": str(draft_path), "bytes": len(draft_raw), "sha256": draft_sha}
    binding["spec_sha256"] = spec_sha
    binding["scope"] = (
        "F3.1 R5.2 documentary draft on the F3.4 two-witness decision; "
        "audited reader sources unchanged; no admission, freeze or opening"
    )
    lineage = {
        "f34_sha256": F34_DRAFT_SHA256,
        "r5_sha256": R5_SHA256,
        "r51_sha256": R51_SHA256,
        "r52_sha256": draft_sha,
        "r52_spec_sha256": spec_sha,
        "r52_function_sha256": function_sha,
    }
    binding["r52_lineage"] = lineage

    gate = BASE_GATE.read_text(encoding="utf-8")
    gate = replace_one(gate, 'F34_RESOLUTION_SHA256 = "01b6a50e6d1fe3a2531b6400880f028b603f22f787c05dacb563d715d2db535d"\n',
                       'F34_RESOLUTION_SHA256 = "01b6a50e6d1fe3a2531b6400880f028b603f22f787c05dacb563d715d2db535d"\n'
                       f'R51_SHA256 = "{R51_SHA256}"\nR52_DRAFT_SHA256 = "{draft_sha}"\n'
                       f'R5_SHA256 = "{R5_SHA256}"\nR52_SPEC_SHA256 = "{spec_sha}"\nR52_FUNCTION_SHA256 = "{function_sha}"\n'
                       f'R52_STATE = "{state}"\n')
    gate = replace_one(gate, 'if draft_pin["sha256"] != F34_DRAFT_SHA256:',
                       'if draft_pin["sha256"] != R52_DRAFT_SHA256:')
    gate = replace_one(gate, 'if draft.get("state") != "RASCUNHO_DOCUMENTAL_F34_NAO_CONGELADO":',
                       'if draft.get("state") != R52_STATE:')
    gate = replace_one(gate, 'if draft.get("derived_from", {}).get("sha256") != ORIGINAL_R4_SHA256:',
                       'if draft.get("derived_from", {}).get("sha256") != R51_SHA256:')
    gate = replace_one(gate, 'raise ReaderGateError("F3.4 projection is not derived from pinned R4")',
                       'raise ReaderGateError("R5.2 draft parent pin differs")')
    gate = replace_one(gate, '    spec = _object(draft.get("spec"), "draft spec")\n',
                       '    if binding.get("r52_lineage") != {"f34_sha256": F34_DRAFT_SHA256,\n'
                       '            "r5_sha256": R5_SHA256, "r51_sha256": R51_SHA256,\n'
                       '            "r52_sha256": R52_DRAFT_SHA256, "r52_spec_sha256": R52_SPEC_SHA256,\n'
                       '            "r52_function_sha256": R52_FUNCTION_SHA256}:\n'
                       '        raise ReaderGateError("R5.2 lineage binding differs")\n'
                       '    spec = _object(draft.get("spec"), "draft spec")\n')
    gate = replace_one(gate, 'if spec_sha256 != F34_SPEC_SHA256:',
                       'if spec_sha256 != R52_SPEC_SHA256:')
    gate = replace_one(gate, '        raise ReaderGateError("F3.4 spec pin differs")',
                       '        raise ReaderGateError("R5.2 spec pin differs")')
    gate = replace_one(gate, '    readers = _object(spec.get("leitores"), "draft readers")\n',
                       '    verdict_record = _object(spec.get("funcao_de_veredito"), "draft verdict function")\n'
                       '    source = _text(verdict_record.get("fonte"), "draft verdict source")\n'
                       '    if (verdict_record.get("nome") != "veredito_fase9_v2_r5_2_proposta"\n'
                       '            or verdict_record.get("sha256") != R52_FUNCTION_SHA256\n'
                       '            or hashlib.sha256(source.encode("utf-8")).hexdigest() != R52_FUNCTION_SHA256):\n'
                       '        raise ReaderGateError("R5.2 verdict function pin differs")\n'
                       '    readers = _object(spec.get("leitores"), "draft readers")\n')
    gate = replace_one(gate, '"""F3.4 fail-closed documentary gate for the two-witness V2 draft and V1.x readers.',
                       '"""R5.2 fail-closed documentary gate for the two-witness V2 draft and V1.x readers.')

    pre = BASE_PRE.read_text(encoding="utf-8")
    pre = replace_one(pre, 'from f9_reader_gate_v1x_f34 import',
                      'from f9_reader_gate_v1x_r52 import')
    stage = BASE_STAGE.read_text(encoding="utf-8")
    stage = replace_one(stage, 'from f9_reader_gate_v1x_f34 import',
                        'from f9_reader_gate_v1x_r52 import')
    stage = replace_one(stage, 'from f9_runner_v1x_preflight_f34 import',
                        'from f9_runner_v1x_preflight_r52 import')
    stage = replace_one(stage, 'import math\n', 'import math\nimport decimal\n')
    stage = replace_one(stage, 'PINNED_R4_VERDICT_SOURCE_SHA256 = "98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d"',
                        f'PINNED_R52_VERDICT_SOURCE_SHA256 = "{function_sha}"')
    stage = replace_one(stage, 'name = "veredito_fase9_v2_r4_proposta"',
                        'name = "veredito_fase9_v2_r5_2_proposta"')
    stage = replace_one(stage, 'PINNED_R4_VERDICT_SOURCE_SHA256:',
                        'PINNED_R52_VERDICT_SOURCE_SHA256:')
    stage = replace_one(stage, '    def import_math(module, *args, **kwargs):\n'
                        '        if module != "math":\n'
                        '            raise ReaderGateError("proposed verdict attempted unexpected import")\n'
                        '        return math\n',
                        '    def import_allowed(module, *args, **kwargs):\n'
                        '        if module == "math":\n'
                        '            return math\n'
                        '        if module == "decimal":\n'
                        '            return decimal\n'
                        '        raise ReaderGateError("proposed verdict attempted unexpected import")\n')
    stage = replace_one(stage, '        "__builtins__": {"__import__": import_math, "abs": abs, "any": any,\n'
                        '                         "int": int, "range": range},\n',
                        '        "__builtins__": {"__import__": import_allowed, "abs": abs,\n'
                        '                         "any": any, "all": all, "bool": bool, "dict": dict,\n'
                        '                         "enumerate": enumerate, "float": float,\n'
                        '                         "format": format, "int": int,\n'
                        '                         "isinstance": isinstance, "len": len, "list": list,\n'
                        '                         "range": range, "set": set, "str": str,\n'
                        '                         "tuple": tuple, "type": type, "ValueError": ValueError},\n')
    stage = replace_one(stage, '<pinned-V2-R4-proposed-verdict>',
                        '<pinned-V2-R5.2-proposed-verdict>')
    stage = replace_one(stage, 'TGL_FASE9_RAZAO_DE_HUBBLE_V2_R4_DRAFT__',
                        'TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_2_DRAFT__')
    stage = replace_one(stage, '"""Compile only the exact R4 draft function already pinned by the V2 spec."""',
                        '"""Compile only the exact R5.2 draft function pinned by the V2 spec."""')
    stage = replace_one(stage, 'SYNTHETIC_ONLY: pinned R4 proposed rule checks',
                        'SYNTHETIC_ONLY: pinned R5.2 proposed rule checks')

    files = {
        "VINCULO_DOCUMENTAL_V1X_R52_20261008.json": pretty(binding),
        "f9_reader_gate_v1x_r52.py": gate.encode("utf-8"),
        "f9_runner_v1x_preflight_r52.py": pre.encode("utf-8"),
        "f9_runner_v1x_staged_r52.py": stage.encode("utf-8"),
    }
    if args.check:
        print(json.dumps({"draft_sha256": draft_sha, "spec_sha256": spec_sha,
                          "function_sha256": function_sha,
                          "would_create": {name: sha(data) for name, data in files.items()}}, indent=2))
        return
    if any((HERE / name).exists() for name in files):
        raise FileExistsError("R5.2 F3.2 output already exists")
    for name, data in files.items():
        with (HERE / name).open("xb") as out:
            out.write(data)
        if (HERE / name).read_bytes() != data:
            raise OSError(f"round-trip differs: {name}")
    print(json.dumps({"draft_sha256": draft_sha, "spec_sha256": spec_sha,
                      "function_sha256": function_sha,
                      "created": {name: sha(data) for name, data in files.items()}}, indent=2))


if __name__ == "__main__":
    main()
