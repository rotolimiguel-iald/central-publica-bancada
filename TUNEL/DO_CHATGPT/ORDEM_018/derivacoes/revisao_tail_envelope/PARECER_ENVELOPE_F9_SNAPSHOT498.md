# Revisão independente — proposta de envelope de cauda F9 (snapshot 498)

[REAL — revisão documental] A entrega selada de request e8bf5643-8da4-4ebb-a923-db65e41bd042 foi conferida por bytes e SHA-256: cinco arquivos do manifesto e suas cinco fontes pinadas coincidem; o próprio manifesto também foi pinado. Consulta prévia do mapa e início registrado em 499. Esta revisão não executou SF, Chernoff, envelope, controles, otimização, CAMB, simulações, importação científica, dados observados, rede ou modelos. Fórmulas e expectativas aqui são [DERIVED — condicionais], não medições.

**Conclusão:** a derivação do ramo positivo, o teto da raiz e a integração conservadora são matematicamente coerentes. Há um achado material de interface, TE-01: o ramo d=0 admite p=0 para entrada positiva sem explicitar a guarda operacional já consumida em C04. O snapshot 498 não deve ser aprovado para uso da API F9 antes dessa correção documental. O achado não invalida a identidade abstrata da cauda de chi-quadrado de dimensão zero. Implementação, qualificação de custo e aplicação científica continuam fora deste parecer.

## 1. Chernoff e majorante racional

[DERIVED] Para Z~chi2_d, inteiro d>0, a MGF é (1-2lambda)^(-d/2), lambda<1/2. Markov com lambda>=0 produz exp(-lambda*x)(1-2lambda)^(-d/2). Sua convexidade dá lambda*=(1-d/x)/2 quando x>d; para x<=d o extremo admissível lambda=0 dá 1. Assim C_d(x)=(x/d)^(d/2)exp((d-x)/2) é a cota otimizada de Chernoff, **não a SF exata**. A derivada (d-x)/(2x) do log é negativa para x>d. As fronteiras e o uso da cauda inclusiva estão corretos para d>0.

Com a=(x-d)/2>0, log(1+a/N)<=a/N dá exp(-a)<=[1+a/N]^(-N). Logo SF<=C<=B, com B=(x/d)^(d/2)[1+(x-d)/(2N)]^(-N). O quadrado R é racional exato para x racional e d,N inteiros. A derivada apresentada,
(d-2N)(x-d)/[2x(2N+x-d)], está correta. N=256 tem 2N>148: B parte de 1 e decresce no domínio proposto d=1..148; não há extrapolação da monotonicidade a d>=512. A cauda de B é polinomial e a proposta a distingue da cauda real. A afirmação N→infinito aproxima Chernoff por cima também é coerente; não é autorização de escolher N após resultados.

A alternativa intervalar B da proposta (exponencial por série positiva e redução de argumento) usa a razão correta y/(n+2) para limitar a sobra a partir de t=y^(n+1)/(n+1)!. Inverter e elevar os extremos positivos preserva as orientações descritas. Não deriva daí custo, monotonicidade de uma implementação adaptativa nem resultado medido.

## 2. Raiz por teto e orientação dos certificados

[DERIVED] Para R=A/B>0, k=isqrt(floor(AQ²/B)) coincide com floor(Qsqrt(R)). Se k²B=AQ², a igualdade permite u=k; senão u=k+1. O certificado (u-1)²B<AQ²<=u²B, u>=1, caracteriza o menor teto na grade, incluindo quadrado perfeito. R<=1 implica u<=Q. O limite 0<=u/Q-sqrt(R)<1/Q e a positividade u/Q>=1/Q estão corretos. A composição de raiz e teto com R decrescente preserva saída não crescente no ramo concluído; o ramo explícito de recursos pode subir a 1, como a proposta já declara.

Não foi preciso calcular nenhuma raiz para esta conclusão. Os alvos simbólicos T03/T04 e o argumento por expoentes inteiros de T06 são coerentes por substituição algébrica. A lista de oito grupos não é recibo de oito controles: nenhum foi executado nesta revisão.

Para L<=S certificado, SF(S)<=SF(L)<=U(L). Deve entrar o extremo inferior de um intervalo do certificado, não um objetivo factível do otimizador. As fórmulas G=max(0,L1), Q=max(0,L1-U3) com H1 contido em H3 e Tj1=Lj-U1 preservam a direção correta. L_i é limite inferior global, U_i é superior factível certificado. Um L pode depender dos dados: a condição necessária é a desigualdade ponto a ponto válida, não independência artificial entre L e S. Um certificado probabilístico continua exigindo o orçamento de falha da prova; esta proposta não o fornece.

## 3. TE-01 — separar o átomo matemático da API F9

[REAL — evidência textual] PROPOSTA_ENVELOPE_F9.md:33 descreve corretamente a cauda abstrata do átomo: 1 se x<=0 e 0 se x>0. Porém CONTRATO_MODULO_CANDIDATO.json:130 permite esse ramo após validação semântica genérica; o estado VALID_ATOM_TAIL aparece na linha158 e todos os estados válidos podem entrar em V2 na linha223. CASOS_SINTETICOS_PROPOSTOS.json:7, T01_ATOM, espera d=0,x=1→0 depois dos certificados pré-validados. Não existe nessa entrega a guarda explícita CONTRACT_INCOHERENCE_NOT_REJECTION.

