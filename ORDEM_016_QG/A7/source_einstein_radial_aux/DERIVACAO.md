[DERIVED — fonte singular fora da diagonal, primeira curvatura; Q2 OPEN]

# Fonte bilocal na orientação da divergência

Defina o acoplamento local `Lie_c h` no extremo X e o vértice ghost no
extremo Y. A fonte, antes da integração do ghost externo, tem a forma

    integral dvolX dvolY hstar_ab(X) [A_ab,r c^r(Y) + B^j_ab,r D_j c^r(Y)].

O motor `bilocal_source_divergence_engine.py` calcula

    C_ab,r(X,0) = A_ab,r(X,0) - partial_Yj B^j_ab,r(X,0).

A diferenciação ocorre antes da ancoragem. Em Y=0, a conexão e a primeira
derivada da densidade de volume são zero. As derivadas das conexões já
contidas nos propagadores NÃO são zero; o motor mantém esses termos.
Os fatores métricos que levantam os índices do vértice Y e fazem a
reversão de traço têm primeira derivada zero na origem. Isso justifica
a sua simplificação nesta integração de UMA derivada, não em duas.

No extremo X, `Lie_c h = c^m D_m h_ab+h_am D_b c^m+h_bm D_a c^m`.
Os três termos entram explicitamente. Nenhuma simetria do teste é usada
para substituir um componente do tensor por duas vezes outro diferente.

## Base completa no recorte usado

O tensor é simétrico em a,b e é covariante sob O(4); não há epsilon nos
vértices. Os três tensores disponíveis, construídos com X e delta, são

    delta_ab Xr,  delta_ar Xb+delta_br Xa,  Xa Xb Xr.

As homogeneidades fixam os denominadores. Com z=X², até primeira K:

    C0_ab,r = -12 delta_ab Xr/z4
              -30(delta_ar Xb+delta_br Xa)/z4 + 96 Xa Xb Xr/z5;

    C1_ab,r = -20 delta_ab Xr/z3
               +2(delta_ar Xb+delta_br Xa)/z3 +104 Xa Xb Xr/z4.

Os três coeficientes são extraídos na direção radial. A implementação
original também conferiu translação plana, escala radial e componentes
não axiais antes de entrar no cálculo Einstein custoso; a execução
auxiliar refez a extração e gravou o checkpoint SOURCE_COEFFICIENTS.json.
Os coeficientes logarítmicos cancelaram no tensor fonte C. Isto não
afirma cancelamento de logs em toda a teoria.

## Decomposição e imagem Einstein

Considere o operador de gauge `G(v)_ab=D_a v_b+D_b v_a`. Para cada r,

    v0_b = 4 delta_br/z3 - 6 Xb Xr/z4,
    v1_b = -(8/3) delta_br/z2 - (34/3) Xb Xr/z3.

As identidades racionais são

    C0 = G0(v0),
    C1 = G0(v1)+G1(v0)-24 Xa Xb Xr/z4.

No fundo Einstein usado, `E G=0`. O resto curvo pode ser separado em
gauge e em um múltiplo conforme da métrica:

    -24 Xa Xb Xr/z4
      = 2 G0(X_b Xr/z3) + (1/2) G0(delta_br/z2)
        -4 delta_ab Xr/z3.

Para `h_ab=delta_ab f`, vale

    E0(h)_ab = 2(delta_ab Box f-partial_a partial_b f).

Logo

    (E C)0 = 0,
    (E C)1_ab,r = -144 delta_ab Xr/z4
                  -48(delta_ar Xb+delta_br Xa)/z4
                  +384 Xa Xb Xr/z5.

O script `source_einstein_radial_aux_check.py` verifica diretamente tanto
a decomposição quanto a aplicação de E (128 igualdades racionais), nas
componentes r=0,1 que separam os três coeficientes por O(4). A variável z
fica independente durante a diferenciação, com a regra

    partial_i = partial/partial Xi + 2 Xi partial/partial z,

e a relação z=X² é imposta depois. Nenhum coeficiente de E foi alterado.
Isso evita a expansão prematura de grandes denominadores em coordenadas.

## Limites

Estes valores só se somam ao par após integrar também todos os termos
com D_X h. Comparar `(E C)` ao par com Dh_X simplesmente zerado mistura
representações e não testa a identidade de Ward completa. A extensão
temporal, seus contatos, a parte suave, tadpoles e aridades restantes
não foram incluídos nesta entrega. Nenhum gate ou original foi alterado.
