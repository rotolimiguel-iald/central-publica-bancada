[REAL — fechamento independente dos achados C7-R1–R4, com controles leves; OPEN — R4 residual documental]

# C7 v3_2 — parecer de fechamento

Data UTC: 2026-09-22T18:46:17.171840+00:00. Escopo: pacote `C7_INDEPENDENT_v3_2`, seu builder, wrapper e validator. Não reabre F2/C6 nem a ciência congelada; suplementos têm revisão separada no adendo de C7_V3_REVIEW.md.

**C7-R1, C7-R2 e C7-R3 fechados no escopo dos defeitos relatados. C7-R4 permanece parcialmente aberto, P2, por dois hashes de atribuição desatualizados.** Os recibos da nova C6 do operador conferem como PASS; nenhuma C6 foi iniciada por esta revisão.

## Fechamentos comprovados

- **R1, fechado:** JSON recusa NaN/Infinity/−Infinity; os três campos numéricos por linha exigem tipo int/float, excluem bool e exigem finitude. A diferença final também exige finitude. Executei as unidades embarcadas com `python -B -O`: PASS, 48 negativas e cinco recusas de entrada. Controle independente no código real isolado por AST: 2.700 mutações recusadas, cobrindo 75 posições × três campos × seis entradas inválidas, nos lados referência e resultado. Os três tokens JSON e seis casos de cobertura/tipo/erro/overflow também recusam. Íntegro dá 75 linhas e erro zero; NOT_VERIFIED continua permitido e CONFIRMED recusado. São controles de código, não novos resultados científicos.
- **R2, fechado para os dois caminhos denunciados:** validator recusa recibo existente antes de mkdtemp; wrapper recusa resultado existente antes de mkdtemp e executa chmod dentro do try. Sondas em memória sob optimize=1: zero temporários nas recusas; PermissionError injetado em chmod gera remoção do filho validado e relatório REPRODUCTION_FAILED com temporary_removed=true, propagando a falha. Não foi feita remoção real por essas sondas. Isso não constitui prova de todo erro de sistema possível.
- **R3, fechado:** marca `CONJECTURE — management hypothesis, not TGL canon` correta em runtime com QNM fornecido, README/OVERVIEW e seis linhas R-MOD das tabelas JSON/CSV. UTF-8 e “5–95%” conferem; paredes Kerr/partição laboratorial preservadas. A constante de teste centraliza a marca esperada; o builder ainda repete literais, mas o defeito de bytes/retorno foi corrigido e protegido pelos testes.

## R4 — correção substantiva, fechamento ainda impedido

Ledger, três records Zenodo e declaração GWOSC agora estão embarcados. Seus hashes conferem contra fontes locais; ids declarados conferem nos records. README distingue declarações arquivadas de textos integrais externos, não atribui licença geral ao código e corrige o ponteiro dos intervalos de catálogo. Português foi identificado como documentação-fonte original. Não foi realizada análise jurídica ou busca externa.

`SHIPPED_ATTRIBUTIONS.json` cobre 78 dos 79 arquivos do manifesto, excluindo corretamente a si próprio para evitar auto-hash. **76 hashes conferem; README e OVERVIEW não conferem.** O manifesto principal e o ZIP estão corretos; a inconsistência é entre o ledger por arquivo e os bytes finais desses dois documentos.

| Arquivo | SHA256 declarado na atribuição | SHA256 efetivo lido |
|---|---|---|
| `README.md` | `48184b62f1f689314e909b19b4eacbd456651f8eaf96908d829e43648811251d` | `a6db77c9856581b88f6f75dfefea55a29989829d6c2f5706d7416043028e7eaa` |
| `OVERVIEW.md` | `48184b62f1f689314e909b19b4eacbd456651f8eaf96908d829e43648811251d` | `a6db77c9856581b88f6f75dfefea55a29989829d6c2f5706d7416043028e7eaa` |

**Causa precisa:** `refeito/build_independent_v3_2_013bis.py:98–105` gera o ledger de atribuições; `:106–111` depois modifica README/OVERVIEW (ponteiro, frase das licenças e parágrafo de idioma). O ledger reteve os hashes anteriores.

**Correção exata em nova versão:** concluir todas as mudanças em `content`, inclusive README/OVERVIEW, antes de gerar SHIPPED_ATTRIBUTIONS; então calcular hashes do conteúdo final. Acrescentar guarda explícita, operante sob −O, que valide conjunto/duplicatas e cada hash de atribuição contra os bytes efetivamente embarcados, excluindo apenas os manifestos autorreferentes declarados. Só depois gerar o manifesto final e ZIP. Testes leves bastam; essa correção documental não demanda C6 nova. Preservar v3_2 e recibos.

## Integridade e reprodução do operador

79/79 arquivos do manifesto conferem por tamanho/hash e o ZIP contém esses arquivos mais MANIFEST, byte a byte. v3_1 e seu ZIP continuam nos pins anteriores; reprodução científica congelada não mudou. Nenhum artefato de produção foi escrito.

`C7_V3_2_CLEAN_VALIDATION.json` e `C7_V3_2_C6_REPLAY.json`: PASS, 75 linhas, diferença máxima zero, estatuto científico **INCONCLUSIVE_SYSTEMATICS**. Conferi identidade de ZIP/manifesto/wrapper/validator/registro/referência, quatro logs de validação e o log de execução; os dois temporários informados estão ausentes. Este parecer confere os recibos da execução do operador, sem executar outra campanha. PASS numérico não promove o estatuto físico.

Controles em `bis/c1_review/c7_v3_2_closing_checks.py`, `c7_v3_2_closing_results.json` e `c7_v3_2_replay_receipt_check.json`. Ciência, PE, C5, injeção A, memória/canônico e F2/C6 fechado ficaram fora do escopo.

| Caminho relativo à raiz | SHA256 lido |
|---|---|
| `refeito/build_independent_v3_2_013bis.py` | `c77a8a7f597362cbba0e3062cd3f561c917ac8bad1183e7eeebd0fbd1ca0260f` |
| `refeito/reproduce_c6_v3_2.py` | `c9477017041da663c0c5954b9611d8b5c39df91f7ab6e1647dfd600ca6999b47` |
| `refeito/validate_package_v3_2_013bis.py` | `030fa8b79211fb043d04b2bc613b14284f9cccb6abd784d0987dbba4adc3d4e4` |
| `C7_INDEPENDENT_v3_2/MANIFEST.json` | `7267e0311dcd321995be26b8d3d7a5947cf28d2a8055039410e6382f20edd699` |
| `cache/C7_INDEPENDENT_v3_2.zip` | `6e623cf5a209e38bf28d74a20f0b1db259f88c262ccad30878436efce4716f44` |
| `C7_INDEPENDENT_v3_2/provenance/SHIPPED_ATTRIBUTIONS.json` | `ca02f4c58ca17aa9bc92641a03840aa6b8639effd79388113ae6cb19fc5f6fe4` |
| `bis/c1_review/c7_v3_2_closing_checks.py` | `416ae654c02755b11e8e84d311fc5bdaa6472c3230aeed504183de1ebb8c422b` |
| `bis/c1_review/c7_v3_2_closing_results.json` | `d876dfa0536e413706084198c38124ffb9ccc6f982e0abc1ba9eb108154d8a2d` |
| `bis/c1_review/c7_v3_2_replay_receipt_check.json` | `7bcabba679cf6b367b3af2565aa352ab810284b81d650cdea85cd57430e425cd` |
