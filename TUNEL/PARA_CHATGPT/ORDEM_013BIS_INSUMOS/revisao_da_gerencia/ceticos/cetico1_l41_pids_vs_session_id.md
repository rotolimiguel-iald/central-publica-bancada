# CÉTICO 1 — linha 41 da ORDEM 013-bis (§1, «Os processos vivos») — refutado=false

## O que medi (22/09/2026, por script)
1. `ORDEM_013_RINGDOWN\STATUS_ORDEM_013.json` → `active_processes[].session_id` = 34860, 19681, 43367, 58182. A chave é `session_id` (handle do Codex), não `pid`.
2. `bis\medir\E_instrumento\MEDICAO_E.json` (`date_utc` 2026-09-22T14:16:14Z = 11:16 -03): `ps_snapshot` no WSL traz os grupos por PID-pai **1261** (`run_real_phase_importance.py --processes 4`, 5 processos, 29,82 GB), **1413** (`... --family SEOBNRv4HM --workers 2`, 3 processos, 0,69 GB), **1449** (`... --family IMRPhenomXPHM --workers 12`, 13 processos, 48,19 GB); `rss_total_GB` 78,71; `jobs[].frac` 0,3531 / 0,2272 / 0,4904; `eta_h` 8,41 / 14,27 / 4,26; `progress_utc` 14:15:41Z / 14:15:39Z / 14:15:59Z; 58182 `vivo_em_ps=false`, `audit_mtime_utc` 14:02:16Z. Os números da linha 41 (35 %, 49 %, 23 %, ETAs, ~79 GB) estão CERTOS — só a identidade dos números e o fuso estão errados.
3. Remedição ao vivo em 15:25:45Z: `ps -eo pid,ppid,etime,...` no WSL mostra os mesmos grupos 1261/1413/1449 (etime 05:45 / 05:21 / 05:15); `ps -p 34860,43367,19681,58182` devolve **vazio, rc=1** — esses PIDs NÃO existem no WSL.
4. Fuso: a linha 4 da ordem usa hora local («22/09 10:04» = STATUS 13:04Z); a linha 41 diz «14:15 de 22/09» sem fuso, que é UTC (11:16 -03); a mesma linha diz «14:02Z» com Z. Três convenções numa página.

## Por que não refuto
A frase «há três em `ps`: 34860 …» afirma que 34860/43367/19681 são entradas do `ps`; medido, são `session_id` do Codex e o `ps` não os conhece. A ordem será imutável; uma bancada que leia PID literal age sobre processo inexistente ou alheio. Mitigante: o F0 (l.58) já aceita por nome de script («`ps` no WSL sem `run_real_phase_importance`, …»), então não é BLOQUEANTE. Fica IMPORTANTE.

## Correção final (substituir o parêntese da linha 41; F0 ganha uma linha)
Ver StructuredOutput / campo correcao_ajustada.
