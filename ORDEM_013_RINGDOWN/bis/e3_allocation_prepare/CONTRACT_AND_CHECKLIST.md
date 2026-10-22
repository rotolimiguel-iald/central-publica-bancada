# Preparação E3.2/E3.3 — sem alocação

[INPUT] Sidecar solicitado pelo principal. [REAL documental] Leitura estática das fontes enumeradas em `PREPARATION_RECEIPT.json`; nenhum módulo científico importado. E2/Kerr permanecem intocados. Nenhuma escolha de evento, bin, número de injeções, seed ou horas foi feita aqui. Axiomas: N/A; teoremas: 0.

## Contrato consumido pelo código congelado

Caminhos abaixo são relativos a `Chatgpt`; `B = ORDEM_013_RINGDOWN`. Fontes de código são relativas a `B`. A ordem é `TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:194` (E3.2) e `:195` (E3.3). Os hashes são calculados no recibo, não transcritos de mensagens.

| Objeto | Campos e condições efetivas |
|---|---|
| E2 original | `allocation_policy.relative_to_Chatgpt` fixa o local do orçamento; `allocation_policy.max_job_wall_seconds` fixa o teto dinâmico. `pe_jobs` originais sobrevivem. `checked_registration` deve validar o mapa original, sua ativação, fontes e runtime antes de derivar a configuração ampliada. |
| Orçamento futuro | `parent_registration_sha256`, `registered_utc`, `witness_relative_to_Chatgpt`, `jobs_relative_to_Chatgpt`, `jobs_sha256`. O hash pai é SHA256 dos bytes do E2 efetivo, não de draft/candidato. `registered_utc >= E2.registered_utc`. |
| Jobs futuros | `schema_version = E2_PE_JOBS_V2`, `parent_registration_sha256`, `jobs` (mapa nome→config completo); `downloads` opcional. Nenhum nome pode substituir job estático. Este sidecar restringe `downloads` a `{}`. |
| Testemunha futura | Arquivo em `TUNEL/DO_CHATGPT`, exatamente uma linha `allocation_sha256: <sha do orçamento>` e uma `registered_utc: <UTC ISO>`. Data do orçamento ≤ data da testemunha ≤ agora; mtime entre data da testemunha−2 s e agora+2 s. Hashar jobs → montar orçamento → hash do orçamento → emitir testemunha; não há hash circular. |
| Reviews cegos | `publication_metadata_review`: `review_passed: true`, `scope` não vazio, `relative_to_Chatgpt`, `sha256`, `reviewed_utc`. Fonte fixada por hash; E2.registered_utc ≤ reviewed_utc ≤ agora. `data_quality_hold` no candidato tem de ser booleano. Se true, exigir `data_quality_resolution` com os mesmos campos, substituindo `scope` por `method` explícito. |

Âncoras: `bis/e2_code/registration_guard.py:31`, `:112`, `:120`, `:157`, `:169`, `:188`, `:210`. `load_authorized_configuration` agrega downloads somente após o contrato da alocação; downloads dinâmicos exigiriam recibo de licença por arquivo. Não são preparados neste sidecar.

**Limite do guard:** ele valida o teto individual, as identidades e as reviews; não impõe soma de horas de todos os jobs, prioridade por informação/hora nem limite agregado de workers entre controladores simultâneos. Esses são deveres da alocação e do lançamento pelo principal. O gerador opcional adota contabilização serial conservadora, sem lançador.

## Config completo por job

Fonte: `bis/e2_code/pe_runner.py:51` e `:173`; `run_controlled.py:36`; `strain_io.py:29` e `:45`; `remnant_conversion.py:11`. `CONTRACT_SCHEMA.json` enumera os campos. Ele é inventário de contrato, não um JSON Schema que certifique sozinho um job.

