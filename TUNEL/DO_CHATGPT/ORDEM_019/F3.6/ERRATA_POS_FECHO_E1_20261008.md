# F3.6.E1 — errata ao lado após o fecho de C16

<!-- F36_E1_POS_FECHO_20261008 -->

**Data:** 08/10/2026. **Estatuto:** [REAL] cronologia e pins conferidos na auditoria c1; [DERIVED] desigualdade de Fisher; [OPEN] rotas posteriores. A F3.6 está **FECHADA pelo critério**, com `UNDERPOWERED_DO_NOT_OPEN_DATA` no Asimov sintético em Λ. Esta camada corrige a escrituração; não refaz o cálculo, não altera o FREEZE e não move o gate.

## História efetiva das três rodadas

| Hora local | Ocorrência auditada | σβ na base nua, covariância corrigida |
|---|---|---:|
| 03:23 | Primeira rodada WSL, núcleo β do FundoV3: dupla contagem do neutrino, integração a partir do futuro. O valor foi exibido antes do FREEZE. | 0,018020762 |
| 03:25:42 | Reescrita do núcleo β com ρ do CAMB, correção D1F-V1 e âncora hoje. | — |
| 03:26 | Segunda rodada WSL. A entalpia da energia escura foi fixada em zero no ponto Λ às 03:26:03, tornando A = B′ por construção. | 0,018043479 |
| 03:28 | Selftest dos passos sobre código anterior ao FREEZE; a auditoria verificou sua equivalência com o congelado, salvo uma frase de limitação. | intervalo 0,017900698–0,018362135 |
| 03:31:28 | Gravação do `FREEZE_PRE_RUN.json`, **depois** de duas rodadas e do selftest. | — |
| 03:32 | Terceira rodada; recibo congelado com números idênticos aos da segunda. | 0,018043479 |

**Correção [REAL]:** a frase do `PRE_REGISTRO_CONDICIONAL.md` «A primeira execução local deu σβ=0,01804348» é falsa. Esse valor é da **segunda** rodada. Após ver σ, a alteração física que afetou a conta foi a troca do núcleo β, incluindo sua âncora, com mudança de σ de aproximadamente **+0,13%**. A auditoria também registra a fixação da entalpia escura em zero no ponto Λ; A = B′ não é validação independente de dois modelos fora de Λ. O FREEZE antecede só o recibo da terceira rodada; não se deve chamá-lo de congelamento prévio à primeira execução.

## Escopo da parede medida

- **NÃO-CEGO [REAL]:** a inspeção expôs incidentalmente médias publicadas no literal `_dados_reais()` do pipeline V3 e em páginas consultadas. As médias observadas não foram processadas nem ajustadas; o Asimov usa previsão sintética no fiducial Λ. CAMB 2.0.4 no WSL foi usado nas três rodadas do `asimov_lambda.py` e em dois selftests. O relatório original já descrevia a exposição, mas omitia este rótulo.
- **Base nua [REAL]:** β de comparação saiu em runtime de `ALPHA_FINE_CODATA_2018 × √e`, dando 0,012031300400803142. A segunda/terceira rodada obteve σβ = 0,018043478961412125 = 1,4997β. O menor σ nos passos foi 0,017900698 > β. A reprodução independente sem CAMB encontrou σβ ≈ 0,018225 e correlações β–w₀ ≈ 0,694, β–wₐ ≈ −0,804. O controle mede falta de poder no DR1 para esta especificação; não cobra a teoria.
- **Base efetiva [REAL/DERIVED]:** na execução principal com mν=0,06 eV, σβ ficou aproximadamente **24,39** com a covariância corrigida e **29,24** com a V3. Está degenerada. Para Fisher positivo definido, marginalizar w₀,wₐ não pode reduzir a variância: **σ(β|w₀,wₐ) ≥ σ(β)**, na notação de controle da casa. A desigualdade do complemento de Schur não substitui os números medidos.
- **Escolha de covariância [REAL]:** D1F-01, D1F-03 e D1F-V1 de 28/09 entraram na **primária**; a covariância da V3 selada ficou como **sensibilidade**. Essa ordem inverte a recomendação da gerência, foi declarada e não altera o portão. D1F-04, a convenção de l_A, pertence à rota de reajuste da V3 (+0,96% em σβ na aferição da c1).

## Pendências separadas

- **Pergunta `call_92df0866…` (04:59:15Z):** RETIRADA da pauta da F3.6 por ter sido prematura. Esta é retirada **documental**: não há evidência de cancelamento técnico do cartão nem resposta do operador. A pendência X18 não é apagada por esta errata.
- **[OPEN]** CPL fora de Λ e CMB completo requerem rotas próprias. Controle 2 com DESI DR2 seria unidade nova, com levantamento e pré-registro próprios; σβ ≈ 0,94β é somente [CONJECTURE] do auditor com incertezas DR2 anotadas de memória, não medição nem autorização de abertura.
- Nenhum dado real do controle 2 foi aberto; nenhuma execução adicional é autorizada por este documento.

## Pins medidos nesta camada

| Artefato | SHA-256 |
|---|---|
| `MAPA_F36.json` | `7b3e8d20e5099252eb8a2207a14c55bb989ca8e39d759dff488629bd45c7d0d0` |
| `selar_f36.py` | `271e56053c751f003305d497fdafd14d22adaafb2aa08eafbc98cb6ede754dfc` |
| `ASIMOV_LAMBDA_SANDBOX/FREEZE_PRE_RUN.json` | `349e8acf4407bfe9ac9642cce3d0ec3ae340f192e5e953387c8e7b843e40aaa2` |
| `ASIMOV_LAMBDA_SANDBOX/BUILD_LOG.txt` | `668f57ba0f65e8b18e347580deb0dcd0ca69e5d3dde64c8a7e3173af200c4a05` |
| `ASIMOV_LAMBDA_SANDBOX/SELFTEST_LOG.txt` | `5e37a133b1b06f5ae8edbb8408347ffb7eb072abfc08dc8f785fdc063d91388a` |
| `AUDITORIA_F3_6_ASIMOV_C1_a809cda3.md` | `bc3bd77fba3eb555f95e33620ba29814613c3e6e324baaf39500bff859b7ed5f` |
| `linha_do_tempo_f36.json` | `e02465940f0cb3af4232cf7f228871749f8e7ce2d19f966ee3ade307bd6b99dd` |

O pin do `PRE_REGISTRO_CONDICIONAL.md` guardado no FREEZE (`9ec666ad…`) continua histórico. A terceira camada é **append após o fecho** com backup de bytes; seu hash atual é registrado em `RESULTADO_E1_20261008.json`.
