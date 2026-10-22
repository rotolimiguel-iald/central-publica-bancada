# F1.1 — importações efetivas da cadeia QG

07/10/2026 · [REAL] leitura de `INVENTARIO_BANCADA_CHATGPT.md`, `QGCitationDischarge.lean`, `QGSolutionComplete.lean`, `TheImportedSecondQuantization.lean` e `TheImportedEquilibrium.lean`. Os SHA-256 integrais, medidos dos arquivos, constam em `RESULTADO.json`. Consulta prévia ao Nós vivo: `consultar.py --unidade F1.1`.

**Régua da tabela.** FECHADO = há termo no núcleo para o elo indicado; VINCULADO = o consumidor Lean usa um campo nomeado, mas o certificado físico não tem habitante construído; SABIDO = resultado externo da literatura ainda sem ligação Lean específica. A estimativa de esforço é uma previsão de engenharia, não um resultado de compilação. Ela supõe um desenvolvedor experiente com Mathlib e exclui a validação física da teoria.

| Resultado externo / enunciado realmente consumido | Pedra e campo | Classe | Estimativa para formalizar o elo faltante |
|---|---|---|---|
| Wigner/BGL: rede real padrão do fóton de helicidade ±1, isotonia, localidade e covariância por translações e boosts | `LightOneParticle.K`, `K_mono`, `K_local`, `K_translate`, `K_boost`; entra por `LightNetData.toLightOneParticle` | VINCULADO | Meses; construir subespaços padrão e geometria causal, além de instanciar o tipo do fóton. |
| Continuidade forte de `U1` e ausência de autovetor da translação nula | `LightOneParticle.U1_continuous`, `null_no_eigen` | FECHADO no fornecedor `LightOneParticleByTerm`; conferir conexão da construção física global | Dias para conferir a fiação; a pedra já fornece os termos, sem refazer a prova. |
| Araki/Leyland–Roberts–Testard: Fock bosônico, segunda quantização unitária, setor de uma partícula, espectro positivo, Weyl e covariância | `FockCertificate.Γ`, `ι`, `Γ_strong`, `Γ_strong4`, `Γ_positive`, `Γ_no_fixed`, `R`, `R_mono`, `R_local`, `R_cov` | VINCULADO | Meses; a biblioteca geral de Fock/Weyl e os limites topológicos dominam o custo. |
| Reeh–Schlieder na cunha, separação e não comutatividade da álgebra de Weyl | `FockCertificate.wedge_cyclic`, `wedge_separating`, `wedge_nonabelian` | VINCULADO | Semanas a meses depois de Fock/Weyl; depende da rede padrão concreta. |
| Bisognano–Wichmann: boost de Fock em `2πt` satisfaz KMS de parâmetro 1 na cunha | `FockCertificate.bw_kms`; `TheImportedEquilibrium.lean` descreve o alcance | VINCULADO | Meses depois de Fock/Weyl/Tomita; prova analítica de faixa KMS. |
| Tomita–Takesaki: conjugação modular, realização de Tomita e fluxo `Ad Δ^{it}` preservando a álgebra da cunha | `FockCertificate.J`, `tomita`, `flow`, `flow_is_Ad` | VINCULADO | Meses; a estrutura abstrata já existe em partes da bancada, mas a instância da cunha continua faltando. |
| Takesaki/Connes: núcleo contínuo, ação dual e traço com `τ(θ_s x)=e^{-s}τ(x)` | `FockCertificate.Core`, `embedding`, `dualAction`, `trace`, `trace_tracial`, `trace_dual_scaling` | VINCULADO para a álgebra da luz; FECHADO para o núcleo regular próprio de `V351RegularCoreTraceConstruction` | Semanas para uma ponte explícita do núcleo `M_n⋊ℝ`; meses para a álgebra da luz. A escala e o traço do núcleo regular já têm termos e não são dívida nova. |
| Connes: projeção finita não nula no núcleo e decomposição em metades ortogonais de mesmo traço | `FockCertificate.PF`, `Pp`, `Pm`, `split`, `orth`, `trace_additive` | VINCULADO | Semanas após instanciar o núcleo físico; não decorre só da escala dual. |
| Maxwell livre/Wightman: domínio invariante e tensor local simétrico, conservado, covariante | `MaxwellCertificate.Dom`, `Dom_translate`, `T` | VINCULADO | Meses; o campo distribucional e a renormalização não estão representados integralmente por um tensor pontual total. |
| Casini–Teste–Torroba/Wall: energia modular no plano nulo igual a `2π` vezes a carga nula; Longo: estado coerente regular não trivial | `MaxwellCertificate.charge_link`, `nontrivial` | VINCULADO | Semanas a meses após Maxwell/Fock; o enunciado consumido é condicionado ao domínio regular nomeado. |
| Jacobson: equilíbrio local `θ=0` e relação termodinâmica do horizonte | `QGSolutionComplete.qg_solution_end_to_end` recebe `hθ`, `G>0` e os certificados; `TheImportedEquilibrium` distingue o fluxo dado pela torre da implicação física | VINCULADO/INPUT | Meses para uma versão geométrica completa; o teorema atual é uma implicação sob entradas nomeadas. |
| Jones: teoria de índice/subfatores | Nenhum campo Jones na assinatura de `qg_solution_end_to_end` nem em `FockCertificate` | SABIDO; **não é importação desta cadeia** | Não estimar trabalho para esta cadeia sem consumidor concreto. |

