# E6 V2 — delta e handoff para fechamento independente R

**READY_FOR_FOCUSED_REVIEW_NOT_AUTHORIZED.** Preparação congelada em nova árvore; V1 preservada byte a byte e copiada em v1_snapshot. Nenhuma montagem E6 real, autorização E6 real ou extração E7. As 180 células e mapeamento histórico permanecem; não mudou matemática, dados ou leitura escolhida.

Parecer que motivou a correção: `e6_review/E6_INDEPENDENT_PREP_REVIEW_V1.md`, SHA256 `00582309a3268d1d49ed8458ec4bbfa028f7661b9aa67ae24c49f4d07591d018`.

| Achado | Delta concreto | Fixture focal |
|---|---|---|
| R1 | Recibo V2, predecessores com pin e evidência temporal separada da emissão; piso de ativação E2; sequência efetiva alocação→calibração→TEST; NO_EXECUTION com parede pinada | stage_before_E2_activation; TEST_before_allocation_and_calibration; pins divergentes; datas future/naive/malformed; paredes e GO preexistente positivos |
| R2 | z/lnB/razão física passam pelo mesmo gate; calibração não emite razão física de teste; UNDERPOWERED exige análise válida e insuficiência revisada sem limiar alto | red_gate_physical_ratio; unpaid_partial_NOT_FALSIFIED_UNDERPOWERED; E3.3 ratio; positivos underpowered com z dummy 0.2 e sem número físico |
| R3 | SEMANTIC_UNITS e contrato/schema por rota/campo; quantidades dimensionais, canais, informação, contagem, equivalentes e taxa não intercambiáveis | green_tau_gate_in_Hz; 220/440/IV cruzados; contagem/informação/equivalentes/base temporal; um binding válido por rota |
| R4 | Grupos futuros no contrato atual apenas projeção, dados=false, AWAITING_DATA e físicos null; sem exceção por booleano | future_ET_physical_test e demais grupos; projeções condicionais positivas |
| R5 | Fonte contraditória recusada: dados presentes red/OPEN somente INCONCLUSIVE_SYSTEMATICS; sem dados AWAITING_DATA | red_data_AWAITING_DATA; red_data_INCONCLUSIVE; no_data_OPEN |

[REAL — produtor, não fechamento independente] 58/58 verificações finitas corresponderam às expectativas; negativos aceitos=0. O caso ET é exercitado tanto no grupo de regressão quanto na matriz futura. Harness AST exclui main, publicação e renderização; activate usa apenas arquivos fictícios dentro de fixtures_v2_001. A grade vazia é fictícia, não montagem de E0/E4. Evidence bindings em memória têm números dummy, não ciência. Partiais, bloqueados e indisponíveis não foram promovidos a completude.

Interfaces para R: `generate_reach_table.py` acrescenta `check_timeline`, constantes `SEMANTIC_UNITS`, `FUTURE_GROUPS`, `EVIDENCE_VERDICTS`; `check_metric` aceita terceiro argumento `route`. Adaptar namespace AST para incluir essas definições. Recibos/reviews precisam declarar timeline/predecessor do contrato V2. Não reutilizar dados temporais inventados como evidência real.

Não se afirma que hashes ou timestamps de fonte provem execução física ou independência organizacional. Não são pedidos novos GO ou alto poder: autorização histórica é admissível antes da ativação, mas atividade após ela; poder insuficiente continua veredito válido quando a análise é válida. Uma parede real não necessita timestamps de execução inexistente.

Pins finais estão no manifesto pareado. O principal deve encaminhar este delta e o manifesto a R para revisão focal R1–R5. V2 não está liberada por seus próprios testes. O próximo helper de paredes será outra árvore e não autoriza E6 nem fabrica recibos reais.
