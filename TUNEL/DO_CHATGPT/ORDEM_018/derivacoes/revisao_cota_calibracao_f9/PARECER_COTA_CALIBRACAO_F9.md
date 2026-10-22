# Revisão independente da cota de calibração F9

[DERIVED — prova condicional examinada] As duas cotas de cauda apresentadas são válidas sob as hipóteses enunciadas. Não identifiquei defeito matemático material na prova, no sentido dos certificados L/U ou na composição com o contrato V2. Este aceite é da demonstração condicional, não uma certificação de que as hipóteses já valem para a implementação/dados da F9.

[REAL — escopo] Request6273a822-5880-4742-a82c-b7cf93f7c128; mapa consultado seq481. Identidade: chatgpt-codex/ordem-018/derivacoes. Foram conferidos24 arquivos,13 snapshots e os recibos das62 checagens documentais. Os8 controles futuros permanecem não executados. Nenhum posto, CDF/SF, Monte Carlo, solver, ajuste, centro ou dado D foi calculado/aberto. INIT003 não foi repetida.

## 1. Projeção e uniformidade da cota base

A prova trabalha no suporte positivo de C_s. Com W C W^T=I e A=WX de posto63, a projeção ortogonal no complemento de Range(A) produz R X=0 e R C R^T=I_nu. O perfil em eta de domínio R^63 é exatamente a norma quadrática de R(Y−mu). Não há sorteio de um prior plano impróprio.

Sob o nulo no parâmetro verdadeiro, o vetor projetado é gaussiano padrão e q_true tem lei chi2_nu. Para o mínimo físico global g_i, 0≤g_i≤q_i,true. Normalizações de likelihood comuns e C fixo dão G1=g1, Q1=g1−g3 e Tj1=gj−g1. Logo cada estatística é dominada por q_true sob o seu próprio nulo. Essa inclusão de eventos vale para todo parâmetro verdadeiro admitido: não depende de estimar o ponto menos favorável numa grade.

Não se conclui que G/Q/T tenham distribuição qui-quadrado. Obtém-se um limite uniforme de cauda. A sobrevivência da lei dominante é um p conservador; a extensão p=1 para estatística não positiva é segura. A ordenação por um limite superior de dimensão é válida por soma de quadrados independentes. O caso nu=0 é corretamente tratado como átomo, não como uma chamada de rotina genérica com df0.

As condições de suporte são essenciais: pseudoinversa não autoriza apagar um resíduo fora do suporte. Não se subtraem automaticamente três/quatro parâmetros físicos de nu. Sua minimização sustenta a desigualdade, não outro pivô exato.

## 2. Refinamento pelo espaço global de diferenças

Fixado o parâmetro verdadeiro do nulo, no quociente x=m_nulo+Z. Se um subespaço V, fixo e independente do dado, contém TODAS as diferenças m_comp(xi)−m_nulo(xi0), a minimização sobre a família competidora fica acima da minimização sobre V inteiro:

g_comp ≥ ||(I−Pi_V)Z||².

Subtrair essa desigualdade de g_nulo≤||Z||² dá ganho≤||Pi_V Z||². Como Z é normal padrão e Pi_V é projeção ortogonal fixa, a norma tem lei chi2_dimV. Não é necessário aninhamento nem superfície física linear; é necessária inclusão global em V. Isso sustenta a cota para Q e para os três contrastes dirigidos.

A representação candidata da média possui16 coordenadas comprimidas de fundo mais uma resposta local a_h h. H4 acrescenta c_C delta. Portanto D17/D18 são envoltórias lineares para as diferenças de médias: a dependência não linear em theta, beta e rd muda coeficientes, não cria outras colunas. Aplicar R_s por cenário pode reduzir, mas não aumentar, essa contagem. Mesmo uma covariância conjunta que misture os blocos não amplia o limite estrutural.

17/18 são limites superiores de dimensão, não postos efetivos medidos, graus de liberdade por Wilks ou números de parâmetros ajustados. Também não dependem de certificar um posto exatamente igual a17/18: basta a inclusão global e o limite superior. Reduzir além disso exige outra justificação, e uma tangente local não a fornece. A checagem futura precisa cobrir as funções realmente implementadas; cinco pontos concordantes não demonstram inclusão global.

## 3. Dimensão residual e vínculos da rede

A aritmética documental n=267+16 e os72 vínculos independentes permitem o limite residual proposto148, desde que os vínculos sejam núcleos EXATOS da covariância conjunta e X mantenha posto63 dentro de seu suporte. O recibo de desenho documenta esses vínculos e postos estruturais, mas não mede aqui o posto científico da matriz conjunta.

A herança do núcleo sob acoplamento PSD está demonstrada corretamente: se v é nulo no bloco marginal, (v,0)^T C_joint(v,0)=0; positividade semidefinida implica C_joint(v,0)=0. Não basta que os blocos diagonais sejam PSD para a montagem ser PSD, nem para X pertencer ao suporte conjunto. Postos adicionais menores são possíveis. A prova mantém essas condições explícitas.

O subset262 e a dimensão condicional143 mencionados na origem não substituem o experimento267. Esta revisão não recalculou nenhum posto nem adotou148 sem suas condições. Se estas não estiverem qualificadas, usa-se apenas uma dimensão/limite superior que tenha sido rigorosamente justificado para aquela montagem.

## 4. Certificados dos mínimos e da cauda

Os limites inferiores das estatísticas estão orientados corretamente:

- G: max(0,L1);
- Q: max(0,L1−U3), apenas com H1 contida em H3;
- Tj1: Lj−U1, conservando o sinal.

