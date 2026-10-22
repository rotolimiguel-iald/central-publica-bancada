# Adaptadores documentais E3.2 → E3.3 → TEST

[INPUT] Autorização do operador: preparar o helper nesta árvore; após a ativação real do orçamento, construir somente o rascunho E3.2 para revisão de R. E3.3/TEST exigem GO posterior. E6 permanece sem autorização. Este pacote não executa ciência, não lê posterior/strain/seeds e não lança jobs.

`wall_stage_adapter.py` usa somente biblioteca padrão. `prepare` publica uma declaração imutável `ADAPTER_REVIEW_REQUEST.json`, explicitamente **UNREVIEWED_NOT_E6_RECEIPT**. `finalize` só vincula revisão independente aceita, com hash exato do pedido, artefato, bindings, predecessor e cronologia. Quem constrói não aprova. Todas as saídas ficam em `candidates/<run_id>` nesta árvore; publicação exclusiva, sem substituição, limite de 25.000.000 bytes por arquivo. Uma falha preserva o que já foi escrito; retomada exige novo identificador, não reparação de recibos antigos.

## Etapas e significado temporal

- E3.2: orçamento efetivamente registrado como artefato e evidência, bindings vazios, predecessor = recibo de ativação E2. O tipo `ALLOCATION_REGISTERED` usa `/registered_utc` nos três campos temporais do contrato. São três referências ao **mesmo evento documental pontual**; não representam duração de PE/injeção nem alegam execução. O GO posterior autoriza a emissão do adaptador, não retroage. Outcome COMPLETED/PARTIAL refere-se ao registro documental; calibração continua não paga.
- E3.3: `NO_EXECUTION`, bindings vazios, outcome PARTIAL/BLOCKED/UNAVAILABLE. Fonte nova registra somente o instante real de documentação da parede, motivo e hash da evidência E3.2. Nenhum início/fim científico é inventado.
- TEST: `NO_EXECUTION`, com 180 bindings = três rotas × dez leituras × seis grupos. Todos têm `test_data_present=false`, `AWAITING_DATA` e campos físicos null. Precisa do adaptador E3.3 revisado da mesma alocação. Não precisa duplicar 180 cenários vazios em E3.3.

O campo `issued_utc` é a data real da primeira declaração, preservada no pedido imutável revisado. A revisão vem depois. `FINALIZATION_RECEIPT.json` registra separadamente a data real em que a referência à revisão foi vinculada. Não se afirma que os bytes finais com essa referência existiam antes da revisão. R/B deve revisar expressamente esta correspondência temporal antes de usar o adaptador em E6.

## Interface para o principal

`prepare --execute --authorization <JSON> --authorization-sha256 <SHA>` recebe:

| Campo | Conteúdo |
|---|---|
| status | AUTHORIZED_WALL_STAGE_CANDIDATE_AFTER_BUDGET |
| stage | E3.2, E3.3 ou TEST |
| helper_sha256 | hash do helper congelado |
| issued_utc | instante real da autorização/registro documental do GO, com fuso |
| run_id | identificador novo em minúsculas |
| outcome, reason | resultado documental e motivo explícito |
| registration, E2_activation | pins E2 e recibo real |
| budget, budget_witness | orçamento no slot ativo e testemunho de máquina real |
| predecessor | E2 activation / E3.2 revisado / E3.3 revisado, respectivamente |
| E6_contract, E0 | pins fornecidos em PREPARATION_PINS.json |
| principal_notes | lista não vazia de notas pinadas; B3 sozinho basta em E3.3/TEST. E3.2 pode usar o recibo real de ativação do orçamento |
| test_posterior_available, new_PE_allowed, new_injections_allowed | todos false |
| cost_per_converged_PE | null |

Pins são exatamente `{path: relativo a Chatgpt, sha256: hash dos bytes}`. O helper verifica o vínculo E2, o slot ativo, testemunho, tempos e arquivo de jobs dinâmicos vazio. Esse vazio não remove o piloto estático do E2 e não autoriza relançá-lo. O helper nunca chama o launcher ou altera guard/orçamento.

`finalize --execute --request <pedido> --request-sha256 <SHA> --review <revisão> --review-sha256 <SHA>` exige a revisão independente `ACCEPTED_FOR_E6_MAPPING`, sem findings bloqueantes, com todos os campos do contrato E6 e `request_sha256`. Revalida pins da alocação/fontes; não produz uma revisão por conta própria. O principal precisa autorizar esta vinculação; construção do rascunho não significa aprovação.

## Semântica e limites

Os pisos E0 são copiados, sem recálculo, apenas para TAU220, como INPUT histórico. TAU440 não recebe piso de 220; rota IV usa unidades de largura/variância de df220, sem trocar desvio padrão por variância. `sigma_c_calibrated`, `sigma_sys_df`, jitter, significância física e lnB ficam null; todas as flags científicas pagas ficam false. Revisão documental não paga calibração física. Contagens zero autorizadas de novos jobs não viram custo zero de posterior convergido.

Esta parede específica não contém teste. O contrato E6 congelado continua impondo `INCONCLUSIVE_SYSTEMATICS` para **dados presentes** com gate red/OPEN e aceita `NOT_FALSIFIED_UNDERPOWERED` quando a validade foi paga sem exigir poder ≥5. O helper não modifica essas regras, produtores E4/E7 ou versões E6.

Fixtures são exclusivamente fictícias, sob `fixtures_*`; não são ativações nem revisões reais. Exercitam E3.2 → E3.3 → TEST, cronologia e mapeamento com funções AST do E6 congelado, além de recusas de pins, datas, valores físicos e substituição. Não executam `main`, `activate` ou baselines E6. Rodada anterior e snapshots preservados. Resultados e hashes constam do manifesto.

[OPEN] O hash prova custódia, não a veracidade física de uma nota. A revisão independente dos adaptadores reais continua necessária. Este pacote não declara E6 concluído, não autoriza extração E7 e não finaliza a ordem.
