# Template final 013BIS — leitura documental delimitada

[REAL — revisão estática] **REDACTION_CORRECTIONS_REQUIRED_BEFORE_FINAL.** Fonte: `refeito/prepare_final_report_013bis.py`, lida e analisada por AST, nunca importada/executada. Esta revisão não gera o rascunho final, não aprova o relatório final nem altera o closing E6 V3. O operador condicionou a futura execução a E6/E7 concluídos e revisão final integral; esse gate permanece.

[INPUT] Escopo: afirmações globais e semântica da tabela, comparadas a B1/B2/MA e à estrutura do E0 pinado. Sem posterior de teste, seed/offset, strain, PE, MC ou novo cálculo científico. As entregas B1/B2/MA foram lidas como documentação histórica não cega; nenhuma alegação de cegueira absoluta. Não revisados aqui os resultados novos Kerr/E7, diagnósticos nativos, orçamento real, integridade final ou futuros recibos de paredes.

## TF1 — separar a referência individual da população e marcar os estatutos

[REAL] Linhas 100–112: a introdução nomeia GWTC5_31 como referência, mas δ/piso vêm de `systematic_conditions/*/delta_GW250114` e `floor5_INPUT`; N90/informação vêm dos targets da população31, e correção/σ vem da C4 herdada dessa população. São referências distintas. O código preserva as dez leituras e os três conjuntos de chaves conferem; a ambiguidade é da apresentação, não prova de número incorreto.

[INPUT — correção para a publicação] Trocar o cabeçalho por “δτ220 previsto na referência GW250114” e “Piso INPUT |δτ220(ref)|/5”. Identificar os outros campos como “N90 condicional — mistura GWTC5_31”, “Informação-alvo Σ1/σ²(δτ220) — mistura31” e “Correção/σ C4 histórica — 31; não cega”. Acrescentar no texto: “As primeiras duas colunas usam a referência individual; não são o efeito médio nem a condição física medida da população31.” Não inferir N90 da divisão entre colunas de referências diferentes.

Marcar o piso /5 e a sensibilidade /15 como INPUT; transportar os estatutos de cada leitura ou fazer remissão explícita e inequívoca ao quadro C1/E6 que os contém. Qualificar a frase R-GLOBAL: “Sob a partição INPUT R-GLOBAL, o efeito local previsto é zero.” Isso preserva a hipótese da leitura em vez de afirmá-la como fato universal. Piso zero não paga o gate. Os cenários N90 continuam condicionais e não demonstram poder real.

## TF2 — não chamar a parede sem dados de TESTE executado

[REAL] Linha 96 contém “Estado sem dados executado/registrado sob E2”. B1/B2 e a rota de parede distinguem registro/avaliação procedural de experimento observacional. O texto pode ser lido como campanha de teste executada, apesar de o próprio relatório declarar PE cega NÃO PAGA.

[INPUT — substituição curta] “Parede e estado AWAITING_DATA registrados sob E2; TESTE observacional não executado.” Manter na coluna não paga: nenhum evento novo admitido/descego; nenhuma calibração física ou significância 5σ paga. Uma validação procedural do estado não deve ser contada como PE/experimento executado. O futuro recibo real sustentará a afirmação documental, sem hora de execução científica inventada.

## TF3 — delimitar negativas globais e seus suportes

[REAL] Linhas 75, 128, 143 e 146 contêm afirmações de história global: sem parada, sem download/novo posterior/descegamento, nenhuma divulgação de seed/offset e nenhuma edição de memória/Atlas/canônico/site/espelho/publicação. MA sustenta uma declaração com escopo da Parte A e B2 descreve custódia procedural local. Esses documentos não demonstram ausência universal de ações em outras tarefas/casas, nem cobrem automaticamente todo o intervalo posterior.

