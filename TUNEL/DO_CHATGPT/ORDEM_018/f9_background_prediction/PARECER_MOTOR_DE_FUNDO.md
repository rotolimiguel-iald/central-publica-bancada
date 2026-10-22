# F9 — motor de fundo e cobertura do prior

Unidade `f132a1d5-7477-405d-963b-b1659db63328`. Entrega de preparação documental, 06/10/2026. Nenhum cálculo cosmológico, centro observado, fit, χ², evidência ou novo sigma executado. Não abre F9, não altera V1, originais, kernel ou gate.

## Recomendação

**Usar CAMB direto como candidato de referência, começando por cinco controles teóricos.** O protocolo e o código estão preparados para a coordenação avaliar antes de executar. Não há motor numericamente qualificado nesta entrega: há ambiente identificado, contrato explícito e código validado estruturalmente.

A tabela histórica não serve como cobertura do prior amplo. Metadados lidos do NPZ: 11×21×21 nós; eixos armazenados H0=[58,78], wb=[.020,.025], wc=[.100,.140]. O interpolador T4 admite somente as coordenadas entre o segundo e o penúltimo nó: H0=[60,76], wb=[.02025,.02475], wc=[.102,.138]. Nós externos são padding, não ampliação do domínio útil.

O prior comum candidato é uniforme independente, na medida dH0 dwb dwc:

- H0 ∈ [50,90] km/s/Mpc;
- wb ≡ Ωb h² ∈ [.015,.030];
- wc ≡ Ωc h² ∈ [.080,.180].

Seu volume nas coordenadas declaradas é 40 × .015 × .10 = 3/50; densidade 50/3 dentro da caixa, zero fora **por definição do prior**. A fração geométrica coberta pela tabela é (16/40)(.0045/.015)(.036/.10) = 27/625 = **4,32%**. Restam **95,68%** sem cobertura útil. Isto não é massa posterior, probabilidade da teoria nem medida do impacto na evidência.

O texto histórico T4 que admitia likelihood zero fora da tabela não é transferido para F9. Dentro do prior, falta de tabela, erro de recombinação, timeout ou falha numérica são **falhas computacionais visíveis**. Interrompem a qualificação; não se convertem em likelihood zero nem em novo prior normalizado sobre a parte computável. A uniformidade também depende da parametrização: trocar H0 por log H0 exige o Jacobiano correspondente.

## Fundo cosmológico explícito — candidato, ainda não ratificado

FLRW espacialmente plano, ΩK=0, constante cosmológica w=−1, wa=0, bárions, matéria escura fria, fótons e neutrinos térmicos. Parâmetros variáveis exclusivamente H0, wb, wc nesta unidade. O termo Λ fecha a densidade total no CAMB; não acrescentamos um setor TGL ao fundo nesta preparação R-A.

Parâmetros fixos propostos: TCMB=2,7255 K; Σmν=.06 eV em uma espécie massiva, hierarquia `degenerate`, zero massa estéril; N_eff=3,046; referência térmica/BBN `standard_neutrino_neff=3.044`. Portanto a tabela BBN é consultada em ΔN=.002. YHe é determinado por consistência BBN usando explicitamente `PRIMAT_Yp_DH_ErrorMC_2024.dat`. Seus eixos instalados [.005,.04] em wb e [−3,7] em ΔN cobrem o prior proposto; isso verifica cobertura da tabela, não precisão física de BBN.

Recombinação `Recfast`, aproximação **`planck` explicitamente selecionada**; τ=.054 fixo apenas para completar a configuração térmica, não como nova evidência. O pacote instalado usa por default a aproximação `cosmorec`; logo deixar o default implícito mudaria esta escolha. RECFAST é aproximação de recombinação; dobrar a precisão numérica não mede seu erro físico comum. Os demais defaults ficam presos aos hashes do pacote e serão registrados integralmente por `str(CAMBparams)` em cada controle futuro.

**Não se afirma equivalência exata com a configuração que gerou a tabela histórica.** O NPZ não armazena parâmetros/configuração do gerador. A pasta original Bancada_Um não pôde ser lida nesta unidade; usamos a cópia já custodiada. PRIMAT2024 e os parâmetros acima são um candidato explícito, não reprodução presumida de todas as hipóteses da compressão Planck histórica. A coordenação precisa compatibilizar o fundo escolhido com a likelihood/compressão CMB; em caso de diferença relevante, usar compressão compatível ou likelihood adequada, nunca alegar identidade por chamar ambos de ΛCDM.

A instalação consultada é `/opt/lal_env/bin/python`: CAMB 2.0.4, NumPy 2.5.3, SciPy 1.18.1. Só metadados, código-fonte local e hashes foram lidos; CAMB não foi importado. O Python Windows atual não contém essas três bibliotecas; o venv ringdown referido pela ponte antiga não contém CAMB. A evidência histórica de um runtime é um retrato, não prova do runtime presente. O manifesto de pacote contém também o binário CAMB e tabelas. Não constitui imagem hermética do sistema: bibliotecas externas e plataforma devem permanecer registradas numa execução futura.

## Quantidades distintas e unidades

