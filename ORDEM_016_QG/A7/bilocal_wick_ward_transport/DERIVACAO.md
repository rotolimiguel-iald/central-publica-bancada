[INPUT/ONTO — fala do operador; DERIVED+CAS — transporte de Ward entre duas entradas]

Fala do operador, verbatim: «Exatamente, aquilo que satisfaz a leitura do conteúdo para afirmá-lo como reconhecido pela forma».

O reconhecimento é aqui aplicado como compatibilidade entre a leitura de Wick
e o diferencial livre. Não acrescentamos um operador ao motor. Conservamos
as correções de uma entrada já identificadas, inclusive nos dois argumentos.

Escreva t=i hbar e decomponha a contração suave W em Cx+Cy+BW, sendo BW
a contração cruzada. Ponha RW=[q,Cx+Cy+BW], Rx=[q,Cx], Ry=[q,Cy].
O produto temporal, expresso na leitura local H, contém exp(t BH), com
BH=BF-BW. BF é a contração temporal na referência anterior; não é a ação
efetiva 1PI. Esta escrita exige a mesma W nas entradas e na saída.

Como q é linear e as contrações são operadores pares de segunda ordem com
coeficientes independentes dos campos, os comutadores com q são de segunda
ordem e comutam com essas contrações. Portanto, por conjugação exata,

 (q+t RW) exp(t BH) - exp(t BH)(q+t Rx+t Ry)
 =t exp(t BH)([q,BH]+[q,BW])
 =t exp(t BH)[q,BF].

Essa é uma igualdade de operadores no produto tensorial graduado, antes da
multiplicação dos campos. A multiplicação transporta RW total à correção
de Wick na saída. O termo do lado direito é a fonte de Ward temporal;
quando BF usa o Green livre adequado, inclui os contatos de Euler.

A identidade mostra exatamente onde entram AS DUAS correções A1: a fonte
espúria -[q,BW] é compensada por +[q,BW]. Omitir Rx ou Ry deixa, respectivamente,
t exp(t BH)Rx ou t exp(t BH)Ry. No modelo finito de controle ambos são não
zero. É inadequado comparar representações com apenas uma dessas correções.

Precisão essencial: só a FONTE [q,BF] perdeu W. O fator exp(t BH) ainda
depende da representação. O CAS também rejeita a afirmação mais forte de
independência total. Na teoria distribucional esse fator aplicado ao contato
produz produtos do tipo delta vezes propagador: ainda é preciso estendê-los
na mesma prescrição e juntar os contatos radiais de duas linhas já medidos.
O cálculo não autoriza substituir todo esse objeto por zero.

Controle finito: duas cópias de um campo bosônico h, anticampo ímpar hdag
e par ghost espectador; q(hdag)=m h. É um setor de Euler nilpotente, não o
complexo BRST completo nem um Green de espaço-tempo. Incluímos vértices
hdag*h*c e barc*h*c para tornar ambas as omissões detectáveis. Resultado:
31 controles exatos, CPU 0.40625s, rc0.

Próximo passo A7.b: identificar/estender a fonte de Euler composta na família
já fixada; o transporte algébrico das duas inserções A1 foi explicitado.
Q2 completa OPEN. Sem nova chamada externa, alteração de original ou gate.
AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.
