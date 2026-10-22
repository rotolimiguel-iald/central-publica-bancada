# CÉTICO 1 — achado «F0 — os três processos vivos» (ordem l.56–58) — 22/09/2026

## Medido
- Ordem l.41: 3 grupos vivos às 14:15 (PIDs 34860/43367/19681); l.56 padrão «encerra ela mesma» com veto do operador; l.58 aceitação «`ps` sem …»; l.222 «F0 decide, antes de qualquer job novo»; l.284 «(1) se os três processos vivos param ou terminam (F0)» é dito ao operador como escolha.
- F8 (l.113): o marco MA NÃO lista o anexo de F0 entre as condições de término.
- RELATÓRIO l.77: pergunta 1 ao operador «parar ou deixar terminar?» — sem recomendação; a resposta do operador («concordo com tudo, com uma exceção …») não a responde. Logo a ordem PRECISA de um padrão; qualquer padrão é escolha da gerência, não partição (a régua reserva ao operador H/relógio/universalidade/440 — não a higiene de processo).
- aud_4 l.95: ETA 8,4–12,7 h / 14,7–16,2 h / 4,9–5,7 h; l.146: «deixá-los terminar … ou encerrá-los; a decisão é do operador» — recomendação do auditor, não régua.
- `ps` no WSL em 2026-09-22T15:26:51Z (leitura só): `run_real_phase_importance --processes 4` (et 20806 s), `run_continuous_source_curves --family IMRPhenomXPHM --workers 12` (19381 s), `--family SEOBNRv4HM --workers 2` (19016 s); RAM usada 86/125 GB. PIDs vistos (1261/1413/1449) ≠ os da l.41 — a aceitação por NOME de script (l.58) está certa; a citação de PID na l.41 é só descritiva.
- Elapsed ≈ 5,3–5,8 h contra ETA total do grupo SEOB ≈ 20–22 h ⟹ no ramo «terminar», o grupo SEOB ainda estará vivo por ~14 h depois desta leitura.

## Veredito por item do achado
- (a) padrão «encerrar» ≠ decisão do operador: REFUTADO. A ordem entrega a escolha ao operador explicitamente (l.56 e l.284-(1)); o relatório fez a pergunta e não houve resposta, então um padrão é obrigatório; o padrão «encerrar» é coerente com o critério de parada que a própria auditoria pediu (aud_4: «não abrir rodada nova»; o ciclo reaberto ~10×). Inverter o padrão é gosto, não achado provado.
- (b) «encerrar não compra nada»: REFUTADO em parte. Não compra CPU para a Parte A (l.53), mas compra 86 GB de RAM/18 workers para a «busca opcional» de F3 (l.90) e fecha o ciclo sem critério de parada. Não é erro.
- (c) aceitação incompatível com o ramo «terminar»: PROVADO. Com ETA restante ~14 h (SEOB) e a Parte A sem CPU, é plausível MA antes do fim; a l.58 exige `ps` vazio nos dois ramos («a regra seguinte vale igual», l.56, não alcança a aceitação). A bancada poderia (i) matar para cumprir a aceitação contra a escolha do operador ou (ii) segurar MA. F8 não lista o anexo, o que deixa a ambiguidade em vez de resolvê-la.
- (d) `audit_phase_source` na aceitação: NOTA — trivialmente satisfeito (l.41 diz que terminou); só redundância.
- A correção proposta pelo revisor tem um defeito próprio: «a bancada acrescenta o anexo final quando terminarem, sem esperar recibo» viola o PARE de F8/prompt (após MA a bancada espera o recibo). O anexo final vai para o marco seguinte (MB1) ou para a resposta ao recibo.

## Gravidade: IMPORTANTE (inconsistência interna explorável), mantendo o padrão da gerência. Correção: só l.56–58, ver StructuredOutput.