Todas as previsões de fundo abaixo devem vir da mesma instância CAMB para cada θ:

- H(z) em km/s/Mpc e E(z)=H(z)/H0, com transição relativística dos neutrinos tratada pelo solver;
- DM(z)=χ(z) no caso plano, em Mpc; DH(z)=c/H(z); DV(z)=[z DM(z)² DH(z)]^(1/3);
- zstar e rstar derivados da história térmica/recombinação; DMstar=DM(zstar);
- zdrag e rdrag derivados do arrasto bariônico;
- CMB: lA=π DMstar/rstar e R=√Ωm,0 H0 DMstar/c, com Ωm,0=Ωb,0+Ωc,0+Ων,massivos,0 lido do CAMB;
- BAO padrão: DM/rdrag, DH/rdrag, DV/rdrag.

**z★ da lei ≠ zstar recalculado por definição.** Preservamos o INPUT histórico z★_lei=1089,95. O motor entrega separadamente E(1089,95), E(zstar_CAMB) e I_lei=(2/3) ln E(1089,95). Não substitui um pelo outro silenciosamente. Caso a coordenação escolha zstar variável para a lei, isso é outra especificação física a ratificar.

O E histórico de T4 aproxima Ωm com (wb+wc+.06/93.14)/h² e acrescenta radiação com N_eff=3.046. Isso trata a massa como matéria em todo z e a radiação pela receita separada; não é automaticamente o mesmo fundo térmico massivo do CAMB em z≈1090. Esta entrega identifica a diferença de prescrição, **sem medir ou inventar sua magnitude**. O candidato usa CAMB para H e todas as distâncias, eliminando a mistura entre essas duas prescrições. A passagem do motor histórico a este candidato deve ser nomeada na F9.

Domínio inicialmente solicitado para distâncias: 0≤z≤3; controles em [0,.1,.5,1,2,3]. Os pontos altos específicos são 1089,95 e os redshifts térmicos derivados. Não se qualifica aqui um interpolador geral até z infinito. Integrais acústicas do solver incluem seu tratamento de épocas anteriores. Nenhum espectro C_l ou P(k) é calculado nesta unidade; um teste completo de espectros CMB requer seu próprio contrato de perturbações/likelihood.

β_TGL não é ajustado nem substituído por literal neste motor padrão. A aplicação posterior da lei fixa usa α_CODATA2018×√e em runtime; β livre é modelo separado. Na rota R-A, essa operação se liga à resposta local especificada, não é autorização para reaplicar a modificação histórica de H(z) dos cronômetros em todo o fundo.

## H5 candidato: régua BAO livre, CMB padrão

Mantém H(z), DMstar e rstar padrão; troca somente o denominador BAO por rd_livre. Com rd_livre uniforme [130,160] Mpc, π(rd)=1/30 Mpc⁻¹. Se q=rd_livre/rdrag_CAMB(θ), o suporte condicional é [130/rdrag,160/rdrag] e π(q|θ)=rdrag/30. Uniforme em q com suporte fixo seria outro prior.

O código prepara as razões BAO em rd=130,145,160 sem novas chamadas CAMB. São controles teóricos, não três observações. H5 não altera a CMB, não aplica o fator local TGL e **não é EDE**. Continua proposta não ratificada; este documento não reabre a análise de nuisance já entregue.

## Protocolo curto — ainda não executado

Cinco pontos escolhidos sem dados: centro [70,.0225,.13] e cantos [50,.015,.08], [50,.03,.18], [90,.015,.18], [90,.03,.08]. Cobrem extremos de cada coordenada e quatro dos oito cantos; não demonstram acurácia em toda a caixa.

Cada ponto terá um CAMB com AccuracyBoost=1 e outro com AccuracyBoost=2. A distância usa a API **array** com tol=1e−5 e 1e−7: a API escalar local ignora esse argumento de tolerância. Controle inicial: diferenças relativas ≤1e−5 nas previsões listadas, E(0)=1, DM(0)=DV(0)=0 e distância monótona na grade. Os limiares são de engenharia; não garantem tolerância na evidência nem significância 5σ. Convergência comum das duas resoluções não detecta todo erro de modelo/recombinação.

No máximo dez chamadas sequenciais, uma thread, timeout 90 s por processo e 960 s totais, sem repetição automática. Registrar tempo por solver e por processo, parâmetros completos e pico RSS. RAM máxima não foi medida nem há limite rígido de RSS implementado; a medição de memória pertence ao piloto. Falha para o lote e deixa recibo explícito. O código não aceita vetores observados nem retorna likelihood.

**Preparação já realizada:** compilação sintática, validação do contrato e recusas de prior adulterado, ponto fora da caixa, NaN, expansão do lote, troca CMB→rd e BBN fora do suporte. Nove controles estruturais passaram, zero solver. Não é teste numérico do CAMB.

Para validar novamente, sem ciência:

```powershell
C:\Python314\python.exe -X utf8 .\background_controls.py --validate-only
```

Somente após revisão/decisão posterior da ROOT, comando proposto no WSL, ainda não executado:

