[REAL/OPEN] Revisão incremental **estática**, sem executar campanha, célula, waveform, PE, conversão ou download. Não encerra a ordem nem constitui autorização de execução. Originais do principal, código E7 e pins E7 não foram alterados. Complementa MAIN_CODE_REVIEW.md; não o sobrescreve.

## Estado exato revisado

Snapshot de bytes: `MAIN_CODE_REVIEW_SNAPSHOT_002.json`, SHA256 **634a61c7a1156a43a6fda0d12be17be44a09ad91cce5e8f39218f3c572cde6dd**. Cada entrada contém bytes em base64, tamanho e SHA calculado **sobre a mesma leitura binária**. Inclui dependências e draft. Esse é o estado do parecer, não o eventual arquivo vivo posterior.

| Arquivo | SHA256 no snapshot |
|---|---|
| null_runner.py | 1b6bf00beced255d45ac642de5209d32440e486f8a3af469e92a47c58fe1c561 |
| fetch_registered.py | 0147ce0917bbf72c69509b984c8a11ee1a80f57a74d569ffcc8db279e48049f6 |
| injection_design.py | 3761d680b45d7726945cfcf9c4020465cc42316010a7916516a826a590652e2c |
| null_campaign.py | c2324f55061214e17f0be8ccaec0914ec14a0a6409313c5675093f2816fbf213 |
| remnant_conversion.py | 641451837ba636cd05eea34bdcc439917a20877d6a9f2d132cca8b32d48fff3f |
| E2_REMNANT_BRIDGE_INPUT.json | d7b3fd879a97cbc8ceabd360c8ac01482c012c5b6243228123729c4a1603671d |

`null_campaign.py` mudou durante a consulta inicial. O primeiro estado observado **não** tinha captura de TimeoutExpired; o snapshot acima **já a tem**. Foi relido diretamente do snapshot. Não atribuo ao estado final a ausência de tratamento de timeout do estado anterior.

## Alterações verificadas favoravelmente

**null_runner:** regex de identificador antes de compor paths; N inteiro entre 2 e 1.000.000; população não vazia; predição None recusada; finitude/sigma positivo e covariância continuam conferidos em projected_components. Escrita delegada a publish_new, que usa arquivo pending exclusivo, flush/fsync, conferência de tamanho e hard link sem sobrescrever. O limite de 25 MB permanece. A interpretação estatística não mudou: alvo fixo ceil(N90 E0), catálogo balanceado, nuisance local INPUT; não é N90 físico/calibrado após nuisance.

**Injeção:** chegada em cada detector deve estar no intervalo sem taper; `analysis_time_contract` é transmitido ao gerador pSEOB; distância após escala de SNR deve ficar estritamente no prior de recuperação. As condições falham por exceção, sem alargar prior depois do resultado. XPHM continua GR-only, sem substituição de envelope por deformação pSEOB. Essas melhorias têm função distinta da exclusão do evento real, discutida abaixo.

**Downloader:** timeout calculado com margem de orçamento, checagens entre leituras e antes de promover bytes/recibo; publicação atômica do recibo. Carregamento dinâmico continua subordinado à guarda E2/E3.2, sem URL arbitrária por CLI. Isso melhora a falha visível e a custódia do recibo; não resolve por si só completude do download ou identificação da alocação no recibo.

## null_campaign.py — coordenação das 25 células

Leitura estática favorável ao fluxo sequencial: checked_registration antes de enumerar células; ordenação fixa das chaves registradas; uso de sys.executable e `-B`; threads numéricas limitadas a um; nenhuma chamada com shell; uma subprocess.run bloqueante por célula; guarda reexecutada pelo null_runner. O próprio novo coordenador precisa entrar em own_code_tree_sha256 na consolidação: o guard compara a árvore inteira, não só o runner antigo.

Recusa campanha já concluída e células anteriormente tentadas, incluindo FAILURE; não refaz silenciosamente os controles. Registra hashes de resultado/log, confere parent registration, especificação da célula e número de draws. Não converte nulos sintéticos em significância física. No snapshot, as 25 células são as do draft 001 já contado na revisão anterior; o coordenador executa todas as chaves congeladas, não escolhe leitura favorita.

**Timeout atualizado:** captura TimeoutExpired, preserva stdout/stderr parcial em log TIMEOUT, marca falha e chega ao recibo agregado. A implementação padrão subprocess.run mata/aguarda seu próprio processo filho ao expirar; nenhum processo alheio é selecionado pelo código.

