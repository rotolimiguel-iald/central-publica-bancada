[DERIVED — consistência BRST livre da soma de contatos e de sua localização]

Objetos já construídos: N_s para o contato singular, N_W para o contato
misto com a referência suave, R_W para a fonte (inclusive rotação e primeiro
jato), E para Einstein livre e G para a transformação de gauge. Não se
impõe R_W=L_W G. Seja N=N_s+N_W. Sob as condições já explicitadas de
adjunto formal, N*=N, E*=E e EG=0. A referência e o cutoff são fixos
sob s0; s0h=Gc, s0hdagger=Eh e s0c=0.

O funcional que reúne as duas construções existentes é

    Bchi=-C_E [1/2 <chi h,N h> + <chi hdagger,R_W c>].

Integração por partes, preservando o cutoff, dá

    -s0 Bchi = Achi
              =C_E <h, Mchi Gc + E(chi R_W c)>,
    Mchi=(chi N+N chi)/2.

No interior chi=1 isso é a soma já medida
    A/C_E=<h,N_s Gc+N_W Gc+ER_W c>.
Na região onde o cutoff varia, a expressão mantém [N,chi]/2 e
[E,chi]R_W. Trata-se da localização pela primitiva; a igualdade com
TODOS os termos de produtos temporais localizados ainda precisa ser
conferida. Não se declara que uma localização escolhida calculou os
diagramas que ainda não foram extraídos.

A consistência livre segue sem exigir um novo operador:

    s0 Achi/C_E=<Gc,Mchi Gc>+<Gc,E(chi R_W c)>=0.

A primeira parcela é zero porque Gc é ímpar e Mchi é formalmente
autoadjunto. Explicitamente, para c=eta1 c1+eta2 c2, o coeficiente de
eta1 eta2 é <Gc1,Mchi Gc2>-<Gc2,Mchi Gc1>=0. A segunda é zero por
integração por partes e EG=0. Este é o uso do produto graduado: tratar
c como variável real comutativa não demonstraria essa identidade.

Portanto a soma construída é s0-exata e representa zero na cohomologia
livre relativa dos funcionais locais, módulo divergências e sob as
hipóteses de suporte. Não se conclui que a quebra Q2 integral pertença
a essa soma, nem que sua classe no BRST interagente seja zero.

Controle independente com os operadores existentes: campos em4D
dependentes de uma coordenada, perfis polinomiais C5 de suporte compacto,
referência métrica anisotrópica variável de posto1 e referência ghost
variável. Reunidos N_s, N_W, R_W e o cutoff. Os três coeficientes de
dois ghosts antissimetrizados são zero. O controle que omite [N,chi]/2
é não nulo em todos os três; por exemplo:

    62447735709630464/55655536011075.

São52 verificações, CPU21.015625s, rc0. O ponto b=c=t=0 foi usado
somente no controle polinomial, não como escolha do operador. A prova
escrita vale para qualquer membro formalmente autoadjunto da família.
O controle não testa todas as componentes curvas nem a existência de
um estado de referência físico; o teorema é condicional à tipagem acima.

Para o próximo degrau, A1=-s0B e s0A2+s1A1=0 implicam
s0(A2+s1B)=0. O valor efetivo de A2 e a exatidão dessa nova classe
não decorrem da conta anterior. Devem vir dos produtos temporais da
prescrição, mantendo as contribuições ainda não calculadas.

Nenhuma fonte original, kernel Lean, prescrição ou gate foi alterado.