[REAL] `qg_solution_end_to_end` e `the_tetelestai_declaration` são teoremas condicionais: recebem rede, certificados Fock/Maxwell, normalização, `G>0`, estado admissível e `hθ`. A parte H1/Breuer vem da torre regular, justaposta à parte física; não há nessa assinatura uma identificação `PkerK ↔ PF`. O cabeçalho de `TheImportedSecondQuantization` registra três limites de formalização: traço total no anel, tensor de tensão pontual total e helicidade como rótulo sem rotação/PCT construída. Nenhuma dessas observações move o gate nem atesta confirmação física.


## 08/10/2026 — ressalva da gerência c1: pedras O16 existentes, fiação da assinatura pendente

<!-- F11_O16_CLASSE2_FIACAO_20261008 -->

[REAL — cético aferidor] Classificação antes de dizer «falta»: **1. EXISTE E ESTÁ LIGADO** — `TheImportedSecondQuantization.lean:565–582` já usa `ReconhecimentoPeloConteudo` em `lightImport` como `selfRecognition`, com `U=id` no mesmo par da luz. **2. EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA** — as seis pedras O16 abaixo têm termos, mas a ponte entre pares/projeções e a ação física de rotação/PCT não aparecem entre as entradas nem na conclusão de `QGSolutionComplete.qg_solution_end_to_end:79–91`. **3. SABIDO** — a identificação espectral no core permanece uma referência sob suas hipóteses; isso não é o termo de ligação. **4. AUSENTE** qualifica apenas o habitante/teorema de colagem tipada e a realização física global, não as pedras que já existem.

| Resultado existente a aproveitar | Pedra e enunciado provado neste escopo | Classe para o elo solicitado | Estimativa do trabalho restante |
|---|---|---|---|
| Reconhecimento modular por conteúdo, dilatação da cunha, caracteres/telas circulares e pontes de rotação/Wick já no `TGLExt/O16`; o alvo novo é ligá-los ao mesmo par de `qg_solution_end_to_end`. | D6 transporta grafos Tomita sob `U`/álgebra/vácuo; D5 reconhece a dilatação sob `D`, covariância, vácuo e realização analítica; D1prime e `circularScreen_conjugate` provam caracteres e conjugação pontual; `RotationGeneratorBridges` liga os três geradores matriciais; `WickBoostRotation` identifica boost complexo e rotação 2×2. Detalhes e hashes abaixo. | **2 — EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA** para a identificação entre pares e o PCT físico. O subcaso D6 `selfRecognition` já usado por `lightImport` é classe 1, sem pagar a ponte para `P_F`. | `[INPUT — engenharia, não medição]` Ver estimativa por pedra abaixo. As faixas se sobrepõem e supõem as testemunhas nomeadas; construir rede/Fock físicos é trabalho distinto. |

**Pinos e fiação, por pedra (SHA-256 integral lido dos bytes):**

