# Testes stdlib preparados, não executados

O arquivo test_bridge_stdlib.py contém testes de composição usando os módulos stdlib reais de cauda/redutor/theta pinados; o perfil é um double com constantes lidas por AST, sem importar código científico e doubles semânticos locais. Importar esse arquivo já carrega módulos candidatos: isso NÃO ocorreu nesta preparação e depende de autorização futura.

Casos específicos: família600×5 e plano completo sem promoção a mínimo contínuo; nó ausente/duplicado; estados fechados; falta de verificador; recibo booleano forjado; falta de certificado sem p=1 artificial; átomo d=0; d=0 positivo inválido; troca cenário/modelo H1/H2; ordem da família; inclusão ausente; erro não limitado; bytes adulterados; estimativa rejeitada como certificado; L=0 analítico sem U; deadline; transporte racional refinado para cima; Bonferroni5 uma única vez usando cauda/redutor reais.

O verificador de fixtures usa exclusivamente SYNTHETIC_CONTROL_ONLY. Mesmo o teste nominal não emite decisão científica. threshold_audit é real e a decisão sintética pode ser conferida. A suíte acrescenta ambos os lados de alpha/5, cruzamento do intervalo, mismatch deliberado do redutor e recusa de perfil com q finito mas estado/log de falha. Os testes verificam integração/recusas, não solver, significância observada ou qualidade de inferência.

Comando futuro proposto, NÃO executado: C:\\Python314\\python.exe -X utf8 -B -m unittest -v test_bridge_stdlib, na pasta desta preparação. Sem WSL, NumPy, CAMB, arrays ou dados observados; leitura dos .py pinados e memória sintética somente. O runner não cria AUTH/CLAIM. Aprovação da preparação não é aprovação automática desse comando.

## Escopo/custo da execução única proposta

26 métodos de teste preparados, zero executados. Módulos reais: theta_integrator.py, tail_envelope.py e decision_reducer.py, todos stdlib e pinados; novos módulos locais bridge/frozen_contract/threshold_audit. affine_profile.py é lido como bytes e AST somente, com double de MODELS/SOURCE_PINS. Nenhum import NumPy/CAMB/profile científico. Não repetir suítes prévias, launch d72, P3 ou controles consumidos.

Uma passagem sintética completa de perfis nível1:16.200registros, gerados e consumidos em fluxo,600cenários×27nós×5modelos. Casos adicionais interrompem cedo ou tratam documentos sintéticos de3000registros por chamada do redutor. Somente um caso solicita cauda não trivial (um cenário COMPAT); demais são recusa ou p=1 exato. Intervalo alpha é construído uma vez por processo/cache; p=1 tem log0 exato sem série repetida.

[INPUT — proposta, não medição nem autorização] Um processo,120s totais incluindo startup/cleanup,1GiB RAM, sem geração de dados persistentes salvo stdout/stderr/recibo do supervisor escolhido pela ROOT. Não há custo/API. Tempo real e pico RAM NÃO_MEDIDOS. Se o supervisor não aferir e encerrar de forma comprovada, resultado incerto não é PASS nem autorização para repetir. Esta entrega não inicia o processo nem implementa outro supervisor.
