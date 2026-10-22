# Manifesto Kerr v3 — somente repin da guarda de aplicação V2

[REAL — delta de custódia; OPEN — revisão B e execução E3.1]

Sucessor: `MANIFEST_v3.json`. `MANIFEST.json` e `MANIFEST_v2.json` permanecem intactos. A autorização futura deve indicar `manifest_filename: "MANIFEST_v3.json"` e seu hash calculado.

A única dependência de execução cujo conteúdo mudou é `bis/e2_code/registration_guard.py`: o caminho fixo da aplicação passou de E2_REVIEW_APPLICATION_V1.json para E2_REVIEW_APPLICATION_V2.json. O teste confirma igualdade byte a byte com o snapshot anterior após essa única substituição literal; 40 controles finitos passaram, incluindo recusa de V1 e V3. Nenhuma outra regra de ativação mudou.

Para B: os nove arquivos Python Kerr têm exatamente os mesmos hashes do MANIFEST_v2.json. Modelo, condicionamento, priors, configuração, PSDs, critérios de convergência, comparação e envelope de7200s permanecem inalterados. Esta revisão não aprova o novo helper Win32 do selador: ele pertence ao principal/revisor. Não se executou selador, política PowerShell, PE, strain ou waveform. A falha anterior de ExecutionPolicy permanece preservada pelo principal; não houve tentativa de contorná-la.

Estado frio: nenhuma autorização ou ativação emitida por este delta. Execução somente pelo principal após revisão B e B2/F0-stop. Equivalência com PSDs externos/C00_AR e versão exata da release continua OPEN; não há reprodução equivalente PAGA.

Recibos: `bis/e2_review/ACTIVATION_APP_V2_PATH_RECEIPT.json` e `MANIFEST_V3_REPIN_RECEIPT.json`; este último contém os hashes finais e a lista de arquivos escritos no complemento.
