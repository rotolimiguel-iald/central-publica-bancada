# P3 — candidato de preparação do orçamento A

[REAL — preparação de software] Identidade 6a99afd6-831c-4fa5-9190-cef5db67e52c. Esta pasta implementa a alternativa A da proposta documental, para revisão independente. Ela não seleciona A para consumo, não contém ROOT_DECISION, AUTH, CLAIM ou unidade de provedor e não executou fonte, waveform, likelihood, sampler, WSL ou dados externos. INIT003, a falha 4a0 e todos os pacotes anteriores permanecem intactos.

A diferença material proposta é investimento de recursos: 10.000 → 100.000 avaliações externas de likelihood e reservas de waveform por caso, 3.600 → 14.400 s de trabalho e CPU 3.300/3.305 → 13.200/13.205 s. O supervisor conserva a estrutura de duas realizações sintéticas sequenciais, com teto nominal de 14.410 s por caso, 8 GiB de espaço de endereçamento por filho e um thread. Fonte pSEOB, prior normalizado, parâmetros fixos, seeds, geometria, arrays esperados, likelihood e dynesty nlive=256/rwalk/walks=25/dlogz=0,1 não foram alterados. Não houve migração científica para v388.

[OPEN] O aumento de orçamento dá oportunidade de exploração adicional, não uma previsão de convergência. O resultado histórico de 9.738 chamadas e delta_logZ≈57,2757 continua insuficiente e terminal. Não há extrapolação de chamadas até convergência nem de custo para os 14 eventos do conjunto D. A proposta B (rslice) permanece alternativa documental não implementada/selecionada; C é conservar o resultado incompleto sem novo consumo.

## Código concreto e dois achados corrigidos

P3-01: o novo supervisor usa uma única criação do filho por caso e posse explícita do handle. Timeout, KeyboardInterrupt e erro inesperado passam pelo fecho kill/reap; erro ou término incerto impedem o segundo caso e qualquer sucesso. SIGINT/SIGTERM são adiados na janela de Popen até atribuição do handle; a interrupção pendente chega ainda no trecho protegido. O filho POSIX herda essa máscara bloqueada e o driver não a desbloqueia: restore_signals não restaura a máscara. O cleanup atual depende expressamente de SIGKILL no grupo do filho, que não é mascarável. SIGALRM/SIGXCPU do orçamento continuam disponíveis. Não existe preexec_fn. A análise é estática e os testes usam doubles, não demonstram sinais reais no Linux.

A partição nominal é 14.400 s de trabalho + 5 s para o filho finalizar + 4 s para kill/reap + 1 s para recibos, dentro de 14.410 s. O prazo começa antes do trabalho/IO de cada caso; o prazo agregado começa antes da admissão do supervisor. Os waits usam somente o restante. Há verificações após persistência/hash/saída com flush. Um recibo provisório não é aceite: exige exit externo zero e ausência de FINALIZATION_FAILURE. IO travado, SIGKILL do supervisor ou perda do host não têm contenção hard-real-time por Python; permanecem limite declarado e resultado incerto, sem retry. Logs são arquivos como na base, sem alegação de quota rígida de disco.

P3-02: result_acceptance confere preparação, execução, decisão, contrato, caso, PID e scientific_qualification=false, além do latch/journal/contadores herdados. O rótulo numérico exige delta_logZ finito em [0;0,1), ESS finita ≥100, span vivo finito >0, inclusão dos live points, chamadas abaixo do teto e ausência de erro. Bool não vale como número. O span antes da adição agora consta no RESULT. Os dois casos precisam satisfazer os critérios para o indicador conjunto. Isso verifica os diagnósticos reportados e vínculos; não é recomputação independente do posterior bruto.

CLEAN_PARTIAL pode encerrar operacionalmente um caso limpo incompleto, como previsto no desenho. A sequência RB foi pré-planejada após GR limpo, convergente ou incompleto; falha/incerteza interrompe a coleção. Exit zero operacional nunca significa F3 qualificada, recuperação estabelecida ou autorização de D.

## Contagem e diagnóstico de recuperação

