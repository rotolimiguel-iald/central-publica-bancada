# ORDEM 013 — A CONFRONTAÇÃO DO RINGDOWN: da lei de dephasing à forma de onda, ao fator de Bayes e aos dados atuais (GW250114, GWTC-3/5) — com a auditoria do texto de confrontação

**DATA:** 21/09/2026 · **DE:** Claude (gerência, sessão da Central de Patentes) · **PARA:** bancada ChatGPT (via Codex, nesta máquina) ·
**RESPONDE A:** nenhuma ENTREGA (frente nova, por ordem direta do operador); última na via de volta: `ENTREGA_CONTORCAO_FONTE_REGIONAL_20260917.md` ·
**PROGRAMA DE REFERÊNCIA:** `um.py` **v369** (sha16 `d9f5bd5dffc3333d`, rodada COMPLETA 5698/5698), só leitura.

> **Ordem do operador (21/09/2026)** `[INPUT — verbatim em ORDEM_013_INSUMOS\ORDEM_OPERADOR_21SET_VERBATIM.md]`: «agora eu quero que vc elabore um handoff  para a sessão do chatgpt Codex ao nosso lado que precisa enfrentar essa questão abaixo para que possamos avançar, eu quero que vc elabore o prompt pra ela».
> A «questão abaixo» é um texto de confrontação que o operador colou (origem externa, não arquivado em nenhuma casa — varredura declarada em `LEITURA_05`), **verbatim** em `ORDEM_013_INSUMOS\TEXTO_CONFRONTACAO_OPERADOR_21SET_VERBATIM.md`. Ele termina com «Com isso vamos conseguir rodar com precisão nos dados atuais» — esse é o alvo.
>
> **Régua da casa, sem exceção:** o número corrige a frase; hash e número SEMPRE lidos por script, nunca de memória; **β nunca literal** (`ALPHA_FINE_CODATA_2018 × √e` em runtime); estatutos `[REAL] [DERIVED] [KNOWN] [INPUT] [ONTO] [OPEN] [DECLARADO] [CONJECTURE]` — **hipótese nova é [CONJECTURE], nunca [DERIVED]**; homônimo até prova; só fonte PRIMÁRIA para literatura, e diga se leu o texto integral ou só o abstract; **`NOT_FALSIFIED` ≠ `CONFIRMED`; CONFIRMED e PROVED são proibidos em veredito**; nenhuma entrega move o gate; **a RG é o limite clássico que a TGL recupera — coincidir com a RG é correspondência, não derrota** (errata do operador, `MEMORIA_DA_LINHAGEM.md` l.8128): diga sempre o tamanho da correção β contra a incerteza σ, nunca «a TGL não se distinguiu da RG».

---

## 0. O OBJETIVO VINCULANTE

Responder **com número** às quatro exigências do texto: (1) Γ_deph em termos de (M, a, D); (2) Γ_deph ≪ ω_QNM para buracos negros estelares; (3) o ln B esperado em O4/O5; (4) a forma de onda modificada que grupos independentes possam ajustar. E **rodar a comparação nos dados atuais**, sem aceitar as premissas que o número desmente e sem esconder as que ele confirma.

O produto que se quer é **a predição da TGL no espaço de parâmetros que a própria LVK já publica** (δf̂₂₂₀, δτ̂₂₂₀), **por leitura, evento a evento, com estatuto**. Junto com ela: o módulo de forma de onda, a confrontação com os posteriores publicados, a distribuição de ln B esperado e, depois do portão do poder, uma rodada registrada com hash em strain público.

**O que isto NÃO é:**
- não é prova nem confirmação da TGL, e não move o gate;
- **não escolhe a partição** (a que Hamiltoniano a lei se aplica e qual é o relógio): isso é do operador, como na v369, cujo registro vigente é `partition_declared = MODULAR_LAB_BRIDGE_OPEN`. Perguntado em 19/09, o operador remeteu a pergunta ao banco de pesquisa da sessão auxiliar (Codex); lá, «vácuo=dephasing» é frase do operador [INPUT/ONTO] com duas realizações matemáticas, e a identificação física fica [OPEN]. A bancada pode APONTAR onde, no seu próprio estudo, está escrito algo que toque a partição, sem escolher;
- não deriva τ★ nem κ a partir de α, β ou θ_M: a regra FP-5 do kernel (`TheHorizonRate.lean`) proíbe κ = F(α, β, θ_M, …) como objetivo;
- não reabre o eco (v341–v348).

---

## 1. O ESTADO DE PARTIDA `[REAL — lido em 21/09/2026 por cinco leitores independentes da gerência e revisto por três revisores adversariais; relatórios em ORDEM_013_INSUMOS\LEITURA_01..05]`

### 1.1 O texto colado, afirmação a afirmação (a bancada REFAZ isto na C0)

Os leitores **divergiram** em algumas linhas; onde divergiram, isso está dito. A coluna da esquerda é paráfrase (o verbatim está no arquivo).

