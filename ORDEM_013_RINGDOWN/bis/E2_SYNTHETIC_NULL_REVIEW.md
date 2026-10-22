# E2 — revisão independente de synthetic_null.py

[REAL — álgebra determinística/AST; INPUT — covariance e modelo sintético; OPEN — calibração física]

**Álgebra gaussiana aprovada no modelo declarado; corrigir R1/R2 antes da campanha. Nenhum Monte Carlo executado.** Arquivo examinado SHA256 `a5b898285bf6da0f3c226256733b058bb90d11eecaf9c491806c9993285c0cf9`, 3534 bytes. Os hashes B1 e NUISANCE_V1 conferem com os comunicados. O censo e o adendoGR para E2 já estão em `bis/e1_selection/CALIBRATION_AND_CANDIDATE_CENSUS.*` e `GR_O4A_ADENDO.*`: calibração33+18−12=39, O4b13 candidatos elegíveis ausentes do corpus; O4a10 adicionais, sem afirmar ausência universal/cegamento.

## Gaussian exact marginal e significado de projected GLS

Se D=diag(σ_i²), η∼N(0,V) e ε∼N(0,D) são independentes, o resíduo centrado r=Xη+ε tem C=D+XVXᵀ. Para sinal fixo δ, I=δᵀC⁻¹δ e w=C⁻¹δ/√I dão Z=wᵀr∼N(0,1). O código implementa C⁻¹δ por Woodbury, inclusive V semidefinida/singular, sem inverter V. As frações a=wᵀDw e b=wᵀXVXᵀw somam1. Quatro matrizes determinísticas comparadas com solução densa independente passaram (erro absoluto máximo 3.33e-16); cinco entradas inválidas foram recusadas sob−O.

Isso é **marginalização gaussiana de nuisance aleatório com V fixada**, não projeção que elimina intercepto/slope arbitrários: Xᵀw em geral não zera. Se a média de nuisance é a estimativa c0,k, o resíduo observado deve subtrair X·média registrada; η representa sua perturbação centrada. Reajustar nuisance ao catálogo de teste ou chamar isso de perfil GLS irrestrito mudaria a estatística e exigiria outra calibração.

O NUISANCE selado marca V como **INPUT da curvatura local gaussiana apenas para nulo sintético**, não covariance fisicamente calibrada. O enunciado normal exato é condicional a D,X,V e δ congelados: não inclui seleção, incerteza de σ, estimação de V, correlação com dados usados para estimá-la, banda KDE ou erro de waveform. O campo `max_squared_signal_fraction` é diagnóstico específico de(w_iδ_i)²; não é por si só número efetivo de eventos nem a participação de Fisher aditiva com correlação.

## E2-SN-R1 — P2: declarar exatamente onde atua a escala t5

O ramo atual simula **Z=√a·G·√(3/U₅)+√b·H**, com G,H∼N(0,1) e U₅∼χ²₅ independentes. É a projeção exata de **ruído de medição t5 elíptico com uma escala compartilhada por catálogo**, somado a nuisance gaussiano independente. Não são t_i independentes por evento; cada entrada do array representa um catálogo inteiro. O fator3 (ν−2) mantém variância1 do ruído padronizado. A convenção de escala da t está na [documentação primária SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html).

**Com b>0, o vetor total não é, em geral, uma t5 elíptica de covariance C; Z é convolução t5+normal.** Uma única escala aplicada ao catálogo inteiro, inclusive nuisance, seria Z=(√a G+√b H)√(3/U₅), outra lei e outra cauda. Shape e covariance tampouco são sinônimos: para t5 de covariance C, shape=(3/5)C. [Definição multivariada](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.multivariate_t.html).

Correção exata recomendada, preservando as contas pretendidas: renomear/declarar o controle como `elliptical_t5_measurement_plus_gaussian_nuisance`, registrar a equação acima, ν=5, unidade de uma escala por catálogo e independência do nuisance. O cabeçalho atual “multivariate elliptical Student t model” precisa desse qualificador; não anunciar t5 de toda C. Se o registro optar pela escala também no nuisance, será mudança de modelo explícita, não mera renomeação.

