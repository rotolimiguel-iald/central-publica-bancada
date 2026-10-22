# Preparação local — guardas de evidência da Bancada Um

[REAL — engenharia local] Candidato preparado e testado para impedir que resumos de ajustes recusados ou números inválidos produzam significância. Revisão independente encerrada como PASS_STATIC_REVIEW_ONLY. Não implantado; nenhum resultado científico novo nesta entrega.

A comparação passa a exigir sucesso booleano verdadeiro, chi2 não negativo e finito, parâmetros finitos e incertezas presentes positivas e finitas. Ausência de covariância permanece ausência. O mínimo do modelo livre deve ser tão bom quanto cada modelo fixo; delta negativo, mesmo pequeno, gera recusa explícita, sem truncamento a zero e sem tolerância científica inventada.

A diferença TGL fixa versus LCDM permanece assinada. A conversão local rotulada por Wilks refere-se somente a TGL fixa versus beta livre, é condicional e conserva regularidade_verificada=false. Não há calibração global demonstrada: p_global e z_global ficam null; o cálculo de Šidák é uma ilustração separada. Probabilidades que não permitem sigma finito recebem indisponibilidade e diagnóstico, sem infinito no resultado. A interface distingue essas situações e torna visível a falha de leitura do livro.

As conexões SQLite agora fecham em finally, preservando commit/rollback. Esta correção foi motivada por WinError32 na limpeza dos bancos temporários. TEST_ATTEMPT_01 conserva a primeira tentativa: 16 métodos, zero falha de asserção e 15 erros de teardown; não é tratada como aprovada.

## Verificação e autoria

TEST_ATTEMPT_02 registra 19 testes Python aprovados, 11 casos do formatador JavaScript e verificação sintática JavaScript com exit0. O harness Python extrai a classe por AST, simula os resumos de ajuste e usa SQLite temporário; as conversões probabilísticas da régua usam SciPy real. Não é teste do otimizador, calibração estatística, servidor completo ou navegador. Nenhum motor científico, observação, GPU, WSL, HTTP ou provedor foi acionado nesses ensaios.

A revisão independente foi estática e não repetiu testes. EG-01 (todas as incertezas finitas/positivas) e EG-02 (probabilidade subnormal levando a sigma infinito) foram corrigidos e revistos. O adendo documental encerra os rótulos de HTML, README e cabeçalho MCP e corrige a contagem antiga: seis originais e oito candidatos, quatorze relações de pins. Os seis originais foram conferidos sem alteração. A lógica testada não mudou após a tentativa02; o delta final foi documental.

## Conteúdo e limite de integração

Seis arquivos existentes têm versões candidatas: bancada/evidencia.py, bancada/regua.py, ui/app.js, ui/index.html, mcp_um.py e README.md. O novo bancada/evidence_checks.py é dependência obrigatória. São sete arquivos para uma eventual integração coordenada. O oitavo candidato, bancada/__init__.py, existe somente para o harness de staging e está excluído de instalação. PATCH.diff não contém o helper novo; não é pacote de instalação autossuficiente.

O contrato evidence-tail-diagnostic-v1 exige atualização conjunta do produtor, interface e descrições MCP. A API existente conserva ValueError como HTTP400; exceções do solver antes do resumo não ganham necessariamente um registro no livro. Não foi implementada auditoria universal de exceções.

Roteiros históricos que formatam z_global como float ainda precisam de migração antes de eventual uso com esse contrato. Não foram executados nem reescritos, e os relatórios históricos permanecem intactos. A revisão de consumidores está em consumer_review/PARECER_CONSUMIDORES.md.

A ORDEM 018 permite esta preparação em Chatgpt; não se estende aqui a modificar/reiniciar os fontes de produção da Bancada. Nenhuma implantação foi feita ou autorizada pelo parecer. Tampouco se executaram d72/P3, se abriu dado para veredito ou se alterou um.py, kernel ou gate. F1 conjunta, F3 conjunto D e F4 final permanecem incompletos. A consulta prévia ao mapa foi realizada; o registro externo continua pendente, preservada a recusa anterior.

## Alternativas avaliadas

1. Contrato identificado, aditivo, com globais null e ilustração separada: implementado no candidato, preserva diagnóstico e explicita a falta de calibração.
2. Remover a estrutura inteira ou devolver significancia=null: não adotado, pois quebraria consumidores existentes e esconderia o motivo da indisponibilidade. O estudo independente dos consumidores documenta essa comparação.

O ganho desta entrega é operacional: reduz caminhos que poderiam anunciar um sigma indevido. Ela não encontra um novo discriminante nem valida a distribuição de nenhuma estatística observada.
