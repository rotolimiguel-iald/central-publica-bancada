# E6 — revisão independente do preparo, V1

**[REAL — revisão finita] BLOCKING_FINDINGS_OPEN. O pacote atual não está liberado para montagem E6.** Cinco achados abaixo permanecem abertos; fechamento exige correção pelo produtor, novos pins e revisão dos deltas. Esta revisão não executou E6 nem produziu quadro científico.

**[INPUT] Escopo:** ordem 013BIS, E6 e sequência obrigatória da Parte B; contrato, código, schemas, manifesto e pins em `bis/e6_prepare`. Escritas exclusivamente em `bis/e6_review`. Nenhum produtor, E2, candidato ou plano de métricas foi alterado. Sem posterior de teste, seed/offset, strain, waveform, PE ou MC. Foram executadas funções selecionadas por AST em fixtures independentes, com raízes redefinidas; `main`, publicação do quadro e montagem com dados científicos reais nunca foram chamados.

## Evidência e limites

**[REAL]** 21 casos finitos: 14 expectativas satisfeitas e **7 entradas negativas indevidamente aceitas**, agrupadas em cinco achados. Preservadas integralmente em `E6_INDEPENDENT_FIXTURE_EVIDENCE_V1.json`; harness `review_fixtures_v1.py`. Não converter 14/21 em aprovação global. As autorizações em `fixture_v1` são fictícias, identificadas como dummy, sem valor operacional. Os casos de ativação usam arquivos fictícios realmente pinados; os casos de binding usam referências exclusivamente em memória para exercitar `append_reviewed`, sem pretender validar custódia real.

**[REAL]** Os 14 pins de fontes/documentos conferiram com os bytes; o manifesto conferiu com seus nove artefatos. A grade vazia fictícia preserva 3 rotas × 10 leituras × 6 grupos = **180 células únicas**, sem seleção por resultado. A inspeção de metadados de seis grupos de campos E0/E4 não encontrou campos obrigatórios ausentes; PSDs/leituras E4 têm enumerações reconhecidas e os detalhes de estatuto C1 coincidem com o contrato. Isso verifica estrutura e identidade, não recalcula os números científicos nem certifica todos os mapeamentos futuros. Evidência separada: `SOURCE_FIELD_METADATA_REVIEW_V1.json`.

**[DECLARADO — exposição da revisão]** Foram lidos código, contratos, documentação e trechos da ordem, que inclui resultados históricos públicos/não cegos. Fontes históricas JSON tiveram acesso restrito a hash e presença de campos/enumerações. Não se afirma cegueira absoluta. Nenhum conteúdo de posterior de teste foi solicitado ou aberto.

## Achados bloqueantes

### E6-R1 — sequência temporal incompleta [OPEN, P1]

Local: `generate_reach_table.py:162`, `:170` e loop de ativação. A ativação E2 é comparada somente à autorização E6. Cada recibo é comparado ao registro E2, sua revisão e autorização; não há vínculo de ordem entre E3.2, E3.3 e TEST.

**[REAL] Reprodução:** `stage_before_E2_activation` aceita recibo E3.2 entre registro e ativação; `TEST_before_allocation_and_calibration` aceita TEST anterior a E3.3 e E3.2, com hashes e revisões locais consistentes. São datas fictícias, não alegação sobre execução real.

**Correção necessária:** usar a conclusão da ativação E2 como limite inferior e validar a sequência obrigatória E3.2 → E3.3 → TEST → autorização E6. O adaptador deve vincular os predecessores por hash e distinguir emissão de recibo de execução/autorizações efetivas: ordenar datas de recibos, sozinho, não prova que houve alocação anterior à execução. Exigir evidência temporal correspondente à regra que se declara satisfeita; não fabricar timestamps retrospectivos. Manter `PARTIAL/BLOCKED/UNAVAILABLE` como paredes explícitas, sem inventar execução paga.

**Fechamento:** os dois negativos devem ser recusados, um fluxo cronológico válido deve continuar aceito, e pins/predecessores divergentes devem falhar. A revisão deve explicitar qual cronologia documental foi demonstrada e qual depende dos recibos reais.

### E6-R2 — classificação incompleta de resultado físico [OPEN, P1]

Local: `:341–363`. `physical` inspeciona apenas `z_physical` e `lnB`; `strong` omite `NOT_FALSIFIED_UNDERPOWERED`.

