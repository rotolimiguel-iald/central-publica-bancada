"""Custody F's measured diagnostic and return unused machine time to T10."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

here = Path(__file__).resolve().parent
ring = here.parents[2]
chatgpt = ring.parent
tunnel = chatgpt / "TUNEL" / "DO_CHATGPT"
run = ring / "cache" / "E3_KERR220_DTAU_F_015"
data = run / "public_psd"
branch = here / "branch_f"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def publish(path: Path, contents: bytes) -> None:
    with path.open("xb") as out:
        out.write(contents)
        out.flush()
        os.fsync(out.fileno())
    assert path.read_bytes() == contents


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()


def main() -> None:
    budget_path = ring / "ORCAMENTO_015_v5.json"
    next_path = ring / "ORCAMENTO_015_v6.json"
    auth_path = ring / "bis" / "E3_KERR_F_AUTHORIZATION_015.json"
    manifest_path = ring / "bis" / "e3_kerr_dtau_f_015" / "MANIFEST_v2.json"
    posterior_path = data / "PAIRED_POSTERIOR.npz"
    conv_path = data / "CONVERGENCE.json"
    comp_path = data / "COMPARISON.json"
    cost_path = run / "COST.json"
    diag_path = branch / "DIAGNOSTIC.json"
    result_path = branch / "RESULT.json"
    note_path = tunnel / "ENTREGA_015_MEDIDA_T04_F_DIAGNOSTIC.md"
    witness_path = tunnel / "ENTREGA_015_ORCAMENTO_015_v6.md"
    for path in (next_path, result_path, note_path, witness_path):
        if path.exists():
            raise FileExistsError(path)
    budget = json.loads(budget_path.read_bytes())
    auth = json.loads(auth_path.read_bytes())
    cost = json.loads(cost_path.read_bytes())
    conv = json.loads(conv_path.read_bytes())
    comp = json.loads(comp_path.read_bytes())
    diag = json.loads(diag_path.read_bytes())
    assert auth["manifest_sha256"] == cost["manifest_sha256"] == sha(manifest_path)
    assert len(cost["runs"]) == 1
    one = cost["runs"][0]
    assert one["variant"] == "public_psd" and one["returncode"] == 0 and one["cutoff"] is False
    assert one["cleanup"]["group_absent"] is True and cost["cleanup"]["group_absent"] is True
    assert 0 < cost["wall_seconds"] <= cost["ceiling_seconds"] == 7200
    assert conv["status"] == "CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW"
    assert conv["accepted_for_analysis"] is True
    assert conv["delta_logz"] <= conv["threshold"]
    assert conv["ess"] >= conv["minimum_ess"]
    assert conv["posterior_samples"] >= 1000
    assert conv["ncall"] < conv["cost"]["maxcall_nominal"]
    assert comp["posterior_sha256"] == sha(posterior_path)
    assert comp["samples"] == conv["posterior_samples"] == diag["samples"]
    assert comp["sigma_eligible"] is False and comp["z_calibrated"] is None
    assert diag["sigma_eligible"] is False and diag["z_calibrated"] is None
    assert diag["input_sha256"]["posterior"] == sha(posterior_path)
    assert diag["input_sha256"]["convergence"] == sha(conv_path)
    assert diag["input_sha256"]["comparison"] == sha(comp_path)
    hours = cost["wall_seconds"] / 3600
    items = {item["item"]: item for item in budget["items"]}
    f = items["T04_branch_F"]
    t10 = items["T10_calibration"]
    assert f["job_started"] is False and f["allocated_machine_hours"] >= hours
    assert t10["job_started"] is False
    unused = f["allocated_machine_hours"] - hours
    result = {
        "status": "F_DIAGNOSTIC_CONVERGED_PENDING_INDEPENDENT_NUMERIC_REVIEW",
        "event": "GW250114_082203",
        "variant": "public_psd",
        "posterior_accepted_for_descriptive_analysis": True,
        "sigma_eligible": False,
        "gate_changed": False,
        "single_220_free_Mf_af_not_identifiable": True,
        "controller_exit_code": 0,
        "child_exit_code": one["returncode"],
        "child_process_group_absent": one["cleanup"]["group_absent"],
        "machine_hours": hours,
        "wall_seconds": cost["wall_seconds"],
        "children_cpu_seconds": cost["children_cpu_seconds"],
        "sampler_ncall": conv["ncall"],
        "delta_logz": conv["delta_logz"],
        "ess": conv["ess"],
        "posterior_samples": conv["posterior_samples"],
        "dtau220_q05_q50_q95": diag["dtau220_q05_q50_q95"],
        "corr_dtau220_Mf": diag["corr_dtau220_Mf"],
        "corr_dtau220_af": diag["corr_dtau220_af"],
        "sha256": {"authorization": sha(auth_path), "manifest": sha(manifest_path),
                   "cost": sha(cost_path), "convergence": sha(conv_path),
                   "comparison": sha(comp_path), "diagnostic": sha(diag_path),
                   "posterior": sha(posterior_path), "run_log": sha(data / "RUN.log")},
    }
    result_bytes = json_bytes(result)
    result_sha = hashlib.sha256(result_bytes).hexdigest()
    now = datetime.now(timezone.utc).isoformat()
    next_budget = copy.deepcopy(budget)
    next_budget["registered_utc"] = now
    next_budget["supersedes_sha256"] = sha(budget_path)
    next_budget["witness_relative_to_Chatgpt"] = "TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v6.md"
    newest = {item["item"]: item for item in next_budget["items"]}
    new_f = newest["T04_branch_F"]
    new_t10 = newest["T10_calibration"]
    new_f.update(allocated_machine_hours=hours, actual_machine_hours=hours,
                 job_started=True, status=result["status"], final_receipt_sha256=result_sha)
    new_t10["allocated_machine_hours"] += unused
    assert abs(sum(item["allocated_machine_hours"] for item in next_budget["items"])
               - next_budget["authorized_machine_hours"]) < 1e-9
    next_budget["allocated_machine_hours"] = next_budget["authorized_machine_hours"]
    next_budget["unallocated_machine_hours"] = 0.0
    next_budget["accounting"]["intervals"].append({
        "target": "T04_branch_F_DIAGNOSTIC",
        "receipt_relative_to_Chatgpt": result_path.relative_to(chatgpt).as_posix(),
        "sha256": result_sha,
        "union_machine_hours": hours,
        "CPU_seconds": cost["children_cpu_seconds"],
    })
    next_budget["accounting"]["machine_hours_spent"] += hours
    next_budget["reallocation_reason"] = "F diagnostic completed under 2h; unused F allocation reassigned to T10 calibration"
    next_budget["reallocation_changes"] = {
        "T04_branch_F": {"old": f["allocated_machine_hours"], "new": hours},
        "T10_calibration": {"old": t10["allocated_machine_hours"],
                            "new": new_t10["allocated_machine_hours"]},
    }
    next_budget["prerequisites_unpaid"] = [x for x in budget.get("prerequisites_unpaid", [])
                                           if x != "T04_F_NEW_INSTRUMENT_BUILD_AND_WITNESS"]
    next_budget["F_diagnostic"] = {
        "result_sha256": result_sha,
        "posterior_sha256": sha(posterior_path),
        "descriptive_only": True,
        "sigma_eligible": False,
        "independent_numeric_review": "QUEUED_NOT_YET_ACCEPTED",
    }
    next_budget["gate_changed"] = False
    budget_bytes = json_bytes(next_budget)
    budget_sha = hashlib.sha256(budget_bytes).hexdigest()
    witness = (
        "[REAL] T04-F concluído; tempo não gasto realocado para T10.\n\n"
        f"allocation_sha256: {budget_sha}\nregistered_utc: {now}\n\n"
        f"Abertura016SHA256: {sha(tunnel / 'ENTREGA_016_ABERTURA_operador.md')}. "
        f"Pai v5 SHA256 {sha(budget_path)}. F RESULT SHA256 {result_sha}; "
        f"F {hours:.12f} h; devolução para T10 {unused:.12f} h. "
        f"Teto total {budget['authorized_machine_hours']:.12f} h, gasto acumulado "
        f"{next_budget['accounting']['machine_hours_spent']:.12f} h. "
        "Posterior F é diagnóstico, sem σ nem gate; revisão numérica externa pendente.\n"
    )
    note = (
        "[REAL] T04-F: MEDIDA do segundo instrumento Kerr com δτ220, NÃO-CEGO.\n\n"
        f"Abertura016SHA256: {sha(tunnel / 'ENTREGA_016_ABERTURA_operador.md')}. "
        f"ORDEM015 SHA256: {sha(chatgpt / 'TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md')}. "
        f"RESULT SHA256: {result_sha}; COST SHA256: {sha(cost_path)}; "
        f"CONVERGENCE SHA256: {sha(conv_path)}; COMPARISON SHA256: {sha(comp_path)}; "
        f"posterior NPZ SHA256: {sha(posterior_path)}; log SHA256: {sha(data / 'RUN.log')}.\n\n"
        f"Controlador e filho rc 0; grupo ausente; parede {cost['wall_seconds']:.6f} s "
        f"({hours:.12f} h), CPU-filhos {cost['children_cpu_seconds']:.6f} s. "
        f"ncall {conv['ncall']}; ΔlogZ {conv['delta_logz']:.9f} ≤ {conv['threshold']}; "
        f"ESS {conv['ess']:.3f}; amostras {conv['posterior_samples']}. "
        f"δτ220 q05/q50/q95 = {diag['dtau220_q05_q50_q95']}; "
        f"corr(δτ,Mf)={diag['corr_dtau220_Mf']:.6f}, "
        f"corr(δτ,af)={diag['corr_dtau220_af']:.6f}. "
        "Essas correlações reforçam a limitação de um modo; não são um teste de identidade física. "
        "O observável difere do pSEOB IMR registrado, e a comparação com o posterior externo "
        "é descritiva: z_calibrated=null, sigma_eligible=false. Revisão numérica independente "
        "ainda pendente; nenhum σ ou gate moveu.\n\n"
        "Comando de reprodução: /opt/lal_env/bin/python -B "
        "bis/e3_kerr_dtau_f_015/controller.py --authorization "
        "ORDEM_013_RINGDOWN/bis/E3_KERR_F_AUTHORIZATION_015.json; uma execução, sem relançamento. "
        "Axiomas Lean: N/A. Próximo ramo: R3 PASSO 12b.\n"
    )
    publish(result_path, result_bytes)
    publish(note_path, note.encode())
    publish(witness_path, witness.encode())
    publish(next_path, budget_bytes)
    assert sha(result_path) == result_sha and sha(next_path) == budget_sha
    print(json.dumps({"status": "T04_F_DIAGNOSTIC_RECORDED", "result_sha256": result_sha,
                      "budget_v6_sha256": budget_sha, "machine_hours": hours,
                      "unused_to_T10_hours": unused, "note_sha256": sha(note_path)}))


if __name__ == "__main__":
    main()
