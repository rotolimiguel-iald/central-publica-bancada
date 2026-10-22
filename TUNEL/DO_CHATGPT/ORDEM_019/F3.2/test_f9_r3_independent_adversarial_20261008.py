"""Independent R3 probes using temporary documentary copies and synthetic data only.

No observed reader values are opened. The pinned source files are read solely to
validate the copied binding, and original R2/R3 artifacts remain unchanged.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile

import f9_reader_gate_v1x_r3 as gate
import f9_runner_v1x_preflight_r3 as preflight
import f9_runner_v1x_staged_r3 as staged


HERE = Path(__file__).resolve().parent
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R3_20261008.json"
FIXTURE = HERE / "FIXTURE_SINTETICO_V1X_R3_20261008.json"
SOURCE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def spec_sha(spec: dict) -> str:
    return sha(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def checked(binding_path: Path, expected_spec_sha256: str) -> dict:
    return gate.verify_v1x_binding(
        binding_path,
        expected_binding_sha256=sha(binding_path.read_bytes()),
        allowed_source_root=SOURCE_ROOT,
        expected_spec_sha256=expected_spec_sha256,
    )


def expect_refusal(binding_path: Path, expected_spec_sha256: str, label: str) -> str:
    try:
        checked(binding_path, expected_spec_sha256)
    except gate.ReaderGateError as exc:
        return f"{label}: REFUSED ({exc})"
    raise AssertionError(f"{label}: gate accepted adversarial binding")


def save_variant(temp: Path, binding: dict, draft: dict) -> tuple[Path, str]:
    current_spec_sha = spec_sha(draft["spec"])
    draft["spec_sha256"] = current_spec_sha
    draft_path = temp / "draft_variant.json"
    draft_raw = json_bytes(draft)
    draft_path.write_bytes(draft_raw)
    binding["draft_v2"] = {"path": str(draft_path), "bytes": len(draft_raw), "sha256": sha(draft_raw)}
    binding["spec_sha256"] = current_spec_sha
    binding_path = temp / "binding_variant.json"
    binding_path.write_bytes(json_bytes(binding))
    return binding_path, current_spec_sha


def coherent_side_swap(reader_id: str) -> str:
    with tempfile.TemporaryDirectory(prefix="f9_r3_side_swap_") as directory:
        temp = Path(directory)
        binding = json.loads(BINDING.read_text(encoding="utf-8"))
        draft = json.loads(Path(binding["draft_v2"]["path"]).read_text(encoding="utf-8"))
        record = next(record for record in binding["readers"] if record["reader_id"] == reader_id)
        record["sigma_published_components"].reverse()
        record["numeric_windows"]["sigma_components"].reverse()
        sides = record["asymmetric_sigma"]
        sides["plus"], sides["minus"] = sides["minus"], sides["plus"]
        reader = draft["spec"]["leitores"][reader_id]
        reader["sigma_plus"], reader["sigma_minus"] = reader["sigma_minus"], reader["sigma_plus"]
        record["draft_metadata"] = copy.deepcopy(reader)
        path, expected = save_variant(temp, binding, draft)
        return expect_refusal(path, expected, f"G1 {reader_id} coherent +/- exchange")


def bare_cchp_anchor() -> str:
    with tempfile.TemporaryDirectory(prefix="f9_r3_bare_anchor_") as directory:
        temp = Path(directory)
        binding = json.loads(BINDING.read_text(encoding="utf-8"))
        draft = json.loads(Path(binding["draft_v2"]["path"]).read_text(encoding="utf-8"))
        record = next(record for record in binding["readers"] if record["reader_id"] == "L2_cchp")
        record["numeric_windows"]["sigma_components"][1]["literal"] = "1.33"
        path, expected = save_variant(temp, binding, draft)
        return expect_refusal(path, expected, "G2 isolated 1.33 anchor")


def family_counts() -> dict[str, object]:
    binding_sha = sha(BINDING.read_bytes())
    spec = checked(BINDING, json.loads(BINDING.read_text(encoding="utf-8"))["spec_sha256"])["spec_snapshot"]
    expected_spec = spec_sha(spec)
    first = preflight.prepare_v1x(
        BINDING, expected_binding_sha256=binding_sha,
        allowed_source_root=SOURCE_ROOT, expected_spec_sha256=expected_spec,
    )
    second = staged.run_synthetic(
        BINDING, binding_sha, SOURCE_ROOT, expected_spec,
        FIXTURE, sha(FIXTURE.read_bytes()),
    )
    count = first["n_alvos_declarados"]
    if count != 2:
        raise AssertionError(f"G3 preflight count {count}, expected 2")
    if second.get("n_alvos_declarados") != count:
        raise AssertionError(f"G3 staged count {second.get('n_alvos_declarados')} != {count}")
    families = second.get("covariance_boxes", {})
    if not isinstance(families, dict):
        raise AssertionError("G3 staged families missing")
    for name in ("P_primaria", "R_r25", "S_com_sirenes"):
        if name not in families:
            raise AssertionError(f"G3 staged family {name} missing")
    return {"preflight": count, "staged": second["n_alvos_declarados"],
            "families": sorted(families),
            "primary_rule1_if_applied": second.get("primary_rule1_if_applied")}


def main() -> None:
    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    checked(BINDING, binding["spec_sha256"])
    results = ["baseline: ACCEPTED", coherent_side_swap("L4_masers_5"),
               coherent_side_swap("L5_tdcosmo"), bare_cchp_anchor()]
    print(json.dumps({"negative_tests": results, "G3": family_counts()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
