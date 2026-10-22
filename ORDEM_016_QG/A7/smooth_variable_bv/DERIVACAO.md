[DERIVED — contato relativo suave variável em duas pontas, fundo plano auxiliar; Q2 completa OPEN]

## Recorte e exaustão local da singularidade mista

Mantém-se a prescrição radial já fixada, sem mudar o estado nem o
contratermo. C_E=-4π² e prefatores comuns dos propagadores estão retirados
dos coeficientes. A linha singular plana é 1/z. Nos vértices utilizados,
cada linha tem no máximo uma derivada em cada ponta: seu grau de escala
é 2, 3 ou 4. Só o último caso admite o contato desta comparação,

    R(∂Xi∂Yj z^-1)-∂Xi∂Yj z^-1=C_E δij δ/4.

Para uma função suave f independente do regulador, a multiplicação
comuta com a extração da parte finita da família meromorfa: FP(fu_a)=
f FP(u_a). Logo o contato crítico é multiplicado por f na diagonal;
seus termos de Taylor transversais positivos multiplicados por δ somem.
Isso NÃO autoriza substituir f por uma constante antes de derivar o
operador resultante. Nem permite retirar as derivadas de f que já
figuram no outro propagador do vértice de fonte.

## Fonte: os primeiros jatos antes omitidos

Se W_H é a linha métrica suave e W_G a ghost, escreva os índices de
fibra separados por | e ∂Y no segundo argumento. A contração dos
vértices de curved_source_jet_engine.py fornece, além do R_W ∂c já
calculado, a contribuição A_W c:

    A_H,ab^r=-1/4[Σm ∂Yr W_am|bm + Σm ∂Yr W_bm|am
                         -Σl ∂Yr W_ab|ll],
    A_G,ab^r=-1/8[∂Ya W_G^r|b+∂Yb W_G^r|a].

O primeiro termo vem de 2h_am ∂b c^m com a linha ghost singular;
o segundo, de c^m ∂m h_ab com a linha métrica singular. As outras
colocações com menos de duas derivadas na linha singular são localmente
integráveis neste recorte. Não se impôs simetria de troca das duas
fibras a ∂Y W: troca de pontas relaciona ∂Y W e ∂X W, não identifica
arbitrariamente ambas. Os coeficientes foram conferidos na base completa
dos primeiros jatos envolvidos.

Para W_H=wI((X+Y)/2)I_sym+wT((X+Y)/2)gg e
W_G=wG((X+Y)/2)I, a derivada Y é metade da derivada da função diagonal.
Assim, com Gc=∂c+(∂c)^T,

    R_I c=-wI Gc/2-wI g tr(Gc)/8-g c·∂wI/2,
    R_T c=-wT Gc/2+wT g tr(Gc)/4+g c·∂wT/4,
    R_G c=-(c⊗∂wG+∂wG⊗c)/16.

São dados formais locais. Não se declarou que qualquer w assim escolhido
produz estado positivo ou par de referências BRST-compatível.

## Bolha: conservar o tensor antes da integração por partes

A contração real dos vértices define o tensor T_ij^{AB} na forma bilinear

    ∫ w ∂i h_A T_ij^{AB} ∂j k_B.

Ele satisfaz T_ij^{AB}=T_ji^{BA}. A medida de fibra é m_A=1 nos
componentes diagonais e 2 nos não diagonais. A Hessiana de METADE
da forma quadrática é

    (N_w h)_A=-(1/m_A)∂i(w T_ij^{AB}∂j h_B).

O tensor métrico I possui 232 componentes não nulos, dos quais 96
têm parte antissimétrica não nula nos índices i,j. O tensor métrico T
possui 184 componentes não nulos e parte antissimétrica zero. O ghost
é zero neste contato. As tabelas completas constam do resultado JSON.
Todos os símbolos quadráticos para w constante reproduzem os coeficientes
anteriores, com p simbólico. A simetria conjunta de derivada e fibra foi
conferida em todos os componentes.

A parte antissimétrica em i,j cancela no símbolo constante p_i p_j,
mas contribui através de ∂i w. Controle: w=x1 e h00=x0 dão, na saída
01 do setor I, N_completo-N_apenas_simétrico=1/8. Portanto a tabela
de quatro invariantes do caso constante não determina sozinha N_w.

## A ligação pelo antifield, sem inventar nova estrutura

Use o diferencial livre já adotado:

    s0h=Gc, s0h†=Eh, s0c=0, s0W=0.

h† tem ghost -1 e paridade ímpar; R_W c tem ghost +1. Como N_w é
autoadjunto e E também, a funcional local de ghost ZERO

    B_W=-C_E ∫[1/2 h·N_w h+h†·R_W c]

satisfaz para suporte compacto

    s0 B_W=-C_E ∫h·(N_w G+E R_W)c.

A prova usa apenas a regra graduada e os adjuntos. No termo antifield,
s0(h†R_Wc)=(Eh)R_Wc-h†s0(R_Wc), e a segunda parcela é zero na variação
livre da referência fixada. A integração por partes põe E sobre R_Wc.
Não é necessário que R_W fatore por G. Assim, a insuficiência da
primitiva exclusivamente métrica não é obstrução à primitiva BV.

Quando w é constante e R_W=L_W G, essa primitiva e a antiga primitiva
puramente métrica N_eff=N_w+EL_W+L_WE diferem por

    B_métrica-B_BV=-C_E s0∫h†·L_W h.

Isso liga as duas construções anteriores; não seleciona uma prescrição.

## Correntes locais: nenhum termo de borda escondido

Para T constante e w variável, a corrente

    J_N^i(h,k)=w T_ij^{AB}[-h_A∂j k_B+k_A∂j h_B]

obedece ∂iJ_N^i=h·N_w k-(N_w h)·k. Para E=C^{ij}∂i∂j com
coeficientes constantes autoadjuntos, a corrente é

    J_E^i(h,k)=C_AB^{ij}[h_A∂j k_B-k_A∂j h_B],

com os pesos de fibra incorporados a C. Ela satisfaz
div J_E=h·Ek-(Eh)·k. Portanto, na densidade da primitiva,

    s0 b_W=-C_E h·(N_wG+ER_W)c
                 +C_E div[J_N(h,Gc)/2+J_E(h,R_Wc)].

Esse é o enunciado local anterior à integração. Um corte χ acrescenta
os termos de ∂χ da corrente; não se declara que somem fora de χ=1.
As identidades gerais seguem das simetrias dos coeficientes, não de
extrapolar amostras. Dois testes polinomiais densos independentes em
cada um dos três setores conferem as correntes e a variação inteira.

Controle negativo: w=x0³-3x0x1², c=e0, então Δw=0 e Gc=0,
mas E R_I c=diag(6,-6,0,0). A primitiva só métrica não poderia produzi-lo,
pois sua variação contém Gc. O antifield produz exatamente o termo.
O controle é local; harmonicidade do escalar não prova admissibilidade
do estado nem compatibilidade BRST do par completo.

## Estatuto e próximo passo

Foram 6645 verificações da fonte, 5101 do tensor de bolha e 182 da
ligação BV/correntes, todos rc0. Não são uma compilação Lean nem uma
prova da QME interagente. O resultado cobre o contato relativo de duas
pontas no recorte plano, incluindo a família isotrópica dependente do
centro. Permanecem a referência geral admissível, curvatura, outros
termos locais/aridades e a passagem causal. Nenhum contratermo foi
aplicado ao programa original e nenhum gate foi alterado.
