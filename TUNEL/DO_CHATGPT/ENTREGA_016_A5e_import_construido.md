[REAL — compilação isolada; DERIVED — import condicional no tipo original]
# A5.e — Propagador construído ligado ao import H3
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

**PAGO no escopo condicional.** `construct_import` produz o tipo original
`ContratoImportH3 W R N T h2`, reutilizando `construct_null_solution` e os
corpos originais de `responseOf`, `areaDensity_responseOf` e
`H3_of_null_solution`. `same_horizon` fecha por `rfl`.

As hipóteses são explícitas: H2 do par; G positivo fixo; classe A de estados
unitários, incluindo o vácuo e estável por translações; continuidade e
integrabilidade absoluta das caudas de ordens zero e um do tensor T.
Há ainda o elo modular, energia não trivial e tela plana **para todo H2
admissível do mesmo par**, porque o campo `produce` tem esse quantificador.
Não reduzimos esse campo ao H2 que indexa o import.

**Controle do vazio:** provado que U(nullDir)=1 exclui H2 fiel e, portanto,
exclui o par dependente (h2, import indexado por h2). Uma função que recebe
esse H2 impossível continua definível, mas não fornece o índice.
O ataque `(Classical.choice ⟨_⟩)` recompilado contra o contrato original
foi rejeitado exatamente no argumento H2 ausente: rc 1, `synthesize placeholder`.
Não foi um erro de import/dependência.

**MEDIDA preservada:** esta sonda é uma generalização do ataque da v3.1.
Não recompilamos os dois exemplos completos legado/brinquedo de
`ProbeVacuousImportV31`: a cadeia integral deles segue a limitação de memória
registrada em A1. O teorema geral cobre a hipótese que ambos utilizam;
nesta rodada não afirmamos ter revalidado suas instanciações completas.

Três módulos finais rc0, 9 entradas auditadas somente com o trio permitido;
cinco tentativas totais, incluindo o negativo esperado. Uma tentativa falhou
por nome não qualificado `solderMetric4`; a versão seguinte acrescentou apenas
`TGLExt.` e passou. Fontes/logs/recibos estão no manifesto.
Máquina: 110.708896s parede e 110.609375s CPU; bancada não exclusiva.
Custos remotos explícitos acumulados US$0.2662637382, incompletos, sem nova chamada.

**Não move o gate:** não construímos H2 físico, não escolhemos tensor T0,
não descarregamos o elo modular para esse tensor. A construção é um termo
condicional do contrato exato, não um pagamento incondicional do par físico.
Próximo: A6, equação da verdade, reutilizando a pedra de 46 teoremas.

Manifesto `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A5\constructed_import_manifest.json`
SHA256 `820daf87f3596277c9608afdf756e5fbd721fd550c459fc67a908390c7e309bf`.
