# Revisão independente futura da tentativa Kerr V2

[INPUT] Preparação autorizada; execução científica pertence ao agente principal. A revisão documental do delta não aceita posterior. Este protocolo não inicia processos, lê strain, gera ondas ou abre amostras. A preparação do piloto permanece separada.

## Entrada e ordem obrigatória

1. Aguardar o recibo completo `bis/E3_KERR_LAUNCH_V2.json`, fechado pelo ativador após retorno do controlador. Ausência é WAITING_COMPLETION_RECEIPT; não inferir conclusão por presença de HDF5, NPZ, log, COMPARISON ou retorno zero isolado. Não consultar amostras parciais.
2. Fotografar hashes atuais dos fontes, CONFIG, MANIFEST, revisão do delta, autorização V2, recibo externo, log, ENVELOPE, COST, CONTEXT, CLAIM, CONTROLLER, CONDITIONING e CONVERGENCE. Conferir vínculos manifest/authorizer/review/registration e parent_authorization/parent_cost/original_envelope. Comparar aos pins da preparação. Não reabrir strain; pins herdados não são nova medição independente dos bytes de strain.
3. Conferir `original_absolute_deadline`, validade da autorização e stop do ENVELOPE contra o ENVELOPE original. CONTEXT.stop deve respeitar ambos o stop original e o limite de 1800 s da nova tentativa. O runner reserva 15 s para encerramento. Horários de finalização e custo incluem cleanup; qualquer ultrapassagem precisa ser discriminada, sem mudar o deadline. Preservar custo das duas tentativas, por variante e acumulado. 1800 s não é limite acumulado de ambas.
4. Exigir exatamente a variante public_psd nesta cópia, uma entrada em COST.runs igual ao CONTROLLER local, sem cutoff/falha e com group_absent=true. Receipt de cleanup é evidência documental, não um novo levantamento de processos. COST e os custos de runner/comparação têm escopos distintos; não somar componentes sobrepostos. Registrar wall, CPU de filhos, CPU de runner, overhead e chamadas sem inventar CPU ausente no receipt externo.
5. CONVERGENCE deve satisfazer os limiares fixados no CONFIG: estado antes de add_live, delta_logz menor que .1, ncall menor que 3 milhões, igualdade de ncall_reported, ESS>=100 e N>=1000, evidência e erro finitos. Nenhuma compensação de delta/N por ESS alto. Comparar também com terminal bruto do HDF5 e recomputar ESS das nested weights quando disponíveis, sem interpretar amostras do posterior antes de superar esta etapa. A história pre-live depende do hook pinado e do recibo, não é dedutível apenas das amostras finais. Arquivo bruto ausente ou esquema divergente fica OPEN; não presumir layout.
6. Contadores: sampler_ncall, chamadas ao likelihood e chamadas de setup são objetos distintos. O contador Kerr incrementa após a guarda de deadline; não mede entradas recusadas nessa guarda. Não aplicar automaticamente o contador R3 do PE a este likelihood. maxcall é nominal por iteração/lote, não teto exato global. Rejeição por maxcall permanece parcial mesmo com arquivo bruto gravado.

`post_result_metadata_gate.py` fornece apenas predicados puros sobre metadados e fixtures sintéticas. Sucesso significa METADATA_PREREQUISITE_ONLY: não executa custódia completa, não aceita ciência e não possui leitura automática de outputs. Seus testes não substituem as etapas acima.

## Somente após conclusão e verificação da convergência

Abrir NPZ pareado com allow_pickle=False, conferir SHA contra COMPARISON, oito chaves físicas exatas, vetores finitos de mesmo N, ordem de parâmetros e suporte dos priors. Confrontar com as oito colunas do posterior bruto do HDF5; verificar igualdade/ordem sem escolher amostras. Verificar campos e tipos reais antes de qualquer cálculo; não converter silenciosamente esquemas. Recalcular quantis 5/50/95, desvios ddof=1 e covariância Mf/af, faixa/prior e concentração em bordas. Os critérios do sampler são necessários, mas não certificam exploração de todos os modos com 512 live points.

Só então comparar Mf detector-frame e af à referência já pinada no CONFIG. Conferir bytes e cabeçalho da referência; documentar interpretação equal-weight e merge provenance OPEN. Recalcular resumo, diferença de medianas, sobreposição e KS descritivo. Razão por largura em quadratura não é z calibrado; não calcular significância, lnB entre famílias ou evidência independente do mesmo evento. Não inferir massas componentes, redshift, dtau livre ou rejeição/validação da TGL de uma calibração Kerr.

## Estatuto final e preservação

- Falha/timeout/partial: NO_ACCEPTED_POSTERIOR_ANALYSIS; diagnóstico de convergência/custo somente, campos de comparação científica null. Não abrir nem promover o posterior parcial e não lançar nova tentativa automaticamente.
- Pré-requisitos satisfeitos mas custódia/array não conferido: REVIEW_PENDING, nunca aceito por rc0.
- Revisão completa: calibração não-cega no escopo verificado, com limitações explícitas. GWOSC vs C00_AR, PSD público NRSur vs PSD da análise pyRing e versão exata da release não têm identidade demonstrada. Ausência de identidade demonstrada não é prova de inequivalência física. Welch previamente recusado continua resultado negativo; sua retirada desta tentativa não fecha robustez entre PSDs.
- Gravar somente novos artefatos em e3_pyring_review; preservar review do delta e todas as fontes/receipts antigos. Qualquer conclusão vinculada aos hashes efetivamente lidos. Sem nova ciência, PE, strain ou atualização de memória/canônico.