[INPUT — correção para o final] Delimitar: “No escopo desta bancada ORDEM013BIS e conforme os recibos/manifestações de integridade e exposição vinculados, ...”. Onde houver somente declaração operacional, usar DECLARADO e indicar seu responsável/intervalo; não promover hash de arquivo a prova de ausência global. Para “sem parada de marco”, conservar a regra da ordem ou a declaração operacional, sem sugerir prova de execução ininterrupta. Nenhuma necessidade de varrer outras casas ou ler segredos para satisfazer este parecer.

As negativas podem ser mantidas quando o ato final efetivamente as sustentar nesse escopo; esta revisão não afirma que sejam falsas. O arquivo recebido por `--integrity-receipt` é atualmente incluído/hashiado, mas seu conteúdo não é interpretado para provar essas frases. A revisão final integral, já prevista pelo operador, deve fazer a ligação claim→recibo. Não se pede nova arquitetura ou execução antecipada.

## Formulações sustentadas e limites mantidos

[REAL — comparação documental] B1/B2/MA sustentam: nuisance/covariância como INPUT condicional; calibração física, eficiência/normalização e c(SNR) não pagos; C4 INCONCLUSIVE_SYSTEMATICS não cega; C5 parede e C6 diagnóstico anterior ao gate; N90 condicional não garante poder com sistemática real; Fisher440 de fonte fixa não mede degenerescência de fonte livre; densidades220/440 do mesmo evento não são evidências independentes; LRT nulo sintético/informação de variância não pagam transferência browniana ou σsys. A redação atual conserva essas distinções.

O texto sobre t5 e limite superior com zero excedências é compatível com o escopo documental já revisado. Não foi refeita integração/MC e não se reabre ciência. Preservar no pacote final a revisão/addendum numérico dos intervalos dos nulos já entregue; a frase “medidos e revisados” não equivale a declarar que todos os checks históricos passaram.

Os “14 sem publicação encontrada no escopo”, dez sem hold e quatro com hold mantêm linguagem limitada; não converter isso em ausência universal de publicação ou admissão automática. As afirmações específicas de E7 e Kerr são pendentes da revisão final dos respectivos recibos; não foram validadas por esta leitura B1/B2/MA. Plots/quadros de projeção devem herdar rótulos condicionais, sem significância física com gate vermelho. NOT_FALSIFIED nunca significa CONFIRMED.

[REAL] A checagem estrutural da tabela encontrou 10 systematic_conditions, 10 targets GWTC5_31 e 10 entradas históricas GWTC5_31, com as mesmas chaves de leituras e ordem de exibição preservada. Não foi calculada/renderizada a tabela nem impresso valor científico novo.

## Pins e encerramento

| Fonte lida | SHA256 medido |
|---|---|
| `ORDEM_013_RINGDOWN/refeito/prepare_final_report_013bis.py` | `a2cebccb5b138bce4ef6f3957ee5bf5613c9cf277a4884a84f42bbb7603d82b7` |
| `TUNEL/DO_CHATGPT/ENTREGA_013BIS_B1_portao_e_nuisance.md` | `c33f4f36eedc9060859ae38bdd3f9993b59fada62cee489e8c964975b792a3e8` |
| `TUNEL/DO_CHATGPT/ENTREGA_013BIS_B2_registro_e_440.md` | `06345093b5fca7b250f9360f66cf40bfc0becbd54b6e4cce4505f828f96fa8d7` |
| `TUNEL/DO_CHATGPT/ENTREGA_013BIS_MA_fechamento.md` | `1e1b31226ddbc211f7a751c4add712d4deeeb99939d5b74c87b45e6d3d3fcbf4` |
| `ORDEM_013_RINGDOWN/PORTAO_DA_AMPLIACAO_V1.json` | `710028a7d2af7b649511afe369d88462d2add95c5fecbb1fb03c517fc91fe8a0` |

Emitido em 2026-09-22T23:09:02.308724+00:00. As três correções são de escopo/redação; produtor permanece intocado. Revisão de custo/orçamento, se solicitada, será separada.
