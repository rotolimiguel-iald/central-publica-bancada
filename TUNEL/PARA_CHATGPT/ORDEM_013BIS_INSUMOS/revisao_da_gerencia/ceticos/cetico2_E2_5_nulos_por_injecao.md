# CÉTICO 2 — achado «E2.5 nulos por injeção» (ORDEM 013-bis l.171 vs l.183/l.218)

**Veredito: refutado = false. Gravidade mantida IMPORTANTE (com um agravante medido).**

## O que confere no texto (lido com numeração)
- l.165–166: «E2 — O REGISTRO DO TESTE … **O registro fixa:**» → os 10 itens são ESPECIFICAÇÃO do registro; l.178 aceitação = «registro completo nos 10 itens; smoke … nenhum posterior novo lido». Logo, em rigor, E2.5 não manda EXECUTAR — isto enfraquece a parte (ii) do achado (o conflito com l.218 só existe se a bancada ler E2.5 como execução).
- MAS a l.171 escreve «(a) FPR do 5σ **com ≥ 1.500 injeções RG na pipeline usada**; (b) σ_sys …; (c) c(SNR); (d) … p por MC do nulo no N_alvo … **dito**» — (d) é redigido como resultado a entregar, e (b)/(c) são literalmente os produtos de E3.3 (l.184: «produtos: **c(SNR)**, **σ_sys de δf̂**»), de MB4 com go (l.231). A ambiguidade «fixar vs executar» é real e explorável nos dois sentidos (MC trivial rotulado de «injeções na pipeline», ou recusa por §5 l.218).
- «pipeline usada» não está nomeada. O observável primário (l.168) vive nos posteriores pSEOB **da LVK** — pipeline que a bancada não controla (CRITICO.md B1: «o que a gerencia nao controla nos posteriores LVK»). Injeção RG «na pipeline usada» ou é (1) posterior sintético sobre a estatística hierárquica (minutos), ou (2) PE pSEOBNRv4HM_PA por injeção (81–542 CPU-h cada, l.182), ou (3) as injeções da própria LVK (`pseobnr_injection/`, E1.3, l.160). A ordem não diz qual.

## Agravante medido (script, scipy): o número 1.500 não faz o que a frase diz
- p(5σ unilateral) = 2,8665×10⁻⁷ (l.169 diz 2,87×10⁻⁷ — confere).
- Com 1.500 injeções RG, falsos positivos esperados sob H0 = 4,3×10⁻⁴; com 0 acertos o limite superior a 95 % da FPR é 2,0×10⁻³ ≙ **2,88σ**. Para esperar 3 falsos positivos a 5σ são ~1,05×10⁷ injeções; para UL95 ≈ p₅σ, ~10⁸ — **exatamente o que o próprio item (d) da l.171 diz («≥ 10⁸ draws ou o p-valor empírico no N_alvo»)**. O item (a) contradiz o (d) na mesma linha.
- Origem do 1.500: literal em `medir/S_sintese/escrever_sintese.py:181` (→ SINTESE.md:157), sem fonte, sem cálculo; não aparece em REFEITOS.json nem em A_poder_eventos. O único «1500» com fonte nas medições é o N da simulação de realização única do auditor 1 (aud_1.txt:60), outra coisa. Estatuto honesto: número sem lastro.
- Portanto (a) como está é NÃO-EXECUTÁVEL no sentido físico (1.500 PEs = 121k–813k CPU-h, o «inviável» de l.183) e INSUFICIENTE no sentido estatístico (calibra ~2,9σ, não 5σ).

## Correção FINAL (substitui o item 5 da l.171, mantendo estilo e estatutos)
Ver campo `correcao_ajustada` do JSON (idêntico ao bloco abaixo).

5. **Nulos, fixados no registro (o que se roda em MB2 e o que espera MB4, dito item a item):** (a) **FPR/calibração da cauda do 5σ** por Monte Carlo do nulo sobre **posteriores sintéticos** (gaussianos e não gaussianos, σ_i reais dos 31/33, c(σ) de E1 amostrado da sua covariância), **≥ 10⁸ draws no N_alvo ou o p-valor empírico no N_alvo, dito** — roda em MB2 (minutos; não é calibração de forma de onda); o mesmo MC dá (d) o nulo do LRT da rota IV com σ_i heterogêneos. **1.500 injeções não calibram um 5σ** (com 0 falsos positivos, UL95 = 2,0×10⁻³ ≙ 2,9σ `[DERIVED]`); (b) **σ_sys do canal δf̂** e (c) **c(SNR)** exigem PE por injeção RG em duas famílias com (M, χ) livres: **são produtos de E3.3 (MB4, só com go)** ou, se houver, das injeções da própria LVK (E1.3) — em MB2 entram no registro só como DESENHO (pipeline nomeada: pSEOBNRv4HM_PA/C7_NATIVE; sementes; N por célula de E3.2; critério de parada) e o gate sistemático fica VERMELHO até serem medidos. Nenhuma injeção com PE roda fora de E3 (§5).
