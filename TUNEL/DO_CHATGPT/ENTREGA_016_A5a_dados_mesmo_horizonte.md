[REAL — compilação isolada; DERIVED condicional]
# A5.a — Dados do MESMO horizonte, por reaproveitamento

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

`HorizonDataReuse.lean` compilou rc0: 11 declarações,
10 theorem/lemma, somente propext/Classical.choice/Quot.sound.
Nove declarações do contrato v3.1 foram reutilizadas com corpo exato; duas composições
novas explicitam os campos e a temperatura no mesmo período. Não há tipo paralelo
de HorizonEquilibriumData nem novo habitante físico H3.

| Campo | Origem e estatuto |
|---|---|
| κ | `C.H2.kappa`, do mesmo W/R/N. Período P e fidelidade angular positivos ⇒ κ/(2π)=1/P; a faixa KMS regional/BW continua no contrato H2. |
| G | `C.G>0`, INPUT fixo antes de ψ; nenhum valor previsto. |
| dA | `windowArea (C.response ψ) x c d`, resposta do mesmo H3 e gerador nulo. |
| dS | `2π*windowCharge T ψ x c d`; leitura unilateral definida sobre o tensor T indexado. |
| dQ | `κ*windowCharge T ψ x c d`; Clausius segue das definições. |
| area_entropy | Derivada de `theta_is_expansion`, `raychaudhuri_einstein` e condição final θ(d)=0; T contínuo no gerador. Não deriva a lei de Einstein sem essa hipótese. |
| ligação mestre | `feeds_the_master` consome H1, o frame de C.H2 e estes dados, preservando suas hipóteses. |

**A5.a PAGO no escopo de discriminar e ligar os dados.** `toHorizonData` recebe
`ContratoH3`, não apenas H2. Construir a resposta/elo modular permanece em A5.b–e.
Não move gate nem altera kernel/originais.

Fonte SHA256 `b7b12a16b79197f62533979b6d52e151e6d63755a1f348d975ad11094ca721c8`; log `fea464ea3326cfbb508e9b200c82958f5627efd381121ae0c4a58535c08b229d`.
Manifesto `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A5\horizon_data_manifest.json` SHA256 `139cbb406737cfbec1a878dce081dc507d830c42348bff0d1f10bd9844ff4203`.
Máquina: 23.726310s parede, 23.734375s CPU na compilação válida.
Tentativa `_01`: falha de preparação por fonte inexistente; log preservado,
tempo não medido, não convertido em prova ou custo zero.
Custódia A4 independente recebida: conferência de hashes/recibos, sem nova execução ou revisão semântica.

**Orquestração:** 2 novas unidades Kimi (contorno/unicidade; matriz/covariância)
e 1 MiMo (rascunho Lean das integrais) preparadas e entregues ao coordenador.
Previews selecionaram os provedores exigidos com memória comum. Ainda aguardam
vaga na fila única; preparação não equivale a chamada nem resultado.
Estimativas explícitas acumuladas do ledger: US$0.1939854588; não fatura, assinaturas
e consumos não informados excluídos. Próximo: A5.b, propagador teleológico.
