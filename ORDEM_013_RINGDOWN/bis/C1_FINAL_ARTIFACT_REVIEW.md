[REAL — revisão adversarial independente C1/F1; artefatos numéricos atuais aprovados no escopo; B1 corrigido, B2 parcialmente corrigido; nenhuma alteração de gate]

# Revisão final dos artefatos C1 — segunda rodada

Data UTC: 2026-09-22T17:36:20.952071+00:00. Raiz dos caminhos relativos: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN`.

**Decisão: os novos artefatos preservam os números aprovados e corrigem a proveniência e os pontos editoriais. As dez mutações anteriores foram recusadas sob `python -O`. Não encerro B2 nem certifico ainda a rotina inteira como fail-closed:** há três correções residuais abaixo, reproduzidas com controles leves. Nenhuma delas demonstra corrupção dos dados atuais; todas dizem respeito à capacidade de recusar evidência inadequada ou uma escrita divergente.

Este parecer se limita a C1/F1. Não aprova F1 inteiro, não exige publicação de um rascunho, não duplica F0/F2/F7 e não move estatutos físicos. O parecer anterior permanece intacto em `bis/C1_ADVERSARIAL_REVIEW.md`.

## Correções conferidas

| Item anterior | Resultado |
|---|---|
| B1: duplicatas, NaN e cobertura de entradas | **CORRIGIDO.** `validate_inputs` recusa duplicatas e valores não finitos e exige a mesma grade 33×8 no catálogo/CSV. As guardas usam exceções explícitas. |
| B2: status, dependências, erros, P1/P2/Unruh-g, cota e contagens | **CORRIGIDO nessas partes.** Hashes das dependências obrigatórias são cruzados, erros são finitos e menores que 10⁻¹², P1 e selo declarado do cache são verificados e as contagens do adendo vêm do retorno validado. Persistem R1/R2. |
| Proveniência da nova versão | **CORRIGIDO.** `origin_generator_sha256` corresponde ao gerador da origem; `v3_generator` corresponde ao registrador v3; `supersedes` aponta à v2 com o hash correto. |
| Cota P2 | **CORRIGIDO no adendo.** Série mediana, margem de calibração e ausência de nível de confiança agora explícitas. |
| ν, κ e frequência complexa | **CORRIGIDO no adendo.** Usa ω_R, explicita κ em s⁻¹ e separa −Im ω na determinação de τ_GR. |
| Sewell | **CORRIGIDO.** Saiu a afirmação de falha web sem log; permanece a página recebida sem artigo. |
| Alcance BW/Kay–Wald/Sewell e hipótese física | **PRESERVADO.** Não se anuncia leitura de todas as provas/PDFs, acesso a texto não obtido nem prova de estado físico Kerr–KMS. |
| Ficha de reaproveitamento | **Referências de linhas corrigidas; hashes conferem.** Scripts/guardas são rastreáveis pelos JSONs, embora a ficha pudesse enumerá-los diretamente. |

## R1 — B2 ainda aceita uma grade de eventos diferente da fonte hasheada [P2]

**Local:** `refeito/c1_evidence_guards.py:61–62`.

`keys(rows, 'measured evidence')` prova que a evidência contém 33 eventos e oito leituras por evento, mas seu conjunto de chaves não é comparado com o CSV/catálogo cujos hashes acabaram de ser conferidos. `validate_inputs` faz essa comparação na etapa do medidor; o registrador chama somente `validate_evidence`.

**Contraexemplo medido:** em cópia somente em memória de `C1_NUMERICAL_CONTROLS_v2.json`, prefixei todos os nomes de evento em `csv_checks` com `WRONG_`. Preservei as 264 linhas, os erros, as contagens e todos os hashes de dependência originais. `validate_evidence` aceitou uma evidência cujas chaves não pertencem ao CSV.

**Correção exata:** dentro de `validate_evidence`, carregar o CSV e o catálogo já validados por hash, aplicar `validate_inputs` e exigir `keys(measured['csv_checks'], ...) == set(validated_csv)`. Rejeitar antes de criar a saída. Acrescentar a mutação de nomes mantendo intactos os hashes. Isso fecha a ligação entre “264 linhas” e “as 264 linhas desses insumos”.

## R2 — B2 não exige esquema completo de perfis e pares QNM [P2]

**Local:** `refeito/c1_evidence_guards.py:80–87`.

O laço dos perfis só verifica finitude dos campos presentes em cada linha; não exige linhas, leituras únicas ou z=0. O laço dos spins exige os sete valores de spin, mas só percorre os campos existentes, sem exigir os pares QNM.

**Três contraexemplos medidos, todos aceitos sob `-O`:**

1. `profile_comparison=[]`: a evidência parcial passa, e o registrador pode publicar uma tabela de perfis vazia.
2. `profile_comparison[0]['comparison_redshift']=1`: passa apesar de o adendo afirmar comparação em z=0.
3. Retirar `exact_qnm` das sete linhas de `spin_comparison`: passa sem os pares que sustentam a evidência QNM do novo discriminante.

**Correção exata:** exigir exatamente cinco perfis distintos (`R-A`, `R-B`, `R-RAIZ-EP4`, `R-RAIZ-REST`, `R-LIN`), os campos numéricos completos e `comparison_redshift == 0`. Para cada um dos sete spins, exigir `exact_qnm` com dois números finitos (parte real positiva e parte imaginária negativa na convenção adotada), `delta_mod`, `delta_root_zero`, `delta_mod_bcw_control` e `mod_bcw_relative_error`, além de `spin`. Rejeitar campos obrigatórios ausentes. Guardas de esquema não substituem a auditoria física/numérica já feita; apenas impedem certificar uma evidência incompleta como se fosse a mesma.

## R3 — Conferência dos bytes do registrador desaparece com `-O` [P2]

**Local:** `refeito/record_c1_013bis_v3.py:13`, em `write_new`.

Permanece `assert tmp.read_bytes()==raw`. Essa conferência é removida pelo interpretador otimizado. Isolei somente o corpo dessa função por AST, sem executar o registrador, e forneci caminhos simulados inteiramente em memória que devolvem bytes divergentes:

| Modo de compilação da função | Divergência recusada? | `replace` alcançado? |
|---|---|---|
| normal | Sim, `AssertionError` | Não |
| optimize=1 | Não | Sim |

**Correção exata:** substituir por `require(tmp.read_bytes() == raw, 'Output bytes differ')` ou exceção explícita equivalente. Manter o teste em caminho simulado sob `-O`. Não houve corrupção de arquivo real no ensaio. A ausência de sobrescrita em concorrência continua sendo uma propriedade distinta da conferência de bytes e não foi exercitada aqui.

## O que foi efetivamente revalidado

Executei um controle próprio com **Python `-B -O`**, registrando `sys.flags.optimize=1` e escrita de bytecode desativada. Importei apenas o módulo de guardas, previamente inspecionado e sem efeitos de escrita no import; não executei os `main` do medidor/registrador nem o script original de mutações, que grava em outro destino.

- Controle positivo: os dados atuais passam nas novas guardas.
- Dez mutações originais: **10/10 recusadas**, reproduzidas independentemente. O hash do script original confere com `C1_GUARD_MUTATION_TESTS.json`.
- Quatro mutações complementares de evidência: **4/4 aceitas**, conforme R1/R2. São os casos remanescentes, não falhas das dez recusas registradas.
- Prova de escrita simulada: conforme R3, sem escrever em nenhum artefato de produção.
- Todas as referências de hash dos novos JSONs/adendo/ficha conferem com os bytes encontrados.
- Todos os insumos monitorados permaneceram idênticos durante esta revisão; os 26 insumos da revisão numérica anterior também conservam seus hashes.

**[REAL — números]** `C1_NUMERICAL_CONTROLS_v2.json` difere do controle anterior somente em `utc` e `dependencies`. Todos os valores numéricos, 264 verificações CSV, sete spins, perfis, dimensões e cota P2 são iguais aos já auditados. As dez linhas de `C1_LEITURAS_v3.json` são iguais às da v2 aprovada numericamente. Logo, permanece aplicável a conferência independente anterior: erro relativo máximo **2.12371e-15**, 99 linhas pequenas não nulas + 33 R-GLOBAL = 132, QNM e perfis conferidos. Não refiz contas caras nem reabri PE para comparar valores idênticos.

O arquivo original dos dez testes não registra o nível de otimização nem os hashes de todas as dependências de teste; isso não invalida as dez recusas, agora reexecutadas sob `-O` com evidência própria. Como melhoria de registro, acrescentar `sys.flags.optimize`, versão do Python e hashes das guardas/evidência a uma próxima versão desse relatório.

## Evidência própria, reprodução e hashes

Controle: `bis/c1_review/review_final_artifacts.py`. Resultado: `bis/c1_review/final_artifact_checks.json`. Os testes negativos modificam cópias em memória e não alteram os JSONs originais. A saída da revisão usa criação exclusiva, temporário, conferência explícita e renomeação; uma segunda execução no mesmo destino recusa sobrescrita.

Comando executado a partir de `C:\IALD\Central de Patentes`:

```powershell
& 'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -O 'Chatgpt/ORDEM_013_RINGDOWN/bis/c1_review/review_final_artifacts.py'
```

Para nova execução, usar uma cópia isolada com os insumos e a mesma estrutura relativa, preservando o resultado desta revisão. Axiomas: N/A — sem Lean. Nenhum `um.py`, PE, injeção, memória ou canônico foi executado/alterado.

| Arquivo | SHA256 lido por script |
|---|---|
| `refeito/c1_evidence_guards.py` | `f247c5c922ae57c17ff9461e21380ea0f0feae4f5c14514a8ef074b6be2004bb` |
| `refeito/measure_c1_013bis_v2.py` | `4106a3a4c60f62e8805c6f6fef9267d674d1d856c017cd032ccd6082aba8cff2` |
| `refeito/record_c1_013bis_v3.py` | `3b3dcf76914f7eef2bc77be9db2b49f29a70bab0ca6ee78a186750d842401455` |
| `refeito/test_c1_guards_013bis.py` | `135899003a5669966a971817443d62e056afc1789cad9ef9fd285ace5ef70100` |
| `bis/C1_NUMERICAL_CONTROLS_v2.json` | `a5c943922993fdef3d09a8b898feb4210586e360121c32da4857ddd644e3edec` |
| `bis/C1_GUARD_MUTATION_TESTS.json` | `3b53b8079ce9e763726441d8c028578d0cca220d60f95f6abdf2d49bc72f28b2` |
| `C1_LEITURAS_v3.json` | `e9fdd97d7429476f3551750b40b2b5d996abe2a8a341472157872687c4a821ea` |
| `C1_ADENDO_CORRECOES_013BIS_v2.md` | `86fa9d99b6386bf20e01d90aca15ac19987aa8ae9459cf6c502586d7e9bf0343` |
| `REAPROVEITAMENTO_C1_v2.md` | `5d0d76d0f68ae9620a3a1e35ce26ca91821f5f44315e1f1bcdd752d10d01ca41` |
| `bis/c1_review/review_final_artifacts.py` | `09a71bd20b6ce8f0ea356dbf584ba8df8b462e108139ef4006e4dece0e8e9a05` |
| `bis/c1_review/final_artifact_checks.json` | `090e0134e86e3dab52f627f68465ce8e8aee2a8a5a59fa361cdcc7c5628c2026` |
| `bis/c1_review/write_final_artifact_review.py` | `f52180cb9f1092c33b8bf3135f051a15491cb7a26dfb2a0b31869f7f819eb706` |

**Encaminhamento:** manter a aprovação dos valores atuais, da proveniência e das correções editoriais; dar B1 por corrigido; concluir B2 e a guarda de escrita com R1–R3 antes de anunciar que a rotina completa recusa evidência parcial ou inválida em modo otimizado. Nenhuma correção proposta foi aplicada aos artefatos pela auditoria.
