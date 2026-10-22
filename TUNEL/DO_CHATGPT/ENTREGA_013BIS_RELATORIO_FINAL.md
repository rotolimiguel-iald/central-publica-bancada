[REAL — relatório final da bancada; encerramento por resultados e paredes medidas. Calibração física e teste cego NÃO PAGOS.]

# ORDEM 013BIS — relatório final

O trabalho entrega o registro, os resultados condicionais, o quadro de alcance e o módulo de leitura. Não produziu um novo posterior pSEOB válido nem demonstrou 5σ físico. O piloto IMR terminou em falha nativa; a revisão do diagnóstico não encontrou um reparo validado que preservasse a região de parâmetros registrada. Por isso a ampliação por PE foi encerrada como parede técnica nesta configuração, e não como falta de tempo ou impossibilidade geral da rota.

Abertura do operador: `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0`. Os recibos encadeiam as etapas realizadas pela bancada até este relatório. A incorporação no programa canônico e a ratificação continuam com a gerência/operador.

## Cumprimento por alvo

| Alvo | PAGO | NÃO PAGO / limite |
|---|---|---|
| F0 | Encerramento conferido dos trabalhos antigos antes do piloto; recibo próprio. | Seus resultados não entram para mudar vereditos. |
| F1 | Entrega M1, correções e portão medido. | Não promove diagnóstico em prova física. |
| F2 | Entrega M2, catálogos, controles e correções ao lado. | C4 permanece INCONCLUSIVE_SYSTEMATICS, NÃO-CEGA. |
| F3 | Entrega M3, template/oráculo e leituras com escopo. | Pontes/identificações abertas não são escolhidas. |
| F4 | Entrega M4, parede C5 e portão do poder. | Calibração livre de massa/spin da C5. |
| F5 | Entrega M5, C6 reclassificada e inícios realizados. | C6 permanece diagnóstico anterior ao portão. |
| F6 | Entrega M6, pacote e reproduções documentadas. | Não converte entrega em evidência física. |
| F7 | Fichas, licenças documentais, arquivos grandes em cache e conferência de integridade. | Custódia/publicação externa não realizadas. |
| F8 | Parte A fechada por resultado/falsificador/parede; MA entregue. | Paredes físicas explicitadas. |
| E0 | Portão refeito, dez leituras, alvos em informação e cenários. | N90 condicionado não garante poder com sistemática real. |
| E1 | Nuisance condicional, seleção documentada e controles existentes. | Eficiência de seleção, normalização e covariância físicas. |
| E2 | Registro com testemunha, hashes, guardas e nulos sintéticos. | Cauda física da pipeline e autorização estatística de descegamento. |
| E3.1 | Comparação Kerr e custo da tentativa IMR; diagnóstico independente. | Reprodução exatamente equivalente do pyRing; posterior pSEOB convergido e custo por evento válido. |
| E3.2 | Orçamento registrado, cinco alternativas, pesos esperados e custo observado separados. | Custo calibrado por posterior/injeção e ganho por hora desconhecidos. |
| E3.3 | Parede, alocação sem novos jobs e estado do gate registrados. | Novas injeções RG/TGL, c(SNR), sigma_sys, cobertura e PE cega. |
| E4 | Fisher440 condicionado, sensibilidade 2D e leituras/modos separados. | Comparação de PE multimodo equivalente e lnB físico normalizado. |
| E5 | Nulo LRT sintético e informação 1/sigma^4. | Transferência browniana na recuperação e sigma_sys físicos. |
| TESTE | Parede/estado AWAITING_DATA registrado sob E2. | TESTE observacional não executado; nenhum evento novo admitido ou descego. |
| E6 | Quadro gerado por script com origens e revisão. | Projeções futuras não são observações nem promessa de datas. |
| E7 | Extrator e consumidor congelados, amostras pareadas completas e revisão. | Likelihood restrita normalizada, seleção e teste físico não implementados/pagos. |

## O portão e as dez leituras

Bases distintas nas colunas: delta e piso são a referência GW250114 sob cada leitura, com seu estatuto C1/E6; N90/informação-alvo e correção/sigma são populacionais, GWTC5_31, com a mistura de precisões preservada. N90 abaixo é o cenário de média gaussiana sem sistemática, não um N garantido para a análise física. O piso é |delta|/5; |delta|/15 permanece sensibilidade. Sigma(c) físico é OPEN em todas as leituras. Na leitura INPUT R-GLOBAL o efeito local é zero por construção; zero não é um piso positivo atendido. Cada estatuto de leitura permanece no quadro completo, sem promoção de INPUT a medição. Correção/sigma é diagnóstico condicional, nunca significância física com gate vermelho.

| Leitura / estatuto | delta de referência | Piso primário INPUT | N90 mistura (arredondado acima) | Informação-alvo N90 | Correção/sigma condicional dos31 | Estado do teste novo |
|---|---:|---:|---:|---:|---:|---|
| R-A [INPUT] | -3.51879e-42 | 7.03757e-43 | OPEN | OPEN | 1.02925e-40 | AWAITING_DATA; gate vermelho |
| R-B [INPUT] | -0.0198453 | 0.00396906 | 3328 | 95216 | 0.604392 | AWAITING_DATA; gate vermelho |
| R-MOD [CONJECTURE] | -0.0368397 | 0.00736794 | 1056 | 30209.4 | 1.06472 | AWAITING_DATA; gate vermelho |
| R-RAIZ-0 [INPUT] | -0.037063 | 0.00741261 | 976 | 27907.2 | 1.11867 | AWAITING_DATA; gate vermelho |
| R-RAIZ-EP4 [INPUT] | -3.51879e-42 | 7.03757e-43 | OPEN | OPEN | 1.02925e-40 | AWAITING_DATA; gate vermelho |
| R-RAIZ-REST [CONJECTURE] | -1.52884e-82 | 3.05769e-83 | OPEN | OPEN | 4.46895e-81 | AWAITING_DATA; gate vermelho |
| R-RAIZ-COHERENT [CONJECTURE] | OPEN | OPEN | OPEN | OPEN | OPEN | AWAITING_DATA; gate vermelho |
| R-LIN [CONJECTURE] | -0.0714769 | 0.0142954 | 263 | 7513.27 | 2.15618 | AWAITING_DATA; gate vermelho |
| R-GLOBAL [INPUT] | -0 | 0 | OPEN | OPEN | 0 | AWAITING_DATA; gate vermelho |
| R-PROP [CONJECTURE] | OPEN | OPEN | OPEN | OPEN | OPEN | AWAITING_DATA; gate vermelho |

