# F9 — cota finita conservadora de calibração

Unidade `6273a822-5880-4742-a82c-b7cf93f7c128`, 06/10/2026. **[DERIVED — prova condicional]**. Proposta documental para revisão independente, sem adoção do contrato, execução científica, leitura de centros, ajuste ou significância medida. Fontes e seus snapshots são enumerados em `SOURCES.json`.

**Resultado:** sob erro gaussiano com covariância fixa e conhecida, suporte comum e 63 nuisance lineares compartilhados, existe uma cota uniforme de cauda por qui-quadrado. Não exige Wilks nem Monte Carlo de cauda extrema. Para os contrastes, um segundo teorema substitui a dimensão residual pela dimensão de um espaço que contém TODAS as diferenças entre previsões. No recorte F9 atual, isso oferece cotas estruturais de **17 e 18** direções, ainda sem medir postos efetivos. A aplicação exige também um limite inferior certificado da estatística observada; um mínimo local de otimização não fornece esse limite.

## 1. Experimento ao qual a prova se aplica

Fixe primeiro um cenário de erros s, independente do dado que será usado no teste:

\[
Y=X\eta+\mu_i(\xi_i)+\varepsilon_s,
\qquad \varepsilon_s\sim N(0,C_s).
\]

Hipóteses suficientes:

1. As mesmas n observações, unidades e transformações são usadas nos modelos. C_s é simétrica positiva semidefinida, determinística, conhecida no modelo de amostragem, comum aos modelos e independente de seus parâmetros. Seu posto exato é r_s.
2. Todas as médias admitidas estão no mesmo suporte afim. Diferenças de médias e colunas de X pertencem a Range(C_s). Resíduos fora desse suporte são falha do contrato, não componentes a apagar com pseudoinversa.
3. X é fixo, tem p=63 colunas independentes no suporte e o domínio de eta é R^63. Há um único projeto nuisance comum. A normalização da densidade de amostragem sobre o suporte é a mesma nos modelos.
4. Sob o nulo testado, o parâmetro físico verdadeiro pertence ao domínio declarado. A média do erro é zero no contrato admitido; vieses não modelados não são automaticamente cobertos pela prova.
5. Seleção, cortes, compressão, conjunto de cenários e família de testes são fixados no contrato, ou seu efeito é incluído na calibração. Não trocar y, C ou X após procurar um resultado favorável.

Esta é uma afirmação sobre a distribuição de amostragem, **não** sobre amostrar eta de uma medida plana imprópria. Eta será eliminado por invariância. Não se usa nem se calcula evidência bayesiana nesta prova.

## 2. Eliminar eta: pivô exato no parâmetro verdadeiro

Escreva C_s=U_s Lambda_s U_s^T no suporte positivo e W_s=Lambda_s^{-1/2}U_s^T. Então W_s C_s W_s^T=I_r. Seja A_s=W_s X, P_s=A_s(A_s^T A_s)^{-1}A_s^T. Escolha B_s com colunas ortonormais que geram o complemento de Range(A_s), e defina R_s=B_s^T W_s. Assim,

\[
R_sX=0,\qquad R_sC_sR_s^T=I_{\nu_s},\qquad \nu_s=r_s-63.
\]

O RSS perfilado em eta, para um parâmetro físico fixo, é

\[
q_{i,s}(\xi)=\inf_\eta (Y-X\eta-\mu_i(\xi))^TC_s^+(Y-X\eta-\mu_i(\xi))
=\|R_s(Y-\mu_i(\xi))\|^2.
\]

Sob H_i no parâmetro verdadeiro xi_0, Z_s=R_s(Y−mu_i(xi_0)) é N(0,I_nu), independentemente de eta. Consequentemente,

\[
q_{i,s}(\xi_0)=\|Z_s\|^2\sim\chi^2_{\nu_s}.
\]

A igualdade é no **parâmetro físico verdadeiro**, não no mínimo ajustado. Não se subtraem mais três ou quatro parâmetros de nu com base apenas na dimensão da cosmologia. Ajustar esses parâmetros só fornecerá uma desigualdade.

## 3. Teorema da cota base para G, Q e T dirigido

Defina g_i=inf_xi q_i(xi), em um mesmo cenário. Os índices s ficam implícitos. Como q_i é soma de quadrados,

\[
0\le g_i\le q_i(\xi_0)\quad\text{sob }H_i.
\]