| afirmação do texto (paráfrase) | o que a casa e a literatura dizem |
|---|---|
| «A TGL prediz GKSL com L_k = √β·√K_∂(k)» | **Notação da casa, com estatuto mais fraco que «prediz».** A ocorrência mais antiga no índice é o README do pipeline TGL_v2 (25/05/2026); a forma exata está em `Davies_geometry.tex` (31/05/2026: fator finito tipo I, **não III₁**) e na legenda da fig02 do Artigo A público (`tgl_paper_unified.py`:9131, «Unique GKSL operator»), candidata a fonte do texto externo [CONJECTURE]. No `um.py` v369 existe UM só L = √β·√K, em `_verb_L` (l.2311–2332). Ali K é um **proxy 4×4 aleatório (seed 11)**, com estatuto `[FINITE_DIM_SANITY_NOT_III1_PROOF]`, e esse L não alimenta nenhum rito de onda gravitacional. O Teorema 1 do Artigo A **enuncia** √β√K, mas o **código** constrói saltos de Davies \|i⟩⟨j\| com taxas β·n_BE: **homônimo**. A família indexada L_k não existe no programa; o único «L_k» do um.py (l.7151–7156) é analogia da IALD. |
| «Γ_deph ~ β·⟨K_∂⟩» | **Contradito pela álgebra.** L = √β√K é Hermitiano, então a coerência entre autoestados de K decai a **Γ_ij = ½β(√k_i − √k_j)²**: diferenças, não média. O programa verifica isso ao vivo (`prove_dephasing_crossover`, l.2831–2875, resíduo 2e-5); a errata v369 ao lado diz que a coincidência com a lei canônica vale só no EXPOENTE. Já β⟨K⟩ = Tr(L†Lρ) é a taxa de saltos no desenrolamento canônico, e **nem é invariante**: L → L + c·1 (c real) dá a mesma equação mestra com outra taxa de saltos. No IR, um ⟨K⟩ grande **suprime** o dephasing (βΔk²/8k̄). Há ainda um problema de tipo. O K_∂ = −ln Δ **bilateral é assinado**, com JKJ = −K e KΩ = 0: isso é [KNOWN] por Tomita–Takesaki e está provado em kernel na FACE FINITA (`ContinuousModularZero.lean`, superoperador em matrizes n×n). Logo √K é mal tipado sem escolher uma parte positiva, e ⟨K⟩ = 0 no vácuo. O K unilateral −log ρ (⟨K⟩ = S em nats; `ModularFirstLaw.lean`) é homônimo e **não existe como operador em III₁**, onde não há matriz densidade. O texto, que pede ao mesmo tempo «fronteira III₁» e √K_∂, precisa escolher. |
| «escala natural de K_∂ ~ M/M_Pl² ~ 10⁷⁶ para 60 M☉; falsificada por O4 sem supressão» | **Dimensionalmente inconsistente.** K_∂ e β são adimensionais, então β⟨K⟩ não é taxa. Em ħ = c = 1, M/M_Pl² = GM é um **TEMPO**: para 60 M☉, GM/c³ = 2,96×10⁻⁴ s = 5,48×10³⁹ t_P. O «10⁷⁶» não sai de nenhuma grandeza natural de um buraco negro de 60 M☉ (varredura finita declarada: 12 candidatos na LEITURA_03 + `kernel_dimcheck.py`). O candidato mais próximo encontrado é (M☉/M_Pl)² ≈ 8,35×10⁷⁵ = S_BH(M☉)/4π, de UMA massa solar, não de 60 [DERIVED — hipótese de origem; a LEITURA_02 reproduz, a 04/05 não acharam leitura que dê 10⁷⁶]. O kernel prova um lema aritmético: nenhuma quantidade positiva é invariante por toda reescala (`scale_invariants_are_exactly_zero`, `kappa_is_not_fixed_by_ambient_scale`, `TheScaleHasNoFixedPoint.lean`) [REAL — kernel]. A aplicação ao III₁ usa o espectro modular ℝ₊ de Connes como hipótese [KNOWN, citada e não redemonstrada]. O próprio módulo avisa que faces finitas escapam ao no-go e que usá-lo para encerrar a busca é usá-lo além do que ele prova. Leitura permitida: a escala não vem da estrutura modular ambiente; entra por algo que a quebra, que aqui é o relógio τ★. **O que o texto acerta:** sem um relógio pequeno, leituras naturais dão taxas em tensão ou excluídas. Γ = β·c³/(GM) daria δτ̂ ≈ −0,13 no GW250114 (fora do intervalo de 90% publicado, ≈ 2σ), e a lei-raiz com k̄ = 0 está excluída nos relógios se a lei for universal. A «supressão» que o texto pede já é frase canônica («magnitude UV-suprimida», τ★ ≈ t_P [PRINCIPLED IDENTIFICATION]; Atlas §I.9, citado na LEITURA_05). O buraco honesto é outro: **nada deriva τ★** (v369). |
| «τ_deph ∝ 1/β, e deveria cair na faixa do LIGO O5» | **Não encontrado na casa.** τ_deph = 2/(βτ★ω²) é ∝ 1/β, mas também ∝ 1/τ★. Com τ★ = t_P, δτ/τ ~ 10⁻⁴² (invisível, «ramo A»). Só o «ramo B» (τ★ = GM_f/c³, **[INPUT]**) dá ~2%. Na casa, «O5» é estrato de 2025 dos ECOS (protocolo de 12/10/2025). |
| «Dephasing anômalo no ringdown: não testado — falta forma funcional» | **PARCIAL: errado na letra, certo no essencial.** A casa tem a forma desde 01/06/2026 (`Haja_Luz\CLAUDE.md` §20) e rodou o rito pré-registrado **v346** em 89 eventos GWTC (O1–O3b): δ = τ_obs/τ_GR − 1 = −½·β·τ★·ω₂₂₀²·τ_GR (`ringdown_dephasing_v2.py`:139–141). **V2, lida por hash** (sha16 `ff15f023dd91d8c7`): 15 séries de 11 eventos, **δτ = +0,1766 ± 0,1089** (1σ); previsão do ramo B −0,0194; z à RG 1,62; **poder 0,18σ** → `INCONCLUSIVE_SYSTEMATICS` (viés relativo 0,240 > 0,2). O mesmo empilhamento dá δf = −0,032 ± 0,013 (2,6σ) [REAL — lido]. O viés relativo 0,240 do V2 é o do estimador de τ (V2_reasons: «vies relativo de tau»); não há viés medido para f. Tratar o δf como sistemático até que as injeções da C5 meçam o viés de f. Três ressalvas: (i) com poder de 0,18σ, o rito não podia decidir a correção do ramo B; (ii) o relógio τ★ é [INPUT] e a partição é [OPEN]; (iii) **o mapeamento GKSL → forma de onda clássica não existe no programa** (é a C2 desta ordem). Divergência dos leitores: LEITURA_01/03/05 CONTRADITO, 04 PARCIAL, 02 NÃO_APLICÁVEL. |
| «β_TGL = α√e: não medido» | **Certo para ondas gravitacionais**: aí β não foi medido (ringdown com poder 0,18σ; ecos inconclusivos). Fora de GW, β foi medido livre na cosmologia e está em TENSÃO com α√e: D1 V3 (17/09/2026), β = −0,01275 (+0,00795/−0,00850), α√e a 3,01σ → `D1_BETA_TENSION` (`MEMORIA_DA_LINHAGEM.md` l.8200). |
| «K_∂ precisa ser expresso em (M, a, D)» | **Certo — buraco real.** No um.py, K_∂ é o proxy 4×4 aleatório, e nenhum módulo o liga a (M, a, D). A casa contorna isso com o τ★ dos ramos [INPUT]. É a C1 desta ordem. |
| «GR passa com precisão de poucos por cento; GW250114 confirma Kerr» | **[KNOWN] — parcialmente.** Na FREQUÊNCIA do 220, sim: GW250114 δf̂₂₂₀ = 0,02 ± 0,02 (90%). No AMORTECIMENTO, a precisão é ~10%: **δτ̂₂₂₀ = −0,01 (+0,10/−0,09), 90%** (arXiv:2509.08099, PRL 136, 041403, lido na fonte LaTeX). A LVK escreve «verification/consistent»; pela régua, consistência é NOT_FALSIFIED, e coincidir com Kerr é correspondência. |
| «Nenhum eco» / «ecos de longo atraso: consistente, não confirmatório» | **[KNOWN] + canon.** GWTC-3 e GWTC-4.0 TGR III não trazem evidência de eco (fonte LaTeX lida). Wu et al., arXiv:2512.24730, PRD 113, 124023 (2026), que inclui o GW250114, também não [KNOWN — só o abstract; conferir]. Na casa, v341–v348 deram `INCONCLUSIVE_SYSTEMATICS` / `NOT_FALSIFIED_UNDERPOWERED`; a busca de longo atraso tinha **eficiência 0,000** para um eco √β, e «não observado» ali não informa. |
| «Alargamento não-térmico de QNM não detectado» | **[KNOWN], com um detalhe de sinal.** Os catálogos puxam δτ̂ > 0, isto é, linhas mais ESTREITAS: GWTC-3 hierárquico 0,13 (+0,21/−0,22) (90%); GWTC-4.0 conjunto 0,17 ± 0,11 (90%, preprint arXiv:2603.19021). O rito V2 da casa puxa para o mesmo lado (+0,177 ± 0,109, 1σ). Qualquer taxa de amortecimento ADITIVA dá δτ̂ < 0; **se o dephasing GKSL vira amortecimento, e de que tamanho numa realização única, é a C2** (ver §1.4). |
| «Decoerência de OG é negligenciável no LIGO» | **Homônimo + [DECLARADO].** Na varredura declarada da LEITURA_04, não se encontrou nenhum limite numérico baseado em dados transientes do LIGO sobre decoerência na PROPAGAÇÃO de OG. A única exclusão da casa ligada ao LIGO (v369, P2) é sobre o **ruído da luz nos braços**, não sobre a onda. «Decoerência» ali mistura a coerência quântica do estado com a coerência de fase da onda clássica. **Compatível com o cânone no ramo A:** com τ★ = t_P, a própria casa prevê Γτ ~ 10⁻⁴². |

### 1.2 A lei, os ramos e a partição — o que o programa tem

