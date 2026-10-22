[DERIVED — vértices de curvatura; REAL — CAS exato; OPEN — soma métrica curva]
# A7.b — potencial métrico, duas bolhas e um tadpole delimitado
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T03:18:12.849546+00:00.

**Ação e limite da decomposição.** Com G=g+h, M=I+g^-1h e
C^rho_mu,nu=Gamma(G)^rho_mu,nu-Gamma(g)^rho_mu,nu,
a densidade Einstein–Hilbert integra-se, módulo divergência, como

    sqrt(G)[G^mu,nu Ric(g)_mu,nu
      +G^mu,nu(C^rho_mu,sigma C^sigma_nu,rho
               -C^rho_mu,nu C^sigma_rho,sigma)-2Lambda].

Na integração por partes usa-se
nabla_rho(sqrt(G)G^mu,nu)=sqrt(G)[C^lambda_rho,lambda G^mu,nu
-C^mu_rho,lambda G^lambda,nu-C^nu_rho,lambda G^mu,lambda].
Assim se recupera a mesma parte Gamma-Gamma principal já calculada,
com derivadas de fundo, e o potencial abaixo. O cutoff precisa ser constante
para descartar a divergência; seus contatos não são apagados da missão.

Ric(g)=3K g,Lambda=3K. O potencial de ação é

    S_pot=-(3K/(2kappa)) integral sqrt(g) P(h),
    P(h)=sqrt(det M)(tr M^-1-2).

Escrevendo t=trh,s_j=tr(h^j), os polinômios homogêneos são

    P2=s2/2-t²/4,
    P3=-t³/12+t s2/2-2s3/3,
    P4=-t⁴/64+3t²s2/16-3s2²/16-t s3/2+3s4/4.

O termo linear é zero. A expansão foi conferida independentemente por
autovalores de uma matriz simétrica: polinômios invariantes, não uma
hipótese de comutação entre polarizações diferentes.

Com h0=h-g trh/4, P3=-2tr(h0³)/3. A polarização cúbica fornece

    16kappa V3_pot(A,B,C)/K = 96 tr(A0 B0 C0).

Logo uma perna g anula V3_pot. Também D_g P4=-(3/2)P3, D_gP3=0,
e V4_pot(g,g,A,B)=0. A polarização usada inclui os fatores combinatórios;
não se divide outra vez por3! ou4!. C_g(h) linear não acrescenta vértices
cúbicos/quárticos de gauge fixing.

**Contribuições calculadas.** Mantendo o mesmo S0 e a contração transposta
de metric_bubble_v2, a bolha com UM vértice de potencial e UM principal,
somadas as duas posições, tem coeficiente log/A0

    K[-32p² trAB+20p² trA trB
       -34(pAp trB+pBp trA)+80pABp].

A bolha com DOIS vértices de potencial dá

    K²[576trAB-144trA trB].

São numeradores métricos **sem** o peso -1/2 da Hessiana efetiva.
Usam propagadores principais nas duas linhas. Não incluem correções de
conexão/transporte/endomorfismo dos demais diagramas; portanto não são
o coeficiente métrico curvo total. Em e12/e12,p=e0, dão -64K e1152K²:
não podem ser simplesmente descartados.

O tadpole do POTENCIAL quartico com o coeficiente log universal coincidente
do propagador métrico, proporcional a (K/2)g_ab g_cd nas convenções já
derivadas, é zero por V4_pot(g,g,A,B)=0. Isso não elimina tadpoles do
vértice quartico com derivadas, termos de potência, W suave ou contatos.

**Verificação.** 273 checks,2 negativos,rc0,CPU 5.09375s.
Inclui55 pares bilineares para cada bolha, polarização por diferenças finitas
exatas, simetrias de Bose, expansão determinante/inversa e interpolação dos
vértices principais conferida fora dos nós. A avaliação das15 parcelas de
momento usa o extrator radial já verificado, sem impor Ward=0.

Reprodução: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/metric_curvature_vertices_check.py. Fontes, plano, log e resultados no
manifesto. Próximo elo: quartico com derivadas e seus jatos coincidentes;
depois os demais termos da bolha curva e fontes BV. Q2 permanece aberta.
Nenhum original, kernel, gate ou arquivo canônico foi alterado.