Onde a predição de referência não é numérica, correção/σ fica OPEN. Os zeros herdados da C4 para R-PROP e R-RAIZ-COHERENT são marcadores históricos, não predições físicas nulas. O zero numérico de R-GLOBAL, sob sua partição INPUT, é preservado como zero por construção; não paga um piso positivo.

Todas as leituras foram preservadas; nenhuma partição, relógio, deformação440 ou realização estocástica foi escolhida. A RG é o limite clássico/controle. Os escores históricos da C4 ficam nas entregas M2/B1, com seu escopo220 condicional e o veto da cláusula relativa.

## Resultados que não se confundem

O controle Kerr do evento conhecido convergiu nos critérios registrados para a variante com PSD pública. A diferença contra o posterior publicado é descritiva, com famílias/configurações e equivalência incompleta explicitadas em B3. A variante Welch foi recusada por condicionamento; o primeiro resultado com PSD pública parou parcial. Ambos foram preservados.

O piloto IMR sofreu SIGSEGV antes de produzir posterior aceito. No diagnóstico isolado, aumentar a frequência de geração produziu também um aborto de alocação de memória num ponto do prior. A hipótese de capacidade do buffer é CONJECTURE; a causa exata do SIGSEGV original continua OPEN. Recusar numericamente pontos do prior, remover modos ou estreitar priors não foi tratado como reparo científico.

Os nulos sintéticos, o Fisher440 e as razões de densidade foram medidos e revisados. A cauda t5 excede muito a referência gaussiana5σ; zero excedências em uma simulação finita é apenas um limite superior de probabilidade. O modo440 não é observação independente do220 no mesmo evento. A rotaIV mantém a dependência da realização estocástica e da transferência ainda aberta.

As candidatas foram classificadas por metadados anteriores à PE: 14 sem publicação encontrada no escopo, dez sem hold e quatro com hold. Os pesos esperados são projeções do ajuste em SNR; nenhum desses pesos é informação observada de uma PE nova. Na execução desta bancada registrada nos recibos, não houve download de strain novo para teste, posterior novo de teste ou descegamento.

E7 processou 33 produtos de calibração. O consumidor devolveu 20 linhas (dez leituras × duas variantes de modos), sem eventos de teste acrescentados. z físico, lnB físico e correção/sigma física permanecem null.

## Custo e itens não pagos

Contador conservador contínuo até a emissão deste documento: 4.937109h desde o início; saldo nominal 35.062891h de40. Prazo efetivo da alocação para finalização (`finalization_stop_utc`): `2026-09-23T01:02:56.988802+00:00`. O saldo nominal das40h não está alocado a novas PE/injeções e não prorroga essa reserva de finalização. Início `2026-09-22T19:06:33.802143+00:00`; deadline inalterado `2026-09-24T11:06:33.802143+00:00`. Orquestração e revisão contam; trabalhos simultâneos não são somados em dobro. O contador final da publicação será atualizado no recibo final.

Os custos medidos de cada campanha e da tentativa falha estão no orçamento/B3; 11 segundos até um crash não são custo por evento convergido. As contagens necessárias para calibrar os pisos e as cinco alternativas estão explicitadas, com custo em horas OPEN quando falta medição válida. Saldo não utilizado não significa que a condição sistemática foi satisfeita. Não se gastou o restante repetindo uma pipeline inválida.

## Reprodução, incidentes e custódia

As entregas intermediárias contêm os comandos e fichas por alvo; a ficha própria e o comando documental estão abaixo. Execuções recusam destinos existentes: reprodução exige cópia isolada e novo registro quando altera o instrumento. O extrator usa h5py no runtime pinado; o consumidor usa NumPy, valida os hashes e preserva amostras completas. N/A — sem Lean; nenhum teorema/gate formal movido.

Foram conservados os abortos, resultados parciais, correções documentais de hashes, revisões recusadas e versões substituídas. A custódia da semente é procedural no mesmo host; não representa separação de administradores. A bancada declara não ter divulgado conteúdo de semente ou offset em seus artefatos desta ordem; isto não é auditoria global do host. O detalhamento das tentativas de selagem, permissões e do código de preparação permanece em B2/B3/B5 e nos manifestos.

A conferência final dos insumos/fontes/ParteA está no recibo de integridade: qualquer exceção de leitura de metadados é explícita. No escopo declarado desta bancada, as escritas foram limitadas à pasta Chatgpt; os pares de hashes e a cobertura do recibo de integridade foram validados antes da emissão. Não se executou commit/push/publicação nesta ordem; essa declaração não equivale a auditar ações de outras sessões. O pacote da bancada aguarda auditoria externa da gerência e ratificação do operador, como determina a ordem.


## Quadro de alcance aprovado — anexo integrante

Quadro integral: [QUADRO_DE_ALCANCE_V1.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.md>) — SHA256 `7b2e772c464033df5edc247613b469e3256ad865851f3876db12c33eef141263`. Revisão documental: [E6_ACTUAL_RESULT_REVIEW_002.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_actual_review/E6_ACTUAL_RESULT_REVIEW_002.json>) — `44e1817a5eb59ab087661c055e29b584e818079d8ba0403be79a30fd3509e8ed`. O JSON pareado, também pinado neste relatório, contém unidades, origens e motivos OPEN de cada campo. Este anexo integra o relatório; não foi recalculado pelo gerador.

