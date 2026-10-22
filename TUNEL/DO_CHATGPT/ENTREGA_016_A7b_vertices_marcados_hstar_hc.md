[DERIVED — topologias e pesos relativos; REAL — CAS exato nos casos descritos; OPEN — identidade tensorial geral e Q2 finita]
# A7.b — h*hc completa a identidade principal h*cc nos casos medidos

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T23:05:48.359856+00:00.

## Convenções e derivação anterior à soma

Mesmos BV069, gauge C de fundo LINEAR e modelo principal Euclidiano tangente
de087; não se substitui a geometria Lorentziana. h* e c* são fontes sem
propagador. Fourier +i, P=4κS0/q², Q^-1=-I/q². S0 é a inversa da forma
tr(EiEj)-tr(Ei)tr(Ej)/2 na base simétrica de10elementos. A fonte h*L_c h
é iU, U_m(T,H,k,l)=k_m tr(TH)+2(HTl)_m. O vértice ghost é

    V_nu,rho(H,k,l)= -[k_rho(H(k+l))_nu+((k+l)·l)H_rho,nu
                        +l_nu(H(k+l))_rho
                        -(k+l)_nu k_rho trH/2-(k+l)_nu(Hl)_rho].

A expansão conectada de -log Z dá -<S_h* S_c> para a bolha mista, isto é
-i U P Q^-1 V após ordenação das variáveis externas ímpares. Assim a bolha
h*c tem fator COMUM +4iκA0, A0=1/(8π²), e kernel R0 já medido.
Derivar essa expressão em h, conservando o fundo de gauge, usa
δP=-P H1 P e δQ^-1=-Q^-1 V_h Q^-1. Há exatamente DUAS topologias1PI:

    +i U P H1 P Q^-1 V       (inserção métrica);
    +i U P Q^-1 V_h Q^-1 V   (inserção ghost).

Não há fonte h*hhc, nem ghost barc hh c, nessa parametrização linear.
Pôr a perna externa h ou c na fonte bilinear deixa apenas uma ligação
interna na fonte, criando grafo1PR, não contribuição1PI. b não participa
de vértices interagentes neste gauge. Os fatores são fixados ANTES da conta:
(4κ)^2/(16κ) vezes o inverso ghost negativo dá -iκ; duas inversas ghost
e uma linha métrica dão +4iκ. Logo R1=G-M/4 depois de remover4iκA0.

Para h*(T,-p-r),h(H,p),c(v,r), escolha q na linha métrica da fonte e
l=p+r-q. A outra linha ghost tem k=r-q. Os numeradores exatos são

    NG=Σij Sij U(T,Ei,q,l)·V(H,p,r-q)V(Ej,-q,r)v,
    NM=Σijkm Sij Skm U(T,Ei,q,l)·V(Em,p-q,r)v
                          ×W(H,p,Ej,-q,Ek,q-p),

W=16κ V3. Denominadores NG: q²(q-r)²(q-p-r)²;
NM: q²(q-p)²(q-p-r)². Os índices pareados estão explícitos, sem pressupor
simetria de W com o encaminhamento fixado. W foi reconstruído como polinômio
quadrático em q e conferido fora dos pontos de interpolação.

O coeficiente de c*cc da entrega anterior recebe o MESMO fator4iκA0.
O fator1/2 da fonte antissimétrica é cancelado pelas duas contrações:
reordenar as pernas externas ímpares fornece +G_ad G_be-G_ae G_bd.
Um verificador independente de permutações e Wick confere esse sinal, o
da bolha mista e o da inserção ghost. Não ajustamos um sinal para obter zero.

## Relação testada e resultado

Retirados os fatores comuns, K_p v=p⊗v+v⊗p, L é a derivada de Lie sem i,
B(p,v;r,w)=(v·r)w-(w·p)v e
R0(p)v=-3/8 p² K_pv+1/2 pp^T(p·v). O componente h*cc da identidade BV é

    K_(p+r) B1(v,w)+R0(p+r)B(v,w)
    -L_v R0(r)w+L_w R0(p)v
    -R1(K_rw,v)+R1(K_pv,w)=0.

Projetamos em T. B1 é o triângulo c*cc efetivamente calculado, não a
redefinição bilinear insuficiente da entrega anterior. Nos quatro casos de
eixos e quatro casos adicionais o resíduo é EXATAMENTE ZERO. Exemplo de
eixos: 7/12+0-1/6-5/12=0. Exemplo denso não axial:

    3739/12 + 216 - 39/2 - 6097/12 = 0.

O segundo conjunto inclui momentos não ortogonais, colineares e um momento
externo zero. O último é apenas extração UV formal, não integral sem escala
renormalizada. O programa independente confere fatores de Grassmann por
recursão de Wick, além da integração simplex das duas topologias em um caso
denso. A primeira conta conferiu16integrações simplex adicionais.

## Alcance

marked_vertex_check: rc0, 16checks de integração independente,
4resíduos BV nulos; wall 12.308727299969178s,CPU 12.171875s.
marked_vertex_independent_check: rc0, 11checks,
5controles que recusam sinais/fatores ou omissões;
wall 38.10376639995957s,CPU 37.8125s. Remover qualquer das duas
topologias quebra o caso denso. Omitir a permutação de variáveis ímpares
também falha. Código, planos prévios, resultados e logs estão nos manifestos.

Essas verificações NÃO demonstram ainda a identidade tensorial para todos
os momentos/polarizações; essa obrigação está discriminada para a revisão.
Tampouco calculam a anomalia causal FINITA, curvatura/cutoffs ou todos os
vértices da QME. A contribuição que faltava à comparação de c*cc foi
localizada e medida; o aparente desencontro com a redefinição bilinear não
autoriza dizer anomalia. Q2 ainda não paga; nenhum kernel/um.py/gate alterado.
