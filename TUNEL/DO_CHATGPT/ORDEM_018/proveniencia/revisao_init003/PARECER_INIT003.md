# Revisão independente — P3 INIT_QUALIFIED_003

[REAL — revisão estática e de integridade, 06/10/2026] **Nenhum novo achado acionável no delta examinado.** O INIT003 preserva a ciência e os limites do CODEC002 e integra a factory B já qualificada, com exceção de leitura ASD exata e verificação da PSD antes/depois da GWT. A preparação está apta a subsidiar decisão específica da coordenação; esta revisão não concede execução.

Foram concluídas **179 verificações estáticas/de integridade**, registradas em RECIBO_REVISAO_INIT003.json: 30 arquivos do manifesto, 26 entradas do contrato, 15 cópias exatas, 21 campos científicos invariantes, novos IDs, hashes dos recibos465 e leitura AST da cadeia de assinatura. São 71 fontes locais registradas. Não executei/importei driver, supervisor, controle ou source; não iniciei WSL, waveform, likelihood, sampler, rede/provedor ou acesso a D. O NPZ sintético foi lido somente como bytes para hash.

## Pins e proveniência

| Artefato | Bytes | SHA256 medido |
|---|---:|---|
| MANIFESTO_PACOTE_INIT003.json | 10082 | a4f085fdace4759ae9839c4ae1b52abf113309bc58e6761b2167f04ad3bc2b6b |
| CONTRATO_P3.json | 21134 | b4d570c60a5a9bdad6c0e9682f817f51b838698e7779320fd9572244df6c2b36 |
| driver_p3.py | 13830 | 265fd07e4c39a239ac79ab1598bd4808d310d63e0a52abbd2bccd8ba8fc94af6 |
| launch_p3.py | 3766 | c3876b1d5350662537fc6139558e8522fd73e440fc8c318e789c4deb67228aa5 |
| init_detectors.py | 4261 | 95dfef3df297d981a1a56fda4e617a0595768c98bee96979dfc208db55dd8890 |

O manifesto465 e seus14 artefatos foram relidos e conferidos. O recibo externo registra uma tentativa, exit0, supervisor4696/filho4697, ambos os rótulos, zero source/waveform/likelihood/sampler, nenhuma operação bloqueada e ausência de permissão P3. Isso sustenta a qualificação anterior de inicialização; não foi repetido o controle nem promovido a evidência de PE.

O recibo do autor VERIFICACAO_RUNTIME_INIT003.json contém1.165 verificações aprovadas (runtime1.162+interpretador+codec+ASD); confrontei os valores registrados com os pins correspondentes. Não refiz a leitura da instalação WSL. O fato medido nesta revisão é a integridade/coerência desse recibo, distinguindo-o de uma nova verificação do runtime.

## Delta efetivo

Os diffs completos do driver e contrato foram regenerados textualmente a partir dos arquivos lidos e coincidem com os patches entregues. Não foram aplicados ou executados.

O único caminho de dados adicionais de runtime é /opt/lal_env/lib/python3.12/site-packages/bilby/gw/detector/noise_curves/aLIGO_O4_high_asd.txt, com bytes/hash fixos. O snapshot local é proveniência, não a PSD final. Helper/geometria/pin de dependência são byte a byte os examinados em457 e usados em465.

No driver, linhas79–82 adicionam helper/metadados e caminho exato. A chamada build_B ocorre na linha115. O helper confere arquivo/origem, recusa sombra local e substitui a PSD default por um objeto novo com arrays analíticos do NPZ. A verificação antes de GWT e a igualdade do strain armazenado aparecem nas linhas125–127; a mesma verificação nos interferômetros da likelihood e igualdade antes/depois estão nas linhas135–137. O resultado acrescenta os estados de inicialização e seus hashes, linhas190–193. Não concede diretório ou regenera PSD.

