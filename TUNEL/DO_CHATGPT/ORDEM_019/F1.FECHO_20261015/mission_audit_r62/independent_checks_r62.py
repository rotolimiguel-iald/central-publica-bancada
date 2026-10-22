"""Independent focal algebra/receipt checks; no evolution or constructor import."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import math
import numpy as np

BASE = Path(__file__).resolve().parent


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest()}


def main():
    records = []

    def check(name, condition, detail=None):
        records.append({"name": name, "passed": bool(condition), "detail": detail})
        assert condition, name

    def close(name, left, right):
        err = float(np.max(np.abs(np.asarray(left) - np.asarray(right))))
        check(name, err < 1e-12, {"max_abs_error": err})

    plan = read(BASE / "PREPARED_READOUT_PLAN_R62.json")
    delivery = read(BASE / "DELIVERY_READOUT_R62.json")
    freeze = read(BASE / "FREEZE_READOUT_R62.json")
    result = read(BASE / "run_r62/RESULT_R62.json")
    summary = read(BASE / "READOUT_SUMMARY_R62.json")
    pins = delivery["artifacts"] + plan["source_pins"] + freeze["files"]
    check("all_26_delivery_plan_freeze_pin_occurrences", all(pin(p["path"])["sha256"] == p["sha256"] for p in pins), len(pins))
    check("freeze_precedes_start", datetime.datetime.fromisoformat(freeze["created_utc"]) < datetime.datetime.fromisoformat(result["started_utc"]))
    check("one_result_exit0", delivery["execution"]["observed_exit_code"] == 0 and result["status"] == "PASS_FINITE_SYNTHETIC_READOUT")
    original = Path(plan["source_pins"][0]["path"])
    defs = {n.name: n for n in ast.parse(original.read_text(encoding="utf-8")).body if isinstance(n, ast.FunctionDef)}
    extracted = {n.name: n for n in ast.parse((BASE / "finite_device_functions_r62.py").read_text(encoding="utf-8")).body if isinstance(n, ast.FunctionDef)}
    check("nine_AST_functions_identical", len(extracted) == 9 and all(ast.dump(defs[k]) == ast.dump(v) for k, v in extracted.items()))
    r1 = (BASE / "run_prepared_readout_r62.py").read_text(encoding="utf-8")
    r2 = (BASE / "run_prepared_readout_r62_r2.py").read_text(encoding="utf-8")
    check("runner_R2_changes_only_review_and_own_name", r1.replace("PREEXEC_REVIEW_R62.json", "ROOT_PREEXEC_REVIEW_R62.json").replace("run_prepared_readout_r62.py", "run_prepared_readout_r62_r2.py") == r2)
    check("579_logged_relations_consistent", len(result["checks"]) == 579 and all(c["passed"] and math.isfinite(c["value"]) and (c["value"] <= c["bound"] if c["relation"] == "le" else c["value"] > c["bound"]) for c in result["checks"]))
    check("30_rows_expected_cartesian_product", len(result["rows"]) == 30 and len({(r["state"], r["time"]) for r in result["rows"]}) == 30)
    maxima = {prefix: max(c["value"] for c in result["checks"] if c["name"].startswith(prefix)) for prefix in summary["maximum_absolute_residuals"]}
    check("summary_maxima_match_record", maxima == summary["maximum_absolute_residuals"])

    # Fresh matrices and tensor convention, not imported from the builder.
    low = np.array([[0, 1], [0, 0]], dtype=complex)
    ident = np.eye(2)
    z = np.diag([1, -1])
    tensor = lambda x, y, w: np.kron(np.kron(x, y), w)
    ai, ao, sm = tensor(low, ident, ident), tensor(ident, low, ident), tensor(ident, ident, low)
    sp, Zi, Zoh = sm.conj().T, tensor(z, ident, ident), tensor(ident, ident, z)
    xi, xo = (ai + ai.conj().T) / math.sqrt(2), (ao + ao.conj().T) / math.sqrt(2)
    pi, po = -1j * (ai - ai.conj().T) / math.sqrt(2), -1j * (ao - ao.conj().T) / math.sqrt(2)
    C, B = ai @ ao, ai.conj().T @ ao
    close("C_operator_decoder", (xi @ xo - pi @ po + 1j * (xi @ po + pi @ xo)) / 2, C)
    close("B_operator_decoder", (xi @ xo + pi @ po + 1j * (xi @ po - pi @ xo)) / 2, B)
    for name, u, v in [("XX", xi, xo), ("PP", pi, po), ("XP", xi, po), ("PX", pi, xo)]:
        close("quadratic_operator_" + name, (u + v) @ (u + v) - (u - v) @ (u - v), 4 * u @ v)
    close("finite_CCR_is_Z", ai @ ai.conj().T - ai.conj().T @ ai, Zi)
    d = result["parameters"]
    lam = result["lambda_runtime"]
    h = d["omega_c"] * (ai.conj().T @ ai + ao.conj().T @ ao) + d["omega_OH"] * (sp @ sm)
    h = h + d["g_JC"] * (ai.conj().T @ sm + sp @ ai) + d["Omega"] * (sp + sm)
    jumps = [(d["kappa_in"], ai), (d["kappa_out"], ao), (d["gamma_OH"], sm), (d["gamma_dephasing"], Zoh), (lam, ao.conj().T @ sm + sp @ ai)]

    def adjoint(observable):
        ans = 1j * (h @ observable - observable @ h)
        for rate, j in jumps:
            jj = j.conj().T @ j
            ans = ans + rate * (j.conj().T @ observable @ j - (jj @ observable + observable @ jj) / 2)
        return ans

    D = tensor(z, low + low.conj().T, low + low.conj().T)
    for name, sign in [("rho_plus", 1), ("rho_minus", -1)]:
        rho = (np.eye(8) + sign * D / 2) / 8
        close(name + "_C_derivative", np.trace(rho @ adjoint(C)), -sign * 1j * d["g_JC"] / 8)
        close(name + "_B_derivative", np.trace(rho @ adjoint(B)), sign * 1j * d["g_JC"] / 8)
    for name, obs, expected in [("pair_phi0", C, .4), ("pair_phiPi2", C, .4j), ("relative_phi0", B, .5), ("relative_phiPi2", B, .5j)]:
        row = next(r for r in result["rows"] if r["state"] == name and r["time"] == 0)
        key = "C_direct" if name.startswith("pair") else "B_direct"
        close(name + "_analytic_initial_value", complex(row[key]["re"], row[key]["im"]), expected)
    check("zero_signal_phase_undefined", all(row[phase]["value"] is None and row[phase]["status"] == "PHASE_UNDEFINED_LOW_MODULUS" for row in result["rows"] if row["time"] == 0 and row["state"] in {"rho_plus", "rho_minus"} for phase in ("phase_C", "phase_B")))
    row = next(r for r in result["rows"] if r["state"] == "pair_phi0" and r["time"] == 0)
    check("nonzero_signal_zero_phase_is_valid", row["phase_C"]["value"] == 0 and row["phase_C"]["status"] == "DEFINED_SYNTHETIC_PHASE")
    check("all_four_negative_controls_rejected", len(summary["negative_controls"]) == 4 and all(v["passed"] and v["value"] > 1e-6 for v in summary["negative_controls"]))
    own = {"status": "PASS_FOCAL_INDEPENDENT_CHECKS", "reviewer": "codex-mission-memory-review", "script": pin(__file__), "checks": records, "count": len(records), "scope": "Fresh operator algebra, initial adjoint/analytic controls and receipt consistency. No expm, trajectory campaign, constructor import or remote call.", "builder_check_count": 579, "builder_checks_independently_reexecuted": False}
    with (BASE / "INDEPENDENT_CHECKS_R62.json").open("x", encoding="utf-8") as f:
        json.dump(own, f, ensure_ascii=False, indent=2)
    print(json.dumps({"status": own["status"], "checks": len(records), "output": pin(BASE / "INDEPENDENT_CHECKS_R62.json")}))


if __name__ == "__main__":
    main()
