# Integração concreta do motor F9 à montagem H1–H5

[REAL — preparação estática] Pedido f07e4aba-e976-4d78-be1c-449968d4a305. Foram preparados configuração, cópias de fontes, wrapper, admissão de proveniência, supervisor Windows–WSL e contrato de uma futura avaliação de engenharia. **Nenhum instrumento candidato foi importado ou chamado; nenhuma avaliação CAMB, observação, ajuste ou significância foi calculada.** Scripts próprios de leitura, geração de arquivos, metadados e AST foram executados. Isso não é um controle numérico.

## O que foi ligado

`worker.py` → cópia exata de `background_controls.prediction_worker` → resultado de fundo e recibo físico → envelope `F9_BACKGROUND_PACKET_V1` → cópia exata de `assemble_five` → cinco vetores de283componentes e desenho nuisance separado. São16componentes CMB/BAO e267locais, com63colunas eta. O worker não implementa equações cosmológicas, não importa um.py e não chama main, validate, run_controls ou execute_worker_once do instrumento histórico.

O montador consumirá o layout já fornecido pela coordenação: ordem CMB R/l_A/omega_b_h2 e13BAO, terminando DH/DM em2,33. Alpha é extraído do mesmo artefato pinado e beta continua calculado como ALPHA_FINE_CODATA_2018*sqrt(e) no montador. Nenhuma fonte original foi alterada.

As cópias ficam em `sources/`. A cópia exata de RUNTIME_METADATA.json acompanha background_controls.py, porque runtime_check resolve esse arquivo em HERE. A configuração de origem foi guardada como PROTOCOL_ORIGIN.json para não confundi-la com EFFECTIVE_CONFIGURATION.json. O engine recebe explicitamente esta última, sem executar seu CLI de dez controles.

## Ponto e diferenças escolhidos antes de dados

O ponto usa quantis1/3,1/2,2/3 dos priors H0/ombh2/omch2, respectivamente. O script verifica que não é um dos cinco pontos do piloto anterior. MODEL_PARAMETERS.json registra os números gerados a partir dessas frações. Eles não são melhores ajustes nem parâmetros escolhidos para favorecer a TGL.

- H1: beta fixa pela regra canônica; H2: beta zero.
- H3: beta=1/40, quantil3/4 do prior diagnóstico.
- H4: s=3/40, quantil3/4 do prior de calibração; somente a coluna Cefeida recebe delta_C.
- H5: rd=275/2Mpc, quantil1/4 do prior de régua BAO.

Essas escolhas exercitam diferenças de interface. Não são escolhas finais para ajuste ou evidência, e não alteram os priors. Todos os modelos compartilham o mesmo theta nesta chamada; otimizações futuras podem ter theta diferentes.

As identidades esperadas são apenas especificadas: três coordenadas CMB iguais entre modelos; BAO H1–H4 iguais no mesmo fundo; resposta local H5 igual aH2; H4 atua somente emc_C. H1/H3 versusH2 diferem nas sete linhas locais de fluxo quando I*beta é não zero. H5 só difere em BAO quando rd livre é diferente do rdrag produzido. Não se exige diferença não nula se a igualdade algébrica pertinente ocorrer. Nenhuma dessas expectativas foi avaliada nesta preparação.

## Grade e orçamento propostos

A grade efetiva é **0 + sete zBAO únicos em ordem crescente**, provenientes do layout. Zero mantém válidas as verificações do engine E(0)=1, DM(0)=DV(0)=0; os treze componentes BAO continuam na ordem do levantamento, independente da ordem de avaliação das oito distâncias. Não há interpolação por vizinho.

Reutiliza-se somente o perfil reference já definido (AccuracyBoost2, tolerância de distância1e-7). Não é uma repetição baseline/reference ou dos dez slots anteriores. No futuro, o wrapper limita `camb.get_background` a uma tentativa, por um contador explícito ao redor da função original; a função é restaurada em finally. Chamada que falhe também consome a tentativa.

Os limites são nominais:180s totais Windows,140s de trabalho primário,110s de trabalho Linux incluindo preâmbulo/filho,25s para cleanup; um WSL primário, no máximo um WSL de cleanup, um filho e uma thread por biblioteca. Encerramento usa identidade exata e pidfd no Linux, handles próprios no Windows. Não é um teto rígido do sistema operacional nem uma garantia de tempo; exit externo e duração externa devem ser conferidos. Pico RSS é o reportado pelo engine; não foi imposto ou alegado um limite rígido de RAM.

## Identidade, isolamento de tentativas e autorização

UNIT_IDENTITY.json contém uma **identidade proposta nova**, diferente do pedido de preparação. CONTRATO_WSL.json fixa caminhos, pins, escopo e orçamento. A preparação não cria AUTORIZACAO_ROOT.json, CLAIM.json, RUN ou RESULT.json. ASSEMBLY_ADMISSION.json é somente o registro de proveniência esperado pelo adaptador; não é autorização para executar nem certificação de física.

Uma execução futura exige autorização específica ROOT ligada ao contrato e à revisão de integração, além dos pins de REVISAO_MONTADOR.json e REVISAO_TRANSPORTE.json. Esses dois arquivos são cópias dos recibos ROOT recebidos, com alcance preservado. A montagem foi aceita estaticamente; o transporte corrigido5b67 teve PASS stdlib em uma unidade própria. Isso **não** qualifica CAMB, imports científicos, caminhos de timeout, native, PE ou dadosD. A integração aqui preparada ainda precisa de revisão independente própria antes de qualquer uso.

