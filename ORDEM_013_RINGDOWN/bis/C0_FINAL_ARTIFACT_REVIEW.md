# Parecer adversarial final dos artefatos C0 — ORDEM_013BIS

[REAL — revisão independente de artefatos e fontes, 22/09/2026] **ACEITO COMO CORREÇÃO DOCUMENTAL, COM LACUNAS EXPLÍCITAS.** Não encontrei novo defeito bloqueante nas seis frases corrigidas, na distinção dos operadores ou no transporte das evidências. Todos os pedidos F1/C0 receberam resposta documental. **Isso não torna integralmente verificada a cronologia de T02, não recupera o template perdido e não fecha a identificação física de τ★/partição.** O rastro histórico primário de T02 permanece PARCIAL; não deve receber PAGO probatório irrestrito.

Este parecer examina somente C0_AUDITORIA_v2.json, C0_ADENDO_FRASES_PUBLICAS.md, REAPROVEITAMENTO_C0.md e o script que os produziu, contra a revisão independente anterior e as fontes nela registradas. Não aprova os outros componentes de F1, não substitui a entrega M1 e não altera gate. O revisor desta tarefa não construiu os artefatos ora examinados.

## Critério e cobertura

Critério lido: [ORDEM_013BIS, F1/C0, linha 72](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md:72>). Na tabela, ATENDIDO significa correção documental sustentada no alcance declarado; não significa conclusão física nem execução nova das inferências históricas.

| Pedido F1/C0 | Localização nos artefatos finais | Resultado independente |
|---|---|---|
| Adendo datado e JSON v2 ao lado, com supersedes | C0_ADENDO_FRASES_PUBLICAS.md:1–5; C0_AUDITORIA_v2.json:757 | ATENDIDO. Hash da v1 preservado; supersedes_sha256 confere. |
| T02: origem da notação e cronologia | C0_ADENDO_FRASES_PUBLICAS.md:9; C0_AUDITORIA_v2.json:746 | RESPOSTA DOCUMENTAL PRESENTE; VERIFICAÇÃO HISTÓRICA PARCIAL. README primário não localizado; datas 25/05 e 31/05 explicitamente DECLARADAS; identidade da fonte externa OPEN. |
| T02: proxy 4×4, seed 11 e alcance não-III₁ | C0_ADENDO_FRASES_PUBLICAS.md:9 | ATENDIDO, conferido diretamente em um.py:2311–2341. |
| T02: família L_k e comparação com Davies | C0_ADENDO_FRASES_PUBLICAS.md:9 | ATENDIDO COM CORREÇÃO DO ESCOPO DA PRÓPRIA ORDEM: um salto em _verb_L; família finita no Artigo A. Não equivalentes. |
| T10: sinal positivo dos catálogos e V2 | C0_ADENDO_FRASES_PUBLICAS.md:13 | ATENDIDO: 24/31 e os dois estratos V2; não somados; sinal negativo da lei de amortecimento contrastado. |
| T11: GW ≈0,18σ e D1 ≈3,01σ | C0_ADENDO_FRASES_PUBLICAS.md:17 | ATENDIDO: efeito/erro separado de probabilidade de poder; convenção simétrica e limitação de cadeia preservadas. |
| T19: −0,1285, supressão canônica e relógio não derivado | C0_ADENDO_FRASES_PUBLICAS.md:21 | ATENDIDO: QNM exato arquivado distinguido de BCW; identificação t_P rotulada; ausência de derivação limitada aos elos examinados. |
| T20/T21: correção β contra σ | C0_ADENDO_FRASES_PUBLICAS.md:25–29 | ATENDIDO: −0,0198452854 / 0,0577943800 → 0,343377425; ensemble, modelo e não-cegueira explicitados. |
| (d): ModularFirstLaw versus ContinuousModularZero | C0_ADENDO_FRASES_PUBLICAS.md:33 | ATENDIDO: Fintype, caráter diagonal e ausência de Σp=1 ditos; unilateral não identificado com superoperador bilateral. |
| (d): fonte teórica III₁ e alcance da leitura | C0_ADENDO_FRASES_PUBLICAS.md:35; C0_AUDITORIA_v2.json:906 | ATENDIDO: traço normal fiel semifinito, representação tracial intrínseca e existência de log Δ separados; fonte e páginas transportadas sem alegar leitura integral. |
| (d): taxas em ±k e (0,1) | C0_ADENDO_FRASES_PUBLICAS.md:37; C0_AUDITORIA_v2.json:764 | ATENDIDO: abs(K) dá zero em ±3; K₊ dá 3β/2; ambas dão β/2 em (0,1); sem unidade SI indevida. |
| Status de arquivamento e referência LVK local | C0_ADENDO_FRASES_PUBLICAS.md:43–48; C0_AUDITORIA_v2.json:644 | ATENDIDO: status corrente atualizado, caminho local e SHA-256 conferem. Arquivado não se tornou integralmente lido. |
| Errata do template histórico | C0_ADENDO_FRASES_PUBLICAS.md:43; C0_AUDITORIA_v2.json:618–660 | ATENDIDA A ERRATA; RECUPERAÇÃO NÃO REALIZADA. Referência histórica retida com mismatch explícito e atual em campo separado. |
| Ficha de reaproveitamento e limites | REAPROVEITAMENTO_C0.md:3–9 | ATENDIDO: existente/reusado/novo/falta discriminados; atribui corretamente ao revisor a reabertura dos HDF5. |

