# E0 — revisão independente compacta do MC da rota IV

[REAL de conferência documental e controles leves; DERIVED no cenário gaussiano; NÃO-CEGO]

UTC 2026-09-22T19:35:06.904184+00:00. **Os cálculos de poder/intervalos e a escolha dentro da grade registrada estão consistentes.** Permanece um achado P2 de proveniência/guarda da mistura31 e um P3 de recusa de não finitos. Eles não contradizem os valores atuais conferidos; impedem chamar a implementação de inteiramente autocontida e fail-closed. Nenhuma nova campanha, HDF5, strain ou PE; nenhum builder executado/importado. Os resultados originais foram produzidos pelo agente principal autorizado, não atribuo a execução ao humano.

## 1. Modelo e estatística

Os dados simulados são gaussianos com média comum livre e variância v_i+q, v_i=sigma_df,i² fixa e q≥0. Perfilar a média produz mu(q)=Σs_k/(v_k+q) / Σn_k/(v_k+q), e a log-likelihood perfilada usada no código é

`-1/2 [Σ n_k ln(v_k+q) + Σ ss_k/(v_k+q) − (Σ s_k/(v_k+q))²/(Σ n_k/(v_k+q))]`.

O teste compara 2[ell(q_hat)−ell(0)]>25. A média é perfilada nas duas hipóteses, não fixada para gerar ganho artificial de informação. O esquema multinomial + soma normal + qui-quadrado centrado tem a distribuição das estatísticas suficientes gaussianas condicional às contagens. Classes vazias contribuem zero. O homocedástico usa RSS/N na MLE e cauda qui-quadrado com N−1 graus de liberdade na distribuição amostral; são papéis distintos e corretos.

Conferi a álgebra em observações determinísticas expandidas, incluindo classe vazia, e maximizei independentemente numa grade mais densa seguida de seção áurea. Erro de log-likelihood ≤8.88e-16; diferença de LRT ≈5.33e-15; deslocar todos os dados em 1,7 preserva LRT dentro de 2.66e-14. Isto é controle pontual, não prova global de convergência do otimizador para toda mistura. A busca heteroscedástica em grade + refinamento continua aproximação numérica; o controle escalar de 16 casos registrado pelo construtor foi lido, não repetido.

O pool31/33 é formado por larguras do produto TGR/GWTC5 de eventos de várias corridas, **não 31/33 novos eventos exclusivamente O4b**. As 66 larguras sigma_df/sigma_tau, N e hashes das fontes coincidem com a extração independente de A em DATASET.json. O conjunto31 atual também coincide. Essa comparação usa resultados de A, não uma nova abertura de posteriores por este revisor. As larguras são proxies gaussianas de calibração, não critérios para admitir eventos no teste.

## 2. Validação independente da exploração

Plano: 27 células, 20.000 draws cada, três N por combinação (N exploratório, ceil(1,10N), ceil(1,21N)). Confirmei a reconstrução da grade, sementes únicas e sem reutilização das sementes dos trials exploratórios registrados, vínculos SHA e ordem temporal exploração → plano → resultado. A escrita do plano precede o loop de draws no fonte. Isso é evidência local consistente; não um carimbo de tempo externo inviolável. Independência significa **novos sorteios**, não algoritmo ou estimador diferente.

