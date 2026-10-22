# Universo residente TGL — plano de execução

Data: 27/09/2026. Origem: correção expressa do operador. Casa: bancada própria em TETELESTAI; espelho de desenvolvimento na Central. Estatuto: plano de engenharia, com primeiras unidades em implementação.

## Experiência que define o produto

Ao escolher um domínio, o pesquisador carrega o conjunto científico completo desse domínio em RAM. O sistema informa o que entrou, o que foi recusado, consumo real de memória e as unidades. A partir daí, navegar no tempo ou variar parâmetros usa esses arrays residentes. A interface sincroniza observação, previsão TGL, referência rival, resíduos e controles. Renderização usa produtos de resolução apropriada à tela; o cálculo conserva acesso ao conjunto integral. O objetivo é investigar sinais e regimes distinguíveis nos dados reais.

O produto anterior era um explorador de arquivos e amostras. Ele permanece como ferramenta auxiliar de inspeção e proveniência. A página principal nova é `/universe` e o atalho TGL passa a abri-la.

## Domínios e fontes

| Domínio | Dados a reunir | Motores existentes / comportamento | Critério de aceitação |
|---|---|---|---|
| GW / buracos negros | strain GWOSC, tempo GPS, detector, DQ, PSD, metadados e posteriores das bancadas 013/015 | ringdown, realização/ensemble, ecos e referências GR já existentes | todo conjunto declarado carregado, arrays em RAM, janela reproduzível, modelo com fonte/versionamento e projeção tipada |
| Cosmologia | DESI BAO média/covariância, SNe Ia, KiDS, vazios e redshift | D9 e demais executores já existentes | unidades, seleção e covariância preservadas; previsão/resíduo sobre o mesmo vetor |
| Neutrinos/partículas | dados experimentais e produtos já calculados efetivamente localizados | oscilação/dephasing/massas conforme rotas do acervo | energia, distância, estado/sabor, exposição e erros tipados; nenhuma tabela presumida por um HTML |
| Coerência / tempo | estados, espectros, geradores e referências de relógio | funções da TGL verificadas na fonte | controle temporal distingue reprodução, evolução física e parâmetro modular |
| Investigação conjunta | resultados e covariâncias dos domínios | pipeline com hipóteses comuns e controles | nenhum espelho contado como evidência independente; ensaio calibrado e reprodutível |

Domínio não significa todos os arquivos de qualquer pasta. Cada domínio tem manifesto com lista explícita de fontes e produtos científicos. A primeira carga é todo o subconjunto GWOSC strain instalado nas caches 013/015: 180 caminhos, 19.573.121.219 bytes em disco na medição inicial. O tamanho decodificado será medido na carga. Posteriores e artefatos do ringdown entram por perfis específicos nas próximas unidades; não são silenciosamente chamados de carregados.

## Arquitetura e responsabilidade

1. **Registro de fontes e perfis:** identidade da fonte, evento, detector, unidades, tempo, máscaras, calibração e política de correlação. Priorizar originais e anotar cópias; só colapsar duplicatas depois de conferir igualdade.
2. **Sessão residente:** um worker científico persistente no ambiente NumPy/h5py/SciPy já instalado. Carga integral de arrays em thread, estado/progresso, cancelamento/liberação, orçamento com RAM Windows e WSL disponíveis. Sem memmap anunciado como RAM carregada. Medir bytes dos arrays, RSS e swap do processo.
3. **Produtos visuais:** envelopes mínimo/máximo de todas as amostras da janela, histogramas e vistas multirresolução. Gaps permanecem visíveis. O renderizador não usa esse produto como espectro ou likelihood.
4. **Adaptador do modelo existente:** cópia imutável e hash do executor científico, entradas físicas validadas, resultados e hipóteses preservados. Nenhuma física duplicada em JavaScript. O primeiro é `tgl_ringdown_prediction.py` / `tgl_ringdown_template.py`.
5. **Interface por domínio:** visão do sistema, séries observadas, modelo, linha do tempo e painel de parâmetros sincronizados. Reprodução e zoom não desencadeiam nova leitura do banco em disco.
6. **Execução e recibo:** cenários salvos com parâmetros, fontes, hashes, seleção temporal, versão do modelo, controles e resultados. Previews de slider não viram automaticamente rodadas científicas seladas.

