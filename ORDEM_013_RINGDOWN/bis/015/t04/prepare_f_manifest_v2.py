"""Add the measured prior and single-mode degeneracy provenance beside F v1."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

here = Path(__file__).resolve().parent
ring = here.parents[2]
chatgpt = ring.parent
fdir = ring / "bis" / "e3_kerr_dtau_f_015"
prior_path = ring / "bis" / "015" / "E2_PE_JOBS_ALLOCATION_015_V4.json"
fisher_path = ring / "C5_FISHER_v3.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    v1_path = fdir / "MANIFEST.json"
    out_path = fdir / "MANIFEST_v2.json"
    assert not out_path.exists()
    v1 = json.loads(v1_path.read_bytes())
    prior = json.loads(prior_path.read_bytes())
    c = prior["jobs"]["GW250114_PILOT_V2_S220_C1"]["priors"]["dtau220"]
    assert (c["kind"], c["minimum"], c["maximum"]) == ("Uniform", -0.8, 2)
    assert json.loads((fdir / "CONFIG.json").read_bytes())["priors"]["dtau220"] == [-0.8, 2]
    fisher = json.loads(fisher_path.read_bytes())
    assert fisher["mass_spin_free"]["status"] == "NON_IDENTIFIABLE_SINGLE_220"
    assert v1["status"] == "PREPARED_NOT_EXECUTED_CALIBRATION_ONLY"
    v2 = dict(v1)
    v2["created_utc"] = datetime.now(timezone.utc).isoformat()
    v2["supersedes"] = "MANIFEST.json"
    v2["supersedes_sha256"] = sha(v1_path)
    v2["script_sha256"] = sha(Path(__file__).resolve())
    v2["source_and_config_pins"] = dict(v1["source_and_config_pins"])
    for path in (prior_path, fisher_path):
        v2["source_and_config_pins"][path.relative_to(chatgpt).as_posix()] = sha(path)
    v2["provenance_added_v2"] = {
        "dtau220_prior": "GW250114_PILOT_V2_S220_C1 Uniform[-0.8,2] in E2 allocation V4",
        "single_mode_free_Mf_af": "C5_FISHER_v3 mass_spin_free NON_IDENTIFIABLE_SINGLE_220",
        "scope": "diagnostic only; no posterior z/sigma or gate movement",
    }
    data = (json.dumps(v2, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with out_path.open("xb") as out:
        out.write(data)
        out.flush()
        os.fsync(out.fileno())
    assert out_path.read_bytes() == data
    print(json.dumps({"status": "F_MANIFEST_V2_PREPARED", "sha256": sha(out_path),
                      "supersedes_sha256": v2["supersedes_sha256"],
                      "source_pin_count": len(v2["source_and_config_pins"])}))


if __name__ == "__main__":
    main()
