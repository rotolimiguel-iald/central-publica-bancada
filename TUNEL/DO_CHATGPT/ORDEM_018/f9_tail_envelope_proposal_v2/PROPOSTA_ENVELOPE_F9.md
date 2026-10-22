# Proposta documental de envelope superior da cauda F9 — V2

[DERIVED — condicional, não adotado] A cota de Chernoff da qui-quadrado e um envelope racional distinto podem substituir a avaliação exata da SF apenas como **majorantes conservadoras**. A proposta recomenda à revisão a alternativa racional com N=256 e grade fixa Q=10^30 por reduzir as funções numéricas a aritmética inteira/racional e raiz inteira. Não seleciona cientificamente um método, não modifica os cinco testes nem concede autorização de execução.

[ERRATA DOCUMENTAL V2 — ao lado da proposta498] A revisão independente identificou que a versão anterior separava d=0 das fórmulas gerais, mas ainda permitia que a API F9 devolvesse p=0 para um limite estatístico positivo. Isso conflita com o C04 consumido. Nesta V2 a identidade matemática do átomo é preservada como referência abstrata; a API F9 exige INVALID, p_upper=null e CONTRACT_INCOHERENCE_NOT_REJECTION quando d=0 e L>0. Não há rejeição automática. A pasta da proposta498 permanece íntegra.

[REAL — alcance desta entrega] Foram lidos documentos e calculados hashes de arquivos. Não houve implementação do módulo, execução dos casos propostos, avaliação de SF/Chernoff, cálculo de estatísticas observadas, importação científica, abertura de séries/posteriores D, rede ou chamadas de modelos. As contas abaixo são derivações simbólicas; os valores esperados dos casos não são recibos de medição. O protocolo consumido 6273, a prova, V2, modelos, fontes e memórias permanecem intactos.

## 1. Premissa que este módulo não cria

A prova candidata e sua revisão independente fornecem uma redução **condicional**: sob cada nulo e cenário admitido, a estatística S tem sua cauda dominada pela cauda de Z~chi2_d. Isso requer o modelo gaussiano de covariância fixa comum, suporte comum íntegro, projeção/nuisance certificados, domínio verdadeiro admitido, e, quando usado, o espaço GLOBAL de diferenças de médias. Um limite superior rigoroso da dimensão serve: para nu<=d, chi2_nu é dominada por chi2_d, pela representação como soma de quadrados independentes. Isto não identifica a distribuição exata de S e não é Wilks.

Os candidatos 17/18 são limites estruturais, não postos medidos. O limite residual 148 continua condicionado aos 72 vínculos exatos e ao posto suportado 63 de X na matriz conjunta. O módulo aceita d certificado; não calcula ou escolhe posto. Não cobre covariância estimada/paramétrica, suporte truncado ou família de cenários incompleta por mera substituição de uma rotina de SF.

## 2. Chernoff, incluindo as fronteiras

Para d inteiro positivo, escreva Z como soma de d quadrados de normais N(0,1) independentes. A integral gaussiana, por mudança de escala, dá

    E exp(lambda Z) = (1-2 lambda)^(-d/2),  0 <= lambda < 1/2.

Por Markov, para qualquer lambda admissível,

    Pr[Z >= x] <= exp(-lambda x) (1-2 lambda)^(-d/2).

O logaritmo da expressão tem derivada em lambda -x+d/(1-2lambda) e segunda derivada 2d/(1-2lambda)^2>0. Se x>d, o mínimo é lambda*=(1-d/x)/2, resultando em

    C_d(x) = (x/d)^(d/2) exp((d-x)/2).

Se x<=d, lambda=0 fornece a cota 1. A expressão otimizada com lambda negativo não é usada. Para x>d,

    d log C_d(x)/dx = (d-x)/(2x) < 0.

Portanto C_d começa em 1 em x=d, é positiva e decrescente depois desse ponto, e satisfaz SF_d(x)<=C_d(x)<=1. Para d>0 a lei é contínua; a cauda inclusiva coincide com a usual.

