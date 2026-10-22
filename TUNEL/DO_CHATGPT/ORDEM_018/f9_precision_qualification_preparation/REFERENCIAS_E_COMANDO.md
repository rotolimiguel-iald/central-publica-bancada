# Q01 — preparação da qualificação dos serviços de precisão

[INPUT] Unidade nova d8aac6d3-7061-42fb-ae33-6e8b834b3de8, preparada por ordem de ROOT. A identidade foi persistida antes do código. [REAL — preparação estática] Nenhum serviço, referência numérica, controle ou solver foi executado. A entrega requer revisão independente de proveniencia e decisão posterior de ROOT.

## Recorte finito e alternativas

São nove chamadas de serviço, uma por caso, em ordem fixa. A alternativa escolhida combina identidades analíticas e referências stdlib independentes com um pequeno conjunto de falhas discriminantes. A alternativa de uma segunda quadratura geral ou varredura de alta precisão foi descartada: acrescentaria outro estimador/campanha sem ser necessária para este recorte. Não há retry, fallback ou ampliação automática.

Os cinco casos de janela exercitam três geometrias e duas escalas extremas representáveis. W02 tem intervalo amplo para exercitar a localização e contabilização da cauda antes do endpoint finito. Não são dados cosmológicos nem uma nova avaliação dos controles de df482: o alvo é a implementação recém-preparada f820. A candidata permanece read-only.

> [nota operacional do operador — omitida no retrato público]

O teto observado global é **16.433 avaliações**, nove chamadas de serviço. As contagens das quatro janelas adaptativas não são fingidas como conhecidas antes de rodar: seus tetos são exatos e as contagens reais serão medidas. Nos outros casos, a contagem exigida já é fixa. Não há chamadas para estimar custo nesta preparação.

As tolerâncias independentes de comparação estão congeladas em CONTROL_CONTRACT.json: W01/W02 3e−8 no log; W03 3e−11 mais a largura analítica d² do intervalo; W04/W05 3e−7; P01 1e−13. P02 usa a majorante clássica de Simpson composta e/(180·16^4), mais 1e−13 para arredondamento. Esses limiares não serão ajustados após olhar resultados.

## Por que as referências são independentes

[DERIVED] Por definição, integral[−1,1]exp(−z²)dz=sqrt(pi)erf(1). A conclusão de W02 decorre de completar o quadrado: −z²−2z=1−(z+1)², com erfc em argumentos explícitos1 e17 (a diferença fica dominada por erfc(1), sem cancelamento estreito). Isso não usa recenter, Fraction, seleção de escala, regra adaptativa ou helpers da candidata.

Para W03, em 0≤z≤d vale exp(−d²)≤exp(−z²)≤1. Integrar e tomar log dá o intervalo usado, sem subtrair CDFs quase iguais. W04/W05 fazem a mudança explícita x=2^500 z e x=2^−500 z, respectivamente: os Jacobianos produzem ∓500ln2. Assim a referência não calcula numericamente a integral extrema.

A primitiva de 1+u³ é elementar. Em P02, o teto mínimo conserva a regra fina composta em16 subintervalos elementares iguais; a fórmula de resto |erro|≤(b−a)h^4 sup|f^(4)|/180, com f^(4)=exp(u)≤e, fornece a comparação independente. A meta1e−30 exige deliberadamente o ramo de não convergência; retornar uma área positiva finita não equivale a atingir essa meta.

math.erf, erfc, log, expm1 e constantes stdlib continuam implementações float. Estes casos não certificam uniformemente funções especiais, arredondamentos ou toda a API. As saídas conservam tanto a diferença para a referência quanto o erro estimado da candidata, sem afirmar que esse estimador seja um bound.

## Contagem, isolamento lógico e carregamento

