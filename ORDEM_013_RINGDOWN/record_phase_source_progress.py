"""Record completed phase audits and the actually observed adaptive run."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
from record_source_evidence_start import safe, sha

ROOT=Path(__file__).resolve().parent
BASE=ROOT/"cache/source_evidence"


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--live-session",type=int,required=True)
    args=parser.parse_args()
    target=ROOT/"C5_PHASE_SOURCE_PROGRESS.json"
    handoff=ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_fase_completa_e_intensidade_continua.md"
    if target.exists() or handoff.exists():
        raise FileExistsError("Create-once receipt")
    run=BASE/"phase_runs/IMRPhenomXPHM_seed130801_N1024"
    adaptive=BASE/"phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048"
    result=json.loads((run/"RESULT.json").read_bytes())
    audit=json.loads((run/"AUDIT_RATE.json").read_bytes())
    continuous=json.loads((BASE/"CONTINUOUS_PHASE_VALIDATION.json").read_bytes())
    adaptation=json.loads((BASE/"phase_adapted_130801/ADAPTATION.json").read_bytes())
    for name,expected in result["hashes"].items():
        if sha(run/name)!=expected:raise ValueError("Pilot result changed")
    for name,expected in adaptation["hashes"].items():
        if sha(BASE/name)!=expected:raise ValueError("Adaptation changed")
    if continuous["status"]!="PASS_CONTINUOUS_STRENGTH_PHASE_LIKELIHOOD":
        raise ValueError("Continuous-strength validation did not pass")
    if sha(BASE/"REGISTRO_C6.json")!=sha(ROOT/"REGISTRO_C6.json"):
        raise ValueError("C6 changed")
    allc=[c for row in continuous["rows"] for c in row["direct_controls"]]
    phaseq=[c for row in continuous["rows"] for c in row["quadratures"]]
    now=datetime.now(timezone.utc).isoformat()
    progress=json.loads((adaptive/"PROGRESS.json").read_bytes())
    stage=dict(folder=str(adaptive.relative_to(ROOT)),last_progress=progress,
        session_id=args.live_session,tool="write_stdin",status="LIVE_OBSERVED_BY_TOOL_BEFORE_RECORD",
        observation="The calling task polled this handle successfully before this recorder. Revalidate before relying on continued activity.")
    if (adaptive/"RESULT.json").exists():
        finished=json.loads((adaptive/"RESULT.json").read_bytes())
        stage.update(status="RESULT_PRESENT_REQUIRES_AUDIT",result_sha256=sha(adaptive/"RESULT.json"),
            passing=finished["draws_passing_precision"],ESS_range=finished["ESS_range"])
    summary=dict(status="PHASE_AUDIT_COMPLETE_SOURCE_PRECISION_OPEN",date_utc=now,
        previous_goal_turn="PROGRESS: complete-phase coordinates and proposal marginal validated; source pilot started",
        this_goal_turn="PROGRESS: pilot completed and audited; proposal adapted without changing prior; continuous-strength likelihood validated",
        pilot=dict(draws=result["draws"],evaluations=result["evaluations"],datasets=1200,independent_noise_intervals_per_detector=50,
            passing=result["draws_passing_precision"],ESS_range=result["ESS_range"],
            ESS_quantiles=audit["ESS_quantiles"],max_weight_quantiles=audit["max_weight_quantiles"],
            arithmetic_errors=audit["independent_arithmetic_errors"],phase_controls=audit["phase_controls"],
            rate_points=len(audit["rate_checks"]),rate_max_logL_change=audit["max_active_rate_difference"],rate_pass=audit["rate_control_pass"],
            scientific_acceptance=False),
        continuous_strength=dict(cells=len(continuous["rows"]),direct_controls=len(allc),
            families=continuous["families"],readings=continuous["readings"],strengths=continuous["strengths"],
            max_waveform_relative_error=max(c["relative_waveform_error"] for c in allc),
            max_logL_error=max(c["logL_error"] for c in allc),
            max_original_binary_integral_difference=max(r.get("original_zero_one_integral_error",0.) for r in continuous["rows"]),
            max_phase_quadrature_error=max(c["error"] for c in phaseq),
            continuous_strength_prior_selected=False,bias_and_coverage_measured=False,scientific_acceptance=False),
        adaptive=stage,prior_changed=False,physical_clock_selected=False,gate_changed=False,original_C6_changed=False)
    paths=[BASE/n for n in ("audit_phase_source.py","adapt_phase_source.py","continuous_phase_source.py","validate_continuous_phase.py",
        "CONTINUOUS_PHASE_VALIDATION.json","phase_runs/REGISTRATION.json","phase_runs/PROPOSAL.json",
        "phase_adapted_130801/ADAPTATION.json","phase_adapted_130801/PROPOSAL.json")]
    paths += [run/n for n in ("RESULT.json","RESULT_ARRAYS.npz","PROPOSALS.npz","AUDIT.json","AUDIT_RATE.json")]
    paths += [adaptive/"START.json",Path(__file__)]
    summary["hashes"]={str(p.relative_to(ROOT)).replace("\\","/"):sha(p) for p in paths}
    safe(target,(json.dumps(summary,ensure_ascii=False,indent=2)+"\n").encode())
    hashes="\n".join(f"| `{name}` | `{value}` |" for name,value in summary["hashes"].items())
    c=summary["continuous_strength"]
    text=f"""[REAL — controles numéricos executados; OPEN — precisão da evidência e calibração da fonte]

# ORDEM 013 — fase inteira, auditoria e intensidade contínua

Registro: {now}. N/A — sem Lean. Nenhuma edição no um.py/kernel/casas canônicas.

