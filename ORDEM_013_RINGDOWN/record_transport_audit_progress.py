"""Record the completed transported pilot, resolution diagnostic and next live run."""
from pathlib import Path
from datetime import datetime,timezone
import argparse
import json
from record_source_evidence_start import safe,sha

ROOT=Path(__file__).resolve().parent
BASE=ROOT/"cache/source_evidence"


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--live-session",type=int,required=True);args=parser.parse_args()
    receipt=ROOT/"C5_TRANSPORT_AUDIT_PROGRESS.json"
    handoff=ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_auditoria_transporte_e_resolucao.md"
    if receipt.exists() or handoff.exists():raise FileExistsError("Create-once progress record")
    folder=BASE/"phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048"
    active=BASE/"phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192"
    result=json.loads((folder/"RESULT.json").read_bytes())
    comparison=json.loads((folder/"PROPOSAL_COMPARISON.json").read_bytes())
    density=json.loads((folder/"DENSITY_AUDIT.json").read_bytes())
    audit=json.loads((folder/"AUDIT_RATE.json").read_bytes())
    resolution=json.loads((BASE/"resolution_refinement/RESULT.json").read_bytes())
    proposal=json.loads((BASE/"phase_ringdown_regularized/PROPOSAL.json").read_bytes())
    oracle=json.loads((BASE/"phase_ringdown_regularized/PROPOSAL_ORACLE.json").read_bytes())
    reg=json.loads((BASE/"phase_ringdown_regularized/REGISTRATION.json").read_bytes())
    for name,expected in reg["hashes"].items():
        if sha(BASE/name)!=expected:raise ValueError("Regularized input changed")
    for name,expected in result["hashes"].items():
        if sha(folder/name)!=expected:raise ValueError("Completed pilot changed")
    for name,expected in resolution["hashes"].items():
        if sha(BASE/"resolution_refinement"/name)!=expected:raise ValueError("Resolution arrays changed")
    if sha(BASE/"REGISTRO_C6.json")!=sha(ROOT/"REGISTRO_C6.json"):raise ValueError("C6 changed")
    interpolation=[c for d in resolution["diagnostics"] for c in d["interpolation"]]
    progress=json.loads((active/"PROGRESS.json").read_bytes())
    now=datetime.now(timezone.utc).isoformat()
    live=dict(tool="write_stdin",session_id=args.live_session,status="LIVE_OBSERVED_BEFORE_RECORD",folder=str(active.relative_to(ROOT)),
        last_progress=progress,observation="Handle confirmed live by calling tool before this receipt; revalidate on continuation")
    measured=dict(date_utc=now,status="TRANSPORT_AUDITED_PRECISION_OPEN",previous_goal_turn="PROGRESS: coordinate/prior validation and transport pilot started",
        this_goal_turn="PROGRESS: transport pilot and all density/rate controls completed, resolution extended to128kHz, regularized larger proposal started",
        pilot=dict(draws=result["draws"],inside=result["evaluations"],passing=result["draws_passing_precision"],ESS_quantiles=comparison["new_ESS_quantiles"],
            efficiency_ratio=comparison["new_median_ESS_per_draw"]/comparison["old_median_ESS_per_draw"],
            changed_lnB_over_point2=comparison["changes_over_point2"],max_abs_lnB_change=comparison["max_abs_lnB_change"],
            pooled_ESS=audit["pooled_target_sample_ESS"],rate_points=len(audit["rate_checks"]),max_active_rate_change=audit["max_active_rate_difference"],
            direct_density_log_error=density["direct_density_log_error"],independent_Jacobian_relative_error=density["max_independent_Jacobian_relative_error"],scientific_acceptance=False),
        resolution=dict(rates=resolution["rates"],summary=resolution["summary"],interpolation_checks=len(interpolation),
            interpolation_failures=sum(not c["all_interpolation_pass"] for c in interpolation),
            max_interpolation_logL_error=max(max(c["logL_errors_by_SNR"]) for c in interpolation),
            scope="Source-point controls, frozen8192Hz injections, not posterior calibration or validation of high-SNR injection resolution"),
        next_proposal=dict(components=len(proposal["components"]),training_pooled_ESS=proposal["training_pooled_ESS"],
            draw_count=8192,seed=130861,physical_prior_changed=False,oracle_status=oracle["status"],
            oracle_max_standardized_error=oracle["max_standardized_error"],hypothesis=reg["hypothesis"]),
        active=live,scientific_acceptance=False,gate_changed=False,C6_changed=False)
    names=["audit_transport_density.py","audit_registered_transport.py","SOURCE_INTEGRATION_METHODS.md","refine_phase_resolution.py",
        "resolution_refinement/REGISTRATION.json","resolution_refinement/RESULT.json","refine_ringdown_proposal.py",
        "phase_ringdown_regularized/REGISTRATION.json","phase_ringdown_regularized/PROPOSAL.json","phase_ringdown_regularized/PROPOSAL_ORACLE.json"]
    paths=[BASE/n for n in names]+[folder/n for n in ("RESULT.json","RESULT_ARRAYS.npz","PROPOSAL_COMPARISON.json","DENSITY_AUDIT.json","AUDIT_RATE.json")]
    paths += [active/"START.json",Path(__file__)]
    measured["hashes"]={str(p.relative_to(ROOT)).replace("\\","/"):sha(p) for p in paths}
    safe(receipt,(json.dumps(measured,indent=2,ensure_ascii=False)+"\n").encode())
    rows="\n".join(f"| {r['snr']:.0f} | {r['passed'][0]}/{r['cells']} | {r['passed'][1]}/{r['cells']} | {r['max_changes'][0]:.9g} | {r['max_changes'][1]:.9g} |" for r in resolution["summary"])
    hashes="\n".join(f"| `{n}` | `{h}` |" for n,h in measured["hashes"].items())
    text=f"""[REAL — implementação auditada e déficits medidos; OPEN — precisão/calibração científica]

# ORDEM 013 — auditoria do transporte e resolução

{now}. N/A — sem Lean. Originais canônicos e C6 preservados.

**PAGO:** piloto em coordenadas de ringdown concluído:2048 propostas,1473 no domínio,575 com integrando zero contadas no denominador. Densidade conferida por soma direta das PDFs, erro log máximo{density['direct_density_log_error']:.17g}; jacobiano por diferenças finitas nos pontos dominantes, erro relativo máximo{density['max_independent_Jacobian_relative_error']:.17g}. Ida/volta e suporte verificados para todas as propostas.

**PAGO:** auditoria das somas e resolução8192→16384Hz nos{len(audit['rate_checks'])} pontos dominantes, alteração relevante máxima{audit['max_active_rate_difference']:.17g}, abaixo de0,1.

**NÃO PAGO:** ZERO/1200 razões atingiu os critérios. ESS mediana{comparison['new_ESS_quantiles'][2]:.9g}; eficiência por proposta multiplicada por{measured['pilot']['efficiency_ratio']:.9g}, mas ainda insuficiente. {comparison['changes_over_point2']}/1200 razões mudaram mais de0,2 contra o piloto anterior; máximo{comparison['max_abs_lnB_change']:.9g}. Nenhuma foi promovida a evidência física ou sigma.

## Resolução estendida

**PAGO:** controles adicionais32768/65536/131072Hz, mesmas fontes/ruídos/hipóteses. Os dados injetados continuam os8192Hz originais: não se demonstrou adequação da resolução das injeções a SNR600. A tabela é de avaliações em pontos de fonte, não da região posterior.

| SNR | 32768→65536 passa | 65536→131072 passa | maior delta logL inicial | maior delta logL seguinte |
|---:|---:|---:|---:|---:|
{rows}

**NÃO PAGO:** resolução uniforme em alta sensibilidade. Phenom melhora no controle entre taxas, mas SEOB permanece instável em parte dos casos; não basta continuar duplicando taxa sem diagnosticar o gerador/alinhamento. Além disso, {measured['resolution']['interpolation_failures']}/{len(interpolation)} controles locais de interpolação falharam algum SNR, máximo delta logL={measured['resolution']['max_interpolation_logL_error']:.9g}. Interpolação, quadratura, resolução do gerador e região posterior são controles diferentes; passar um não quita os outros. A falha numérica não é exclusão da TGL.

## Próxima integração, efetivamente iniciada

**EM EXECUÇÃO:** `phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192`, sessão{args.live_session}, observado{progress['done']}/{progress['valid_draws']}. O conjunto anterior ganhou ESS agregada{audit['pooled_target_sample_ESS']:.9g}. Hipótese computacional: poucos pontos efetivos podem ajustar em excesso uma mistura6D de12 componentes. O próximo piloto usa3 componentes e8192 novas propostas; não elimina nenhum dos sete parâmetros físicos nem altera seu prior. A hipótese de melhora ainda será medida.

O oráculo de32768 amostras da proposta passou: maior desvio padronizado dos momentos={oracle['max_standardized_error']:.9g}. Isso verifica normalização/momentos computacionais, não significância astrofísica. Dez por cento da proposta continua sendo o prior original integral.

**Continuar:** revalidar sessão{args.live_session}; não reiniciar por timeout. Sessões73887,95183 e81510 terminaram com código0. Após o RESULT:

```text
audit_registered_transport.py IMRPhenomXPHM_seed130861_N8192 --stage phase_ringdown_regularized
audit_phase_source.py ../phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192 --rate --processes 6
compare_phase_runs.py phase_ringdown_transport/IMRPhenomXPHM_seed130841_N2048 phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192
```

O auditor parametrizável é cópia do auditor anterior, com seleção explícita de pasta e contagem dinâmica; o original foi preservado. Os comandos de auditoria desta nova rodada ainda não foram executados, pois ela está viva. A descrição em inglês `SOURCE_INTEGRATION_METHODS.md` registra integral, priors, jacobiano, propostas externas, intensidade contínua e limites dos testes, para a entrega independente.

Faltam precisão/repetição dos fatores de Bayes, SEOB como recuperação integrada, demais leituras/SNR e calibração contínua de a. Nos SNR altos, diagnosticar as falhas persistentes antes de usar a inferência. Nenhum resultado recente move gate nem altera a C6 congelada.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
{hashes}
"""
    safe(handoff,text.encode())
    path=ROOT/"STATUS_ORDEM_013.json";status=json.loads(path.read_bytes())
    status.update(date_utc=now,previous_goal_turn=measured["previous_goal_turn"],this_goal_turn=measured["this_goal_turn"])
    status["verified"]["C5_transport_audit_progress"]={k:v for k,v in measured.items() if k not in ("active","hashes")}
    status["active_processes"]=[live];status["hashes"].update(measured["hashes"])
    status["next_action"]=(f"Revalidar write_stdin{args.live_session}: phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192. "
        "Piloto de transporte2048 e auditorias terminaram. Após RESULT, executar audit_registered_transport com --stage phase_ringdown_regularized, "
        "audit_phase_source via caminho ../phase_ringdown_regularized/... e compare_phase_runs. "
        "Resolução até128kHz já concluída: alta sensibilidade segue falhando em parte dos casos SEOB/interpolação; diagnosticar em vez de duplicar taxas cegamente. "
        "Faltam precisão/repetição, recuperação SEOB, demais leituras/SNR e a contínuo; C6 congelada, nenhum lnB novo aceito.")
    status["requirements_remaining"][0]=status["next_action"]
    safe(path,(json.dumps(status,ensure_ascii=False,indent=2)+"\n").encode())
    p=ROOT/"PROGRESSO.md";safe(p,p.read_bytes()+("\n\n---\n"+text).encode())
    print(json.dumps(dict(status=measured["status"],live=live,handoff=str(handoff)),ensure_ascii=False))


if __name__=="__main__":main()
