[REAL — C1/F1: B1/B2 e R1–R3 encerrados para os artefatos e controles auditados; sem alteração de gate]

# Fechamento da revisão C1

Data UTC: 2026-09-22T17:46:55.493227+00:00. Raiz dos caminhos: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`.

**APROVADO no escopo desta revisão.** Os dez controles originais e as quatro mutações adicionais foram recusados sob `python -B -O` (optimize=1). A guarda de bytes também recusa a divergência nesse modo. Não restou bloqueante dos achados nomeados. Esta aprovação não certifica ausência universal de defeitos nem aprova F1/F4 ou a ordem inteira.

| Achado | Evidência de encerramento |
|---|---|
| B1 — duplicatas/NaN/cobertura | Guardas explícitas permanecem operantes com otimização; controles positivos passam e mutações anteriores são recusadas. |
| B2/R1 — chaves da evidência | A validação reabre CSV/catálogo cujos hashes conferiu e compara a grade de evidência com as chaves efetivas. Prefixar todos os eventos com WRONG_ agora é recusado. |
| B2/R2 — cinco perfis | Tabela vazia e redshift alterado são recusados; esquema e conjunto exato de cinco leituras são exigidos. |
| B2/R2 — sete QNM | Remover os pares é recusado; esquema exato e par finito com convenção real positiva/imaginária negativa são exigidos nos sete spins. |
| R3 — bytes | Corpo isolado de write_new compilado com optimize=1: bytes íntegros alcançam replace; bytes simulados divergentes recebem ValueError antes de replace. |

Os testes alteram somente cópias em memória. Importei o módulo de guardas inspecionado; não executei main do medidor, registrador, teste original ou um.py. A sonda de escrita usou caminhos simulados sem operações no disco de produção.

**Proveniência e preservação:** v4_generator e evidence_validator conferem por hash com os novos scripts; supersedes aponta à v3 correta; origin_generator continua identificando o gerador original. É correto que o controle numérico v2 continue citando a guarda v1 que o produziu: a nova guarda v2 está identificada separadamente como validador do registrador v4. Não houve reatribuição retrospectiva de proveniência.

O controle numérico v2 permanece byte a byte igual. As dez linhas de C1_LEITURAS_v4 são iguais às da v3. Mantém-se a conferência independente anterior: 264/264 linhas, diferença relativa máxima 2,1237132116536×10⁻¹⁵, 99 pequenas não nulas + 33 R-GLOBAL = 132; sete QNM, dimensões e perfis conferidos. A revisão não repetiu computação sem mudança de valores.

O corpo editorial foi preservado: cota P2 da série mediana com calibração e sem confiança atribuída; ν com ω_R e κ em s⁻¹; BW limitado às seções lidas; Kay–Wald/Sewell sem promoção a integrais lidos; Kerr–KMS ainda [CONJECTURE]; nenhuma escolha física ou fala do operador preenchida. Todos os hashes citados no novo adendo/ficha foram reconhecidos contra os arquivos lidos. As versões históricas monitoradas permaneceram intactas.

## Reprodução

Controle e evidência em bis/c1_review/closing_c1_checks.py e closing_c1_results.json. Comando executado da Central:

```powershell
& 'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -O 'Chatgpt/ORDEM_013_RINGDOWN/bis/c1_review/closing_c1_checks.py'
```

As saídas recusam sobrescrita. Para reproduzir novamente, usar uma cópia isolada preservando a estrutura relativa e os insumos. Axiomas: N/A — sem Lean. Sem PE, injeções, alteração de memória/canônico ou execução de produção.

| Arquivo | SHA256 lido por script |
|---|---|
| `refeito/c1_evidence_guards_v2.py` | `69dff0a899f531bb4104ba3ab32fc061cab0508ab02d06105962a03c5edf30ff` |
| `refeito/record_c1_013bis_v4.py` | `1967c46dc3eafc55b2e38df16e9157d1ea4503f8943347676c71e82d35a3bbfd` |
| `C1_LEITURAS_v4.json` | `126270a896d8589870954b209155f26a8b08295839b31e0e9a6e28e512621980` |
| `C1_ADENDO_CORRECOES_013BIS_v3.md` | `a688b542e5d4d1c6be356d2196f6bf9661609bc9b0c50c7ea3b0152fe3e2feed` |
| `REAPROVEITAMENTO_C1_v3.md` | `81f52718f827ef20fed6d1026371a0bb00614a4dde2c10a4af78cdc7e8311fbc` |
| `bis/C1_NUMERICAL_CONTROLS_v2.json` | `a5c943922993fdef3d09a8b898feb4210586e360121c32da4857ddd644e3edec` |
| `bis/c1_review/closing_c1_checks.py` | `6f84c0157ff98f58efba7bd9f34c657476dcef72ef5a209c83a40ce7fe0a163a` |
| `bis/c1_review/closing_c1_results.json` | `aab005f72450b9ee6d4a14d89b1475798f859ef916c680109c6e5a3ebdd8ae73` |