CallBudget reserva a likelihood antes da avaliação, incluindo os live points iniciais. A reserva nativa ocorre no checkpoint imediatamente anterior à waveform; a fonte original e seu contador de chamadas completadas ficam intactos. Reservas e conclusões são campos separados, sem cap+1 oculto. O maxcall interno do dynesty não substitui esse contador externo. O max_native_calls=32 de CONFIG_SYNTHETIC é metadado congelado de P0/P2 validado pelo adaptador; o generator não o usa para limitar a campanha P3. Ele foi conservado, enquanto os tetos P3 são explícitos no contrato e no driver.

A proposta de recuperação é implementada por quantis empíricos ponderados inf{x:Fw(x)≥p}, sem interpolação/resampling: q05/q50/q95, largura, deslocamento da mediana, CDF na verdade, massas nas bordas inclusivas e W90/2,52. A aritmética é float/stdlib com somas compensadas, sem certificação de quantis. Não há corte de valores não finitos ou de massa inválida: erro permanece erro. A condição “verdade no intervalo e W90<2,52” é fraca, específica da realização e subordinada à convergência limpa e interpretação independente de forma/bordas. ESS100 não certifica caudas nem cobertura. O diagnóstico não vira PASS científico, e campos produzidos antes de eventual falha final não prevalecem sobre a recusa do validador terminal.

## Acesso que ainda exige decisão específica

PLANO_ACESSO_REQUERIDO.json é inventário/proposta, não autorização:

1. Conferência de bytes/SHA/tamanho dos 11 nomes externos, 5.396.115 bytes declarados pelo contrato histórico. Incluem NPZ sintético de 5.218.208 bytes e ASD de projeto de 71.136 bytes.
2. Decodificação do NPZ sem pickle, somente frequência/PSD analítica e ruído/sinal GR_GAUSS/RB_GAUSS × H1/L1; leitura da normalização sintética documental.
3. Runtime/interpreter e imports pré-hook pinados; a ASD instalada nominal serve só à inicialização, substituída pela PSD analítica antes da likelihood. O plano inclui os 1.162 paths históricos do runtime e o startup nominal; não são pins Linux frescos nesta preparação.
4. Execução dos dois casos somente após decisão específica sobre A, recursos, diagnóstico e acesso. O recibo histórico de imports tem papel documental separado e não autoriza ciência.

Nenhum desses alvos brutos foi aberto, copiado, decodificado ou hasheado nesta preparação. AUTO_REVIEW_REJECTION.json é uma cópia histórica byte-idêntica da base, identificada no manifesto; não registra tentativa nova. A recusa de acesso aos inputs e a recusa d72 continuam válidas; este pacote não as contorna. Não há observado/PSD observado, A/B/C/D, nova coleta ou provedor.

## Verificação entregue e limite do aceite

[REAL — local stdlib] 143 conferências estáticas/pins, AST de 18 módulos, 70 posições de uso de limites/diagnósticos inventariadas. Os 18 membros reutilizados são byte-idênticos. Chamadas do driver a NestedSampler, sample, GravitationalWaveTransient, generator e np.load têm AST igual à base; mudanças de orçamento vêm do contrato.

Os primeiros 25 controles de software passaram; a revisão da janela de posse motivou uma correção específica e um caso adicional. A versão final passou 26/26, em cerca de 0,0024 s internos, com recibos anteriores/backups preservados (51 execuções de teste, 26 casos distintos finais). São vetores pequenos e doubles: zero processo filho real, zero sinal real, zero biblioteca científica, zero array externo. Não são nova execução de INIT003, qualificação científica ou validação do runtime Linux.

[INPUT — proposta de custo máximo] Dois casos permitem no máximo 200.000 avaliações de likelihood e 200.000 reservas nativas; soma nominal do supervisor 28.820 s (8 h e 20 s), CPU hard dos filhos 26.410 s (7 h, 20 min e 10 s), concorrência um. Esses são tetos de política, não previsão financeira ou de sucesso. RAM de 8 GiB refere-se ao filho via RLIMIT_AS, não a toda a máquina.

O comando candidato está em COMANDO_CANDIDATO_NAO_EXECUTAR.json e contém marcadores de hashes futuros. Não o invoque neste estado. Próximo passo é revisão independente deste manifesto/delta, seguida — se pertinente — da decisão específica do operador. Nenhuma aprovação desta preparação autoriza consumo. Memórias globais, fila, ledger e originais não foram alterados; MCP não foi chamado.
