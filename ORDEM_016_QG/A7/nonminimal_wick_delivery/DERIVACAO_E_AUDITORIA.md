[DERIVED — jatos completos no setor antifield, prescrição euclidiana explícita; Q2 OPEN]

# A derivada do bloco misto participa da primeira ordem

Usamos o espaço-forma4D, K constante, os operadores mínimos Lh e Lq já
calculados e Hr=U0/z-U1 log(z/l²)/4+U2 z log(z/l²)/16+..., sem acrescentar
parte suave. Todos os números abaixo usam coeficiente comum de1/z igual a1;
o normalizador físico e a continuação lorentziana NÃO foram fixados aqui.

Da apresentação graduada068/069, transportada apenas como identidade de
blocos, Hfull tem hh=HD=-4κ Hh Itr, hb=Kg HQ, bh=HQ Kg*, bb=0,
cbarc=HQ, barcc=-HQ. ell=1/(2κ), D=H0+ell C*C. Defina

 S=ell C HD-HQ Kg*.
 (P Hfull)_hh=D HD-C*S, (P Hfull)_bh=S/ell,
 (P Hfull)_bb=(P Hfull)_cc=(P Hfull)_barcbarc=Q HQ.

A primeira igualdade mostra por que não bastava inserir3U2/4 diretamente.
S vale zero no ponto por isotropia, mas sua DERIVADA pode ser não nula.
Nenhum estado do fundo distinto de068 foi transferido para este modelo.

# O primeiro jato misto foi calculado

O entrelaçamento Lh Kg=Kg Lq implica, por unicidade formal de transporte do
calor, B_n=A_(n+1)/4, onde B_n=div_x U_h,n+sym nabla_y U_q,n e A_n usa
os mesmos slots com nabla z. A0=0. Diferenciando o parametrix, os termos
1/z e log(z) cancelam, restando B_H=A2/16+O(r³log r).
Como S=-2B_H, seu primeiro jato é -nabla A2/8. Usando os U2 já medidos:

 [nabla_lambda S_nu](h)=K²[-25g_lambda,nu tr(h)/12+10h_lambda,nu/3],
 [C*S]=K²[-10P_TL/3-5P_tr].

O passo de transporte teve um controle independente em16 componentes:
os segundos jatos ORDENADOS de U1h e U1q reproduzem nabla A2/4.
O jato misto do calor é -xx_ji por Synge; não foi confundido com o jato
logarítmico do Green (a2 delta/2-xx_ji). A identidade formal de calor é
hipótese/derivação escrita; o CAS confere estes jatos e a álgebra, não constrói
um estado global nem prova microlocalmente toda a expansão infinita.

Na convenção da bancada qhdagger=H0h+C*b e qcdagger=-Qbarc-Kg*hdagger,
os slots estendidos tornam-se

 Jh0=K²(137P_TL/60+579P_tr/20), Jc0=179K²I4/20.

Jh1/Jc1 têm posto ímpar e zeram sob a covariância natural/paridade assumidas.
Para Faf=int chi(hdagger Lie_c h+cdagger_i c^j nabla_j c^i):

 A1(Faf)/(i hbar)=(337/10)K² int chi div(c).

A expressão recebe ainda o fator comum de normalização física da covariância.
Ignorar C*S daria81/5; a contribuição perdida é35/2, todos multiplicados porK².
A primitiva algébrica deste setor é337K² int chi tr(h)/20, pois qtrh=2divc.
Não é ainda escolha de contratermo: admissibilidade, realidade e continuação
precisam acompanhar o dicionário físico. Inventário de todoV1 e Q2 permanecem
separados. São49controles exatos, CPU0.09375s, rc0.

# Revisão independente MiMo87d recebida e auditada

O MiMo identificou corretamente o canal antifield-Euler e a insuficiência
de C(Faf)=0. Seu teste par qdagger=-x dá+w e foi mantido nessa convenção.
Não adotamos os sinais compactos: a fórmula escrita para[q,partial_odd]
omite o sinal graduado. Contraexemplo qx=c: [q,partial_c]_graded x=+1;
a fórmula escrita daria-1. A ordem das derivadas ímpares no C_H escrito
também dá C(cbarc)=-H_cbarc, exigindo dicionário antes de transferir sinais.
Além disso, Qbarc contém duas derivadas; com a derivada do outro slot,
precisam-se jatos mistos de ordem3. x²y+xy² tem todos os jatos≤2 nulos
na origem e derivada xxy=2: o limite de ordem2 da resposta não basta.
São13controles locais; detalhes e original preservados.

DeepSeek recebeu para admissão uma revisão cética distinta do jato misto
e do coeficiente337/10; preview selecionou o executor requerido. Kimi
mantém os pedidos existentes sujeitos à recuperação real da quota5h.
Nenhum original, kernel ou gate alterado. AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
