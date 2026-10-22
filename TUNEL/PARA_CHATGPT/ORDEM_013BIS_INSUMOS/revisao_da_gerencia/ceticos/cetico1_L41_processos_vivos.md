# CÉTICO 1 — achado «L41 / §1 Os processos vivos» — VEREDITO: NÃO REFUTADO (refutado=false), gravidade IMPORTANTE mantida

Medido às 15:29Z de 22/09 (12:29 −0300), bancada só-leitura.

## O que se confirmou [REAL — por script]
1. Fuso. `stat` da ordem: mtime 2026-09-22 11:57:03 −0300 (= 14:57Z). A linha diz «às 14:15 de 22/09» sem sufixo; se fosse local, seria DEPOIS da gravação. A retro-extrapolação linear dos PROGRESS.json (13:04Z → 15:29Z) a 14:15Z dá 35,4 / 49,1 / 22,8 % e ETAs 8,4 / 4,2 / 14,2 h — bate com «35 %, ~8 h; 49 %, ~4 h; 23 %, ~14 h». Logo 14:15 é UTC (= 11:15 −0300). Ao lado, «14:02Z» com Z: mistura de convenções na mesma frase. E «14:02Z» confere: AUDIT_RATE.json mtime 11:02:16 −0300.
2. 34860 / 43367 / 19681 / 58182 são `session_id` em `STATUS_ORDEM_013.json.active_processes` (handles do Codex, com `folder` e `last_progress`), NÃO PIDs. `ps` do WSL às 15:29Z: PID 1261 (`run_real_phase_importance.py --processes 4`, +4 workers 1289–1292), PID 1413 (`run_continuous_source_curves.py run --family SEOBNRv4HM --workers 2`, +1441–1442), PID 1449 (`… --family IMRPhenomXPHM --workers 12`, +1477–1488); `audit_phase_source` AUSENTE (aud_5.txt l.98 o registrava como PID 1819). A frase «há três em ps: 34860 …» é inverificável por `ps` como está.
3. Percentuais: denominador é `valid_draws` (22384 / 22384 / 8520), não N32768 / N16384. Sobre N32768 o real_phase estaria em 24,2 %, não 35 %. A ordem não diz o denominador.
4. RSS somado (processos-pai + workers) agora 88,95 GB; `free -g`: used 86 / total 125. Às 13:34Z a aud_5 media 73,4 GB; ~79 GB às 14:15Z é consistente; crescimento medido ≈ 5–6 GB/h [REAL, entre 13:34Z e 15:29Z].
5. AUDIT_RATE.json (phase_native_repeat\SEOBNRv4HM_seed130942_N16384): status PASS_ARITHMETIC_NOT_PRECISION, passed_precision 444, scientific_acceptance false. O «/1200» vem de RESULT.json (rows = 1200 mocks; aud_4.txt l.60/95/134) — o número da ordem está sustentado, mas a fonte do denominador é RESULT.json, não AUDIT_RATE.json.

## Por que IMPORTANTE e não NOTA
A ordem será imutável; a bancada, que opera em −0300 e vê `ps` do WSL, não consegue reproduzir «três em ps: 34860…» nem a hora. Não induz erro de física nem decide nada do operador (a frase é descritiva; a conclusão «nenhum produto muda o portão» não depende dela) — logo não é BLOQUEANTE.

## Correção FINAL (substitui, na L41, o parêntese inteiro «(`STATUS.active_processes` listava quatro; … 444/1200 na precisão)»)
Ver campo `correcao_ajustada` do StructuredOutput (texto idêntico abaixo).

(`STATUS.active_processes` listava quatro **handles** do Codex — `session_id`, não PIDs; às **14:15Z (11:15 −0300)** de 22/09 há **três** em `ps` do WSL: PID 1261 `run_real_phase_importance` (handle 34860; 4 workers; `done/valid_draws` ≈ 35 % de 22384, ETA ~8 h); PID 1449 `run_continuous_source_curves` IMRPhenomXPHM (handle 43367; 12 workers; ≈ 49 % de 22384, ETA ~4 h); PID 1413 `run_continuous_source_curves` SEOBNRv4HM (handle 19681; 2 workers; ≈ 23 % de 8520, ETA ~14 h) — percentuais sobre `valid_draws` dos `PROGRESS.json` de cada pasta, não sobre N32768/N16384; RSS somado ≈ 79 GB de 125, crescendo ≈ 5–6 GB/h `[REAL — ps/free do WSL, 13:34Z→15:29Z]`; o quarto, handle 58182 / PID 1819 `audit_phase_source`, **terminou** — produto `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\AUDIT_RATE.json`, 14:02Z, `PASS_ARITHMETIC_NOT_PRECISION`, `passed_precision` 444 dos 1200 mocks de `RESULT.json`)
