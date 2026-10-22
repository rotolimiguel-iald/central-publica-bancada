# CÉTICO 2 — achado L41 (PIDs × session_id; «14:15» sem fuso) — VERIFICADO, NÃO REFUTADO

Medido em 22/09/2026 15:22Z (script: `wsl ps`, `python json`, `ls --time-style=full-iso`).

1. `Chatgpt\ORDEM_013_RINGDOWN\STATUS_ORDEM_013.json` (mtime 10:04:13 -03 = 13:04Z): `active_processes[]` traz SOMENTE `session_id` = 34860, 19681, 43367, 58182. Não há campo `pid`.
2. `wsl ps -p 34860,43367,19681,58182` → vazio, rc=1. `wsl ps -eo pid,ppid,etime,rss,args` → pais reais 1261 (run_real_phase_importance, 4 filhos), 1413 (continuous SEOBNRv4HM, 2 filhos), 1449 (continuous IMRPhenomXPHM, 12 filhos); etime 05:42 / 05:19 / 05:13 às 15:22Z. `wsl uptime -s` = 04:40:47 -03 (aud_5.txt:100 diz 04:42; mesma janela).
3. A PRÓPRIA MEDIÇÃO da gerência já tinha os PIDs certos: `medir/E_instrumento/MEDICAO_E.json:2` `date_utc = 2026-09-22T14:16:14Z`; `:21` `ps_snapshot` lista 1261/1413/1449 e filhos. A ordem (mtime 11:57:03 -03 = 14:57Z) trocou os PIDs do snapshot pelos `session_id` do STATUS.
4. Fuso: a ordem nasceu às 14:57Z; «14:15 de 22/09» só pode ser 14:15Z (≈ o snapshot de 14:16Z) — 14:15 locais seria futuro. Os outros horários da ordem («01:36 de 22/09», «20:41 de 21/09», «20:02») são locais sem marca; «14:02Z» tem marca. Inconsistência real, não gosto.

Gravidade: IMPORTANTE mantida (número errado numa ordem imutável; a bancada, que conhece seus PIDs, leria a gerência como quem não mediu). Não é BLOQUEANTE: não move física, portão nem partição; a aceitação de F0 por NOME (L58) fica.

Correção FINAL (substituir o parêntese em L41, da abertura até «444/1200 na precisão)»):

**Os processos vivos** (`STATUS.active_processes` listava quatro `session_id` — 34860, 43367, 19681, 58182 —, que são handles da ferramenta da bancada, não PIDs; às 14:16Z de 22/09 há **três** em `ps` `[REAL — medir/E_instrumento/MEDICAO_E.json, ps_snapshot]`: PID 1261 `run_real_phase_importance`, 4 workers, 35 %, ETA ~8 h; PID 1449 `run_continuous_source_curves` IMRPhenomXPHM, 12 workers, 49 %, ETA ~4 h; PID 1413 `run_continuous_source_curves` SEOBNRv4HM, 2 workers, 23 %, ETA ~14 h; RSS somado ~79 GB de 125; o quarto, `audit_phase_source` (session 58182), **terminou** — produto `AUDIT_RATE.json`, 14:02Z, `PASS_ARITHMETIC_NOT_PRECISION`, 444/1200 na precisão) atacam só o R-B em SNR40 com fonte marginalizada.

(O resto da linha fica como está.)
