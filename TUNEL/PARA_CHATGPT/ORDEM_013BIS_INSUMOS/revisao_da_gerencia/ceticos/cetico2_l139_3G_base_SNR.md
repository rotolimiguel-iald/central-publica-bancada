# CÉTICO 2 — ORDEM 013-bis, linha 139, §4.0 (i) 3G — achado da lente estatistica_poder

Veredito: NÃO REFUTADO (refutado=false). Gravidade mantida: IMPORTANTE. Um ajuste na correção proposta.

## O que medi (por script, 22/09/2026)

1. `bis/medir/B_catalogos/RENDIMENTO_E_5SIGMA.json` (gerado por `rendimento_e_5sigma.py:57-61`, `sig40=min(G)`, comentário «pos-fusao ~40 por ORDEM 1.3»):
   R-B N(SNR_RD≥50)=131,2 · N(≥100)=32,8 · R-MOD 43,2/10,8 · R-RAIZ-0 38,2/9,5 · R-LIN 10,3/2,6. Todos com Σz²=25 ⇒ poder 50 %.
   ×1,578 (l.125 da ordem): R-B 207/52 · R-MOD 68/17 · R-RAIZ-0 60/15 · R-LIN 16/4. Os números de l.139 («~130/~33/~40/~10») são N₅₀ numa ordem cuja convenção declarada (l.125) é 90 %. Confirmado.
2. Âncora: σ=0,058 posta em SNR_RD=40. Com a âncora em 34,48 (=2/0,058, Fisher da C5: 0,0497×40=1,99): 97,6/24,4. Confirmado (reviewer: 96,5/24,1 — diferença de arredondamento de dmed).
3. `ORDEM_013_RINGDOWN/C5_FISHER.json` → `same_source_R_B`: O4 {snr_if_O4_were_40: 40, z 0,405}; ET {snr_ratio 9,547, snr 381,9, z 3,856}; CE {17,456, 698,2, z 7,028}; scope «Same source, same projection, individual reference PSD; no detector network»; parameters M_det 68,1, χ 0,68, `source_status: ILLUSTRATIVE_INPUT`. Logo «z = 3,86/7,03 com um só evento» é a fonte de referência da C5 posta a SNR 40 em O4 e escalada pela razão de PSD — e aud_4.txt (bloco C5_IMR_RECOVERY, reference_SNR_403Mpc) mede que SNR40 na janela de 10 t_M é 4,2–4,4× a fonte de referência a 403 Mpc em O4. Não é «um evento» qualquer nem um GW250114. Confirmado.
4. Base do SNR_RD de Berti/Bhagwat: `berti_bhspec.txt` diz só «ringdown SNR, SNR_RD» (Fig. 76, Fisher em população sintética, ET-D + CE 20 km); a janela/início não está dita no texto em cache. A l.139 não declara base alguma; a errata 4 da própria ordem (l.48) exige «toda tabela de poder declara a base do SNR». Inconsistência interna confirmada.

## Onde a correção proposta precisa de ajuste

O «96/24» NÃO é o número certo em lugar de «131/33»: a equivalência 0,058 ≙ SNR_RD 34 vive na base do Fisher da C5 (só ringdown 220, fonte fixa, um detector), onde o GW250114 real tem SNR ~9–10 na janela de 10 t_M (aud_4) — o 0,058 do GW250114 vem do pSEOB completo (inspiral informa massa/spin). Âncora «~40 pós-fusão» e âncora «34 Fisher-equivalente» são bases distintas; nenhuma das duas é a de Berti/Bhagwat até a bancada a ler. O par 131/97 deve entrar como BANDA de sensibilidade à âncora (~30 %), não como número corrigido. Com isso a gravidade fica IMPORTANTE (ambiguidade explorável + violação da errata 4), não BLOQUEANTE (a ordem já manda a bancada refazer e já declara Fisher como teto na l.145).

## Correção FINAL (substituir a l.139 inteira)

Ver campo `correcao_ajustada` da saída estruturada (texto idêntico ao abaixo):

**(i) Onde o 5σ é alcançável por contagem: 3G** `[DERIVED; taxas [KNOWN] Berti et al. 2026 / Bhagwat 2023; datas [DECLARADO] e discordantes: ET 2035 vs «early 2040s», CE «mid-2030s to 2040s»]`: R-B com a fonte de referência da C5 (68,1 M☉ detector, χ 0,68, `ILLUSTRATIVE_INPUT`; posta a SNR 40 em O4 na base do Fisher da C5 — um detector, PSD de referência, sem rede; na janela de 10 t_M isso é 4,2–4,4× a fonte a 403 Mpc, aud_4) e escalada pela razão de PSD (ET ×9,5; CE ×17,5): z = 3,86 (ET) / 7,03 (CE) `[DERIVED — Fisher de fonte fixa, teto; não é um evento GW250114-like]`; população 3G com a âncora σ(δτ̂) = 0,058 do GW250114 posta em SNR_RD = 40 («pós-fusão ~40», ORDEM 013 §1.3) e σ ∝ 1/SNR_RD: **~130 eventos com SNR_RD ≥ 50 ou ~33 com ≥ 100 a 50 % de poder; ~207 / ~52 a 90 % (convenção desta ordem)** — banda de âncora: com o SNR Fisher-equivalente 34 (2/ρ, C5) dá 97 / 24 (N₅₀), bases distintas; R-MOD ~43 (~68 a 90 %), R-RAIZ-0 ~38 (~60), R-LIN ~10 (~16) com SNR_RD ≥ 50; largura de δf̂ em 3G: 5–9 eventos com σ_meas = 0,005. **A base do SNR_RD de Berti/Bhagwat (rede; início da janela) não está dita no texto em cache: a bancada a lê na fonte, declara-a (errata 4) e converte para a escala do GW250114 antes de qualquer N.** Taxas 10²/ano (≥ 50) e O(10)/ano (≥ 100) são [KNOWN] de ordem de grandeza; «anos» só como cenário com banda, nunca como alvo (o alvo é N). **Em 3G o problema inverte: a estatística sobra, o modelo manda** — o 5σ exige forma de onda validada contra NR a **0,40 % no amortecimento do 220** (R-B; hoje a discrepância SEOB × Phenom é 1,3–5,2 % na mesma fonte e até 9,7 % em outras).

## Fontes (caminhos)
- Ordem: `...\scratchpad\ordem013\bis\ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md` l.48, l.125, l.139, l.145
- `...\scratchpad\ordem013\bis\medir\B_catalogos\rendimento_e_5sigma.py:57-61`; `RENDIMENTO_E_5SIGMA.json` (N_5sigma); `FRENTE_B_RESULTADO.md:33`; `berti_bhspec.txt` (Fig. 76)
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C5_FISHER.json` (same_source_R_B; parameters) — só leitura
- `...\scratchpad\ordem013\auditoria\aud_4.txt` (bloco «C5_IMR_RECOVERY.json (reference_SNR_403Mpc)»)
- `...\scratchpad\ordem013\bis\revisao\estatistica_poder\REFEITOS_REVISAO.json` (3G_N5_RB_ancora_SNR40.0 / SNR34.28)
