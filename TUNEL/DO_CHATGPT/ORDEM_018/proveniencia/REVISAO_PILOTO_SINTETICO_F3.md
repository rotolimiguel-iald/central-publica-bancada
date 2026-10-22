# Revisão independente F3 — piloto sintético P0–P2

[REAL — auditoria local] **Nenhum achado bloqueante no recorte congelado P0–P2.** Uma errata documental P3 foi identificada e resolvida ao lado, preservando contratos, código e rodadas. A revisão aceita a qualificação de fonte e construção de injeções nos casos exercitados. **P3/PE, recuperação, cobertura, viés e poder do conjunto D permanecem OPEN e não foram executados.**

## Achado e resolução

**F3-01 — P3, resolvido.** O campo `read_allowlist_policy` do contrato02 dizia `writes RUN_001 only`; `run_id`, a expressão `run=ROOT/contract["run_id"]`, o hook e os caminhos registrados usam RUN_002. A [errata documental](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico/ERRATA_ALLOWLIST_RUN002.json>) corrige a frase, mantém os hashes e não produz nova execução. A identidade do contrato, script e RESULT citados na errata foi reconferida. Nenhum código do autor foi modificado nesta revisão.

A abertura da API01 para objetos arbitrários em memória havia sido detectada pelo autor. A revisão02 acrescenta registro da origem/truth/hash das polarizações, identidade e estado dos IFOs, PSD, grade e ruído; rejeita troca desses objetos e reinjeção nos controles registrados. Isso foi conferido no [delta V2](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico/DIFF_ADAPTER_V2.patch>) e no [adaptador final](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico/src/synthetic_adapter_v2.py:18>). A execução01 preservada não é usada como prova automática da API02.

## Evidência conferida

O script independente `review_synthetic_f3.py` executou **212 conferências**, todas aprovadas, em **44 arquivos**: pins do manifesto, contratos, launchers, inputs, logs/recibos, fontes originais e cópias, V1 por bytes, resultados e arrays estritamente sintéticos. Leitura `numpy.load(..., allow_pickle=False)`; nenhum módulo do autor importado ou executado. Uma segunda leitura independente por biblioteca padrão conferiu os **165 arquivos de runtime** pinados em `/opt/lal_env/lib/`: todos os hashes e tamanhos coincidem. Ambos os recibos estão ao lado desta nota em JSON.

| Escopo | RUN_001 | RUN_002 |
|---|---:|---:|
| Controles registrados aprovados | 30 | 38 |
| Gerações nativas registradas | 6 | 6 |
| rc do processo | 0 | 0 |
| EDOM / PE | 0 / 0 | 0 / 0 |
| stderr | vazio | vazio |

São **12 gerações no total**, sob teto agregado32; segunda rodada tinha saldo26. Os contratos precedem os horários registrados de início, os launchers conferem seus próprios pins e inputs antes do processo, e stdout/rc/RESULT concordam. O limite e os hashes foram conferidos no disco; não são apenas frases da nota. As seis construções de injeção das duas revisões correspondem a **três casos distintos** repetidos, com os mesmos arrays. Os controles registrados não são 38 realizações estatísticas independentes.

**Fonte e grade [REAL documental/processual].** A família é IMR `pSEOBNRv4HM_PA`; somente DTau220 se deforma. DTau440, DOmega220 e DOmega440 são zeros nas validações, nos dicionários lidos e nas 12 entradas de trace. “Só-220” se refere à deformação livre; os demais harmônicos GR da família continuam presentes. A [fonte copiada](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico/src/pseob_source.py:101>) cria `lal.CreateDict()` a cada geração. O guard da [qualificação](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico/qualify_synthetic_v2.py:128>) inspeciona o dicionário entregue à chamada e a grade:8192Hz de geração, Nyquist4096Hz,131073 bins. Dados sintéticos4096Hz,65537 bins, passo0,03125Hz; banda20–1024Hz com32129 bins. Os hashes das cópias pSEOB/temporal e seus originais coincidem.

**GR→RB→GR [REAL no recibo conferido].** O trace é 0 → −0,42461995389788576 → 0 em DTau220; o controle registra retorno GR bit a bit, erro relativo0. O segundo fixture usa −0,5421017699312789. A aritmética beta=ALPHA_FINE_CODATA_2018×sqrt(e), k, F, Q e −x/(1+x) foi refeita localmente a partir do spin sintético registrado e coincide. O fit remanescente e os espectros nativos não foram recalculados pelo revisor: sua proveniência é código pinado + guard + trace + recibo de processo. Não há nova observação natural aqui. A diferença relativa RB/GR e a repetibilidade são controles de implementação, não detecção da TGL.

