[DERIVED — normalização plana condicional e dicionário de aridade; Q2 curvo OPEN]

# A7.b — condição concreta de primeira ordem

O cálculo reutiliza a base simétrica métrica e generaliza a matriz livre
ao fundo plano de assinatura (-,+,+,+), mantendo o controle euclidiano.
Campos: h_ij (10), b_i (4), c_i (4), barc_i (4). p representa derivada
formal; em Fourier, todas as ocorrências devem usar p=i k, inclusive os
blocos mistos. Não se mudou a continuação dos contatos já calculados.

Se R é o Gram da base, Itr a reversão de traço, Gc=partial_i c_j+partial_j c_i,
C(h)_j=partial^i h_ij-partial_j tr(h)/2 e E=-p² Itr+Itr G C, os blocos são

 P_hb=[[R E/(4 kappa), -C^T eta],[eta C, -2 kappa eta]],
 N_hb=[[-4 kappa Itr R^-1, G eta],[-eta G^T, 0]],
 P_ghost=[[0,-p² eta],[p² eta,0]], N_ghost=[[0,eta],[-eta,0]].

O CAS verifica P N=N P=p² I22, a adjunção graduada de P, a troca de pontos
de N e Q²=0. Qh=Gc, Qbarc=-b. Com epsilon=diag(+1 nos14 bósons,-1 nos8 ghosts),

 Q(p)N(p)+epsilon N(p)Q(-p)^T=0.

Remover os blocos h-b/b-h viola essa última identidade: a componente h00,barc0
é 2p0 no controle euclidiano e -2p0 no lorentziano. Não se descartou o auxiliar.
São 14 verificações matriciais/controles, CPU0.3125s, rc0.

Escolhido um fplus que seja bisolução exata de box, Hplus=N(partial)fplus
herda P Hplus=0 e a identidade Ward. O enunciado é condicional a essa escolha;
não afirma positividade no espaço total de campos de gauge. No espaço plano
lorentziano, o kernel escalar de frequência positiva da onda sem massa é um
candidato habitual; sua existência/condição microlocal não foram objeto deste CAS.

Prova da consequência para Wick: numa contração de dois campos, a derivação
livre produz precisamente QH+epsilon H Q^T. Ela é zero. Nos termos em que
o BRST de um antifield produz a equação livre, surge P H, também zero.
Logo a derivação comuta com cada pareamento e com a soma de Wick:
shat0 T1(F)=T1(s0 F). Assim A1(F)=0 nesta prescrição plana equivarante.
É uma condição suficiente explícita, não a afirmação de que qualquer ordenamento
normal torna A1 zero. A extensão localmente covariante curva continua pendente.
Não se adotou retroativamente um estado ou um T1 para as contas anteriores.

# Dicionário necessário para o contato de segunda ordem

[KNOWN — Fröb, arXiv1803.10235v3, equações74/154, Teoremas3/6;
DERIVED — polarização e subtração abaixo.] Para F,G pares, a expansão em
aridade, com shat0 no alvo quântico e s0 nos funcionais, dá

 T1(A2(F,G)) = (i/hbar)[shat0 T2(F,G)-T2(s0F,G)-T2(F,s0G)
                   -T2(A1(F),G)-T2(F,A1(G))] -T1((F,G)).

Essa expressão conserva ambos os termos A1. A equação162 da fonte é um
caso especial com uma entrada só de antifields e A1 dessa entrada zero;
não serve para eliminar o segundo termo A1 em duas interações genéricas.
Fonte primária: https://arxiv.org/pdf/1803.10235v3 (pp17–18,34–38).

Defina U2(F,G)=T2(F,G)-T1(F) star T1(G), para essa ordem escrita.
Como shat0 é derivação de star e shat0 T1=T1(s0+A1), os termos desconexos
cancelam exatamente na combinação acima. Portanto a mesma fórmula vale
substituindo T2 por U2 em todos os cinco termos dentro dos colchetes.
Não se usou transformada de Legendre: U2 conectado não é, por esse argumento,
o coeficiente W2 da ação efetiva 1PI. Os mapas permanecem distintos.

Com A1=0 efetivamente estabelecido, restam três termos de U2 e o antibracket.
O contato local calculado pela bancada só pode ser identificado com A2 após
conferir os fatores i/hbar, a subtração T1((F,G)) e o Wick T1 da mesma prescrição.
A igualdade das16 componentes da descida testa a condição localizada; não
preenche por si só essas identificações. Os grafos de corrente já existentes
entram nas duas inserções s0F/s0G; não devem ser recriados como novos grafos.

Nenhum novo teorema Lean, estado curvo, normalização de Euler composta ou
gate foi obtido. Próximo passo: usar a crítica dos produtos temporais para
identificar essas subtrações nos coeficientes já calculados, preservando o
recorte do espaço-forma do alvo. A7.b encerra às20:32UTC.
Abertura SHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
