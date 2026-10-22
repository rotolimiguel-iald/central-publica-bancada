# Revisão independente do redutor lógico F9 V2

**Nenhum defeito acionável identificado no conjunto selado examinado.** [REAL — leitura, hashes e AST] O módulo implementa os predicados delimitados do contrato V2 de forma coerente. A tabela de 24 casos inventados é compatível com essa implementação por inspeção estática. **Nenhum dos 24 casos foi executado nesta revisão.**

Pedido bf6d6747-6383-40a0-9aa4-7c02e76cadd6. Manifesto de preparação: 1.865 bytes, SHA256 bec431e8dbe6d61f663b451acb62634281be5d03dfa206e794b2d55c9b9cf61c. O pin do contrato V2, os cinco membros e a imutabilidade até a conferência final constam no recibo. Este aceite não ratifica V1, não concede acesso a observados e não autoriza a execução do driver.

## Predicados e estatutos

[REAL — correspondência textual/AST] Foram lidos integralmente REQUEST.json, decision_reducer.py, API_E_ESCOPO.md, logical_checks.py, o recibo estático da ROOT e F9_VERDICT_CONTRACT_CANDIDATE_V2.json. A leitura inicial corrigiu o caminho do contrato pelo REQUEST existente; a primeira tentativa na raiz deu FileNotFoundError, não conteúdo válido. Não houve execução/importação do módulo ou do driver para recuperar contexto.

O redutor importa somente math. Seu cálculo usa metadados já admitidos por um chamador confiável; não constrói estatística, calibração, likelihood, evidência Bayesiana, potência ou dados. O contrato-fonte é identificado pelo hash dos bytes lidos, e os cinco nomes/ordem de testes e estados de calibração coincidem com ele. O esquema de saída V1 é versão do formato da API, não ratificação científica do V1.

| Objeto | Implementação e conclusão da revisão |
|---|---|
| Completude por cenário | Linhas 121–132: ausência/None conserva MISSING e complete=false; registro presente passa por schema estrito. Estatística válida implica disponível. Calibração admitida exige estatística válida, escopo, log-p finito e referências externas. |
| Completude do teste | Linhas 133–143: exige todos os cenários fornecidos na família congelada, previamente não vazia e sem duplicatas. O máximo robusto é calculado somente após essa condição. Não há máximo do subconjunto disponível. |
| Rejeição de H1 | Linhas 148–153: OR das rejeições completas COMPAT_H1/LAW_H1_VS_FREE. Uma rejeição completa continua visível se o outro teste estiver indisponível ou parcial. |
| Não-rejeição calibrada de H1 | Linha 149: AND da completude e não-rejeição dos dois testes. Ausência não equivale a não-rejeição. Rivais ausentes não apagam a não-rejeição válida de H1 no campo compatibility. |
| Rival Hj | Linhas 155–161: discriminação combinada requer não-rejeição calibrada de H1, teste rival completo/rejeitado e direção positiva certificada em todos os cenários. A rejeição isolada do rival fica em null_rejected. |
| Direção | Linhas 66–70 e 144–146: certificado de direção requer T válido estritamente positivo, teste rival e referência; positividade sem certificação não basta. T negativo é permitido como estatística válida, mas não certifica preferência por H1. |
| H3 | Não há teste de rejeição de toda a classe que contém H1. LAW_H1_VS_FREE testa a lei fixa sob H1 contra sua extensão. |
| Saídas separadas | compatibility, comparisons, cenários e faltas sobrevivem à prioridade do resumo. relative_evidence, sigma_equivalent, information_power e use_novelty permanecem indisponíveis neste escopo. Não há porta de potência que suprima rejeição. |

O status de topo pode comunicar rejeição de H1 ou discriminação contra um rival mesmo se outro teste faltar. Isso respeita a prioridade do V2: não afirma completude de todos os testes; os campos por teste preservam as faltas. O predicado combinado é por rival, não uma afirmação simultânea sobre H2, H4 e H5.

Quando toda a família está completa e não há reivindicação robusta prioritária, a diversidade das decisões por cenário ou dos sinais gera SYSTEMATICS_SENSITIVE_RESULT. Nos demais casos, o detalhe das decisões/sinais permanece nos registros; o resumo de topo não é uma prova de invariância entre cenários. A cobertura física fica explicitamente limitada à família finita fornecida.

## Bonferroni, logaritmos e precisão

