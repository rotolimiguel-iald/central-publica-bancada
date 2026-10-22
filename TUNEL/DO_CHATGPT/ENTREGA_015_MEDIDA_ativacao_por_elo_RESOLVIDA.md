[REAL — integração corrigida em cópia versionada; nenhuma alteração científica]

# Resolução ao lado da MEDIDA de ativação

Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a
Data: 2026-09-26T15:34:41.316900+00:00
supersedes: ENTREGA_015_MEDIDA_ativacao_por_elo.md; sha256: 84873ec957d49c9fba3459c2c4d714a91884d245033e77b9b2ac73ff5559b806

Correção de escopo da nota anterior: T03-C e T03(xi) já autorizam reparar as sondas/guarda e registrar uma subemenda. Foi feito em árvore irmã NOVA `bis/e2_code_v1_1_2`, alterando somente `check_activation_v1_1`. A identidade da testemunha determina o recibo imutável daquele elo; recibos antigos continuam intactos. V1.1.1 não é retroativamente declarada executável.

Registro atual V1.1.2: a02c4224b0c832a85e8eaef736197754235aa573290760bb2307ad6ac4c713b4. Guarda: 4dd3005ed34b30a2736c0bb96a9a23d0776ecbe791c9ba463fe632d0a8036a83. Recibo: d93a03ccb7f29da1739e0067665cb24b4f62afc231bf4b743348df8f3e14a845. A execução real de checked_registration em /opt/lal_env passou pelas verificações e recusou somente o relógio R7 ainda ausente, como esperado. A cadeia do orçamento foi verificada.

Controles: 53 executados nesta correção; 109 anteriores transportados por identidade de código/AST, NÃO reexecutados. Evidência: `ORDEM_013_RINGDOWN/bis/015/activation_v2/REGISTERED_RESULT.json`, sha256 aa33411d85b05f40f235ab3a6fd34fbb975ca544ab8dce19388a7effeb168a32.

Máquina pesada 0h; chamadas externas novas 0; custo da coordenação não informado. Nenhuma semente/dado cego aberto, nenhum canônico ou gate modificado. Próximo: R7 imediatamente antes dos nulos T03.
