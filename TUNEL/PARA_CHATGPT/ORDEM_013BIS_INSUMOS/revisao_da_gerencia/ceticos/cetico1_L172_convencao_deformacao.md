# CÉTICO 1 — achado L172 (convenção de deformação pós-pico) — 22/09/2026

**Veredito: NÃO refutado (refutado=false). Gravidade mantida: IMPORTANTE.**

## O que foi medido (só leitura; nenhum número novo — é questão de texto e estatuto)
- ORDEM 013-bis L172: «**Convenção única de deformação pós-pico [INPUT]:** a gerência propõe como padrão pSEOBNRv4HM_PA … O operador pode vetar». L219: «a gerência propôs UMA convenção de deformação como padrão, com veto dele». L284 (2): «se veta a convenção de deformação padrão (E2.6)». PROMPT L9: «(a gerência propôs pSEOBNRv4HM_PA como convenção de deformação padrão, com veto dele)».
- Fonte da própria gerência, `bis/medir/SINTESE.md:158` (§4.7) e `S_sintese/escrever_sintese.py:182`: «[INPUT do operador]: escolher uma entre pSEOBNRv4HM_PA …, C7_NATIVE … e C5 …». A ordem inverteu a autoria (operador → gerência com veto) e manteve o rótulo [INPUT]. Rótulo [INPUT] preenchido pela gerência viola a régua dos estatutos.
- O que as três «convenções» fixam (bancada, só leitura):
  - `C7_INDEPENDENT/tgl_ringdown_prediction.py:69,125`: Γ calculado com o ω **do modo passado** (`mode=(2,2,0)` default; com (2,2,1) dá outro Γ) — convenção **por modo** (é uma quarta, omitida na lista da SINTESE; aud_3.txt:113-116 já a apontou).
  - `STATUS_ORDEM_013.json:142` (C5): «All 22 overtones share the effective imposed 220 Gamma; 44 overtones share 440 Gamma … not a unique TGL overtone prediction».
  - C7_NATIVE (`medir_E.py:146`): h_a = h_all + (e^{-aΓ220 t}−1)h22 + (e^{-aΓ440 t}−1)h44 — envoltória sobre o harmônico inteiro (22 e 44), inclusive o que houver de overtone dentro dele.
  - pSEOBNRv4HM_PA: DTau220/DTau440 fracionais no QNM fundamental de cada (l,m).
  - Conclusão: **o δτ̂₂₂₀ fundamental é o MESMO nas três/quatro** (todas somam Γ₂₂₀ ao 220); elas divergem em (i) se/como os overtones se deformam e (ii) se/como o 440 se deforma. (ii) é declarado partição pela própria ordem (L22, L173, L190). (i) é da mesma classe (qual modo carrega a lei) e a C5 diz textualmente que não é predição única da TGL. Logo o conteúdo físico da «convenção» é do operador; o que é da gerência é só o **espaço de comparação** com o publicado (pSEOB, onde a C4 comparou) — fato instrumental [REAL], não escolha.
- ORDEM 013 L22/L169/L199/L278: escolher/preferir é do operador; a gerência nomeia tabela de opções. Vale por analogia.

## Por que não é BLOQUEANTE
Há veto explícito (L172) e o §8 leva a pergunta ao operador antes da abertura (L284). A ordem não decide sem ele; mas num pré-registro com hash (E2), «padrão salvo veto» vira o registrado por silêncio — e o piloto E3.1 «UMA família (pSEOBNRv4HM_PA)» (L182) já pressupõe o padrão. A bancada pode explorar a ambiguidade («a gerência mandou pSEOB») e o estatuto [INPUT] fica falso. IMPORTANTE.

## Ajuste à correção proposta pelo revisor (o que mudei e por quê)
1. Não chamar o **mapa TGL→δτ̂₂₂₀** de [INPUT]: ele é [DERIVED] por leitura (`tgl_ringdown_prediction.py`, fd0fc446e1c732f3) e coincide nas convenções. O [INPUT] do operador é **quais modos carregam a deformação** (overtones; 440).
2. Listar a quarta convenção (por modo, o template) — a SINTESE a omitiu; aud_3 a mediu.
3. «Rodam em paralelo» sem custo: o mapa analítico e as tabelas, sim, sempre; a PE/injeção de calibração roda no espaço de comparação (pSEOB, DTau220 + DTau440 nas duas variantes de E4.3) e o C7_NATIVE entra como controle de família já previsto em L181 — não triplica o orçamento de E3.2 (já «provavelmente inviável»). O piloto E3.1 numa família é **instrumental** (custo), dito assim.

## Texto FINAL para substituir (ver StructuredOutput / abaixo)
