# F9 — contrato numérico para mínimos globais e integrais relativas

Unidade b5fe6406-4430-48a0-bc59-e58f68917c12, 06/10/2026. **[DERIVED — especificação condicional; INPUT — proposta não ratificada]**. Preparação documental/simbólica: nenhum centro observado, solver, ajuste, quadratura, controle sintético ou chamada externa executado. Os cinco modelos, os priors integrais, a família finita de cenários, o nulo, alpha e a abertura §6 permanecem os do rascunho pinado.

## 1. O que já existe e a decisão recomendada

A busca foi delimitada aos documentos admitidos pelo pedido e pelo RESOLUTOR_F9. A prova da cota já contém L_i≤g_i≤U_i, envoltórias externas, testemunha factível, regra de cauda e distinção entre limite conservador e ausência de calibração. A montagem e a medida nuisance já fornecem a integral gaussiana plana. O protocolo de fundo já recusa likelihood zero por falha. **Reutilizar essas peças; não escrever outro teste físico, outra cota de cauda ou outro motor cosmológico.** Não foi localizado nesse recorte um contrato completo de células, oráculos, propagação de erro e integral relativa com saída verificada. Isso não afirma inexistência em todo o acervo.

| Alternativa | Produto | Requisito ainda não satisfeito pelas fontes | Utilidade imediata |
|---|---|---|---|
| A — limites validados em todo o domínio | Intervalos que contêm o mínimo e a integral, com prova de cobertura e arredondamento dirigido | Envoltórias do motor contínuo, suporte/métrica validados e integrador com resto limitado | Interface concreta abaixo; pode ser testada com funções sintéticas conhecidas |
| B — cálculo adaptativo de engenharia | Estimativas, dispersão entre resoluções e erro não limitado explicitamente marcado | Não possui automaticamente certificado global ou erro uniforme do CAMB | Exploração computacional e planejamento; resultado inconclusivo onde o certificado é necessário |

**Recomendar B como implementação inicial, com interface A obrigatória e um verificador independente de certificados.** B pode localizar pontos e sugerir células para A. Somente o verificador promove um intervalo a certificado. Não é necessário provar a natureza para implementar o experimento gaussiano declarado. É necessário distinguir o cálculo desse experimento da adequação de sua lei ao processo físico. Nenhuma execução, implementação científica ou adoção é autorizada por esta preparação.

## 2. Alvo fixo e contratos tipados

Para cada cenário s e modelo i, sejam D_i o domínio físico completo, C_s a covariância estipulada comum, X o projeto comum e y o vetor futuro. Sob as condições já estabelecidas de suporte afim comum, X no suporte e posto63:

\[
q_{i,s}(\xi)=\inf_{\eta\in\mathbb R^{63}}(y-\mu_i(\xi)-X\eta)^TC_s^+(y-\mu_i(\xi)-X\eta)
=\|R_s(y-\mu_i(\xi))\|^2,\qquad g_{i,s}=\inf_{\xi\in D_i}q_{i,s}(\xi).
\]

R_sX=0 e R_sC_sR_sᵀ=I no quociente. A igualdade exige que as restrições determinísticas sejam satisfeitas. Não criar jitter, truncar autovalores positivos, eliminar linhas ou projetar uma violação para fazê-la desaparecer. Usar inf evita pressupor que um otimizador já encontrou o mínimo; continuidade no compacto, quando demonstrada, garante atingimento.

As interfaces futuras, ainda sem implementação, são:

- `qualify_geometry(s, contract_pins) -> GeometryCertificate`: suporte, posto, X, métrica, normalização comum, aritmética e sua evidência.
- `enclose_prediction(i, cell, geometry, engine_pin) -> CertifiedMeanEnclosure | UnboundedTheoryError | ComputationalFailure`. Um valor float isolado não implementa a primeira alternativa.
- `bound_profile(i, cell, geometry, mean_enclosure) -> CellBounds`: q_lower≤q(ξ)≤q_upper para TODO ξ na célula, mais método/prova; infinito superior é permitido e explícito.
- `certify_witness(i, point, ...) -> WitnessUpper | UncertifiedEstimate`: ponto factível e limite superior de seu q verdadeiro, não somente retorno do minimizador.
- `verify_cover(domain, cells, prune_ledger) -> CoverageCertificate`: cobertura exata de todo D_i, incluindo fronteiras para mínimos; particionamento sem duplicação de massa para integrais.
- `assemble_minimum(...) -> MinimumInterval`; `integrate_prior_bounds(...) -> RelativeIntegralInterval`; `compare_models(...) -> PairwiseIntervals`. Cada consumidor verifica os pins e os certificados de que depende.

