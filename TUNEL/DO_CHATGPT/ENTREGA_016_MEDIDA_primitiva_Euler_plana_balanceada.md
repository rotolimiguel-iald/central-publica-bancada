[DERIVED+CAS — primitiva local do representante principal plano delimitado]

Na normalização R_bal/CE e no limite de jatos de cutoff constantes, os
três grafos Euler deram o tensor h_ij c_r com coeficientes
A=-1817/15360, B=-397/15360, C=503/3840 na base registrada no cálculo anterior.
Foi encontrada e conferida uma Hessiana local autoadjunta M de ordem4:

 M=a delta_ij delta_kl(q²)²+b I_ij,kl(q²)²
  +u(delta_ij q_k q_l+delta_kl q_i q_j)q²
  +v(delta_ik q_j q_l+delta_jk q_i q_l
     +delta_il q_j q_k+delta_jl q_i q_k)q²+e q_i q_j q_k q_l,
 a=A/2-u, b=B-2v, e=C/2-u-2v.

Para B_local=1/2 int h M h, q0h=G c dá
q0 B_local=int h M Gc. O CAS confere todas40 componentes desse resultado
contra os grafos medidos, para u e v SIMBÓLICOS; ambas as direções livres
estão no núcleo de M G. Nenhum valor dessas liberdades foi adotado.
Um exemplo matemático de primitiva (u=v=0) é

 B_local=int[-1817/61440 tr(h) box² tr(h)
             +-397/30720 h_ij box² h_ij
             +503/15360(partial_i partial_j h_ij)²].

As integrações por partes usam campos/testes apropriados no setor local.
Logo ESSE representante tem classe zero no problema de cohomologia livre,
plano, quadrático e de acoplamento constante. Ele é não nulo antes da
primitiva; sua exatidão não é declaração de que toda Q2 já desapareceu.

Não transportar a conclusão aos cutoffs variáveis: o representante
localizado anteriormente medido tem quadrado BV não nulo e sua identidade
é INHOMOGÊNEA, com inserções clássicas q0V. Um único q0 B não pode produzir
essa expressão inteira, pois q0²=0. A família de contratermos, curvatura,
setores escalares e referência física continuam separados.
633 controles, CPU0.46875s,rc0; originais/gate intactos.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
