[DERIVED — obstrução à mudança só de campos neste escopo; REAL — CAS exato; OPEN — primitiva BV completa]
# A7.b — o resíduo transversal exige ampliar a candidata local

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T23:50:59.983542+00:00.

Mantemos o R1=G-M/4 medido, o Z da entrega anterior e a normalização
principal com4κA0 retirado. A primeira candidata era uma mudança local só
de h,c: h_antigo=h+εA2(h,h), c_antigo=c+εFc-εZ(h,c).
Ela produziria no vértice adicional -2A2(H,K_l v), além de R1coord.

## Contraexemplo mínimo

Escolha momento do ghost l=0, momento métrico p=e0, ghost v=e0 e
polarizações H=T=e11. Então:

    G=3/32, M=-7/24, R1=G-M/4=1/6.
    K_l v=0; T:K_p Z=0 para QUALQUER vetor Z.

Logo T:R1coord=0 e T:A2(H,K_l v)=0, mas T:R1=1/6.
Não é defeito da escolha de um dos oito parâmetros livres de Z: nenhuma
troca de Z muda essa contração transversal. A presença de uma mudança
linear local da métrica, com coeficientes constantes, também não basta
nesse setor: ela comuta com a translação constante L_v=v·∂.
Essa exclusão refere-se às mudanças de h,c descritas; não exclui todos
os geradores BV nem mudanças envolvendo outros slots.

O teste parou no primeiro contraexemplo, conforme pré-registro. O valor
foi reconferido por parâmetros de Feynman/simplex, separadamente da extração
radial UV, com seis verificações e T p=0 simbólico. Nenhuma fonte foi ajustada.

## O resíduo tem uma forma de equação de movimento

Defina E_p(H)=p² Itr(H)-2 C_p^*C_pH, a Hessiana Einstein principal sem
o fator físico1/(4κ). No subespaço p·H=0, E_p(H)=p²(H-P_T trH),
P_T=I-pp^T/p². Para l=0, v paralelo a p e H transversal, obtivemos

    P_T R1(H,p;0,v) P_T
       = -(p·v)[ E_p(H)/6 + P_T tr(E_p(H))/12 ].

Os coeficientes foram localizados em dois casos, depois verificados nos
36pares da base completa S²(p-perp)×S²(p-perp);12valores são nãozero.
Esta é uma igualdade do mapa bilinear nesse recorte, não interpolação
em36momentos. Homogeneidade de grau3 e covariância O4 das contrações
estendem p=v=e0 a p nãozero e v paralelo a p. Não demonstra o caso
v não paralelo, l nãozero, as componentes longitudinais ou a parte curva.

O próximo ramo local usa geradores BV quadráticos em antifields, que podem
produzir termos proporcionais a E(h). A identidade graduada correspondente
está na entrega associada, com as condições de normalização ainda expostas.

Execuções: rc0 em todos os scripts; não houve compilação Lean nem chamada
externa nova. CPU total desta rodada28.390625s, wall dos scripts29.316245299996808s.
Logs, fontes e resultados constam dos manifestos. Q2finitaOPEN; gateintacto.

Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/metric_primitive_zero_ghost_check.py.
rc0; log SHA256 `31a2464dc1fa7d3a2d6d1385dfe53694b284b5f583c316ec7808230147f1d905`. Custo externo novo zero; próximo ramo: primitiva BV graduada local no mesmo A7.b.
