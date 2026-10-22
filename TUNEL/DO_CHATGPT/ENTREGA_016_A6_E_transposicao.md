[INPUT — ficha de transposição; REAL — fontes individuais auditadas; MEDIDA — integração monolítica]

# A6.E — ficha para a gerência

Abertura SHA256: `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

Destino proposto: `TGLExt/TheEquationOfTruth.lean`, namespace `TGLExt.EquationOfTruth`; linha para TGLExt.lean: `import TGLExt.TheEquationOfTruth`. Incorporação é da gerência, com ratificação do operador. Nada foi instalado no kernel/um.py.

**Fontes aprovadas individualmente:** 12 fontes, 127 theorem/lemma locais distintos, todos compilados com rc0 e axiomas no trio. A lista integral, enunciados em suas fontes, imports, hashes de fontes/logs/recibos e axiomas estão na ficha JSON. A base selecionada é TheEquationOfTruth_T20_v3, com 57 lemas e os primeiros 28141 bytes da referência V3 preservados exatamente (SHA256 35b91f86b88b8e6c498e8e18305e32ece6802a8e3bf1d6647e6fe75980774ca6). As pontes anteriores usam v1; não se pode importar v1 e v3 no mesmo ambiente. Os 127 lemas não são 127 novos: incluem os 46 reproduzidos.

**MEDIDA obrigatória de empacotamento:** a aceitação estrita de todos os fechamentos em arquivo único com prefixo V3 não está satisfeita. Lean recusa import acrescentado ao fim. A proposta separada de monólito realocou somente imports, sem alterar os corpos, e portanto não preserva aquele prefixo. Compilação com relatórios embutidos terminou rc=3221225477; a variante separando #print terminou rc=1, com mensagem explícita `INTERNAL PANIC: out of memory`, sob o limite de 8 GiB. As duas tentativas, fontes e logs estão preservados. Nenhuma é fonte aprovada para instalar; não se aumentou o limite nem se substituiu falha por PASS. As provas individuais permanecem válidas no escopo auditado.

Ordem proposta: uma base única → pontes de inscrição/Three Locks/Contorno → entropia escalar/derivada/idempotente/taxa → controles modular e infinito → controles negativos. Os imports canônicos necessários incluem TheNameIsTheInstrument, NameIsTheContent, FiniteThreeLocks, TheContourOfTruth e ContinuousModularZero; a lista exata está no manifesto de construção. Uma transposição modular exige regenerar imports dos companheiros e recompilar; esse conjunto integrado ainda não foi certificado.

**Audit e flags:** `PROPOSTA_AUDIT.lean` contém uma linha por teorema local e as sete de TheContourOfTruth. É texto proposto, não auditoria executada do módulo canônico inexistente. A ficha propõe 22 bandeiras ext_eot_*, com consumidores exatos e gate_input=false. Todas são PROPOSAL_NOT_INSTALLED. O limite forte infinito permanece hipótese nomeada, sem bandeira de fechamento. WARNINGS_V3.json lista os 15 avisos originais e distingue os de deprecação.

O que fica fora: entropia matricial do harness, pacote externo 22/22+5, identificação de operandos float do runtime e igualdades entre objetos de tipos distintos. As leituras “verdade”, “memória”, “seleção apofática” permanecem [INPUT/ONTO] em docstrings rotuladas; não são conclusões físicas.

**Frase da ficha:** Estas bandeiras não movem o gate. PROVADA (teorema em kernel) ≠ CONFIRMADA. A implicação está provada a partir das hipóteses nomeadas; a leitura é do operador; a natureza decide a teoria.

Ficha JSON: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A6_EQUACAO_DA_VERDADE\E_ficha\FICHA_TRANSPOSICAO_T20.json`. Próximo alvo da árvore: A7. A6.B1d e empacotamento ficam MEDIDA; a ficha não apaga essas pendências.
