# Parecer independente de prontidão v389

**Aceite limitado: integridade estática e delta científico coerentes; nenhuma instalação ou execução autorizada por este parecer.**

A v389 está disponível como artefato local selado. Os bytes do programa, selo, resultados e demais arquivos vinculados permaneceram estáveis durante a conferência (2026-10-06T19:48:28.972660+00:00 → 2026-10-06T19:48:36.472226+00:00). A ordem direta anterior do operador autoriza preparar a atualização local quando disponível; a ressalva genérica de ratificar/vetar no §7 do handoff não cria, por si, novo bloqueio. Commit/push continuam atos separados e reservados.

## Identidade conferida

| Artefato | Bytes | SHA256 |
|---|---:|---|
| um.py | 33823528 | 193b1e9b30c3ba7f8ad56a2a35eb6ff21d9b9c241d397b0e497fe1ebd5c7284a |
| um_absoluto_selo.json | 103932 | ef4d8bf9f0e4e58d3ceebe86ee2c18c138921c8a7b09bdde41497555084b65a6 |
| um_absoluto.json | 4984523 | d00507744723c2895610173f31a5646b4b70f1570c8fb22293d6a9e1a5a1a95e |
| tgl_kernel_proof_manifest.json | 1478163 | 0a1a3691c0e84c5214c8ebcca612e41e0c175a836a8bdef404c31e3133d0b09b |

Foram aprovadas **2618 verificações locais de integridade** — majoritariamente confinamento de caminhos e comparação de hashes, não 2618 experimentos científicos. Os 14 pins no selo conferem. Também conferem 65 membros do arquivo da cadeia, os três arquivos do exame/errata e o vínculo de versão/data/hash entre resultado, selo e manifesto formal.

O resultado_hash foi confrontado entre selo e resultados. Não foi recalculado o hash do world anterior à comparação externa: input_manifest incorpora entradas externas, fora deste escopo. A integridade byte a byte dos arquivos que transportam esse registro foi verificada.

## Contagens: medidas versus registradas

- **[REAL — AST/bytes]** Os 1.214 arquivos embutidos são idênticos aos da v388. Os 1.215 arquivos do manifesto formal materializados em disco conferem com os hashes, inclusive o suplemento identificado. O agregado formal é cb8ad48d338f46f9d18afb4da4566262f8c69131400ee78cc69faa30ef7ffe7d, igual na v388/v389.
- **[REAL — cardinalidade documental]** O axiom_report contém 10256 entradas, idênticas às da v388. Isso não significa 10256 novos teoremas nem nova compilação.
- **[DECLARADO na rodada; lido/confrontado aqui]** A escada registra 6.154/6.154 limpos; stdout registra RITO_RC=0 e FAIL_CLOSED_SELFTEST_PASSED. Não reexecutei Lean, conferidor ou programa. “Rodada COMPLETA” refere-se à camada rite_checkpoints desligada; o pilar quântico registra separadamente modo REUSE. Não afirmar que todo subcálculo foi refeito.
- **[REAL — contagem independente de literais AST]** Ledger: 1.025 caminhos únicos; 156 arquivos TGLExt fora do ledger; todos esses156 em TGLExt/O16. A errata 1.015/166 fica ao lado.
- **[REAL — contagem de registros]** Exame v388: 189 achados, com3 CORRIGIR,186 NOTA e0 BLOQUEIA. O conferidor existente declara9 critérios “deve mudar” e10 “não pode mudar”, todos satisfeitos; esta auditoria não executou esse conferidor.

## Delta científico v388 → v389

Nenhuma fonte Lean embutida mudou. Não há pedra ou teorema novo na v389. A pedra v388 continua com seu alcance próprio; não promover as correções textuais a avanço empírico.

O core passou de377 para378 tópicos pela adição de text_label_errata_v389. Nenhum dos vereditos preexistentes mudou. α, β, ω(I), gate, bandeiras formais verdadeiras e axiom_report são idênticos. Os 216 caminhos de diferença no JSON se dividem em206 tempos de execução, timestamp/proveniência da rodada, registro novo, rótulo/errata e a diferença de memória descrita abaixo; detalhes completos em DELTA_CORE.json.

A fonte tem duas funções novas (_ledger_counts_v389 e text_label_errata_v389) e seis funções modificadas. O diff independente está em DELTA_FONTE.diff. As mudanças específicas são:

1. Rótulo CLOCK_TORSION_CONFIRMED_ON_PHYSICAL_NET → CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET. O nome antigo fica em seals_errata_v389 como registro; cálculos da rede permanecem.
2. Introdução PT/EN atualizada para o arco v384→v389.
3. Resumo/Parte B adotam o axioma POSTO, preservando a decisão do operador e a errata anterior. A correção “fronteira mínima” remove o segundo uso indevido de axioma.
4. Seção histórica v387 remete explicitamente à abertura v388.
5. Parte C passa a contar caminhos únicos/arquivos fora do ledger;12 substituições textuais foram conferidas no próprio código.
6. Registro fail-closed da errata por hashes: arquivo de exame ausente/adulterado produz NOT_SEALED_THIS_RUN, e exceção vira NOT_RECORDED_THIS_RUN ao lado do gate.

A marca beta_runs_bounded_below_v388.memory_file.on_disk_matches mudou deTrue paraFalse. **Não foi encoberta ou reescrita.** Conferi que o backup exato tem o hash pinado e o arquivo atual começa integralmente por esses bytes e só cresceu. É o acréscimo documental da cadeia, não uma mudança da fórmula, β0, hipóteses ou resultado físico.

## Requisitos concretos para atualizar

Não identifiquei bloqueador de integridade que exija repetir a rodada. A etapa seguinte é preparar e revisar os snapshots/manifestos v389 dos destinos, preservando v388 para rollback.

O novo registrador usa três caminhos absolutos locais de EXAME/ERRATA (um.py:193932–193944). Distribuição que pretenda executar o programa precisa preservar ou resolver explicitamente essa dependência pelo contrato autorizado; copiar só um.py para outra máquina não comprova disponibilidade desses arquivos. A carga documental do app não deve importar/executar esse registrador.

O pacote v389 deve preservar LOCAL_SEALED e não atribuir publicação/commit remoto ainda não conferidos. D-H/Fase9, governança das especificações e μ continuam com seus estatutos; esta errata não resolve essas decisões nem libera d72/P3.

O prefixo e os dois JSONs Sonnet v388 continuam selados, sem alteração. **Nenhuma contagem v388 certifica uma montagem v389**. Contagens novas, mudança de modelo público, ativação ou instalação não ocorreram nesta auditoria. A estabilidade foi medida durante esta janela; revalidar por CAS/hash imediatamente antes de qualquer cópia operacional.

## Escopo e referências

Handoff lido: HANDOFF_CUSTODIA_CONJUNTA_v383_v389.md. Skill tgl-atlas e adendo v389 do Atlas consultados; não foram escritas memórias compartilhadas. Nenhum AGENTS.md foi encontrado nos seis caminhos ascendentes explicitamente consultados; aplicam-se as instruções globais fornecidas e o escopo delegado.

AUDITORIA_V389.json reúne todos os pins, diferenças e verificações; não transforma o relatório de compilação da origem numa compilação realizada aqui. Estatutos, hipóteses e NOT_FALSIFIED ≠ CONFIRMED permanecem.
