"""Append the measured numerical failures and adaptive integration outcome."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
from record_source_evidence_start import safe

ROOT = Path(__file__).resolve().parent
BASE = ROOT/"cache/source_evidence"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(name):
    return json.loads((BASE/name).read_bytes())


def main():
    handoff = ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_auditoria_integracao_fonte.md"
    if handoff.exists():
        raise FileExistsError("Create-once recorder")
    pilot_name = "runs/IMRPhenomXPHM_seed130522_nlive256"
    first_name = "importance_runs/IMRPhenomXPHM_seed130522_nlive256_seed130701_N4096"
    adapted_name = "importance_runs/IMRPhenomXPHM_adapted_130701_seed130707_N16384"
    pilot, pa = read(pilot_name+"/RESULT.json"), read(pilot_name+"/AUDIT.json")
    first = read(first_name+"/RESULT.json")
    adapted, aa = read(adapted_name+"/RESULT.json"), read(adapted_name+"/AUDIT.json")
    balanced, independent = read("BALANCED_ORACLE.json"), read("IMPORTANCE_ORACLE.json")
    phase = read("PEAK_PHASE_DIAGNOSTIC.json")
    if sha(ROOT/"REGISTRO_C6.json") != sha(BASE/"REGISTRO_C6.json"):
        raise ValueError("C6 changed")
    now = datetime.now(timezone.utc).isoformat()
    result = dict(status="NUMERICAL_AUDIT_NOT_PHYSICAL_ACCEPTANCE", date_utc=now,
                  nested=dict(ncall=pilot["ncall"], maxcall_reached=pilot["maxcall_reached"],
                              ESS_range=pilot["component_ESS_range"], components_passing=pilot["components_passing_weight_thresholds"],
                              rate_pass=pa["sample_rate_pass"], all_precision_pass=pa["all_MC_precision_pass"]),
                  balanced_toy_seed_lnB_difference=balanced["difference_between_seed_lnB"],
                  independent_toy_lnB_max_error=max(abs(r["lnB_error"]) for r in independent["rows"]),
                  importance_initial=dict(draws=first["draws"], evaluated=first["evaluated_draws"], passing=first["draws_passing_precision"]),
                  importance_adapted=dict(draws=adapted["draws"], evaluated=adapted["evaluated_draws"],
                         passing=adapted["draws_passing_precision"], all_precision_pass=adapted["all_draws_pass_precision"],
                         minimum_component_ESS=min(r["min_component_ESS"] for r in adapted["rows"]),
                         maximum_component_weight=max(r["max_component_weight"] for r in adapted["rows"]),
                         maximum_lnB_MC_sd=max(r["MC_lnB_sd_max"] for r in adapted["rows"]), audit=aa),
                  source_dimensions_integrated=7, amplitude_dimensions_integrated=2,
                  physical_prior_unchanged=True, no_C6_change=True, scientific_acceptance=False,
                  physical_partition_selected=False, no_target_strain_read=True)
    result["phase_coordinate_diagnostic"] = {k:phase[k] for k in (
        "mass_phase_range_rad", "common_spin_phase_range_rad", "phase_response_slope", "phase_response_residual_rad")}
    paths = ["source_evidence.py", "importance_source_evidence.py", "validate_balanced_mixture.py", "validate_importance_mixture.py",
             "refine_importance_proposal.py", "audit_importance_source.py", "analyze_source_evidence.py", "BALANCED_ORACLE.json", "IMPORTANCE_ORACLE.json",
             "validate_balanced_mixture.py.import_order_failed_bytes", "validate_importance_mixture.py.numpy_bool_failed_bytes",
             "REGISTRATION.json", "runs/IMRPhenomXPHM_adapted_130701/IMPORTANCE_PROPOSAL.json"]
    paths += ["diagnose_peak_phase.py", "PEAK_PHASE_DIAGNOSTIC.json", "PEAK_PHASE_COORDINATES.md"]
    paths += [pilot_name+"/"+n for n in ("RESULT.json", "AUDIT.json", "samples.npz", "IMPORTANCE_PROPOSAL.json")]
    paths += [first_name+"/"+n for n in ("RESULT.json", "RESULT_ARRAYS.npz", "START.json")]
    paths += [adapted_name+"/"+n for n in ("RESULT.json", "RESULT_ARRAYS.npz", "AUDIT.json", "START.json")]
    hashes = {"cache/source_evidence/"+n:sha(BASE/n) for n in paths}
    hashes[Path(__file__).name] = sha(Path(__file__))
    result["hashes"] = hashes
    safe(ROOT/"C5_SOURCE_EVIDENCE_AUDIT_SUMMARY.json", (json.dumps(result, indent=2, ensure_ascii=False)+"\n").encode())
    text = f"""[REAL — resultados numéricos e auditoria; OPEN — aceitação científica da fonte não linear]