```text
/opt/lal_env/bin/python /mnt/c/IALD/Central\ de\ Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_background_prediction/background_controls.py --run-controls --ack-root-review --output theory_controls_01
```

`--ack-root-review` registra a intenção do chamador, não substitui a autorização nem a revisão científica. A pasta de saída precisa ser nova. Falha ou resultado incerto não autoriza repetir sob outro nome. Ler o recibo primeiro.

## Alternativa: tabela derivada ampliada

Mantendo passos (2,.00025,.002), o prior exige 21×61×51 nós. Com um nó extra de cada lado para a máscara/stencil histórico, a grade teria **23×63×53=76.797** nós. Só cinco campos float64 ocupam 3.071.880 bytes, antes de eixos, metadados, distâncias/H(z) e validações. O custo dominante de geração não pode ser inferido desse tamanho pequeno: T≈76.797×tempo_medido_por_nó + controles. Não foi gerada tabela nesta unidade.

A tabela histórica contém apenas zstar,zdrag,rstar,rdrag,DMstar. Ampliá-la sem acrescentar H(z), E_lei e distâncias consistentes não resolve a mistura de prescrições. Uma nova tabela/emulador deve declarar campos, suporte em z, interpolação, padding, tolerâncias e controles independentes fora dos nós. Stencil de grau5 não garante positividade nem limite uniforme de erro por si só; domínio/cobertura não garante precisão.

Após o piloto, duas vias: (A) CAMB direto com cache por parâmetros+configuração+hash, se custo permitir; (B) tabela/emulador ampliado com referência CAMB e controles teóricos determinísticos de cantos/faces/arestas/interiores, refinamento orientado só por erro preditivo. Qualquer cache miss calcula pelo motor validado ou interrompe: jamais likelihood zero. A escolha depende do custo medido e do orçamento de erro do composto que a ROOT ratificar.

## Limites e entrega

O obstáculo de cobertura está localizado e quantificado; a solução executável está preparada, não qualificada numericamente. Faltam: ratificar configuração/prior/compressão; executar o pequeno lote autorizado em unidade posterior; estender a qualificação de precisão ao domínio inteiro e ao orçamento de erro da integral; escolher cache/tabela se necessário. Nenhum desses passos permite reabrir por inferência o composto observado.

Fontes e hashes efetivamente lidos: `SOURCES.json`, `TABLE_METADATA.json`, `RUNTIME_METADATA.json`, `BBN_METADATA.json`, `LOCAL_API_EXTRACTS.json`. Contrato `PROTOCOL.json`; código `background_controls.py`; controles `VALIDACAO_PREPARACAO.json`. Identidade integral em `MANIFESTO_ENTREGA.json`. Resultados de E45, PSD, desenho linear e medidas nuisance anteriores não foram recalculados.

<!-- F9_BACKGROUND_WORKER_FIX_f132a1d5_20261006 -->
## 06/10/2026 — Correção ao lado: worker reservado antes do solver e escopo de runtime

[REAL — revisão incorporada] Request f132a1d5-7477-405d-963b-b1659db63328. A versão inicial avaliava prediction_worker antes de write_new recusar uma saída existente; portanto a promessa de não repetir não estava implementada integralmente na entrada direta --worker. Não houve execução cosmológica naquela entrega. Fonte/manifesto/recibos anteriores preservados; código corrigido SHA256 c41aee4bcd1d8a137df8d7541e53738e68e9a77605ec8e51d4051459544265a2.

[REAL — correção] Claim exclusivo e persistente por request+hashdoProtocolo+ponto+precisão, mais reserva exclusiva do caminho de saída, ambos antes do solver. Sucesso, falha, interrupção e claim parcial não permitem retry. Claim sem terminal é incerteza visível. Treze controles stand-in passaram, incluindo entrada CLI direta, arquivo parcial, repetição com outro nome, concorrência e falha; três chamadas simuladas, zeroCAMB. VALIDACAO_WORKER_CLAIM.json. Não constitui validação numérica cosmológica.

[ERRATA — runtime] A frase anterior “Python Windows atual sem as três bibliotecas” excedia a medição. No subprocesso sandbox desta sessão, importlib.util.find_spec/importlib.metadata retornaram ausência de numpy/scipy/camb; isto caracteriza somente a resolução de módulos sob aquele token/ambiente. O preflight262 executado no ambiente normal do usuário registrou Python3.14.3 em C:\Python314\python.exe e NumPy2.4.3. SciPy não foi usado ali; isso não estabelece ausência nem disponibilidade de SciPy/CAMB no normal-user. Fonte lida: C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\derivacoes\preflight_262\PREFLIGHT_262_RESULT.json, SHA256 507c91dc51928fcb9e2b9f3a5f9ed0b3a5146570abd78a938f130abc97e31910. A existência em WSL /opt/lal_env é outra consulta independente. Mesmo executável não garante o mesmo sys.path/user-site/token. Nenhuma instalação/desinstalação realizada.

[OPEN] Configuração cosmológica continua candidata. Cinco pontos teóricos não executados. Revisão deste ajuste não autoriza F9 observado, solver ou nova grade. Manter leitura dos recibos e não repetir unidade incerta.

