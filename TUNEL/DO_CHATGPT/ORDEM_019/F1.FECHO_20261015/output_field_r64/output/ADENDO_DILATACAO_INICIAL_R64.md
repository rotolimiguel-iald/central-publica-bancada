# Adendo R64 — hipótese inicial e realização instrumental

**[INPUT — H_MARKOV_VACUUM_PORTS, explicitação solicitada na revisão prévia]**

O estado inicial é `ρS,OH(0) ⊗ |vac⟩⟨vac|` dos **cinco banhos**, com a preparação óptica–OH já fixada no plano. O vácuo dos banhos é produto entre canais distintos. Os incrementos futuros de entrada são independentes do sistema e do passado; os operadores de sistema são adaptados à filtragem temporal dessa dilatação.

Escolhe-se uma dilatação de Hudson–Parthasarathy com matriz de espalhamento identidade e os cinco operadores de colapso explicitados no contrato. As duas portas ópticas monitoradas correspondem a canais distintos; os três canais restantes permanecem na dinâmica e não são monitorados. A relação de entrada–saída adotada é

`dB_out,j(t) = dB_in,j(t) + L_j(t) dt`.

A corrente homódina ideal, com a fase do oscilador local indicada por θj, é normalizada como

`dX_j = [exp(−iθj) dB_out,j + exp(iθj) dB_out,j†]/√2`.

No vácuo de entrada, a tabela de Itô `dB_in,j dB_in,k† = δjk dt`, com os demais produtos de segunda ordem nulos, dá `dX_j dX_k = δjk dt/2`. Essa é a origem do termo diagonal de ruído no sistema de momentos filtrados, e não uma normalização acrescentada depois de ver o resultado.

Este adendo especifica a **hipótese instrumental utilizada**; não afirma que o GKLS, sozinho, selecione esses banhos/portas ou que a patente implemente fisicamente esta dilatação. Não altera parâmetros, preparo sintético, fórmulas, runner, tolerâncias ou controles do plano. Nenhuma execução ocorreu antes deste adendo.
