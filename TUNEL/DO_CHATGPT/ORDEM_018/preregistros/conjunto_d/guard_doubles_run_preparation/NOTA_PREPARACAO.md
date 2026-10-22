# Preparação da execução única dos doubles do audit guard

[INPUT — PREPARAÇÃO, NÃO AUTORIZAÇÃO] ROOT pediu somente o launcher/contrato para executar futuramente os 21 testes preparados, após revisão e decisão específica. Esta entrega não executa/importa candidatos ou suíte. Não cria AUTORIZACAO_ROOT.json, CLAIM.json, RUN, unidade PE ou novo identificador científico; persiste um request_id operacional uma única vez.

A clarificação ROOT registrada no mapa493 seleciona **supervisor externo + um filho puro**, com uma única execução da suíte. “Processo único” não significa depender de watchdog no processo testado. Os drivers científicos continuam PREPARATION_ONLY no pacote de origem.

## Alternativas examinadas

1. **Selecionada:** supervisor externo e um filho Python isolado, seleção exata de testes, reserva persistente e prazo monotônico comum. Permite observar retorno/timeout e coletar stdout/stderr sem depender da disciplina do teste. Acrescenta apenas threads operacionais de captura no supervisor.
2. **Não selecionada:** suíte no próprio processo com watchdogs internos. É simples, mas o término/coleta pode depender do processo sob teste e de exceções absorvidas; ROOT expressamente preferiu a primeira.
3. Contenção OS mais forte é possível em outra unidade, mas não é inferida destes doubles nem necessária para alegar apenas seus resultados. O hook do worker é defesa cooperativa de escopo, não sandbox nativo completo.

## Identidade, seleção e autorização futura

IDENTIDADE_PREPARADA.json contém o request_id, os nomes dos21 métodos extraídos por AST e pins iniciais. CONTRATO_DOUBLES.json fixa a mesma identidade, módulos, intérprete e código do launcher. A seleção é uma TestSuite explícita por nome; não há discovery de outros diretórios ou importação de drivers P3.

O comando proposto exige AUTORIZACAO_ROOT.json futuro, ligado ao request_id e SHA256 exato do contrato, escopo AUDIT_GUARD_21_PURE_DOUBLES_ONLY_ONCE, uma execução,30s totais, uma thread de trabalho e parecer independente aceito/pinado. O schema descrito no contrato não é essa autorização. Sem arquivo válido, não há claim nem subprocesso.

CLAIM.json é criado exclusivamente, fsync e verificação, antes do Popen único. O filho exige identidade, nonce, pai correto e hash da autorização; cria RUN/WORKER_CLAIM.json exclusivamente antes de executar qualquer byte de candidato/suíte. Há caminho canônico fixo, sem parâmetro de saída alternativa. Claim, RUN ou resultado existentes, inclusive parciais/incertos, impedem repetição. Mudança de nome do output não redefine a unidade; erro/falha não limpa recibos nem libera tentativa.

## Limites e coleta

Pré-checagens/pins e persistência do claim precedem o relógio nominal, conforme o padrão já usado nos oito controles. A partir daí, configuração/Popen/espera/coleta compartilham **30s**: prazo de trabalho em25s, reserva de5s dentro30. Não existe segundo orçamento de cleanup. Timeout, overflow ou outra falha mata o filho conhecido e recolhe apenas até o deadline total. Estado não resolvido fica PROCESS_STATE_UNCERTAIN; nenhuma repetição ou espera ilimitada.

Stdout e stderr usam drenos separados, cada qual conserva no máximo65.536bytes; bytes vistos e truncamento ficam registrados. Overflow implica falha, não resultado aprovado truncado. Os drenos seguem consumindo sem acumular além do teto até o recolhimento. O filho usa -I -S -B, sem site-packages/PYTHONPATH/bytecode, e dependências científicas não são importadas. Variáveis de bibliotecas paralelas são fixadas em1 por precaução; só há uma thread de trabalho na suíte.

O supervisor tem duas threads daemon exclusivamente para captura. A suíte não cria descendentes. O hook do worker recusa eventos Python de subprocessos/rede, importações fora da biblioteca padrão e dos dois módulos admitidos, e escrita após a reserva. O teste que menciona “native”, “likelihood” ou “campaign” usa doubles/listas/counters; esses nomes não são chamadas científicas.

[OPEN — limite honesto] O prazo é nominal, não garantia de tempo real do OS. A escrita do recibo terminal é tentada imediatamente após coleta, inclusive para registrar atraso/estado incerto, sem nova espera. Se houver falha severa de IO/processo, CLAIM/WORKER_CLAIM/PROCESS existentes e ausência de RESULT são evidência de incerteza terminal; não se presume sucesso. O hook Python não impede qualquer syscall nativa arbitrária, e esta preparação não valida contenção OS. Os códigos executáveis estão pinados, são puros e foram somente examinados estaticamente.

## Saída e alcance

PASS requer retorno0, exatamente21 testes e mesma ordem nominal, todos sem erro/falha/skip/expected failure/unexpected success, nenhuma recusa do guard e captura íntegra dentro do prazo. O supervisor emite RESULT.json com identidades, retorno, stdout/stderr limitados, tempo e classificação; falha retorna nãozero. Mesmo PASS só qualifica estes doubles e não autoriza inicialização, waveform, likelihood, sampler, PE ou leituraD.

A preparação fez apenas AST/sintaxe, identidades e hashes. Nenhum teste foi executado para validar o launcher. A revisão pode apontar defeitos antes da decisão ROOT. O pacote original, seus PREPARATION_ONLY, IDs consumidos e memórias compartilhadas permanecem intactos.