Registros têm request/unit IDs, modelo, cenário e hash da LISTA INTEIRA de cenários, alvo/engine/configuração, domínio/prior, unidades, X/C/suporte, célula ou testemunha, bounds, precisão, método, dependências, validade e evidência. Não basta verificar hashes dos itens presentes se a lista puder ser encurtada. Campo estimado e campo certificado são separados. JSON usa null e um tipo explícito para infinito/indisponível; NaN, Infinity literal e string numérica inválida são recusados.

## 3. Cobertura completa e mínimos certificados

Mapear os priors físicos uniformes para u∈[0,1]^d por transformações afins exatas nas coordenadas originalmente escolhidas. H1/H2 têm d=3; H3/H4/H5 d=4. Manter H4 em s e H5 em rd_livre para evitar alteração acidental do prior. A malha adaptativa subdivide caixas diádicas nessa representação; limites racionais permitem verificar cobertura sem tolerância geométrica inventada.

Para uma cobertura finita B_k de TODO D_i, com \(\ell_k\le\inf_{B_k}q\), e testemunhas factíveis ξ_j com q(ξ_j)≤u_j:

\[
L_i=\max(0,\min_k\ell_k),\qquad U_i=\min_j u_j,\qquad L_i\le g_i\le U_i.
\]

Sem testemunha validada, U_i=+∞. Sem limite local informativo, usar ℓ_k=0 por não negatividade, com a razão registrada. Isso fornece limite trivial válido no experimento qualificado; não certifica um ótimo numérico nem resolve outras hipóteses ausentes. Um otimizador local gera propostas de testemunha: sua tolerância, multistarts e concordância não são prova de L_i, e seu float só vira U_i depois de incluir erro de avaliação/viabilidade.

Uma célula pode ser podada para o mínimo se seu limite inferior certificado não for menor que U corrente. Conservar o certificado de poda e toda a árvore de cobertura. **Célula podada para o mínimo continua contribuindo para a integral.** Um mínimo na fronteira não desaparece porque essa fronteira tem medida zero para Bayes. Uma união incompleta de células não fornece L global; completar a região omitida com limite0 mantém cobertura e informa a frouxidão.

### 3.1 Envoltórias da média

No quociente exato, x=R_sy, m_i=R_sμ_i. Se m_i(B) está contida na bola de centro c_B e raio ρ_B, então

\[
\ell_B=\max(0,\|x-c_B\|-\rho_B)^2.
\]

Todos os termos recebem arredondamento externo. Uma caixa que contém o resíduo inteiro fornece limites por componente: distância de cada intervalo a0 para a soma inferior dos quadrados e máximo de módulo para a superior. Dependências ignoradas alargam a caixa, não invalidam uma inclusão realmente demonstrada.

Uma cota de Lipschitz pode construir ρ_B a partir de um ponto e diâmetro da célula, **desde que a constante seja limitada uniformemente na célula** e o erro no ponto seja certificado. Diferenças finitas ou gradientes amostrados não demonstram essa constante. Pode-se reutilizar a inclusão global B17/B18 como envoltória afim mais frouxa, quando validada: a distância ao espaço afim externo dá um limite independente de cobertura fina do motor, mas não uma testemunha superior.

### 3.2 Certificado dual opcional sem pseudoinversa explícita

Para b=y−μ e qualquer vetor v com Xᵀv=0 **exatamente**, vale

\[
q(b)\ge 2v^Tb-v^TC_sv.
\]

Prova: para resíduo admissível e=b−Xη no suporte, \((e-C_sv)^TC_s^+(e-C_sv)\ge0\) implica eᵀC_s⁺e≥2vᵀe−vᵀC_sv; Xᵀv=0 remove η; tomar inf preserva a desigualdade. Uma avaliação intervalar inferior dessa expressão em uma célula fornece ℓ_B; combinar vários v pelo máximo e com0. O vetor pode ser proposto por engenharia, mas o anulamento deve ser verificado exatamente ou por uma representação no núcleo exato de Xᵀ. Com η irrestrito, um resíduo apenas pequeno em Xᵀv não tem erro uniformemente limitado: não usar tolerância como substituto.

## 4. Erros de C, suporte, nuisance e previsão

