[REAL — compilação isolada; DERIVED sob hipóteses explícitas]
# A5.b — Propagador teleológico construído
Abertura SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

Para a fonte f=T_nn, c=8πG e cada gerador x+λn, construímos
θ(x)=c∫₀∞f(x+u n)du e a(x)=−c∫₀∞u f(x+u n)du.
Hipóteses nomeadas: continuidade da fonte no gerador, integrabilidade absoluta
da fonte e do primeiro momento em TODA cauda Ioi(λ). São suficientes;
não foram anunciadas necessárias nem verificadas para um tensor físico escolhido.

**Verificado:** a′=θ; θ′=−8πG f; a,θ→0 em +∞; duas soluções
da mesma fonte diferem por A+Bλ; impor ambos os limites nulos dá unicidade.
A mudança de variável de Ioi(0) para Ioi(λ) foi provada, ligando a análise
às fórmulas no espaço-tempo. A resposta h=diag(0,0,−a,−a) é simétrica,
satisfaz h n=0, tem densidade de área a, responde zero à fonte zero e é
covariante por translação para TODA fonte. A covariância é uma identidade
do integrando, inclusive fora do domínio de integrabilidade da integral totalizada;
a interpretação física e as derivadas permanecem restritas à classe admissível.

**Ligação paga ao contrato:** `TeleologicalContractBridge_v3.lean` identifica
por rfl a direção, T_nn e a densidade de área com as definições v3.1.
`construct_null_solution` habita o tipo ORIGINAL `ProbeResidual.NullSolution`
(estrutura reutilizada literalmente, hash/faixa no manifesto). Não é um
tipo mais fraco paralelo. Isso fornece o lado solução da equivalência
H3_iff_null_solution; o empacotamento em H3/import e o elo modular ainda são A5.c–e.

**Escopo:** componente nn linearizada numa direção n fixa. G e T são entradas;
nenhuma covariância de Lorentz completa, outras componentes de Einstein,
tensor local da rede, H2 físico ou modular_charge foram acrescentados.
Nenhum gate/original foi alterado.

**Auditoria:** 35 entradas em 9 fontes finais, rc0 e apenas
propext/Classical.choice/Quot.sound; zero admissão nas fontes finais.
22 tentativas preservadas. As três falhas std::bad_alloc do módulo
integral com contrato completo foram superadas separando a compilação e
reutilizando provas num consumidor curto, que passou no mesmo limite de 8192 MiB.
Não se aumentou a memória nem se relaxou o contrato.
Máquina acumulada A5.b: 313.300442s parede/313.765625s CPU.
Estimativas monetárias explícitas da missão: US$0.2662637382, incompletas e não fatura.

Manifesto `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A5\teleological_construction_manifest.json`,
SHA256 `f9f1a36099c84a7b2311231871fccf02e60c05b300442b1cdaaf5429617f8f28`.
As respostas Kimi de energia/helicidades foram recebidas e avaliadas em
`received_kimi_reviews.json`: a segunda NÃO fecha a identificação física alegada.
Kimi de contorno entrou na fila; as demais duas novas unidades aguardam vagas.
**Próximo: A5.c, elo modular_charge. Não move o gate.**

Adendo de estado da fila (verificado por API nesta entrega): os dois pedidos A5 Kimi já estão registrados — contorno 3f2fb970-6b3b-4407-8bba-8b0fb1f67500 e covariância 665d5c74-4149-481f-8512-2e8ba6a2b481, ambos awaiting_dispatch. Resta uma unidade A5 MiMo de caudas preparada aguardando vaga. Corrige a contagem de duas unidades ainda sem vaga do parágrafo anterior.