**[REAL] Reprodução:** `red_gate_physical_ratio` conserva `correction_over_sigma_physical=6` no gate vermelho; o número é dummy. Esse campo também é impresso no Markdown. `unpaid_partial_NOT_FALSIFIED_UNDERPOWERED` aceita esse veredito com etapas `PARTIAL`, flags não pagas e sem passar pela vinculação obrigatória à calibração. A falta de poder não dispensa a validade física da análise.

**Correção necessária:** toda métrica explicitamente física, inclusive razão física do gate, deve passar pelas mesmas exigências de calibração, completude e revisão, ou permanecer null. Distinguir essa razão de `correction_over_sigma` condicional, cuja transcrição diagnosticada é permitida. Aplicar o vínculo de calibração e as condições de validade também ao veredito `NOT_FALSIFIED_UNDERPOWERED`, sem exigir poder alto para esse veredito. Um gate vermelho/OPEN nunca publica significância física. Corrigir o caminho E3.3 além de TEST se ele carregar campo explicitamente físico.

**Fechamento:** recusar os dois negativos; conservar cenários condicionais e paredes null/OPEN; aceitar `NOT_FALSIFIED_UNDERPOWERED` somente com validade paga e potência insuficiente explicitamente revisada. `NOT_FALSIFIED` nunca vira `CONFIRMED`.

### E6-R3 — igualdade de rótulos não garante unidades compatíveis [OPEN, P1]

Local: `:323`, comparação de gate `:354` e `check_metric`. Uma string não vazia basta; dois erros iguais em E3.3 e TEST passam.

**[REAL] Reprodução:** `green_tau_gate_in_Hz` aceita gate de deformação fracionária δτ220 cujos pisos e σc são rotulados `Hz`, chegando a `NOT_FALSIFIED_POWERED` com z físico dummy.

**Correção necessária:** contrato de unidades por rota/campo e validação explícita na entrada. δτ220 e δτ440 são deformações fracionárias adimensionais de modos distintos; δf̂220 fracionário, largura de δf̂, informação de variância e contagem não são intercambiáveis. Razões/z/lnB são adimensionais; taxas e seus IC devem compartilhar base temporal; N90 informacional, contagem condicional e equivalentes de canal precisam de tipos semânticos próprios. Se houver conversão, ela deve vir de fonte revisada e pinada; o builder não deve fazê-la silenciosamente. Null continua admissível para quantidades inaplicáveis com motivo explícito.

**Fechamento:** recusar Hz em δτ e unidades cruzadas 220/440/IV; conservar um binding válido por rota e a separação informação/contagem/equivalentes. Sem recalcular física.

### E6-R4 — projeção futura aceita como resultado observado [OPEN, P1]

Local: `append_reviewed`, aceitação de `data_group` e bloco TEST. O grupo identifica a célula, mas não existe contrato de disponibilidade real do conjunto que impeça promover cenários futuros.

**[REAL] Reprodução:** `future_ET_physical_test` aceita `NOT_FALSIFIED_POWERED` e z físico dummy em ET, com a mesma estrutura de recibos. `test_data_present=true` por si só não distingue projeção de observação futura legitimamente disponível.

**Correção necessária:** nesta preparação, O4c/GWTC6, O5, ET e CE devem conservar resultados físicos OPEN/null e `AWAITING_DATA`, admitindo projeções condicionais rotuladas. Para suportar uso futuro, exigir ato/manifesto de disponibilidade de dados, identidade do conjunto observado e revisão explícita, posteriores à sua disponibilidade; não inferir isso de SNR projetado, N90 ou simples booleano. Vincular essa exceção à autorização, sem alterar E2.

**Fechamento:** recusar o mock ET físico no contrato atual; manter cenários Fisher/âncoras condicionais em ET/CE e as 180 células. Qualquer extensão futura exige contrato revisado, não reclassificação silenciosa.

### E6-R5 — teste presente e vermelho rotulado como ausência [OPEN, P2]

Local: `:364–367`; divergência de `CONTRACT.json:/red_or_open_with_test` e PREPARATION.md.

**[REAL] Reprodução:** `red_data_AWAITING_DATA` aceita `test_data_present=true`, gate vermelho e `AWAITING_DATA`. A parede sistemática desaparece sob um rótulo de ausência.

**Correção necessária:** sem dado → `AWAITING_DATA`; com dado e gate vermelho/OPEN → `INCONCLUSIVE_SYSTEMATICS`, sem campos físicos. Rejeitar combinação contraditória na fonte, em vez de substituir seu veredito silenciosamente.

**Fechamento:** negativo recusado; preservar mock sem dados/OPEN aceito e acrescentar teste presente/vermelho/inconclusivo válido.

## O que está adequadamente preparado

