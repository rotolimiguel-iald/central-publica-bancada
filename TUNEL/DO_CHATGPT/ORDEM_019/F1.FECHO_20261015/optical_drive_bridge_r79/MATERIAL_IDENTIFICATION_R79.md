# R79 — identificação material OH → modos, superfície e gerador

**[DERIVED — candidato analítico/documental, NOT_LEAN]** r69_locality_bridge, 18/10/2026; F1.FECHO_20261015, reivindicação967/escopo983. Project e check R4 ready na revisão536, lease0ed9ed5e-f855-4788-8d99-33f533bbefd1, recibos AGENT_MATERIAL_*. Referência exata da missão preservada. Nenhuma execução científica, provedor, dado observado, memória, kernel ou produção alterados. As hipóteses abaixo delimitam uma identificação possível e verificável; não alegam aparelho calibrado.

## 1. O mapa recuperado existe parcialmente

| Objeto | Fonte / localização | Identificação recuperada e estatuto |
|---|---|---|
| Hamiltoniano OH/cavidade | Patente v2:356–370; INPI P79–80 | [REAL documental] ωc, ωOH, gJC e Ω já aparecem no mesmo Hamiltoniano. O termo de bomba é ℏΩ(σ++σ−), sem fator1/2. |
| Dipolo | INPI P337, extração R58:337 | [DECLARADO na fonte] dOH≈1,7Debye. O texto nomeia momento de dipolo elétrico, não identifica o elemento de transição vetorial d_eg de um par hiperfino/polarização selecionado. Não usar automaticamente o número como d_eg. |
| Orientação | INPI P173 e189 | [DECLARADO] Alinhamento dos dipolos sob o campo de micro-ondas já descrito. Não fornece distribuição angular, população de subníveis ou fator de polarização medido. |
| Geometria/material | Patente v2:684–738 | [INPUT de projeto] Cubo9cm, seis faces, eletrodos5mm, janelas25mm×5mm e portas780nm. Espessura do eletrodo/janela não é espessura da camada ativa OH. |
| Densidade e preparo | Patente v2:762–795; manual P87 | [INPUT/DECLARADO] Pressão parcial H2O, dosagem, RF e formação de radicais/gotículas propostas. Pressão de H2O não determina sozinha nOH, fração dissociada, população ressonante ou distribuição espacial. |
| Perda | Graviton.tex:350–353; patente:381–383 | [REAL documental] L_loss=√κ a e κ=ω/Q já escritos. Uma taxa de energia pode ser identificada com Q do MESMO modo; largura de amplitude tem metade dessa taxa na convenção D[a]. |
| Resposta e rede | R72 §§1–3; R77 §§3–6; R78 | Reaproveitar kernels/perfis, mapa livre normalizado, resposta material e quadro de fase. Nem uma Gram nem o nome do meio identifica automaticamente a região/dispositivo. |
| Dissipador conjunto | Patente v2:351–354 | λD[J], J=a_out†σ−+σ+a_in, com λ=βγΛ no contrato vigente. Sua textura comum não é substituída por dois dissipadores independentes. |

O Nós Vivo retorna unidade não indexada; MAP_QUERY.json recupera as rotas existentes. Não se reconstrói o grafo. A patente contém calibração histórica por ajuste de α₂:789–791; esta nota não adota esse procedimento para ajustar β. A regra vigente mantém β calculado em runtime, sem ajuste ao dado.

## 2. Acoplamento dipolar: contrato explícito e coeficientes

**[INPUT — H_DIPOLE_RWA]** Admitir, no regime especificado, dois estados moleculares |g>,|e>, frequência de transição ω0, aproximação dipolar elétrica H_int=−d·E, campo de modo de frequência real e aproximação de onda girante (RWA). O meio/banho devem justificar erros e faixa dessa redução. Estes são pressupostos nomeados, não resultados inferidos da existência da patente.

Para cada centro s, escreva

    d_s = d_eg,s σ+_s + d_eg,s* σ−_s,
    E_quant(r_s) = E1(r_s) a + E1(r_s)* a†.

Reter σ+a e σ−a† dá, por expansão do produto,

    H_JC/ℏ = Σ_s [g_s σ+_s a + g_s* a†σ−_s],
    g_s = −d_eg,s · E1(r_s)/ℏ.                         (1)

O produto é a contração do elemento de transição com o perfil complexo do campo por quantum; seu módulo inclui orientação, posição e fase. A fase de um único g pode ser absorvida numa escolha de base, mas a mesma mudança deve transportar bomba, salto J e leitura R74. Não remover fases relativas de vários centros/canais para forçar um único coeficiente real.

**[INPUT adicional, somente cavidade ideal]** Se o modo pertence a um meio não dispersivo, sem absorção, com εr real positiva e μ=μ0, escolha u com ∫εr|u|²d³r=1 e E1=i√(ℏωc/(2ε0))u. Essa normalização é uma convenção canônica de campo por quantum assumida no modelo ideal, não a normalização de um modo ressonante complexo de uma cavidade aberta. Sob ela,

    |g_s|² = ωc |d_eg,s·u(r_s)|²/(2ℏε0).             (2)

