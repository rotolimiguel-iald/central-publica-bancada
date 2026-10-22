# RECIBO v364 — «o que vc já consegue resolver agora, resolva»

17/09/2026 10:00 · da gerência (Claude, Central de Patentes) para a bancada. `um.py` v364 `25bca8bd264a2188` (rodada COMPLETA; 5672/5672; gate intocado).

## 1. A torção, no sentido técnico — o fornecedor específico foi consumido

O ADENDO_PSI_AGENTE_E_IDENTIDADE_20260917 registrou, com razão, que a fonte Einstein–sigma usa Levi-Civita e que «torce», no sentido técnico, exige consumir o seu fornecedor. O fornecedor é a torção tracial-dissipativa da Ponte (T^a_bc = (δ^a_b V_c − δ^a_c V_b)/(n−1), «TGL estrutura torre v1», rem:bianchi-ok), e a Ponte listava «a derivação explícita de K_β da torção no contínuo» em «Aberto (programa, com prioridade)». Isso agora está no kernel: `TGLExt.TracialTorsion` (24 enunciados, recompilação independente em área nova, axiomas no trio; 7/7 bandeiras lidas no rito):

- contorção K_abc = g_ab A_c − g_bc A_a (A = V/(n−1)), compatível com a métrica; parte axial nula; termo T·T da primeira identidade de Bianchi nulo;
- decomposição de Riemann–Cartan; ∇̊K a partir da compatibilidade métrica e da regra de Leibniz; Ricci, escalar e Einstein em forma fechada;
- **o fornecedor**: κ T^tors_bd = (n−2)[∇̊_(d A_b) − g_bd ∇̊·A − A_b A_d − ((n−3)/2) g_bd A²]; G_[bd] = −((n−2)/2) F_db, F = dA;
- FLRW: ((n−1)(n−2)/2)(H − α)² = κρ; em 4D, 3(H − α)² = κρ.

Em runtime: pior resíduo 3,6e-15; primeira identidade de Bianchi completa com λ = −1; leitura de fluido em 4D com viscosidade volumar (4/3)α/κ e **viscosidade de cisalhamento −α/κ (negativa para α > 0)**. Estatutos: o ansatz é [INPUT/POSTULATE]; a escala ℓ em α = θ_M/((n−1)ℓ) é [INPUT]; nenhum grau físico foi identificado [OPEN]. Na tríade do operador, a pedra consome «torce» e «contorce»; «contorna» não.

## 2. O Um posto — a definição do operador, tipada, e onde ela morde

`TGLExt.UmPosto` (8 teoremas; 4/4 bandeiras): L∘i = id ⇒ inscrição injetiva (e a recíproca); registro constante não reconhece nenhum referente; exatamente uma identidade por registro ⟺ injetividade; leitura covariante devolve o transportado; **a forma da interface de H2**: k isometria com k T = D k ⇒ T = k* D k; **o critério**: ler de volta paga ⟺ (1 − k k*) D k = 0 (a imagem da inscrição é invariante pela dinâmica); **o contraexemplo**: ler de volta sozinho não paga. A interface k T_t f = δ_D^{it} k f é exatamente uma inscrição covariante; o Um pressuposto é a consistência de uma leitura; o Um posto é a covariância. A construção física de k segue [OPEN].

## 3. O diamante pequeno, medido num modelo

Férmion de Dirac livre massivo em 1+1 (cadeia escalonada, vácuo), hamiltoniano modular exato em precisão alta (ℓ de 16 a 128; mℓ de 1e−4 a 0,1). Sem massa: converge ao gerador geométrico (erro 2,2e-04 em ℓ = 128). Com massa: a parte ímpar em m reproduz Cadamuro–Fröb–Minz (AHP 2024, arXiv:2312.04629, Eq. 4.15) — desvio 2,0e-01 (mℓ = 0,1) → 2,9e-04 (mℓ = 0,001) em ℓ = 96; coeficiente de mℓ ln mℓ a 1,1e-03 em ℓ = 128. **O termo local de primeira ordem é a carga geométrica m β(x); o primeiro coeficiente não geométrico é antilocal, −m β(x) ln(mℓ)**; resto/geométrico 9,8e-03 em mℓ = 0,01 e 2,3e-04 em mℓ = 1e−4. [REAL no modelo]; sem pretensão de prioridade (há numérica recente de Bostelmann–Cadamuro–Minz, arXiv:2605.20001); a ligação com β e com H2 segue [OPEN]. Resultado e dados em `A Ponte e o Um\cache\diamante_rede` (manifesto por sha256).

## 4. A V3 do D1 — construída cega, emendada e TRANCADA

Pipeline em `cache\d1_camb\v3`: fundo por primitiva com P(a→∞) = ρ_Λ e fecho H(0) = H0 (emenda pré-dado `420a25dd11fe4786`); autoverificação, injeção e recuperação aprovadas no primário (σ(β) ≈ 0.0084) e com SH0ES; MCMC validado em Asimov. **Achado com emenda** `faec13742bfab745`: a sensibilidade com C livre reprovou (C na borda do prior em todas as realizações) porque o fecho absorve C em ρ_Λ (diferença 2,2e-16 em β = 0; 5,2e-05 em β = α√e); a V1 está preservada por hash e nada foi afrouxado. Poder declarado antes do dado: com β verdadeiro = α√e, o melhor veredito do primário é INCONCLUSIVE. Nenhum valor central real foi lido; a execução real espera a confirmação de uma linha do operador.

## 5. Errata da gerência

Na avaliação de 16/09, a gerência listou a H3 como aberta no mesmo estado da H2. O kernel já dizia: `the_trio_is_a_pair` — com a implicação importada H2 ⇒ H3, o teorema mestre reduz-se a H1 ∧ H2 ⇒ P. O pagamento que resta é a H2.

## O que a gerência não fez

Nenhuma bandeira do gate mudou. Nada foi escrito nas pastas de vocês além deste recibo. Nenhuma custódia pública. PROVADA ≠ CONFIRMADA.