- `RecognitionGraph_v2.lean` — `4be9c34d816df0b1bbd8b38a56fa574a6f1252d64d6d2cae7a7ac5ea90021e65`. `ReconhecimentoPeloConteudo` pede unitário `U`, preservação do vetor e equivalência das álgebras; os teoremas transportam grafo Tomita/fecho e operadores fechados sob hipóteses de realização. `selfRecognition` usa `U=id` no import v3.2, mas não identifica a projeção da torre `P_ker K` com `C.PF` do core da luz. **Fiação:** construir/fornecer o reconhecimento entre os pares efetivamente distintos, os mapas entre cores/cantos de tipos diferentes e um consumidor tipado na cadeia QG. **Esforço `[INPUT]`:** 2–5 dias só para a interface depois de fornecidos os certificados; semanas–meses para a identificação entre pares, cores e projeções.
- `DilationModularRecognition_v2.lean` — `de48dcb43e7738e1afc9639dc0c3198845b7dd94c728dd720b19772102be9388`. `dilation_recognizes_modular_content` conserva `J` e fluxo no mesmo par da cunha para dilatação positiva, **sob** `D`, `hVac`, `hNet` e `PairTomitaAnalyticRealizationMeasured`; rejeita dilatação zero. **Fiação:** adaptar o contrato O16, uma cópia retipada de `TGL.SpecificAQFT`, ao certificado da cadeia; instanciar `D`, `hVac`, `hNet` e ligar o teorema à assinatura. A pedra não constrói `D` físico. **Esforço `[INPUT]`:** 2–5 dias para interface e conversão tipada com testemunhas fornecidas; a dilatação física é trabalho adicional.
- `PhotonScreenCharacters_v3.lean` — `f179509af8edcdd875a2a38cf53a42093ce39ad725ea62f0ce5a1b6bcdd77580`. Prova métrica transversal, coeficientes O(2), fase/caracteres compostos e troca **pontual** das seções circulares por conjugação; orientação `det=+1` é hipótese adicional. O próprio arquivo nega inferência automática de PCT da rede. **Fiação:** representação global induzida de helicidade ±1, orientação, ação no `H1`/Fock e covariância da rede `D.K` no mesmo par. **Esforço `[INPUT]`:** semanas para integração tipada; meses se a representação física não estiver disponível.
- `BoostScreenPolarizations_v2.lean` — `0a3f83f932cc7d889173767f21a9c25b8fabbd5baebd3c636dcf3e5cbd8574ac`. `complex_boost_circular` transporta vetores de tela; `circularScreen_conjugate` troca `h↔−h` componente a componente e as telas diferem na carta regular. **Fiação:** promover a identidade pontual a antiunitário global e PCT da rede/Fock com domínio e covariância, não apenas trocar um rótulo. **Esforço `[INPUT]`:** dias para o transporte local sob representação pronta; semanas–meses para PCT físico.
- `RotationGeneratorBridges.lean` — `f7d31563b28f46ad8692f81b3a0350ff933135c3e53bbfd575a3bf6c5bf9969e`. Liga `genK=Grot` e `rotGen.map=Grot`, suas exponenciais a `Smat`, e o boost Wick a esses geradores **matriciais**. **Fiação:** representar essa rotação no `H1`/Fock da assinatura e provar o entrelaçamento com o mesmo `D.K`; a identidade 2×2 não faz isso. **Esforço `[INPUT]`:** dias para a ponte matricial já tipada; semanas para a ação física.
- `WickBoostRotation_v2.lean` — `61f7d0b275edb64725420037bdcc6bc43bdd592cad28dd14b0154181142cf48a`. Prova continuação complexa matricial exata boost→`Smat` e a identidade em `2π`; o arquivo declara que isso **não** afirma estado KMS. **Fiação:** ação unitária/antiunitária sobre o par físico e faixa analítica KMS quando requerida, sem confundir a rotação compacta com o boost hiperbólico. **Esforço `[INPUT]`:** dias para consumir a identidade de matrizes; semanas–meses para a ponte modular/KMS física.

[ERRATA AO LADO] O parágrafo histórico acima que diz «não há ... identificação»/«sem rotação/PCT construída» deve ser lido no escopo da **assinatura e do par físico completo**. As pedras de reconhecimento, tela e rotação **existem no kernel**. O que não está demonstrado por elas é `U P_kerK U⁻¹ = C.PF` (ou a correspondência espectral tipada pertinente), nem o operador PCT global no `H1`/Fock/rede da assinatura. `P_ker K = ρ*_IALD` na luz e `ρ* ↔ P_F` por saber externo têm estatutos distintos; nenhum hash ou nome os funde. A tabela original de 12 linhas permanece intacta, Jones segue sem consumidor, e nenhum gate se move.

[EVIDÊNCIA] `O16_AFERICAO_F11.json` registra os seis caminhos, hashes integrais, bytes, âncoras e os dois arquivos da assinatura por hash. Nenhum `um.py` ou original Lean foi alterado; nenhuma compilação nova foi executada para esta classificação.


### Errata de escopo da linha O16 — leitura das duas correções c1 de 07/10/2026

<!-- F11_O16_ESCOPO_ROTACOES_ERRATA_20261008 -->

[REAL — consulta posterior] `C:\IALD\CLAUDE.md` (SHA-256 `59b0facd70dfd1315473ef1af18d3f5bdd05b476d6f765acfc98e2e20faee475`; marcadores `errata_rotacoes_homonimas_07out` e `errata_leitura_cria_o_objeto_07out`) corrige a aferição de 27/09 citada pela gerência. A **classe 2 da linha acrescida acima classifica as seis pedras O16 existentes e sua interface ainda não consumida pela assinatura**. Não classifica a rotação espaço-tempo de todos os planos nem o PCT global da rede como teoremas O16 prontos que só precisem de um `import`.

