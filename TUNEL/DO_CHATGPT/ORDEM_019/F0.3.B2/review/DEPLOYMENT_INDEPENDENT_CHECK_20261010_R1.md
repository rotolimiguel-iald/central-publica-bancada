# Verificação independente da implantação — 10/10/2026

[REAL] Resultado: PASS. Intervalo: 2026-10-10T09:40:18.351151+00:00 a 2026-10-10T09:40:23.429731+00:00.

- 71 arquivos instalados: bytes iguais ao candidato e ao recibo; backups conferidos quando havia versão anterior.
- Manifesto: 32 entradas de código e 67 fontes conferidas por tamanho e SHA-256; nenhuma fonte foi importada ou analisada numericamente.
- Programa v391: `8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6`; selo: `95061f18c7102248ebd00c9414f1ef0dadcf08cefc1bec00bf046d778b38070a`; vínculo selo→programa conferido.
- Manifesto instalado: `54fc9e27e4599c49990adb9587a45a8858393f2d8f5d66ec3e022b8140757c1b`.
- GET /api/estado HTTP 200, pronta=True, erro=None; identidade carregada e proveniência do alpha coincidem com os bytes atuais.
- Processo 75052, socket 127.0.0.1:18777, início e comando conferidos. Atividades no instantâneo: {'idle': True, 'active': [], 'quiescing': False}.
- MCP: o recibo LIVE guarda uma sessão stdio nova, 28 ferramentas distintas e chamada sintética; o verificador inicia mcp_um.py instalado, inicializa a sessão e consulta a lista. Os 28 nomes coincidem com as declarações atuais por AST, sem importar o módulo nesta revisão.

## Limites

A sessão MCP registrada é nova; esta revisão não mede a reconexão de cada sessão antiga. Clientes ainda conectados à descoberta anterior precisam reconectar/atualizar sua lista. O runtime_verified=false do recibo de reinício é o retrato anterior à verificação LIVE, não o estado medido agora.

A igualdade de arquivos e a identidade do processo não são um despejo de todos os objetos em RAM. Não se alegou ociosidade formal do serviço anterior. Custódia não é admissão pelo operador. Nenhum fit, abertura de dado, reinício ou escrita na Bancada foi feito; não há sigma de natureza e o gate permanece intocado.

## Reaproveitamento

F0.3.B2 não consta do grafo Nós Vivo; a consulta F0.3 localizou a custódia v391 e a validação canônica existente. O relatório reutiliza DEPLOY_RECEIPT_R1, RESTART_RECEIPT_R1 e LIVE_VERIFICATION_R1 e acrescenta leitura independente dos bytes e do estado atual.

## Evidências

- JSON completo: `DEPLOYMENT_INDEPENDENT_CHECK_20261010_R1.json`.
- HTTP bruto: `DEPLOYMENT_INDEPENDENT_CHECK_20261010_R1_HTTP_STATE.json`.
- Processo/socket: `DEPLOYMENT_INDEPENDENT_CHECK_20261010_R1_PROCESS.json`.
