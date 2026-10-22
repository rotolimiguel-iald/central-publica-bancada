# Revisão independente Q01 — nove casos dos serviços de precisão

[REAL — revisão estática] **Nenhum bloqueador material identificado para a execução futura e única do conjunto pinado.** O pacote prepara uma qualificação de engenharia finita dos serviços f820; este parecer não autoriza consumo, não afirma que os casos passaram nem certifica precisão uniforme.

[INPUT] Pedido revisado: d8aac6d3-7061-42fb-ae33-6e8b834b3de8. A rota foi consultada antes, no estado597. Manifesto de preparação, dez membros, candidata, runtime indicado e seis fontes contratuais foram conferidos por bytes. O snapshot inicial é preservado e a conferência final consta do recibo. Pacote examinado: f9_precision_qualification_preparation. Revisor independente: chatgpt-codex/ordem-018/proveniencia.

## Referências e alcance da qualificação

[DERIVED — álgebra, sem avaliação numérica] Os cinco casos da janela correspondem a integral exp(hz−Az²/2). W01 usa a identidade sqrt(pi)erf(1). W02 completa −z²−2z=1−(z+1)² e usa exp(1)sqrt(pi)/2·[erfc(1)−erfc(17)]; o sinal do deslocamento, os extremos e o fator1/2 são coerentes. W03 limita a média da exponencial entre exp(−d²) e1: ln(d)−d²≤ln(W)≤ln(d), d=2^−40. Não faz subtração estreita de CDFs.

Em W04, x=2^500z transforma A=2^1001 no mesmo integrando exp(−x²), com Jacobiano2^−500. Em W05, x=2^−500z transforma A=2^−999, com Jacobiano2^500. Os deslocamentos ∓500ln2 são corretos. As potências declaradas ficam representáveis no float usado; a referência não chama recenter, Fraction, helpers de escala/cauda ou a quadratura candidata.

P01 compara a integral de1+u³ a5/4. P02 preserva17 nós: quatro painéis iniciais, cada regra fina com quatro subintervalos elementares, dão Simpson composta sobre16 subintervalos em[0,1]. Seu resto clássico é limitado por e/(180·16^4), mais a margem float explícita; a saída candidata usa a regra fina, sem correção Richardson na área. A referência expm1(1) não reutiliza esse somatório. O caso exige converged=False para metas1e−30, enquanto P01 exige True. Não confunde valor positivo com meta atingida.

> [nota operacional do operador — omitida no retrato público]

[OPEN — resultado ainda não medido] Não foram calculadas referências nem integrais. Os nove casos exercitam interior, fronteira/cauda, janela curta, duas escalas extremas, quadratura positiva, não convergência e duas recusas. Não cobrem toda entrada admissível nem todos os erros. Um futuro PASS sustentará acordo nesses casos e tolerâncias de comparação, que são mais largas que algumas metas estimadas; não provará que o erro estimado é bound ou que a meta pedida é uma garantia externa. math.erf/erfc/log/expm1 compartilham o runtime float, não constituem referência intervalar certificada.

## Contadores, callbacks e profiler

[REAL — estrutura lida] Há duas chamadas de serviço em ramos mutuamente exclusivos de run_case, uma por caso, e nove casos em ordem fixa. W01/W02/W04/W05 têm contagem adaptativa desconhecida antes da execução; W03/P01/P02/N01/N02 exigem5/17/17/0/3. A soma dos tetos desses caminhos é16.433, sem contar álgebra racional, localização da cauda ou operações elementares como avaliações adicionais.

O profiler é instalado somente depois da referência independente e da leitura das entradas. Ele exige ausência de profiler anterior, filtra evento Python call, co_filename da candidata compilada e co_name=integrand. Na fonte pinada existe uma única definição integrand, aninhada no serviço da janela. _Samples.at chama essa função somente após a consulta do cache e o incremento do contador. Assim o filtro observa as avaliações que o recibo da candidata pretende contar, incluindo os dois lados, sem incluir a referência nem substituir o algoritmo. finally remove o profiler. Não há audit hook aqui: a observabilidade não depende da regra __cantrace__ encontrada na unidade anterior. Falha do profiler torna o caso FAIL; sua eventual desativação por exceção não produz PASS.

Para os demais casos o callback próprio conta suas entradas, recusa coordenada inválida e detecta nós duplicados. Recibos de sucesso são comparados com essa observação; tipos/status/error_kind/finitude/convergência são verificados. Uma falha inesperada é persistida e interrompe a sequência.

**Limite explícito de instrumentação, não bloqueante para esta fonte fixa:**16.433 é a soma dos caminhos pinados e condição de aceite. O somatório do supervisor ocorre depois de cada caso. N01 recebe orçamento16 e N02 recebe17, embora os resultados esperados sejam0 e3; o wrapper não é uma quota global antecipada contra uma implementação arbitrariamente diferente que engolisse exceções. Tal desvio reprovaria o caso. A fonte atual, lida integralmente, não possui esse caminho de repetição. Não reutilizar o contrato para outra candidata sem nova análise, nem apresentar o teto como confinamento universal de código alterado.

