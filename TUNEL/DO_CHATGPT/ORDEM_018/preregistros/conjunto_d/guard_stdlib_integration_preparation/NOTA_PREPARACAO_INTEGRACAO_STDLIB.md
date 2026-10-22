# Integração stdlib do guard — preparação para revisão

**PREPARATION_ONLY_NOT_AUTHORIZED_NOT_EXECUTED.** Pedido 278b56a3-36e0-4adc-9708-af49f094d1df. Nenhuma autorização, CLAIM, RUN, instância de journal, hook ou execução dos casos foi criada nesta etapa. Somente escrita de instrumentos, leitura, AST e pins. Sem PE, dados D ou retomada INIT003.

## Alternativas comparadas

| Alternativa | Avaliação |
|---|---|
| A — supervisor externo e um filho descartável por caso | Escolhida: hook real, journal original, importador real e separação do estado de hooks. Três filhos sequenciais, no máximo um ativo, prazo nominal comum de 30 s. |
| B — todos os casos num processo ou manter writer/importador simulados | Rejeitada para esta pergunta: hooks não se removem e contaminam casos; mocks não exercitam o probe absorvido nem a escrita física. |

Nenhum quarto caso intencional de timeout foi incluído. O caminho de timeout será especificado, mas não poderá ser anunciado como exercitado porque três casos rápidos passem.

## Casos fixos

**I01_REAL_HOOK_JOURNAL.** Dois arquivos triviais são criados antes do hook. A abertura de ambos é recusada pelo hook real; o teste captura PermissionError. O PreopenedJournal original deve gravar dois registros e completar dois fsync reais. Primeira ocorrência e ordem são preservadas; checkpoints seguinte e final impedem callback trivial, cujo contador permanece zero.

**I02_IMPORT_CACHE_SWALLOWED.** SourceFileLoader tenta ler o .pyc derivado de um fonte contendo somente VALUE=42; o hook recusa esse caminho. A implementação local importlib/_bootstrap_external.py, linhas 851–853, captura OSError, da qual PermissionError é subclasse. -B impede escrita de bytecode, sem remover a tentativa de leitura. O futuro teste exige que o fonte termine de carregar e que o latch então barre o callback seguinte. PermissionError simplesmente propagada não satisfaz o caso. Se o runtime não percorrer o ramo, o caso falha e não é repetido automaticamente.

**I03_PHYSICAL_JOURNAL_FAILURE.** O descritor real do journal é fechado antes do hook. A abertura recusada aciona os.write, que deve falhar com EBADF. A primeira ocorrência, o latch e o erro de escrita ficam em memória; o arquivo físico permanece vazio e o callback segue impedido. Nenhum writer falso substitui o journal.

PASS_EXPECTED_LATCHED significa sucesso do controle com bloqueios deliberados, não guard limpo. São esperados dois/um/um bloqueios; operação inesperada impede aceite. Callback é função trivial, não fonte, likelihood ou sampler.

## Instrumentação e alcance

sources/audit_guard.py é cópia byte a byte da versão revisada. Não há substituição de os.write, os.fsync ou PreopenedJournal. sys.setprofile observa chamadas C e seus retornos/exceções enquanto sys.addaudithook executa as recusas reais. O supervisor também relê JSONL e confere bytes, hash e eventos contra o snapshot do filho. Retorno de fsync e leitura posterior não provam persistência após perda de energia nem cobrem toda falha de IO.

O runtime proposto é CPython 3.14 no Windows, C:/Python314/python.exe. Os 21 pins incluem exe/DLL, módulos stdlib relevantes, instrumentos, guard e identidade. O fonte do importador ancora o ramo; o runtime congelado se vincula ao exe/DLL e deverá demonstrar a absorção. Isto não qualifica CPython 3.12 da WSL, driver científico, LAL, waveform, sampler, integração nativa ou cobertura/convergência de PE.

Antes do hook: bootstrap stdlib e arquivos fixos de contrato/autorização/claims/pins. Só depois do CASE_CLAIM durável são carregados os bytes do guard e criadas fixtures, journal e descritor do resultado. Depois do hook: leituras apenas do fonte trivial e journal exatos; cache/arquivos bloqueados são alvos negativos fixos. Novas aberturas para escrita são recusadas; são usados descritores já abertos do journal/resultado e stdout/stderr. Compilação/execução só admite o nome exato do fonte trivial. Imports adicionais, salvo o trivial, subprocessos, sockets, ctypes, mutações e novo hook são recusados.

