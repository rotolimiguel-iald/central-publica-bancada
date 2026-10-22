[DERIVED — extensão da candidata local; REAL — CAS; OPEN — identificação com Q2 completa]
# A7.b — cutoff e descida não linear da primitiva quadrática
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T05:30:18.530730+00:00.

Prossegue a família D_t da entrega Ward_K2_e_primitiva_quadratica_local,
sem escolher t nem adotar um contratermo. Fixe a referência espaço-forma,
K constante, cutoff real inerte chi e suporte compacto. Todas as
contrações e a medida abaixo são da referência, inerte sob s.

## 1. Operador localizado e corrente nova
Escreva D_t=K C^ij nabla_(i nabla_j)+K² A. Os coeficientes C e A são
paralelos e simétricos entre as fibras. Para tensores simétricos X,Y,

    C^ij(X,Y)=-delta^ij(d1 X.Y+d2 trX trY)
      -d3(X^ij trY+trX Y^ij)
      -d4/2 (X^i_a Y^ja+X^j_a Y^ia),
    A(X,Y)=(t+7/3)X.Y-(t+22/3)trX trY,
    (d1,d2,d3,d4)=(1/2-t/2,9/4+t/2,-1-t/2,t).

A escrita em quadro ortonormal se covariantiza com a métrica de
referência. A simetria de C e A é algébrica; foi também conferida em
toda a base de dez fibras, todos os dezesseis pares de índices e nos
dois coeficientes afins em t. Não se pressupôs autoadjunção do operador
localizado chi D isolado. O gradiente correto é

    B_chi[h]=1/2 integral chi h.D_t h,
    F=M_chi h,  M_chi=(chi D_t+D_t chi)/2
                =chi D_t+[D_t,chi]/2,
    [D_t,chi]T=K C^ij[(nabla_i nabla_j chi)T
                                  +2(nabla_i chi)nabla_j T].

O termo K² comuta com chi. Na prova escrita, integração por partes,
paralelismo e simetria fornecem estas identidades para campos suaves
de suporte compacto. O CAS usa jatos polinomiais em coordenadas
normais até K², com a conexão já calibrada; o produto chi*h foi
calculado por dois caminhos: antes das derivadas coordenadas e pela
regra covariante de Leibniz.

## 2. Variação não linear explícita
Na convenção da classe087, s h=L_c(gbar+h), s c=c.grad c. A segunda
igualdade é ímpar: equivale a [c,c]/2, não a um colchete de vetores
comutativos iguais. Referência, t e chi são inertes. Segue

    s B_chi = integral [G(c)+L_c h].F
            =s0 B_chi+s1 B_chi,
    s1 B_chi=integral (L_c h).F.

Depois de uma integração por partes, a corrente do ghost é

    J_r=F^ab nabla_r h_ab
             -2 nabla_a[(gbar_rb+h_rb)F^ab],
    [G(c)+L_c h].F = c^r J_r
             +nabla_a[2c^r(gbar_rb+h_rb)F^ab].

Isso exibe o termo h²c e a corrente de fronteira, incluindo as
derivadas de chi dentro de F. Não se confundiu a densidade pontual
com seu funcional integrado. Fonte da convenção BRST: classe087,
SHA256 `bd1a27316e99c33718e583f9442f8869bc3a234c63e3d20c74ee36abec43da5c`; não se transportou seu H4 para ghost1.

## 3. Consistência da candidata, com a fronteira mantida
Para dois parâmetros pares u,v usados apenas na polarização dos
dois ghosts ímpares, L_u L_v-L_v L_u=L_[u,v]. A checagem covariante
incluiu a referência e a perturbação, até duas derivadas externas e
K². A polarização da variação da densidade deixa a expressão de
Green com X=L_v(gbar+h), Y=L_u(gbar+h):

    X.M_chi Y-(M_chi X).Y = nabla_i I^i,
    I^i=K chi [C^ij(X,nabla_jY)-C^ij(nabla_jX,Y)].

Essa identidade decorre da forma divergente
M=K nabla_i(chi C^ij nabla_j)+K C^ij chi_;ij/2+K²chi A.
Logo s(sB_chi)=0 como funcional integrado, com a corrente local
indicada. É a consistência de uma candidata exata já construída;
NÃO é inferência de que toda quebra quântica seja essa candidata.

## 4. Evidência e alcance
8205 verificações exatas; CPU 3.6875s. Três controles negativos:
omitir o contatochi deixa835/4 em uma componente; omitir s1B deixa
53611 em uma amostra; sinal errado do colchete deixa-10. Uma segunda
auditoria encontrou12 amostras com divergência pontual não nula,
embora a corrente integre a zero no suporte compacto. Os números são
dos campos de teste normalizados no script, não constantes físicas.

**O que foi pago:** extensão local com cutoff e variação não linear
da família quadrática que cancelava o componente h*c logarítmico
medido. **O que falta nesta etapa:** comparar s1B com o coeficiente
quântico h²c e ligar as partes finitas da prescrição temporal aos
mesmos grafos covariantes. As identidades universais de contato
logarítmico já existem e serão reutilizadas; não se introduziu uma
nova prescrição. Nenhum t escolhido, gate movido ou original alterado.