- **A lei física dos ritos** é a forma de Milburn: dρ/dt = −(βτ★/2ħ²)[H,[H,ρ]], com **Γ_ω = ½·β·τ★·ω²** `[REAL na forma]` e τ★ = t_P `[PRINCIPLED IDENTIFICATION]`. «A lei nao diz a que Hamiltoniano se aplica» (um.py l.190961, grafia da fonte) `[OPEN]`.
- **Relógios v369** (`core.clock_test_result_v369`):
  - τ★ ≤ 4,8×10¹² t_P (95%, ⁸⁷Sr);
  - *se a lei for universal*, estão **EXCLUÍDAS** as leituras «lei-raiz com k̄ = 0» (taxa LINEAR na energia, Γ = βω/2) e «k̄ = massa de repouso»;
  - *se a lei for universal*, estão excluídas também Unruh-g (τ★ = 2πc/g, Γ_Sr ≈ 8×10³⁶ s⁻¹) e GM_⊕/c³.
- **Ramo B** (τ★ = GM_f/c³ [INPUT]): **δ_B = −β·(Mω₂₂₀)(a)·Q₂₂₀(a)**, que depende só do spin: −0,0094 (a = 0), −0,0203 (a = 0,68), −0,0415 (a = 0,9). D não entra (só via redshift, que cancela). A LEITURA_03 dá diferença 0,0 contra `per_series[2]` do V2; o critério formal está na C3.
- **Γ/ω = x/(2Q), com x = Γτ₂₂₀:**
  - nos ramos A e B e na lei-raiz-vácuo, Γ/ω ≤ β/2 ≈ 6,0×10⁻³ (o máximo, β/2 exato, é o da lei-raiz-vácuo);
  - na leitura modular da §1.4, ≤ 6×10⁻² com co-rotação; **sem co-rotação, Γ/ω ≈ 0,09–0,17 e x ≈ 0,6–1,7**, e aí NÃO vale Γ ≪ ω.
  - O critério observacional é x contra σ(δτ̂), não Γ/ω: a exigência (2) do texto, cumprida, não diz nada sobre viabilidade.
- **Um τ★ UNIVERSAL já é decidido pelos relógios.** O GW250114 dá, para τ★ universal, τ★ ≲ 3×10⁴⁰ t_P (90%), ~28 ordens mais fraco que os relógios. **O ringdown só testa relógios escalados pela fonte.**
- **Três leis de «dephasing» homônimas no próprio acervo** `[OPEN — tensão interna]`:
  1. a do kernel em comentário, **linear no gap** (β|K|, classe de Davies/Poisson–Cauchy; `NoFullWitness.lean` l.16–18). `Ergodicity.lean` prova só o semigrupo de Schur com taxas GENÉRICAS g_ij, nunca a taxa;
  2. a de Milburn, **quadrática** (L ∝ H);
  3. a **lei-raiz** de L = √β√K.

  O kernel não as reconcilia.
- **As falas do operador** `[ONTO — verbatim, MEMORIA_DA_LINHAGEM.md l.8114 e l.8122]`:
  - «[…] onda gravitacional=manifestação direta da gravidade pura; eco gravitacional=manifestação direta da resposta da fronteira»;
  - «a lei de dephasing do ringdown e minha definição não se chocam em nada, a gravidade pura responde o tempo todo à fronteira mesmo, betatgl está de fato na propagação da onda e ligada ao ringdown nmós provamos isso no teste dentro do um.py».

  O número ao lado, registrado no diário (l.8122): o programa tem a FORMA da lei, o protocolo pré-registrado e o V2 (`INCONCLUSIVE_SYSTEMATICS`); ver também as erratas ao lado (l.8124, l.8128). **A bancada NÃO relaciona leitura nenhuma a essas falas: isso é do operador.**

### 1.3 A literatura e os dados (localizados pela gerência; a bancada reconfere na fonte primária)

- **GW250114.**
  - Artigos: LVK, PRL 135, 111403 (2025), arXiv:2509.08054 (área/Kerr); LVK, PRL 136, 041403 (2026), arXiv:2509.08099 (espectroscopia/TGR). Fonte LaTeX lida.
  - Parâmetros: M_f = 62,7 (+1,0/−1,1) M☉ (fonte) e 68,1 (+0,8/−0,9) M☉ (detector); χ_f = 0,68 ± 0,01; D_L = 403 (+74/−70) Mpc; SNR da rede 80 (76,9 no GWTC-5.0 TGR); pós-fusão ~40.
  - **Strain público no GWOSC** (H1/L1, 4 kHz e 16 kHz, HDF5/GWF, CC BY 4.0; evento `GW250114_082203`). ⚠ A página HTML do GWOSC mostra «Network SNR 3.6»: é o SNR do modo (4,4), não o da rede.
  - **Amostras:**
    - IMR de (M_f, χ_f), com NRSur7dq4 preferido: Zenodo **10.5281/zenodo.16877102**. É o release do artigo de descoberta, **SEM δτ̂₂₂₀**.
    - **Posteriores de δf̂₂₂₀/δτ̂₂₂₀: Zenodo 10.5281/zenodo.17018009**, `TGR_companion_S250114ax_results.tar.gz` (1.671.496.586 B). Contém `gw250114_pseobnr/posterior_samples.h5` (a análise pSEOBNR do −0,01), `gw250114_pyring_results/` (pyRing, inclusive TEOB com domega/dtau_220 e grade de tempos de início) e `pseobnr_injection/` (injeções da LVK). Listado pela revisão da gerência via API do Zenodo; a bancada lista de novo antes de extrair.
- **Catálogos, em ordem de preferência:**
  1. **GWTC-5.0 TGR**: arXiv:2607.19293 (21/07/2026; 168 eventos até O4b, inclui o GW250114); release Zenodo **10.5281/zenodo.21454847** (`pSEOB.tar.gz` 711.331.923 B; `RD.tar.gz` 415.283.962 B; `QNMRF.tar.gz`). É o catálogo corrente e já aparece no SEU plano de 13/09. [KNOWN — localizado pela revisão; números a ler na fonte.]
  2. **GWTC-3 TGR** (arXiv:2112.06861, PRD 112, 084080): Zenodo **10.5281/zenodo.17461225** (`IGWN-GWTC3-TGR-v2-rin.zip`).
  3. **GWTC-4.0 TGR III** (arXiv:2603.19021): release de amostras **NÃO localizado** no Zenodo em 21/09/2026. Procure no DCC e no GWOSC; se não existir, os números do artigo entram só como [KNOWN] de conferência, nunca como posterior.
- **QNM de Kerr.** Berti, Cardoso & Will, PRD 73, 064030 (2006), l = m = 2, n = 0: f1 = 1,5251, f2 = −1,1568, f3 = 0,1292, q1 = 0,7000, q2 = 1,4187, q3 = −0,4990 (conferidos na tabela da fonte; são os do programa). Erro de ajuste ≤ 1,85%, **amplificado** em toda leitura com ω − mΩ_H perto de a → 1: em a = 0,9 a revisão achou −0,006 (BCW) contra −0,008 (Leaver exato), e em a = 0,99 um fator ≈ 34 (−0,0077 contra −0,00022; `revisao_da_gerencia\revisao_numeros_result.json`, bloco g). Para essas leituras, usar QNM exatos (Leaver / pacote `qnm`).
- **Fator de Bayes.**
  - Vallisneri, PRD 86, 082001 (2012), lido integral. Dele a gerência DERIVOU ⟨ln B⟩ ≈ ½(a/σ_a)² + ½ − ln[Δ_prior/(√(2π)σ_a)] **para parâmetro livre com prior plano Δ ≫ σ** (Laplace). **Para previsão PONTUAL** (τ★ fixo): ⟨ln B⟩ = +½z² se a leitura for verdadeira e −½z² se a RG for, com desvio-padrão z, sem o +½ e sem Occam.
  - Na prática, a LVK usa Savage–Dickey e nested sampling. bilby: Ashton et al., ApJS 241, 27 (2019) [KNOWN — só o abstract].
