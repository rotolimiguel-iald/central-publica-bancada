[REAL] T04-F — preparo do segundo instrumento, 2026-09-27 UTC. NÃO-CEGO; diagnóstico, não significância.

Abertura 016 sha256: 216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a
Abertura 015 sha256: dbd0a307438dda2969a21baf64665d54e8b70fb84c3fe10f8c233ddeac736610
ORDEM 015 sha256: c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3

C terminou PARTIAL_MAXCALL_NOT_ACCEPTED, sem posterior aceito; H foi interrompido após correção explícita da leitura da árvore. O próximo ramo escrito é F. C e H ficam preservados em seus recibos e MEDIDAs; esta nota não os reclassifica.

O Kerr V2 original foi copiado para `ORDEM_013_RINGDOWN/bis/e3_kerr_dtau_f_015`. `kerr_model.py` acrescenta `dtau220` e multiplica apenas o tempo de amortecimento 220 por `1+dtau220` na função usada pela verossimilhança; `runner.py` usa rótulo exclusivo e marca `sigma_eligible=false`. Nenhum original da Física foi alterado. Prior Uniform[-0.8,2] veio de E2_PE_JOBS_ALLOCATION_015_V4. C5_FISHER_v3 registra NON_IDENTIFIABLE_SINGLE_220 para Mf/af livres; não se calculará σ deste posterior.

Manifesto F v2 sha256: 9598d4d17abebf368664e86c5febe9d1acffa1839664b49dfbc755a07966cf60; substitui sem apagar v1 sha256 24998d8bd8b2a2f4acf6abc5284c2f6f6bca0a0f2384b028dcb503f9e8e16e4f. Quarenta e oito pins de fonte foram conferidos byte a byte; os cinco hashes de código e as três cópias inalteradas também. Orçamento v5 sha256: 63d3436d3b812f8e3977252173575d903f7e08f941c1dbb7b2b2e757c885e7bb; reserva F 7.958360255746666 h, teto do controlador 2 h. Teste de fonte em `/opt/lal_env/bin/python -B` rc 0, log sha256: 8eefac0435ad6cd6c8795434a081482b27af1710b94864ab39f05a68e7868b07. Resultado: δτ=0 erro exato 0; δτ=0.5 razão analítica nas ramas + e − com erros 4.44e−15 e 2.67e−15; suporte inválido rejeitado 3/3. Comando: `wsl.exe --exec /opt/lal_env/bin/python -B /mnt/c/IALD/Central\ de\ Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/015/t04/test_kerr_dtau_f.py` (caminho passado como um argumento).

Revisão externa: Kimi recebeu especificação, apontou que não viu os arquivos. O diff exato foi enviado em unidade idempotente d9d0f405-4d5d-4a3e-95c1-36890cc99a44, job 85fad11a-2080-4b34-abc0-9f2fdca63cbc; parecer ainda pendente nesta nota. Não há autorização F nem execução pesada. Aceitação final de F dependerá do recibo e da custódia WSL, sem previsão de convergência. Axiomas Lean: N/A.
