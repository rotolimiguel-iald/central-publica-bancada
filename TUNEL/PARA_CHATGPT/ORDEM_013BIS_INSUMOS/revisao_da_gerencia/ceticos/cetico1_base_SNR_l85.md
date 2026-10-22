# CÉTICO 1 — achado «base de SNR do GW250114 = 9,07–10,65» (ORDEM 013-bis l.85; também l.35 e l.125)

**Veredito: NÃO refutado. Gravidade ajustada: IMPORTANTE (não BLOQUEANTE).**

## O que medi (script, 22/09/2026)

1. `C5_IMR_RECOVERY.json` (bancada, só leitura): campo `reference_SNR_403Mpc` por célula —
   O4: XPHM 9,066–10,066; SEOB 9,537–10,654 (faixa total 9,07–10,65); O5: XPHM 15,38–17,06; SEOB 16,20–18,07.
   É a FONTE DE REFERÊNCIA DAS INJEÇÕES (403 Mpc, PSD de referência, janela 10 t_M), como diz aud_4.txt l.74 — não é medida do GW250114.
2. Razões 40/ρ_ref refeitas: O4 **3,75–4,41** (aud_4 e a ordem dizem «4,2–4,4»: é só a ponta baixa); O5 **2,21–2,60** (aud_4/ordem «2,5–2,6»: idem).
3. Evento REAL na janela de 10 t_M: aud_2.txt l.119 ρ = √(602,36 + 576,44 − 2×407) = **19,10**; aud_4.txt l.74: 40 × 0,443 = **17,7** (0,443 = exp(−10 t_M/τ) com t_M = 3,354e-4 s, τ = 4,12 ms → 0,4430, refeito).
4. σ(δτ̂) = 0,058 e z = 0,343 da §4.0(a) (l.123) vêm do POSTERIOR pSEOB IMR completo do GW250114 (`A_poder_eventos/A1_por_evento.csv`: sigma_dtau_std = 0,05779; (0,087+0,103)/3,29 = 0,0578) — uma TERCEIRA base (≙ ρ_eff = 2/0,058 ≈ 34,5, SINTESE.md l.137). Não é «contradição» com o Fisher só-ringdown: são bases distintas, e a ordem não as separa.
5. z_RB (fonte fixa, σ = 2/ρ, δ = −0,0199): ρ = 9,07–10,65 → 0,090–0,106; ρ = 17,7–19,1 → 0,176–0,190; posterior IMR → 0,343.

## Por que o achado está certo
- l.85 escreve literalmente «na base de SNR do GW250114 (rede, janela de 10 t_M: 9,07–10,65 no O4)». A fonte (aud_4 l.74) atribui esse número à fonte de referência; o auditor dá o GW250114 real em ~17,7 (e aud_2 em 19,1). A ordem herdou a frase solta de aud_4 l.23/l.144 («2,5–4,4× o GW250114») e a promoveu a definição da base do portão, que será registrada com hash (`PORTAO_DO_PODER_013.json`).
- Efeito se a bancada obedecer à letra: a conversão SNR40 → «escala do GW250114» sai ×3,8–4,4 em vez de ×2,1–2,3; o z de um evento GW250114-like no portão cai a ~0,09–0,11 (metade do que o strain dá) e a 1/3,5 do z = 0,343 que E0 usa para N_alvo = 212. Inconsistência interna F4 × §4.0/E0, explorável na reconciliação de l.125.
- l.125 mistura o fator O5 (2,5–2,6, e na verdade 2,2–2,6) com o fator O4 (4,2–4,4, na verdade 3,8–4,4) numa faixa única «2,5–4,4×» e a chama de «o GW250114».
- §2 l.48 corrige o gênero da ORDEM 013 («base não fixada»), mas não diz que o «pós-fusão ~40» (ORDEM 013 l.77, l.99) é o SNR a partir do pico, e que na janela primária de 10 t_M ele vale ~18–19. A ORDEM 013 l.99 já avisava «a base de SNR tem de ser dita»; a errata deve fechar o número.

## Por que NÃO é bloqueante
- Nenhum veredito muda: todo poder fica < 5 em qualquer das três bases, e a base errada torna o portão MAIS conservador, não menos (aud_4 l.76: «a conclusão fica mais forte»).
- A ordem já manda «dizendo a conversão» e a bancada mede; os N_alvo de E0 assentam no posterior (0,058), que está certo e tem fonte.
- Não fabrica número (9,07–10,65 existe no JSON), não decide partição, não viola régua. É número com rótulo errado + faixa mal copiada + errata incompleta: IMPORTANTE.

## Correção final (texto pronto; ver StructuredOutput)
