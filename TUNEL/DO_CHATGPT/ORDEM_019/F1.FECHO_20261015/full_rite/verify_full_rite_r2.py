"""Read actual final outputs; never import candidate or replace its core.

Historical v393 is comparison only. This script neither executes another rite
nor changes any scientific output or gate. Result is an audit candidate.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
ROOT = Path(r"C:\IALD\Central de Patentes\work\rite394_20261015\r3")
BASE = UNIT.parent / "F1.TEMPO.V394" / "baseline"
TRIO = {"propext", "Classical.choice", "Quot.sound"}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def pin(path):
    return {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size}

def save(path, obj):
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()
    temp = path.with_name(path.name + ".tmp")
    if path.exists():
        raise FileExistsError(path)
    with temp.open("xb") as f:
        f.write(raw)
    assert temp.stat().st_size == len(raw)
    temp.rename(path)

def main():
    receipt = load(ROOT / "RITE_RECEIPT.json")  # absent means still running
    if receipt["exit_code"] != 0:
        raise RuntimeError("The actual full process did not exit zero")
    fresh = load(ROOT / "um_absoluto.json")
    core = fresh["core"]
    seal = load(ROOT / "um_absoluto_selo.json")
    old_core = load(BASE / "um_absoluto.json")["core"]
    old_seal = load(BASE / "um_absoluto_selo.json")
    kf, old_kf = core["kernel_formalization"], old_core["kernel_formalization"]
    ax = kf.get("axiom_report", {})
    ladder = core.get("external_ladder", {})
    qg = core.get("qg_closure", {})
    time_record = core.get("tempo_frequencia_v394", {})
    quad_names = [k for k in core if "quadratic" in k and k.endswith("v394")]
    quadratic = core[quad_names[0]] if len(quad_names) == 1 else {}
    true_lost = sorted(k for k, v in old_kf.items() if v is True and kf.get(k) is not True)
    old_verdicts = {k: v["verdict"] for k, v in old_core.items() if isinstance(v, dict) and "verdict" in v}
    verdict_changes = {k: {"old": v, "new": (core.get(k) or {}).get("verdict")}
                       for k, v in old_verdicts.items() if (core.get(k) or {}).get("verdict") != v}
    artifacts = []
    for suffix in ["json", "selo.json", "pt.tex", "en.tex", "pt.pdf", "en.pdf", "pt.txt", "en.txt", "forma_canonica.md", "manifest.md"]:
        p = ROOT / ("um_absoluto.json" if suffix == "json" else "um_absoluto_" + suffix)
        artifacts.append({**pin(p), "nonempty": p.stat().st_size > 0} if p.is_file()
                         else {"path": str(p), "missing": True})
    source_mismatches = []
    for relative, expected in kf.get("formal_files_sha256", {}).items():
        p = ROOT / "tgl_kernel" / relative
        if not p.is_file() or sha(p) != expected:
            source_mismatches.append(relative)
    network = core.get("rede_fock_v394", {})
    preaudit_path = HERE / "kh_patch_tests_r3" / "KH_N1_V394_PREAUDIT_CONTRACT_R3.json"
    preaudit = load(preaudit_path)
    if sha(preaudit_path) != "a86b73d64c49dd6d1feef4c70df4400e9d4c507ddbcfe8c131565db6bb0783c6":
        raise RuntimeError("Independent preaudit contract changed")
    checks = {
        "actual_process_exit_zero": receipt["exit_code"] == 0,
        "candidate_and_execution_copy_unchanged": receipt["candidate_original_unchanged"] and receipt["execution_copy_unchanged"],
        "external_inputs_unchanged": receipt["external_inputs_unchanged"],
        "no_unexpected_python_guard_refusals": receipt["guard_refusal_count"] == 0,
        "version_v394": seal.get("um_version") == "v394",
        "strict_formal_mode": kf.get("mode") == "strict",
        "real_lake_build": kf.get("lake_build_ok") is True and kf.get("build_returncode") == 0,
        "real_audit": kf.get("audit_file_ok") is True and kf.get("audit_returncode") == 0,
        "formal_all_verified": kf.get("all_verified") is True,
        "axioms_all_within_trio": bool(ax) and all(set(v or []) <= TRIO for v in ax.values()),
        "axiom_report_preserves_baseline_entries": set(old_kf.get("axiom_report", {})) <= set(ax),
        "source_forbidden_tokens_absent": kf.get("source_forbidden_tokens_absent") is True,
        "sorryAx_absent": kf.get("sorryAx_absent") is True,
        "formal_source_hashes_match_final_restored_sources": not source_mismatches,
        "prior_true_flags_preserved": not true_lost,
        "external_ladder_8107": ladder.get("all_verified") is True and ladder.get("n_theorems_clean") == ladder.get("n_theorems_expected") == 8107,
        "network_consumer_fresh_all_verified": network.get("all_verified") is True,
        "preaudit_report_count_matches": len(ax) == preaudit["axiom_report_entries"],
        "executed_file_identity_preserved": receipt.get("preserved_r3_alias_unchanged") is True and Path(receipt["execution_copy_path"]).name == "um_v394_final.py",
        "time_consumer_fresh_all_verified": time_record.get("all_verified") is True and time_record.get("runtime_executed") is True,
        "quadratic_consumer_fresh_all_verified": quadratic.get("all_verified") is True,
        "v393_consumers_preserved": all((core.get(k) or {}).get("all_verified") is True for k in ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393"]),
        "gate_verdict_unchanged": seal.get("qg_closure_verdict") == old_seal.get("qg_closure_verdict"),
        "gate_18_true_flags": sum(v is True for family in ["formal_flags", "physics_flags", "experiment_flags"] for v in qg.get(family, {}).values()) == 18,
        "identity_alpha_beta_unchanged": all(core.get(k) == old_core.get(k) for k in ["omega_I", "alpha", "beta"]),
        "selftest_passed": seal.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED",
        "whole_rite_checkpoint_switch_off": seal.get("rite_checkpoints", {}).get("switch_on") is False,
        "all_required_articles_present_nonempty": all(x.get("nonempty") for x in artifacts),
    }
    prefixes = ["TGLExt.TimeGraviton", "TGLExt.TimeQuadratic", "F1Fecho", "F1Rede"]
    report = {
        "status": "PASSA_CONTROLES_REQUER_RECONCILIAR_DELTAS" if all(checks.values()) else "FALHA_CONTROLE_VISIVEL",
        "time_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "checks": checks, "all_checks_passed": all(checks.values()),
        "actual_process_receipt": pin(ROOT / "RITE_RECEIPT.json"),
        "baseline_comparison_only": [pin(BASE / "um_absoluto.json"), pin(BASE / "um_absoluto_selo.json")],
        "axiom_report_count": len(ax), "new_named_axioms": {k: v for k, v in ax.items() if any(k.startswith(p) for p in prefixes)},
        "prior_true_flags_lost": true_lost, "formal_source_mismatches": source_mismatches,
        "historical_verdict_changes_to_reconcile": verdict_changes,
        "time_consumer": time_record, "quadratic_consumer_keys": quad_names, "quadratic_consumer": quadratic,
        "network_consumer": network,
        "independent_preaudit": pin(preaudit_path),
        "artifacts": artifacts, "script": pin(Path(__file__)),
        "no_import_or_scientific_rerun_in_this_checker": True,
        "no_canonical_installation_or_gate_change": True,
        "scope": "Actual integral rite in sandbox, not a new independent observation or nature confirmation. Historical data and existing quantum-pillar reuse retained as labelled by the unchanged program.",
    }
    out = HERE / "FULL_RITE_OUTPUT_REVIEW_R2.json"
    save(out, report)
    print(json.dumps({"checks_passed": sum(checks.values()), "checks": len(checks),
                      "failed": [k for k, v in checks.items() if not v],
                      "axioms": len(ax), "verdict_deltas": len(verdict_changes), "report": str(out)}, ensure_ascii=False))
    return 0 if all(checks.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
