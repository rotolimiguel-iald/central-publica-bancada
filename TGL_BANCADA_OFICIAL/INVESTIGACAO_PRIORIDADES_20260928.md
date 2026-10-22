# Investigação da bancada TGL — 28/09/2026

**Resultado:** a bancada facilita uma investigação conjunta com agentes, e isso foi medido em execução. A rodada identificou uma comparação sem sensibilidade por construção no ensaio ACT, quantificou a degenerescência do fundo BAO e conferiu a degenerescência de um único modo de ringdown. Não produziu nova significância física nem alterou o kernel ou o gate.

## 1. O ganho real do sistema

[REAL — HTTP e contadores do processo] O serviço GW manteve **180/180 arquivos, 22,50550 GiB de arrays próprios**, mesmo identificador de carga e geração, swap zero. Seis consultas de uma série, incluindo os 16.777.216 pontos de sua janela integral, responderam em **31–80 ms**, mediana 36,36 ms. O contador permaneceu em 900 leituras numéricas: **zero releituras de dados**. Isso mede navegação nessa série, não concorrência, ajuste completo ou carga inicial.

O executor cosmológico respondeu a **21 cenários** sobre o vetor BAO com 13 observações, sete redshifts e covariância 13×13. Cursor/escala em cache levou aproximadamente 3,6–4,4 ms e novos fundos 27–47 ms. Os dados carregados desse executor são os produtos comprimidos BAO; não são todos os catálogos DESI nem os mapas CMB.

Os agentes puderam consultar as APIs e registrar parâmetros, previsões, covariâncias e fontes usadas pela interface. Eu conferi os resultados por métodos independentes: eliminação gaussiana para os 21 recibos BAO; custódia de 29 fontes e inversão de Q por bisseção no ringdown; conferência de sete blocos de resultados e dos trechos originais do ensaio ACT. Os três recibos de revisão deram PASS, **dentro desses escopos**.

O catálogo geral contém 1.350 arquivos, aproximadamente 72 GiB, incluindo cópias e resultados históricos. Contagem de arquivos não mede observações independentes. A cobertura de leitores por formato também não demonstra que todos os esquemas e likelihoods estão integrados. O índice de domínios ainda informa cosmologia não implementada, apesar do executor separado em :18766 estar funcional: há uma inconsistência de integração a corrigir em entrega própria, sem interromper a RAM de GW agora.

A GPU atende à visualização WebGL; não medimos cálculo científico executado na GPU. A RAM compartilhada pelo servidor evita releitura, mas os agentes recebem consultas e resultados delimitados — os 22,5 GiB não entram integralmente no contexto de cada IA.

## 2. Onde concentrar a investigação

Esta é uma **ordem operacional fundamentada**, não uma estimativa numérica da probabilidade de descobrir a TGL.

| Rota | Achado conferido | Próxima investigação útil |
|---|---|---|
| **D10 — CMB–BAO acústico** | No fundo BAO residente, mudanças de escala e densidade absorvem quase toda a diferença estudada. | Confrontar conjuntamente as relações entre distâncias, escala acústica e espectros, com o modelo perturbativo canônico integrado e rivais explícitos. Continua a prioridade estratégica pedida pelo operador. |
| **Vazios + lenteamento ACT** | A comparação usada no Fisher V9 aplica o piso a um perfil que nunca o alcança. | Auditar em cópia a sensibilidade do ensaio, antes de atribuir Fisher zero exclusivamente ao ruído. É o reparo metodológico imediato mais concreto desta rodada. |
| **Ringdown multimodo** | Um único modo amortecido pode ser reproduzido por outra massa e outro spin de GR. | Medir a componente adicional dos modos 220+440 com massa e spin comuns, amplitude observável e ruído real. É o piloto mais próximo do banco já residente. |
| **Neutrinos** | Há uma previsão condicionada à normalização e à hierarquia; o recibo registra tensão, não detecção. | Rever essas condições e a independência das determinações, preparando confronto prospectivo. Custo computacional pequeno. |

### 2.1 BAO: a diferença visível é largamente compensável

[REAL — diagnóstico entre modelos] No cenário de referência H₀=67,4, Ωm=0,315 e r_d=147,09 Mpc, a distância quadrática entre a previsão fixa da TGL e a previsão com β=0 é:

\[
d^2=\Delta\mu^T C^{-1}\Delta\mu=0,55873894.
\]

Um exemplo com β=0, Ωm=0,3184750793 e r_d=146,9684221 Mpc reduz essa distância a **0,00473259**, absorvendo **99,153% da distância quadrática**. É uma comparação entre previsões, não um ajuste global aos dados, uma fração de sinal físico removido ou uma significância.

Com todos os parâmetros fixados, χ² passa de 28,69347 para 26,08025. Essa melhora de 2,61322 não é Z nem prova de preferência depois de ajustar os modelos. Os maiores desvios brutos do conjunto estudado aparecem no redshift 2,33; 0,934 também é relevante na métrica da covariância. Isso não estabelece o melhor redshift global.

