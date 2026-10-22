# E3.2 — parecer independente do candidato e da ativação documental

**Candidato aprovado no escopo documental**, em `E3_WALL_BUDGET_CANDIDATE_REVIEW_v2.json`: 772 controles independentes, todos verdadeiros. SHA do candidato medido no recibo. Nenhum builder, helper do autor, PE, waveform, strain, bootstrap ou ajuste foi executado.

[REAL] Conferidos manifesto, cópias byte a byte e fontes atuais, árvore congelada E2, 14 eventos elegíveis com ausência de publicação limitada ao censo, quatro holds e dez sem hold. Cada SNR foi cruzado com a linha/versão do CSV e E2; pins dos pareceres de publicação foram conferidos. Isto não constitui nova pesquisa universal de publicação nem admissão de evento.

[DERIVED/INPUT] Recalculadas as 28 linhas de pesos dos ajustes 31/33, incluindo covariância completa dos coeficientes, intervalos condicionais, flags de extrapolação e somas separadas 10/4/14. `exp(-2mu)` é proxy; `exp(-2mu+2s²)` é expectativa lognormal com dispersão fixada. Os ajustes não são somados entre si. Não são informação realizada, likelihood física calibrada, poder medido ou ranking por custo/hora. Os três candidatos abaixo de 12,9 têm extrapolação declarada no ajuste31. As dez leituras conservam os limites operacionais nulos e exemplos de N não viram alocação.

[REAL] O prazo global original termina em **24/09/2026 11:06:33.802143 UTC**. A reserva final começa na preparação e termina em **23/09/2026 01:02:56.988802 UTC**; revisão e ativação consomem a mesma reserva. As 34,060226 horas devolvidas são saldo não alocado, não gasto. Os custos dos controladores são explicativos e não se somam outra vez ao relógio contínuo. Os recibos Kerr e piloto foram comparados diretamente. A tentativa IMR de cerca de 11 segundos não é custo por posterior convergido, que permanece `null`.

[INPUT] Zero novas PE/injeções/downloads/reparo é uma decisão admissível após a parede instrumental medida. As cinco alternativas estão presentes, cada uma com custo de programa qualificado desconhecido; não há impossibilidade global, aceitação de posterior parcial ou qualificação da recuperação IMR pelo Kerr. E3.3, cobertura, `sigma_c`, `sigma_sys` e teste físico continuam não pagos.

## Ativação

`E3_WALL_BUDGET_ACTIVATION_V2_CLOSING_REVIEW.json` aprova exclusivamente o ativador v2 pinado para esse candidato: 12 fixtures documentais em diretórios temporários próprios e 16 controles. Duplicatas, NaN, overflow, review futuro, alocação booleana, jobs alterados, prazo vencido e reserva além do limite são recusados antes de publicação. Saídas/pending preexistentes são preservadas. Não houve ativação real. O pin de revisão fornecido pelo principal é a âncora de confiança; o emissor não pode substituir a revisão independente por autoaprovação.

`E3_WALL_BUDGET_V2_WITNESS_CLOSING.json` acrescenta a conferência por regex das linhas únicas `allocation_sha256` e `registered_utc`. O SHA fresco confirmou que essas linhas já estavam nos bytes executados pelas fixtures do fechamento v2, apesar da leitura estática anterior.

Ressalva não bloqueante BW-N1: abertura ausente ou falha de publicação posterior pode deixar orçamento parcial sem testemunha/recibo completo. A abertura real existe e foi pinada. Uma publicação parcial deve ser registrada como falha e preservada; não basta a existência de `ORCAMENTO_40H.json` para afirmar conclusão. O contrato documental não revoga jobs estáticos nem muda o guard E2, e não autoriza relançar o piloto.

## Errata do revisor, preservada ao lado

O primeiro `E3_WALL_BUDGET_CANDIDATE_REVIEW.json` trazia `approved:false` por erro no meu teste: exigia igualdade com **todo** `test_candidates`, incluindo inelegíveis e metadados pendentes. O conjunto correto é o de `eligible is True` e `published_deformation_at_registration is False`; coincide exatamente com os 14 candidatos. Fonte e recibo v1 permanecem intactos. O v2 corrige apenas esse controle e o nome de saída; nenhum artefato de A foi modificado.
