[REAL - aritmetica verificada; OPEN - resultados fisicos da mistura]

# ORDEM 013 - Mistura continua registrada

Registro: 2026-09-22T10:25:20.384098+00:00. N/A - sem Lean. Canone, Atlas e C6 preservados.

**PAGO:** `continuous_family_mixture.py` reaproveita `mix_statistics`, ja
validada, para cada intensidade contra a=0. O prior de familia e o mesmo em
toda a curva: metade Phenom, metade SEOB; nao foi introduzido prior sobre a.
Misturam-se Z_f(a), nunca os logaritmos e nunca os mocks.

O oraculo independente usa somas em long double, numeros diferentes de
amostras por familia, tres alvos e 17 intensidades. Maximos erros:
logZ=1.61741280091e-15, razao logaritmica=
1.884451796e-15, erro MC pareado=
8.29954645455e-18. A media incorreta de logaritmos
erra em 0.67830685282 nesse controle.
Integrandos constantes devolvem erro MC=2.64018065658e-16,
compativel com zero. A familia com precisao insuficiente continua recusada
mesmo com prior1e-10; uma bandeira otimista que contradiz o ESS e recusada.
Nao repetimos o ensaio binario de4000 realizacoes: o reaproveitamento e explicito.

**REGISTRADO / NAO EXECUTADO:** `continuous_source_family_combination` exige
os dois resultados completos, os cubos/estatisticas sob hash, as auditorias
integrais dos extremos e as auditorias de densidade das propostas respectivas.
O comando `combine_continuous_source_curves.py run` recusou corretamente os
resultados ainda ausentes. Registro separado da mistura binaria antiga:
na continua entram Phenom32768 e SEOB16384; na binaria previamente registrada
continuam Phenom16384 e SEOB16384. Nao houve substituicao silenciosa.

**NAO PAGO:** integrar as curvas em execucao, auditar, medir vies e cobertura;
repeticao continua independente e controle de resolucao dos novos dominantes;
outros SNR/leituras do objetivo completo. A combinacao preserva todas essas
pendencias. Intervalo LR90 de Z(a) marginalizado nao vira intervalo bayesiano,
e a cobertura sera aferida por celula com os50 ruidos reutilizados.

## Execucoes e proximo passo

Os handles34860,40860,19681,43367 foram revalidados vivos. Nao repetir esses
jobs nem abrir nova rodada apenas porque estao demorando. Aguardar conclusoes
para auditoria de densidade/binarios, `run_continuous_source_curves.py analyze`
e `audit_continuous_endpoints.py --family <familia> --require-complete`.
So entao rodar `combine_continuous_source_curves.py run`.
A saida combinada permanece diagnostica ate passar repeticao, resolucao e
calibracao: o codigo nao aceita fisica automaticamente.

Ficha de aproveitamento: mesmas evidencias, priors, dados e estimador centrado
de covariancia; apenas a indexacao por intensidade e a verificacao conjunta
foram acrescentadas. Sem novos sinais experimentais ou conversao para sigma.
Tentativas anteriores preservadas.

## Custodia - SHA256 lidos por script

- `cache\source_evidence\continuous_family_mixture_validation\RESULT.json`: `37342e279f0e61e94e6657ff59bdee729e9306eeeaf23247abaf30393e72074b`
- `cache\source_evidence\continuous_family_mixture_validation\REGISTRATION.json`: `d0914ba7c9e283666f51575d90a46b0dcf88a027cf76d53d6f2709271934558d`
- `cache\source_evidence\continuous_source_family_combination\REGISTRATION.json`: `d8f521ffadeb4a40b8322e92a673d1d02a698ac9c39d6af3450e761274bda22a`
- `cache\source_evidence\continuous_source_family_combination\INCOMPLETE_GUARD_CHECK.json`: `3ed94ea20e24d37823b505f7ad3603b9445d4264ed23c767fbdac87634a0136d`
- `cache\source_evidence\continuous_family_mixture.py`: `a76a8001afb21ed76a7dbac016eaa939c36c00b01c25324e03000e21a483b978`
- `cache\source_evidence\validate_continuous_family_mixture.py`: `0ddee4d4c6d14b2bd80f188635c961df68c44d594fdda359a454906587931116`
- `cache\source_evidence\combine_continuous_source_curves.py`: `b74aa70c305c66e80c3c2b9857f80c44fc7962c57f8e096366b3eab3c9c3e7b9`