Separar três objetos: (a) C exata escolhida para o experimento; (b) erro numérico ao representar/fatorar essa C; (c) diferença eventual entre C escolhida e a covariância física. Aqui certifica-se (b); (c) continua no contrato estatístico/sistemático existente, sem novas exigências ou cenários inventados.

O núcleo deve vir das relações estruturais e a positividade do complemento de um limite espectral verificado. Em uma base comum do suporte, seja Ĉ uma matriz de referência com limite inferior certificado λ para seu menor autovalor e \(\|C-\widehat C\|\le e_C<\lambda\). Então

\[
\|C^{-1}-\widehat C^{-1}\|\le\frac{e_C}{\lambda(\lambda-e_C)}.
\]

A fórmula refere-se às restrições invertíveis no MESMO suporte, não à pseudoinversa através de mudança de posto. O limite λ não é autovalor float sem margem. Se a lacuna espectral não é qualificada, manter a falha; não deduzir posto de um cutoff escolhido para fechar o teste.

Alternativamente, se \((1-\epsilon)C_0\preceq C\preceq(1+\epsilon)C_0\), 0≤ε<1, no mesmo suporte, então, para o mesmo b e X,

\[
q_{C_0}(b)/(1+\epsilon)\le q_C(b)\le q_{C_0}(b)/(1-\epsilon).
\]

As desigualdades valem para cada η antes do inf, logo passam ao perfil. Isso é propagação numérica de uma inclusão comprovada, não ratificação de uma C física desconhecida.

Se um R̂ nas MESMAS coordenadas do quociente satisfaz \(\|R-\widehat R\|\le e_R\) e \(\|b-\widehat b\|\le e_b\), então

\[
\|Rb-\widehat R\widehat b\|\le e_R\|\widehat b\|+(\|\widehat R\|+e_R)e_b=\delta.
\]

Com n=‖R̂b̂‖ validado, q está em \([\max(0,n-\delta)^2,(n+\delta)^2]\). Erros do núcleo nuisance, solução linear e ortogonalização entram em e_R ou em outra prova direta; não desaparecem com QR/SVD nominal. X deve conservar seus coeficientes exatos estipulados. Alterar X, a_h ou c_C para acomodar erro é alteração do experimento, não arredondamento.

O oráculo do motor deve limitar todos os campos usados e suas operações: H/E, distâncias, rstar/rdrag distintos, zstar térmico, E no z_lei fixado e mapas h_local. Denominadores têm de ficar afastados de zero; logaritmos precisam de domínio positivo certificado. β fixa é sempre α_CODATA2018×sqrt(e), com a representação/arredondamento documentados; não substituí-la por valor decimal memorizado. H3 conserva seu prior e o nesting exige conferir a presença do valor fixo nele.

O piloto CAMB pinado relata dez unidades em cinco pontos, duas precisões, `full_prior_qualified=false`. Ele fornece evidência de engenharia naqueles pontos. Duas resoluções podem concordar e compartilhar o mesmo erro; não demonstram erro uniforme, resto de interpolação, derivadas ou cobertura de todas as células. Não repetir o piloto. Se não houver bound do motor, marcar `UnboundedTheoryError`; aumentar AccuracyBoost não muda esse estatuto por si só.

A aproximação física RECFAST/configuração adotada e o erro numérico ao resolver esse modelo são distintos. Pode-se investigar o experimento declarado sem certificar que ele é a natureza. Um eventual alvo definido como algoritmo float/emulador também deve ser explicitamente ratificado e identificado; não trocar silenciosamente o alvo contínuo por esse algoritmo para dizer que o erro desapareceu.

## 5. Integrais relativas: priors normalizados, medida nuisance comum

Preservar a proposta corrente, não impor novo prior próprio para os63 nuisance. Para o cenário fixo, com X/C/suporte comuns e independentes de ξ, a integração com a MESMA medida κdη produz

\[
J_{i,s}=\kappa A_s I_{i,s},\quad
A_s=(2\pi)^{-(r_s-63)/2}[\operatorname{pdet}(C_s)\det(X^TC_s^+X)]^{-1/2},
\quad I_{i,s}=\int_{D_i}e^{-q_{i,s}(\xi)/2}\pi_i(\xi)d\xi.
\]

Os priors FÍSICOS π_i são próprios/normalizados; κdη não é. I é uma integral dimensionless no experimento de quociente; J é evidência RELATIVA até a constante arbitrária comum κ, não evidência absoluta normalizada sobre η. Razões por cenário satisfazem B_ij=I_i/I_j porque A_s/κ cancelam simbolicamente sob as hipóteses verificadas. Não trocar a medida η por modelo nem por cenário para favorecer cancelamento. Sem fator comum, conservar os prefatores dentro de cada integral e rever o contrato.

