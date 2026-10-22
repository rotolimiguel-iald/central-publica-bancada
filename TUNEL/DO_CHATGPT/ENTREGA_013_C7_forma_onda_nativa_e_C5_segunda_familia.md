[REAL — forma de onda reproduzida; OPEN — evidência integrada e calibração]

# ORDEM 013 — Forma de onda portátil e recuperação da segunda família

Registro: 2026-09-22T08:07:42.169719+00:00. Axiomas: N/A — sem Lean.

**PAGO:** a integral de fase/amplitudes via modos nativos SEOB reproduz a
implementação original em quatro pontos fonte/taxa,2400 componentes por ponto,
erro máximo |ΔlogL|=1.1434362306772528e-05, abaixo de0,001.
Os tempos do teste têm cache aquecido: não são benchmark independente de velocidade.
Cada ponto da nova inferência continua comparado com o gerador COMPLETO original
em três fases externas à malha, sem dispensar os critérios anteriores.

**PAGO:** proposta SEOB usa mapa de remanescente e jacobiano próprios; o aprendizado
Phenom fornece apenas uma distribuição computacional inicial. Não foi usado como
prior físico. As sete coordenadas da fonte, a fase inteira e as amplitudes comuns
continuam integradas. Normalização em32768 amostras:
0.99595461 ±0.015648269; maior desvio dos13
momentos=0.9946938. A eficiência para SEOB ainda não é conhecida.

**PAGO — C7:** pacote standalone `cache/C7_NATIVE_SEOB_WAVEFORM_v1.zip`, 64766bytes,
10arquivos de conteúdo e manifesto. Dispensa memória/contexto da
bancada e dados privados. `prepare_ringdown` gera todos os modos SEOB41;
`polarizations` aplica a leitura condicional explícita, intensidade, distância e
polarização comuns, retornando strain adimensional. Não escolhe relógio físico.
As demais harmônicas ficam preservadas. β vem do cálculo em runtime.

Reprodução real em `python -I -B`:144 comparações passaram,
erro relativo máximo=4.0127806320932996e-16. Três fontes, duas taxas,
quatro leituras condicionais, três intensidades, duas escolhas de distância/rotação.
Seis entradas inválidas foram recusadas. A leitura de estado coerente é recusada
como exponencial completa porque só fornece a inclinação inicial nessa API.

**PAGO:** arquivo ZIP conferido byte a byte contra o pacote testado. Uma cópia
descartável adulterada foi recusada pelo consumidor antes dos imports científicos.
Os originais continuam intactos. Isso é controle de integridade, não aprovação
externa independente da teoria. Resultado do replay:`C7_NATIVE_SEOB_WAVEFORM/cache/replay_20260922_080209_864989/RESULT.json`.

**EM EXECUÇÃO, observado antes deste registro:**
- IMRPhenomXPHM:sessão62818, 2928/8554avaliações no suporte, `cache/source_evidence/phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384`.
- SEOBNRv4HM:sessão61984, 320/1024avaliações no suporte, `cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048`.

Não há resultado final dessas rodadas. A primeira integra16384 propostas; a
segunda é piloto2048. Propostas fora do suporte têm integrando zero e continuam
no denominador. Os50 intervalos de ruído são reutilizados/pareados; não são1200
eventos independentes.

**NÃO PAGO:** convergência/replicação das duas famílias, viés/cobertura da intensidade
contínua, demais leituras/SNR e aceitação científica dos fatores de Bayes. Os
controles prévios de alta SNR continuam falhando; a entrega portátil não os apaga.
Dados/C6/cânone preservados. Nenhuma declaração de confirmação ou5σ.

**PRÓXIMA AÇÃO:** revalidar os dois handles acima. Só após RESULT, executar
`audit_registered_transport.py <nome_da_rodada> --stage <fase>`; a fase é
`phase_ringdown_balanced` ou `phase_native_seob`. `audit_phase_source.py
../<fase>/<nome_da_rodada> --rate --processes 2` usa o gerador original para
controle independente de taxa (SEOB é mais caro). Comparação de Phenom contra
8192 em `compare_phase_runs.py`; não comparar famílias como se fossem repetições
do mesmo estimador. Repetições por seed da mesma família permanecem necessárias.

