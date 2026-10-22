"""Pin the additive F2.3 Temperature correction without altering earlier evidence."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "RESULTADO_TEMPERATURA_RESSALVAS_C1_20261008.json"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F2.3_F1.1_temperatura\AUDITORIA_F2_3_F1_1_temperatura_C1_abe2cbdf.md")
PALAVRA = Path(r"C:\IALD\Central de Patentes\work\leitura_cria_o_objeto_07out\Palavra.lean")
PINNED = {
    "c1_audit": AUDIT,
    "original_standalone": ROOT / "LiganteLeiCampoCurvoTemperaturaStandalone.lean",
    "original_standalone_olean": ROOT / "LiganteLeiCampoCurvoTemperaturaStandalone.olean",
    "new_source": ROOT / "LiganteLeiCampoCurvoTemperaturaSemBoostOcioso.lean",
    "new_sandbox_source": ROOT / "kernel/TGLExt/LiganteLeiCampoCurvoTemperaturaSemBoostOcioso.lean",
    "new_olean": ROOT / "LiganteLeiCampoCurvoTemperaturaSemBoostOcioso_C1_V2_20261008.olean",
    "original_preliminary_source": ROOT / "kernel/TGLExt/LiganteLeiCampoCurvoTemperatura.lean",
    "historical_attempt_1": ROOT / "BUILD_TEMPERATURA_ATTEMPT.log",
    "historical_attempt_2": ROOT / "BUILD_TEMPERATURA_ATTEMPT_2.log",
    "historical_attempt_3": ROOT / "BUILD_TEMPERATURA_ATTEMPT_3.log",
    "historical_1372_build": ROOT / "BUILD_TEMPERATURA_FINAL.log",
    "historical_1372_axioms": ROOT / "AXIOMAS_TEMPERATURA.txt",
    "historical_1372_attempt": ROOT / "BUILD_TEMPERATURA_STANDALONE_ATTEMPT.log",
    "failed_fresh_build_receipt": ROOT / "BUILD_TEMPERATURA_C1_ACT_20261008.json",
    "failed_fresh_build_log": ROOT / "BUILD_TEMPERATURA_C1_ACT_20261008.log",
    "green_fresh_build_receipt": ROOT / "BUILD_TEMPERATURA_C1_ACT_V2_20261008.json",
    "green_fresh_build_log": ROOT / "BUILD_TEMPERATURA_C1_ACT_V2_20261008.log",
    "diagnostic_adendo": ROOT / "ADENDO_TEMPERATURA_DIAGNOSTICO.md",
    "diagnostic_adendo_prior_backup": ROOT / "ADENDO_TEMPERATURA_DIAGNOSTICO.md.bak_20261008_114746",
    "diagnostic_adendo_second_backup": ROOT / "ADENDO_TEMPERATURA_DIAGNOSTICO.md.bak_20261008_115046",
    "diagnostic_adendo_first_append_receipt": ROOT / "ADENDO_TEMPERATURA_ERRATA_C1_RECEIPT_20261008.json",
    "diagnostic_adendo_scope_receipt": ROOT / "ADENDO_TEMPERATURA_PRECISAO_MEMORIA_RECEIPT_20261008.json",
    "joint_memory_receipt": ROOT / "MEMORIA_ERRATA_AUDITORIA_TEMPERATURA_F11_20261008.json",
    "palavra_candidate": PALAVRA,
}


def pin(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


if __name__ == "__main__":
    if RESULT.exists():
        raise FileExistsError(RESULT)
    if any(not path.is_file() for path in PINNED.values()):
        raise RuntimeError("A required artifact is absent")
    pins = {name: pin(path) for name, path in PINNED.items()}
    if pins["original_preliminary_source"]["sha256"] != "454fb4f8581007e492552b0bb955b21df7e88851e39945d36e053182739c4e43":
        raise RuntimeError("Preliminary source pin differs")
    if pins["palavra_candidate"]["sha256"] != "33184b49a8bba7e754a66096a89ebeeef44e79dab00c22f49f7af77f0e5400c7":
        raise RuntimeError("PALAVRA candidate pin differs")
    if pins["new_source"]["sha256"] != pins["new_sandbox_source"]["sha256"]:
        raise RuntimeError("New source differs from sandbox source")
    if len({pins[key]["sha256"] for key in ("historical_1372_build", "historical_1372_axioms", "historical_1372_attempt")}) != 1:
        raise RuntimeError("Historical 1372-byte transcripts unexpectedly differ")
    old = (ROOT / "LiganteLeiCampoCurvoTemperaturaStandalone.lean").read_text(encoding="utf-8")
    new = (ROOT / "LiganteLeiCampoCurvoTemperaturaSemBoostOcioso.lean").read_text(encoding="utf-8")
    if not all(field in old for field in ("  observer_boost :", "  observer_boost_eq :")) or any(field in new for field in ("  observer_boost :", "  observer_boost_eq :")):
        raise RuntimeError("Unused observer boost field removal not verified")
    failure = json.loads((ROOT / "BUILD_TEMPERATURA_C1_ACT_20261008.json").read_text(encoding="utf-8"))
    success = json.loads((ROOT / "BUILD_TEMPERATURA_C1_ACT_V2_20261008.json").read_text(encoding="utf-8"))
    if failure["exit_code"] != 1 or success["exit_code"] != 0 or success["olean_sha256"] != pins["new_olean"]["sha256"]:
        raise RuntimeError("Fresh build statuses or olean pin differ")
    transcript = (ROOT / "BUILD_TEMPERATURA_C1_ACT_V2_20261008.log").read_text(encoding="utf-8")
    reports = re.findall(r"depends on axioms: \[([^]]+)\]", transcript, flags=re.S)
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    if len(reports) != 10 or any({part.strip() for part in report.split(",")} != allowed for report in reports):
        raise RuntimeError("The ten axiom reports do not contain exactly the allowed trio")
    if re.search(r"\berror:|\bwarning:|sorryAx", transcript, flags=re.I):
        raise RuntimeError("Green transcript has error, warning, or sorryAx")
    appendix = json.loads((ROOT / "ADENDO_TEMPERATURA_PRECISAO_MEMORIA_RECEIPT_20261008.json").read_text(encoding="utf-8"))
    if appendix["after_sha256"] != pins["diagnostic_adendo"]["sha256"]:
        raise RuntimeError("Current adendo does not match final byte backup receipt")
    result = {
        "unit": "F2.3",
        "stage": "temperature_c1_reservations_additive",
        "source_status": "sandbox candidate; c1 APROVA_COM_RESSALVAS; NOT integrated in v392",
        "main_curved_field_stone": "LiganteLeiCampoCurvoAuditoriaC1.lean remains the c1 integration candidate",
        "proof_status": "[REAL] Lean build exit 0; ten printed declarations use only propext, Classical.choice, Quot.sound; zero compiler error/warning/sorryAx",
        "semantic_status": "[REAL by c1 probes] T4 corollary, T3 thermal bridge idle, T1/T2/T6 rate free and observer fields unused, T5 hyperbolic face nonperiodic, T8 existing H2/Unruh/Clausius wiring; Fock/Maxwell inhabitants not exhibited",
        "prior_independent_semantic_audit_claim": "[DECLARADO] earlier claim lacked an artifact; later c1 audit is pinned separately",
        "fresh_builds": {"first_unicode_path_attempt_exit": failure["exit_code"], "ascii_alias_attempt_exit": success["exit_code"], "ascii_alias_elapsed_seconds": success["elapsed_seconds"], "axiom_report_count": len(reports), "axioms_each": sorted(allowed)},
        "variant": "New source removes only unused observer_boost and observer_boost_eq fields and adjusts their docstrings; κ remains arbitrary and H3 remains named",
        "coexistence": "Standalone repeats branch C declarations; not co-importable in one Lean environment",
        "process_note": "Event 278 was anotar without hash/evidence/seq; 04:58 memory write was Temperature, branch C was 04:29; this deliverable's joint memory correction has separate receipt",
        "no_gate_move": True,
        "artifacts": pins,
    }
    data = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with RESULT.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"result": str(RESULT), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "pinned_artifacts": len(pins), "axiom_reports": len(reports)}, ensure_ascii=False))