**P2 residual de custódia de falhas:** time_guard fora do try, erro de leitura/JSON/pin de recibo e erro ao criar log ainda levantam exceção antes do recibo agregado. A falha fica visível e os resultados anteriores permanecem, mas pode faltar RESULT_E2_NULL_CAMPAIGN.json com estado parcial, custo e célula em curso. Recomendo um try/except/finally externo que tente publicar um recibo de falha não sobrescritível com os recibos já coletados, mantendo/reerguendo a exceção. Não usar esse endurecimento como licença para retry automático. A correção não muda o modelo científico nem exige executar controles nesta revisão.

## Achados anteriores ainda abertos nos bytes capturados

1. **P1 — janela de análise da injeção versus evento real:** injection_design ainda verifica apenas igualdade dos arquivos e chegada dentro da região sem taper. Não compara a janela [start,start+duration) com o intervalo protegido de event_GPS. pe_runner.validate_config no snapshot também não faz essa comparação. strain_io só separa a janela da PSD; não exclui sinal real da janela de injeção. Logo a fixture da revisão anterior identifica uma classe de entrada ainda não bloqueada. Corrigir antes das injeções de recuperação; isso não impede revisar separadamente os nulos sintéticos.
2. **P2 — completude do download:** fetch ainda não lê/compara Content-Length nem um tamanho exato registrado. Só teto, não-vazio e checksum opcional. Um timeout não distingue EOF truncado. O achado anterior permanece aberto quando não há checksum primário. Não executei novamente a fixture de HTTP nesta etapa.
3. **P2 — identidade E3.2 no recibo:** main ainda chama fetch(reg,digest,key,recipes), descartando `_allocation_sha256` da view. O recibo ainda não inclui digest da alocação, configuração ou receita. O carregamento é verificado, mas o recibo não liga sozinho os bytes à versão da autorização dinâmica que os pediu.
4. **P2 — limite de parede do download:** socket timeout limita espera de I/O, não demonstra duração total máxima de uma chamada read(1 MiB) sob resposta que envia pequenos blocos continuamente. O comentário de que toda leitura é estritamente limitada pelo timeout é forte demais. Para garantia rígida das 40 h, usar limite externo de parede para o processo próprio ou leitura/controle com deadline efetivo; manter a margem atual como defesa adicional. Nenhum ensaio de rede foi feito.

## Metadado do remanescente e configuração pendente

O SHA medido do novo E2_REMNANT_BRIDGE_INPUT.json é **d7b3fd879a97cbc8ceabd360c8ac01482c012c5b6243228123729c4a1603671d**. Pin ECSV interno **cb54925ee712fb46f9b820d6057a4cdc0c34414a4b4e3ca5c76aba98baa5e59d** e os seis parâmetros cosmológicos conferem com a fixture de duas linhas da revisão anterior. Trata-se de Planck18 externo INPUT e ajuste GR alinhado, não derivação TGL de H0 nem remanescente inspiral-only medido independentemente. O código de conversão tem o mesmo hash já testado; não o reexecutei.

Incluir esse JSON e sua transposição exata para remnant_conversion_INPUT no registro/configuração. O código ainda não compara automaticamente os parâmetros ao conteúdo do ECSV: a revisão pinada dos valores concretos é a evidência disponível. Se o principal alterar parâmetros, a igualdade ao nome Planck18 deve ser verificada de novo ou a variante deve receber nome próprio.

No snapshot, o pe_runner ainda emite remnant/redshift OPEN e a integração A permanece pendente. O draft 001 continua sendo o retrato antigo de 4 s; o builder capturado contém 8 s. O principal informou que a configuração numérica final pode passar a **16 s**. Esta revisão **não fixa 8 s**, não executa o builder e não certifica suporte temporal da waveform. O estado final de duração/start/priors/analysis_time_contract deve ser consolidado e pinado junto com o teste finito de A antes do freeze.

O censo 9 publicados / 14 não localizados no escopo e os quatro quality holds continuam sujeitos à incorporação descrita no parecer anterior; este adendo não reclassifica eventos. Seeds, contagem, matrizes C1 e seleção científica não foram alteradas. Nenhuma execução foi autorizada ou iniciada por este revisor.