O hook é cooperativo: não intercepta todo uso de descritores ou syscalls e não confina código hostil. BaseException/SystemExit não é mecanismo infalível. Uma recusa inesperada falha sem ampliar a lista de permissões durante o caso. A allowlist científica não foi relaxada; quatro candidatos anteriores (driver, launcher, source e guard) foram reconferidos sem mudança e seus PREPARATION_ONLY/IDs consumidos permanecem.

## Identidade, prazo e aceite

AUTORIZACAO_ROOT.json não existe. Revisão e decisão específicas de ROOT devem nomear request, hash do contrato, escopo, uso único, três filhos e 30 s; o contrato não concede essa autorização. COMANDO_PROPOSTO_NAO_EXECUTADO.json é somente proposta.

O supervisor cria CLAIM exclusivo com fsync antes de Popen/fixtures/import do candidato. Cada despacho tem nonce; cada filho exige PID do pai, pins/autorização e CASE_CLAIM exclusivo antes do caso. CLAIM, RUN ou RESULT existentes tornam a identidade consumida/incerta. Nenhum reset, output alternativo, retry ou resume.

Relógio: primeira leitura monotônica após import time, antes dos demais imports do supervisor e da pré-validação. Prazo nominal total 30 s, trabalho até 24 s e até 6 s por filho dentro disso. Reap após kill e joins são finitos dentro do restante. Capturas limitadas a 32 KiB por fluxo/filho; overflow falha e para. Filhos não lançam descendentes pelo código/hook; o supervisor encerra o filho identificado, sem alegar contenção geral de árvore nativa.

Aceite exige três casos exatos na ordem, rc0, recibo físico igual a stdout, journal e invariantes conferidos e nenhuma operação inesperada. Falha impede o próximo filho e propaga exit nãozero. Resultado ausente ou estado incerto não vira sucesso. O prazo é verificado novamente após IO do recibo final: ultrapassagem provoca exit nãozero e invalida eventual PASS provisório no JSON. O aceite externo sempre exige exit0 do pai. IO e escalonamento não têm garantia temporal absoluta.

## Estado da entrega

O snapshot inicial registra 60 conferências estáticas passadas: AST, imports, invariantes textuais, 21 pins, cópia original, preservação de quatro candidatos anteriores e ausência de arquivos de autorização/consumo. **Não são controles executados nem prova dinâmica.** Uma tentativa de gravar esta nota junto a um recibo de mapa excessivamente grande foi recusada na criação do processo Windows (erro 206); nenhum instrumento foi iniciado. A escrita documental foi dividida, sem repetir mutação incerta.

Entregues contrato, worker, supervisor, guard qualificado, identidade, comando não executado, recibo estático e manifesto para revisão de ROOT. Não foram alteradas memórias compartilhadas. Próxima decisão é a unidade stdlib concreta; não há autorização implícita para ciência ou D.

## Errata de preparação PREP-CANTRACE-01 — revisão independente ROOT

ROOT identificou antes de autorização um defeito de observabilidade: CPython suprime tracing/profiling durante hooks de auditoria Python, salvo opt-in __cantrace__. Sem ele, os contadores físicos de os.write/fsync poderiam permanecer zero apesar da escrita real. Acrescentado audit.__cantrace__ = True imediatamente antes de sys.addaudithook; dois comentários explicitam esse alcance. O guard original, a allowlist, o supervisor, os três casos, os limites e todas as exigências dinâmicas ficam idênticos. Isto corrige a preparação; nenhuma identidade foi consumida e nenhum caso foi executado para reproduzir o defeito.

Fontes primárias conferidas por ROOT: [documentação sys.addaudithook](https://docs.python.org/3.14/library/sys.html#sys.addaudithook) e [CPython v3.14.3, Python/sysmodule.c](https://raw.githubusercontent.com/python/cpython/v3.14.3/Python/sysmodule.c), linhas 297–323, EnterTracing/LeaveTracing condicionado por __cantrace__. Este agente não arquivou nova cópia externa nem atribui hash a essas páginas. A demonstração dinâmica dos contadores continua pendente, sem dispensar qualquer asserção.

Backups imediatos de bytes preservam worker, contrato, comando, nota e manifesto anteriores; DELTA_CANTRACE.patch mostra o delta exato. RECIBO_PREPARACAO_AST_PINS.json permanece como snapshot histórico das 60 conferências, vinculado aos pins anteriores. RECIBO_DELTA_CANTRACE.json mede 38 conferências estáticas atuais (AST, delta, 21 pins, escopo/limites, preservação e ausência de consumo), sem importar os candidatos nem instalar hooks. A contagem não é execução de testes de integração.
