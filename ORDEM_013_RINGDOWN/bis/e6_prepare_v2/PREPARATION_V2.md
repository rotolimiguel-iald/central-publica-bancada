# E6 preparo V2 — correções R1–R5, não executado

[INPUT] Correção solicitada pelo principal após `bis/e6_review/E6_INDEPENDENT_PREP_REVIEW_V1.md`. A v1 permanece intocada e foi copiada byte a byte em `v1_snapshot/`. Esta árvore é nova; não altera E2, ciência, fontes históricas, parâmetros, tolerâncias dos produtores ou escolhas de leituras. Não há autorização para executar E6.

O quadro e mapeamento históricos continuam os de `v1_snapshot/SOURCE_MAP.md`: três rotas, dez leituras e seis grupos, cenários preservados, sem novos cálculos físicos. O contrato V2 restringe somente entrada, cronologia, semântica e classificação. Não executar `main`, montar fontes científicas reais ou publicar quadro durante este preparo. Fixtures permitidas: metadados fictícios e funções isoladas, sem strain/posterior/seed/ondas/PE/MC.

## R1 — evidência temporal e predecessores

O recibo adaptador passa a `E6_REVIEWED_STAGE_V2`. Além dos campos anteriores, requer `predecessor` (referência por caminho/SHA) e `timeline`. A revisão independente deve reproduzir exatamente bindings, outcome, predecessor e timeline. E3.2 referencia o recibo de ativação E2; E3.3 referencia o recibo E3.2; TEST referencia E3.3. Não é busca automática de versões.

`timeline.evidence` aponta a JSON revisado/pinado, com pointers literais para timestamps existentes:

- `ALLOCATION_REGISTERED` em E3.2: `authorized_utc_pointer`, `started_utc_pointer`, `finished_utc_pointer`; início/fim podem apontar ao mesmo instante efetivo da alocação quando a fonte assim o registra.
- `EXECUTED` em E3.3/TEST: os mesmos pointers, referentes à autorização e atividade efetivas. A conclusão do predecessor não pode vir depois do início atual. Os estágios E3.3/TEST incluem `predecessor_evidence_sha256_pointer`: o valor fonte deve vincular o SHA da evidência temporal precedente, além do vínculo entre recibos adaptadores.
- `NO_EXECUTION`, somente em PARTIAL/BLOCKED/UNAVAILABLE: `recorded_utc_pointer` e `reason_pointer`, lidos da parede documental. Não exige nem inventa hora de execução. Uma atividade não pode suceder requisito sem execução/alocação, mas paredes sucessivas são permitidas.

O limite inferior da atividade/registro da parede é `E2_ACTIVATION_COMPLETE.finished_utc`. Start ≤ finish ≤ emissão do adaptador ≤ sua revisão ≤ autorização E6 ≤ agora. Adaptadores são emitidos em ordem e seus predecessores são pinados; a cronologia das atividades é conferida separadamente. Uma autorização/GO preexistente pode anteceder E2, desde que a atividade efetiva não anteceda a ativação e a autorização fonte não seja posterior ao início. Nenhuma exigência de novo GO foi criada.

Adaptador retrospectivo deve dizer sua data real de emissão; não pode usar um timestamp antigo fictício para parecer anterior à execução. Os campos temporais e links precisam vir de evidências verdadeiras e revisão responsável. Se o formato legado não comportar diretamente a evidência, um envelope documental novo deve pinar e explicar as fontes originais e ser revisado; não preencher um registro antigo nem alegar prova temporal que não existe. Hash assegura vínculo de bytes, não autenticidade física do relógio. Evidência ausente permanece parede, sem resultado físico.

## R2/R5 — números físicos e vereditos

`z_physical`, `lnB` e `gate.correction_over_sigma_physical` são campos físicos. Antes de TEST permanecem null. Em TEST, qualquer um deles ou qualquer veredito de evidência (incluindo NOT_FALSIFIED_UNDERPOWERED) requer completude dos estágios, calibração E3.3 compatível pinada, gate verde, flags de validade pagas e decisões revisadas. A razão física do teste não é exigida no artefato de calibração; comparam-se os demais números/unidades de calibração, não um resultado de teste contra ausência de teste.

NOT_FALSIFIED_UNDERPOWERED requer `power_assessment=INSUFFICIENT_REVIEWED`. Isso **não exige z≥5, poder≥90% ou qualquer limiar numérico alto**. A insuficiência de poder não paga validade/calibração. Os cenários condicionais `correction_over_sigma` permanecem transportáveis mesmo com gate vermelho, claramente identificados; nunca viram significância física.

Estado coerente da fonte: sem dados de teste → AWAITING_DATA e números físicos null; dados presentes e gate vermelho/OPEN → INCONCLUSIVE_SYSTEMATICS e números físicos null. Combinação contraditória é recusada, não rebatizada pelo montador. Esse uso de INCONCLUSIVE_SYSTEMATICS está entre os vereditos permitidos pelo E2/ordem; NOT_FALSIFIED_UNDERPOWERED fica reservado aqui à análise válida com poder insuficiente. PARTIAL/BLOCKED/UNAVAILABLE continuam admitidos como paredes sem números físicos.

## R3 — tipos semânticos de unidades

`CONTRACT.json:/semantic_units` e `SEMANTIC_UNITS` enumeram unidades por rota/campo. Fracional dtau220, fracional dtau440, fracional df220 e largura fracional df220 são tipos diferentes. Informação de média em tau, informação de variância em df, contagens e equivalentes também. Razões, z e lnB são adimensionais. Taxa e IC90 usam a mesma base anual; não há conversão de unidades. Campo inaplicável fica null/OPEN com motivo; string vazia nunca é unidade.

As unidades antigas dos cenários históricos permanecem aceitas somente no canal correspondente. Gate numérico tem tipo próprio por rota; piso dtau não entra em largura df. Uma conversão necessária deve existir explicitamente em fonte revisada/pinada com seu escopo, não ser feita silenciosamente pelo montador. A comparação entre duas strings iguais não substitui a verificação de seu tipo permitido.

## R4 — grupos futuros

O4C_GWTC6, O5_BANDA, ET e CE só comportam projeções condicionais no contrato atual. Em bindings de TEST: `test_data_present=false`, AWAITING_DATA, z/lnB/razão física null. Não há exceção por booleano ou por autorização genérica E6. Fisher e âncoras condicionais futuras permanecem intactos. Uso observacional futuro exigirá outro contrato revisado com manifestação efetiva de disponibilidade/identidade de dados e autorização específica; não se alterará E2 nem se reclassificará projeção silenciosamente.

## Interface e fechamento

O comando futuro permanece `generate_reach_table.py --execute --authorization <arquivo-real> --authorization-sha256 <hash-real>`, agora na árvore V2. **Não executado nesta entrega.** A autorização futura deve pinar os quatro arquivos exatos do pacote V2; a V1 não libera V2. Schemas são documentação estrutural; validação semântica efetiva está nas funções do código.

O manifesto final conterá hashes calculados, predecessor V1, testes e delta. O principal/R devem conferir os negativos focados antes de fechar a revisão. Não há recibos E3/TEST reais, ativação E6, quadro, admissão de evento ou extração E7 produzidos aqui. Nome de revisor no contrato é declaração de responsabilidade; não prova independência organizacional.
