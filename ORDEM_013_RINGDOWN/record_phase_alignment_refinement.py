"""Record the verified numerical peak fix and the still-live source integral."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
from record_source_evidence_start import safe, sha

ROOT = Path(__file__).resolve().parent
BASE = ROOT/"cache/source_evidence"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-session", type=int, required=True)
    args = parser.parse_args()
    receipt = ROOT/"C5_PHASE_ALIGNMENT_REFINEMENT.json"
    handoff = ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_correcao_pico_de_fase.md"
    methods = BASE/"PHASE_ALIGNMENT_NUMERICS.md"
    if any(p.exists() for p in (receipt, handoff, methods)):
        raise FileExistsError("Create-once recorder")
    diagnostic = json.loads((BASE/"generator_alignment_diagnostic/RESULT.json").read_bytes())
    copied = json.loads((BASE/"stable_peak_validation/RESULT.json").read_bytes())
    provenance = json.loads((BASE/"STABLE_PEAK_MODEL_PROVENANCE.json").read_bytes())
    for key in ("source", "copy"):
        if sha(BASE/provenance[key]) != provenance[key+"_sha256"]:
            raise ValueError("Generator custody changed")
    for relative in ("phase_runs/REGISTRATION.json", "generator_alignment_diagnostic/REGISTRATION.json", "stable_peak_validation/REGISTRATION.json"):
        registration = json.loads((BASE/relative).read_bytes())
        for name, expected in registration["hashes"].items():
            if sha(BASE/name) != expected:
                raise ValueError("Registered input changed: "+name)
    for name, expected in diagnostic["hashes"].items():
        if sha(BASE/"generator_alignment_diagnostic"/name) != expected:
            raise ValueError("Diagnostic arrays changed")
    if copied["status"] != "PASS_COPIED_PHASE_ALIGNMENT":
        raise ValueError("Copied correction failed")
    if sha(ROOT/"REGISTRO_C6.json") != sha(BASE/"REGISTRO_C6.json"):
        raise ValueError("C6 custody changed")
    active = BASE/"phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192"
    if (active/"RESULT.json").exists():
        raise ValueError("Run completed; record a terminal state instead of live")
    progress = json.loads((active/"PROGRESS.json").read_bytes())
    now = datetime.now(timezone.utc).isoformat()
    live = dict(tool="write_stdin", session_id=args.live_session, status="LIVE_OBSERVED_BEFORE_RECORD",
                folder=str(active.relative_to(ROOT)).replace("\\", "/"), last_progress=progress,
                observation="Live tool handle polled before recording; revalidate next turn")
    rates = []
    for family in ("IMRPhenomXPHM", "SEOBNRv4HM"):
        for pair in ((32768, 65536), (65536, 131072)):
            rows = [r for r in copied["rate_diagnostics"] if r["family"] == family and (r["low_rate"], r["high_rate"]) == pair]
            rates.append(dict(family=family, rates=pair, max_amplitude_only_residual=max(r["common_amplitude_residual_norm"] for r in rows),
                              max_tangent_residual=max(r["tangent_residual_norm"] for r in rows),
                              max_direct_shifted_residual=max(r["direct_shifted_residual_norm"] for r in rows),
                              max_derivative_relative_change=max(max(r["derivative_relative_convergence"]) for r in rows)))
    text_en = f"""# Intrinsic-peak phase alignment: measured numerical correction

Date: {now}. This is a numerical diagnostic, not a physical detection.

For an aligned binary, the isolated face-on complex 22 mode has orbital-phase
dependence through a unit phase factor. Its amplitude and intrinsic peak are
therefore phase independent. The previous implementation minimized a spline
amplitude separately at each orbital phase. At source90 the measured peak
spread was of order 1e-10 seconds. That minimization noise contaminated the
otherwise finite Fourier dependence on orbital phase.

`stable_peak_imr_model.py` is a byte-preserving copy except for its explanatory
header and one replacement: the face-on peak uses `coa_phase=0.`. The actual
waveform still receives the requested orbital phase and inclination. No mode,
phase branch, source parameter, physical prior or conditional TGL clock was
removed. The source model used by the running registered integral is unchanged.