## T02: o enquadramento que foi efetivamente aceito

O texto em [C0_ADENDO_FRASES_PUBLICAS.md:9](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C0_ADENDO_FRASES_PUBLICAS.md:9>) incorpora a distinção central da auditoria: **não há uma família de saltos em `_verb_L`, mas existe família de transições no Artigo A**. A expressão da ordem “família L_k inexistente” não poderia ser repetida para todo o acervo. Corrigi-la por fonte, como foi feito, cumpre a régua em vez de contrariar o objetivo de F1.

Fontes primárias reabertas neste turno:

- [um.py:2311](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/um.py:2311>): `K = (Araw @ Araw.T) / n`, n=4, seed=11 e um único `L = sqrt_beta * sqrtK`.
- [tgl_paper_unified.py:1989](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:1989>): taxas de transição e A_ij=|i⟩⟨j|; laços i≠j, com guarda para gaps numericamente degenerados em 2013. A contagem 56 é a do caso d=8 sem gaps removidos, usado como exemplo; não uma contagem universal para toda entrada numérica.
- [tgl_paper_unified.py:2892](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/tgl_paper_unified.py:2892>): a correção da redundância coerente está no próprio código. O trecho reconhece diferença `-i[K,rho] != 0` para rho genérico e restringe a igualdade ao setor KMS/estacionário. O adendo, linha 39, preserva essa restrição.

O contraexemplo da revisão anterior foi corretamente transportado: salto hermitiano f(K) conserva populações na base de K, enquanto os saltos Davies as transferem. Não se promoveu a matriz finita a construção III₁.

**Limite do aceite:** “família física de horizonte não construída”, na linha 9, é lido no recorte das implementações examinadas, conforme `remaining` do JSON. Não certifico uma busca exaustiva em todo o acervo. A cronologia não verificada continua DECLARADA e a atribuição da fonte do texto externo continua OPEN. O marcador inicial [REAL] do parágrafo não cancela esses estatutos internos explícitos.

## Hipóteses finitas e estatuto documental

[ModularFirstLaw.lean:45–58](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/ModularFirstLaw.lean:45>) foi relido: `[Fintype n]`, p_i>0 e Σq_i=0; não há Σp_i=1. A conclusão é uma derivada diagonal. O adendo acerta ao não atribuir positividade de −log p ao teorema. A afirmação posterior −logρ≥0 pressupõe o estado finito normalizado e positivo, mantendo a positividade estrita já exigida para o log comum. Não é um novo teorema sobre o caso ilimitado.

