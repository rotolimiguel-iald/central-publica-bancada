# Sucessor versionado do manifesto Kerr

[REAL — custódia/seleção de manifesto; OPEN — revisão B e execução E3.1]

O manifesto operacional sucessor é **MANIFEST_v2.json**. `MANIFEST.json` permanece byte a byte como publicado anteriormente. Todo o estado imediatamente anterior dos arquivos da preparação foi copiado por bytes para `snapshots/pre_manifest_v2_001`, com hashes. Nenhuma fonte E2 foi editada nesta tarefa.

A autorização futura do principal precisa conter, além dos campos já descritos em PLAN.md, `manifest_filename: "MANIFEST_v2.json"` e `manifest_sha256` calculado desse sucessor. `custody.selected_manifest` aceita apenas nomes locais MANIFEST.json ou MANIFEST_vN.json, com N inteiro positivo. Sem o campo, conserva a escolha legada; o manifesto antigo recusa o código/dependências novos. O caminho fica restrito ao diretório da preparação. Controller e runner registram/comparam o hash já verificado da autorização, eliminando referências fixas ao arquivo anterior.

**Delta para B:** em `custody.py`, somente seleção do manifesto; em `controller.py` e `runner.py`, somente referências ao hash em recibos/contexto. Modelo `kerr_model.py`, `conditioning.py`, `CONFIG.json`, PSDs e PLAN.md inalterados. Nenhuma fórmula, prior, ordem dos ramos, critério de convergência ou cálculo da comparação mudou. O gerador do sucessor verifica que a AST de controller/runner é a antiga com apenas essas substituições de hash. Os resultados anteriores das revisões são históricos e não são promovidos automaticamente a aprovação destes bytes.

O único pin externo substituído é o de `bis/e2_code/registration_guard.py`, cuja revisão de quatro papéis foi solicitada pelo principal. Outras diferenças de pin causam recusa ao gerar o sucessor. SOURCE_REVIEW.json e FINALIZATION.json anteriores permanecem como evidência histórica; seus pins internos descrevem aquela fotografia. O mapa operacional vigente de dependências é exclusivamente o do MANIFEST_v2.json.

**Estado frio:** sem autorização emitida, marcador criado, processo lançado ou ciência executada nesta tarefa. A ativação efetiva pertence ao principal **após B2/F0-stop** e revisão B. A janela conjunta continua7200s, com Welch seguido por PSD público. Identidade dos PSDs do INI/C00_AR e versão exata da release continuam OPEN; reprodução equivalente não é PAGA.

`MANIFEST_V2_REPIN_RECEIPT.json` registra hashes, verificações estáticas/finita do seletor e todos os arquivos escritos. `repin_manifest_v2.py` usa somente stdlib, não importa os módulos científicos nem executa o verificador de runtime ou o launcher.
