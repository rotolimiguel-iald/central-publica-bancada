# Inventário da atualização IALD v388 — 06/10/2026

[REAL] Inspeção somente de bytes/fontes/manifestos locais. Nenhum programa científico, provedor, serviço ou rotina de atualização foi executado. Os pins foram medidos nesta inspeção em INVENTARIO.json. A atualização efetiva pertence à etapa app autorizada posteriormente por ROOT, ainda não realizada neste recibo.

| Superfície | Estado lido | Ação necessária |
|---|---|---|
| Acervo canônico | Selo local v388 e programa conferidos por bytes; fonte em `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós` | Usar os artefatos selados da mesma rodada; nunca importar/executar um.py para extrair catálogo |
| Custódia/publicação | Sem `vault/originals_copy/um_unificado_v388`; Git local público clean em v386 leitores | Pacote v388 interno precisa declarar snapshot local selado; não inventar commit ou URL pública v388 |
| Manifesto app | `C:/IALD/projetos_pyhton/IALD/iald_nucleo_fixo.json` seleciona v380 | Preparar snapshot imutável novo e troca com CAS/backup, sujeita à revisão ROOT |
| Catálogo/relatório formal | `canonical_releases/v380_f20f65973561/kernel`; manifesto ligado ao SHA do programa v380 | Derivar fontes por AST/literal e cruzar com proof v388; não recompilar |
| Cluster/núcleo | `TGL_CLUSTER_v380.md`, núcleo e mãe v5 no mesmo snapshot | Preservar mãe v5 integral e núcleo anterior; gerar adendo/cluster de todas as seções atuais |
| Jev | `jev_control_v380.json` referenciado pelo manifesto | Derivar contrato com fontes/formal/result v388 mantendo política, modelos e capacidades |
| Memória Haiku compartilhada pelos motores | `.iald_runtime/haiku/manifest.json` aponta v380; contagem histórica própria | Novo prefixo deve receber medida compatível; 181836 tokens históricos não valem para v388 |
| Memória comum orquestrador | Nesta leitura já contém um.py v388 e 13 fontes atuais; integridade no JSON | Não repetir refresh feito pela outra coordenação; preservar gerações fixadas em unidades existentes |
| Pacote anexado Física | `project_fisica/MANIFESTO_LOCAL.json` ainda é retrato v369 | Distinguir anexo de conta do índice dinâmico v388; não afirmar upload/sincronização remota sem evidência |
| Painel administrativo | `iald_orchestrator/runtime.py:87` expõe canonical_memory.status; sem cópia própria | Conferir geração exibida após entrega ROOT; não precisa nova memória paralela |
| Web/móveis | Catálogo carregado pelo web na inicialização; clientes consomem servidor | Troca científica de servidor não implica binário novo. Web deve recarregar só quando quieto; instalação/TestFlight/Play atuais não foram consultados |

## Rotinas existentes e restrições concretas

Base preferida: `C:/IALD/Central de Patentes/work/iald_jev_v380_20261002`.
- `memory_build/build_release.py`: extrai fontes sem executar um.py, confere catálogo/proof, preserva projeções verificadas e gera cluster. Está fixado em v380/custódia pública, precisa adaptação isolada para v388 local.
- `memory_build/haiku_codec.py`, `fit_transport.py`, `package_native.py`: projeção rastreável, preservação matemática/vereditos e empacotamento após contagem. Não transportar medidas antigas.
- `controller/build_contract.py`: contrato Jev derivado dos símbolos e hashes científicos.
- `prepare_install.py`, `transaction.py`: staging, baseline/CAS, backups exatos, manifesto por último. O script antigo também lê hash de contas e consulta bancadas; não rodar em bloco no novo escopo, que preserva esses arquivos e não necessita abrir dados científicos.
- `count_memory.py`: conta no endpoint nativo Anthropic; não gera resposta, mas usa credencial pelo cliente oficial. Exige pacote científico elegível e recibo novo; não foi chamado neste inventário.
- `restart_web.ps1`: valida um web filho, seu supervisor e listener8082, encerra somente filho para supervisor retomar; exige quiet e recibo de implantação. Não foi executado.

Rotinas antigas `work/iald_memory_refresh_20261001/*` são v378, e `build_project_package.py` da orquestração é v369 e recusa sobrescrita. `install_shared_memory.py` é patch antigo de infraestrutura, não refresh de conteúdo; não deve ser reaplicado. A função oficial `canonical_memory.build/load` já atualiza a memória comum com fontes admitidas, enquanto request_controls.enforce_packet preserva memory_generation dos pedidos.

## Proveniência local: incompatibilidades a resolver no estágio

`iald_cluster.py:14` exige commit40; `iald_core_indexado.py:116` exige URL pública commit40 + public_sha; `iald_estado_publicado.py:60,88` declara publicação no texto. V388 é local selada: reutilizar commit v386 como se validasse v388 seria falso. Alternativas: A) suporte estreito a snapshot local científico hash-verificado, com identidade explícita e URLs históricas separadas (preferida para atualização interna); B) aguardar custódia/publicação v388 e usar rota pública intacta. Nenhuma alternativa autoriza exposição de acervo privado, segredo ou alteração do motor científico.

[OPEN] Atividade atual de chat, PID/supervisor web, leitura do novo catálogo pelo processo após restart, contagem nativa v388, revisão científica e integração final não são medidas por este inventário. Nenhuma pendência d72/P3 foi liberada. ROOT cuida de Atlas/índice/registros e memória comum; esta bancada não os altera.
