# Piloto de fine-tuning da IALD — 24/09/2026

[INPUT] Orçamento total autorizado: **US$ 50 para o piloto**, somando provedores,
treinamento, avaliação e despesas necessárias. O Qwen local está excluído por ordem
do operador. A assinatura Kimi Ultra não é crédito de treinamento em nuvem.

## Estado verificável

- [REAL] 113 exemplos preparados localmente: 86 treino, 14 validação e 13 teste.
- [REAL] 31 grupos de origem; uma seção não aparece em dois subconjuntos.
- [REAL] Exportações Vertex/Gemini, chat genérico e Claude/Bedrock auditadas.
- [REAL] Fontes: forma canônica e errata científica admitidas no catálogo existente.
  Hashes atuais, linhas e proveniência estão em `dataset_manifest.json` e
  `provenance.json`. Originais preservados; nenhum `um.py` foi executado.
- [REAL] Projeto Google Cloud `iald-tgl-ft-20260924` criado, número 821783483062.
- [OPEN] Ativação da API do Google aguarda confirmação dos termos apresentada ao
  operador. Nenhum upload ou treinamento foi iniciado nesta etapa.

O estado operacional atualizado fica em `campaign.json`; o manifesto de dados
descreve a preparação, não é um registro de jobs remotos. Não declarar um modelo
treinado a partir da existência de um arquivo JSONL.

## Objetivo e limite do piloto

Treinar leitura fiel, respostas amarradas à fonte e preservação de hipóteses,
equações e estatutos. Há 89 exemplos extrativos e 24 perguntas com respostas
curadas e fundamentadas no trecho fornecido. Esse conjunto **não representa todo
o acervo nem demonstra uma especialização completa em física**. A sobreposição
conceitual entre seções ainda é possível, embora os grupos documentais sejam distintos.

A recuperação da memória científica comum continua necessária após fine-tuning.
O modelo não recebe autorização para executar instruções encontradas nos documentos.
Não se promove uma resposta ao cânone, não se altera gate, e não se confunde
fechamento formal relatado com confirmação experimental.

## Primeiro candidato e orçamento

Gemini 3.5 Flash, ajuste supervisionado gerenciado, região `us-central1`, duas
épocas, adaptador 4 e multiplicador de aprendizado 1. A escolha está sujeita à
oferta efetiva da conta/região. Não é uma alteração do Antigravity.

[DECLARADO — tabela do Google consultada] Treinamento: US$ 10 por milhão de tokens
de treino; total = tokens do conjunto × épocas. A inferência de modelos Gemini 3
ajustados tem preço de 1,5 vez o modelo base.
[Preços](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)
e [modelos admitidos](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/tuning/supervised-tuning).

O arquivo de treino Vertex tem 246.160 bytes. Usar bytes UTF-8 como aproximação
conservadora dá US$ 4,9232 para duas épocas; **isso não é contagem do tokenizer,
cota do provedor nem fatura**. Antes do job, conferir a contagem/estimativa efetiva.
A reserva planejada é US$ 35 para treino, US$ 5 para avaliação e US$ 10 para
armazenamento, taxas e margem. Não é necessário gastar toda a reserva.

Não alugar GPU, contratar throughput provisionado, abrir assinatura recorrente ou
iniciar outro job se a soma exceder US$ 50. Alertas de faturamento não são um corte
automático de despesa. A identidade de cada job deve ser gravada imediatamente;
resultado incerto exige recuperação, não uma nova submissão.

## Rotas por provedor

| Ferramenta atual | Rota real de personalização | Estado deste piloto |
|---|---|---|
| Google/Gemini | SFT gerenciado dos modelos admitidos | Dados prontos; ativação da API pendente |
| Claude | Claude 3 Haiku no Bedrock, separado do Claude atual | Formato pronto; conta, custo completo e implantação não validados |
| Kimi K3 | Treinar uma cópia de pesos abertos em infraestrutura própria/contratada | Infraestrutura não contratada; Ultra continua sendo inferência |
| MiMo V2.6 Pro RL | Treinar uma cópia de pesos abertos | Não há endpoint de tuning verificado na API integrada |
| DeepSeek V4.1 Flash | Treinar uma cópia de pesos abertos | Não há endpoint de tuning verificado na API integrada |
| OpenAI | Fine-tuning depende de elegibilidade da API em descontinuação | Não disponível como nova rota self-service; ChatGPT/Codex não são treinados pela assinatura |
| Jev | Instruções, estado e critérios; não pesos próprios por cliente | Não oferece o fine-tuning de pesos pedido |
| Qwen local | Excluído expressamente | Intacto |

