[DERIVED — 11 novas declarações Lean auditadas; resolvente geral construído]

# A-2.5.c — adendo: I+D² para o operador prescrito

UTC 2026-09-24T14:32:50.317165+00:00. ABERTURA SHA256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.
Complementa ENTREGA_016_MEDIDA_A2_5c_grafo_resolvente.md, preservada.

Agora o resolvente foi construído para TODO D auto-adjunto em LinearPMap,
em Hilbert complexo completo; não é mais dado de entrada de uma família escolhida.

1. O grafo complexo fechado de D é colocado em WithLp 2 (H×H).
   A projeção ortogonal de (z,0) produz x∈dom(D) com
   ⟨z−x,u⟩=⟨Dx,Du⟩ para todo u∈dom(D).
2. Pela definição do adjunto e D*=D, Dx∈dom(D) e D²x=z−x.
   Portanto I+D² é sobrejetivo, conservando o domínio sucessivo real da operação.
3. Positividade e simetria de D² são derivadas da energia e do emparelhamento.
   A construção existente partialPositiveResolvent produz R=(I+D²)^(-1).
4. Provados 0≤R≤I, injetividade, a equação do inverso e
   resolventGraphOperator(R)=D² com igualdade de grafos/domínios.

Tudo acima foi compilado, incluindo a existência. Não se postulou a sobrejetividade
nem a positividade para o D auto-adjunto recebido. A densidade e o fechamento
vieram das propriedades de IsSelfAdjoint da Mathlib efetivamente consultada.

## Passagem ainda aberta e próxima construção

R geral está pago. Falta concluir a testemunha normalizada do MESMO D:
A=sqrt(R), ran(A)=dom(D), B=D A limitado e auto-adjunto, AB=BA, A²+B²=I.
O condicional de núcleo/gap já auditado então se aplica.
Rota localizada nos arquivos existentes: V350ResolventSquareRoot constrói |D|
com quadrado D²; V350PartialSquareGraphCore e V350GraphCoreNormTransfer permitem
comparar os domínios de |D| e D via igualdade de normas no domínio de D².
As etapas posteriores não são anunciadas como concluídas neste adendo.

## Custódia e custos

11 theorem/lemma com #print axioms no trio permitido; rc 0 nos dois arquivos;
zero sorry/axioma novo, zero alteração de kernel detectada, zero erro de custódia.
A tentativa inicial falhou apenas ao normalizar projeções de par na identidade
vetorial final; está preservada. Warnings de variáveis sem uso não foram suprimidos.
Comandos integrais nos recibos (lake env lean -j1 -M8192, runner isolado).
Manifesto: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\general_resolvent_manifest.json`.
Auditoria: `C:\IALD\Central de Patentes\Chatgpt\ORDEM_016_QG\A2\general_resolvent_axioms.json`.

- `ClosedLinearGraphResolvent_v2.lean` SHA256 `ccd62fee28c20d46b1f62f793c5ef6b97758c454c94a704eb66d0c3ceeacd6e8`; log `linear_graph_resolvent_02.log` SHA256 `f2525e8b4a729bf50a5d766ad4da5eee07c3cc78325ac13a98124686e32bf79f`.

- `SelfadjointSquareResolvent.lean` SHA256 `1b51c81c72458cf531670defdab31da75c8a9c971353a772a76c55a68a7d8492`; log `selfadjoint_resolvent_01.log` SHA256 `eb557138b708c35541f97ee68dc1cff3e376d93b8b63845684954ec1588b23b5`.

Máquina adicional: 71.673s parede, 70.859s CPU, 3 tentativas.
Bancada desde o checkpoint anterior: 443.670s. Custo externo conhecido por
request_id: US$ 0.159306135; valores ausentes não são tratados como zero.
A sessão Orquestrar IAs na Central IALD registrou separadamente a revisão Kimi
dos quatro arquivos ANTERIORES: request c101844e-52f8-4aac-8dfb-881771481a24,
job f16dd00e-d6ff-48d4-943e-8c82f3911024; pendente, não duplicada, sem incluir
os dois arquivos deste adendo. A bancada não escreveu no ledger nessa janela.

A-2.5.c permanece EM CURSO. Nenhum original, um.py, kernel ou gate alterado.
Não houve seleção de Dirac físico/H_min nem afirmação de confirmação experimental.
