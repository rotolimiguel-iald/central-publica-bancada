# Complemento R2 — implantação e manifesto

[REAL — revisão estática dos bytes atuais] Os quatro ajustes residuais da REVIEW_DEPLOY_MANIFEST_R1 foram conferidos no diff e estão atendidos: manifesto lido uma vez; backup usa current já conferido; contrato NU e extrações copiados dos mesmos buffers validados; rollback confere old_sha256 antes de declarar restored. A identidade programa/selo usa os mesmos buffers e confere a versão. Os pinos exatos estão em DEPLOY_REVIEW_RECEIPT_R2.json e os scripts foram preservados em DEPLOY_REVIEW_SNAPSHOT_R2.

Nenhum novo defeito material foi encontrado nessa revisão limitada. Não foi executado --apply, nem o builder; o rollback completo não foi ensaiado. As sondas anteriores exercitaram só contenção de paths e helper atomic com falha simulada de replace, preservando o original e limpando temporário. Os destinos de implantação permanecem confinados à Bancada; um.py, selo, kernel e fontes externas absolutas são somente lidos.

A regressão após as rotas de neutrinos permaneceu 31/31, EXIT 0, em CORE_RECEIPT_R3_neutrino_routes.json, com bytes estáveis durante o teste. Sem dados observados.

[DECLARADO — coordenação] O reinício do legado será registrado como sem carga observada, não como ociosidade formalmente demonstrada, após conferir estado, processo exato, CPU/GPU e filhos; a recarga e os testes vivos são da coordenação. A distinção responde à limitação do legado sem endpoint de atividades. Esta revisão não afirma que a parada, implantação ou reconexão MCP já aconteceram. Nenhum gate mudou.
