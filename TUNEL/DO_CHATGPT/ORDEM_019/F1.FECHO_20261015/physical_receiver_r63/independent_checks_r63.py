"""Focal independent checks: Gaussian measure and documentary counterexamples."""
from pathlib import Path
import hashlib
import json
import sympy as s

B = Path(__file__).resolve().parent


def main():
    checks = []

    def check(name, got, expected):
        residual = s.simplify(got - expected)
        assert residual == 0, (name, residual)
        checks.append({"name": name, "got": str(got), "expected": str(expected), "passed": True})

    x = s.symbols("x", real=True)
    weight = s.exp(-x*x) / s.sqrt(s.pi)
    for k, wanted in enumerate([1, 0, s.Rational(1, 2), 0, s.Rational(3, 4)]):
        check("Gaussian_moment_" + str(k), s.integrate(x**k * weight, (x, -s.oo, s.oo)), wanted)
    # The one-photon wavefunction density is 2*x^2*weight.
    check("one_photon_homodyne_second_moment", s.integrate(2*x**4*weight, (x, -s.oo, s.oo)), s.Rational(3, 2))
    a = s.Matrix([[0, 1], [0, 0]])
    one = s.Matrix([0, 1])
    check("one_photon_coherent_amplitude", (one.T*a*one)[0], 0)
    check("one_photon_total_occupation", (one.T*a.T*a*one)[0], 1)
    check("count_minus_coherent_intensity", (one.T*a.T*a*one)[0] - (one.T*a*one)[0]**2, 1)
    # Orthonormal packet norm: two orthogonal tensor terms, each norm 1.
    fi, fo = s.Matrix([1, 0]), s.Matrix([0, 1])
    v = (s.kronecker_product(fi, fo) + s.kronecker_product(fo, fi)) / s.sqrt(2)
    check("orthonormal_two_packet_norm", (v.T*v)[0], 1)
    pure = lambda f: s.kronecker_product(f, f)
    diff = pure(fi + fo) - pure(fi) - pure(fo) - s.sqrt(2)*v
    check("two_packet_diagonal_span_polarization", (diff.T*diff)[0], 0)
    ratio = s.Rational(1667359000) * s.Rational(780, 10**9) / 299792458
    assert ratio != s.Rational(6, 5)
    checks.append({"name": "single_time_scale_cannot_match_both_absolute_frequencies", "document_ratio_exact": str(ratio), "document_ratio_float": float(ratio), "synthetic_ratio": "6/5", "passed": True})
    out = {"status": "PASS_FOCAL_INDEPENDENT_CHECKS", "reviewer": "codex-mission-memory-review", "checks": checks, "count": len(checks), "constructor_script_executed": False, "trajectory_runs": 0, "scope": "Independent Gaussian integrals and exact finite/documentary controls; not repetition of the 18 constructor identities or R62 dynamics.", "script": {"path": str(Path(__file__)), "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    target = B / "INDEPENDENT_CHECKS_R63.json"
    with target.open("x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps({"status": out["status"], "count": len(checks), "path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
