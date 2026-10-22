# Leitura da gerencia (Claude) para a ORDEM 013 — os numeros (auditoria dimensional, lei da casa no QNM 220, propagacao, sensibilidade)

> Levantamento SOMENTE LEITURA feito em 21/09/2026 por um leitor independente da gerencia, depois revisto por tres revisores adversariais. Estatutos como gravados pelo leitor; onde a ORDEM 013 corrige esta leitura, VALE A ORDEM. Numeros [DERIVED] aqui sao estimativas A REFAZER; [KNOWN] de literatura deve ser conferido NA FONTE PRIMARIA. Editada para o escopo da ORDEM 013.
> **Caminhos em `...\AppData\Local\Temp\claude\...\scratchpad\...` sao da sessao da gerencia e EFEMEROS: nao sao fonte.** Para reconferir, baixe a fonte primaria (e-print do arXiv, release do Zenodo) para `Chatgpt\ORDEM_013_RINGDOWN\fontes\` e cite a sua copia com sha256.

SUMMARY: O texto de confrontação erra em dimensão e em álgebra, e o próprio programa já contém a resposta.

1. **Dimensão.** O K_∂ = −ln Δ e o β são adimensionais, então 'Γ ~ β⟨K⟩' não é uma taxa. O M/M_Pl² (com ħ=c=1) tem dimensão de TEMPO: vale GM/c³ = 2.96e-4 s para 60 Msun, ou 5.48e39 t_P. Nenhuma grandeza natural de um BH de 60 Msun dá 10^76. As grandes são (M/M_Pl)² = 3.0e79, S_BH = 3.8e80 e K_BH = 8π(M/M_Pl)² = 7.6e80.

2. **Álgebra GKSL.** Com o gerador da casa, L = √β√K (um.py:2311-2325), a coerência decai a ½β(√k_i−√k_j)², e no IR isso é βΔk²/(8k̄) (errata v369 em um.py:2837). Um ⟨K⟩ grande SUPRIME a defasagem. O β⟨K⟩ é a taxa de saltos. Minha checagem GKSL finita confirma: saltos = βN e decaimento de ⟨a⟩ ≈ β/(8N). Na onda clássica, com N ~ 3e78 quanta, dá Γ ~ 7e-79 s⁻¹ [DERIVED aqui].

3. **Lei da casa no QNM 220.** A lei é Γ = ½βτ★ω² e δ = −Γτ (ringdown_dephasing_v2.py:141).
   - Ramo A (t_P): Γ ≈ 8e-40 s⁻¹, δ ≈ −3.2e-42. É invisível; o ringdown fica igual ao de Kerr, e isso é correspondência com a RG, não derrota.
   - τ★ = t_P/β: o β cancela.
   - Ramo B (GM_f/c³, INPUT): δ_B = −β·mω(a)·Q(a), que depende SÓ do spin. Dá −0.0200 no GW150914 (o JSON dá −0.019962, diff 0) e −0.0203 no GW250114. O '−0.0194' registrado é a média ponderada da pilha V2.
   - Γ/ω = ½βτ★ω, no máximo 6e-3, então Γ ≪ ω em toda leitura.
   - O dephasing do ringdown FOI testado com forma funcional pré-registrada: V2 deu INCONCLUSIVE_SYSTEMATICS (viés 0.240), com poder de 0.18σ.

4. **Energia modular de um modo.** K = ħω_220/(k_B T_H) ≈ 15.4 no GW150914 e 15.6 no GW250114 (9.3 com a=0); com o termo superradiante, ≈ 4. A lei-raiz do programa com fundo E_lo = M_f c² dá Γ ~ 3e-80 s⁻¹. A leitura 'vácuo' (δ = −βQ ≈ −0.038) e a de massa de repouso já estão excluídas pelos relógios v369, se a lei for universal.

5. **Propagação.** Γ·D/c ≈ 3.4e-23 com t_P e 1.6e-10 com a cota dos relógios: invisível. Com o ramo B daria 2e17, mas isso é erro de tipo, porque o M é da fonte. Para ter Γ·D/c = 1 seria preciso τ★ ~ 1.5e-21 s, 10 ordens mais fraco que os relógios.

6. **Sensibilidade.** Hoje σ(δτ_220) ≈ 0.058 com GW250114 e 0.103 com GWTC-4 (arXiv:2509.08099, a conferir).
   - Ramo B: z ≈ 0.35 e ln B ≈ 0.06. Para 5σ precisa σ ≈ 0.004, ou seja, ~200 eventos tipo GW250114 ou SNR de ringdown ~1e3.
   - Canônico: ln B ≈ 0 sempre.

Faltas declaradas: o GW250114 não está no programa (os valores vêm de fonte secundária, a conferir na primária) e não verifiquei projeções de O5/CE/ET. O estrato antigo (tgl_cosmological_observables.tex, com 'GW250114 −2.3±15%') não deve ser citado.

Fontes web: https://arxiv.org/html/2509.08099 ; https://arxiv.org/abs/2509.08054 ; https://en.wikipedia.org/wiki/GW250114 ; https://www.emergentmind.com/topics/binary-black-hole-signal-gw250114

SWEEP: Leituras (só leitura): o texto verbatim da confrontação; ringdown_dephasing_v1.py e v2.py inteiros; os JSON RINGDOWN_DEPHASING_V1 e V2 (stacks, GW150914 por série, séries usadas); gwtc_full_catalog.csv (cabeçalho, linha do GW150914 e busca por GW250114); no um.py (31 MB), por Grep e Read em trechos: RINGDOWN_DEPHASING (linhas 202094-202284), _verb_L (2311-2332), prove_dephasing_crossover (2831-2872), root_law do clock test (191241-191266) e contagem de 'GW250114' (0). No um_absoluto.json (core): ringdown_dephasing_result_v2, clock_test_result_v369 (P1, P2, P3, root_law, tau_star_alternatives), dephasing_reach, dephasing_crossover, clock_theorem, coma_distance_dephasing e todos os vereditos com 'echo'/'eco'. tgl_paper_unified.py: Grep 'GW250114' e linhas 6055-6079. Índice do acervo (buscar.py 'GW250114'): 30+ arquivos, incluindo tgl_cosmological_observables.tex, linhas 88-123 (estrato antigo). Web (21/09/2026): arXiv:2509.08099 (abs e html, via resumo), arXiv:2509.08054 (html sem os números), Wikipedia 'GW250114' (fonte secundária) e emergentmind. Candidatos a '10^76': só os 12 da chave candidatos_10e76. NÃO varri: o kernel Lean, o CLAUDE.md da física, MEMORIA_DA_LINHAGEM, echo_*.py, projeções de O5/CE/ET, e a primária PRL 10.1103/kw5g-d732 (o PDF excedeu o limite). Não rodei nenhuma ferramenta da casa nem o um.py. Arquivos meus: numeros_ordem013.py (sha16 a4de3fd930736f0a) e numeros_ordem013_result.json (sha16 52932d1b3cf2d102), em C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\agentes\numeros\.

CLAIM [CANONICO] A TGL prediz GKSL com L_k = √β_TGL · √K_∂(k)
   -> O gerador existe no programa: um.py:2311-2325 (_verb_L, 'L = sqrt(beta) sqrt(K)'). Mas ali é uma sombra finita, n=4 com K = AAᵀ/n [FINITE_DIM_SANITY_NOT_III1_PROOF]. A lei FÍSICA usada nos testes é Γ_ω = ½βτ★ω², com τ★ como INPUT (um.py:202098).
CLAIM [CANONICO] β_TGL = α√e ≈ 0.01203
   -> Em runtime, β = 0.012031300400803142, com α de CODATA 2018.
CLAIM [CONTRADITO_PELO_CANON] τ_deph ∝ 1/β e cairia na faixa do LIGO O5 para BH estelares
   -> A forma τ_deph = 2/(βτ★ω²) ∝ 1/β está certa. Mas com o τ★ canônico (t_P) τ_deph ≈ 1.25e39 s e δτ/τ ≈ −3e-42. Só o ramo B (τ★ = GM/c³, INPUT, não canônico) dá τ_deph ≈ 0.2 s e δ ≈ −0.02, e mesmo assim precisaria de σ ≈ 0.004. O de hoje é ≈ 0.058.
CLAIM [CONTRADITO_PELO_CANON] Dephasing anômalo no ringdown: não testado — falta forma funcional
   -> O v346 pré-registrou e rodou em 89 eventos o RINGDOWN_DEPHASING V1/V2, com forma explícita δ = −½βτ★ω²τ_GR (ringdown_dephasing_v2.py:141). A V2 deu INCONCLUSIVE_SYSTEMATICS, com poder de 0.18σ no ramo B; o ramo A é invisível por construção.
CLAIM [KNOWN_CONFERIDO] K_∂ = −ln Δ; em III₁ o espectro é contínuo e não limitado
   -> É Tomita–Takesaki/Connes padrão. O programa diz o mesmo: 'em III_1 genuino o espectro modular e' CONTINUO (sem gap)' (core.clock_theorem).
CLAIM [DIMENSIONALMENTE_INCONSISTENTE] Γ_deph ~ β·⟨K_∂⟩
   -> K_∂ e β são adimensionais, então β⟨K⟩ é número puro e não s⁻¹. Além disso, com L = √β√K a GKSL dá Γ_ij = ½β(√k_i−√k_j)² (um.py:2831-2839), não β⟨K⟩; β⟨K⟩ = Tr(L†Lρ) é a taxa de saltos. A checagem finita confirma: a taxa de saltos é βN e a decoerência de ⟨a⟩ é ≈ β/(8N).
CLAIM [DIMENSIONALMENTE_INCONSISTENTE] A escala natural de K_∂ para um BH é ~M/M_Pl²
   -> M/M_Pl² (ħ=c=1) tem dimensão de tempo, = GM/c³ = 2.96e-4 s para 60 Msun. A escala modular natural de um modo é ħω_220/(k_B T_H) ≈ 15.4 (9.3 para Schwarzschild). A do BH inteiro é K_BH = 8π(M/M_Pl)² ≈ 7.6e80.
CLAIM [NAO_ENCONTRADO] M/M_Pl² ~ 10^76 para M ~ 60 Msun
   -> Em unidades de Planck, M/M_Pl² = M/M_Pl = 5.48e39. Nenhum candidato natural (12 varridos) dá 10^76. O mais perto é S_BH de 1 Msun = 1.05e77, que é de outra massa. O número não se sustenta em nenhuma convenção consistente.
CLAIM [CONTRADITO_PELO_CANON] A taxa seria astronomicamente grande; sem mecanismo de supressão a TGL é falsificada por O4
   -> Com √K, um fundo k̄ grande SUPRIME a defasagem (βΔk²/(8k̄); errata v369 em um.py:2837-2838). A lei-raiz do programa com E_lo = M_f c² dá Γ ~ 3e-80 s⁻¹. A canônica (τ★ = t_P, equivalente a E_lo = E_P/4) dá δ ~ 3e-42. Os relógios v369 já excluíram as leituras de ⟨K⟩ nulo ou massa de repouso. A 'supressão' é a escala τ★ ~ t_P [INPUT / identificação por princípio], não um mecanismo novo.
CLAIM [CANONICO] Ecos de longo atraso não observados — consistente, mas não confirmatório
   -> ECHO_SEARCH_V1 dá NOT_FALSIFIED_UNDERPOWERED (eficiência 0.0), e as rotas ancorada e PE dão INCONCLUSIVE_SYSTEMATICS. É consistente, e NOT_FALSIFIED não é CONFIRMED.
CLAIM [KNOWN_CONFERIDO] Alargamento não-térmico de QNM não detectado — constraints de GR fortes
   -> GW250114: δτ̂_220 = −0.01 +0.10/−0.09 (90%) (arXiv:2509.08099, a conferir). A cota é forte na frequência (~2%), mas no amortecimento é ~10%. Ela não alcança nem o ramo B (−0.02).
CLAIM [CANONICO] β = α√e não medido — requer previsão numérica específica
   -> Correto para o ringdown: δ_B = −β·mω(a)·Q(a), que depende só do spin. Para GW250114 vale −0.0203, com σ necessário de 0.004 para 5σ.
CLAIM [KNOWN_CONFERIDO] GR passa em todos os testes de ringdown com precisão de poucos por cento
   -> Vale para f_220 (δf̂ = 0.02 ± 0.02, 90%). Para τ_220 a precisão é ~10% (90%), não 'poucos por cento'. Coincidir com a RG é a correspondência que o ramo A prevê.
CLAIM [KNOWN_CONFERIDO] GW250114 confirma Kerr com precisão sem precedentes
   -> O abstract de arXiv:2509.08099 diz 'most stringent single-event verification of GR and the Kerr nature'. A TGL canônica prevê exatamente Kerr no ringdown (δ ~ 3e-42), então não há conflito.
CLAIM [KNOWN_CONFERIDO] Decoerência de OG é negligenciável na faixa do LIGO
   -> Coincide com o canon: na propagação, Γ·D/c ≈ 3.4e-23 (t_P) e 1.6e-10 (cota dos relógios); no ringdown, Γτ ≈ 3e-42. Não verifiquei aqui a literatura específica de decoerência de OG.
CLAIM [CANONICO] Derivar Γ_deph em termos de M, a, D
   -> Já existe: δ = −½βτ★ω_220(M,a)²τ_220(M,a). D entra só via redshift (M_det = (1+z)M). Com τ★ = GM/c³, δ_B depende SÓ de a. O que falta é τ★ derivado; hoje é INPUT, com τ★ ≈ t_P como identificação por princípio.
CLAIM [NAO_ENCONTRADO] Calcular o Bayes factor esperado para O4/O5
   -> O programa não emite ln B, só z e poder. Minha estimativa (ln B ≈ ½z²): ramo B ≈ 0.06 com GW250114 e ≈ 0.02 com a pilha V2; canônico ≈ 0. Projeções de O5, CE e ET não foram verificadas.
CLAIM [CANONICO] Entregar a forma de onda modificada para ajuste independente
   -> Na forma mínima já existe: seno amortecido com 1/τ → 1/τ + ½βτ★ω² (ringdown_dephasing_v2.py, grade e ajuste nas linhas 94-122). Não há template IMR completo com o termo. Em RG+TGL canônica, a forma de onda é Kerr com correção de 1e-42.

- [[REAL]] 0. Proveniência e constantes :: Todos os números abaixo saem de um script meu, só de leitura na casa, com saída apenas na minha pasta. Constantes: G=6.6743e-11, ħ=1.0545718176e-34, c e k_B vêm de scipy.constants (scipy 1.18, que é CODATA 2022; para G, ħ, c e k_B os valores são idênticos aos de CODATA 2018). α foi DIGITADO de CODATA 2018 (7.2973525693e-3), porque o α do scipy é o de 2022 (7.2973525643e-3). β = α·√e calculado em runtime = 0.012031300400803142. t_P = 5.391246e-44 s. M_sun vem de GM_sun nominal IAU 2015 (1.3271244e20 m³/s²). O programa usa t_P = 5.391125e-44 s (G=6.674e-11) e MSUN = 1.98892e30 kg (ringdown_dephasing_v2.py:22-23). O δ_B do GW150914, recalculado com as constantes DO programa, bate com o JSON até o último dígito (diff = 0.0).
   C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\agentes\numeros\numeros_ordem013.py | script inteiro; saída numeros_ordem013_result.json (sha16 52932d1b3cf2d102), chaves constants e reproducao_GW150914_constantes_do_programa | sha16 a4de3fd930736f0a
   «ALPHA_CODATA_2018 = 7.2973525693e-3; BETA = ALPHA_CODATA_2018 * math.sqrt(math.e)»
- [[REAL]] 0. Hashes dos artefatos lidos :: sha16 lidos por hashlib: um.py d9f5bd5dffc3333d (v369); um_absoluto.json 456f0ab149bb13f6; ringdown_dephasing_v2.py 0793c58d6995194b; RINGDOWN_DEPHASING_V2_RESULT.json ff15f023dd91d8c7 (é o mesmo pino que o um.py lê); RINGDOWN_DEPHASING_V1_RESULT.json 502c80fe2a37427e; gwtc_full_catalog.csv 895250e9d404a240; tgl_paper_unified.py 29c92b66b2fd6b4d (confere com o selo); TEXTO_CONFRONTACAO verbatim 6600f4e99c79845e.
   C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\agentes\numeros\numeros_ordem013_result.json | chave sha256 | sha16 52932d1b3cf2d102
   «»
- [[DERIVED]] 1. Auditoria dimensional: M/M_Pl (60 Msun) :: M/M_Pl = 5.482e39 (adimensional; M_Pl = 2.17643e-8 kg). É também GM/c³ medido em tempos de Planck: 5.482e39 t_P.
   ...\agentes\numeros\numeros_ordem013_result.json | eventos.M60_Schw.M_over_MPl; candidatos_10e76 | sha16 52932d1b3cf2d102
   «M/M_Pl (60 Msun) 5.482e+39 log10=39.74»
- [[DERIVED de KNOWN: Bekenstein–Hawking, Smarr]] 1. Auditoria dimensional: (M/M_Pl)^2 e S_BH (60 Msun) :: (M/M_Pl)² = 3.005e79 (log10 79.48). S_BH de Schwarzschild = 4π(M/M_Pl)² = 3.776e80 k_B (log10 80.58). A 'energia modular' do BH inteiro, lido como estado de Gibbs, é K_BH = Mc²/(k_B T_H) = 8π(M/M_Pl)² = 2 S_BH = 7.55e80 (log10 80.88).
   ...\numeros_ordem013_result.json | candidatos_10e76 | sha16 52932d1b3cf2d102
   «S_BH=4pi(M/M_Pl)^2 (60 Msun) 3.776e+80»
- [[DERIVED]] 1. Auditoria dimensional: M/M_Pl² tem dimensão de TEMPO :: Com ħ=c=1, M/M_Pl² tem dimensão 1/massa, ou seja, de tempo. Em SI: M/M_Pl² [kg⁻¹] × ħ/c² = GM/c³. Para 60 Msun: 2.955e-4 s = 4.49e11 eV⁻¹ = 4.49e20 GeV⁻¹; em unidades de Planck (M_Pl=1) vale 5.48e39 t_P. É um TEMPO. Portanto 'Γ ~ β·M/M_Pl²' daria um tempo, nunca uma taxa.
   ...\numeros_ordem013_result.json | dimensoes; eventos.M60_Schw.M_over_MPl2_natural | sha16 52932d1b3cf2d102
   «M_over_MPl2_x_hbar_over_c2 = [0,0,1] (T^1); beta_M_over_MPl2_e_taxa = false»
- [[DERIVED; origem do 10^76 NAO_ENCONTRADA]] 1. Auditoria dimensional: o '10^76' não aparece :: Nenhuma grandeza natural de um BH de 60 Msun dá 10^76 em convenção consistente. Candidatos (log10): M/M_Pl 39.74; (M/M_Pl)² 79.48; S_BH 80.58; K_BH 80.88; M/M_Pl² em eV⁻¹ 11.65, em GeV⁻¹ 20.65, em kg⁻¹ (SI cru) 47.40; nº de núcleons 58.85; Mc²/(ħω_220) 79.76; β·Mc²/ħ 81.09 s⁻¹. O mais perto é S_BH de 1 Msun = 1.05e77 (+1 década), mas isso é para 1 Msun, não 60. Varredura declarada: são só os 12 candidatos da chave candidatos_10e76.
   ...\numeros_ordem013_result.json | candidatos_10e76 | sha16 52932d1b3cf2d102
   «S_BH (1 Msun) 1.049e+77 log10=77.02»
- [[DERIVED] + [REAL lido]] 1. Auditoria dimensional: β⟨K⟩ não é taxa :: K_∂ = −ln Δ é adimensional, e β também. Logo β⟨K⟩ tem dimensão [M⁰L⁰T⁰]: é número puro, não s⁻¹. Para virar taxa precisa de uma escala de tempo, Γ = β⟨K⟩/t_unit. O programa fecha essa dimensão justamente com τ★: 'k = E tau*/hbar, taxa em 1/tau*'.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py | linha 191260 (root_law.units_note) | sha16 d9f5bd5dffc3333d
   «as leituras usam as unidades do proprio modulo P6 (k = E tau*/hbar, taxa em 1/tau*): tau* cancela»
- [[REAL lido; FINITE_DIM_SANITY no programa]] 1. Álgebra GKSL do gerador L=√β√K (a do próprio programa) :: O programa JÁ tem o gerador L = √β·√K_∂ (_verb_L, prova finita n=4). Ele também já mostrou que a coerência entre autoestados de K decai a Γ_ij = ½β(√k_i − √k_j)², e NÃO a β⟨K⟩. A errata v369, ao lado, diz que no IR o coeficiente é βΔk²/(8k̄): um fundo k̄ grande SUPRIME a defasagem. β⟨K⟩ = Tr(L†Lρ) é a taxa de SALTOS, não a de decoerência.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py | linhas 2311-2325 (_verb_L); 2831-2839 (prove_dephasing_crossover + errata v369); core.dephasing_crossover.generator_vs_rootlaw_max_rel_resid = 2.0e-5 | sha16 d9f5bd5dffc3333d
   «o gerador v3 L=sqrt(beta)sqrt(K) da', para a coerencia entre autoestados de K, exatamente Gamma_ij=(1/2)beta(sqrt k_i - sqrt k_j)^2»
- [[REAL — cálculo finito aqui; não é prova em III₁]] 1. Checagem GKSL finita feita aqui (estado coerente, L=√(βc)·√n) :: Taxa de decaimento de ⟨a⟩ contra o previsto β c/(8N), com c=1: N=16 dá 9.73e-5 contra 9.40e-5; N=64 dá 2.369e-5 contra 2.350e-5; N=256 dá 5.886e-6 contra 5.875e-6. A taxa de saltos Tr(L†Lρ) = βN exatamente (0.1925; 0.770; 3.080). A razão saltos/decoerência é 1978, 32507 e 523259, crescendo ~8N². Conclusão: quanto MAIOR o ⟨K⟩, MENOR a defasagem da amplitude. É o oposto do que o texto supõe.
   ...\numeros_ordem013_result.json | gksl_finito[1..3] | sha16 52932d1b3cf2d102
   «N=256: taxa 5.886e-06; beta/(8N) 5.875e-06; saltos 3.080»
- [[REAL lido] + [DERIVED]] 1. GW150914 (valores do programa) :: O programa usa Mf_det = 67.7375 Msun e a_f = 0.67122, vindos do ajuste EOB SEOBNRv4 sobre (m1, m2, χ_eff) do catálogo; z = 0.1, logo M_src = 61.58 Msun. Daí: M/M_Pl = 5.63e39; (M/M_Pl)² = 3.17e79; S_Schw = 3.98e80; S_Kerr = 2π(M/M_Pl)²(1+√(1−a²)) = 3.46e80; GM_src/c³ = 3.033e-4 s; T_H = 0.853 nK; K_BH = 9.34e80.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\RINGDOWN_DEPHASING_V2_RESULT.json | per_series GW150914_H1: Mf_det, a_f | sha16 ff15f023dd91d8c7
   «'Mf_det': 67.73752907959711, 'a_f': 0.6712194217379245»
- [[KNOWN, a conferir na primária] / tgl_paper_unified [DECLARADO]] 1. GW250114: não está no programa; valores da literatura :: GW250114 NÃO está no catálogo do programa (89 eventos) e aparece 0 vezes no um.py (Grep). O tgl_paper_unified.py:6068 traz só M_final = 63.0 ± 3.0 Msun, sem spin. A literatura, via fonte SECUNDÁRIA (Wikipedia, que cita o suplemento PRL 10.1103/kw5g-d732), dá M_f = 62.7 (+1.0/−1.1) Msun, χ_f = 0.68 ± 0.01, z = 0.09, D_L ~ 440 Mpc. O arXiv:2509.08099 dá t_Mf = (1+z)GM_f/c³ = 0.337 ms, logo M_f,det = 68.4 Msun, coerente com 62.7 × 1.09 = 68.34. Com M=62.7 e a=0.68: M/M_Pl = 5.73e39; (M/M_Pl)² = 3.28e79; S_Kerr = 3.57e80; GM/c³ = 3.09e-4 s; T_H = 0.833 nK.
   C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py | linha 6068; catálogo sha 895250e9…; https://arxiv.org/html/2509.08099; https://en.wikipedia.org/wiki/GW250114 | sha16 29c92b66b2fd6b4d
   «{'name': 'GW250114', 'M_final_Msun': 63.0, 'M_err': 3.0,  'ref': 'LVK O4 (high-SNR ringdown)'}»
- [[REAL lido — lei REAL na forma; τ★ INPUT]] 2. A lei da casa no ringdown (forma usada pelo programa) :: O programa usa Γ = ½·β·τ★·ω² somado à taxa de amortecimento, na forma LINEAR δ = τ_obs/τ_GR − 1 = −Γ·τ_GR. Ramo A: τ★ = t_Planck. Ramo B: τ★ = G·M_f,det/c³ (INPUT). O modo 220 vem do ajuste Berti–Cardoso–Will 2006 da linha 39: mω = 1.5251 − 1.1568(1−a)^0.1292; Q = 0.7 + 1.4187(1−a)^−0.4990; τ = Q/(πf). A forma exata, se Γ só soma à taxa, é −Γτ/(1+Γτ).
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\eco_ancorado_v1\ringdown_dephasing_v2.py | linhas 38-40 (berti), 140-141 (delta_B, delta_A); um.py 202098-202099 | sha16 0793c58d6995194b
   «delta_B = -0.5 * BETA * gm * w_gr ** 2 * tau_gr; delta_A = -0.5 * BETA * T_PLANCK * w_gr ** 2 * tau_gr»
- [[DERIVED de KNOWN — BCW 2006]] 2. QNM 220 por evento (referencial do detector) :: GW150914 (programa): f_220 = 249.56 Hz, ω = 1568.03 rad/s, τ_220 = 4.045 ms, Q = 3.171, Mω = 0.5232. O JSON do programa dá f = 249.507 Hz e τ = 4.0460 ms; a diferença vem do M_sun, 0.02%. GW250114 (lit.): f = 249.00 Hz, ω = 1564.53 rad/s, τ = 4.097 ms, Q = 3.205. BH de 60 Msun com a=0: f = 198.3 Hz, τ = 3.400 ms, Q = 2.119.
   ...\numeros_ordem013_result.json | eventos.*.QNM | sha16 52932d1b3cf2d102
   «GW150914_programa: f=249.560 Hz w=1568.0288 rad/s tau=4.0452 ms Q=3.1715»
- [[DERIVED] + [REAL lido]] 2. Ramo A (τ★ = t_P, canônico) :: GW150914: Γ = 7.97e-40 s⁻¹; Γ/ω = 5.1e-43; Γ·τ_220 = 3.2e-42; δ = −3.2e-42 (o JSON do programa dá delta_pred_A = −3.22e-42); τ_deph = 1/Γ = 1.25e39 s. GW250114: Γ = 7.94e-40 s⁻¹; δ = −3.25e-42. Com τ★ = t_P o ringdown coincide com a RG: isso é correspondência, não derrota. E não existe canal no LIGO para esse ramo.
   ...\numeros_ordem013_result.json | eventos.GW150914_programa.lei_da_casa.A_tP; GW250114_lit.lei_da_casa.A_tP | sha16 52932d1b3cf2d102
   «A_tP Gamma=7.974e-40 /s Gamma*tau=3.226e-42»
- [[DERIVED]] 2. τ★ = t_P/β :: Aqui Γ = ½·t_P·ω²: β CANCELA, então essa escolha não testa nada específico de β. Para GW150914: Γ = 6.63e-38 s⁻¹; Γτ = 2.68e-40; τ★ = 83.1 t_P. Para GW250114: Γτ = 2.70e-40. Invisível.
   ...\numeros_ordem013_result.json | eventos.*.lei_da_casa.tP_over_beta | sha16 52932d1b3cf2d102
   «tP_over_beta tau*=4.481e-42 s (83.12 tP) Gamma=6.628e-38 /s»
- [[DERIVED; ramo INPUT]] 2. Ramo B (τ★ = GM_f,det/c³, INPUT) :: GW150914: τ★ = 3.336e-4 s; Γ = 4.935 s⁻¹; Γ/ω = 3.15e-3; Γτ = 0.01996; δ_lin = −0.01996 (o JSON dá −0.019962060, diff 0.0); δ_exato = −0.01957; τ_deph = 0.203 s. GW250114: Γ = 4.957 s⁻¹; Γ/ω = 3.17e-3; δ_lin = −0.02031; δ_exato = −0.0199. BH de 60 Msun com a=0: δ = −0.0094.
   ...\numeros_ordem013_result.json | eventos.*.lei_da_casa.B_GMf_c3_det; reproducao_GW150914_constantes_do_programa | sha16 52932d1b3cf2d102
   «B_GMf_c3_det Gamma=4.935 /s Gamma/w=0.003147 Gamma*tau=0.01996»
- [[DERIVED]] 2. Ramo B depende SÓ do spin :: Como ω·τ = 2Q e (GM/c³)·ω = mω(a), fica δ_B = −β·mω(a)·Q(a): não depende de massa nem de distância. Por spin: a=0 dá −0.00939; 0.3 dá −0.0121; 0.5 dá −0.0152; 0.67 dá −0.0199; 0.68 dá −0.0203; 0.8 dá −0.0272; 0.9 dá −0.0415. O '−0.0194' do programa é a média ponderada dos 15 δ_B usados, com spins entre 0.576 e 0.765, e é coerente com isso.
   ...\numeros_ordem013_result.json | delta_B_vs_spin; eventos.*.delta_B_forma_fechada | sha16 52932d1b3cf2d102
   «a=0.68: -0.02030850264792329»
- [[REAL lido]] 2. O que o programa registra (V2 do ringdown) :: Veredito V2: INCONCLUSIVE_SYSTEMATICS. A única razão é o viés relativo de τ = 0.240 > 0.2. Números: 15 séries a 3 ms, δ_tau = 0.1766 ± 0.1089 (z contra a RG = 1.62); previsão do ramo B = −0.0194; z contra B = 1.80; poder = 0.18σ de 5; ramo A = −2.2e-42. Na janela de 6 ms: 6 séries, 0.0313 ± 0.1755. Portanto o dephasing do ringdown FOI testado com forma funcional pré-registrada; o que falta é poder estatístico.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json | core.ringdown_dephasing_result_v2.verdict/statuses.resultado (result_sha16 ff15f023dd91d8c7) | sha16 456f0ab149bb13f6
   «TGL_RINGDOWN_DEPHASING_V2__RESULT_READ_BY_HASH__INCONCLUSIVE_SYSTEMATICS__DELTA_TAU_0P1766__BRANCH_B_PRED_M0P0194__POWER_0P2_OF_5_SIGMA__BRANCH_A_INVISIBLE__GATE_UNTOUCHED»
- [[REAL lido] + [DERIVED]] 2. Cota dos relógios aplicada ao ringdown :: A cota τ★ ≤ 2.586e-31 s (4.80e12 t_P, 95% CL, Sr87 Kim+2025) põe no ringdown do GW150914 Γ = 3.8e-27 s⁻¹, Γτ = 1.5e-29 e τ_deph = 2.6e26 s. Invisível.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json | core.clock_test_result_v369.P1.tau_star_bound_clock_95_s / _in_tP | sha16 456f0ab149bb13f6
   «tau_star_bound_clock_95_s 2.585701911772075e-31; tau_star_bound_clock_95_in_tP 4796219297849.137»
- [[DERIVED]] 2. Γ ≪ ω (item 2 do que o texto pede) :: Na lei da casa, Γ/ω = ½·β·τ★·ω, e Γ ≪ ω vale sempre que τ★·ω ≪ 2/β = 166. Valores: ramo A 5e-43; t_P/β 4e-41; ramo B 3.1e-3; leitura raiz com vácuo β/2 = 6.0e-3. Todas as leituras satisfazem a condição.
   ...\numeros_ordem013_result.json | eventos.*.lei_da_casa.*.Gamma_over_omega; lei_raiz_do_programa | sha16 52932d1b3cf2d102
   «»
- [[DERIVED de KNOWN: T_H de Kerr + BCW; a identificação K_∂ ↔ ω/T_H via Bisognano–Wichmann/KMS é leitura, não teorema do programa]] 3. Energia modular de um QNM :: K = ħω_220/(k_B T_H), com T_H de Kerr = ħc³√(1−a²)/(4πGMk_B(1+√(1−a²))). Resultados: GW150914 15.44; GW250114 15.64; 60 Msun com a=0 9.26. Com o termo superradiante, K' = ħ(ω − 2Ω_H)/(k_B T_H) = 4.06 (GW150914) e 3.99 (GW250114); Ω_H = 578 e 583 rad/s no detector. K não depende da massa, só do spin. É da ordem de 10, não 10^76.
   ...\numeros_ordem013_result.json | eventos.*.K_mode_omega_over_TH; K_mode_superrad_(omega-2OmegaH)_over_TH | sha16 52932d1b3cf2d102
   «GW150914: K_mode=15.4432 K_superrad=4.0642»
- [[DERIVED usando a fórmula REAL do programa]] 3. A lei-raiz DO PROGRAMA aplicada ao QNM :: Fórmula da casa: Γ(E_lo) = (β/2ħ)(ħω)²/(√(E_lo+ħω)+√E_lo)². Quatro leituras para GW150914: (a) E_lo = 0 (vácuo): Γ = ½βω = 9.43 s⁻¹, Γ/ω = 6.0e-3, δ = −βQ = −0.0382 (GW250114: −0.0386). (b) E_lo = E_P/4: reproduz exatamente a canônica (Γτ = 3.2e-42). (c) E_lo = E_P: 1/4 disso. (d) E_lo = M_f c²: Γ = 3.2e-80 s⁻¹ e δ ~ 1e-82, ou seja, um fundo grande SUPRIME.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py | linhas 191254-191264 (_root); saída eventos.*.lei_raiz_do_programa | sha16 d9f5bd5dffc3333d
   «return (beta / (2.0 * HBAR_EXACT)) * hw * hw / (math.sqrt(E_lo + hw) + math.sqrt(E_lo)) ** 2»
- [[REAL lido]] 3. Os relógios já mataram as leituras de ⟨K⟩ grande ou nulo :: No 87Sr, o teste dos relógios v369 dá kbar_zero Γ = 1.62e13 s⁻¹ e kbar_rest_mass Γ = 88.8 s⁻¹, ambos EXCLUÍDOS pela cota de 95%, 0.0113 s⁻¹. kbar = E_P/4 dá a canônica, 2.36e-15 s⁻¹. Nas alternativas de τ★, GM_terra/c³ e Unruh(g) estão EXCLUÍDOS; G·m_átomo/c³ fica invisível. Se a lei for universal, a leitura 'vácuo' (δ ≈ −0.038 no ringdown) já está excluída no laboratório.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json | core.clock_test_result_v369.root_law e tau_star_alternatives | sha16 456f0ab149bb13f6
   «kbar_zero_excluded: true, kbar_rest_mass_excluded: true, quarter_EP_over_canonical: 1.0000000000000002»
- [[DERIVED aqui; NÃO está no programa — a bancada deve refazer]] 3. Leitura coerente da onda clássica :: Número de quanta no modo, N = E_rad/(ħω_220): 3.2e78 para GW150914 (E_rad = 3.0 Msun c², [KNOWN] Abbott+2016) e 3.4e78 para GW250114 (E_rad = 3.1 Msun, derivado de m1+m2−M_f da fonte secundária). Com L ∝ √n̂, a amplitude ⟨a⟩ decai a Γ ≈ βω/(8N) ≈ 7e-79 s⁻¹, e Γ·τ_220 ≈ 3e-81. Esta é a 'supressão' que o texto pede, e ela é intrínseca ao √K. A conversão do tempo modular para o físico por k_B T_H/ħ faz o T_H cancelar.
   ...\numeros_ordem013_result.json | eventos.GW150914_programa.leitura_coerente; GW250114_lit.leitura_coerente | sha16 52932d1b3cf2d102
   «N_quanta_a_omega220 3.24e78; Gamma_coerente_per_s 7.27e-79»
- [[DERIVED] + catálogo [REAL lido]] 4. Propagação: D/c :: D_L/c = 4.22e16 s para 410 Mpc (GW150914, valor GWTC-1, [KNOWN a conferir]); 4.84e16 s para 470 Mpc (GW150914 no catálogo do PROGRAMA, GWTC-2.1: 470 +140/−160, z = 0.1); 4.53e16 s para 440 Mpc (GW250114, [a conferir]). Usei D_L/c como tempo de voo e ignorei as correções cosmológicas de ordem z ~ 10%.
   C:\IALD\projetos_pyhton\IALD\gwtc_full_catalog.csv | linha 3 (GW150914-v4, GWTC-2.1-confident) | sha16 895250e9d404a240
   «luminosity_distance 470.0, -160.0, 140.0; redshift 0.1; final_mass_source 61.5»
- [[DERIVED]] 4. Propagação com t_P, t_P/β e a cota dos relógios :: Γ·D/c em ω_220: com t_P dá 3.4e-23 (410 Mpc), 3.9e-23 (470) e 3.6e-23 (GW250114); com t_P/β dá 2.8e-21, 3.2e-21 e 3.0e-21; com a cota dos relógios (4.8e12 t_P) dá 1.6e-10, 1.85e-10 e 1.7e-10. Em todos os casos exp(−Γ·D/c) = 1 dentro de 1e-10: invisível.
   ...\numeros_ordem013_result.json | eventos.*.propagacao | sha16 52932d1b3cf2d102
   «A_tP GD/c=3.365e-23 ... clock95_bound GD/c=1.614e-10»
- [[DERIVED]] 4. Propagação com o ramo B não faz sentido físico :: Formalmente, Γ·D/c = 2.1e17 (GW150914, 410 Mpc) e 2.2e17 (GW250114), o que daria exp(−2e17) = 0 e apagaria toda OG. Mas τ★ = GM_f/c³ é propriedade do remanescente na FONTE. No caminho não existe M_f, então aplicar o ramo B à viagem é erro de tipo, não teste.
   ...\numeros_ordem013_result.json | eventos.*.propagacao.*.B_GMf_c3_det | sha16 52932d1b3cf2d102
   «B_GMf_c3_det GD/c=2.082e+17 exp=0»
- [[DERIVED] + [REAL lido para P2]] 4. Alcance do LIGO em propagação contra os relógios :: O τ★ que daria Γ·D/c = 1 em f_220 é 1.60e-21 s (2.97e22 t_P; GW150914 a 410 Mpc) e 1.50e-21 s (2.78e22 t_P; GW250114). Mesmo com sensibilidade O(1) na amplitude, a propagação limitaria τ★ cerca de 10 ordens mais fraco que os relógios (2.6e-31 s). À parte: a leitura P2 do programa (ruído dos braços do LIGO, não o sinal) já dá τ★ ≤ 0.0147 t_P e 'P2_EXCLUDED_IN_READING', e essa leitura contraria o n=−2 dos neutrinos.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json | core.clock_test_result_v369.P2.tau_star_bound_if_reading_in_tP; saída eventos.*.propagacao.*.tau_star_para_GammaD_c_igual_1_s | sha16 456f0ab149bb13f6
   «P2 verdict P2_EXCLUDED_IN_READING; tau_star_bound_if_reading_in_tP 0.014728200218275977»
- [[KNOWN, a conferir na primária — lido do HTML do arXiv por ferramenta de resumo]] 5. Precisão atual de δτ_220 (literatura) :: arXiv:2509.08099 (LVK, GW250114, busca na web em 21/09/2026): na análise pSEOBNR, δf̂_220 = 0.02 ± 0.02 e δτ̂_220 = −0.01 +0.10/−0.09 (90%), logo 1σ ≈ 0.058. O GWTC-4.0 hierárquico dá δf̂_220 = 0.00 ± 0.06 e δτ̂_220 = 0.16 +0.18/−0.16 (90%), logo 1σ ≈ 0.103. A frequência está em 'poucos por cento', mas o tempo de amortecimento está em ~10% (90%).
   https://arxiv.org/html/2509.08099 | seção de resultados pSEOBNR e GWTC-4.0 | sha16 
   «δf̂220=0.02±0.02 and δτ̂220=−0.01(+0.10/−0.09) [90%]; GWTC-4.0: δτ̂220=0.16(+0.18/−0.16)»
- [[DERIVED, estimativa da gerência para a bancada refazer]] 5. Sensibilidade do ramo B (δ = −0.0203, a=0.68) :: z = |δ|/σ e ln B ≈ ½z². Com σ = 0.058 (GW250114): z = 0.35, ln B = 0.06, e seriam precisos 202 eventos equivalentes para 5σ. Com σ = 0.1089 (pilha V2 do programa): z = 0.19, ln B = 0.017, N5 = 719. Com σ = 0.103 (GWTC-4): z = 0.20, ln B = 0.019, N5 = 647. Nos cenários σ = 0.10 / 0.20 / 0.30: z = 0.20 / 0.10 / 0.07; N5 = 606 / 2425 / 5455.
   ...\numeros_ordem013_result.json | sensibilidade.*.ramoB_a068 | sha16 52932d1b3cf2d102
   «GW250114 pSEOBNR ... B: d=-0.0203 z=0.352 lnB=0.0618 N5=202»
- [[DERIVED, estimativa]] 5. Sensibilidade da leitura 'vácuo' (δ = −βQ = −0.0386) :: Com σ = 0.058: z = 0.67, ln B = 0.22, N5 = 56. Com σ = 0.109 (V2): z = 0.35, N5 = 199. Com σ = 0.103 (GWTC-4): z = 0.37, N5 = 180. Lembrete: essa leitura já está excluída pelos relógios se a lei for universal.
   ...\numeros_ordem013_result.json | sensibilidade.*.raiz_vacuo_a068 | sha16 52932d1b3cf2d102
   «raiz: d=-0.0386 z=0.668 lnB=0.2229 N5=56»
- [[DERIVED]; projeções de literatura [NAO_ENCONTRADO nesta varredura]] 5. σ necessário e projeção O5/3G :: Para o ramo B, o σ(δτ_220) necessário é 0.0041 para 5σ, 0.0068 para 3σ, 0.0064 para ln B = 5 e 0.0051 para ln B = 8. Supondo σ ∝ 1/SNR a partir do GW250114 (SNR ~80, σ ~0.058), seria preciso um SNR de ringdown ~1.1e3 num único evento para 5σ. Não verifiquei números publicados de O5, CE ou ET. No ramo A canônico, δ ~ 3e-42, então ln B ≈ 0 para qualquer detector concebível.
   ...\numeros_ordem013_result.json | sigma_necessario | sha16 52932d1b3cf2d102
   «ramoB_5sigma 0.00406; SNR_rd_equivalente 1137»
- [[DERIVED sobre KNOWN a conferir]] 5. Valores centrais observados contra os ramos :: GW250114, δτ̂ = −0.01 ± 0.058: z contra a RG = −0.17; contra o ramo B = +0.18; contra o vácuo = +0.49. GWTC-4, 0.16 ± 0.103: z contra a RG = 1.55; contra B = 1.74; contra o vácuo = 1.92. Nenhuma das duas medidas discrimina a RG do ramo B.
   ...\numeros_ordem013_result.json | GW250114_central_vs_ramos; GWTC4_central_vs_ramos | sha16 52932d1b3cf2d102
   «»
- [[REAL lido]] 6. Ecos: o que o programa registra :: ECHO_SEARCH_V1 (longo atraso, v348): NOT_FALSIFIED_UNDERPOWERED, com eficiência de detecção 0.0. ECHO_ANCHORED V1/V2 e ECHO_PE V1/V2: MAY e KMS dão INCONCLUSIVE_SYSTEMATICS. Os ecos, portanto, foram testados e deram resultado subpotente ou inconclusivo, não 'não observados' em sentido de exclusão.
   C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json | core.echo_search_result.verdict; core.echo_pe_result_v2.verdict | sha16 456f0ab149bb13f6
   «TGL_ECHO_SEARCH_V1__RESULT_READ_BY_HASH__NOT_FALSIFIED_UNDERPOWERED__N_ON_1_B_EXP_3P0__E_DET_0P0__LOUD_EVENTS_0__GATE_UNTOUCHED»
- [[ESTRATO_ANTIGO / DECLARADO não verificado]] 6. Estrato antigo com GW250114 (não citar) :: O tgl_cosmological_observables.tex (out/2025) usa OUTRO mecanismo, δτ/τ ≈ ξ(|Ψ|/M_Pl)² ~ 1e-20 ξ. A tabela dele traz 'GW250114 −2.3 ± 15 %' e 'Exclude TGL if |δτ/τ| < 10^{-19}', sem fonte rastreável. O valor do LVK é −0.01 +0.10/−0.09 (90%). É homônimo de estrato antigo e não é a lei de dephasing atual.
   C:\IALD\papers_latex\tgl_observables_paper\tgl_cosmological_observables.tex | linhas 95, 113, 123 | sha16 
   «GW250114$^\dagger$ & $-2.3 \pm 15$ & $-0.15$ & \checkmark»