- **O5.** A meta do aLIGO era 330 Mpc para BNS e 2500 Mpc para BBH (LRR 23, 3, 2020), mas o **cronograma está «in discussion»** (página IGWN, 03/09/2026; antes vem o IR1, a partir de nov/2026). Não se achou número de SNR de ringdown típico em O5.
- **3ª geração (ET/CE):** ~10² eventos/ano com SNR_RD ≳ 50 (Berti et al., CQG 43, 123001, 2026, citando Bhagwat et al. 2023).

### 1.4 O que a gerência estimou e **a bancada tem de refazer, nunca copiar** `[DERIVED — estimativas; NÃO verificadas]`

- **Ramo B, sensibilidade** (δ = −0,0203, a = 0,68). σ(δτ̂) ≈ 0,058 no GW250114 (1σ a partir do 90%).
  - Separação esperada (Fisher) z ≈ 0,35. Para a hipótese PONTUAL «ramo B × RG», ⟨ln B⟩ = +½z² ≈ +0,06 se B for verdadeiro (−0,06 se a RG for), com desvio-padrão ≈ 0,35: **nenhuma decisão possível**.
  - O ln B observado com o GW250114 dá ≈ −0,001.
  - Com a amplitude livre a ∈ [0, 1], ⟨ln B⟩ ≈ 0,05 (integral exata). A fórmula de Laplace é inválida aqui porque o prior é mais estreito que σ, e daria o absurdo +2,5.
  - Para 5σ, σ ≈ 0,0041: ~200 eventos tipo GW250114, ou um único evento com SNR de REDE ~1,1×10³, equivalente a SNR pós-fusão ~5,7×10² (escalando σ ∝ 1/SNR a partir de ~40; grosseiro, e a base de SNR tem de ser dita).
- **Leitura coerente com L ∝ √n̂** (leitura da gerência para o K do texto; o texto não a afirma) `[DERIVED — não está no programa]`: ⟨a⟩ decai a ≈ β/(8N) **por unidade de tempo MODULAR** (checagem finita N = 16–256). Com a hipótese K = ħωn̂/(k_B T_H) e a conversão modular → Killing (k_B T_H/ħ, um [INPUT] de relógio), isso dá Γ ≈ βω/(8N) ~ 7×10⁻⁷⁹ s⁻¹ para N ~ 3×10⁷⁸ (T_H cancela). Um QNM não é modo normal: N = E_rad/ħω₂₂₀ é heurístico, porque E_rad inclui a inspiral.
- **Média de ensemble × realização única** (revisão da gerência, `fase_difusa`). Na média de ensemble ⟨h⟩, a taxa aditiva dá δτ̂ = −x/(1+x) e δf̂ = 0. Numa realização única (difusão de fase de Milburn), sem ruído de detector, o ajuste devolve δτ̂ médio ≈ 0,3 × (−x/(1+x)) e um **espalhamento de δf̂ por evento** ≈ 0,7·√(2x)/(2Q) (≈ 2,3% no ramo B). Esse espalhamento é da ordem da precisão atual em δf̂ (σ ≈ 0,012): o observável populacional seria a largura hierárquica σ_δf̂, não só μ_δτ̂. A GKSL sozinha não fixa o desenrolamento.
- **R-MOD, «leitura modular do horizonte»** — **[CONJECTURE — hipótese da gerência de 21/09/2026; NÃO é cânone nem leitura do operador]**.
  - **A hipótese:** se K_∂ fosse o gerador modular do exterior do buraco negro, então por quantum ΔK = 2π(ω − mΩ_H)/κ_H, e a forma de Milburn no tempo modular, convertida ao tempo de Killing, **reproduziria a FORMA da lei da casa, SE a identificação valesse**, com τ★ = 2π/κ_H e ω → ω − mΩ_H.
  - **Números** (δ exato −x/(1+x); BCW em `estimativa_da_gerencia\estimativa_leitura_modular.py`, Leaver em `revisao_da_gerencia\revisao_numeros_result.json`, bloco g): δ ≈ −0,037 no GW250114 (Leaver; BCW dá −0,038); ≈ −0,19 em a = 0; ≈ −0,008 em a = 0,9 (Leaver; BCW dá −0,006). A tendência de spin é OPOSTA à do ramo B, o que dá um discriminante por bins de spin. (O ramo B e a lei-raiz na §1.2 são LINEARES, −x, como no rito v346.)
  - **Sem co-rotação**, −0,38 no GW250114, a ~6σ do publicado (gaussiano).
  - **No GW250114, R-MOD (−0,038 exato, −0,039 linear) ≈ lei-raiz k̄ = 0 (−0,039 linear, −0,037 exato):** o evento sozinho não as separa; só a dependência em spin separa.
  - **Paredes conhecidas, a conferir na fonte** `[KNOWN — Bisognano–Wichmann e Sewell de memória, NÃO lidos; Kay–Wald: só o abstract, lido via INSPIRE pela revisão]`:
    - Bisognano–Wichmann (J. Math. Phys. 16, 985, 1975; 17, 303, 1976) vale para a cunha de Minkowski;
    - Sewell (Ann. Phys. 141, 201, 1982) vale para o horizonte bifurcado estático (Schwarzschild, Hartle–Hawking; a = 0);
    - **Kay & Wald (Phys. Rep. 207, 49, 1991) provam que NÃO existe estado estacionário Hadamard em Kerr** (a ≠ 0), ou seja, não há Hartle–Hawking de Kerr, e o estado de Unruh não é KMS no exterior;
    - **o mesmo relógio** (o período KMS do horizonte local) aplicado a um relógio de laboratório é a alternativa **Unruh-g**, EXCLUÍDA pelos relógios v369 se a lei for universal. A R-MOD só sobrevive com uma regra explícita de NÃO universalidade, e essa regra é partição, do operador.
- **A forma dimensionalmente consertada do texto colado**, Γ = β/t_M, daria −0,13 no GW250114: fora do intervalo de 90% publicado (−0,10; +0,09), ≈ 2σ.

### 1.5 Estratos que NÃO se citam como resultado

- `tgl_cosmological_observables.tex` (out/2025): «GW250114 −2,3 ± 15%», com outro mecanismo e sem fonte rastreável;
- o ln B = −89 da PE V1 do eco: artefato (as injeções não rodaram, GW190521 com 42% do peso);
- os Bayes factors de 2025 de outros canais («~100», «802», «1,2 ± 0,3»);
- o veredito do «juiz» de 08/08/2026 («Morto. Não invista.»): [DECLARADO], números não refeitos;
- o `TGL_article` de 2025: β ali é EXPOENTE livre de (K/K★)^β, homônimo de β_TGL;
- números de fonte secundária (Wikipedia etc.).

---

## 2. O PROTOCOLO DE APROVEITAMENTO — OBRIGATÓRIO ANTES DE QUALQUER LINHA NOVA

