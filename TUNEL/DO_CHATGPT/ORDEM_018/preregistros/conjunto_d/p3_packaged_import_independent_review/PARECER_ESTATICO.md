# Revisão independente estática da composição P3 pré-hook B

[REAL — leitura de bytes/AST] Revisão 209ce869-06d7-4035-a26d-3570df0f206a, 2026-10-06T16:05:21.212884+00:00, por chatgpt-codex/ordem-018/preregistros. Autor do pacote: ordem-018/derivacoes. Preparação examinada: 2bfd4665-a7e7-410a-aeb3-0406f90a596f.

**Parecer: composição estática aceita para a decisão futura de ROOT sobre uma inspeção de imports, com a limitação de diagnóstico P3PKG-01 abaixo. Nenhum defeito bloqueante foi localizado nesse recorte. PE continua PREPARATION_ONLY.** Não é autorização, sucesso dos imports, qualificação de ciência nem reabertura de INIT003.

Manifesto relido: 5506 bytes; SHA256 ab1a7de573199182fcb5bc08109d23b152fd850addec1741109fb6edb87fa684. A consulta anterior do mapa reteve as sequências619,627,668 de ringdown.ramo_b_preregistro_v386; a revisão619 não foi repetida. Nenhum arquivo observado/strain/PSD/NPZ/HDF5 foi aberto. Resumos históricos encontrados na rota não foram usados. Nenhum candidato, NumPy, solver, WSL ou controle foi importado/executado. Não houve rede/provedor, AUTH, CLAIM ou ROOT_DECISION.

## Evidência de composição

Foram feitas 121 comparações e verificações de metadados/estrutura, todas sem divergência, e parse AST de 13 fontes Python. O subconjunto inicial contém99 comparações de bytes/pins:30 membros,2 fontes documentais,17 fontes reutilizadas,16 cópias idênticas,20 entradas,13 pins Python do plano e o diff textual exato. Conferidos também6 pins documentais históricos, sem repetir seus controles. O recibo detalha cada verificação; esses números não são testes de runtime.

driver_p3.py:26-27 e launch_p3.py:15-16 ainda interrompem incondicionalmente antes da campanha. As cópias de audit_guard.py, result_acceptance.py, launch_p3.py e src/pseob_source.py são byte a byte iguais às fontes indicadas. O patch do driver contém apenas a referência ao módulo adapter, a chamada/recibo do pré-hook e campos de proveniência no resultado futuro. Priors, parametrização, sampler, grade e allowlist não mudaram. O pacote contém metadados, não arrays nem contrato P3 executável.

## Import B, identidade e fronteira

Em driver_p3.py:86-98, o helper roda antes de abrir o journal, instalar o callback na fonte e instalar o audit hook (:115). prehook_imports.py:47-65 exige um único módulo pseob_source, o adapter canônico, os mesmos objetos função/conversão e globals/origem de código da fonte; também exige que o callback ainda não tenha sido instalado. Assim o callback posterior atinge a referência realmente capturada pelo adapter.

prehook_imports.py:68-78 confere e materializa lal, lalsimulation, bilby.gw.source e temporal_contract, conservando os imports tardios/checkpoints originais. O helper não enfraquece audit_guard.py nem inclui diretórios de cache na allowlist. O journal original abre por O_EXCL antes do hook, escreve pelo FD e mantém latch irrevogável/checkpoints; isso é preservação por identidade de bytes, não nova demonstração runtime. O qualifier não instala esse hook e não pretende testá-lo.

qualify_imports.py:98-124 fixa a política de bytecode e os caminhos locais antes dos imports do pacote/runtime. Rehash dos1162 arquivos de runtime e do interpretador é trabalho FUTURO: aqui só foi conferida sua metadata histórica. O inventário posterior distingue runtime pinado, módulos locais pinados e stdlib com metadata nova sem pin histórico (:80-105 do helper). A pasta UNUSED_BYTECODE_CACHE não existe no snapshot lido; essa observação não é uma prova geral contra alteração concorrente ou código hostil no sistema de arquivos.

