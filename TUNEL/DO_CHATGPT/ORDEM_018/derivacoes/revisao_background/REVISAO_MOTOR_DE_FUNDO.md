# Revisão independente do motor de fundo F9

[REAL — revisão documental e estática] O prior, a separação das escalas e as fórmulas do candidato são coerentes no escopo declarado. Há um reparo operacional pontual necessário antes do piloto: a entrada interna do worker inicia o solver antes de recusar um resultado já existente. A revisão não importou CAMB, não executou solver ou os nove controles anteriores, não leu vetores observados e não alterou o pacote.

Solicitação f132a1d5-7477-405d-963b-b1659db63328; mapa consultado antes, seq460. Autoria da revisão: chatgpt-codex/ordem-018/derivacoes. O recibo anexo identifica fontes e hashes medidos.

## Achados para a coordenação

**BG-01 — reparar antes de executar.** Em background_controls.py:203–207, a expressão write_new(output,prediction_worker(...)) avalia prediction_worker primeiro. O teste de existência está somente em write_new:28. Assim, uma reinvocação direta de --worker para uma saída existente executaria CAMB novamente antes da recusa de gravação. Esta conclusão vem da leitura do código e da ordem de avaliação de Python; nenhum solver foi acionado para demonstrá-la.

O caminho normal run_controls cria diretório exclusivo, é sequencial, possui limite de dez chamadas e não contém retry. Portanto o defeito é localizado na entrada interna, não prova de duplicação já ocorrida. A correção escolhida pela coordenação é reservar a saída/claim antes do solver e recusar saída ou claim prévio antes de qualquer chamada, incluindo unidade interrompida de resultado incerto. Isso pode ser conferido depois com AST ou stand-in sem CAMB, sem repetir ciência. O estado IN_PROGRESS atual fica apenas em memória até o fim; uma reserva persistente também deixa rastreável a tentativa interrompida. Nada foi reparado nesta revisão.

**BG-02 — correção documental ao lado.** A frase da linha31 de PARECER_MOTOR_DE_FUNDO.md sobre ausência das três bibliotecas no Python Windows deve identificar o ambiente/token consultado. O recibo já existente do preflight262 registra Python3.14.3, C:/Python314/python.exe e NumPy2.4.3 em Windows normal-user. A presente revisão releu esse recibo e seu hash; não repetiu o preflight nem sondou instalações. Esse recibo não certifica CAMB no Windows, e o candidato CAMB em WSL é um ambiente distinto.

## Prior, cobertura e escalas

[DERIVED — álgebra exata por Fraction] Na medida dH0 dwb dwc, a caixa [50,90]×[.015,.030]×[.080,.180] tem volume3/50 e densidade50/3; a integral do prior é1. Uniformidade nessa medida não se transfere sem Jacobiano a log H0 ou outras coordenadas.

A tabela histórica armazena11×21×21 nós; a máscara útil do interpolador T4 usa [60,76]×[.02025,.02475]×[.102,.138]. A fração do volume do prior é27/625=4,32%, não massa posterior. A tabela não fornece H(z), E(z) ou distâncias em baixo z. Falha de cálculo/cobertura dentro do prior deve interromper, como o protocolo exige; não pode virar likelihood zero ou normalização restrita à área computável. Os76.797 nós e3.071.880 bytes para cinco campos float64 da alternativa ampliada estão aritmeticamente corretos. A tabela ampliada não foi construída.

[DERIVED — sob o fundo plano candidato] O motor usa a mesma instância CAMBdata para H, E, distâncias e escalas acústicas, evitando misturar E analítico histórico com distâncias de outro fundo. DM=χ, DH=c/H e DV=(z DM² DH)^(1/3). A razão CMB lA=π DM(zstar)/rstar usa recombinação; BAO usa rdrag, associado a zdrag. R=√Ωm,0 H0 DM(zstar)/c inclui bárions, CDM e neutrinos massivos; a API distingue nu massivo de neutrino sem massa.

O INPUT z★_lei=1089,95 permanece separado de zstar derivado pelo solver. E(1089,95), E(zstar_CAMB) e I_lei=(2/3)ln E(1089,95) têm saídas diferentes. A troca do motor histórico por este fundo térmico deve continuar nomeada; não foi medida nesta revisão a magnitude dessa diferença.

## Neutrinos, BBN e recombinação

[INPUT — configuração candidata explícita] ΩK=0, w=−1, wa=0, TCMB=2,7255K; soma de massas.06eV em uma espécie massiva com hierarchy=degenerate, massa estéril zero e N_eff=3,046. O solver trata o fundo térmico massivo; a receita histórica que soma matéria mν/93,14 em todo z e uma radiação separada não é automaticamente equivalente.

A referência standard_neutrino_neff=3,044 implica ΔN=.002 no interpolador BBN. YHe=None utiliza consistência BBN com PRIMAT2024 explicitamente pinado; os eixos declarados wb[.005,.04], ΔN[−3,7] cobrem a proposta. Trata-se de cobertura e configuração, não de certificação física de BBN.

A escolha Recfast com aproximação planck é explícita. O default instalado é cosmorec; omitir a escolha mudaria a proposta. A tabela BBN e a aproximação de recombinação não foram demonstradas idênticas à geração histórica nem à prescrição da compressão Planck que vier a ser adotada. Essa compatibilidade já é condição expressa do pacote; não se exige aqui novo teste artificial. Dobrar AccuracyBoost não limita erros físicos comuns da recombinação. A API de distância em array realmente recebe tol, diferentemente da rota escalar local; o candidato usa a primeira.

## H5 e alcance do piloto

[DERIVED — candidato BAO-only] Com rd_livre uniforme[130,160]Mpc, densidade1/30, q=rd_livre/rdrag(θ) tem suporte condicional[130/rdrag,160/rdrag] e densidade rdrag/30. O Jacobiano está correto. O código troca somente o denominador BAO; mantém rstar/DMstar de CMB e não aplica resposta local TGL. Isso não constitui EDE nem uma aprovação científica de H5.

[REAL — leitura estática] Cinco pontos teóricos × duas precisões, uma thread e workers sequenciais; limite90s por worker e960s total, sem retry automático. Erro de retorno, timeout ou diferença acima do limiar interrompe o lote normal. Peak RSS será registrado, sem promessa de um limite rígido de memória que o código não implementa. Os controles E(0), DM(0), DV(0), positividade e monotonicidade são pertinentes.

[OPEN — já explicitado no protocolo] Quatro dos oito cantos e o ponto central não qualificam o prior inteiro; diferença≤1e−5 entre as duas precisões não certifica erro da evidência, erro comum de modelo nem regiões não examinadas. Não se produziu integral, S/g, ajuste, H0, lnB, veredito, aprovação física ou alteração de gate.

## Custódia e encaminhamento

[REAL] Os17 arquivos do manifesto, quatro fontes históricas referidas, três pins de entrada do protocolo e o pin do manifesto no FINAL_CHECK coincidem. A leitura independente do WSL conferiu38 arquivos CAMB e16 excertos de API sem importação do pacote. Esses hashes atestam integridade dos bytes consultados, não execução numérica correta. A tabela histórica foi apenas hasheada nesta revisão; vetores preditivos/centros não foram carregados.

A revisão estática é suficiente para os achados acima. Encaminhamento: preservar esta versão; produzir correção ao lado da reserva do worker e da frase de ambiente; conferir a recusa pré-solver com controle sem CAMB; só então a coordenação decide e identifica a unidade teórica limitada. Esta revisão não autoriza solver, grade completa ou composto observado.