Os21 campos enumerados por COMPARACAO_ESCOPO.json são iguais ao CODEC002; a errata473 corrige a antiga contagem22. Jobs diferem somente no id: rótulos, verdades sintéticas, seeds e normalizações permanecem iguais. Supervisor, prior_transform, source, adapter, contrato temporal, FailureAudit, configuração e codec permanecem byte a byte iguais. Assim são preservados priors/normalização de massas, grade, DTau220 livre, os outros três desvios nulos, nova dictLAL por waveform, limite10000 e demais escolhas científicas anteriores. Não se deriva uma nova lei ou mudança de hipótese deste reparo.

## Assinatura e ausência de bloqueios do controle

O adapter imutável vincula synthetic_only220 original ao WaveformGenerator. O construtor da fonte Bilby pinada atribui frequency_domain_source_model e depois infere source_parameter_keys (linhas65–67). No novo driver, generator(cfg) vem na linha129; apenas depois o wrapper FailureAudit é atribuído à callable efetiva, linhas130–131. A classe examinada não apresenta descriptor dessa propriedade que refaça a inferência.

O wrapper já revisado usa wraps, conserva args/kwargs e propaga exceções/None com a classificação específica; não converte falha de domínio em rejeição de prior. Não há shim __signature__, guard “zero chamadas”, substituição de métodos WFG/GWT ou bloqueio de sampler copiado de control_init.py. O helper contém alternativa A como código preservado, mas o driver chama B uma única vez. O reparo não traz os bloqueios próprios da unidade de inicialização para a PE proposta.

## Identidades, claims e limites reais

Novas identidades: P3_GR_INIT_QUALIFIED_003 e P3_RB_INIT_QUALIFIED_003; saída EXECUTION_INIT_QUALIFIED_003. Não coincidem com V2/CODEC002. No instante da revisão, não existiam diretório dessa campanha, autorização ou CLAIM no pacote. Os pins do contrato e recibo terminal CODEC002 foram reconferidos; nenhuma unidade antiga foi reaberta. A identidade nova, por si só, não autoriza ciência repetida.

launch_p3.py exige autorização correspondente a ação/contrato/lista exata de jobs e reserva diretório por mkdir(exist_ok=False). Em sequência, cria CLAIM específico e inicia o filho; falha/incerteza interrompe o restante. O driver exige CLAIM exato e recusa RESULT/CHILD_STARTED prévios. Não existe resume/fallback.

A checagem de orçamento antecede e incrementa toda avaliação da likelihood, inclusive as chamadas de inicialização do NestedSampler: linhas103–106 e138–149. O maxcall do Dynesty é adicional; o contador externo fixa10000 por job. CPU3300/3305s, memória8GiB, um worker/thread e jobs seriados permanecem iguais.

**Limite operacional herdado, explicitado:** o supervisor aplica timeout3610s à espera inicial de cada filho. Depois de SIGKILL usa p.wait() sem timeout (launch_p3.py44). Os7220s são soma das esperas nominais, não teto OS absoluto de campanha/cleanup/IO. O preparo/pins do parent também não estão dentro dessas esperas. Este comportamento é anterior e não foi modificado nesta revisão delimitada; não anunciar garantia irrestrita de encerramento dentro de7220s. Ausência de recibo/identidade incerta exige reconciliação, nunca retry.

## Aceite restrito

[DERIVED] Nenhuma regressão estática ou diferença científica indevida foi localizada no delta. [OPEN] O INIT003 ainda não executou Dynesty, avaliou o prior, demonstrou convergência/recuperação, mediu custo de PE ou cobertura. Dois alvos de ruído pareado não são dois modelos rivais, nem permitem interpretar seus logZ como BF entre datasets. A qualificação465 se limita à inicialização.

O hook continua posterior a imports/pins fixos e não é confinamento OS/nativo. A revisão preserva V1, holds, D e pacotes anteriores. Cabe à coordenação uma decisão específica para eventual lançamento único; esta nota e o manifesto de revisão não são autorização.
