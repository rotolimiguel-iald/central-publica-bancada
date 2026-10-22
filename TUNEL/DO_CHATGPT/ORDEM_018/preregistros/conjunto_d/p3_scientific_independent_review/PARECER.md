# Parecer independente estático do P3

[REAL — revisão local] O pacote foi conferido por bytes e AST. **A preparação atual permanece bloqueada para consumo e requer duas correções técnicas no sucessor antes de futura admissão.** Este parecer não autoriza execução, não é qualificação científica e não altera o pacote selado.

## Objeto e método

Preparação `3249312d-d7b6-4a04-93d6-81f65d4f4945`; manifesto `MANIFESTO_PREPARACAO.json`, 6069 bytes, SHA256 `c68972f9901f0d898a9b37b30147031d92813e3181fa69d6077b6ba317bb9140`. Foram medidos os 33 membros, todos coincidentes, analisados 13 arquivos Python por `ast.parse` e confrontadas 36 ligações locais de contrato/pre-hook. Priors e grade do contrato coincidem com CONFIG_SYNTHETIC. A sintaxe válida não demonstra execução ou correção numérica.

Somente arquivos locais de código, contratos e documentos foram lidos. O inventário de runtime contém 1.162 referências históricas; seus alvos não foram abertos. Os onze alvos externos do contrato, a curva ASD instalada e quaisquer arrays/PSD/observados não foram lidos, copiados, decodificados nem re-hashados. AUTO_REVIEW_REJECTION e RECIBO_POS_SELO_MAPA_RECUSADO foram respeitados. Nenhum candidato foi importado/executado; nenhum teste científico, WSL, provedor ou registro MCP foi acionado.

## Ligações e guardas conferidas

- **Admissão:** `science_admission.py:30–58` exige Linux isolado, identidade nobody, raiz exata, contrato/decisão pinados e modo sintético. `NOT_JUSTIFIED_UNDER_INHERITED_ENVELOPE` recusa em 57–58, antes dos reads externos de 92–93, do claim e de Popen. Mesmo uma decisão com approved=true não admite o contrato atual. O manifesto/entradas só seriam verificados no caminho posterior de uma invocação futura com contrato distinto e revisão própria.
- **Identidade e não repetição:** admissão vincula preparação, execução UUID, contrato, manifesto, raiz, diretório e dois casos ordenados; `launch_p3.py:24–38` reserva campanha com O_EXCL e vincula o claim de cada filho à decisão/execução/PID. `driver_p3.py:34–39` confere o pai e recusa saída já iniciada/concluída. Reserva não comprova término; ver P3-01.
- **Driver → adapter → fonte:** `driver_p3.py:146–161` constrói o WaveformGenerator, envolve o callable efetivamente ligado com FailureAudit e passa-o à likelihood. `synthetic_adapter_v2.py:63–87` mantém somente DTau220 livre, os demais deltas zero, catch_waveform_errors=false e a grade congelada. `prehook_imports.py:47–64` confere identidade de módulo/função/globals/origem. `pseob_source.py:109–133` exige guardas temporais, dicionário LAL novo por avaliação e checkpoints antes/depois da chamada, contando tentativas mesmo quando lançam exceção.
- **Prior e família:** a transformação de 12 coordenadas preserva o prior conjunto normalizado e a restrição de razão de massas, com área 3477,5 e peças 1687,5/1200/590; não há descarte como rejeição de likelihood para esconder falha. A fonte usa pSEOBNRv4HM_PA, quadro detector, spins alinhados, dois casos pareados e os seeds/grades do contrato. Igualdade de configurações e leitura de fórmulas foram estáticas; não se calculou waveform nem se declarou domínio nativo integralmente qualificado.
- **Dados sintéticos e inicialização:** o caminho proposto compara verdade/normalização e hashes do arquivo qualificado, substitui o ASD da factory pela PSD analítica e verifica estado antes/depois da construção da likelihood (`driver:65–69,125–153`; `init_detectors:24–69`). Isso é código de verificação futura, não integridade bruta medida agora. A factory somente é referência permitida no contrato; a recusa de acesso atual continua vigente.
- **Falhas e contadores:** contador de likelihood incrementa após budget e antes da avaliação (`driver:119–123,155–164`); tentativas de waveform são contadas no finally da fonte. None, domínio, temporal, não finito e exceções não viram -inf/rejeição do prior. Latch retém negações e erros de journal; o aceite exige journal vazio, contadores/checkpoints consistentes e exit0. Esgotamento limpo de orçamento tem tratamento parcial explícito; todos os abortos científicos, auditoria, timeout externo, saída não zero e recibo ausente/malformado permanecem falha terminal. O rótulo EDOM histórico não é somado como total: domain_error_total=null.

