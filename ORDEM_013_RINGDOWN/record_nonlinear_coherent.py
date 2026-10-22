"""Record measured nonlinear controls, peak correction and portable replay."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def safe(p,raw):
    old=p.read_bytes() if p.exists() else None
    if old is not None:
        backup=p.with_name(p.name+".bak_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(old)
        if backup.read_bytes()!=old:raise ValueError("Byte backup failed")
    tmp=p.with_name(p.name+".tmp");tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError("Short write")
    if old is not None and p.read_bytes()!=old:raise ValueError("Concurrent memory modification")
    tmp.replace(p)
    if p.read_bytes()!=raw:raise ValueError("Replacement differs")


def main():
    run=ROOT/"cache/nonlinear_intrinsic_peak"
    handoff=ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_fonte_nao_linear_e_pico_intrinseco.md"
    if handoff.exists():raise FileExistsError("Create-once recorder")
    reg=json.loads((run/"REGISTRO_C5_NONLINEAR_COHERENT.json").read_bytes())
    for n,h in reg["hashes"].items():
        if sha(run/n)!=h:raise ValueError("Registered input changed")
    if sha(ROOT/"REGISTRO_C6.json")!=reg["hashes"]["REGISTRO_C6.json"]:raise ValueError("Original C6 changed")
    result=json.loads((run/"C5_NONLINEAR_COHERENT.json").read_bytes())
    validation=json.loads((run/"C5_NONLINEAR_COHERENT_VALIDATION.json").read_bytes())
    prior=json.loads((run/"C5_COHERENT_LIKELIHOOD_VALIDATION.json").read_bytes())
    diagnosis=json.loads((ROOT/"C5_COHERENT_PEAK_DIAGNOSTIC.json").read_bytes())
    package=json.loads((ROOT/"C7_COHERENT_SOURCE_PACKAGE.json").read_bytes())
    if sha(ROOT/package["archive"])!=package["sha256"]:raise ValueError("Archive changed")
    replays=list((ROOT/package["package"]/"cache").glob("replay_*/RESULT.json"))
    if len(replays)!=1:raise ValueError("Replay missing or ambiguous")
    replay=json.loads(replays[0].read_bytes())
    if replay["status"]!="PASS":raise ValueError("Replay failed")
    now=datetime.now(timezone.utc).isoformat()
    receipt=dict(status="PASS",date_utc=now,package=package,replay=replay,
                 replay_path=replays[0].relative_to(ROOT).as_posix(),replay_sha256=sha(replays[0]),
                 scope="Actual IMR generator replay and candidate QR verification; optimizer search not rerun")
    receipt_path=ROOT/"C7_COHERENT_SOURCE_REPLAY_VALIDATION.json"
    safe(receipt_path,(json.dumps(receipt,indent=2)+"\n").encode())
    same=[r for r in validation["checks"] if r["same_family"]]
    opposite=[r for r in validation["checks"] if not r["same_family"]]
    compact=dict(status="NONLINEAR_CONSTRUCTIVE_DEGENERACY_NOT_FULL_SOURCE_PE",cases=len(result["results"]),
        same_family_candidates=len({r["label"] for r in same}),same_family_below_one_in_both_rates=all(r["both_residuals_below_one"] for r in same),
        same_family_residual_range=[min(r["residual_32768"] for r in same),max(r["residual_32768"] for r in same)],
        opposite_family_residual_range=[min(r["residual_32768"] for r in opposite),max(r["residual_32768"] for r in opposite)],
        same_family_gaussian_5sigma_power_upper_range=[min(r["gaussian_power_upper_bound_at_one_sided_5sigma"] for r in same),max(r["gaussian_power_upper_bound_at_one_sided_5sigma"] for r in same)],
        peak_convention_correction=dict(old_jump_s=diagnosis["polarization_peak_range_s"],intrinsic_variation_s=diagnosis["intrinsic_peak_range_s"]),
        exact_distance_polarization_integration_error=prior["max_logz_difference"],QR_error=validation["max_QR_difference"],
        physical_source_evidence="OPEN: seven nonlinear coordinates still require posterior integration and noisy varied-source calibration",
        original_C6_unchanged="INCONCLUSIVE_SYSTEMATICS")
    summary=ROOT/"C5_NONLINEAR_SOURCE_SUMMARY.json"
    safe(summary,(json.dumps(dict(date_utc=now,**compact,checks=validation["checks"]),ensure_ascii=False,indent=2)+"\n").encode())
    names=["coherent_imr_model.py","coherent_imr_likelihood.py","nonlinear_coherent_recovery.py",
           "validate_coherent_model.py","validate_coherent_likelihood.py","REGISTRO_C5_NONLINEAR_COHERENT.json",
           "C5_COHERENT_MODEL_VALIDATION.json","C5_COHERENT_LIKELIHOOD_VALIDATION.json","C5_NONLINEAR_COHERENT.json",
           "C5_COHERENT_PEAK_DIAGNOSTIC.json","diagnose_coherent_peak.py","prepare_intrinsic_peak_run.py",
           "verify_nonlinear_coherent.py","build_coherent_source_package.py","C7_COHERENT_SOURCE_PACKAGE.json",
           "C7_COHERENT_SOURCE_REPLAY_VALIDATION.json","C5_NONLINEAR_SOURCE_SUMMARY.json",Path(__file__).name,package["archive"]]
    artifacts=[ROOT/n for n in names]
    artifacts += [run/n for n in ("REGISTRO_C5_NONLINEAR_COHERENT.json","C5_NONLINEAR_COHERENT.json",
                                  "C5_NONLINEAR_COHERENT_VALIDATION.json","C5_COHERENT_MODEL_VALIDATION.json",
                                  "C5_COHERENT_LIKELIHOOD_VALIDATION.json","PEAK_CORRECTION_PROVENANCE.json",
                                  "coherent_imr_model.py","nonlinear_coherent_recovery.py")]
    hashes={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts}
    manifest=ROOT/"cache/MANIFESTO_DOWNLOADS.json";m=json.loads(manifest.read_bytes())
    entries={r["path"].replace("\\","/"):r for r in m["files"]}
    entries[package["archive"]]=dict(path=package["archive"],sha256=sha(ROOT/package["archive"]),bytes=(ROOT/package["archive"]).stat().st_size,
                                   origin="Own coherent nonlinear-source supplement; public PyCBC/LAL and previously frozen offsource covariance")
    m.update(at=now,files=list(entries.values()),status="PRIOR_ENTRIES_PRESERVED_COHERENT_SOURCE_PACKAGE_ADDED")
    safe(manifest,(json.dumps(m,indent=2,ensure_ascii=False)+"\n").encode());hashes["cache/MANIFESTO_DOWNLOADS.json"]=sha(manifest)
    status_path=ROOT/"STATUS_ORDEM_013.json";status=json.loads(status_path.read_bytes())
    remaining=[
      "Há agora uma likelihood de fonte não linear com distância/polarização comuns integradas exatamente. Falta integrar os sete parâmetros de fonte e medir distribuições O4/O5 e cobertura sob fontes variadas; candidatos de Powell não são posteriores nem fatores de Bayes. Usar o módulo corrigido em cache/nonlinear_intrinsic_peak (ou C7_COHERENT_SOURCE_REPRODUCTION), não a versão histórica de pico projetado.",
      "As seis fontes/famílias próprias admitem candidatos GR com resíduo menor que um em SNR40, verificado até 32768 Hz; isso demonstra degenerescência construtiva no cenário condicional. As trocas de família continuam a produzir erro de modelo. Não repetir Fisher nem tomar budgets de otimização como calibração; não usar posterior do mesmo evento como prior.",
      *status["requirements_remaining"][2:]
    ]
    status.update(date_utc=now,previous_goal_turn="PROGRESS: incerteza local da fonte e três rodadas de controle de derivadas",
                  this_goal_turn="PROGRESS: 24 buscas não lineares, correção mensurada do pico, integral física comum, verificação QR e reprodução de candidatos em pasta nova",
                  goal_status="ACTIVE_NOT_COMPLETE",active_processes=[],requirements_remaining=remaining,next_action=remaining[0],no_blocker_recurrence=True)
    status["verified"]["C5_nonlinear_coherent_source"]=compact
    status["verified"]["C7_coherent_source_replay"]=receipt
    status["hashes"].update(hashes)
    safe(status_path,(json.dumps(status,ensure_ascii=False,indent=2)+"\n").encode())
    table="\n".join(f"| {r['label']} | {r['psd']} | {r['residual_16384']:.6g} | {r['residual_32768']:.6g} | {'sim' if r['both_residuals_below_one'] else 'não'} |" for r in validation["checks"])
    text=f'''[REAL — candidatos de fonte física e verificação numérica; DERIVED condicional no limite de poder; marginalização completa OPEN]

# Ordem 013 — fonte não linear, polarização coerente e correção do pico

UTC: {now}. Axiomas: N/A — sem Lean. O C6 e o programa canônico permanecem intactos.

## Resultado

Foram feitas 12 buscas com a convenção antiga de pico e 12 numa rodada corrigida, reaproveitando os candidatos anteriores. Três binários alinhados, duas famílias de injeção e duas de recuperação. A injeção tem a=1 no ramo B; a recuperação busca uma fonte GR, a=0, variando massa total, razão de massas, ambos os spins, inclinação, fase e instante do pico. Distância e uma polarização são compartilhadas pela rede.

**As seis recuperações pela própria família admitem candidatos sem dephasing com resíduo de {compact['same_family_residual_range'][0]:.4g} a {compact['same_family_residual_range'][1]:.4g} em unidades da métrica de ruído, para SNR de ringdown 40**, nas PSDs O4/O5 de referência. Verificados com geradores a 16384 e 32768 Hz. A busca é local: um candidato válido dá uma cota superior para o melhor resíduo, mesmo quando o otimizador esgota seu orçamento. Não é garantia de ótimo global, cobertura, posterior ou fator de Bayes.

As trocas de família têm resíduos entre {compact['opposite_family_residual_range'][0]:.4g} e {compact['opposite_family_residual_range'][1]:.4g}. Portanto a incerteza do gerador precisa permanecer no modelo. Não se seleciona apenas o ajuste favorável.

| Candidato | PSD | Resíduo a 16384 Hz | Resíduo a 32768 Hz | Ambos abaixo de um |
|---|---|---:|---:|---|
{table}

## A falha identificada e corrigida

Para o par alinhado ±22, h+ é proporcional a (1+cos²i)/2 vezes uma quadratura e h× a cos i vezes a outra. Assim h+²+h×² pode oscilar com a fase quando a fonte é inclinada: seu máximo não é a amplitude intrínseca do modo complexo. No candidato problemático, o pico projetado saltou **{1e3*diagnosis['polarization_peak_range_s']:.6g} ms** ao mudar a resolução. O pico intrínseco variou **{1e6*diagnosis['intrinsic_peak_range_s']:.6g} μs** no mesmo diagnóstico.

A rodada nova usa o máximo da amplitude do 22 visto face-on, antes da projeção para a orientação da fonte, e mantém um único instante para todos os harmônicos. Trata-se de uma convenção nova, registrada separadamente: não alteramos o início ou o resultado do C6. A taxa do modelo continua aplicada ao tempo desde o pico declarado; nenhuma identificação física única de início/desenrolamento é inferida disso. O pico e as buscas antigos permanecem como evidência do erro.

## O que o limite gaussiano permite dizer

Para dois templates fixos h0 e h1, branqueados por uma covariância conhecida, r=||h1−h0||. O estatístico S=⟨h1−h0,Y−h0⟩/r tem distribuição N(0,1) sob h0 e N(r,1) sob h1. Um teste que controle o falso alarme do nulo composto GR também precisa controlá-lo no candidato h0 encontrado. No modelo gaussiano, o melhor poder desse par a um limiar unilateral de cinco sigmas é Φ(r−5).

Nos pares da própria família, isso dá cotas de poder entre {compact['same_family_gaussian_5sigma_power_upper_range'][0]:.6g} e {compact['same_family_gaussian_5sigma_power_upper_range'][1]:.6g} em SNR40. **É uma derivação condicional para os templates e ruído gaussiano, não uma medição da cauda do ruído real, nem uma conversão de ln B para sigma.** Uma fonte sem dephasing quase idêntica impede alto poder uniforme nesse cenário; não exclui a TGL nem elimina a necessidade da inferência.

## Likelihood que fica disponível

`coherent_imr_likelihood.py` reaproveita a integral linear existente com somente dois coeficientes comuns de rede: c=A cos(2ψ), d=A sin(2ψ). Eles representam distância e rotação de polarização, em vez de amplitudes independentes para cada modo/detector. O prior isotrópico gaussiano desses coeficientes equivale a ψ uniforme módulo π e p(D)=403²/(s²D³) exp[−403²/(2s²D²)], D em Mpc. É normalizado e marcado INPUT; não é prior uniforme em volume.

A integral de distância/polarização é exata, inclusive determinante; o maior erro contra a covariância completa foi {prior['max_logz_difference']:.12g}. **Os sete parâmetros não lineares da fonte ainda não foram integrados.** O código não normaliza a forma de onda a um SNR escolhido dentro da likelihood. O SNR40 é apenas a normalização declarada das injeções de controle.

## Critérios, reprodução e aproveitamento

- **PAGO:** modelos físicos de rede com polarização comum; três fontes; ambas as famílias; resultados negativos incluídos.
- **PAGO:** pico intrínseco corrigido por diagnóstico explícito; nova rodada registrada; hashes e C6 original conferidos.
- **PAGO:** regeneração dos 12 candidatos e projeção QR independente, diferença máxima {validation['max_QR_difference']:.12g}; controle em 32768 Hz.
- **PAGO:** pacote inglês `{package['archive']}`, {package['bytes']} bytes; reprodução em pasta nova regenerou os candidatos, com diferença máxima de resíduo {replay['max_residual_difference']:.12g}. O otimizador não foi repetido na reprodução; isso está expresso.
- **NÃO PAGO:** marginalização dos sete parâmetros, distribuição de evidência de fonte completa, calibração de ruído não gaussiano e cobertura sob população de fontes.
- **INALTERADO:** C6 INCONCLUSIVE_SYSTEMATICS, leituras físicas condicionais, escolha de relógio/partição e gate.

Descompactar o pacote e executar `python -B reproduce.py` num Python com PyCBC/LAL/NumPy/SciPy. Versões testadas constam no README e nos recibos. Os arquivos de forma de onda usam dados e geradores públicos; não há programa canônico ou acervo privado no pacote.

{remaining[0]}

As buscas são não cegas, partem das fontes simuladas e de candidatos anteriores, e têm orçamentos limitados. Saídas de orçamento não foram renomeadas como sucesso. Nenhum evento real foi relido. As memórias locais receberam backups imediatos de bytes; a gerência mantém a incorporação canônica.

## Custódia lida nesta execução

| Arquivo | SHA-256 |
|---|---|
'''
    text+="\n".join(f"| `{n}` | `{h}` |" for n,h in hashes.items())+"\n"
    safe(handoff,text.encode());progress=ROOT/"PROGRESSO.md";before=progress.read_bytes();safe(progress,before+b"\n\n"+text.encode())
    if not progress.read_bytes().startswith(before):raise ValueError("Memory prefix changed")
    print(json.dumps(dict(status="PROGRESS_NOT_COMPLETE",handoff=str(handoff),summary=compact),ensure_ascii=False),flush=True)


if __name__=="__main__":main()