## Hashes, carregamento e auto-referência

O grafo relevante é acíclico: o manifesto fixa membros, contrato, candidata e aceite anterior; não se inclui como membro. O contrato não contém seu próprio hash nem o do manifesto Q01. O recibo estático é membro, mas seus pins tratam fontes anteriores/candidata/runtime. Uma futura ROOT_DECISION fixa o hash do manifesto já fechado e é externa a ele. O argumento CLI fixa os bytes da decisão. As marcas de execução e resultados não são entradas auto-referentes do manifesto de preparação.

driver.py:148–159 compila os bytes previamente verificados com filename explícito, dont_inherit=True e optimize=0, e os executa em ModuleType novo. Não depende de importar precision_services por busca de nome. As dependências são heapq/math/fractions stdlib; não há dataclass ou outra necessidade de registro desse módulo em sys.modules na fonte lida. Cases usa apenas math/sys/time. As funções exportadas são conferidas por globals e co_filename; hashes dos bytes e dos objetos compilados são persistidos. Arquivos são relidos depois do carregamento e ao final dos casos.

Isso liga os objetos ao código pinado no processo conhecido; não é autenticação criptográfica de um processo hostil nem sandbox de Python arbitrário. O pin de python.exe e as flags verificam esse executável/configuração, não todo DLL/stdlib transitivo. Nenhuma qualificação Linux/WSL ou científica anterior é transferida a este processo Windows. -I/-S/-B e o carregamento por bytes evitam dependência do diretório do pacote para localizar os dois módulos e não geram pycache da candidata.

## Consumo exclusivo e término

validate exige caminho fixo, Python3.14, isolamento/no_site/nobytecode, decisão específica e manifesto coerentes, fontes pinadas, nove casos e limites fixos. O template com FUTURE_* no contrato não é decisão executável. A ausência física dos nomes de decisão/claim/saída foi conferida nesta revisão; nenhum deles foi criado.

O supervisor cria RUN_CLAIM por O_EXCL antes de criar a saída e lançar o único Popen. Duas invocações concorrentes não consomem dois filhos: só a que adquire o marcador chega ao lançamento; a outra recusa. Mesmo uma gravação parcial deixa a marca. O filho valida nonce, manifesto/decisão e PID do pai e cria WORKER_STARTED por O_EXCL antes de carregar a candidata. Falha anterior ao resultado não libera replay. Raiz e diretório de saída são fixos; não existe argumento de saída alternativo.

A referência de revisão em ROOT_DECISION é validada como identidade/hash bem formado, não relida/autenticada pelo driver. A verificação substantiva dessa referência pertence a ROOT ao emitir a decisão. Isso é uma fronteira de confiança explícita, não prova de aprovação por forma JSON.

O relógio começa em main, antes da validação; os imports/inicialização do próprio supervisor antecedem esse ponto. Deadline cooperativo23s é transmitido ao filho; espera externa termina em25s; nominal30s inclui coleta/persistência/readback. Os pontos de observação cobrem callbacks, início/fim de caso, escrita de RESULT e os I/Os finais do supervisor. Operações entre checkpoints não são preemptadas pelo relógio cooperativo. Timeout sinaliza somente o Popen próprio, com coleta limitada; não há garantia de hard realtime/ausência absoluta de órfãos sob falha do SO.

O worker precisa sair zero e não ter WORKER_FAILURE. O supervisor exige RESULT e todos os nove recibos coerentes, caps, deadline e hash final. stdout/stderr são arquivos diretos com limite de aceitação pós-coleta64KiB, sem alegação de quota de disco. Após persistir TERMINAL_RECEIPT, há conferência de tempo, readback/hash, nova conferência e check depois de stdout flush. Se algum falhar, retorna não zero e tenta persistir FAILURE. Um PASS escrito ou emitido antes dessa falha continua provisório: aceite requer exit0 externo e ausência de falhas. Falha de disco não apaga claims. O pequeno intervalo após o último check e a saída do processo não é tratado como teto OS certificado.

## Parecer e custódia

[REAL — revisão somente] Fontes e controles de metadados/AST foram examinados; os checks registrados são de estrutura/pins, não execução dos nove casos. Nenhuma candidata, driver ou referência foi importada/chamada; zero backend, WSL, solver, modelo remoto, observados, AUTH/CLAIM. Nenhuma fonte congelada, memória compartilhada ou ledger ROOT foi alterado.

**Aceite estático restrito do preparo Q01.** A decisão concreta e eventual único consumo continuam com ROOT. A tarefa não precisa de campanha adicional para sustentar este parecer; eventual resultado futuro deve conservar a distinção entre qualificação dos nove casos e validade geral/estatística/física dos serviços.