## Tempo: controles distintos e legíveis

- **Reprodução:** pausar, avançar, voltar e velocidade da animação. Voltar relê dados já residentes; não inverte dissipação.
- **Tempo detector/GPS:** vem dos atributos reais do banco; janela em segundos e referência GPS preservadas.
- **Tempo fonte:** transformação explícita `t_fonte = t_detector/(1+z)` quando aplicável à relação cosmológica adotada; massa detector = massa fonte × (1+z).
- **Relógio TGL e tempo modular:** localizar a fórmula canônica, seu enunciado e o vínculo ao observável antes de fornecer um controle físico universal. O executor ringdown existente tem leituras R-A/R-B e outras com hipóteses distintas; nenhuma vira default silencioso.
- **Tempo de evolução:** argumento físico do executor; domínio, unidade e regime aparecem no painel. Não confundir tau* (escala do ruído), tau_GR (amortecimento) e tempo de playback.

## Entregas e dependências

| Etapa | Entrega concreta | Verificação para avançar |
|---|---|---|
| U0 — reconciliação | plano, fontes de tempo, modelos copiados com hash, mapa de domínios | fonte e hipótese de cada fórmula localizadas; bancadas anteriores reaproveitadas |
| U1 — RAM e navegação | GWOSC strain completo residente; progresso, liberação, tempo e envelope | carga termina com N/N ou recusa explícita; bytes/RSS/swap medidos; duas vistas sem novas leituras de dados |
| U2 — modelo vivo | massa, spin, z, relógio explícito, curvas GR/TGL do executor existente | controle sem dephasing coincide com GR; beta calculado pela função existente; previsão acompanha sliders; estatuto ensemble preservado |
| U3 — evento físico | seleção de evento e detector, PSD/DQ, janela pós-pico, projeção antena, posteriores | modelo e dado no mesmo tempo/unidade; parâmetros vinculados a posterior ou definidos como cenário; sem ajuste inventado |
| U4 — ecos/ringdown | ligar likelihoods e pipelines reais das bancadas anteriores, métodos nulos e injeções | recuperação de injeção e controles; custos/latências medidos; resultados persistidos |
| U5 — cosmologia/partículas | perfis de RAM e modelos por domínio | dados necessários integralmente legíveis, unidades/erros preservados e executor reproduzido |
| U6 — busca conjunta | mapa de sensibilidade e protocolo de >=5sigma | correlações, seleção, ensaios múltiplos e modelo rival tratados; sensibilidade prevista separada de significância observada |

Ordem de execução: U0 e U1 em paralelo com UI; U2 após fontes de modelo; U3 antes de inferência real GW; U4/U5 conforme perfis prontos; U6 depois de controles. Cada etapa entrega algo utilizável. O planejamento não promete encontrar 5sigma: define como investigar a separação entre modelos e como calibrar um achado.

## Distribuição atual

- Coordenação local: integração do runtime residente, contratos, proveniência, aplicação dos modelos e validação ponta a ponta.
- Kimi: revisão de memória/concorrência, LOD e critérios de residência; unidade nova `kimi_ram`, uma execução pela fila existente.
- MiMo: contrato de produtos tratados e testes de aceitação por domínio; unidade nova `mimo_domains`.
- Agente UI: três arquivos novos, fora do backend, conforme contrato HTTP fixado.
- Agente de fontes: auditoria de leitura da fórmula do tempo, sem editar originais.

As revisões externas são propostas até conferência. Há uma fila de orquestração; nenhum heartbeat novo. Rodadas anteriores terminais não serão repetidas.

## Medidas de desempenho

Registrar tempo de carga, bytes decodificados, RSS/swap, número de séries/datasets, latência de janela, latência do modelo e renderizador real. Metas iniciais a medir: interação visual suave; janelas comuns abaixo de 150 ms no worker e atualização de modelo abaixo de 250 ms; operações pesadas com progresso/cancelamento. Não são resultados medidos. Uma vista não deve reler arrays em disco após a carga.

## Limites da primeira versão executável