Não há chamada direta a fonte, validação temporal LAL, detector, likelihood ou sampler no qualifier. O codec cp437 é efetivamente invocado para seu roundtrip de256 bytes; não é cálculo científico. A declaração de zero ciência é sobre as funções diretamente chamadas pelo candidato. Imports podem executar inicializadores Python/C, explicitamente reconhecidos; não há promessa de zero função C, zero syscall ou clausura total de imports futuros.

## Admissão, recursos e terminalidade

qualify_imports.py:39-81 exige Linux isolado -I/-B, hash canônico da decisão futura, schema exato, UUID da qualificação, ação QUALIFY_PINNED_IMPORTS_ONLY, mesma preparação e pins do manifesto/contrato/interpretador. O manifesto é lido e todos os seus membros conferidos. As raízes Linux são absolutas POSIX no comando proposto; não há transporte WSL criado nem aplicação de WindowsPath ao argvLinux.

O supervisor começa o relógio antes da admissão (:135-140), reserva IMPORT_QUALIFICATION e CLAIM exclusivamente antes de Popen (:141-158). O filho verifica novamente admissão/claim e cria CHILD_STARTED exclusivamente antes de imports científicos (:84-124). Uma falha depois da reserva permanece consumida; não há retry/resume automático. O sucesso exige rc0, identidade/status do recibo filho, recibo terminal, hash/flush e nova checagem de prazo (:172-202). Falha de I/O/parse/exit ou FINALIZATION_FAILURE invalida um COMPLETE provisório.

O orçamento é120s nominais totais,110s de trabalho, com recolhimento dentro do mesmo deadline. CPU do filho100/105s,8GiB de espaço de endereçamento e2MiB por arquivo após a admissão são explícitos. O código usa piso de1ms no wait de cleanup quando o tempo remanescente já acabou; isso pode ultrapassar o instante nominal por esse piso/agendamento/I/O, mas o check final impede exit0 tardio. Não se promete hard realtime. RLIMIT_FSIZE não é limite global da soma dos arquivos, memória de captura ou inicializadores anteriores à sua aplicação. A saída vai diretamente a arquivos, não a communicate com retenção ilimitada em RAM.

O kill se dirige ao handle Popen do filho recém-criado; não há varredura de PID ou killpg no novo qualifier. Não há contenção de descendentes nativos maliciosos, tampouco declaração dessa garantia. O antigo launch_p3 contém código histórico de campanha ainda bloqueado na primeira linha de main; não foi considerado um supervisor científico recém-qualificado.

## P3PKG-01 — diagnóstico de PID incompleto no timeout precoce (não bloqueante)

Local: qualify_imports.py:155-172,183-190; worker:84-93. A atualização child_pid/returncode está somente depois da espera normal. Se a espera der timeout enquanto o filho ainda verifica a admissão, CHILD_STARTED pode ainda não existir; o terminal então pode registrar falha/cleanup_unconfirmed sem PID do filho. A identidade da unidade/decisão permanece no CLAIM e o handle usado pelo pai continua correto. Não há caminho derivado deste achado para falso COMPLETE ou retry permitido.

Melhoria mínima possível, somente se ROOT decidir: persistir a identidade do filho imediatamente após Popen e mantê-la nos ramos de falha, em delta pinado. Esta revisão não altera o pacote e não exige relançamento de nenhuma unidade para recuperar a identidade. A limitação deve acompanhar a decisão de execução imports-only.

## Próximo passo mínimo e saldo honesto

ROOT pode decidir especificamente sobre a qualificação única de imports pinada, conhecendo P3PKG-01, ou pedir apenas esse delta de diagnóstico antes de consumir a unidade. Nenhuma decisão foi criada pelo revisor. O comando atual contém placeholder de hash; não é comando atualmente autorizado.

Só um futuro recibo real poderia qualificar os imports dessa invocação e tornar atuais os pins Linux. Isso ainda não prova ausência de novos imports/checkpoints falhos na ciência. Para PE, o contrato já exige outro pacote científico com novas identidades, inputs sintéticos qualificados, runtime/recibo reais, remoção explícita dos bloqueios em cópia nova e decisão específica. INIT003 e todos os controles consumidos permanecem terminais. Não invento uma dependência P3 para F1, nem trato imports-only como cobertura, convergência ou veredito D.
