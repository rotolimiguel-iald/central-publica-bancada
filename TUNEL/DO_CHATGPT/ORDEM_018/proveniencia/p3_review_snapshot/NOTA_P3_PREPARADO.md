# P3 sintético: contrato e instrumento preparados

[REAL — preparação local] O contrato CONTRATO_P3.json fixa somente dois jobs: P3_GR_001 usa GR_GAUSS e P3_RB_001 usa RB_GAUSS do arquivo sintético RUN_002/SYNTHETIC_ARRAYS.npz já qualificado. Cada dado é noise + signal, conferido pelo hash da injeção. Ambos têm SNR ótimo de rede IMR 20 e compartilham a mesma realização gaussiana. Não são duas realizações independentes. Não se leem D, seus centros ou strain observado.

[INPUT — escopo] A coordenação autorizou preparar P3 e reteve a execução até revisão. A preparação não exige nova pergunta ao operador. O exemplo de recibo é deliberadamente authorized=false e não autoriza execução. Não há AUTORIZACAO_COORDENACAO.json nem diretório EXECUTION_001 nesta entrega. O comando literal, inclusive hash lido do contrato, está em COMANDO_EXATO_NAO_EXECUTADO.json.

## Hipótese, prior e alvo

[INPUT/DERIVED] GR/RB são os rótulos das verdades injetadas. Os dois jobs usam a mesma hipótese de recuperação pSEOBNRv4HM_PA alinhada, com 12 coordenadas livres: duas massas detector-frame, dois spins alinhados, DTau220, distância, inclinação, RA, declinação, polarização, fase e tempo geocêntrico. DOmega220, DTau440 e DOmega440 são zeros fixos. Não há teste GR versus TGL por evidência entre datasets distintos.

As distribuições e extremos copiados de CONFIG_SYNTHETIC estão no contrato. O prior das massas é uniforme no retângulo original condicionado a 0,2 ≤ m2/m1 ≤ 1. A transformação usa a inversa analítica do CDF marginal de m1 e m2 uniforme na faixa permitida. A área normalizadora é 3477,5 massas solares², frente a 4500 do retângulo. Isso preserva a distribuição condicionada, sem rejeição de likelihood e sem normalização ambígua da evidência. Os demais priors permanecem Uniform/Sine/Cosine; RA, psi e fase são periódicos.

A PSD analítica, as grades de análise 4096 Hz/32 s e geração 8192 Hz/4096 Hz, banda 20–1024 Hz, referência 20 Hz e geocentro sintético estão pinados. Os dados não serão regenerados. A verdade RB vem do recibo sintético qualificado, derivada anteriormente com β calculado em runtime a partir de α CODATA2018 × √e; não foi escolhida a partir de centros D.

## Limites e estatutos de saída

[INPUT] Dynesty3.1.0 estático: nlive256, rwalk25, bound multi, dlogz0,1, seeds180602/180603, um processo por vez e uma thread. O contador externo inclui a inicialização e impede a chamada10001. O maxcall interno do Dynesty é adicional: a fonte instalada verifica seu teto entre iterações, portanto ele isoladamente não é uma trava rígida.

Por job: 3600 s de parede no filho, supervisor3610 s; CPU soft3300/hard3305 s; espaço de endereçamento8GiB; no máximo10000 avaliações de likelihood e no máximo10000 gerações waveform. Dois jobs somam envelopes máximos7220 s de supervisor,6610 s de CPU dos filhos e20000 likelihoods. São limites, não consumo medido.

EDOM, domínio temporal, mudança de pin, acesso fora da lista, erro nativo ou processo incerto interrompem sem nova tentativa. Não se converte falha de waveform em -infinito para aparar o prior. Exaustão controlada de limite grava diagnóstico parcial e admite o segundo job previsto. Kill/timeout incerto impede o restante. Não há checkpoint nem resume.

Convergência numérica exige contribuição restante delta_logz<0,1 antes de incluir live points, abaixo do teto e sem erro. ESS ponderado≥100 é um diagnóstico adicional; ESS baixo permanece incompleto. Nem essas condições nem dois jobs demonstram cobertura, identificação global de modos, ausência de viés ou prontidão para D. Não existe veredito físico automático.

## Custo e isolamento

[REAL] O contrato usa como referência a duração de seis gerações já medidas em P0–P2. Multiplicar a média por10000 é apenas proxy de custo da fonte, pois o custo depende das massas/spins e o overhead de likelihood não foi medido. Não se apresenta esse número como piloto PE executado ou previsão validada de14 eventos.

[REAL — código preparado] As três fontes P0–P2 foram copiadas byte a byte e permanecem pinadas. Cada geração mantém uma nova dict LAL com os quatro desvios inseridos. O driver usa apenas o construtor de waveform do adaptador; não usa o registry de injeções para acumular objetos de PE. Lê o NPZ qualificado com allow_pickle=False, verifica a reconstrução por hashes e usa a PSD pinada.

Foram inventariados1162 arquivos do runtime científico, incluindo os165 pins P0–P2 conferidos, mais o interpretador por hash. O hook Python aceita arquivos científicos/sintéticos exatos e saídas do job; recusa subprocessos e rede no filho. O supervisor cria apenas os dois filhos previstos. Imports fixos e conferência de pins antecedem o hook; isso não é confinamento de syscalls nativas nem prova de isolamento do sistema operacional. O comando usa -I -B e as variáveis de uma thread. Nenhuma instalação é necessária.

[REAL — controles de preparação] Conferência de sintaxe, pins, normalização de prior por quadratura independente, suporte de10000 pontos artificiais e Jacobiano constante. Nenhum desses controles instancia sampler/likelihood, importa Bilby/LAL/Dynesty ou gera waveform. A montagem efetiva do likelihood e a execução de P3 continuam [OPEN] até revisão e autorização da coordenação.

As quatro holds, a lista V1, fontes originais, o Atlas e a fila não foram alterados. O manifesto da preparação registra código, contrato, recibo de controles e pins; a revisão P0–P2 seq412 continua restrita à etapa anterior. Próximo passo permitido: revisão independente deste driver/contrato. Somente depois a coordenação poderá emitir o recibo para o comando exato.
