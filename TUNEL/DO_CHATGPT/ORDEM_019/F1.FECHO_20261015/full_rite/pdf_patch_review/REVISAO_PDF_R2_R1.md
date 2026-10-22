# Revisão independente — patch PDF R2

[REAL] **PASSA COM ESCOPO MIKTEX LOCAL**, sem achado material.

10/10 casos independentes simulados passam; 11/11 verificações nativas do construtor e 18 pinos foram conferidos.

- R2 exige exit 0 nas duas passagens, antes de consultar existência do PDF. PDF velho não mascara falha da primeira ou segunda passagem.
- Identificação MiKTeX consulta stdout e stderr de --version; falha de identificação ou timeout retorna False. Motor ausente retorna None.
- Apenas MiKTeX identificado com TGL_NO_NETWORK=1 recebe as opções documentadas --disable-installer e --disable-write18.
- O recibo nativo contém duas passagens bem sucedidas e duas recusas por pacote ausente; 11 verificações e seus pinos conferem. Nesta revisão não se relançou motor nativo: 10 casos independentes com subprocess substituído verificam os ramos.
- A fonte de patch contém uma única definição compile_pdf. Aplicação ao candidato completo e comparação das demais funções são responsabilidade da integração posterior.

## Limites

- Não é firewall/sandbox do processo nativo.
- Outros motores e modo sem TGL_NO_NETWORK mantêm opções anteriores; o contrato auditado é o MiKTeX identificado nesta máquina.
- True exige dois exits zero e PDF existente; não valida conteúdo, frescor ou renderização do PDF.
- Os testes independentes não executaram processos externos, provedor, rede, um.py nem dados científicos.

Relatório JSON contém comandos simulados, hashes e recibo nativo. Nenhuma alteração de produção, memória ou gate.