Para material dispersivo/aberto, manter E1 como perfil de acoplamento do modelo aumentado campo+banho, ou extrair os pacotes exteriores pela resposta R_D da R72. Não substituir a norma física por volume geométrico ou máximo do perfil sem demonstração. O mapa de Maxwell livre da R72 permanece apenas na região/domínio a que se aplica.

### Bomba e a convenção de fator2

Fixe um campo clássico monocromático real

    E_p(r,t)=Re[𝓔_p(r)e^(−iωd t)].

A mesma expansão dipolar/RWA dá

    H_p/ℏ=Σ_s[Ω_s e^(−iωd t)σ+_s+Ω_s* e^(iωd t)σ−_s],
    Ω_s=−d_eg,s·𝓔_p(r_s)/(2ℏ).                       (3)

No quadro adequado isso é a bomba complexa já transportada em R74. Para o Hamiltoniano ℏΩσx, a probabilidade excitada em ressonância isolada é sin²(|Ω|t); a frequência angular de oscilação populacional é2|Ω|. Assim chamar Ω de “frequência de Rabi” sem convenção não autoriza perder o fator2. Se a amplitude de campo for definida como parte de frequência positiva, em vez do fasor Re, o fator1/2 muda junto com a definição — não com a física.

Para a antena, uma identificação operacional é 𝓔_p(r)=√P_MW e_p(r), com e_p incluindo entrega, orientação, fase e resposta da cavidade. Ela requer resposta linear da cadeia de excitação e calibração do perfil; P em watts sozinho não a fornece. O quociente P/Pth da fonte não substitui e_p nem deduz a lei tanh. Não se iguala ωd, frequência de Rabi, taxa de relaxação e portadora óptica.

## 3. Muitos OH: modo brilhante e resíduo fora dele

O único σ da patente pode representar uma transição selecionada. Se representar um ensemble, é preciso mostrar qual redução o produz. No subespaço de zero/uma excitação molecular, com |G> todos no fundamental e |s> uma excitação no centro s, defina

    G=√Σ_s|g_s|² >0,   |B>=Σ_s g_s|s>/G.

Então H_JC leva |1_c,G> a ℏG|0_c,B>: o acoplamento coletivo é G, e a identificação é exata nesse setor. A bomba leva |G> ao vetor Σ_sΩ_s|s>, cuja componente brilhante é

    Ω_B = Σ_s g_s*Ω_s/G,
    ||Ω_dark||² = Σ_s|Ω_s|² − |Ω_B|² ≥0.             (4)

A desigualdade é Cauchy–Schwarz. Portanto há um falsificador concreto da redução a um único σ: bomba com componente escura relevante não é a mesma bomba de um só modo brilhante. Mesmo Ω_dark=0 não basta se detunings, dephasing ou interações diferentes misturarem B com modos escuros. Com várias excitações, o ensemble não é automaticamente um qubit; a invariância do setor/redução exige prova ou erro de aproximação. Não trocar por um oscilador ou por um σ sem declarar essa mudança.

No limite de descrição por densidade e distribuição de orientações,

    G² = (1/ℏ²)∫_V nOH(r) ⟨|d_eg·E1(r)|²⟩orient d³r. (5)

Esta expressão é a passagem de Σ_s para uma densidade assumida; inclui preenchimento espacial e projeção vetorial. Para uma camada fina, pode-se integrar na espessura para obter uma densidade superficial n_surf e uma integral sobre a face, somente se a variação de perfil/estado na espessura for controlada. A área de seis faces do cubo não substitui essa integral. Sob gás ideal diluído, nH2O=p/(kBT) é uma parametrização adicional; ainda precisa da fração que produz OH e da população da transição ativa. Não atribuímos números a essas frações.

## 4. Da resposta OH a uma superfície óptica: uma ponte derivada no regime declarado

**[INPUT — H_LINEAR_OH_SHEET]** Acrescentar: prova fraca, população estacionária diagonal w=p_g−p_e, coerência transversal com taxa γ2, transição isolada e regime monocromático/RWA. Este submodelo não substitui o resolvente do gerador completo R78 sob bombeamento forte.

Com s=<σ−>, a equação assumida nesse regime é

    dot s=−(γ2+iω0)s−i w Ω e^(−iωt).

Usando (3), a solução harmônica é

    s(t)=[w(d_eg·𝓔_p)/(2ℏ(ω0−ω−iγ2))]e^(−iωt).

Como o fasor da polarização é 𝓟=2nOH d_eg* s_amplitude, resulta

    χ_ab(r,ω)=nOH(r) w(r) d_eg,a* d_eg,b
              /[ε0ℏ(ω0−ω−iγ2)].                    (6)

É consequência algébrica do submodelo nomeado; orientações/distribuições de transições exigem média/soma. A equação conserva detuning, largura e força de oscilador, em vez de produzir automaticamente apenas uma fase exp(iωOHt). Havendo drive forte ou estado não diagonal, reutilizar a derivada/resolvente completo R78, com suas taxas e erro de corte; não forçar (6).

