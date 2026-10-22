# ORDEM 018 — F2: derivações e limites observacionais

[REAL — análise local e revisão independente concluídas no escopo documental/algébrico, 2026-10-06T01:04:42.718014+00:00] As sete rotas solicitadas foram examinadas com estatutos explícitos. O resultado principal é que a distância usa a **integral de k(z)**; temperatura, lentes e crescimento precisam de pontes adicionais para virar previsões observacionais. Uma lacuna localizada é resultado da F2, sem declarar inexistência no acervo inteiro.

O desenvolvimento completo, fontes com linhas, duas alternativas por lacuna e cálculos estão em [derivacoes/NOTA_DERIVACOES_F2.md](</C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/NOTA_DERIVACOES_F2.md>). O manifesto [derivacoes/MANIFESTO_F2.json](</C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/MANIFESTO_F2.json>) fixa os artefatos; beta é sempre recalculado de alpha_CODATA2018 vezes sqrt(e). Não se executou o canônico nem se abriu dado para novo veredito.

| Rota | Equação / previsão | Estatuto e sensibilidade |
|---|---|---|
| R-D | k=E^(2 beta/3); Q=(integral k/E)/(integral 1/E). Q−1=0,19751% em z=1 e 0,40433% em z=2,3, na fiducial de baixo z da nota. | [DERIVED condicional] Taxa no ponto final não é distância integrada. No mapa implementado, BAO permanece nu. |
| R-E | eta=fL/fA: 1 se leitura comum; Q/K* se luminosidade apenas, forma normalizada Q. | [OPEN mapa] A lei K não seleciona fA nem transporte de fótons. R-D e R-E não são dados independentes. |
| R-F | Tr(H[H,[H,rho]])=0 para dephasing na base do mesmo H. Com redshift geométrico usual e expansão adiabática, T=T0(1+z); uma gamma_T constante exigiria Qgamma=4 gamma_T H rho_gamma. | [DERIVED sob hipóteses / OPEN outro ramo] sigma_gamma direto 0,018; combinado 0,008 sobrepõe SN/dualidade. A identidade de traço sozinha não deriva a lei cosmológica; gamma=beta não derivado. |
| R-G | FD=fl fs/fls; fphi=DeltaPhi_fit/DeltaPhi_true; **Hfit/Hbg=fphi/(ft FD)**. | [DERIVED condicional / OPEN ponte] sigma maior TDCOSMO 3,9; depende de Pantheon+ para Omega_m. A errata seq393 prevalece sobre a expressão ambígua anterior. |
| R-L | Com sigma8 fixo: sqrt(1+beta)−1=0,599766%; em S8=0,8, Delta=0,004798. | [DERIVED aritmético / OPEN dinâmica] Proxy Delta/0,021=0,2285. Falta P(k,z), mu, slip, normalização e operador observacional; não determina sinal da tensão física. |
| R-J | Gamma=.5 beta tau* omega²; tau*=tP e 100 Hz dão 1,28036e−40 s⁻¹. | [DERIVED condicional] Duas leituras não derivam outra escala dimensional. P1/P2/P3 não foram reabertas. |
| R-K | m2=beta sin45° vezes 1 eV=8,507414 meV; m1=0, NO dão Dm21²=7,2376095e−5 eV². | [DERIVED de POSTULATE/NORM] sigma JUNO=0,12e−5; LCDM não fixa splitting. Soma aposentada por D2 preservada; teste vigente pede determinações autônomas. |

## Verificação numérica da forma

[derivacoes/poder_forma/NOTA_PODER_FORMA.md](</C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/poder_forma/NOTA_PODER_FORMA.md>) utiliza somente redshifts, tipos e covariâncias publicadas, sem centros observados. Foram conferidas as identidades das matrizes; a amostra SN tem 1580 **linhas de curvas de luz**, não necessariamente 1580 objetos independentes. A projeção por Cholesky/SVD remove amplitudes e a tangente de Omega_m.

- Mapa A (implementado): SN D=0,183 com amplitude livre; D=0,030 com amplitude e Omega_m. BAO não recebe sinal beta, mas restringe Omega_m comum: conjunto D=0,164, com amplitudes próprias.
- Mapa B (hipotético comum): conjunto D=0,294 após nuisance; eta=1. Este cenário não foi adotado como previsão da TGL.
- A covariância cruzada SN–BAO foi assumida zero neste planejamento. A hipótese e os nuisance congelados delimitam os números.

Estas são separações gaussianas esperadas condicionais, não z-scores observados nem probabilidades de detecção. Não se promete um calendário Euclid/DESI-Y5 com base em reduzir matematicamente todas as barras.

## Revisão e alcance da conclusão

[proveniencia/REVISAO_ADVERSARIAL_F2.md](</C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/proveniencia/REVISAO_ADVERSARIAL_F2.md>) conferiu as derivações e encontrou uma convenção ambígua de lentes. [derivacoes/ERRATA_R_G_FPHI.md](</C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/derivacoes/ERRATA_R_G_FPHI.md>) a resolve: se o potencial reconstruído dobra com os outros fatores unitários, Dfit cai à metade e Hfit dobra. A expressão antiga foi preservada como história e recebe a correção ao lado. Os casos fphi=1 não mudam.

[proveniencia/REVISAO_PODER_FORMA.md](</C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/proveniencia/REVISAO_PODER_FORMA.md>) realizou 51 verificações independentes; diferença máxima nas distâncias gaussianas 5,8e−9. A análise inicial tem 54 verificações; o forecast, 57. São verificações diferentes, não um placar de comprovação física.

Mapa: R-D/E/F/G/L/J/K seq376–382; forma seq389–390; revisão seq391; errata seq393; revisão de forma seq394. Nenhum executor remoto nesta subtarefa, request_ids despachados=[]; assistência Work ausente. **F2 está entregue como investigação das sete rotas, incluindo seus itens OPEN; não declara fechadas as pontes observacionais.**