Grupos: O4_HOJE, O4_CEGO, O4C_GWTC6, O5_BANDA, ET, CE. Todas as dez leituras, sem seleção. As contagens abaixo descrevem cobertura documental, não eventos científicos ou poder.

| Rota | Células | Cenários já produzidos | Unidade da informação-alvo | Estado do TESTE |
|---|---:|---:|---|---|
| TAU220_POPULATION | 60 | 370 | Σ1/σ²(dtau220) | AWAITING_DATA; físico null |
| TAU440_FIXED_SOURCE_FISHER | 60 | 1980 | Σ1/σ²(dtau440), fonte fixa | AWAITING_DATA; físico null |
| DF220_POPULATION_WIDTH_IV | 60 | 190 | informação local da variância df220; pesos 1/σ⁴ | AWAITING_DATA; físico null |

O anexo preserva z esperado **condicional**, N90 em informação, equivalentes GW250114 do canal próprio, IC de taxa e correção/σ por cenário. Fisher440 não paga PE multimodo; IV permanece limite inferior enquanto transferência/σsys estão OPEN. Taxas e bandas O5/ET/CE não são promessa de data.

## Leituras e variantes E7 — estados efetivos

| Leitura | Estatuto C1/E6 | Variante | Veredito | Dados/modos | Alvo | Motivo físico OPEN |
|---|---|---|---|---|---|---|
| R-A | INPUT | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-A | INPUT | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-B | INPUT | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-B | INPUT | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-MOD | CONJECTURE | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-MOD | CONJECTURE | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-RAIZ-0 | INPUT | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-RAIZ-0 | INPUT | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-RAIZ-EP4 | INPUT | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-RAIZ-EP4 | INPUT | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-RAIZ-REST | CONJECTURE | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-RAIZ-REST | CONJECTURE | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-RAIZ-COHERENT | CONJECTURE | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-RAIZ-COHERENT | CONJECTURE | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-LIN | CONJECTURE | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-LIN | CONJECTURE | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-GLOBAL | INPUT | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-GLOBAL | INPUT | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-PROP | CONJECTURE | 220_only | AWAITING_DATA | CONDITIONAL_220_ONLY | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |
| R-PROP | CONJECTURE | 220_plus_440_INPUT | AWAITING_DATA | OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM | OPEN_OPERATIONAL_TARGET_NOT_CALIBRATED | OPEN_NORMALIZED_RESTRICTED_MODEL_SELECTION_CALIBRATION_AND_BLIND_RELEASE |

OPEN por leitura nos diagnósticos condicionais (copiado de estados/motivos; sem ler amostras):

- R-A [INPUT]: OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-B [INPUT]: OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-MOD [CONJECTURE]: EXACT_PAIRED_QNM_REQUIRED_NO_BCW_SUBSTITUTION; OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-RAIZ-0 [INPUT]: OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-RAIZ-EP4 [INPUT]: OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-RAIZ-REST [CONJECTURE]: OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-RAIZ-COHERENT [CONJECTURE]: Occupation and fitting window required; initial slope is not delta_tau; OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-LIN [CONJECTURE]: OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-GLOBAL [INPUT]: OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated
- R-PROP [CONJECTURE]: Propagation exponent is not a local damping rate; OPEN_MISSING_440_POSTERIOR_AND_EXACT_QNM: Five-column extractor carries 220 only; 220+440 is not evaluated

## Custos observados por campanha — não somar ao ledger contínuo

Transcrição dos recibos/orçamento. CPU de filhos, soma de paredes de filhos e intervalo controlador têm escopos diferentes. Nenhuma destas linhas é acrescentada ao contador contínuo. Outros trabalhos não itemizados permanecem incluídos nele; não se inventa custo isolado.

| Item / origem e ponteiro | Parede ou intervalo (s) | CPU (s) | Escopo |
|---|---:|---:|---|
| Ajuste nuisance B1 — [RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/runs/authorized_001/RECEIPT.json>) `/wall_seconds`; SHA256 `7b63a6faa19eb8fc4fd5f9879b90c9408c662fb8e6a73fdad9ede4ffd16ef5a5` | 41.584701691 | 24.338969549 `/cpu_seconds` | Ajuste condicional existente; covariância INPUT, não calibração física |
| Revisão direta B1 — [E1_DIRECT_KDE_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E1_DIRECT_KDE_REVIEW.json>) `/wall_seconds`; SHA256 `230dd8f9424a3d8603d52131eb8fd92996cba84ff70527bf0ee31d00c65b6c31` | 13.677909669 | OPEN | Revisão direta KDE condicional; CPU não declarada neste recibo |
| Nulos MC E2 — [RESULT_E2_NULL_CAMPAIGN.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/RESULT_E2_NULL_CAMPAIGN.json>) `/wall_seconds`; SHA256 `cb104ff0c6c4049e9bc4ee9db7a95a53224045039916438738958a691ee4643a` | 437.517602269 | OPEN | Campanha de nulos sintéticos; não calibração física |
| E4/E5 produtor — [RESULT_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e4_e5_prepare/runs/authorized_001/RESULT_RECEIPT.json>) `/wall_seconds_through_result_hash`; SHA256 `1f4fb47ad04a1b37b8df458056ed02c4cbdd71512c613e7ee0627aa521e4184b` | 6.056717614 | 4.315131978 `/process_CPU_seconds_through_result_hash` | Entrada no main até gravação/hash do resultado; exclui gravação do recibo |
| Revisão independente E4/E5 — [INDEPENDENT_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json>) `/wall_seconds`; SHA256 `d8f8d56faf6e6a65735594d9d80a5a3d39c18022f4d4782a2fcf31f241f2205d` | 8.570956578 | OPEN | Revisão aritmética condicional; não nova ciência |
| Controlador E4/E5 — [E4_E5_EXECUTION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E4_E5_EXECUTION_V1.json>) `/wall_seconds`; SHA256 `3cfaec349e3b3dcf6c2334ff4d6fd4783cc37a46e66726ad4a90cadd5e06061f` | 6.350248688 | OPEN | Envelope do lançamento; sobrepõe o tempo do produtor, não somar |
| /measured_costs/Kerr_V1 | 394.299 | 389.027 | Includes initialization, conditioning, sampling and cleanup; one process/one BLAS thread; no physical claim |
| /measured_costs/Kerr_V2 | 641.003 | 637.422 | Includes initialization, conditioning, sampling and cleanup; one process/one BLAS thread; no physical claim |
| /measured_costs/Kerr_Welch_separate_diagnostic | 3.40237 | 1.6328 | Includes custody, deterministic wrapper tests, single preparation and source rehash; excludes final receipt flush |
| /measured_costs/IMR_pilot_failed_controller | 11.0111 | usuário 4.43522; sistema 1.25899 | Tentativa falha; não custo por posterior |
| /measured_costs/IMR_native_diagnostic | soma filhos 13.1688; plano→último fim 192.043 | soma filhos 10.4009 | Medidas sobrepostas; não somar entre si |
| E7_FINAL_EXECUTION_V1 /wall_seconds | 256.918 | OPEN | Extração/consumo documental de calibração existente; sem PE nova |

