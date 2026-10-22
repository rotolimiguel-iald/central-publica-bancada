## Crítica para a ORDEM_018

**Nenhuma rota apresentada demonstra hoje poder para atingir 5σ global.** A prioridade que proponho é um **estudo local de sensibilidade do ringdown-dephasing nos dados GWOSC residentes**, começando por inventariar eventos independentes e medir poder por injeção e recuperação. Essa é uma prioridade para *avaliar viabilidade*, não uma escolha de sinal vencedor.

Não recebi os seis relatórios nem a fonte local v375 nesta conversa. A correção abaixo incide sobre as conclusões e números descritos no pedido; alegações particulares dos relatórios que não estejam transcritas permanecem **[OPEN]**. Os anexos disponíveis são anteriores e não substituem a v375.

### Correções que devem prevalecer no debate

- **173 hashes distintos não são 173 eventos independentes.** As 102 séries do stack de eco também não são 102 eventos independentes. Nenhuma dessas contagens pode alimentar uma projeção de \(N\), \(p\) ou \(\sigma\) antes da deduplicação por evento.
- **\(0{,}177851389\) é poder condicional do ramo B de dephasing**, não significância observada do eco. No registro de dephasing: 89 eventos, \(z_{\mathrm{vs\,GR}}=1{,}622194321\), \(z_{\mathrm{vs\,B}}=1{,}800045710\), resultado `INCONCLUSIVE_SYSTEMATICS`.
- **Eco:** `power_sigma=2,534380329` de 5 é uma medida de poder no registro informado; \(z_{\rm det}=-2{,}040941700\) e \(z_{\rm excl,1}=4{,}824890438\) têm hipóteses distintas. O `mismatch_max_abs=1,016802435` e `INCONCLUSIVE_SYSTEMATICS` impedem converter o valor próximo de 5 em descoberta ou falsificação.
- **R–B \(0{,}343377425\)** é correção dividida pelo desvio padrão amostral do ensemble. Não é Bayes factor nem teste calibrado. Os fatores **790×/212×**, calculados por escala quadrática desses números sub-sigma, não são estimativas válidas de eventos ou poder.
- **Bonferroni** controla a família de testes mesmo sob dependência arbitrária, desde que os \(p\)-valores individuais sejam válidos. Ele não corrige sistemáticas, seleção posterior dos testes ou uma estatística ainda sem calibração.
- **D1 V3 \(3{,}0124975σ\)** é tensão da previsão fixa \(\beta=\alpha\sqrt e\) frente ao ajuste de \(\beta\) livre. **T11 \(2{,}952854σ\)** é tensão contra a escala de neutrino declarada. Nenhum deles é evidência de 3σ a favor da TGL. V11 `NOT_FALSIFIED_POWERED` tampouco é confirmação.
- **GW250114:** os controles de amplitude/fase e os testes do operador \(B=\sqrt{W^\mathsf TW}\) verificam o pipeline. Suas 410 coordenadas misturam amostras e não constituem 410 observações independentes. Não há fit, posterior, \(p\), \(\sigma\) ou inferência C6; o estado segue `INCONCLUSIVE_SYSTEMATICS`.

### Comparação das rotas

| Rota | Significância observada pertinente | Poder prospectivo com o material descrito | Unidade independente e impedimento principal |
|---|---|---|---|
| **Ringdown-dephasing** | \(z_{\rm vs\,GR}=1{,}622\); \(z_{\rm vs\,B}=1{,}800\), sob sistemáticas inconclusivas | Poder condicional B \(=0{,}17785\); **não** é demonstração de 5σ | Evento astrofísico deduplicado; famílias IMR, calibração e seleção |
| **Eco** | \(z_{\rm det}=-2{,}041\); \(z_{\rm excl,1}=4{,}825\), inelegível como falsificação pelas sistemáticas | `power_sigma=2,534/5`; atraso é [INPUT] | Evento deduplicado, não série; mismatch e modelo de eco |
| **GW250114 atual** | Nenhuma inferência C6 | Desconhecido | Um evento H1/L1; janelas e coordenadas transformadas não ampliam \(N\) |
| **Vazios/shear** | Nenhuma detecção de 5σ apresentada | Fisher full-cov \(2{,}2710\times10^{-6}\); redução de variância exigida \(11.818.412{,}35\) no protocolo | Volume/covariância de levantamento; rota κ-CMB carece de mapa e cálculo próprio |
| **Vazios/κ-CMB** | `INCONCLUSIVE_SYSTEMATICS`; Fisher do piso \(=0\) | SNR esperado \(0{,}4816\), sem poder demonstrado | Mapa, máscaras, covariância e nulos |
| **Cosmologia, inclusive D1/V11** | D1 é tensão **contra** previsão fixa; V11 não falsificada no protocolo | Não demonstrado para 5σ global | Conjuntos de dados e covariâncias comuns; evitar contagem dupla |
| **Neutrinos/T11** | \(2{,}952854σ\) contra a escala declarada | Não demonstrado; JUNO requer estudo próprio | Dados/exposições independentes, backgrounds e escala pré-fixada |
| **NMC-Shapiro** | `AWAITING_DATA`, zero eventos | 21σ apenas projeção sob condições futuras | Eventos ainda inexistentes no teste |

