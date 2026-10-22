# E3.2 — prontidão documental dos candidatos cegos

[REAL documental/aritmético] Preparação somente. E2, Kerr, guard e serializador anterior intactos. Nenhum download de strain, leitura de posterior de candidato, PE, onda, draw, registro ou admissão. Fontes primárias remotas consultadas somente como metadados; manifesto final lista cada arquivo/hash.

**Censo efetivo: 14 elegíveis registrados com published_deformation_at_registration=false; 10 sem hold, quatro com hold.** False significa ausência no corpus delimitado, não inexistência universal de publicação. GR_input_eligibility e medianas GR são entradas herdadas do E2; não foram novamente medidas nem usadas para admitir eventos. E2 contém campos históricos E2_registered/blindness_certified=false nas entradas: não sobrescritos; o estado global do registro não certifica cegueira individual.

A atualização documental de R em `bis/e3_publication_refresh/PUBLICATION_METADATA_REVIEW_INDEX.json` foi lida; os 14 recibos e seus hashes foram conferidos. Reviews pós-E2 permanecem reviews de publicação, sem resolução de hold nem decisão de admissão. A ordem abaixo conserva SNR E0; não usa posterior estreito ou informação/hora.

## Informação esperada — modelo de planejamento, não potência do teste

Fonte: `bis/E0_SNR_INFORMATION_FIT.json`, revisada em `bis/E0_SNR_FIT_REVIEW.md`. JSON deste sidecar preserva ambos os fits 31/33, coeficientes, covariância completa, dispersão e percentis bootstrap já existentes. Para mu=a+b ln(rho), sigma_med=exp(mu), proxy=exp(-2mu) e E[I|rho,s]=exp(-2mu+2s²). São objetos diferentes. A tabela usa o fit primário 31; o 33 está em `EXPECTED_INFORMATION.json`, sem tratá-lo como réplica independente.

A coluna IC95 de E[I] propaga somente a covariância dos coeficientes com quantil t herdado, s fixado. A dispersão residual 5/50/95 de sigma, IC da mediana e integração gaussiana dos coeficientes aparecem separadas no JSON. Não é intervalo preditivo físico completo. Incertezas de SNR, seleção, transferência para pSEOB alinhado com priors largos e incerteza de s continuam OPEN. `information_for_actual_new_PE=null` para todos. Não interpolamos bootstrap: não há draws de coeficientes armazenados para os SNR exatos. A grade bootstrap original foi preservada, sem novo sorteio.

| Evento | SNR E0 | Hold | sigma_med | 1/sigma_med² (proxy) | E[1/sigma²] lognormal | IC95 coeficientes, s fixo | Fora domínio 31 |
|---|---:|---|---:|---:|---:|---|---|
| GW230919_215712 | 16.8 | não registrado | 0.28662 | 12.1726 | 13.4707 | [11.1567, 16.2647] | não |
| GW241111_111552 | 16.3 | não registrado | 0.29492 | 11.4969 | 12.7230 | [10.4649, 15.4684] | não |
| GW240930_035959 | 16.1 | SIM — preservado | 0.29838 | 11.2318 | 12.4296 | [10.1927, 15.1574] | não |
| GW240513_183302 | 14.5 | não registrado | 0.32941 | 9.2158 | 10.1986 | [8.1201, 12.8092] | não |
| GW240920_073424 | 14.0 | não registrado | 0.34051 | 8.6244 | 9.5442 | [7.5146, 12.1219] | não |
| GW250118_170523 | 13.9 | não registrado | 0.34283 | 8.5084 | 9.4157 | [7.3961, 11.9868] | não |
| GW241130_034908 | 13.8 | não registrado | 0.34518 | 8.3930 | 9.2881 | [7.2785, 11.8526] | não |
| GW240923_204006 | 13.6 | não registrado | 0.34997 | 8.1646 | 9.0353 | [7.0460, 11.5864] | não |
| GW241210_060606 | 13.4 | não registrado | 0.35490 | 7.9392 | 8.7859 | [6.8171, 11.3233] | não |
| GW240615_160735 | 13.1 | SIM — preservado | 0.36258 | 7.6066 | 8.4178 | [6.4805, 10.9342] | não |
| GW250109_010541 | 13.1 | não registrado | 0.36258 | 7.6066 | 8.4178 | [6.4805, 10.9342] | não |
| GW240515_005301 | 12.8 | SIM — preservado | 0.37061 | 7.2807 | 8.0572 | [6.1524, 10.5517] | SIM |
| GW241102_144729 | 12.7 | SIM — preservado | 0.37336 | 7.1736 | 7.9386 | [6.0449, 10.4256] | SIM |
| GW250104_015122 | 12.1 | não registrado | 0.39084 | 6.5465 | 7.2447 | [5.4200, 9.6837] | SIM |

Controle determinístico: 72 comparações com a grade já auditada, erro relativo máximo 9.62e-16. Não houve refit. Cada SNR traz caminho SHA256, linha CSV, campo, versão e URL primária em `CANDIDATES_SORTED.json` e `EXPECTED_INFORMATION.json`. A comparação corrente dos cinco alvos confirmou os mesmos SNR; os nove demais usam explicitamente o snapshot E0.