1. **Ler, nesta ordem:**
   - `ORDEM_013_INSUMOS\` inteiro.
   - `ringdown_dephasing_v1.py`, `v2.py` e `rite_ringdown_v346.py`: a forma, a âncora por filtro casado, a exclusão de borda, a autópsia V1→V2 e o Welch (v2 l.41–46).
   - Os dois `RINGDOWN_DEPHASING_*_RESULT.json`.
   - `echo_pe_v2.py`, o molde bilby+dynesty: prior de tempo ANCORADO, piso de massa, marginalização analítica da amplitude, injeções fora da fonte, jackknife, BLAS a 1 thread por processo.
   - **O seu `PLANO_EXPERIMENTAL_5SIGMA.md` de 13/09/2026**, que esta ordem executa: H₀/H₁, parâmetro de amplitude a, δτ = −x/(1+x) exato, convenção de Γ, GW250114 como estudo de sensibilidade, GWTC-5.0.
2. **Os scripts de `ORDEM_013_INSUMOS\` são para LER e COPIAR.** Antes de rodar qualquer um, copie-o para `Chatgpt\ORDEM_013_RINGDOWN\refeito\` e rode a cópia; **nada se executa dentro de `PARA_CHATGPT\`** (a via de ida é só leitura para você). Compare o resultado refeito com o do insumo por script e imprima a diferença. Os caminhos `…\scratchpad\…` citados nas LEITURAS são da sessão da gerência e efêmeros: NÃO são fonte. Para reconferir literatura, baixe o e-print (`https://arxiv.org/e-print/<id>`) para `Chatgpt\ORDEM_013_RINGDOWN\fontes\` e cite a sua cópia com sha256.
3. **Ficha de aproveitamento por alvo** (`REAPROVEITAMENTO_Cn.md`): o que já existe (arquivo:linha), o que se reusa, o que é novo e por quê. Não refazer o que está medido; não criar objeto sem consumidor.
4. **Lições que já custaram caro (v340–v350):**
   - o estimador se escolhe por INJEÇÃO, nunca pelo número da fonte;
   - nulo de descasamento com duas famílias de forma de onda;
   - prior de tempo ancorado (o GPS de catálogo é grosseiro);
   - robustez (jackknife, peso máximo por evento, borda) dentro da matriz de veredito;
   - emenda só com autópsia lida do resultado e hash novo ANTES do dado novo;
   - o smoke do registro em arquivo próprio, nunca sobrescrito.

---

## 3. O QUE SE PEDE — alvos C0–C7, entregues em MARCOS (a bancada PARA ao fim de cada marco e espera o recibo da gerência)

**Marcos:**
- **M1 — responde ao texto inteiro:** C0 + C1 (R-MOD como linha [CONJECTURE] com a estimativa refeita; derivação completa no M3) + C2 (fórmulas analíticas e convenção) + C3.1 (predição δf̂/δτ̂ por leitura) + **C5-Fisher** (distribuição de ln B esperado com as PSDs nomeadas, sem injeções).
- **M2 — roda nos dados atuais:** C4.
- **M3:** C3.2 (template) + oráculo completo da C2 + derivação completa (ou parede) da R-MOD e da R-PROP.
- **M4:** C5, injeção–recuperação.
- **M5:** C6, só depois do portão.
- **M6:** C7.

### C0 — A auditoria do texto de confrontação (refazer, não copiar)
Ficha `C0_AUDITORIA.md` + `.json`. Comece **segmentando o texto verbatim em afirmações atômicas numeradas T01…Tnn**, cada uma com a linha do arquivo. Para cada Tnn, registre:
- o veredito do conjunto {CANÔNICO, CERTO_NO_ESSENCIAL, PARCIAL, HOMÔNIMO, ESTRATO_ANTIGO, NÃO_ENCONTRADO, CONTRADITO_PELO_CANON, DIMENSIONALMENTE_INCONSISTENTE, KNOWN_CONFERIDO, DECLARADO, NÃO_APLICÁVEL};
- a evidência (arquivo:linha ou teorema; sha16 lido);
- a coluna obrigatória **«o que o texto acerta»** (pode ser «nada», mas dito);
- **a frase corrigida** que se pode dizer em público.

**Aceitação:**
- (a) toda linha não vazia de 3 a 65 do arquivo verbatim aparece em ≥ 1 Tnn, conferido por script;
- (b) a auditoria dimensional é refeita por script próprio, com unidades explícitas e CODATA 2018 para α, incluindo a origem do 10⁷⁶ como hipótese;
- (c) a álgebra GKSL de L = √β√K é refeita num oráculo independente (Liouvilliano construído e diagonalizado): taxa de saltos × taxa de decoerência, e a não invariância de Tr(L†Lρ) sob L → L + c;
- (d) a questão de tipo: dizer, com teorema citado, que operador positivo toma o lugar de √K (parte positiva K₊, |K| ou o unilateral −log ρ, que não existe em III₁), e calcular Γ nas duas escolhas principais;
- (e) nenhuma frase atribuída à TGL sem fonte.

### C1 — A partição para a onda: qual H, qual relógio (tabela de opções; a escolha é do operador)
Tabela `C1_LEITURAS.md` + `.json`, uma linha por leitura, **derivada com o MESMO rigor para todas**. Colunas:
- o Hamiltoniano/operador a que a lei se aplica;
- o relógio (τ★): INPUT, testemunha física ou derivado?;
- compatível com FP-5?;
- Γ(M_f, a_f) e, se couber, a dependência em D;
- x = Γτ₂₂₀ e Γ/ω para GW150914 (valores do programa) e GW250114 (fonte primária);
- estatuto;
- está no canon (arquivo:linha) ou é nova;
- bandeira **EXCLUÍDA_SE_UNIVERSAL** (relógios v369).

A coluna **«relação com as falas do operador de 16/09» fica EM BRANCO: é do operador.**

Leituras, no mínimo:
- **R-A** — ramo A do rito v346 (τ★ = t_P [PRINCIPLED IDENTIFICATION]). H = ħω a†a do modo 220 é escolha do rito, não do cânone.
- **R-B** — ramo B do programa (τ★ = GM_f/c³ [INPUT]).
- **R-MOD** — a hipótese da §1.4, **[CONJECTURE]**. Testar se ela se sustenta:
  1. o que Kay–Wald provam para Kerr e, portanto, em que sentido K_∂ pode ser gerador modular: a = 0 com Hartle–Hawking; a ≠ 0 só com restrição de região/modo (por exemplo, dentro da superfície de velocidade da luz, modos co-rotantes), ou com o estado de Unruh sem KMS global (diga qual e o que se perde);
  2. a conversão do tempo modular ao tempo de Killing;
  3. o sinal de ω − mΩ_H;
  4. a regra de NÃO universalidade que a separa da Unruh-g excluída (partição, do operador);
  5. se o −0,037 no GW250114 é a mesma leitura que a lei-raiz k̄ = 0 ou coincidência numérica;
  6. o que é [KNOWN] com fonte primária lida e o que é identificação [CONJECTURE].

  Se falhar em algum passo, a linha fica com o defeito nomeado; **falhar também é resultado.**
- **R-PROP** — dephasing na propagação sobre D com τ★ universal (t_P; a cota dos relógios). Na varredura declarada da LEITURA_01, item (f), o programa não tem leitura de dephasing que se acumule com D. Derivar com o mesmo rigor e dizer SE o ramo B aplicado à viagem é erro de tipo (a LEITURA_03 diz que sim, porque o M_f é da fonte [DERIVED], a conferir).
- **R-GLOBAL** — tempo comum a tudo (inobservável; Simon & Jaksch, PRA 70, 052104, 2004; conferir na fonte).
- **R-RAIZ** — lei-raiz de L = √β√K com k̄ ∈ {0, massa de repouso, E_P/4, ⟨K⟩ da leitura coerente}.
- **R-LIN** — lei linear no gap do comentário do kernel (β|K|, Davies). A **tensão linear × quadrática** fica dita, não resolvida por preferência.

