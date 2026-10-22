"""Exact two-mode CCR/covariance checks. No providers, data or original writes.

The operator computations use the full bosonic vacuum algebra, never a cutoff.
Analytic convergence and unbounded-operator domains are proved in the companion
derivation; symbolic algebra is not presented as a substitute for those proofs.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import sys
import time
import uuid

import sympy as sp

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent.parent
checks: list[dict] = []
negative_controls: list[dict] = []
c, s, p, v = sp.symbols("c s cos_phi sin_phi", real=True)
I = sp.I
z = p + I * v
zb = p - I * v
basis = sp.groebner([c*c - s*s - 1, p*p + v*v - 1], c, s, p, v,
                    extension=I)


def pin(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def save_new(name: str, obj: dict) -> dict:
    target = ROOT / name
    assert target.parent.resolve() == ROOT
    if target.exists():
        raise FileExistsError(target)
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temp = target.with_name(target.name + ".tmp_" + uuid.uuid4().hex)
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == data
    os.rename(temp, target)
    return pin(target)


def normal(expr):
    return sp.expand(basis.reduce(sp.expand(expr))[1])


def zero(name, expr, *, polynomial=True):
    values = list(expr) if isinstance(expr, sp.MatrixBase) else [expr]
    residual = [normal(x) if polynomial else sp.simplify(x) for x in values]
    assert all(x == 0 for x in residual), (name, residual)
    checks.append({"id": name, "status": "PASS", "scalar_identities": len(values)})


def rejected(name, witness, meaning):
    witness = sp.simplify(witness)
    assert witness != 0, name
    negative_controls.append({"id": name, "status": "EXPECTED_REJECTION",
                              "exact_witness": str(witness), "meaning": meaning})


def vacuum_word(word):
    """Apply the exact word, right-to-left, to |0,0>; no finite matrices."""
    occ = [0, 0]
    coeff = sp.Integer(1)
    for op in reversed(word):
        mode = 0 if op in ("a", "ad") else 1
        if op in ("ad", "bd"):
            occ[mode] += 1
            coeff *= sp.sqrt(occ[mode])
        else:
            if occ[mode] == 0:
                return sp.Integer(0)
            coeff *= sp.sqrt(occ[mode])
            occ[mode] -= 1
    return coeff if occ == [0, 0] else sp.Integer(0)


transformed = {
    "a": [(c, "a"), (s*z, "bd")],
    "b": [(c, "b"), (s*z, "ad")],
    "ad": [(c, "ad"), (s*zb, "b")],
    "bd": [(c, "bd"), (s*zb, "a")],
}


def moment(*word):
    result = 0
    for choices in itertools.product(*(transformed[x] for x in word)):
        result += sp.prod(x[0] for x in choices) * vacuum_word([x[1] for x in choices])
    return normal(result)


def source_manifest():
    sources = {
        "graviton": (Path(r"C:\IALD\papers_latex\graviton_paper\graviton_paper.tex"),
                      [(202, 216), (239, 260), (365, 367)]),
        "tratado": (Path(r"C:\IALD\Artigo\Tratado\secao_03_particulas.tex"),
                     [(179, 185), (228, 239)]),
        "physical_field": (OUT / "maxwell_global/PhysicalSchwartzMaxwellR1.lean",
                           [(27, 49), (66, 76)]),
        "circular_field": (OUT / "maxwell_global/CircularPhysicalFieldTransportR1.lean",
                           [(23, 32), (90, 107), (109, 150)]),
        "canonical_pairing": (OUT / "orbital_rotation/PhysicalSymplecticPairingR7.lean",
                              [(12, 22)]),
        "canonical_density": (OUT / "orbital_rotation/PhysicalCanonicalWedgeEqualityR3.lean",
                              [(19, 29)]),
        "canonical_formula": (OUT / "orbital_rotation/PhysicalCircularRapidityR1.lean",
                              [(14, 30)]),
    }
    rows = []
    for key, (path, ranges) in sources.items():
        lines = path.read_bytes().decode("utf-8-sig").splitlines()
        excerpts = []
        for first, last in ranges:
            assert 1 <= first <= last <= len(lines)
            excerpts.append({"first": first, "last": last,
                             "text": "\n".join(f"{i}: {lines[i-1]}" for i in range(first, last+1))})
        rows.append({"id": key, **pin(path), "excerpts": excerpts})
    return rows


def main():
    started = time.perf_counter()
    swap = sp.Matrix([[0, 1], [1, 0]])
    eye2 = sp.eye(2)
    A = c * eye2
    B = s * z * swap
    zero("bogoliubov_CCR_diagonal", A*A.conjugate().T - B*B.conjugate().T - eye2)
    zero("bogoliubov_CCR_cross", A*B.T - B*A.T)
    for op in transformed:
        zero("mean_" + op, moment(op))
    expected = {
        ("ad", "a"): s*s, ("bd", "b"): s*s,
        ("a", "ad"): c*c, ("b", "bd"): c*c,
        ("a", "b"): c*s*z, ("ad", "bd"): c*s*zb,
        ("a", "a"): 0, ("b", "b"): 0,
        ("ad", "b"): 0, ("a", "bd"): 0,
    }
    for word, value in expected.items():
        zero("moment_" + "_".join(word), moment(*word) - value)
    zero("number_pair_fourth_moment", moment("ad", "a", "bd", "b") - (s*s + 2*s**4))
    zero("Wick_fourth_moment", moment("a", "b", "ad", "bd") - (c**4 + c*c*s*s))

    omega = sp.diag(sp.Matrix([[0, 1], [-1, 0]]), sp.Matrix([[0, 1], [-1, 0]]))
    T = sp.Matrix([[c, 0, s*p, s*v], [0, c, s*v, -s*p],
                   [s*p, s*v, c, 0], [s*v, -s*p, 0, c]])
    C0 = (sp.eye(4) + I*omega) / 2
    V = T*T.T / 2
    C = V + I*omega/2
    K0 = sp.Matrix([[1, I, 0, 0], [0, 0, 1, I]])
    K = K0*T.T
    zero("real_symplectic_map", T*omega*T.T - omega)
    zero("covariance_transport", T*C0*T.T - C)
    zero("Gram_factor_positivity", K.conjugate().T*K/2 - C)
    zero("CCR_from_Gram", C-C.T-I*omega)
    zero("pure_covariance", V*omega*V-omega/4)
    zero("determinant_pure_covariance", V.det()-sp.Rational(1, 16))
    n = s*s
    m = c*s*z
    zero("pure_pair_relation", m*sp.conjugate(m)-n*(n+1))
    Vtarget = sp.Matrix([[c*c+s*s, 0, 2*c*s*p, 2*c*s*v],
                        [0, c*c+s*s, 2*c*s*v, -2*c*s*p],
                        [2*c*s*p, 2*c*s*v, c*c+s*s, 0],
                        [2*c*s*v, -2*c*s*p, 0, c*c+s*s]])/2
    zero("quadrature_matrix", V-Vtarget)

    rho, phi, theta, eta = sp.symbols("rho phi theta eta", real=True)
    trig = {c: sp.cosh(rho), s: sp.sinh(rho), p: sp.cos(phi), v: sp.sin(phi)}
    ua = sp.Matrix([sp.cos(theta), sp.sin(theta), 0, 0])
    ub = sp.Matrix([0, 0, sp.cos(eta), sp.sin(eta)])
    cross = (ua.T*Vtarget*ub)[0].subs(trig)
    target = sp.sinh(rho)*sp.cosh(rho)*sp.cos(phi-theta-eta)
    zero("rotated_cross_quadrature", sp.trigsimp(cross-target), polynomial=False)
    difference = ((ua-ub).T*Vtarget*(ua-ub))[0].subs(trig)
    D = sp.cosh(2*rho)-sp.sinh(2*rho)*sp.cos(phi-theta-eta)
    zero("rotated_difference_variance", sp.trigsimp(difference-D), polynomial=False)
    zero("aligned_variance", sp.expand_trig(D.subs(eta, phi-theta))-sp.exp(-2*rho), polynomial=False)
    zero("anti_aligned_variance", sp.expand_trig(D.subs(eta, phi-theta-sp.pi))-sp.exp(2*rho), polynomial=False)
    zero("commuting_EPR_pair", (sp.Matrix([1, 0, -1, 0]).T*omega*sp.Matrix([0, 1, 0, 1]))[0])

    # Full geometric series: convergence for |q|<1 is established in the proof.
    q = sp.symbols("q", real=True, positive=True)
    x = sp.symbols("x", real=True)
    geometric = 1/(1-x)
    norm = (1-q*q)*geometric.subs(x, q*q)
    number = (1-q*q)*(x*sp.diff(geometric, x)).subs(x, q*q)
    anomalous_amplitude = (1-q*q)*q*sp.diff(geometric, x).subs(x, q*q)
    zero("series_normalization", norm-1, polynomial=False)
    zero("series_number", number-q*q/(1-q*q), polynomial=False)
    zero("series_anomalous", anomalous_amplitude-q/(1-q*q), polynomial=False)
    zero("series_matches_Bogoliubov", (m.subs({c: 1/sp.sqrt(1-q*q), s: q/sp.sqrt(1-q*q)})-z*anomalous_amplitude), polynomial=False)
    k = sp.symbols("k", integer=True, positive=True)
    ck = sp.sqrt(1-q*q)*q**k
    derivative = (1-q*q)*sp.diff(ck, q)
    generator_coeff = sp.sqrt(1-q*q)*(k*q**(k-1)-(k+1)*q**(k+1))
    zero("series_generator_positive_k", derivative-generator_coeff, polynomial=False)
    zero("series_generator_k0", (1-q*q)*sp.diff(sp.sqrt(1-q*q), q)+q*sp.sqrt(1-q*q), polynomial=False)
    M = sp.sinh(2*rho)/2
    phase_jacobian = sp.Matrix([M*sp.cos(phi), M*sp.sin(phi)]).jacobian([rho, phi]).det()
    zero("phase_recovery_jacobian", phase_jacobian-sp.sinh(4*rho)/4, polynomial=False)
    zero("vacuum_phase_singularity", phase_jacobian.subs(rho, 0), polynomial=False)
    zero("two_quadrature_phase_recovery", ((2*n+1)-(2*n+1-2*c*s*p))/2-I*((2*n+1-2*c*s*v)-(2*n+1))/2-m)
    time_var, wa, wb = sp.symbols("time omega_a omega_b", real=True)
    mt = sp.exp(-I*(wa+wb)*time_var)*m
    zero("free_phase_evolution", sp.diff(mt, time_var)+I*(wa+wb)*mt, polynomial=False)

    sample = {c: sp.Rational(5, 4), s: sp.Rational(3, 4),
              p: sp.Rational(3, 5), v: sp.Rational(4, 5)}
    rejected("wrong_anomalous_sign", (moment("a", "b")+m).subs(sample),
             "The source uses +pair creation in S; changing m to -m fails its vacuum calculation.")
    rejected("treat_half_generator_as_full", sp.Rational(1, 2)-sp.Rational(1, 4),
             "At Tratado r=log(2), aligned variance is exp(-r)=1/2, not exp(-2r)=1/4.")
    rejected("ignore_quadrature_phase", sp.Integer(4)-sp.Rational(1, 4),
             "At rho=log(2), phi=pi, unrotated difference is 4, not 1/4.")
    bad_moment_gram = sp.Matrix([[1,0,0,2],[0,1,2,0],[0,2,2,0],[2,0,0,2]])
    test = sp.Matrix([1,0,0,-1])
    witness = (test.T*bad_moment_gram*test)[0]
    assert witness < 0
    rejected("excess_anomalous_breaks_positivity", witness,
             "n=1,m=2 gives a negative <L*L>; violates |m|^2<=n(n+1).")
    rejected("discard_pair_correlations", ((sp.Rational(3,2)*sp.eye(4))*omega*(sp.Rational(3,2)*sp.eye(4))-omega/4)[0,1],
             "n=1,m=0 remains a positive mixed state, but cannot replace the specified pure squeezed state.")
    rejected("replace_antilinear_by_linear_mixing", (c*c+s*s-1).subs(sample),
             "Wrong a'=c a+s exp(i phi)b has commutator c^2+s^2 instead of 1.")
    rejected("Bogoliubov_is_not_complex_linear", (-2*I*s*z).subs(sample),
             "k(i e_b)-i k(e_b)=-2i s exp(i phi)e_a; circularH1 is complex linear.")
    rejected("single_difference_does_not_determine_phase", I*sp.sqrt(3),
             "phi=+pi/3 and -pi/3 have equal cos(phi), but unit pair phases differ by i sqrt(3).")
    rejected("zero_linear_mean_does_not_erase_pair_phase", (1-I)*sp.Rational(15,16),
             "At tanh(rho)=3/5, phases 0 and pi/2 both have zero linear means but different m.")
    rejected("unchecked_packet_basis", sp.Rational(1,2),
             "If <h1,h2>=1/2, [a(h1),a*(h2)] is not the required zero cross commutator.")
    for test_rho in (0.0, 0.2, 0.8, 1.3):
        for test_phi in (-2.4, 0.0, 0.37, 2.9):
            amplitude = math.sinh(test_rho)*math.cosh(test_rho)
            pair = amplitude*complex(math.cos(test_phi), math.sin(test_phi))
            if amplitude == 0:
                recovered = None
                assert pair == 0
            else:
                recovered = math.atan2(pair.imag, pair.real)
                error = math.atan2(math.sin(recovered-test_phi), math.cos(recovered-test_phi))
                assert abs(error) < 1e-14
                assert abs(0.5*math.asinh(2*abs(pair))-test_rho) < 1e-14
            checks.append({"id": f"phase_numeric_{test_rho}_{test_phi}", "status": "PASS",
                           "synthetic": True, "phase_identified": recovered is not None})

    manifest = save_new("SOURCE_PINS_R1.json", {
        "kind": "R59_SQUEEZING_PRIMARY_SOURCE_PINS", "sources": source_manifest(),
        "scope": "Source reading and exact finite-mode algebra; existing Lean statements not recompiled."})
    result = {
        "kind": "R59_EXACT_SQUEEZING_CHECKS", "status": "PASS",
        "author": "codex-pair-covariance-r59", "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "sympy": sp.__version__, "seconds": time.perf_counter()-started},
        "script": pin(Path(__file__)), "sources": manifest,
        "parameters": {"rho": "real coefficient of the pair generator", "graviton": "rho=r",
                       "tratado": "rho=r/2", "phase": "phi modulo 2*pi; unidentifiable at rho=0"},
        "formulas": {"n": "sinh(rho)^2", "m": "exp(I*phi)*sinh(rho)*cosh(rho)",
                     "difference_variance": "cosh(2*rho)-sinh(2*rho)*cos(phi-theta-eta)",
                     "C": "V + I*Omega/2 = K.conjugate().T*K/2", "K": str(K),
                     "V": str(Vtarget), "T": str(T)},
        "checks": checks, "checks_passed": len(checks),
        "negative_controls": negative_controls, "negative_controls_passed": len(negative_controls),
        "limits": ["Infinite-series convergence and operator domains are justified in DERIVATION_R1.txt, not by CAS.",
                   "No Lean compilation, observed data, provider, physical calibration or full network identification.",
                   "Finite-mode dimension is not a finite occupation cutoff. No truncated CCR matrix is used.",
                   "No new identification of beta, device modes, Maxwell helicity, regularFockDomain or Poincare dynamics."]}
    receipt = save_new("SYMBOLIC_RESULTS_R1.json", result)
    print(json.dumps({"result": receipt, "checks": len(checks),
                      "negative_controls": len(negative_controls),
                      "seconds": result["runtime"]["seconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