| Alternativa não paga | Custo estimado qualificado (s) | Alocação nova (s) | Motivo |
|---|---:|---:|---|
| i — Calibrar apenas pisos R-LIN/R-MOD | OPEN | 0 | Coeficientes recalculados abaixo; nenhum sigma_inj/custo de recuperação qualificada medido. Piso mais largo não corrige falha nativa. |
| ii — Calibrar somente bins de SNR alto | OPEN | 0 | Menor largura é expectativa condicional; viés abaixo do piso não demonstrado. Nenhum bin ou evento admitido por este candidato. |
| iii — PE reduzida com amplitude marginalizada | OPEN | 0 | Alternativa metodológica da ordem; instrumento diferente, sem implementação/custo/convergência validados neste escopo. Nenhum workaround executado. |
| iv — Reutilizar injeções públicas LVK | OPEN | 0 | Diagnóstico F2 existente revisado pode ser reutilizado descritivamente; duas recuperações com/sem44 não são curva c(SNR), cobertura repetida nem sigma_sys calibrado. Zero PE nova. |
| v — pSEOBNRv5PHM via pyseobnr em venv próprio | OPEN | 0 | Instalabilidade, custo e qualificação não medidos aqui; sem instalação, rebuild ou troca de runtime. Custo permanece null. |

Custo por posterior IMR convergido: OPEN. Zero alocado não é custo estimado zero. Os tempos B1/B2 acima foram copiados dos campos dos recibos pinados, não dos arredondamentos da nota nem inferidos por diferença. O controlador E4/E5 engloba o produtor: não somar suas durações.

## Integridade efetivamente conferida no recibo

Recibo em `2026-09-22T23:42:52.203720+00:00`: inventário com 217 insumos, 31 fontes e 47 artefatos entregues da Parte A; cobertura e pares de hashes conferidos pelo gerador. Não é uma nova auditoria de outras casas nem varredura de segredos. O conteúdo do cache não foi varrido pelo recibo; o gerador não abre JSON de amostras ou HDF. Pins desses payloads são transportados do recibo E7 e closure, com tamanho conferido.