C7, por ter calibração de fonte livre e reprodução não cega, não fornece uma descoberta independente. ORDEM_015 T03 (0/30 células), T04 (sigma inelegível), T05 (condicional sem sistemática) e T12 (zero eventos cegos) também não fecham essa lacuna.

### Experimento mínimo prioritário

**Pergunta:** com o acervo GWOSC já residente, um teste pré-especificado de ringdown-dephasing consegue potência útil para rejeitar **H0: GR com ruído e sistemáticas instrumentais/astrofísicas** em favor de **H1: lei fixa de dephasing da TGL**, em significância **global** de 5σ? Tratar um ramo B ajustável como rival adicional, sem confundi-lo com a previsão fixa.

1. **Congelar protocolo e inventário.** Registrar versão, hashes e parâmetros do teste antes de olhar resultados finais. Ler metadados/manifesto dos 180 arquivos, formar IDs de evento e mapear arquivos, detectores, segmentos e séries para cada ID. Resolver sobreposições e versões: um evento contribui uma vez à estatística conjunta; H1/L1 são medidas correlacionadas do mesmo evento.
2. **Definir observável e estimador.** Especificar exatamente a alteração prevista no ringdown e seu domínio de frequência/tempo, janela, modos, população e eventuais parâmetros fixos ou ajustáveis. Construir uma razão de verossimilhanças ou estatística de score conjunta com covariâncias; calibrar sua distribuição empiricamente, sem presumir que \(\sqrt{\mathrm{TS}}\) seja um \(z\).
3. **Modelar nuisance antes da inferência.** Incluir famílias IMR rivais, massa/spin e seleção de eventos, incerteza de calibração H1/L1, PSD off-source, qualidade de dados, glitches, escolha de janela e modo. Exigir estabilidade sob alternativas de PSD e calibração. O operador \(W\) e a visualização \(B\) podem verificar resíduos, mas não criar graus de liberdade independentes.
4. **Calibrar nulos e recuperação.** Fazer time slides/controles apropriados, simulações GR com ruído realista e injeções de H1 em níveis pré-definidos; executar o mesmo pipeline e seleção em nulos e injeções. Medir taxa de falso positivo, eficiência, incerteza Monte Carlo e sensibilidade à família IMR. Reservar um conjunto cego ou uma etapa prospectiva de confirmação.
5. **Contabilizar busca e poder.** Enumerar todos os ramos efetivamente tentados — eventos, janelas, modos, parâmetros, eco e demais famílias se entrarem na mesma reivindicação. Calibrar diretamente o máximo global nos nulos, ou aplicar correção conservadora a \(p\)-valores válidos. Reportar \(P(\text{rejeitar H0 a 5σ global}\mid\text{H1 fixa})\) com intervalo de incerteza e, separadamente, o poder sob variantes condicionais. Uma extrapolação em \(N\) só cabe após validar a população e a escala por injeções.
6. **Regra de parada.** Encerrar a **avaliação de sensibilidade** quando inventário, cobertura de sistemáticas, nulos e precisão do poder pré-especificados estiverem completos; publicar também resultado sem poder suficiente. Suspender qualquer reivindicação de \(\sigma\) se o nulo não atingir a cauda exigida com precisão adequada, se houver falha de DQ/calibração ou se a conclusão mudar entre famílias IMR. Novos testes escolhidos após ver os dados constituem nova família de trials.

**Handoff para Claude Opus:** redigir a ORDEM_018 como protocolo executável *de leitura e análise derivada*, sem executar `um.py` original nem alterar gate ou fontes. Marcar como **[REAL]** apenas arquivos, contagens e resultados locais efetivamente auditados; **[DERIVED condicional]** fórmulas de poder e projeções dependentes de hipóteses explícitas; **[INPUT]** atraso de eco e constantes/limiares fixados pelo operador; **[DECLARADO]** os seis recibos e alegações dos executores até revisão; **[OPEN]** número de eventos independentes, leitura integral v375, adequação das sistemáticas, calibração da cauda global e poder final. A saída exigida da bancada deve ser um manifesto de eventos deduplicados, especificação congelada da estatística, relatórios de nulos/injeções e tabela de poder com incerteza, terminando em **viável**, **inviável** ou **inconclusivo** para 5σ global — nunca em um sigma fabricado a partir de controles de pipeline.
