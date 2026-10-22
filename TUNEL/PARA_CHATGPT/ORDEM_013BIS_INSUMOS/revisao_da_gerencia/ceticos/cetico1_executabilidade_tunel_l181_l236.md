# CÉTICO 1 — achado executabilidade_tunel, ORDEM 013-bis l.181 (§4 E3) e l.236 (§6 Instrumento)
Data: 22/09/2026. Veredito: **refutado = false** (achado confirmado por medição; gravidade IMPORTANTE mantida).

## O que medi (WSL, 22/09, por script)
1. `/opt/lal_env/bin/python`: lalsimulation 6.2.1; bilby 2.8.2; dynesty 3.1.0; gwpy 4.0.2; h5py 3.16.0; lalinference 4.1.10;
   `pSEOBNRv4HM_PA` True; `SimInspiralWaveformParamsInsertDTau220/DTau440/DOmega220` True; pycbc/pesummary/pyseobnr AUSENTES.
   `'lal_waveform_dictionary' in inspect.getsource(bilby.gw.source)` → True.
2. `/opt/pycbc_env/bin/python`: pycbc 2.11.0, lalsimulation 6.2.1, pSEOBNRv4HM_PA True; bilby AUSENTE.
3. Teste da cola: `WaveformGenerator(frequency_domain_source_model=lal_binary_black_hole, waveform_arguments={approximant:'pSEOBNRv4HM_PA', lal_waveform_dictionary: dict com DTau220})`,
   (36+29) M☉, 4 s @ 2048 Hz: DTau220=0 vs −0,5 → diferença relativa máx. 0,032 da forma; 0,13 s / 0,11 s por forma. Ou seja: o caminho `frequency_domain_source_model` padrão
   já transporta o LALDict até o pSEOB — `time_domain_source_model` (l.181) NÃO é exigido. O que falta é só um source model que insira o DTau220/DTau440 AMOSTRADO no dict a cada chamada (~20 linhas).
4. Base da frase «nenhum ambiente tem tudo» na medição da gerência (`medir\E_instrumento\MEDICAO_E.json` l.195-235; `SINTESE.md` l.76): os «ausentes» são pyseobnr, pyRing, qnm, pycbc.
   Nenhum deles é insumo de E3.1 (PE bilby+dynesty com pSEOBNRv4HM_PA do lalsimulation). A frase é verdadeira para o instrumento da ORDEM 013 §5 inteiro, mas na l.181 está dentro de E3 e induz
   a bancada a montar venv desnecessário ou a declarar bloqueio por «ambiente incompleto».

## Por que não refuto
- Número: o ambiente medido pela gerência e por mim coincide; a inferência «nenhum tem tudo» é que não se aplica ao E3.1. Frase > número → a frase muda.
- A lacuna de validação é real: l.182 pede «reproduz o δτ̂₂₂₀ publicado dentro da sua σ» e l.185 aceita «diferença contra o publicado impressa», sem nenhum teste da cola antes do dado real.
  Um wrapper com bug (dict não inserido, sinal invertido, DTau440 ignorado) produz «não reproduz» que a bancada entregaria como parede física. Isso é IMPORTANTE (não bloqueante: a ordem é executável).

## Ajustes à correção proposta pelo revisor (mantidos no texto final abaixo)
- «recuperado dentro de 1σ» é critério que reprova por acaso 32 % das vezes por injeção; substituí por «o valor injetado dentro do IC 90 % do posterior» (e repetição única com outra semente, declarada, se falhar).
- Cada PE completa custa 81–542 CPU-h (l.182); duas injeções a custo pleno triplicam o piloto. A validação da cola pede PE REDUZIDA (SNR alto, nlive reduzido, duração curta, declarados): valida a plumbing, não a cobertura — a cobertura é da E3.3.
- Corrigido «time_domain_source_model» → source model no caminho `frequency_domain_source_model` + `lal_waveform_dictionary` (medido).
