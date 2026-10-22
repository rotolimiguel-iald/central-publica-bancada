# CÉTICO 2 — achado «base de SNR do GW250114 = 9,07–10,65» (ORDEM 013-bis l.85, l.35, l.125; §2 l.48)

**Veredito: NÃO refutado. Gravidade mantida: BLOQUEANTE** (o número entra em `PORTAO_DO_PODER_013.json`, registrado com hash, como «base do GW250114»; a bancada o tomaria como fato).

## O que medi (script, 22/09/2026)
1. `C5_IMR_RECOVERY.json` (bancada, só leitura), campo `reference_SNR_403Mpc` por célula: O4 XPHM 9,066–10,066; O4 SEOB 9,537–10,654; O5 XPHM 15,38–17,06; O5 SEOB 16,20–18,07. Origem: `calibrate_imr_recovery.py` l.25 `RESPONSES = {"H1":(.7,.2),"L1":(-.3,.8)}` (fatores de resposta FIXOS, arbitrários), injeção a 403 Mpc em ruído recolorido pela PSD de referência, janela a partir de `start_tM=10`. **É o SNR da fonte de referência das injeções — não é o GW250114 medido no strain.** aud_4.txt l.74 diz exatamente isso («a fonte de referência a 403 Mpc dá SNR entre 9,07 e 10,65 no O4»).
2. GW250114 REAL na janela de 10 t_M, duas estimativas independentes: aud_2.txt l.119 (ρ ≈ 19,1 ± 1,5 pelo excesso da norma branqueada 602,36 + 576,44 − 2×407) e aud_4.txt l.74 (~40 × 0,443 = 17,7). Refiz o fator: exp(−10·t_M/τ₂₂₀) com t_M = 3,369477856e-4 s e τ = 4,12 ms = **0,4414** ✓.
3. Terceira base, usada pela própria ordem em l.123: σ(δτ̂) = 0,058 do posterior pSEOB publicado (IMR completo) ≙ ρ_eq = 2/0,058 = **34,5** (SINTESE.md l.137 já o diz: «0,058 ≙ SNR_RD ≈ 34»).
4. Conversões (σ = 2/ρ; δ_RB = −0,0199): ρ 9,07 → σ 0,2205, z 0,090; ρ 10,65 → σ 0,188, z 0,106; ρ 17,7 → σ 0,113, z 0,176; ρ 19,1 → σ 0,105, z 0,190; ρ 34,5 → σ 0,058, z 0,343. Fator SNR40/ρ: 4,41 / 3,76 / 2,26 / 2,09 / 1,16.

## Por que o achado está certo
- l.85 chama de «base de SNR do GW250114 (rede, janela de 10 t_M: 9,07–10,65 no O4)» um número que é da fonte de referência com resposta fixa. Com essa base, o z de um evento GW250114-like fica 0,09–0,11 — contradiz o z = 0,343 (σ = 0,058) que a l.123 usa para o MESMO evento.
- l.125 «σ = 0,0497 em SNR40 é 2,5–4,4× o GW250114 na janela de 10 t_M; com o σ real do GW250114 dá 212» é internamente incoerente: se SNR40 fosse 2,5–4,4× o evento, o σ do evento seria 0,12–0,22, não 0,058. O 2,5–2,6 é O5 e o 4,2–4,4 é O4 (aud_4 l.74) — misturados, e o 4,2–4,4 vale só para o XPHM (SEOB dá 3,76–4,19).
- l.35 «as células SNR40 são 4,2–4,4× mais fortes que o GW250114» herda a conflação do próprio aud_4 (l.23, l.133, l.144 dizem «o GW250114»; l.74 diz «fonte de referência»). A ordem copiou a frase solta, não a linha que a define.
- §2 l.48 corrige o gênero («base não fixada») mas deixa vivo o «pós-fusão ~40» da ORDEM 013 l.77 e a escala «a partir de ~40» da l.99, que os auditores mediram como ~18–19 na janela.

