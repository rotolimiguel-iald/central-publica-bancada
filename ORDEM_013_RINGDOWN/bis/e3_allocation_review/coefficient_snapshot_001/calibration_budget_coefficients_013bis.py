"""Planning coefficients only; no selected allocation or calibrated nuisance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, os

B = Path(__file__).resolve().parents[1]
R = B.parent

def pin(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    gate = B / "PORTAO_DA_AMPLIACAO_V1.json"
    order = R / "TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md"
    data = json.loads(gate.read_bytes())
    rows = []
    for item in data["systematic_conditions"]:
        for sigma in (0.0497, 0.058, 0.24):
            for divisor in (5, 15):
                floor = item[f"floor{divisor}_INPUT"]
                n = (sigma / floor)**2 if floor is not None and floor > 0 else None
                row = {
                    "reading": item["reading"],
                    "sigma_injection_INPUT": sigma,
                    "floor_source": f"floor{divisor}_INPUT",
                    "floor": floor,
                    "N_per_cell_continuous_conditional": n,
                    "N_per_cell_ceiling_conditional": math.ceil(n) if n is not None else None,
                    "cells_INPUT": 10,
                    "N_ten_cells_conditional": 10 * math.ceil(n) if n is not None else None,
                    "status": "DERIVED_CONDITIONAL_PLANNING" if n is not None else "NO_FINITE_TARGET_FROM_ZERO_OR_OPEN_EFFECT",
                    "actual_injections_completed": 0,
                    "cost_per_converged_injection_hours": None,
                    "allocated_hours": None,
                }
                rows.append(row)
    value = {
        "status": "PLANNING_COEFFICIENTS_NOT_ALLOCATION_OR_SYSTEMATIC_CALIBRATION",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "code_sha256": pin(Path(__file__)),
        "gate_sha256": pin(gate),
        "order_sha256": pin(order),
        "gate_pointer": "/systematic_conditions",
        "formula": "N_cell=(sigma_injection_INPUT/floor)^2; integer ceiling per cell; multiply by ten for five SNR bins and two families",
        "assumptions": [
            "The three sigma values are illustrative inputs from order E3.2, not measurements of this pilot or injections.",
            "Equal independent unbiased uncertainty across repetitions; this assumption has not been calibrated. Noise reuse and systematic floor can invalidate inverse-square-root scaling.",
            "Ten cells are a common-sigma lower-planning scenario, not a measurement of five different SNR bins.",
            "Conditional N concerns resolution of a mean nuisance estimate; it does not certify coverage, selection normalization or a 5-sigma false-positive tail.",
            "A converged known-event pilot may inform cost but cannot establish the cost distribution or uncertainty of every injection.",
            "No reading prioritized. R-MOD retains management-conjecture status; zero/open effects do not receive an invented finite target.",
            "Binary64 is used. Astronomical counts are illustrative scales, not exact enumerable experiment designs."
        ],
        "rows": rows,
    }
    target = B / "bis/E3_CALIBRATION_BUDGET_COEFFICIENTS_V1.json"
    raw = (json.dumps(value, indent=2, allow_nan=False)+"\n").encode()
    tmp = target.with_name(target.name+".pending")
    with tmp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    if tmp.stat().st_size != len(raw): raise IOError("Incomplete output")
    os.link(tmp, target); tmp.unlink()
    print(json.dumps({"path":str(target),"sha256":pin(target),"rows":len(rows),"scope":value["status"]}))
    for row in rows:
        if row["sigma_injection_INPUT"] == 0.058 and row["floor_source"] == "floor5_INPUT" and row["reading"] in ("R-B","R-MOD","R-RAIZ-0","R-LIN"):
            print(json.dumps(row))

if __name__ == "__main__": main()
