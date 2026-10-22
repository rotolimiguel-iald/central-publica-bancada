[DERIVED — contribuição de referência suave; REAL — CAS; OPEN — soma Ward]
# A7.b — resíduo nulo não elimina o contato finito
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T02:26:43.195328+00:00.

Na bolha h-dagger/c já construída, trocar um propagador pela diferença suave W
entre duas referências de Hadamard deixa apenas três tipos com grau de escala4:

    (partial_Y W_G)(partial_X partial_Y z^-1),
    (partial_X partial_Y z^-1)(partial_Y W_H),
    (partial_X partial_Y z^-1)W_H nabla(v).

Os demais produtos têm grau abaixo4 e são localmente integráveis. Termos
superiores do Taylor de W também reduzem o grau; W_G W_H é suave.
O numerador angular da derivada segunda é -2delta_ij+8n_i n_j.
Sua média em S3 é zero, pois <n_i n_j>=delta_ij/4. Logo **a mudança suave
não altera o resíduo logarítmico desta bolha**. A conclusão não exige escolher
W=0 e não se estende por esse argumento a outros grafos ou à anomalia completa.

Mas a prescrição fixa R tem

    R(partial_i partial_j z^-1)-partial_i partial_j z^-1
      =-(C/4)delta_ij delta,
    R(partial_Xi partial_Yj z^-1)-partial_Xi partial_Yj z^-1
      =+(C/4)delta_ij delta.

Aqui C é retirado como nas entregas anteriores (euclidiano:-4pi²); a
continuação Lorentziana completa não é presumida. Multiplicação por um
coeficiente suave reduz esse contato ao seu valor de coincidência.

**Mapa local nos jatos suaves.** Todos os W e suas primeiras derivadas abaixo
são avaliados em X=Y, em referencial normal; fatores globais da bolha ficam
separados. Denote D_a v^b o primeiro jato externo. Por contração dos mesmos
vértices da fonte e do ghost,

    N_W/C = -1/4 T^munu v^m (partial_Ymu W_G^mnu)
             -1/2 T^ab sum_m [
                 v^r partial_Yr W_H(am,bm)
                 +(D_b v^r) W_H(am,rm)+(D_m v^r) W_H(am,br)
                 -delta_bm/2 v^r sum_l partial_Yr W_H(am,ll)
                 -delta_bm sum_l (D_l v^r) W_H(am,lr) ].

Índices repetidos são somados. Na primeira parcela, o numerador métrico
trace-reversed contrai com a reversão de traço do vértice ghost: I_tr²=id.
Por isso aparece T^munu, e não I_tr(T)^munu. A fórmula representa a diferença
entre estender os kernels fora da diagonal por R e conservar a derivada do
propagador já estendido. Não é uma anomalia física inferida de W.

Controle: W_H(ab,cd)=wI(delta_ac delta_bd+delta_ad delta_bc)/2+wT delta_ab delta_cd,
primeiros jatos nulos e W_G sem contribuição dão

    N_W/C=-(wI+wT)T^ab D_a v_b
           -(wI/4-wT/2)tr(T) D_a v^a.

Com wI=1,wT=0,T01=T10=1,D0v1=1, o resultado é -1, não zero.
É controle algébrico, não alegação de que jatos arbitrários definem um estado
físico no espaço curvo. O cancelamento com os outros contatos ainda deve ser
testado na mesma referência admissível. CAS:42assertivas,rc0,
CPU0.078125s. Não foi acrescentado leitor/gate ao programa.