## Cinco primeiros sem hold — dados anunciados, ainda não baixados

[REAL metadados] GETs primários GWOSC de evento, listagem de arquivos, timelines, bitmasks e catálogo MD5 arquivados em `metadata/`, com URL/data/sha e recibo HTTP. Nenhum GET/HEAD de hdf5/gwf. As listagens retornaram também estatísticas públicas de arquivos; não foram usadas para escolher PSD/janela ou ordenar candidatos. Não foram consultados valores amostrais.

| Evento | GPS primário | Arquivo on-source inicia GPS; duração | H1/L1 no instante: flags | Primeiro bloco 256 s no mesmo arquivo, H1 / L1 |
|---|---:|---|---|---|
| GW230919_215712 | 1379195850.0 | 1379192832; 4096 s | passa / passa | [1379194069, 1379194325] / [1379192832, 1379193088] |
| GW241111_111552 | 1415358970.6 | 1415356416; 4096 s | passa / passa | [1415358394, 1415358650] / [1415356416, 1415356672] |
| GW240513_183302 | 1399660400.9 | 1399656448; 4096 s | passa / passa | [1399656448, 1399656704] / [1399656448, 1399656704] |
| GW240920_073424 | 1410852882.5 | 1410850816; 4096 s | passa / passa | [1410850816, 1410851072] / [1410850816, 1410851072] |
| GW250118_170523 | 1421255141.2 | 1421254656; 4096 s | passa / passa | [1421254656, 1421254912] / [1421254656, 1421254912] |

Os blocos acima são **sondagem de intervalos**, sob INPUT de PSD 256 s e exclusão 16 s herdados do piloto. Não são janelas finais escolhidas. A busca local real deve também terminar antes do início de análise, exigir finitude do strain e conferir as flags do HDF5; um bloco anunciado não garante PSD válida/estacionária. A janela de PE, padding, fmin e suporte de prior ainda não foram definidos. Os intervalos completos que contêm cada evento e opções de arquivo anterior estão no JSON. Todos os links exatos H1/L1, duração 4096 s, taxa 4096 Hz, MD5 e linha no catálogo do provedor estão em `METADATA_READINESS.json`.

