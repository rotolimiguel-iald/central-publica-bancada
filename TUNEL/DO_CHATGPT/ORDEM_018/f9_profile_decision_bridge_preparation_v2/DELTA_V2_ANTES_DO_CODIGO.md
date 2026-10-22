# Sucessor v2 — correção mínima de prazo após verificador

[INPUT] ROOT solicitou sucessor preservando integralmente a preparação original. O revisor independente localizou falta de checkpoint imediatamente depois do object_verifier: o recibo poderia ser válido mas tardio.

Alternativa A: checkpoint central imediatamente após o callback em _objects(), antes de aceitar o recibo. Cobre construção, entrada e encerramento de estimate_family e as demais utilizações de _objects.
Alternativa B: inserir checkpoints separados em cada chamador antes de retornar. Mais pontos de manutenção e risco de omissão futura.
Escolha A: uma linha funcional, sem novo recurso, certificador, solver ou alteração de hipóteses/domínio/família. Acrescentado um teste stdlib com relógio falso e recibo válido após deadline. Nenhum teste/callback executado nesta preparação.

Observações documentais do revisor: o modo sintético permanece separado; callbacks_executed=0 no resultado de estimativas significa zero callbacks científicos/solver/perfil, não zero chamadas dos verificadores de objetos. Estes são chamados e agora têm checkpoint antes e depois. Corrigido o cabeçalho histórico do teste; branch defensivo antigo sem efeito permanece preservado.
