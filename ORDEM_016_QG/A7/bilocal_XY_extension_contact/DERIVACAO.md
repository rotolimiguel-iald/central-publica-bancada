[DERIVED — contato do par singular hc, até O(K), em duas extensões euclidianas; Q2 OPEN]

# Derivar o regulador antes de ancorar

Conservam-se os vértices, propagadores e pesos -metrico/2+ghost da
identidade bilocal não coincidente. O operador de fonte é o mesmo E.
O fator de extensão é F_a=(1-a)mu^(2a)rho^(2a), e se mede também a
completação de comparação w^a, com w=(X-Y)². Nenhuma das duas é escolhida
pelo valor do resíduo. Em Y=0, ambas têm rho²=w=z=X², mas suas segundas
derivadas em Y diferem. O cálculo conserva essa diferença.

## Jatos necessários

Escrevendo f=log rho², na origem de Y:

    f_Yi = -2Xi/z,
    f_YiYj = 2delta_ij/z-4XiXj/z²
              -(2K/3)(delta_ij-XiXj/z).

O último termo está ausente para w. Assim, para qualquer coeficiente U
de um vértice (tensor ou matriz nas fibras),

    rho^(-2a) D_Yi(rho^(2a) U)-D_Yi U = a f_Yi U;
    rho^(-2a) D_YiD_Yj(rho^(2a) U)-D_YiD_Yj U
      = a(f_Yi D_Yj U+f_Yj D_Yi U+f_YiYj U)
        +a² f_Yi f_Yj U.

O motor aplica essas regras às contrações existentes. Termos sem
derivada externa de Y comutam com o regulador e não contribuem ao
defeito. Os vértices algébricos de curvatura continuam presentes na
parte com uma derivada. O termo de fonte antes da integração é A+B^j D_jc;
logo a correção da fonte C=A-divY B é deltaC=-a f_Yj B^j.

Foram recuperados todos os três coeficientes O(4) de h_X, os sete de
D_Xh_X e os três da fonte; mantidos os polinômios em a e L=log(mu²z).
O motor confere componentes não usadas na extração (320 igualdades).
A fonte foi controlada contra a implementação plana anterior e em
ponto não axial nas ordens K0/K1. A comparação do raio auxiliar impõe
w=X² somente após derivar. O primeiro teste esqueceu essa relação e
falhou com (2/3)(1-X²/w); a versão corrigida do teste está preservada
ao lado, sem alteração dos coeficientes calculados.

## Soma após as duas integrações

Se C0,C1 são os coeficientes de h e Dh depois da integração não regulada
em Y, a identidade anterior é C0-divX C1+EC=0 fora da diagonal. Portanto
o contato no extremo X é a parte finita de

    F_a [-2a Xi C1^i/z + E_a C - EC],

onde E_a=z^(-a) E z^a. O motor reutiliza E com a regra exata

    D_i -> D_i + 2a Xi/z

e converte seus dois índices covariantes de coordenadas para o frame.
A correção adicional originada em Y é a parte finita de

    F_a [deltaC0-divX deltaC1-2a Xi deltaC1^i/z+E_a deltaC].

A divergência inclui as conexões dos três índices em X. Em ambos os
casos o elemento de volume acrescenta -Kz/2 vezes a parte plana.
Os índices de Y não recebem conexão de X. Esse procedimento não
comuta E ou as derivadas através da extensão sem contabilizar o resto.

## Parte finita, inclusive logaritmos

As distribuições racionais homogêneas têm polo simples. Como o defeito
é divisível por a, para D(a)=aD1+a²D2+... temos, em unidades do resíduo:

    FP[(1-a) D(a) z^a u] = Res(u) D1;
    FP[(1-a) D(a) z^a log(mu²z) u] = Res(u)(D1-D2).

Logo os termos a² log NÃO podem ser descartados. A extração foi
conferida diretamente por série de Laurent. Os resíduos de monômios
foram conferidos também por integração radial e momentos exatos de S³,
independentemente da fórmula por derivadas de delta (280 pares de
monômio/potência no conjunto da soma).

O resultado está em results.json. A base é

    K0: delta_ab qr(q²)², (delta_ar qb+delta_br qa)(q²)²,
        qa qb qr q²;
    K1: delta_ab qr q², (delta_ar qb+delta_br qa)q², qa qb qr.

Os coeficientes multiplicam C_E=-4pi², ainda com os fatores comuns dos
propagadores removidos como nos motores anteriores. q significa
derivadas da delta em coordenadas normais, com os testes em frame e a
densidade de volume já incluída. Não é um novo parâmetro espectral.

A diferença entre as duas completações é zero em K0 e
(-35/144,-1/12,7/72) na base K1 acima. É uma diferença LOCAL de extensão,
não uma diferença do núcleo não coincidente. Omitir logs altera o
contato: o controle negativo registra explicitamente esse erro.

## Primitiva no recorte plano

Chamando os três coeficientes planos de u,v,w, tome duas constantes
livres b,c e a Hessiana de ordem quatro com coeficientes

    (v-c/2, u/2-b, b, c, w/2-b-c/2)

na base de cinco estruturas indicada no script. Ela é autoadjunta
formalmente e satisfaz N G=A_plano para todos os componentes e momentos.
Consequentemente B_bc=-C_E/2 integral h.N h obedece s0 B_bc=-A_hc
nesse recorte integrado plano com suporte compacto (180 verificações).
Nenhuma escolha de b,c ou subtração foi adotada na prescrição.

## Pendências preservadas

Este contato é do par singular métrico/ghost mais a fonte especificada.
Não inclui todos os diagramas locais, W suave geral, K², aridades não
lineares ou valores de contorno lorentzianos. A primitiva plana não
demonstra extensão curva ou não linear. Para a convenção A1=-s0 B e
s0 A2+s1 A1=0, a combinação fechada correta na próxima ordem é
A2+s1 B, não A2-s1 B. A auditoria do Kimi registra esse sinal com
contraexemplo graduado exato. A Q2 completa não foi declarada calculada.
