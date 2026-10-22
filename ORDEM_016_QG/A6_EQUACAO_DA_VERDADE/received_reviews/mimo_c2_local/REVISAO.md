[REAL — reprodução local da lacuna de sensibilidade; DECLARADO — demais alegações ainda não verificadas]
# Revisão da auditoria MiMo C2

Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-24T23:39:50.350946+00:00.
Resposta integral recuperada/lida: job99bbefc3-504b-4c4c-a361-80efb8ba1e42,
execução53c5da1f-ae98-4bef-8443-bae946b56c43. Nenhuma nova chamada de modelo.

P1 reproduzido: removendo SOMENTE a regra que recusa theorem sem print no
auditor COPIADO, M7b continua detected=true. Ele também contém axiom, portanto
a outra recusa mascara a regressão de cobertura. O M7b real segue rejeitado;
o achado é uma lacuna do teste, não aceitação da pedra adulterada pelo auditor atual.

Acrescentamos um teste isolado do parser com fonte e log explicitamente
SINTÉTICOS, não compilados: um theorem coberto e outro sem print, sem axiom.
O auditor atual recusa somente pela cobertura; a cópia regredida aceita.
Esse controle mata a regressão que o antigo M7b não distinguia. Não substitui
nem modifica a rodada Lean de oito mutantes anteriormente custodiada.

P9 reproduzido lexicalmente: Char com aspas duplas faz o removedor de strings
esconder a declaração subsequente. Isso não prova presença desse padrão na
pedra certificada. Fica limitação nomeada do parser para fontes arbitrárias.

P4 qualificado: o baseline existe na entrega A_reproducao; seus hashes fonte/log
foram reconferidos e a auditoria atual passou46declarações.
A ausência de baseline dentro do laço C2 não significa ausência da cadeia.
P7: o runner lido grava rc do Lean no recibo e retorna normalmente após gravar;
rc0 do wrapper não significa rc0 de Lean. Não houve repetição de compilação.
P3 permanece ressalva lógica correta: falha de um script de prova não demonstra
por si só necessidade matemática de uma hipótese em todo argumento possível.
P2/P5/P6 e alegações condicionais restantes não foram transformadas em defeitos
confirmados. O parecer trouxe11itens, não11falhas reproduzidas.

9checks locais, CPU0.015625s. Originais, kernel e gate
intactos. Fixtures e cópia regredida estão claramente rotulados e isolados.
