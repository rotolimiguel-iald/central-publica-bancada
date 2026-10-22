# ORDEM018 F3 — qualificação local P0–P2 do instrumento sintético

[REAL — medido nesta pasta] P0–P2 concluídos localmente. A segunda revisão passou em **38 controles**. Ela é a candidata final à revisão independente; a primeira permanece intacta como linhagem. **Nenhum PE/P3 foi executado.** Não foram abertos strain, posteriores ou estimativas observadas de D; V1, lista e quatro holds permanecem preservados.

## Autorização e congelamento

A instrução posterior da coordenação autorizou expressamente P0–P2 como cópia local reversível. Ela substitui a exigência rotineira inferida do plano anterior. Não há pendência de confirmação rotineira para esta unidade. P3 continuou expressamente excluído.

Os contratos foram escritos e hasheados antes de cada execução: preflight de versões, hashes de runtime, rodada01 e adendo02. Os launchers recusam divergência de seus próprios hashes/inputs, conservam stdout/stderr/rc e verificam os originais científicos de código depois. A cópia pSEOB e temporal_contract preserva os bytes da bancada; não se executou o original. Execução nativa pelo ambiente existente /opt/lal_env, sem instalação, sem provedor remoto.

Contrato final: CONTRATO_P0_P2_V2.json — 23f9013c5139f5480a18fce103ea802750e020706808b5f52256e5ee478c1415.
Adaptador final: src/synthetic_adapter_v2.py — 31b34a86a9f033b1f395139c7f20154284ede2a6bfe0f9adcb8d7fa312e98fd5.
Recibo final: RUN_002/RESULT.json — 02293a030529b43190b87b7d37940e3969fcf3d977e6c664f244d4969fd251a5.
Diferença da revisão: DIFF_ADAPTER_V2.patch — 281ee5da1a581b9caa22d5ed774e28a9337236954ff33c112fe4662a8022e238.

## O que foi exercitado

- Modelo IMR pSEOBNRv4HM_PA: DTau220 é a única deformação livre; DTau440, DOmega220 e DOmega440 ficam fixos em zero. Harmônicos GR da família permanecem.
- Grade de geração8192Hz/Nyquist4096Hz, restrita aos bins comuns dos dados sintéticos4096Hz; banda20–1024Hz. A chamada efetiva LAL recebeu131073 bins e fmax4096.
- Dicionário LAL novo em cada geração, registrado por identidade de objeto. A sequência GR→RB→GR reproduziu GR bit a bit, erro relativo 0.0.
- Verdade sintética RB calculada de β=ALPHA_FINE_CODATA_2018×sqrt(e), fit GR LAL SEOBNRv4 e lei exata V1. Para SYN_A, chi_f=0.745848186938 e DTau220=-0.424619953898. São valores de simulação, não metadados/centros D.
- PSD analítica LAL e ruído gaussiano de seed fixada; nenhuma PSD medida usada. Casos: GR em ruído zero, GR e RB no mesmo ruído gaussiano sintético. SNR ótimo de rede20 nos três, não SNR de ringdown.
- Normalização do ruído conferida pelo quadrático esperado por bin. Reescala de distância equivale à amplitude direta dentro da tolerância congelada.
- Limites temporais conservadores conferidos nos32 cantos válidos de prior (outros32 excluídos pela restrição de razão de massas já declarada); margem mínima 13.602284551s. Isso não certifica vazamento FFT/tail exato.
- Campos de caminho/evento real, priors livres nos três zeros, geração incorreta, overrides de dicionário e erros silenciosos foram recusados.

A revisão02 acrescentou controles reais para uma lacuna localizada na revisão01: a API de injeção aceitava objetos arbitrários em memória. A final registra a origem e o hash de polarizações produzidas pelo gerador, da PSD analítica, das séries sintéticas, da grade e dos objetos H1/L1. Recusa objetos externos, troca de PSD/ruído, polarizações não geradas sob a verdade indicada e reutilização após injeção. Cada controle adicional foi executado; a diferença de código permanece no patch. O resultado da execução fechada01 não foi promovido a cobertura automática da API02.

## Runtime e isolamento

ENVIRONMENT_PREFLIGHT.json registra LALSuite7.26.15, Bilby2.8.2, NumPy2.5.3, SciPy1.18.1 e Python3.12.3. ENVIRONMENT_NATIVE_HASHES.json pina165 arquivos de código/bibliotecas carregados no ambiente existente; a rodada02 conferiu os165 hashes antes das chamadas nativas. Não houve atualização de pacote.

> [nota operacional do operador — omitida no retrato público]

[OPEN — limite explícito] O hook Python não prova isolamento absoluto contra syscalls nativas não auditadas. A demonstração vale para o código/contrato e os casos executados. Os registros de origem em memória têm vida limitada a este processo; não representam certificação automática de um driver de PE geral.

## Custo efetivamente medido

| Rodada | Controles | Gerações nativas | Wall nativo (s) | CPU filho (s) | Wall filho (s) |
|---|---:|---:|---:|---:|---:|
| RUN_001 | 30 | 6 | 0.344741 | 1.223982 | 1.716213 |
| RUN_002 | 38 | 6 | 0.332953 | 1.269193 | 1.693237 |

Total: 12 gerações nativas, 0.677694s wall nativo, 2.493175s CPU dos filhos e 7.511290s wall dos dois launchers. A contagem de três cenários foi repetida na revisão02: seis construções de injeção, **não seis evidências independentes**. Zero EDOM; rc0 nas duas rodadas; stderr vazio. Preflights de metadados/runtime estão separados e não são custo de fonte/PE.

Esses números medem **geração e construção de injeções**, não uma recuperação de parâmetros. Não medem convergência, viés, cobertura C2, poder D ou custo de analisar14 eventos. Nenhum resultado de natureza ou gate foi alterado.

## Entrega para revisão independente

Revisão atribuída a /root/ordem018_proveniencia. Entradas sugeridas: contrato02 → pins/código e patch → recibos de execução/RESULT → arrays sintéticos e hashes → limite de isolamento e P3 excluído. Todos os arquivos são enumerados em MANIFESTO_PILOTO_SINTETICO.json; contratos/rodadas anteriores continuam presentes. Nenhum passo P3 deve ser inferido desta qualificação local.