No plano do boost `t–x`, as identidades matriciais Wick/rotação dão a leitura angular e o contorno `2π`; a segunda errata c1 impede chamá-las simplesmente de «homônimas». A frase «a leitura cria o objeto» é interpretação `[INPUT/ONTO]` do operador; a pedra que a formula explicitamente foi compilada só no sandbox e não foi contada como kernel instalado aqui. O que ainda não está no kernel/tipo são as leituras dos outros planos — rotações `x–y`, `x–z`, boosts `t–y`, `t–z`, família Lorentz de cunhas e PCT global da rede. Para a conclusão em uma direção nula da v376, a gerência os registrou como **3. SABIDO / FORA_DO_CAMINHO**, por referências Wigner/BW/BGL, não como nova construção exigida aqui. `D1prime` e `circularScreen_conjugate` continuam provas de caractere e conjugação da tela, não uma ação PCT global no `H1`/Fock/rede. A fiação `P_ker K ↔ C.PF` segue classe 2 quanto à rota D6 disponível, mas sua instância não trivial e o mapa de cores/projeções de tipos diferentes seguem sem termo exibido na assinatura. A estimativa de interface em dias supõe os certificados; não paga as construções globais.

[REAL] Esta errata preserva integralmente a linha e o parágrafo anteriores como histórico. O inventário continua com as 12 linhas originais, uma linha aditiva para O16 e este esclarecimento ao lado. Nenhuma prova, compilação ou gate foi promovido.


## 08/10/2026 — terceira camada: correção R1–R5 da auditoria c1

<!-- F11_TERCEIRA_CAMADA_C1_R1_R5_20261008 -->

[REAL] Esta camada corrige **ao lado** a classificação das pedras O16 feita nas duas camadas anteriores. A classe depende do consumidor: uma declaração pode estar ligada à cadeia v375/v376, mas ficar fora do caminho da implicação mais estreita `qg_solution_end_to_end` (v374). Fonte e âncoras por SHA-256 dos bytes em `FONTE_TERCEIRA_CAMADA.json` (d33532a8b25194bbd172e612e00096d85da12e117b9379c920d42b8b930890c2); auditoria c1 lida do arquivo e incluída nesse manifesto. As 12 linhas originais e as duas camadas históricas acima continuam preservadas.

| Ressalva | Classificação vigente e prova/consumidor | O que falta, se alguém quiser outra rota |
|---|---|---|
| **R1 — D1′** | **1. EXISTE E ESTÁ LIGADO** na cadeia `LightHelicityWigner.lean:35,80–85` → `TetelestaiOneObject.lean:115,126,137` → `TheWholeIsOne.lean:107,141,163`. `photonPhase` dá o caráter de helicidade consumido pelos dois teoremas posteriores. `qg_solution_end_to_end` em `QGSolutionComplete.lean:79–91` usa `lightH3` e não consome D1′. | Nenhuma fiação D1′ é requisito dessa implicação v374. A representação induzida global é outro alvo, classificado R2. |
| **R2 — representação global e D5** | O certificado `GlobalHelicityInducedRepresentationMeasured` e a covariância global `PhotonDilationCovarianceMeasured` são **3. SABIDO / FORA_DO_CAMINHO** na conferência v376 (`um.py:199231–255`). As pedras locais D1′ e D5 continuam existentes, com seus enunciados condicionais próprios. | A representação física global e a instância de dilatação podem ser projetos próprios; as estimativas anteriores em semanas/meses eram `[INPUT]` e não são prazo da cadeia QG atual. |
| **R3 — projeções** | **1. EXISTE E ESTÁ LIGADO**: `LightRhoStar.lean:85–93` prova `rho_star_is_P_kerK_on_the_light`; a conferência v376 marca `PkerK_eq_rhoStar_IALD` como VINCULADO por termo, apoiado também em `TheKeyIsTheReader.lean:48–76`. **3. SABIDO**: `rhoStar_PF_Takesaki`, uma correspondência espectral em álgebras/tipos distintos. A v376 recusa expressamente uma igualdade de operadores com `C.PF` como mal tipada (`um.py:199071–083`). | Uma comparação tipada entre as duas álgebras exigiria mapas e hipóteses novos. A rota D6 `ReconhecimentoPeloConteudo` não fornece por si essa igualdade nem deve ser classificada como fiação crítica já pronta. |
| **R4 — o antigo “4. AUSENTE”** | O habitante completo de `CertificatesMatchTheLiterature` é **3. SABIDO**, não exibido; a colagem `link_PkerK_PF` separa a metade VINCULADA de R3 da metade SABIDA; realização global de outros planos e PCT é **3. SABIDO / FORA_DO_CAMINHO** na conclusão v376 (`um.py:199270–276`). | Não usar “AUSENTE” para cobrar essas três peças como lacunas da implicação demonstrada. Uma colagem física nova seria enunciado adicional, a tipar antes de estimar. |
| **R5 — D6** | `selfRecognition` em `TheImportedSecondQuantization.lean:566–580` usa `U=id` e está ligado **só ao contrato de importação v3.2** por `lightImport`; o cabeçalho da pedra o chama identidade por construção. Na assinatura QG, `FockCertificate.tomita : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured` (`:223`) já existe como **campo condicionado**. `qg_solution_end_to_end` usa `lightH3`, enquanto `qg_contract_from_the_cited_net` consome o contrato citado (`QGSolutionComplete.lean:79–126`). | O campo Tomita não ganha habitante físico por `selfRecognition`. Instanciá-lo é dívida própria do certificado, sem apagar o termo já ligado à assinatura. |

