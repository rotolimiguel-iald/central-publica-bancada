[DERIVED — operador ghost em fundo fixo; REAL — controles CAS; OPEN — contatos causais]
# A7.b — redução covariante da contribuição quadrática ghost
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:46:27.758768+00:00.

Não se varia o fundo g nem se diferencia o calor livre on-shell. Varia-se
somente h no operador realmente presente na ação069: Q(h)c=C_g L_c(g+h).
Identificamos vetores/covetores por g, h como endomorfismo, K a curvatura,
C_nu(h)=nabla^mu h_mu,nu-(1/2)nabla_nu trh. A expansão dá exatamente

    Q(h)=(I+h)(box+3K)+A^lambda nabla_lambda+B,
    A^lambda_nu,rho=nabla_rho h^lambda_nu+nabla^lambda h_rho,nu
                      -nabla_nu h^lambda_rho+delta^lambda_nu C_rho(h),
    B_nu,rho=nabla_rho C_nu(h).

O termo de ordem zero usa dois comutadores distintos. Com a convenção
R^a_bmn=K(delta^a_m g_bn-delta^a_n g_bm),

    [nabla^mu,nabla_rho]h_mu,nu=4K h_rho,nu-K g_rho,nu trh,
    h_mu,a [nabla^mu,nabla_nu]c^a=K(trh g_nu,rho-h_nu,rho)c^rho.

Sua soma é 3K h. Também nabla_lambda A^lambda=B+box h: os dois
comutadores adicionais cancelam por simetria de h. Tudo isso foi conferido
por índices no CAS. Em coordenadas normais, h coordenadamente constante
tem B=-2K h, enquanto box c=partial²c-Kc na origem; o termo 2K h restante
cancela. Esse controle impede confundir componentes constantes com campo
covariantemente paralelo. O operador reduzido reproduz o vértice plano
inteiro, não apenas seu símbolo principal.

## Resíduo integrado, com as hipóteses analíticas explícitas

Perto de h=0, M=I+h é invertível como série formal. Escreva
Qtilde=M^-1 Q=box+3K+a^mu nabla_mu+b, com a=M^-1 A,b=M^-1 B.
Com a conexão nablatilde=nabla+a/2, o endomorfismo é
E=3K+b-(nabla_mu a^mu)/2-a_mu a^mu/4. Até grau2 em h:

    E1=(B-box h)/2,
    E2=-hB+(1/2)nabla_mu(h A^mu)-(1/4)A_mu A^mu,
    Omega1_mu,nu=F_mu,nu/2, F_mu,nu=nabla_mu A_nu-nabla_nu A_mu,
    Omega2_mu,nu=-[nabla_mu(h A_nu)-nabla_nu(h A_mu)]/2
                  +[A_mu,A_nu]/4.

Para o traço local de calor integrado, a classificação de invariantes de
operador Laplace fornece tr(E²/2+R E/6+Omega²/12), além da parte puramente
geométrica fixa e divergências. Os coeficientes 1/2,1/6,1/12 são os mesmos
fixados pelo transporte de calor livre já derivado; o uso dessa classificação
para E não paralelo é uma hipótese analítica explicitada, não uma saída CAS.
Como R=12K,E0=3K e nabla Omega0=0, a parte quadrática, módulo divergências, é

    a4_2 = tr{ 5K[-hB-A_mu A^mu/4]
             +(B-box h)^2/8+F_mu,nu F^mu,nu/48
             +Omega0_mu,nu[A^mu,A^nu]/24 }.

Essa expressão mantém a ordem matricial e os comutadores da conexão. Ela
é covariante e contém a contribuição curva, mas ainda não foi reduzida a
uma base mínima de operadores K nabla² e K² nem combinada ao setor métrico.
Não foi extraída do número de calor livre -571K²/15.

Para identificar seu log com o operador original Q, usamos a ciclicidade
do resíduo logarítmico de símbolos: variando log Q, o fator M acrescenta
Tr(M^-1 delta M), puramente multiplicativo, sem termo de símbolo de ordem-4.
Assim não acrescenta resíduo log. Isto **não** é identidade dos determinantes
finitos; uma anomalia multiplicativa finita/contato não foi descartada.
Ciclicidade/classificação do resíduo permanecem condições analíticas a auditar.
As integrações por partes usam h compacto ou identificam densidades módulo
divergência. Com cutoff variável, suas derivadas precisam ser restauradas.

## Controle contra o laço já calculado

No plano, h=a A exp(ipx)+b B exp(-ipx). O coeficiente de ab em a4_2 é
tr(E1_A E1_B)+(1/6)tr(Omega1_A Omega1_B). Ele reproduz, SEM ajuste de fator,
os cinco coeficientes da bolha ghost já medida, com A0 retirado:

    [1/12,7/48,-1/8,-1/12,1/6].

Conferidos os55 pares da base simétrica, uma polarização densa não axial,
a troca de pernas, o vértice simbólico e os comutadores. 127 checks,
3 controles negativos; rc0, CPU 0.5625s. Retirar a curvatura
da conexão do calor plano altera o teste e12 por -1/3. A peça ghost
isolada continua longitudinalmente não nula (e00/e00 dá1/16).

É uma fórmula candidata explícita para o resíduo ghost curvo, com controle
plano independente. Não é a hierarquia causal completa, não calcula a parte
finita de Q2 e não demonstra cancelamento com os outros setores. A auditoria
externa pedirá a redução dos operadores e um contraexemplo à identificação
do log, se houver. Nenhum original, kernel ou gate foi alterado.