O fundo V3 usado inclui Λ na rota total, com a condição de contorno e a normalização documentadas no executor. No recorte testado, r_d é uma entrada; não calculamos Cℓ nem uma likelihood CMB. A lacuna aqui é da **ligação ao executor e aos dados desta bancada**; esta auditoria não conclui que as derivações correspondentes estejam ausentes do acervo.

Próxima unidade: localizar e congelar a tradução canônica para as perturbações e o cálculo de r_d, confrontar limites e precisão, e então ligar as likelihoods. Relatar separadamente previsão fixa, β livre, compatibilidade entre eles e poder contra cada rival. Dados D9/D10/Planck reaproveitados entram uma vez no modelo conjunto. A necessidade de covariância de sobreposição também é explícita na [análise DESI de Full Shape DR1 + BAO DR2](https://arxiv.org/abs/2602.18761); disponibilidade dessa análise não significa integração local concluída.

### 2.2 ACT: o Fisher zero tem uma causa anterior ao ruído

[REAL — fonte conferida] Em `Nós/um.py`, linhas 149404–149454 da fonte identificada por hash no recibo, o modelo utiliza:

\[
f(r)=1+\delta_c\frac{1-(r/s_1)^2}{1+r^6},\qquad
\delta(r)=\max(f(r),r_\star)-1.
\]

A comparação do Fisher fixa δc=−0,95 e s₁=1 e troca somente r⋆=0 por r⋆=β. Para 0≤r≤1, a fração está entre 0 e 1, logo f(r)≥0,05; para r≥1, f(r)≥1. Como **β=α_CODATA√e<0,05**, os dois recortes são iguais para todo r≥0. A projeção e o filtro seguintes recebem exatamente o mesmo perfil. Portanto:

\[
\mu_{\beta}=\mu_0\quad\Longrightarrow\quad F=0
\]

nesse ensaio, qualquer que seja a precisão dos dados. Um controle em 10.001 pontos confirmou diferença zero; a troca diagnóstica para δc=−1 ativou o piso, produzindo diferença positiva. **Esse controle não é uma escolha física validada, um novo ajuste ou uma demonstração de sensibilidade do ACT.**

O resultado histórico `UNDERPOWERED` permanece registrado, mas a explicação de sua origem precisa dessa correção ao lado. A grade posterior de perfil não usa apenas δc=−0,95; o achado não autoriza chamar toda a análise ACT de insensível.

Há outras qualificações antes de inferência: variâncias diagonais não substituem a covariância completa entre bins; recentrar as próprias rotações e verificar a média nula não é validação independente; SNR de detecção do vazio não é poder de distinguir o piso TGL. O diagnóstico rotulado `detection_sigma_raw` usa √max(χ²−N,0), não Z global calibrado.

Próxima unidade: reutilizar o código em cópia, congelar uma família fisicamente admissível que permita testar o piso, verificar a diferença depois de filtros e ajuste dos perfis, construir a covariância e validar com nulos independentes e injeções. Se a diferença continuar indistinguível, registrar isso. Não escolher perfis depois de olhar o resultado mais favorável.

O rito SDSS/VAST V11 já registra `NOT_FALSIFIED_POWERED`: 438 vazios, piso calibrado de traçador 0,12693±0,01363. É um teste unilateral condicionado à relação traçador–matéria, não medição do piso de matéria nem discriminação automática de ΛCDM. Vale incorporá-lo à interface com seus controles existentes.

### 2.3 Ringdown: vários modos do mesmo remanescente

[DERIVED — modelo de ensemble explicitado] No modo único,

\[
\tau_{\rm eff}^{-1}=\tau_{\rm GR}^{-1}+\Gamma,
\qquad
\frac{\tau_{\rm eff}}{\tau_{\rm GR}}-1=-\frac{x}{1+x},
\quad x=\Gamma\tau_{\rm GR}.
\]

No relógio R-B, o exemplo massa fonte 65 M☉, spin 0,7 e z=0,1 dá x=0,0211559. A frequência e o amortecimento do modo podem ser reproduzidos por GR com massa fonte aproximadamente 64,16615 M☉ e spin 0,683526. No exemplo spin 0,95, o efeito relativo é maior, mas continua compensável por outro par massa–spin. Massa menor elevou a frequência sem elevar x no controle R-B estudado.

Essa equivalência foi conferida na aproximação BCW do modelo exploratório. Não deve ser extrapolada automaticamente a uma reconstrução IMR completa. Mostra por que aumentar a deformação visível não basta para tornar o modelo distinguível.

[REAL — resultados existentes, sem novo fit] C6/GW250114 permanece **INCONCLUSIVE_SYSTEMATICS**, com ln B(R-B/GR)=−0,002595 no caso primário. O requisito de calibração com duas famílias IMR não foi satisfeito. As limitações de ruído C6 e a recusa de condicionamento H1 na rota T10/T15 são diagnósticos diferentes e continuam registrados.

Próxima unidade: reutilizar QNM_GRID e os operadores C6, comparar 220 com 220+440 na métrica do ruído, impor **a mesma massa e o mesmo spin** e projetar as direções livres de amplitude/fase. Reportar valores singulares e diferença residual. Exigir informação real do 440: colocar um modo sem amplitude informativa no modelo não cria sensibilidade. A [análise LVK de GW250114](https://arxiv.org/abs/2509.08099) distingue os modos requeridos no pós-merger das restrições ao 440 obtidas na análise IMR completa; não tomar estas últimas como detecção isolada de 440 no ringdown.

Há também uma escolha de observável: o amortecimento exp(−Γt) é do ensemble; uma realização de difusão de fase exige seu estimador próprio. O painel visual ainda não resolve essa tradução física. R-A, R-B e tempo global devem permanecer hipóteses identificadas, sem selecionar a favorável após observar os dados.

### 2.4 Rotas secundárias

- **Neutrinos:** o recibo m₂ utiliza β·sin(45°)·1 eV, com a escala 1 eV marcada como normalização e condições sobre m₁/hierarquia. A tensão global registrada é aproximadamente 2,95σ; a revisão atual conferiu o recibo, não revalidou externamente todas as medidas. JUNO e um ajuste global que incorpora JUNO não são confirmações independentes.
- **Ecos:** as recuperações históricas de injeções nulas e positivas não distinguem adequadamente os casos em partes da pipeline. Um proxy de poder de 4,4 não é detecção observada e não autoriza empilhar sigmas. Qualificar o estimador precede nova campanha.
- **Relógios:** o protocolo P1 com t_P tem sensibilidade prevista aproximadamente 12,46 ordens aquém da meta, sob sua ponte física condicionada. Baixa prioridade para detecção direta com esse ensaio atual.

## 3. Regra comum de pesquisa com agentes

Para priorização local, com covariância positiva definida fixa C, W tal que WᵀW=C⁻¹ e Jacobiana de nuisance J, usar:

\[
A=WJ,\qquad P_\perp=I-AA^+,\qquad
\eta=\|P_\perp W(\mu_{\rm TGL}-\mu_{\rm rival})\|^2.
\]

[DERIVED — aproximação local] A pseudoinversa e os valores singulares mostram que parte da diferença não é absorvida localmente pelos parâmetros livres. **η não é Z global.** Ajuste não linear, covariância dependente de parâmetros, escolhas de alvo e sistemáticas requerem análise adicional. A estatística final compara likelihoods ajustadas e é calibrada sob cada rival; a hipótese TGL fixa e a alternativa β livre são análises distintas.

O fluxo útil é: agente consulta domínio residente → registra cenário e linhagem → mede diferença identificável → coordenação confere controle → apenas candidatos informativos recebem ajuste e simulação mais caros. Congelar a seleção ou reproduzi-la nas simulações; separar exploração e avaliação por identidades e proveniência, sem presumir dados ainda cegos depois de buscas históricas.

**Participação nesta rodada:** três agentes locais concluíram BAO, GW/ecos e outros domínios. MiMo concluiu um parecer pela fila existente. A chamada Kimi falhou sem resposta aceita e não foi repetida. Nenhuma contribuição de Claude ou DeepSeek foi produzida nesta rodada.

O parecer MiMo foi preservado integralmente e recebeu revisão: corrigimos o projetor após branqueamento, δτ exato, a confusão entre cobertura de 1σ e 95%, e a insuficiência de 10⁴ nulos para medir uma cauda de 5σ. Seus cortes de correlação, falso alarme e poder são sugestões sem calibração, não critérios adotados. O documento `MIMO_REVISAO_COORDENACAO.md` detalha as correções. Parecer de provedor não substitui medição independente.

## 4. Entrega e limite da rodada

Foram usados os motores e recibos existentes. Não houve novo ajuste GW, nova inferência ACT, MCMC cosmológico completo, reinício de serviço, mudança de interface, original científico, kernel ou gate. A bancada residente continuou disponível.

**Recomendação final:** prosseguir com D10 como rota acústica principal, resolver primeiro a sensibilidade estrutural do ensaio ACT em cópia e executar o diagnóstico multimodo qualificado na infraestrutura GW existente. A próxima decisão deve vir da diferença identificável e da recuperação de sinais conhecidos. Nenhuma rota recebeu nesta rodada demonstração de poder de 5σ global.

**Evidências locais:** [pasta da investigação](state/investigation_20260928/), [medição do sistema](state/investigation_20260928/system_measurement.json), [revisão BAO](state/investigation_20260928/bao_independent_review.json), [revisão GW](state/investigation_20260928/gw_independent_review.json), [revisão ACT/outros domínios](state/investigation_20260928/other_domains_independent_review.json). O manifesto de entrega calcula hashes dos arquivos por script; números não são transcritos como novos selos científicos.
