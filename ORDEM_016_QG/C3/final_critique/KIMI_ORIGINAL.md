# Auditoria C3 — resposta à pergunta única

**Declaração prévia de escopo:** não executei nada, não compilei, não li arquivos locais; os hashes e contagens abaixo são os **recebidos** (JSON + RELATORIO + trechos Lean), não medidos por mim. O que faço é verificação de coerência interna da evidência contra a frase auditada.

## 1. A frase se sustenta — e com precisão cirúrgica

A evidência sustenta **exatamente** "doze fontes coexistem, com só dois imports trocados e corpos preservados":

- **Coexistem:** 12 grupos rc 0 + `IntegrationAudit.lean` importando as 12, rc 0 — 13 processos seriais, conforme declarado. O DAG fecha dentro do pacote (NegativeControls → controles_v3 → OperatorContourBridge_v2 → InscriptionBridge → T20_v3) mais TGLExt.
- **Só dois imports trocados:** `changes` não-vazio em exatamente 2 de 12 grupos (InscriptionBridge, PenaltyThreeLocksBridge_v2), cada um com **uma** linha de import (`T20` → `T20_v3`). Coerente com "duas linhas de import".
- **Corpos preservados:** `body_bytes_equal: true` em 12/12 e `body_changes: 0`. Detalhe que **confirma** em vez de enfraquecer: `source_sha256 = copy_sha256` nos 10 intocados, e `source ≠ copy` **exatamente** nos dois editados — a assinatura esperada de uma mudança restrita à linha de import. A métrica "corpo = arquivo menos imports" é declarada no relatório (l.18) e tem o mesmo escopo da afirmação; não é circular, porque a exceção está registrada em `changes`.
- **Aritmética fecha:** 57+14+2+3+6+5+2+4+3+4+23+4 = **127** (confere `theorem_count`); 127 + 3 = **130** (`unique_printed`), com os 3 declarados (1 definição + 2 teoremas importados).

## 2. As quatro conferências pedidas

**(a) alias T20/T20_v3 — não existe alias; existe renomeação.** Nada na evidência mostra um mecanismo de alias (nenhum arquivo T20 re-exportando T20_v3, nenhuma declaração de alias). O que houve: os dois consumidores restantes de T20 foram apontados para T20_v3; FiniteGapRate_v2 já a usava (changes vazio — coerente com "já usada pela taxa espectral"). Consequência: **T20 não é mais referenciada por nada no pacote** — se existe em disco, ficou órfã (não medido). Isto não é erro; é uma diferença factual em relação à palavra "alias", que convém não usar: o resultado é **substituição de referência**, não alias.

**(b) alcance do consumidor com prints.** O IntegrationAudit demonstra: (i) as 12 fontes compilam sob um único import; (ii) as declarações impressas estão no trio (audit PASSA). Limites do que ele demonstra: os 2 `#print axioms` exibidos são amostra; os outros 128 não foram exibidos; **cobertura integral e zero-sorry são alegados via `AXIOM_AUDIT.json`, que não foi fornecido** — aceito como INPUT relatado, não como verificado. E um limite estrutural: coexistência **no pacote isolado** ≠ coexistência **com o canônico**. O pacote depende de `TGLExt.TheNameIsTheInstrument`, `TGLExt.NameIsTheContent`, `TGLExt.ContinuousModularZero`, `TGLExt.TheContourOfTruth`, `TGL.FiniteThreeLocks`; **a versão do TGLExt do ambiente de compilação não está pinada na evidência**. Se divergir do canônico, compila aqui e falha na incorporação. O relatório diz corretamente "é o pacote verificável para a gerência incorporar" — a verificação de interface é da incorporação, não desta rodada.

**(c) 127 teoremas / 130 declarações.** Sem inconsistência: a soma por grupo dá 127; as 130 impressas incluem 3 externas (declarado). rc 0 no consumidor também implica **ausência de colisão de nomes** entre os 12 módulos — bom sinal adicional para "coexistem".

