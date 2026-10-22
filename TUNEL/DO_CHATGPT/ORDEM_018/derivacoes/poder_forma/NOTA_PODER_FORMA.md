# PODER DA FORMA Q(z) — adendo R-D/R-E da ORDEM_018
[DERIVED condicional; REAL da execução local] 06/10/2026 UTC. Identidade: chatgpt-codex/ordem-018/derivacoes.

A forma integrada Q(z) contém informação independente da amplitude, mas pouca nesta covariance: Pantheon+ dá distância esperada D=0,18321 depois de remover M/H0/K*, e D=0,03021 permitindo também Omega_m em aproximação tangente. DESI pode restringir o fundo sem receber um sinal K: no mapa atual de luminosidade, o conjunto chega a D=0,16396 com as duas amplitudes livres e Omega_m compartilhado. Não são pulls de dados, significâncias observadas ou vereditos.

## Escopo, fontes e seleção
A coordenação solicitou este cálculo novo de poder da forma, não repetição dos fits antigos. O mapa foi consultado antes; PLANO_ANTES_DO_PODER.md e ADENDO_FONTES_ANTES_DO_PODER.md foram gravados e hasheados antes de executar forecast_shape.py. Obstáculos, pelo menos duas alternativas e critério de medida estão fixados no plano. Os resultados históricos da Fase5 permanecem intactos.

As fontes foram verificadas por bytes: Pantheon+ tabela e covariance STAT+SYS coincidem com o release público conforme recibo da coordenação, novamente conferido pelo script; DESI covariance coincide com o arquivo do release Cobaya baixado nesta rodada. O registro FONTES_COVARIANCIAS_METADATA.json contém hashes calculados e URLs. Isto estabelece identidade das fontes atuais, não demonstra qual arquivo uma execução histórica usou.

Foram convertidos somente zHD, zHEL e IS_CALIBRATOR da tabela SN; no DESI, apenas z e tipo de distância, colunas0 e2. Valores centrais não entram no código nem no JSON. O parser recebe bytes das tabelas para extrair metadados; não alegamos ignorância do conteúdo público nem cegueira de toda a sessão. Os centros enviados depois pela coordenação para outra reprodução não foram usados.

A seleção SN congelada é zHD>0,01 e IS_CALIBRATOR=0: **1580 linhas**, entre zHD=0,01016 e2,26137. São linhas de curvas de luz, não uma contagem de supernovas únicas. Calibradores são excluídos mesmo se acima do corte. Portanto o N não deve ser confundido com1593 de outra máscara histórica. A covariance inclui correlações de medidas repetidas; não deduplicar por nome silenciosamente.