O prior base é uniforme nas coordenadas (H0,wb,wc), [50,90]×[0,015;0,030]×[0,08;0,18], densidade50/3. H3 acrescenta β em[−0,05;0,05], densidade10; H4 s em[−0,15;0,15], densidade10/3; H5 rd em[130,160]Mpc, densidade1/30. A passagem afim ao cubo unitário absorve exatamente esses fatores: π_i(ξ)dξ=du. Não truncar caixas em ±nσ do melhor ajuste.

Se outra implementação usar δ_C=−5log10(1+s), transportar densidade \((\ln10/1,5)10^{-\delta_C/5}\) e extremos. Se usar q_d=rd/rd_CAMB(θ), transportar limites dependentes de θ e densidade rd_CAMB(θ)/30. O cubo nas coordenadas originais evita essas duas armadilhas. Nenhuma densidade nova é escolhida nesta unidade.

## 6. Quadratura validada e intervalos de Bayes

Se, em cada célula de uma partição de massa de prior w_k, \(q\in[\ell_k,u_k]\) para todo ponto, então

\[
I^- =\sum_k w_k e^{-u_k/2}\ \le I\le\ \sum_k w_k e^{-\ell_k/2}=I^+.
\]

As somas e exponenciais são calculadas com enclosures externos; massa total é1 por construção exata do particionamento. Uma regra de quadratura de ordem alta só estreita esses limites se apresentar resto certificado e hipóteses/derivadas válidas em cada célula. Diferença entre duas ordens/grades, ESS ou erro reportado por integrador comum não substitui esse resto. Refinar as células pela contribuição ao intervalo é adaptação computacional, não mudança do prior ou seleção de dado.

Numa célula sem previsão limitada, o bound seguro é q∈[0,+∞], portanto contribuição∈[0,w_k]. **Isso não significa likelihood zero.** Sua massa permanece no erro superior. Se o motor falhar, a falha continua visível mesmo que esse intervalo universal seja matematicamente válido para o modelo estipulado. Se a própria existência do alvo nessa região estiver indefinida, nem esse diagnóstico resolve o contrato: marcar alvo inválido/indefinido, sem renormalizar o prior restante.

Para mínimos, a mesma célula desconhecida tem ℓ=0 e pode impedir exclusão. Para Bayes, ela pode ter massa pequena e permitir um intervalo útil — sempre contabilizada. Uma célula com ℓ≥U_mínimo pode ser descartada da busca do mínimo, mas **não** da soma da evidência; sua contribuição tem de ser limitada e guardada.

Se 0<I_i^-≤I_i^+ e 0<I_j^-≤I_j^+, então

\[
B_{ij}\in[I_i^-/I_j^+,I_i^+/I_j^-],\qquad
\ln B_{ij}\in[\ln I_i^- -\ln I_j^+,\ln I_i^+ -\ln I_j^-].
\]

Limite inferior zero não autoriza log(0) como evidência medida: o intervalo correspondente é aberto/infinito explicitamente, com `insufficient_lower_bound`. Mesmo I>0 matematicamente pode exigir nova precisão para um limite inferior numérico positivo. Usar log-domain/escala comum e arredondamento externo; underflow não é massa zero comprovada. Um prefator comum muito incerto pode cancelar simbolicamente na razão, mas isso não cancela erro em q.

Se houver erro uniforme comprovado |q−q̂|≤ε_q, então \(e^{-\epsilon_q/2}\widehat I\le I\le e^{\epsilon_q/2}\widehat I\), além do erro de quadratura de Î. Erro só nos nós não demonstra essa relação. Para dois modelos, a incerteza de log-ratio recebe, no pior caso, a soma de seus semintervalos; correlação comprovada dos erros pode estreitar o cálculo conjunto, nunca um cancelamento presumido.

Reportar os cinco logJ até uma constante comum e as dez razões pareadas POR cenário. Faixa entre cenários é sensibilidade, não credibilidade; não promediar cenários sem pesos e não multiplicar razões baseadas nos mesmos dados. Nenhuma razão de Bayes vira sigma.

## 7. Conexão com a decisão F9 já existente

