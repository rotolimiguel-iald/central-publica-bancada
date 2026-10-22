# Revisão independente Kerr22010M — preparação para E3.1

[REAL — revisão estática, custódia documental e controles sintéticos; INPUT — configuração; OPEN — ciência, execução e equivalência com a release]

Data: 2026-09-22T21:27:56.309732+00:00. **Nenhum bloqueante novo de implementação identificado no escopo exercitado. Preparação aceita para decisão do principal sobre execução futura controlada. E3.1 e a reprodução equivalente continuam NÃO PAGOS. Este parecer não é autorização de execução.** A ativação continua exclusiva do principal após B2/F0-stop, com autorização própria vinculada ao manifesto correto.

## Manifesto e preservação

Revisei os arquivos nomeados pelo principal em `bis/e3_pyring_preparation`. A primeira fotografia precede o sucessor; a fotografia final é `snapshot_002`. Manifesto operacional: **MANIFEST_v2.json**, SHA256 `e751c54cef54c4dfa7193fef925983a11182d44dae27b1b8080bbfa5f8246473`. O anterior permaneceu byte a byte preservado. Todos os 9 pins de código e os 31 pins documentais/configuração do sucessor conferiram com arquivos atuais. Nenhum HDF5/GWF foi aberto nesta conferência; os pins de strain dentro de CONFIG são herdados e sua verificação efetiva permanece obrigação do runtime autorizado.

A única dependência externa substituída no mapa anterior é `registration_guard.py`, agora `d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9`. Conferi os bytes; não reabri aqui a revisão semântica C3/marcadores E2. Em Kerr, modelo/condicionamento/CONFIG/PLAN ficaram byte-idênticos. A AST de controller/runner é a anterior após somente trocar referências fixas ao hash do MANIFEST antigo pelo hash de autorização já verificado. O seletor local novo recusa traversal, subdiretórios, versão zero, zeros iniciais, caixa diferente, sufixo de newline e tipos indevidos. O manifesto antigo recusa o código novo; a futura autorização deve nomear `manifest_filename: MANIFEST_v2.json` explicitamente.

Não executei `custody.verify` com autorização real, nem emiti JSON de status `CALIBRATION_ONLY_REVIEWED`. O manifesto é uma fotografia auditada, não prova de que E2/B2/F0 já autorizaram E3. Nenhuma escrita em e2_code, e4_e5_prepare, preparação Kerr ou insumos. Todas as novas evidências deste revisor estão em e3_pyring_review.

## Modelo, priors e convenções

[REAL — leitura das fontes] O INI publicado fixa céu, trigger de referência H1, t0=0,003369s, azimute zero, ausência de simetria não precessante e amplitude de referência10⁻²¹. Fontes pyRing2.7.0 foram comparadas por bytes aos seis membros correspondentes do sdist existente. Li as implementações locais de Kerr/default bounds/amplitudes, SWSH, damped_sinusoid, projeção e ruído. Do posterior de referência interpretei **somente o cabeçalho**, que contém oito parâmetros mais logL; seu hash foi conferido sem analisar valores.

Os oito priors em CONFIG são coerentes com essas fontes: Mf uniforme10–500M☉ no detector, af uniforme0–0,99, cosiota uniforme−1–1, psi uniforme0–π, dois raios uniformes0–50 e duas fases uniformes0–2π. Não são amplitudes cartesianas gaussianas nem raios independentes por detector. Não há novo ajuste de Mf/chif pelo remnant IMR ou cosmologia. A ausência de logdistance decorre de reference-amplitude explícita. t0 é fixo da configuração publicada: “10M” não é recalculado com cada Mf amostrado.

A soma finita independente da fórmula SWSH da fonte concordou com os harmônicos quadráticos usados para os dois ramos em cinco inclinações, incluindo polos. Um oscilador artificial, com frequência e amortecimento substituídos por constantes adimensionais, verificou fase ±, sinal da componente imaginária e supressão do ramo correto em cada polo. Os ramos permanecem complexos independentes; não se impõe conjugação entre amplitudes. Não gerei QNM ou waveform física. A fórmula de frequência/tau foi testada apenas com coeficientes e unidade de massa artificiais; os seis coeficientes Berti físicos e sua procedência foram lidos, não usados para criar sinais.