[REAL — estatuto] Nenhuma das correções acima acrescenta prova Lean, constrói PCT global, deriva a instância física ou altera a conclusão de `qg_solution_end_to_end`. As estimativas históricas `[INPUT]` permanecem como história, não como cronograma de fechamento. `NOT_FALSIFIED` não é `CONFIRMED`; gate intacto.


## 08/10/2026 — quarta camada: errata c1 sobre as rotações, CR-09

<!-- F11_CR09_ROTACOES_20261008 -->

[INPUT — errata expressa da gerência c1, fundada em CR-08/CR-09] Esta leitura **prevalece**, para a F1.1, sobre a interpretação de que `ChatgptAudit.Wick016` forneceria as rotações espaciais da rede da luz por mera fiação. A segunda camada acima já registrava que essas pedras são identidades matriciais; a frase posterior «impede chamá-las simplesmente homônimas» não autoriza transportar o mesmo nome para a ação espaço-temporal. As igualdades 2×2 são verdadeiras **no seu tipo** e as rotações da rede são outro objeto. A correção fica ao lado do histórico, sem apagar o que foi medido.

| Objeto e alcance efetivamente lido | Classe vigente na F1.1 | O que ainda falta e esforço estimado |
|---|---|---|
| `ORDEM016.D1prime.photonPhase`, caráter/cociclo, e `ChatgptAudit.WignerRapidityMeasure016.circularScreen_conjugate` provam fase de helicidade e troca pontual das polarizações circulares do **pequeno grupo**. `LightHelicityWigner` consome `photonPhase` na cadeia v375/v376; a assinatura estreita `qg_solution_end_to_end` não o consome. | **1. EXISTE E ESTÁ LIGADO** para o caráter de helicidade na cadeia posterior; teorema local no kernel, sem PCT global. | Nenhuma fiação D1′ é requisito da conclusão v374 em uma direção nula. Representação global e PCT da rede/Fock seriam projetos distintos; estimativa histórica `[INPUT]`: semanas–meses sob certificados físicos disponíveis. |
| `ORDEM016.D6.ReconhecimentoPeloConteudo` transporta grafo/fecho Tomita sob unitário, vácuo e álgebra correspondentes. `selfRecognition` com `U=id` já alimenta `lightImport`; `FockCertificate.tomita` continua campo condicionado. | **1** só para o autorreconhecimento no mesmo par; **2. EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA** para reconhecimento **não trivial** entre pares físicos e respectivos cores/projeções. | Fornecer unitário e identificação tipados, com certificados, antes de compor o mesmo objeto; D6 não prova `P_ker K = C.PF`, igualdade entre tipos distintos. `[INPUT]` interface 2–5 dias com testemunhas prontas; construção física própria não incluída. |
| `ORDEM016.D5.dilation_recognizes_modular_content` conserva `J` e fluxo no mesmo par da cunha sob dilatação positiva, `D`, preservação do vácuo, covariância da rede e realização analítica. | **2. EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA** quanto à instância física da dilatação. | Instanciar `D`, `hVac`, `hNet`, `hReal` e converter o contrato O16 para o certificado consumidor. `[INPUT]` interface 2–5 dias se as testemunhas forem dadas; não é construção dessas testemunhas. |
| `ChatgptAudit.Wick016` identifica geradores `genK`, `Grot`, `rotGen` e a continuação de boost complexo com `Smat(φ)` como **matrizes `Fin 2 × Fin 2`**; prova retorno em `2π`. | **1** para as identidades matriciais no regime **angular/projeção**; **não** classe 2 das rotações espaço-temporais da rede. O nome «rotação» é homônimo quando se tenta passar desse tipo 2×2 à ação de Lorentz nas cunhas. | A identidade matricial já existe; não há fiação automática de `Smat` para uma ação de Poincaré em `K(O)` nem para PCT físico. Consumir a igualdade no mesmo tipo: dias `[INPUT]`; ação na rede exige hipótese/construção separada. |
| Rotações espaciais da rede da luz, família de Lorentz de cunhas para **todas** as direções nulas e PCT global da rede/Fock. | **3. SABIDO POR CITAÇÃO** (Wigner 1939; Bisognano–Wichmann 1975; BGL 2002, conforme CR-09), **fora do tipo e do kernel desta cadeia**. **FORA_DO_CAMINHO** para a conclusão `nn` numa direção nula da v376. Para todas as componentes de Einstein (CR-08/F2.3), a família volta como hipótese nomeada ou construção nova. | Não cobrar `import` de Wick016 como solução. Para o ramo condicional F2.3, explicitar a família como antecedente: dias de tipagem `[INPUT]` após fixar contrato. Construí-la fisicamente no kernel é trabalho maior, sem prazo aferido aqui. |

