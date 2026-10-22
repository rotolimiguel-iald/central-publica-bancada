[DERIVED — ligação de sinais existentes; REAL — composição CAS; OPEN — continuação causal curva]
# A7.b — normalização relativa formal já disponível na bancada
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T01:40:50.089158+00:00.

O sinal não precisava de nova bolha: marked_vertex_independent já verificou
mixed_bubble_Wick_sign e effective_bubble_after_Q_inverse_minus. Seu script
foi re-hasheado contra o recibo antes do reaproveitamento; não foi reexecutado.
Na ordenação da fonte T U h eta e do vértice bareta V h c, externalizar T,c
e contrair os ghosts dá +1. A expansão conectada de Gamma=-hbar log Z dá
o sinal negativo; o inverso Q^-1 tem outro sinal negativo. Com G_H=4kappa S/p²
e fonte iU, o fator da correção h* c é portanto

    (-hbar) (4kappa) (-1) i = +4 i kappa hbar.

A Hessiana física é E/(4kappa), e a transformação de gauge em Fourier é
iK. Logo, na convenção formal/euclidiana já adotada,

    Gamma1_hh (iK) + (E/4kappa) Gamma1_h*c
       = i hbar A0 [P4 K + E R0] no setor logarítmico,

e o lambda relativo deixado simbólico na entrega finita vale **1**.
Isso usa a Hessiana física; a gauge-fixada não pode substituí-la.

A mudança entre símbolos de momento e derivadas também não introduz
um sinal relativo entre graus3 e4: (-i)^n i^n=1. Para o contato euclidiano,
C_E/(16pi^4)=-2A0. A quebra finita principal bruta é assim

    -2 i hbar A0 W_1(T,v),
    W_1=(187/1920) q4 Tq·v +(73/960) q4 trT(q·v)
                         -(33/160) q²(qTq)(q·v).

Não é nula. A subtração dos dois contatos já medidos a remove; o
completamento com chi arbitrário está em ENTREGA_016_A7b_contatos_cutoff_finito.md.
O fator relativo foi **composto**, não escolhido para cancelar o resultado.

Cinco verificações algébricas novas, CPU 0.078125s; zero novo laço,
zero chamada remota, zero alteração em originais ou gate. Isto resolve a
normalização relativa na convenção formal da conta. Não registra como feita
a continuação de toda amplitude temporal Lorentziana no espaço-forma nem a
coincidência com a hierarquia causal completa: essas continuam distintas.

Reprodução: symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/finite_relative_normalization_v2.py, em destino novo. Manifesto ao lado.
