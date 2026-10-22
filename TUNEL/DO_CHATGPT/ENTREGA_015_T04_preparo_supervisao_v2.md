[REAL — revisão e controles de software; piloto não executado]

Abertura016SHA256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a
Data: 2026-09-26T15:57:32.997249+00:00

Revisão local independente: 536d443ba2612e30407a0a4274836bdaefa553b58ca743f373da7e63d29634c3. Versão anterior preservada. V2: 1e10069ebee87c63af02adcfcba47f032b66d099395aec592b40f8c0d53a62c4; controles dos dois validadores:24/24, SHA256 5d65c80807e4e588e74926052a62e968ff50e64c8f522cf0ede0c5f4a779fca0. O teste cobre apenas classificação e pareamento de registros; não é teste de lifecycle completo nem fonte nativa.

Correções: preflight antes de reservar pasta, pareamento exato400PRECALL/RETURN e resumo, qualificação incompleta sai com erro, piloto classifica ausência/falha/partial/cleanup, processo seguinte vedado até confirmar limpeza. V2 lê a alocação corrente e recusa se o limite interno do controlador exceder o reservado.

Antes do piloto: alocação v2 deve reservar8h para coincidir com o hardcap já registrado, transferindo4h de T10(19→15); total34,2h permanece. Reserva prudencial não é custo medido; reconciliar saldo real depois. Até esta nota, essa alocação ainda NÃO foi publicada.

Limite de processos: a arquitetura inspecionada tem supervisor+controller+runner+Pool24=27[DERIVED]; snapshots não são hardcapdeSO. cgroup pids.max conta threads e não se confunde com esse limite. A verificação de lifecycle fica depois do término dos nulos para não somar processos acima28. Nenhuma alteração de código científico, job pinado, semente cega, original ou gate.

T03 continua na sessão64813, controlador próprio com1halocada. Não reiniciar. Próximo: recibo finaldosnulos→entregaT03→preflightT04.