Com a mesma normalização de likelihood, as estatísticas do contrato são:

\[
G_1=g_1,\qquad Q_1=g_1-g_3,
\qquad T_{j1}=g_j-g_1\quad(j=2,4,5).
\]

Portanto G_1<=q_1(xi_0), Q_1<=g_1<=q_1(xi_0) sob H1, e T_j1<=g_j<=q_j(xi_0) sob Hj. A inclusão H1 em H3 garante Q_1>=0; a desigualdade superior não precisa dessa inclusão. T pode ser negativo.

Para t>0, cada estatística S, sob seu próprio nulo, satisfaz uniformemente:

\[
\boxed{\sup_{\xi_0,\eta}\Pr(S\ge t)\le \Pr(\chi^2_{\nu_s}\ge t).}
\]

Logo p_bound(S)=SF_chi2(nu_s,S) para S>0, e p_bound=1 para S<=0, é um p conservador válido para o nulo composto. A prova segue da inclusão de eventos {S>=t} contida em {q_true>=t}. Para nu>0 a transformação pela cauda contínua é superuniforme. Não se afirma que a distribuição de S seja qui-quadrado, nem que a cota seja apertada.

Se somente nu_s<=nu_bar for conhecido rigorosamente, pode-se usar chi-quadrado de nu_bar: somar quadrados gaussianos independentes demonstra a ordenação estocástica. Para nu=0, o pivô é massa pontual em zero: a cauda inclusiva é 1 para t<=0 e 0 para t>0. Não passar df=0 a uma rotina genérica sem tratar esse caso. Um nulo válido com nu=0 não produz estatística positiva.

## 4. Teorema mais informativo para ganhos: espaço global de diferenças

No espaço quociente, escreva x=m_j(xi_0)+Z, m_i(xi)=R_s mu_i(xi), com Z normal padrão. Suponha que um **subespaço linear V_jk,s fixo, não escolhido pelo dado** contenha

\[
m_k(\xi)-m_j(\xi_0)\quad
\text{para TODOS os parâmetros de }H_k\text{ e TODOS os parâmetros de }H_j.
\]

Se Pi_V é o projetor ortogonal, a relaxação da família competidora para o subespaço inteiro fornece

\[
g_k=\inf_\xi\|Z-[m_k(\xi)-m_j(\xi_0)]\|^2
\ge \|(I-\Pi_V)Z\|^2.
\]

Como g_j<=||Z||²,

\[
\boxed{g_j-g_k\le\|\Pi_VZ\|^2\sim\chi^2_{d_{jk,s}},
\qquad d_{jk,s}=\dim V_{jk,s}.}
\]

É uma cota finita e uniforme sob H_j, sem linearizar a superfície de médias. Não requer aninhamento dos modelos. Uma aproximação tangente/Jacobiana em um único ponto NÃO substitui a inclusão global acima. Uma curva não linear de um parâmetro pode gerar muitas direções lineares.

### Aplicação estrutural à F9 candidata

As fontes do projeto estabelecem a forma local X eta+a_h h_i(xi)+c_C delta_i(xi). O fundo comprimido contém 3 coordenadas Planck e 13 BAO. Excluídos offsets fixos comuns, a média conjunta é

\[
\mu_i(\xi)=\begin{pmatrix}b_i(\xi)\\a_hh_i(\xi)+c_C\delta_i(\xi)\end{pmatrix},
\qquad b_i(\xi)\in\mathbb R^{16}.
\]

Defina D17 com 16 colunas de coordenadas do fundo e uma coluna local a_h; D18 acrescenta c_C. Assim, **antes de qualquer whitening**, diferenças entre H1/H2/H3/H5 estão em Range(D17); diferenças que envolvem H4 estão em Range(D18). A dependência não linear de h, beta, E, distâncias e r_d muda coeficientes, não cria colunas adicionais nesta representação.

Para CADA cenário, usar V_s=Range(R_s D17) ou Range(R_s D18). R_s, o projetor nuisance e o subespaço transformado devem corresponder àquela C_s. Misturas entre blocos por uma covariância conjunta conhecida não aumentam o limite de posto. É permitido usar uma envoltória maior que as diferenças fisicamente admissíveis; as diferenças reais precisam sempre obedecer ao suporte comum.