## Onde o achado original precisa de ajuste (incorporado na correção)
O achado propõe usar 17,7–19,1 como «a base do GW250114». Isso corrige a l.85, mas a ordem usa TRÊS bases e tem de nomeá-las, senão a bancada troca uma pela outra: (i) fonte de referência das injeções (9,07–10,65 O4; 15,38–18,07 O5); (ii) GW250114 real, só-ringdown na janela (17,7–19,1); (iii) GW250114 pelo posterior pSEOB publicado, IMR completo (σ = 0,058 ≙ ρ_eq 34,5 — é esta a base do z = 0,343 da l.123 e do N = 212 da l.125). A conversão do portão se declara nas três.

## CORREÇÃO FINAL (texto exato)
**l.85, substituir** «**na base de SNR do GW250114** (rede, janela de 10 t_M: 9,07–10,65 no O4) e também em SNR40 na mesma base, dizendo a conversão.» por:
«**com a base do SNR declarada nas três escalas que já existem, e a conversão entre elas impressa:** (i) a fonte de referência das injeções C5 (68 M☉, 403 Mpc, PSD de referência, fatores de resposta fixos `RESPONSES` de `calibrate_imr_recovery.py`:25; rede; janela de 10 t_M): 9,07–10,65 no O4 e 15,38–18,07 no O5 (`reference_SNR_403Mpc`) — **não é o evento**; (ii) o GW250114 REAL só-ringdown na janela de 10 t_M, que a bancada MEDE no strain/PSD real (estimativas dos auditores: ρ ≈ 19,1 ± 1,5 pela norma branqueada [aud_2]; ~17,7 = 40 × 0,441 [aud_4], com 0,441 = exp(−10 t_M/τ₂₂₀)); (iii) o GW250114 pelo posterior pSEOB publicado (IMR completo): σ(δτ̂) = 0,058 ≙ ρ_eq = 2/σ ≈ 34,5 — a base do z = 0,343 e do N = 212 de §4.0. Em SNR40 (fonte fixa): R-B 0,41, R-MOD 0,76, R-RAIZ-0 0,78, R-LIN 1,55 [REAL — C5_FISHER; aud_4]; para o GW250114 só-ringdown (ρ ≈ 18–19, σ = 2/ρ ≈ 0,105–0,113): R-B ≈ 0,18–0,19, as demais pela mesma razão — a bancada recalcula e registra as três linhas [DERIVED].»

**l.35, substituir** «as células SNR40 são 4,2–4,4× mais fortes que o GW250114» por: «as células SNR40 são 3,8–4,4× mais fortes que a fonte de referência das injeções no O4 (2,2–2,6× no O5) e ~2,1–2,3× o GW250114 real na janela de 10 t_M (ρ ≈ 17,7–19,1, aud_2/aud_4)».

**l.125, substituir** «(σ = 0,0497 em SNR40 é 2,5–4,4× o GW250114 na janela de 10 t_M; com o σ real do GW250114 dá 212)» por: «(σ = 0,0497 é o Fisher só-ringdown em SNR40 — 2,1–2,3× o GW250114 real na janela de 10 t_M e 3,8–4,4× a fonte de referência das injeções no O4 [2,2–2,6× no O5]; o σ = 0,058 do GW250114 é do posterior pSEOB com o IMR completo, ρ_eq ≈ 34,5, e dá 212)».

**§2, acrescentar item 6:** «**§1.1 l.77 e §1.4 l.99, “pós-fusão ~40”.** A ORDEM 013 tomou o SNR pós-fusão do pico; na janela de 10 t_M ele é ~18–19 (aud_2 l.119; aud_4 l.74: fator 0,441 = exp(−10 t_M/τ₂₂₀)). Toda escala “a partir de ~40” da l.99 fica sem efeito; vale a tríplice base de F4.»
