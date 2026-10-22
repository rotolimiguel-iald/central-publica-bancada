"""Combine T07 local search and public window-power data with visible QC limits."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    path = HERE / name
    return json.loads(path.read_bytes()), sha(path)


source, source_sha = load("T07_A_RESULT.json")
initial, initial_sha = load("T07_RHO_CATALOG_RESULT_v5.json")
salvage, salvage_sha = load("T07_RHO_SALVAGE_RESULT.json")
quality, quality_sha = load("T07_ONSOURCE_QUALITY_AUDIT.json")
plan, plan_sha = load("T07_DOWNLOAD_PLAN_v3.json")
sup, sup_sha = load("T07_SUPPLEMENT_PLAN.json")
alt, alt_sha = load("T07_ALTERNATE_PLAN.json")
audit = {(r["event"], r["detector"]): r for r in quality["rows"]}
initial_by = {r["event"]: r for r in initial["rows"]}
salvage_by = {r["event"]: r for r in salvage["rows"]}
events = [r["event"] for r in initial["rows"]]
events += [r["event"] for r in plan["skipped"] if r["event"] not in events]
assert len(events) == 33 and len(set(events)) == 33
rows = []
for event in events:
    brief = salvage_by.get(event) if initial_by.get(event, {}).get("status") == "MEASUREMENT_FAILED" else initial_by.get(event)
    if brief is None:
        rows.append({"event": event, "status": "NO_REGISTERED_COMPLETE_OFFSOURCE_FRAME", "rho_power": None})
        continue
    if not brief["status"].startswith("MEASURED_"):
        rows.append({"event": event, "status": brief["status"], "rho_power": None,
                     "initial_error": initial_by.get(event, {}).get("error"),
                     "salvage_sha256": brief.get("result_sha256")})
        continue
    directory = "results_rho_salvage" if event in salvage_by else "results_rho"
    path = HERE / directory / (event + ".json")
    detail = json.loads(path.read_bytes())
    if brief["result_sha256"] != sha(path):
        raise ValueError("DETAIL_HASH_DIFFERS:" + event)
    kept, rejected = [], []
    for detector in detail["detectors"]:
        qc = audit[(event, detector["detector"])]
        if qc["result_sha256"] != sha(path):
            raise ValueError("QUALITY_AUDIT_DETAIL_MISMATCH:" + event)
        if qc["all_required_masks_good"] and qc["samples_all_finite"]:
            kept.append(detector)
        else:
            rejected.append({"detector": detector["detector"],
                             "reason": "ONSOURCE_DQ_OR_NONFINITE"})
    if not kept:
        rows.append({"event": event, "status": "ONSOURCE_QC_NO_DETECTOR", "rho_power": None,
                     "result_sha256": sha(path), "rejected": rejected})
        continue
    dof = sum(d["noise_degrees_of_freedom"] for d in kept)
    excess = sum(d["norm_squared"] for d in kept) - dof
    rho = math.sqrt(excess) if excess > 0 else None
    se = math.sqrt(2 * dof + 4 * excess) / (2 * rho) if rho and 2 * dof + 4 * excess > 0 else None
    outliers = [d["detector"] for d in kept
                if audit[(event, d["detector"])]["outlier_diagnostic_ratio_gt_10_not_exclusion_rule"]]
    rows.append({
        "event": event, "status": "MEASURED_POSITIVE_POWER_EXCESS" if rho is not None else "MEASURED_NONPOSITIVE_POWER_EXCESS_NO_REAL_RHO",
        "result_sha256": sha(path),
        "reference_method": detail["reference_method"],
        "detectors_used": [d["detector"] for d in kept],
        "detectors_discarded_for_onsource_quality": rejected,
        "detectors_skipped_before_onsource_audit": detail.get("skipped_detectors", []),
        "noise_source_by_detector": {d["detector"]: d.get("noise_source", "original") for d in kept},
        "heldout_chi2_median_by_detector": {d["detector"]: d["held_out_reduced_chisquare_median"] for d in kept},
        "whitened_power_minus_noise_dof": excess,
        "rho_power": rho,
        "rho_gaussian_stationary_se": se,
        "descriptive_power_outlier_detectors_ratio_gt_10": outliers,
        "rho_interpretation": "finite-window power excess estimator; not matched-filter SNR, z or detection sigma",
    })

measured = [r for r in rows if r["status"].startswith("MEASURED_")]
positive = [r for r in measured if r["rho_power"] is not None]
negative = [r for r in measured if r["rho_power"] is None]
assert len(rows) == 33 and len(measured) == 31
f4 = json.loads((CHAT / "ORDEM_013_RINGDOWN" / "bis" / "F4_GW250114_WINDOW_POWER_NORM.json").read_bytes())
gw = next(r for r in rows if r["event"] == "GW250114_082203")
f4_rel_diff = abs(gw["rho_power"] - f4["network_rho_estimate"]) / f4["network_rho_estimate"]
assert f4_rel_diff < 1e-6
start = datetime.fromisoformat(json.loads((HERE / "T07_START.json").read_bytes())["registered_utc"].replace("Z", "+00:00"))
end = datetime.now(timezone.utc)
wall_hours = (end - start).total_seconds() / 3600
assert wall_hours < 2
result = {
    "status": "T07_MEDIDA_PARTIAL_NO_ZFREE_NO_PHYSICAL_SIGMA",
    "created_utc": end.isoformat(),
    "T07_machine_hours_conservative_start_to_finalizer": wall_hours,
    "source_search_sha256": source_sha,
    "initial_rho_sha256": initial_sha,
    "salvage_sha256": salvage_sha,
    "onsource_quality_sha256": quality_sha,
    "download_plan_v3_sha256": plan_sha,
    "supplement_plan_sha256": sup_sha,
    "alternate_plan_sha256": alt_sha,
    "count_registered": len(rows), "count_power_measured": len(measured),
    "count_positive_excess_rho_defined": len(positive),
    "count_nonpositive_excess_rho_undefined": len(negative),
    "count_unmeasured": len(rows) - len(measured),
    "count_descriptive_extreme_power_events": sum(bool(r.get("descriptive_power_outlier_detectors_ratio_gt_10")) for r in measured),
    "F4_GW250114_rho_reference": f4["network_rho_estimate"],
    "F4_GW250114_rho_this_run": gw["rho_power"],
    "F4_rho_relative_difference": f4_rel_diff,
    "rows": rows,
    "z_free_per_reading": None,
    "N90_reexpressed_with_measured_rho": None,
    "reason_not_zfree_or_N90": "All four Powell searches reached maxfev; local candidate is upper bound on global minimum mismatch, not calibrated z_free. Power-rho estimates and source-search residuals have different objectives and cannot be combined into N90 without calibration.",
    "statistical_scope": "Calibrating pre-specified events using public strain and same algebraic F4 whitened-power norm. Posterior-median time proxies, recalculated per-event PSD, detector subsets, alternative off-source age, stationarity and gross power outliers limit interpretation. No matched-filter SNR, physical detection sigma or gate movement.",
    "gate_changed": False,
}
target = HERE / "T07_FINAL_RESULT.json"
raw = (json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
out_sha = sha(target)

lines = [
    "[REAL — medição de potência; OPEN — z_free, N90 e significância física]",
    "",
    "# ORDEM 015 / T07 — veredito de bancada",
    "",
    f"Foram cadastrados 33 eventos; a norma de potência na janela 10 tM foi medida em **{len(measured)}**. Em **{len(positive)}** o excesso foi positivo e a raiz define rho; em **{len(negative)}** o excesso foi não positivo e rho fica indefinido pelo estimador F4. Dois eventos ficaram sem medida válida. Isso não é uma tabela de 31 SNRs de detecção.",
    "",
    f"O controle GW250114 deu rho={gw['rho_power']:.9f}, contra F4={f4['network_rho_estimate']:.9f}, desvio relativo={f4_rel_diff:.3g}. A W foi recalculada pelo mesmo algoritmo, não copiada do npz congelado; a referência temporal dos demais eventos vem da mediana do posterior público. Um detector on-source falhou na máscara DQ e foi retirado da soma com registro. Dois eventos exibem potência extrema descritiva (>10 por grau de liberdade em um detector); permanecem flagados, sem interpretação como sinal.",
    "",
    "As quatro buscas de fonte livre terminaram com candidatos finitos, mas todos os otimizadores atingiram maxfev. Por isso z_free e N90 reescrito permanecem **não pagos**. O resultado T07 é parcial e **não fornece sigma**, Bayes, exclusão de GR ou alteração do gate.",
    "",
    f"Tempo de máquina conservador: {wall_hours:.6f} h; JSON final `{out_sha}`; busca de fonte `{source_sha}`; catálogo inicial `{initial_sha}`; recuperação `{salvage_sha}`; qualidade on-source `{quality_sha}`. Cada linha do JSON final remete ao resultado por evento e às fontes custodidas.",
    "",
    "| Evento | Detectores após QC | Excesso | rho de potência | Observação |",
    "|---|---|---:|---:|---|",
]
for row in rows:
    if row["status"].startswith("MEASURED_"):
        notes = []
        if row["descriptive_power_outlier_detectors_ratio_gt_10"]:
            notes.append("POTÊNCIA EXTREMA: " + ",".join(row["descriptive_power_outlier_detectors_ratio_gt_10"]))
        if row["detectors_discarded_for_onsource_quality"]:
            notes.append("DQ rejeitou " + ",".join(d["detector"] for d in row["detectors_discarded_for_onsource_quality"]))
        if row["detectors_skipped_before_onsource_audit"]:
            notes.append("rede parcial")
        rho_text = f"{row['rho_power']:.5g}" if row["rho_power"] is not None else "indef."
        lines.append(f"| {row['event']} | {','.join(row['detectors_used'])} | {row['whitened_power_minus_noise_dof']:.5g} | {rho_text} | {'; '.join(notes)} |")
    else:
        lines.append(f"| {row['event']} | — | — | indef. | {row['status']} |")

handoff = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_MEDIDA_T07_portao_e_rho.md"
with handoff.open("xb") as handle:
    handle.write(("\n".join(lines) + "\n").encode())
print(json.dumps({"final_sha256": out_sha, "handoff_sha256": sha(handoff),
                  "machine_hours": wall_hours, "power_measured": len(measured),
                  "rho_defined": len(positive), "rho_undefined": len(negative)}))