| Estatística / nulo | Limite estrutural d_bar | Cota candidata |
|---|---:|---|
| Q_1 / H1 fixa | 17 | SF_chi2(17,t) |
| T_21 / LCDM | 17 | SF_chi2(17,t) |
| T_41 / viés diferencial Cefeida | 18 | SF_chi2(18,t) |
| T_51 / régua BAO livre | 17 | SF_chi2(17,t) |
| G_1 / adequação de H1 | nu_s, ou limite rigoroso nu_bar | SF_chi2(nu_bar,t) |

**17/18 são limites estruturais de dimensão, não postos medidos, graus de liberdade por Wilks, números de parâmetros físicos ou poder medido.** Se nu_s exato for menor, pode-se usar min(nu_s,d_bar). Não se reduz Q a chi-quadrado_1 só porque beta livre acrescenta um parâmetro.

A prova perde essa contagem se a implementação acrescentar coordenadas CMB, modos de resposta local, correções dependentes do dado, projetos nuisance diferentes ou outro mapa físico. Um cálculo de espectros CMB completos não é o experimento comprimido de 16 coordenadas. A verificação futura deve mostrar que TODA função de média efetivamente implementada tem essa forma em TODO o domínio. Não basta conferir cinco pontos.

## 5. Dimensões da montagem completa e do subset

**[REAL documental]** O projeto tem 267 linhas locais, X de posto 63 e 72 ciclos estelares independentes. **[INPUT condicional]** Esses ciclos pertencem ao núcleo da covariância científica admitida; a abertura ainda precisa conferir suporte/precisão dos centros.

Somar Planck3 e BAO13 dá n=283. Mantidos os 72 vínculos, r_s<=211, portanto nu_s<=148. Pode-se usar a cota base chi-quadrado_148 sem afirmar r_s=211, desde que X continue de posto 63 dentro do suporte conjunto e os vínculos sejam exatos. Igualdade r_s=211 exige ausência de núcleos adicionais. Independência de blocos e positividade dos blocos restantes são condições suficientes específicas, não fatos presumidos.

Mesmo com correlações entre blocos, um núcleo marginal exato é herdado pela matriz conjunta PSD: v^TC_local v=0 implica ||C_joint^(1/2)(v,0)||²=0, logo C_joint(v,0)=0. Correlações podem reduzir mais o posto; também exigem revalidar que X está no suporte conjunto. Apenas a positividade dos blocos diagonais não garante isso.

O preflight de **262** linhas excluiu os cinco MM e registrou posto local 190 em duas variantes condicionais; com 16 coordenadas adicionais e independência/positividade, r=206 e nu=143. Isso não substitui as 267 linhas nem qualifica a família inteira. Não reutilizar 143 no experimento completo. Nenhum novo posto ou matriz foi calculado nesta unidade.

## 6. Otimização: o sentido correto do certificado

Um otimizador local devolve um valor factível U_i>=g_i. Ele NÃO fornece L_i<=g_i. Em G ou num contraste, superestimar o mínimo nulo pode fabricar rejeição. Múltiplos starts e concordância de mínimos são diagnósticos, não uma prova global.

Exigir intervalos certificados L_i<=g_i<=U_i, incluindo erros do modelo, interpolações, whitening, suporte e arredondamento. Limites inferiores seguros para a estatística são:

\[
\ell_G=\max(0,L_1),\quad
\ell_Q=\max(0,L_1-U_3),\quad
\ell_{T_{j1}}=L_j-U_1.
\]

O máximo com zero em Q usa a inclusão qualificada H1 em H3. Se essa inclusão falhar, o contrato deve conservar o contraste assinado. Limite negativo ou zero de T recebe p_bound=1 e não certifica direção positiva. Um intervalo que cruza zero não deve ser rotulado preferência dirigida.

Como SF é decrescente e ell<=S, SF(ell)>=SF(S): usar ell conserva o teste. L_i=0 sempre é um limite trivial para RSS não negativo, mas geralmente deixa o teste sem informação. Não convertê-lo em nova significância. Um RSS negativo relevante é erro numérico/contratual a esclarecer, não valor a cortar silenciosamente para certificar o cálculo.

