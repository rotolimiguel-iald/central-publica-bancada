# Kerr V3 — fechamento independente do delta documental

[REAL — hashes e três provas finitas do caminho; OPEN — execução E3.1]

2026-09-22T21:44:45.657508+00:00

**PAGO no escopo do delta de custódia V3. Nenhum novo bloqueante.** Foram 67 verificações documentais/finítas, sem repetir ciência. `MANIFEST_v3.json`: `3b327c742e5634dbd9220d6e7e725fbe94ebc7a89fa6f117aa2aa6f5261aee7e`.

Os nove fontes Kerr atuais conferem com V2 e V3. MANIFEST.json/V2 permanecem preservados. O único pin preexistente alterado é registration_guard.py: `d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9` → `3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7`. Conferi contra o snapshot anterior: exatamente uma substituição literal de E2_REVIEW_APPLICATION_V1.json por E2_REVIEW_APPLICATION_V2.json; nenhum outro byte mudou.

Além desse repin, V3 acrescenta três pins documentais: recibo da guarda, nota V3 e manifesto V2. Os campos históricos herdados do manifesto continuam descrevendo etapas anteriores; não são novas execuções. Todos os pins do mapa V3 conferiram. O seletor aceita MANIFEST_v3.json; controller/runner conservam o transporte do hash autorizado já revisado.

Três controles próprios sob optimize=1: caminho V1 e V3 recusados antes de qualquer leitura; caminho V2 alcança a primeira leitura, interrompida deliberadamente pelo fixture. Isso não executa ativação. Os40 controles de A tiveram recibo/proveniência conferidos, sem rerun e sem serem promovidos a controles independentes.

A autorização futura do principal deverá indicar `manifest_filename: MANIFEST_v3.json` e o hash acima. Nenhuma autorização/ativação foi criada. Este fechamento não audita ACL nativa, selagem candidate003, sua cronologia ou a conclusão de B2/F0-stop. Nenhuma fonte congelada, produção ou manifesto foi editado pelo revisor.

**PAGO:** preparação científica/contratual no recorte já auditado e atualização documental V3. **NÃO PAGO:** execução, custo físico medido, convergência/posterior e aceitação E3.1. **OPEN:** identidade GWOSC/C00_AR, PSDs da release e versão executável; identidade não demonstrada não é prova de inequivalência física. A declaração de reprodução equivalente continua não sustentada.

N1/N2 permanecem qualificações obrigatórias nas saídas conforme decisão do principal; nenhum fonte foi modificado para resolvê-las. Execução somente pelo principal após E2/B2/F0-stop e autorização própria.

## Orquestrador externo — revisão estática separada

`refeito/activate_kerr_013bis.py`, SHA256 `c0b8682629e2e91edd8d3ae9a2e40fd38bdc2dd1f2c440309775374e948eaf2d`: somente lido/AST, não executado. Confere checked_registration, caminhos locais, hashes fornecidos, F0 com after_processes vazio sob o mesmo registro e hash da entrega B2. Não cria timeout externo concorrente; o controller continua responsável por prazo/cleanup. Retorno zero vira EXECUTION_COMPLETED_REVIEW_PENDING, com aviso explícito de que variantes/convergência ainda devem ser examinadas. A semântica de contador após a guarda está qualificada. Esses pontos estão corretos no alcance estático.

**ORCH-R1 [P2 — vínculo do GO automático pendente]:** o script hasheia o parecer, mas não lê seu conteúdo nem compara o manifesto nele auditado com o escolhido. Um parecer anterior ou que não feche bloqueantes passa pelos mesmos checks se seus bytes/hash forem fornecidos corretamente. Correção exata: aceitar o recibo independente JSON, carregar estritamente e exigir manifest_filename/manifest_sha256 iguais ao selecionado, status de fechamento em allowlist explícita e blocking_findings vazio, antes de publicar autorização. MD pode continuar pinado como narrativa. No estado atual, o pareamento depende da decisão manual do principal; não chamar o script de validador automático desse GO. Este achado é do orquestrador novo, não reabre a ciência ou o repin V3.

**ORCH-N1 [P3 — recibo de falha]:** se log.open falhar sem criar o arquivo, sha(log) incondicional impede gravar o recibo externo. Usar hash nulo quando ausente e preservar error_type evita mascarar a causa. Não é falso aceite de posterior; é lacuna de registro da tentativa.

Recibo: MANIFEST_V3_INDEPENDENT_RECEIPT.json, SHA256 `eda685870b4c77f66e0c15e6645fc0b85cba45f4bb2253389b05462b0ca0f827`. Script: verify_manifest_v3.py. Tempo documental 0.043253s. Nenhuma waveform física, valor de strain ou PE.
