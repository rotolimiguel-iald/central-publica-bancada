[DERIVED — vértices métricos localizados completos até a ordem quártica]

## A divergência que o cutoff não permite apagar

No fundo plano da conta, use a conexão de Levi-Civita do campo completo
g=delta+h e S=-integral chi sqrt(g)R/(2kappa). Contraindo a definição de
Ricci e integrando os termos de derivada da conexão uma vez, obtém-se

    sqrt(g)R = C_GammaGamma + partial_mu B^mu,
    B^mu = sqrt(g)[g^ab Gamma^mu_ab-g^mu,a Gamma^b_ab],
    C_GammaGamma = sqrt(g)g^ab
                  [Gamma^r_as Gamma^s_br-Gamma^r_ab Gamma^s_rs].

Os termos que diferenciam sqrt(g)g^ab usam
partial_mu sqrt(g)=sqrt(g)Gamma^r_mu,r e
partial_mu g^ab=-Gamma^a_mu,r g^rb-Gamma^b_mu,r g^ar.
Substituí-los no produto derivado dá exatamente os dois produtos de
conexões acima. São as convenções do motor já existente.

Para cutoff constante, o segundo termo é uma divergência descartável
no funcional de suporte apropriado. Com chi variável,

    S_chi = -integral chi C_GammaGamma/(2kappa)
            +integral (partial_mu chi) B^mu/(2kappa).

Portanto o vértice GammaGamma não é sozinho o vértice da ação localizada.
B depende da conexão e não foi tratado como um vetor tensorial independente:
é a soma inteira sqrt(g)R que é densidade geométrica.

## Construção sem hipótese de comutação

O motor metric_boundary_current_engine.py extrai a polarização em n pernas
usando variáveis formais t_i com t_i²=0, h=sum_i t_i H_i. Esse quociente
preserva exatamente o coeficiente multilinear procurado. As matrizes H_i
continuam NÃO comutando. Para cada subconjunto S de pernas,

    P_empty=I;
    P_S=sum_(i in S) H_i P_(S minus i);
    (g^-1)_S=(-1)^|S| P_S;
    (log sqrt(det g))_S=(-1)^(|S|+1) tr(P_S)/(2|S|).

Se l é esse logaritmo e d=sqrt(det g), sua exponenciação tem a recorrência

    d_empty=1;
    d_S=sum_(A subset S, i0 in A) l_A d_(S minus A),

com i0 qualquer perna fixa de S. A regra vem de derivar exp(l), retendo o
coeficiente das outras pernas. Ela não presume diagonalização simultânea.
O motor multiplica esses coeficientes nos dois inversos e na densidade de
B; a conexão com índice inferior fornece uma perna diferenciada. Obtém
assim todas as polarizações de B, não só a direção de traço.

Na convenção Fourier exp(+ip.x), escreva B_n=i*b_n e Q=sum_i p_i.
Sua contribuição ao vértice da ação, na normalização já existente, é

    Vnraw_boundary = 2^n Q.b_n,
    Vnraw_full = Vnraw_GammaGamma+Vnraw_boundary,

onde Vnraw=2^(n+1)kappa*Vn. Isso usa i²=-1 em div B e o sinal da ação.
Não há nova divisão por n!: o coeficiente extraído já é a polarização.

## Ward com momento do cutoff

Para o parâmetro vetorial c fixo, delta_c g=Lie_c g. Como sqrt(g)R é
densidade de peso1, delta_c L=partial_mu(c^mu L). Multiplicando por chi
e integrando, a variação é -integral (c.dchi)L. O coeficiente cúbico,
antes da integração com o cutoff, equivale à identidade

    V4raw_full(A,Gc,U,V)+2sum V3raw_full(Lie_c uma das três pernas)
      = 2(Q.v) V3raw_full(A,U,V).

Aqui Q=p+k+r+s pode ser não zero; chi fornece o momento -Q. Todos os
termos têm o mesmo fator i da transformação retirado. O lado direito não
pode ser posto em zero quando o cutoff varia. A identidade universal
decorre da transformação da densidade; o CAS testa a implementação.

Ao contrair U,V com W simétrico, a fórmula fornece o termo de fronteira
do tadpole finito: dividir a expressão acima por16, com os demais
prefatores comuns já registrados. Na parcela quártica a correção é Q.b4.
Devem ser mantidas também as correções cúbicas e o lado direito da Ward;
a parcela quártica isolada não é a soma localizada completa.

## Controles e limite do resultado

O motor passou21 verificações exatas, CPU0.109375s, rc0. Incluem a
normalização de sqrt(1+t), a permutação de pernas, a identidade acima em
seis triplas de polarizações e um diagnóstico que distingue o termo de
fronteira. Em um controle, os dois lados completos são1368; GammaGamma
sozinho deixa defeito72. Cinco dos seis controles detectam a omissão.
Um controle com defeito zero não foi descartado: consta na tabela.

Controle estrutural: em g=(1+u)delta, B=-3du exatamente, logo B_n=0 para
n>=2. Isso explica por que a verificação anterior só na direção de traço
não poderia testar o termo de fronteira quártico. O cálculo presente
completa essa parte nas demais polarizações sem alterar o resultado anterior.

O motor constrói vértices clássicos localizados necessários às contrações
quânticas. Não calculou sozinho extensões distribucionais com esses vértices,
outras aridades, setor ghost completo ou a quebra Q2 integral. É uma
correção explícita da contabilidade de fronteira, não escolha de contratermo,
estado ou horizonte físico. Nenhuma alteração de kernel ou gate.
