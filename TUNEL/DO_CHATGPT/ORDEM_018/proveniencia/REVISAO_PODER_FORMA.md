# Revisão independente da separação esperada da forma Q

[REAL da auditoria local / DERIVED condicional] ORDEM_018. Revisora: chatgpt-codex/ordem-018/proveniencia. 2026-10-06T00:47:18.829670+00:00.

## Achados primeiro

**Nenhum erro numérico ou desalinhamento entre template e covariância foi identificado no escopo examinado.** Os números podem ser apresentados como **separação gaussiana esperada condicional entre templates**, após remover os parâmetros indicados, com covariância fixa no fiducial.

**FORMA-REV-01 — P3, terminologia:** o título da entrega e a frase “Isso é resultado de poder” na linha 50 de NOTA_PODER_FORMA.md podem sugerir poder estatístico probabilístico. O corpo e o protocolo já delimitam corretamente D e excluem significância observada, probabilidade de detecção e veredito. Recomenda-se usar “separação esperada condicional” também no título e nessa frase. Esta ressalva não invalida os valores publicados nem exige repetir o cálculo.

D não é um pull observado: nenhum vetor de resíduos em relação aos dados foi empregado. Também não é, sozinho, poder de teste. Seria necessário definir estatística, hipóteses e regra de rejeição. Como ilustração matemática restrita a um contraste gaussiano direcional com variância unitária, a potência seria Phi(D−c) para um limiar c; D sozinho não especifica c. Isso não adota um novo teste para a missão. D=5 tampouco constitui uma detecção observada ou uma garantia de detecção.

## Projeção de amplitude e Omega_m

[DERIVED] A métrica implementada corresponde ao mínimo quadrático local:

D² = min_a (s−Ja)^T C^−1 (s−Ja).

Com C definida positiva, a solução a=(J^T C^−1 J)^−1 J^T C^−1 s produz o W escrito no protocolo. Branquear por L^−1, onde C=LL^T, e retirar as colunas de L^−1J por SVD é uma implementação correta. A revisão usou outra solução: equações normais GLS com solves de Cholesky, resíduos explícitos e derivadas analíticas de Omega_m.

No SN, o intercepto constante representa o espaço degenerado de M/H0/K*. A tangente dmu/dOmega_m atua na forma, mantendo o restante do fundo fixo. No BAO, uma escala comum tem vetor y_bg, porque as razões DM/r_d, DH/r_d e DV/r_d variam todas pela amplitude inversa H0*r_d; normalizar sua parametrização de outro modo não altera o espaço projetado.

No conjunto, as colunas são corretamente [1_SN,0_BAO], [0_SN,y_BAO] e [dmu_SN/dOmega_m,dy_BAO/dOmega_m]. Há duas amplitudes livres e **um** Omega_m compartilhado. Não foram acidentalmente impostos uma calibração comum de amplitude ou dois fundos independentes.

A palavra “marginalização” só tem aqui alcance gaussiano linear com prior plano e espaço tangente fixo. O programa calcula a norma residual, não uma evidência bayesiana com priors normalizados, posterior ou perfil não linear. A distância local não certifica a separação global entre duas famílias cosmológicas curvas.

## Correspondência entre modelos, linhas e covariância

[REAL] A revisão conferiu os bytes de origem, a extração restrita de metadados, a máscara e a ordem:

- Pantheon+: 1701 linhas antes do corte; 1580 com zHD>0,01 e IS_CALIBRATOR=0. Os índices zero-based dos templates coincidem exatamente com as linhas selecionadas; a submatriz usa os mesmos índices em ambos os eixos. São medidas de curvas de luz, sem deduplicação implícita.
- DESI: as 13 componentes mantêm a ordem da tabela de origem, inclusive DH e depois DM em z=2,33. Os tipos escolhem o template correspondente; as barras guardadas coincidem com a raiz da diagonal da covariância na mesma ordem.
- Os vetores SN estão em magnitudes e usam covariância de magnitude ao quadrado. BAO compara DM/r_d, DH/r_d ou DV/r_d com a covariância desses mesmos observáveis adimensionais. H0, c e r_d têm unidades compatíveis de km/s/Mpc, km/s e Mpc.
- Ambas as matrizes selecionadas são simétricas, finitas e admitem Cholesky sem reparação de autovalores. O bloco cruzado SN–BAO nulo permanece uma hipótese declarada, não uma independência demonstrada por essa conferência.