# ORDEM 013 — Auditoria da integração de fonte

{now}

O piloto de amostragem aninhada terminou com {pilot['ncall']} chamadas e sem atingir a
meta de convergência. ESS das componentes: {pilot['component_ESS_range']}; componentes
aprovadas no critério de pesos: {pilot['components_passing_weight_thresholds']} de 2400.
Esses fatores de Bayes NÃO são uma entrega científica aceita. Dobrar a taxa da forma
de onda passou no controle dos pontos relevantes; a integração estatística falhou.

No oráculo analítico, balancear componentes melhorou os pesos, mas duas sementes ainda
diferiram {balanced['difference_between_seed_lnB']:.9g} em ln B (critério: 0,2). A etiqueta
de consistência ampla do teste não substitui essa exigência. A alternativa de amostragem
independente obteve erro máximo {result['independent_toy_lnB_max_error']:.9g} em quatro
controles de integrais conhecidas; isso valida seu mecanismo, não o modelo astrofísico.

## Integração independente no problema real

| rodada | propostas | avaliações dentro do prior | conjuntos com precisão mínima |
|---|---:|---:|---:|
| inicial | {first['draws']} | {first['evaluated_draws']} | {first['draws_passing_precision']} / 1200 |
| adaptada | {adapted['draws']} | {adapted['evaluated_draws']} | {adapted['draws_passing_precision']} / 1200 |

A rodada adaptada usou 24 componentes Student-t aprendidas de TODOS os pesos do piloto.
Dez por cento das propostas vêm do prior original completo; pontos fora do cubo têm
integrando zero e continuam no denominador. O prior físico, os parâmetros, o modelo e
os intervalos de ruído não foram reduzidos para conseguir passar. Aprender uma proposta
não é restringir o prior; a integral usa o quociente pela densidade da proposta.

Pior ESS na rodada adaptada: {result['importance_adapted']['minimum_component_ESS']:.9g};
maior peso individual: {result['importance_adapted']['maximum_component_weight']:.9g};
maior erro estimado de Monte Carlo em ln B: {result['importance_adapted']['maximum_lnB_MC_sd']:.9g}.
Auditoria aritmética/taxa: {aa['status']}. Critérios completos de precisão:
{adapted['all_draws_pass_precision']}. Uma repetição independente da proposta final
e a calibração contínua do parâmetro de dephasing ainda faltam.

Cada conjunto simulado é analisado separadamente. Os 1200 conjuntos reutilizam 50
intervalos pareados por detector; não são eventos independentes. O4/O5 são sensibilidades
de cenário. Não houve leitura nova do evento, alteração da C6, do um.py ou do gate.
SEOBNRv4HM continua na matriz de injeções e controles; sua integração como família de
recuperação ainda está pendente. A confirmação física e qualquer significância nova
permanecem não estabelecidas. N/A — sem Lean.

Falhas operacionais preservadas: ordem de importação do dynesty local no oráculo
balanceado; booleano NumPy não serializável no primeiro registro do oráculo independente.
As cópias de bytes estão ao lado dos scripts corrigidos. Nenhuma delas foi falha de física.

