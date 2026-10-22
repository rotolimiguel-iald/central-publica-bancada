# CÉTICO 2 — achado «F0 — Os três processos vivos» (ordem l.55–58) — 22/09/2026 15:27Z

**Veredito: refutado = false. Gravidade mantida: IMPORTANTE.** O achado sobrevive nos itens (c) e (d), que são inconsistências internas medidas; (a) e (b) são verdadeiros mas, sozinhos, seriam NOTA.

## O que foi medido (bancada só-leitura; nenhum processo tocado)

1. **Fontes sobre quem decide.** `RELATORIO_AUDITORIA_AO_OPERADOR_22SET.md:77` põe a pergunta ao operador («parar ou deixar terminar?») e não propõe padrão; o «Concordo com tudo…» do operador não responde à pergunta 1. `aud_4.txt:146`: «Deixá-los terminar como anexo diagnóstico ou encerrá-los; a decisão é do operador». `medir/SINTESE.md:145`: «parar ou nao e do operador». A ordem l.56 fixa «encerra ela mesma» como padrão e l.284 repete como «padrão desta ordem» com veto. Um padrão é necessário para a ordem ser executável; mas o padrão escolhido é o **irreversível** (encerrar perde 3–13 h de cômputo já pago; terminar pode ser revertido a qualquer momento pelo operador).
2. **Parte A não precisa de CPU** (ordem l.53: «Nenhum job novo de calibração… Tudo o que é número já existe em disco ou se recalcula em segundos»). Encerrar compra só RAM (79 GB) — útil apenas na Parte B, depois do recibo do MA.
3. **Estado atual dos três grupos (lido de `cache/source_evidence/*/PROGRESS.json` às 15:27Z, totais do `MEDICAO_E.json`):**
   - `phase_real_refined/IMRPhenomXPHM_seed130972_N32768`: 9392/22384 (42,0 %), 0,451/s, **ETA 8,0 h**
   - `continuous_source_curves/SEOBNRv4HM_seed130942_N16384`: 2464/8520 (28,9 %), 0,127/s, **ETA 13,3 h**
   - `continuous_source_curves/IMRPhenomXPHM_seed130972_N32768`: 13904/22384 (62,1 %), 0,730/s, **ETA 3,2 h**
   `ps` no WSL (Ubuntu-24.04) confirma os três grupos vivos e **nenhum `audit_phase_source`**.
4. **(c) confirmado:** l.58 exige «`ps` no WSL sem `run_real_phase_importance`, `run_continuous_source_curves`». No ramo «deixá-los terminar» (permitido por l.56 e l.284) essa aceitação só é satisfeita daqui a ~13,3 h — o MA fica sem critério de fechamento ou fica NÃO PAGO por construção.
5. **(d) confirmado:** l.41 diz que `audit_phase_source` (58182) **terminou** (`AUDIT_RATE.json`, 14:02Z); l.58 lista-o entre os que devem sumir do `ps`. Inconsistência interna (trivialmente satisfeita, mas induz a bancada a procurar um quarto processo).
6. **Achado lateral que sustenta a forma da correção:** os números 34860 / 43367 / 19681 / 58182 da ordem l.41 são `session_id` do `STATUS.active_processes` (`MEDICAO_E.json` campo `session_id`), **não PIDs do WSL** — os pais no `ps` são 1261, 1413, 1449. A ordem l.41 diz «há três em `ps`: 34860 …», o que é falso como PID. Consequência: F0 deve identificar os processos **por nome de script** (`pgrep -f` / `pkill -f`), nunca por esses números.
7. `PROMPT_CODEX_ORDEM_013BIS.txt:6` repete «encerre-os você mesma» — ao mudar F0, o prompt deve ser regenerado (sha16 no `MANIFESTO_INSUMOS.json`).

## Correção FINAL (substitui as três linhas de F0, l.56–58)

(ver campo `correcao_ajustada` da resposta estruturada; texto idêntico)