O DESI tem13 componentes correlacionadas (DV, DM, DH por r_d) até z2,33. A documentação primária especifica a ordem e o formato:
- [Pantheon+ release: distâncias e covariâncias](https://github.com/PantheonPlusSH0ES/DataRelease/tree/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR).
- [DESI DR2 no release Cobaya](https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2).

## O que é derivado e o que é hipótese
Com FRW plano e rho+p>=0, k=E^(2beta/3), beta=alpha_CODATA2018*sqrt(e) em runtime. As duas leituras do motor dão
D_M,s=(c/H0)/K* integral du/E;
D_M,ac=(c/H0)/K* integral k du/E;
Q=D_M,ac/D_M,s=(integral k/E)/(integral1/E).
Assim dL_ac/dL_s=Q, e o sinal de magnitude é5log10Q. O fator (1+zHEL) cancela. Usar k(z) em vez de Q(z) seria trocar taxa pelo caminho integrado.

A amplitude constante K* cancela nesta razão e entra no mesmo espaço de nuisance de H0/M. A covariância não separa tais amplitudes sem informação externa. O regime da face e a projeção angular não são identificados por esta parametrização; nenhum lema formal é ampliado.

**Mapa A — recorte implementado no motor:** somente o canal de luminosidade recebe a leitura acumulada; BAO permanece no fundo nu. Então o sinal direto de BAO ézero. Se dA fica geométrico, eta_ac/eta_s=Q; o valor absoluto de eta depende da normalização e do mapa de leitura. Não se demonstrou absorção de fótons ou violação de reciprocidade.

**Mapa B — extensão adicional para diagnosticar dependência do mapa:** transporte comum de distâncias e taxa. D_M e dA recebem Q, D_H recebe k, D_V recebe Q^(2/3)k^(1/3); dL=(1+z)^2dA preserva eta=1. Este B não é previsão já adotada pelo motor nem novo candidato selecionado pelos dados. Os dois mapas exibem por que K sozinho não fixa a dualidade.

Fiduciais de planejamento, não ajustes: H0=70 km/s/Mpc, Omega_m=0,3, Omega_r=9e-5, r_d=147 Mpc. A amplitude comum BAO é normalizada no fiducial e o fator constante K* pode ser absorvido nela; nenhum K* é calculado aqui. Com covariance dimensional fixa, os números B dependem da amplitude fiducial, do mapa e do fundo; não são limites universais da TGL. A radiação baixa foi incluída para alinhar ao F0 da coordenação, distinta da ilustração Or=0 no relatório F2 anterior.

## MEDIDA
Para sinal s e matriz de nuisance J:
W=C^-1-C^-1 J(J^T C^-1 J)^-1 J^T C^-1,
D=sqrt(s^T W s).
Implementação: Cholesky para branqueamento e SVD para projeção, sem inversão de C. D é distância gaussiana esperada entre templates com covariance fixa. A aproximação tangente de Omega_m não constitui ajuste não linear nem veredito sobre o céu.

| Canal/mapa | amplitudes fixas (diagnóstico) | amplitudes comuns removidas | também Omega_m tangente livre |
|---|---:|---:|---:|
| SN, forma Q |0,304460|0,183211|0,030213|
| BAO, mapa A do motor |0|0|0|
| SN+BAO A |0,304460|0,183211|0,163963|
| BAO, mapa B hipotético |1,414726|0,808383|0,221368|
| SN+BAO B hipotético |1,447116|0,828885|0,293649|

No conjunto, o intercepto SN e a amplitude BAO são independentes e Omega_m é compartilhado. Crosscovariance SN–BAO=zero é hipótese explícita. DESI A restringe a mudança do fundo que poderia imitar Q nos SNe, por isso o conjunto conserva mais informação que SN sozinho com Omega_m livre. Não foi acrescentado um sinal BAO inexistente.

A projeção de amplitude retém36,21% de D² SN; amplitude+Omega_m retêm0,985% do diagnóstico com amplitude fixa. O efeito é pequeno e grande parte é degenerada com parâmetros comuns. Isso é resultado de poder, não ausência de solução matemática nem teste negativo da natureza.

Como escala ideal, reduzir TODA a covariance SN de forma uniforme (incluindo sistemáticas) exigiria melhoria de sigma27,29 vezes para D=5 com apenas intercepto livre, ou165,49 vezes com Omega_m livre. Para o conjunto A completo o fator ideal é30,49. Estes fatores não são previsão de levantamento, cronograma ou simples aumento de N: sistemáticas/correlações podem impedir essa redução. Não há alegação de capacidade em2027/2030.

## Verificação e limites
Python3.14.3 normal usuário; NumPy2.4.3; SciPy1.18.0. Tempo interno0,560s;57 checks passaram. Quadraturas64/128 nós diferiram no máximo6,66e-16 em Q. Reduzir passo da derivada Omega_m de1e-4 a5e-5 mudou dmu/dOmega_m em3,27e-8 e dy_BAO/dOmega_m em9,25e-7. Covariâncias selecionadas simétricas e Cholesky positivo, sem reparar autovalores. Controle de sinal puramente constante SN e escala comum BAO desapareceu até D<7e-14.

Não foram importados/executados um.py ou os motores da Bancada. Não houve chamada a executor, upload científico privado, ajuste de beta/rd/Om ao dado, calibração SH0ES ou centro Planck. O mapa físico único para R-E continua [OPEN]. Para transformar o forecast em teste físico é necessário fixar esse mapa, independências, sistema de calibração e nuisances admissíveis, com função de veredito separada. O pré-registro aqui vale para esta conta de poder.

Artefatos: forecast_shape.py; PODER_FORMA.json; TEMPLATES_SEM_CENTROS.json; metadados filtrados e covariâncias; planos; recibos de proveniência e consulta de mapa; manifesto de hashes. Não alteram kernel, gate, originais ou resultados históricos. A coordenação/gerência deve revisar antes de qualquer integração canônica.
