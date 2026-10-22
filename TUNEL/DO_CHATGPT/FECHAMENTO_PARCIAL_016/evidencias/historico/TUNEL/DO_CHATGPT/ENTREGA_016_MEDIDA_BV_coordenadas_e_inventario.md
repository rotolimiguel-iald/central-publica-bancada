[DERIVED — equivalência de coordenadas BV e inventário condicionado; Q2 OPEN]

# Os sinais são transportados junto com os antifields

A fórmula98 de Fröb1803.10235v3, p26, usa derivadas direita/esquerda e
(phiA,fdagB)=deltaAB; s=(S,.) é a convenção104. Fonte primária lida:
https://arxiv.org/pdf/1803.10235v3 . A expressão seguinte é a correspondência
derivada aqui, não uma nova normalização nem uma afirmação atribuída ao artigo.

Nas coordenadas B da bancada, torne explícito o antibracket:

 (F,G)_B=sum_A epsilonA[(dR_phiA F)(dL_bdagA G)-(dR_bdagA F)(dL_phiA G)],
 epsilonA=(-1)^paridade(phiA).

Com fdagA=epsilonA*bdagA, o pullback do bracket canônico F é exatamente B.
Os campos e suas contrações não mudam. A ação livre B

 Sfree+hdagB Kg c-barcdagB b

vira Sfree+hdagF Kg c+barcdagF b. Ambas dão qh=Kg c e qbarc=-b.
O vértice B hdagB Lie_c h+cdagB c.nabla c vira
hdagF Lie_c h-cdagF c.nabla c. Também qcdag muda de sinal:

 qcdagB=-Qbarc-Kg*hdagB, qcdagF=+Qbarc+Kg*hdagF.

Portanto o sinal do defeito ghost E e o sinal do vértice mudam juntos.
A contribuição +d div(c) de aridade1 permanece. Não é permitido mudar só
um desses sinais e citar a outra convenção. A escolha implícita anunciada
em069 fica agora explicitada; o texto069 original permanece intacto.

CAS: 1185controles, CPU0.890625s, rc0. Foram conferidos
o bracket em monômios até grau3, todos os geradores, o quadrado do diferencial,
o transporte da ação e o monômio cdag c dc. O modelo finito usa um componente
de gauge e não substitui a análise funcional do espaço-tempo. Controle
negativo ímpar: q1h=c h'+2h c', q1c=c c' dá q1²h=0; trocar só o sinal
de q1c dá -2c c'h'-4h c c'', não zero.

# Inventário em primeira ordem

No modelo métrico da087 com gauge linear da069, a interação cúbica é
V1=V1metrico+V1ghost+Faf. As duas primeiras parcelas só têm campos.
A matriz Hfull com hb=Kg HQ,bh=HQ Kg*,bb=0 e blocos ghost +/-HQ
tem defeito de Ward ENTRE CAMPOS igual a zero por multiplicação de blocos,
independentemente de HD ser bisolução. Seu defeito Euler estendido aos
antifields pode ser não nulo, como calculado na entrega anterior.

Logo, mantendo a representação livre G equivarante e a prescrição Hfull
declaradas, A1 nos vértices sem antifields zera. Nesse inventário,
A1(V1)=A1(Faf); A1(V2)=0 porque os vértices quarticos são sem antifields:
as transformações difeomórficas de h e c têm somente a parcela livre e
a parcela quadrática que gera Faf. Isso não computa A2(V1,V1).

Se forem mantidas as três flutuações escalares do alvoS3, o fundo constante
não as elimina da teoria quântica. O vértice antifield adicional é
xi†_a c^mu nabla_mu xi^a. Sua contribuição de aridade1 depende só do
primeiro jato do defeito Euler escalar; esse vetor natural zera no espaço-forma
constante e par. Essa observação NÃO elimina os laços escalares em aridade2
nem demonstra um quociente quântico do modelo acoplado. O fundo físico
phi=id continua distinto da referência087.

O representante normalizado euclidiano encontrado foi
a1(V1)=337K² int chi div(c)/10. Ele é q0 da primitiva linear
337K² int chi tr(h)/20 na mesma normalização e, por q0 c=0,
é q0-fechado. Com cutoff variável, int chi div(c)=-int dchi.c e não
pode ser descartado como se chi fosse constante. Trata-se de aridade1
localizada, não da primeira quebra interagente COMPLETA já removida.

O coeficiente337/10 continua condicionado à normalização euclidiana e sob
revisão independente DeepSeek6945. MiMo57e7 revê este dicionário de sinais.
A passagem aos produtos temporais, realidade, família causal admissível e
consistência com A2 ainda precisa ser verificada. Nenhum contratermo foi
adotado, nenhum resultado transferido ao par físico, nenhum gate alterado.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