## Achados concretos

### P3-01 — encerramento do supervisor (P1)

`launch_p3.py:42–47` abre sessão de processo própria e só cobre TimeoutExpired com killpg/wait. KeyboardInterrupt, SIGTERM e erro inesperado do supervisor não têm cleanup em finally ou handler. Em uma futura execução admitida, a saída do supervisor pode deixar o filho ativo, apesar do claim impedir repetição. Não houve ensaio dessa situação nesta revisão.

Alternativa A: sucessor com posse explícita de Popen, handlers de cancelamento e cleanup/reap auditável em todas as saídas controláveis, preservando falha/incerteza quando recolhimento não for comprovado. Alternativa B: supervisor externo especificado, pinado e revisto, dono do grupo e dos recibos; o comando atual não prova que exista. SIGKILL/perda do host continuam limite próprio. Nenhuma alternativa foi implementada aqui.

### P3-02 — aceite terminal por rótulo (P2)

`result_acceptance.py:25–26,73` transforma DLOGZ_REACHED_ESS_OK em CLEAN_CONVERGED sem ler ΔlogZ, ESS, error, preparation_id, execution_id, decision_sha256 ou scientific_qualification. A não degeneração é examinada no driver em 179, mas não é serializada no resultado. Por inspeção, retirar esses campos não altera as condições de assess. O cálculo existe no driver pinado; falta a reconciliação no validador terminal. Não foi construído/executado recibo de teste no candidato.

Alternativa A: exigir identidades esperadas pelo supervisor e critérios finitos de parada/ESS do contrato, registrar não degeneração e recusar incoerências. Alternativa B: conservar apenas aceite de protocolo com rótulo neutro e exigir validador separado pinado para qualquer alegação numérica. **Mesmo após correção, parada/ESS não provam contração ou recuperação científica.** F3, cobertura, ruídos independentes e PE observado permanecem separados. A proposta científica nova é revisada pela ROOT, fora deste parecer.

## Condicionantes, não defeitos novos

NOT_JUSTIFIED é a recusa deliberada correta, não motivo para trocar uma flag. O consumo depende de desenho/contrato revisados, acesso específico ainda pendente e decisão própria; estes atos não existem por efeito desta revisão. O resultado antigo não prevê trajetória idêntica nem impossibilidade de convergir.

8 GiB, 10.000 avaliações por caso, parede suave3600 s, espera do supervisor3610 s e CPU3300/3305 s são tetos de configuração; não custo medido nem prova de recursos livres. A espera externa inclui o preflight do filho, mas o timer e a medição internos começam após seus hashes/limites. A admissão do supervisor antecede o relógio da campanha, e persistência/recolhimento não têm garantia de hard realtime. A nota já declara esse alcance nominal; não se exige nova campanha para medi-lo nesta etapa.

A auditoria é cooperativa Python para eventos de open/process/socket após imports fixos. Não é isolamento de syscalls nativas, não revoga descritores preexistentes e não demonstra ausência universal de I/O antes do hook. Não há evidência nova do runtime atual. Ausência de confirmação dos arrays ou dos imports posteriores é lacuna declarada; não foi preenchida por inferência.

## Encerramento

[REAL] Pacote e contrato originais preservados; nenhum AUTH, CLAIM ou ROOT_DECISION criado. INIT003, 4a0 e imports5e391d57 não foram repetidos/reabertos. [OPEN] Duas correções técnicas para eventual sucessor, decisões de acesso/recursos e qualificação científica futura. Os pareceres/documentos presentes bastam para encerrar esta revisão estática, sem consumo adicional.

A rota informada pela ROOT foi ringdown.ramo_b_preregistro_v386, sequência687 e total688; registro tratado como [DECLARADO] nesta revisão. Não houve leitura/escrita MCP nem tentativa de repetir o registro pós-selo recusado. A consolidação compartilhada cabe à ROOT.