O limite é unilateral Clopper–Pearson, alpha=0,05/27. Para k>0, p_lo resolve `P[Binomial(20000,p_lo)≥k]=alpha`. Recalculei todas as 27 células por soma binomial/recorrência e bisseção, sem scipy/beta.ppf: erro máximo **1.7e-14**. A desigualdade de [Bonferroni (NIST)](https://www.itl.nist.gov/div898/handbook/prc/section4/prc473.htm) controla a família com cobertura ≥95%; não exige independência entre as células. Escolher uma célula que passou nessa grade mantém a proteção simultânea. A referência ao [método exato Clopper–Pearson](https://docs.scipy.org/doc/scipy-1.16.1/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html) foi conferida; não se usou Wilson como certificado final pós-seleção.

| cenário | sigma_jit | N da grade validado | k/20000 | limite inferior simultâneo |
|---|---:|---:|---:|---:|
| GW250114_actual_width | 0.019 | 61 | 18312/20000 = 0.91560 | 0.909745526983 |
| GW250114_actual_width | 0.0228 | 39 | 18349/20000 = 0.91745 | 0.911652119838 |
| GW250114_actual_width | 0.03 | 22 | 18505/20000 = 0.92525 | 0.919700306022 |
| GWTC5_31_quality_mixture | 0.019 | 1588 | 18223/20000 = 0.91115 | 0.905162697912 |
| GWTC5_31_quality_mixture | 0.0228 | 996 | 18263/20000 = 0.91315 | 0.907221832677 |
| GWTC5_31_quality_mixture | 0.03 | 524 | 18299/20000 = 0.91495 | 0.909075838136 |
| GWTC5_33_quality_mixture | 0.019 | 1696 | 18203/20000 = 0.91015 | 0.904133466052 |
| GWTC5_33_quality_mixture | 0.0228 | 1144 | 18754/20000 = 0.93770 | 0.932583215558 |
| GWTC5_33_quality_mixture | 0.03 | 594 | 18652/20000 = 0.93260 | 0.927299863351 |

Fracassos preservados:

- Mistura33, sigma_jit=0.0228: N=1040, poder pontual=0.9039, limite=0.897705607705; **não passou**.
- Mistura33, sigma_jit=0.03: N=540, poder pontual=0.90475, limite=0.898579321114; **não passou**.

As duas falhas sobem respectivamente para1144 e594 na grade +10%; o +21% também foi predefinido e avaliado, mas não foi necessário para os alvos selecionados. N50 permanece exploratório. N90 aqui é **menor N aprovado dentre três candidatos**, não prova de mínimo inteiro nem localização exata do limiar populacional.

Recalculei ainda as potências homogêneas por recorrência da função gama/qui-quadrado e conferi os três controles analíticos originais. A tabela de nove células homogêneas e quatro mutações rejeitadas pelas guardas próprias deste revisor está em `bis/c1_review/e0_mc_independent_results.json`. O controle próprio durou 0.201s, uma thread; não foram gerados novos draws MC. Tempos originais registrados: busca 35.327371s e validação 16.748353s, além da parede de coordenação.

## 3. Achados e correções exatas

**E0-MC-R1 — P2, proveniência da mistura31 incompleta.** Em `refeito/e0_route_iv_power_013bis_v2.py:30–31` a guarda verifica comprimentos, sem unicidade/inclusão. Em `refeito/validate_e0_mc_targets_013bis.py:22–24`, o plano é gravado antes de reler a seleção de `C4_CATALOG_COMBINATION.json`, cujo hash/membros não são fixados no plano nem no resultado exploratório. Negativa isolada: substituir um membro por UNKNOWN_EVENT deixa len(selected)=31 e len(rows)=33, mas o filtro constrói **30 classes** sem essa guarda recusar. Não alterei arquivo algum nem rodei draws.

Correção ao lado: (a) registrar explicitamente os membros ordenados e larguras por população, probabilidades e hashes de C4_CATALOG_SCHEMA/C4_CATALOG_COMBINATION; (b) exigir nomes únicos, conjunto selecionado contido nos33 e cardinalidades efetivas1/31/33 antes de gravar plano; (c) carregar a população da definição congelada na exploração, sem reler seleção externa mutável após o plano; (d) preservar vínculos de plano/código/resultado. Um adendo de proveniência pode amarrar o snapshot atual à confirmação por A **sem recalcular MC**; deve dizer que é conferência posterior, não fingir que o hash estava no plano original. Para futuros runs, a guarda deve anteceder a escrita. No snapshot corrente a seleção e as larguras foram conferidas e não há evidência de população trocada.

**E0-MC-R2 — P3, recusa de não finitos antes da contagem.** `lrt` aceita uma estatística suficiente NaN e devolve LRT NaN; `t>25` transforma esse caso em falso sem erro (`power:75–76`; validator:27–28). O caso não aparece nos dados atuais conferidos. Correção: `require` explícito de larguras finitas e estritamente positivas, N/draws válidos, estatísticas finitas/consistentes e todos os LRT finitos antes de calcular k. Não depender de assert ou apenas allow_nan=False na serialização: o NaN pode sumir ao virar booleano. Acrescentar negativa leve sob -O. Não é autorização para nova campanha.

## 4. Alcance do aceite

Aceito a **consistência aritmética dos alvos e a proteção simultânea de poder na grade, condicionais ao modelo documentado e à proveniência atual cruzada**. A denominação “limite inferior” significa cenário otimista com sigma_sys=0 e transferência perfeita do jitter ao estimador; não foi provado limite universal para qualquer estimador/população. São larguras condicionadas a priors/modelos existentes, tomadas como conhecidas, sem propagar sua incerteza.

LRT>25 não calibra por si só falso positivo de5σ. Os540.000 draws da validação são de alternativas, não calibradores da cauda do nulo. Uma variância sistemática livre pode confundir-se com jitter; sensibilidade física e função de seleção não foram pagas. A média livre remove deslocamento comum, não todos os sistemáticos. E2 (nulo/seleção) e E5 (inferência populacional completa) seguem OPEN. Nenhuma leitura TGL foi escolhida, nenhum gate movido.

## Custódia

- `refeito/e0_route_iv_power_013bis_v2.py`: `3d6009594c919da22bde0efee23afa93ac070f3f2b19e99ecd5250251d1efcdb`.
- `refeito/validate_e0_mc_targets_013bis.py`: `eb1b79f34fc26c6ee2d2b10f333c5211082ca65d9c4ca311864fa4e9bbf52a26`.
- `bis/E0_ROUTE_IV_POWER_v2.json`: `ae457e82c8c18b5cccf47d60c785d82b3ec3888db7975f2184666c558e4ddd93`.
- `bis/E0_ROUTE_IV_VALIDATION_PLAN.json`: `908727da18cb48a28fcb12f07c9578764af2f266aa08d8ba406735fb18c7fc55`.
- `bis/E0_ROUTE_IV_VALIDATION.json`: `047554eb39c332a9b19190d241a5c34de2e16293074c5aca500ae00f4e3d1c42`.
- `C4_CATALOG_COMBINATION.json`: `f3d8c1959ded3efd15045923ce0cbafe7356ec888ced1934d8d0c183046d0d01`.
- `C4_CATALOG_SCHEMA.json`: `9339c27512482f55b6bfd0b76364ea37cae2abcbaf65f16d3d36a50b9ed92724`.
- `bis/e0_core/DATASET.json`: `89d39541bd9a43f00720bda7b76886a0ee97658749c360682cb6e671c38ec7c0`.
- `bis/PART_B_BUDGET_START.json`: `2b3cfefd17cb8f3df845172a3b41f6e457b92b2c5bb164128aa0b40e8919355f`.
- `bis/E0_ROUTE_IV_POWER_NOTE.md`: `303d40fd5d86c8261dfda57fd5164505d6a053777862a5562eaf9392cb2e5acf`.
- Controle independente: `87b74bc7c95c3696ffa0a8a3e9759cd0e075cd1c4c9289d039568caa667d4e8d`.
- Resultado do controle: `61a2a2ab22acbf83d143a21a736f3ff22fd22f8885e173db0dc5f1b53ac4f1a0`.

Produções permaneceram somente-leitura. Parecer novo, sem substituir os anteriores.