## Critérios desta etapa

- **PAGO:** o piloto de fase integral terminou (1024 propostas;843 dentro do prior). As181 externas têm integrando zero e contam no denominador. São1200 dados simulados, com50 intervalos de ruído por detector reutilizados entre células; não1200 observações independentes.
- **PAGO:** soma alternativa em precisão estendida, erro máximo {max(audit['independent_arithmetic_errors'].values()):.17g}; taxas8192→16384Hz nos35 pontos dominantes, mudança relevante máxima {audit['max_active_rate_difference']:.17g}, limite0,1. Esses testes verificam a implementação, não a suficiência das amostras.
- **NÃO PAGO:** precisão da evidência. ZERO/1200 comparações passou; ESS entre{result['ESS_range'][0]:.8g} e{result['ESS_range'][1]:.8g}, contra mínimo100. Não usar os lnB desse piloto como resultado físico aceito. Fase explícita não resolveu sozinha a exploração das demais coordenadas.
- **PAGO:** proposta computacional adaptada usando igualmente todos os2400 alvos.70% mistura ajustada,20% mistura anterior,10% prior inteiro. Priors físicos, likelihood e critérios inalterados. Nova integração com2048 propostas independentes: sessão{args.live_session}, último registro{progress['done']}/{progress['valid_draws']} avaliações internas. Conferir o handle; este documento não promete que continuará viva.
- **PAGO:** leitura contínua de a implementada e comparada à geração direta em{c['direct_controls']} controles ({c['cells']} células; duas famílias, duas fontes, quatro leituras, O4/O5; a=-0,25;0;0,37;1;2). Erro relativo máximo da onda={c['max_waveform_relative_error']:.17g}; logL={c['max_logL_error']:.17g}. O controle negativo de a é extensão fenomenológica de diagnóstico, não gerador GKLS físico.
- **PAGO:** em a=0/1 a nova integral recupera a anterior, diferença máxima{c['max_original_binary_integral_difference']:.17g}.
- **NÃO PAGO:** repetição independente, precisão suficiente da fonte, recuperação SEOB integrada, demais SNR/leituras e viés/cobertura de a contínuo. Nenhum prior de a foi escolhido pelo simples teste da nova função.

## O que se integra

Na realização condicional inteira de harmônicos já usada, h_a = h_all + (exp(-a Γ_220 t)-1) h_22 + (exp(-a Γ_440 t)-1) h_44. Cada termo usa a mesma fonte, o pico intrínseco22 e distância/polarização comuns. O amortecimento ocorre ANTES do branqueamento pela covariância do detector. Demais harmônicos ficam como estavam; não é uma derivação da taxa de cada overtone.

A integral de fase é da **verossimilhança**, (1/2π)∫L(d|η,φ,a)dφ, não uma média da forma de onda. Marginalizar uma fase orbital desconhecida não é aplicar dephasing físico nem escolher um desenrolamento quântico. As duas ramificações orbitais e todos os harmônicos gerados continuam incluídos. A força contínua altera apenas a mesma lei de amortecimento explicitamente condicional.

## Reprodução e continuação

Scripts em `cache/source_evidence`, Python WSL `/opt/pycbc_env/bin/python -B`:

```text
audit_phase_source.py IMRPhenomXPHM_seed130801_N1024 --rate --processes 6
validate_continuous_phase.py
adapt_phase_source.py fit
adapt_phase_source.py run --draws 2048 --seed 130811 --processes 6
```

Comandos acima JÁ executados/iniciados. Arquivos create-once recusam sobrescrita; reproduzir numa cópia preservada ou usar nova semente/pasta quando aplicável. Não iniciar outra cópia da sessão{args.live_session}. As sessões85465 (piloto),40076 (auditoria) e45570 (validação contínua) foram observadas terminais, código0. Após a nova rodada, conferir RESULT, somas, ESS, peso máximo e erro MC antes de interpretar lnB. C6 original permanece congelada. Nenhum número foi convertido em sigma, e nenhum gate foi movido.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
{hashes}
"""
    safe(handoff,text.encode())
    status_path=ROOT/"STATUS_ORDEM_013.json"
    status=json.loads(status_path.read_bytes())
    status.update(date_utc=now,previous_goal_turn=summary["previous_goal_turn"],this_goal_turn=summary["this_goal_turn"])
    status["verified"]["C5_phase_source_progress"]={k:v for k,v in summary.items() if k not in ("hashes","adaptive")}
    status["active_processes"]=[stage] if stage["status"].startswith("LIVE") else []
    status["hashes"].update(summary["hashes"])
    status["next_action"]=(f"Revalidar write_stdin{args.live_session}, phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048. "
        "Piloto1024 e auditorias anteriores terminaram; não reiniciá-los. Ao terminar, auditar a nova integração, comparar precisão, "
        "e só depois decidir repetição/adaptação. API contínua validada em480 controles, mas sem prior de a ou calibração de viés/cobertura. "
        "Ainda faltam SEOB como recuperação integrada, demais SNR/leituras e aceitação científica. Nenhuma conclusão5sigma; C6 congelada.")
    status["requirements_remaining"][0]=status["next_action"]
    safe(status_path,(json.dumps(status,ensure_ascii=False,indent=2)+"\n").encode())
    progress_path=ROOT/"PROGRESSO.md"
    safe(progress_path,progress_path.read_bytes()+("\n\n---\n"+text).encode())
    print(json.dumps(dict(status=summary["status"],handoff=str(handoff),live=stage,continuous_controls=len(allc)),ensure_ascii=False))


if __name__=="__main__":
    main()