## Reprodução

## Causa numérica localizada e próximo passo

A fase 22 no pico gira {phase['mass_phase_range_rad']:.9g} rad na varredura de massa
60–100 massas solares e {phase['common_spin_phase_range_rad']:.9g} rad na varredura
do spin comum −0,25 a 0,25. A fase de referência, portanto, pode criar muitas curvas
estreitas no posterior. Isso é um diagnóstico do gerador, não uma identificação física.
`PEAK_PHASE_COORDINATES.md` deriva uma mudança EXATA de variável que conserva o prior:
fase no pico uniforme em [0,π), somando as duas pré-imagens orbitais com pesos 1/2.
É essencial conservar ambos os ramos e todas as harmônicas, inclusive ímpares. A soma
é invariante à troca de ramo do argumento complexo. Implementação e validação de
quadratura ainda não foram feitas. Essa é a próxima ação justificada pelo diagnóstico;
não repetir as integrações anteriores apenas aumentando o número de amostras.

## Reprodução dos artefatos existentes

Scripts e resultados ficam em `cache/source_evidence`. Scripts create-once recusam
sobrescrever rodadas. Para nova integração usar semente/nome distintos; preservar os
priors e verificar o registro. `audit_importance_source.py <nome_da_rodada>` confere
custódia, somas diretas em precisão estendida e taxa duplicada nos pontos dominantes.
Os cálculos desta entrega terminaram; não retomar as sessões históricas como se estivessem vivas.

## Custódia

| arquivo relativo à bancada | SHA256 medido |
|---|---|
"""
    text += "".join(f"| `{n}` | `{h}` |\n" for n, h in hashes.items())
    safe(handoff, text.encode())
    status_path = ROOT/"STATUS_ORDEM_013.json"
    status = json.loads(status_path.read_bytes())
    status["previous_goal_turn"] = "PROGRESS: integração de fonte registrada e processo iniciado"
    status["this_goal_turn"] = "PROGRESS: piloto encerrado e reprovado numericamente; alternativa independente validada, executada, adaptada e auditada"
    status["date_utc"] = now
    status["active_processes"] = []
    status["verified"]["C5_source_evidence_audit"] = {k:v for k, v in result.items() if k != "hashes"}
    status["next_action"] = ("Ler C5_SOURCE_EVIDENCE_AUDIT_SUMMARY e os RESULT/AUDIT das integrações independentes. "
       "Todos os processos desta rodada terminaram. Não reutilizar sessão79591/95506/24793 como viva. "
       "Os fatores de Bayes de fonte não linear não estão aceitos: falta precisão de todas as componentes e repetição independente, "
       "integração SEOB e calibração contínua de a. Melhorar a integração preservando os priors e todas as células; "
       "usar as propostas/amostras já obtidas, sem repetir construção do modelo, oráculos analíticos ou C6. "
       "O diagnóstico mediu 35,78 rad de enrolamento da fase ao variar massa e 12,20 rad ao variar spin. "
       "Próximo passo: implementar PEAK_PHASE_COORDINATES.md, preservando o prior por soma exata das duas pré-imagens "
       "orbitais e todas as harmônicas; validar a identidade por quadratura antes de nova inferência. "
       "Não repetir o mesmo amostrador apenas aumentando o orçamento.")
    status["requirements_remaining"][0] = status["next_action"]
    status["hashes"].update(hashes)
    safe(status_path, (json.dumps(status, indent=2, ensure_ascii=False)+"\n").encode())
    progress = ROOT/"PROGRESSO.md"
    safe(progress, progress.read_bytes()+("\n\n---\n"+text).encode())
    print(json.dumps(dict(status="PROGRESS_NOT_COMPLETE", handoff=str(handoff),
                          precision_accepted=adapted["all_draws_pass_precision"], active_processes=[])))


if __name__ == "__main__":
    main()