No limite adicional de folha elétrica fina, defina χ_sheet=∫χ dz, P_sheet=ε0χ_sheet E_t e, na convenção e^(−iωt), K_sheet=−iωP_sheet. Impostas as condições de contorno nomeadas E_t contínuo e n×(H2−H1)=K_sheet, resolve-se reflexão/transmissão para os meios e perfis especificados. Isso entrega um mapa explícito: transição/perfis/populações → χ → resposta de superfície → modos de saída. Não fornece por si a geometria correta da face OH nem transforma superfície molecular em parede macroscópica.

Em particular, coincidência dessa resposta com g_OH S_beta é um resultado a verificar, não a condição usada para escolher χ. A fase, a dispersão e as perdas materialmente obtidas precisam ser transportadas ao instrumento. Condições de contorno clássicas não demonstram o salto dissipativo J.

## 5. Taxas: identificações distintas que não se somam por nome

Para um único modo passivo sem drive, na convenção κD[a], a álgebra dá d<n>/dt=−κ<n> e d<a>/dt=−κ<a>/2−iω<a>. Se Q é definido como ω×energia/potência perdida do mesmo modo, κ=ω/Q, coerente com a fonte Graviton:352. Isso é o decaimento de energia; ajustar uma largura de amplitude sem o fator2 mede outra constante. As parcelas externa/absorção/espalhamento precisam ser discriminadas se a porta monitorada usa √κ_ext a; não usar perda total como eficiência de extração sem vínculo.

Para um qubit isolado com γ1D[σ−]+γφD[Z], γ2=γ1/2+2γφ, porque D[Z] multiplica a coerência por−2. Relações com T1/T2 requerem isolar esse modelo do drive e do acoplamento. Um linewidth observado de um sistema acoplado não é automaticamente γ1, γφ ou γΛ.

A densidade, espessura, dipolo e perfil podem determinar as combinações (1)–(6) quando admitidos; não determinam por mera dimensionalidade a intensidade e textura do banho que produz λD[J]. Γ_OH, nome histórico do fator de transferência da patente, γΛ do dissipador, γ_eff da desigualdade de regime e Ω do Hamiltoniano são objetos diferentes.

## 6. O peso que falta à microidentificação de J fica explícito

Ponham F1=a_out†σ− e F2=σ+a_in. O dissipador λD[F1+F2] corresponde, na base (F1,F2), à matriz de Kossakowski

    C = λ [[1,1],[1,1]],  λ≥0.                       (7)

A expansão de D mostra os termos cruzados F1ρF2† e F2ρF1†, e seus anticomutadores. A matriz é positiva de posto1 para λ>0; seus elementos cruzados saturam |C12|²=C11 C22. Dois banhos independentes com as mesmas diagonais dão C12=0 e outro gerador.

Logo uma derivação material precisa produzir uma matriz de correlação espectral de banho compatível com (7), a frequência/regime de redução e a ausência ou tratamento explícito dos demais canais e deslocamentos de Hamiltoniano. Um acoplamento microscópico assumido proporcional a (F1+F2)⊗B†+adjunto já insere a textura desejada: pode realizá-la no modelo Markov, mas não é sua dedução a partir do dipolo/parede. R66 já construiu uma realização reservatório→gerador; não refazemos essa realização nem a identificamos com OH pela igualdade de nomes.

O produto λ=βγΛ é o coeficiente do contrato vigente. Conhecer β não mede γΛ. Calibração coerente de g, Ω ou fase de transferência não determina as correlações dissipativas comuns. Esse é um resíduo material preciso, não falta de uma rede abstrata nem de uma fórmula de Lindblad.

## 7. Conclusão e cobertura

[DERIVED condicional] Foram explicitadas as relações de identificação material para gJC, Ω, acoplamento coletivo/preenchimento, resíduo escuro, susceptibilidade de prova fraca, folha de contorno e κ; o critério de banho (7) conserva o salto original. [OPEN] Faltam valores/perfis/populações/banho admitidos para aplicar essas relações ao MESMO aparelho, além dos erros de cada redução. As escalas RF-OH e luz780nm coexistem na patente; não se identifica automaticamente um modo óptico com uma transição de micro-ondas. Conversão mediada/Raman exigiria níveis, drives e balanço de frequências próprios, não acrescentados nesta rodada.

A normalização de uma função no espaço de Hilbert e a localização dos smears não determinam watts, espessura ou taxa. Reutilizam-se R71/R72 para a rede e R74/R78 para quadro/resposta. R4 não é fechado por este contrato.

Cobertura focal: patente v2 textual; extratos INPI/manual já custodiados R58, com hashes atuais dos DOCX originais e extratos conferidos contra o manifesto; trecho de perdas do artigo Graviton; R72/R77/R78. Consulta R67 sobre69 extrações/2414 parágrafos com os padrões no manifesto: zero hits depois de exigir palavra inteira para Rabi. Não é ausência em todo acervo nem leitura de fórmulas em imagens. Sem nova varredura de disco. Fontes/linhas/SHA atuais e os excertos efetivamente usados acompanham esta nota.
