"""Bounded pyseobnr API/timing probe; no inference or physical verdict."""

from __future__ import annotations

import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from pyseobnr.generate_waveform import GenerateWaveform


HERE = Path(__file__).resolve().parent
OUT = HERE / "T14_B_API_PROBE.json"
PARAMS = {
    "mass1": 50.0,
    "mass2": 30.0,
    "spin1x": 0.0,
    "spin1y": 0.0,
    "spin1z": 0.5,
    "spin2x": 0.0,
    "spin2y": 0.0,
    "spin2z": 0.8,
    "distance": 1000.0,
    "inclination": math.pi / 3,
    "phi_ref": 0.0,
    "f22_start": 20.0,
    "f_ref": 20.0,
    "f_max": 2048.0,
    "deltaT": 1.0 / 4096.0,
    "deltaF": 1.0 / 16.0,
    "approximant": "SEOBNRv5PHM",
    "ModeArray": [(2, 2), (4, 4)],
}
DEVIATION_KEYS = ("2,2", "2,1", "3,3", "3,2", "4,4", "4,3", "5,5")


def deviation_22(value: float) -> dict[str, float]:
    return {key: value if key == "2,2" else 0.0 for key in DEVIATION_KEYS}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(label: str, extra: dict) -> dict:
    params = dict(PARAMS)
    params.update(extra)
    start = time.perf_counter()
    try:
        times, modes = GenerateWaveform(params).generate_td_modes()
        seconds = time.perf_counter() - start
        result = {
            "label": label,
            "status": "FINITE_WAVEFORM",
            "wall_seconds": seconds,
            "samples": len(times),
            "mode_keys": [str(k) for k in modes],
            "time_first": float(times[0]),
            "time_last": float(times[-1]),
            "mode_norms": {},
        }
        for key, values in modes.items():
            arr = np.asarray(values)
            if not np.isfinite(arr).all():
                raise ValueError(f"nonfinite mode {key}")
            result["mode_norms"][str(key)] = float(np.linalg.norm(arr))
        if not np.isfinite(np.asarray(times)).all():
            raise ValueError("nonfinite time grid")
        return result
    except Exception as exc:
        return {
            "label": label,
            "status": "API_FAILURE",
            "wall_seconds": time.perf_counter() - start,
            "error_type": type(exc).__name__,
            "error": str(exc)[:2000],
        }


if __name__ == "__main__":
    cases = [
        run_case("GR", {}),
        run_case("DTAU_22_0P1", {"dtau_dict": deviation_22(0.1)}),
        run_case("DOMEGA_22_0P1", {"domega_dict": deviation_22(0.1)}),
    ]
    payload = {
        "status": "API_PROBE_ONLY",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_api": "https://waveforms.docs.ligo.org/software/pyseobnr/source/notebooks/pseob_example.html",
        "script_sha256": sha(Path(__file__)),
        "parameter_scope": "official example parameters, two selected modes, not a GW250114 PE",
        "cases": cases,
        "gate_changed": False,
        "physical_confirmation": False,
    }
    temporary = OUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(OUT)
    print(json.dumps({"cases": [(c["label"], c["status"], c["wall_seconds"]) for c in cases], "out": str(OUT)}))