**Aceitação:** unidades conferidas por script em toda linha; nenhuma leitura escolhida, preferida ou descartada pela bancada. **«Viável»** = toda leitura cuja Γ(M_f, a_f) fecha em unidades. Nenhuma é descartada: as de |δ| < 10⁻⁶ recebem só a linha analítica (ln B ≈ 0 por construção, dito, sem PE); as EXCLUÍDA_SE_UNIVERSAL entram com a bandeira. **Regra herdada da v369:** qualquer escolha de partição feita depois da C4 será registrada NÃO-CEGA.

### C2 — O mapeamento GKSL → forma de onda clássica (o homônimo que a literatura aponta)
O detector registra UMA realização de strain clássico, não a matriz densidade. Para cada gerador de C1, **derivar dois observáveis e dizer qual é o físico**:
- (i) a **média de ensemble ⟨h⟩**: decaimento de amplitude? deslocamento de frequência?;
- (ii) a **realização única** (difusão de fase / desenrolamento estocástico): δτ̂ médio e espalhamento de δf̂ por evento.

Dizer que modelo físico de desenrolamento se assume (Milburn = jitter de tempo por realização); o que acontece com ⟨h²⟩ (a energia se conserva sob dephasing de energia: vira potência incoerente com o mesmo espectro? o filtro casado perde SNR?); qual quantização se usa para um modo quase normal (não autoadjunto); e como N é definido (sensibilidade das conclusões a N). **Fixar a convenção** de Γ (coerência × amplitude × potência; os fatores de 2) e a forma exata δτ̂ = −x/(1+x) sob taxas aditivas. Dizer se δf̂₂₂₀ = 0 na ordem dominante, à luz do δf = −0,032 ± 0,013 do V2 da casa.

**Aceitação:**
- fórmulas analíticas + oráculos numéricos independentes: Liouvilliano diagonalizado; estado coerente com N até ~256 e extrapolação; trajetórias estocásticas para (ii), com e sem ruído colorido de detector; resíduos impressos;
- a afirmação explícita para N ~ 10⁷⁸;
- a convenção escrita numa linha que o módulo de C3 cita.

### C3 — A predição no espaço da LVK e o módulo de forma de onda (o item 4 do texto)
1. **C3.1** `tgl_ringdown_prediction.py` (numpy puro; β em runtime): uma função (M_f,det, χ_f, leitura, observável ∈ {ensemble, realização}) → (δf̂₂₂₀, δτ̂₂₂₀ e, na realização, o espalhamento). BCW para o ramo B; **QNM exatos (Leaver / pacote `qnm`) para toda leitura com ω − mΩ_H**, com o BCW só como controle e o desvio impresso. Inclui a tabela **evento a evento**: no M1, GW150914 (valores do programa) e GW250114 (GWOSC); no M2, com a C4, os eventos do GWTC-5.0/GWTC-3 com δτ̂₂₂₀ publicado.
2. **C3.2** `tgl_ringdown_template.py`: seno amortecido 220 (+221 opcional) no domínio do tempo, com τ_obs e f_obs da leitura, nas convenções de pycbc/bilby/pyRing (documentar fase, tempo de início e polarizações), + o **parâmetro de amplitude a** (a = 0: RG; a = 1: a leitura) do seu plano de 13/09.

**Aceitação (regressão):**
- com Mf_det e a_f lidos por script de `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\RINGDOWN_DEPHASING_V2_RESULT.json`, chave `per_series[2]` (GW150914; sha16 `ff15f023dd91d8c7`), e as constantes de `ringdown_dephasing_v2.py`:22–23 (G = 6,674e-11, M☉ = 1,98892e30 — NÃO são CODATA/IAU; diga isso), o módulo devolve `delta_pred_B` e `delta_pred_A` com **|Δ|/|δ| ≤ 1e-12** contra os valores LIDOS do mesmo JSON;
- um perfil CODATA 2018/IAU é permitido para as predições novas, com a diferença entre perfis impressa;
- testes de unidade; docstring com estatutos; nenhum literal de β.

### C4 — A confrontação com o que já está publicado (sem nova PE)
**Fontes:**
- GW250114: primário `gw250114_pseobnr/posterior_samples.h5` (Zenodo 17018009); secundário, só para robustez, pyRing TEOB domega_dtau_220 (mesmo release).
- Catálogo: GWTC-5.0 TGR (21454847) e GWTC-3 TGR (17461225). GWTC-4.0 só como [KNOWN] de conferência se não houver release.

Liste cada tarball (`tar -tzf`) antes de extrair; registre o sha256 do tarball e de cada .h5; diga se o release traz amostras por evento ou só produtos de figura (KDE/hierárquico); nenhum evento conta duas vezes entre releases (o GWTC-5.0 é cumulativo: GWTC-5.0 × GWTC-3 × 17018009).

**Estatística (fixada aqui):**
- Para uma leitura L sem parâmetro livre: B_{L/RG} = [p(δf̂ = δf̂_L, δτ̂ = δτ̂_L | d) / p(0, 0 | d)] ÷ [π(δ_L)/π(0)], com **densidade CONJUNTA (δf̂, δτ̂)** por KDE nas amostras do evento e o prior π lido do próprio .h5 (se for uniforme, diga que a razão é 1). Reporte também a versão só com a marginal de δτ̂ e a diferença.
- Predição dependente do spin: δ_L(χ_f) avaliada amostra a amostra (média da razão condicional) e na mediana.
- Leituras com τ★ livre: **não há ln B de ponto**. Reporte o limite superior de τ★ a 90%/95% com dois priors pré-declarados (log-uniforme em [t_P, GM_f/c³] e uniforme).
- Catálogo: produto das razões por evento; o hierárquico só como [KNOWN] de conferência.
- Por linha: ln B, z = (δ̂ − δ_L)/σ, e o tamanho da correção β contra σ.

**Regra de exclusão, pré-especificada e RELATIVA à RG.** Uma leitura só é `EXCLUDED_IN_READING` se ln B(leitura/RG) ≤ −ln(limiar) — limiar e nível de credibilidade registrados, com sha256, na ENTREGA do M1 — **e** se a RG não estiver ela própria fora do mesmo intervalo de credibilidade. Quando a RG estiver fora (é o caso dos posteriores conjuntos do GWTC-3, z(RG) ≈ 2,1, e do GWTC-4.0 O4a, z(RG) ≈ 2,5; gaussiano a partir do 90%), o veredito do catálogo para as leituras é `INCONCLUSIVE_SYSTEMATICS`, com o z da RG ao lado. **Nunca excluir uma leitura por um critério que excluiria o limite clássico.**

**Aceitação:** todo número com fonte primária e sha; o fato de o catálogo e o V2 da casa puxarem δτ̂ > 0 (sinal oposto a qualquer amortecimento aditivo) tratado sem cherry-picking; **NÃO-CEGO, dito sem atenuar**: esses posteriores são públicos, e a gerência já leu os números centrais.

### C5 — O ln B esperado e o portão do poder (o item 3 do texto)
- **C5-Fisher (entra no M1):** por leitura, declarar se a hipótese é PONTUAL (τ★ fixo) ou tem parâmetro livre, e reportar a **DISTRIBUIÇÃO** de ln B (média e dispersão), não só a média, contra o SNR de ringdown, com as PSDs:
  - O4 = Welch em dado FORA da fonte do GW250114 (só t < t_GPS − 2 s, como na chamada de `ringdown_dephasing_v2.py` l.149; a função está nas l.41–46), **sem ler a janela do evento antes do registro da C6**; referência `aLIGO_O4_high_asd.txt` (bilby). Se o strain ainda não estiver baixado no M1, use a referência e diga;
  - O5 = `Aplus_asd.txt` (bilby) e, como controle, `aLIGOAPlusDesignSensitivityT1800042` (pycbc), imprimindo a razão entre as curvas; diga que o cronograma de O5 está «in discussion»;
  - 3G = `ET_D_psd.txt` e `CE_psd.txt` (bilby) e, como controle, `EinsteinTelescopeP1600143` e `CosmicExplorerP1600143` (pycbc), com a razão impressa.

  Mais o número de eventos para 5σ.
