# PE-R3 e contrato temporal compartilhado

[REAL — implementação e mocks finitos; OPEN — revisão independente B e execução física]

`pe_runner.counted_likelihood_class(base,counter)` sobrescreve somente `log_likelihood_ratio`. No Bilby instalado, `log_likelihood` chama essa fronteira uma única vez; o wrapper completo não foi sobrescrito. Contador compartilhado registra entradas, retornos, exceções e soma de tempos de parede por invocação, inclusive falhas anteriores ao gerador. Chamadas apenas de ruído são excluídas. Não equivale a CPU total nem a teto global maxcall.

Snapshots cumulativos antes/depois da construção do sampler e depois de `run_sampler` distinguem as fases. `likelihood_calls`, `sampler_ncall` e `source_calls` permanecem três grandezas separadas. O custo/chamada da fonte mantém seu denominador próprio. Exceções são preservadas e o recibo de falha inclui o contador. Interrupção forçada pelo controlador pode impedir a emissão final desse contador; o controlador conserva seu recibo parcial de parede/grupo.

O teste usa o wrapper completo instalado, corpo da razão substituído por função analítica e dois processos fork com sete chamadas cada. Resultado: 17 entradas, 16 retornos, uma exceção; nenhuma contagem duplicada e nenhuma execução de PE, strain ou waveform. O escopo não demonstra desempenho da likelihood física nem overhead sob 24 workers. Recibo: `LIKELIHOOD_COUNTER_FINITE.json`.

`registration_guard.checked_registration` agora verifica também as origens ativas de astropy e pandas contra os arquivos já pinados no runtime. Ambos conferiram no teste, sem instalação ou alteração de `/opt`.

Por instrução do principal, `pseob_source.py` delega os limites escalares ao seu `temporal_contract.validate_time_contract`, passando também dtau220/440. O helper foi lido; nenhum módulo de injeção foi editado. Replay com funções LAL mock devolvendo os limites previamente medidos verifica os mesmos 16 registros em duas janelas (32 decisões), sem recomputar limites ou gerar sinais. Mantidos ±22 ms e aborto visível por janela. Não certifica todo o domínio do prior. Recibo: `SHARED_TEMPORAL_REPLAY.json`.

As únicas três fontes A modificadas neste complemento são `pe_runner.py`, `registration_guard.py`, `pseob_source.py`. Elas voltam a aguardar B, sem nova alteração durante a revisão. PE-R1/R2 da injeção são responsabilidade do principal/B. Hashes e lista de arquivos no recibo `PE_R3_RECEIPT.json`.
