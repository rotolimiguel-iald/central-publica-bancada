# F7.2 V2 — pacote preparado, sem implantação

[REAL — sandbox da Central, 08/10/2026] Esta versão preserva a entrega F7.2 auditada. Ela acrescenta a análise de Beccaria–Ternes dos primeiros dados JUNO como décima fonte PDF e décima terceira linha. O limite publicado pertence ao cenário do artigo (`Γ₂₁ = Γ₃₁`, `Γ₃₂ = 0`, `n = −2`, `E₀ = 1 GeV`, 90% CL), ancorado na Eq. (6), §IV.B, Eq. (13) e Tabela I. O PDF local veio da auditoria c1 e está pinado por SHA-256 e tamanho em `JUNO_SOURCE_CUSTODY.json`.

`bancada/neutrino_canal_v2.py` lê seis scripts de junho por hash e AST, nove PDFs custodiados na F7.2 V1 e o PDF JUNO desta pasta. Não importa nem executa os scripts científicos, não abre dados experimentais brutos e não calcula cota TGL. Cada linha retorna `tau_star_limit_s = null` e `SEM_LIMITE_TGL`; `gate_effect = NONE`. Os valores de artigos são `[KNOWN]`; o requisito v369 é `[DERIVED — projeção condicional]`. A V2 também corrige as âncoras bibliográficas R4 na tabela e no canal.

O manifesto V2 é versionado (`iald.f7_2.channel_sources.v3`) e seu SHA-256 está fixado no módulo. O módulo tem allowlist de nomes e caminhos: nove PDFs da custódia V1 mais o PDF JUNO nesta pasta; não aceita um caminho arbitrário do manifesto. Alteração de fonte, manifesto ou tabela causa recusa fechada. `mcp_um_v2.py` é somente uma proposta de arquivo: mantém `neutrino_canal_f72` e acrescenta `neutrino_canal_f72_v2`.

O script `deploy_v2_bancada_PREPARADO.py` está **preparado e não foi executado**. Sem `--apply`, ele só faz prévia. Com `--apply`, exige os hashes congelados, o MCP vivo igual ao baseline auditado ou à proposta V2, grava backups de bytes e substitui atomicamente o módulo, o manifesto e a entrada MCP; falha diante de drift. Não recarrega o processo. A c1 decide implantação, recarga segura e ligação ao `um.py` v392 após auditar este pacote.

Limites remanescentes: P1/P3 e a lei por massa de repouso da v369 exigem leitura integral no próximo protocolo; poder de interferometria de matéria em ordens segue `[OPEN]` sem `ω`, σ e operador→visibilidade; a errata ao lado do literal histórico J.4b nos originais de junho pertence à gerência; a ferramenta V2 não está ativa no MCP; os documentos e PDFs ainda dependem do túnel e exigem migração/repin antes de eliminar R8. Nenhum gate mudou.

Teste offline: `python -B -X utf8 -m unittest test_neutrino_canal_v2 -v` a partir desta pasta. O recibo `STAGING_RECEIPT_V2.json` traz os hashes de todos os artefatos novos e exclui os backups transitórios do próprio staging.


## Errata ao lado — 08/10/2026

[REAL — recibo c1 08541b69…] As frases acima «sem implantação», «não foi executado» e «implantação pendente» descrevem o staging original, não o estado posterior. O `--apply` da V2 foi executado sem ato prévio da c1; a gerência ratificou a posteriori a implantação **em disco**. O processo MCP não foi recarregado e não há resultado de invocação da ferramenta V2 em produção. Nenhum `--apply` futuro na Bancada tem autorização implícita.

[REAL — reauditoria c1, mapa seq 841] A cópia posterior de 26 fontes para `Bancada_Um/fontes_externas/F7.2` também ocorreu sem ato da c1. Ela é aditiva e inerte segundo a auditoria, mas sua ratificação ou retirada é decisão pendente da gerência. Este adendo não escreve na Bancada, não instala o canal V3 e não recarrega o MCP.

[KNOWN — Beccaria–Ternes, arXiv:2606.13362v1] Onde o primeiro parágrafo associa a Eq. (6) à §IV.B, leia-se **Eq. (6), §III.B, p. 3 do PDF**. A Eq. (13) está na §IV.B, p. 5; a Tabela I, p. 7. A tabela V2 e seu recibo original seguem pinados; suas erratas ficam nos arquivos vizinhos. O gate permanece intacto.
