"""Bind copied Kerr-dtau code/config to a new, reviewable Part-015 manifest."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHATGPT = RING.parent
OLD = RING / "bis" / "e3_kerr_continuation" / "MANIFEST.json"
NEW = RING / "bis" / "e3_kerr_dtau_f_015"
MANIFEST = NEW / "MANIFEST.json"
SOURCE_NAMES = ("conditioning.py", "controller.py", "custody.py", "kerr_model.py", "runner.py")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    original = json.loads(OLD.read_bytes())
    copied = MANIFEST.read_bytes()
    assert copied == OLD.read_bytes(), "Copied base manifest drifted before first F version"
    assert not (NEW / "MANIFEST_F_PREPARED.json").exists()
    cfg = json.loads((NEW / "CONFIG.json").read_bytes())
    assert cfg["priors"]["dtau220"] == [-0.8, 2.0]
    assert cfg["output_relative_to_Chatgpt"] == "ORDEM_013_RINGDOWN/cache/E3_KERR220_DTAU_F_015"
    assert cfg["budget_path"] == "ORDEM_013_RINGDOWN/bis/PART_015_BUDGET_START.json"
    assert cfg["wall_envelope_seconds"] == 7200 and cfg["variant_wall_seconds"]["public_psd"] == 6800
    assert cfg["variants"] == ["public_psd"]
    start = json.loads((RING / "bis" / "PART_015_BUDGET_START.json").read_bytes())
    budget = json.loads((RING / "ORCAMENTO_015_v5.json").read_bytes())
    assert budget["items"][-1]["item"] == "T04_branch_F"
    assert budget["items"][-1]["allocated_machine_hours"] > 2.0
    manifest = dict(original)
    manifest["created_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["parent_manifest_sha256"] = sha(OLD)
    manifest.pop("original_envelope_stop_utc", None)
    manifest["part015_hard_deadline_utc"] = start["hard_deadline_utc"]
    manifest["reason"] = "ORDEM015 T04-F after measured C maxcall partial; diagnostic Kerr V2 + dtau220 on GW250114"
    manifest["changes"] = {
        "kerr_model.py": "Ninth parameter dtau220 scales only 220 damping tau by 1+dtau220 in polarizations",
        "runner.py": "Unique sampler labels and explicit single-mode free-Mf-af no-sigma marker",
        "CONFIG.json": "Same data, PSD and baseline eight priors; ninth prior [-0.8,2] inherited from C; unique seed/output; Part015 clock; 2h envelope",
    }
    manifest["unchanged"] = "Kerr frequency, harmonics, phases, H1/L1 geometry, covariance, likelihood, data and PSD inputs"
    manifest["wall_contract"] = "2h own-controller hard envelope; 6800s public_psd variant; under T04-F v5 reserve; Part015 absolute deadline"
    manifest["cost_projection_INPUT"] = {
        "baseline_kerr_v2_runner_wall_seconds": 638.337946532,
        "new_ninth_parameter_cost": "OPEN_MEASURE_IN_F",
        "convergence_forecast": "NONE",
    }
    manifest["script_sha256"] = sha(Path(__file__).resolve())
    manifest["code_sha256"] = {name: sha(NEW / name) for name in SOURCE_NAMES}
    pins = dict(manifest["source_and_config_pins"])
    for path in (NEW / "CONFIG.json", RING / "bis" / "PART_015_BUDGET_START.json",
                 RING / "ORCAMENTO_015_v5.json",
                 CHATGPT / "TUNEL" / "PARA_CHATGPT" / "ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md"):
        pins[path.relative_to(CHATGPT).as_posix()] = sha(path)
    manifest["source_and_config_pins"] = pins
    data = (json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    backup = NEW / "MANIFEST_F_PREPARED.json"
    with backup.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert backup.read_bytes() == data
    # Preserve the copied v2 manifest in its dated byte backup, then atomically replace the copy.
    assert list(NEW.glob("MANIFEST.json.bak_*"))
    temp = NEW / "MANIFEST.json.pending_f"
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.stat().st_size == len(data)
    os.replace(temp, MANIFEST)
    assert MANIFEST.read_bytes() == data
    print(json.dumps(dict(status="F_MANIFEST_PREPARED_NOT_AUTHORIZED_OR_EXECUTED",
                          sha256=sha(MANIFEST),code_sha256=manifest["code_sha256"],
                          config_sha256=sha(NEW / "CONFIG.json"),
                          source_pin_count=len(pins))))


if __name__ == "__main__":
    main()