The common-peak diagnostic had 72 held-out controls (two families, three rates,
two PSDs, two strengths, three phases). Data were the same frozen8192Hz injections
scaled to SNR40/200/600. Recomputing the peak per phase failed44/72 controls;
using one common peak failed0/72. The copied implementation was then evaluated
independently against that common-peak Fourier bank: maximum relative waveform
error {copied['max_waveform_error']:.17g} and maximum log-likelihood error
{copied['max_logL_error']:.17g}. These results concern source90, not the entire
source prior or posterior region. They do not validate high-SNR injection
resolution, evidence precision or posterior coverage.

The original SEOB rate discrepancy persists after the phase fix. A separate
noiseless SNR600 diagnostic projected the rate difference onto the existing
common amplitude/polarization, orbital phase and peak-time directions. Each
linear time/phase correction was also evaluated in the full waveform, with
amplitude/polarization refitted. For SEOB64kHz versus128kHz the largest directly
reevaluated residual norm is {rates[-1]['max_direct_shifted_residual']:.17g}.
This is a whitened waveform distance, not a detection significance. Time/phase
alignment reduces but does not eliminate the source90 SEOB shape difference.
It is not legitimate to substitute this profile diagnostic for prior
marginalization or the registered numerical evidence checks.

The corrected model is available for a separately registered follow-up.
Do not insert it into the live integral or overwrite frozen runs. Future use
requires controls over the relevant source region and waveform rates.
"""
    safe(methods, text_en.encode())
    paths = [BASE/n for n in ("diagnose_generator_alignment.py", "generator_alignment_diagnostic/REGISTRATION.json",
             "generator_alignment_diagnostic/RESULT.json", "stable_peak_imr_model.py", "STABLE_PEAK_MODEL_PROVENANCE.json",
             "validate_stable_peak_and_rate.py", "stable_peak_validation/REGISTRATION.json", "stable_peak_validation/RESULT.json",
             "PHASE_ALIGNMENT_NUMERICS.md", "coherent_imr_model.py", "phase_ringdown_regularized/REGISTRATION.json")]
    paths += [Path(__file__)]
    hashes = {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in paths}
    measured = dict(date_utc=now, status="PHASE_ALIGNMENT_FIXED_IN_COPY_SOURCE_EVIDENCE_STILL_OPEN",
                    previous_goal_turn="NO_PROGRESS_ON_GOAL: the intervening reply addressed the user's short-prompt request",
                    this_goal_turn="PROGRESS: revalidated live inference; isolated and corrected phase-peak numerical jitter in a copy; completed held-out validation and independent direct waveform reevaluation of rate-alignment shifts",
                    diagnostic_interpolation=diagnostic["interpolation_summary"],
                    copied_validation={k:copied[k] for k in ("status", "count", "max_waveform_error", "max_logL_error", "scope")},
                    rate_shape_diagnostic=rates, active=live, source_model_in_live_run_changed=False,
                    scientific_acceptance=False, C6_changed=False, gate_changed=False, hashes=hashes)
    safe(receipt, (json.dumps(measured, indent=2, ensure_ascii=False)+"\n").encode())
    table = "\n".join(f"| {r['family']} | {r['rates'][0]} → {r['rates'][1]} | {r['max_amplitude_only_residual']:.9g} | {r['max_direct_shifted_residual']:.9g} |" for r in rates)
    custody = "\n".join(f"| `{n}` | `{v}` |" for n,v in hashes.items())
    text = f"""[REAL — correção numérica medida em cópia; OPEN — evidência integrada/calibração]

# ORDEM 013 — correção do pico de fase e diagnóstico da resolução

{now}. N/A — sem Lean. Nenhum original canônico alterado.

**PAGO:** localizada a origem das falhas de interpolação em fase no caso source90.
O pico intrínseco do modo22 deve ser independente da fase orbital, mas sua
reotimização para cada fase criava dispersão de aproximadamente10⁻¹⁰s. Usar o
mesmo pico medido em fase zero levou os controles de44 falhas em72 para zero
falhas em72. Fontes: duas famílias, três taxas32/64/128kHz, duas PSDs, duas
intensidades e três fases fora da malha; SNR40/200/600.