[REAL — conferência de tipos] `RotationGeneratorBridges.lean:11–33` usa `TGLExt.Smat`/`genK`/`Grot`/`rotGen`; `WickBoostRotation_v2.lean:11–50` define `complexBoost : Matrix (Fin 2) (Fin 2) ℂ` e prova a continuação matricial, declarando que não afirma estado KMS. `TheImportedSecondQuantization.lean:57–60` registra que `W` não tem rotações e que a distinção fóton/escalar por rotações/PCT está fora do tipo. `QGSolutionComplete.lean:79–91` usa uma direção nula e não recebe a família de cunhas. Esta auditoria lê os enunciados; não adiciona prova Lean nem compilação. A distinção face hiperbólica × leitura angular permanece preservada.

**SHA-256 integral dos bytes lidos nesta errata:**

- `consolidado.json`: `7a8aaaeb8d17a3e6fb3cc9a52676d68711e0744534de56c183934b4fe231f9fe`.
- `TheImportedSecondQuantization.lean`: `ef35478400ef07f20476f2bb937d8fbe2df7b9e506139f54dc5a37401e7d5242`.
- `QGSolutionComplete.lean`: `8c3a4bc82c5c4308515063254744cfaefcc7e7b926038221be2e7de6293dc598`.
- `RecognitionGraph_v2.lean`: `4be9c34d816df0b1bbd8b38a56fa574a6f1252d64d6d2cae7a7ac5ea90021e65`.
- `DilationModularRecognition_v2.lean`: `de48dcb43e7738e1afc9639dc0c3198845b7dd94c728dd720b19772102be9388`.
- `PhotonScreenCharacters_v3.lean`: `f179509af8edcdd875a2a38cf53a42093ce39ad725ea62f0ce5a1b6bcdd77580`.
- `PhotonCharacterCocycle.lean`: `08e03316e12e2cec7425ae8534e2ffb80718d11c575e1ee7cd2c1befa0d6bff7`.
- `BoostScreenPolarizations_v2.lean`: `0a3f83f932cc7d889173767f21a9c25b8fabbd5baebd3c636dcf3e5cbd8574ac`.
- `RotationGeneratorBridges.lean`: `f7d31563b28f46ad8692f81b3a0350ff933135c3e53bbfd575a3bf6c5bf9969e`.
- `WickBoostRotation_v2.lean`: `61f7d0b275edb64725420037bdcc6bc43bdd592cad28dd14b0154181142cf48a`.
- `LightHelicityWigner.lean`: `e08c9a4b00e0057b1cdd0e5c1c93a33b3a727ef49edc80cd50911053d672e714`.

[REAL — escopo] A terceira camada R1–R5 permanece como medição dos consumidores específicos. Esta errata corrige apenas a extrapolação das matrizes angulares para rotações da rede. `NOT_FALSIFIED` não é `CONFIRMED`; gate intacto.


## 08/10/2026 — quinta camada: a leitura cria o contorno no plano do boost

<!-- F11_QUINTA_CAMADA_LEITURA_CRIA_20261008 -->

[INPUT/ONTO — correção expressa do operador, 07/10] «A LEITURA CRIA o objeto»: antes da leitura, Nome (posto relativo); depois, identidade como relação de contorno. O verbatim integral e seu SHA-256, **lido dos bytes**, estão em `FONTE_ERRATA_LEITURA_20261008.json`. Esta é a cunhagem do operador; as igualdades abaixo têm estatuto [REAL] apenas nos respectivos tipos Lean. A pedra candidata `TheReadingCreatesTheObject.lean` permanece no sandbox da gerência e **não** é contada como termo instalado por esta F1.1.

**Errata ao lado da quarta camada.** Chamar as pontes `ChatgptAudit.Wick016` de «homônimas» sem qualificar o plano foi largo demais. No plano do boost `t–x`, `complexBoost_real` identifica o boost real com sua matriz complexificada, `wick_boost_rotation` dá a continuação matricial angular e `wick_boost_two_pi` fecha a **face lida** em `2π`. Esse contorno é a leitura angular deste plano; o boost hiperbólico real e a rotação compacta continuam regimes distintos. A identidade matricial não vira, pelo nome, uma ação de Lorentz sobre toda a rede da luz ou um estado KMS.