Flags consultadas: DATA, CBC_CAT1/2/3, NO_CBC_HW_INJ, NO_BURST_HW_INJ, NO_DETCHAR_HW_INJ, NO_STOCH_HW_INJ. A primeira lista e a segunda são separadas no leitor. Esta é a escolha do piloto, não uma nova aprovação para cada evento. As [definições O4](https://gwosc.org/O4/o4_details/) e bitmasks oficiais foram arquivadas; as flags são publicadas em resolução de 1 s. Passar no instante não implica passar em toda a janela nem remove os quatro holds independentes.

[DECLARADO pelo provedor] Os MD5 dos 18 arquivos listados foram localizados nos catálogos oficiais, mas não verificados contra bytes. `local_sha256=null`, `expected_bytes=null`: as APIs consultadas não forneceram tamanhos exatos; não houve HEAD de strain. Licença CC BY 4.0 e agradecimentos vêm da [página primária da release](https://gwosc.org/O4/o4_details/) e das [instruções GWOSC](https://gwosc.org/acknowledgement/). `PER_FILE_LICENSE_METADATA.json` vincula URL por URL a essa fonte pinada; a referência comum continua sendo um recibo com mapeamento por arquivo, não autorização de download ou parecer jurídico.

## Contrato exato de extensão — sem modificar E2/guard

Fontes: `bis/e2_code/registration_guard.py:188` (`load_jobs`), `:210` (`load_authorized_configuration`), `:169` (reviews), `fetch_registered.py:14` (`validate_url`), `:43` (`_fetch`); localizadores AST/hash no manifesto/checks. O registro original é sempre validado antes da vista ampliada.

- Orçamento ativo futuro no caminho já fixado `ORDEM_013_RINGDOWN/ORCAMENTO_40H.json`: `parent_registration_sha256`, `registered_utc`, `witness_relative_to_Chatgpt`, `jobs_relative_to_Chatgpt`, `jobs_sha256`. Jobs: `schema_version=E2_PE_JOBS_V2`, mesmo parent, `jobs` e opcional `downloads`. Testemunha no túnel com `allocation_sha256` e `registered_utc`, cronologia conferida. Nenhum desses arquivos ativos foi produzido.
- Receita fetch: `event`, `mode=blind_test`, `kind=public_strain`, `url`, `filename` (basename seguro, destino B/cache), `maximum_bytes` inteiro positivo ≤3e9, `license_source`, `license_status`, `license_receipt_relative_to_Chatgpt`, `license_receipt_sha256`; opcionais `provider_checksum`, `provider_checksum_algorithm=md5/sha256`, `expected_bytes`. URL HTTPS sem query, credenciais ou fragment; hosts gwosc.org/www.gwosc.org/zenodo.org, inclusive redirects. Limite de bytes precisa ser escolhido explicitamente, não inferido de duração. Bytes só promovidos após conferência de comprimento/checksum e autorização estável.
- Dependência SHA: download novo não tem SHA256 local antecipadamente. O caminho suportado é uma configuração testemunhada **downloads-only, jobs={}**, mantendo o piloto estático; após recibos de bytes, uma configuração sucessora versionada com jobs completos e novas testemunhas. Não inventar SHA a partir de MD5. A versão ativa única fica no caminho de política: preservar arquivos/pins/testemunhas anteriores e substituir a referência somente pelo principal, sem downloads em trânsito. A lista dinâmica não se acumula automaticamente entre versões: carregar as entradas anteriores que devam continuar autorizadas. Não substituir nomes estáticos. Não existe esquema novo jobsV3: o nome de arquivo pode ser versionado, o schema aceito continua E2_PE_JOBS_V2.
- O serializador de `e3_allocation_prepare` conserva `downloads={}`, exige jobs não vazios e recusa orçamento já existente. Ele não serve para essas duas etapas sem um sucessor próprio revisado. Não foi alterado nem executado. Os fragmentos aqui são deliberadamente incompletos, sem schema de jobs e com campos null; não são carregáveis como autorização.
- `authorize_event` não resolve DQ por si só; `load_jobs` valida reviews dos jobs. Na etapa downloads-only não há novo job cujo review possa ser checado: o guard exige elegibilidade/censo para fetch, mas não aplica ali um novo gate de resolução de hold. O principal deve preservar a restrição aos eventos sem hold e as reviews antes de qualquer preparação de receita. Isso é uma diferença de alcance documentada, não um novo controle core nem autorização para contorná-lo.

`publication_metadata_review` é copiado fielmente do índice R. Um hold requer `data_quality_resolution` com `review_passed`, `method`, caminho/hash e `reviewed_utc` pós-E2; não existe resolução fabricada aqui. Recibos de custódia/transferência DACL pinados constam como proveniência em `NONEXECUTABLE_TEMPLATES.json`, sem inspeção do segredo ou novos requisitos core. O recibo host lido não substitui verificação de runtime futura; sua ressalva de integração WSL foi preservada.

## Configuração ainda OPEN por evento

1. Priors de **massas componentes no frame detector**, spins componentes e demais parâmetros físicos livres. E0 fornece medianas marginais source-frame e chi_eff; não fornecem chi1/chi2 nem amostras pareadas. Não usar massas remanescentes como componentes; não converter produto de medianas em posterior ou prior validado. Nenhum prior novo foi decidido.
2. fmin/fmax/referência, duração/início inteiro compatível com amostragem, prior temporal e padding. `temporal_contract.py:5` usa limites LAL de inspiral+merger+tail, dtau máximos e ±0,022 s de atraso. Conferir futuramente extremos dos priors e suporte, não apenas medianas GR; aqui não houve chamadas LAL, PE ou ondas. Não transplantar 16 s/20 Hz para todos como certificado.
3. Rede detectores: links H1/L1 disponíveis; alguns eventos também anunciam Virgo. O SNR E0 é rede/preferred e pode não coincidir com análise H1/L1. Isso limita a transferência do fit, não modifica a ordenação solicitada.
4. Flags/janelas/PSD, hashes locais, remnant_conversion_INPUT pinado, priors completos (16 campos), `variant`/deformações, sampler e critérios de convergência. Templates mantêm esses requisitos abertos; nenhuma troca de prior depois do resultado. Recuperação com dtau livre não paga mapa TGL nem calibração de duas famílias.
5. Custo real do piloto e alocação posterior: máximo solicitado 8 h/job e 24 workers, deadline global original e reserva de limpeza. Sem custo/hora, ganho operacional ou novas horas estimadas. Offsets permanecem internos; não há acesso a seed, médias cegas ou descegamento.

## Verificação e limites

125 checks finitos passaram, incluindo URLs, JSON duplicado, validação estrutural do config piloto, falhas de prior/caps e extensão downloads-only em memória. Funções puras selecionadas por AST; nenhum módulo produtor importado ou gate real chamado. A testemunha nos fixtures é mock: não certifica ativação temporal/custódia. As 72 contas determinísticas do fit são adicionais. Revisão independente desta preparação permanece OPEN.

Uma primeira consulta de rede foi recusada pelo sandbox; recibo da falha preservado. A consulta posterior de metadados foi autorizada fora do sandbox. Houve ainda erro de quoting em uma inspeção local auxiliar, sem escrita/ciência; substituído por operação de cópia simples. A linha de resumo do builder `unheld:5` conta **alvos inspecionados**, não o censo sem hold: o artefato CANDIDATES_SORTED registra corretamente 10. Nenhuma dessas ocorrências muda elegibilidade.

Axiomas N/A; teoremas 0. Resultado: prontidão de **metadados/contrato**, não prontidão executiva aprovada. Holds, transferência do fit, custo, suporte temporal e configuração científica continuam como gates abertos. O principal decide a alocação após custo real do piloto.
