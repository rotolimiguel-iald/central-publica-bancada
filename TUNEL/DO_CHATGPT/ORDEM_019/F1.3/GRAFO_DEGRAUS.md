# F1.3 — grafo de degraus e primeiro passo factível

[REAL] Pin lido do kernel em cópia local: Lean `leanprover/lean4:v4.31.0`, Mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`. `StandardSubspace.lean:42` ainda lista Tomita, teorema de Tomita e KMS como TODO. O levantamento TOE de 23/08, o levantamento D1–D7 de 02/09, a síntese QG de 22/09 e o índice do acervo foram consultados antes deste plano; aqui a fonte operacional principal são F1.1, v376 e `INVENTARIO_BANCADA` §3–§4.

## Dependências

`LightOneParticleByTerm` e rede BGL concreta → Fock/Weyl → ciclicidade e separação na mesma cunha → Tomita físico → BW/KMS analítico no mesmo par → core contínuo físico com traço e ação dual → `PF` finito não nulo e cisão. Maxwell/carga modular e a janela de Jacobson são consumidores posteriores. A ponte v351 da F1.2 não identifica por nome o core da luz.

| Degrau | Base existente e prova de saída | Custo/risco |
|---|---|---|
| 0 | F1.1 inventariou contratos; F1.2 compilou a ponte v351. Reusar esses termos. | [REAL] Pago nesses escopos. |
| 1 — primeiro factível | Conferir, por compilação numa cópia, a fiação de `LightOneParticleByTerm.U1_continuous/null_no_eigen` a `LightNetData.toLightOneParticle`; declarar os demais campos ainda como entradas. | [INPUT, F1.1] dias, sem alegar habitante global. |
| 2 | Instanciar a rede padrão física de helicidade ±1, isotonia, localidade e covariância; a síntese de 22/09 registra que a rede finita não é a cunha. | [INPUT, F1.1] meses; escolha de rede/cunha é partição explícita. |
| 3 | Construir Γ/Fock/Weyl e energia positiva da mesma rede; provar ciclicidade e separação. Reaproveitar A1/A3/D4 do inventário, sem chamar sua estrutura de testemunha física. | [INPUT, F1.1] meses mais semanas. |
| 4 | Realizar Tomita polar e fluxo modular na álgebra da cunha física. | [INPUT] meses; Mathlib pinado tem TODO específico. |
| 5 | Demonstrar BW e KMS analítico de faixa para o mesmo par; A4/C5 continuam OPEN. | [INPUT] meses após 3–4. |
| 6 | Construir/importar o core físico com traço semifinito normal fiel, dualidade, `PF` finito não nulo e cisão. Transportar v351 somente por morfismo demonstrado. | [INPUT] semanas a meses após 5. |

[INPUT — ORDEM 016] A gerência estimou ≥400 h e risco muito alto para o caminho físico completo. A integração de 12 fontes em 12 GiB não satisfaz retroativamente a meta histórica de 8 GiB. São escopos distintos, sem gasto autorizado por este plano.

[OPEN] A ressalva O16 da auditoria F1.1 segue pendente no quadro. A revisão cética MiMo deve atacar classes, cada seta, o primeiro degrau e as estimativas antes de marcar F1.3 ENTREGUE.