[ContinuousModularZero.lean:62–93](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/casa/ContinuousModularZero.lean:62>) também é finito: `y * logRho rho - logRho rho * y`, isto é, L_h−R_h para h=−logρ. O nome do arquivo não muda essa hipótese. O adendo não confunde esse superoperador com o h unilateral e não atribui nova compilação ou nova auditoria de axiomas.

Em [C0_ADENDO_FRASES_PUBLICAS.md:35](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/C0_ADENDO_FRASES_PUBLICAS.md:35>), a fonte externa é expressamente atribuída ao **revisor**. O campo `external_primary_reading_scope` coincide integralmente com a revisão independente: Connes pp.133–134 efetivamente consultadas naquela revisão; Sorce, introdução eqs.(1)–(6); nenhuma alegação de leitura integral. Nesta rodada não houve novo download nem nova leitura desses artigos: verifiquei a transferência do recibo e a conservação de seu alcance. A construção modular citada pressupõe Δ positivo **autoadjunto** e injetivo em representação adequada; a frase abreviada do adendo é aceita dentro desse contexto, não para operador positivo arbitrário sem hipóteses.

A falta de leitura integral das provas não impede, por si, atender o pedido documental C0(d), que exige fonte e alcance honesto, não uma reconstrução integral de Tomita–Takesaki. Tampouco autoriza afirmar essa reconstrução. A ausência de traço normal fiel semifinito não foi convertida em ausência de estados normais, inexistência de log Δ ou H_eff=0.

Os campos `independent_findings` mantêm as etiquetas CORRIGIR do parecer recebido. São registro dos achados de origem, transportados literalmente, e devem ser lidos junto às correções correntes; não constituem este novo parecer final. Não houve promoção dessas etiquetas a prova física.

## Verificações efetivamente executadas

[REAL] Verificação por Python em leitura somente, sem importar ou executar o builder:

1. **64/64 hashes** de fontes/scripts do recibo independente conferem novamente; nenhuma divergência.
2. **24/24 itens** preservados. Exatamente T02, T10, T11, T19, T20 e T21 mudaram, somente nos campos de frase, frase anterior e evidência acrescentada. Os outros **18 itens** são idênticos à v1.
3. **38/38 linhas não vazias exigidas** do verbatim cobertas; zero divergência textual. As chaves de evidência de todos os itens resolvem no dicionário `references`.
4. `previous_sentence_v1` coincide com cada frase original substituída. `supersedes_sha256`, hash do verbatim, hash da abertura e hash da revisão independente conferem.
5. As seis expressões do dicionário `corrections` foram avaliadas isoladamente após inspeção de AST, usando somente os dados do recibo, sem executar `main()` nem qualquer escrita. **6/6 frases coincidem** com o JSON final e aparecem literalmente no adendo.
6. `modular_distinctions`, `independent_findings`, `external_primary_reading_scope` e `remaining` coincidem integralmente com seus campos de origem.
7. **17/18 referências locais** do JSON coincidem com o SHA declarado. A única divergência é `references.template`, deliberadamente histórica e anotada; `template_current` confere. Não se deve somar essa referência ao total de integridade como se fosse recuperada.
8. Os hashes dos relatórios citados no adendo/ficha conferem. A v1 permaneceu com o mesmo hash da revisão anterior.

Os números científicos já reproduzidos na revisão independente foram comparados quanto a transporte, método e arredondamento. **Não houve nova PE, leitura estatística dos HDF5, MCMC, KDE conjunto, solução Leaver nem compilação Lean neste turno.** Rehashar HDF5 não equivale a refazer sua inferência. Nenhum arquivo de fonte foi alterado.

## Builder e falha de formatação preservada

