[REAL — parecer auditado e parcialmente refutado; DERIVED — identidade de registro; Q2 OPEN]

DeepSeekcd6 confirmou o transporte pré-multiplicação com as duas correções
A1, no mesmo escopo do CAS anterior. Porém introduziu X_anti=(X(F,G)-X(G,F))/2
para as entradas PARES. Isso é incorreto: T2 e A2 são graduadamente simétricos,
e o antibracket ímpar satisfaz (F,G)=(G,F) quando ambos são pares.

Controle independente: F=(hdag+barc)h c em ambas as entradas, no modelo de
Euler qhdag=m h. A multiplicação dos dois slots dá
 m exp(t BH)[q,BF]=-2m fh t(fg-wg)h c,
em geral não zero. A projeção anti proposta apagaria o resultado com F=G.
Isto refuta a fórmula do parecer; não é cálculo distribucional da TGL.

Há outro erro: t*m*C-bracket não é outra forma de -m*C-bracket. O primeiro
é parte de um resíduo cru; a definição Tc2=-1/t(T2-S2) impõe o segundo.
Mantendo a mesma representação H e supondo TODOS os domínios de extensão,
o simples produto de operadores fornece a identidade de registro correta:

 A R E-E R B não é a ordem usada; a ordem correta é A R E-R E B
 =(A R-R A)E+R(A E-E B).

Com A=QW, B=Qin, E=E_H e A E-E B=t E_H[q,BF], segue

 A2_H=-m R(E_H[q,BF])-(1/t)m[QW,R]E_H-(F,G).

Usam-se entradas graduadamente SIMÉTRICAS, sem a projeção anti do parecer.
A aplicação N_H recupera T1(A2); a multiplicação m e a representação
não devem desaparecer silenciosamente da fórmula. [QW,R]=[q,R]+t[RW,total,R].
Esta é uma identidade condicional de registro de termos, não a construção
da extensão do contato composto. R ordinário sobre kernels fora da diagonal
ainda não especifica por si só R(delta vezes propagador). Nada foi zerado
por definição para declarar ausência de anomalia.

6 controles locais novos, CPU 0.03125s,rc0. Resposta original e recibo
preservados. Uso={"prompt_tokens": 232267, "completion_tokens": 30041, "total_tokens": 262308, "prompt_tokens_details": {"cached_tokens": 512}, "completion_tokens_details": {"reasoning_tokens": 27906}, "prompt_cache_hit_tokens": 512, "prompt_cache_miss_tokens": 231755};
custo estimadoUSD0.105578772, contabilizado uma vez, não fatura.
Kimi continua com unidades preservadas sob cota; nenhuma chamada substituta.
Próximo A7.b: construir/identificar o contato Euler composto e somar a
fonte localizada (I1,B1) agora calculada. Originais/kernel/gate intactos.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