**PAGO:** a correção entrou somente na cópia `stable_peak_imr_model.py`.
O gerador original e a integração já registrada continuam intactos. A cópia
foi conferida contra o banco de fase com alinhamento comum: erro relativo
máximo de forma de onda={copied['max_waveform_error']:.17g}; erro máximo na
log-verossimilhança={copied['max_logL_error']:.17g}, em72 controles.
Isso não atesta ainda a região inteira do prior/posterior.

**NÃO PAGO:** o erro SEOB entre resoluções não desaparece com essa correção.
Um diagnóstico adicional ajustou apenas as direções já presentes de
amplitude/polarização, fase e tempo, em SNR600 sem ruído. A coluna final foi
conferida gerando novamente a forma de onda com o deslocamento calculado.

| família | taxas (Hz) | maior resíduo após amplitude/polarização | após também fase/tempo, avaliação direta |
|---|---:|---:|---:|
{table}

Esses números são normas na métrica do ruído, não sigmas de detecção. Ajustar
fase e tempo reduz parte da diferença SEOB, mas sobra erro de forma. O teste
é pontual e não substitui integração do prior, estabilidade de evidências,
controle da resolução das injeções nem cobertura dos posteriores.

**EM EXECUÇÃO:** sessão{args.live_session}, rodada8192 propostas
`phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192`, observada em
{progress['done']}/{progress['valid_draws']} avaliações dentro do suporte.
Propostas externas ao suporte físico continuam contadas com integrando zero.
O diagnóstico46894 e a validação71668 terminaram com código0.

**Continuar:** revalidar sessão{args.live_session}; não reiniciar por timeout.
Após RESULT, executar `audit_registered_transport.py` com
`--stage phase_ringdown_regularized`, `audit_phase_source.py` com `--rate` e
comparar com o piloto anterior via `compare_phase_runs.py` conforme o recibo
`C5_TRANSPORT_AUDIT_PROGRESS.json`. Não usar a nova cópia retroativamente.
Faltam precisão/repetição, recuperação SEOB integrada, demais leituras/SNR e
calibração contínua de a. A causa de fase foi resolvida no escopo medido;
a precisão física/estatística não foi declarada por consequência.

Descrição técnica em inglês: `cache/source_evidence/PHASE_ALIGNMENT_NUMERICS.md`.
Nenhum resultado novo é confirmação física ou conversão para5σ. C6 preservada.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
{custody}
"""
    safe(handoff, text.encode())
    path = ROOT/"STATUS_ORDEM_013.json"
    status = json.loads(path.read_bytes())
    status.update(date_utc=now, previous_goal_turn=measured["previous_goal_turn"], this_goal_turn=measured["this_goal_turn"])
    status["verified"]["C5_phase_alignment_refinement"] = {k:v for k,v in measured.items() if k not in ("hashes", "active")}
    status["active_processes"] = [live]
    status["hashes"].update(hashes)
    status["next_action"] = (f"Revalidar write_stdin{args.live_session}, integração8192 phase_ringdown_regularized. "
        "Após RESULT, auditar densidade/rate/repetição conforme C5_TRANSPORT_AUDIT_PROGRESS. "
        "46894 e71668 concluídos: pico comum corrige interpolação em source90, cópia stable_peak_imr_model validada72controles. "
        "Não incorporar a cópia na rodada já registrada; validar futura região de fonte. "
        "SEOB ainda tem erro de forma entre resoluções após ajustar fase/tempo. Precisão/calibração científica permanecem abertas.")
    status["requirements_remaining"][0] = status["next_action"]
    safe(path, (json.dumps(status, indent=2, ensure_ascii=False)+"\n").encode())
    path = ROOT/"PROGRESSO.md"
    safe(path, path.read_bytes()+("\n\n---\n"+text).encode())
    print(json.dumps(dict(status=measured["status"], active=live, handoff=str(handoff)), ensure_ascii=False))


if __name__ == "__main__":
    main()
