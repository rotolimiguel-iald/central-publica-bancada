[DERIVED — identidade da completação covariante até O(K), condicionada à ponte distribucional; Q2 OPEN]

Data 2026-09-25T09:59:28.073936+00:00. Abertura SHA256 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a.

A família quadrática N_bct satisfaz N_bct G=A_cov até primeira ordem
na curvatura, nas duas completações de regulador, com b,c,t livres.
Foram conferidas 256 igualdades simbólicas em todos os momentos
e polarizações; CPU 6.53125s. Não foi escolhido contratermo.
O comando do cálculo foi A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/bilocal_curved_contact_primitive_check.py; terminou com rc0.
Log SHA256 389138126563b0df3bd9671ae3bc416330d284a7f72e47b541486bd9073643c4.

O alcance é a identidade do operador covariante definido no cálculo.
Passar do contato em derivadas de delta nos dois extremos para esse
operador exige conferir transposição, sinal, densidade e mudança de
âncora. Essa ressalva permanece explícita: não se afirma ainda que o
contato efetivamente medido foi removido, nem que a Q2 completa foi paga.

## Divisão de trabalho a pedido do operador

- Kimi: ponte entre o contato em frame normal e a completação covariante,
  incluindo derivadas ímpares e transposição entre os extremos.
- DeepSeek: autoadjunta da Hessiana de quarta ordem e expansão ordenada
  dos termos do corte, incluindo [N,chi]/2 e o sinal na próxima descida.
- Bancada: verifica as respostas contra fontes e cálculos locais.

Prévia Kimi: 21049 caracteres, selected=kimi. Prévia DeepSeek: 15673,
selected=deepseek. Ambos receberam restrição de uma chamada por unidade
e memória científica comum pelo adaptador. Catálogo e recibo estão em
C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A7\orchestration_contact_bridge_v2. A coordenação aceitou staging depois do catálogo
bilocal_completion_v2; ainda não há job_id para as duas novas unidades.
A fila estava em 5/5, com Kimi ativo. Não se abriu outro worker.

A primeira preparação Kimi tinha 24111 caracteres e foi recusada
LOCALMENTE na prévia, antes de qualquer envio. V2 retirou apenas uma fonte
auxiliar redundante. A tentativa e os dois pacotes são preservados.

MiMo acumulou outra falha IncompleteRead; o pedido seguinte está retido
para revisão do transporte. Não foram repetidas chamadas terminais.
Os pareceres harmônico/suave recém-entregues pelo Kimi serão auditados
separadamente; não se promove conclusão textual a prova.

Permanecem fora deste resultado W geral, demais diagramas locais, K²,
aridades superiores e valores de contorno lorentzianos. Próximo passo:
auditar a ponte e os termos localizados, continuando A7.b no prazo vigente.
Nenhuma alteração de um.py, kernel, gate, fonte científica ou parâmetro.
