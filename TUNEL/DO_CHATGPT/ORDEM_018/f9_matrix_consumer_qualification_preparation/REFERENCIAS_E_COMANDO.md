# Q01 — junção matricial e consumidor: preparação

Pedido ROOT29981416-d6fe-4d68-acff-46f88e8819fb; unidade Q01_MATRIX_CONSUMER_JOIN; identidade755c3b08-e8a6-448d-a7b1-1ec08d4dc7c7. [REAL documental] Identidade persistida antes do código, mapa637. Este pacote é preparação para revisão independente; não autoriza execução. Não houve importação de candidato/NumPy, cálculo de matrizes, solver, WSL, leitura de observados, instalação ou provedor.

## Escolha entre duas alternativas

**A — escolhida:** runtime Windows já instalado no bundle Codex. Leitura de METADATA informa NumPy2.3.5; WHEEL declara cp312-cp312-win_amd64; python312.dll e python.exe existem. O inventário registra hashes reais do executável, arquivos na raiz, DLLs, biblioteca padrão, NumPy, numpy.libs e dist-info, excluindo caches. O coletor usa C:\Python314 apenas para leitura de bytes, JSON e AST. Ele não inicia o Python do bundle. A presença dos arquivos não demonstra que a extensão nativa carregará; isso só poderá ser verificado numa execução distintamente autorizada. Não há alegação de fechamento completo das DLLs do Windows.

**B — alternativa documental:** runtime Linux /opt/lal_env descrito na linhagem já existente. Não foi iniciado nem repinado; requer transporte e admissão próprios antes de reutilização, sem reabrir c435/ffd6/NC02. Usá-lo agora acrescentaria dependências que a alternativa A evita. Um backend falso que apenas devolvesse a referência foi rejeitado: não verificaria a junção real.

Se a carga Windows, o posto, o prazo ou a precisão falhar, registrar falha consumida. Não instalar, alterar prior/tolerância, trocar runtime ou iniciar WSL como fallback automático. Um comando preparado não é prova de executabilidade.

## Menor recorte escolhido

Usar as fontes originais pinadas de prepare_joint, PreparedJoint.evaluate_five, integrate_at_fixed_theta, _Curve.__init__, FlatNuisanceGaussian, SupportGaussian e os dois serviços de precisão. O harness fornece o mesmo layout283linhas/63nuisance e os coeficientes X/a_h/c_C da especificação congelada. Não cria um segundo solver gaussiano de produção.

O pacote de previsões e o pequeno fundo são **fixtures sintéticos feitos pelo harness**. Não são recibos de CAMB ou execução do assembler. Os campos schema/status/pins necessários ao consumidor descrevem a interface exercitada; os documentos incluem HAND_CONSTRUCTED_NOT_A_SOLVER_EXECUTION e ASSEMBLER_NOT_EXECUTED. Todos os hashes de referências são calculados de bytes reais; nenhuma referência declara revisão independente que não ocorreu. A revisão da unidade é externa, pela ROOT. Não se pretende testar o produtor de previsões nesta unidade.

Um theta sintético comum (70;0,022;0,12) alimenta as cinco leituras, com E=exp(3) e I=(2/3)ln E. β_TGL é calculado em runtime a partir de ALPHA_FINE_CODATA_2018 do layout vezes √e; não é literal. Os extras de referência são β=0,01, s=0,02, rd=142. **Seus domínios integrais permanecem exatamente** β∈[−0,05;0,05], s∈[−0,15;0,15], rd∈[130;160]. O theta não é integrado nem estreitado: o recorte é explicitamente condicional em um único ponto sintético. A medida comum continua κdη; κ arbitrário é omitido igualmente, sem evidência absoluta.

## Construção e prova da referência independente

Seja X a matriz racional283×63 obtida exclusivamente das linhas estruturais congeladas, com a conversão para magnitude já prevista na fonte. Eliminação racional exata seleciona63linhas P com X_P invertível; seu inverso e determinante são obtidos sobre Frações. A preparação **não executa essa eliminação** nem anuncia seu resultado. O código futuro exige posto completo e limita numeradores/denominadores a16384bits. O resultado só pode ser aceito se essa exigência se confirmar.

