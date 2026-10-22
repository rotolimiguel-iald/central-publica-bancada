"""Render concise readiness notes/tables and pin all sidecar files; no science."""
import json
from datetime import datetime, timezone
from pathlib import Path
from build_readiness import HERE, B, ROOT, sha, write


def main():
    candidates = json.loads((HERE / "CANDIDATES_SORTED.json").read_bytes())
    readiness = json.loads((HERE / "METADATA_READINESS.json").read_bytes())
    info = json.loads((HERE / "EXPECTED_INFORMATION.json").read_bytes())
    tests = json.loads((HERE / "FINITE_INTERFACE_CHECKS.json").read_bytes())
    results = {(r["event"], r["fit_population"]): r for r in info["rows"]}
    lines = ["# E3.2 — prontidão documental dos candidatos cegos", "",
      "[REAL documental/aritmético] Preparação somente. E2, Kerr, guard e serializador anterior intactos. Nenhum download de strain, leitura de posterior de candidato, PE, onda, draw, registro ou admissão. Fontes primárias remotas consultadas somente como metadados; manifesto final lista cada arquivo/hash.", "",
      "**Censo efetivo: 14 elegíveis registrados com published_deformation_at_registration=false; 10 sem hold, quatro com hold.** False significa ausência no corpus delimitado, não inexistência universal de publicação. GR_input_eligibility e medianas GR são entradas herdadas do E2; não foram novamente medidas nem usadas para admitir eventos. E2 contém campos históricos E2_registered/blindness_certified=false nas entradas: não sobrescritos; o estado global do registro não certifica cegueira individual.", "",
      "A atualização documental de R em `bis/e3_publication_refresh/PUBLICATION_METADATA_REVIEW_INDEX.json` foi lida; os 14 recibos e seus hashes foram conferidos. Reviews pós-E2 permanecem reviews de publicação, sem resolução de hold nem decisão de admissão. A ordem abaixo conserva SNR E0; não usa posterior estreito ou informação/hora.", "",
      "## Informação esperada — modelo de planejamento, não potência do teste", "",
      "Fonte: `bis/E0_SNR_INFORMATION_FIT.json`, revisada em `bis/E0_SNR_FIT_REVIEW.md`. JSON deste sidecar preserva ambos os fits 31/33, coeficientes, covariância completa, dispersão e percentis bootstrap já existentes. Para mu=a+b ln(rho), sigma_med=exp(mu), proxy=exp(-2mu) e E[I|rho,s]=exp(-2mu+2s²). São objetos diferentes. A tabela usa o fit primário 31; o 33 está em `EXPECTED_INFORMATION.json`, sem tratá-lo como réplica independente.", "",
      "A coluna IC95 de E[I] propaga somente a covariância dos coeficientes com quantil t herdado, s fixado. A dispersão residual 5/50/95 de sigma, IC da mediana e integração gaussiana dos coeficientes aparecem separadas no JSON. Não é intervalo preditivo físico completo. Incertezas de SNR, seleção, transferência para pSEOB alinhado com priors largos e incerteza de s continuam OPEN. `information_for_actual_new_PE=null` para todos. Não interpolamos bootstrap: não há draws de coeficientes armazenados para os SNR exatos. A grade bootstrap original foi preservada, sem novo sorteio.", "",
      "| Evento | SNR E0 | Hold | sigma_med | 1/sigma_med² (proxy) | E[1/sigma²] lognormal | IC95 coeficientes, s fixo | Fora domínio 31 |",
      "|---|---:|---|---:|---:|---:|---|---|"]
    for row in candidates["candidates"]:
        p = results[(row["event"], "GWTC5_31")]
        lo, hi = p["expected_I_coefficient_only_95_t_interval_s_fixed"]
        lines.append(f"| {row['event']} | {row['SNR_network']:.1f} | {'SIM — preservado' if row['data_quality_hold'] else 'não registrado'} | {p['sigma_conditional_median']:.5f} | {p['inverse_squared_conditional_median_proxy']:.4f} | {p['expected_inverse_variance_lognormal_s_fixed']:.4f} | [{lo:.4f}, {hi:.4f}] | {'SIM' if p['outside_fit_SNR_domain'] else 'não'} |")
    lines += ["", f"Controle determinístico: {info['fit_grid_scalar_checks']} comparações com a grade já auditada, erro relativo máximo {info['max_relative_error']:.3g}. Não houve refit. Cada SNR traz caminho SHA256, linha CSV, campo, versão e URL primária em `CANDIDATES_SORTED.json` e `EXPECTED_INFORMATION.json`. A comparação corrente dos cinco alvos confirmou os mesmos SNR; os nove demais usam explicitamente o snapshot E0.", "",
      "## Cinco primeiros sem hold — dados anunciados, ainda não baixados", "",
      "[REAL metadados] GETs primários GWOSC de evento, listagem de arquivos, timelines, bitmasks e catálogo MD5 arquivados em `metadata/`, com URL/data/sha e recibo HTTP. Nenhum GET/HEAD de hdf5/gwf. As listagens retornaram também estatísticas públicas de arquivos; não foram usadas para escolher PSD/janela ou ordenar candidatos. Não foram consultados valores amostrais.", "",
      "| Evento | GPS primário | Arquivo on-source inicia GPS; duração | H1/L1 no instante: flags | Primeiro bloco 256 s no mesmo arquivo, H1 / L1 |",
      "|---|---:|---|---|---|"]
    for row in readiness["targets"]:
        streams = [next(f for f in d["files"] if f["role"] == "EVENT_FILE_ONSOURCE_AND_POSSIBLE_PSD") for d in row["detectors"]]
        scouts = [s["first_256s_all_flags_segment_before_GPSminus16_INPUT"] for s in streams]
        lines.append(f"| {row['event']} | {row['event_GPS']} | {streams[0]['GPSstart']}; {streams[0]['duration']} s | passa / passa | {scouts[0]} / {scouts[1]} |")
    lines += ["", "Os blocos acima são **sondagem de intervalos**, sob INPUT de PSD 256 s e exclusão 16 s herdados do piloto. Não são janelas finais escolhidas. A busca local real deve também terminar antes do início de análise, exigir finitude do strain e conferir as flags do HDF5; um bloco anunciado não garante PSD válida/estacionária. A janela de PE, padding, fmin e suporte de prior ainda não foram definidos. Os intervalos completos que contêm cada evento e opções de arquivo anterior estão no JSON. Todos os links exatos H1/L1, duração 4096 s, taxa 4096 Hz, MD5 e linha no catálogo do provedor estão em `METADATA_READINESS.json`.", "",
      "Flags consultadas: DATA, CBC_CAT1/2/3, NO_CBC_HW_INJ, NO_BURST_HW_INJ, NO_DETCHAR_HW_INJ, NO_STOCH_HW_INJ. A primeira lista e a segunda são separadas no leitor. Esta é a escolha do piloto, não uma nova aprovação para cada evento. As [definições O4](https://gwosc.org/O4/o4_details/) e bitmasks oficiais foram arquivadas; as flags são publicadas em resolução de 1 s. Passar no instante não implica passar em toda a janela nem remove os quatro holds independentes.", "",
      "[DECLARADO pelo provedor] Os MD5 dos 18 arquivos listados foram localizados nos catálogos oficiais, mas não verificados contra bytes. `local_sha256=null`, `expected_bytes=null`: as APIs consultadas não forneceram tamanhos exatos; não houve HEAD de strain. Licença CC BY 4.0 e agradecimentos vêm da [página primária da release](https://gwosc.org/O4/o4_details/) e das [instruções GWOSC](https://gwosc.org/acknowledgement/). `PER_FILE_LICENSE_METADATA.json` vincula URL por URL a essa fonte pinada; a referência comum continua sendo um recibo com mapeamento por arquivo, não autorização de download ou parecer jurídico.", "",
      "## Contrato exato de extensão — sem modificar E2/guard", "",
      "Fontes: `bis/e2_code/registration_guard.py:188` (`load_jobs`), `:210` (`load_authorized_configuration`), `:169` (reviews), `fetch_registered.py:14` (`validate_url`), `:43` (`_fetch`); localizadores AST/hash no manifesto/checks. O registro original é sempre validado antes da vista ampliada.", "",
      "- Orçamento ativo futuro no caminho já fixado `ORDEM_013_RINGDOWN/ORCAMENTO_40H.json`: `parent_registration_sha256`, `registered_utc`, `witness_relative_to_Chatgpt`, `jobs_relative_to_Chatgpt`, `jobs_sha256`. Jobs: `schema_version=E2_PE_JOBS_V2`, mesmo parent, `jobs` e opcional `downloads`. Testemunha no túnel com `allocation_sha256` e `registered_utc`, cronologia conferida. Nenhum desses arquivos ativos foi produzido.",
      "- Receita fetch: `event`, `mode=blind_test`, `kind=public_strain`, `url`, `filename` (basename seguro, destino B/cache), `maximum_bytes` inteiro positivo ≤3e9, `license_source`, `license_status`, `license_receipt_relative_to_Chatgpt`, `license_receipt_sha256`; opcionais `provider_checksum`, `provider_checksum_algorithm=md5/sha256`, `expected_bytes`. URL HTTPS sem query, credenciais ou fragment; hosts gwosc.org/www.gwosc.org/zenodo.org, inclusive redirects. Limite de bytes precisa ser escolhido explicitamente, não inferido de duração. Bytes só promovidos após conferência de comprimento/checksum e autorização estável.",
      "- Dependência SHA: download novo não tem SHA256 local antecipadamente. O caminho suportado é uma configuração testemunhada **downloads-only, jobs={}**, mantendo o piloto estático; após recibos de bytes, uma configuração sucessora versionada com jobs completos e novas testemunhas. Não inventar SHA a partir de MD5. A versão ativa única fica no caminho de política: preservar arquivos/pins/testemunhas anteriores e substituir a referência somente pelo principal, sem downloads em trânsito. A lista dinâmica não se acumula automaticamente entre versões: carregar as entradas anteriores que devam continuar autorizadas. Não substituir nomes estáticos. Não existe esquema novo jobsV3: o nome de arquivo pode ser versionado, o schema aceito continua E2_PE_JOBS_V2.",
      "- O serializador de `e3_allocation_prepare` conserva `downloads={}`, exige jobs não vazios e recusa orçamento já existente. Ele não serve para essas duas etapas sem um sucessor próprio revisado. Não foi alterado nem executado. Os fragmentos aqui são deliberadamente incompletos, sem schema de jobs e com campos null; não são carregáveis como autorização.",
      "- `authorize_event` não resolve DQ por si só; `load_jobs` valida reviews dos jobs. Na etapa downloads-only não há novo job cujo review possa ser checado: o guard exige elegibilidade/censo para fetch, mas não aplica ali um novo gate de resolução de hold. O principal deve preservar a restrição aos eventos sem hold e as reviews antes de qualquer preparação de receita. Isso é uma diferença de alcance documentada, não um novo controle core nem autorização para contorná-lo.", "",
      "`publication_metadata_review` é copiado fielmente do índice R. Um hold requer `data_quality_resolution` com `review_passed`, `method`, caminho/hash e `reviewed_utc` pós-E2; não existe resolução fabricada aqui. Recibos de custódia/transferência DACL pinados constam como proveniência em `NONEXECUTABLE_TEMPLATES.json`, sem inspeção do segredo ou novos requisitos core. O recibo host lido não substitui verificação de runtime futura; sua ressalva de integração WSL foi preservada.", "",
      "## Configuração ainda OPEN por evento", "",
      "1. Priors de **massas componentes no frame detector**, spins componentes e demais parâmetros físicos livres. E0 fornece medianas marginais source-frame e chi_eff; não fornecem chi1/chi2 nem amostras pareadas. Não usar massas remanescentes como componentes; não converter produto de medianas em posterior ou prior validado. Nenhum prior novo foi decidido.",
      "2. fmin/fmax/referência, duração/início inteiro compatível com amostragem, prior temporal e padding. `temporal_contract.py:5` usa limites LAL de inspiral+merger+tail, dtau máximos e ±0,022 s de atraso. Conferir futuramente extremos dos priors e suporte, não apenas medianas GR; aqui não houve chamadas LAL, PE ou ondas. Não transplantar 16 s/20 Hz para todos como certificado.",
      "3. Rede detectores: links H1/L1 disponíveis; alguns eventos também anunciam Virgo. O SNR E0 é rede/preferred e pode não coincidir com análise H1/L1. Isso limita a transferência do fit, não modifica a ordenação solicitada.",
      "4. Flags/janelas/PSD, hashes locais, remnant_conversion_INPUT pinado, priors completos (16 campos), `variant`/deformações, sampler e critérios de convergência. Templates mantêm esses requisitos abertos; nenhuma troca de prior depois do resultado. Recuperação com dtau livre não paga mapa TGL nem calibração de duas famílias.",
      "5. Custo real do piloto e alocação posterior: máximo solicitado 8 h/job e 24 workers, deadline global original e reserva de limpeza. Sem custo/hora, ganho operacional ou novas horas estimadas. Offsets permanecem internos; não há acesso a seed, médias cegas ou descegamento.", "",
      f"## Verificação e limites\n\n{tests['count']} checks finitos passaram, incluindo URLs, JSON duplicado, validação estrutural do config piloto, falhas de prior/caps e extensão downloads-only em memória. Funções puras selecionadas por AST; nenhum módulo produtor importado ou gate real chamado. A testemunha nos fixtures é mock: não certifica ativação temporal/custódia. As {info['fit_grid_scalar_checks']} contas determinísticas do fit são adicionais. Revisão independente desta preparação permanece OPEN.", "",
      "Uma primeira consulta de rede foi recusada pelo sandbox; recibo da falha preservado. A consulta posterior de metadados foi autorizada fora do sandbox. Houve ainda erro de quoting em uma inspeção local auxiliar, sem escrita/ciência; substituído por operação de cópia simples. A linha de resumo do builder `unheld:5` conta **alvos inspecionados**, não o censo sem hold: o artefato CANDIDATES_SORTED registra corretamente 10. Nenhuma dessas ocorrências muda elegibilidade.", "",
      "Axiomas N/A; teoremas 0. Resultado: prontidão de **metadados/contrato**, não prontidão executiva aprovada. Holds, transferência do fit, custo, suporte temporal e configuração científica continuam como gates abertos. O principal decide a alocação após custo real do piloto.", ""]
    path = HERE / "READINESS.md"
    raw = "\n".join(lines).encode("utf-8")
    with path.open("xb") as handle:
        handle.write(raw)
    if path.stat().st_size != len(raw):
        raise OSError("Incomplete report")
    files = sorted(p for p in HERE.rglob("*") if p.is_file())
    sourcepins = json.loads((HERE / "SOURCE_PINS.json").read_bytes())["sources_sha256_relative_to_Chatgpt"]
    for relative, digest in sourcepins.items():
        if sha(ROOT / relative) != digest:
            raise ValueError("Source changed before finalization: " + relative)
    manifest = {"status": "PREPARATION_COMPLETE_NO_ALLOCATION_OR_ADMISSION", "created_utc": datetime.now(timezone.utc).isoformat(),
                "registration_sha256": candidates["E2"]["sha256"],
                "files": [{"relative_to_Chatgpt": p.relative_to(ROOT).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size} for p in files],
                "all_written_files": [p.relative_to(ROOT).as_posix() for p in files] + [(HERE / "MANIFEST.json").relative_to(ROOT).as_posix()],
                "sources_unchanged_at_finalize": True, "finite_checks": tests["count"], "fit_grid_checks": info["fit_grid_scalar_checks"],
                "posterior_candidate_reads": False, "strain_downloads": False, "PE": False, "admission_decision": False,
                "new_fit_bootstrap_or_draws": False, "cost_hour_ranking": None,
                "independent_review": "OPEN", "manifest_self_hash": "Compute externally"}
    write("MANIFEST.json", manifest)
    print(json.dumps({"manifest_sha256": sha(HERE / "MANIFEST.json"), "written_file_count": len(manifest["all_written_files"]),
                      "readiness_sha256": sha(path), "information_sha256": sha(HERE / "EXPECTED_INFORMATION.json")}))


if __name__ == "__main__":
    main()
