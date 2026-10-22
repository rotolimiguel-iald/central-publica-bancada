# CÉTICO 1 — achado L41 (§1, «Os processos vivos»): session_id ≠ PID; «14:15» sem fuso

**Veredito: refutado = false. Achado PROVADO. Gravidade mantida: IMPORTANTE.**

## O que a ordem diz (L41)
«às 14:15 de 22/09 há **três** em `ps`: 34860 `run_real_phase_importance` …; 43367 `run_continuous_source_curves` IMRPhenomXPHM …; 19681 … SEOBNRv4HM …; … o quarto, 58182 `audit_phase_source`, terminou — … 14:02Z»

## Medido por script (22/09/2026, 15:22:54Z, `wsl -e sh`)
1. `STATUS_ORDEM_013.json` → `active_processes[].session_id` = 34860, 19681, 43367, 58182 (campo chama-se `session_id`, com `observation: "Exact handle returned live during this continuation"` — handle da ferramenta da bancada).
2. `ps -p 34860,43367,19681,58182` → vazio, rc=1. Nenhum desses números é PID no WSL.
3. `ps -eo pid,ppid,etime,rss,cmd | grep run_|audit` → pais **1261** (`run_real_phase_importance --processes 4`, filhos 1289–1292, etime 05:42:50), **1413** (`run_continuous_source_curves --family SEOBNRv4HM`, filhos 1441–1442, etime 05:19:05), **1449** (`… --family IMRPhenomXPHM`, filhos 1477–1488 = 12, etime 05:13:00). Nenhum `audit_phase_source` (o 1819 do aud_5:98 terminou — coerente com `AUDIT_RATE.json` mtime 14:02:16Z).
4. `uptime -s` = 2026-09-22 04:40:47 (tz do WSL = America/Sao_Paulo, −03); aud_5.txt:100 «O WSL reiniciou às 04:42». Os etimes ~5 h batem com o reinício: PIDs baixos (1261/1413/1449) são de processos relançados após o reboot — os handles 34860 etc. jamais foram PIDs dessa árvore.
5. Fonte do «14:15»: `medir/E_instrumento/MEDICAO_E.json` — `progress_utc` 14:15:39/41/59+00:00 e `date_utc` 14:16:14Z; `medir_E.py:56` copia `session_id` do STATUS e (`:68-80`) decide `vivo_em_ps` **por NOME** no `ps`, nunca por PID. Logo «14:15» é UTC, e na mesma frase a ordem escreve «14:02Z» — inconsistência de fuso interna à linha. (Ordem mtime: ver stdout; WSL/host em −03.)
6. `rss_total_GB` = 78,71 (MEDICAO_E) — o «~79 GB de 125» da ordem está certo; 4/12/2 workers, 35 %/49 %/23 %, ETA 8,41/4,26/14,27 h conferem com `frac`/`eta_h` do JSON.

## Por que não se refuta
A frase «há três em `ps`: 34860 …» afirma que `ps` mostra esses números. `ps` não os mostra (rc=1). A ordem será imutável e a bancada pode ler «PID» e tentar `kill 34860` (falha) ou, pior, tomar o handle da ferramenta por identificador de SO na ficha `C5_ANEXO_PROCESSOS_ENCERRADOS.json` (F0 pede «hora do encerramento» — o identificador registrado tem de ser o que o SO conhece). Não bloqueia: F0 (L58) aceita por NOME em `ps`, então a execução não quebra; por isso IMPORTANTE, não BLOQUEANTE.

## Correção FINAL (substituir o trecho entre «às 14:15 de 22/09» e «14:02Z,» inclusive; o resto da L41 fica)
«às **14:15Z** de 22/09 (11:15 −03; `MEDICAO_E.json`) há **três** em `ps` — os números 34860/43367/19681/58182 abaixo são os `session_id` do `STATUS_ORDEM_013.json` (handles da ferramenta da bancada, **não PIDs**; em `ps` às 15:22Z os pais são **1261**, **1413** e **1449**, com etime ~5 h desde o reinício do WSL às 04:42 −03, aud_5) `[REAL — medido]`: 34860 `run_real_phase_importance`, 4 workers, 35 %, ETA ~8 h; 43367 `run_continuous_source_curves` IMRPhenomXPHM, 12 workers, 49 %, ETA ~4 h; 19681 `run_continuous_source_curves` SEOBNRv4HM, 2 workers, 23 %, ETA ~14 h; RSS somado ~79 GB de 125; o quarto, 58182 `audit_phase_source`, **terminou** — produto `AUDIT_RATE.json`, 14:02Z,»

Adendo mínimo em F0 (L59, bullet do anexo), para que a bancada registre o identificador certo: acrescentar «(identificar cada processo por PID de `ps` + `session_id` do STATUS; os dois, lado a lado)».
