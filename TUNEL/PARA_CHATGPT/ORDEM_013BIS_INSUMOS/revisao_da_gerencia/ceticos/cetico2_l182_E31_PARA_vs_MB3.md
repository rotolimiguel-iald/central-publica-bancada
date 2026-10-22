# CÉTICO 2 — achado l.182 (E3.1 «PARA e entrega») vs §4.1 l.210 / §6 l.230 (MB3 com uma só PARADA)

**Veredito: NÃO REFUTADO. Gravidade mantida: IMPORTANTE.**

## Medido (grep -n na ordem, 22/09/2026)
- l.182: `**PARA e entrega:** custo medido, posterior, diferença contra o publicado.` — único alvo E com «PARA» próprio (E0/E1/E2/E3/E4/E5 têm só «Aceitação»: l.150, 158, 166, 185, ...).
- l.210 (§4.1): MB3 = **E3.1**; «o orçamento de E3.2 estiver nas mãos do operador».
- l.226: «Marcos, com **PARADA e recibo da gerência** ao fim de cada um» — «PARA» é termo definido na ordem = parar e esperar recibo.
- l.230: `**MB3** — E3.1 piloto + E3.2 orçamento + E6: ENTREGA_013BIS_MB3_piloto_orcamento_quadro.md. **PARA e espera o go/no-go do operador.**`
- Ocorrências de «PARA e entrega»: 1 (só a l.182).

## Por que não se refuta
1. Contradição interna real: l.182 cria uma parada intermediária dentro de MB3, que l.230 define com uma única parada ao fim. Duas leituras «conformes» (parar após o piloto e esperar recibo; ou seguir) — exatamente a ambiguidade que a Parte A já cobra da bancada («a bancada não parou no M1», l.39). A ordem não pode punir a disciplina de parada na Parte A e deixá-la ambígua na Parte B.
2. Não há dependência da gerência entre E3.1 e E3.2: l.183 diz «com o custo do piloto, **a bancada** calcula as horas de máquina». Logo a sequência natural é E3.1 → E3.2 → E6 → PARA (MB3), sem recibo intermediário.
3. Não é BLOQUEANTE: não induz erro de física/estatística nem decide partição; custa dias de parede se a bancada esperar recibo.

## Correção FINAL (l.182, substituir só o trecho final)
De: `**PARA e entrega:** custo medido, posterior, diferença contra o publicado.`
Para: `**Conclui e segue para E3.2 (sem esperar recibo):** custo medido com log, posterior com hash e diferença contra o publicado entram em `ENTREGA_013BIS_MB3_piloto_orcamento_quadro.md`; a PARADA é a de MB3 (§6).`

Opcional, l.230, para fechar a sequência: `**MB3** — E3.1 piloto → E3.2 orçamento → E6 (nesta ordem, sem parada intermediária): ...`