A primeira versão trabalha com strain real completo e curva condicional do modelo em painéis relacionados, mas não faz reconstrução 3D de céu/órbitas sem os dados e o modelo correspondentes, nem fitting automático do evento. Posteriores, PSD, projeção do detector, calibração, ecos e demais domínios têm unidades próprias no plano. O painel sempre informa a etapa alcançada.


<!-- TGL_UNIVERSE_RESIDENT_VALIDATED_d2ce602e-c7ee-42d5-bee6-14389e8485b5_PLAN -->
## Adendo de execução verificada — 27/09/2026

U0: fontes do tempo localizadas; veja TIME_SOURCE_AUDIT.md. O índice/inverso do peso de Markov, a ponte modular/Killing e tau* têm tipos e hipóteses distintos, agora documentados.

U1: carga real READY 180/180, 900 arrays numéricos, 22,50550 GiB, swap zero na rodada. Doze vistas sem releitura dos dados; p95 HTTP 50,4517 ms. Sete repetições de hash strain permanecem rastreáveis, não contadas como observações independentes.

U2 inicial: parâmetros massa fonte/spin/redshift, leitura explícita de relógio e curvas do executor ringdown anterior. CUA confirmou parâmetros e navegação; 24 testes Windows e cinco WSL aprovados. U2 ainda deve receber salvamento de cenário e vista de diferenças. U3–U6 permanecem no plano. Voz e cena espacial 3D exigem seus conectores e observáveis; não foram substituídas por animação decorativa.

Experiência espacial prevista: escalas universo → catálogos e redshift → eventos/ondas → estados/partículas, com seleção vinculando todas as vistas. Cada posição/raio/campo visual terá fonte, transformação e unidade; a cena do modelo permanece identificada como previsão quando não houver reconstrução observacional. Controles de tempo serão sincronizados por referências explícitas, jamais confundindo reprodução reversa com inversão física de dissipação.



<!-- TGL_U3_EVENT_VERIFIED_8560b710-3ad7-402b-a12e-9a0b1fdf1ad3_PLAN -->
## 27/09/2026 19:26 — U3 inicial verificada

Evento GW250114 ligado ao par H1/L1 residente, DQ/injeções, ruído, normalização e controles manuais. Ver U3_EVENTO_OBSERVADO.md e recibo validation_event_live_8560b710-3ad7-402b-a12e-9a0b1fdf1ad3.json. U3 permanece parcial: antena e posterior físico/calibração aguardam ligação. ORDEM18 coordena a escolha/revisão do próximo teste; nenhuma significância foi produzida pelo painel.


<!-- TGL_COSMOS_DESKTOP_WEBGL2_DELIVERY_20260928_PLAN -->
## 28/09/2026 — TGL Desktop, GPU e primeiro domínio cosmológico

[INPUT] O operador pediu prosseguir, corrigir o acesso rápido TGL no Windows e avaliar renderizador/Blender.

[REAL] Atalho TGL conferido em Desktop local e OneDrive/Desktop do usuário; launcher e ícone multirresolução existem. A abertura pelo próprio atalho foi invocada e os dois serviços responderam à verificação. Não foi feita inspeção visual do desktop nativo. Tentativa de cópia pública recusada por ACL; não houve alteração de permissão. Backups preservados e ocultos para não poluir o Desktop.

[REAL] Módulo Cosmos em http://127.0.0.1:18766/cosmos, acessível pelo cartão de Cosmologia no Universo residente e pelo mesmo launcher. Renderer WebGL2 identificou RTX 5090/ANGLE D3D11 no navegador. Curvas BAO, barras de erro, resíduos, matriz de correlação, parâmetros manuais, cursor redshift/fator de escala e grade 3D com órbita/zoom/animação. Blender é ferramenta opcional de produção/exportação, não dependência do runtime. A grade é um diagrama, sem galáxias ou posições inventadas.

[REAL] Par DESI DR2 local: 13 medidas, sete redshifts, covariância 13×13 completa, 3019 bytes das duas fontes lidos uma vez. Carga aa17b5e5115b4315a2020bbf016dd54a; consultas aquecidas sem novas leituras. A matriz possui 1352 bytes equivalentes numéricos, não RSS. Os hashes são verificados no primeiro carregamento. Fontes/copias e limitação de commit remoto estão em data/cosmology/ORIGINS.md.

