# CÉTICO 2 — achado do revisor estatistica_poder sobre a ORDEM 013-bis l.131 (§4.0 e) e l.216 (§5)

**Veredito: NÃO refutado.** O número existe, foi refeito por script e a régua da própria ordem (l.11) o exige ao lado.

## Refeito por script (`cetico2_l131_RG191_refeito.txt`, a partir de `medir/A_poder_eventos/A1_por_evento.csv`, 31 eventos, σ_i = std do posterior)
- média ponderada δτ̂₂₂₀ = +0,0668 ± 0,0336 → z_vs_0 = 1,99 → N(5σ contra a RG) = 31×25/1,99² = **196**
- mesma base do revisor (`REFEITOS_REVISAO.json`: ±0,0332, z = 2,014) → **191,06**
- leituras (CSV): R-B 2,595σ → 115 · R-MOD 3,055σ → 83 · R-RAIZ-0 3,109σ → 80 · R-LIN 4,147σ → 45 (JSON do revisor: 112 / 81 / 78 / 44 — mesma base do «112» da ordem l.131)
- ⚠ a ordem já mistura duas bases: (d) l.129 usa ±0,0336/2,59σ (base CSV → 115) e (e) l.131 usa 112 (base 0,0332). Diferença ~3 %, não muda a conclusão; o «≈» cobre. O N contra a RG fica **≈ 191–196**; escrever «≈ 191» (base do 112) é coerente com o parágrafo.

## Por que não é gosto
- l.11 da ordem: «nunca exclua uma leitura por um critério que excluiria a própria RG». A ordem dá o N em que o critério exclui as leituras (112/81/78/44) mas NÃO o N em que o mesmo critério exclui a RG (≈191). O l.129 diz «o mesmo desvio que põe a RG a 2σ», mas não fecha a conta em N — e é a conta em N que a bancada vai ler ao lado de «112».
- Sem o 191, a leitura «a leitura cai antes da RG» (verdadeira em aritmética: 112 < 191, porque a predição TGL é −0,020 e o viés é +0,067) pode ser explorada como se o critério discriminasse TGL de RG. Com o 191 fica explícito que o critério cai sozinho: ele falsifica a RG a 5σ em ~191 eventos de mistura O4, logo não é estatística de teste — exatamente a consequência vinculante que a ordem já declara.
- Gravidade: **IMPORTANTE** mantida (inconsistência com a régua interna l.11; ambiguidade explorável pela bancada). Não é BLOQUEANTE: a consequência vinculante (proibição do offset fixo em 0) já está correta na ordem.