**[REAL — estrutura, não validação científica]** Fonte ausente permanece null/OPEN; os dez nomes/estatutos são preservados sem seleção. O builder separa N90 informacional de contagem de fontes idênticas, equivalentes 220 de informação de variância IV, IC de taxa de incerteza total de poder. Fisher 440 mantém perfil/variante/base SNR; âncora genérica 3G não vira previsão específica. Os pisos históricos 220 não são promovidos a calibração 440/IV. Sem transformar correção/σ condicional em z físico, N condicional em poder real, nem taxa em promessa de anos.

**[REAL — mocks]** Foram recusados revisão anterior ao recibo, hash errado de artefato, bloqueante aberto, bindings divergentes, estágio TEST ausente, pacote alterado, z físico vermelho, hash de calibração divergente, flags físicas não pagas, leitura física com etapa parcial e falsificação sem dados. Permanecem necessários os cinco reparos acima.

**[OPEN — limites documentais]** Os schemas são estruturais e não são validados integralmente no runtime; a validação observada está no código. Nome de revisor não demonstra independência organizacional por si; esta continua uma declaração responsável do ato de revisão/principal. Hash autentica bytes e vínculos, não a verdade física ou independência do autor. Não foram emitidos recibos reais E3/TEST, autorização E6 ou quadro final pelo revisor.

**[DECLARADO — atualização do principal, durante esta revisão]** A nova checagem de metadados de ruído cobre flags/geometria de janelas candidatas e PSD; não foi usada para pagar gate E6. Não foi reaberta nesta revisão. Finitude, qualidade do PSD, SNR atingido e alocação continuam OPEN segundo a atualização recebida. O preparo de injeções e o plano de métricas anterior permanecem preservados; N=1/2 não valida viés entre repetições nem σsys.

## Custódia desta revisão

Os hashes abaixo são preenchidos por leitura dos arquivos. O JSON de evidências contém os 14 pins externos, esperado/medido e resultado. Nenhum fechamento será atribuído automaticamente por alteração de arquivo: requer revisão focada dos novos bytes e negativos correspondentes, preservando esta V1.


| Arquivo revisado | SHA256 medido |
|---|---|
| `e6_prepare/CONTRACT.json` | `156801c4c7beae98b15e32c215d1a2a54eb538225373e455f15703cbc7190419` |
| `e6_prepare/generate_reach_table.py` | `1a2eac3379f67e2c093e0a48815562d9cc238a59ab610d79bc1181fc548e0428` |
| `e6_prepare/OUTPUT_SCHEMA.json` | `b619ca7f564fa0b4debeb3f4ae0898e02c6ce1971f26da0f468e5a601b2d0711` |
| `e6_prepare/PREPARATION.md` | `59562a94cb71a31d39a45c6e21eb597d7cccf16ca08b28ecbb38ce9d6ecf4c2e` |
| `e6_prepare/PREPARATION_MANIFEST.json` | `092575a3956840610d9ee0125f206c0c0185ed6752f18a93d2ededcd82e6fe27` |
| `e6_prepare/prepare_static.py` | `8e6712f11ef641d22c933bbb6586da4c9090fc5bc1e95b236b4cef018a97c805` |
| `e6_prepare/SOURCE_MAP.md` | `3d11faf80325187f01e9231bcb70c894475556244171d256ce869a646736d395` |
| `e6_prepare/SOURCE_PINS.json` | `b52b18616b15342987838edb77d7f4559dc81c5e3cfc8d91b9d957c33b6489af` |
| `e6_prepare/STAGE_RECEIPT_SCHEMA.json` | `32b287dcf7cbbb8fa33fe55af80759a12972497fa10dcf15c75bbc3cb75f85f5` |
| `e6_prepare/STATIC_RECEIPT.json` | `48a12792b646c74d174ba1be743ec915f9218b4b412525c4f04d75ef138cb6ff` |
| `e6_review/review_fixtures_v1.py` | `338b9a3a1ab1afac7f8ae21e61302994cfae946520c53865c76fb181681e86ab` |
| `e6_review/E6_INDEPENDENT_FIXTURE_EVIDENCE_V1.json` | `dc6e8f3349d7c0e798de79a4b63db740b9276a27089201d283db700c99a6e667` |
| `e6_review/SOURCE_FIELD_METADATA_REVIEW_V1.json` | `5ff7b0d0a2c44609abec482415552ef739ce7b1b8c8d1e7a4e4af7ae60fb3058` |

[REAL] Pins do produtor reconferidos ao encerrar; inalterados em relação às fixtures. Relatório escrito em 2026-09-22T22:43:01.691846+00:00.