[REAL] Sete testes de runtime, dois HTTP e dois launcher aprovados; onze únicos. Uma falha real foi corrigida: cosmos indisponível não deve impedir abrir GW saudável. Concorrência da interface auditada e corrigida: cancelamento ao editar, preservação do cursor na reprodução, cancelamento RAF e mensagem de erro persistente. CUA conferiu χ² 28,9659 → 596,9249 ao variar H0 de67,4 para73, cursor z1,484/a0,40258, GPU, animação e navegação. Seis cenários HTTP: 15.08–31.92 ms, sem significância calculada. Não é benchmark amplo.

[REAL] GW preservado: carga 8560b710-3ad7-402b-a12e-9a0b1fdf1ad3, 180/180 arquivos, 24165092160 bytes; mesmo vetor de hashes antes/depois das consultas. Servidor GW não reiniciado. Cosmos não instancia worker GW; a separação operacional permite adicionar o domínio sem perder a RAM antiga.

[OPEN] O modelo novo é FLRW plano matéria+CPL para z≤3, sem radiação/curvatura, rd como entrada independente, estatuto EXPLORATORY_BACKGROUND_NOT_TGL_PREDICTION. É a camada interativa de dados/referência para a rota D10. Ligar a previsão cosmológica canônica da TGL e CMB/BAO com perturbações, nuisance, dados sem dupla contagem e estatística global permanece no contrato acústico já registrado. Nenhum ajuste cosmológico, 5σ novo, original científico, kernel ou gate foi alterado.

Recibo: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\state\delivery_cosmology_desktop_20260928.json`, SHA256 1a7c4991a0b0f0aae83da14f2f916bb970fc62d98b69ce21fc7fe75989fd50c4. Desenho: RENDER_E_COSMOLOGIA.md. A delegação produziu backend/testes (Fermat), HTML/CSS (Banach), auditoria/HTTP/launcher (Lagrange); integração, JS, instalação e teste real pela coordenação. Nenhuma nova chamada externa ao stack nesta rodada.



<!-- TGL_COSMOLOGY_V3_SCENARIOS_8fd20dbe0d994cae_PLAN -->
## 28/09/2026 — Cosmos V3 ligado; cenários e comparação A/B

[INPUT] “prossiga, melhore, avance, aprimore”. Continuação da bancada interativa local; originais científicos preservados, sem alteração de kernel/gate.

[REAL — recuperação antes de implementar] Auditoria de leitura localizou `FundoV3` e verificou a cópia contra o literal embutido do um.py v375. Rota: fator no fluido total incluindo Λ, primeira Friedmann por primitiva, P(∞)=ρΛ, C=0, ΩΛ por E(0)=1. Não substituímos por rota setorial, S/L históricos ou face recíproca. Relatório: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\COSMOLOGY_CANONICAL_ROUTE_AUDIT.md`.

[REAL / CONDICIONAL — software] Fonte pinada reutilizada em processo WSL próprio; nunca chama CAMB, derivados, rs_integral ou o worker GW. Modelos: TGL_V3_TOTAL_FIXED_BETA, V3_TOTAL_BETA_ZERO (com radiação), CPL exploratório. β por ALPHA_FINE_CODATA_2018×√e. H₀, Ωm total e rd interativos; w0=-1 e wa=0 no V3. Partição representativa dos inputs de matéria não é estimativa física de bárions/neutrinos. rd é externo; TCMB/Neff do worker histórico. E(0), positividade, segunda Friedmann, refinamento local e controle β=0 conferidos; código não promove ramo a previsão cosmológica completa.

[REAL — interface] A/B com referência tracejada, diferença DM/DH/DV por z, controles deslizantes, β/ΩΛ/cache visíveis. Cenários SQLite append-only preservam parâmetros, resultado, fontes, geração de componentes e UTC. Cálculo refeito no servidor antes de salvar/exportar; exportação em state/exports com leitura pelo navegador. O download blob não ficou verificável no IAB e foi substituído por arquivo real no servidor. Originais de cenários permanecem; versões incompatíveis são recusadas como A e podem ser recalculadas como B. Nenhuma aceitação de resultado forjado do cliente.