A claim externa é criada exclusivamente antes do lançamento e permanece em sucesso, falha ou incerteza. O filho cria claim própria antes de verificar/importar o motor. Não há retry, sobrescrita de unidade consumida ou remoção de claim. O STOP persistente antecede cleanup e o mesmo launch gate impede que um supervisor atrasado abra novo filho. A construção de argv reutiliza PurePosixPath/as_posix do reparo revisado; paths de transporte Linux não são construídos por WindowsPath. O recibo guarda argv e identidade de processo.

## Runtime e diagnóstico específico

RUNTIME_INVENTORY.json foi obtido por leitura UNC de arquivos instalados, sem iniciar Python Linux ou WSL. Inclui stdlib, sysconfig e os pacotes CAMB/NumPy/SciPy, metadados de distribuição, dados auxiliares e bibliotecas nativas. O pin de versão/pacote do engine é preservado. O wrapper evita site/.pth sob -I -S e acrescenta explicitamente somente o diretório site-packages instalado e pinado.

A primeira coleta documental encontrou um alias do carregador ELF ilegível por UNC e terminou sem gravar o inventário. A coleta corrigida preservou a obrigação de conferência no Linux. O suplemento identificou bibliotecas candidatas pelo DT_SONAME, preservando backup byte a byte do inventário anterior. **Correspondência SONAME não foi declarada prova de resolução de symlink.** O worker terá de comparar no Linux o hash de cada alias com o candidato pinado antes do solver; qualquer divergência interrompe a unidade.

O worker verifica os arquivos pinados e, nos pontos de controle, identifica nome/caminho/hash de módulos efetivamente carregados e bibliotecas visíveis em /proc/self/maps. A lição NC02 foi incorporada: UNPINNED_IMPORTED_MODULE é acompanhada de módulo, caminho, fase e motivo; bibliotecas nativas têm diagnóstico equivalente. O inventário não é um traço dinâmico, e Python audit não observa todas as leituras/syscalls de código nativo. Não se alega sandbox de SO.

O audit latch é reutilizado em cópia exata. Operações de rede/processo, novas escritas e leituras existentes não pinadas são recusadas; callbacks do cálculo são interrompidos após qualquer latch, mesmo se uma biblioteca absorver a exceção original. As saídas são abertas exclusivamente antes do hook e escritas por descritores preabertos, com fsync. O journal é físico e sua sequência será conferida pelo supervisor.

O loader Python pode sondar caches ou metadados opcionais ausentes mesmo com -B. Sondagens de arquivo **demonstravelmente ausente dentro de uma árvore pinada do runtime** são registradas como ABSENT_RUNTIME_PROBE_NO_CONTENT. Arquivo existente sem pin, leitura fora dessas árvores ou qualquer escrita após o hook permanece recusada. Esse tratamento não promove uma falta de dependência real a sucesso. Há uma janela normal entre stat e open neste monitor cooperativo; não é proteção contra um adversário que altere o filesystem simultaneamente. O resultado exige as verificações posteriores de módulos/mapeamentos e não recebe certificado de isolamento.

## Saídas futuras e limites científicos

Uma execução válida produziria BACKGROUND_RESULT.json, ENGINE_EXECUTION_RECEIPT.json, BACKGROUND_PACKET.json e FIVE_MODEL_OUTPUT.json, além de CASE_RESULT, journal e recibos de supervisão/cleanup. O envelope refere o hash dos bytes do recibo real do engine, configuração efetiva e inventário de runtime; não apenas strings SHA sem objetos. O supervisor verifica os arquivos e sua correspondência com stdout/status do filho.

O resultado continua ENGINEERING_ONLY, com cota uniforme/certificado/sigma/lnB/chi2 ausentes. Não se exige uma cota global do CAMB para disponibilizar uma previsão de engenharia. Também não se transforma essa previsão em evidência de5sigma. A hipótese MM condicional e o transporte Ty/TCTt continuam obrigações do futuro consumidor de dados; não há y ou C observado nesta unidade.

As alternativas comparadas foram: A, reutilizar prediction_worker com configuração separada e supervisor externo novo (selecionada); B, escrever outro solver ou copiar suas equações (desnecessária e recusada). O próximo passo é revisão estática independente de **todo o pacote concreto**, especialmente runtime/sondagens, recibos, limites, identidade e casamento com a API aceita. Não se cria autorização de execução neste documento.

## Adendo de entrega: versão congelada sob revisão

A revisão independente iniciou sobre os 24 membros do MANIFESTO_PREPARACAO.json. Esta nota foi criada depois e é suplemento documental fora desse manifesto. Nenhum daqueles 24 membros nem o manifesto foi alterado nesta conferência final. O manifesto não deve ser regenerado durante a revisão.

Há uma diferença de metadados informada à coordenação: EFFECTIVE_CONFIGURATION.resources.timeout_seconds_per_worker conserva 100 s, enquanto o supervisor novo tem 110 s de trabalho Linux. O campo de 100 s é consumido apenas pelo antigo run_controls, que não é chamado; prediction_worker não o usa. O limite operacional está no supervisor/contrato. A diferença foi encaminhada à revisão sem editar silenciosamente o pacote congelado; uma correção requerida deverá constituir revisão explícita.

VERIFICACAO_FINAL_ESTATICA.json registra hashes, AST, identidade da configuração e ausência de autorização/claim/resultado. Também é suplemento documental, não recibo de execução do candidato. As obrigações de alias Linux continuam não executadas.