[refeito/record_c0_013bis.py:16–24](<C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/refeito/record_c0_013bis.py:16>) recusa destino existente e usa temporário exclusivo, confere bytes e substitui. As linhas 32–35 conferem as fontes do recibo; a linha 124 confere que a v1 não mudou. Não executei esse fluxo de escrita: li o código e conferi os artefatos resultantes.

O arquivo `.failed_PERCENT_FORMAT` está presente e foi hashado. O diff contra o script corrente consiste apenas no escape de dois percentuais literais da frase T20: `2%` → `2%%` e `90%` → `90%%`, na linha 43. A tentativa preservada tem 10.815 bytes; o script corrigido, 10.817 bytes.

A avaliação isolada da string antiga reproduziu:

```text
ValueError: unsupported format character ' ' (0x20) at index 127
```

O erro ocorre na construção de `corrections`, antes da primeira chamada `new`, na linha 70. Isso sustenta a explicação de falha anterior à emissão dos três produtos por aquela execução. O arquivo preservado é o **fonte da tentativa falha**, não um log de execução; o fato histórico foi informado pelo operador e o mecanismo foi reobtido aqui. Não tratei a falha como teste passado nem executei novamente o builder inteiro.

## Pendências que continuam pendências

- **Cronologia T02:** README histórico e datas primárias não verificados. O encadeamento posterior da nota/figura/implementações foi documentado, mas não paga a primeira âncora histórica.
- **Custódia:** a versão histórica do template não foi recuperada. F1 pede a errata e ela está paga; recuperação dos bytes continua ausente. Nada autoriza reprodução byte a byte dos testes históricos com o template atual.
- **Física:** não foi derivada a identificação de τ★, a partição física ou uma dinâmica de horizonte a partir do proxy. São abertos explícitos, não objetivos declarados resolvidos pelo adendo.
- **Literatura/Lean:** somente os alcances de leitura declarados; nenhuma nova prova formal ou compilação. Os demais itens de F1/M1 ficam fora deste parecer.

Conclusão de aceitação: **as correções ao lado estão coerentes com a fonte e podem compor o fechamento documental C0, desde que essas pendências permaneçam visíveis. Não registrar F1/C0 como êxito probatório integral, nem a cronologia T02 como primariamente verificada.**

## Hashes calculados nesta revisão

Todos os caminhos da tabela são relativos à raiz absoluta `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`.

| Artefato | Bytes | SHA-256 calculado |
|---|---:|---|
| C0_AUDITORIA_v2.json | 36040 | `37f4e792584550c7c2ded07b50a7b07befa67a0351a21667ed7c2669903aaef7` |
| C0_ADENDO_FRASES_PUBLICAS.md | 5696 | `81a85af8e96c0b989f1dd3304385b66921c1ab6e939c868aa143551adc195a60` |
| REAPROVEITAMENTO_C0.md | 1286 | `80e82020c2bc722551b99bbce315d5359e8f2e08b66cc88b3330c684baacbb41` |
| refeito/record_c0_013bis.py | 10817 | `44c6a62fecc932e39b86e6682baec257b068543fec6be9618cd7d2c2ef025794` |
| refeito/record_c0_013bis.py.failed_PERCENT_FORMAT | 10815 | `be768f95b68dac2e0e162e1b079c9eb584153cb27912cc150324033f4407795c` |
| C0_AUDITORIA.json | 24269 | `f0009e1194282434ac599a35df68573db08967951a320218184670e15e1559cd` |
| bis/C0_ADVERSARIAL_SOURCE_REVIEW.json | 99236 | `21644dea544c1019c148d585b41997ba6a137b870c5f87a9fb4fb367b865d2e0` |
| bis/C0_ADVERSARIAL_SOURCE_REVIEW.md | 31648 | `a4ee68c4831dd032ee651ec2aff051a515d5e32e256e913e0009238c78369910` |

**Único arquivo escrito neste turno:** `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\C0_FINAL_ARTIFACT_REVIEW.md`. Nenhum script novo, builder, artefato C0, memória ou canônico foi escrito ou modificado.
