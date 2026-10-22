"""Compare frozen C6 algebra to the actual, unmodified pyRing 2.7.0 extension.

No new target-strain fit. The implementation oracle uses synthetic Toeplitz
controls and held-out OFF-source data. It cannot validate differences between
our mode/amplitude priors and the published LVK posterior.
"""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent
os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
                  MPLCONFIGDIR=str(ROOT / "cache/pyring_oracle/mpl_cache"))
import hashlib
import importlib.metadata
import json
import sys
import tarfile
from types import SimpleNamespace
sys.path.insert(0, str(ROOT / "cache/pyring_oracle/vendor"))
import numpy as np
from scipy.linalg import cholesky, qr, solve_triangular, toeplitz
from scipy.interpolate import CubicSpline
import pyRing
from pyRing import likelihood as upstream
from tgl_ringdown_likelihood import linear_statistics
from tgl_ringdown_prediction import prediction
from c6_engine import checked_registration


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def upstream_log_density(data, chol, normalizer):
    """Run upstream's full loglikelihood in the residual-data branch.

    With waveform_model=None, data is a supplied residual vector. The generic
    Gaussian function does not interpret these projected coordinates as GPS
    strain or perform a new detector response calculation.
    """
    data = np.ascontiguousarray(data, dtype=np.float64)
    detector = SimpleNamespace(time=np.arange(len(data), dtype=float),
                               time_series=data, cholesky=chol,
                               log_normalisation=float(normalizer))
    model = SimpleNamespace(tevent=0.0, detectors={"H1": detector})
    return upstream.loglikelihood(model, None, None, 0., 0., 0., 0.,
                                  {"H1_H1": 0.}, "H1", 0, len(data),
                                  likelihood_method="cholesky-solve-triangular")


