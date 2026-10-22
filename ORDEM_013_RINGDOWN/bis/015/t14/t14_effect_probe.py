"""Check that accepted pyseobnr deviation keys alter the complex mode."""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from pyseobnr.generate_waveform import GenerateWaveform

from t14_api_probe import PARAMS, deviation_22

HERE = Path(__file__).resolve().parent
OUT = HERE / "T14_B_EFFECT_PROBE.json"


def case(extra: dict) -> tuple[np.ndarray, np.ndarray, float]:
    params = dict(PARAMS)
    params.update(extra)
    begin = time.perf_counter()
    times, modes = GenerateWaveform(params).generate_td_modes()
    return np.asarray(times), np.asarray(modes[(2, 2)]), time.perf_counter() - begin


def relative_on_overlap(t0: np.ndarray, h0: np.ndarray, t1: np.ndarray, h1: np.ndarray) -> dict:
    lo = max(float(t0[0]), float(t1[0]))
    hi = min(float(t0[-1]), float(t1[-1]))
    grid = t0[(t0 >= lo) & (t0 <= hi)]
    left = np.interp(grid, t0, h0.real) + 1j * np.interp(grid, t0, h0.imag)
    right = np.interp(grid, t1, h1.real) + 1j * np.interp(grid, t1, h1.imag)
    delta = right - left
    return {
        "overlap_samples": len(grid),
        "relative_L2_whole_overlap": float(np.linalg.norm(delta) / np.linalg.norm(left)),
        "max_absolute_difference": float(np.max(np.abs(delta))),
        "all_finite": bool(np.isfinite(left).all() and np.isfinite(right).all()),
    }


if __name__ == "__main__":
    t0, h0, cost0 = case({})
    tt, ht, costt = case({"dtau_dict": deviation_22(0.1)})
    tf, hf, costf = case({"domega_dict": deviation_22(0.1)})
    result = {
        "status": "T14_API_EFFECT_PROBE_ONLY",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_probe_sha256": hashlib.sha256((HERE / "T14_B_API_PROBE.json").read_bytes()).hexdigest(),
        "cost_seconds": {"GR": cost0, "dtau": costt, "domega": costf},
        "dtau_vs_GR": relative_on_overlap(t0, h0, tt, ht),
        "domega_vs_GR": relative_on_overlap(t0, h0, tf, hf),
        "gate_changed": False,
        "physical_confirmation": False,
    }
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    tmp.replace(OUT)
    print(json.dumps({"dtau": result["dtau_vs_GR"]["relative_L2_whole_overlap"], "domega": result["domega_vs_GR"]["relative_L2_whole_overlap"]}))