O contrato de mínimos alimenta a cota existente, preservando G1=g1, Q1=g1−g3, Tj1=gj−g1. Bounds inferiores: max(0,L1); max(0,L1−U3) apenas com nesting H1⊂H3; Lj−U1 para j=2,4,5. Diferenças usam arredondamento para baixo, sem substituir U por estimativa. Para intervalos superiores, usar U1−L3 e Uj−L1, com sinais/contenção coerentes; inconsistência entre bounds é erro visível.

A cauda SUPERIOR certificada já especificada na outra unidade consome esses limites; não se implementa aqui nova SF. Preservar graus residuais ou de span qualificados, caso dimensão0, cauda inclusiva, max sobre a família INTEIRA e Bonferroni5. Alpha5=erfc(5/sqrt(2))/2 não muda. Certificados determinísticos são a recomendação para não gastar alpha adicional. Certificado probabilístico, se posteriormente escolhido, precisa de falha total contabilizada no orçamento existente, e não acrescentada por fora.

Toda etiqueta de cenário precisa de resultado/certificado ou representação equivalente demonstrada. L=0 certificado pode levar a p_upper=1 válido e frouxo; isso difere de geometria inválida ou falta de calibração. Um cenário não calculado pode manter placeholder conservador1, mas não satisfaz por si só a completude/V2 nem produz não rejeição global. Não usar subconjunto disponível como família completa. Uma rejeição já válida de um dos controles H1 segue as regras independentes do V2; não apagar resultados válidos nem inventar os ausentes.

Não há tolerância de otimização universal que garanta decisão5sigma. Configurar ε_g e largura de logB como metas de eficiência, independentes da conclusão desejada; a decisão usa sempre os intervalos finais. Parar quando o orçamento acabar conserva intervalos válidos largos, estimativas separadas e lacunas. Não mudar alpha, rival, erro ou prior para atravessar um limiar.

## 8. Runtime e plano delimitado, sem campanha

O runtime CAMB é apenas o retrato pinado: WSL `/opt/lal_env/bin/python`, Python3.12.3 e CAMB2.0.4, com versões/configuração/bibliotecas conforme metadados. O recibo do piloto mede seu lote; não dá teto uniforme por célula nem orçamento de domínio inteiro. Não importar CAMB ou repetir controles para atualizar esses números nesta preparação.

Implementação futura precisa de: aritmética racional para domínios/cobertura; backend de intervalos com arredondamento externo e funções elementares certificadas; álgebra linear validada no suporte; armazenamento de DAG de dependências/células; oráculo de previsão com estatuto explícito; verificador separado que recusa bounds sem prova; cache por ponto/célula+modelo+configuração+precisão+hashes. Disponibilidade do backend validado não foi examinada/instalada aqui.

CPU determinística, uma thread inicial, precisão registrada. GPU pode apoiar visualização/propostas; não é certificado aritmético sem um backend qualificado. Claims persistentes antes de qualquer chamada e leitura de terminal em caso de incerteza reutilizam a infraestrutura existente. Nova execução só em unidade própria. Reutilizar resultado pinado idêntico não é rerodar unidade consumida.

`PLANO_SINTETICO_NUMERICO.json` delimita dez controles de contrato novos, sem CAMB, dados reais ou Monte Carlo de cauda. Propõe teto total180s,10s por unidade, uma thread,512MiB RSS e4096 células por caso; são **tetos propostos para controles sintéticos**, não estimativas de custo ou licença para F9 científico. Precisões128/256bits propostas; sem backend validado, resultado BLOCKED_DEPENDENCY. Bibliotecas, enforcement real de memória/tempo e prazo após persistência têm de ser qualificados antes; não afirmar enforce com medição somente posterior.

O plano não repete C01–C08, o piloto de dez CAMB, INIT003, controles de cauda/guard já consumidos ou a fila Claude bloqueada. Os recibos existentes são dependências, não convites à repetição. Não há comando de execução científica nesta entrega.

## 9. Estado desta entrega

Os documentos fornecem a interface, as provas condicionais dos bounds elementares, normalização relativa, estratégia de implementação e plano de controles. O JSON mantém todos os mínimos, matrizes, integrais, razões, likelihoods e significâncias observadas em null. Permanecem abertos a implementação/revisão do oráculo numérico, a qualificação das dependências e a adoção científica pela coordenação. Essas tarefas são distintas de provar a natureza.

O script de preparação somente verifica bytes/SHA e estrutura de documentos; não executa as fórmulas aqui expostas. Sua auditoria é de custódia/documentação, não teste de precisão, desempenho, cobertura física ou do solver. Originais, memórias compartilhadas e gate intactos.
