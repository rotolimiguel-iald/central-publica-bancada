[REAL — NÃO-CEGO; E0.6 reobtido dos estimadores C5 existentes; calibração operacional NÃO PAGA]

# E0.6 — adendo direto C5 e tipagem de N

Preserva DATASET.json/E0_CORE.json. Lê os draws/estimadores arquivados, sem rerun de C5, PE, onda ou strain. Nenhuma magnitude da gerência entrou nesta matriz.

**Conversão:** δτ(a)=−a·x/(1+a·x), com x=Γτ do 220 exato da família de recuperação. Média/DP/EP foram calculados após transformar cada a_hat. O antigo proxy a·δτ(1) aparece somente como controle. Negativos são diagnósticos de ajuste, não geradores GKLS físicos.

Matriz: 576 células IMR (206 ruídos cada); 480 células 220+440 por janela (50 ruídos cada); 228 controles sem ruído. Casos não identificáveis permanecem nulos. As células reutilizam intervalos e não são evidências independentes.

EP da média e do DP: influência agrupada pelos pares GPS salvos/índices de intervalo, condicionada à biblioteca finita. Não inclui PSD, dependência entre intervalos ou erro de modelo. Controle sem ruído: N=1, EP=null; Fisher local não é EP medido. Na mistura, a família vencedora não está nos draws: conversão única e σδτ NÃO PAGOS.

Exemplo R-B, O4, a injetado=0, SNR40, início 10tM; cada δ é relativo ao GR da sua família:

| Injeção → recuperação | δτ sem ruído | Média δτ ± EP | DP δτ ± EP | N |
|---|---:|---:|---:|---:|
| SEOBNRv4HM → SEOBNRv4HM | -1.049757e-08 | -0.002885076 ± 0.00313 | 0.04487783 ± 0.00206 | 206 |
| IMRPhenomXPHM → SEOBNRv4HM | -0.03278029 | -0.03757339 ± 0.00304 | 0.04358335 ± 0.00207 | 206 |
| SEOBNRv4HM → IMRPhenomXPHM | 0.02667791 | 0.03819117 ± 0.00352 | 0.05053133 ± 0.00251 | 206 |
| IMRPhenomXPHM → IMRPhenomXPHM | -9.874647e-09 | 0.01593966 ± 0.00393 | 0.0564725 ± 0.00209 | 206 |

Pisos |δ|/5 e |δ|/15 vêm da referência GW250114 recalculada no DATASET, ambos INPUT. Cada célula tem fonte/índice, família, ruído, janela, bordas e comparação aos pisos. Nenhuma comparação de magnitude substitui σ(c_calibrado) pSEOB: gate operacional permanece NÃO PAGO.

**N_alvo_operacional=null** no adendo, inclusive para todas as linhas de subresolução. N50/N90 astronômicos da v1 ficam apenas em analytic_only, sem constituir alvos de aquisição. R-GLOBAL é efeito nulo; R-RAIZ-COHERENT/R-PROP continuam OPEN para este observável. Não escolher leitura.

A revisão escalar principal foi comunicada pelo operador; este adendo ainda requer revisão distinta. MC da rota IV não foi refeito. E1 não iniciado. Axiomas N/A; teoremas 0.

Arquivos novos deste adendo: build_systematics_adendo.py, SYSTEMATICS_ADENDO.json, SYSTEMATICS_ADENDO.md, SYSTEMATICS_COST.json. SHA/fontes e custo nos JSONs.