## E2-SN-R2 — P2: guardas antes do RNG e confiança do recibo

O prefixo real de validação, extraído por AST e encerrado **antes** de construir RNG, aceita `draws=1`, `chunk=0`, `chunk<0`, `chunk=0.5` e `seed=None`. Nenhum draw foi gerado para demonstrar isso. Com chunk0, n=0/used=0 a cada volta: a rotina não progride até eventual recusa do time_guard. Com draws1, o retorno divide por used−1=0 depois de gastar o draw. SeedNone escolhe entropia externa e não assegura replay pelo recibo. O código também não valida α; nomes `one_sided_upper95`/`central95` permanecem95 mesmo quando α≠0,05.

Correção ao lado: exigir antes do RNG inteiros não booleanos `draws≥2`, `chunk≥1`, seed inteiro não negativo e `time_guard` callable; componentes finitos, não negativos e soma1 na tolerância registrada. Em binomial_result exigir α finito em(0,1), inteiros não booleanos k,n e publicar `confidence_level=1−alpha` com nomes genéricos, ou restringir explicitamente α=0,05. Testar recusas sob−O com RNG que lança se alcançado; zero draws nas negativas. Isso não exige campanha.

## Planejamento100M+100M e rotaIV separada

No gaussiano, P(Z>5)=2.86651571879e-07;100 milhões geram em média 28.665157 excedências, com EP relativo aproximadamente 18.68%. É resolução útil para conferir a cauda dentro do modelo, sem alta precisão relativa. O Clopper–Pearson usado por quantis beta é a fórmula correta para contagens IID; sobα=0,05, distingue limite superior unilateral e intervalo central. Não é banda simultânea sobre todas as leituras/modelos. Se o critério exigir upper95≤p5 no próprio limiar teórico5, a aprovação não ocorre normalmente quando p verdadeiro=p5: registrar o critério antes de contar, sem ajustá-lo ao resultado.

No controle de medição t5 puro (b=0), a integral analítica dá P(Z>5)=0.000663962717496, muito acima do normal. Isso é consequência do INPUT não gaussiano, não falha da implementação nem “cinco sigma” físico. Com nuisance gaussiano, a cauda depende de a,b. A projeção reduzida é válida para esse modelo compartilhado; não reproduz uma população de t_i independentes ou catálogos que reestimem a covariance em cada realização.

**O nulo heterogêneo da rotaIV é outro ensaio:** µ perfilado, variância intrínseca≥0 e LRT>25. `synthetic_null.py` não implementa essa estatística; não transportar os100M escalares para seu recibo. O milhão planejado deve rodar a implementação separada pinada, com σ_i/população/µ/nuisance/sigma_sys e seeds registrados, reportando k, N e limite empírico. Se k=0 em1M, upper95=1−0,05^(1/N)=2.99572778635e-06, **maior** que p5; nem zero falsos positivos certifica cauda5σ com esse tamanho. Seriam necessários ao menos 10,450,778 draws sem excedência para esse limite unilateral ficar abaixo de p5. LRT25 não é5σ sem calibração; não assumir Wilks com parâmetro de variância na borda e heterogeneidade.

O módulo não contém sozinho o agendamento100M/100M, o runner do milhão rotaIV, as seeds/células ou o recibo E2. Esses números permanecem **planejados, não executados/verificados como campanha**. O registro deve fixar unilateralidade/direção, tratamento de várias leituras e covariance INPUT; o wrapper autorizado deve verificar os pins antes de qualquer chamada. A leitura pontual de registration_guard/run_controlled não constituiu auditoria integral da árvore PE.

**Não autorizado aqui executar MC:** aguardar registro E2 e a ordem explícita solicitada pelo usuário. Sem PE, posterior novo, strain, waveform, alteração do código examinado ou de resultados selados.

Controle determinístico: `bis/e1_selection/review_e2_synthetic_null.py`; recibo `E2_SYNTHETIC_NULL_CONTROLS.json`. Zero chamadas a simulate_projection completo, zero RNG, zero Monte Carlo. Axiomas N/A.
