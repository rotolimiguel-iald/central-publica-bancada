"""Preserve the actual phase-coordinate validation and live inference handle."""
from pathlib import Path
from datetime import datetime, timezone
import json
from record_source_evidence_start import safe, sha

ROOT = Path(__file__).resolve().parent
BASE = ROOT/"cache/source_evidence"


def main():
    receipt = ROOT/"C5_PHASE_INTEGRATION_START.json"
    if receipt.exists():
        raise FileExistsError("Create-once progress record")
    validation = json.loads((BASE/"PEAK_PHASE_COORDINATES_VALIDATION.json").read_bytes())
    proposal = json.loads((BASE/"phase_runs/PROPOSAL_VALIDATION.json").read_bytes())
    progress = json.loads((BASE/"phase_runs/IMRPhenomXPHM_seed130801_N1024/PROGRESS.json").read_bytes())
    if validation["status"] != "PASS_PRIOR_PRESERVING_PHASE_COORDINATES" or proposal["status"] != "PASS_EXACT_PROPOSAL_MARGINAL":
        raise ValueError("Required validation failed")
    if sha(BASE/"REGISTRO_C6.json") != sha(ROOT/"REGISTRO_C6.json"):
        raise ValueError("C6 changed")
    all_controls = [c for row in validation["rows"] for c in row["direct_controls"]]
    quadratures = [c for row in validation["rows"] for c in row["quadratures"]]
    now = datetime.now(timezone.utc).isoformat()
    measured = dict(date_utc=now, status="PHASE_COORDINATE_VALIDATED_SOURCE_RUN_LIVE",
        families=2, source_controls=4, direct_phase_hypothesis_controls=len(all_controls),
        max_waveform_relative_error=max(c["waveform_relative_error"] for c in all_controls),
        max_logL_interpolation_error=max(c["logL_error"] for c in all_controls),
        max_coordinate_integral_difference=max(c["coordinate_change_error"] for c in quadratures),
        max_single_branch_omission_error=max(c["error_if_only_one_branch_kept"] for c in quadratures),
        proposal_marginal_relative_error=proposal["max_relative_error"],
        source_parameters_integrated=7, source_parameters_sampled=6,
        phase="Full0..2pi prior integrated by checked quadrature; both orbital branches and odd modes retained",
        prior_changed=False, gate_changed=False, original_C6_changed=False,
        live=dict(tool="write_stdin", session_id=85465, observed="live with advancing counters before record", progress=progress),
        scientific_acceptance=False)
    names = ["peak_phase_coordinates.py", "validate_peak_phase_coordinates.py", "PEAK_PHASE_COORDINATES_VALIDATION.json",
             "phase_marginal_source.py", "validate_phase_proposal.py", "phase_runs/REGISTRATION.json", "phase_runs/PROPOSAL.json",
             "phase_runs/PROPOSAL_VALIDATION.json", "phase_runs/IMRPhenomXPHM_seed130801_N1024/START.json"]
    measured["hashes"] = {"cache/source_evidence/"+n:sha(BASE/n) for n in names}
    safe(receipt, (json.dumps(measured, indent=2, ensure_ascii=False)+"\n").encode())
    status_path = ROOT/"STATUS_ORDEM_013.json"
    status = json.loads(status_path.read_bytes())
    status.update(date_utc=now, previous_goal_turn="PROGRESS: integrações insuficientes auditadas e enrolamento da fase medido",
        this_goal_turn="PROGRESS: mudança de variável validada em ambas as famílias; integral de fase preservada; inferência com fase marginalizada iniciada")
    status["active_processes"] = [measured["live"]]
    status["verified"]["C5_phase_coordinates_and_live_integration"] = {k:v for k, v in measured.items() if k not in ("hashes", "live")}
    status["hashes"].update(measured["hashes"])
    status["next_action"] = ("Revalidar write_stdin85465, integração com fase inteira marginalizada: phase_runs/IMRPhenomXPHM_seed130801_N1024. "
        "Não repetir os pilotos anteriores nem reiniciar por timeout. Ao terminar, conferir RESULT, ESS/pesos e controles por ponto; "
        "a mudança mantém sete parâmetros integrados, com seis amostrados e fase em quadratura. "
        "As duas ramificações são obrigatórias: omitir uma deu erro de até73,68 em log da integral nos controles. "
        "Faltam repetição, taxa de geração duplicada no posterior relevante, recuperação SEOB, demais SNR/leituras e calibração contínua de a. C6 permanece congelado.")
    status["requirements_remaining"][0] = status["next_action"]
    safe(status_path, (json.dumps(status, indent=2, ensure_ascii=False)+"\n").encode())
    progress_path = ROOT/"PROGRESSO.md"
    note = (f"\n\n---\n[REAL — {now}] Mudança para fase no pico validada em duas famílias e dois pontos de fonte por família. "
        f"Erro máximo de integral ao mudar coordenadas: {measured['max_coordinate_integral_difference']:.17g}; "
        f"erro máximo ao omitir um ramo: {measured['max_single_branch_omission_error']:.17g}. "
        f"Marginal da proposta conferida por quadratura: {proposal['max_relative_error']:.17g}. "
        "Rodada phase_runs/IMRPhenomXPHM_seed130801_N1024 em execução na sessão85465; sete parâmetros integrados, "
        "fase em quadratura e seis em amostragem. Evidência científica ainda não aceita. Ver C5_PHASE_INTEGRATION_START.json.\n")
    safe(progress_path, progress_path.read_bytes()+note.encode())
    print(json.dumps(dict(status=measured["status"], session_id=85465, last_done=progress["done"])))


if __name__ == "__main__":
    main()
