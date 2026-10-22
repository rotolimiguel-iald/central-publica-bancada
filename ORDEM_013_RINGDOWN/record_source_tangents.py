"""Record the source-uncertainty finding without promoting local surrogates.

Only local task memories and the authorized outgoing handoff are written.
Every existing memory gets an immediate byte-identical sibling backup.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p,raw):
    old=p.read_bytes() if p.exists() else None
    if old is not None:
        backup=p.with_name(p.name+".bak_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(old)
        if backup.read_bytes()!=old:raise ValueError("Backup mismatch")
    tmp=p.with_name(p.name+".tmp");tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError("Short write")
    if old is not None and p.read_bytes()!=old:raise ValueError("Concurrent memory change")
    tmp.replace(p)
    if p.read_bytes()!=raw:raise ValueError("Replacement mismatch")


def main():
    handoff=ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_incerteza_da_fonte.md"
    if handoff.exists():raise FileExistsError("Create-once recorder")
    locations=[ROOT,ROOT/"cache/source_tangents_refinement",ROOT/"cache/source_tangents_highrate"]
    runs=[];artifacts=[];cache_files=[]
    for location in locations:
        reg=json.loads((location/"REGISTRO_C5_SOURCE_TANGENTS.json").read_bytes())
        for name,h in reg["hashes"].items():
            if sha(location/name)!=h:raise ValueError("Registered input changed: "+name)
        out=json.loads((location/"C5_SOURCE_TANGENTS.json").read_bytes())
        validation=json.loads((location/"C5_SOURCE_TANGENTS_VALIDATION.json").read_bytes())
        inputs=json.loads((location/"C5_SOURCE_TANGENTS_INPUTS.json").read_bytes())
        if validation["status"]!="PASS_NUMERICAL_INTEGRAL_NOT_FULL_SOURCE_INFERENCE":raise ValueError("Verification missing")
        if out["registration_sha256"]!=sha(location/"REGISTRO_C5_SOURCE_TANGENTS.json"):raise ValueError("Registry mismatch")
        for row in inputs["rows"]:
            p=location/row["path"]
            if sha(p)!=row["sha256"]:raise ValueError("Source waveform changed")
            cache_files.append(p)
        draw=location/out["draws"]["path"]
        if sha(draw)!=out["draws"]["sha256"]:raise ValueError("Noise draws changed")
        cache_files.append(draw)
        for name in ("REGISTRO_C5_SOURCE_TANGENTS.json","C5_SOURCE_TANGENTS_INPUTS.json","C5_SOURCE_TANGENTS.json","C5_SOURCE_TANGENTS_VALIDATION.json"):
            artifacts.append(location/name)
        runs.append(dict(path=location.relative_to(ROOT).as_posix(),waveforms=len(inputs["rows"]),
                         cells=len(out["surrogate_evidence"]),stable=validation["stable_cases"],total=validation["total_stability_cases"],
                         generation_rates=[reg["primary_generation_rate_hz"],reg["high_generation_rate_hz"]],
                         axes=reg["axes"],validation=validation))
    ext=json.loads((ROOT/"C5_SOURCE_TANGENTS_EXTENDED_VALIDATION.json").read_bytes())
    if ext["status"]!="PASS":raise ValueError("Extended integral check failed")
    primary=runs[-1]["validation"];b=[r for r in primary["stability"] if r["reading"]=="R-B"]
    stable_b=[r for r in b if r["status"]=="STABLE_LOCAL_DIAGNOSTIC"]
    latest=json.loads((locations[-1]/"C5_SOURCE_TANGENTS.json").read_bytes())
    # Keep every prior/truth example, including a=0: positive log B is not detection.
    examples=[r for r in latest["surrogate_evidence"] if r["reading"]=="R-B" and r["psd"]=="O5" and r["SNR"] in (40.,600.)]
    now=datetime.now(timezone.utc).isoformat()
    summary=dict(status="LOCAL_SOURCE_INFORMATION_LOSS_MEASURED__FULL_PE_OPEN",date_utc=now,
                 independent_physical_sources="One representative aligned binary; 204 waveform parameter/resolution samples are controls, not independent astrophysical events",
                 runs=[{k:v for k,v in r.items() if k!="validation"} for r in runs],
                 primary_B=b,stable_B_information_fraction_range=[min(r["retained_information_fraction"] for r in stable_b),max(r["retained_information_fraction"] for r in stable_b)],
                 surrogate_B_examples=examples,source_prior_interpretation="INPUT diagnostic Gaussian uncertainties; true source at prior center; no event posterior used as prior",
                 independent_comparisons=sum(r["comparisons"] for r in ext["reports"]),
                 independent_max_lnB_error=max(r["max_lnB_difference"] for r in ext["reports"]),
                 conclusions=["Phenom local source-information loss stable under three registered resolutions/steps",
                              "SEOB derivatives remain resolution-sensitive; no quantitative astrophysical promotion",
                              "Exact affine Gaussian integrals verified, but no nonlinear source marginalization or source-varied calibration",
                              "C6 and physical clock/partition choices unchanged"])
    summary_path=ROOT/"C5_SOURCE_UNCERTAINTY_SUMMARY.json"
    if summary_path.exists():raise FileExistsError(summary_path)
    write(summary_path,(json.dumps(summary,ensure_ascii=False,indent=2)+"\n").encode())
    artifacts += [ROOT/n for n in ("prepare_source_tangents.py","analyze_source_tangents.py","verify_source_tangents.py",
                                  "refine_source_tangents.py","refine_source_tangents_highrate.py","verify_source_tangents_extended.py",
                                  "C5_SOURCE_TANGENTS_EXTENDED_VALIDATION.json","C5_SOURCE_UNCERTAINTY_SUMMARY.json",Path(__file__).name)]
    hashes={p.relative_to(ROOT).as_posix():sha(p) for p in artifacts}
    manifest=ROOT/"cache/MANIFESTO_DOWNLOADS.json";m=json.loads(manifest.read_bytes())
    entries={x["path"].replace("\\","/"):x for x in m["files"]}
    for p in cache_files:
        name=p.relative_to(ROOT).as_posix()
        entries[name]=dict(path=name,bytes=p.stat().st_size,sha256=sha(p),origin="Own registered IMR local-source diagnostic; public generator and existing offsource noise")
    m.update(at=now,files=list(entries.values()),status="PRIOR_ENTRIES_PRESERVED_SOURCE_CONTROLS_HASHED")
    write(manifest,(json.dumps(m,ensure_ascii=False,indent=2)+"\n").encode());hashes["cache/MANIFESTO_DOWNLOADS.json"]=sha(manifest)
    status_path=ROOT/"STATUS_ORDEM_013.json";status=json.loads(status_path.read_bytes())
    remaining=[
        "O diagnóstico local da fonte está calculado, mas não substitui marginalização não linear. Phenom mantém só 0,8–2,7% da informação local do ramo B depois dos parâmetros livres testados. A família SEOB falha nos controles de derivada mesmo com refinamento; avançar com avaliação não linear/coerente de fonte, sem trocar isso por mais rodadas de Fisher ou aceitar números instáveis.",
        "As razões de Bayes novas integram somente um modelo afim com priors diagnósticos centrados na fonte simulada. É necessário medir cobertura/viés com fontes variadas e modelo físico de rede antes de promovê-las a forecast astrofísico. Não reutilizar posterior do mesmo evento como prior.",
        "R-B em SNR40 continua não calibrado na análise IMR original; C6 congelado permanece INCONCLUSIVE_SYSTEMATICS. Os êxitos com fonte fixa em SNR200/600 não justificam 5 sigma com fonte desconhecida.",
        *status["requirements_remaining"][2:]
    ]
    status.update(date_utc=now,previous_goal_turn="NO_GOAL_PROGRESS: respondeu apenas ao pedido do prompt curto; pesquisa retomada após revalidação",
                  this_goal_turn="PROGRESS: 204 formas IMR de controle, três rodadas de convergência, 288 distribuições afins por rodada e 648 comparações integrais independentes",
                  goal_status="ACTIVE_NOT_COMPLETE",active_processes=[],requirements_remaining=remaining,
                  next_action=remaining[0],no_blocker_recurrence=True)
    status["verified"]["C5_source_uncertainty_local"]=summary
    status["hashes"].update(hashes)
    write(status_path,(json.dumps(status,ensure_ascii=False,indent=2)+"\n").encode())
    table="\n".join(f"| {r['family']} | {r['psd']} | {r['a']:g} | {r['z_fixed_SNR40']:.6g} | {r['z_free_SNR40']:.6g} | {100*r['retained_information_fraction']:.4g}% | {r['status']} |" for r in b)
    text=f'''[REAL — diagnóstico local e integrais verificadas; INPUT nos priors e na transposição física; inferência astrofísica completa OPEN]

# Ordem 013 — incerteza da fonte e limites do resultado com fonte fixa

UTC: {now}. Axiomas: N/A — sem Lean. Nenhuma mudança do gate, do um.py ou do C6.

## Resultado e interpretação

A rodada anterior de recuperação IMR fixava massas, spins, fase e inclinação. Esta extensão mede a informação que resta ao acrescentar, à mesma liberdade de amplitudes por detector, o instante do pico e quatro parâmetros intrínsecos: log da massa total, log da razão de massas, deslocamento comum dos spins alinhados e deslocamento oposto dos spins. A inclinação e o céu ainda são fixos. São duas famílias, O4/O5 de referência, quatro leituras observáveis, a=0/1 e uma única fonte representativa.

**Na família Phenom, o ramo B conserva cerca de {100*summary['stable_B_information_fraction_range'][0]:.3g}% a {100*summary['stable_B_information_fraction_range'][1]:.3g}% da informação local disponível após ajustar amplitudes, ao liberar também tempo e parâmetros da fonte.** O resultado é estável sob refinamento. Isso mede degenerescência neste modelo; não é exclusão da leitura B e não mede significância de um evento.

Na SEOB, a derivada da razão de massas e a dos spins continuam sensíveis à resolução. As estimativas estão preservadas e marcadas **NUMERICAL_SENSITIVITY_UNRESOLVED**. Não escolhemos o refinamento que produziria um resultado desejado. Passaram 16/32 controles em cada rodada: os 16 da Phenom. Essa contagem não representa uma aprovação física por maioria.

| Família | PSD | a de referência | z local, fonte fixa, SNR40 | z local, fonte livre, SNR40 | Informação restante | Controle |
|---|---|---:|---:|---:|---:|---|
{table}

O símbolo z nesta tabela é a norma local da derivada projetada, em unidades de ruído ideal, para Δa=1. É um diagnóstico de Fisher. Não é sigma observado nem conversão de fator de Bayes. O SNR é referido ao sinal nominal a=0 neste novo teste; não é exatamente a renormalização de cada injeção da rodada anterior.

## Construção e controle da conta

Escrevendo d=∂h/∂a e A para as colunas de parâmetros indesejados após branqueamento, calculamos d_perp=(I−AA⁺)d e I_a=||d_perp||². Os ranks são conferidos com três tolerâncias. As derivadas intrínsecas vêm de formas IMR novas, geradas por PyCBC/LAL, com o remanescente próprio de cada família; não de uma alteração arbitrária da frequência do QNM.

O pico é o máximo contínuo, por spline, da amplitude do harmônico 22. Todos os harmônicos compartilham esse pico. A janela de dados fica fixa em 10 tM do remanescente nominal enquanto variamos a fonte. Isso evita transformar mudança de janela em informação de massa.

Foram geradas 68 formas por rodada: nominal e diferenças centrais, mais controles de resolução. A segunda rodada divide os passos por quatro; a terceira dobra as taxas de geração para 16384/32768 Hz. As duas anteriores, seus registros e resultados continuam intactos. Total 204 formas de controle, não 204 eventos físicos independentes.

## Distribuições de razão de Bayes: escopo estritamente afim

Cada rodada também calcula 288 distribuições de ln B, com 206 intervalos de ruído por célula, usando os mesmos intervalos externos 50:256 já conhecidos. São reutilizados entre cenários e rodadas. A integral é a de um modelo afim h=h_a+J_a·u, com prior gaussiano normalizado em u. Assim C_a=I+J_a Σ J_aᵀ e log Z_a=−(r_aᵀC_a⁻¹r_a+log det C_a)/2, fora a constante comum.

Os três priors da fonte são: fixo, σ=0,002 e σ=0,02 em cada uma das quatro coordenadas declaradas. Eles são **INPUT diagnóstico**, centrados na fonte simulada. Não são informação do evento nem derivação da TGL. As amplitudes têm prior próprio, idêntico em definição entre hipóteses; a integração inclui o determinante. Também calculamos média e variância analíticas para ruído gaussiano ideal no centro do prior, mantendo-as separadas do ruído empírico.

Esses resultados não substituem uma integral sobre formas de onda não lineares. Uma média positiva sob a=0, que continua possível por efeito do prior, não é detecção. Os números completos de ambos a=0/1 estão no resumo JSON, sem selecionar somente a hipótese favorável.

## Critérios e evidências

- **PAGO:** registro e hashes antes de cada rodada; parâmetros físicos e regras de aceitação declarados; nenhum novo strain do evento lido.
- **PAGO:** integral afim conferida por Cholesky da covariância completa, independente da implementação SVD de produção: {summary['independent_comparisons']} comparações, maior diferença de ln B={summary['independent_max_lnB_error']:.12g}.
- **PAGO no escopo local:** convergência das derivadas e informação projetada na Phenom, nas quatro leituras/duas PSDs/duas amplitudes.
- **NÃO PAGO:** convergência da SEOB pelo critério pré-fixado; derivadas sensíveis preservadas como tal.
- **NÃO PAGO:** cobertura/viés sob variação não linear de fontes, marginalização astrofísica completa e rede com polarizações coerentes. As 12 amplitudes independentes por detector são uma flexibilidade fenomenológica, não uma inferência física de orientação.
- **INALTERADO:** C6, seus hashes, o veredito INCONCLUSIVE_SYSTEMATICS, as leituras físicas abertas e os pacotes anteriores.

## Próximo passo e aproveitamento

{remaining[0]}

Reaproveitados PSDs, ruído externo, QNMs, leis condicionais e geradores já instalados. Nada foi instalado em /opt. Para reproduzir o cálculo de uma rodada já gerada, entrar em sua pasta e executar `python -B analyze_source_tangents.py` seguido de `python -B verify_source_tangents.py` **em uma cópia nova com as saídas removidas da cópia**, preservando as entradas/registro; os scripts recusam sobrescrever resultados. A análise exige NumPy/SciPy; gerar fontes exige PyCBC/LAL. `verify_source_tangents_extended.py` confere as três rodadas sem repetir a geração. A geração usa só fontes públicas e o ruído derivado já custodiado. Não se entrega um novo ZIP duplicando os pacotes anteriores nesta etapa diagnóstica.

As falhas desta rodada são os controles numéricos da SEOB, registrados nos três resultados; as execuções terminaram com código zero. Não há processo em curso. STATUS, PROGRESSO e manifesto foram atualizados com backup imediato de bytes. Memórias canônicas são somente leitura nesta ordem.

## Custódia lida nesta execução

| Arquivo | SHA-256 |
|---|---|
'''
    text+="\n".join(f"| `{n}` | `{h}` |" for n,h in hashes.items())+"\n"
    write(handoff,text.encode())
    progress=ROOT/"PROGRESSO.md";before=progress.read_bytes();write(progress,before+b"\n\n"+text.encode())
    if not progress.read_bytes().startswith(before):raise ValueError("Progress history changed")
    print(json.dumps(dict(status="PROGRESS_NOT_COMPLETE",handoff=str(handoff),stable_B_information_fraction_range=summary["stable_B_information_fraction_range"],
                         verified_comparisons=summary["independent_comparisons"]),ensure_ascii=False),flush=True)


if __name__=="__main__":main()
