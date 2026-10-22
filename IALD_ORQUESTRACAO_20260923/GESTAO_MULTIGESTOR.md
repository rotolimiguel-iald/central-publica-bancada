# Gestão independente do modelo — IALD

O núcleo de coordenação é a fila local persistente da IALD. Codex, Claude e um
controlador da IALD nativa podem ler o mesmo estado e propor a próxima ação.
Quem estiver no comando não se torna autoridade para criar missão: a admissão
continua pelo pedido do operador, com `request_id`, restrições, casa e fontes.

`manager_cli.py` recebe **um JSON por stdin** e devolve JSON. Operações:

| Operação | Efeito |
|---|---|
| `status` | Estado, conexões, memória e coordenações recentes; sem chamada a modelo. |
| `next` | Próximo trabalho da fila única; sem chamada a modelo. |
| `list` / `get` | Lista ou recupera o `job_id` existente. |
| `preview_job` | Roteamento determinístico do pedido existente, sem execução. |
| `act` | Transição de um `job_id` existente pela máquina de estados; `execute` pode enviar uma chamada autorizada. |

Exemplo de leitura: `{"operation":"preview_job","job_id":"UUID-EXISTENTE"}`.
O transporte de entrada de novos pedidos permanece `transport_cli.py` ou o
painel administrativo, onde a autorização do operador é verificada. Nunca
converter texto de modelo em uma nova submissão. Um gestor deve reler `get`
após cada transição e recuperar um envio incerto antes de qualquer repetição.

O seletor local (`policy.py` + `matrix.py`) já funciona sem Jev. Seu peso é uma
política de agendamento, não uma probabilidade calibrada de acerto. Jev é uma
ponte opcional e permanece desativado sem acesso explícito. A IALD nativa/Qwen
já consta como executor local; para torná-la gestora, um controlador separado
deve pedir ao Qwen uma proposta **estruturada** apenas para um `job_id`
existente, validar essa proposta contra `preview_job` e o estado persistente,
então chamar `act`. Qwen não deve alterar diretamente SQLite, iniciar outro
worker/heartbeat ou mudar `required_provider`.

Antes de promover Qwen a gestor automático, executar um ensaio em sombra com
pedidos já concluídos, comparando escolha, abstenções, falhas e violações de
restrição com a política atual. A resposta do modelo não é prova de execução.
O gestor ativo da fila atual continua o heartbeat Codex; este contrato permite
trocar o controlador sem migrar a fila ou seus IDs, mas não instala um novo
agendador nem afirma que Qwen já gerencia autonomamente.
