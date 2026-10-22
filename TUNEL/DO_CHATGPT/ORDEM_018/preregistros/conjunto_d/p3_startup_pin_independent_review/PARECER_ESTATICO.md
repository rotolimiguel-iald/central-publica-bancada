# Revisão independente do sucessor P3: pin nominal de startup

[REAL — leitura de bytes, AST e documentos; sem execução]

Revisão ebec012f-9863-4d9b-9a8c-e4e24144d198 da preparação d50bb889-1682-4320-8106-9bdbd8368257, por chatgpt-codex/ordem-018/preregistros. Autor do sucessor: ordem-018/derivacoes.

**Parecer: o delta está apto à decisão específica de ROOT sobre UMA nova qualificação imports-only. Nenhum bloqueador concreto foi encontrado no recorte.** Este parecer não autoriza nem executa a qualificação. PE permanece PREPARATION_ONLY; a unidade 4a0d70f2 e INIT003 continuam terminais.

Manifesto do sucessor: 5725 bytes, SHA256 21213acfdf02d3133c2660e8b785179745a79b3c8c18999924a34120024dacc9. Contrato: 26218 bytes, SHA256 e7ab9766de262b183aafc5e4ec3e4a0e4b0fe38691f95bdeeb0bb15d60effc81. Os pins foram lidos dos artefatos, não copiados como prova a partir de declarações do autor.

## Escopo e método

Mapa ringdown.ramo_b_preregistro_v386 consultado antes; registros 671/673/675/676/677/678 preservados. Relidos a falha terminal 4a0d70f2, seu traceback, diagnóstico stdlib/sitecustomize e revisão 209ce869. A revisão antiga de componentes não foi refeita: a preservação foi conferida por bytes, com foco no delta novo.

AUDITORIA_ESTATICA.json contém 170 comparações de pins sobre 98 identidades de arquivo distintas, todas coincidentes. Incluem 29 membros do sucessor, 30 do pai terminal, vínculos de entrada/plano/linhagem, recibos terminais e documentos da revisão anterior. Foram parseadas 13 fontes Python como AST, sem importação. O patch foi reconstruído por diff textual e coincide integralmente com DELTA_FONTES.patch. Esses números são verificações documentais, não ensaios de runtime ou ciência.

Dezessete cópias do pacote anterior são idênticas byte a byte, inclusive driver, launcher, guard, validador, fontes, configuração e metadados. As 17 referências de originais também conferem; dentre elas, 16 preservam identidade direta e o driver mantém o delta pré-hook já revisto. Não há novo delta científico.

## Falha precedente e causa documentada

O recibo anterior registra uma única qualificação consumida, status TERMINAL_FAILURE_CONSUMED_NO_RETRY, accepted=false, WSL exit2 e filho PID13/exit1. O traceback chega ao inventário do helper e recusa o destino resolvido /etc/python3.12/sitecustomize.py. Não há IMPORT_RECEIPT de sucesso. O fluxo e o traceback sustentam que a execução alcançou essa fronteira; não sustentam qualificação completa dos imports.

O diagnóstico posterior foi uma leitura separada sob nobody/venv, não repetição do candidato. São 33 módulos de startup, com um arquivo nominal fora das categorias. O alias /usr/lib/python3.12/sitecustomize.py resolve ao destino /etc/python3.12/sitecustomize.py. O texto registrado tem 155 bytes e SHA256 43d81125d92376b1a69d53a71126a041cc9a18d8080e92dea0a2ae23be138b1e; a rehash do texto do diagnóstico coincide com SYSTEM_STARTUP_PIN, plano e contrato.

O conteúdo tenta importar apport_python_hook; ImportError é suprimido e install só aparece no ramo de sucesso. O módulo não aparece no snapshot inicial. Isso não prova ausência geral de efeitos ou disponibilidade futura. A opção -I não implica -S; a execução automática de sitecustomize pertence ao startup preservado. Nenhuma importação explícita desse módulo foi acrescentada. Esta revisão não releu o arquivo Linux nem executou WSL: o pin medido é proveniente do diagnóstico, e a futura invocação deve reconferir seus bytes.

## Delta exato e alcance da nova permissão

Em prehook_imports.py:83–85, o conjunto de chaves da classe adicional deve ser exatamente o singleton /etc/python3.12/sitecustomize.py. Em :95–101, o ramo só é alcançado quando o caminho canônico carregado coincide com essa chave; exige o nome sitecustomize e que o alias lógico pinado resolva ao mesmo destino. Em :25–34, _module_pin exige origem __file__, bytes/SHA e concordância de __spec__.origin. Um arquivo diverso fora das categorias preservadas continua recusado em :113–114.