- Identidade: `event`, `mode` (`calibration`/`blind_test`), `privacy_mode: procedural_same_host`, `label`, `output_directory_name` exclusivo, `variant`, `fixed_deformation_parameters`.
- Janela: `event_GPS`, `segment_start_GPS`, `duration_s`, `sample_rate_hz`, `minimum_frequency_hz`, `maximum_frequency_hz`, `reference_frequency_hz`, `onsource_roll_off_s`, `psd_duration_s`, `psd_segment_s`, `offsource_exclusion_s`, `quality_required`, `injection_flags_required`, `detectors`, `data` por detector (`onsource_path`, `onsource_sha256`, `offsource_path`, `offsource_sha256`). Não ler os bytes de strain para preparar a alocação.
- `priors` contém exatamente 16 nomes: `mass_1`, `mass_2`, `mass_ratio`, `chi_1`, `chi_2`, `luminosity_distance`, `theta_jn`, `phase`, `ra`, `dec`, `psi`, `geocent_time`, `dtau220`, `dtau440`, `domega220`, `domega440`. Cada prior livre tem `kind`, `minimum`, `maximum` e pode ter `boundary`. `theta_jn=Sine`, `dec=Cosine`, `mass_ratio=Constraint`; demais `Uniform`. Massas/distância positivas, spins estritamente entre −1 e 1, q≤1, deformações >−1; limites finitos e ordenados. Massas e spins continuam livres na recuperação.
- Para este sidecar: `variant: 220_plus_440_free` ou `pilot_all_four_free`; `fixed_deformation_parameters: {}`. O runner também admite variante registrada com deformações fixas, mas `validate_truth_support` espera dicionários para todos os priors. Não propor essa combinação com injeção nem alterar código congelado para habilitá-la.
- `sampler`: `nlive`, `walks`, `maxcall`, `workers`, `seed`, `dlogz`, `minimum_posterior_samples`, `minimum_effective_samples`; `check_point: false`, `check_point_plot: false`. Inteiros positivos onde exigidos, seed≥0, maxcall>nlive, amostras≥2, ESS/dlogz positivos. Valores científicos concretos dependem do E2/piloto e não são escolhidos aqui.
- `wall_budget_seconds`: positivo, no máximo `min(28800, E2.allocation_policy.max_job_wall_seconds)`. `workers≤24` neste sidecar. O runner genérico permite até 28; o controlador permite até 10 h em calibração. Isso não relaxa a ordem atual de 8 h/24. Teto de maxcall não é garantia de exatamente aquele número: dynesty pode ultrapassar por iteração/lote.
- `remnant_conversion_INPUT`: `remnant_fit: LAL_SEOBNRv4_aligned_NR_fit`, `cosmology_name: Planck18_external_INPUT`, `cosmology_source_path`, `cosmology_source_sha256`, `cosmology_parameters` (`H0_km_s_Mpc`, `Om0`, `Tcmb0_K`, `Neff`, `m_nu_eV`, `Ob0`). Herdar a entrada pinada e revisada. Mf detector/spin são derivados por fit GR nomeado, z por cosmologia externa; não são massas componentes nem medidas independentes.

Checagens anteriores ao lançamento: banda dentro de Nyquist, janela não consumida pelo Tukey, prior temporal dentro da parte não apodizada, suporte temporal conservador LAL e atrasos de detector, duração suficiente em todo suporte relevante. Preservar controles existentes e exigir revisão de novas janelas; não inferir que 16 s serve para qualquer configuração. Sem reamostragem implícita. Escolha de bloco PSD é o primeiro bloco válido por flags/finitude, anterior à janela analisada e à exclusão do evento; não por nível favorável da PSD.

## Custo real e relógio

[OPEN até recibos] Receber E2 efetivo/pin, orçamento global pinado pelo E2 e custo REAL do piloto. Não usar os custos históricos estimados da ordem como medição desta execução. Derivar `hard_deadline_utc` do artefato de orçamento; não reiniciar 40 h na alocação.

`CONTROLLER.json` fornece `wall_seconds`, início/fim, `children_user_cpu_seconds`, `children_system_cpu_seconds`, `returncode`, estado e cleanup. `PRIVATE_CONVERGENCE.json` fornece `accepted_for_analysis`, `cost.sampler_ncall`, `cost.likelihood_calls`, `cost.source_calls`, tempos e snapshots. Ler apenas esses metadados, não logs privados, seeds ou `ANALYST_OUTPUT` com amostras. O recibo de convergência antecede a conversão de remanescente: não é custo completo do job. Parede total do controlador inclui essa etapa/limpeza. Soma de tempos por chamada entre workers não é parede total nem CPU medida. `CHILD_COMPLETED_REQUIRES_REVIEW` sozinho não aceita posterior; piloto parcial mede custo gasto, não custo de uma PE convergida. Fonte: `pe_runner.py:235`, `run_controlled.py:77`.