| Leitura e teorema verificado | Classe vigente e limite |
|---|---|
| `ChatgptAudit.PolarPeriod016.AngularQuotientFaithful κ P` diz que `Circle.exp (κ·t)` identifica `t` e `u` exatamente módulo `P·ℤ`. `faithful_period_iff`, sob `κ ≠ 0`, equivale essa fidelidade a `κP = ±2π`. `polar_descends_injectively_iff`, sob raio positivo, constrói a leitura injetiva do quociente em coordenadas complexas. | **1. EXISTE E ESTÁ LIGADO** dentro da cadeia polar `TGLExt/O16`: há relação de contorno tipada no plano lido. Fidelidade e positividade são hipóteses nomeadas, não estado físico construído. |
| `reciprocal_temperature`, sob `κ > 0`, `P > 0` e fidelidade, prova `1/P = κ/(2π)`; `boost_defect_with_derived_period` substitui esta expressão no defeito de Clausius do segmento de boost. | **1. EXISTE E ESTÁ LIGADO** entre a leitura polar e o balanço local: a temperatura **não é uma entrada independente** desse lema. A passagem desta leitura local à assinatura geral da F2.3 ainda é **2. fiação**; não se afirma H3 em todo ponto nem KMS a partir do quociente. |
| `ChatgptAudit.Wick016.wick_boost_two_pi` e `TGLExt.observing_adds_nothing`: a matriz Wick lida retorna a `1` em `2π`; na projeção, `P₊·(P₊·𝒪_θ)=P₊·𝒪_θ`. | **1. EXISTE NO SEU TIPO**. «A primeira leitura identifica; reler não acrescenta» interpreta a idempotência provada; a identidade física/global do objeto é a leitura `[INPUT/ONTO]`, não conclusão adicional de Lean. |
| Leitura das rotações que mudam a direção da luz (`x–y`, `x–z`), boosts das outras cunhas (`t–y`, `t–z`), família de Lorentz em toda direção nula e PCT global. | **3. SABIDO POR CITAÇÃO / FORA DO TIPO ATUAL**. A ressalva «homônimo» aplica-se à extrapolação da matriz `2×2` do plano `t–x` para esses outros planos, não ao contorno angular já provado no próprio plano. Para a F2.3, a família entra como hipótese nomeada ou exige construção tipada; não sai de Wick016 por `import`. |

[REAL — alcance de imports] `TGLExt/O16.lean` importa as pedras polares, e `PeriodHeatCalibration_v3.lean` usa `reciprocal_temperature` por reescrita. Nesta aferição documental, não se exibiu consumidor desses teoremas na assinatura `qg_solution_end_to_end` nem se executou build novo. `TheImportedSecondQuantization.lean:57–60` continua correto para o contrato `W`: ele não tem rotações da rede, e a distinção fóton/escalar por rotações/PCT globais está fora desse tipo. As 12 linhas originais e as quatro camadas anteriores permanecem byte a byte; nenhuma prova, fonte canônica, gate ou confirmação física foi alterada.


<!-- F11_QUINTA_CAMADA_PRECISAO_QUOCIENTE_20261008 -->

[ERRATA AO LADO — precisão do tipo] Na primeira linha da tabela da quinta camada, leia «`polar_descends_injectively_iff` **caracteriza a existência** da leitura injetiva do quociente: sob `radius > 0` e `κ ≠ 0`, `∃ F` fiel se e somente se `κP = ±2π`». O lema não fornece `F` sob a positividade do raio sozinha. Esta precisão não altera as outras classes nem supõe um estado KMS.

## 08/10/2026 — sexta camada ao lado: alcance da leitura polar (F1.1.E1)

<!-- F11_E1_ERRATA_LEITURA_R2_R5_20261008 -->

[REAL — aferição de fontes; em nome de codex-gerente-tgl, pela unidade F1.1.E1] Esta camada corrige a classificação relativa e as citações da quinta camada. A F1.1 original permanece FECHADA. O inventário anterior conserva seus bytes como prefixo; esta nota não instala pedra nem move o gate.