- **C5-injeção (M4):** matriz com a = 0 e a = 1 por leitura, em ruído fora da fonte, com o nulo de família **SEOBNRv4HM (ou v4PHM) × IMRPhenomXPHM** (as famílias disponíveis; ver §5).

**Aceitação:**
- **viés** = |mediana(â) − a_inj| em unidades de a, com limiar 0,2;
- **cobertura** = fração das injeções com a_inj dentro do IC de 90%, aceita em [0,80; 0,97];
- **N ≥ 50 injeções por célula** (leitura × PSD × SNR);
- **poder** = |δ_L|/σ_comb, em σ, como no v346.

**Portão:** poder ≥ 5 ⇒ a C6 é teste; poder < 5 ⇒ a C6 roda como medida calibrada, com veredito máximo `NOT_FALSIFIED_UNDERPOWERED` ou `EXCLUDED_IN_READING`.

### C6 — O registro e a rodada nos dados atuais (strain público do GW250114; opcional: eventos O4 com strain aberto)
No molde do `CLOCK_TEST_V1` da v369: registro com hash, NÃO-CEGO dito, porque o δτ̂ publicado do GW250114 já é conhecido. O registro fixa:
- regras, leituras, priors, janelas, eventos e matriz de vereditos;
- parâmetros executados e versões das bibliotecas;
- **UMA rota de verossimilhança**, justificada por injeção:
  - (a) anel no domínio do tempo com covariância de Toeplitz do ruído, implementação própria, validada contra as amostras pyRing do release 17018009; ou
  - (b) sinal completo com o 220 modificado sobre SEOBNRv4HM/XPHM, no molde de `echo_pe_v2.py` (amplitude marginalizada analiticamente);
- a grade de tempos de início da rota (a): {6; 8; 10; 10,5; 12} t_Mf após o pico, primário 10 t_Mf, comparada às amostras pyRing na mesma grade.

**Mecanismo verificável:** o registro é entregue como `DO_CHATGPT\ENTREGA_013_C6a_REGISTRO_<slug>.md`, com o sha256 de `REGISTRO_C6.json`, ANTES de qualquer leitura do strain na janela do evento. O `RESULT_*.json` embute esse sha256, e o script recusa rodar se o registro em disco não bater.

**Vereditos permitidos:** `NOT_FALSIFIED_UNDERPOWERED` · `EXCLUDED_IN_READING` (com a regra relativa da C4) · `NOT_EXCLUDED` · `INCONCLUSIVE_SYSTEMATICS` · `AWAITING_DATA`. **Proibidos:** CONFIRMED, PROVED.

### C7 — O pacote para grupos independentes (em inglês)
README curto com: a lei; as leituras com estatuto; a tabela δf̂/δτ̂ por evento; os dois módulos; a reprodução. **A frase de escopo sai da tabela C1/C4, leitura a leitura, com estatuto** (ex.: *reading X [status]: predicts δτ̂₂₂₀ = … ± …; excluded / not excluded at …*). Hipóteses da gerência vão marcadas *[CONJECTURE — management hypothesis, not TGL canon]*; nenhuma leitura é nomeada antes da C4; nada de «confirma».

---

## 4. O QUE NÃO FAZER

