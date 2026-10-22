[REAL - extremos numericos conferidos; OPEN - integrais e calibracao fisica]

# ORDEM 013 - Duas familias continuas em execucao

Registro:2026-09-22T10:16:35.443924+00:00. N/A - sem Lean. Canone, Atlas e C6 preservados.

**PAGO no escopo parcial:**96 pontos SEOB e192 Phenom confrontados com os
checkpoints binarios das mesmas coordenadas e mesmas propostas. Para cada
ponto, a=0 e a=1 nos1200 mocks:691200 comparacoes de logL, discrepancia maxima
zero. Os arquivos foram lidos em bytes uma vez, com SHA256 do mesmo conteudo.
Isto confere identidade numerica de leitores; nao cria eventos independentes
nem demonstra a precisao da integral ainda incompleta.

**PAGO, recusa:**a auditoria com --require-complete recusou ambas as rodadas
incompletas. Os retratos parciais tem full_comparison_complete=false e nao
promovem a aceitacao cientifica. Nenhuma soma parcial substituiu o N registrado.

**INICIADO:**Phenom continuo32768/22384 validas,17 intensidades,handle43367,
12 trabalhadores. Antes da partida, WSL informou48 CPUs acessiveis,carga1min
10.09 e114651380KiB de memoria disponivel. SEOB continuo19681 permanece com
2 trabalhadores; binarios34860 e40860 permanecem com4 cada. Todos revalidados
vivos na mesma rodada de registro. Nenhuma execucao duplicada ou reiniciada.

**NAO PAGO:**concluir integrais, conferir densidades e covariancia, repetir
independentemente as curvas, controlar resolucao e medir vies/cobertura.
Continuam os demais SNR/leituras do objetivo completo e os limites da C6.
Sem novo sigma e sem aceitacao fisica. A extensao nao escolhe relogio fisico,
prior sobre a ou novo beta. Negativos sao diagnosticos, nao GKLS fisica.

## Continuacao

- Revalidar34860,40860,19681,43367, usando os handles existentes.
- A auditoria util de encerramento e `audit_continuous_endpoints.py --family
  SEOBNRv4HM --require-complete` (analogamente IMRPhenomXPHM), depois de ambos
  os resultados respectivos estarem completos. Evitar repetir retratos
  parciais apenas para produzir novos arquivos.
- Ao fim de cada corrida continua, executar `run_continuous_source_curves.py
  analyze --family <familia>`. E diagnostico, nao aceitacao automatica.
- Integrais binarias concluidas exigem auditoria de densidade, comparacao de
  repeticoes e seus proprios pontos de controle de resolucao.
- Mistura binaria ja registrada continua Phenom16384+SEOB16384; nao substituir
  silenciosamente o Phenom por32768. Mistura de curvas continuas requer
  evidencia por familia com prior comum, nunca media de log-fatores.

Ficha de aproveitamento:mesmas propostas,indices,ruidos,amplitudes e geradores;
acrescentada apenas a comparacao entre checkpoints das duas leituras numericas.
Tentativas anteriores preservadas.

## Custodia - SHA256 lidos dos artefatos

- `cache\source_evidence\continuous_source_curves\SEOBNRv4HM_seed130942_N16384\endpoint_audits\20260922T101217_966853Z\RESULT.json`: `f39192a57096dfef90926ae1b6359db6b09acb79e171a73dab0dbd1eff43fd75`
- `cache\source_evidence\continuous_source_curves\IMRPhenomXPHM_seed130972_N32768\endpoint_audits\20260922T101245_712920Z\RESULT.json`: `6a2c2fdf24d66443395d2b8d2450c4f59356984f955752c1612d5bf0e717f7e0`
- `cache\source_evidence\continuous_source_curves\INCOMPLETE_GUARD_CHECK.json`: `c46aca6fd5d7e2dbfd6d0a116ff18b39c6a06b433e7cf78867301b7715b97c1c`
- `cache\source_evidence\continuous_source_curves\IMRPhenomXPHM_seed130972_N32768\START.json`: `ed47027bb6535823886093d6c44af17246c8478aadb237100506fd9196f59749`
- `cache\source_evidence\audit_continuous_endpoints.py`: `75baac0f50510952c9fb46aa7fa05073b632be6851f1ba9e3ef7f3aea406219c`