Para d=0, Z é abstratamente o átomo em zero: a cauda inclusiva matemática é 1 quando x<=0 e 0 quando x>0, sem divisão por d, rotina gama ou underflow. **Essa identidade abstrata não é a regra de retorno da API F9 para x>0.** No contrato de G/Q/T, dimensão certificada zero com limite estatístico positivo denuncia incoerência entre estatística, suporte e certificados; deve produzir INVALID, p_upper=null e CONTRACT_INCOHERENCE_NOT_REJECTION. Exige revisão do suporte comum, do grau/espaço global, da identidade do teste e do limite inferior, sem rejeição automática. O C04 consumido já distingue o zero abstrato desse diagnóstico operacional. Com d=0 e limite não positivo, a API pode devolver VALID_ATOM_TAIL, p_upper=1, após validar as demais premissas. Nenhum modo abstrato/override está disponível na API proposta para alimentar uma rejeição F9.

## 3. Direção do certificado da estatística

Se L<=S é um limite inferior certificado, a monotonicidade da SF implica

    SF_d(S) <= SF_d(L) <= C_d(L) <= U(L),

onde U é qualquer majorante numérica certificada de C. A dominância de S pelo pivô torna SF_d(S) um p conservador; a majorante ponto a ponto continua conservadora. Para L<=d, U=1 é uma cota válida, embora fraca. Nenhuma hipótese de L ser o valor exato ou um estimador independente é necessária; é necessária a desigualdade certificada em todos os dados admissíveis.

Se L é representado por um intervalo rigoroso [ell_lo,ell_hi], usar ell_lo, nunca ell_hi. Um RSS de otimização local factível fornece limite SUPERIOR U_i para o mínimo global, não limite inferior L_i. Preservam-se as fórmulas do candidato:

- G: max(0,L_1).
- Q: max(0,L_1-U_3), somente com inclusão H1 em H3 qualificada.
- T_j1: L_j-U_1, preservando o sinal; a condição dirigida exige limite inferior positivo em todos os cenários.

A proposta não produz nenhum desses certificados nem avalia as fórmulas em dados.

## 4. Três alternativas de engenharia antes de medir

**A — SF exata com intervalo certificado.** Recorrências da gama incompleta para graus inteiros/semipares, com erfc e exponenciais intervalares, podem fornecer limite estreito da SF real. É a opção mais apertada entre as listadas, mas requer qualificação geral de domínio/erro/custo. Os cinco pontos de C08 já registrados pela coordenação não certificam uma implementação para todo d<=148 e toda entrada. Não se transforma float comum, concordância pontual ou underflow em certificado.

**B — Chernoff original com avaliação intervalar.** Calcula C_d, não a SF exata. Em entrada racional exata x>d, o fator (x/d)^(d/2) é racional para d par; para d ímpar requer raiz positiva com extremo superior. Multiplicar majorantes positivas desse fator e de exp(-(x-d)/2) dá uma majorante. Quando a=(x-d)/2 vem de intervalo, exp(-a) exige o extremo INFERIOR de a; a solução preferida é fixar primeiro x no limite inferior certificado.

Uma construção possível de exp(-a), sem prometer custo: escolha k>=0 com y=a/2^k<=1. Para n>=0, sejam S_n=sum_{j=0}^n y^j/j! e t=y^(n+1)/(n+1)!. A razão dos termos posteriores é no máximo y/(n+2)<1; logo

    S_n <= exp(y) <= S_n + t/(1-y/(n+2)).
    (S_n+t/(1-y/(n+2)))^(-2^k) <= exp(-a) <= S_n^(-2^k).

Todos os extremos são racionais para y racional. Potências e denominadores podem custar muito; precisam de limites prévios. O intervalo matemático é rigoroso, mas uma implementação adaptativa de fatores arredondados não herda automaticamente monotonicidade ponto a ponto de sua saída superior. Essa monotonicidade de saída não é necessária para uma majorante pontual válida; não deve ser afirmada sem prova própria.

**C — envelope racional fixo N=256.** Evita exponencial, logaritmo, gama e erfc na avaliação da cauda. É deliberadamente outra majorante, geralmente mais frouxa que Chernoff. Recomendada para revisão como alteração numérica de menor variedade de primitivas, sem adoção científica nem comparação medida de desempenho/poder. A opção A permanece disponível como alternativa mais apertada; nada será escolhido após buscar significância.