Cada L_i precisa ficar abaixo do mínimo global verdadeiro e cada U_i acima. Um ponto factível fornece U; um algoritmo local, muitos starts ou tolerância interna não fornecem L global. Um erro nesse sentido pode fabricar rejeição. Para cada estatística basta certificar os extremos que ela usa; o fato de U ser factível dispensa demonstrar que esse ponto é o minimizador global.

A distância a uma envoltória EXTERNA da imagem de uma célula é limite inferior. Tomar o mínimo desses limites numa cobertura completa mantém L global; omitir regiões do domínio invalida a conclusão. O raio que limita erros da média, a métrica e a projeção devem ser certificados. Cinco controles CAMB e uma tabela incompleta não bastam, como a própria fonte reconhece.

Se ell≤S, a monotonicidade da sobrevivência implica SF(ell)≥SF(S). Usar o limite inferior da estatística junto de um limite SUPERIOR da SF mantém conservadorismo. As recorrências par/ímpar de gama incompleta estão corretas como receitas analíticas, ainda sem certificado de uma implementação. Underflow numérico para zero não é cauda certificada; limites probabilísticos de erro precisam entrar no orçamento global de falha.

## 5. Falhas concretas examinadas

**F01 — tangente usada como espaço global.** Uma curva como m(t)=(t,t²) tem tangente unidimensional na origem, mas suas diferenças saem dessa reta. Um projetor só na tangente não deixa o resíduo competidor limitado pela parte ortogonal como a prova necessita. A fonte acerta ao exigir o span global, não um Jacobiano no melhor ajuste.

**F02 — mínimo local usado como limite inferior.** RSS factível é maior ou igual ao ínfimo. Colocá-lo no lugar de L nulo pode aumentar a estatística e reduzir artificialmente o p. Os certificados globais pedidos são uma condição matemática concreta, não uma exigência de demonstrar ausência de toda sistemática.

**F03 — covariâncias diferentes.** O contraexemplo N(0,1) versus N(0,epsilon²) foi conferido algebricamente: o termo −2ln epsilon no contraste não é diferença de RSS com uma normalização comum. A assimptótica apresentada mostra que a falha pode alcançar a cota de cauda, não somente a desigualdade pontual. Esse contraexemplo impede transplantar a prova para likelihoods de covariância diferente/paramétrica.

**F04 — covariância estimada ou suporte truncado.** Condicionar numa estimativa independente não a torna a covariância verdadeira. Um C calculado dos próprios centros tampouco gera automaticamente o pivô. Tratar erros reportados como fixos especifica um modelo condicional, cuja adequação não é demonstrada por esta álgebra. Cortar autovalores pequenos positivos também muda o modelo; não prova72 vínculos exatos. A prova identifica essas limitações corretamente.

**F05 — família incompleta ou escolha pelo dado.** Omitir cenários indisponíveis ao formar max p ou escolher span/cortes depois de procurar significância quebra o procedimento declarado. Os campos de disponibilidade do V2 e a fixação prévia continuam necessários.

A extensão opcional Sigma≤a C está correta para covariâncias fixas gaussianas no suporte comum: após projeção, os autovalores são limitados por a, e a soma de quadrados ponderados é dominada por a vezes a qui-quadrado correspondente. Não se infere daí validade para matriz/projetor adaptativo ou fator a escolhido após o resultado.

## 6. Família, V2 e significado de não rejeitar

O máximo dos limites p_upper sobre TODOS os cenários admitidos domina o p do cenário verdadeiro. Bonferroni5 controla a família sem independência. Não há fator600 adicional quando a conclusão exige todos os cenários; escolher um cenário favorável seria outra regra.

A interoperabilidade com V2 está preservada: uma rejeição H1 completa e válida continua visível se outro teste estiver indisponível; não-rejeição exige ambos controles H1 completos/calibrados. Um limite p grande, mas válido, significa que ESTE teste conservador não rejeita; não é ausência de calibração e não demonstra que o p exato seria grande. Uma cota frouxa não valida o modelo nem mede poder. Calibração parcialmente disponível é outra categoria.

Isso não usa priors para ponderar o supremo, não converte Bayes em sigma e não afirma confirmação. A qualificação continua restrita à família/modelo de erros ratificados; não exige nem certifica cobertura de todas as sistemáticas imagináveis.

## 7. Alternativas e parecer

**A — cota residual geral.** Matematicamente válida com nu ou limite superior rigoroso, com menos condições sobre a forma global das previsões; pode ser muito conservadora.

**B — G residual e Q/T no espaço global17/18.** Válida e potencialmente mais informativa quando a representação global da média realmente implementada está certificada em todo o domínio e por cenário. É razoável como candidata preferida, sem promessa de poder.

**C — cauda específica mais apertada.** Possibilidade futura se a cota conservadora não for útil, em unidade própria. Não é requisito para reconhecer a validade de A/B e não autoriza Wilks ou simulação automática.

O parecer é favorável à prova condicional e à coerência do candidato documental. A aplicação ainda precisa preencher os requisitos explicitamente pendentes: modelo gaussiano/C fixo, suporte, projeção, forma global, certificados dos mínimos e da SF, família completa e decisões de escopo. Esses requisitos não são defeitos ocultos do documento, nem resultados já medidos. Os8 controles futuros são especificações, não execução nem certificado científico; não os rodamos.

## 8. Custódia

Os24 artefatos do manifesto conferem. Os13 snapshots e respectivas fontes foram conferidos por bytes e hashes; FINAL_CHECK aponta para os hashes efetivamente lidos do manifesto/prova/candidato. A origem registra62 checagens documentais aprovadas; lemos o recibo sem executar seus scripts. O candidato mantém valores observados/certificados/p/sigma/lnB nulos e não autoriza abertura.

A prova e os fontes do autor permanecem intactos. Este parecer, recibo e manifesto são novos artefatos em pasta própria. Nenhum gate ou contrato consumido foi alterado.
