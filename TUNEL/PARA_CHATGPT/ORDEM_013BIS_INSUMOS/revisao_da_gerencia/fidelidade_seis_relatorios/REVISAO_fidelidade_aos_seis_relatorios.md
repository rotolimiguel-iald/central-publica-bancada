# REVISÃO ADVERSARIAL — ORDEM 013-bis — LENTE: fidelidade aos seis relatórios de auditoria

Revisor: subagente da gerência (só leitura na bancada; nada escrito fora desta pasta). Data: 22/09/2026, ~12:05 −0300 (15:05Z).
Arquivo revisado: `scratchpad\ordem013\bis\ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md` (65.268 B, mtime 11:57 −0300), lido com numeração de linhas.
Fontes: `scratchpad\ordem013\auditoria\aud_1.txt … aud_6.txt`; disco da bancada `Chatgpt\ORDEM_013_RINGDOWN\` (STATUS, PROGRESS, AUDIT_RATE, C4_220_INITIAL); `ps`/`free`/`date -u` no WSL; ORDEM 013; relatório ao operador; `DO_CHATGPT\`.

## (a) Números da §1/§3 contra os relatórios

Conferidos um a um e ENCONTRADOS no relatório correspondente (lista não exaustiva, os que o brief pediu e mais): 38/38 (aud_1, aud_5); 8e-17 (aud_1: 8,3e-17 próprio, 1,4e-17 bancada); 2,9553e-4 s = 5,4817e39 t_P e 8,3468e75 (aud_1 l.37); resíduo 8,75e-9 e det = −Q′/Q (aud_4 l.124, aud_6 l.133); 0 de 96 e viés mediano 0,88 (aud_4 l.46); viés até 0,919 e cobertura 0,752 (aud_4 l.48-49); 444/1200 e 238/1200 (aud_4 l.60); 55 s (aud_2 l.4); 1e-10 e R-B −0,0026/R-RAIZ-0 −0,043/R-LIN −0,091/R-MOD −0,251 (aud_2 l.6); 52/52, 125/125, 194/194 (aud_3 l.48); 53 arquivos > 25 MB (2,71 GB) (aud_5 l.37); 8/30 notas (aud_5 l.38); ln B com 18: −5,40/−10,26/−18,11/−7,99 (aud_5 l.55); só-220: R-B −0,0156 e R-MOD −0,268 (aud_2 l.78: −0,2681); H1/L1 inícios realizados e first_index 1299333 (aud_2 l.68, l.41); BCW −0,0380 × −0,0368 e −0,0059 × −0,0077 (aud_1 l.58, l.118); a = 0: −0,192 × −0,025; a = 0,9: −0,0077 × −0,059 (aud_1 l.52); qnm 0.4.4 ≈ 1e-13 (aud_1 l.58); Ξ = 3,0e-23 (aud_1 l.54: 3,01e-23); 0,29 com N = 1500 e 0,0226 vs 0,0192 (aud_1 l.60); EP ≈ 0,003 (aud_1 l.127); 3,5e-16 (aud_3 l.4: 3,48e-16 R-B); ln B +0,029, |ln B| ≲ 0,1, correção/σ 0,34 (aud_6 l.6-7, l.41); +0,072 [+0,015; +0,134], HPD 0,983, −1,81/−3,56/−3,66/−8,22 (aud_6 l.39, l.129; aud_3 l.60); GWTC-3 +0,144, HPD 0,969 (aud_6 l.131); 24 de 31 (aud_6 l.43); V2 +0,177 (aud_6 l.57: +0,1766 ± 0,1089); z_RB 0,41/0,4074, SNR_RD ≈ 490, ~150 eventos, O5 0,80/ET 3,86/CE 7,03 (aud_4 l.41, l.44); z cai a 0,035–0,066 (aud_4 l.126); 0,443 (aud_4 l.74); 9,3e82 (aud_4 l.54); 4608 + 576 + 1200 (aud_4 l.45); 262144 Hz (aud_4 l.79-80); 01:36 de 22/09 (aud_4 l.94); 64,1 × 73,5 M☉ e 0,325 t_M (aud_2 l.16, l.42); C4 às 20:02, 22 min (aud_6 l.80); C7 até 05:00 (aud_5 l.50); 21 notas parciais (aud_4 l.69); 29/29, 37/37, 1.355 JSON, 344/344 (aud_5 l.3, l.26, l.35); 14,1 GB (aud_5 l.60: 14,13); 4 pastas mkdtemp com os nomes (aud_5 l.73); 20:41 (aud_5 l.41: 20:41:44); −0,1285 (aud_1 l.107); β/2 = 0,0060157 e rate(+3,−3) = 0 (aud_1 l.39); 0,0147 t_P (aud_1 l.78: 0,01473); R-A 2,3e-4 / R-B ~1e-16 (aud_3 l.40); −1,10/−2,67/−5,11 (aud_6 l.91); 17018009 MIT, 21454847 CC BY (aud_5 l.36); 2365 s / ~325 s (aud_2 l.93); H1 χ² 0,937 ~14σ (aud_2 l.98); R-MOD +0,62 em 6 t_M (aud_2 l.103).

Números da §1/§3 que NÃO estão em relatório nenhum, ou estão DIFERENTES:

1. l.33 (C3): «264 linhas evento × leitura recalculadas (erro 0; R-MOD 1,5e-11)». aud_3 l.6 e l.39: o auditor recalculou **165** linhas (33 eventos × 5 leituras: R-A, R-B, R-RAIZ-0, R-LIN, R-MOD) das 264 da CSV. As outras 99 (3 leituras) não foram recalculadas.
2. l.4: «as 31 notas `DO_CHATGPT\ENTREGA_013_*.md` (21/09 20:05 → 22/09 10:04)». Contagem em disco: **30** notas nessa janela (a 31ª entrada é `ENTREGA_013_ESPONTANEA_…` de 05/09/2026, anterior à ORDEM 013; há ainda um `.bak`). aud_5 l.38 conta 30 notas; o «31» é o «31 arquivos mudaram em DO_CHATGPT» de aud_5 l.22, que inclui o `.bak`.
3. l.35 e l.85: «a fonte de referência a 403 Mpc dá 9,07–10,65 no O4: as células SNR40 são 4,2–4,4× mais fortes que o GW250114» e «na base de SNR do GW250114 (rede, janela de 10 t_M: 9,07–10,65 no O4)». aud_4 l.74 diz 9,07–10,65 para **a fonte de referência das injeções** (68 M☉, 403 Mpc, PSD de referência, «fatores de resposta fixos»), não para o GW250114 medido. Os dois auditores que estimaram o evento REAL nessa janela dão ~18–19: aud_2 l.119 (ρ ≈ 19,1 pela norma branqueada, 602,36 + 576,44 − 2×407) e o próprio aud_4 l.74 (~40 pós-fusão × 0,443 = ~17,7). Ver BLOQUEANTE 1.
4. l.125 (§4.0 b): «σ = 0,0497 em SNR40 é 2,5–4,4× o GW250114 na janela de 10 t_M». aud_4 l.74: 4,2–4,4× é no **O4**; 2,5–2,6× é no **O5**. A faixa mistura dois detectores como se fosse uma incerteza.
5. l.41: «34860 … 43367 … 19681 … 58182» apresentados como o que «há em `ps`». Em `STATUS_ORDEM_013.json.active_processes` esses números são `session_id` (handles do Codex), não PIDs; os PIDs do WSL são 1261 (run_real_phase_importance, 4 workers), 1449 (XPHM, 12), 1413 (SEOB, 2) e 1819 (audit_phase_source, terminou) — aud_5 l.98. aud_4 l.95 também usa os session_id, então a origem é de auditor; mas a frase «há três em `ps`» com esses números não bate com o `ps`.
6. l.41: «às 14:15 de 22/09» sem sufixo Z, ao lado de «AUDIT_RATE.json, 14:02Z». A ordem foi gravada às 11:57 −0300; 14:15 só pode ser UTC (11:15 −0300). Verificado por retro-extrapolação dos PROGRESS.json (15:05Z: 8960/22384 = 40,0 %; 13072/22384 = 58,4 %; 2304/8520 = 27,0 %; taxas 0,460/0,738/0,128 draw/s ⇒ em 14:15Z: 33,9 % / 48,5 % / 22,5 % ≈ 35/49/23 %). A bancada, em −0300, lerá 14:15 como hora local futura.

## (b) BLOQUEANTE/CORRIGIR dos seis relatórios sem alvo F que os pague

- aud_6 CORRIGIR (l.54-57), δτ̂ > 0: o FIX pede «contagem de sinais, **o jackknife** e **o peso máximo por evento**» (jackknife do R-LIN [−8,32; −7,54]; nenhum evento > 13 % da soma). F2 (l.71) traz só contagem 24/31 e o V2; jackknife e peso máximo aparecem apenas no registro futuro E2.3 (l.169), não no adendo da Parte A.
- aud_6 CORRIGIR (l.59-62), estimador: «Rotular o oráculo 3D como controle de quadratura com o mesmo estimador; reportar ln B(R-B) como |ln B| ≲ 0,1 com sinal indeterminado; **acrescentar um estimador de densidade de fato independente**». A ordem não tem nenhuma das três exigências em F2/F6 (grep «oráculo 3D», «estimador independente», «controle de quadratura»: zero); F2-Aceitação (l.76) diz «sem novo KDE», o que fecha a porta ao estimador independente.
- aud_6 CORRIGIR (l.64-67), RD.tar.gz: «Baixar o RD.tar.gz (ou justificar por escrito) **e rodar o mesmo ln B por leitura como robustez**». F2 l.74 reduz a «listados (`tar -tzf`) com sha256». A robustez por segundo método sumiu.
- aud_6 NOTA (l.94-97), 440 fixo na RG em 32 dos 33 eventos: «Quantificar o efeito ou limitar a frase de escopo a “setor 220 condicional com modos superiores de Kerr”». A ordem não carrega essa frase de escopo em F2/F6 (grep: zero); toda a C4 é hipótese híbrida 220-TGL/440-Kerr e a frase de escopo das 10 leituras (F6) não o diz.
- aud_2 BLOQUEANTE 1 (l.54) e aud_5 (l.31, l.50): «**Perguntar ao operador se ele autorizou seguir além do M1** no goal do Codex». O relatório ao operador fez a pergunta (l.78) e a resposta «concordo com tudo» não a responde. A ordem não a carrega nem no §8.
- aud_2 CORRIGIR (l.86-89), pyRing: «Antes da C6b, reproduzir o Kerr_220_10M do pyRing com configuração equivalente e declarar a diferença residual». Não há C6b, mas há E3.1 (PE nova no mesmo evento) sem essa validação.
- aud_4 NOTA (l.103-106), Occam: «Manter esse aviso [ln B > 0 sem sinal em SNR40 é volume de prior] em qualquer texto público e **não converter esses ln B em σ**». Ausente (grep «Occam»: zero).
- aud_4 NOTA (l.108-111): «Nenhum grupo passou» vale só para FULL_IMR (0/288); MATCHED_RINGDOWN passa 94/288. Ausente (grep «FULL_IMR|MATCHED»: zero).
- aud_6 NOTA (l.84-87), ESS ≥ 100 / INCONCLUSIVE_DENSITY_SUPPORT: «registrar o limiar numa emenda datada, NÃO-CEGA». F7 l.109 só mapeia como status técnico; o limiar não é registrado.
- aud_6 NOTA (l.99-102), C4_JOINT_MODES: «Não ler o −0,137 como evidência e reportar a faixa entre estimadores». E4.2 l.189 manda «completar» sem o aviso.

Tudo o mais (aud_1 CORRIGIR ×8 e NOTA ×6; aud_2 restantes; aud_3 BLOQUEANTE e CORRIGIR ×6 e NOTA ×8; aud_4 BLOQUEANTE, CORRIGIR ×7, NOTA not_done e ln(1+x); aud_5 BLOQUEANTE, CORRIGIR ×5, NOTAs; aud_6 restantes) tem alvo F ou E que o paga — conferido item a item.

## (c) FIX de auditor endurecido ou afrouxado

- F1 Kay–Wald/BW/Sewell (l.63): aud_1 l.89 «Obter os textos integrais **ou declarar a parede com estatuto**» — a ordem é FIEL («se 403, parede DECLARADA com o que se tentou»).
- F4 «busca barata … se couber em < 1 h de máquina» (l.86): aud_4 l.91 disse «a busca de resíduo não linear, **que é barata**, ou declará-la NÃO PAGA». O «< 1 h» é da gerência, não do auditor; deve vir marcado como tal, senão a bancada pode declarar NÃO PAGO por um teto que ninguém mediu.
- F0 (l.56): a ordem faz de «a bancada encerra ela mesma» o padrão. aud_4 l.96/146 e aud_5 l.101: «a decisão é do operador»; aud_5: «Não matar nada». O relatório ao operador perguntou (l.77) «parar ou deixar terminar?» e não obteve resposta. O padrão da ordem inverte a preferência dos auditores e decide o que foi remetido ao operador.
- §2.1 (l.45): «a bancada acertou ao usar … razão de densidades marginais na predição **avaliada na mediana** e, como robustez, a integral da predição dependente do spin». aud_6 l.35-37 e `C4_220_INITIAL.json`: o primário (+0,029) é `lnB_joint_spin_curve` (cisalhamento amostra a amostra, jacobiano 1); `lnB_fixed_median_spin` = 0,027148 é o secundário. A ordem descreve ao contrário.
- §2.2 (l.46): «a bancada mediu por conta própria que o dado só começa a cortar em τ★ ≳ 5–10 GM_f/c³: ln B(5 t_M) = −1,10 …». aud_6 l.91 e l.127: foi o **auditor**, «estendendo por conta própria», «conta do auditor, NÃO-CEGA». A bancada não tem esse artefato.
- F2 RD.tar.gz: afrouxado (ver (b)). E1.3 (l.160) paga a leitura das injeções da LVK, que aud_6 pedia; ok.
- l.37 «55 s»: aud_2 (NTFS, primeiro byte 21:57:27) = 55 s; aud_5 l.5 (downloaded_utc 00:57:32) = 61 s. Os dois são reais e medem coisas diferentes; a ordem escolhe um sem dizer.
- F1 tabela em spin {0; 0,3; 0,5; 0,6785; 0,8; 0,9; 0,95} (l.63): o auditor deu 3 pontos; a grade é da gerência — aceitável, é mais forte no sentido certo.

## (d) Estado dos processos — conferido em disco e em `ps` (só leitura, 15:05Z)

- `cache\source_evidence\phase_native_repeat\SEOBNRv4HM_seed130942_N16384\AUDIT_RATE.json`: mtime 11:02:16 −0300 = **14:02Z** ✓; `status = PASS_ARITHMETIC_NOT_PRECISION` ✓; `passed_precision = 444` de 16384 draws (8520 inside) ✓; `scientific_acceptance = false`.
- `ps` no WSL: run_real_phase_importance (PID 1261, 4 workers, etime 5h23), run_continuous_source_curves SEOBNRv4HM (1413, 2 workers, 4h59), IMRPhenomXPHM (1449, 12 workers, 4h53). `audit_phase_source`: **ausente** ✓ (terminou). Três vivos ✓.
- PROGRESS.json (15:05Z): 8960/22384; 13072/22384; 2304/8520. Denominador = `valid_draws`, não N32768/N16384 (aud_5 usou 32768). Percentuais e ETAs da l.41 batem com 14:15**Z** por retro-extrapolação (ETAs de 8,9 h / 4,3 h / 14,4 h em 14:15Z; agora 8,1 / 3,5 / 13,5 h).
- RSS somado dos 21 processos python dos três jobs: **85,3 GB** agora (free: 83 usados de 125). O «~79 GB» da l.41 é plausível para 14:15Z; a RAM cresce ~6 GB/h — o F0 pede «RAM antes/depois», bem.

## (e) A §2 — os cinco itens

1. Média da razão condicional: erro real (ORDEM 013 l.231; aud_6 l.104-107). Mas a descrição do que a bancada fez está invertida (ver (c)).
2. Teto do prior: erro real (aud_6 l.89-92). Atribuição errada (auditor, não bancada; NÃO-CEGA).
3. Licença: correto (aud_5 l.36, l.88-91).
4. Base do SNR: correto no gênero, mas a §2 NÃO corrige o número que a ORDEM 013 pôs — l.77 «pós-fusão ~40» e l.99 «escalando σ ∝ 1/SNR a partir de ~40». Dois auditores medem ~18–19 na janela de 10 t_M (aud_2 l.119-120; aud_4 l.74). Este é o erro numérico da ORDEM 013 que a §2 omite, e é o que gera o BLOQUEANTE 1.
5. «Congelar»: correto (relatório l.60; ordem do operador).

Omissão adicional: a ORDEM 013 pediu «pseobnr_injection/» listada (l.81) e «RD.tar.gz» (l.83) e a bancada não os abriu — não é erro da ordem; ok.

## Achados (gravidade · seção · linha · trecho · problema · evidência · correção) — ver StructuredOutput.

## O que está certo (fidelidade)

- A tabela da §1 é, salvo os itens acima, uma transcrição fiel e densa dos seis relatórios: todo número testado (≈ 90) tem origem localizável no relatório da frente correspondente.
- F1, F3, F5, F6 e F7 pagam os FIX de aud_1, aud_2, aud_3 e aud_5 quase literalmente (bandeiras, passo 1/5, T02/T10/T11/T19/T20-21, teorema III₁ + ModularFirstLaw + |K|, BCW, unidades por sympy, N ≥ 1000, recolorido, realization, LEGACY, t_start, overtones, delta_tau_linear, reproduce_c6, frase de escopo, R-MOD marca, bundle único, MAX_PATH, 53 arquivos, mkdtemp com `finally`, errata ef1b4d69, contrato 8 notas, fichas, licença por arquivo, status técnicos).
- F4 registra o portão exatamente como aud_4 l.140 pediu (fonte fixa = limite otimista; todos < 5; C6 vira medida; INCONCLUSIVE mantido pela calibração reprovada), com a lista NÃO PAGO de aud_4 l.142-143 completa e o critério de parada de aud_4 l.96.
- A reclassificação C6-pre (F5) segue aud_2 l.24/129 e o adendo realizado traz os cinco inícios por detector, a diferença 0,325 t_M, a variante só-220 e a cobertura da guarda.
- O AUDIT_RATE.json, os três processos vivos, os percentuais e as ETAs da l.41 conferem em disco e em `ps`, entendendo 14:15 como UTC.
- Os relatórios copiados aos insumos são o conteúdo integral: diferem do original só por um cabeçalho HTML de 2 linhas (declarado no README_INSUMOS.md).