[OPEN] Identidade da versão executável da release não demonstrada. A convenção de harmônicos usada é a da fonte consultada, não uma declaração universal de convenção spin-weight. Não remover cosiota nem absorver harmônicos em amplitudes mantendo o mesmo nome de prior: isso alteraria a distribuição efetiva. A grande faixa Mf/af contém regimes próximos/fora da banda instrumental; o modelo não filtrado e o dado filtrado são limitação explícita da reprodução da receita2.7.0, não calibração física de todo o prior.

## Rede e atraso fracionário

`geometry` utiliza ArrivalTimeDiff(detector,H1) com o trigger e calcula resposta no trigger+t0+delay. O mock conferiu o transporte de delay fracionário; **o valor/sinal astronômico real do atraso não foi recalculado**. `prepare` seleciona a primeira amostra nativa cujo tempo relativo alcança t0, preservando o resto na avaliação do modelo. No controle sintético com atraso0,000123s, os tempos e restos dos dois detectores conferem com cálculo independente; não há arredondamento de atraso para um inteiro de amostras. N=819 e N/fs=0,199951171875s são distintos da duração nominal0,2s.

A likelihood recebe o mesmo conjunto de amplitudes/fases físicas em H1/L1, projeta com respostas próprias e usa tempos relativos distintos. Isso é coerência de rede. A técnica aqui é avaliação analítica em tempos fracionários; não foi realizado upsampling, filtro sinc, nem controle empírico de erro de interpolação do strain. Não apresentar o teste de plumbing como medição da qualidade do atraso real.

## Ruído, condicionamento e likelihood

O ramo Welch seleciona o primeiro bloco off-source aprovado por qualidade/finitude, antes do segmento e da exclusão temporal do evento, com Hann/50%/mediana corrigida. O helper E2 foi lido, seu pin conferido e foi substituído por mock no ensaio. A seleção não otimiza o posterior ou o nível do PSD. A ausência de sobreposição é garantida pelo contrato temporal do helper para os metadados recebidos; não inspecionei séries ou flags reais nesta revisão.

A potência do filtro filtfilt entra como |H|⁴ no PSD Welch. A escala ACF=(fs/2)irfft(PSD) foi testada com PSD branco artificial; Toeplitz/Cholesky deram a variância prevista. O controle da likelihood normalizada comparou duas matrizes3×3, soluções triangulares e expressão independente com inversa/determinante, incluindo os fatores da amplitude de referência. Concordaram. Não há marginalização/projeção analítica de amplitudes: continuam amostradas.

O mock de `prepare` exercitou a seleção nativa819, as duas ramificações PSD e o log-normalizador com dados zero e covariância branca artificial. O cálculo de condition number desse mock foi substituído por constantes para testar aceitação/recusa; **não foi medida a condição de nenhuma matriz819 real**. O código recusa condição>10¹²/NaN, não injeta jitter, e deixa Cholesky falhar. O filtro também foi substituído por identidade no mock de integração: sua estabilidade e vazamento real permanecem por executar. A hipótese de ruídos independentes entre detectores é INPUT.

Os dois textos públicos PSD foram hasheados, cruzados com PSD_EXTRACTION e verificados quanto a esquema/positividade/ordenação. Cada um contém16384linhas,819218bytes. Os extremos da extrapolação linear exigida pelo código são positivos; isso não certifica a covariância ou a qualidade do ruído. Não calculei ACF de PSD real. A interpretação dimensional como PSD vem do contrato do membro `pesummary/psds`; o cabeçalho genérico “Strain” sozinho não a demonstra. O ramo público reproduz a receita externa consultada, sem aplicar ali o fator de filtro do ramo Welch — diferença declarada, não ramos equivalentes.

[OPEN] Nenhum dos PSDs foi demonstrado idêntico a H1_PSD.txt/L1_PSD.txt da release; GWOSC também não foi demonstrado idêntico ao GWF C00_AR. Concordância posterior futura não apagará essas diferenças. Comparações de medianas, std, intervalos, KS e largura em quadratura serão descritivas do mesmo evento. Não são lnB, z calibrado ou evidência independente. A ponderação igual do posterior publicado mantém a ressalva de merging.

