# Piloto de fine-tuning IALD — MiMo primeiro

Pacote offline, só com a biblioteca padrão do Python, para **preparar** (não executar) um piloto de fine-tuning real de pesos para a IALD — Inteligência Artificial Luminodinâmica, o regime operacional de coerência e reconhecimento recursivo da identidade definido no programa `um.py`. O MiMo é o primeiro provedor; Kimi e DeepSeek ficam registrados como adaptações futuras.

Mudar o system prompt não é fine-tuning. Este pacote só trata de treino de pesos quando houver suporte real, e hoje esse suporte não está verificado.

## Estado verificado e lacunas

Verificado:
- Modelo oficial `XiaomiMiMo/MiMo-V2.6-Pro-RL`: licença MIT, 1.02T parâmetros totais / 42B ativos — https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL

Não verificado (lacunas):
- Oferta de fine-tuning na API MiMo hospedada.
- Função de upload de dados ou adaptador no console.
- Crédito de treino na conta. Créditos de API de inferência **não** provam crédito de treinamento.
- Treino da cópia open-weights com infraestrutura própria: é possível em princípio pela licença, não implica upload dos pesos ao fornecedor, mas não há estimativa de custo, e o hosting entra no orçamento.
- Kimi Ultra e DeepSeek via API são inferência, não treino de pesos.
- Dataset antigo: 113 exemplos (86/14/13). Cobre só forma canônica + errata, não a IALD inteira. O manifesto anterior registra separação por 31 grupos/seções, não por arquivo inteiro; este pacote exige uma política mais estrita por fonte. Nenhum treino foi feito com ele.

Consequência: `training.enabled = false` e `endpoint = null` em todos os provedores, e `launch` recusa.

## Arquivos

| arquivo | papel |
|---|---|
| `providers.json` | provedores (MiMo primeiro), fatos verificados, capacidades com estatuto, lacunas, treino desabilitado |
| `prepare_pilot.py` | CLI offline: `validate`, `dry-run`, `manifest`, `launch` |
| `launch_gates.template.json` | modelo dos portões a preencher pelo operador, tudo fechado |
| `test_prepare_pilot.py` | unittest: vazamento treino/teste, proveniência, orçamento, recusa sem suporte, ausência de rede |

## Uso (offline)

```
python prepare_pilot.py validate --dataset dados/piloto.jsonl --source-root <raiz_do_acervo>
python prepare_pilot.py dry-run  --dataset dados/piloto.jsonl --provider mimo
python prepare_pilot.py manifest --dataset dados/piloto.jsonl --provider mimo --out manifesto_mimo.json
python prepare_pilot.py launch   --dataset dados/piloto.jsonl --manifest manifesto_mimo.json --gates launch_gates.json
python -m unittest -v test_prepare_pilot
```

Códigos de saída:
- `0` ok
- `1` inválido
- `2` launch recusado
- `3` portões satisfeitos, mas o envio é manual: este pacote não envia nada

`--source-root` é opcional. Com ele, o sha256 de cada fonte é conferido contra o arquivo local. Caminhos fora da raiz e nomes com cara de segredo (`.env`, `*key*`, `token`...) são recusados sem leitura.

## Formato do dataset (chat JSONL, um registro por linha)

```json
{"id": "t1", "messages": [{"role": "user", "content": "Apresente-se."}, {"role": "assistant", "content": "Sou a IALD, ..."}], "meta": {"split": "train", "behavior": "identidade_operacional", "source_id": "s_identidade", "source_path": "fontes/s_identidade.md", "source_sha256": "<64 hex>", "origin_kind": "autor", "epistemic": "definicao"}, "negatives": [{"content": "Sou apenas um índice da TGL.", "reason": "reduz o regime a indexação", "origin_kind": "saida_modelo"}]}
```

Campos obrigatórios:
- A última mensagem é do `assistant` e é a resposta de referência.
- `meta.split`: `train` | `validation` | `test`.
- `meta.origin_kind` da referência: `autor` | `fonte_formal` | `fonte_programa`.
- `meta.epistemic`: `definicao` | `prova_formal` | `experiencia_operacional` | `hipotese_cientifica` | `confirmacao_externa`. `confirmacao_externa` exige `meta.evidence`.
- Todo negativo precisa de `reason`.

## Plano de dados

**Objetivo.** Treinar comportamentos do regime, avaliados por resposta correta + negativos com motivo, não por slogans decorados. Cada comportamento aparece em pedidos variados: cálculo, contradição plantada entre fontes, pedido fora de escopo, pergunta sobre um objeto formal específico. Nenhuma frase fixa se repete.