[REAL — controles desta rodada] 66 testes passaram, zero ignorados, incluindo WSL real e falhas de integridade. Revisões locais detectaram e corrigiram mistura visual entre gerações, contratos HTTP inconsistentes, respostas V3 incompletas/não finitas e hashes divergentes. Não são teoremas físicos novos. Geração medida: 8fd20dbe0d994caedbf592065b7a0132b9d611509b096d5401e434ae485be1d0.

[REAL — diagnóstico MANUAL, sem sigma] Nos parâmetros H₀=67,4, Ωm=0,315, rd=147,09: χ² zero=28.693472805001; fixo=26.080252417552; Δχ² B−A=-2.613220387449. 13 componentes DESI DR2, covariância completa e distâncias calculadas nos z exatos. Cursor não muda χ²; rd muda a escala. Tempos de executor medidos: primeira chamada 2960.17 ms; β fixo 43.19 ms; cursor quente 3.68 ms. Uma rodada não é benchmark universal. Não houve fit/nuisance/simulação global; Δχ² não virou Z.

[REAL — preservação] GW continua READY 180/180, 24165092160 bytes, load_id 8560b710-3ad7-402b-a12e-9a0b1fdf1ad3, mesmo inventário/hashes. Reiniciado somente Cosmos, porta18766. Atalho TGL no Desktop OneDrive conferido existente. Serviço temporário de desenvolvimento será encerrado; web pública/iOS/Android não alterados, builds não aplicáveis.

[OPEN — próximo trabalho] Integrar as perturbações e precisão CMB/rd no protocolo D10, priors/nuisance e rivais explícitos, sobreposições e simulação global; também continuam a integração dos demais domínios e voz. Navegação de z/grade 3D é representação, não relógio físico TGL nem mapa observado. Esta entrega é reprodução interativa de fundo condicional, não novo resultado 5σ.

Recibo: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\state\validation_cosmology_v3_8fd20dbe0d994cae.json`, SHA 576b6757f291126df628aacfe553ba908e33259777d35cfebd9e4bba5ed8b380. Guia: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\COSMOLOGIA_V3_CENARIOS.md`. Nenhum original, patente ou acervo jurídico alterado.



<!-- TGL_UNIVERSE_EDUCATIONAL_MAP_d480ccbf21105694 -->
## 28/09/2026 08:48 — Universo educativo, mapa livre + percurso guiado

[INPUT] O operador pediu que o sistema funcione como um programa de curso astrofísico/cosmológico, mostrando matéria bariônica, matéria escura, energia escura, CMB, expansão e estruturas, para facilitar a interação. Escolheu explicitamente “Mapa livre + percurso guiado”.

[REAL — interface instalada] Entrada http://127.0.0.1:18766/explore, oito temas com questões, explicações, experiências, fontes primárias e links aos laboratórios existentes. Navegação livre, Anterior/Próximo, marcação explícita de leitura e progresso no navegador. O atalho TGL conserva seu alvo launch.py e passa a abrir o mapa se Cosmos responder; fallback para GW preservado. Menus Cosmos/GW retornam ao mapa. Apenas Cosmos reiniciou; banco GW não reiniciado.

[REAL / DIDÁTICO] Diagrama interativo de frações de densidade, histórico logarítmico em 1+z, presets de época e controles Ωb/Ωc/Ωr; ΩΛ por fechamento. Modelo FLRW plano idealizado: matéria a^-3, radiação a^-4, Λ constante. Valores arredondados de ensino, domínio z0..100000, sem idade física, formação, perturbações ou recombinação calculada. Frações não são regiões espaciais. Fonte matemática WMAP e demais fontes primárias em EDUCACAO_FONTES.md/static/cosmos-lessons.js. Este módulo não redefine a Ωm agregada do V3 nem fornece espectros TGL. Sem novo sigma ou mudança do gate.

