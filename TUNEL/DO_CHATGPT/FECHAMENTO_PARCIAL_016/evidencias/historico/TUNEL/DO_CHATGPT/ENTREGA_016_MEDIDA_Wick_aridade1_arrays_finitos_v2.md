[DERIVED — aridade1 condicional e CAS graduado; A1 curvo numérico e Q2 OPEN]

# Transporte de Wick sem redefinir o diferencial para forçar zero

Hipóteses explícitas: uma representação livre G equivarante já fixada;
H é o parametrix local; W=G-H é suave; não há contrações de antifields.
A derivação quântica é fixada em geradores/Leibniz, não escolhida por
conjugação de H. As equações7,20–21,140/160 de Fröb1803.10235v3
fornecem as convenções de representação; usamos a relação
N_H=N_G exp(i hbar C_W). Fonte primária consultada nesta rodada:
https://arxiv.org/pdf/1803.10235v3 (pp3,5,31,37).

Como q é linear e C_W é uma contração de coeficientes independentes dos
campos, R_W=[q,C_W] tem coeficientes constantes e [C_W,R_W]=0. Então

 exp(-t C_W) q exp(t C_W)=q+t R_W,
 A1(F)=i hbar R_W F.

Isto deriva a correção em H a partir da derivação livre fixa em G. Não
declara existência de G/H completos no alvo. Uma troca de estado G+B
preserva esta fórmula quando [q,C_B]=0; suavidade sozinha não basta.
São 1483 controles em 488 monômios
da álgebra graduada finita, com testemunhas não nulas; não são uma prova
de existência de covariância no espaço-tempo. CPU3.296875s.
Exemplo: q(hdagger)=m h, F=hdagger h c, C_W F=0, mas
C_W(qF)=m W_hh c e R_W F=-m W_hh c. O termo Euler não desaparece.

# O vértice existente exige quatro arrays finitos

Use coordenadas independentes h_A simétricas e antifields duais. Escreva
Lie_c h_A=c^k nabla_k h_A+M_A^B(nabla c)h_B. Seja D_H o defeito Ward
estendido a campos/antifields: no slot hdagger ele inclui a equação livre
completa, inclusive b; no slot cdagger, a equação ghost e seus sinais.
Defina os quatro arrays no ponto de coincidência:

 Jh0[A,B]=[D_H(hdagger_A,h_B)], Jh1[k,A,B]=[nabla_y,k D_H(hdagger_A,h_B)],
 Jc0[i,j]=[D_H(cdagger_i,c^j)], Jc1[k,i,j]=[nabla_y,k D_H(cdagger_i,c^j)].

Para Faf=int chi(hdagger Lie_c h+cdagger_i c^j nabla_j c^i),

 A1(Faf)/(i hbar)=int chi [c^k Jh1[k,A,A]+M_A^B(nabla c)Jh0[A,B]
                         +Jc0[i,j]nabla_j c^i-Jc1[j,i,i]c^j].

A última subtração é Grassmann; omiti-la falha no controle. Até três
derivadas de H são necessárias, porque a equação livre tem ordem2 e
o vértice acrescenta uma. Os11controles dos slots não
medem esses arrays do multiplet completo. O resto mínimo3U2/4 calculado
antes NÃO pode ser substituído diretamente por Jh0/Jc0.

Se, adicionalmente, os arrays são naturais, invariantes de espaço-forma
e pares sob O4, seus primeiros jatos têm posto tensorial ímpar e zeram.
Escreva Jh0=aTL P_TL+aTr P_tr, Jc0=d I4. A representação simétrica dá
tr(M P_TL)=9 div(c)/2 e tr(M P_tr)=div(c)/2. Logo

 A1(Faf)/(i hbar)=(9aTL/2+aTr/2+d) int chi div(c).

Nesse setor condicionado, a primitiva linear é metade desse coeficiente
vezes int chi tr(h), pois q tr(h)=2 div(c). Verificado por9
controles matriciais. Não se supôs que M preserva cada setor. Não é a
anomalia de todo V1, nem família admissível/reality de contratermos já paga.

# MiMoa46 — resposta preservada, cálculo e limitação do pedido

O prompt da bancada dizia f_a,g_a «acima», mas não os definia, nem definia
tau. Essa lacuna é minha. MiMo adotou f_a=g_a=z^(a-1) e tau como contato
finito; também chamou Euler de dilatação. Não transportamos essa resposta
como se fosse o cálculo com tau de alocação feito antes pela bancada.
Seu contato q²/16 para uma linha no esquema simétrico é correto.

Para f_a=z^(tau a-1), g_a=z^((1-tau)a-1), com o mesmo prefator de R:
FP[(box f_a)g_a]/CE=tau q²/8; a outra linha dá(1-tau)q²/8.
O gradiente total é8R3/CE+q²/4; a soma é8R3/CE+3q²/8.
C_box(z^-2)/CE=-3q²/8, independente da escala. Mantidos tau0,1,1/2
como diagnósticos, sem adotar um deles. São15controles.
Corrigidos ainda o grau6 de x_i x_j z^-4 e a ausência indevida de box delta
na tabela de grau≤4. Grau de escala sozinho admite termos inferiores;
restrições homogêneas/dimensionais adicionais devem ser declaradas.
Nenhum motor anterior foi refeito, nenhum parâmetro foi ajustado.

MiMo87d está executando a revisão independente da fórmula de aridade1;
as conclusões locais não foram inseridas em seu prompt. Q2/gate intactos.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