Seja N a lista ordenada de linhas restantes. Defina Z inicialmente pelas colunas e_i,i∈N. Introduza uma cisalha R=I+(1/4)e_0e_lastᵀ nas coordenadas N; como as duas posições são distintas, detR=1 e R⁻¹=I−(1/4)e_0e_lastᵀ. A primeira linha N é CMB e a última é local; daí nasce uma covariância cruzada não nula entre domínios. Monte L=[X,ZR] e C_out=LLᵀ.

Na ordem P,N, L é triangular por blocos:

    L = [[X_P, 0], [X_N, R]],     |det L|=|det X_P|.

Para qualquer residual v, as coordenadas independentes são

    a = X_P⁻¹ v_P,
    w = R⁻¹(v_N − X_N a).

Sob v=Xη+Lε, ε gaussiano padrão, a integral dη elimina as primeiras63coordenadas, sem alterar a medida do restante. Assim, para r=283,

    log ∫L(v−Xη)dη = −(r−63)/2 ln(2π) − ln|det X_P| − ||w||²/2.

O oráculo calcula w por esse sistema racional conhecido convertido a float, não por eigendecomposição, SVD, pseudoinversa ou chamada ao backend candidato. Não reaproveita a normalização calculada pelo candidato. A referência analítica é independente quanto ao algoritmo; continua compartilhando os dados estruturais declarados, como deve.

Para o segundo fixture, retire somente a direção da linha2 (índice Python) da base Z. X é nulo nas primeiras16linhas. Todas as médias dos cinco modelos têm a mesma componente0,022 nessa linha. Portanto o suporte afim é v_2=0 relativamente à origem cujo componente2 vale0,022, e r=282. Nas coordenadas ortonormais da hiper-superfície, o mesmo argumento dá a fórmula acima com r=282. Não há mudança arbitrária da medida entre modelos do mesmo fixture.

**Limite deliberado:** essas covariâncias sintéticas não são as covariâncias físicas nem realizam os72vínculos determinísticos locais do cenário documental. Elas verificam o transporte/interface e a normalização nos suportes especificados, não o suporte efetivo dos dados da natureza, Q02/Q03 ou a integração I03 inteira.

Dados y são construídos como μ_H2+Lε com coordenadas racionais fixas; a origem tem componentes não nulas. Os inputs nativos são T⁻¹y, T⁻¹C_out T⁻¹ e T⁻¹origem. T contém exatamente os sete fatores5 da fonte. Verificam-se Ty, TCTᵀ, Torigem, estrutura imutável e normalização comum. A geometria usa todas as283linhas e os63nuisance, sem descarte de blocos.

## Referências dos extras

Para direção d e referência x0, use r=w(y−μ), v=w(d), a=v·v, b=r·v. Então

    logL(x)=logL(x0)+b(x−x0)−a(x−x0)²/2.

Os coeficientes são confrontados com os construídos por _Curve.__init__. H3 usa d=(I/ln10)a_h e densidade10 no domínio β original. H4 usa d=c_C e δ=−5log10(1+s), com densidade λexp(−λδ)/0,30, λ=ln10/5. Completar quadrados fornece primitivas em erf, com argumento e sinal independentes da chamada de precisão candidata.

H5 usa d_BAO=145×médiaBAO_de_base e zeros nas outras linhas; q=1/rd. A referência integra em rd original com Simpson composto fixo512painéis/513pontos, enquanto o candidato integra adaptativamente em q com seu Jacobiano1/(30q²). O oráculo ancora no máximo restrito da gaussiana; o integrando escalado é≤1 em aritmética real.

Com m=x0+b/a, z=max|1/rd−m|, R=130, limites das quatro derivadas do expoente são U1=az/R², U2=a/R⁴+2az/R³, U3=6a/R⁵+6az/R⁴ e U4=36a/R⁶+24az/R⁵. Logo |f⁽⁴⁾|≤U4+4U1U3+3U2²+6U1²U2+U1⁴. O erro da média Simpson é≤h⁴B4/180. A margem log é −ln(1−erro/média), exigindo0≤erro<média; se não satisfizer, há falha da referência, nunca ajuste posterior de regra ou malha.

