# R87 — Contratos escritos de Ψ, matéria, ação e variação: ligação documental

Autor /root/r69_locality_bridge. [REAL — leitura, linhas, hashes] e [DERIVED — consequências tipadas abaixo]. Sem nova execução Lean, sem novo modelo material escolhido. Missão própria revision569, preflight ready=true. Escopo: fontes principais já inventariadas R58, remissões pertinentes de setembro, kernel atual e as 69 extrações existentes R67. Não é varredura de todo o computador.

## 1. Âncora corrente e precedência documental

O um.py corrente mede SHA256 18be2ddb06c60f9037b1efecb72034e6a0c9409b0d3900452fd9d186cf4905c0 e coincide com o selo de 14/10/2026 18:11:50, o pacote v393 referido no baseline R58. O programa não foi executado. A fonte SectorFluidClosure embutida em um.py:127532 coincide BYTE A BYTE com o arquivo do kernel. As demais fontes formais foram lidas diretamente; esse controle não afirma igualdade de todos os módulos embutidos.

A precedência usada é explícita: a definição tipada governa o objeto do respectivo teorema; a nota ambiente de09/09 governa a construção que ela declara [INPUT]; a correção de17/09 governa a interpretação de ψ/agente e recusa identificações nominais; o consumidor v370 ainda presente no programa selado governa o alcance da ligação Cartan. Nenhum desses textos declara que a ação ambiente sigma substitui toda a ação do Custo. Atualização de data ou palavras iguais não cria revogação ou identificação matemática. R83–R86 são candidatos recentes desta missão e não alteraram essas fontes canônicas.

## 2. Matriz dos contratos encontrados

| Objeto / fonte e linha | Contrato efetivamente escrito | Ligação sustentada / pendência |
|---|---|---|
| Custo, tgl_paper_unified.py:10317–10345; publicado paper_PT.tex:145–175 | Soma matéria+campo+grav+modular. Matéria contém Dirac, Yang–Mills, escalar Higgs. Campo tem −¼Φ², Φ_mu,nu=partial_mu Ψ_nu−partial_nu Ψ_mu; texto chama Ψ de escalar. | Fórmula requer uma 1-forma; rótulo escalar não lhe fornece índices. Não foi especificado o mapa de um escalar para essa 1-forma. |
| Custo:10349–10384 | +[1/(2κ²)+ξ|Ψ|²]R, ξ=1/6; L_mod=L_LCDM β|1+w_eff(z)|. | Não especifica em tais trechos R(g) versus conexão independente, a contração de |Ψ|² para uma 1-forma, nem L_LCDM[g,campos] e w_eff fora do fundo. Não autoriza substituir L_LCDM por −ρ sem nomear a hipótese. |
| Custo:10418–10460 | Enuncia (Box−m²−ξR)Ψ=βK_partial Ψ e distingue conjectura de identificação operatorial plena. | É uma EOM declarada escalar. A cinética −¼dΨ·dΨ da 1-forma produz equação vetorial; a forma Klein–Gordon exige um fornecedor/identificação adicional. |
| Ponte.tex:832–880 | Fonte candidata P_mu,nu=+2/sqrt(−g) δ<K>/δg^{mu,nu}, marcada CONJ; camadas e regime modular. | Fixou o sinal da candidata modular, não um tensor Hilbert derivado da ação completa nem o funcional métrico do estado/K. |
| Ponte.tex:1045–1064 | Regime de assinatura com direção outer negativa, sombra diag(−,+,+,+). | É convenção/operação da reconstrução ali. Não transplantar sinais à carta SelectedMetric (+---) sem mapa e transformação da ação. |
| SelectedProbabilitySigma.lean:41–51,104–108,133–150 | s=P_selected; φ_j=sqrt(P_j/(1−s)), Σφ²=1; covetores dφ_j; recordMetric=selectedMetric P e source=finiteCovectorStressField desses dφ. | Same-P real já construído. φ é aplicação em esfera, dφ família de 1-formas exatas; não é definição de Ψ_nu do artigo. |
| SelectedFisherGibbsBridge.lean:41–70 | Outra fonte same-P usa covetores dP_i. | Covetores e métrica compartilham P, mas essa fonte não é idêntica à sigma condicionada por mera notação. |
| AbsoluteOne.lean:10–26,63–90; PsiEmergence:24–47 | Ψ algébrico é regra região→densidade positiva, absoluteOneField escolhe I/n; vetor GNS I/sqrt(n). | Não é um campo escalar em M nem um covetor. A unidade normalizada e a amplitude radial livre são tipos diferentes. |
| OPERADOR_JACOBI_GAUGE_E_ESCOPO.md:7–30,338ff (09/09) | Ação ambiente ESCOLHIDA: −1/(2κ)∫(R−2Λ)+c/2∫g^{-1}(dφ,dφ); φ:M→S³; (+---); g e φ independentes. | Contrato concreto do ramo quantizado; fundo a(r)=2cos(r/2), κ=4/c, Λ=3/4. A nota distingue expressamente ambiente dos cinco pesos, cujas variações são difeomorfias. |
| IDENTIFICACAO_PSI_SIGMA_E_TORSAO.md:3–9 (17/09) | Se literalmente ψ=φ com mesma norma1, F=F0+ξ constante ⇒ Cartan sem spin tem torsão zero. | Ligação negativa já derivada; não refazer como achado novo. Norma radial/novos campos alteram o modelo, não são fiação. |
| ADENDO_PSI_AGENTE_E_IDENTIDADE_20260917.md:5–9,29–35 | ψ é campo de sustentação; não substituir por J, densidade ou fóton pelo vocabulário. Ação ambiente g,φ independentes. | Corrige interpretação, não fornece Ψ(P) ou nova ação física. |
| um.py:216279–216293,216469–216480 | Cartan fornecedor condicional; identificação ψ escalar livre / forma Ψ_mu / φ norma1 e Cartan versus métrica permanecem INPUT. | No pacote corrente esse resíduo é EXPLÍCITO, não concluído pela existência de um ramo. |
| SectorFluidClosure:21–41; SectorFriedmann:22–48 | w_i constante, não troca H_nx e fonte corrigida; conservação FLRW; H_null entrada. | O completamento de correntes R86 é condicional útil, mas não há nessa estrutura campo que identifique essas correntes com P/Ψ. |
| um_absoluto_pt.tex:302; TheVerbSelectsTheAction.lean:122–130 | action_locks_zero_iff seleciona núcleo; S=∫L d4x ainda OPEN no texto selado. | Ação de operador não supre estacionariedade gravitacional. As novas derivações R82–R86 são camadas candidatas distintas. |