Assim, a ampliação é nominal: não há teste de prefixo /etc, wildcard, confiança geral no diretório ou relaxamento do ramo stdlib anterior. A evidência de alias é a igualdade de caminhos resolvidos; is_symlink/link_target são metadados históricos do diagnóstico, não um novo ensaio de topologia/inodes. O aceite não promete verificação de ambiente hostil ou imunidade a mudança concorrente de arquivos.

Em qualify_imports.py:15 muda somente a identidade da preparação; a comparação de bytes após essa única substituição coincide com o pai. Não mudam a função de admissão, os imports, o supervisor, os prazos ou os ramos de saída. Os quatro alvos e os vínculos adapter/source continuam os mesmos. O driver é byte a byte igual ao pacote anterior: journal, FD, latch e checkpoints não receberam modificação. O qualifier continua sem instalar o guard científico e não finge qualificá-lo.

As duas alternativas documentadas são proporcionais à causa: A, pin nominal do arquivo observado, preserva startup; B, -S e reconstrução de caminhos, muda a política de inicialização e não foi adotada. O delta implementa somente A. Os campos históricos da alternativa B pré-hook referem-se à escolha anterior de carregar os quatro módulos antes do hook; não confundem essa denominação com a alternativa -S rejeitada no diagnóstico novo.

## Identidade, consumo, limites e PE

qualify_imports.py:39–81 continua exigindo Linux isolado -I/-B, hash canônico da decisão futura, schema exato, ação QUALIFY_PINNED_IMPORTS_ONLY, nova preparação, UUID da qualificação e pins de manifesto/contrato/interpretador. O comando Windows usa --exec, nobody e argv Linux POSIX como tokens completos, inclusive os caminhos com espaços. A raiz é a nova pasta, não a do pacote consumido. Não há shell intermediário ou troca implícita de conta.

A reserva exclusiva IMPORT_QUALIFICATION/CLAIM continua antes do Popen (:141–158); o filho repete admissão e cria CHILD_STARTED antes dos imports (:84–124). Uma falha após reserva não admite retry/resume. O sucesso continua condicionado a exit0 externo, recibos correspondentes, ausência de FINALIZATION_FAILURE e prazo pós-I/O (:172–202). Contrato e código conservam 120s nominais totais, 110s de trabalho, CPU100/105s, 8GiB de endereço, um filho, um thread e RLIMIT_FSIZE de2MiB por arquivo após admissão. Não prometem hard realtime, teto global de arquivos/RAM ou contenção de descendentes nativos.

P3PKG-01, limitação não bloqueante já aceita pela ROOT, permanece: timeout precoce pode omitir child_pid no terminal porque a atualização ocorre após a espera normal (:172). O handle direto continua sendo o recém-criado; a falha não produz falso COMPLETE ou permissão de retry. O delta não ampliou essa limitação e não propõe repetir um controle para redemonstrá-la.

Os dois entrypoints PE continuam lançando erro na primeira instrução: driver_p3.py:26–27 e launch_p3.py:15–16. science_enabled=false, nenhum job científico e nenhum comando PE. Na inspeção estática, ROOT_DECISION, AUTH, CLAIM e IMPORT_QUALIFICATION estão ausentes no sucessor. O comando contém placeholder para hash de decisão futura. A autorização da unidade falha não é transferida.

## Encaminhamento mínimo

ROOT pode emitir decisão específica para UMA nova qualificação imports-only do sucessor, vinculando manifesto/contrato e nova identidade de consumo. Este parecer não cria essa decisão. Se houver falha ou resultado incerto depois da reserva, recuperar identidade/evidência e parar, sem fallback ou repetição. Não é necessário inventar outro controle para aceitar o delta nominal.

Só recibos reais de uma futura invocação podem qualificar seus imports e atualizar a evidência dos 1162 arquivos Linux. Mesmo sucesso de imports não qualifica waveform, likelihood, sampler, convergência, recuperação, cobertura ou PE D. Uma etapa científica posterior continua exigindo o contrato e decisão próprios já previstos. Não se cria dependência de P3 para F1.

Zero importação/execução de candidato, NumPy ou biblioteca científica nesta revisão; zero WSL, solver, provedor, observado, strain/PSD/NPZ/HDF5. Nenhum AUTH/CLAIM/ROOT_DECISION ou edição do pacote, memórias e ledger. Apenas documentos da revisão nesta pasta e registro posterior no mapa.