A aritmética float e math.erf não são intervalares. Tolerâncias congeladas:2e−7 nas integrais pontuais/normalização;1e−6 mais resto independente e5e−11 de margem no confronto de priors; coeficientes2e−6 absoluto/2e−8 relativo; arrays2e−12 absoluto/relativo. São critérios de engenharia finitos, não cotas uniformes certificadas. Não se supõe convergência antes de medir: as seis chamadas positivas precisam devolver converged=true e ESTIMATED_NOT_CERTIFIED; uma recusa não é resultado físico.

## Cinco casos e orçamento

| Caso | Ensaio | Aceite |
|---|---|---|
| J01 | C positiva definida,283×63, covariância cruzada, três extras | Cinco log integrais pontuais e cinco médias condicionais concordam com referência; transformações e normalização conferem |
| J02 | C de posto282 e origem afim não nula | Mesmo confronto completo no suporte afim fixo, incluindo _Curve e três extras |
| J03 | Mesmo suporte282, y deslocado1/8 fora dele | Cinco resultados −∞ com estatuto de suporte, zero chamadas de precisão; não underflow |
| J04 | Média H1 deslocada1/8 fora do suporte admitido | AFFINE_SUPPORT_CHANGED, sem resultado parcial ou zero disfarçado |
| J05 | Troca dos dois primeiros identificadores de linha | ROW_ERROR antes de construir o backend |

Quatro tentativas prepare_joint; três construtores backend; sete entradas evaluate_five (incluindo as internas à integração); três integrate_at_fixed_theta; nove construtores _Curve; seis serviços de precisão reais. Tetos24586avaliações serviço/callback,8200leituras de curva e1026avaliações de referênciaH5. As contagens adaptativas reais são desconhecidas na preparação. O profiler identifica objetos de código e conta janelas; wrapper mede callbacks de quadratura e recusa nó repetido. Só nesta quadratura a duplicação de nós é verificada.

Matrizes têm dimensões fixas; referências exatas têm tamanho limitado e verificações de prazo. Um processo filho Windows oculto, sem shell e sem subprocesso científico. OPENBLAS/OMP/MKL são solicitados com uma thread pelo ambiente; não se alega medição ou imposição por JobObject. Não há hard cap de RAM/disco. Limites de shape/chamadas e128KiB por stream são critérios de aceite, não quotas do SO.

Prazo nominal120s desde main, validação antes do claim≤15s, worker cooperativo80s, espera externa90s e recolhimento5s. Leitura/pinagem do runtime ocorre antes e depois; custos reais e capacidade de carga serão medidos somente se autorizado. Não é execução em tempo real garantida. Uma falha antes do claim não roda ciência; claim parcial/existente ou output existente impede repetição. Resultado worker permanece provisório até terminal sem falha e exit0 do supervisor confirmado externamente.

## Custódia, comando e limites

driver.py exige ROOT_DECISION futura com schema Q01_MATRIX_CONSUMER_ROOT_DECISION_V1, identidade da unidade, hash real do manifesto, referência de revisão, authorize_single_execution=true e scope FIVE_SYNTHETIC_MATRIX_JOIN_CASES_ONLY. O exemplo de schema do contrato contém marcadores descritivos, não autorização. Não foi criada ROOT_DECISION, AUTH ou CLAIM.

Comando futuro, não executado:

```powershell
& 'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -I -S -B -X utf8 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_matrix_consumer_qualification_preparation\driver.py' --decision-sha256 '<SHA_REAL_DA_DECISAO_FUTURA>'
```

As fontes candidatas são compiladas de bytes conferidos, sem pycache; seus módulos e funções registram origem e vínculo ao NumPy carregado. Não é alegada identidade marshal entre processos. A limitação de serialização encontrada na unidade anterior4f5a é preservada; aquela unidade não é repetida para investigá-la. Os arquivos NumPy/Python inventariados são rechecados; DLLs do sistema e todo o estado do loader não estão certificados. O caminho site-packages só entra após decisão/claim; -S evita executar .pth/sitecustomize.

Este recorte não conclui Q01 integral, não testa solver/assembler, não integra theta, não valida C real, não substitui I02/guard/filesystem, não decide O01–O04, Q02/Q03 ou V1, não abre observados e não produz sigma físico. ReparoI02_99e2 e P3 seguem separados. Stack remoto inelegível por âncora/geração; nenhuma tentativa de repin ou execução. Ledger e memórias globais ficam sob ROOT.
