"""One authorized pinned Welch preparation; observe cond, return it unchanged.

Never calls a waveform, likelihood, sampler, random seed, posterior parser, or
alternate PSD. Only custody pin hashing and the existing Welch preparation run.
"""
import os
for _key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_key] = "1"
import hashlib
import json
import math
import signal
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ROOT = B.parent
KERR = B / "bis/e3_pyring_preparation"
RUN = B / "cache/E3_KERR220_CALIBRATION_V1"
AUTH = B / "bis/E3_KERR_AUTHORIZATION_V1.json"
EXPECTED = "Covariance fails registered conditioning threshold; no jitter"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def publish(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    pending = path.with_name(path.name + ".pending")
    with pending.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    require(pending.stat().st_size == len(raw), "Incomplete diagnostic receipt")
    os.link(pending, path)
    pending.unlink()


def check_deadline(wall_end, monotonic_end):
    if time.time() >= wall_end or time.monotonic() >= monotonic_end:
        raise TimeoutError("Diagnostic guardian deadline")


def main():
    require(os.name == "posix" and Path(sys.prefix).resolve() == Path("/opt/lal_env"), "WSL pinned environment required")
    claim = HERE / "ONCE_CLAIM.json"
    # A failed attempt stays claimed. Do not rerun even if the diagnostic fails.
    started_utc = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    cpu = time.process_time()
    publish(claim, {"status": "ONE_DIAGNOSTIC_ATTEMPT_CLAIMED", "created_utc": started_utc,
                    "pid": os.getpid(), "script_sha256": sha(Path(__file__)), "maximum_wall_seconds": 120})
    result = {"status": "DIAGNOSTIC_STARTED", "started_utc": started_utc,
              "script_sha256": sha(Path(__file__)), "prepare_calls": 0, "cond_observations": [],
              "tests": {}, "PE_calls": 0, "waveform_calls": 0, "draws": 0,
              "posterior_values_read": False, "alternate_PSD_prepared": False,
              "thread_caps_requested": {k: os.environ[k] for k in (
                  "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS")}}
    original_cond = None
    watched = []
    before = {}

    def timeout_handler(signum, frame):
        raise TimeoutError("Diagnostic 120s/registered-deadline watchdog")

    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        sys.path.insert(0, str(KERR))
        from custody import verify, strict_json, utc
        watched = [AUTH, KERR / "MANIFEST_v3.json", KERR / "CONFIG.json",
                   *sorted(KERR.glob("*.py")), B / "bis/e2_code/strain_io.py",
                   B / "bis/e2_code/registration_guard.py", RUN / "welch/FAILURE.json",
                   RUN / "ENVELOPE.json", RUN / "welch/CONTEXT.json"]
        before = {str(p.relative_to(ROOT)): sha(p) for p in watched}
        original_failure = strict_json((RUN / "welch/FAILURE.json").read_bytes())
        require(original_failure["error"] == "ValueError(" + repr(EXPECTED) + ")", "Original failure differs")
        verify_start = time.perf_counter()
        cfg, manifest, auth, limit = verify(str(AUTH))
        result["custody_verify_seconds"] = time.perf_counter() - verify_start
        result["custody_verify"] = "PASSED_REAL_AUTHORIZATION_AND_SOURCE_RUNTIME_PINS"
        result["custody_hashing_scope"] = "verify hashes all manifest pins, including an existing reference-posterior file; no posterior values parsed"
        require(auth["manifest_filename"] == "MANIFEST_v3.json", "Unexpected manifest")
        envelope = strict_json((RUN / "ENVELOPE.json").read_bytes())
        context = strict_json((RUN / "welch/CONTEXT.json").read_bytes())
        require(envelope["authorization_sha256"] == sha(AUTH), "Envelope authorization differs")
        require(envelope["manifest_sha256"] == context["manifest_sha256"] == auth["manifest_sha256"], "Envelope/context pins differ")
        end = min(limit.timestamp(), utc(envelope["stop_utc"]).timestamp(),
                  utc(context["stop_utc"]).timestamp(), time.time() + 120 - (time.perf_counter() - start)) - 5
        monotonic_end = time.monotonic() + end - time.time()
        result["diagnostic_stop_utc"] = datetime.fromtimestamp(end, timezone.utc).isoformat()

        def guard():
            check_deadline(end, monotonic_end)

        guard()
        signal.setitimer(signal.ITIMER_REAL, max(0.001, end - time.time()))
        import numpy as np
        from strain_io import window, offsource_psd, require_pin
        from conditioning import prepare
        original_cond = np.linalg.cond
        observed = result["cond_observations"]

        def make_observer(delegate, log, detectors, deadline_guard):
            def observe(matrix, *args, **kwargs):
                deadline_guard()
                input_digest = hashlib.sha256(np.asarray(matrix).tobytes(order="C")).hexdigest()
                value = delegate(matrix, *args, **kwargs)
                diagonal = np.diag(matrix)
                raw_float = float(value)
                log.append({"detector": detectors[len(log)], "shape": list(matrix.shape),
                            "dtype": str(matrix.dtype), "diagonal_min": float(np.min(diagonal)),
                            "diagonal_max": float(np.max(diagonal)),
                            "covariance_scale": "Toeplitz(acf)/reference_amplitude^2; reference_amplitude=1e-21",
                            "cond_norm": "2 (np.linalg.cond default; SVD)",
                            "condition_number": raw_float if math.isfinite(raw_float) else None,
                            "condition_number_repr": repr(raw_float), "condition_number_hex": raw_float.hex(),
                            "registered_threshold": 1e12,
                            "threshold_exceeded_or_nonfinite": not math.isfinite(raw_float) or raw_float > 1e12,
                            "matrix_sha256_C_order": input_digest,
                            "matrix_bytes_unchanged_by_observer": input_digest == hashlib.sha256(np.asarray(matrix).tobytes(order="C")).hexdigest()})
                deadline_guard()
                return value  # SAME object/value, never clipped or replaced.
            return observe

        # Deterministic tiny tests only, no random draws and no second preparation.
        sentinel = np.float64(2.0)
        toy = np.diag([1.0, 2.0])
        test_log = []
        wrapper = make_observer(lambda matrix: sentinel, test_log, ["MOCK"], lambda: None)
        require(wrapper(toy) is sentinel, "Observer did not preserve exact return object")
        require(test_log[0]["matrix_bytes_unchanged_by_observer"], "Observer mutated matrix")
        require(float(original_cond(toy)) == 2.0, "Finite analytic cond test failed")
        result["tests"]["observer_same_return_object_and_unchanged_input"] = True
        result["tests"]["finite_analytic_diagonal_cond_2"] = True
        for label, wall, mono in (("wall_expired", time.time() - 1, time.monotonic() + 10),
                                  ("monotonic_expired", time.time() + 10, time.monotonic() - 1)):
            try:
                check_deadline(wall, mono)
            except TimeoutError:
                result["tests"][label] = True
            else:
                raise RuntimeError("Deadline test did not refuse")

        np.linalg.cond = make_observer(original_cond, observed, cfg["detectors"], guard)
        preparation_start = time.perf_counter()
        result["prepare_calls"] += 1
        try:
            prepare(cfg, "welch", ROOT, guard, (window, offsource_psd, require_pin))
        except ValueError as error:
            result["exception"] = {"type": type(error).__name__, "message": str(error),
                                   "frames": [{"file": frame.filename, "line": frame.lineno, "function": frame.name}
                                              for frame in traceback.extract_tb(error.__traceback__)]}
            require(str(error) == EXPECTED, "Preparation failed for a different reason")
            require(observed and observed[-1]["threshold_exceeded_or_nonfinite"], "Missing rejecting condition observation")
            result["status"] = "EXPECTED_REGISTERED_CONDITIONING_FAILURE_REPRODUCED_ONCE"
            result["tests"]["expected_original_exception_preserved"] = True
        else:
            raise RuntimeError("Unexpected Welch success; no sampling performed")
        finally:
            result["preparation_wall_seconds"] = time.perf_counter() - preparation_start
            np.linalg.cond = original_cond
        result["detectors_not_reached"] = cfg["detectors"][len(observed):]
        require(result["prepare_calls"] == 1 and all(x["shape"] == [819, 819] for x in observed), "Preparation shape/count differs")
        require(all(x["matrix_bytes_unchanged_by_observer"] for x in observed), "Observed matrix mutated")
        result["tests"]["single_prepare_expected_shape_819"] = True
        result["tests"]["np_cond_restored"] = np.linalg.cond is original_cond
        result["eigenvalues"] = "NOT_COMPUTED; condition/diagonal suffice for this scoped diagnosis"
        result["input_pins_checked_by_prepare"] = {name: cfg["data"][name] for name in cfg["detectors"][:len(observed)]}
        result["thread_count_scope"] = "Environment caps set before scientific imports; no threadpoolctl or process-wide thread attestation"
    except BaseException as error:
        result["status"] = "DIAGNOSTIC_FAILED_NO_RETRY"
        result["diagnostic_error"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        if original_cond is not None:
            np.linalg.cond = original_cond
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
        result["source_hashes_before"] = before
        result["source_hashes_after"] = {str(p.relative_to(ROOT)): sha(p) for p in watched}
        result["tests"]["watched_sources_config_authorization_failure_unchanged"] = before == result["source_hashes_after"]
        if before != result["source_hashes_after"]:
            result["status"] = "SOURCE_CHANGED_DIAGNOSTIC_INVALID"
        result["cost"] = {"wall_seconds_through_checks": time.perf_counter() - start,
                          "process_cpu_seconds_through_checks": time.process_time() - cpu,
                          "cost_scope": "Includes custody, deterministic wrapper tests, single preparation and source rehash; excludes final receipt flush",
                          "processes": 1, "requested_BLAS_threads": 1}
        result["finished_utc"] = datetime.now(timezone.utc).isoformat()
        result["all_written_files"] = [str(Path(__file__)), str(claim), str(HERE / "DIAGNOSTIC.json")]
        publish(HERE / "DIAGNOSTIC.json", result)
        print(json.dumps({"status": result["status"], "receipt_sha256": sha(HERE / "DIAGNOSTIC.json"),
                          "observations": result["cond_observations"], "cost": result["cost"], "tests": result["tests"]}))
    if result["status"] != "EXPECTED_REGISTERED_CONDITIONING_FAILURE_REPRODUCED_ONCE":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