**(d) FlowTendsToFamily disfarçada? Não.** Pelos trechos:
- É `def ... : Prop` rotulada "Hipotese NOMEADA" (l.298-300) e entra como **parâmetro** `hlim` em `conserved_iff_factors` (l.305) e `conserved_iff_factors_T` (l.326). Hipótese explícita, não conclusão.
- A única descarga é `conserved_iff_factors_of_nonneg` (l.644-648), sob `variable [FiniteDimensional 𝕜 E]` (l.642), via `flowTendsToFamily_of_finiteDimensional H hH hpos`. Ou seja: **em dimensão finita, com H autoadjunto não-negativo, a convergência é teorema** — com nome distinto e contexto explícito, não escondida. Ressalva minha: o **corpo** de `flowTendsToFamily_of_finiteDimensional` não está nos trechos; sua existência e tipo são garantidos pelo rc 0, seu conteúdo fica coberto pelo audit não exibido.
- O relatório (l.24) declara abertamente: "A recíproca infinita ainda conserva FlowTendsToFamily como hipótese; não foi paga por esta ligação." Não há disfarce no texto.
- **Também não disfarçadas:** `hinj : Set.InjOn l (H.ker)` é parâmetro (l.654); `[H.ker.HasOrthogonalProjection]` é condição de instância explícita nas assinaturas; a compatibilidade nome=conteúdo está marcada "INPUT/ONTO compatibility" no próprio código (InscriptionBridge l.12-13) — alinhada com a v368 da memória (decisão do operador, não descrição do artefato).

## 3. Separação pedida: três camadas, três estatutos

1. **Leitura preservada** — `reading_T H hH s x` (usada em InscriptionBridge e nos teoremas de conservação): **provada**, é a espinha do pacote.
2. **Leitor discriminante (InjOn)** — `distinguishing_reading_iff` / `distinguishing_verdict_eq`: **condicionais**; a injetividade de `l` no kernel é hipótese `hinj`, nunca conclusão. O comentário em l.661 ("Equality of binary comparisons, not equality of numerical distances") marca a limitação corretamente.
3. **Vínculo físico Ward/BW** — **ausente do pacote e não reivindicado**: o relatório nega identificação entre fluxo dissipativo e fluxo modular unitário (l.26-27) e remete o cociclo físico ao C4. Nenhuma ponte com H2/H3, gráviton ou horizonte segue desta entrega.

## 4. Conclusões mais fortes que NÃO seguem

1. Que o pacote esteja no canônico — o JSON declara `kernel_installed: false`, `gate_changed: false`.
2. Qualquer verdade física (Ward, BW, H2, H3, gráviton, dinâmica dissipativa = modular unitária).
3. Que FlowTendsToFamily esteja provada em geral (vale hipótese no caso abstrato/infinito; teorema só finito-dimensional, não-negativo).
4. Que algum leitor concreto discrimine (InjOn é hipótese; nenhuma instância exibida).
5. Completude da auditoria de axiomas/zero-sorry (base `AXIOM_AUDIT.json` referenciada, não exibida; 128 prints não exibidos).
6. Que 127 meça profundidade, novidade ou não-vacuidade matemática — é contagem de declarações; a força dos controles negativos (23+4 teoremas) não é avaliável sem seus corpos.
7. Que T20 foi eliminada ou virou alias — apenas deixou de ser consumida pelo pacote.
8. Que a interface com o TGLExt canônico está garantida (versão do ambiente não pinada).
9. Que entropia escalar do qubit escala para entropia matricial (o relatório mesmo o nega, l.25-26).
10. Que a recíproca vale sem `T2Space Y` ou sem `Continuous l` — ambas são usadas (unicidade de limite; composição com Tendsto).
11. Qualquer efeito sobre gate, selo ou os 5750 teoremas do canônico.

## 5. Correção concreta — uma só, de redação

No RELATORIO l.20-23, a lista do que convive marca todos os itens com escopo ("recíproca **em dimensão finita**") exceto um: **"comparação discriminante"** aparece sem qualificador. Como o conteúdo é `distinguishing_*` **condicional a InjOn**, proponho trocar por "comparação discriminante **condicional (InjOn como hipótese)**". Uma palavra, nenhuma camada nova, nenhum código tocado. Fora isso, não encontrei erro factual: aritmética, contagens, escopo dos imports e honestidade das hipóteses estão consistentes em todas as fontes recebidas.

## 6. Lacunas declaradas

Não vi: `AXIOM_AUDIT.json`; os 128 prints restantes do IntegrationAudit; o corpo de `flowTendsToFamily_of_finiteDimensional`; os corpos dos 27 teoremas de controles; a versão/hash do TGLExt do ambiente de compilação; a existência ou não de T20 em disco. Hashes: recebidos, não medidos. Nada foi executado, compilado ou alterado; o gate e o canônico não foram tocados — e nada nesta auditoria os move.