[DERIVED — setor logarítmico principal BV; REAL — CAS exato; OPEN — anomalia causal finita]
# A7.b — primeira inserção antifield–ghost e identidade hc

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T22:51:36.330146+00:00.

Fonte BV069: h* L_c h e +barc C(L_c h), com C de fundo linear. Antifields
são fontes externas sem propagador. Escrevemos o vértice da fonte como iU:

    U_m(T,H,k,l)=k_m tr(T H)+2(H T l)_m.

T é a polarização simétrica de h*, H a métrica, k o momento métrico e l o
momento ghost. Derivação por índices confere U com a derivada de Lie. A bolha
externa h*(-p),c(p)=v contém h(q),c(p-q) e vértice ghost V(H,-q,p). Seu
numerador sem peso global é Σ U_m(T,E_i,q,p-q) S0_ij V_mρ(E_j,-q,p)vρ.
Denominadores q²(q-p)²; mesma extração log Λ_UV euclidiana. O fator fonte i,
4κ métrico, sinal do inverso ghost e convenções Grassmann globais ficam
explicitamente fora dos números abaixo. Eles não afetam as anulações que
ocorrem separadamente.

## Resultado medido

Sobre A0=1/(8π²), a correção é <T,R(p)v>, com

    R(p)v= -3/8 p²(p⊗v+v⊗p)+1/2(p⊗p)(p·v).
    F(p)v= -3/8 p²v+1/4 p(p·v),     R=K_p F.

Não apareceu o terceiro tensor permitido p² I(p·v): seu coeficiente foi zero,
sem ser imposto no ajuste. Logo a Hessiana de Einstein SEM gauge anula R.
Já a parte métrica Σ_log calculada na entrega precedente anula K_p. No setor
hc de referência plana principal, o coeficiente logarítmico de

    Σ_log K_p + H_EH R_log

é zero, inclusive antes de fixar a fase relativa, porque ambas as parcelas
anulam separadamente. Mantemos b na identidade BV; eliminar b do propagador
interno não permite trocar H_EH por H_gf nessa equação com b=0.

O vértice antighost é obtido do mesmo U aplicando C: V=-U(C_p^T e,H,k,l)
depois de retirar os fatores i. A linearidade da integral dá o kernel ghost
sem peso -C_p R=+3/8 p4 I-1/4 p² pp^T, compatível com Q(p)F(p), Q=-p²I.
Isto é uma identidade entre os kernels marcados, não uma nova contribuição
de ghost duplicada na soma.

Uma mudança LOCAL c_old=(I+εF)c, com transformação cotangente inversa do
antifield, reproduz essa estrutura livre. Sua extensão algébrica do colchete é
δ_F B=B(Fv,w)+B(v,Fw)-F B(v,w). Ela satisfaz Jacobi por transporte da operação,
e64exemplos Fourier verificam também o termo de primeira ordem. Isso é uma
construção de mudança de coordenadas, NÃO o cálculo do triângulo quântico.

## Evidência e alcance

antifield_vertex_check.py: rc0,47checks,2negativos; wall 2.515252999961376s,
CPU 2.5s. Quarenta pares da base, direção não axial,
vértice de Lie por índices, antighost e parâmetros de Feynman independentes.
principal_bv_identity_check.py: rc0,134checks,2negativos; wall
0.9106227000011131s,CPU 0.890625s. As identidades hc são polinomiais
em momento/polarização arbitrários; Jacobi foi checada nos64trios escolhidos,
além do argumento algébrico de transporte.

É o cancelamento LOGARÍTMICO principal do componente hc. Não foi calculada a
parte finita da anomalia causal A(e^V), nem o mapa completo entre a 1PI e a
prescrição causal com cutoffs. Curvatura, contatos, pesos globais completos e
vértices marcados superiores continuam obrigações distintas. Q2 não está paga;
nenhuma alteração de kernel/um.py/gate.