**Opção implementável futura:** cobrir todo o domínio físico por células e limitar rigorosamente a imagem da média de cada célula no quociente. A distância até uma envoltória EXTERNA dessa imagem fornece limite inferior por célula; o mínimo sobre uma cobertura completa é L_i. Para uma bola de centro m_c e raio R_c que contém toda a imagem da célula, o limite é max(0,||x−m_c||−R_c)². Avaliar um ponto factível com erro de norma <=e fornece U_i=(||x−m_hat||+e)². A tabela antiga incompleta não cobre o domínio; cinco pares CAMB concordantes não fornecem R_c no contínuo.

Se houver certificados |g_i−g_hat_i|<=epsilon_i, a diferença inferior é g_hat_null−g_hat_comp−epsilon_null−epsilon_comp. Não usar tolerância do otimizador como se fosse esse certificado.

Também a rotina de SF precisa produzir um limite SUPERIOR confiável, preservando caudas pequenas sem underflow para zero. Pode-se usar aritmética intervalar ou erro rigorosamente limitado na gama incompleta. Para df=2m, SF=e^(−x) sum_(k=0)^(m−1) x^k/k!, x=t/2; para df ímpar, iniciar em Q(1/2,x)=erfc(sqrt(x)) e usar Q(a+1,x)=Q(a,x)+x^a e^(−x)/Gamma(a+1). Estas são receitas analíticas para implementação posterior; nenhuma cauda foi avaliada agora.

## 7. Limites, falhas e extensões

**Covariância diferente/paramétrica.** Com normalizações diferentes, T não é simplesmente diferença de RSS. Contraexemplo: nulo Y~N(0,1), rival Y~N(0,epsilon²), 0<epsilon<1, ambos com média zero. A razão dirigida é T=−2 ln epsilon+(1−epsilon^(−2))Y². Em Y=0, T>0 e RSS_true=0: a desigualdade pontual falha. A cauda também pode falhar: para t=2 ln(1/epsilon)−1, Pr(T>=t)=Pr(Y²<=1/(epsilon^(−2)−1)), assintoticamente sqrt(2/pi)epsilon; a cauda chi-quadrado_1 em t é assintoticamente sqrt(2/pi)epsilon sqrt(e)/sqrt(t). A razão cresce sem limite. Portanto nem o envelope de cauda é universal para likelihoods com covariâncias distintas.

Uma estatística definida SOMENTE como RSS com C(xi) verdadeira no nulo pode admitir outro envelope por avaliação no parâmetro verdadeiro, se o posto for uniformemente limitado. Isso não transfere a presente prova para razões de likelihood com log-determinantes ou suportes variáveis. Exige contrato e demonstração próprios.

**Erros estimados.** Substituir C por C_hat estimada dos mesmos dados não produz automaticamente um pivô chi-quadrado. Mesmo uma estimativa independente de C não a torna igual à covariância verdadeira condicionalmente. Casos Wishart específicos podem admitir outras distribuições; não importá-las sem suas hipóteses. Tratar erros publicados como fixos define um modelo condicional explícito, não prova que representam toda a incerteza. Variâncias dos MM que dependam de distâncias observadas exigem esse tratamento antes da aplicação conjunta.

**Inflação certificada opcional.** Se o erro for gaussiano com covariância verdadeira Sigma e houver uma cota determinística uniforme Sigma<=a C_s no suporte comum, a mesma prova algébrica dá envelopes a*chi-quadrado_nu e a*chi-quadrado_d. A covariância do vetor projetado tem autovalores <=a; acoplar quadrados gaussianos prova a dominação. a precisa de justificativa independente; não é um fator a escolher após ver o resultado. Métrica/projetor estimados adaptativamente exigem análise adicional.

**Suporte e precisão.** Um corte espectral numérico não prova um núcleo físico exato. Apagar autovalores pequenos positivos altera o modelo. Erros de arredondamento das linhas com vínculos devem ser tratados no contrato; não acrescentar jitter nem descartar resíduos fora do suporte para obter aceitação.

**Não linearidade.** h(theta), beta livre, logaritmos e r_d não invalidam as duas provas enquanto a média estiver corretamente incluída no domínio/subespaço. Transformar dados de modo dependente de theta e conservar a antiga distribuição de erro pode invalidá-las. O experimento comprimido com q0/j0 fixados permanece uma escolha do contrato.

**Seleção.** Otimizar dentro de domínios previamente fixados é coberto. Escolher depois quais dados, modelos, tempos, cenários ou testes reportar não é automaticamente coberto. A multiplicidade histórica não some porque o cálculo foi feito na RAM.

