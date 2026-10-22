[DERIVED — cancelamento principal quadrático; REAL — CAS exato independente; OPEN — Ward curva completa]
# A7.b — correção da contração e cancelamento métrico–ghost

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T22:34:22.864288+00:00.
Supersede os coeficientes métricos de metric_bubble/results.json, SHA256
`7b0385f506c56abbaaccb33ea8e2c2bfecabda1a9300f0d565e4fb85b86bd1fc`. A tentativa anterior e sua MEDIDA permanecem intactas.

## Erro identificado antes do novo cálculo

Os vértices são W_A(i,j;q)=16κ V3(A,p,E_i,q,E_j,-p-q) e W_B(k,l;q),
depois de inverter simultaneamente os momentos do segundo vértice. As linhas
conectam i a k e j a l. Portanto a soma é

    N_m = Σ W_A(i,j) W_B(k,l) S0(i,k) S0(j,l)/16
        = Tr(S0 W_A S0 W_B^T)/16.

O cálculo anterior omitiu a transposição. W não é simétrica a q fixado: a
simetria de Bose também troca q e -p-q. A soma explícita de quatro índices
confere a fórmula corrigida e recusa a anterior num caso não degenerado.
A inversa S0 foi também recalculada diretamente da forma da base, sem presumir
seus blocos. Nem vértice, gauge, ghost, peso de laço ou extrator foi ajustado.

## Coeficientes corrigidos e identidade

Com A0=1/(8π²), na ordem
trAB*p4, trA*trB*p4, (pAp*trB+pBp*trA)*p2, pABp*p2, pAp*pBp:

    métrica/A0 = [71/60, 27/40, -19/30, -11/5, 26/15]
    ghosts/A0  = [1/12, 7/48, -1/8, -1/12, 1/6]
    (-métrica/2+ghosts)/A0
                = [-61/120, -23/120, 23/120, 61/60, -7/10].

A ponderação é a Hessiana formal de (ħ/2)Trlog H-ħTrlog Q; fases Lorentz
permanecem separadas. Para p=e0, E00/E00, a métrica vale A0/8 e o ghost A0/16,
logo a soma é zero. As dez contrações duplas de base anulam. Mais forte:
para p,v,H simbólicos arbitrários, K_p(v)=p⊗v+v⊗p,

    F_log(K_p(v),H)=0.

Se T=I-pp^T/p², o polinômio bilinear pode ser escrito para p²≠0 como

    F_log(A,B)/(ħ A0) = (p²)²[-61/120 tr(T A T B)
                                      -23/120 tr(T A)tr(T B)].

A identidade polinomial não exige dividir por p² e inclui p=0.
Em termos das curvaturas LINEARIZADAS em espaço tangente plano,

    F_log/(ħ A0) = -61/30 Ric^(1)(A):Ric^(1)(B)
                         +19/60 R^(1)(A)R^(1)(B).

Essa expressão é a Hessiana quadrática calculada. Ela não determina por si
uma ação covariante não linear única nem os coeficientes curvos Kp² e K².
Não há termo log p4 do tadpole massless principal com vértice quartico de
somente duas derivadas: sua contagem não chega a q^-4 com quatro derivadas
externas. Isso NÃO descarta tadpoles com curvatura ou outras ordens.

## Verificações e próximo elo

metric_bubble_check_v2.py: rc0,68checks,3controles; wall 7.424492200021632s,
CPU 7.390625s. Inclui55pares da base e dez interpolações fora dos nós.
metric_bubble_independent_check.py: rc0,9checks,3controles; wall
6.736765900044702s,CPU 6.71875s. Os cinco coeficientes foram
reproduzidos por parâmetros de Feynman e momentos Dirichlet, sem recorrência
radial; direção p=(1,2,-1,1) e polarizações densas deram20489/30 sobreA0 por
ambas as vias. A identidade longitudinal simples e a expressão em Ric/R foram
conferidas simbolicamente. Peças isoladas e troca do sinal relativo falham.
diagnose_metric_ward.py:440exemplos clássicos,276não triviais,zerofalhas.

O cancelamento é do termo logarítmico principal quadrático, no modelo truncado.
Não é a primeira quebra Q2 completa: faltam inserções BV, contatos e termos
finitos da prescrição, contribuições curvas e identidades de ordens superiores.
Não foi executada continuação Lorentziana de toda amplitude. Gate inalterado.
Próximo ramo do A7.b: termos curvos e marcados, preservando este resultado.
