"""Read-only, bounded C6 source manifest; no scientific pipeline is imported.

build_event_manifest() uses the event identity read from REGISTRO_C6.json.
An optional explicit event is an identity check, never an event alias.
The default uses the standard library only. DQ application is pending until the
resident worker reads each mask's own epoch/cadence/shortnames. Optional HDF5
inspection uses h5py in a suitable interpreter. No network or writes.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import os
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit
import zipfile

DEFAULT_ROOT = Path("C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN" if os.name == "nt"
                    else "/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN")
MAX_JSON_BYTES = 2_000_000
MAX_MASK_SAMPLES = 100_000


def _finite(value: Any, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Expected a numeric scalar")
    value = float(value)
    if not math.isfinite(value) or (positive and value <= 0):
        raise ValueError("Nonfinite or nonpositive scalar")
    return value


def _integer(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("Expected a positive integer")
    return value


def _names(values: Any) -> list[str]:
    if (not isinstance(values, list) or not values or len(values) > 64
            or not all(isinstance(v, str) and v for v in values)
            or len(set(values)) != len(values)):
        raise ValueError("Missing, duplicate or invalid flag names")
    return values


def _local(root: Path, name: str) -> Path:
    """Resolve only relative, contained paths, including symlink resolution."""
    if not isinstance(name, str):
        raise ValueError("Source path is not a string")
    name = name.replace("\\", "/")
    if name.startswith("/") or ":" in name or ".." in name.split("/"):
        raise ValueError("Source path escapes the allowed root")
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Source path escapes the allowed root")
    return path


def _cache_name(name: str, folder: str) -> str:
    """Rebase documented Windows/WSL receipts, never arbitrary absolute paths."""
    name = name.replace("\\", "/")
    marker = "/ORDEM_013_RINGDOWN/"
    if marker in name:
        name = name.split(marker, 1)[1]
    prefix = f"cache/gwosc/{folder}/"
    if not name.startswith(prefix) or "/" in name[len(prefix):] or ".." in name:
        raise ValueError("Unexpected referenced GWOSC cache location")
    return name


def _hash(path: Path) -> tuple[str, int]:
    before = path.stat()
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("Source changed while being hashed")
    return h.hexdigest(), after.st_size


def _npz_schema(path: Path) -> dict:
    """Read NPY headers inside the ZIP, not arrays or pickle payloads."""
    output = {}
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if len(entries) > 64:
            raise ValueError("Too many NPZ arrays")
        for entry in entries:
            name = entry.filename
            if not re.fullmatch(r"[A-Za-z0-9_]+\.npy", name) or name[:-4] in output:
                raise ValueError("Invalid or duplicate NPZ member")
            with archive.open(entry) as stream:
                magic = stream.read(8)
                if magic[:6] != b"\x93NUMPY" or magic[6:] not in (b"\x01\x00", b"\x02\x00", b"\x03\x00"):
                    raise ValueError("Invalid NPY header")
                width = 2 if magic[6] == 1 else 4
                length = int.from_bytes(stream.read(width), "little")
                if not 0 < length <= 65536:
                    raise ValueError("Invalid NPY header size")
                header = ast.literal_eval(stream.read(length).decode("utf-8" if magic[6] == 3 else "latin1"))
                dtype, shape = header["descr"], header["shape"]
                if not isinstance(dtype, str) or not re.fullmatch(r"[<>=|][biufc](?:1|2|4|8|16)", dtype):
                    raise ValueError("NPZ requires plain numeric arrays; object/structured dtype refused")
                if (not isinstance(shape, tuple) or len(shape) > 4 or any(
                        type(n) is not int or n < 0 for n in shape)):
                    raise ValueError("Invalid NPZ shape")
                expected = 8 + width + length + math.prod(shape) * int(dtype[2:])
                if expected != entry.file_size:
                    raise ValueError("NPY payload length does not match header")
                output[name[:-4]] = {"shape": list(shape), "dtype": dtype,
                                    "fortran_order": bool(header["fortran_order"])}
    return output


def _hdf5_metadata(path: Path, reg: dict, detector: str, on_source: bool) -> dict:
    import h5py  # Optional runtime dependency; never imports c6_engine.

    def text(value):
        return value.decode("utf-8") if isinstance(value, bytes) else str(value)

    with h5py.File(path, "r") as handle:
        def dataset(name):
            current = handle
            for part in name.split("/"):
                if not isinstance(current.get(part, getlink=True), h5py.HardLink):
                    raise ValueError(f"Nonlocal HDF5 link refused: {name}")
                current = current[part]
            if not isinstance(current, h5py.Dataset) or current.is_virtual or current.external:
                raise ValueError(f"External/virtual/non-dataset HDF5 source refused: {name}")
            return current

        def scalar(name):
            ds = dataset(name)
            if ds.shape != ():
                raise ValueError(f"Expected scalar: {name}")
            return ds[()]

        gps = _finite(float(scalar("meta/GPSstart")))
        duration = _finite(float(scalar("meta/Duration")), positive=True)
        if text(scalar("meta/Detector")) != detector:
            raise ValueError("HDF5 detector disagrees with receipt")
        strain = dataset("strain/Strain")
        spacing = _finite(float(strain.attrs["Xspacing"]), positive=True)
        rate = 1 / spacing
        if rate != 4096 or len(strain.shape) != 1 or strain.shape[0] != duration * rate:
            raise ValueError("C6 requires complete 4096 Hz strain metadata")
        if float(strain.attrs["Xstart"]) != gps or strain.dtype.kind != "f":
            raise ValueError("Strain epoch/dtype disagrees with metadata")
        result = {"status": "METADATA_AND_MASKS_READ_STRAIN_NOT_LOADED", "gps_start": gps,
                  "duration_s": duration, "gps_end_exclusive": gps + duration,
                  "sample_rate_hz": rate, "strain": {"dataset": "strain/Strain",
                  "shape": list(strain.shape), "dtype": str(strain.dtype),
                  "xspacing_s": spacing, "units": "dimensionless strain"}, "masks": {}}
        mask_values = {}
        for key, parent, prefix, required_key in (
            ("dq", "quality/simple", "DQ", "quality_required"),
            ("injection", "quality/injections", "Inj", "injection_flags_required"),
        ):
            ds = dataset(f"{parent}/{prefix}mask")
            short = dataset(f"{parent}/{prefix}Shortnames")
            descriptions = dataset(f"{parent}/{prefix}Descriptions")
            if len(short.shape) != 1 or not 0 < short.size <= 64 or descriptions.shape != short.shape:
                raise ValueError("Invalid mask bit schema")
            names = _names([text(v) for v in short[:]])
            desc = [text(v) for v in descriptions[:]]
            mask_start = _finite(float(ds.attrs["Xstart"]))
            mask_spacing = _finite(float(ds.attrs["Xspacing"]), positive=True)
            mask_units = text(ds.attrs["Xunits"])
            if (len(ds.shape) != 1 or not 0 < ds.size <= MAX_MASK_SAMPLES
                    or ds.dtype.kind != "u" or len(names) > ds.dtype.itemsize * 8
                    or int(ds.attrs["Bits"]) != len(names)
                    or mask_units != "second"):
                raise ValueError("Invalid mask schema/units/bit width")
            required = _names(reg[required_key])
            bits = [{"name": n, "bit": i, "value": 1 << i, "description": desc[i],
                     "required": n in required} for i, n in enumerate(names)]
            if any(n not in names for n in required):
                raise ValueError("Required flag absent from HDF5 bit names")
            required_mask = sum(1 << names.index(n) for n in required)
            values = [int(v) for v in ds[:]]  # At most MAX_MASK_SAMPLES; never returned.
            mask_values[key] = (values, required_mask, mask_start, mask_spacing)
            result["masks"][key] = {"dataset": f"{parent}/{prefix}mask", "dtype": str(ds.dtype),
                "shape": list(ds.shape), "gps_start": mask_start, "xspacing_s": mask_spacing,
                "xunits": mask_units,
                "bits": bits, "required_names": required, "required_mask": required_mask,
                "pass_condition": "(value & required_mask) == required_mask",
                "failed_mask_bins_whole_file": sum((v & required_mask) != required_mask for v in values),
                "set_bit_means": "test passes / data present" if key == "dq" else "named hardware injection absent"}
            if key == "injection" and "NO_CW_HW_INJ" in names:
                cw = 1 << names.index("NO_CW_HW_INJ")
                result["masks"][key]["cw_not_vetoed"] = "NO_CW_HW_INJ" not in required
                result["masks"][key]["cw_present_seconds"] = mask_spacing * sum(not v & cw for v in values)
        if on_source:
            peak = _finite(reg["reference_peak_GPS"][detector])
            n = _integer(reg["interval_samples"])
            stride = _integer(reg["sample_stride"])
            tm = _finite(reg["reference_tM_seconds"], positive=True)
            if rate / stride != _finite(reg["analysis_sample_rate_hz"], positive=True):
                raise ValueError("Analysis rate disagrees with retained source samples")
            starts = reg["start_times_tM"]
            if not isinstance(starts, list) or not 0 < len(starts) <= 64:
                raise ValueError("Invalid registered window count")
            windows = []
            for start in starts:
                requested = peak + _finite(start) * tm
                first = math.ceil((requested - gps) * rate)
                stop = first + n * stride
                if first < 0 or stop > strain.shape[0]:
                    raise ValueError("Registered window outside strain")
                # C6 covers the entire original span through stop-1. Use each
                # mask's own epoch/cadence rather than the strain sample clock.
                passed = True
                mask_intervals = {}
                for key, (vals, mask, epoch, cadence) in mask_values.items():
                    begin = math.floor((gps + first / rate - epoch) / cadence)
                    end = math.floor((gps + (stop - 1) / rate - epoch) / cadence)
                    if begin < 0 or end >= len(vals):
                        raise ValueError("Registered window outside mask coverage")
                    mask_intervals[key] = {"first": begin, "last_inclusive": end}
                    passed = passed and all((vals[s] & mask) == mask for s in range(begin, end + 1))
                windows.append({"start_tM": start, "requested_gps": requested,
                    "first_index": first, "stop_index_exclusive": stop, "sample_stride": stride,
                    "samples": n, "first_sample_gps": gps + first / rate,
                    "last_sample_gps": gps + (stop - stride) / rate,
                    "mask_intervals": mask_intervals, "dq_injection_pass": passed})
            result["registered_windows"] = windows
        return result


def build_event_manifest(event: str | None = None, root: str | Path | None = None,
                         *, inspect_hdf5: bool = False) -> dict[str, Any]:
    """Return a JSON-safe source manifest, including errors instead of false OK.

    root is the ORDEM_013_RINGDOWN directory (a temporary fixture is supported).
    All paths are confined to it. Full file SHA256s are streamed; NPZ reads
    headers only. By default HDF5 is left to the resident worker: metadata
    below is a declared schema, DQ is NOT applied. inspect_hdf5=True optionally
    inspects metadata/masks with h5py, never strain. No result file is written.
    ready_for_source_use is custody readiness for the requested event, not DQ
    acceptance, nor permission to claim physical detection or exclusion.
    root is trusted worker configuration, never an HTTP client path.
    """
    root = Path(root if root is not None else DEFAULT_ROOT).resolve()
    out: dict[str, Any] = {"schema_version": 1, "requested_event": event, "event": None,
        "event_matches": False, "status": "BLOCKED", "ready_for_source_use": False,
        "scientific_status": None,
        "dq_status": "PENDING_RESIDENT_VALIDATION",
        "event_gps": None, "event_gps_scope": "Geocentric event GPS not supplied by C6; detector peaks are separate",
        "reference_peak_gps": {}, "root": str(root), "sources": {}, "detectors": {},
        "errors": [], "limitations": [
            "No strain array or model was executed; this is a source/custody manifest.",
            "Local SHA256 matching is not an independent GWOSC checksum or physical validation.",
            "DQ/injection bit acceptance is separate from instrument calibration and scientific calibration.",
            "Scientific status must be read from the bound C6 result; metadata readiness does not promote it.",
            "C6 does not provide instrument amplitude/phase calibration uncertainty or marginalization.",
            "Without optional HDF5 inspection, mask bit positions and acceptance must come from resident dataset metadata.",
            "Do not multiply overlapping windows or same-event posterior evidences."]}

    def error(code, source, detail):
        out["errors"].append({"code": code, "source": str(source), "detail": str(detail)[:500]})

    def record(name, expected=None):
        entry = {"relative_path": name, "expected_sha256": expected, "sha256": None,
                 "integrity": "UNREADABLE"}
        out["sources"][name] = entry
        try:
            path = _local(root, name)
            entry["path"] = str(path)
            digest, size = _hash(path)
            entry.update(sha256=digest, bytes=size, integrity="LOCALLY_HASHED_UNPINNED")
            if expected is not None:
                if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
                    raise ValueError("Invalid expected SHA256")
                entry["integrity"] = "MATCH" if digest == expected.lower() else "MISMATCH"
                if entry["integrity"] == "MISMATCH":
                    error("HASH_MISMATCH", name, "Calculated SHA256 differs from recorded pin")
                    return None
            return path
        except (OSError, ValueError) as exc:
            error("SOURCE_UNREADABLE", name, exc)
            return None

    def read_json(name, expected=None):
        path = record(name, expected)
        if path is None:
            return None
        try:
            if path.stat().st_size > MAX_JSON_BYTES:
                raise ValueError("JSON exceeds metadata budget")
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != out["sources"][name]["sha256"]:
                raise ValueError("JSON changed after hash")
            obj = json.loads(raw, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
            if not isinstance(obj, dict):
                raise ValueError("Expected JSON object")
            return obj
        except (OSError, ValueError) as exc:
            error("INVALID_JSON", name, exc)
            return None

    reg = read_json("REGISTRO_C6.json")
    if reg is None:
        return out
    try:
        if event is None:
            event = reg.get("event")
            out["requested_event"] = event
        if not isinstance(event, str) or not event or not isinstance(reg.get("event"), str):
            raise ValueError("Event identity missing")
        out["event"] = reg["event"]
        out["event_matches"] = event == reg["event"]
        if not out["event_matches"]:
            error("EVENT_MISMATCH", "REGISTRO_C6.json", f"Requested {event}; record names {reg['event']}; no relabeling allowed")
        out["reference_peak_gps"] = {d: _finite(reg["reference_peak_GPS"][d]) for d in ("H1", "L1")}
        out["reference_source"] = reg["reference_source"]
        out["reference_redshift"] = _finite(reg["reference_redshift"])
        out["analysis"] = {key: reg[key] for key in ("interval_samples", "analysis_sample_rate_hz", "sample_stride",
            "start_times_tM", "primary_start_tM", "reference_tM_seconds", "time_selection", "noise")}
        out["analysis"].update(
            reference_mass_detector_solar_for_start=_finite(reg["reference_mass_for_start_solar"], positive=True),
            quality_required=_names(reg["quality_required"]),
            injection_flags_required=_names(reg["injection_flags_required"]))
        out["model"] = {key: reg[key] for key in ("likelihood", "scope", "computed_readings", "subresolution_readings",
            "omitted_nonexponential", "mass_detector_prior_solar", "spin_prior", "amplitude_prior", "physical_gate")}
        out["model"].update(projection="Independent complex amplitudes per detector; no shared F_plus/F_cross projection",
            physical_clock_selected=False, physical_exclusion_allowed=False,
            instrument_calibration_uncertainty="NOT_PROVIDED_BY_THIS_RECORD")
        _names(reg["quality_required"]); _names(reg["injection_flags_required"])
        pins = reg["code_and_input_hashes"]
        if not isinstance(pins, dict) or not pins or len(pins) > 64:
            raise ValueError("Invalid pinned source inventory")
        for name, expected in pins.items():
            if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
                raise ValueError(f"Missing/invalid registration SHA256: {name}")
            record(name, expected)
        reg_hash = out["sources"]["REGISTRO_C6.json"]["sha256"]
        downloads = read_json("C6_DOWNLOADS.json")
        results = read_json("C6_RESULTS.json")
        for name, doc in (("C6_DOWNLOADS.json", downloads), ("C6_RESULTS.json", results)):
            if doc is not None and doc.get("registration_sha256") != reg_hash:
                error("REGISTRATION_HASH_MISMATCH", name, "Summary/receipt is not bound to current C6 registration")
        if results is not None:
            out["scientific_result"] = {key: results.get(key) for key in ("status", "reason", "scope", "do_not_combine")}
            out["scientific_status"] = results.get("status")
            if results.get("status") != "INCONCLUSIVE_SYSTEMATICS":
                error("SCIENTIFIC_STATUS_CHANGED", "C6_RESULTS.json", "Expected C6 inconclusive status; independent review required")
            if results.get("registration_sha256") == reg_hash:
                out["scientific_result"]["registration_matches"] = True
            else:
                out["scientific_result"]["registration_matches"] = False
        if "C5_EMPIRICAL_NOISE.json" not in pins:
            raise ValueError("Noise summary is not pinned by registration")
        noise = read_json("C5_EMPIRICAL_NOISE.json", pins["C5_EMPIRICAL_NOISE.json"])
        if downloads is None or noise is None:
            return out
        if not isinstance(downloads.get("files"), list) or len(downloads["files"]) != 2:
            raise ValueError("Expected exactly H1 and L1 download entries")
        files = {item["detector"]: item for item in downloads["files"]}
        if len(noise["detectors"]) != 2 or len(reg["target_downloads"]) != 2:
            raise ValueError("Duplicate/missing noise or target detector")
        noises = {item["detector"]: item for item in noise["detectors"]}
        targets = {item["detector"]: item for item in reg["target_downloads"]}
        if set(files) != {"H1", "L1"} or set(noises) != set(files) or set(targets) != set(files):
            raise ValueError("Missing or duplicate detector source")
        for detector in ("H1", "L1"):
            item, n = files[detector], noises[detector]
            info = out["detectors"][detector] = {"source_event": reg["event"], "reference_peak_gps": out["reference_peak_gps"][detector]}
            if item.get("registration_sha256") != reg_hash:
                error("REGISTRATION_HASH_MISMATCH", detector, "Strain receipt is bound to another registration")
            on_name = _cache_name(item["path"], "on_source")
            off_name = _cache_name(n["input_path"], "offsource")
            if item.get("url") != targets[detector]["hdf5_url"] or Path(urlsplit(item["url"]).path).name != Path(on_name).name:
                error("DOWNLOAD_SOURCE_MISMATCH", detector, "Strain URL/file disagrees with registered target")
            for role, name, expected in (("strain", on_name, item["sha256"]), ("offsource", off_name, n["input_sha256"])):
                path = record(name, expected)
                info[role] = {"source": name, "path": str(_local(root, name)), "metadata": {
                    "status": "DECLARED_SCHEMA_RESIDENT_VALIDATION_PENDING",
                    "gps_start": targets[detector]["gps_start"] if role == "strain" else n["GPSstart"],
                    "sample_rate_hz": 4096, "rate_scope": "C6_REGISTERED_SOURCE_RATE_NOT_HEADER_CHECKED",
                    "strain": {"dataset": "strain/Strain", "time_attributes": ["Xstart", "Xspacing", "Xunits"]},
                    "masks": {key: {"dataset": f"{parent}/{prefix}mask",
                        "shortnames_dataset": f"{parent}/{prefix}Shortnames",
                        "descriptions_dataset": f"{parent}/{prefix}Descriptions",
                        "required_names": reg[required], "required_mask": None,
                        "time_attributes": ["Xstart", "Xspacing", "Xunits"],
                        "required_mask_rule": "sum(1 << shortnames.index(name) for name in required_names)",
                        "pass_condition": "(value & required_mask) == required_mask",
                        "set_bit_means": "test passes / data present" if key == "dq" else "named hardware injection absent"}
                        for key, parent, prefix, required in (
                            ("dq", "quality/simple", "DQ", "quality_required"),
                            ("injection", "quality/injections", "Inj", "injection_flags_required"))},
                    "registered_windows": [{"start_tM": start,
                        "requested_gps": out["reference_peak_gps"][detector] + start * reg["reference_tM_seconds"],
                        "samples": reg["interval_samples"], "sample_stride": reg["sample_stride"],
                        "dq_injection_pass": None} for start in reg["start_times_tM"]] if role == "strain" else []}}
                info[role]["metadata"]["masks"]["injection"]["cw_not_vetoed"] = "NO_CW_HW_INJ" not in reg["injection_flags_required"]
                if path is None:
                    continue
                if not inspect_hdf5:
                    continue
                try:
                    metadata = _hdf5_metadata(path, reg, detector, role == "strain")
                    info[role]["metadata"] = metadata
                    if role == "strain":
                        if metadata["gps_start"] != targets[detector]["gps_start"]:
                            raise ValueError("Strain GPS does not match registered download")
                        if not all(w["dq_injection_pass"] for w in metadata["registered_windows"]):
                            error("DQ_WINDOW_REJECTED", name, "Registered window fails required DQ/injection bits")
                    elif metadata["gps_end_exclusive"] >= min(out["reference_peak_gps"].values()):
                        raise ValueError("Offsource file reaches the event reference")
                except ImportError as exc:
                    error("HDF5_READER_UNAVAILABLE", name, exc)
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    error("HDF5_SCHEMA_ERROR", name, exc)
            npz_name = f"cache/empirical_noise/{detector}_noise.npz"
            if npz_name not in pins or pins[npz_name] != n["cache_sha256"]:
                raise ValueError("Noise NPZ has inconsistent/missing registration and summary pins")
            path = record(npz_name, pins[npz_name])
            info["noise"] = {"source": npz_name, "path": str(_local(root, npz_name)), "arrays": None,
                "metadata_status": "DECLARED_IN_PINNED_NOISE_SUMMARY",
                **{k: n[k] for k in ("training_seconds", "sample_selection", "method", "nuisance", "whitened_dof",
                    "interval_samples", "sample_rate_hz", "original_sample_rate_hz", "no_filter", "no_PSD_floor", "CW_scope")},
                "strain_scale": 1e21, "whitener_input": "whitener_scaled @ (strain * 1e21)",
                "scope": "PSD/whitener belong to this event/interval/stride/polynomial quotient, not arbitrary playback"}
            if path is not None:
                try:
                    arrays = _npz_schema(path)
                    count = _integer(reg["interval_samples"])
                    if arrays["whitener_scaled"]["shape"] != [n["whitened_dof"], count]:
                        raise ValueError("Whitening operator has the wrong interval shape")
                    if (n["interval_samples"] != count or n["whitened_dof"] != count - 3
                            or n["sample_rate_hz"] != reg["analysis_sample_rate_hz"]
                            or arrays["covariance_scaled"]["shape"] != [count, count]
                            or arrays["projected_covariance_scaled"]["shape"] != [count - 3, count - 3]):
                        raise ValueError("Noise covariance/degree-2 quotient disagrees with analysis")
                    freq = arrays["frequency_hz"]["shape"]
                    if len(freq) != 1 or arrays["median_psd_strain"]["shape"] != freq:
                        raise ValueError("PSD and frequency shapes disagree")
                    info["noise"]["arrays"] = arrays
                except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, SyntaxError) as exc:
                    error("NPZ_SCHEMA_ERROR", npz_name, exc)
        c7_name = "C7_C1_C6_ADDENDUM.json"
        if _local(root, c7_name).exists():
            c7 = read_json(c7_name)
            if c7:
                out["c7_summary"] = {"status": c7.get("status"), "C6": c7.get("C6"),
                                     "unresolved_acceptance": c7.get("unresolved_acceptance")}
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        error("REGISTRATION_SCHEMA_ERROR", "C6 sources", exc)
    out["ready_for_source_use"] = not out["errors"]
    if inspect_hdf5 and out["ready_for_source_use"]:
        out["dq_status"] = "REGISTERED_WINDOWS_PASS"
    out["status"] = ("SOURCE_MANIFEST_VERIFIED_SCIENCE_INCONCLUSIVE" if out["ready_for_source_use"]
                     else "BLOCKED_EVENT_MISMATCH" if not out["event_matches"] else "BLOCKED_SOURCE_VALIDATION")
    # Enforce finite standard JSON and bounded output even on unexpected metadata.
    try:
        if len(json.dumps(out, allow_nan=False)) > 250_000:
            raise ValueError("Manifest exceeds metadata output budget")
    except (ValueError, TypeError):
        return {"schema_version": 1, "requested_event": str(event), "event": reg.get("event"),
                "status": "BLOCKED_SOURCE_VALIDATION", "ready_for_source_use": False,
                "errors": [{"code": "INVALID_MANIFEST_METADATA", "source": "C6 sources",
                            "detail": "Nonfinite, non-JSON or oversized metadata"}]}
    return out
