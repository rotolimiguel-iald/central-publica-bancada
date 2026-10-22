"""Preserve the measured failure of adaptation and the next validated transport."""
from pathlib import Path
from datetime import datetime,timezone
import argparse
import json
from record_source_evidence_start import safe,sha

ROOT=Path(__file__).resolve().parent
BASE=ROOT/"cache/source_evidence"


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--live-session",type=int,required=True);args=parser.parse_args()
    receipt=ROOT/"C5_RINGDOWN_COORDINATES_PROGRESS.json"
    handoff=ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_coordenadas_ringdown_e_resolucao.md"
    if receipt.exists() or handoff.exists():raise FileExistsError("Create-once receipt")
    folder=BASE/"phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048"
    active=BASE/"phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048"
    comparison=json.loads((folder/"PROPOSAL_COMPARISON.json").read_bytes())
    audit=json.loads((folder/"AUDIT_RATE.json").read_bytes())
    high=json.loads((BASE/"PHASE_HIGH_SNR_CONTROLS.json").read_bytes())
    transport=json.loads((BASE/"RINGDOWN_COORDINATES_VALIDATION.json").read_bytes())
    oracle=json.loads((BASE/"phase_ringdown_transport/PROPOSAL_ORACLE.json").read_bytes())
    reg=json.loads((BASE/"phase_ringdown_transport/REGISTRATION.json").read_bytes())
    for name,expected in reg["hashes"].items():
        if sha(BASE/name)!=expected:raise ValueError("Transport input changed")
    if sha(BASE/"REGISTRO_C6.json")!=sha(ROOT/"REGISTRO_C6.json"):raise ValueError("C6 changed")
    if transport["status"]!="PASS_NUMERICAL_PRIOR_TRANSPORT" or oracle["status"]!="PASS_TRANSPORT_PROPOSAL_MOMENTS":
        raise ValueError("Transport validation failed")
    now=datetime.now(timezone.utc).isoformat()
    progress=json.loads((active/"PROGRESS.json").read_bytes())
    live=dict(tool="write_stdin",session_id=args.live_session,status="LIVE_OBSERVED_BEFORE_RECORD",
        folder=str(active.relative_to(ROOT)),last_progress=progress,
        observation="Calling task confirmed handle alive immediately before recording; revalidate on continuation")
    points=transport["point_checks"];integrals=transport["conditional_prior_integrals"]
    measured=dict(date_utc=now,status="SAMPLING_PRECISION_OPEN_NEW_COORDINATES_VALIDATED",
        previous_goal_turn="PROGRESS: first phase pilot audited, continuous-a API verified, adapted pilot initiated",
        this_goal_turn="PROGRESS: adapted pilot completed and audited, high-SNR rate deficits measured, prior-preserving ringdown coordinates validated and inference initiated",
        adaptation=dict(passing=comparison["new_passing"],draws=comparison["new_draws"],
            ESS_quantiles=comparison["new_ESS_quantiles"],old_median_ESS_per_draw=comparison["old_median_ESS_per_draw"],
            new_median_ESS_per_draw=comparison["new_median_ESS_per_draw"],changes_over_point2=comparison["changes_over_point2"],
            max_abs_lnB_change=comparison["max_abs_lnB_change"],arithmetic_error=comparison["independent_arithmetic_max_error"],
            rate_points=len(audit["rate_checks"]),max_active_rate_difference=audit["max_active_rate_difference"],scientific_acceptance=False),
        high_SNR_point_controls=high["summary"],
        high_SNR_scope="Original source points, R-B, frozen8192Hz injections rescaled. Not posterior evidence and not sufficient injection-resolution calibration at high SNR.",
        coordinates=dict(roundtrip_points=len(points),max_roundtrip_error=max(p["roundtrip_error"] for p in points),
            max_independent_Jacobian_relative_error=max(p["Jacobian_relative_error"] for p in points),
            conditional_integrals=len(integrals),max_conditional_integral_error=max(p["error"] for p in integrals),
            monotonicity_grid_points=transport["monotonicity_grid_points"],minimum_quality_slope_wrt_spin1=transport["minimum_quality_slope_wrt_spin1"],
            scope="Numerical coordinate/Jacobian/prior controls, not a formal global theorem or astrophysical convergence"),
        proposal_oracle={k:v for k,v in oracle.items() if k not in ("registration_sha256",)},
        active=live,scientific_acceptance=False,physical_prior_changed=False,clock_selected=False,C6_changed=False,gate_changed=False)
    names=["check_phase_high_snr.py","PHASE_HIGH_SNR_CONTROLS.json","compare_phase_runs.py",
        "ringdown_source_coordinates.py","validate_ringdown_coordinates.py","RINGDOWN_COORDINATES_VALIDATION.json",
        "transport_phase_source.py","phase_ringdown_transport/REGISTRATION.json","phase_ringdown_transport/PROPOSAL.json",
        "phase_ringdown_transport/PROPOSAL_ORACLE.json"]
    paths=[BASE/n for n in names]+[folder/n for n in ("RESULT.json","RESULT_ARRAYS.npz","PROPOSAL_COMPARISON.json","AUDIT_RATE.json")]
    paths += [active/"START.json",Path(__file__)]
    measured["hashes"]={str(p.relative_to(ROOT)).replace("\\","/"):sha(p) for p in paths}
    safe(receipt,(json.dumps(measured,indent=2,ensure_ascii=False)+"\n").encode())
    table="\n".join(f"| {r['snr']:.0f} | {r['pass8192']}/{r['cells']} | {r['pass16384']}/{r['cells']} | {r['max_change8192']:.9g} | {r['max_change16384']:.9g} |" for r in high["summary"])
    hashes="\n".join(f"| `{name}` | `{h}` |" for name,h in measured["hashes"].items())
    c=measured["coordinates"]
    text=f"""[REAL — resultados numéricos; OPEN — precisão científica da fonte e calibração]

# ORDEM 013 — coordenadas de ringdown e resolução

{now}. N/A — sem Lean. O objetivo permanece a confrontação precisa, sem selecionar relógio/partição e sem mover gate.

## O que a nova rodada efetivamente mediu

**PAGO:** a rodada adaptada2048 terminou (1656 propostas no domínio); a auditoria independente de soma deu diferença máxima{comparison['independent_arithmetic_max_error']:.17g}. O controle de geração8192→16384Hz nos54 pontos dominantes deu variação relevante máxima{audit['max_active_rate_difference']:.17g}, abaixo de0,1.

**NÃO PAGO:** ZERO/1200 comparações passou a precisão. A ESS mediana passou de{comparison['old_ESS_quantiles'][2]:.9g} para{comparison['new_ESS_quantiles'][2]:.9g} com o DOBRO de propostas; eficiência por proposta caiu de{comparison['old_median_ESS_per_draw']:.9g} para{comparison['new_median_ESS_per_draw']:.9g}. {comparison['changes_over_point2']}/1200 razões mudaram mais de0,2; mudança máxima{comparison['max_abs_lnB_change']:.9g}. A média favorável de uma célula não é evidência aceita. Não repetir essa proposta inalterada como solução da precisão. Nenhuma média dos dois pilotos foi fabricada.

## Resolução em SNR alto

**PAGO:** controles em duas famílias de recuperação, três fontes, O4/O5, a=0;0,37;1, ambas as famílias/amplitudes injetadas,50 ruídos pareados por célula. A tabela conta avaliações em pontos de fonte fixados, não posteriores integrados. Critério: alteração de logL≤0,1.

| SNR | 8192→16384 passa | 16384→32768 passa | maior alteração inicial | maior alteração seguinte |
|---:|---:|---:|---:|---:|
{table}

**NÃO PAGO:** precisão uniforme para SNR200/600. As injeções8192Hz foram conservadas e apenas reescaladas em amplitude: isso isola a resolução da recuperação, mas não valida a resolução da própria injeção em SNR600. Algumas avaliações fora da região posterior podem falhar sem dominar evidência; isto deve ser medido, não presumido. Não converter essas falhas em exclusão física.

## A mudança de coordenadas e o prior

**PAGO numericamente:** a mesma fonte é agora parametrizada para a proposta por

`y = (log(f220/250Hz), log(tau220/0.004s), u_q, u_spin2, u_cosi, u_t0)`.

Os parâmetros físicos originais continuam variando.250Hz e0,004s são somente unidades de coordenada e não relógios de dephasing. A forma de onda continua sendo gerada integralmente com os parâmetros binários recuperados pela inversa; a fase orbital continua integrada sobre0..2π.

Se `M_f = M_total * F(q,s1,s2)` e `chi = chi(q,s1,s2)`, então

`log f = log omega_R(chi) - log M_total - log F + const`,
`log tau = log M_total + log F - log abs(omega_I(chi)) + const`.

A derivada de F cancela no determinante. Nas coordenadas uniformes originais, a largura de M é60 e a de s1 é0,8. Portanto:

`J = |det(dy/du)| = (48/M_total) * (dchi/ds1) * d[log(omega_R/abs(omega_I))]/dchi`.

**O jacobiano não pode ser omitido.** Na proposta há10% do prior original transportado, com densidade1/J no domínio, e90% de mistura Student-t em y. A densidade da proposta na coordenada original é `q_u = q_y * J`; pesos de importância usam `L/q_u`. Propostas sem inversa física têm integrando zero e CONTAM no denominador total. O arquivo guarda y real e marca explicitamente o sentinela externo, em vez de apresentá-lo como fonte física.

Verificações: {c['roundtrip_points']} idas/voltas em duas famílias, erro máximo{c['max_roundtrip_error']:.17g}; determinante por diferenças finitas independente, erro relativo{c['max_independent_Jacobian_relative_error']:.17g}; {c['conditional_integrals']} integrais condicionais de normalização/momentos, erro máximo{c['max_conditional_integral_error']:.17g}; grade de monotonicidade com{c['monotonicity_grid_points']} pontos. São verificações numéricas do ajuste e da spline; não se intitulam prova formal global. Controles locais continuam ativos na inferência.

O oráculo da proposta sorteou32768 pontos independentes. Normalização estimada{oracle['mean'][0]:.9g}±{oracle['MC_standard_errors'][0]:.9g} (erro Monte Carlo); maior desvio padronizado entre13 momentos={oracle['max_standardized_error']:.9g}. Isso testa a distribuição computacional; não é significância física.

## Execução e pendências

**EM EXECUÇÃO:** `phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048`, sessão{args.live_session}; registro observado{progress['done']}/{progress['valid_draws']}. Revalidar o handle. Não duplicar por timeout. Sessões38040,85447 e75295 foram observadas terminais com código0.

Scripts em `cache/source_evidence`, Python `/opt/pycbc_env/bin/python -B`:

```text
compare_phase_runs.py phase_runs/IMRPhenomXPHM_seed130801_N1024 phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048
audit_phase_source.py ../phase_adapted_130801/IMRPhenomXPHM_seed130811_N2048 --rate --processes 6
check_phase_high_snr.py
validate_ringdown_coordinates.py
transport_phase_source.py fit
transport_phase_source.py oracle
transport_phase_source.py run --draws 2048 --seed 130841 --processes 6
```

Todos esses comandos já executados ou iniciados; artefatos create-once recusam sobrescrita. Reproduzir em cópia preservada. Primeiro conferir precisão da nova rodada, densidade/jacobiano, amostras externas e resolução nos pontos relevantes. Permanecem repetição, recuperação SEOB integrada, outras leituras, calibração contínua de a e resolução em SNR alto. C6 e o programa canônico não foram alterados. Nenhum lnB destes pilotos foi promovido a resultado aceito ou a sigma.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
{hashes}
"""
    safe(handoff,text.encode())
    path=ROOT/"STATUS_ORDEM_013.json";status=json.loads(path.read_bytes())
    status.update(date_utc=now,previous_goal_turn=measured["previous_goal_turn"],this_goal_turn=measured["this_goal_turn"])
    status["active_processes"]=[live]
    status["verified"]["C5_ringdown_coordinate_progress"]={k:v for k,v in measured.items() if k not in ("active","hashes")}
    status["hashes"].update(measured["hashes"])
    status["next_action"]=(f"Revalidar write_stdin{args.live_session}: phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048. "
        "Rodada adaptada anterior e seus controles terminaram; eficiência por proposta caiu, não repeti-la inalterada. "
        "Ao terminar a rodada em coordenadas f/tau, auditar integral, densidade/jacobiano, ESS e taxa antes de interpretar lnB. "
        "SNR200/600 falhou resolução em parte dos controles; separar pontos de fonte de região posterior e conferir também resolução da injeção. "
        "Faltam precisão/repetição, SEOB integrado, demais leituras e a contínuo. C6 congelada; sem resultado5sigma.")
    status["requirements_remaining"][0]=status["next_action"]
    safe(path,(json.dumps(status,indent=2,ensure_ascii=False)+"\n").encode())
    p=ROOT/"PROGRESSO.md";safe(p,p.read_bytes()+("\n\n---\n"+text).encode())
    print(json.dumps(dict(status=measured["status"],live=live,handoff=str(handoff)),ensure_ascii=False))


if __name__=="__main__":main()