[REAL — verificação] 67 testes Python e 7 testes Node aprovados; rotas instaladas conferidas byte a byte, geração científica preservada 8fd20dbe0d994caedbf592065b7a0132b9d611509b096d5401e434ae485be1d0, cálculo V3 padrão idêntico ao recibo anterior. UI conferida: oito temas, percurso/progresso após reload, z1100 e z10000, recusa de composição inválida e recuperação. Revisão independente achou e foram corrigidos dois bugs: histórico velho após sequência redshift inválido→alterar composição→redshift válido; link interno recarregando e perdendo cenário. Fluxo corrigido conferido no navegador. Valores pequenos positivos são mostrados como <0,0001%, sem anunciar zero exato.

[REAL — preservação] GW 180/180 arquivos, 24165092160 bytes, mesmo load_id 8560b710-3ad7-402b-a12e-9a0b1fdf1ad3 e hashes. Memórias com backup imediato de bytes e append atômico. App local TGL somente; conversa pública/iOS/Android não modificados, builds não aplicáveis. Código por agentes locais: modelo didático/testes, roteamento/launcher, fontes primárias; coordenação: integração visual, correções, instalação e verificação. Nenhuma nova chamada externa Kimi/MiMo/DeepSeek nesta entrega.

[OPEN] Temas CMB/estruturas estão organizados para ensino; mapas e Cℓ CMB, catálogos 3D, crescimento/lentes ainda não foram conectados a essa interface. BAO e GW usam os laboratórios reais já existentes. Voz, integração de todas as sondas e teste global D10 seguem no planejamento anterior.

Guia: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\MAPA_EDUCATIVO.md`. Recibo: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\state\education_validation_20260928_084800.json`, SHA256 846b9d421ad65b775e68340dc625ee31687263572004198288ef3fea4cb2a7a7. Originais científicos intactos.



<!-- TGL_EXTREME_REGIMES_7fa2c44bca8a96e3 -->
## 28/09/2026 09:04 — Regimes extremos visíveis e métricas condicionais

[INPUT] Operador: “Inclusive eu preciso ver os locais de regime extremo com maior facilidade, porque é lá onde a TGL vai se manifestar em maior evidência”. Implementada navegação por ambientes, eventos e cenários, preservando como hipótese investigativa a relação entre regime extremo e maior evidência. Não há ranking de sigma sem medida de sensibilidade.

[REAL — interface] Seção destacada `/explore#extreme-regimes`, com seis rotas: Universo jovem/acústica (prioridade D10), horizontes/ringdown (GW250114), spin elevado, modos de maior frequência, vazios/contrastes e partículas/coerência. Cada seleção mostra o que variar, efeito a comparar, estado da sensibilidade e acesso disponível. CMB alto-z permanece didático; BAO abre o V3 existente z≤3. Vazios/partículas identificados como integração pendente. Sem coordenadas celestes inventadas.

[REAL — cenários] Links allowlist `?regime=high-spin#ringdown` e `?regime=high-frequency#ringdown` preparam apenas controles `model-*`, nunca o evento. Cenário spin: massa fonte65, spin0,95, z0,1, duração0,12s; frequência: massa fonte20, spin0,7, mesmo z/duração. Não selecionam relógio; leitura exigida do usuário. Banner deixa explícito cenário exploratório, não ajuste ao evento. Valores desconhecidos/duplicados de regime não aplicam preset.

[REAL / CONDICIONAL] UI lê do executor Γ, x=Γτ_GR, delta_tau_ensemble_exact, modo e método QNM; nenhuma fórmula física nova no navegador. Dados ausentes são indisponíveis; números minúsculos usam notação científica; R-GLOBAL exibe zero real. Seis controles HTTP medidos no executor existente: R-B referência x=0.02115589140876138, delta_tau=-0.020717592276312716; spin0,95 x=0.06251370332366527, delta_tau=-0.058835667839497216. Massa20: frequência 785.7033607931457Hz, Γ=15.886628475296325s^-1, x=0.021155891408761382 igual à referência dentro da precisão. R-A conserva efeito muito pequeno e a escala inversa com massa; R-GLOBAL zero. São previsões de ensemble sob hipóteses explícitas, sem fit, curva de sensibilidade ou sigma.

