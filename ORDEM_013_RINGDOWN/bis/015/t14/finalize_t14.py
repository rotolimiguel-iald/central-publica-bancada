"""Finalize the bounded T14 software measurement and conservative budget debit."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
WORK = ROOT / "ORDEM_013_RINGDOWN"
HERE = WORK / "bis" / "015" / "t14"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, value: dict) -> None:
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    tmp.write_bytes(data)
    if tmp.stat().st_size != len(data):
        raise IOError("short write")
    tmp.replace(path)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


if __name__ == "__main__":
    prereg = HERE / "T14_A_PRE_REG.json"
    pip = HERE / "T14_B_FINAL_PIP_v2.log"
    api = HERE / "T14_B_API_PROBE.json"
    effect = HERE / "T14_B_EFFECT_PROBE.json"
    original = WORK / "cache" / "t14_local_deps" / "src" / "pygsl_lite-0.1.8.tar.gz"
    upstream = "3213755c71da61e9629551e088530130d28e27048cd5f3ba48deb8165e6df6de"
    if sha(original) != upstream:
        raise ValueError("upstream pygsl source changed")
    if (HERE / "T14_B_FINAL_PIP_v2.rc").read_text().strip() != "0":
        raise ValueError("pip not successful")
    if (HERE / "T14_B_API_PROBE.rc").read_text().strip() != "0":
        raise ValueError("API probe failed")
    if (HERE / "T14_B_EFFECT_PROBE.rc").read_text().strip() != "0":
        raise ValueError("effect probe failed")
    ap = read(api)
    ef = read(effect)
    if len(ap["cases"]) != 3 or any(c["status"] != "FINITE_WAVEFORM" for c in ap["cases"]):
        raise ValueError("nonfinite API result")
    if ef["source_probe_sha256"] != sha(api):
        raise ValueError("effect references other probe")
    for field in ("dtau_vs_GR", "domega_vs_GR"):
        if not ef[field]["all_finite"] or ef[field]["relative_L2_whole_overlap"] <= 0:
            raise ValueError("deformation has no measured effect")
    first = datetime.fromisoformat(read(prereg)["registered_utc"])
    last = datetime.fromisoformat(ef["created_utc"])
    elapsed = (last - first).total_seconds()
    if not 0 < elapsed <= 7200:
        raise ValueError("T14 cap exceeded")
    hours = elapsed / 3600.0
    sources = [prereg, pip, api, effect, original, HERE / "T14_B_PATCH_RECEIPT.json", HERE / "T14_B_PATCH_RECEIPT_ERRATA.md"]
    result = {
        "status": "T14_INSTALL_AND_API_MEASURED_NO_PE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "version": "pyseobnr==0.3.7",
        "official_source": "https://pypi.org/project/pyseobnr/0.3.7/",
        "official_api": "https://waveforms.docs.ligo.org/software/pyseobnr/source/notebooks/pseob_example.html",
        "source_sdist_sha256": read(prereg)["source_sdist_sha256"],
        "sources": [{"relative_to_Chatgpt": relative(p), "sha256": sha(p)} for p in sources],
        "install_rc": 0,
        "finite_waveforms": 3,
        "dtau_relative_L2_whole_overlap": ef["dtau_vs_GR"]["relative_L2_whole_overlap"],
        "domega_relative_L2_whole_overlap": ef["domega_vs_GR"]["relative_L2_whole_overlap"],
        "cost_per_form_seconds": {c["label"]: c["wall_seconds"] for c in ap["cases"]},
        "warmup_notice": "GR first call contains import/JIT cost; later calls are warm-cache. Example parameters, not GW250114 PE cost.",
        "machine_hours_charged_conservative": hours,
        "accounting_statute": "START_OF_PREREG_TO_FINAL_EFFECT_RESULT_ELAPSED_UPPER_BOUND; includes idle gaps, not exact job union",
        "PE_posterior": False,
        "sigma_c": None,
        "gate_changed": False,
    }
    out = HERE / "T14_B_RESULT.json"
    write_new(out, result)

    old = WORK / "ORCAMENTO_015_v12.json"
    budget = read(old)
    if abs(budget["accounting"]["machine_hours_spent"] - 13.221245983976575) > 1e-9:
        raise ValueError("unexpected prior budget state")
    budget["registered_utc"] = datetime.now(timezone.utc).isoformat()
    budget["supersedes_sha256"] = sha(old)
    budget["witness_relative_to_Chatgpt"] = "TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v13.md"
    budget["accounting"]["intervals"].append({
        "target": "T14_PYSEOBNR_LOCAL_INSTALL_AND_API",
        "receipt_relative_to_Chatgpt": relative(out),
        "sha256": sha(out),
        "union_machine_hours": hours,
        "accounting_statute": result["accounting_statute"],
    })
    budget["accounting"]["machine_hours_spent"] += hours
    for item in budget["items"]:
        if item["item"] == "T14_pyseobnr":
            item["actual_machine_hours"] = hours
            item["job_started"] = True
            break
    else:
        raise ValueError("T14 item missing")
    budget["T14_measurement"] = {
        "receipt_relative_to_Chatgpt": relative(out),
        "sha256": sha(out),
        "status": result["status"],
    }
    budget["reallocation_reason"] = "T14 installation/API measurement; allocation unchanged; conservative elapsed upper-bound charged"
    budget["reallocation_changes"] = {}
    if budget["accounting"]["machine_hours_spent"] > budget["authorized_machine_hours"]:
        raise ValueError("budget exceeded")
    new = WORK / "ORCAMENTO_015_v13.json"
    write_new(new, budget)
    print(json.dumps({"T14_result": sha(out), "budget_v13": sha(new), "charged_hours": hours, "spent_total": budget["accounting"]["machine_hours_spent"]}))
