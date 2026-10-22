# Provedor e limites por pedido — ORDEM 016

24/09/2026. [REAL] Inspeção local, sem chamadas de modelos ou alteração de políticas.
Origem: tarefa `01a070fc-9484-7e13-a654-c6b5f61093a4`.

## Lacuna confirmada

- `iald_orchestrator/policy.py:route` aplica disponibilidade, classe, cobrança autorizada, contagem diária e orçamento estimado. Não recebe preferência/restrição persistente de provedor por pedido. `excluded` é diagnóstico de falha, não canal para impor preferência.
- `Runtime.submit(prompt, request_id, routing_prompt=None, start_worker=True)` não recebe orçamento financeiro nem provedor obrigatório. `routing_prompt` é texto para classificação, não comando de seleção. `_perform` recalcula a seleção antes de executar.
- `Coordination.create`, `transport_cli.py` e MCP `iald_coordination_submit` recebem somente pedido e UUID. Portanto texto como “use MiMo” não garante seleção MiMo.
- O adaptador MiMo possui `max_output`, mas o fluxo geral não o recebe por pedido. Os demais adaptadores não oferecem todos os mesmos controles. Custo estimado depois da chamada não é teto preventivo. Timeout não equivale a teto de tokens ou custo.
- Não existe estado de retenção por pedido no protocolo atual. Não chamar `submit` para uma missão que depende desses controles. Recibo local com UUID estável não é submissão; preservá-lo até haver mecanismo adequado. Nenhum pedido pendente contendo ORDEM 016 ou a identidade da sessão de origem foi localizado na consulta inicial; isso não descarta uma submissão posterior ou com outros identificadores.

## Ajuste mínimo proposto — NÃO IMPLEMENTADO

Acrescentar `execution_constraints` como JSON persistente em coordenação e execução, transportado por CLI/MCP até `route` e o adaptador. Exemplo de formato pretendido, NÃO aceito pelas ferramentas atuais:

```json
{
  "required_provider": "mimo",
  "max_output_tokens": 1024,
  "max_cost_usd": "0.02"
}
```

Os números acima são exemplos de schema, não orçamento autorizado para a ORDEM 016. A origem deve fornecer valor, unidade e alcance do teto real. Diferenciar limite de saída, total de tokens e valor financeiro. Esclarecer se o teto inclui a coordenação ChatGPT Work, cujo consumo não é medido/controlado pelo adaptador executor.

1. Validar e persistir as restrições antes de disponibilizar a unidade ao worker; incluí-las na comparação de idempotência. Mesmo UUID com restrições diferentes é conflito, nunca alteração silenciosa.
2. `required_provider` limita os candidatos por interseção com todos os filtros existentes. Não contornar indisponibilidade, cota, fonte ou cobrança; não manipular pesos, contagens ou falhas. Nunca substituir por outro provedor quando este for obrigatório.
3. Conferir capacidade do adaptador de impor cada limite. Se houver teto estrito que o caminho não consiga garantir, reter a unidade com motivo explícito. Em API paga, usar tabela de preços versionada, contagem de entrada suportada e reserva conservadora do custo máximo; falta de informação impede promessa de teto. Não estender automaticamente isso à cota das assinaturas.
4. Acrescentar retenção persistente (`awaiting_constraints`) e ação explícita de liberação, com controle de versão. O worker respeita a retenção antes da criação Work e novamente antes do executor. Preservar ordem e um único worker; não criar heartbeat por sessão.
5. MiMo para rascunho e Kimi para crítica são unidades distintas, cada uma com UUID e restrições próprias. A crítica só é registrada após a origem fornecer a falha efetivamente medida e o material permitido. Compilação e avaliação Lean permanecem com a origem.
6. Testar conflito de idempotência, provedor indisponível, limites não suportados, retomada, concorrência e rejeição antes de qualquer chamada externa. Só depois liberar unidades compatíveis.

## Antigravity

[REAL] O conector desta instalação foi corrigido e validado anteriormente nesta mesma tarefa como `ready`. Processo novo no ambiente real do usuário confirmou `ready` durante esta inspeção, sem modelo. Processo Python restrito do sandbox falhou na importação de PyYAML; isso é dependência do ambiente e não recusa da conta Google. Um processo que ainda apresenta `tools_filter_unavailable` pode estar com o módulo anterior carregado. Não retirar filtros nem editar recibos para forçar prontidão; conferir ambiente, versão e recibo existentes.
