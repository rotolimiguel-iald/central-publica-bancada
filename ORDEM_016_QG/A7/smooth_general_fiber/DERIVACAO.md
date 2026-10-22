[DERIVED — referência suave geral no contato relativo de duas pontas; não é Q2 completa]

## Extensão da construção anterior

A hipótese de isotropia foi retirada da linha métrica suave na diagonal.
Consideram-se as simetrias reais W_ab|cd=W_ba|cd=W_ab|dc=W_cd|ab.
O espaço resultante tem dimensão55. Não se impôs que todo elemento
desse espaço seja parte de um estado positivo ou de um par BRST-compatível.

Para cada elemento da base, o script contrai os MESMOS vértices e
matrizes de contato usados no caso isotrópico; conserva /16, -1/2 e as
duas colocações da linha suave. Obtém T_ij^{AB}(W), linear em W.
A igualdade T_ij^{AB}=T_ji^{BA} foi conferida nas55 bases completas.
O resultado compreende 88000 igualdades de transposição, incluindo zeros,
não88000 experimentos físicos independentes. As tabelas estão em
tensor_basis.json, com coeficientes racionais exatos.

Por linearidade, qualquer W diagonal com as simetrias indicadas,
inclusive com55 coeficientes suaves variáveis, define o operador

    (N_W h)_A=-(1/m_A)∂i[T_ij^{AB}(W)∂j h_B].

Com m_A=1 nos índices diagonais e2 nos não diagonais, esse operador
é formalmente autoadjunto para a contração tensorial completa e testes
compactos. A derivada age também sobre W; não se pressupõe W paralelo.
As combinações lineares que reproduzem W_I e W_T recuperaram todos
os coeficientes da entrega anterior. A linha ghost foi testada em
todos os16 componentes coincidentes: a bolha mista continua zero
neste contato pela orientação dos blocos dos vértices.

## Fonte geral e rotação preservada

Usa-se a fonte já contraída e conferida na base completa:

    R_W c=R_ab^{jr}∂j c_r+A_ab^r c_r,
    R_ab^{jr}=-[δjb S_ar+δja S_br+W_aj|br+W_bj|ar-2W_ab|jr]/4,
    S_ar=Σm W_am|rm.

Os coeficientes A dos primeiros jatos estão na entrega anterior. Seus
jatos ∂Y são dados distintos da derivada diagonal ∂X+∂Y. A generalização
do tensor de bolha não os identifica nem descarta.

Não se substitui R_W por L_WG: a parte -[Ω,S]/4 permanece quando
S não é escalar. Um controle explícito usa W_00|00=w((X+Y)/2),
w=x0²-x2² e c=(-x1,x0,0,0). Embora Gc=0, o cálculo dá

    (R_Wc)00=x0x1/4,
    (R_Wc)01=(R_Wc)10=(x0²-x2²)/4,
    (E R_Wc)01=(E R_Wc)10=1/2.

Os outros componentes de E R_Wc são zero. Assim, exigir a fatoração
por G apagaria uma contribuição medida. Não é exemplo de estado
físico: é um teste dos jatos e da tipagem da operação.

## A mesma primitiva BV continua válida

Sem alterar s0h=Gc, s0h†=Eh, s0c=0 e s0W=0, vale

    B_W=-C_E ∫[h·N_W h/2+h†·R_Wc],
    s0B_W=-C_E ∫h·(N_WG+ER_W)c.

O argumento é exatamente o da entrega anterior: transposição de N_W,
adjunto de E, regra graduada e as correntes explícitas. Não exige
isotropia, fatoração por G nem inversão de um operador diferencial.
Três controles polinomiais anisotrópicos independentes verificaram a
identidade local incluindo correntes; o argumento universal é algébrico,
com a transposição conferida na base completa, não extrapolação desses
três exemplos. O novo resultado é a compatibilidade do tensor EFETIVO
da bolha geral com essa construção, conservando a fonte rotacional.

## Onde entra a curvatura: medição separada

Nos propagadores bilocais existentes à primeira ordem em K, calculou-se
cada componente com zero ou uma derivada em cada ponta, ANTES de
ancorar Y=0. Foram2900 componentes e6122 monômios. Todos os monômios
de primeira curvatura têm grau de escala no máximo2, abaixo do crítico4;
todos os resíduos meromorfos correspondentes são zero. Multiplicadores
quadráticos de densidade/frame também foram conferidos na linha crítica.

Consequência limitada: esses termos de K não criam contato adicional
da linha mista ANTES das derivadas externas de Ward. O contato crítico
fica determinado pelo símbolo principal no ponto. A curvatura continua
presente ao covariantizar N_W, G, E, os jatos e suas composições.
Não se afirma que a expressão de Ward inteira seja independente de K.

O argumento de grau de escala aplica-se a uma expansão Hadamard
U/z+V log z+W sob as hipóteses indicadas: termos não constantes de U
reduzem a singularidade, e até duas derivadas de log z são subcríticas.
Isso não é permissão para descartar logaritmos em outras operações.
Controle negativo na mesma prescrição:

    contato(∂0² log z)/C_E=0,
    contato(∂0⁴ log z)/C_E=-1/2.

A limitação ao número de derivadas é indispensável. O cálculo computou
explicitamente K¹; não mediu todas as ordens de curvatura e não resolveu
a normalização causal/lorentziana.

## Evidências e limite de conclusão

smooth_general_fiber_check.py:88462 verificações, CPU6.046875s, rc0.
mixed_curvature_scaling_check.py:12246 verificações, CPU29.9375s, rc0.
O resultado cobre o contato relativo singular/suave desses vértices,
com estrutura BV geral. Restam a soma da Q2 na prescrição fixada,
outros diagramas locais/aridades e compatibilidade física da referência.
A primitiva encontrada não foi aplicada como contratermo; nenhum
original científico, kernel ou gate foi alterado.
