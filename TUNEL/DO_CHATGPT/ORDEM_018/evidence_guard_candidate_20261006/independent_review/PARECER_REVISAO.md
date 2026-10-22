# Revisão independente final do guard de evidência

**PASS_STATIC_REVIEW_ONLY — EG-01 e EG-02 resolvidos no delta pinado.** Nenhum bloqueador adicional localizado no recorte final. Este aceite é de código/contrato e compatibilidade do candidato; não valida Wilks, independência de testes, busca global, convergência do motor ou ciência observada, nem declara implantação.

## Fechamento dos achados

- **EG-01 resolvido:** `candidate/bancada/evidence_checks.py:17–31` exige sucesso booleano verdadeiro, chi2 e parâmetros finitos, `sigma_JtJ` como dicionário e cada sigma presente real, finito e positivo. Dicionário vazio continua permitido: ausência de covariância não vira sigma zero. `evidencia.py:145,183,186,188` aplica essa validação antes de anunciar o resultado ou prosseguir para o próximo ajuste. A UI mostra as incertezas ausentes como indisponíveis (`app.js:160–161`). O registro de recusa continua com estatística/p_local null.
- **EG-02 resolvido:** `candidate/bancada/regua.py:105–112` confere finitude após cada `z_de_p`; resultado infinito/NaN vira null e o limite local recebe `NUMERICAL_LIMIT_NO_FINITE_Z`. Isso cobre o p positivo subnormal cujo p/2 da conversão original arredonda para zero. Nenhum sigma infinito é publicado por esse caminho. `p_global/z_global` permanecem null; números Šidák ficam somente em `sidak_ilustrativo` e são explicitamente ilustrativos.
- **Contrato identificável:** `regua.py:109` adiciona `schema=evidence-tail-diagnostic-v1`. A conversão local da comparação é rotulada como condicional TGL fixa versus beta livre e regularidade não verificada (`evidencia.py:199–205`); TGL fixa versus LCDM conserva diferença assinada, sem conversão automática em sigma. Este parecer reconhece a rotulagem, não certifica a hipótese.

## Delta de conexão e apresentação

`regua.py:65–72` transforma `_con` em context manager: `with connection` conserva commit/rollback e `finally` fecha a conexão. A busca nos consumidores Python atuais localizou somente quatro usos de `_con`, todos sob `with` em regua; nenhum consumidor local foi encontrado esperando conexão retornada diretamente. Não há alteração de esquema SQL nem reescrita de registros antigos.

`app.js:143–152` usa `Number.isFinite` e não exibe valores globais legados mesmo quando presentes. `330–336` descreve a contagem do livro como rastreabilidade, sem calibração, e mostra a falha de leitura. O contrato de erro HTTP existente continua aplicável: exceções não se tornam resultados de sucesso HTTP200. O patch não prometeu nem implementou serializador JSON global novo; a guarda cobre os campos produzidos nos caminhos revisados, não objetos arbitrários nem todas as operações da aplicação.

## Ensaios atribuídos à ROOT, sem repetição

[REAL — recibo lido] `TEST_ATTEMPT_02.json` registra exit0 em 19 testes Python, 11 casos do formatador extraído e `node --check`. Conferi a presença estática dos 19 métodos e li os programas/saídas; não executei nenhum. Os testes Python importam os candidatos `evidence_checks` e `regua`, extraem por AST a classe `Evidencia`, substituem `_ajuste` e entradas por fixtures e usam SQLite temporário. As funções `z_de_p/p_de_z` de regua são reais e têm import de `scipy.stats` quando chamadas; portanto esta suíte não é descrita como stdlib puro. Não importa o motor nem chama fit, GPU, HTTP ou observados segundo o harness lido. O ensaio JS executa somente o formatador extraído; não qualifica navegador, servidor ou implantação. A tentativa01 com falha de teardown permanece história da ROOT; não foi apagada nem reexecutada pelo revisor.

## Limites para entrega/instalação

1. `candidate/bancada/evidence_checks.py` é dependência nova obrigatória do patch. `PATCH.diff` contém os quatro arquivos alterados e não basta sozinho para instalar o helper. O `__init__.py` de 35 B é explicitamente `staging_only_not_installable` em SOURCE_PINS; o arquivo original vazio não deve ser trocado implicitamente.
2. Os rótulos antigos de `ui/index.html:87`, `README.md:39` e header `mcp_um.py:6` estavam fora do delta revisto. Não declarar alinhamento de toda a documentação sem a atualização correspondente. As descrições das ferramentas MCP já distinguem diagnóstico/ilustração; a pequena incorreção gramatical “traz a diagnóstico” não afeta o contrato.
3. Roteiros históricos que formatam z_global como float e relatórios que truncam a representação permanecem catalogados no parecer consumer_review. Não são qualificados para executar com o contrato novo nem devem ser usados para testar o patch com dados reais. Resultados históricos ficam intactos.
4. O novo registro de falha cobre resumos recusados e deltas inválidos. Uma exceção dentro do solver antes de retornar resumo continua falha HTTP, sem garantia de uma linha de ledger por esse helper. Não descrever o patch como auditoria universal de todas as exceções.

[REAL — alcance do revisor] Dez relações de pins do autor conferidas contra bytes atuais; AST dos Python conferida, trechos lidos e recibos pinados. Zero imports/execuções de candidatos pelo revisor, zero testes, ciência, dados observados, WSL, HTTP, provedores ou produção alterada. ACHADOS_INICIAIS.json foi preservado byte a byte; o fechamento está neste documento e em EVIDENCIAS_FINAIS.json.
