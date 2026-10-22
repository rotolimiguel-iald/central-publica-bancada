---
name: iald-orquestrar
description: Use a fila única da IALD para coordenar as IAs integradas quando o operador pedir orquestração, seleção de executores ou acompanhamento de um pedido. Não acione provedores por mera menção à IALD.
---

# Orquestração IALD no Claude Code

Esta habilidade funciona no Claude Code local do VS Code por meio do servidor MCP de usuário `iald-orchestrator`. A base operacional é `C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923`. O worker existente do Codex é o único responsável pelas transições da fila; não crie outro worker, fila ou agendamento.

## Ao receber uma tarefa concreta do operador

1. Identifique a casa de origem, o objetivo e o material que pode sair para provedores. Consulte `iald_orchestration_status` e `iald_selection_preview`; status e prévia não chamam modelos. O conjunto de executores é dinâmico: disponibilizar todas as IAs não implica chamar todas nem prometer que cada conta está pronta.
2. Se a tarefa toca TGL/IALD, use também `tgl-atlas` para navegar o cânone. A memória científica comum é montada pelos adaptadores na execução, com recibo de geração, fontes e linhas. Não copie o Atlas nem presuma que ele foi instalado nos pesos de qualquer modelo.
3. Para cada unidade realmente autorizada, gere um UUID `request_id` e registre-o ANTES do envio em `BASE\state\session_requests\<request_id>.json`, com pedido permitido, casa de origem, data e identidade real da sessão se disponível. Use escrita temporária, verificação e substituição atômica; faça backup byte a byte de qualquer arquivo existente que for alterar. Recupere IDs anteriores da mesma unidade em vez de criar outros.
4. Envie uma vez com `iald_coordination_submit(prompt, request_id, execution_constraints)`; guarde o `job_id`. Restrições de executor são permitidas somente quando o contrato vigente da missão as aceitar. Em envio incerto, recupere a identidade pelo mesmo `request_id` e mesmo conteúdo, sem nova unidade. Acompanhe com `iald_coordination_get(job_id)`.
5. Informe o resultado apenas após estado terminal, separando resposta do executor `[DECLARADO]`, revisão local, eventual assistência ChatGPT/Física e evidência efetiva. Ação descrita por um modelo não prova que ocorreu no sistema.

## Limites e proteção

- Use o MCP para registrar e consultar. Não chame `iald_coordination_action` para disputar as transições com o worker existente, salvo recuperação expressamente autorizada após conferir seu estado e o guia `TRANSPORTE_DESASSISTIDO.md`.
- Pedidos `failed`/`cancelled` e chamadas incertas não são repetidos; executor obrigatório não é substituído automaticamente. MiMo requer processo novo auditado por unidade quando aplicável.
- Não envie corpos jurídicos, credenciais, `.env`, `iald_stack_v7.py`, `iald_psion_state.json` ou acervos confidenciais a provedores remotos. Preserve as casas e a autorização da missão.
- ChatGPT/Física é assistência opcional; sua disponibilidade não bloqueia a fila. O worker controla os limites de Work e a proveniência da preparação e síntese.
- Se o servidor MCP não aparecer numa sessão já aberta do VS Code, reabra a sessão do Claude Code para carregar a configuração de usuário. Consulte `claude mcp get iald-orchestrator` no ambiente Windows normal para verificar a conexão. Não recrie o servidor.