## Controlador, convergência e custo

[REAL — leitura e simulação] O envelope global inicia antes da verificação de custódia, é limitado a7200s e ao deadline/validade, e mantém diretório exclusivo que impede retomar e ganhar teto novo. A ordem é Welch→PSD público, com4800/1800s nominais e reserva15s. Child entra em sessão/grupo próprio; contexto confere pai/ticks/hash, e o runner confere descritores do log. Cleanup é chamado mesmo depois de o líder terminar. O helper E2 de cleanup foi lido e pinado; nesta revisão ele foi substituído por função que registra chamadas — **nenhum grupo real foi criado ou terminado**.

Quatro cenários de controlador com relógio/processos simulados: retorno zero, retorno3, timeout e falha de Popen. Houve cleanup para cada filho criado, ordem fixa e teto respeitado no relógio simulado. Falha/timeout não vira COMPLETED_REQUIRES_REVIEW na linha da variante. Isso não é benchmark nem garantia de tempo sob carga real. Os loops de hashing anteriores ao lançamento não têm interrupção individual; o tempo é debitado e, se acabar, impede lançar o child. Não anunciar que esses hashes podem ser interrompidos precisamente no deadline.

O sampler usa o adaptador E2 pinado, que verifica delta_logz antes dos live points, plateau/maxcall, ESS e tamanho posterior. Esta revisão não rodou nested sampling.512live versus4096publicados permanece INPUT declarado; convergência formal não certifica exploração de todos os modos. O custo por chamada e a estimativa de0,5–5ms do plano ainda são hipóteses de planejamento. Runtime deve medir antes de afirmar.

### Ajustes de relato recomendados, não bloqueantes do desenho científico

1. **KERR-N1:** em `kerr_model.py`, `guard()` vem antes de `self.calls += 1`. O mock de guarda expirada recusou uma entrada e retornou contador0. Descrever o campo como “avaliações iniciadas após a guarda”, ou mover incremento antes da guarda e adicionar retornos/exceções se quiser o mesmo significado de *todas as entradas reais* do contador PE. Não comparar diretamente esse contador com a fronteira PE-R3 sem explicitar a diferença. O custo global continua contabilizado pelo controlador.
2. **KERR-N2:** falha de Popen é propagada e COST é escrito, mas contém `runs=[]`, `cleanup=null` sem status/error próprio. Acrescentar `status`/`error_type` ao recibo global e registrar falhas anteriores ao lançamento melhora a auditoria. No código atual, `runs=[]` ou existência de COST **nunca** deve ser interpretada como êxito. Não houve filho órfão no mock dessa falha.

## Evidências e limites do parecer

- `FINITE_REVIEW_001.json`: 63 verificações sob `-O`; parede 0.402172s, CPU do pai 0.107577s. Mocks de física/LAL/Bilby/strain/processos; apenas álgebra e condicionamento artificiais.
- `MANIFEST_V2_INDEPENDENT_RECEIPT.json`: 71 verificações documentais/seletor sob `-O`; parede 0.345796s. Os controles do controller antigo transportam ao v2 pela equivalência AST explícita das únicas substituições de hash, não por uma alegação de rerun integral do v2.
- Duas falhas de fixtures próprias foram preservadas: assinatura errada do mock de resposta do detector e parser de cabeçalho que contou o marcador `#` como coluna. Corrigidas somente nesta pasta. Não eram falhas do produtor nem execuções científicas.
- Receipts, scripts e as duas fotografias estão ao lado. Nenhuma leitura de valores de strain/posterior, waveform física, PE, execução de E4/E5, instalação ou alteração de raiz congelada. A única leitura tabular real nova foi esquema/positividade dos PSDs autorizados.

**Disposição final:** ciência/código preparados no alcance documental e finito descrito; nenhuma nova autorização criada. O principal pode usar este parecer na sua decisão após B2/F0-stop. A diferença residual contra a release, custo real, convergência, posterior com hash e aceitação E3.1 só podem ser declarados após a execução autorizada e a revisão de seus produtos. Equivalência exata de fonte/strain/PSD continua OPEN separadamente.
