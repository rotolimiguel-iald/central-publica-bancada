"""Write only the authorized final review; refuse an existing output."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output=ROOT/'bis/C1_FINAL_ARTIFACT_REVIEW.md'
    if output.exists():raise FileExistsError(output)
    evidence=json.loads((HERE/'final_artifact_checks.json').read_bytes())
    changed=[p for p,h in evidence['input_hashes'].items() if sha(ROOT/p)!=h]
    if changed:raise RuntimeError('Audited inputs changed: '+repr(changed))
    names=['refeito/c1_evidence_guards.py','refeito/measure_c1_013bis_v2.py',
           'refeito/record_c1_013bis_v3.py','refeito/test_c1_guards_013bis.py',
           'bis/C1_NUMERICAL_CONTROLS_v2.json','bis/C1_GUARD_MUTATION_TESTS.json',
           'C1_LEITURAS_v3.json','C1_ADENDO_CORRECOES_013BIS_v2.md',
           'REAPROVEITAMENTO_C1_v2.md','bis/c1_review/review_final_artifacts.py',
           'bis/c1_review/final_artifact_checks.json',
           'bis/c1_review/write_final_artifact_review.py']
    table='\n'.join(f'| `{p}` | `{sha(ROOT/p)}` |' for p in names)
    report=f'''[REAL — revisão adversarial independente C1/F1; artefatos numéricos atuais aprovados no escopo; B1 corrigido, B2 parcialmente corrigido; nenhuma alteração de gate]

# Revisão final dos artefatos C1 — segunda rodada

Data UTC: {datetime.now(timezone.utc).isoformat()}. Raiz dos caminhos relativos: `{ROOT}`.

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

**[REAL — números]** `C1_NUMERICAL_CONTROLS_v2.json` difere do controle anterior somente em `utc` e `dependencies`. Todos os valores numéricos, 264 verificações CSV, sete spins, perfis, dimensões e cota P2 são iguais aos já auditados. As dez linhas de `C1_LEITURAS_v3.json` são iguais às da v2 aprovada numericamente. Logo, permanece aplicável a conferência independente anterior: erro relativo máximo **{evidence['previous_independent_csv_max_relative_error']:.6g}**, 99 linhas pequenas não nulas + 33 R-GLOBAL = 132, QNM e perfis conferidos. Não refiz contas caras nem reabri PE para comparar valores idênticos.

O arquivo original dos dez testes não registra o nível de otimização nem os hashes de todas as dependências de teste; isso não invalida as dez recusas, agora reexecutadas sob `-O` com evidência própria. Como melhoria de registro, acrescentar `sys.flags.optimize`, versão do Python e hashes das guardas/evidência a uma próxima versão desse relatório.

## Evidência própria, reprodução e hashes

Controle: `bis/c1_review/review_final_artifacts.py`. Resultado: `bis/c1_review/final_artifact_checks.json`. Os testes negativos modificam cópias em memória e não alteram os JSONs originais. A saída da revisão usa criação exclusiva, temporário, conferência explícita e renomeação; uma segunda execução no mesmo destino recusa sobrescrita.

Comando executado a partir de `C:\\IALD\\Central de Patentes`:

```powershell
& 'C:\\Users\\rotol\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' -B -O 'Chatgpt/ORDEM_013_RINGDOWN/bis/c1_review/review_final_artifacts.py'
```

Para nova execução, usar uma cópia isolada com os insumos e a mesma estrutura relativa, preservando o resultado desta revisão. Axiomas: N/A — sem Lean. Nenhum `um.py`, PE, injeção, memória ou canônico foi executado/alterado.

| Arquivo | SHA256 lido por script |
|---|---|
{table}

**Encaminhamento:** manter a aprovação dos valores atuais, da proveniência e das correções editoriais; dar B1 por corrigido; concluir B2 e a guarda de escrita com R1–R3 antes de anunciar que a rotina completa recusa evidência parcial ou inválida em modo otimizado. Nenhuma correção proposta foi aplicada aos artefatos pela auditoria.
'''
    raw=report.encode('utf-8');tmp=output.with_name(output.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise RuntimeError('Review byte mismatch')
    if output.exists():raise FileExistsError(output)
    tmp.rename(output)
    print(json.dumps({'path':str(output),'sha256':sha(output),'bytes':len(raw),'audited_inputs_unchanged':True},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