cases.py observa as chamadas Python do integrando interno das janelas via sys.setprofile, filtrando co_filename da fonte pinada e o nome da função. Restaura o profiler em finally e exige ausência de profiler prévio. Isso conta avaliações efetivas sem monkeypatch, alteração de bytecode, substituição do algoritmo ou confiança exclusiva no campo evaluations. O overhead de observação pertence a esta qualificação; não será vendido como benchmark de produção.

> [nota operacional do operador — omitida no retrato público]

driver.py compila e executa somente bytes pinados de precision_services.py e cases.py, em módulos novos, depois do consumo. Registra os hashes dos bytes, dos objetos de código compilados e das duas funções exportadas, com co_filename/globals conferidos. Não faz busca de módulo no path nem escreve pycache. Os bytes são relidos após o carregamento e ao fim. Esse atesto liga o código carregado ao pin; não é uma sandbox contra um arquivo Python arbitrário adulterado fora do contrato.

Python normal do sandbox: C:\Python314\python.exe, versão3.14, com -I -S -B -X utf8. Só stdlib; heapq/fractions/math são as dependências concretas da candidata. Não há WSL, CAMB, NumPy, SciPy, rede, consumer, theta, fontes científicas executadas ou observados. Um supervisor e um único filho puro; nenhum descendente adicional é lançado pelo código pinado.

## Consumo e término

ROOT_DECISION.json **não é criado nesta entrega**. Seu schema está descrito no contrato; futuramente deve vincular request_id, unidadeQ01, manifesto inteiro e referência da revisão independente, autorizar explicitamente uma execução e restringir o escopo aos nove casos. A chamada também exige o SHA real desse arquivo por argumento. O manifesto de preparação permanece PREPARATION_ONLY; a decisão futura é um documento separado.

RUN_CLAIM.json é criado por O_EXCL antes de lançar o filho. A raiz/saída são fixas, sem opção de outro nome para contornar replay. O filho confere nonce, PID do pai, decisão/manifesto e cria WORKER_STARTED.json por O_EXCL antes de carregar a candidata. A tentativa não é retomada por ausência de resultado: claim sem terminal é consumo incerto, preservado.

O orçamento nominal é30s a partir da entrada main do supervisor: inclui validação, inicialização do filho, trabalho, coleta, persistência e readback final. A inicialização/imports do próprio supervisor antecede esse relógio. O filho tem deadline cooperativo23s; o supervisor espera até25s e reserva o restante para terminar/coletar seu único filho e persistir. Não há promessa de hard realtime do sistema operacional. Em timeout só é sinalizado o Popen filho próprio; qualquer coleta incerta é falha, nunca PASS.

Arquivos por caso registram início e resultado. Resultado do worker é provisório. PASS exige saída externa zero do supervisor, RESULT e TERMINAL_RECEIPT coerentes e ausência de qualquer falha; há checagens monotônicas após escrever, reler/hash e emitir stdout com flush. Um PASS provisório persistido antes de atraso/erro permanece histórico, invalidado por FAILURE/exit não zero. Falha de disco que impeça o recibo não apaga claims nem libera retry.

stdout/stderr ficam em arquivos diretos, com cap de aceitação posterior de64KiB cada; não é uma quota física de retenção. O worker conhecido não emite saída volumosa. Os limites de tempo, callbacks e conjunto fechado impedem uma campanha automática, não certificam consumo máximo de RAM/disco diante de falha do sistema operacional.

## Comando proposto — NÃO executado

Após revisão independente e criação da decisão específica por ROOT:

    & 'C:\Python314\python.exe' -I -S -B -X utf8 'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_precision_qualification_preparation\driver.py' --decision-sha256 SHA256_REAL_DA_DECISAO_ROOT

O placeholder não é um hash ou autorização. Nenhum AUTH, CLAIM ou diretório execution_once é entregue. Uma execução futura deverá conservar seu recibo externo/exit code. O preparo não repete NC02, tail, 24casos ou c435 e não libera dados, inferência ou veredito F9.
