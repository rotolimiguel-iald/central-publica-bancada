[DERIVED — completamento BV quadrático com cutoff; REAL — CAS exato; OPEN — Q2 causal completa]
# A7.b — termos de fronteira do contato finito hc
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T01:34:38.127358+00:00.

N é o contato quártico da Hessiana e R o contato cúbico da fonte,
calculados nas entregas anteriores, com seus coeficientes lidos dos
resultados. No setor livre principal, sh=Kc, sc=0,
s hat_h†=Eh e EK=0; hat_h† conserva seu termo com antighost.
E é a Hessiana física não gauge-fixada. Seja chi uma função escalar
externa BRST-inerte. Considere

    B_chi=integral chi [ (1/2) h:N(partial)h + lambda hat_h†:R(partial)c ].

As constantes físicas globais continuam separadas; lambda não é ajustado.
No pareamento formal integrado, N*=N, E*=E e R* tem sinal negativo
por ser cúbico. A integração por partes dá EXATAMENTE

    sB_chi = integral c · [chi K* N h + [K*,chi] N h
                         +(1/2) K* [N,chi]h
                         +lambda(chi R* E h + [R*,chi] E h)].

A primeira correção tem coeficiente UM, não meio: há duas contribuições
de 1/2 ao mover as derivadas das duas pernas métricas. K* atua no
produto inteiro à sua direita. Até cinco derivadas de chi no setor
métrico e três no setor fonte podem aparecer. Quando chi é constante,
todas essas correções desaparecem e recupera-se o resultado anterior.

**Consistência com ghosts.** Para momentos formais q do h, r do ghost,
k=-q-r do cutoff, a parcela métrica é

    (1/2) [ N_q(H,K_r v) + N_r(H,K_r v) ],

onde N_p(H,T)=H:N(p)T. Substituir H=K_q w dá coeficiente simétrico sob
(q,w)<->(r,v); a anticomutação dos dois modos ghost o anula.
A fonte anula por E_q K_q=0. Logo s0(s0 B_chi)=0 com chi variável,
para esta primitiva. Não se descartou uma divergência com cutoff variável.

Controle q=e0,r=2e0,v=w=e0: manter somente chi vezes a fórmula de
cutoff constante dá defeito de troca **-1323/320**. O completamento
dá zero; o coeficiente simétrico é -357/320. Isso vale nas duas
assinaturas. O teste detecta também o erro de meio no primeiro
comutador e o sinal errado do adjunto cúbico.

CAS: 304 identidades polinomiais gerais, duas assinaturas,
3 controles, rc0, CPU 8.390625s. Verificação independente
em posição: chi=(1-x²)^6 em [-1,1], com os jatos necessários nulos
nas extremidades, 12 checks e 2 controles, rc0,
CPU 0.6875s. Por exemplo a omissão de fronteira métrica
no primeiro caso muda a integral em 99776/32725;
na fonte, em 25856/36465, ambos não zero.

**Alcance:** obtivemos o completamento local com cutoff da primitiva
principal já medida. Não se identificou por esse cálculo o coeficiente
de todos os termos com derivadas dos acoplamentos no produto temporal
original. Curvatura, fases relativas da amplitude e a família multilocal
admissível continuam necessárias para Q2 completa no modelo truncado.
Nenhum original, kernel ou gate alterado. Reprodução e hashes nos
manifestos finite_cutoff_contact e finite_cutoff_position.
