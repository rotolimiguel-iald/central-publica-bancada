"""Audit reusable F4.3 power inputs without reading the D strain."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
V1 = Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.json")
P220 = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\ramo_b\pre_registro\PODER_CEGO_RAMO_B_v2.json")
O4 = Path(r"C:\IALD\Bancada_Um\fontes_externas\gwosc_o4\GWOSC_O4_32S_V1.manifest.json")
C7 = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C7_INJECTION_REPRODUCTION_v3_2\MANIFEST.json")
PSD = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\PSD_CONTROLS.json")
QNM = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\QNM_GRID.json")
V3 = HERE / "PREREGISTRO_F4_3_V3.json"
PREVIOUS_RESULT = HERE / "RESULTADO_C1_F43_R4_20261008.json"
PREVIOUS_MAP = HERE / "MAPA_C1_R4_F43_20261008.json"
INVENTORY = HERE / "INVENTARIO_INSUMOS_PODER_F43_R4_20261008.json"
RESULT = HERE / "RESULTADO_C1_F43_R4_V2_20261008.json"
MAP = HERE / "MAPA_C1_R4_F43_V2_20261008.json"


def pin(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def new_json(path: Path, value: dict) -> None:
    if path.exists():
        raise FileExistsError(path)
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.stat().st_size != len(data):
        raise IOError("short write")
    os.replace(temp, path)


def main() -> None:
    for path in (INVENTORY, RESULT, MAP):
        if path.exists():
            raise FileExistsError(path)
    sources = {
        "V1_Ramo_B": pin(V1),
        "PODER_CEGO_220_V1": pin(P220),
        "O4_32S_archive_manifest": pin(O4),
        "C7_injection_bundle": pin(C7),
        "PSD_controls": pin(PSD),
        "QNM_grid": pin(QNM),
        "F43_V3": pin(V3),
    }
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    o4 = json.loads(O4.read_text(encoding="utf-8"))
    c7 = json.loads(C7.read_text(encoding="utf-8"))
    v3 = json.loads(V3.read_text(encoding="utf-8"))
    fields = v3["manifest_from_v2"]["complete_before_power"]
    if len(fields) != 13 or any(v3["manifest_from_v2"][key] is not None for key in fields):
        raise RuntimeError("F4.3 manifest state changed; audit again")
    eligible = v1["conjuntos"]["D"]["eventos_elegiveis"]
    holds = v1["conjuntos"]["D"]["com_data_quality_hold"]
    if len(eligible) != 14 or len(holds) != 4:
        raise RuntimeError("V1 candidate counts changed")
    where = {
        "event_list_final_pinned": "V1 gives 14 eligible candidates and 4 holds, but says event-by-event freeze is future; final D list is not pinned for F4.3.",
        "event_list_hash": "V1 file hash pins the selection rule/candidates, not the future final list after holds.",
        "psd_per_event_and_detector": "O4 32 s archive exists; C7 carries generic O4/other design PSD and one off-source example. No per-event/detector PSD selection for 220+440 D.",
        "psd_hashes": "C7 pins generic PSD asset hashes; no map assigning a chosen PSD hash to every D event/detector.",
        "analysis_windows": "O4 manifest window_s=32 names extraction windows; not ringdown start/end/fit windows for the F4.3 PE.",
        "window_hashes": "No per-event ringdown fit-window hashes chosen for F4.3.",
        "priors_and_bounds": "V1 and C7 contain prior/control families for 220/IMR; no frozen joint 220+440 shared-source bounds under V1 clock.",
        "prior_hash": "No chosen F4.3 joint-prior artifact hash.",
        "start_time_rule": "V1 C4 varies t0; no single F4.3 decision start-time rule and sensitivity grid fixed for D.",
        "waveform_family_and_version": "V1 names a pSEOB single-220 IMR instrument; C7 uses earlier waveform families. The 440 deformation with common M_f,chi_f is INPUT and no chosen implementation/version exists.",
        "waveform_hash": "QNM grid is pinned, but not the executable joint 220+440 V1-clock waveform/likelihood.",
        "detector_covariance": "C7 older controls use independent Gaussian quadratures; V1 C7 groups H1/L1 by event. No covariance choice validated for this joint F4.3 experiment.",
        "injection_seed_and_null_repetitions": "Older C7 injection bundle is not an F4.3 seed/count. No frozen seed, null count or exact-power campaign for D.",
    }
    if set(where) != set(fields):
        raise RuntimeError("field inventory mismatch")
    inventory = {
        "unit": "F4.3",
        "status": "REUSE_AUDIT__EXACT_JOINT_POWER_INPUTS_INCOMPLETE",
        "sources": sources,
        "read_scope": "Only manifests, protocol JSON and existing power JSON were read; no D strain, posterior or PE was opened.",
        "v1_D_candidates": len(eligible),
        "v1_D_holds": len(holds),
        "o4_archive_window_s": o4.get("window_s"),
        "c7_status": c7.get("status"),
        "p220_scope": "PODER_CEGO_RAMO_B_v2 is 220-only/older A-B-C sigma-and-spin power; cannot transport to F4.3 joint 220+440 D power.",
        "fields": [{"name": name, "status": "NOT_SATISFIED_FOR_F43", "reuse_and_gap": where[name]} for name in fields],
        "conclusion": "F4.3 exact synthetic injection power on D cannot be measured honestly from the frozen inputs available now; AWAITING_POWER and operator request suspended.",
    }
    new_json(INVENTORY, inventory)
    result = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    result["evidence_revision"] = "V2_ADD_INPUT_AUDIT"
    result["previous_result"] = pin(PREVIOUS_RESULT)
    result["input_inventory"] = pin(INVENTORY)
    result["map_original_rejected_schema"] = pin(PREVIOUS_MAP)
    result["remaining"][0] = "F4.3 exact D-set joint injection power NOT_MEASURED: all 13 mandatory manifest fields have only partial or inapplicable older sources, as documented field by field in input_inventory"
    new_json(RESULT, result)
    old_map = json.loads(PREVIOUS_MAP.read_text(encoding="utf-8"))
    old_map["metodo"] += " Inventário por arquivo/hash dos 13 campos obrigatórios, sem leitura de strain/posterior."
    old_map["resultado"] += " O V1 fornece 14 candidatos/4 holds; C7/O4 fornecem material histórico parcial, sem escolher PSD/janelas/priors/waveform conjunta para D."
    old_map["artefatos"] = [
        {"caminho": p["path"], "bytes": p["bytes"], "sha256": p["sha256"]}
        for p in [pin(V3), pin(INVENTORY), pin(RESULT), pin(HERE / "ADENDO_C1_R4_F43_20261008.md"), pin(HERE / "PODER_ANALITICO_F43_R4_20261008.json")]
    ]
    old_map["nota"] = "Corrige a seq 842. O primeiro input MAPA_C1_R4_F43_20261008.json falhou na validação do esquema (path em vez de caminho) e não foi registrado; preservado por hash. Poder F4.3 D segue não medido."
    new_json(MAP, old_map)
    print(json.dumps({"inventory": pin(INVENTORY), "result": pin(RESULT), "map": pin(MAP)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
