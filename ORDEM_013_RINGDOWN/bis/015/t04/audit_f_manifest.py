"""Read-only integrity and budget audit before any F authorization."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHATGPT = RING.parent
F = RING / "bis" / "e3_kerr_dtau_f_015"
OLD = RING / "bis" / "e3_kerr_continuation"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    m = json.loads((F / "MANIFEST.json").read_bytes())
    cfg = json.loads((F / "CONFIG.json").read_bytes())
    b = json.loads((RING / "ORCAMENTO_015_v5.json").read_bytes())
    assert m["parent_manifest_sha256"] == sha(OLD / "MANIFEST.json")
    assert m["status"] == "PREPARED_NOT_EXECUTED_CALIBRATION_ONLY"
    assert set(m["code_sha256"]) == {p.name for p in F.glob("*.py")}
    for name,pin in m["code_sha256"].items():
        assert sha(F/name) == pin, name
    for name,pin in m["source_and_config_pins"].items():
        path = (CHATGPT/name).resolve()
        assert path.is_relative_to(CHATGPT.resolve()), name
        assert sha(path) == pin, name
    for name in ("conditioning.py","controller.py","custody.py"):
        assert sha(F/name) == sha(OLD/name)
    assert set(cfg["priors"]) == {"psi","Mf","af","cosiota","A2220_1","A2220_2",
                                  "phi2220_1","phi2220_2","dtau220"}
    assert cfg["priors"]["dtau220"][0] > -1
    assert cfg["output_relative_to_Chatgpt"] == "ORDEM_013_RINGDOWN/cache/E3_KERR220_DTAU_F_015"
    assert not (CHATGPT/cfg["output_relative_to_Chatgpt"]).exists()
    f = next(x for x in b["items"] if x["item"] == "T04_branch_F")
    assert f["job_started"] is False and f["allocated_machine_hours"] > cfg["wall_envelope_seconds"]/3600
    assert b["accounting"]["machine_hours_spent"] < b["authorized_machine_hours"]
    print(json.dumps(dict(status="F_MANIFEST_READ_ONLY_AUDIT_PASS_NOT_AUTHORIZED_OR_LAUNCHED",
                          manifest_sha256=sha(F/"MANIFEST.json"),
                          code_files=len(m["code_sha256"]),source_pins=len(m["source_and_config_pins"]),
                          F_reserved_hours=f["allocated_machine_hours"])))


if __name__ == "__main__":
    main()
