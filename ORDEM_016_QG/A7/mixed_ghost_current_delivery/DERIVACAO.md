[DERIVED — blocos planos de correntes calculados; Q2 OPEN]

## Normalização livre antes da contração

Use10 componentes simétricas, Gram R=diag(2-delta_ab), reversão de traço Itr
e S=Itr R^-1. Para símbolos diferenciais reais p, escreva Gc=p_a c_b+p_b c_a,
C(h)=p.h-p trh/2, q=p.p e E=-q Itr+Itr G C.
A matriz bosônica da ação é P=[[R E/(4kappa),-C^T],[C,-2kappa I]].
A inversa simbólica é P^-1=(1/q)[[-4kappa S,G],[-G^T,0]].
CAS verificou os DOIS produtos, com p e kappa simbólicos, além de CG=q I,
EG=0 e CS=G^T/2. O sinal inferior vem do adjunto formal de uma derivada.
Isso realiza a fórmula BV069; o zero b-b não elimina a linha mista b-h.

O vértice raw quadrático do motor em momentos Fourier(p,-p) foi comparado
com -2 R E em todos100 pares de fibras e dois momentos não axiais.
Assim o sinal de símbolos diferenciais não foi confundido com o de i.p.
Raw V3=16kappa V3fisico, GD=-4kappa S GQ e Ghb=G GQ dão fator-1/4
para UM emparelhamento ordenado X(h,h)-Y(b,h), antes dos fatoriais do diagrama.
Esse fator vem da inversão/ação; não foi escolhido para zerar resultado.

## Corrente mista

Jb^mu=b_nu[Z_mu,nu-delta_mu,nu trZ/2], Z=L_c h.
Seu vértice foi expandido em b_nu, h_ab, suas derivadas e c_r, dc_r.
160 comparações simbólicas verificam a expansão para todos r,nu,ab.
O vértice EH emX inclui a fronteira -8dchiX.b3. A contração preserva as
duas orientações b-h; elas foram medidas iguais. O engine retorna UMA
orientação. Somar ambas e ainda incluir o fatorial1/2 é uma decisão que
deve sair da expansão de Wick global, não de comparação numérica.
575checks, CPU3.1875s, rc0.

## Corrente ghost

Jgh^mu=(d_mu barc_nu)c^rho d_rho c^nu
 -barc_nu(d_mu c^rho)d_rho c^nu-barc_nu c^rho d_mu d_rho c^nu.
No produto ordenado(barX,cX,barY,cYA,cYB), as duas escolhas de cY externo
têm sinais totais-,+ (incluindo <barX cY>=-GQ). Uma álgebra exterior
independente calculou Gamma_G²/2 sobre o monômio de cinco geradores e
recuperou esses sinais. Inverter a covariância muda ambos os resultados.
As duas contrações dirigidas foram incluídas, com fronteira ghost emX e
adjunção dos jatos de h_X e c_Y. Omitir qualquer uma altera o controle.
286checks, CPU0.96875s, rc0.

## Números no escopo declarado

Para h11,c0, x=(1,2,-1,1) e contato emq=(2,1,0,0), unidade CE=-4pi²:

| jatos(lambda,eta) | b-h ordenado fora diagonal | contato b-h | ghost fora diagonal | contato ghost |
|---|---:|---:|---:|---:|
| (0,0) |0|0|0|0|
| (0,e0) |-128/16807|259/192|2671/117649|-4391/3840|
| (e0-e1,e0) |1222/16807|35/32|-4941/235298|-2651/3840|

A extensão é a prescrição anterior R=FP[(1-a)mu^(2a)z^a], com C_D=RD-DR
e transferência completa q->q-lambda. Os polinômios completos estão nos JSON.
Não somamos esses blocos como Q2: faltam pesos globais conferidos, curvatura,
partes suaves/tadpoles e demais aridades/continuação causal exigidas na A7b.

Falha inicial preservada: eta=0 deixa soma vazia, int0 sem método subs.
v2 muda apenas o acumulador de contato para Integer(0). Não mudou coeficiente.
Script/check/log v1 e diagnóstico permanecem com hashes no manifesto.

Total861checks, CPU4.15625s. Nenhuma chamada externa nova nesta computação.
Custo externo conhecido recontado no ledger:US$1.4569561218, parcial/estimativa,
não fatura; assinaturas e chamadas sem consumo informado continuam desconhecidas.
Originais, um.py, kernel e gate não foram alterados.
Abertura sha256:216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