Exceções de metadados registradas (não ocultadas pelo status PASS):
- {"path": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e3_allocation_review\\fixtures_001\\finding_symlink_output_escape\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e3_allocation_prepare\\candidates", "error": "[WinError 1920] Não é possível o acesso ao arquivo pelo sistema: 'C:\\\\IALD\\\\Central de Patentes\\\\Chatgpt\\\\ORDEM_013_RINGDOWN\\\\bis\\\\e3_allocation_review\\\\fixtures_001\\\\finding_symlink_output_escape\\\\Chatgpt\\\\ORDEM_013_RINGDOWN\\\\bis\\\\e3_allocation_prepare\\\\candidates'", "lstat_bytes": 0, "scope": "No content read; link/fixture must be classified independently"}

## Reprodução documental isolada

Executar no mesmo ambiente Python do comando abaixo. Não executa ciência, não publica no túnel e não abre arrays de posterior/HDF. Requer novo destino; o horário do replay será novo e não é reprodução byte a byte nem consumo científico adicional. O replay não reabre o orçamento e não substitui o draft aprovado.

```powershell
& 'python' '-B' 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\refeito\prepare_final_report_v5_013bis.py' '--e6-result' 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e6_prepare_v3\runs\wall_actual_001\QUADRO_DE_ALCANCE_V1.json' '--e7-review' 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e7_execution_review\E7_EXECUTION_INDEPENDENT_REVIEW.json' '--integrity-receipt' 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\FINAL_INTEGRITY_20260922T234252203720Z.json' '--extra-manifest' 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\FINAL_ARTIFACT_CLOSURE.json' '--e6-review' 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e6_actual_review\E6_ACTUAL_RESULT_REVIEW_002.json' '--output-dir' 'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\final_report_replay_20260923T000247Z' '--replay'
```

Ficha: [REAPROVEITAMENTO_FINAL_REPORT_V5.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/REAPROVEITAMENTO_FINAL_REPORT_V5.md>); SHA256 `3ecaaa434f0f4e4be4256ea87479738b1c7b252bf54f5408f4406f26425dd4fd`.

## Arquivos, hashes e portas de auditoria

- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md>) — `0118a54b7a806a0a5ef5572afc8349c223cc3da4bec62ff18a9cd1b07433f9f0` (876 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_MA_fechamento.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_MA_fechamento.md>) — `1e1b31226ddbc211f7a751c4add712d4deeeb99939d5b74c87b45e6d3d3fcbf4` (5020 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013_M1_fechamento.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013_M1_fechamento.md>) — `ad1f6eb74d3f80a9e84fc62f726e665b8f3616f80f270fb4f0f2a31e94663aca` (8290 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013_M2_C4_fechamento.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013_M2_C4_fechamento.md>) — `2c3f8a7d0aad00ba3ec246718f159f036a8e7a543550f3f1d3f77abaced6b34f` (17368 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013_M3_C3_2_C2_RMOD.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013_M3_C3_2_C2_RMOD.md>) — `611c64fcb1f807ec90ed16549a388695779e60d2112cd0b3b6cdccb4ee61306a` (7005 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013_M4_C5_parede_e_portao.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013_M4_C5_parede_e_portao.md>) — `b34688251e8904b5aa721deddd26bac889d7328e756fbe38c255876058c4001e` (7471 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013_M5_C6pre.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013_M5_C6pre.md>) — `7827196400da515d23c606e3ed81a645ec8b7efede7447afa9aaae7431147e3d` (6829 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013_M6_C7_final.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013_M6_C7_final.md>) — `2e7107568c3020d5ac81b7ceb81aa9eb0a6adf944f7f28d78fbe55a508f12f8a` (8032 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013_ERRATA_contrato.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013_ERRATA_contrato.md>) — `13d8c47e8faaa38aa48a5a6e2cb138e7e0cd06ed3edc5989d47b01c16c2a751f` (42681 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_B1_portao_e_nuisance.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_B1_portao_e_nuisance.md>) — `c33f4f36eedc9060859ae38bdd3f9993b59fada62cee489e8c964975b792a3e8` (6601 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_E2_REGISTRO_V1.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_E2_REGISTRO_V1.md>) — `e95787fd52852c090b18d760ba5f58cb422087b136686414571023a19782403c` (6390 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_B2_registro_e_440.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_B2_registro_e_440.md>) — `06345093b5fca7b250f9360f66cf40bfc0becbd54b6e4cce4505f828f96fa8d7` (20687 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_B3_piloto_e_orcamento.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_B3_piloto_e_orcamento.md>) — `f8c0a12ab4fe9505392006d9d3dce6938f972eb35a734ad1ea9b38977fb79394` (11886 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_B4_calibracao_e_cegos.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_B4_calibracao_e_cegos.md>) — `0978f95d40f9734d768ac25b3dc6652d27fdf8800cf13b90ec0f9aec3fb5c112` (5406 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_TESTE_O4_cegos.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_TESTE_O4_cegos.md>) — `5702a6f11ec97228f03c9589e97106938560885b13b632de1922c0f11c145c9e` (5773 B).
- [TUNEL/DO_CHATGPT/ENTREGA_013BIS_B5_quadro_e_modulo.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_013BIS_B5_quadro_e_modulo.md>) — `ede7e0cf67cee821def99a1e834099104b5d19269ff4bd113dac1dd48311b19a` (9006 B).
- [ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.json>) — `f021e0c94df00d23a8f9fff236856c6227019762a98ce2738161f486fda6678b` (17870774 B).
- [ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/QUADRO_DE_ALCANCE_V1.md>) — `7b2e772c464033df5edc247613b469e3256ad865851f3876db12c33eef141263` (1671106 B).
- [ORDEM_013_RINGDOWN/bis/e6_actual_review/E6_ACTUAL_RESULT_REVIEW_002.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_actual_review/E6_ACTUAL_RESULT_REVIEW_002.json>) — `44e1817a5eb59ab087661c055e29b584e818079d8ba0403be79a30fd3509e8ed` (5856 B).
- [ORDEM_013_RINGDOWN/bis/e7_execution_review/E7_EXECUTION_INDEPENDENT_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_execution_review/E7_EXECUTION_INDEPENDENT_REVIEW.json>) — `284a3cddb6eaa4b799c4268f76844f1d1f1a6da5704a58946f09271ded397e26` (263584 B).
- [ORDEM_013_RINGDOWN/bis/FINAL_INTEGRITY_20260922T234252203720Z.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/FINAL_INTEGRITY_20260922T234252203720Z.json>) — `6e2d203b20cc704196d51cd7a11a2b9ab56c1fca1aff4996d33f25a39a65cd29` (123701 B).
- [ORDEM_013_RINGDOWN/bis/FINAL_ARTIFACT_CLOSURE.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/FINAL_ARTIFACT_CLOSURE.json>) — `2cc314a265e412fb7403971c24924cbff1e947f6bfb3bfd53b57a38d8578022a` (18163 B).
- [ORDEM_013_RINGDOWN/bis/e6_actual_review/B5_ACTUAL_DELIVERY_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_actual_review/B5_ACTUAL_DELIVERY_REVIEW.json>) — `b5c68489ad318bcb553282d671c287624e3802e66457b6bd4ea71d158d402b75` (11875 B).
- [ORDEM_013_RINGDOWN/bis/B5_DELIVERY_MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/B5_DELIVERY_MANIFEST.json>) — `985275ce9928f487201a0e7645c4321876e438a46b98e77d220c8759e9c3672c` (3339 B).
- [ORDEM_013_RINGDOWN/ORCAMENTO_40H.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/ORCAMENTO_40H.json>) — `892e416585062eef5229e01c2e8a6c5b8d3c4ee8a10a72798c0ab2034e5f42e4` (126793 B).
- [ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1.json>) — `e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416` (183005 B).
- [ORDEM_013_RINGDOWN/NUISANCE_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/NUISANCE_V1.json>) — `83f860bbfa904c0048005c8b0f1b367814032052f352e780af7d77ed1f257b85` (1437250 B).
- [ORDEM_013_RINGDOWN/PORTAO_DA_AMPLIACAO_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/PORTAO_DA_AMPLIACAO_V1.json>) — `710028a7d2af7b649511afe369d88462d2add95c5fecbb1fb03c517fc91fe8a0` (903525 B).
- [ORDEM_013_RINGDOWN/bis/E7_FULLSAMPLE_RESULT_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E7_FULLSAMPLE_RESULT_V1.json>) — `c2f96864c18f3aea1e3da7b74da17fdd482230e626adbfaf1fb533094fc4e9ea` (384193 B).
- [ORDEM_013_RINGDOWN/bis/E7_FINAL_EXECUTION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E7_FINAL_EXECUTION_V1.json>) — `035212e25370f7d7c780c4a2e1f4a5732785d83b55e60417e8c5ee9ea31f10c9` (3489 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json>) — `9c56068518044bf077b12fb3c7d2a85eb8fb7eb5d1411467ebac30d094b29893` (54926 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_failure_diagnostic/MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_failure_diagnostic/MANIFEST.json>) — `f24326c2c202547495f91018545f8eb10f0f7e327c984873a6cf73f5c537aa01` (35308 B).
- [ORDEM_013_RINGDOWN/bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json>) — `0e92967fd6f228ad2e6bc003b0ed8a67a994a6fdc6d660013e99c66a686248c7` (2190412 B).
- [ORDEM_013_RINGDOWN/bis/M6_MA_DELIVERY_MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/M6_MA_DELIVERY_MANIFEST.json>) — `a4fe6be99038dcd8ef832303d237673ef2edaef69a7a76567180c223a3dfbcf0` (7899 B).
- [ORDEM_013_RINGDOWN/bis/B2_DELIVERY_MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/B2_DELIVERY_MANIFEST.json>) — `5e40faf24890b5cba5a603b821d3b6f205bc0db8b34531e15a72b1639384ff61` (4386 B).
- [ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/PART_B_BUDGET_START.json>) — `2b3cfefd17cb8f3df845172a3b41f6e457b92b2c5bb164128aa0b40e8919355f` (1536 B).
- [ORDEM_013_RINGDOWN/bis/B1_DELIVERY_MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/B1_DELIVERY_MANIFEST.json>) — `ef3d21edfd3a925812a26920f8f218ee9d6c6d0588f6436e3f0550dcd6fddcb4` (614 B).
- [ORDEM_013_RINGDOWN/bis/E3_WALL_BUDGET_ACTIVATION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E3_WALL_BUDGET_ACTIVATION_V1.json>) — `15a24c061d3e8adf989399203f46b27f255a5c8feb3951ba2fb943cb9125b7d5` (761 B).
- [ORDEM_013_RINGDOWN/bis/INPUT_INTEGRITY_013BIS_retry.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/INPUT_INTEGRITY_013BIS_retry.json>) — `e87878ac8b15e31d726557a540f044d62f334d81e3e9b5d56d7368113e65b5cd` (114960 B).
- [ORDEM_013_RINGDOWN/C1_LEITURAS_v4.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C1_LEITURAS_v4.json>) — `126270a896d8589870954b209155f26a8b08295839b31e0e9a6e28e512621980` (35419 B).
- [ORDEM_013_RINGDOWN/refeito/prepare_final_report_v5_013bis.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/prepare_final_report_v5_013bis.py>) — `6f2128516efa7f7781fddd89dcd0eda0dff1e97a1d4a580fd09c67e5ba5f57df` (39134 B).
- [ORDEM_013_RINGDOWN/refeito/REAPROVEITAMENTO_FINAL_REPORT_V5.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/REAPROVEITAMENTO_FINAL_REPORT_V5.md>) — `3ecaaa434f0f4e4be4256ea87479738b1c7b252bf54f5408f4406f26425dd4fd` (1551 B).
- [ORDEM_013_RINGDOWN/refeito/FINAL_REPORT_V5_IMPLEMENTATION_MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/FINAL_REPORT_V5_IMPLEMENTATION_MANIFEST.json>) — `4783b65c87b8d9a241bd5f8d95aa650ec85b6e2e738f16f87e3dcd6c42d5081d` (2755 B).
- [ORDEM_013_RINGDOWN/bis/e6_review/FINAL_DRAFT_INDEPENDENT_REVIEW_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_review/FINAL_DRAFT_INDEPENDENT_REVIEW_V1.json>) — `e14b558579d5f769bc1d8bae965bb5089cc512c2bcc5830470b5305483cc3387` (20142 B).
- [ORDEM_013_RINGDOWN/bis/e3_budget_wall_review/SYMLINK_CLASSIFICATION.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_budget_wall_review/SYMLINK_CLASSIFICATION.json>) — `2f0023b08f6b3ba785a3090e570e96beea7dd07d654c9c726aa31dd10ca39ca1` (818 B).
- [ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/runs/authorized_001/RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e1_nuisance_v2/runs/authorized_001/RECEIPT.json>) — `7b63a6faa19eb8fc4fd5f9879b90c9408c662fb8e6a73fdad9ede4ffd16ef5a5` (1316 B).
- [ORDEM_013_RINGDOWN/bis/E1_DIRECT_KDE_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E1_DIRECT_KDE_REVIEW.json>) — `230dd8f9424a3d8603d52131eb8fd92996cba84ff70527bf0ee31d00c65b6c31` (12117 B).
- [ORDEM_013_RINGDOWN/bis/RESULT_E2_NULL_CAMPAIGN.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/RESULT_E2_NULL_CAMPAIGN.json>) — `cb104ff0c6c4049e9bc4ee9db7a95a53224045039916438738958a691ee4643a` (8052 B).
- [ORDEM_013_RINGDOWN/bis/e4_e5_prepare/runs/authorized_001/RESULT_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e4_e5_prepare/runs/authorized_001/RESULT_RECEIPT.json>) — `1f4fb47ad04a1b37b8df458056ed02c4cbdd71512c613e7ee0627aa521e4184b` (756 B).
- [ORDEM_013_RINGDOWN/bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json>) — `d8f8d56faf6e6a65735594d9d80a5a3d39c18022f4d4782a2fcf31f241f2205d` (61377 B).
- [ORDEM_013_RINGDOWN/bis/E4_E5_EXECUTION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E4_E5_EXECUTION_V1.json>) — `3cfaec349e3b3dcf6c2334ff4d6fd4783cc37a46e66726ad4a90cadd5e06061f` (757 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_review/E3_WALL_BUDGET_CANDIDATE_REVIEW_v2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_review/E3_WALL_BUDGET_CANDIDATE_REVIEW_v2.json>) — `cbea2938b692b79206cf87977567ba060963a0a835e1bb10502a4dad1ce51943` (95501 B).
- [ORDEM_013_RINGDOWN/bis/e3_budget_wall/MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_budget_wall/MANIFEST.json>) — `c049aa8c257e9706882bc8853aeda81c0245764d8417570f4769433c475f01c8` (6677 B).
- [ORDEM_013_RINGDOWN/bis/E3_KERR_LAUNCH_V2.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E3_KERR_LAUNCH_V2.json>) — `4d56e6bc1906a644ddd6554d7330cd1e1aa8263b5ff1f75ce868022aa529a305` (917 B).
- [ORDEM_013_RINGDOWN/cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json>) — `39e0073a17aa9236420cf93232786f5a289593359aa40e1c01103474c1821efb` (3636 B).
- [ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V1/CONTROLLER.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_PSEOB_PILOT_V1/CONTROLLER.json>) — `bf3f874342d15c4d7687380baf52710237dab7a67fb4ffc0a759a3f59506d72b` (828 B).
- [ORDEM_013_RINGDOWN/bis/e3_blind_review/REVIEW_RECEIPT_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_blind_review/REVIEW_RECEIPT_V1.json>) — `e456d058f41847acc37d45d58543d34a4be638fedce1ee2eeeaad7b2603ee920` (1596 B).
- [ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B3.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B3.md>) — `7535ec53b4c1851728e5e3a09de400cd17f91362f1faefa7cd773e5358526f59` (613 B).
- [ORDEM_013_RINGDOWN/bis/B3_DELIVERY_MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/B3_DELIVERY_MANIFEST.json>) — `1ceeafc2987088a37213a922b95a07f9c935222d520ecbe6e67a8c2dd9715981` (2568 B).
- [ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/e3_2_actual_001/ADAPTER_REVIEWED.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/e3_2_actual_001/ADAPTER_REVIEWED.json>) — `3f81fa0f7b517a58a9cdb90f2625e1993a0bbcab5cacf81cea8bf1b97d7620dc` (1119 B).
- [ORDEM_013_RINGDOWN/bis/e6_review/E3_2_ACTUAL_MAPPING_REVIEW_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_review/E3_2_ACTUAL_MAPPING_REVIEW_V1.json>) — `56ce9ae31243ed704949022095c299c0528f35aecf0032c1d5f89928329ca0f1` (4161 B).
- [ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/e3_3_actual_001/ADAPTER_REVIEWED.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/e3_3_actual_001/ADAPTER_REVIEWED.json>) — `9a25fb168b4be4139b3c4fcead35ef9cb9271c939bf8cb001a13eb7a5c8c2c28` (1246 B).
- [ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/e3_3_actual_001/WALL_SOURCE.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/e3_3_actual_001/WALL_SOURCE.json>) — `48923a9c63c11a99473ceccb755055de755032d17d61ac4635edc811fa4bce43` (1647 B).
- [ORDEM_013_RINGDOWN/bis/e6_review/E3_3_ACTUAL_MAPPING_REVIEW_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_review/E3_3_ACTUAL_MAPPING_REVIEW_V1.json>) — `056ff20f33ede7e01797837734343e859de0c7a33b661a374ab9fa05777512b8` (4583 B).
- [ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/test_actual_001/ADAPTER_REVIEWED.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/test_actual_001/ADAPTER_REVIEWED.json>) — `f0cf7a668276d3df0355a231f9c38d46fdef42f29de984e3b144dcf5a286e2de` (325360 B).
- [ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/test_actual_001/WALL_SOURCE.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_wall_stages/candidates/test_actual_001/WALL_SOURCE.json>) — `60d1b3354c270062d6b1511ff1e8b842902956fb295e14354700669c7f413904` (319114 B).
- [ORDEM_013_RINGDOWN/bis/e6_review/TEST_ACTUAL_MAPPING_REVIEW_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_review/TEST_ACTUAL_MAPPING_REVIEW_V1.json>) — `10246775bac165116c3de2362e7722b04822e291edd96d3af31bac0762a0babc` (328854 B).
- [ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B4_TESTE.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B4_TESTE.md>) — `834d7ba3586247c9654ecd344c5e0f75043dca212a32f9f01e9b534898ddc07a` (432 B).
- [ORDEM_013_RINGDOWN/bis/B4_TEST_DELIVERY_MANIFEST.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/B4_TEST_DELIVERY_MANIFEST.json>) — `a431926241035a2a6b5ffeba27feef263780fb9cd0b2e06c1c731a0cd22aeac9` (2756 B).
- [ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/RESULT_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001/RESULT_RECEIPT.json>) — `971142f08e53d3f1bbb4e0c98c9ab4a9dd18a5d85624e5e61539ae55948801bd` (455 B).
- [ORDEM_013_RINGDOWN/cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json>) — `81e65ff3c54260611ae4bf7539624119050f9ee7389d52cbc4ef2756f54771c0` (92737524 B).
- [ORDEM_013_RINGDOWN/bis/E7_FINAL_AUTHORIZATION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E7_FINAL_AUTHORIZATION_V1.json>) — `2848e969bcbbeb6807eaac5fa2137dd9122bce802efecaf09e0d6dc78fab60a7` (982 B).
- [ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/extrai_posteriores_pseob.py>) — `3e896bd014db610c9b83c6171de2b3b98db506e597b068da20617e189734e330` (7673 B).
- [ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/producer/tgl_ringdown_ampliacao.py>) — `99a9ebc8e8a22c3a14f06b8f6dd465400beaf4d95cbef989d7d5652b5b4b8355` (29940 B).
- [ORDEM_013_RINGDOWN/bis/e7_prepare/EXTRACTION_PLAN.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e7_prepare/EXTRACTION_PLAN.json>) — `7dc138a1690d45d381fc36d6e5cb54967b028741158f625ac814fb92159a7335` (47760 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_review/E7_ORCHESTRATION_V2_CLOSING_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_review/E7_ORCHESTRATION_V2_CLOSING_REVIEW.json>) — `6dc86ef2e1963eb073dd257ac6384752f38709c4a4cedc9fd25b799abbc4b19b` (1067 B).
- [ORDEM_013_RINGDOWN/bis/e6_review/E6_FOCUSED_CLOSING_V3_RECEIPT.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_review/E6_FOCUSED_CLOSING_V3_RECEIPT.json>) — `5cb67afe68462376e1e1fc093326cb82dfe1405a00098a9045dad3440070f0dd` (1947 B).
- [ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B5.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/REAPROVEITAMENTO_AMPLIACAO_B5.md>) — `d5277c4d033062fd0214df008f2631837f5b0e485e7f1cadec040a3dee93abfc` (469 B).
- [ORDEM_013_RINGDOWN/bis/E6_ACTUAL_AUTHORIZATION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E6_ACTUAL_AUTHORIZATION_V1.json>) — `3dfa461737d70fbb86753359fae618ebe2b79c53bb2ab8936b40a7bf56976381` (2011 B).
- [ORDEM_013_RINGDOWN/bis/E6_ACTUAL_EXECUTION_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E6_ACTUAL_EXECUTION_V1.json>) — `c93674065d0d5ea4d6b63eec47c7411ecda624ce2e896d1f14bc2e1ad8409822` (1524 B).
- [ORDEM_013_RINGDOWN/bis/e6_actual_review/E6_EXECUTION_AND_MARKDOWN_REVIEW_001.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_actual_review/E6_EXECUTION_AND_MARKDOWN_REVIEW_001.json>) — `f15bb719fec2d535e80409be40488c9428a75e5b5e1c7b16dc53be2d0dbf2c02` (1487 B).
- [ORDEM_013_RINGDOWN/bis/e3_wall_stages/STAGE_CHAIN_FINAL_MANIFEST_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_wall_stages/STAGE_CHAIN_FINAL_MANIFEST_V1.json>) — `56915f0788607788f899bd5bba4838518c6ab3d3f6a99bb751310da54e4f7565` (5716 B).
- [ORDEM_013_RINGDOWN/bis/e3_wall_stages/STAGE_CHAIN_HANDOFF_V1.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_wall_stages/STAGE_CHAIN_HANDOFF_V1.json>) — `181879b3c8ed06cb18044c5d516de3c75ecbbc55d9f1d3e1eb02dde9af8b125f` (5076 B).
- [ORDEM_013_RINGDOWN/bis/e6_review/FINAL_PUBLISHER_STATIC_CLOSING_V2.md](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e6_review/FINAL_PUBLISHER_STATIC_CLOSING_V2.md>) — `3cad1981021e95708a75966c846a5c6cae1d04df5c2f539e2f86997e9282090a` (3196 B).
- [ORDEM_013_RINGDOWN/refeito/publish_final_report_v2_013bis.py](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/publish_final_report_v2_013bis.py>) — `d42fc24746e545d89f2c251461be2bdc6f39d41f220e5ec2e194f63a6f3b39ce` (4858 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_review/E3_WALL_BUDGET_ACTIVATION_V2_CLOSING_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_review/E3_WALL_BUDGET_ACTIVATION_V2_CLOSING_REVIEW.json>) — `fb42200925fc3424334fad937085e8fd27a3fd980ff4ca425a5058e0d979ff98` (5094 B).
- [ORDEM_013_RINGDOWN/bis/e3_pilot_review/DELIVERY_NOTES_V2_STATIC_CLOSING.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_pilot_review/DELIVERY_NOTES_V2_STATIC_CLOSING.json>) — `831a0217789ab610f23fa3ecd158d4fbff789f9741af6df601d9fcde39d8c430` (1526 B).
- [ORDEM_013_RINGDOWN/bis/e3_budget_wall_review/B3_V2_CLOSING_REVIEW.json](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_budget_wall_review/B3_V2_CLOSING_REVIEW.json>) — `a3eed1bb9b948e890923638d8eed0255191f95227a68332e85cf4f67d006d550` (9521 B).

## Contabilidade contínua por etapa

Intervalos não sobrepostos entre recibos, incluindo revisão e orquestração. Não são CPU-h nem duração isolada do algoritmo. Os custos de campanhas dentro desses intervalos estão nas entregas; somá-los outra vez duplicaria consumo. Em E3.3 e TEST, novas execuções científicas tiveram duração0 porque não foram lançadas; documentação continua consumindo parede.

| Etapa | Início UTC | Fim UTC | Parede h |
|---|---|---|---:|
| E0/E1, preparo e revisão B1 | 2026-09-22T19:06:33.802143+00:00 | 2026-09-22T20:04:21.233353+00:00 | 0.963175 |
| E2/E4/E5, registro e revisão B2 | 2026-09-22T20:04:21.233353+00:00 | 2026-09-22T21:57:59.392122+00:00 | 1.893933 |
| E3.1/E3.2, Kerr, piloto, diagnóstico e orçamento | 2026-09-22T21:57:59.392122+00:00 | 2026-09-22T23:15:57.517462+00:00 | 1.299479 |
| Paredes E3.3/TEST, E6/E7 e integração final | 2026-09-22T23:15:57.517462+00:00 | 2026-09-23T00:02:47.394343+00:00 | 0.780521 |
