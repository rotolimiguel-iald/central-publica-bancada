[REAL — lido por script em 24/09/2026 08:08 (−03); adendo da gerência à ORDEM 016; não altera a matemática, os alvos nem os tetos]

# ADENDO 016-001 — O TRANSPORTE DESASSISTIDO ENTRE AS IAs (autorizado pelo operador em 24/09/2026)

**CITA:** `ORDEM_016_a_gravidade_quantica_primeiro.md` (sha16 `c0614dbd8d9ba606`), §8.2 («Como nasce uma chamada externa») e §9.11-(h).

**O que mudou depois da publicação da ORDEM 016:** o operador autorizou em 24/09 o transporte desassistido entre as IAs, sem o clique intermediário (registro da frente do orquestrador: `Chatgpt\IALD_ORQUESTRACAO_20260923\TRANSPORTE_DESASSISTIDO.md` `cf67fb14e385d826`; `transport_cli.py` `8d4d18b095b6219f`; teste fim a fim `validation\unattended_roundtrip.json` `72d158599c4b24eb`). O MCP `iald-orchestrator` tem agora `iald_coordination_submit` e `iald_transport_next`.

**Correção ao lado da §8.2 e da §9.11-(h):** a frase «todo pedido nasce do botão do painel, por clique do operador» e a consequência «sem clique, só Lean local; o cético de outro provedor fica NÃO PAGO» ficam SUPERADAS. A bancada PODE submeter pedidos pelo `iald_coordination_submit` (ou pelo `transport_cli.py` equivalente), um por pergunta, com `request_id` próprio, **dentro de todas as regras da §8**: preview antes; a rota da tabela (MiMo primeiro; Kimi só após falha medida e como cético; IALD local para o mecânico; Física para sentido [INPUT/ONTO]; Claude, Codex-executor, Antigravity e Jev ZERO); os tetos (4 + 1 cético por lema; 40 por ramo; Kimi 8/dia; Física 3/dia; MiMo US$ 0,50 por ramo e US$ 10 na missão); o `LEDGER_016.jsonl` no ato; nada confidencial nem reservado a provedor externo; e-mail proibido.

**Custo que o operador pediu para não desperdiçar:** cada verificação do heartbeat consome uso do Codex; **não criar pedido sem alvo da árvore**, e nunca pedido só para manter a fila viva. Fila vazia não chama os outros provedores.

*Nada move o gate. PROVADA ≠ CONFIRMADA. NOT_FALSIFIED nunca é CONFIRMED.*
