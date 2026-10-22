# Execução única P3 CODEC_002: falha de inicialização preservada

[REAL] Sob recibo específico da coordenação seq448, o supervisor foi lançado uma única vez. Identidades: supervisor PID 4659, filho PID 4660; início 2026-10-06T03:04:02.292040+00:00. O processo retornou; nenhuma sessão ficou pendente.

P3_GR_CODEC_002 terminou FAILED, código do filho 2: ValueError: Interferometer H1 not implemented. O hook registrou tentativa bloqueada de leitura de /opt/lal_env/lib/python3.12/site-packages/bilby/gw/detector/noise_curves/aLIGO_O4_high_asd.txt durante inicialização do detector. NPZ sintético e H1.interferometer aparecem nas leituras anteriores; cp437 não repetiu a falha. A fronteira observada é inicialização/configuração do detector, antes de likelihood e waveform.

Contadores: zero avaliações de likelihood, zero chamadas nativas de waveform, uma APPLICATION_EXCEPTION. domain_error_total permanece null; não é uma falha de domínio certificada. Não há convergência, ESS ou recuperação científica para avaliar.

Tempo do filho: 2.572406232 s parede; 2.264531530 s CPU no intervalo e 2.501248534 s CPU total do processo. Parede da campanha: 3.110528136 s. Estes números medem inicialização interrompida, não custo de PE.

P3_RB_CODEC_002 não foi iniciado; seu diretório/CLAIM não existe. O supervisor interrompeu conforme contrato. Não houve retry, resume, fallback, mudança da allowlist ou outro pacote corretivo. Dados D, V1 e quatro holds continuam intactos. V2 falho, candidato e entradas pinadas foram reconferidos sem alteração.

[OPEN] A coordenação decide o próximo passo após examinar o diagnóstico. Este registro não concede nova execução ou reparo.
