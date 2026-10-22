# CÉTICO 2 — achado «l.41: session_id ≠ PID; 14:15 é UTC» — VEREDITO: NÃO REFUTADO (IMPORTANTE)

Medido em 22/09/2026 12:25 -03 (15:25Z), por script, só leitura.

1. `STATUS_ORDEM_013.json` (sha16 0815ce7d607ac49f, lido em MEDICAO_E.fontes): `active_processes[].session_id` = 34860, 19681, 43367, 58182. A chave chama-se `session_id`; nenhum campo `pid`.
2. `MEDICAO_E.json.ps_snapshot` (14:16:14Z) e `ps -eo pid,ppid,etime,pcpu,rss,args` no WSL às 15:25Z: PIDs reais são 1261 (+1289–1292) `run_real_phase_importance.py --processes 4` (5 procs); 1413 (+1441,1442) `run_continuous_source_curves.py run --family SEOBNRv4HM --workers 2` (3 procs); 1449 (+1477–1488) `… --family IMRPhenomXPHM --workers 12` (13 procs). Nenhum PID 34860/43367/19681 existe. `ps_groups` de MEDICAO_E confirma 5/3/13 procs e RSS 29,82/0,69/48,19 GB (total 78,71).
3. Hora: `MEDICAO_E.date_utc = 14:16:14Z` e `jobs[].progress_utc = 14:15:xxZ` → o «14:15» da l.41 é UTC = 11:15 -03. A l.4 escreve «22/09 10:04» para a última nota, cujo mtime é 13:04:13Z (10:04 local, medido em DO_CHATGPT). A ordem mistura UTC sem sufixo (l.41) com hora local (l.4) e UTC com «Z» (l.41, «14:02Z»). Inconsistência interna real.
4. Não é BLOQUEANTE: F0 (l.55–58) já aceita por nome de script em `ps`, então a ordem é executável; mas a l.41 chama de «em ps» números que não são de ps, e uma bancada que faça `kill 34860` não mata nada (ou, em outro momento, mata processo alheio). IMPORTANTE mantido.
