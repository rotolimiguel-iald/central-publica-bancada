# Interface do serializador opcional — NÃO EXECUTADO

[INPUT de preparação] O principal poderá fornecer posteriormente um JSON inteiramente preenchido, sem placeholders, sob `bis/e3_allocation_prepare`. Não há tal JSON agora. O programa aceita um argumento posicional com esse caminho e só renderiza candidatos não publicados.

| Campo da proposta | Tipo / conteúdo |
|---|---|
| `schema_version` | `E3_ALLOCATION_PROPOSAL_V1` |
| `slug` | Nome novo seguro; identifica somente pasta de candidatos |
| `registration` | `{relative_to_Chatgpt, sha256}` do `RINGDOWN_5SIGMA_V1.json` efetivo |
| `pilot_controller` | Referência/pin de metadados `CONTROLLER.json` do piloto estático, não de PE cega |
| `pilot_convergence` | Referência/pin de `PRIVATE_CONVERGENCE.json` no mesmo diretório |
| `allocation_registered_utc` | UTC com timezone, futura emissão proposta ≥ E2 e ≤ hora da renderização; revalidar na publicação |
| `jobs_relative_to_Chatgpt` | Destino futuro novo dentro de B para jobsV2; **não é escrito** pelo serializador |
| `witness_relative_to_Chatgpt` | Destino futuro novo dentro de `TUNEL/DO_CHATGPT`; **não é escrito** |
| `jobs` | Configs completos já escolhidos pelo principal; mapa de novos nomes. Sem download neste gerador. |
| `ordered_job_names` | Cada nome de `jobs` exatamente uma vez; ordem decidida pelo principal |
| `global_reserve_seconds` | Positivo, escolhido e justificado pelo principal para trabalhos fora da fila, revisão/publicação; sem valor default |
| `decision_documentation` | Objeto com `five_alternatives`, `per_job_cost_and_information`, `unpaid`, `stopping_rules`, `selection_rationale`, `pilot_independent_review`, `reserve_rationale`; conteúdos revisados pelo principal, não certificados pelo serializador |

`five_alternatives` tem cinco entradas identificadas 1–5. `per_job_cost_and_information` tem exatamente os nomes dos jobs, distinguindo: custo medido usado como referência; projeção e hipóteses; teto de parede; informação esperada/fonte; valor null e motivo quando OPEN. `unpaid` inclui células inviáveis/não implementadas. `pilot_independent_review` deve localizar o parecer que conferiu custo/convergência/comparação, sem incluir amostras. Esses subdocumentos são preservados como declarações; o programa não os transforma em evidência independente.

O código lê apenas os metadados JSON expressamente referidos (cada arquivo ≤25 MB e dentro de Chatgpt): proposta, E2, orçamento indicado/pinado por E2, controlador, convergência. Não percorre caminhos de strain, posterior, segredo ou logs do registro. Recusa piloto parcial/não convergido nesta interface de projeção; custo parcial pode e deve ser reportado pelo principal como gasto, sem simular custo convergido. Não lê nem cria `AUTHORIZATION` e não certifica ativação E2.

No futuro produziria somente `JOBS_V2.CANDIDATE.json`, `ORCAMENTO_40H.CANDIDATE.json`, `CANDIDATE_RECEIPT.json` em pasta nova. O orçamento candidato carrega os cinco campos exatos do loader e metadados adicionais em `preparation`; `status: CANDIDATE_NOT_PUBLISHED` é documental e **não é um gate reconhecido pelo loader**. Não copiar/publicar os candidatos sem revisão, atualização do relógio e testemunha anterior ao teste. A ausência de publicação no local ativo e de testemunha, não o campo status, impede ativação nesta preparação.

Contabilização é soma serial dos tetos + reserva global ≤ tempo restante até deadline pinado no instante da renderização. O controlador desconta sua própria reserva de limpeza dentro do teto. O serializador não projeta velocidade a partir de workers, não faz agendamento paralelo e não aplica automaticamente nenhuma das cinco alternativas. A passagem do tempo pode invalidar a conta antes da publicação: reconferir.