- escrever no `um.py`, no kernel canônico (`Nós\tgl_kernel`), em memórias, selos, Atlas, diários, espelho ou site; **só a gerência incorpora** (um rito novo entra no um.py pela gerência, depois da auditoria);
- **escolher, preferir ou descartar leituras** (a C1 é tabela de opções; a escolha é do operador); relacionar leituras às falas do operador; derivar τ★ ou κ de α, β, θ_M (FP-5);
- declarar CONFIRMED/PROVED; tratar coincidência com a RG como derrota da TGL; tratar «não observado» de uma busca sem poder como exclusão; excluir uma leitura por um critério que excluiria a RG;
- citar os estratos da §1.5 como resultado; usar números de fonte secundária ou de artigo no lugar do posterior; hash ou número de memória; β literal;
- rodar ferramentas da casa que escrevem ao rodar (`atlas_indice.py`, `arvore_da_prova.py`, `porta_memoria.py`), o `um.py` canônico, ou qualquer script dentro de `PARA_CHATGPT\`;
- instalar pacotes em `/opt` do WSL (esses ambientes reproduzem os ritos v345–v347) ou no Python do sistema;
- abrir arquivos confidenciais e credenciais (os que o seu AGENTS.md exclui); entrar em `E:\` ou `C:\Escritorio`; usar como fonte qualquer material que não esteja nos insumos desta ordem, na tabela da §6 ou em fonte primária publicada;
- publicar qualquer coisa (o pacote da C7 é entregue à gerência; publicar é ato do operador).

## 5. COMO ENTREGAR (protocolo do túnel)

- **Onde e como.** Uma ENTREGA por marco em `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\`, com nome `ENTREGA_013_C<n>_<slug>.md` (ou `ENTREGA_013_M<k>_<slug>.md` para o fechamento de um marco). O prefixo `ENTREGA_013_C`/`_M` a distingue da `ENTREGA_013_ESPONTANEA_…` de 05/09, que não responde a esta ordem. Cada entrega segue o contrato do protocolo:
  - estatuto na 1ª linha;
  - critérios um a um, **PAGO / NÃO PAGO**, com a prova;
  - arquivos com **sha256 lido**;
  - o comando de reprodução;
  - o que NÃO foi feito;
  - tentativas falhas preservadas, com sufixo do defeito;
  - axiomas: «N/A — sem Lean» quando não houver pedra;
  - a ficha de aproveitamento anexada.
- **Bloqueios.** Se divergir o sha16 da ordem, de um arquivo dos insumos, do pacote v369 (`um.py`, `um_absoluto.json`, `um_absoluto_selo.json`, `rodada_v369_stdout.txt`) ou de qualquer outra fonte congelada: PARE e escreva `ENTREGA_013_C0_BLOQUEIO_manifesto.md`, com o arquivo e os dois hashes. Se divergir só uma fonte VIVA da casa (`MEMORIA_DA_LINHAGEM.md`, `Haja_Luz\CLAUDE.md`, `TUNEL_PROTOCOLO.md`, que crescem por append): registre os dois sha16 na ficha da C0, confira por conteúdo as linhas que a ordem cita (diário l.7700–7709, 8114, 8122, 8124, 8128, 8200; CLAUDE.md §20) e siga; se o conteúdo citado mudou, PARE como acima.
- **Artefatos** em `C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\`.
- **Downloads** (strain e releases) em `…\ORDEM_013_RINGDOWN\cache\`, com sha256 em `cache\MANIFESTO_DOWNLOADS.json` e a atribuição CC BY 4.0; nenhum arquivo acima de 25 MB fora de `cache\`. Baixar de gwosc.org, zenodo.org e arxiv.org (e de pypi.org / files.pythonhosted.org para os venvs próprios) é **permitido e necessário**. No M1, do GW250114 só o strain fora da fonte e a API de eventos do GWOSC; os releases do Zenodo são da C4/C6. Tamanhos:
  - GWOSC H1/L1 4 kHz HDF5 do GW250114: ~41 MB cada;
  - Zenodo 17018009: 1,67 GB;
  - Zenodo 21454847: pSEOB 0,71 GB + RD 0,42 GB;
  - Zenodo 17461225: 2,2 GB.

  **Sem rede:** escreva `ENTREGA_013_C4_BLOQUEIO_rede.md` com as URLs e os tamanhos exatos para o operador baixar, e pare a C4. Nunca substitua o posterior por números de artigo.
- **Instrumento (medido pela revisão da gerência em 21/09/2026).**
  - WSL `Ubuntu-24.04` (usuário root): `/opt/lal_env` (lalsuite 7.26.15, bilby 2.8.2, dynesty 3.1.0, gwpy 4.0.2, gwosc 0.8.3, h5py 3.16.0) e `/opt/pycbc_env` (PyCBC 2.11.0).
  - **NÃO há** pyRing, pyseobnr, pesummary nem qnm, e **faltam os dados de forma de onda do LAL**: SEOBNRv5/v4_ROM e NRSur7dq4 falham.
  - Famílias disponíveis: SEOBNRv4/v4HM/v4PHM × IMRPhenomXAS/XHM/XPHM/XO4a/TPHM.
  - SEOBNRv5/NRSur/qnm só num ambiente NOVO de usuário (por exemplo, `python -m venv ~/tgl013_env`, com os dados do LAL do Zenodo 14999310 via `LAL_DATA_PATH`), nunca em `/opt`; diga o que instalou e as versões.
  - Comando: `wsl.exe -d Ubuntu-24.04 -e bash -lc "..."` a partir do PowerShell (no Git Bash, exporte `MSYS_NO_PATHCONV=1`, senão `/opt` vira um caminho do Git). Nos pools, `OMP_NUM_THREADS=1` por processo.
  - Sem WSL: C0–C3 com numpy/scipy/sympy do Windows (Python 3.14; **sem h5py**). Para a C4, crie `…\ORDEM_013_RINGDOWN\.venv` (`python -m venv` + `pip install h5py`) e registre as versões.
- **Depois.** A gerência audita adversarialmente (refaz as contas, relê as fontes, roda as injeções de controle), incorpora o que passar como rito no `um.py` e roda o rito COMPLETO; **o operador ratifica**.

## 6. OS INSUMOS (caminhos absolutos; sha16 lido por script em 21/09/2026; o mesmo conteúdo, para máquina, em `ORDEM_013_INSUMOS\FONTES_DA_CASA.json`)

| papel | caminho | bytes | sha16 |
|---|---|---|---|
| o programa v369 (SÓ LEITURA) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | 31,136,661 | `d9f5bd5dffc3333d` |
| o JSON da rodada v369 (core) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` | 4,131,975 | `456f0ab149bb13f6` |
| o selo v369 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` | 51,321 | `18db1bbd8462c3be` |
| o stdout canônico v369 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\rodada_v369_stdout.txt` | 197,632 | `0dc67e39c16ff956` |
| pipeline do ringdown V1 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\ringdown_dephasing_v1.py` | 14,086 | `31a9f41da1b72321` |
| pipeline do ringdown V2 (a forma, l.139–141; constantes l.22–23; Welch l.41–46) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\ringdown_dephasing_v2.py` | 18,415 | `0793c58d6995194b` |
| o rito v346 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\rite_ringdown_v346.py` | 23,673 | `dd95a416f5d74e52` |
| o molde de PE bayesiana (eco v347) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\echo_pe_v2.py` | 26,408 | `ad51b73d9836686a` |
| a instalação do instrumento WSL | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\wsl_setup_lal.sh` | 1,847 | `953264c81b15b298` |
| resultado ringdown V1 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\RINGDOWN_DEPHASING_V1_RESULT.json` | 209,114 | `502c80fe2a37427e` |
| resultado ringdown V2 (alvo da regressão da C3: `per_series[2]`) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\RINGDOWN_DEPHASING_V2_RESULT.json` | 247,065 | `ff15f023dd91d8c7` |
| resultado da PE do eco V2 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\ECHO_PE_V2_RESULT.json` | 1,693,653 | `3072349afb00ab2c` |
| catálogo GWTC do programa | `C:\IALD\projetos_pyhton\IALD\gwtc_full_catalog.csv` | 27,787 | `895250e9d404a240` |
| no-go de escala | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheScaleHasNoFixedPoint.lean` | 6,891 | `0ed72186957c2a8a` |
| K bilateral assinado (face finita) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\ContinuousModularZero.lean` | 12,075 | `0dad5794f98ba1cb` |
| K unilateral e a primeira lei (face diagonal) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\ModularFirstLaw.lean` | 4,875 | `aee3eb49a6d0544e` |
| semigrupo de Schur (taxas genéricas) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\Ergodicity.lean` | 13,583 | `79bc3b939b6e4e59` |
| a «face GKLS» (unicidade da taxa) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\NoFullWitness.lean` | 7,250 | `fde4ca999c40e689` |
| κ testemunha, FP-5 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheHorizonRate.lean` | 4,731 | `0638b438d53d6c6e` |
| \|R\| = √β (amplitude do eco) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\SMatrix.lean` | 13,011 | `14f7e717a4ef7020` |
| \|R\|² = β em θ_M | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheVerbalCoupling.lean` | 11,431 | `912bf222f07256b1` |
| Bisognano–Wichmann na face finita | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\BisognanoWichmann.lean` | 8,191 | `5218c8eb32682a58` |
| Artigo A (Teorema 1 × Davies; fig02) | `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` | 1,216,423 | `29c92b66b2fd6b4d` |
| a nota de origem da forma exata de L_k (tipo I) | `C:\IALD\Artigo\Haja_Luz\Davies_geometry\davies_geometry.tex` | 18,365 | `46cee772901ee605` |
| o SEU plano de 13/09 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\bancada_corpus\TETELESTAI_V350_KERNEL_20260911\HANDOFF_SESSAO_UM_20260913\PLANO_EXPERIMENTAL_5SIGMA.md` | 11,436 | `f855e32523fede20` |
| o diário (l.7700–7709 v346; l.8112–8128 falas de 16/09 e a errata da RG; l.8200 D1 V3) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\MEMORIA_DA_LINHAGEM.md` | 685,017 | `7b17e5622271c6f4` |
| a memória da física (§20, a forma de 01/06) | `C:\IALD\Artigo\Haja_Luz\CLAUDE.md` | 1,196,984 | `55e12178b5bfb413` |
| o cálculo de 14/08 (ramo A inobservável) | `C:\IALD\Artigo\MCMC_V2_RAZAO\35_dephasing_ringdown.json` | 1,313 | `1ccc757b7757dcae` |
| o protocolo do túnel | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\TUNEL_PROTOCOLO.md` | 5,425 | `4234902dc6f5e03c` |

**A pasta desta ordem** é `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013_INSUMOS\`. Contém:
- os verbatim do operador: a ordem de 21/09 e o texto colado;
- as cinco leituras da gerência (programa, kernel, números, literatura, estratigrafia);
- os scripts e resultados numéricos (`numeros\`);
- a estimativa da gerência (`estimativa_da_gerencia\`, [CONJECTURE]);
- `FONTES_DA_CASA.json`, com caminho absoluto, bytes e sha16 de cada fonte da casa acima;
- **`MANIFESTO_INSUMOS.json`**, com o sha16 de cada arquivo da pasta e da própria ordem; ele não se lista a si mesmo.

## 7. PARA O OPERADOR ABRIR ESTA ORDEM NO CODEX

Abrir o Codex em `C:\IALD\Central de Patentes\Chatgpt` e colar o prompt da gerência. O texto integral está em `ORDEM_013_INSUMOS\PROMPT_CODEX_ORDEM_013.txt`, com sha16 no manifesto; em caso de divergência entre o prompt e esta ordem, vale esta ordem.

*Esta ordem não move o gate: ela define o objetivo. A matemática prova a implicação; a leitura (a partição) é do operador; a natureza decide a teoria.*
