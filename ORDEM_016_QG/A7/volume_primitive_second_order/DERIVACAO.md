[DERIVED+CAS — continuação quadrática explícita da primitiva linear; A2 integral OPEN]

Mantemos a1=alpha_W div(c), cujo alpha_W auxiliar foi calculado antes;
seu fator físico ainda é explícito. B1=alpha_W tr(h)/2 já estava derivado.
Uma continuação algébrica é a expansão de volume
B(u)=alpha_W(sqrt(det(I+u g^-1 h))-1)=u B1+u² B2+...,
B2=alpha_W[(tr h)²/8-tr(h²)/4]. Não alegamos unicidade dessa continuação.

Para q(u)=q0+u q1, q0h=Lie_c g, q1h=Lie_c h e q1c=c.nabla c,
q(u)B(u)=alpha_W u div(c rho(u)). Portanto
 q0 B1=a1,
 q0 B2+q1 B1=a2=alpha_W div(c tr(h))/2,
 q0 a2+q1 a1=0.
O CAS conserva a anticomutação dos jatos: sum(d_i c^j)(d_j c^i)=0,
mas sum c^j d_i d_j c^i não é zero. É exatamente a fonte inhomogênea
que q0a2 cancela. Inverter o sinal de q1c ou omitir q1B1 falha.

Foram 20 controles em assinaturas euclidiana e lorentziana,
CPU 0.15625s, rc0. A expansão do determinante foi conferida
separadamente por menores principais. Em coordenadas normais, as identidades
de volume têm a tradução covariante correspondente. Não construímos estado
global nem fixamos a continuação física do fator alpha_W.

Com teste compacto chi, int chi*a2=-alpha_W/2 int(dchi).c tr(h).
Logo o termo não desaparece sob localização. Aqui chi é o TESTE externo
de um diferencial BRST NÃO LOCALIZADO. Substituir q1 por chi*q1 é outro
problema e acrescenta termos de derivadas de chi. Não identificamos esta
continuação com A2(Vchi,Veta), nem com a soma completa das inserções I1/I2.

Também não adotamos B como contratermo da prescrição causal existente: sua
realidade, naturalidade e vínculo à normalização temporal precisam ser
verificados. Ele usa a métrica de fundo e K constante no modelo truncado;
não é uma afirmação de independência entre fundos. O resultado fornece uma
família explícita para transportar a primitiva de A1, mantendo os termos
de consistência em vez de declarar A1 zero por conveniência.

Próximo: fonte de Euler composta e sua extensão na mesma família T2.
Nenhum original, kernel ou gate alterado. AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