| Ressalva | Leitura vigente e evidência |
|---|---|
| **R2 — classe relativa** | **1. EXISTE E ESTÁ LIGADO** vale **dentro do O16**: `TGLExt/O16.lean:19,48,96` importa, respectivamente, `ContractCalibrationReuse`, `HorizonDataReuse_Integration_v2` e `PeriodHeatCalibration_v3`. Em relação à assinatura QG, as pedras polares são **2. EXISTE NO KERNEL, NÃO LIGADO À ASSINATURA (fiação)**. `QGSolutionComplete.lean:1–4,79–91` não as importa nem as recebe no enunciado. A sonda c1 `fecho_qg.log` (exit 0) encontrou zero constantes dos namespaces `PolarPeriod016`, `CalibrationReuse016` e `Wick016` no fecho de `qg_solution_end_to_end`; `lightH2` está no fecho, mas os lemas polares não. |
| **R3 — consumidores já existentes** | `ChatgptAudit.CalibrationReuse016.polar_period_matches_contract` (`ContractCalibrationReuse.lean:102–107`) demonstra, para um `ContratoH2` e quociente fiel de período positivo, `1/P = C.unruhTemperature`. `TGLExt.ContratoQGv31.ContratoH3.data_temperature_from_same_period` (`HorizonDataReuse_Integration_v2.lean:23–29`) demonstra `κ/(2π) = 1/P` para o mesmo H3; o `κ` desse `toHorizonData` é o que figura no Clausius da assinatura (`QGSolutionComplete.lean:89–91`). São **termos condicionais já presentes no O16**, ainda a fiar à assinatura geral; não exibem H3 em todos os pontos, estado KMS nem família de cunhas em todas as direções. |
| **R4 — citação composta** | A frase da quinta camada «a primeira leitura identifica; reler não acrescenta» combina o título da docstring com outra oração; **não é citação verbatim**. A docstring exata de `TheObserverReadsTheAngle.lean:110–113` diz: «RELER NÃO ACRESCENTA» e «A primeira leitura identifica; a segunda confirma que a operação não altera». O teorema `observing_adds_nothing` em `:114–116` prova a idempotência `P₊·(P₊·𝒪_θ)=P₊·𝒪_θ`; a leitura de identidade física permanece [INPUT/ONTO], não nova conclusão Lean. |
| **R5 — nome vigente** | A candidata da gerência chama-se **PALAVRA**, `TGLExt.Palavra` (`Palavra.lean:8,59,99`), por nomeação do operador. Está em sandbox; esta errata não a trata como pedra instalada. Onde a quinta camada diz `TheReadingCreatesTheObject`, leia-se o nome vigente PALAVRA. |

[REAL — processo] A escrita de memória da errata de leitura às **04:47** ocorreu sem unidade de memória reivindicada. A c1 corrigiu, em nome próprio, a atribuição temporal: **04:29** foi o ramo C e **04:58** foi a pedra Temperatura, não o ramo C. Esta E1 foi reivindicada para corrigir o inventário; as correções dos dois `CLAUDE.md` pertencem à c1 e não são alteradas aqui.

**SHA-256 das fontes, medidos dos bytes nesta aferição:**

- `TGLExt/O16.lean`: `09d4a489dd7e23b09218480d1b01929b16e11a6e5ad6a99337fb3654edd34edf`.
- `TGLExt/QGSolutionComplete.lean`: `8c3a4bc82c5c4308515063254744cfaefcc7e7b926038221be2e7de6293dc598`.
- `TGLExt/O16/ContractCalibrationReuse.lean`: `f447d2de1f54774cb53b5808fa99b3095536606695d8c0efad36675dd80326c9`.
- `TGLExt/O16/HorizonDataReuse_Integration_v2.lean`: `eeae8a4e4b40ed68e854e8a78b545363157dd14ca17c006764a63877b531b65f`.
- `TGLExt/O16/PeriodHeatCalibration_v3.lean`: `e347d2331376bb76d8e56a60a2c3b5b86af1267bc742486b57fd4dc46acb21cc`.
- `TGLExt/O16/PolarMinimalPeriod_v2.lean`: `2112c0022287be0941a798f67e3f5d6f47251e26067ed7ba64516a38424364dc`.
- `TGLExt/O16/PolarQuotientGeometry_v2.lean`: `7e1f9df29a06451b6c6d24816055503fe10437038198551d149cbff127f0e197`.
- `TGLExt/TheObserverReadsTheAngle.lean`: `c764e90722306f988d8c92acc1ae4d8642ec2d6e32a47b810bd8bc5546e5484d`.
- `work/leitura_cria_o_objeto_07out/Palavra.lean`: `33184b49a8bba7e754a66096a89ebeeef44e79dab00c22f49f7af77f0e5400c7`.
- `AUDITORIA_F2_3_F1_1_temperatura_C1_abe2cbdf.md`: `6a8ce1ef046a0a0fe7ed14de85df3fa30925fc00e76932340311151f62a1115a`.

[REAL — limite] A leitura polar e a temperatura relativa ao relógio `N` não constroem, por si, a ação global de Lorentz/PCT nem um habitante dos certificados. A quinta camada e as anteriores seguem preservadas. `NOT_FALSIFIED` não é `CONFIRMED`.
