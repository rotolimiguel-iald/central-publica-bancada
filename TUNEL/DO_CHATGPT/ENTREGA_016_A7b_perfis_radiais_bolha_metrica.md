[DERIVED — perfil radial local; REAL — CAS exato; OPEN — conversão covariante e Q2]
# A7.b — contração da bolha métrica em posição
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`. UTC 2026-09-25T04:10:08.297749+00:00.

**Resultado novo:** o motor de vértices diferenciados50x50 foi contraído
com os jatos tensoriais nas duas pontas e o volume em coordenadas normais.
O limite plano reproduz os cinco coeficientes obtidos em momentos. O primeiro
teste conferiu7500 componentes dos jatos e cinco valores de laço: total
7505 checks, rc0, CPU2.3125s.

O teste ampliado conferiu a decomposição de40 vértices com momentos
independentes, três contrações explícitas por quatro índices, os100 pares
ordenados da fibra e três pares com momento fora do eixo. Inclui controles
de homogeneidade radial. Total157 checks, rc0,
CPU85.59375s. A cubatura racional integra monômios até grau8;
a contagem de derivadas limita o plano a8 e a primeira curvatura a6.

**Correção preservada:** a tentativa inicial presumiu quatro invariantes
simétricos no perfil radial; falhou com `Linear system has no solution`,
rc1 após45.234375s de CPU medidos na última linha. O perfil deixa X eY
em posições diferentes: integra X, ancora Y e usa o quadro radial de Y.
O teste v2 permite separadamente (pAp)trB e(pBp)trA, sem alterar o motor.
O fracasso antigo e seu hash permanecem; não foi forçado um coeficiente.

Retirando K*A0, A0=1/(8*pi²), na base ordenada

    [p²trAB, p²trA trB, (pAp)trB, (pBp)trA, pABp],

a bolha com dois vértices derivativos fornece

    ['163/9', '-283/18', '241/9', '131/6', '-160/3'].

O coeficiente angular de log(mu²z), mantido até o fim, resultou zero
nos cinco invariantes. Isto não diz que todas as partes finitas ou todos
os diagramas estão livres de log; diz apenas o que este perfil retornou.
Os dois coeficientes mistos diferentes são um aviso para não confundir
esse perfil com a Hessiana covariante integrada autoadjunta.

**Controle independente de potencial:** incluídos os dois posicionamentos
de um vértice cúbico do potencial e um derivativo, com propagadores principais,
a conta em posição reproduz ['-32', '20', '-34', '80'] na base simétrica
anterior. 55 pares, rc0, CPU33.34375s. A tabela
foi cotejada com os bytes do resultado em momentos, sem reajuste de fatores.
Somada somente essa parcela ao perfil derivativo, a base ordenada dá

    ['-125/9', '77/18', '-65/9', '-73/6', '80/3'].

Normalização: bolha bruta/A0; NÃO inclui o peso-1/2 da Hessiana efetiva.
As parcelas de inserçãoE já estão no parametrix e não devem ser somadas
novamente. O tadpole quartico previamente pago é outra contribuição.

**Escopo pendente:** converter estes perfis em operador covariante com
derivadas ordenadas e adjuntos; verificar o termoK² completo; combinar
ghost/fonteBV/tadpole; tratar extensão finita, estado e cutoff. Nenhuma
anomalia causal completa ou fechamento físico é inferido. Gate intacto.

**Distribuição adicional:** Kimi recebe a tarefa de conversão radial→covariante;
MiMo recebe auditoria independente da contração esparsa/sinais/grauangular.
As prévias selecionaram os provedores exigidos. A coordenadora confirmou
staging APÓS metric_quartic, com nove unidades aguardando vaga e cinco
registradas no snapshot; uma chamada MiMo em andamento. Estas duas novas
unidades ainda NÃO foram executadas. Os resultados acima não foram enviados
aos revisores. Fontes, hashes, IDs e memória comum constam no catálogo.