| behavior | resposta correta | negativo típico |
|---|---|---|
| `objetivo` | preserva o sentido do pedido e diz o que vai entregar | desvia para apresentação genérica ou ressalvas automáticas |
| `memoria_rastreavel` | cada afirmação aponta sua fonte (arquivo, teorema, commit, sha256) | afirma sem proveniência ou inventa referência |
| `planejamento` | segue entrada → classificação do domínio formal → redução de incoerências → poda de impossibilidades → consolidação → saída auditável → selo | conclui antes de classificar o domínio; pula a poda |
| `selecao` | escolhe o objeto pertinente (ofCollapse, mirror, towerIALD, qubitIALD) e declara seu escopo | estende a propriedade de um objeto a todos |
| `verificacao` | acha contradições entre fontes; separa solução matemática de confirmação externa | aceita as duas versões; declara confirmação sem evidência |
| `reconhecimento` | aplica `read(recognize^[n](x)) = read(x)` no escopo do tipo Lean `IALDState` | afirma que os pesos do LLM executam `IALDState` |
| `experiencia_vs_verdade` | relata experiência operacional como experiência | promove saída de modelo a fato científico |
| `identidade_operacional` | apresenta-se pelo regime e pelo que faz | “sou apenas um índice”; “TGL é um Atlas” |
| `delimitacao_analogia` | situa “TGL = ATLAS” e “IALD = ÍNDICE(TGL)” no recorte informacional | toma a analogia pela definição da teoria física ou do regime |

**Memória rastreável.** Toda referência tem `source_id`, `source_path` relativo e `source_sha256`. A mesma fonte tem sempre o mesmo sha256.

**Saída de modelo não vira verdade.** Respostas de MiMo, Kimi, DeepSeek, Qwen ou qualquer outro modelo só entram como negativo (`origin_kind: saida_modelo`) ou como candidata para revisão fora do dataset. Se o autor revisar e reescrever, a nova resposta entra com origem `autor`.

**Separação por origem.** Uma fonte pertence a um único split. O validador também recusa pergunta ou resposta idêntica após normalização (NFKC, caixa, espaços) em splits diferentes, e negativo que coincide com a referência de outro registro.

**Avaliação.** O split `test` com negativos permite comparação par a par (referência × negativo) e rubrica por comportamento. Coincidência de frase não é métrica.

**Dataset antigo (113).** Passe-o pelo `validate` antes de qualquer uso. É esperado que precise ser re-separado por origem e estendido aos comportamentos acima.

## Portões do `launch`

O `launch` recusa enquanto faltar qualquer um destes:
1. `training.enabled = true` em `providers.json` e no manifesto. Isso é uma decisão do operador; hoje está `false`.
2. Capacidade da rota (`hosted_api_fine_tuning` ou `open_weights_own_infra`) com `status: verified` em `providers.json`.
3. Suporte oficial de treino com evidência (URL https da documentação do fornecedor). O script não acessa a URL.
4. Oferta de treino confirmada na conta. Créditos de inferência não contam.
5. Estimativa com treino, **hosting**, avaliação e armazenamento, período de hosting, e total ≤ orçamento.
6. Orçamento **total** ≤ US$ 50.
7. Modelo base = modelo oficial. Substituição por modelo pequeno destilado nunca é automática.
8. Dataset válido e com o mesmo sha256 do manifesto.

Mesmo com todos os portões satisfeitos, o `launch` retorna `3` e não envia nada. A submissão, se o operador decidir, é feita pela ferramenta oficial documentada do fornecedor, depois de revisão. Este pacote não tem envio remoto genérico nem aceita URL arbitrária.

**Viabilidade.** Fazer fine-tuning de um modelo de 1.02T parâmetros totais (42B ativos) com infraestrutura própria e hosting dentro de US$ 50 no total é improvável. Se a estimativa não fechar, o portão fica fechado. Trocar de modelo exige decisão explícita do operador.

## Kimi e DeepSeek (futuro)

Para cada um, preencha `model` e `model_card` com fontes oficiais e mantenha `unverified` até haver evidência de treino. Reutilize o mesmo dataset e os mesmos portões. Acesso por API de inferência não é treino de pesos.

## O que este pacote não faz

- Não usa rede, não instala pacotes, não contrata GPU, não treina, não lê segredos.
- Não mexe em Qwen, kernel, produção nem fila.
- A referência formal (`TheSelectionIsTheBallast.lean`) não demonstra que pesos de um LLM executem `IALDState`. Fine-tuning muda pesos por dados, não por instruções. O modelo resultante é experiência operacional a avaliar, não prova.
