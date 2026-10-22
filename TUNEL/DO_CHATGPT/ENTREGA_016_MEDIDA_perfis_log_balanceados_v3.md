[DERIVED+CAS — conversão balanceada dos perfis logarítmicos de Hadamard]

A tentativa v1 falhou no controle de linha suave: o valor é3/4, não1.
A v3 registra essa incompatibilidade; não a elimina trocando a expectativa
por uma alegação de sucesso. O motor e as tentativas originais são preservados. A v2 falhou apenas
na redução de uma identidade racional (expand não reduz denominadores);
a v3 usa cancel no verificador, sem alterar as expressões do motor.

O motor mantém a mesma prescrição R_bal, agora em linhas rotuladas
1/z,log(mu²z),1. Não soma coeficientes de Rraw aos grafos balanceados.
1485 entradas até ordem4 foram calculadas; troca de linhas/perfis,
Leibniz até ordem3 e coincidência com o motor f/f existente conferidas.

Correções de Euler normalizadas por CE:
 f/f:3*q0**2/32 + 3*q1**2/32 + 3*q2**2/32 + 3*q3**2/32; f/log:1; log/f:-1; f/1:3/4.
Os valores f/log e log/f não devem ser confundidos: na segunda posição
o Laplaciano age na outra linha; trocar as linhas troca também a inserção.

A extensão ingênua dá R_bal((Box f)1)/CE=3/4 e
R_bal(f Box1)/CE=-1/4. Isso não respeita a linha constante como suave;
Leibniz sozinho não fixa essa compatibilidade. A tabela, portanto,
NÃO é promovida a família temporal completa.

No modelo RADIAL escalar de primeira curvatura,
H=1/z+K/4-K log(mu²z)/2 e L=4z dzz+(8-2Kz)dz.
L1(1/z)=2/z cancela o termo -Box(log)/(2z) fora da diagonal.
Mas não se pode reduzir L1 antes de estender: seus coeficientes
(z delta_ij-x_i x_j)/3 e -2x_i deixam contato adicional -1/8.
Este contato é mantido na conta abaixo.
O contato composto no jato sem derivadas adicionais é
 CE[3q²/32+K*(1/16)] no recorte descrito.
Esse número pertence à extensão com o defeito suave identificado acima.
Não é o valor de uma família temporal admissível nem a anomalia curva.

Faltam os jatos covariantes bilocais/tensoriais, a referência suave e a
montagem dos vértices de curvatura na MESMA família. Esta conta não
identifica o horizonte físico nem demonstra causalidade lorentziana.
3966controles;CPU7.515625s,rc0. Sem chamadas/gate.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