**Arrays e normalização [REAL independente].** Cada NPZ tem14 arrays, sem objetos serializados. Hashes de PSD, ruído e sinal coincidem. A soma independente `noise + signal` reconstrói **exatamente os 12 hashes de strain injetado** dos recibos. `sqrt((4/T) Σ_det,bin |signal|²/PSD)` dá20 nos três casos de cada rodada. É SNR ótimo de rede do IMR completo, não SNR exclusivo de ringdown. PSD tem unidades strain²/Hz, coeficientes de Fourier strain·s; `df=1/T`. A PSD é analítica no código pinado, positiva e finita na banda e infinita fora. A revisão não importou LAL para gerar uma segunda PSD.

O ruído gaussiano tem quadráticos H1=64401,02866412935 e L1=64082,783819217395 para64258 graus de liberdade, z=0,39897389673 e −0,48875994782. O caso zero contém zeros; H1/L1 não são arrays iguais; GR/RB usam os mesmos ruídos emparelhados. Isso confere a normalização desta realização; não estabelece cobertura ou independência estatística a partir de uma única seed. Os dois NPZ são idênticos por hash. A distância foi reescalada para o mesmo SNR por projeto: esse procedimento de simulação não é ajuste de beta a dados D.

## Entrada, isolamento e limites

> [nota operacional do operador — omitida no retrato público]

[OPEN — alcance explícito] O hook é instalado **depois** de imports/leituras fixas de piloto/runtime e abertura do log EDOM; a lista de operações não é uma captura completa do sistema operacional. Não prova ausência universal de syscall nativa não auditada. Os165 pins reforçam identidade do runtime enumerado, sem transformar esse conjunto em auditoria de toda dependência transitiva do SO. Registros Python em memória não resistem a código arbitrário malicioso, e seu ciclo de vida não certifica um driver geral de PE. Esses limites já constam da [nota do autor](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/preregistros/conjunto_d/piloto_sintetico/NOTA_QUALIFICACAO_P0_P2.md:35>) e permanecem nesta aprovação restrita.

[REAL/OPEN] O teste temporal cobre32 cantos físicos do prior, com outros32 excluídos por razão de massas e margem mínima13,602284550666809s. Não é varredura/prova de todos os pontos interiores, vazamento FFT ou tail exato. Dois progenitores sintéticos, três cenários e uma seed não constituem campanha de recuperação, sistemáticas, viés ou cobertura. Não há significância observada, separação D ou potência de teste medida. O custo de geração não estima o custo de PE de14 eventos.

[REAL — preservação] O V1 foi apenas hasheado e comparado à auditoria anterior: bytes e SHA coincidem. Nenhum strain, posterior, centro observado, lista ou hold foi aberto para novo exame. Fontes/rodadas do autor e originais científicos ficaram read-only; todas as saídas desta revisão ficam em `proveniencia`. Zero nova geração nativa, zero PE e zero provedor remoto pelo revisor.

## Identidades finais

| Artefato | SHA256 lido por script |
|---|---|
| Manifesto final do piloto | `87bcef2f93a1f1ecd8e153229ab704b6f4696e5d5922bfc6f316c8f2f2ee6d72` |
| Contrato02 | `23f9013c5139f5480a18fce103ea802750e020706808b5f52256e5ee478c1415` |
| Adaptador02 | `31b34a86a9f033b1f395139c7f20154284ede2a6bfe0f9adcb8d7fa312e98fd5` |
| RESULT02 | `02293a030529b43190b87b7d37940e3969fcf3d977e6c664f244d4969fd251a5` |
| Arrays02 | `a54e8b4af0b63343910d8702f197a10c2ee4b6b2f7662aeb39082680f007020b` |
| Errata ao lado | `e10edcbe874f8ca9f5e843165eb9cdfd16b5147a72ab4c2083962149f5653187` |

Os hashes completos, tamanhos, trechos com linhas,212 resultados e inventário de chamadas estão em `REVISAO_PILOTO_SINTETICO_F3.json`; os165 hashes de runtime lidos novamente em `REVISAO_PILOTO_SINTETICO_F3_RUNTIME.json`. Esta revisão encerra a verificação de P0–P2 no recorte fixado; não autoriza P3 nem muda gate ou estatuto físico.