## 5. Envelope racional e condição exata de monotonicidade

Para a=(x-d)/2>0 e N>0, log(1+a/N)<=a/N implica

    exp(-a) <= (1+a/N)^(-N).

Logo, para x>d,

    SF_d(x) <= C_d(x) <= B_{d,N}(x)
    B_{d,N}(x) = (x/d)^(d/2) [1+(x-d)/(2N)]^(-N).

Seu quadrado é racional quando x é racional, d inteiro e N inteiro:

    R = B_{d,N}(x)^2 = (x/d)^d / [1+(x-d)/(2N)]^(2N).

A derivada é

    d log B_{d,N}(x)/dx
      = d/(2x) - N/(2N+x-d)
      = (d-2N)(x-d) / [2x(2N+x-d)].

O denominador é positivo. Assim, o ramo é estritamente decrescente em x>d **somente quando 2N>d**. Em 2N=d é constante 1; em 2N<d cresce e não sustenta a afirmação de decaimento. Em N=256, 2N=512>148, portanto a condição cobre todo d=1..148. B(d)=1 e 0<B(x)<1 para x>d. A extensão B=1 para x<=d é contínua e não crescente.

N é fixado antes de dados. O limite N→infinito aproxima Chernoff por cima, mas não é necessário à prova e não autoriza ajustar N por resultado. Para x grande, B tem decaimento polinomial de ordem N-d/2; não deve ser descrito como a cauda exata/exponencial.

## 6. Raiz com arredondamento para cima em grade fixa

Proposta fixa Q=10^30. Para R=A/B>0 com inteiros A,B positivos, tome a menor raiz superior na grade:

    u = ceil(Q sqrt(R)),      U = u/Q.

Uma implementação futura pode obter k=isqrt(floor(A Q^2/B)); usar u=k se k^2 B=A Q^2, e u=k+1 caso contrário. A identidade de piso é válida porque k<=sqrt(AQ²/B)<k+1 equivale à desigualdade inteira de quadrados correspondente. O certificado verificável é

    (u-1)^2 B < A Q^2 <= u^2 B,  u>=1.

O caso de quadrado perfeito mantém a igualdade à direita. As comparações são inteiras exatas. Como R<=1 provado no domínio, u<=Q e U<=1. Uma violação de R<=1 ou do certificado é falha de implementação, não algo a esconder com clipping. Fora do ramo, retorna-se 1 para x<=d e trata-se d=0 separadamente.

Conclui-se

    SF_d(x) <= C_d(x) <= B_{d,256}(x) <= U(x) <=1,
    0 <= U(x)-B_{d,256}(x) < 1/Q.

Como sqrt e ceil são funções não decrescentes de seu argumento e R(x) é decrescente, U(x) é não crescente em x no ramo concluído certificado. Para todo x racional finito com d>0, U>=1/Q>0, mesmo que a cauda seja muito menor: não há falso zero por underflow. A grade é um piso da saída conservadora, não um piso físico da SF. A prova não exige float/Decimal transcendente.

**Limite da afirmação de monotonicidade:** um ramo operacional que devolva a cota trivial 1 por esgotamento de recursos pode subir em relação a uma entrada anterior concluída. Sua validade pontual permanece, mas não há promessa de monotonicidade global entre esses estados. O recibo deve distingui-los.

## 7. Falha matemática, indisponibilidade e limite de recursos

A ordem das guardas é parte do contrato:

**Guarda de coerência F9 de dimensão zero:** depois das validações semânticas/de tipo e antes de qualquer retorno de cauda, cota trivial por recurso ou agregação, d=0 com x_lower>0 termina INVALID/null, motivo CONTRACT_INCOHERENCE_NOT_REJECTION. Esse caso não pode ser convertido em p=0, p=1, não rejeição ou rejeição. O teste afetado não dispõe de p robusto completo enquanto a incoerência persistir; outros testes completos e válidos mantêm a regra V2 original.

1. Validar identidade/pins, modelo/covariância/suporte, certificado de dominância e de d, cobertura pertinente e certificado L<=S. Não basta um booleano fornecido pelo solicitante: devem existir referências verificáveis aos certificados e ao escopo congelado.
2. Validar representação racional canônica e domínio. Tipo inválido, d fora de 0..148, float sem envoltória certificada, denominador inválido ou entrada sem certificado não são caudas calculáveis.
3. Só depois executar o ramo matemático selecionado, com os limites previamente declarados.

