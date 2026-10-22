[DERIVED — família formal de contratermos; coeficientes físicos K² e Q2 integral OPEN]

A família finita anteriormente calculada N4+K N2 foi completada por
K²(e1 Id+e2 g tr), reutilizando o motor existente de jatos covariantes.
No recorte natural par h,c de grau declarado, o contato ainda desconhecido
é K²[u Gc+v g div(c)]. u e v permanecem simbólicos: não foram medidos nem
ajustados para fechar um resíduo. A primitiva é B=-CE/2 integral h.Nh.

Na carta geodésica:
 e1=4b/3-2c+t+u+28219/4320;
 e2=-89b/6-c/4-t+v/2-208259/34560.
Na carta coordenada:
 e1=4b/3-2c+t+u+8933/1440;
 e2=-89b/6-c/4-t+v/2-63793/11520.
b,c,t são os parâmetros já existentes nas ordens anteriores. Não foram
escolhidos aqui. Os coeficientes distintos não demonstram naturalidade entre
cartas. O cálculo conserva os termos de conexão nos índices de derivadas.
Foram verificadas 128 identidades polinomiais: todas as quatro polarizações
do ghost, 16 componentes tensoriais e ambas as cartas, com os quatro momentos
simbólicos. Mais dois controles de determinação e uma variação independente
totalizam 131 controles, CPU 39.9375s, rc0.
Isto completa a família algébrica condicional neste recorte. Não calcula o
contato efetivo em K² nem prova continuação causal ou QME não linear.

A identidade BV já verificada pode agora ser lida por ordem sem novo teste
artificial. Seja S=S0+gV1+g²V2, (S0,S0)=0, W=gW1+g²W2 e J=gJ1+g²J2.
W é o coeficiente de hbar da ação efetiva; J é o coeficiente de hbar da
inserção da quebra clássica I=(S,S)/2. Ponha A=(S,W)-J e s0=(S0, .).
Jacobi dá (S,A)+(W,I)+(S,J)=0. Extraindo g²:

 s0 A2+(V1,A1)+(W1,I1)+s0 J2+(V1,J1)=0,
 I1=s0 V1, A1=s0 W1-J1, A2=s0 W2+(V1,W1)-J2.

Esta é extração algébrica da identidade existente, não um cálculo novo da
ação efetiva. Mesmo se W1=J1=0 forem efetivamente demonstrados, resulta
s0 A2=-s0 J2, e não a condição homogênea sem a inserção. Normal ordering
sozinho não estabelece essas hipóteses. Tampouco identifica automaticamente
a matriz h,c já calculada com a anomalia completa A2. O alvo restante é
derivar a normalização das inserções Euler e o peso global compatível com
essa identidade, sem escolher a alocação tau por ajuste do resíduo.

Kimi f3 foi recebido e auditado uma única vez. Mantida sua organização
Noether, corrigidos quatro pontos: Qraw+2 sum(Craw), condição de conservação
dos momentos ou corrente de fronteira, duas ordenações da segunda derivada
da métrica inversa, e distinção entre referência BRST-inerte e constante.
Controle: -288+2(40+80+24)=0; a fórmula entregue deixava -144. Fora da
conservação, o controle dá -216. Nove verificações locais, CPU 0.046875s.
Recibo e resposta integral preservados. Nenhuma resposta de modelo foi
promovida a prova por concordância. Uso remoto já lançado no ledger.

Total desta entrega: 140 controles, CPU 39.984375s, dois comandos rc0.
Originais, kernel e gate intactos. Três execuções remotas foram observadas
às15:25:39UTC pelo coordenador: Kimi ee44, MiMo24ad e DeepSeek70e9.
Duas unidades seguintes Kimi e uma MiMo estão preparadas para as vagas da
fila; preparação não é execução. Não despachar novo A7.b após20:32UTC.
Abertura sha256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
