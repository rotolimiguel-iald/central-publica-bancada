[DERIVED — plano de cálculo dentro de A7.b; hipóteses de implementação ainda a testar]
# Próxima contração da bolha em posição — não é resultado já calculado

Usar metric_radial_bitensor_engine.py com suas2500comparações e angular_cubature/results.json.
Não somar um perfil completo aos E-insertions: estes já estarão nele, usar como controle de decomposição.

Representação proposta: cada perna interna tem índice (d,a), d=-1 semderivada ou0..3 comuma, a=0..9 fibra.
Vértice Gamma-Gamma tem no máximo uma derivada em cada campo. Formar matrizes50x50 W_A(d1a,d2b).
Separar N_X=1 (derivada no campo externo) e N_X=2 (externo semderivada); W00=0.
Extrair usando eh_cubic_16k(A,p,Ea,q,Eb,r), SEM impor r=-p-q até a integração por partes.
Termos q_i e r_j são W_i0,W_0j; termos q_i r_j são W_ij. Verificar Bose entrepernas.

Escolher A noquadro radial emX, B emY=0, fases externas exp(-ipX),exp(+ipY).
Na covderivada deA entra p_X=-p-K(zI-xx)p/6 e ainda -i*A_i^rep A no numerador de momento.
O termo geométrico deconexão externo é linear emx; pré-computar porquatrodireções. GaugefixingC_glinear nãoacrescentaV3.
Gbig(d,a;e,b)=nabla_Xd nabla_Ye H_ab (d/e=-1 omitidos), matriz50x50.
Condição decontração a testar explicitamente por4índices: frobenius(G.T W_X G,W_Y), mantendo posições das pontas.

Fatores: substituir cada momento interno por -i*nabla. Para N=N_X+N_Y,
parte plana usa Taylorj=N, coef(-1)^N*(p.x)^N/N!;
primeiraK dos propagadores evolume usa j=N-2, coef(-1)^(N-1)*(p.x)^(N-2)/(N-2)!;
correçãop_X de coframe tambémj=N-2;
conexão externa (-i extra) usa j=N-1, coef(-1)^N*(p.x)^(N-1)/(N-1)!.
Incluirmedida sqrt(g_X)=1-Kz/2. Normalização prevista rawbubble/A0 =angularmean/16.
ESSAS REGRAS SÃO CANDIDATAS: validarprimeiro todo coeficienteplano contra metric_bubble_v2 antes da curva.

Na primeiraK, graus angulares previstos<=6; no plano<=8. Provar/medir cota antes de cubatura.
Em nó inteirov, z=v², todos termos da expressão com Taylor têm grau-4: avaliar e multiplicarz²;
isso dá ovalor na esfera semraízes. ManterL simbólico; coeficientes deL podem produzirpólosmaiores,
não descartar antes de verificar sua soma angular e a prescrição deextensão.
Se usararrays inteiros, G0 denominadorcomum2z³ eG1semL denominador24z²; conferirconversões.

Um perfil emquadrosradiais nãoé automaticamente umaHessiana covariante integrada.
Converter/apurar adjuntos e divergências, eventualmente usando o caso ghost jápago como controle;
não escolher4coeficientes porWard=0. A fontecurva produzresíduo não nulo jámedido.
Correções deordemK², partefinita/estado/cutoff continuamdevidas depois.
