[REAL — errata temporal; sem mudança do plano]

O campo `created_utc` em `T10_B_PRE_REG.json` foi digitado manualmente como 10:37:00Z e está incorreto. O arquivo foi criado, segundo `CreationTimeUtc` do Windows, em 2026-09-27 10:31:36Z; `T10_B_RESULT.json` foi criado em 10:31:53Z. A precedência do registro sobre a medida é confirmada por esses metadados, não pelo campo inválido. Os dois arquivos originais são preservados. SHA256 do plano: `b013efebc6120a81062d81d4ed3db97fb60af73c99914308c0ca8969f21b3532`; SHA256 do resultado: `321ae1e1a6ee6b3d0bd61306f0effb696350426c498caf54cc14c341dd08457a` (ambos lidos por script).

Nenhum resultado foi mudado pela errata. A entrada de tempo digitada não deve ser usada como testemunha temporal.
