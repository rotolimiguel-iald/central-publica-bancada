# Parecer independente do pacote P3 A

**STATIC_REVIEW_ONLY — bloqueado antes de qualquer consumo futuro.** A preparação 6a99afd6-831c-4fa5-9190-cef5db67e52c permanece selada e sem autorização de execução. Há dois bloqueadores: janela de interrupção na entrada do cleanup e tabela de custo antiga sem rótulo histórico.

A revisão leu bytes, JSON, código e AST. Não importou candidatos nem repetiu os 26 testes stdlib do autor; não iniciou WSL, waveform, likelihood, sampler, PE ou provedores. Arrays/NPZ/PSD/ASD externos e observados não foram abertos nem hashados. Nenhum AUTH, CLAIM ou ROOT_DECISION foi criado. Não se comprova aqui comportamento de processos reais ou qualificação científica.

## P3A-01 — P1: cancelamento pode escapar antes de kill/reap

Em launch_p3.py:70–72, SIGINT/SIGTERM chamam handler que lança SupervisorInterrupted, derivada de BaseException. cleanup_context (launch_p3.py:55–64) lê os handlers e depois os substitui um a um por SIG_IGN, sem proteger a entrada até que ambos estejam ignorados.

O with cleanup_context() de process_supervision.py:42 já está no finally de supervise, fora dos catches internos de poll/kill/wait. Caminho estático concreto: filho vivo; timeout; entrada no finally; SIGTERM antes de seu handler ser ignorado; exceção sai do context manager antes de kill_owned_group e proc.wait. O except externo de launch_p3.py:179–188 pode registrar a falha e retornar2, sem recuperar o handle para recolher o filho.

O defeito não produz PASS falso: pode deixar filho vivo após uma interrupção que o pacote declara tratar. Não se exige garantia contra SIGKILL externo, perda de host ou I/O ininterruptível. É exceção Python assíncrona permitida pelo próprio fluxo controlável.

A máscara de ownership protege Popen→handle; o teste26 cobre interrupção pendente na saída desse contexto. Isso não cobre a entrada desprotegida de cleanup. A herança POSIX da máscara SIGINT/SIGTERM pelo filho está documentada; cleanup usa SIGKILL e SIGALRM/SIGXCPU não entram nessa máscara. Essas propriedades foram lidas, não medidas por processos reais.

O reparo mínimo precisa impedir escape assíncrono antes do cleanup limitado do filho possuído, preservando identidade, deadline, falha e no-retry. ROOT sugeriu avaliar handlers com flag, sem exceção assíncrona, e waits curtos. É hipótese de solução para sucessor, não solução aprovada, implementada ou testada pelo revisor.

## P3A-02 — P2: dois envelopes aparecem como vigentes

CONTRATO_P3.json:303–307, cost.hard_envelope_two_jobs, ainda contém 7220s de supervisor, 6610s de CPU hard e 20000 chamadas. O campo não está rotulado como histórico.

limits (256–266) e aggregate_maxima_proposed (719–724) definem A: 100000 chamadas/caso, 14410s por supervisor e 13205s de CPU hard; para dois casos, 200000 chamadas, 28820s de supervisor e 26410s de CPU hard. O código usa A corretamente. O defeito afeta clareza da decisão e contabilização de recursos; não foi encontrada ampliação oculta do runtime.

O sucessor deve separar explicitamente o envelope histórico ou corrigir o campo vigente. Proxies antigos continuam história, sem previsão linear de convergência ou custo em D.

## Preservações e correções constatadas

Conferidos 40 membros e seis backups: 46 pins correspondem. Dezoito Python foram analisados por AST, dezoito itens reutilizados coincidem byte a byte com a base e os 14 campos científicos comparados são iguais: hipótese, parâmetros livres/fixos, priors, normalização de massa, grid, geometria, detectores, PSD analítica, referências a arrays/resultados qualificados, regra de dados, ruído e sampler. Os jobs preservam metadados e seeds GR180602/RB180603, ressalvadas as identidades da preparação. Isso não reconfere os bytes externos dos arrays.

O IMR pSEOBNRv4HM_PA mantém DTau220 como única deformação QNM livre; DOmega220, DTau440 e DOmega440 ficam em zero. prior_transform.py foi preservado. O contador likelihood reserva antes de cada avaliação, incluindo inicialização; waveform reserva antes de sua fronteira nativa, sem cap+1. Esse contador não inventaria todas as funções C auxiliares da guarda temporal/dicionário. A fonte mantém dicionário LAL novo por geração.

A admissão exige decisão externa exata, hashes de contrato/manifesto/acesso, identidade e escolha de recursos, além do ambiente Linux/UID/modo isolado previstos. Não há autorização ou CLAIM no candidato. A leitura bruta de entradas externas depende da resolução específica já declarada; a recusa anterior não foi contornada.

A correção do P3-02 da revisão-base foi material: result_acceptance.py exige identidade, tipos estritos sem bool, delta_logz finito no intervalo admitido, ESS finito suficiente, live span finito positivo, final_live adicionado, contagens válidas, ausência de erro e auditoria/journal limpos para aceitar convergência. CLEAN_PARTIAL continua operacional incompleto, distinto de convergência e sucesso científico. RB após GR clean parcial é o segundo caso previsto, não retry.

Quantis usam CDF empírica ponderada sem reamostragem/interpolação; não finitos, pesos negativos e amostras fora do prior são recusados. Intervalo central90%, posição da verdade, deslocamento mediano e contração relativa ao prior são diagnósticos. Verdade no intervalo e largura inferior a2.52 são condição descritiva fraca, não PASS científico. Dois casos pareados não demonstram cobertura. logZ de datasets diferentes não constitui BF.

Orçamento nominal por caso:14400s de trabalho+5s finalização do filho+4s kill/reap+1s recibo=14410s; CPU soft/hard13200/13205s, memória8GiB, um worker/thread, até dois casos, sem retry. Há checagens após I/O/hash/print e exigência de saída externa coerente sem marcador de falha. Python não garante hard-real-time; captura em arquivos não tem quota rígida de disco, como declarado. Isso não elimina P3A-01.

## Alcance e próximo passo

[REAL documental] Núcleo científico preservado e validação de resultados melhorada; permanecem um bloqueador de cleanup e incoerência de custo. O recibo do autor — 26 testes/143 verificações/18 AST — foi lido sem repetição e não prova contenção POSIX real.

[OPEN] Convergência, recuperação dos dois casos, cobertura e PE em D não foram estabelecidos. Unidades terminais, incluindo INIT003, continuam terminais. P3 não cria dependência para F1/d72.

Próximo passo mínimo: delta separado dos dois achados, preservando snapshot/recibos, e revisão específica. Decisão de execução e acesso exato às entradas já são requisitos do contrato. Nenhuma expansão de campanha, autorização ou execução é proposta por este parecer.
