"""Exact symbolic Heisenberg calculation for the already specified finite device.

No observed data, numerical evolution, fitted parameter, or model provider.
The full pump, Jaynes-Cummings coupling and all five jump terms are retained.
The output is an exact finite-model result, not an experimental realization.
"""
from __future__ import annotations
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time

import sympy as s

ROOT = Path(__file__).resolve().parent
REFERENCE = Path(r"C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json")
ACTOR = {"id": "codex-device-clock-r57", "kind": "agent"}
CLI = r"C:\IALD\MEMORIA_IALD\mission_cli.py"


def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def new(name, obj):
    path = ROOT / name
    raw = (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    return pin(path)


def mission(request, tag):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    new(f"receipts/{tag}_{stamp}_REQUEST.json", request)
    process = subprocess.run([sys.executable, "-B", "-X", "utf8", CLI],
                             input=json.dumps(request, ensure_ascii=False).encode(), capture_output=True)
    response = json.loads(process.stdout)
    new(f"receipts/{tag}_{stamp}_RESULT.json", response)
    if not response.get("ok"):
        raise RuntimeError(response)
    return response["result"]


def preflight():
    current = mission({"operation": "project", "reference": str(REFERENCE), "max_chars": 400000}, "PROJECT")
    task = next(x for x in current["projection"]["active"] if x["id"] == "R4")
    checked = mission({"operation": "check", "reference": str(REFERENCE), "actor": ACTOR,
                       "task_id": "R4", "lease_id": task["lease"]["id"],
                       "expected_revision": current["projection"]["revision"],
                       "projection_sha256": current["projection_sha256"]}, "PREFLIGHT")
    assert checked["ready"]
    return checked


def main():
    if (ROOT / "SYMBOLIC_RESULT_R57.json").exists() or (ROOT / "RUN_START_R57.json").exists():
        raise FileExistsError("The R57 exact calculation already has an execution identity.")
    preflight()
    scope = json.loads((ROOT / "SCOPE_R57.json").read_text(encoding="utf-8"))
    for item in scope["source_pins"]:
        assert pin(item["path"]) == item, item["path"]
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    timer = time.perf_counter()
    new("RUN_START_R57.json", {"start_utc": start, "script": pin(__file__),
                              "scope": pin(ROOT / "SCOPE_R57.json"), "mode": "exact_symbolic",
                              "python": platform.python_version(), "sympy": s.__version__})

    # Same factors and lowering convention as run_finite_device.py: in, out, OH.
    eye = s.eye(2)
    lower = s.Matrix([[0, 1], [0, 0]])
    z2 = s.diag(1, -1)
    kron = s.kronecker_product
    ai, ao, sm = kron(lower, eye, eye), kron(eye, lower, eye), kron(eye, eye, lower)
    sp, Z = sm.H, kron(eye, eye, z2)
    ni, no, ne = ai.H * ai, ao.H * ao, sp * sm
    wc, w, g, Om = s.symbols("omega_c omega_OH g_JC Omega_Rabi", positive=True)
    ki, ko, gam, gp, lam = s.symbols("kappa_in kappa_out gamma_OH gamma_phi lambda_holo", positive=True)
    amp = s.Symbol("a", positive=True)
    h = wc * (ni + no) + w * ne + g * (ai.H * sm + sp * ai) + Om * (sp + sm)
    J = ao.H * sm + sp * ai
    jumps = [(ki, ai), (ko, ao), (gam, sm), (gp, Z), (lam, J)]

    def dissipator_adjoint(j, A):
        q = j.H * j
        return j.H * A * j - (q * A + A * q) / 2

    def lad(A):
        out = s.I * (h * A - A * h)
        for rate, jump in jumps:
            out += rate * dissipator_adjoint(jump, A)
        return out.applyfunc(s.expand)

    checks = []

    def zero(name, expression):
        values = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
        errors = [s.simplify(v) for v in values]
        ok = all(v == 0 for v in errors)
        checks.append({"name": name, "passed": ok, "nonzero_entries": [str(v) for v in errors if v != 0]})
        if not ok:
            raise AssertionError(name)

    zero("hamiltonian_hermitian", h - h.H)
    zero("trace_preservation_dual_identity", lad(s.eye(8)))
    holo_formula = ai.H * ao.H * sm - (ni + ao * ao.H) * sp / 2
    zero("holographic_adjoint_identity", dissipator_adjoint(J, sp) - holo_formula)
    rhs = (s.I * w - gam / 2 - 2 * gp) * sp + s.I * g * ai.H * Z + s.I * Om * Z + lam * holo_formula
    zero("complete_OH_polarization_identity", lad(sp) - rhs)
    # The pump obstruction survives with every other model term kept.
    eigen_residual = lad(sp) - s.I * w * sp
    zero("pump_diagonal_witness", eigen_residual[0, 0] - s.I * Om)

    vacuum = s.diag(1, 0)
    rho_spin = s.Matrix([[s.Rational(1, 2), amp / 2], [amp / 2, s.Rational(1, 2)]])
    rho = kron(vacuum, vacuum, rho_spin)
    z0 = s.simplify(2 * s.trace(rho * sp))
    d1 = s.simplify(2 * s.trace(rho * lad(sp)))
    d2 = s.factor(s.simplify(2 * s.trace(rho * lad(lad(sp)))))
    Gamma = gam / 2 + 2 * gp + lam / 2
    zero("density_trace_one", s.trace(rho) - 1)
    zero("spin_eigenvalue_plus", rho_spin * s.Matrix([1, 1]) - (1 + amp) / 2 * s.Matrix([1, 1]))
    zero("spin_eigenvalue_minus", rho_spin * s.Matrix([1, -1]) - (1 - amp) / 2 * s.Matrix([1, -1]))
    zero("initial_waveform_matches", z0 - amp)
    zero("initial_derivative_exact", d1 - amp * (s.I * w - Gamma))
    mismatch = s.factor(d1 - s.I * w * amp)
    # Argument derivative formulas require a>0, automatically true under the scope.
    phase_velocity = s.simplify(s.im(s.expand_complex(d1 / amp)))
    phase_acceleration = s.factor(s.simplify(s.im(s.expand_complex(d2 / amp - (d1 / amp) ** 2))))
    zero("initial_phase_rate", phase_velocity - w)

    # Same OH reduced state, different cavity preparation: no universal OH-only closure.
    rs = s.Matrix([[s.Rational(3, 4), s.Rational(1, 4)], [s.Rational(1, 4), s.Rational(1, 4)]])
    plus = s.Matrix([[s.Rational(1, 2), s.Rational(1, 2)], [s.Rational(1, 2), s.Rational(1, 2)]])
    rho_A, rho_B = kron(vacuum, vacuum, rs), kron(plus, vacuum, rs)
    shared = s.simplify(2 * s.trace(rho_A * sp))
    zero("same_reduced_signal", 2 * s.trace(rho_B * sp) - shared)
    reduction_difference = s.factor(s.simplify(2 * s.trace((rho_B - rho_A) * lad(sp))))
    zero("reduction_nonclosure_difference", reduction_difference - (s.I * g / 2 - lam / 8))

    # Actual state-to-matrix reading; amplitude is retained, not normalized away.
    x, y = s.symbols("x y", real=True)
    z = x + s.I * y
    K = s.Matrix([[0, 1], [-1, 0]])
    Pp, Pm = (s.eye(2) - s.I * K) / 2, (s.eye(2) + s.I * K) / 2
    A = z * Pp + s.conjugate(z) * Pm
    reading = s.expand(2 * (Pp * A)[0, 0])
    zero("amplitude_preserving_matrix_reader", reading - z)
    zero("amplitude_preserving_reconstruction", reading * Pp + s.conjugate(reading) * Pm - A)
    zero("rereading_idempotent", Pp * (Pp * A) - Pp * A)
    zero("singular_scale", A.H * A - (x * x + y * y) * s.eye(2))

    # The patent's G_OH is multiplicative. This fixed-boundary encoding preserves
    # the boundary splitting, unlike replacing theta_M by theta_M+omega*t.
    theta = s.Symbol("theta_M", real=True)
    Sm = s.cos(theta) * s.eye(2) + s.sin(theta) * K
    phase0 = s.cos(theta) + s.I * s.sin(theta)
    fixed_A = z * Sm
    fixed_reading = s.expand(2 * (Pp * fixed_A)[0, 0])
    recovered_scalar = s.simplify(fixed_reading * s.conjugate(phase0))
    zero("fixed_boundary_scalar_reading", fixed_reading - z * phase0)
    zero("fixed_boundary_scalar_recovery", recovered_scalar - z)
    zero("fixed_boundary_matrix_reconstruction", recovered_scalar * Sm - fixed_A)
    zero("fixed_boundary_reflected_weight", s.conjugate(fixed_A[1, 0]) * fixed_A[1, 0] - (x*x+y*y)*s.sin(theta)**2)
    zero("fixed_boundary_transmitted_weight", s.conjugate(fixed_A[0, 0]) * fixed_A[0, 0] - (x*x+y*y)*s.cos(theta)**2)
    zero("fixed_boundary_total_weight", sum(s.conjugate(fixed_A[k, 0])*fixed_A[k, 0] for k in range(2))-(x*x+y*y))

    # A constructive phase-reference route, explicitly a nonautonomous laboratory
    # drive contract rather than a silent reinterpretation of source frequencies.
    t = s.Symbol("t", real=True)
    wd = s.Symbol("omega_drive", positive=True)
    N = ni + no + ne
    R = s.diag(*[s.exp(s.I * wd * t * N[k, k]) for k in range(8)])
    Rdag = R.H
    h0 = wc * (ni + no) + w * ne + g * (ai.H * sm + sp * ai)
    h_lab = h0 + Om * (s.exp(-s.I * wd * t) * sp + s.exp(s.I * wd * t) * sm)
    h_rot = (wc - wd) * (ni + no) + (w - wd) * ne + g * (ai.H * sm + sp * ai) + Om * (sp + sm)
    zero("rotation_unitarity", R * Rdag - s.eye(8))
    zero("free_JC_total_number_covariance", N * h0 - h0 * N)
    zero("holographic_jump_total_number_covariance", N * J - J * N)
    zero("laboratory_to_rotating_generator", R * h_lab * Rdag + s.I * R.diff(t) * Rdag - h_rot)
    zero("rotating_OH_polarization_carrier", R * sp * Rdag - s.exp(s.I * wd * t) * sp)
    zero("rotating_holographic_jump", R * J * Rdag - J)
    for name, jump in [("in", ai), ("out", ao), ("OH", sm)]:
        zero("rotating_loss_phase_" + name, R * jump * Rdag - s.exp(-s.I * wd * t) * jump)
    zero("rotating_dephasing_invariant", R * Z * Rdag - Z)
    zero("loss_phase_unit_modulus", s.exp(-s.I * wd * t) * s.exp(s.I * wd * t) - 1)

    # Fixed beta is bound at runtime to the pinned canonical alpha, never fitted/literal.
    alpha_source = Path(scope["alpha_source"])
    tree = ast.parse(alpha_source.read_text(encoding="utf-8"))
    vals = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id in {"ALPHA_FINE_CODATA_2018", "_SEALED_ALPHA_CODATA_2018"}}
    assert vals["ALPHA_FINE_CODATA_2018"] == vals["_SEALED_ALPHA_CODATA_2018"]
    alpha = s.Rational(str(vals["ALPHA_FINE_CODATA_2018"]))
    beta = alpha * s.sqrt(s.E)
    assert alpha > 0
    final = {
        "statute": "REAL exact symbolic verification in the stated finite model; physical realization OPEN",
        "start_utc": start, "end_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "seconds": time.perf_counter() - timer, "mode": "exact_symbolic_no_numerical_evolution",
        "dimension": 8, "factor_order": ["in", "out", "OH"], "all_terms_retained": True,
        "parameters_assumed_strictly_positive": [str(v) for v in [wc, w, g, Om, ki, ko, gam, gp, lam]],
        "amplitude_domain": "0<a<1; a=tanh(P_MW/P_th), finite positive powers",
        "canonical_beta": {"alpha_source": pin(alpha_source), "alpha_exact_decimal_interpretation": str(alpha),
                           "runtime_expression": str(beta), "holographic_rate_binding": "lambda_holo = beta * gamma_Lambda"},
        "checks": checks,
        "formula": "Ldag(sigma+)=(i*omegaOH-gammaOH/2-2*gammaPhi)*sigma+ + i*gJC*a_in_dagger*Z + i*OmegaRabi*Z + lambda*(a_in_dagger*a_out_dagger*sigma- -(n_in+a_out*a_out_dagger)*sigma+/2)",
        "cutoff_warning": "a_out*a_out_dagger=I-n_out here; I+n_out only for untruncated CCR on a common core",
        "eigenoperator_obstruction_entry_000": str(eigen_residual[0, 0]),
        "state_counterexample": {"rho_spin": str(rho_spin), "rho_mode_in": "vacuum", "rho_mode_out": "vacuum",
                                "rho_spin_eigenvalues": [str((1 + amp) / 2), str((1 - amp) / 2)],
                                "z0": str(z0), "first_derivative": str(d1), "claimed_derivative": str(s.I * w * amp),
                                "residual": str(mismatch), "Gamma": str(Gamma), "second_derivative": str(d2),
                                "phase_velocity_at_zero": str(phase_velocity), "phase_acceleration_at_zero": str(phase_acceleration)},
        "reduction_obstruction": {"shared_OH_density": str(rs), "input_A": "vacuum", "input_B": "plus",
                                  "out_both": "vacuum", "same_initial_reading": str(shared),
                                  "derivative_B_minus_A": str(reduction_difference), "det_shared_OH": str(rs.det())},
        "OH_reading_candidate": "z(rho)=2*Tr(rho*sigma+); actual bounded polarization, not identified by decree with prescribed G_OH",
        "auxiliary_opposite_phase_map": "A(z)=z*P+ + conjugate(z)*P-; mathematically reconstructible but not the fixed-beta scalar multiplication of the patent",
        "fixed_boundary_map": {
            "source_form": "Psi_out = T_M[sqrt(abs(Psi_in))] * G_OH * exp(i theta), patent lines 474-478",
            "encoding": "A_beta(z)=z*S(thetaMiguel(beta))",
            "reading": "phaseReading(A_beta(z))=z*exp(i thetaMiguel(beta))",
            "decoder": "D_beta(w)=(w*exp(-i thetaMiguel(beta)))*S(thetaMiguel(beta))",
            "weights": "reflection=abs(z)^2*beta; transmission=abs(z)^2*(1-beta); for z!=0 their normalized proportions remain beta and 1-beta",
            "zero_amplitude": "Matrix reconstruction remains zero; normalized proportions and phase inference are undefined and must not be reported",
            "physical_scope": "A mathematically explicit encoding compatible with the scalar source structure; H/J does not thereby force z=a*exp(i omegaOH t)."
        },
        "phase_reference_construction": {
            "named_input": "LAB_PHASE_LOCKED_DRIVE: microwave drive has the explicit laboratory phases exp(+-i omega_drive t)",
            "rotation": "R(t)=exp(i omega_drive t N_total); rho_rot=R rho_lab R_dagger",
            "derived_h_rot": "(omega_c-omega_drive)*N_c+(omega_OH-omega_drive)*n_e+gJC+OmegaRabi*(sigma++sigma-)",
            "all_dissipators_preserved": "J and Z invariant; lowering jumps gain only unit-modulus phases",
            "derived_reading": "z_lab(t)=exp(i omega_drive t)*z_rot(t)",
            "stationary_consequence_scope": "If a stationary rotating preparation is later constructed, z_rot is its computed constant; it has NOT been set to tanh(P/Pth).",
            "not_source_reinterpretation": "The source constant Hamiltonian uses named absolute frequencies; the subtraction of omega_drive is additional explicit frame modeling, not a relabeling of that source."
        },
        "limits": ["Natural OH polarization is not an exact universal e^(i omegaOH t) eigenobservable.",
                   "No autonomous OH-only semigroup valid for arbitrary cavity preparation follows from tracing out modes.",
                   "No exclusion of specially prepared invariant sectors, larger justified dilations, or a separately supplied phase reference.",
                   "No physical clock calibration, root-energy origin or full bosonic generator existence is proved."]}
    result = new("SYMBOLIC_RESULT_R57.json", final)
    new("RUN_END_R57.json", {"exit_code": 0, "result": result, "script": pin(__file__),
                             "source_pins_still_valid": all(pin(x["path"]) == x for x in scope["source_pins"])})
    print(json.dumps({"result": result, "checks": len(checks), "all_passed": all(x["passed"] for x in checks),
                      "residual": str(mismatch), "phase_acceleration": str(phase_acceleration),
                      "reduction_difference": str(reduction_difference), "seconds": final["seconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
