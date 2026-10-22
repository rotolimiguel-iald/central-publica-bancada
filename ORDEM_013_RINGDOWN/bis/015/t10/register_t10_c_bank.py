"""Append the preregistered T10-C injection bank to the existing V1.1 chain."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHAT = RING.parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def new(path, raw):
    with Path(path).open("xb") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())


def main():
    parent = RING / "RINGDOWN_5SIGMA_V1_1_2.json"
    assert sha(parent) == "a02c4224b0c832a85e8eaef736197754235aa573290760bb2307ad6ac4c713b4"
    control = RING / "C5_IMR_CONTROLS.json"
    script = RING / "prepare_imr_controls.py"
    assert sha(control) == "1fe989525c3c9cff7059caa748eea541f94d01f9d416840117072c1f094fe2c1"
    assert sha(script) == "5139864946af88ee0f4f3c52f85edba0acd690ab1249489068bb4677004f3e19"
    prior = json.loads(parent.read_bytes())
    plan = {
        "status": "T10_C_PRE_REGISTERED_NOT_STARTED",
        "registered_utc": datetime.now(timezone.utc).isoformat(),
        "parent_registration_sha256": sha(parent),
        "C5_control_sha256": sha(control),
        "C5_generator_sha256": sha(script),
        "purpose": "Generate a new two-family GR injection bank; no deformation, PE, sigma(c), or gate claim",
        "family_order": ["SEOBNRv4HM", "IMRPhenomXPHM"],
        "snr_bin_order": [19.1, 17.0, 15.0, 13.0, 12.0],
        "sources_by_bin": [
            {"mass1": 39.0, "mass2": 33.0, "spin1z": .05, "spin2z": -.03},
            {"mass1": 37.0, "mass2": 34.0, "spin1z": .02, "spin2z": -.04},
            {"mass1": 42.0, "mass2": 31.0, "spin1z": .08, "spin2z": .01},
            {"mass1": 35.0, "mass2": 30.0, "spin1z": -.02, "spin2z": .04},
            {"mass1": 40.0, "mass2": 35.0, "spin1z": .01, "spin2z": -.01}
        ],
        "noise_seed_formula": "15260430 + 10*bin_index + family_index",
        "detectors": ["H1", "L1"],
        "noise": "Synthetic Gaussian colored by the pinned public PSD; not real off-source noise",
        "waveforms": "Fresh LAL/PyCBC time-domain waveforms for each parameter set; isolate 22 only to define peak, then retain full modes; aligned-spin representatives",
        "stop": "Exactly 10 waveform/noise cells in the stated order, or first failure; 1 hour machine hard cap; do not cherry-pick cells",
        "scope": "C bank creation only; no injection recovery or sigma(c) from waveform generation"
    }
    prior["t10_bank_v1_1_3"] = plan
    # Do not change the statistical registry, tested candidates, or their roles.
    target = RING / "RINGDOWN_5SIGMA_V1_1_3.json"
    new(target, (json.dumps(prior, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())
    witness = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_E2_REGISTRO_V1_1_3.md"
    content = ("[INPUT — T10-C, banco sintético pré-registrado; nenhum gate movido]\n\n"
               f"supersedes RINGDOWN_5SIGMA_V1_1_2.json sha256 {sha(parent)}\n"
               f"registered_utc: {plan['registered_utc']}\n"
               f"registro_sha256: {sha(target)}\n\n"
               "A subemenda acrescenta somente `t10_bank_v1_1_3`: 5 bins de SNR × 2 famílias GR, "
               "sementes e critério de parada fixados antes da primeira geração. "
               "O banco é controle sintético colorido pela PSD pública; não fornece σ(c), PE ou leitura física.\n"
               "Axiomas: N/A — sem Lean.\n")
    new(witness, content.encode())
    print(json.dumps({"registry_sha256": sha(target), "witness_sha256": sha(witness),
                      "registered_utc": plan["registered_utc"]}))


if __name__ == "__main__":
    main()
