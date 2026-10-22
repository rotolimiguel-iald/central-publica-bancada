[REAL — compilação condicional; OPEN — faixa KMS regional do par construído]

# ORDEM 016 — MEDIDA A4k.4

UTC 2026-09-24T17:38:32.683776+00:00; abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

A tentativa reutilizou exatamente o corpo `KMSAt.rescale` da v3.1 e compôs
dois teoremas: KMS em rapidez a 2π e KMS em tempo de Killing a 2π/κ.
São **condicionais** a `H_regional_modular_strip` e
`H_modular_equals_geometric`. A reescala não produz a função analítica nem
suas duas bordas a partir do círculo. A energia positiva orbital previamente
compilada tampouco fornece, sozinha, a rede e o vácuo regional.

Comando: `lake env lean -j1 -M8192 -R A4 -o A4/KMSStripConditional.olean A4/KMSStripConditional.lean`
(caminhos absolutos/LEAN_PATH e dependências no recibo `kms_strip_01.json`).
rc=0; três declarações auditadas, somente trio; corpo reutilizado comparado.
Log SHA256 `18f027ce5cf38bb592f3e58c0fdac77ca3cb0f82ca3f78470cbce9a004ca5729`.
Fonte SHA256 `63fd714315d50e182061839e4ad66a1b4fd8ccff2dde80bf1e5d7b18f7414574`.
Tempo da tentativa 24.542s parede.

O TODO lido em `StandardSubspace.lean` confirma ausência dessa API pronta;
não é demonstração de impossibilidade. O controle `kms_with_incompatible_geometric_data`
do kernel é uma identidade KMS algébrica, não um contraexemplo a todo KMS analítico.
Não se declarou o teto de oito horas consumido: a ordem aceita MEDIDA com a
hipótese nomeada. A revisão Kimi permanece separada da evidência do compilador.
Nenhum gate/original alterado. Próximo ramo: A4k.5/6 (pagos nesta entrega), depois A-5.