def main():
    outpath = ROOT / "C6_PYRING_IMPLEMENTATION_ORACLE.json"
    if outpath.exists():
        raise FileExistsError("Preserve prior oracle receipt")
    registration, registration_hash = checked_registration()
    preparation = json.loads((ROOT / "cache/pyring_oracle/PREPARATION.json").read_bytes())
    if preparation["status"] != "PYRING_IMPORTED" or pyRing.__version__ != "2.7.0":
        raise ValueError("Unexpected pyRing installation")
    source = ROOT / "cache/source_distributions/pyRingGW-2.7.0.tar.gz"
    if digest(source) != preparation["source_sha256"]:
        raise ValueError("Upstream source changed")
    # Verify that the installed, declared Cython source is identical to the sdist.
    with tarfile.open(source) as archive:
        source_bytes = archive.extractfile("pyRingGW-2.7.0/pyRing/likelihood.pyx").read()
    installed_source = ROOT / "cache/pyring_oracle/vendor/pyRing/likelihood.pyx"
    if installed_source.read_bytes() != source_bytes:
        raise ValueError("Installed pyRing likelihood source is not byte-identical")
    rng = np.random.default_rng(130629)
    controls = []
    # Distinct upstream inversion paths and determinant algorithm.
    for n in (17, 64, 127):
        for rho in (0.0, 0.5, 0.95):
            acf = rho ** np.arange(n)
            covariance = toeplitz(acf)
            chol = cholesky(covariance, lower=True)
            residual = rng.normal(size=n)
            whitening = solve_triangular(chol, np.eye(n), lower=True)
            expected = float(np.dot(whitening @ residual, whitening @ residual))
            observed = {
                "cholesky": upstream.residuals_inner_product_cholesky_solve_triangular(residual, chol),
                "toeplitz": upstream.residuals_inner_product_toeplitz_inversion(residual, acf),
                "direct": upstream.residuals_inner_product_direct_inversion(residual, np.linalg.inv(covariance)),
            }
            sign, logdet = upstream.toeplitz_slogdet(acf.copy())
            reference_logdet = np.linalg.slogdet(covariance)[1]
            errors = {k: abs(v - expected) / max(1., abs(expected)) for k, v in observed.items()}
            controls.append(dict(n=n, rho=rho, relative_errors=errors,
                                 determinant_sign=float(sign),
                                 determinant_abs_error=float(abs(logdet-reference_logdet))))
    qnm = json.loads((ROOT / "QNM_GRID.json").read_bytes())["modes"]
    interpolation = {k: CubicSpline(qnm[k]["spins"], np.asarray(qnm[k]["real"])
                                   + 1j*np.asarray(qnm[k]["imag"])) for k in ("220", "440")}
    n = registration["interval_samples"]
    time = np.arange(n) / registration["analysis_sample_rate_hz"]
    orthogonal, _ = qr(np.polynomial.legendre.legvander(np.linspace(-1, 1, n), 2), mode="full")
    projection = orthogonal[:, 3:].T
    projected_checks, marginal_checks = [], []
    for detector in ("H1", "L1"):
        path = ROOT / "cache/empirical_noise" / f"{detector}_noise.npz"
        relative = path.relative_to(ROOT).as_posix()
        if digest(path) != registration["code_and_input_hashes"][relative]:
            raise ValueError("Frozen noise changed")
        with np.load(path) as archive:
            white = archive["whitener_scaled"]
            covariance = archive["projected_covariance_scaled"]
            targets = archive["held_out_strain_scaled"][:3].copy()
        chol = cholesky(covariance, lower=True)
        norm = -np.log(np.diag(chol)).sum() - len(chol)*np.log(2*np.pi)/2
        for index, target in enumerate(targets):
            projected = projection @ target
            expected = -float(np.dot(white @ target, white @ target))/2 + norm
            got = upstream_log_density(projected, chol, norm)
            projected_checks.append(dict(detector=detector, target=index,
                                         log_density_difference=float(got-expected)))
        wt = targets @ white.T
        for mass, spin in ((55., .4), (68.1, .68), (85., .9)):
            for reading in registration["computed_readings"]:
                columns = []
                for label, mode in (("220", (2, 2, 0)), ("440", (4, 4, 0))):
                    p = prediction(mass, spin, reading, redshift=registration["reference_redshift"],
                                   mode=mode, qnm_dimensionless=complex(interpolation[label](spin)))
                    envelope = np.exp(-(1/p["tau_gr_s"]+p["gamma_per_s"])*time)
                    columns.extend([envelope*np.cos(p["omega_rad_s"]*time),
                                    envelope*np.sin(p["omega_rad_s"]*time)])
                basis = white @ np.column_stack(columns)
                for sd in registration["amplitude_prior_sd_scaled"]:
                    _, expected = linear_statistics(basis, wt, sd)
                    # Independent Gaussian convolution in DATA space (407x407),
                    # rather than the production coefficient-space (4x4) solve.
                    expanded = np.eye(len(white)) + sd**2 * (basis @ basis.T)
                    chol_m = cholesky(expanded, lower=True)
                    norm_m = -np.log(np.diag(chol_m)).sum() - len(chol_m)*np.log(2*np.pi)/2
                    norm_null = -len(chol_m)*np.log(2*np.pi)/2
                    for i, target in enumerate(wt):
                        signal = upstream_log_density(target, chol_m, norm_m)
                        null = upstream_log_density(target, np.eye(len(target)), norm_null)
                        difference = float(signal-null-expected[0, i])
                        marginal_checks.append(dict(detector=detector, mass=mass, spin=spin,
                                                    reading=reading, prior_sd=sd, target=i,
                                                    lnZ_difference=difference))
    # Deliberate wrong likelihood implementations must fail the comparison.
    example_basis = np.column_stack([np.linspace(0, 1, 31), np.linspace(0, 1, 31)**2])
    example_target = rng.normal(size=31)
    _, correct = linear_statistics(example_basis, example_target, 2.)
    gram = example_basis.T @ example_basis
    rhs = example_basis.T @ example_target
    no_determinant = .5 * rhs @ np.linalg.solve(gram+np.eye(2)/4, rhs)
    missing_det_delta = float(no_determinant-correct[0, 0])
    stats = dict(toeplitz_controls=len(controls), projected_noise_checks=len(projected_checks),
                 marginalized_checks=len(marginal_checks),
                 max_inner_relative_error=max(max(r["relative_errors"].values()) for r in controls),
                 max_determinant_abs_error=max(r["determinant_abs_error"] for r in controls),
                 max_projected_log_density_error=max(abs(r["log_density_difference"]) for r in projected_checks),
                 max_marginal_lnZ_error=max(abs(r["lnZ_difference"]) for r in marginal_checks),
                 missing_determinant_control_difference=missing_det_delta)
    passed = (stats["max_inner_relative_error"] < 1e-10
              and stats["max_determinant_abs_error"] < 1e-9
              and all(r["determinant_sign"] == 1 for r in controls)
              and stats["max_projected_log_density_error"] < 1e-4
              and stats["max_marginal_lnZ_error"] < 1e-6
              and missing_det_delta > .1)
    result = dict(status="PASS_IMPLEMENTATION_ONLY" if passed else "ORACLE_FAILED",
                  stats=stats, registration_sha256=registration_hash,
                  target_strain_read=False, canonical_files_modified=False,
                  pyRing_version=pyRing.__version__, source_sha256=digest(source),
                  installed_likelihood_pyx_sha256=hashlib.sha256(source_bytes).hexdigest(),
                  compiled_extension_sha256=digest(Path(upstream.__file__)),
                  generator_sha256=digest(Path(__file__)),
                  versions={k:importlib.metadata.version(k) for k in ("numpy", "scipy", "Cython", "pyRingGW")},
                  controls=controls, projected_checks=projected_checks, marginal_checks=marginal_checks,
                  limitations=["No repeated LVK posterior or nested sampling",
                               "Projected coordinates, not a new polarization-coherent physical model",
                               "Cannot repair the failed two-family injection gate",
                               "The published start-time posteriors still have different modes and priors",
                               "No new physical clock/partition/unraveling selected"])
    temp = outpath.with_suffix(".json.tmp")
    temp.write_bytes((json.dumps(result, indent=2)+"\n").encode())
    temp.replace(outpath)
    print(json.dumps(dict(status=result["status"], **stats)), flush=True)
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
