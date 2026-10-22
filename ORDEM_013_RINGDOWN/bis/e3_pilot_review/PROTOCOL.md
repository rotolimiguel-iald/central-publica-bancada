# Preparação da revisão independente — GW250114_PILOT

[REAL — contratos/fontes e testes de metadados; INPUT — protocolo; OPEN — resultado futuro]

Ownership exclusivo: bis/e3_pilot_review. Calibração NÃO CEGA GW250114, pSEOBNRv4HM_PA alinhado; Kerr primeiro. Nenhum launcher, PE, waveform, strain ou posterior foi executado/aberto. A informação B2/F0 recebida não foi reconstituída neste protocolo. Pareceres Kerr/orquestrador e fontes permanecem imutáveis.

## Ativação e sequência

`review_future_pilot.py` sem flags apenas informa PREPARED_INACTIVE, sem abrir arquivos de resultado. O caminho permitido vem do job registrado: cache/E3_PSEOB_PILOT_V1. Não aceita evento cego ou diretório arbitrário. O contrato pinado é uma fotografia; se fonte/configuração mudar, recusa e pede atualização explícita ao lado, sem inventar transporte.

Comando **futuro, não executado**, somente quando o principal informar o resultado concluído:

```text
/opt/lal_env/bin/python -B review_future_pilot.py --activate-existing-result-review --output-name PILOT_REVIEW_001.json
```

O output fica nesta pasta, exige nome novo e nunca modifica produtos. Sem CONTROLLER.json: AWAITING, sem abrir amostras. Timeout, parcial, erro, cleanup não confirmado ou convergência ausente/inválida: registra custo/status disponível e deixa posterior_summary/comparison nulos. Arquivo bruto incidental, checkpoint ou pickle não resgata uma rodada recusada. Preservar falhas; nunca fabricar cadeia, reponderar parcial ou anunciar posterior aceito porque existe HDF5. Nenhum unpickle/import de resultado Bilby.

## Antes de qualquer comparação científica

1. Conferir registro/job/configuração, código pinado e status não cego; controlador terminado com retorno0, grupo ausente e sem FAILURE/ANALYST_STATUS parcial. Retorno0 é necessário, não suficiente.
2. PRIVATE_CONVERGENCE: captura before_add_live verdadeira, delta_logz finito abaixo do dlogz registrado, ncall abaixo de maxcall, contador reportado igual, ESS≥mínimo e N≥mínimo. Plateau, maxcall, baixo ESS/N ou evidência numérica inválida recusam. O snapshot foi capturado pelo adaptador antes da adição de live points. O resultado final HDF5 corrobora esse snapshot; não permite reconstruir a cronologia sozinho. Não renomear delta_logz final como evidência pré-live independente.
3. Reconciliar R3: entradas=retornos+exceções, fases cumulativas monótonas e snapshot final igual ao custo. sampler_ncall, likelihood_calls e source_calls são grandezas distintas. maxcall pode ultrapassar em lote, e uma rodada no limite já recusa. Segundos/fonte usam source_calls. Parede da tarefa, CPU pai, CPU dos filhos e soma de parede por invocação entre workers não se somam como se fossem uma métrica única. Custos finais após remanescente não podem retroceder. Relatar overruns como questão aberta, não esconder em médias.
4. Só então ler ANALYST_OUTPUT, HDF5 bruto cujo hash foi publicado e18 colunas pareadas (11 físicas+4deformações+3derivadas). Recomputar ESS dos pesos nested, conferir as15 colunas nativas contra JSON e o N. Rejeitar links HDF5 externos/virtuais, schema ausente, não finitos ou mistura de linhas. HDF5 ausente/fallback pickle fica OPEN/recusa; não carregar objetos executáveis. O ramo completo deste leitor ainda não foi executado.
5. Conferir priors e mass_ratio, remanescente pareado/sem thinning, domínio e recibo de conversão. Mf é detector-frame derivado pelo fit GR alinhado; spin e redshift condicionais, com Planck18 INPUT. Não são medidas independentes do remanescente. Ler PSD_receipts futuramente e conferir intervalo, banda, flags e escala com o contrato antes da aceitação científica humana; o script não relê strain ou recalcula PSD.

## Comparação publicada, depois dos gates

Relatar medianas, quantis5/95 e std ddof1; delta de medianas e sobreposição90% são descritivos. Não converter automaticamente intervalo90% em sigma gaussiana. Alvo dtau documental da ORDEM: −0,013 [−0,103;+0,087], com caminho/hash/contexto em CONTRACT. Não tratá-lo como estatística calculada agora.

A referência de amostras é o HDF5 GW250114 pSEOB já existente, com hash herdado concordante de C4_SCHEMA e extraction_receipt; nenhum byte de amostra foi aberto agora. REFERENCE_CONTRACT fixa grupo pSEOBNRv5PHM/posterior_samples e cinco campos. No futuro, verificar hash, ler apenas campos necessários e conferir Mf_detector=Mf_source×(1+z) linha a linha (tolerâncias numéricas declaradas); se falhar, comparação Mf fica OPEN. Não multiplicar medianas independentes por1+z; não substituir por Kerr220. Comparar dtau220, Mf detector e spin mantendo os pares e a limitação de merging/pesos iguais. Outras convenções de remnant/evolução ou diferenças de schema exigem revisão, não adivinhação.

Família própria alinhada pSEOBNRv4HM_PA versus publicada precessante pSEOBNRv5PHM, priors amplos INPUT: diferença residual não identifica sozinha causa física. Mesmo evento/dado, sem evidência independente, sem lnB calculado pela proximidade de posteriores, sem z calibrado e sem seleção populacional paga. O script sempre mantém scientific_acceptance=false, mesmo quando consistências numéricas passam; multimodalidade/cobertura e gate sistemático requerem revisão. O grau em que o piloto reproduz o publicado deve ser declarado, nunca inferido só do nome do evento.

## Entregáveis e estado

CONTRACT.json e REFERENCE_CONTRACT.json: entradas/pins. FIELD_MAP.json: nomes esperados JSON/HDF5. REVIEW_SCHEMA.json: saída. BILBY_HDF5_SERIALIZATION_SOURCE.json: fontes de serialização instaladas lidas sem importar Bilby, hashes conferidos contra runtime. Foram22 controles sintéticos de gates sob -O; modo default inativo também conferido. Nenhuma campanha ou benchmark. A rota de HDF5 e comparação só poderá ser validada sobre resultado existente na ativação futura; ausência de validação dessa rota fica explícita.

**PAGO:** preparação documental/código e gates finitos de metadados. **NÃO PAGO:** revisão científica do piloto, convergência real, custo medido e comparação de posterior. Não houve alteração no orquestrador/Kerr/E2/E4. E4 executado e revisão W ficam fora deste trabalho.