O recibo ROOT dos controles consumidos registra em C04 tanto zero_rank_positive_tail=0 (identidade da cauda abstrata) quanto positive_statistic_zero_rank=CONTRACT_INCOHERENCE_NOT_REJECTION. A proposta conserva o primeiro resultado, mas não transporta de forma explícita o segundo para sua interface F9.

[DERIVED — alcance exato do problema] Para G, dimensão residual realmente zero e suporte qualificado tornam o residual projetado identicamente zero. Para Q/T, dimensão global zero das diferenças entre médias comparadas faz coincidir os resíduos mínimos no quociente; o ganho não pode ser positivo. Um limite superior certificado de dimensão igual a zero tem a mesma consequência. Portanto um L estatístico positivo é incompatível com esses certificados/esse suporte: não constitui automaticamente uma nova rejeição calibrada. Isso é específico da estrutura usada na F9; não é uma negação da possibilidade abstrata de observar um evento fora de um nulo degenerado em outro teste.

**Correção pedida, sem modificar a fonte:** manter a identidade matemática separada e estabelecer na API F9: d=0 e lower estatístico positivo => INVALID, p_upper=null, reason=CONTRACT_INCOHERENCE_NOT_REJECTION, revisão de suporte/dimensão/certificados. Não mapear esse ramo como calibração válida nem convertê-lo em rejeição/não rejeição. d=0 com entrada não positiva pode retornar a cota1 após as demais guardas.

Duas alternativas suficientes:
1. API F9 restrita com guarda explícita; a cauda abstrata fica somente no texto ou em função matemática futura separada. É a recomendação, por preservar C04 diretamente.
2. Duas interfaces formalmente distintas, uma genérica para a cauda do átomo e outra adaptadora F9, que recusa a incoerência antes de emitir p. Se adotada, T01 precisa distinguir os dois contratos e o agregador não pode aceitar o estado genérico como evidência F9.

Não é necessário rerodar C04 ou implementar uma função para corrigir esse defeito documental. ROOT solicitou ao autor delta V2 separado; este parecer avalia exclusivamente o snapshot 498, sem antecipar aceite da correção.

## 4. Hipóteses herdadas e dimensão superior

[DERIVED — condicional] Trocar a SF por um majorante não cria o pivô. Mantêm-se covariância gaussiana fixa e comum, normalização/densidade e suporte afim comuns, X de posto suportado63, nuisance comum e domínio contendo o nulo verdadeiro. O refinamento17/18 requer o span GLOBAL de todas as diferenças de médias relevantes, não tangente local nem número de parâmetros ajustados. O residual148 depende dos72 vínculos exatos e do posto63 de X na matriz conjunta. Limite superior rigoroso de dimensão é suficiente por dominância estocástica; posto medido exato adicional não é requisito artificial.

A proposta rotula essas condições como não certificadas por este módulo. Cinco pontos teóricos, preflight262 e C08 não certificam todos os cenários nem a SF em domínio geral. O modelo condicional de erros publicados/propagados permanece possível, com alcance explícito; sua ratificação não transforma covariância dependente dos dados em pivô frequentista finito exato. Esta revisão não amplia nem fecha tal aplicação.

## 5. Recurso, família, Bonferroni e não rejeição

A política de retornar1 por recurso está explicitamente separada de falha semântica, identidade ou certificado. Depois de qualificadas estatística e hipóteses, uma majorante1 é pontualmente válida; se a política for escolhida antes da aplicação, produz teste conservador possivelmente sem poder. Não é sucesso da avaliação apertada e não afirma p exato grande. Se não adotada, recurso esgotado fica indisponível. Ambas são alternativas operacionais admissíveis antes de dados; falha científica continua INVALID/UNAVAILABLE e p=null. O prazo30s é nominal e não garantia de contenção do sistema; custo e limites ainda não foram medidos. Não se deve exigir que este documento já os tenha medido.

[REAL — igualdade documental] Os decision_predicates incorporados no JSON são exatamente iguais ao objeto verdict.decision_predicates do V2 pinado, conferidos por comparação estrutural. Por teste, o máximo é sobre toda a família admitida, não o subconjunto disponível. Se algum cenário do nulo composto é verdadeiro, o máximo domina o p conservador desse cenário: não se exige fator600 adicional. Bonferroni5 cobre a família de cinco testes com dependência arbitrária. Falta de cenário impede somente o robusto correspondente, sem apagar uma rejeição completa independente. H1 não rejeitada exige os dois controles H1 válidos; direção positiva permanece requisito de cada contraste dirigido.

Comparar p_FWER<=alpha_lo é suficiente para rejeição e p_FWER>alpha_hi para dizer que o envelope adotado não rejeita; sobreposição é comparação não resolvida. O limiar unilateral exato não foi avaliado ou alterado. Mesmo uma cota válida igual1 não autoriza confirmação, adequação, poder ou não rejeição de um teste que ainda carece de estatística válida/família completa. Bayes continua separado.

## 6. Resultado da revisão e próximos passos

[REAL] Parecer documental suficiente para localizar TE-01 e conferir as derivações; não houve necessidade nem autorização para avaliação numérica. A proposta tem três alternativas reais de cálculo (SF intervalar, Chernoff intervalar, envelope racional fixo), com perdas de aperto e lacunas de implementação explícitas. Nada foi escolhido por significância observada.

[OPEN] Aguardar e conferir somente delta selado que preserve d>0, N/Q, cinco testes, modelos, limiar e fonte histórica. Depois, cabe à coordenação decidir uma nova preparação/qualificação delimitada. Este parecer não autoriza execução, não abre dados, não congela V1, não conclui F1 nem altera gate.