O formulário futuro deve separar: custo observado; projeção condicionada a esse custo com hipóteses; teto reservado; informação esperada e sua fonte. Valores desconhecidos ficam null/OPEN, nunca zero. Uma PE não mede universalmente a distribuição de custos de outros eventos ou injeções. Exigir revisão da extrapolação, atualizar gasto real a cada etapa e parar antes do deadline. O controlador já reserva 12 s internos para limpeza; não contar essa reserva duas vezes. Além disso, declarar margem global para revisão, publicação e outros trabalhos concorrentes. O gerador não decide essa margem.

## Matriz E3.3 e identificabilidade

| Célula proposta, ainda sem N/SNR/horas | Suporte do código congelado | Dependência e produto |
|---|---|---|
| GR, pSEOBNRv4HM_PA, a=0 | Quatro deformações verdadeiras zero; recuperação livre pSEOB | Ruído real off-source, parâmetros físicos de verdade declarados, cobertura, c(SNR), dispersão e 440. |
| GR, IMRPhenomXPHM, a=0 | Quatro deformações zero obrigatórias; recuperação livre pSEOB | Controle entre famílias (spins alinhados na injeção atual), não equivalência com pSEOBNRv5PHM precessante publicado. |
| TGL por leitura, pSEOB, a=1 | Injeção fenomenológica com dtau/domega explicitamente fornecidos | [OPEN] Mapa revisado leitura→verdade→parâmetros pSEOB, convenções, unidades, frame, Mf/chif/z correlacionados e fit adotado. `dtau` livre no ajuste não paga esse mapa. |
| TGL por leitura, XPHM, a=1 | **NÃO IMPLEMENTADO**: qualquer desvio não nulo é recusado | [OPEN/NÃO PAGO] Segunda família TGL. Não substituir por envelope pós-pico, não marcar matriz de duas famílias TGL como completa. |

`injection` tem exatamente a interface `family`, `noise_kind: REAL_OFFSOURCE`, `parameters` (11 coordenadas físicas + quatro deformações; q opcional consistente), `target_network_optimal_SNR`. Só `mode: calibration` e evento da calibração. `event_GPS` continua o evento real em `E2.event_reference_GPS`; o tempo geocêntrico da injeção pertence ao trecho off-source realmente analisado. A janela inteira precisa estar fora da exclusão do evento real. Por detector, `onsource_path == offsource_path` e hashes iguais, contendo também o bloco PSD anterior necessário. Verdade dentro do suporte antes/depois da normalização; distância estritamente interior após reescala. SNR alvo é ótimo de rede **full IMR na PSD/banda**, não SNR de ringdown. A implementação reescala amplitude/distância uma vez e confere SNR; não executa busca iterativa. Fonte: `injection_design.py:26`, `:42`.

Repetições devem especificar trechos de ruído e dependência entre eles; mudar `sampler.seed` não cria ruído independente. Verdades são fixadas por célula, parâmetros de recuperação permanecem livres. Antes de executar: estimador de c, IC/cobertura nominal, tolerância, fórmula de σ(c), correlações por segmento, tratamento de falhas e regra de parada. O cálculo `(σ_inj/piso)^2` só é projeção sob hipóteses de variância/independência verificadas; não fornece N pago agora. Distinguir resolução de recuperação de dtau, poder de separar TGL/GR e identificabilidade após nuisance. Obter σ_sys de df e resultados 440, não inferi-los apenas de dtau220. Se σ(c)>|δ|/5, gate continua vermelho; máximo `NOT_FALSIFIED_UNDERPOWERED`. Não promover convergência do sampler a validade física.

## Cinco alternativas exigidas, sem selecionar

