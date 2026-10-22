# F8.2.NU2 — disponibilidade de dados de neutrinos, R1

Unidade reivindicada pela coordenação, evento 618. Autor: Codex / nu2_data_sources. Consulta em 09/10/2026.

## O que a casa já tem

[REAL documental] O Nós Vivo F7.2 foi consultado antes desta nota; devolveu F7.2 FECHADA e localizou as tabelas do canal n=-2. A TABELA_DE_PODER_POR_CANAL_V2.md foi lida: ela já registra o limite JUNO e mantém SEM_LIMITE_TGL até ligar operador e likelihood. Reaproveitamos esse alcance. Seu antigo estado de staging não é usado; a âncora vigente da Eq.(6) é III.B. Caminho, hash lido dos bytes e recibo da consulta estão no JSON vizinho.

## Seis entradas primárias

1. **JUNO 59,1 dias.** [Artigo Nature](https://www.nature.com/articles/s41586-026-10538-z), publicado em 10/06/2026. Data availability oferece source data de Fig.3,4 e Extended2; código e dados brutos não são públicos. Há link de ZIP suplementar, mas seu conteúdo não foi conferido (o clique pelo navegador de pesquisa falhou). [OPEN] Matriz completa de resposta/covariância e likelihood do pacote.
2. **JUNO atualizado.** [arXiv:2609.37895v1](https://arxiv.org/html/2609.37895v1), 29/09/2026: 207,2 dias e 8.294 candidatos, ajuste conjunto JUNO–TAO–Daya Bay. Eq.(1) explicita resposta, covariâncias e nuisances. Não localizamos release numérica correspondente nesta consulta. Isso não prova inexistência. Não se substitui a exposição no limite de junho sem reanálise.
3. **KamLAND oficial.** [Coleção 2013](https://www.awa.tohoku.ac.jp/KamLAND/2013_result_data_release/2013PRD.html) anuncia mapa chi-quadrado usual (57 MB). A [release 2011](https://www.awa.tohoku.ac.jp/KamLAND/4th_result_data_release/4th_result_data_release.html) anuncia histograma observado/predições/fundos com eficiência incorporada. A [release 2005](https://www.awa.tohoku.ac.jp/KamLAND/datarelease/2ndresult.html) anuncia energias individuais, livetime mensal, fundos, fissão e resolução aproximada. Nenhuma tabela de eventos foi baixada. [DERIVED] Mapa apenas nos parâmetros usuais não é likelihood em Gamma; recálculo exige reproduzir o padrão.
4. **Textura do limite JUNO.** [Beccaria–Ternes](https://arxiv.org/html/2606.13362v1), 11/06/2026, §§II,III.B,IV.B: GLoBES, Poisson+pulls e comparação com/sem prior solar. O limite 4,1e-27 GeV,90%CL,Delta chi2=2,71 é para gamma21=gamma31,gamma32=0,n=-2,E0=1GeV. [DERIVED] O duplo comutador com H geralmente tem gammaij proporcional a (Delta mij^2)^2. Coincidência do expoente não transfere a cota à TGL.
5. **Ia simulada.** [Wright2016 v2](https://arxiv.org/html/1605.01408v2), §IV.1 Eq.(10): propagação ao detector já decoerida na base massiva. A Tabela2 prevê para JUNO-like 0,014/0,032 interações NMO/IMO a10kpc, antes de perda por eficiência, no modelo N100nu. Não localizamos arquivo de fluxo N100nu nem amostra observada conjunta Ia–neutrinos–bolometria. [DERIVED condicional] Dephasing adicional na mesma base após decoerência completa não altera populações. Produção/matéria são rotas diferentes.
6. **Ferramenta de previsão.** [SNOwGLoBES](https://github.com/SNOwGLoBES/snowglobes): código,seções de choque,eficiências e smearing; listagem fluxes com Livermore/GKVM e gerador pinched. N100nu não apareceu nessa listagem. Repositório não foi clonado,pinado ou executado. Respostas são representativas; não certificam a resposta detalhada do aparelho.

## Alcance e próximo passo

[REAL documental] Consultamos HTML/artigos e metadados das releases. Nenhum evento,histograma bruto ou matriz experimental foi aberto para ajuste. Não há hash alegado dos downloads externos porque os bytes não foram custodiados nesta unidade; os URLs e limites de acesso estão explícitos. Foram escritos apenas artefatos derivados novos nesta pasta. Originais,memórias,Bancada e kernel não foram alterados.

[PROPOSTA] Derivar primeiro a textura de taxas TGL e medi-la no sintético de reatores. A rota Ia requer fluxo de produção e tratamento em matéria; as fontes consultadas não entregam uma amostra observada conjunta para esse teste. Nenhum limite publicado foi convertido em significância TGL, e não se obteve 5sigma nesta etapa.