Comandos da etapa: `run_native_seob_source.py register`, `oracle`, `run --draws
2048 --seed 130901 --processes 2`. Artefatos concluídos são create-once; reproduzir
em cópia separada, nunca sobrescrever resultados. Pacote: `python -I -B
C7_NATIVE_SEOB_WAVEFORM/reproduce.py` cria diretório de replay próprio.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
| record_native_package_and_seob_start.py | 4eb23cc51cae962337d5a3fbf306178fea21e53d909cef32e5873efb2def2050 |
| build_native_waveform_package.py | 456643f2582fbaa20da5f6b6e1f4015f8f3ef8f8ffa8ce4d2069e494865ced72 |
| verify_native_package_integrity.py | 9747c5688e21ff0f9a290dc0de2aee0c68ada94f25b7afd87a180070fc1ff372 |
| C7_NATIVE_SEOB_WAVEFORM_PACKAGE.json | 9e68a2d2f4153c29d99a2bfbef3e9de2c8df7f25cd29b8ad83676e570d57b08c |
| C7_NATIVE_SEOB_INTEGRITY_VALIDATION.json | 3fb3c27c6671e66247a439ca6a8e437606dd4a5a4c09e168fb08a7a56b12e51d |
| C7_NATIVE_SEOB_REPLAY_VALIDATION.json | 054937a524d8a7187d661130b29d148c20903c59e6af8181283353d8f47f3288 |
| C7_NATIVE_SEOB_WAVEFORM/cache/replay_20260922_080209_864989/RESULT.json | 8262b938587c554916130fc337132fd9012541a6c7f8ad5e2516de534dd5982d |
| cache/C7_NATIVE_SEOB_WAVEFORM_v1.zip | a368ae336532096297ceb4a7a9554dbb13dc648b8024f770b94183433a1eb09d |
| C7_NATIVE_SEOB_WAVEFORM/MANIFEST.json | a8d8ab561d1b96f3826a89b458943efafdd51a092e712c2c1bdbde8036721913 |
| cache/source_evidence/native_seob_source_likelihood.py | 942000641f1c1f096319857b340357a1606df3e4b040be32e6a67e30c13a345d |
| cache/source_evidence/validate_native_source_integral.py | 2b1906606c2a037c9647a3bce182111368f61ec5c791f69b9867b3e389f80818 |
| cache/source_evidence/run_native_seob_source.py | 8255927ce5991fbad1d3817105daeba703250a0edf5a3f964d72636b5e28e7e4 |
| cache/source_evidence/native_source_integral_validation/REGISTRATION.json | 0a45412c4283b5bbac84859d0d8ebc6447234880c6e30f495ac5e0d778d77775 |
| cache/source_evidence/native_source_integral_validation/RESULT.json | e1caf33c4878a99fea1c27a1450b4c2528afc8b677fb35e7a370cb10eb32b830 |
| cache/source_evidence/phase_native_seob/REGISTRATION.json | b6ef3665b895959ecd8480434170c373bff16a7cc6502c2eb21bb1ee87acb69b |
| cache/source_evidence/phase_native_seob/PROPOSAL.json | efd8f63d0b7a7215b7f42d01a9c682cbaa69fc9fdf490eac110d5881d6da1763 |
| cache/source_evidence/phase_native_seob/PROPOSAL_ORACLE.json | d01b269df9d50f7524b41149fd58b22abd856cf9df8b7b6ac1dfda81074faf0a |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/START.json | c68bc077955892d62533db56bb01c88b645894e90c20fa31713a81fb6cc86cd5 |
| cache/source_evidence/phase_native_seob/SEOBNRv4HM_seed130901_N2048/PROPOSALS.npz | 29df29259777dac8cab89082f85ba771bb3d1a6dfd22820808dd4f1f278183d9 |
