[DERIVED — contato finito marcado e exatidão principal hc; REAL — CAS; OPEN — causal completo]
# A7.b — combinar a fonte h* c com a Hessiana
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T01:15:33.605405+00:00.

Mantida a extensão de um par R=FP[(1-a)mu^(2a)z^a·], com mu fixo.
O numerador marcado já medido, sem seu fator global, é

    R0(q)v=-3q² K_q(v)/8 + q⊗q(q·v)/2 = K_q F(q)v.

Chamando q de símbolo formal das derivadas do delta, o mesmo cálculo de
resíduos da entrega precedente dá agora, para P3 cúbico,

    N3[P3]=-13P3/48-q² Lap_q(P3)/64,
    R(P3(partial)U2)-P3(partial)R(U2)=C N3[P3](partial)delta.

As derivadas radiais abertas precisam dos fatores métricos de partial_i z.
Após a correção registrada abaixo, as duas assinaturas dão

    N3[R0]v=(5/32)q²K_q(v)-(13/96)q⊗q(q·v)
                         -(1/64)q²g(q·v).

A parcela de traço é nova e não é gauge pura. Com o símbolo físico NÃO
gauge-fixado E(q)H=q²ItrH-Itr K C(H), usado nas entregas anteriores,

    E(q)N3[R0]v=-(1/32)q²(q·v)(q⊗q-q²g).

É importante manter E; substituir pela Hessiana gauge-fixada destrói essa
identificação. O fator4kappa e sinais/fases de Fourier completos ainda não
foram fixados na comparação causal. Por isso lambda abaixo registra esse
fator RELATIVO; ele não foi ajustado nem identificado como parâmetro físico.

**Combinação explícita.** Retirados C e o fator global comum, a quebra local
do setor principal hc, a partir das duas extensões uniformes, é

    W_lambda(T,v)=(187/1920)q4(Tq·v)
       +(43/960+lambda/32)q4 trT(q·v)
       +(-7/40-lambda/32)q²(qTq)(q·v).

Ela não se anula por uma escolha de lambda. Um controle particularmente
direto toma q=v=e0 e T=K_q(e0): W=-21/320, e a contribuição marcada é
zero por E K=0. Esse é um contato finito de normalização, não uma nova
obstrução cohomológica inferida desse número.

Subtrair os DOIS contatos calculados, N4[P] da Hessiana e N3[R0] da fonte,
leva às extensões diferenciais P(partial)R(U2) e R0(partial)R(U2).
Nelas as duas parcelas se anulam separadamente pela transversalidade e
E K=0. A restauração desse setor vale para qualquer fator relativo constante;
isso não dispensa fixá-lo para determinar a amplitude física original.

**Forma BV e WZ no recorte.** No modelo livre principal, use
hat_h^ddagger=h^ddagger+C*barc, com s0hat_h^ddagger=Hh e s0c=0.
O polinômio local que codifica as diferenças é da forma

    B = (1/2)<h,N4 h> + lambda'<hat_h^ddagger,N3 c>,

com os fatores globais recolocados em lambda' e no primeiro termo.
Ele tem ghost0, e sua variação contém a combinação hc obtida. A parcela
com antighost em hat_h^ddagger deve ser conservada para cancelar os termos
com b; não é um novo laço. Assim a quebra PRINCIPAL aqui reconstruída é
s0-exata, módulo integrações por partes, nessa classe local de símbolos.
Pode-se escolher a densidade simetrizada s0B, que é fechada por s0²=0.
Ao recolocar cutoffs, as integrações por partes trazem derivadas de chi;
esta entrega vale na região chi constante, sem declarar tais termos zero.

Uma checagem explícita da consistência integrada: a matriz de dois ghosts
K(-q)^T N4(q)K(q) é simétrica sob (i,q)↔(j,-q), logo sua contração com
c_i(-q)c_j(q) é nula por Grassmann. O número duplo-gauge -21/320 não
contradiz WZ: esta usa a antissimetria dos ghosts, não a nulidade de cada
entrada da matriz. A contribuição marcada anula por E K=0.

**Evidência e limites.** v3:138identidades exatas nas duas assinaturas,
quatro controles descritos,rc0,CPU2.625s. Auditoria independente
por momentos esféricos/Taylor, incluindo o sinal ÍMPAR do jato de teste:
36checks,3negativos,rc0,CPU0.296875s. Fontes e logs nos manifestos.
Não foi provada admissibilidade de toda uma hierarquia de normalização,
realidade da amplitude Lorentziana com suas fases, Ward não linear completa,
curvatura ou equivalência ao par físico. Q2 completa continua aberta.
Nenhuma mudança em kernel,um.py ou gate; nenhuma nova execução remota.