[DERIVED] O sinal SN é 5log10 Q, com Q=integral(k/E)/integral(1/E). O fator heliocêntrico e K* cancelam na razão ac/sombra. A revisão reconstruiu as integrais por quadratura adaptativa e calculou dI/dOmega_m = −(1/2)integral[((1+u)^3−1)/E³]du; daí dmu/dOmega_m=(5/ln10)(dI/dOmega_m)/I. No BAO, derivou DM, DH e DV analiticamente no mesmo fundo.

O mapa A tem sinal BAO **zero**. A informação DESI ainda limita a mudança de Omega_m que poderia absorver o sinal SN: isso explica o aumento de D conjunto em relação a SN com Omega_m livre. Não significa que DESI recebeu um sinal K. O mapa B acrescenta a hipótese DM→Q DM, DH→k DH e DV→Q^(2/3)k^(1/3) DV, preservando dualidade se ambas as distâncias compartilham o transporte; seus números não são promovidos à previsão do motor A.

## Resultado da conferência independente

| Canal | Sem projeção | Amplitudes livres | Também Omega_m tangente |
|---|---:|---:|---:|
| SN | 0,304460111 | 0,183210987 | 0,030213463 |
| SN+BAO A | 0,304460111 | 0,183210987 | 0,163963115 |
| BAO B hipotético | 1,414725511 | 0,808383241 | 0,221368370 |
| SN+BAO B hipotético | 1,447115832 | 0,828884630 | 0,293649418 |

[REAL] **51 verificações passaram**, com 21 arquivos-fonte registrados por SHA-256. A diferença máxima entre D independente e publicado foi **5,717978202035567e−9**, decorrente da substituição da diferença finita por derivadas analíticas. As discrepâncias máximas foram 6,66e−16 em Q, 1,45e−15 mag no sinal SN, 1,09e−8 em dmu/dOmega_m e 3,08e−7 em dy_BAO/dOmega_m. Os controles de intercepto SN e escala BAO foram anulados numericamente. Não foi executado o script do autor para obter esses resultados.

As frações retidas são frações de D², não de D. Os fatores ideais 5/D têm o alcance declarado: ao substituir **toda** a matriz relevante por C/f², D cresce por f. Para o conjunto A, o fator 30,49 requer essa redução uniforme no bloco conjunto inteiro, inclusive BAO e sistemáticas; não é o efeito de melhorar só SN, aumentar N ou esperar um ano específico. A comparação permanece condicionada ao fundo fiducial, ao mapa, à amplitude fiducial BAO, às covariâncias fixas e aos parâmetros livres escolhidos antes da conta.

## Proveniência e limites

Fonte examinada: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\derivacoes\poder_forma\NOTA_PODER_FORMA.md, 7654 bytes, SHA-256 `10c50944bd5c7de29023b8d63a8bf6e2d2d61d88157943e266d07ea4833c163a`. Planos, script, JSON, templates, metadados, matrizes e recibos estão identificados em **REVISAO_PODER_FORMA.json**; o código independente é **review_shape.py**.

Os hashes locais coincidiram com o manifesto, com os pins do resultado e com o recibo capturado das fontes públicas. Não houve nova consulta remota: a revisão não certifica a versão atual de um servidor nem reconstitui uma execução histórica. Conferir o hash do plano preservado também não é prova independente da cronologia de pré-registro; o guard de mtime do autor não demonstra por si só anterioridade a toda a sessão.

Foram lidos bytes de tabelas para hash e extração das colunas de metadados; nenhum centro observado foi convertido para número, exibido ou usado em cálculo. Nenhum original ou código do autor foi executado/importado; não houve ajuste a dados, chamada a provedor, abertura de rito, alteração de originais ou movimento de gate. O resultado revisto é separação esperada condicional, não veredito sobre a natureza.
