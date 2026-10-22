"""Register measured progress without promoting a closed model set to nature."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path,raw):
    if path.exists():
        old=path.read_bytes();backup=path.with_name(path.name+".bak_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(old)
        if backup.read_bytes()!=old:raise ValueError("Backup differs")
    tmp=path.with_name(path.name+".tmp");tmp.write_bytes(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError("Short write")
    tmp.replace(path)
    if path.read_bytes()!=raw:raise ValueError("Replacement differs")


def main():
    handoff=ROOT.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C5_recuperacao_IMR_e_limites.md"
    if handoff.exists():raise FileExistsError("Create-once recorder")
    output=json.loads((ROOT/"C5_IMR_RECOVERY.json").read_bytes())
    validation=json.loads((ROOT/"C5_IMR_RECOVERY_VALIDATION.json").read_bytes())
    package=json.loads((ROOT/"C7_IMR_RECOVERY_PACKAGE.json").read_bytes())
    replays=list((ROOT/package["package"]/"cache").glob("run_*/RESULT.json"))
    if len(replays)!=1:raise ValueError("Replay absent or ambiguous")
    replay=json.loads(replays[0].read_bytes())
    if replay["status"]!="PASS" or validation["status"]!="PASS":raise ValueError("Numerical verification failed")
    if sha(ROOT/package["archive"])!=package["sha256"]:raise ValueError("Package changed")
    if any(r["max_absolute_difference"]!=0 for r in replay["arrays"]):raise ValueError("Unexpected fresh draw difference")
    reg=json.loads((ROOT/"REGISTRO_C5_IMR_RECOVERY.json").read_bytes())
    for name,value in reg["hashes"].items():
        if sha(ROOT/name)!=value:raise ValueError("Registered source changed")
    now=datetime.now(timezone.utc).isoformat()
    supplemental=dict(status="PASS",date_utc=now,package=package,replay=replay,
                      replay_path=replays[0].relative_to(ROOT).as_posix(),replay_sha256=sha(replays[0]),
                      scientific_scope=output["scope"])
    replay_receipt=ROOT/"C7_IMR_RECOVERY_REPLAY_VALIDATION.json"
    if replay_receipt.exists():raise FileExistsError(replay_receipt)
    write(replay_receipt,(json.dumps(supplemental,indent=2)+"\n").encode())
    identities=["R-B","R-RAIZ-0","R-LIN","R-MOD"]
    groups=[r for r in output["joint_mixture_criteria"] if r["reading"] in identities]
    passed=sum(r["pass_all_four"] for r in groups)
    if len(groups)!=24 or passed!=19:raise ValueError("Review outcome before recording")
    b=[r for r in output["results"] if r["reading"]=="R-B" and r["recovery"]=="EQUAL_FAMILY_MIXTURE"]
    b40=[r for r in b if r["SNR"]==40.]
    opposite=[r for r in output["results"] if r["recovery"] not in (r["injection_family"],"EQUAL_FAMILY_MIXTURE") and r["absolute_bias"] is not None]
    if any(r["status"]=="CALIBRATED_CONDITIONAL_CELL" for r in opposite):raise ValueError("Review opposite-family outcome")
    compact=dict(cells=len(output["results"]),N_per_cell=206,paired_noise_indices=[50,256],
                 identifiable_joint_groups=24,joint_mixture_groups_passed=19,
                 same_family_passing_cells=sum(r["status"]=="CALIBRATED_CONDITIONAL_CELL" and r["recovery"]==r["injection_family"] for r in output["results"]),
                 mixture_passing_cells=sum(r["status"]=="CALIBRATED_CONDITIONAL_CELL" and r["recovery"]=="EQUAL_FAMILY_MIXTURE" for r in output["results"]),
                 opposite_family_passing_cells=0,opposite_family_identifiable_cells=len(opposite),
                 B_at_SNR40=dict(all_joint_groups_pass=False,bias_range=[min(r["absolute_bias"] for r in b40),max(r["absolute_bias"] for r in b40)],
                                coverage90_range=[min(r["coverage_90"] for r in b40),max(r["coverage_90"] for r in b40)]),
                 independent_SVD_max_error=validation["max_lnB_abs_difference"],
                 scientific_acceptance="PARTIAL_FIXED_SOURCE_CLOSED_MODEL_SET_ONLY",
                 observed_C6_verdict_unchanged="INCONCLUSIVE_SYSTEMATICS")
    artifacts=["REGISTRO_C5_IMR_RECOVERY.json","calibrate_imr_recovery.py","C5_IMR_RECOVERY.json",
               "verify_imr_recovery.py","C5_IMR_RECOVERY_VALIDATION.json","package_reproduce_imr_recovery.py",
               "build_imr_recovery_package.py","C7_IMR_RECOVERY_PACKAGE.json","C7_IMR_RECOVERY_REPLAY_VALIDATION.json",
               package["archive"]]+[x["path"] for x in output["draws"]]
    hashes={name:sha(ROOT/name) for name in artifacts}
    manifest_path=ROOT/"cache/MANIFESTO_DOWNLOADS.json"
    manifest=json.loads(manifest_path.read_bytes());entries={x["path"].replace("\\","/"):x for x in manifest["files"]}
    for name in [package["archive"],*[x["path"] for x in output["draws"]]]:
        entries[name]=dict(path=name,bytes=(ROOT/name).stat().st_size,sha256=sha(ROOT/name),
                           origin="Own conditional IMR recovery experiment; public-derived inputs declared in registration")
    manifest.update(at=now,status="PRIOR_ENTRIES_PRESERVED_NEW_ARTIFACTS_HASHED",files=list(entries.values()))
    write(manifest_path,(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode())
    hashes["cache/MANIFESTO_DOWNLOADS.json"]=sha(manifest_path)
    remaining=[
        "A recuperação IMR resolve a discrepância apenas no conjunto fechado testado: 19/24 grupos passam, mas o gerador verdadeiro está entre os candidatos e massas/spins/extrínsecos estão fixados. Para PE astrofísica, estudar a marginalização dos parâmetros da fonte e validação fora dessa identidade injeção-recuperação, com registro não-cego separado.",
        "O ramo B continua sem calibração em SNR40 nas duas PSDs; zero de 96 células identificáveis com recuperação somente pela família oposta passou. Não transportar o sucesso de SNR200/600 para o evento real nem alterar o C6 congelado.",
        "A verossimilhança original está numericamente conferida com pyRing; a comparação com posteriores publicados ainda usa modos/priors/pré-processamento diferentes e não há produto 10,5 tM no release inspecionado.",
        "Partição/relógio/desenrolamento físicos continuam não selecionados conforme a ordem. Kay-Wald/Milburn seguem no escopo efetivamente lido. Não refazer consolidação C1, reproduções dos catálogos ou os 576 cálculos já entregues."
    ]
    status_path=ROOT/"STATUS_ORDEM_013.json";status=json.loads(status_path.read_bytes())
    status.update(date_utc=now,goal_status="ACTIVE_NOT_COMPLETE",active_processes=[],
                  previous_goal_turn="PROGRESS: C1 consolidada e verossimilhança comparada ao pyRing original; pacote v2 reproduzido",
                  this_goal_turn="PROGRESS: recuperação por formas IMR completas registrada e testada, 576 células/206 intervalos, SVD independente e reprodução em pasta limpa",
                  requirements_remaining=remaining,next_action=remaining[0],no_blocker_recurrence=True)
    status["verified"]["C5_full_IMR_recovery_extension"]=compact
    status["verified"]["C7_IMR_recovery_reproduction"]=supplemental
    status["hashes"].update(hashes)
    write(status_path,(json.dumps(status,ensure_ascii=False,indent=2)+"\n").encode())
    rows="\n".join(f"| {r['psd']} | {r['reading']} | {r['SNR']:g} | {'PAGO neste conjunto' if r['pass_all_four'] else 'NÃO PAGO'} |" for r in groups)
    text=f'''[REAL — injeções, cálculo e custódia; DERIVED condicional nas taxas; NÃO-CEGO; sem promoção a confirmação física]

# Ordem 013 — recuperação com formas IMR completas

UTC: {now}. Axiomas: N/A — sem Lean.

## Resultado

As formas IMR completas substituíram a base curta de QNMs somente neste novo estudo. Foram preservadas as duas famílias, oito leituras, β calculado em runtime e os critérios viés≤0,2, cobertura de 90% em [0,80;0,97], sem borda.

**19 de 24 grupos identificáveis passaram** conjuntamente nas duas famílias e nas duas amplitudes com a mesma verossimilhança de mistura. Total: 576 células, 206 intervalos de ruído por célula, O4/O5 e SNR de ringdown 40/200/600. Os intervalos 50:256 eram externos ao treinamento da PSD e não foram usados no forecast anterior de 50 injeções; são reutilizados entre cenários, não 118.656 eventos independentes.

Há 78 células individuais aprovadas na mistura e 76 na recuperação pela própria família. **Nenhuma das 96 células identificáveis recuperadas somente pela família oposta passou.** Metade das 576 células é sub-resolução e não recebe um selo de calibração.

| PSD | Leitura | SNR de ringdown | Duas famílias × a=0/1, mistura |
|---|---|---:|---|
{rows}

## O limite que impede promover o resultado

O gerador verdadeiro está contido na mistura, e a fonte é um único binário com massas, spins, inclinação e fase fixados. O teste paga calibração **dentro desse conjunto fechado**, não robustez para uma fonte arbitrária ou estimação dos parâmetros desconhecidos. A análise por família oposta torna esse limite mensurável.

**R-B em SNR40 continua NÃO PAGO**: viés entre {compact['B_at_SNR40']['bias_range'][0]:.6g} e {compact['B_at_SNR40']['bias_range'][1]:.6g}; cobertura entre {compact['B_at_SNR40']['coverage90_range'][0]:.6g} e {compact['B_at_SNR40']['coverage90_range'][1]:.6g}. O sucesso de SNR200/600 não se transporta para a sensibilidade atual. Uma razão de Bayes média positiva também aparece sob a=0 em baixo SNR; não convertê-la em sigma.

As taxas são aplicadas a todo o conteúdo dos harmônicos 22/44, cada qual com sua taxa fundamental; outros harmônicos permanecem como no controle. Essa transposição continua condicional. A mistura bayesiana tem prior 1/2 para cada família e soma evidências; o máximo entre famílias é usado apenas no perfil diagnóstico. Não se seleciona a família que produz a frase desejada.

## Verificação e reprodução

- **PAGO:** registro separado antes da execução, código e entradas conferidos por hash; nenhum novo strain on-source lido.
- **PAGO:** critérios recalculados de todas as 288 células identificáveis a partir dos sorteios gravados.
- **PAGO:** 96 células e 288 sorteios conferidos por integral SVD independente; maior diferença de ln B = {validation['max_lnB_abs_difference']:.12g}. A base da própria família contém exatamente a injeção sem ruído, controle explícito que não é robustez externa.
- **PAGO:** reprodução em pasta nova: {replay['numeric_fields']} campos numéricos, identidades e estatutos conferidos; todas as diferenças nos arrays de sorteios foram zero.
- **PAGO:** pacote `{package['archive']}`, {package['bytes']} bytes. Começa de matrizes IMR/ruído derivadas e conferidas. A produção dessas entradas desde strain público/PyCBC/LAL já está no pacote anterior C7_INJECTION_REPRODUCTION; não foi repetida.
- **NÃO PAGO:** marginalização de parâmetros da fonte e validação fora do conjunto finito contendo o gerador da própria injeção.
- **INALTERADO:** C5 anterior, C6 congelado, veredito INCONCLUSIVE_SYSTEMATICS, escolha física da partição/relógio/leitura e gate canônico.

## Próximo passo

{remaining[0]}

## Comando e aproveitamento

Descompactar C7_IMR_RECOVERY_REPRODUCTION_v1.zip e executar `python -B reproduce.py` com NumPy/SciPy. Ambiente efetivamente testado: Python 3.12, NumPy 2.5.3 e SciPy 1.18.1. A reprodução verifica o manifesto antes de executar e cria uma nova pasta de trabalho.

Reaproveitados os dois arquivos IMR, as PSDs, o ruído, as taxas e os QNMs já calculados. Nenhum pacote de sistema, um.py, kernel ou memória de outra casa foi alterado. STATUS, PROGRESSO e manifesto local atualizados com backups imediatos byte a byte. Nenhuma falha de execução nesta rodada; os negativos científicos permanecem nos arquivos.

## Custódia lida nesta execução

| Artefato | SHA-256 |
|---|---|
'''
    text+="\n".join(f"| `{n}` | `{v}` |" for n,v in hashes.items())+"\n"
    raw=text.encode();write(handoff,raw)
    progress=ROOT/"PROGRESSO.md";before=progress.read_bytes();write(progress,before+b"\n\n"+raw)
    if not progress.read_bytes().startswith(before):raise ValueError("Memory prefix changed")
    print(json.dumps(dict(status="PROGRESS_NOT_COMPLETE",handoff=str(handoff),summary=compact,
                          package=package["archive"]),ensure_ascii=False),flush=True)


if __name__=="__main__":main()
