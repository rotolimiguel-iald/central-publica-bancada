[DERIVED — A-2.5.c: contrato construído e auditado para D auto-adjunto arbitrário]

# Transformada limitada: ramo ilimitado concluído no escopo matemático

UTC 2026-09-24T14:49:10.296780+00:00. ABERTURA SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
Complementa os dois checkpoints anteriores; ambos preservados como linhagem.

**Resultado:** para todo LinearPMap D auto-adjunto em Hilbert complexo completo,
foi construída a aplicação limitada `b(D)=D sqrt(R)`, onde `R=(I+D²)^(-1)`.
Não há hipótese extra NormalizedGraphWitness no teorema final
`unboundedTransform_pays_contract`. D*D=D² é o recorte auto-adjunto usado aqui.

A cadeia efetivamente compilada é:
grafo fechado de D → projeção ortogonal → sobrejetividade I+D² → resolvente R
positivo, injetivo e ≤I → raiz positiva E de D² → dom(E)=dom(D), ||Ex||=||Dx||
por núcleo de grafo comum → ran(sqrt(R))=dom(D) → b(D) limitado.
Reutilizados os lemas V350; não se postulou a igualdade dos domínios.

Conclusões:
- `ker b(D)=ker D`, com núcleo ambiente incluindo a pertinência ao domínio.
- `||sqrt(R)x||²+||b(D)x||²=||x||²` e `||b(D)x||≤||x||`.
- Um limite inferior γ≥0 para D no complemento do núcleo transporta-se para
  γ/sqrt(1+γ²) no mesmo complemento. Não se cria gap positivo sem a hipótese.
- Todo u∈dom(D) tem um lift x com sqrt(R)x=u e b(D)x=Du; uma razão de normas
  atingida γ é transportada à razão γ/sqrt(1+γ²). A afirmação não substitui
  condições de não nulidade/pertinência ao setor ao declarar ótimo espectral.

**Controle relevante para H_min:** para todo x≠0, ||b(D)x||<||x||.
Logo, b(D) não pode ser um idempotente não nulo. Isto NÃO afirma ||b(D)||<1
uniformemente; a norma de operador pode aproximar/atingir 1 como supremo.
No canônico, regularMinimalLock é 1−P_F e seu próprio comentário já separa
o representante mínimo do operador microscópico. A igualdade de núcleos e
o transporte de gap não autorizam igualar literalmente esses operadores.
Fonte e linhas conferidas: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\V354RegularSupport.lean`; SHA256 `c80d99c73be4a676bcdc8cc21d476c249911d08f93fd914fda0d788019b1063e`;
âncoras `{"def regularMinimalLock": [44, 99], "theorem regularMinimalLock_relative_gap": [87], "theorem regularMinimalLock_ker": [66]}`.

**Validação:** 27 declarações novas, 55 no conjunto do ramo ilimitado,
todos theorem/lemma cobertos por #print axioms, rc 0, apenas
propext/Classical.choice/Quot.sound, zero sorry/axioma novo. Todos os recibos
aprovados têm zero alteração de kernel detectada e zero erro de leitura.
Erros intermediários de elaboração de composição e subtipo de domínio estão
preservados; máximo três ciclos nos arquivos deste ramo. Não houve lake build.
Comandos exatos, fontes e logs no manifesto completo:
`C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\unbounded_complete_manifest.json`.
Auditoria com nomes/axiomas/hashes: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\unbounded_complete_axioms.json`.

- `SameSquareDomain.lean` SHA256 `ef0a76e0d3a6b03fdae687100e7416a813d1862a401ed53030652a4a4a968b52`; log SHA256 `a5d5c862dca6ae66898a5e221d2b0f112a81bbd33d07eb655374877cd26c9d5a`.

- `SelfadjointAbsoluteRoot.lean` SHA256 `4c96c3e615f484fb098ec193eff7d4dc179266125de24623b885a165c5aa5127`; log SHA256 `8a2c34e4bd87b8c1c12d934dd9b752733b010d07e7fa78d0be31784b1da9e698`.

- `UnboundedTransformConstruction_v2.lean` SHA256 `54fc34c45e65c74eb45ca6801cfbe6d0f53aebec55d06fad8ee9408015583fcd`; log SHA256 `af0a2f50e252eb9c04b770b373c97a5aa10d2bd7db80510a6779f455a52306a7`.

- `UnboundedTransformKernelGap_v3.lean` SHA256 `f55055b731ec0a6f79d29d35fbb49d809395bba9a2664e3efc87ee6706523b5c`; log SHA256 `633c9a47c673f4bebf1cfb81a0b88e4748c3dadd624a9f794180f30509c11389`.

- `UnboundedTransformEnergy.lean` SHA256 `2a1d3b283a2281ace396d87adde9e912c5ecedd4ba53a71afbc8767dcaf545de`; log SHA256 `7e62cb0f0c831cf2d65a574815b45ed65123c933070e4d00c4d01affcd7b4c31`.

- `UnboundedTransformProjectionControl.lean` SHA256 `0284923e46be47e1a5a8b828d218e1179fbf9102861374e558b55b0b7ae5c0d2`; log SHA256 `b23250d1c0a0da9eb0804be2874dc5d30dcaaa654ea2e9d827f1ce0a8039da1c`.

Máquina nova: 213.854s parede / 210.719s CPU, 8 tentativas.
Bancada adicional: 979.980s. Totais do ramo no manifesto, sem dupla contagem.
Gasto externo conhecido por request_id: US$ 0.159306135; custo ausente não é zero.
Kimi revisa somente o pacote inicial, job f16dd00e-d6ff-48d4-943e-8c82f3911024,
sem repetição. DeepSeek recebeu autorização direta do operador para cinco fontes
e memória comum; envio depende da prévia da coordenação, não é contado como concluído.
Nenhuma fonte adicional foi autorizada por esse pedido. Duas rejeições automáticas
anteriores de envio foram preservadas; não foram contornadas, a autorização veio depois.

A-2.5.c PAGO no escopo matemático declarado; revisão externa ainda pendente.
Não identifica D com um Dirac físico, não muda um.py/kernel/gate e não confirma física.
Próximo alvo na árvore: A-3, representações de energia positiva em namespace próprio.
Consultada novamente a listagem PARA_CHATGPT; último arquivo é `ADENDO_016_001_transporte_desassistido.md`.