## 8. Composição com o contrato V2 existente

O V2 resolve VC-01 por predicados explícitos de disponibilidade/calibração. Esta nota não o modifica. O envelope analítico pode preencher `VALID_UNIFORM_NULL_OR_CONSERVATIVE_BOUND` após suas hipóteses e certificados serem verificados. Não é necessário medir a distribuição exata para ter um teste conservador válido.

Para cada teste j e cenário s, formar um limite p_upper_j,s pela cauda superior certificada aplicada ao limite inferior certificado da estatística. Manter a família congelada:

\[
p_{robust,j}=\max_s p_{upper,j,s},\qquad
p_{FWER,j}=\min(1,5p_{robust,j}).
\]

O máximo exige TODOS os cenários admitidos ou cobertura equivalente provada, com etiquetas preservadas. Validade é para a união dos modelos de erro contemplados; não cobre qualquer sistemática imaginável. Não há Bonferroni extra por 600 etiquetas quando a conclusão exige todas, pois o máximo domina o p do cenário verdadeiro; escolher o melhor cenário seria outra regra.

Bonferroni5 vale sem independência das cinco perguntas. O limiar do contrato é alpha5=erfc(5/sqrt(2))/2. Z_lower=Phi^(-1)(1−p_FWER_upper) é somente o limite conservador na convenção gaussiana de cauda superior; não é uma medição gaussiana nem deve ser anunciado positivo quando p é grande. Com limites probabilísticos de certificação, sua probabilidade de falha deve ser incluída no orçamento total alpha; um certificado determinístico evita esse custo.

Para preferência dirigida, todos os T_j1 precisam ter direção positiva certificada. Rejeição de um controle H1 válido permanece reportável mesmo se outro estiver indisponível. Não-rejeição de H1 exige AMBOS os controles completos e calibrados, como no V2; disponibilidade parcial nunca vira `NOT_FALSIFIED`.

Uma cota válida com p_bound grande é **teste conservador sem rejeição**, não `CALIBRATION_UNAVAILABLE`. Mas p_bound>alpha não prova que o p exato seja >alpha; a cota pode ser frouxa. Adequação não rejeitada não demonstra validação física. Poder é um campo separado e ainda não medido. Nenhum fator de Bayes é convertido em sigma, e dados comuns não são multiplicados como evidências independentes.

## 9. Alternativas e recomendação

| Alternativa | Entrega | Limitação |
|---|---|---|
| A — envelope residual geral | chi-quadrado_nu, ou limite148 qualificado, para todas as estatísticas; certificados globais dos mínimos | Simples e rigoroso, possivelmente muito conservador |
| B — envelope do espaço global de diferenças | G com envelope residual; Q/T com limites17/18; mesmos certificados | **Recomendada** se a forma inteira das médias e whitening por cenário forem verificados; não garante poder |
| C — calibração específica mais apertada | distribuição exata em casos especiais, limites uniformes adicionais ou método raro-evento validado | Opcional futura; maior custo, nenhum método/resultado aprovado nesta unidade |

A fornece fallback. B reaproveita a estrutura linear já derivada em vez de inventar novas funções físicas. Brute force de 5sigma não é pré-requisito para A/B. Se a cota for insuficiente, isso permite avaliar custo/benefício de C; não autoriza trocar a cauda por Wilks nem declarar que a TGL falhou.

## 10. Próximos passos delimitados

1. Revisão independente da prova e das hipóteses de aplicação às funções realmente usadas na F9.
2. Decisão da coordenação sobre alternativa e erro admitido; sem reabrir V1 por esta nota.
3. Implementação posterior dos certificados e somente os controles sintéticos específicos de `PROTOCOLO_CONTROLES_FUTUROS.json`. Nenhuma repetição dos controles nuisance/CAMB já qualificados.
4. Abertura/execução observada somente pelo fluxo da missão. Registrar separadamente adequação de H1, beta livre, rejeição de cada rival, sistemáticas, incerteza numérica e poder.

**Não executado nesta unidade:** matriz científica nova, postos numéricos, otimizador, SF, Monte Carlo, solver cosmológico, y/S/g/H0/lnB, dados D, modelos remotos. A nova contribuição é a prova e a especificação de sua aplicação. Originais, motor e contratos consumidos permanecem intactos.