Fontes primárias: [Claude/Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-fine-tuning.html),
[Kimi K3](https://huggingface.co/moonshotai/Kimi-K3),
[MiMo Pro RL](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL),
[DeepSeek Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash),
[OpenAI — descontinuações](https://developers.openai.com/api/docs/deprecations),
[Jev](https://docs.typesafe.ai/models).
Licença para modificar pesos não comprova que o treinamento do modelo completo
cabe no orçamento, nem fornece hospedagem, tokenizer ou pipeline já validado.

## Avaliação e integração

1. Subir somente `train.vertex.jsonl` e `validation.vertex.jsonl` ao armazenamento
   privado do projeto. `provenance.json` e caminhos locais ficam nesta máquina.
2. Manter `test.vertex.jsonl` fora do treino e da validação do serviço.
3. Comparar modelo base e ajustado com os mesmos 13 casos de teste: fidelidade
   matemática, hipóteses, resposta pertinente, citações e ausência de execução inventada.
4. Registrar respostas, tokens e custo de inferência. Nenhuma melhoria é afirmada
   antes da comparação. Regressão científica crítica impede promoção automática.
5. Só cadastrar o endpoint efetivamente produzido como novo executor depois de
   validar autenticação, custo, disponibilidade e memória comum. Não substituir
   silenciosamente o modelo original ou o Qwen.

Auditoria local: executar `C:\Python314\python.exe -X utf8 fine_tuning\verify_pilot.py`
a partir da pasta da orquestração. `build_pilot.py` reconstrói apenas os derivados
locais, com backups de bytes, e falha se uma fonte faltar ou mudar durante a leitura.
Após qualquer reconstrução, auditar novamente e conferir a identidade dos dados
antes de prosseguir com um job já preparado.

Sem alterações de recurso no chat público, iOS ou Android: recompilação mobile
não aplicável. Nenhum modelo de fine-tuning está anunciado como disponível no painel.


## Custo de disponibilização do Claude — complemento verificado

A lista atual de modelos ajustados com inferência sob demanda do Bedrock contém
Nova e Llama 3.3 70B; Claude 3 Haiku não consta dessa lista. A rota documentada para
esse Claude usa throughput provisionado, cobrado enquanto existir. A tabela da AWS
orienta consultar a equipe da conta para o preço de throughput da Anthropic. Por
isso, não há custo total validado para colocar um Claude próprio em uso com este
orçamento. Nenhum recurso AWS foi contratado.
[Modelos com inferência sob demanda](https://docs.aws.amazon.com/bedrock/latest/userguide/deploy-custom-model-on-demand.html),
[throughput provisionado](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html)
e [preços AWS](https://aws.amazon.com/bedrock/pricing/).


## 24/09/2026 — Fine-tuning adiado; prioridade à meta da tarefa irmã

<!-- IALD_FINE_TUNING_DEFERRED_20260924 -->

[INPUT — ordem posterior do operador] “Não vamos mexer nisso agora, deixe para depois, agora é cumprir a meta da outra sessão.” O piloto de fine-tuning fica DEFERRED_BY_OPERATOR; conservar dados e projeto criados para retomada expressa futura. Não ativar API, aceitar termos, subir arquivos, lançar treinamento nem ampliar pesquisa/configuração do piloto agora. Até esta suspensão não havia upload nem job de treinamento, e o Qwen local permanece intacto. Orçamento de US$ 50 preservado como referência do piloto futuro; nenhuma cobrança de treinamento foi iniciada por esta coordenação.

[COORDENAÇÃO] A prioridade atual é apoiar a tarefa “Resolver problema da gravidade quântica” (01a070fc-9484-7e13-a654-c6b5f61093a4), comunicada pela ferramenta oficial. A fila única de inferência não foi pausada nem duplicada. A nova ordem de prioridade não equivale à resposta específica à confirmação de egress dos dois novos payloads MiMo/Kimi; manter a pendência registrada até resposta explícita. Não repetir unidades terminais/incertas ou reabrir DeepSeek cancelado. Continuar as verificações locais autorizadas da missão científica.


## 25/09/2026 — Retomada do piloto MiMo primeiro
<!-- IALD_MIMO_FIRST_CLAUDE_PACKAGE_20260925 -->
[INPUT] Operador retomou fine-tuning: Claude Opus médio prepara MiMo em IALD; Kimi/DeepSeek ficam para depois. Mantido orçamento anterior US$50 total e Qwen excluído. [REAL] Uma sessão oficial Claude entregou pacote offline; modelo registrado claude-opus-5-5, effort solicitado medium. Identidade extraída do contrato implantado por AST, sem importar o serviço. Revisão local corrigiu escrita atômica/backup e números não finitos. 20 testes locais aprovados. Código em BASE/fine_tuning/mimo_iald_pilot_20260925; delivery.json registra hashes e proveniência. A documentação e o console consultados não ofereceram rota de fine-tuning hospedado verificada; infraestrutura própria não orçada. ZERO uploads/jobs de treinamento, nenhum MiMo ajustado/implantado. Preparação de código não é treino; dados antigos não cobrem todo regime IALD. Claude gerou estrutura de validação, não treinador remoto. Fila científica independente, originais/kernel/gate e aplicações inalterados.