## 3. Ligações que se podem fazer sem escolher outro modelo

### 3.1 O ramo ambiente tem sinais definidos; troca global não resolve seu residual

A ação de09/09 é −EH+sigma positivo, incluindo Λ. O seu negativo GLOBAL é EH−sigma, incluindo o termo cosmológico correspondente: δ(−S)=−δS, portanto os pontos estacionários são exatamente os mesmos. Isso é o contrato reduzido empregado em R85, com o Λ separado ou recolocado. Trocar globalmente a convenção não apaga o residual encontrado. Trocar somente o sinal de uma parcela muda a equação e o modelo.

O artigo Custo com +EH e as cinéticas escritas não fixa sozinho a tradução de todas as convenções da carta +---. A declaração do operador em um_absoluto_pt.tex:1024 distingue acoplamento negativo e geometria positiva; o consumidor OrientedFace trata o sinal da resposta entrópica/fator cosmológico condicional. Não é uma derivação de que todos os sinais Hilbert da ação completa já estão conciliados.

### 3.2 Honrar a dimensão do campo efetivamente escolhido

O ramo ambiente tem φ em S³⊂R⁴. Sua parametrização sigma condicionada usa quatro componentes, portanto cinco probabilidades no modelo mínimo. O tipo formal SelectedProbabilitySigma aceita outros J, mas a testemunha livre P16 de R85 usa quinze componentes condicionadas, alvo S14. A existência/rank normal10 ali é um resultado sobre uma classe maior; NÃO constitui o mesmo campo físico S³ da quantização09/09. Não transportar Hadamard/Jacobi do alvo S³ para S14 por nome.

### 3.3 Uma tentativa de identificação escalar→1-forma tem consequência verificável

Se alguém escolhesse Ψ_mu=partial_mu ψ para um escalar suave, a expressão EXATA do Custo daria Φ_mu,nu=partial_mu partial_nu ψ−partial_nu partial_mu ψ=0. O mesmo ocorre com cada covetor dφ_j do fornecedor sigma. Esta consequência é independente da conexão porque o artigo escreveu derivadas parciais/exterior d; torsão não faz d² diferente de zero. Logo essa identificação particular não produz a cinética Maxwell não trivial pretendida. Uma conexão com curvatura não nula, campo potencial independente ou outro mapa teria de ser fornecido. Não se conclui que todo mapa escalar→gauge seja impossível, apenas que gradiente puro não resolve esta ligação.

### 3.4 Diferença entre norma escalar e norma de covetor importa já na variação

Se u=|ψ|² é norma de campo escalar independente da métrica, δ_g u=0. Se u=g^{ab}Ψ_a Ψ_b com covetor fixo, δ_g u=Ψ_a Ψ_b δg^{ab} (ou parte real hermitiana no complexo). Portanto variar ξuR gera uma parcela algébrica adicional ξR Ψ_aΨ_b no segundo caso. R83 já formalizou a distinção de densidade local; não se pode escolher u independente e afirmar que resolveu o caso Ψ_mu. Se ψ=φ unitário com norma alvo, u=1 e dF=0: o caso Cartan não minimal se reduz ao fornecedor sem torsão, como a nota17/09 já prova.

## 4. Acervo R67 e limite da recuperação

Foram consultadas as 69 extrações JSON previamente guardadas, 2414 parágrafos, sem reextrair documentos. Busca focal por lagrang, variacional, covetor, escalar, Einstein.Hilbert, não-mínim/nao-minim e rho(n) retornou zero parágrafos. Os hashes de TODAS essas extrações e o padrão estão em SEARCH_AND_CANONICAL_CHECK_R87.json. Não significa que os documentos não tratem Ψ, identidade ou permanência; significa que esta busca não localizou a especificação variacional necessária neles. Não foi feita afirmação de ausência em todo o acervo.

## 5. Contrato recuperado para continuar

[DERIVED documental] É possível continuar o ramo já escolhido Einstein–sigma S³ com seus sinais, variáveis independentes e fundo específico, sem inventar outro Lagrangiano. [OPEN] Sua restrição same-P P5 é só órbita de difeomorfias e não fornece variações livres; ampliar para P16 muda o alvo. [OPEN] A ação completa do Custo ainda exige o mapa tipado de Ψ, o funcional material modular fora do fundo e a compatibilidade com a fonte do MESMO P. O próprio um.py corrente conserva essas escolhas como INPUT e não há, nos trechos examinados, revogação explícita que selecione uma delas. O trabalho novo deve preencher essa ligação preservando os contratos encontrados; uma candidata mais simples não os substitui.
