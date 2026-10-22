# E2 — sidecar independente dos recibos de nulos

[REAL — revisão documental e numérica finita] 2026-09-22T22:06:08.994551+00:00

**Status: BLOCKERS_CLOSED_IN_SCOPE_WITH_NUMERICAL_ADDENDUM.** Não encontrei bloqueante na identidade dos recibos nem na interpretação condicional publicada em B2. A verificação inicial conserva **319 verificações satisfeitas e seis discrepâncias numéricas**, sem converter seu resultado bruto em PASS. O adendo de alta precisão abaixo explica as seis. Nenhuma campanha foi repetida; nenhuma fonte ou B2 foi editada.

## Recibos e integridade

[REAL] Conferidos registro, manifesto B2, campanha, auditor, 25 recibos e 25 logs: hashes, identidade/célula completa, contagens, parâmetros registrados, código associado, ordem temporal, limiares, intervalos, transcrição arredondada na tabela B2 e estabilidade dos bytes ao final. Cobertura exata: 16×100.000.000 + 9×1.000.000 = **1.609.000.000 draws**. São draws de modelos/células distintos, não um único ensaio binomial agregável. Registro precede início da campanha; auditor e entrega B2 seguem seu fim. Tempos dos recibos são evidência registrada, não medição independente de CPU desta revisão.

O auditor existente valida hashes e inverte probabilidades binomiais, mas **copia** a referência analítica de cada recibo. Esta revisão complementa esse ponto por convolução independente; não afirma que o auditor por si recalcula a cauda. Nenhum import de produtor, nova MC, PE, HDF, strain ou leitura da seed/offset real ocorreu.

## Fórmula e FPR

[DERIVED] Com a fração de variância de medida a e de nuisance b (a+b≈1), o controle não gaussiano usa Z=√a·√(3/U)·G+√b·H, U~χ²₅ e G,H normais padrão independentes. Logo P(Z>5)=∫Φ̄(5/√(3a/u+b))fχ²₅(u)du. O fator **3**, não 5, normaliza a variância de medida. Para b>0, a soma não é uma Student t5 pura; a escala compartilhada do catálogo é parte do modelo elíptico declarado.

[REAL] Recalculei as oito referências por outro integral: ∫φ(h)·S_t5((5−√b·h)/√(3a/5))dh, h∈[−12,12]. A massa normal omitida é inferior a 4×10⁻³³. Maior diferença absoluta para os recibos: 7.67e-17. A referência gaussiana unilateral é p5=2.8665157187919e-07; também conferida com a+b medido.

Os controles t5+normal têm FPR analítico de 5.12880669e-06 a 9.98141354e-05, **17.89 a 348.21 vezes p5**. Portanto, z>5 nominal não fornece FPR de 5σ nesses modelos. Isso não é evidência contra/a favor da TGL: é calibração sintética condicional do limiar. Os 16 valores analíticos estão dentro dos respectivos IC centrais95%; o aviso de B2 sobre possível desencontro pontual é geral, não descreve um desencontro observado aqui. Em GWTC5_31_R_B_G, UL95 unilateral fica abaixo de p5; isso é compatível com cobertura unilateral95%, não autoriza seleção desse caso ou certificação física.

## Rota IV e intervalos

[REAL/DERIVED] Em cada célula IV n=1.000.000, limiar estrito LRT>25. Sete células têm k=0: UL95=1−0,05^(1/n)=2.995727786353e-06; IC central95%=[0; 3.688872650206e-06]. Duas têm k=1 (GWTC5_31/N1588 e GWTC5_33/N1696): UL95≈4,743855638×10⁻⁶; IC central95%≈[2,531780766×10⁻⁸; 5,571630655×10⁻⁶]. Os UL são respectivamente **10,45 e 16,55 vezes p5**. Zero é a estimativa empírica k/n, nunca prova de p=0. LRT>25 não ganha equivalência física5σ por nome; a cauda analítica IV permanece OPEN neste escopo. Não agrupar populações/N para reduzir o UL. Os intervalos são Clopper–Pearson pontuais, não simultâneos/familywise. Apenas como identidade binomial, seriam necessários 10,450,778 draws com zero contagem para UL95≤p5; não é pedido de nova campanha.

## Adendo numérico preservado

[REAL] A comparação inicial beta.ppf versus raízes de scipy.binom, com tolerância absoluta1e−16 e relativa1e−10, marcou seis células gaussianas. Investigação separada usa soma binomial direta Decimal80 e 180 bisseções, sem simulação: maior erro absoluto dos endpoints publicados nesses casos **1.3431e-16** (relativo máximo 4.0207e-10). A raiz SciPy também difere da referência Decimal. São diferenças de precisão numérica que não mudam arredondamento B2, inclusão no IC ou conclusão. O arquivo inicial FAIL e o adendo permanecem separados e imutáveis; não houve relaxamento seguido de reexecução para obter PASS.

## Alcance e exposição

[INPUT] Covariância E1, populações e sigma_sys são condicionantes declarados. [OPEN] Cauda física, seleção e erros de waveform não pagos. **INCONCLUSIVE_SYSTEMATICS; NOT_FALSIFIED nunca CONFIRMED.** Esta revisão não reabre ciência fechada, não decide admissão/PE e não autoriza rerodar células.

[REAL — exposição desta revisão] O arquivo B2 foi exibido integralmente na leitura documental, incluindo sua seção de diagnósticos numéricos440 arquivados; isso fica declarado. Nenhum arquivo de posterior/amostras foi aberto ou baixado nesta sidecar. Não se afirma cegueira absoluta nem independência das bibliotecas numéricas: SciPy é compartilhado; a inversão Decimal80 e a variável de convolução fornecem checagens distintas.

## Pins lidos dos bytes

- `RINGDOWN_5SIGMA_V1.json` — `e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416`.
- `ENTREGA_013BIS_B2_registro_e_440.md` — `06345093b5fca7b250f9360f66cf40bfc0becbd54b6e4cce4505f828f96fa8d7`.
- `RESULT_E2_NULL_CAMPAIGN.json` — `cb104ff0c6c4049e9bc4ee9db7a95a53224045039916438738958a691ee4643a`.
- `E2_NULL_RECEIPTS_AUDIT_V1.json` — `93cffda37b3d80bb961dcaca229e31f8dd5b0c11a183d583300a80429840ae31`.
- `audit_e2_null_receipts_013bis.py` — `3c8577eb46ca0cd43d47e24e89216411e1dc2040f6a588d658bd9b222712866c`.
- `null_runner.py` — `1b6bf00beced255d45ac642de5209d32440e486f8a3af469e92a47c58fe1c561`.
- `synthetic_null.py` — `be0fa6d4b678993edcbc7dec15f311950c51e466020dc99c5d0f043763eb65f1`.
- `route_iv_null.py` — `dfcf9491ab98f9d32aae119177f53a3622289593c19c528e50cd091ebd7000cd`.
- `review_null_receipts_finite.py` — `dde8e2fe8b928f1826e3307a2077cffdb495ecccb2d45bf470122005920509f6`.
- `E2_NULL_CAMPAIGN_REVIEW_EVIDENCE.json` — `7ff83a9df4793d103151feda357fff9046fe38ba0d0fbc48d580b899a86576d2`.
- `E2_NULL_INTERVAL_NUMERICAL_ADDENDUM.json` — `992415f858db84538fac532f44ab632ad27b1f31d978376551d7717b6e40368e`.

A evidência JSON conserva pins individuais dos 25 recibos/logs, verificações e valores por célula. Nenhum hash é inferido de nome ou memória.
