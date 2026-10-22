[DERIVED — contato misto plano com referência suave constante; Q2 completa OPEN]

## Domínio e prescrição

Espaço euclidiano auxiliar 4D, curvatura zero. Calcula-se a diferença
entre a extensão radial fixada e a referência definida por derivação;
não a quebra quântica completa. Retiram-se dos coeficientes C_E=-4π²
e os prefatores comuns dos propagadores. p representa derivada real.
Mantêm-se os vértices previamente construídos, a contração métrica /16
e a combinação -métrica/2+ghost. Não se ajustou normalização.

O contato de entrada é

    R(∂Xi∂Yj z^-1)-∂Xi∂Yj z^-1 = C_E δij δ/4.

A linha suave constante só tem bloco sem derivadas. A linha de contato
só tem bloco com uma derivada em cada ponta, multiplicado por δij/4.
Se J denota esta última matriz e W a primeira, a contração é

    <Jᵀ A_X W + Wᵀ A_X J, B_Y>.

O fator métrico total é -1/32; o ghost tem fator +1 e transposição
do vértice da segunda ponta. O emparelhamento da delta põe q=-p.
Os blocos de vértice com campo externo não derivado dão matriz mista
zero, verificado em toda a base de dez tensores simétricos.

## Coeficientes medidos

Na base bilinear

    [p² tr(AB), p² trA trB, (pAp)trB+(pBp)trA, pABp]

os coeficientes são:

| linha suave | coeficientes |
|---|---|
| W_I=(δacδbd+δadδbc)/2 | (23/8,-13/16,1,-2) |
| W_T=δabδcd | (3/4,-3/8,1/2,-1) |
| W_G=δab | (0,0,0,0) |

O ajuste resolve cem pares de base para cada setor, tem solução única
nessa base invariante e é conferido em momentos não axiais e fibras
densas reservados. A estrutura O(4) vem das contrações invariantes,
não de extrapolar um teste axial isolado.

Com Gv=pvᵀ+vpᵀ e

    E(h)=-p²h+g p²trh/2+pCᵀ+Cpᵀ-g(p·C),
    C=hp-p trh/2,

temos EG=0. O contato da fonte previamente calculado é R_W=L_W G,
com L_I(h)=-h/2-g trh/8 e L_T(h)=-h/2+g trh/4.
A soma efetivamente medida N_bolha G+E R_W NÃO é zero nos dois
setores métricos. Na base [g p²(p·v),p²Gv,ppᵀ(p·v)], ela vale:

    W_I: (-1/8,15/8,1/2),
    W_T: (5/4,1/4,-1).

Isso é um resíduo deste recorte, não uma classe não trivial de anomalia.

## Primitiva explícita, sem escolher subtração

Como E e L_W são autoadjuntos, N_eff=N_bolha+E L_W+L_W E é
autoadjunto e N_eff G=N_bolha G+E R_W. Seus coeficientes na base
bilinear anterior são

    W_I: (31/8,-37/16,9/4,-4),
    W_T: (7/4,-3/8,1,-3).

Para testes compactos, B=-C_E/2 ∫h·N_eff h satisfaz

    s0 B=-C_E ∫h·(N_bolha G+E R_W)c.

Adicionar ηE não altera a variação porque EG=0. η permanece livre;
não se adotou representante nem se mudou a prescrição. O script da
primitiva confere todos os componentes do resíduo armazenado e a
transposição na fibra com p simbólico.

## Evidência e limite

flat_mixed_smooth_bubble_check.py: 336 verificações, CPU 3.25s.
flat_mixed_smooth_primitive_check.py: 328 verificações, CPU 0.296875s.
Ambos rc0 nas execuções registradas; resultados e hashes no manifesto
da entrega. Não foram incluídos jatos de W, curvatura, outros diagramas
locais, aridades superiores ou continuação lorentziana. A existência
desta primitiva não seleciona um estado físico e não fecha a QME.
