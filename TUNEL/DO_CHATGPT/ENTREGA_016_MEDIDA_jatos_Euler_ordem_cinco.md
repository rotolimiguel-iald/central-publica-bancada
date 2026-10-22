[DERIVED+CAS — controle diferencial das ordens efetivamente usadas]

Os novos grafos usam até três derivadas adicionais sobre as duas linhas,
além do operador Euler de ordem2. A tabela inicial só conferia pares até
ordem4; por isso verificamos agora TODOS os165pares Euler até ordem
adicional3 (par subjacente até5), sem repetir a avaliação dos grafos.

E_(u+i,v)+E_(u,v+i)=q_i E_(u,v), troca de linhas, paridade e grau
homogêneo2+|u|+|v| passaram em675controles, CPU13.6875s,
rc0. Esse alcance cobre as palavras diferenciais dos grafos registrados;
não transforma o controle escalar em fechamento tensorial de Ward.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
