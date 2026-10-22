"""Record the completed C1/upstream-oracle work with immediate byte backups."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_write(path, raw):
    before = path.read_bytes() if path.exists() else None
    if before is not None:
        backup = path.with_name(path.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(before)
        if backup.read_bytes() != before:
            raise ValueError("Memory backup differs")
    temp = path.with_name(path.name+".tmp")
    temp.write_bytes(raw)
    if temp.stat().st_size != len(raw):
        raise ValueError("Incomplete temporary write")
    temp.replace(path)
    if path.read_bytes() != raw:
        raise ValueError("Memory changed after replacement")


def main():
    handoff = ROOT.parent / "TUNEL/DO_CHATGPT/ENTREGA_013_C1_C6_leituras_e_oraculo_pyring.md"
    if handoff.exists():
        raise FileExistsError("Create-once handoff")
    audit = json.loads((ROOT/"C7_C1_C6_ADDENDUM.json").read_bytes())
    package = json.loads((ROOT/"C7_C1_C6_ADDENDUM_VALIDATION.json").read_bytes())
    fresh = ROOT/package["fresh_directory"]/"C1_C6_ADDENDUM"
    results = list((fresh/"cache").glob("oracle_*/RESULT.json"))
    if len(results) != 1:
        raise ValueError("Fresh numerical replay is not completed uniquely")
    replay = json.loads(results[0].read_bytes())
    if replay["status"] != "PASS" or package["status"] != "PASS":
        raise ValueError("Delivery failed")
    if sha(ROOT/package["archive"]) != package["sha256"]:
        raise ValueError("Delivered package changed")
    original = json.loads((ROOT/"C6_PYRING_IMPLEMENTATION_ORACLE.json").read_bytes())
    if replay["numeric_stats"] != original["stats"]:
        raise ValueError("Fresh-directory oracle differs")
    now = datetime.now(timezone.utc).isoformat()
    followup = dict(status="PASS", date_utc=now, replay=replay,
                    result_path=results[0].relative_to(ROOT).as_posix(), result_sha256=sha(results[0]),
                    artifact_manifest_validation=package,
                    all_numeric_stats_identical=True,
                    scope="Fresh numerical execution with the same checked compiled binary; not an independent compiler run")
    receipt = ROOT/"C7_C1_C6_REPLAY_VALIDATION.json"
    if receipt.exists():
        raise FileExistsError(receipt)
    safe_write(receipt, (json.dumps(followup,indent=2)+"\n").encode())
    names = ["C1_LEITURAS.json", "C1_LEITURAS.md", "complete_c1_contract.py",
             "C6_PYRING_IMPLEMENTATION_ORACLE.json", "verify_pyring_likelihood.py",
             "prepare_pyring_oracle.py", "package_reproduce_pyring_oracle.py",
             "build_c1_c6_addendum.py", "C7_C1_C6_ADDENDUM.json", "C7_C1_C6_ADDENDUM.md",
             "C7_C1_C6_ADDENDUM_VALIDATION.json", "C7_C1_C6_REPLAY_VALIDATION.json",
             "cache/pyring_oracle/PREPARATION.json", package["archive"]]
    hashes = {n:sha(ROOT/n) for n in names}
    manifest_path = ROOT/"cache/MANIFESTO_DOWNLOADS.json"
    manifest = json.loads(manifest_path.read_bytes())
    rows = {r["path"].replace("\\", "/"):r for r in manifest["files"]}
    for name in [package["archive"], "cache/pyring_oracle/PREPARATION.json"]:
        rows[name] = dict(path=name, bytes=(ROOT/name).stat().st_size, sha256=sha(ROOT/name),
                          origin="Task-local research delivery or dependency-build receipt")
    manifest.update(at=now, status="PRIOR_ENTRIES_PRESERVED_NEW_ARTIFACTS_HASHED", files=list(rows.values()),
                    pyring_oracle_installation=dict(date_utc=now, receipt="cache/pyring_oracle/PREPARATION.json",
                                                    source_unmodified=True, system_environment_modified=False))
    safe_write(manifest_path, (json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode())
    hashes["cache/MANIFESTO_DOWNLOADS.json"] = sha(manifest_path)
    remaining = [
        "C5: resolver o viés de recuperação da forma de onda. Os 4608 cálculos e sua reprodução já terminaram; nenhum grupo FULL_IMR passa as duas famílias e as duas amplitudes. Próxima ação científica: avaliar recuperação com formas IMR completas (rota b), em estudo não-cego separado, preservando o C6 e os critérios originais. Não repetir a grade QNM já reprovada nem ajustar critérios para obter aprovação.",
        "C6: o código gaussiano está conferido contra pyRing; uma reprodução idêntica do posterior publicado ainda exigiria seus modos, priors e pré-processamento. Não chamar os 285 controles desta rodada de reprodução dos posteriores. Produto 10,5 tM ausente no release inspecionado.",
        "Identificação física de partição, relógio e leitura continua aberta e sem escolha, conforme a ordem; taxas e Bayes permanecem condicionais.",
        "Kay-Wald/Milburn continuam com leitura de resumo somente. Essa limitação não vira teorema físico. C1 documental está completa; não refazer sua consolidação nem as reproduções já entregues."
    ]
    status_path = ROOT/"STATUS_ORDEM_013.json"
    status = json.loads(status_path.read_bytes())
    status.update(date_utc=now, goal_status="ACTIVE_NOT_COMPLETE", active_processes=[],
                  previous_goal_turn="NO_GOAL_PROGRESS: o último turno visível respondeu apenas ao pedido de prompt simples; o objetivo completo foi relido nesta continuação",
                  this_goal_turn="PROGRESS: C1 auditada; pyRing original compilado em cache, 285 controles executados e reproduzidos; pacote v2 e memória atualizados",
                  no_blocker_recurrence=True, requirements_remaining=remaining, next_action=remaining[0])
    status["verified"]["C1_contract"] = audit["C1"]
    status["verified"]["C6_upstream_implementation_oracle"] = dict(status=original["status"], stats=original["stats"],
        source_sha256=original["source_sha256"], limits=original["limitations"])
    status["verified"]["C7_delivery_bundle_v2"] = dict(**package, replay_receipt=receipt.name,
                                                     replay_now_completed=True)
    status["verified"]["C7"]["status"] = "V2_AND_UPSTREAM_ORACLE_REPLAY_VERIFIED__SCIENTIFIC_CALIBRATION_OPEN"
    status["preserved_failures"] += [
        "C1 contract generator initially expected x for R-RAIZ-COHERENT; KeyError occurred before output. First version preserved as complete_c1_contract.py.bak_COHERENT_HAS_NO_EXPONENTIAL_X; fixed to retain x/delta_tau null for a non-exponential mixture.",
        "Read-only WSL inventory was denied by the sandbox service; authorized escalation succeeded. pyRing build process 35031 terminated with exit zero; fresh-replay process 96886 likewise.",
        "pyRing emitted pkg_resources deprecation and optional surfinBH-unavailable warnings. setuptools was pinned locally below 81; no surrogate or remnant function requiring surfinBH was used.",
        "pip noted that vendor/bin already exists; only imported scientific extension functions were used, and no entrypoint script replacement was needed."
    ]
    status["hashes"].update(hashes)
    safe_write(status_path, (json.dumps(status,ensure_ascii=False,indent=2)+"\n").encode())
    s = original["stats"]
    text = f'''[REAL — controle de implementação e custódia; DERIVED/INPUT/CONJECTURE nas leituras físicas; NÃO-CEGO]

# Ordem 013 — C1 completa e oráculo original do pyRing

UTC: {now}. Axiomas: N/A — sem Lean novo.

## Critérios, um a um

- **PAGO — C1 documental:** dez leituras, nove âncoras, dezoito linhas numéricas e dez verificações de unidade. `C1_LEITURAS.json/.md` reúne operador, relógio/estatuto, FP-5, fonte/novidade, universalidade e dependência em distância. Conferidos hashes e textos das âncoras. A escolha e a relação com as falas do operador permanecem `null`.
- **PAGO — implementação gaussiana de C6:** executado pyRing 2.7.0 original, compilado somente em cache. Fonte likelihood.pyx instalada idêntica à distribuição pública. Nove casos Toeplitz, seis vetores de ruído fora do evento e 270 integrais. Erro máximo em log-evidência: {s['max_marginal_lnZ_error']:.12g}; em log-densidade projetada: {s['max_projected_log_density_error']:.12g}. A omissão intencional do determinante produz diferença {s['missing_determinant_control_difference']:.12g}, recusada.
- **PAGO — reprodução em pasta limpa:** todos os valores do novo oráculo coincidiram exatamente. Foi reutilizado o binário compilado e conferido; não chamar isso de nova compilação independente. O teste não leu novamente o strain do evento.
- **PAGO — pacote v2:** `{package['archive']}`, {package['bytes']} bytes; {package['verifier']['files']} arquivos do manifesto verificados após extração nova. O v1 permanece intacto, inclusive seus resultados e reproduções.
- **NÃO PAGO — calibração científica C5:** continua reprovada conjuntamente nas duas famílias/duas amplitudes. O oráculo elimina uma suspeita aritmética específica; não elimina o viés do modelo de forma de onda.
- **PARCIAL — validação pelo posterior publicado:** a comparação pyRing continua com modos/priors/pré-processamento distintos; o release inspecionado não tem 10,5 tM. O oráculo verifica a implementação gaussiana, não a equivalência desses problemas inferenciais.
- **ABERTO — ponte física:** nenhuma partição, relógio ou desenrolamento foi escolhido. A realização KMS finita e as predições continuam condicionais; Kay-Wald/Milburn somente no escopo dos resumos efetivamente lidos.

## Aproveitamento

Foram reutilizados a matriz C1, os relógios da v369 congelada, a covariância e o ruído off-source de C5, o registro C6 e os quatro pacotes já reproduzidos. Não houve nova função em um.py, nova pedra Lean, nova PE de posterior ou repetição do catálogo. A instalação do pyRing usa o tarball público já existente e dependências somente sob cache/pyring_oracle.

Também foi conferida a suspeita de atribuição de remanescente: SEOBNRv4HM já usa a função SEOB correspondente; IMRPhenomXPHM já usa suas funções FinalMass2017/FinalSpin2017. Não há correção a fazer nessa atribuição, e ela não explica o viés.

## Próxima ação científica

{remaining[0]}

Nenhum resultado de strain foi promovido: INCONCLUSIVE_SYSTEMATICS permanece. Não multiplicar os posteriores do mesmo evento nem tratar estes controles numéricos como observações. O objetivo continua ativo, sem reivindicação de precisão integral já alcançada.

## Reprodução

Descompactar o v2, executar `python verify_delivery.py`, entrar em `C1_C6_ADDENDUM` e executar `python -B reproduce.py --download` no ambiente científico da entrega. Para reutilizar a distribuição conferida: `--source-archive /path/to/pyRingGW-2.7.0.tar.gz`. A opção `--vendor-cache /path/to/vendor` registra explicitamente o reaproveitamento de binário.

O recibo separado `C7_C1_C6_REPLAY_VALIDATION.json` paga a pendência histórica `independent_directory_oracle_replay=PENDING` do recibo imutável do empacotamento. Não sobrescrever o histórico para esconder a sequência.

## Tentativas e memória

A primeira tentativa do gerador C1 falhou por pedir x à leitura coerente não exponencial; código anterior preservado e tipagem corrigida antes da entrega. Avisos do pyRing e a recusa inicial de acesso WSL estão no STATUS. STATUS, PROGRESSO e manifesto local recebem backup imediato dos bytes anteriores. Nenhuma memória canônica de outra casa foi tocada.

## Custódia

| Artefato | SHA-256 lido |
|---|---|
'''
    text += "\n".join(f"| `{name}` | `{value}` |" for name,value in hashes.items())+"\n"
    raw = text.encode()
    safe_write(handoff, raw)
    progress = ROOT/"PROGRESSO.md"
    prior = progress.read_bytes()
    safe_write(progress, prior+b"\n\n"+raw)
    if not progress.read_bytes().startswith(prior):
        raise ValueError("Progress is not append-only")
    print(json.dumps(dict(status="PROGRESS_NOT_COMPLETE", handoff=str(handoff),
                          package=package["archive"], scientific_acceptance="NOT_PASSED",
                          next_action=remaining[0]), ensure_ascii=False))


if __name__ == "__main__":
    main()
