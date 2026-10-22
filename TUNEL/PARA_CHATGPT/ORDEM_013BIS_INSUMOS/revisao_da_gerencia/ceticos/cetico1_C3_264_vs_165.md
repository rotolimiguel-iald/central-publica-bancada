# CÉTICO 1 — achado «264 linhas recalculadas» (ORDEM 013-bis, l.33, §1 C3 «o que se aceita»)

**Veredito: refutado = false (achado CONFIRMADO por medição). Gravidade: IMPORTANTE (mantida).**

## Medido por script (22/09/2026)
- CSV `C7_INDEPENDENT/tables/event_reading_predictions.csv` (bancada, só-leitura): **264 linhas de dados = 33 eventos × 8 leituras** (R-A, R-B, R-RAIZ-0, R-RAIZ-EP4, R-RAIZ-REST, R-LIN, R-MOD, R-GLOBAL; 33 cada). Idêntica nas duas cópias em `cache/delivery_*`.
- `auditoria/aud_3.txt` l.6: «33 eventos × 5 leituras … recalculadas por mim»; l.39: «Recalculei **165 linhas** (R-A, R-B, R-RAIZ-0, R-LIN, R-MOD) … erro 0 nas quatro primeiras e 1.5e-11 em R-MOD». A l.137 recomputa R-RAIZ-EP4/R-RAIZ-REST/R-GLOBAL só para GW250114 (1 evento), não as 33 linhas de cada.
- Logo a ordem (l.33) declara 264 recalculadas onde a fonte diz 165. Sobram **99 linhas não recalculadas**.
- Nuance medida: R-GLOBAL tem δτ̂ = 0 e Γ = 0 em **33/33** (≡ RG por construção — leitura, não recálculo); R-RAIZ-EP4 coincide com R-A nas 4 colunas numéricas em apenas **13/33** eventos (a frase «Γ idênticos» da C1 vale para o GW250114, não para o catálogo inteiro — fora deste achado, mas fica dito). R-RAIZ-REST: 33 linhas sem qualquer conferência (δτ̂ ~ 1e-82 a 1e-83).

## Por que não se refuta
Não é gosto: a ordem será imutável e o recibo «ACEITO» da C3 transporta à bancada como fato um recálculo que o auditor não fez. A régua (hash/número lido do artefato; [DECLARADO] nunca disfarçado) exige o número da fonte. Gravidade IMPORTANTE (número errado no recibo; não induz erro de física nem decide partição; a substância das 5 leituras resolvidas está de fato conferida).

## Correção FINAL (substituir na l.33, célula «o que se aceita», o trecho exato)
DE: `264 linhas evento × leitura recalculadas (erro 0; R-MOD 1,5e-11)`
PARA: `165 das 264 linhas evento × leitura recalculadas pelo auditor (33 eventos × as 5 leituras resolvidas R-A, R-B, R-RAIZ-0, R-LIN: erro 0; R-MOD 1,5e-11); as 99 linhas sub-resolução (R-RAIZ-EP4, R-RAIZ-REST, R-GLOBAL — esta ≡ 0 em 33/33 por construção) não recalculadas [DECLARADO] — a bancada as confere por script na F1`
