"""One preregistered finite collision campaign; no scientific original imported."""
from pathlib import Path
import ast
import datetime
import hashlib
import importlib.util
import json
import math
import sys
import time
import traceback

BASE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def write_new(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)


def main():
    freeze = json.loads((BASE / "FREEZE_R66.json").read_text(encoding="utf-8"))
    for item in freeze["files"]:
        if pin(item["path"])["sha256"] != item["sha256"]:
            raise ValueError("Frozen bytes changed: " + item["path"])
    review = json.loads(Path(freeze["review_path"]).read_text(encoding="utf-8"))
    if not str(review.get("status", review.get("verdict", ""))).startswith("PASS"):
        raise ValueError("Independent PASS missing")
    plan = json.loads((BASE / "PLAN_COLLISION_R66.json").read_text(encoding="utf-8"))
    for item in plan["sources"]:
        if pin(item["path"])["sha256"] != item["sha256"]:
            raise ValueError("Source changed: " + item["path"])
    start = datetime.datetime.now(datetime.timezone.utc)
    if datetime.datetime.fromisoformat(freeze["created_utc"]) >= start:
        raise ValueError("Freeze must precede execution")
    write_new(BASE / "START_COLLISION_R66.json", {"started_utc": start.isoformat(), "freeze": pin(BASE / "FREEZE_R66.json")})
    timer = time.perf_counter()
    try:
        result = calculate(plan)
        result.update({"started_utc": start.isoformat(), "ended_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       "seconds": time.perf_counter() - timer, "freeze": pin(BASE / "FREEZE_R66.json")})
        write_new(BASE / "RESULT_COLLISION_R66.json", result)
        print(json.dumps({"status": result["status"], "checks": len(result["checks"]),
                          "failed": [v for v in result["checks"] if not v["passed"]],
                          "seconds": result["seconds"], "result": pin(BASE / "RESULT_COLLISION_R66.json")}))
        return 0 if result["status"].startswith("PASS") else 1
    except Exception:
        write_new(BASE / "FAILURE_COLLISION_R66.json", {"traceback": traceback.format_exc(), "seconds": time.perf_counter() - timer})
        raise


def calculate(plan):
    import numpy as np
    import scipy
    from scipy.linalg import expm
    helper = next(row["path"] for row in plan["sources"] if row["role"] == "pure_helper_R62")
    spec = importlib.util.spec_from_file_location("finite_collision_r66_reuse", helper)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    original = json.loads(Path(next(row["path"] for row in plan["sources"] if row["role"] == "R62_plan")).read_text(encoding="utf-8"))
    for row in original["source_pins"]:
        if pin(row["path"])["sha256"] != row["sha256"]:
            raise ValueError("R62 ancestor bytes changed")
    alpha_path = next(row["path"] for row in original["source_pins"] if "ALPHA_FINE_CODATA_2018" in row["role"])
    constants = {}
    for node in ast.parse(Path(alpha_path).read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in {"ALPHA_FINE_CODATA_2018", "_SEALED_ALPHA_CODATA_2018"}:
            constants[node.targets[0].id] = ast.literal_eval(node.value)
    if constants["ALPHA_FINE_CODATA_2018"] != constants["_SEALED_ALPHA_CODATA_2018"]:
        raise ValueError("Alpha pin mismatch")
    beta = constants["ALPHA_FINE_CODATA_2018"] * math.sqrt(math.e)
    m = original["model"]["parameters"]
    checks = []
    def norm(a): return float(np.linalg.norm(a, ord="fro"))
    def check(name, value, bound, relation="le"):
        value = float(value)
        valid = math.isfinite(value) and (value <= bound if relation == "le" else value > bound)
        checks.append({"name": name, "value": value, "bound": bound, "relation": relation, "passed": bool(valid)})
    def interval(name, value, bounds):
        check(name + "_lower", value, bounds[0], "gt")
        check(name + "_upper", value, bounds[1], "le")
    tol = plan["tolerances"]
    lower = np.array([[0, 1], [0, 0]], complex)
    ai = old.embed(lower, (0,), (2, 2, 2)); ao = old.embed(lower, (1,), (2, 2, 2))
    sm = old.embed(lower, (2,), (2, 2, 2)); sp = sm.conj().T
    Z = old.embed(np.diag([1., -1.]), (2,), (2, 2, 2))
    A = ao.conj().T @ sm; B = sp @ ai; J = A + B
    h_base = m["omega_c"] * (ai.conj().T @ ai + ao.conj().T @ ao) + m["omega_OH"] * sp @ sm
    h_base += m["g_JC"] * (ai.conj().T @ sm + sp @ ai)
    drive = m["Omega"] * (sp + sm)
    h_full = h_base + drive
    gamma_Lambda = plan["model"]["gamma_Lambda"]
    lam = beta * gamma_Lambda
    rates = [m["kappa_in"], m["kappa_out"], m["gamma_OH"], m["gamma_dephasing"], lam]
    if not all(math.isfinite(v) and v > 0 for v in rates): raise ValueError("All five rates must stay positive")
    if not m["g_JC"] > 0 or not m["Omega"] > 0: raise ValueError("Coupling/pump must stay positive")
    operators = [ai, ao, sm, Z, J]
    collapses = [math.sqrt(r) * op for r, op in zip(rates, operators)]
    alpha = 1j * m["Omega"] / math.sqrt(m["gamma_OH"])
    derived_drive = 1j * (alpha.conjugate() * collapses[2] - alpha * collapses[2].conj().T)
    check("coherent_drive_sign_and_factor", norm(derived_drive - drive), tol["matrix"])
    gen = old.liouvillian(h_full, list(zip(rates, operators)))
    check("collapse_vs_rate_generator", norm(gen - old.liouvillian(h_full, [(1., op) for op in collapses])), tol["matrix"])
    rho0 = np.kron(old.projector(np.array([1., 0., 0., .5], complex) / math.sqrt(1.25)), np.eye(2) / 2)
    check("generator_direct_reuse", norm(old.unvec(gen @ old.vec(rho0), 8) - old.direct_generator(h_full, list(zip(rates, operators)), rho0)), tol["matrix"])
    T = plan["model"]["T"]
    target = expm(T * gen)
    gen_norm = norm(gen); target_norm = norm(target)
    id_super = np.eye(64, dtype=complex)

    def collision(h, delta, coherent_alpha, tag, epsilon_sign=1):
        d = 8; q = 6
        V = np.zeros((d*q, d*q), complex)
        for j, collapse in enumerate(collapses, start=1):
            e = np.zeros((q, q), complex); e[j, 0] = 1
            V += np.kron(collapse, e) - np.kron(collapse.conj().T, e.conj().T)
        eps = epsilon_sign * math.sqrt(delta)
        exponent = eps * V - 1j * delta * np.kron(h, np.eye(q))
        U = expm(exponent)
        b = np.zeros(q, complex); b[0] = 1.; b[3] = eps * coherent_alpha
        b /= np.linalg.norm(b)
        ks = np.einsum("ajbe,e->jab", U.reshape(d, q, d, q), b)
        channel = sum(np.kron(k.conj(), k) for k in ks)
        completeness = sum(k.conj().T @ k for k in ks)
        choi = sum(np.outer(old.vec(k), old.vec(k).conj()) for k in ks)
        check(tag + "_antihermitian_exponent", norm(exponent + exponent.conj().T), tol["matrix"])
        check(tag + "_unitary", norm(U.conj().T @ U - np.eye(d*q)), tol["cptp"])
        check(tag + "_Kraus_TP", norm(completeness - np.eye(d)), tol["cptp"])
        check(tag + "_Choi_CP", max(0., -float(np.linalg.eigvalsh((choi + choi.conj().T) / 2).min())), tol["cptp"])
        check(tag + "_Choi_trace", abs(np.trace(choi) - d), tol["cptp"])
        return channel

    results = {}
    for branch, H, reservoir_alpha in [("coherent_OH_hbase", h_base, alpha), ("vacuum_explicit_drive", h_full, 0j)]:
        rows = []
        for index, N in enumerate(plan["steps_N"]):
            delta = T / N
            phi = collision(H, delta, reservoir_alpha, branch + "_N" + str(N))
            if index == 0:
                negative_epsilon = collision(H, delta, reservoir_alpha, branch + "_parity", epsilon_sign=-1)
                check(branch + "_joint_parity", norm(phi - negative_epsilon), tol["matrix"])
            step_target = expm(delta * gen)
            total = np.linalg.matrix_power(phi, N)
            local = norm(phi - step_target)
            global_error = norm(total - target)
            derivative = norm((phi - id_super) / delta - gen)
            final = old.unvec(total @ old.vec(rho0), 8)
            check(branch + "_rho_trace_N" + str(N), abs(np.trace(final) - 1), tol["state"])
            check(branch + "_rho_hermitian_N" + str(N), norm(final - final.conj().T), tol["state"])
            check(branch + "_rho_positive_N" + str(N), max(0., -float(np.linalg.eigvalsh((final + final.conj().T) / 2).min())), tol["state"])
            rows.append({"N": N, "delta": delta, "local_channel_error_F": local,
                         "global_error_F": global_error, "global_relative_error_F": global_error/target_norm,
                         "generator_derivative_error_F": derivative, "generator_derivative_relative_F": derivative/gen_norm})
        for k in range(len(rows)-2, len(rows)):
            older, newer = rows[k-1], rows[k]
            interval(branch + "_local_order_N" + str(newer["N"]), older["local_channel_error_F"]/newer["local_channel_error_F"], plan["convergence"]["local_ratio"])
            interval(branch + "_global_order_N" + str(newer["N"]), older["global_error_F"]/newer["global_error_F"], plan["convergence"]["global_ratio"])
            interval(branch + "_derivative_order_N" + str(newer["N"]), older["generator_derivative_error_F"]/newer["generator_derivative_error_F"], plan["convergence"]["global_ratio"])
        check(branch + "_global_finest", rows[-1]["global_relative_error_F"], plan["convergence"]["global_relative_max"])
        check(branch + "_derivative_finest", rows[-1]["generator_derivative_relative_F"], plan["convergence"]["derivative_relative_max"])
        results[branch] = rows

    conventional = list(zip(rates[:4], operators[:4]))
    split_gen = old.liouvillian(h_full, conventional + [(lam, A), (lam, B)])
    no_drive_gen = old.liouvillian(h_base, list(zip(rates, operators)))
    opposite_phase_gen = old.liouvillian(h_base - drive, list(zip(rates, operators)))
    witness = np.zeros(8, complex); witness[1] = 1/math.sqrt(2); witness[4] = 1/math.sqrt(2)
    w = old.projector(witness)
    cross = A @ w @ B.conj().T + B @ w @ A.conj().T
    check("split_bath_cross_identity", norm(old.unvec((gen-split_gen) @ old.vec(w),8) - lam*cross), tol["matrix"])
    check("negative_separate_bath_witness", norm(lam*cross), plan["negative_threshold"], "gt")
    negatives = {}
    for name, wrong in [("separated_A_B", split_gen), ("pump_absent", no_drive_gen), ("pump_phase_opposite", opposite_phase_gen)]:
        difference = norm(gen-wrong); end_difference = norm(target-expm(T*wrong))
        check("negative_"+name+"_generator", difference, plan["negative_threshold"], "gt")
        check("negative_"+name+"_final_channel", end_difference, plan["negative_threshold"], "gt")
        negatives[name] = {"generator_distance_F": difference, "final_channel_distance_F": end_difference}
    return {"status": "PASS_FINITE_RESERVOIR_COMPONENT" if all(c["passed"] for c in checks) else "FAIL_FINITE_RESERVOIR_COMPONENT",
            "checks": checks, "branches": results, "negative_controls": negatives,
            "model": {"parameters_reused": m, "beta_runtime": beta, "gamma_Lambda_INPUT": gamma_Lambda,
                      "lambda_holo": lam, "coherent_alpha": {"re": alpha.real,"im": alpha.imag},
                      "system_dimension": 8, "ancilla_dimension": 6, "unitary_dimension": 48,
                      "all_five_rates": rates, "time_T_INPUT": T},
            "versions": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__},
            "limits": ["Finite 0/1 per optical mode, not total-excitation cutoff or infinite bosonic system.",
                       "Coherent-bin ancilla approximates a continuous coherent reservoir; it is not an exact coherent state in C6.",
                       "Frobenius error measured; mathematical diamond-norm convergence is a separate bounded-operator proof.",
                       "Engineered fresh-reservoir input and external phase are explicit; no thermal Davies identification.",
                       "No device calibration, beta inference, observed data, global Lorentz net or whole R4/R5 acceptance."]}


if __name__ == "__main__":
    raise SystemExit(main())
