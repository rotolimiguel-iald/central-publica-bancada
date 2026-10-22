# CÉTICO 1 — achado «E2.5 nulos por injeção» (ordem l.171 vs l.183, l.184, l.218, l.229)

**Veredito: NÃO REFUTADO (refutado=false). Gravidade: IMPORTANTE (mantida; a soma dos dois defeitos beira BLOQUEANTE).**

## 1. O que a ordem diz (lido com numeração)
- l.166: «O registro fixa:» — E2 é REGISTRO (MB2, l.229), antes de MB3 (E3.1 piloto) e MB4 (E3.3, só com go, l.210/l.231).
- l.171: «(a) FPR do 5σ com ≥ 1.500 injeções RG na pipeline usada; (b) σ_sys do canal δf̂ (RG em duas famílias); (c) c(SNR); (d) … a calibração a 2,9×10⁻⁷ pede ≥ 10⁸ draws ou o p-valor empírico no N_alvo».
- l.184 (E3.3, MB4): «produtos: c(SNR), σ_sys de δf̂» — os itens (b) e (c) de E2.5 SÃO os produtos de E3.3.
- l.198 (E5.4): «σ_sys … por injeção RG em duas famílias — hoje NÃO ENCONTRADO».
- l.218 (§5): proíbe «abrir job novo de calibração fora de E3 e sem o orçamento de E3.2 aprovado».

## 2. Tentativa de refutação e por que falha
A leitura benigna («o registro apenas FIXA o desenho dos nulos; nada se executa em MB2») é possível pela l.166, mas a l.171 não a diz: «FPR … com ≥ 1.500 injeções» e «σ_sys» são resultados, não desenhos, e o critério de aceitação (l.178: «registro completo nos 10 itens») não distingue registrar de executar. A bancada pode (i) entregar (a) por MC trivial e chamar de «injeções na pipeline», (ii) recusar (b)/(c) citando l.218, ou (iii) abrir PE por injeção em MB2 violando l.218. Três leituras válidas = ambiguidade explorável. **Achado mantido.**

«A pipeline usada» tem três candidatas na própria ordem: a combinação hierárquica sobre posteriores pSEOB (E2.2, l.168 — sem PE, custo de minutos); a PE pSEOBNRv4HM_PA por evento (E3, 81–542 CPU-h/evento, l.182); o estimador próprio da bancada da C5 (l.161: «viés do estimador da bancada por SNR … já medido» vem da C5, fechada como parede, l.36/l.218 «reabrir a C5 como campanha» proibido). Nenhuma nomeada em l.171.

## 3. Defeito adicional, medido (não estava no achado)
Fonte de «1.500»: `bis\medir\SINTESE.md` l.157 «(c) 1.500 injecoes RG para FPR do 5σ» — número da própria síntese da gerência, sem derivação. Conta (script, scipy):
- p(5σ, unilateral) = 2,8665×10⁻⁷.
- 0 falsos em 1.500 ⟹ FPR ≤ 1,995×10⁻³ (Clopper-Pearson 95 %) ≙ **z = 2,88σ**. 1.500 injeções esperam 4,3×10⁻⁴ falsos positivos a 5σ.
- Para esperar 1 falso positivo a 5σ: N ≥ 3,49×10⁶; para limite 95 % com 0 observados: N ≥ 1,05×10⁷.
Logo «FPR do 5σ com ≥ 1.500 injeções» é estatisticamente incoerente, e a própria linha o admite em (d) («≥ 10⁸ draws»). `CRITICO_completude\REFEITOS.json` (nota) e `CRITICO.md` l.99 dizem o mesmo: «a calibracao a 2.9e-7 exigiria >= 1e8 draws (nao feito por ninguem)». Como está, a bancada pode entregar «FPR(5σ) = 0/1500 — PAGO», o que é erro de estatística induzido pela ordem.

## 4. Correção FINAL (substitui integralmente o item 5 da l.171)
5. **Nulos por injeção — todos REGISTRADOS em MB2 (desenho, pipeline nomeada, sementes, N, estatuto); executam-se em MB2 só os que não pedem PE:** (a) **nulo ponta-a-ponta da combinação hierárquica** (E2.2) por ≥ 1.500 conjuntos sintéticos RG (posteriores gaussianos E não gaussianos, σ_i reais dos 31/33, c(σ) de E1 aplicado) — **certifica a FPR até ~3σ** (0/1.500 ⟹ FPR ≤ 2,0×10⁻³ a 95 %, ≙ 2,9σ), **nunca a 5σ**; (d) **a cauda a 5σ**: nulo do LRT e do z com σ_i heterogêneos e posteriores não gaussianos por MC do nulo no N_alvo — a calibração a 2,87×10⁻⁷ pede ≥ 10⁸ draws (custo de minutos a horas em numpy, sem PE) ou o p-valor empírico no N_alvo, dito qual; (b) **σ_sys do canal δf̂** (RG em duas famílias) e (c) **c(SNR) por injeção** exigem PE por injeção: **ficam para E3.3 (MB4, só com go)** ou, se houver, saem das injeções da própria LVK (E1.3) — em MB2 entram só como desenho, marcados `AWAITING_E3` (ou `NÃO PAGO — sem injeção utilizável`); enquanto (b)/(c) não existirem, o gate sistemático de E2.4 fica vermelho e o veredito máximo é NOT_FALSIFIED_UNDERPOWERED/INCONCLUSIVE_SYSTEMATICS. **Nenhuma PE por injeção em MB2** (§5, l.218). Para cada nulo o registro diz: pipeline (hierárquica E2.2 · pSEOBNRv4HM_PA E3 · injeções LVK E1.3), N, semente, o que a FPR medida certifica (σ equivalente) e o estatuto.

## 5. Ajuste coerente fora da l.171 (para não deixar contradição)
- l.157 da SINTESE não muda (é medição, histórico); a ordem é que corrige.
- Se a gerência quiser, em l.178 acrescentar: «Aceitação: … nulos (a) e (d) executados com log; (b) e (c) registrados como AWAITING_E3».