| Alternativa E3.2 | Informação a receber | Situação de implementação / limite |
|---|---|---|
| 1. Piso R-LIN/R-MOD | Piso com fonte por leitura, σ_inj medido, custo do piloto e erro residual | Configuração fenomenológica depende do mapa TGL revisado; nenhuma prioridade atribuída. |
| 2. Bins SNR altos | Distribuição SNR dos elegíveis e calibração que demonstre viés abaixo do piso | SNR alto sozinho não prova viés pequeno. Não selecionar por posterior estreito ou efeito favorável. |
| 3. PE reduzida, amplitude marginalizada | Modelo/priors, auditoria e custo próprios | Não é opção do runner congelado: marginalizações atuais false. Não habilitável só por jobsV2; fora desta preparação. |
| 4. Injeções LVK E1.3 | Resultados já auditados, contrato de prior/verdade e alcance | Reuso descritivo possível; seleção/cobertura e transferência ao novo recovery não ficam pagas por descrição. Nenhum novo posterior lido aqui. |
| 5. pSEOBNRv5PHM / pyseobnr | Instalação, runtime, custo e validação próprios | Não é backend do runner congelado; não habilitável trocando um campo. Não instalar ou medir agora. |

Para cegos, usar lista efetiva do E2/censo e holds, não a contagem histórica de 31 da ordem. Imprimir posteriormente por item SNR com convenção/fonte, E[1/σ²] com hipótese/erro, ganho esperado por hora e soma frente ao alvo. Não igualar automaticamente 1/E[σ]² a E[1/σ²]. Esta previsão informa alocação; não é potência calibrada nem resultado do teste.

## Checklist de publicação futura pelo principal

1. Conferir E2 ATIVO, suas quatro reviews, pins de runtime/código, relógio global e recibos reais do piloto. Nenhum destes gates foi executado nesta preparação.
2. Preencher as cinco alternativas, custos observados/projetados e seus limites; selecionar explicitamente jobs/ordem, bins/verdades/repetições e regra de parada. Registrar o que não cabe como NÃO PAGO, com projeção sustentada ou custo OPEN.
3. Para cegos, revisar publicação depois do E2 e resolver cada DQ hold por evidência pinada. Ausência no corpus auditado não é ausência universal de publicação. Nada de cortes por largura ajustada.
4. Preservar cegueira: offsets dos quatro campos são derivados internamente do segredo já comprometido, por evento/campo. Não pôr seed secreto, offsets, sinais ou médias de parâmetros cegos no orçamento. `sampler.seed` é distinto do segredo. Outputs físicos pareados não autorizam descegar deformações; cegueira é procedural no mesmo host (`blinding.py:14`).
5. Validar configs completos e tempo/priors/injeções contra a árvore congelada e obter revisão independente. O gerador abaixo não substitui `validate_config`, `checked_registration`, validação de lançamento ou parecer científico.
6. Publicar jobs em caminho novo/versionado, orçamento no caminho já fixado pelo E2, depois testemunha correta no túnel **antes** de PE cega. Preservar versões anteriores. Só o principal faz essa publicação; este diretório não emite testemunhas.
7. Rodar exclusivamente pelo controlador, uma fila serial ou outra estratégia com teto agregado comprovado, ≤24 workers e ≤8 h/job nesta ordem. Revalidar tempo/reviews imediatamente antes de cada lançamento. Custo e falhas preservados; deadline não é extensível por config.

## Gerador opcional, não executado

`render_allocation_candidates.py` é um serializador de candidatos com checagens documentais limitadas. Recebe proposta completa do principal conforme `GENERATOR_INPUT.md`, E2/pin, budget/pin e recibos de custo; não escolhe alocação, não calcula ciência, não lê dados científicos ou segredo, não importa `e2_code`. Só escreve futuramente sob `bis/e3_allocation_prepare/candidates/<slug>` com criação exclusiva. Não grava `ORCAMENTO_40H.json` real, jobs ativo, testemunha, registro ou seed. Nenhum input de alocação/candidato foi criado nesta preparação. Sua sintaxe foi inspecionada por AST; sem execução/teste funcional. Revisão independente permanece OPEN.