Falha dos itens 1/2, corrupção, violação de identidade, erro de orientação ou falha de certificado da raiz => UNAVAILABLE/INVALID explícito e p_upper=null. Nunca substituir esses casos por p=1, zero ou não rejeição.

Proposta operacional estrita: se, APÓS aquelas validações, apenas o limite pré-declarado de tempo/tamanho impedir o cálculo da majorante apertada, devolver p_upper=1 como **VALID_TRIVIAL_BOUND_RESOURCE_LIMIT**, com razão, etapa e limites atingidos. É a desigualdade exata Pr(evento)<=1, explicitamente escolhida como parte do algoritmo futuro, não resultado da SF nem sucesso do cálculo interrompido. Não há retry/fallback tácito. A aprovação dessa política ainda pertence à revisão/adoção do contrato; esta entrega não a ativa. Se não for adotada, o mesmo esgotamento termina indisponível.

A cota 1 pressupõe estatística/modelo válidos; não corrige falha anterior do instrumento científico. Uma cota válida grande, inclusive 1 por ramo matemático ou operacional predefinido, corresponde a teste conservador não rejeitante se o teste completo assim for adotado. Isso não prova p exato grande, adequação do modelo ou poder suficiente. Falha em qualquer cenário continua visível e não é omitida.

## 8. Cenários, Bonferroni5 e limiar inalterado

Para cada teste j completo, usar o máximo das majorantes sobre TODA a família congelada, ou cobertura equivalente integral certificada com rótulos:

    p_robust,j = max_s p_upper,j,s
    p_FWER,j  = min(1,5 p_robust,j).

Fator cinco preservado, sem independência exigida e sem fator novo pelo número de cenários. Não usar média ponderada, produto ou cenário favorável. Ausência/invalidez de um cenário impede o p robusto daquele teste; não apaga uma rejeição independente completa e válida de outro teste. A semântica dos dois controles H1 e dos contrastes dirigidos permanece a do V2: ambos H1 completos para sua não rejeição; uma rejeição completa H1 continua reportável mesmo com o outro indisponível; direção positiva em todos os cenários para uma afirmação dirigida.

O limiar continua exatamente alpha5=0.5*erfc(5/sqrt(2)), cauda unilateral. O módulo proposto não avalia alpha, não emite sigma, Bayes, decisão física nem veredito. Uma futura comparação certificada com alpha num intervalo [alpha_lo,alpha_hi] prova rejeição apenas quando p_FWER<=alpha_lo; prova que ESTE envelope não rejeita quando p_FWER>alpha_hi; se o intervalo estrangular a comparação, esta fica não resolvida, sem arredondar o limiar para conveniência. O limiar teórico não muda e a igualdade segue <=.

Não se promete rejeição, poder, cauda observada ou certificado científico da F9. Uma majorante frouxa pode não rejeitar onde a SF exata rejeitaria. Isso é perda de poder possível, não defeito lógico da majorante nem licença para escolher outra opção depois do resultado.

## 9. Contrato proposto e próximos passos

CONTRATO_MODULO_CANDIDATO.json define entradas/saídas/guardas e limites ainda não executáveis. CASOS_SINTETICOS_PROPOSTOS.json contém oito grupos fixos de casos, com resultados simbólicos esperados justificados antes de qualquer avaliação. O caso de cauda muito pequena tem expectativa de saída exatamente 1/Q por desigualdade analítica, não por observação numérica. T01 foi corrigido nesta V2: o terceiro retorno F9 é INVALID/null; [1,1,0] aparece somente como referência abstrata da cauda do átomo. T02–T08 permanecem estruturalmente iguais.

A recomendação é submeter C à revisão independente, mantendo A/B explicitamente distintas. Somente depois de decisão específica se prepararia uma implementação e seus controles em nova unidade, sem mudar contratos consumidos. Não há código, comando executável, CLAIM, autorização ou job científico neste pacote. Tempo/custo de avaliação e desempenho permanecem não medidos.
