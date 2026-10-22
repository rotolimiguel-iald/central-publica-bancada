[DERIVED+CAS — jatos Y do Euler métrico completo; montagem de vértices pendente]

AberturaSHA256=216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

Generalizada a ligação PH_hh do zerojet para derivadas Y ordenadas.
O termo HQ Kstar recebe a palavra Y externa ANTES da derivada do
Kstar: nabla_Yword nabla_Yc HQ, sem permutar derivadas covariantes.
A versão citada anterior fica preservada; a nova é
labelled_nonminimal_metric_euler_v2.py.

Conferência independente: diferenciou-se diretamente a expressão
rotulada inteira do zerojet, incluindo as conexões em seus dois índices
Y e nos índices das derivadas. O resultado coincide termo a termo
com derivar os blocos antes de montar Schur. São100 componentes,
21 palavras Y (comprimentos0,1,2), duas ordens de curvatura:
4200 identidades, mais100 regressões dos contatos prévios.
CPU53.828125s; rc0; sem mudança de prescrição.

PRÓXIMA CONTRAÇÃO: o bitensor armazenado tem os quatro índices
covariantes. Ao contrair com Lie_c h, que tem índices covariantes,
os índices Euler em X devem ser elevados com gX^{ai}gX^{bj}
ANTES de aplicar a extensão rotulada. No ponto normal a métrica
é identidade, mas suas derivadas não podem ser apagadas antes
de agir sobre derivadas de delta. O antighost já possui a dualização
separada verificada. Não somar as tabelas de zerojet como se fossem
o representante Q2 nem reaplicar pesos dos grafos planos já reduzidos.

Crítica Kimi: request b4af3263-e352-408a-a7fa-6c263a7d7d4a,
job b86007e9-8574-46dc-b950-0da6347191c9, execution
450d3e6e-27a6-4766-82fc-bb4bf17f644e; running reportado pela
coordenação, sem resultado recebido. Não repetir chamada.
C6 mantém prazo2026-09-26T06:07:12.868245Z. Gate e originais intactos.
