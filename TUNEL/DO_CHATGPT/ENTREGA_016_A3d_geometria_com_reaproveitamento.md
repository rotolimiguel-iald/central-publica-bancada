[REAL — compilação isolada e auditoria; escopo geométrico]

# ORDEM 016 — A-3.d: composição com a normalização já existente

UTC 2026-09-24T15:23:23.288797+00:00. ABERTURA sha256 `216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a`.

**PAGO no escopo pedido dos campos geométricos de H2 dado o boost.** Para todo
`N : KillingNormalization` admissível, a composição entrega κ>0, norma de Killing
unitária no ponto N, frame regional suave com determinante invertível, arrasto
`E(boost(s)x)=boostMat(s)E(x)` e coluna fiducial positivamente proporcional ao Killing.
Não escolhe N, rede W, realização R, massa ou partição física.

O frame utilizado é `E(x)=[[x¹,x⁰,0,0],[x⁰,x¹,0,0],[0,0,1,0],[0,0,0,1]]`:
`det E=(x¹)²−(x⁰)²>0` na cunha. A taxa é `κ=1/sqrt((N¹)²−(N⁰)²)`.

**Reaproveitamento explícito:** `refRadius`, `refRadius_pos` e
`observer_unit_of_index` foram extraídos de ContratoQG_v31_Teoremas sem mudar seus
corpos, apenas com import/namespace de bancada para compilação isolada.
O lema de composição `geometric_fields_reused` consome esses dois resultados e os
fornecedores de WedgeDraggedFrame_v6. Não se anuncia nova derivação da normalização.
As variantes WedgeKillingNormalization até v4 ficam preservadas como rascunhos não
compilados e não são necessárias para estes campos. A derivada do boost já existe
em ApproximateBoostFlow; A2/BoostRepresentationBridges conserva a ligação de matriz
por permutação dos eixos e inversão de rapidez. Nenhuma nova derivada foi alegada aqui.

**Validação:** rc 0, 3 declarações auditadas na composição/extrato (duas reutilizadas,
uma composição), acrescidas às 7 do frame: 10 declarações verificadas no trio permitido,
zero sorry/axiom novo. Fonte/log/recibos e hashes completos em
`A3/geometric_reuse_manifest.json`. Nova rodada `existing_calibration_01` em
`lake env lean -j1 -M8192`, dependências mínimas do contrato; original do kernel intacto.
Os 6 ciclos anteriores do determinante permanecem preservados; extração/composição
passou no primeiro ciclo. Máquina total desta frente: 0.067885 h parede,
0.067218 h CPU. Novas chamadas externas apenas registradas, custo ainda não medido.

**Move / não move a fronteira da QG:** não move o gate. Entrega a parte geométrica
do tipo; não fornece por si W, R, KMS, BW unitário, energia positiva ou segunda
quantização. Kimi e MiMo verificam o reaproveitamento mais amplo do acervo em unidades
separadas; suas respostas não substituem estes recibos Lean.

Próximo ramo prescrito: sub-alvo 1, fidelidade das translações nas três órbitas,
lado a lado; depois sub-alvo 4. A crítica externa pode corrigir a composição,
mas não exige refazer a seleção de horizonte já registrada.