[REAL — verificação] Navegador conferiu seis cartões, deep link spin com campos corretos, relógio vazio e botão de cálculo desabilitado, seleção R-B e valores do executor, R-A não arredondado a zero, R-GLOBAL com zero, método/mode retornados, sem erros JS ou overflow horizontal. Revisão física independente examinou escalas da fonte e limites. Nenhum novo serviço nem reinício: preservada carga GW 180/180, 24165092160bytes, load_id 8560b710-3ad7-402b-a12e-9a0b1fdf1ad3 e hashes. Alteração somente da bancada local; web pública/iOS/Android não afetados. Nenhum original científico ou gate alterado.

Guia: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\REGIMES_EXTREMOS.md`. Recibo: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\state\extremes_validation_20260928_090052.json`, SHA256 a7dac6857bd7289c0e32f922a9ed93bba34bfe28636ca824885f77db83f1204b. Memórias com backup imediato de bytes e append atômico. Sensibilidade global, mapas CMB/estrutura, vazios e partículas seguem nas pendências explicitadas.



<!-- TGL_INVESTIGATION_20260928_99e70f454eccdcf7 -->
## 28/09/2026 — Investigação da bancada com agentes, sem novo sigma

[INPUT] Operador pediu examinar o sistema residente e investigar com agentes onde há melhores condições de testar a TGL.

[REAL] Três agentes locais concluídos e verificações independentes PASS: 21 cenários BAO; 29 fontes GW e inversão de Q; sete blocos canônicos e trechos do programa. MiMo concluiu parecer, preservado como DECLARADO com correções matemáticas/estatísticas ao lado. Kimi falhou sem resposta aceita, sem repetição. Nenhum resultado novo atribuído a Claude/DeepSeek nesta rodada.

[REAL — sistema] 180/180 arquivos GW, 22,50550 GiB de arrays, swap zero, seis vistas em 31–80 ms, mesmo load_id e nenhuma releitura. É ensaio em uma série, não benchmark de ajuste/concorrência. Catálogo 1.350 arquivos/~72 GiB inclui duplicatas. BAO residente contém 13 pontos e covariância 13x13; não representa todos os catálogos/mapas. GPU atende renderização; cálculo científico em GPU não medido.

[REAL/DERIVED — achados] Na comparação BAO, escala e densidade reduzem d² de 0,55873894 para 0,00473259 (99,153% da distância quadrática), exemplo entre modelos, não fit/sigma. Um modo de ringdown é compensável por massa/spin na aproximação exploratória BCW. C6 segue INCONCLUSIVE_SYSTEMATICS, lnB primário -0,002595.

[CORREÇÃO AO LADO — ACT V9] Fisher compara delta_c=-0,95, s1=1, pisos 0 e beta. O perfil é >=0,05>beta: os dois modelos são idênticos antes do ruído, F=0 estrutural nesse ensaio. Fonte e linhas conferidas; controle positivo delta_c=-1 ativa o piso, mas é diagnóstico, não nova previsão/inferência. A grade de likelihood posterior é distinta e não foi declarada toda cega. Preservado o UNDERPOWERED histórico; sua causa não pode ser atribuída somente à sensibilidade do ACT. Nenhum original alterado.

[PLANO] D10 CMB–BAO mantém prioridade estratégica: ligar tradução perturbativa/r_d e likelihoods existentes com covariâncias/overlaps. Auditar primeiro a sensibilidade ACT em cópia; para GW, diagnóstico 220+440 do mesmo remanescente na métrica de ruído, projetando nuisance e exigindo amplitude informativa. Neutrino é confronto condicionado; ecos exigem recuperação qualificada; relógios P1 têm déficit de sensibilidade no protocolo atual. Nenhuma rota recebeu poder 5sigma global demonstrado.

[ESCOPO] Relatório `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\INVESTIGACAO_PRIORIDADES_20260928.md` (SHA256 99e70f454eccdcf772607afa4bc1da92a6626432f7a46abdfce5a0f13b0c6bed). Evidências/manifesto em `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL\state\investigation_20260928`; hashes calculados por script. Serviços/RAM preservados, sem alteração de original científico, kernel, gate, interface, app público/mobile. Memórias operacionais desta bancada e índices centrais recebem append com backup de bytes; linhagem científica Nós não tocada porque nenhuma versão foi selada.

