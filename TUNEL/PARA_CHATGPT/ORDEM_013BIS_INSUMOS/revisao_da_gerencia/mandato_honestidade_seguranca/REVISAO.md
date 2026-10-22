# REVISÃO ADVERSARIAL — ORDEM 013-bis · lente: MANDATO DO OPERADOR, HONESTIDADE E SEGURANÇA

**Data:** 22/09/2026 · **Revisor:** Claude (subagente da gerência) · **Objeto:** `...\scratchpad\ordem013\bis\ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md` (65.268 B, 286 linhas, sha16 `dbc5e7f2c2bc5698` lido por script) + `PROMPT_CODEX_ORDEM_013BIS.txt` + `ORDEM_013BIS_INSUMOS\` (estado do scratchpad às 12:00 local).
**Nada foi escrito fora desta pasta; nenhum processo tocado; pasta da bancada só lida.**

## O que foi medido (não dito de memória)

- sha16 lidos por script: `um.py` 31.136.661 B `d9f5bd5dffc3333d` ✓ (l.6, l.243); `TUNEL_PROTOCOLO.md` 5.425 B `4234902dc6f5e03c` ✓ (l.271); ORDEM 013 50.620 B `d4440c6a28eaad4b` ✓ (l.5, l.272); manifesto 013 3.737 B `ef951a3fc8fe840e` ✓ (l.273); selo v369 51.321 B `18db1bbd8462c3be` ✓ (l.245).
- `grep -c scratchpad` na ordem: **0**; no prompt: **0**. Termos `nome-confidencial-1|nome-confidencial-2|.env|senha|token|E:\|Escritorio|RESERVAD|termo-restrito-3`: **0** na ordem e no prompt; nos insumos só as frases negativas saneadas do aud_5 (l.37, 42, 43 — nomes de `.bak`, não confidenciais).
- Os 13 arquivos de medição citados por sha16 na `SINTESE.md` §0/§7 e no `CRITICO.md` §0/§5 existem como cópia de bytes em `ORDEM_013BIS_INSUMOS\medicao_da_ampliacao\` com o MESMO sha16 (13/13 OK).
- Erratas da §2 contra a ORDEM 013: (1) «média da razão condicional» está na ORDEM 013 l.227 ✓; (2) prior «[t_P, GM_f/c³]» l.228 ✓; (3) «atribuição CC BY 4.0» l.299 ✓; (4) «SNR de ringdown» **NÃO existe na ORDEM 013** (as únicas menções a SNR são l.99 — «SNR de REDE ~1,1×10³, equivalente a SNR pós-fusão ~5,7×10²», ou seja, a base ESTÁ fixada — e l.206).
- Processos vivos (`wsl ps` 12:03 local): 3 pais `1261 run_real_phase_importance --processes 4`, `1413 run_continuous_source_curves SEOBNRv4HM --workers 2`, `1449 ... IMRPhenomXPHM --workers 12`, etime ≈ 5h23. Os números 34860/43367/19681 da ordem são `session_id` do `STATUS_ORDEM_013.json`, não PIDs do `ps`. `PROGRESS.json` às 15:05Z: 8976/22384 (40 %), 2304/8520 (27 %), 13104/22384 (58,5 %) — as ETAs da ordem (~8/~14/~4 h) conferem por regra de três. A hora «14:15» da l.41 é UTC não marcada.
- `STATUS_ORDEM_013.json` traz `goal_status = WORK_RESUMED_NOT_COMPLETE` e (aud_5 l.10/33/52) «user requested continuation». A ordem tem **0** ocorrências de «continuation/continuação».
- Notas em `DO_CHATGPT\ENTREGA_013*.md`: **31 arquivos, mas 30 no intervalo 21/09 20:05 → 22/09 10:04**; o 31.º é `ENTREGA_013_ESPONTANEA_nulidade_e_tela_construida_no_ponto.md` de **05/09/2026** (outra ordem).
- «como no piso dos vazios» (l.125): grep em `um.py` por `poder|power` junto a `90 %|0.9|1.28` → **0 hits**; o piloto populacional do piso usa `P_LCDM_falsify ≥ 0,05` e a v4.1 usa `β·Σμ ≥ 25`. A afirmação não tem fonte no canônico.
- Eventos O4 com strain (SNR_rede ≥ 12) sem posterior pSEOBNR publicado: `gwosc_strain_files_snr12.json` (45) − `A1_por_evento.csv` (39) = **31 eventos** (GW240413_022019 … GW241111_111552). Para δτ̂ eles são CEGOS; a ordem (l.184) os rotula NÃO-CEGOS em bloco.
- Aritmética: (5+1,28)²/25 = 1,5775 ✓; 212×1,578 = 334,5 → 335 ✓; 2.062×1,578 = 3.254 (a ordem diz «≈ 2.100» e depois «≈ 3.250»: 2.100×1,578 = 3.314).
- ORDEM 014 na ordem: **0** menções (os hits de «014» são `0,0147` e `0,0143`).
- E4.4 (l.191) não está em nenhum marco (§4.1 l.210 e §6 l.229 atribuem só E4.1–4.3 ao MB2).

## Respostas ao mandato da lente

**(1) Obedece à exceção do operador?** Em substância sim: não há congelamento de escopo; a Parte B pré-registra a ampliação. Mas «congela» em três lugares sem dizer: (a) l.184 — os 45 O4 públicos com strain saem do teste em bloco como NÃO-CEGOS, quando 31 deles nunca tiveram δτ̂ publicado (é a única ampliação disponível HOJE, e a ordem a rebaixa a calibração por rótulo, não por número); (b) l.199 (E5.5) — «só eventos com σ_δf̂ < 0,03» é seleção pela largura do posterior, exatamente o que a l.216 proíbe; (c) l.56 (F0) — o padrão «encerra ela mesma» destrói ~5,4 h × 22 workers de trabalho em curso sem ganho (a Parte A «se recalcula em segundos», l.53) numa decisão que o relatório pôs ao operador e ele não respondeu. Amplia o que ele não pediu explicitamente: E3 (PE própria, piloto de até ~25 h de parede), E4/E5, E7 — é a ORDEM 014 absorvida, sem dizer. A frase da l.49 («nada físico se congela; o que se fecha é o que estava aberto sem critério de término») é fiel ao propósito mas falsa na letra por (a) e (b).

**(2) Cobre os 6 itens do relatório?** Sim: M1–M6 → F1–F6; portão com hash → F4; C6-pre → F5; C5 parede → F4; seção 2 inteira (GWTC-3 18 e 10) → F1/F2/F6/F7; «congelar» → substituído. A **ORDEM 014 foi absorvida (E3 rota b IMR; (g)/(i)/E6 O5/3G; E5 largura de δf̂) e NÃO está dito** — e a decisão 4 do relatório («A ORDEM 014?») não foi respondida pelo operador.

**(3) Honestidade.** A ordem diz, sem suavizar, que o R-B não fecha 5σ por contagem em O4 nem em O5 (l.135) e só em 3G com modelo a 0,40 % (l.139) — mas diz isso na l.135 de 286, dentro de §4.0(g); o §0 (l.20) não traz o número-manchete. Não há promessa; há uma frase em «anos» sem banda (l.135 «R-LIN fecha em ~1 ano de O5») contra a própria régua da l.216. Tom: construtivo (l.113 «nada disso é derrota»; l.141 «compra a CONDIÇÃO»). RG como rival: **nenhuma ocorrência**; regra relativa mantida (l.169).

**(4) Decisões da gerência.** Propor convenções de aceitação é papel da gerência (TUNEL_PROTOCOLO l.22). Mas a ordem é imutável, e quatro decisões mudam o escopo do que «ampliar até 5σ» significa: poder 90 % (×1,578 no N_alvo) sem fonte no «piso dos vazios»; piso |δ|/5 [INPUT] sem dizer de quem, com brecha «ou o piso alternativo, declarado» (l.170) que a bancada pode explorar; o padrão de encerrar processos; o piloto E3.1 autorizado sem go. Só as três da §8 são vetáveis ao abrir. **Perguntas ao operador ANTES de publicar** (lista na conclusão).

**(5) Segurança.** Conforme: zero scratchpad na ordem e no prompt; zero nomes confidenciais; zero E:\ / Escritório; o publicador varre `PROIBIDO` na ordem e em todo insumo de texto; os aud_1..6 receberam cabeçalho de remissão. Resíduo: os arquivos de `medicao_da_ampliacao\` (SINTESE l.13–22 e 194–197; CRITICO l.108–110; `reconciliacao.json` ×9; `A_poder_eventos.json` ×2; `FONTES.json`; `MANIFESTO_B.json`; `REFEITOS.json`; `medir_E_stdout.txt` ×2; 5 scripts) citam `...\scratchpad\ordem013\bis\medir\...` como FONTE com sha16 — **todas cobertas por cópia de bytes (13/13 sha16 iguais)**, mas o README (l.3) só remapeia `auditoria`; a remissão de `medicao` não está escrita em lugar nenhum, e a cópia da SINTESE carrega 23,9 e 35 sem errata no próprio arquivo.

**(6) Tamanho.** 65 KB / 286 linhas (a 013 tinha 50 KB) — executável, mas §4.0 (l.121–143, ~12 KB) e F1-C0/C1 (l.62–63, ~4 KB) duplicam SINTESE/CRITICO/aud_1 que vão nos insumos, e a §7 (l.241–273, ~6 KB) duplica `FONTES_DA_CASA.json`. Corte sem perda de critério: ~18 KB.

**(7) O que falta para «publique».** Ver conclusão.

## Achados (linha · trecho · problema · correção) — ver StructuredOutput para o texto integral

IMPORTANTE: A01 §0 sem a manchete do número · A02 l.184 os 31 O4 cegos rotulados NÃO-CEGOS · A03 l.199×l.216 seleção por σ · A04 l.170 brecha do piso · A05 l.125 «como no piso dos vazios» sem fonte · A06 l.48 errata 4 atribui à ORDEM 013 frase que ela não tem · A07 ORDEM 014 absorvida sem dizer · A08 F0 padrão de encerrar + PIDs + hora UTC · A09 l.39 «não parou no M1» sem o «user requested continuation» · A10 l.4 «31 notas» são 30 · A11 E4.4 órfão de marco · A12 §8/prompt sem mecanismo de registro das respostas do operador · A13 E3.1 piloto sem go · A14 insumos: remissão de `medicao` ausente + SINTESE sem errata.
NOTA: A15 3.250 vs 2.100×1,578 · A16 «~1 ano» sem banda · A17 0,63 vs 0,25 do relatório aprovado · A18 R-RAIZ-0 4,0–6,5 fundido em 3,9–6,3 · A19 «O5 z≈0,8» (1 evento) vs «2,2–3,1σ» (população) · A20 cortes de tamanho.
BLOQUEANTE: nenhum — nenhuma decisão de partição tomada, nenhum hash fabricado, nenhum CONFIRMED, nenhum RG-rival. Mas A02+A08+A09+A13 juntos decidem, por padrão, coisas que o relatório aprovado pôs ao operador; a ordem é imutável — perguntar antes.

## Perguntas ao operador antes de publicar

1. Os três processos: encerrar ao abrir ou deixar terminar (3,5–13 h; nenhum produto entra em veredito)?
2. O «user requested continuation» do STATUS: o senhor autorizou o Codex a seguir além do M1? (muda a linha «Protocolo — NÃO PAGO» da §1 de «não parou» para «não entregou os marcos».)
3. A ORDEM 014 (rota b IMR, O5/3G, largura de δf̂) está absorvida na Parte B — confirma?
4. O piloto E3.1 (1 evento, 1 família, até ~25 h de parede) fica autorizado pela publicação, ou só com go?
5. Piso sistemático |δ|/5 (deixa passar 1σ_stat) ou |δ|/15 (usual)?
6. Convenção de poder 90 % (N_alvo ×1,578) — aceita?
7. Veto à convenção pSEOBNRv4HM_PA (E2.6)? Partição, se já a tiver (E2.7)?
8. Os 31 eventos O4 com strain e sem δτ̂ publicado podem entrar no TESTE (cegos, sob o registro E2, com PE = go)?