[DERIVED — álgebra do predicado] Para valores positivos representados por log-p, a monotonicidade de log permite max_s log p_s = log(max_s p_s). O código usa log_p_FWER = min(0, log(5) + max_s log p_s), comparado a log(0.5 erfc(5/sqrt(2))). O fator cinco permanece fixo, inclusive quando faltam testes; não é reduzido ao número de resultados disponíveis. Não há produto de p correlacionados, hipótese de independência, Wilks, sqrt(DeltaChi2) ou conversão Bayes→sigma.

O limiar é unilateral, como no V2. Um log-p positivo, NaN ou infinito é recusado. -infinito não serve como p=0. Quando exp de um log finito underflowa, p_upper fica None e o log finito permanece como representação decisória; não se publica zero como probabilidade obtida.

[LIMITE NUMÉRICO] As operações math/float e as comparações são de engenharia, arredondadas. O redutor não é verificador de aritmética intervalar, não certifica arredondamento para fora e não demonstra uma decisão exata em toda vizinhança do limiar. O log é a referência da comparação; a conversão exp é uma representação de ponto flutuante. A futura integração deve respeitar a exigência do contrato de incluir incerteza numérica nas cotas admitidas, sem transformar igualdade float em prova estatística.

## Fronteira de confiança

[INPUT — condição da API] O chamador deve autenticar os artefatos e demonstrar que:

- a família de scenario_ids é a família congelada inteira, ou equivalência admitida com mapeamento/prova;
- o teste, hipótese nula, domínio, cenário e procedimento correspondem à calibração indicada;
- log_p_upper representa cota superior conservadora válida, incluindo incerteza numérica;
- o orçamento de falha da certificação, inclusive de uma cota de confiança Monte Carlo se usada, está incorporado ao orçamento global exigido pelo contrato;
- suporte, integridade, certificados de direção e autorização/ratificação são realmente válidos.

O módulo verifica forma e presença de referências, não seu conteúdo ou autenticidade. Um digest bem formado ou flags true não demonstra nada disso. API_E_ESCOPO.md:7–11 e 31–38 e scope da saída explicitam essa distinção. Não há afirmação de verificação estatística externa pelo redutor.

A função admite None em records quando os dados/ratificação não estão liberados ou quando suporte/integridade falham; campos de decisão permanecem None. Entradas de schema inválido provocam erro visível. A saída não ratifica, não autoriza, não altera gate e não significa CONFIRMED. Os registros inventados do driver possuem referências explicitamente fictícias e não são certificados utilizáveis na ciência.

## Tabela planejada e driver

[REAL — inspeção, não PASS de execução] A leitura/AST identificou 24 rótulos distintos de conferência, incluindo a expansão textual do laço dos dois testes H1. Cobrem:

- dados fechados, suporte inválido, IDs desconhecidos/duplicados e família sem resultados;
- cada rejeição H1 com o outro teste faltando; necessidade de ambos para não-rejeição;
- discriminação com os requisitos completos, máximo entre cenários e fator cinco;
- direção apenas positiva sem certificado; H1 rejeitado impedindo discriminação combinada;
- calibração parcial, cenário faltante e estatística inválida sem conversão em rejeição;
- underflow, log-p positivo/NaN, bool como estatística e referência ausente;
- mudança de sinal entre cenários.

As condições esperadas dos 24 casos foram conferidas pela leitura das fórmulas e ramos. Não constituem prova de todas as entradas possíveis nem verificação de calibração real. A contagem de 44 conferências no recibo desta revisão refere-se a pins/AST/metadados, não aos 24 casos executados.

logical_checks.py verifica os cinco pins do manifesto, exige revisão ROOT vinculada ao manifesto e permissão específica do controle lógico, e cria CLAIM_LOGIC.json por O_EXCL antes da importação futura do módulo. Exige ausência de resultado anterior e grava resultado por arquivo temporário verificado/substituição. Falha após claim consome a unidade; não há autorização de repetição automática. O acesso a fontes e a importação descritos são atos futuros do driver, não realizados nesta revisão.

Na conferência final não existiam REVISAO_ROOT.json, CLAIM_LOGIC.json ou RESULT_LOGIC.json. Nenhuma autorização/claim foi criada por esta revisão. Não foram alterados módulo, API, driver, contrato, originais, unidades consumidas, memórias compartilhadas ou ledger.

## Conclusão limitada

O conjunto selado está apto a uma decisão da ROOT sobre o controle lógico único já planejado. Não identifiquei correção material necessária antes desse controle delimitado e não proponho campanha adicional. O sucesso futuro dos casos ainda precisa de recibo de execução; mesmo se ocorrer, comprovará apenas comportamento sobre metadados inventados, não validade das premissas estatísticas, física ou autorização de abertura.
