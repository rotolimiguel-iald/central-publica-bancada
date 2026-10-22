"""Metadata-only readiness and deterministic E0 planning projections; no data reads."""
import csv
import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import NormalDist
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
ROOT = B.parent
META = HERE / "metadata"
SOURCES = {}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(path):
    path = path.resolve()
    if not path.is_relative_to(ROOT) or path.stat().st_size > 25_000_000:
        raise ValueError("Source outside scope/size cap")
    SOURCES[path.relative_to(ROOT).as_posix()] = sha(path)
    return path.read_bytes()


def read(path):
    return json.loads(source(path))


def pin(path):
    source(path)
    return {"relative_to_Chatgpt": path.relative_to(ROOT).as_posix(), "sha256": sha(path)}


def write(name, obj):
    raw = (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    path = HERE / name
    temp = path.with_name(path.name + ".pending")
    with temp.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.stat().st_size != len(raw):
        raise OSError("Incomplete artifact")
    os.link(temp, path)
    temp.unlink()


def metadata(label):
    receipt = read(META / (label + ".receipt.json"))
    if receipt["status"] != "METADATA_READ_NO_SCIENCE_BYTES":
        raise ValueError("Metadata unavailable: " + label)
    path = META / (label + ".body")
    raw = source(path)
    if hashlib.sha256(raw).hexdigest() != receipt["sha256"]:
        raise ValueError("Metadata snapshot changed")
    return raw, {"receipt": pin(META / (label + ".receipt.json")), "body": pin(path),
                 "url": receipt["final_url"], "retrieved_utc": receipt["finished_utc"]}


def intersect(a, b):
    out = []
    for lo, hi in a:
        for low, high in b:
            left, right = max(lo, low), min(hi, high)
            if left < right:
                out.append([left, right])
    return sorted(out)


def main():
    reg_path = B / "RINGDOWN_5SIGMA_V1.json"
    reg = read(reg_path)
    reg_pin = pin(reg_path)
    index_path = B / "bis/e3_publication_refresh/PUBLICATION_METADATA_REVIEW_INDEX.json"
    publication = read(index_path)
    if publication["parent_registration_sha256"] != reg_pin["sha256"]:
        raise ValueError("Publication review parent mismatch")
    csv_path = B / "bis/e0_metadata/GWOSC_EVENTS.csv"
    source(csv_path)
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    by_id = {row["event"]: (line, row) for line, row in enumerate(csv_rows, 2)}
    if len(by_id) != len(csv_rows):
        raise ValueError("Duplicate E0 metadata ID")
    candidates = sorted((v for v in reg["test_candidates"].values()
                         if v["eligible"] is True and v["published_deformation_at_registration"] is False),
                        key=lambda v: (-v["SNR_network_GWOSC"], v["event"]))
    rows = []
    for rank, entry in enumerate(candidates, 1):
        event = entry["event"]
        line, e0 = by_id[event]
        rho = float(e0["network_matched_filter_snr"])
        if rho != entry["SNR_network_GWOSC"] or type(entry["data_quality_hold"]) is not bool:
            raise ValueError("SNR/hold source mismatch")
        refreshed = publication["events"][event]
        review = refreshed["publication_metadata_review"]
        p = ROOT / review["relative_to_Chatgpt"]
        read(p)
        if sha(p) != review["sha256"] or refreshed["data_quality_hold"] != entry["data_quality_hold"]:
            raise ValueError("Review pin/hold differs")
        if not reg["registered_utc"] <= review["reviewed_utc"] <= datetime.now(timezone.utc).isoformat():
            raise ValueError("Review chronology differs")
        rows.append({"rank_by_existing_SNR": rank, "event": event, "SNR_network": rho,
                     "run": entry["run"], "data_quality_hold": entry["data_quality_hold"],
                     "registered_eligible": True, "published_deformation_at_registration": False,
                     "publication_census_scope": entry["publication_census_scope"],
                     "GR_final_mass_detector_median_INPUT": entry["GR_final_mass_detector_median"],
                     "GR_final_spin_median_INPUT": entry["GR_final_spin_median"],
                     "GR_metadata_origin": entry["metadata_origin"],
                     "E2_candidate_locator": "/test_candidates/" + event,
                     "SNR_source": {**pin(csv_path), "line": line, "field": "network_matched_filter_snr",
                                    "version_key": e0["version_key"], "primary_url": e0["event_metadata_url"]},
                     "publication_metadata_review": review,
                     "admission": None, "blindness_certified_here": False,
                     "role": "REGISTERED_CANDIDATE_METADATA_ONLY_HOLD_PRESERVED"})
    if len(rows) != 14 or sum(not r["data_quality_hold"] for r in rows) != 10:
        raise ValueError("Unexpected registered census; do not silently reselect")
    write("CANDIDATES_SORTED.json", {"status": "PREPARATION_NOT_ADMISSION", "E2": reg_pin,
          "publication_refresh_index": pin(index_path), "candidates": rows,
          "count_total": len(rows), "count_unheld": 10, "count_held": 4,
          "ranking": "Existing rounded GWOSC preferred network IMR SNR, not ringdown SNR or information/hour"})

    # All arithmetic below uses the already reviewed nonblind fit; never new draws.
    fit_path = B / "bis/E0_SNR_INFORMATION_FIT.json"
    fitdoc = read(fit_path)
    source(B / "bis/E0_SNR_FIT_REVIEW.md")
    information = []
    control_errors = []
    for fit in fitdoc["fits"]:
        if fit["population"] not in ("GWTC5_31", "GWTC5_33"):
            continue
        a, b = fit["coefficients_log_intercept_slope"]
        cov = fit["covariance"]
        s = fit["residual_sigma_ln_ddof_Nminus2"]
        tcrit = fit["coefficient_95_t_halfwidth"][0] / math.sqrt(cov[0][0])
        if not math.isclose(tcrit, fit["coefficient_95_t_halfwidth"][1] / math.sqrt(cov[1][1]), rel_tol=1e-12):
            raise ValueError("Inconsistent stored t uncertainty")
        def project(rho):
            x = math.log(rho)
            mu = a + b * x
            vm = cov[0][0] + x * (cov[0][1] + cov[1][0]) + x*x*cov[1][1]
            if vm <= 0 or not math.isfinite(vm):
                raise ValueError("Invalid propagated coefficient covariance")
            half = tcrit * math.sqrt(vm)
            median = math.exp(mu)
            proxy = math.exp(-2*mu)
            expectation = math.exp(-2*mu + 2*s*s)
            return {"ln_sigma_mean_mu": mu, "mu_variance_from_full_coefficient_covariance": vm,
                    "sigma_conditional_median": median,
                    "sigma_residual_conditional_05_50_95": [math.exp(mu+s*NormalDist().inv_cdf(p)) for p in (.05,.5,.95)],
                    "sigma_median_coefficient_only_95_t_interval": [math.exp(mu-half), math.exp(mu+half)],
                    "inverse_squared_conditional_median_proxy": proxy,
                    "expected_inverse_variance_lognormal_s_fixed": expectation,
                    "expected_I_coefficient_only_95_t_interval_s_fixed": [expectation*math.exp(-2*half), expectation*math.exp(2*half)],
                    "parameter_gaussian_integrated_information_s_fixed": expectation*math.exp(2*vm),
                    "ratio_expectation_to_proxy": math.exp(2*s*s),
                    "outside_fit_SNR_domain": not fit["SNR_domain"][0] <= rho <= fit["SNR_domain"][1],
                    "bootstrap_interval_at_candidate_SNR": None,
                    "bootstrap_interval_status": "OPEN: stored bootstrap quantiles only at other SNR grid points; no stored coefficient draws; no interpolation or new bootstrap",
                    "full_predictive_uncertainty": "OPEN: s uncertainty, SNR error, transfer/selection and waveform/prior differences not calibrated",
                    "information_for_actual_new_PE": None,
                    "actual_new_PE_status": "OPEN: empirical published-posterior width model not validated for broad-prior aligned custom PE"}
        for stored in fit["predictions"]:
            current = project(stored["SNR_network"])
            for old, new in (("median_sigma_tau", "sigma_conditional_median"),
                             ("inverse_squared_median", "inverse_squared_conditional_median_proxy"),
                             ("expected_inverse_variance_tau", "expected_inverse_variance_lognormal_s_fixed"),
                             ("parameter_uncertainty_gaussian_integrated_information", "parameter_gaussian_integrated_information_s_fixed")):
                err = abs(current[new]-stored[old]) / max(abs(stored[old]), 1e-300)
                if err > 1e-12:
                    raise ValueError("Projection does not reproduce existing fit grid")
                control_errors.append(err)
        for row in rows:
            information.append({"event": row["event"], "data_quality_hold": row["data_quality_hold"],
                                "SNR_network": row["SNR_network"], "SNR_source": row["SNR_source"],
                                "fit_population": fit["population"], "fit_SNR_domain": fit["SNR_domain"],
                                **project(row["SNR_network"])})
    write("EXPECTED_INFORMATION.json", {"status": "DETERMINISTIC_NONBLIND_PLANNING_PROXIES_NOT_TEST_POWER_OR_ADMISSION",
          "fit_source": pin(fit_path), "fit_review": pin(B / "bis/E0_SNR_FIT_REVIEW.md"),
          "formula": "mu=a+b*ln(rho); proxy=exp(-2mu); E[I|rho,s]=exp(-2mu+2s^2); Var(mu)=[1,lnrho] Cov [1,lnrho]^T",
          "coefficient_intervals": "t critical recovered from existing fit halfwidth/covariance; conditional s held fixed; not full prediction intervals",
          "fits_preserved": [{k: f[k] for k in ("population", "coefficients_log_intercept_slope", "covariance", "coefficient_95_t_halfwidth", "residual_sigma_ln_ddof_Nminus2", "SNR_domain", "bootstrap_draws")} for f in fitdoc["fits"]],
          "stored_bootstrap_grid_preserved": [{"population": f["population"], "grid": [{"SNR": p["SNR_network"], "interval": p["event_bootstrap_information_025_50_975"]} for p in f["predictions"]]} for f in fitdoc["fits"]],
          "fit_grid_scalar_checks": len(control_errors), "max_relative_error": max(control_errors),
          "rows": information, "posterior_candidate_reads": False, "new_fit_or_draws": False,
          "cost_hour_ranking": None, "information_additivity_or_covariance_between_candidates": "OPEN",
          "fit31_vs33": "Overlapping calibration samples; not independent evidence"})

    md5_maps = {}
    for run in ("O4a", "O4b"):
        raw, provenance = metadata(run + "_md5")
        mapping = {}
        for lineno, line in enumerate(raw.decode().splitlines(), 1):
            checksum, filename = line.split()
            name = filename.rsplit("/", 1)[-1]
            if name in mapping:
                raise ValueError("Ambiguous provider checksum filename")
            mapping[name] = {"checksum": checksum, "line": lineno, "provider_path": filename}
        md5_maps[run] = (mapping, provenance)
    _, license_source = metadata("O4_details")
    license_body = (META / "O4_details.body").read_text(encoding="utf-8")
    if "creativecommons.org/licenses/by/4.0" not in license_body:
        raise ValueError("License statement absent")
    metadata("acknowledgement")
    pilot = reg["pe_jobs"]["GW250114_PILOT"]
    flags = pilot["quality_required"] + pilot["injection_flags_required"]
    targets = [r for r in rows if not r["data_quality_hold"]][:5]
    details = []
    licenses = []
    for row in targets:
        event = row["event"]
        run = row["run"]
        event_label = event + ("_retry" if event == "GW230919_215712" else "")
        raw, event_source = metadata(event_label)
        event_doc = json.loads(raw)
        e = next(iter(event_doc["events"].values()))
        if e["commonName"] != event or float(e["network_matched_filter_snr"]) != row["SNR_network"]:
            raise ValueError("Fresh event identity/SNR differs; do not silently rerank")
        timeline_label = "timeline_GW230919" if event == "GW230919_215712" else "timeline_" + event
        raw, timeline_source = metadata(timeline_label)
        timelines = json.loads(raw)
        dataset_raw, dataset_source = metadata(run + "_dataset")
        dataset = json.loads(dataset_raw)
        if not set(flags) <= {x["shortName"] for x in dataset["bits"]}:
            raise ValueError("Missing required flag definitions")
        gps = float(e["GPS"])
        detectors = []
        for detector in ("H1", "L1"):
            stream = [s for s in e["strain"] if s["detector"] == detector and s["sampling_rate"] == 4096 and s["format"] == "hdf5"]
            if len(stream) != 1:
                raise ValueError("Ambiguous event file")
            stream = stream[0]
            archive_label = "archive_H1_GW230919" if event == "GW230919_215712" and detector == "H1" else "archive_" + detector + "_" + event
            archive_raw, archive_source = metadata(archive_label)
            files = [f for f in json.loads(archive_raw)["strain"] if f["detector"] == detector and f["format"] == "hdf5" and f["sampling_rate"] == 4096]
            if not any(f["url"] == stream["url"] for f in files):
                raise ValueError("Event/archive URL disagreement")
            combined = [[timelines[detector+"_DATA"]["start"], timelines[detector+"_DATA"]["end"]]]
            for flag in flags:
                combined = intersect(combined, timelines[detector+"_"+flag]["segments"])
            containing = [segment for segment in combined if segment[0] <= gps < segment[1]]
            file_records = []
            for f in sorted(files, key=lambda x: x["GPSstart"]):
                if f["GPSstart"] > stream["GPSstart"]:
                    continue
                name = urlsplit(f["url"]).path.rsplit("/", 1)[-1]
                checksum = md5_maps[run][0].get(name)
                if checksum is None:
                    raise ValueError("Official MD5 not found")
                possible = intersect(combined, [[f["GPSstart"], min(f["GPSstart"]+f["duration"], math.floor(gps)-16)]])
                first256 = next(([math.ceil(lo), math.ceil(lo)+256] for lo, hi in possible if math.ceil(lo)+256 <= hi), None)
                record = {k: f[k] for k in ("GPSstart", "duration", "sampling_rate", "format", "detector", "url")}
                record.update(role="EVENT_FILE_ONSOURCE_AND_POSSIBLE_PSD" if f["url"] == stream["url"] else "PRECEDING_OFFSOURCE_OPTION_NOT_SELECTED",
                              first_256s_all_flags_segment_before_GPSminus16_INPUT=first256,
                              provider_checksum_algorithm="md5", provider_checksum=checksum["checksum"],
                              checksum_source={**md5_maps[run][1], "line": checksum["line"], "provider_path": checksum["provider_path"]},
                              provider_checksum_verified_against_bytes=False, local_sha256=None, expected_bytes=None,
                              filename=name, metadata_only=True, license_status="CC_BY_4_0_DECLARED_BY_PRIMARY_GWOSC_RELEASE_PAGE",
                              license_source=license_source["url"])
                file_records.append(record)
                licenses.append({"event": event, "detector": detector, "url": f["url"], "filename": name,
                                 "license_status": record["license_status"], "license_source": record["license_source"],
                                 "license_evidence": license_source, "acknowledgement_url": "https://gwosc.org/acknowledgement/",
                                 "scope": "Per-file mapping to primary release policy; metadata only, no download or legal adjudication"})
            detectors.append({"detector": detector, "files": file_records,
                              "event_GPS_passes_all_required_public_timeline_flags": bool(containing),
                              "all_flags_interval_containing_event": containing,
                              "intervals_all_flags_within_queried_span": combined,
                              "onsource_window_final": None, "offsource_window_final": None,
                              "timeline_source": timeline_source, "archive_source": archive_source,
                              "not_proven": "HDF5 1Hz masks, finite strain, PSD positivity/stationarity and actual analysis-window coverage require later authorized byte checks"})
        e0 = by_id[event][1]
        details.append({"event": event, "SNR_network_existing": row["SNR_network"], "event_GPS": gps,
                        "source": event_source, "dataset_flags_source": dataset_source,
                        "quality_required_INPUT_from_pilot": pilot["quality_required"],
                        "injection_flags_required_INPUT_from_pilot": pilot["injection_flags_required"],
                        "PSD_scout_contract_INPUT_NOT_ALLOCATED": {"duration_s": 256, "exclusion_s": 16, "selection": "earliest metadata-valid block per file; true runner also requires finiteness and cutoff<=analysis_start"},
                        "GR_existing_E0_summary_INPUT": {k: e0[k] for k in ("mass_1_source", "mass_2_source", "redshift", "chi_eff", "event_metadata_url")},
                        "GR_summary_limit": "Source-frame marginal medians, not paired detector masses; chi_eff is not chi1/chi2; not inspiral-only proof or a prior",
                        "publication_metadata_review": row["publication_metadata_review"], "data_quality_hold": False,
                        "detectors": detectors, "admission": None,
                        "missing_config_inputs": ["local strain SHA256 after registered fetch", "approved free component-mass/spin/deformation priors", "mass frame and angular priors", "fmin/fmax/reference frequency", "duration/start/geocent_time prior and prior-wide temporal bounds", "detector network choice; catalog SNR may include Virgo", "PSD and flag contract approval for this event", "remnant/cosmology INPUT copy with pins", "sampler settings and cost-derived wall reservation", "unique output directory and refreshed prelaunch gates"]})
    write("METADATA_READINESS.json", {"status": "FIVE_TOP_UNHELD_METADATA_ONLY_NOT_ADMITTED", "targets": details,
          "fresh_SNR_matches_existing_E0": True, "strain_downloaded": False, "posterior_read": False,
          "provider_file_sizes": "Not supplied by queried metadata; no strain HEAD/GET performed",
          "timeline_scope": "Public interval metadata only, not strain validation or DQ hold clearance"})
    write("PER_FILE_LICENSE_METADATA.json", {"status": "PRIMARY_RELEASE_POLICY_MAPPED_TO_FILES_NOT_DOWNLOAD_AUTHORIZATION", "files": licenses})
    license_pin = pin(HERE / "PER_FILE_LICENSE_METADATA.json")
    templates = []
    for item in details:
        templates.append({"event": item["event"], "state": "INCOMPLETE_NONEXECUTABLE_TEMPLATE", "not_jobs_schema": True,
                          "publication_metadata_review": item["publication_metadata_review"],
                          "job_fields_known": {"event": item["event"], "mode": "blind_test", "event_GPS": item["event_GPS"], "privacy_mode": "procedural_same_host"},
                          "job_fields_pending": item["missing_config_inputs"],
                          "download_recipe_fragments": [{"event": item["event"], "mode": "blind_test", "kind": "public_strain",
                              "url": f["url"], "filename": f["filename"], "maximum_bytes": None, "expected_bytes": None,
                              "provider_checksum_algorithm": "md5", "provider_checksum": f["provider_checksum"],
                              "license_status": f["license_status"], "license_source": f["license_source"],
                              "license_receipt_relative_to_Chatgpt": license_pin["relative_to_Chatgpt"], "license_receipt_sha256": license_pin["sha256"],
                              "INCOMPLETE_REASON": "maximum_bytes and actual allocation/review remain unassigned; no recipe activated"}
                              for d in item["detectors"] for f in d["files"]]})
    custody_sources = []
    for name in ("E2_CUSTODY_TRANSFER_V1.json", "E2_CUSTODY_HOST_VERIFIED_V1.json"):
        path = B / "bis" / name
        doc = read(path)
        if doc["registration_sha256"] != reg_pin["sha256"]:
            raise ValueError("Custody provenance wrong parent")
        custody_sources.append({**pin(path), "status": doc["status"], "scope": "Metadata provenance only; no seed/offset accessed; no new core gate"})
    write("NONEXECUTABLE_TEMPLATES.json", {"status": "PREPARATION_ONLY_NO_JOBS_NO_BUDGET_NO_ADMISSION",
          "templates": templates, "custody_provenance": custody_sources, "cost_estimates": None})
    for name in ("registration_guard.py", "fetch_registered.py", "pe_runner.py", "strain_io.py", "temporal_contract.py", "run_controlled.py"):
        source(B / "bis/e2_code" / name)
    source(B / "bis/e3_allocation_prepare/render_allocation_candidates.py")
    write("SOURCE_PINS.json", {"status": "READ_ONLY_SOURCES_FOR_PREPARATION", "created_utc": datetime.now(timezone.utc).isoformat(),
          "sources_sha256_relative_to_Chatgpt": SOURCES, "builder_sha256": sha(Path(__file__)),
          "E2_runtime_gate_executed": False, "allocation_emitted": False, "secret_read": False})
    print(json.dumps({"candidates": len(rows), "unheld": len(targets), "metadata_targets": [r["event"] for r in targets],
                      "projection_rows": len(information), "fit_grid_checks": len(control_errors), "max_relative_error": max(control_errors),
                      "timeline_event_pass": {r["event"]: {d["detector"]: d["event_GPS_passes_all_required_public_timeline_flags"] for d in r["detectors"]} for r in details}}))


if __name__ == "__main__":
    main()
