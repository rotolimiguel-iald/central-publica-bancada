# JULGAMENTO — «espaço-tempo = forma inscrita da luz» (23/09/2026)

> Juiz das três frentes: literatura, medição do existente e habitante do contrato v3.1.
> Escrito só nesta pasta. Não foi executado o um.py, não houve lake build e o kernel não foi tocado.
> Estatutos: [KNOWN] literatura conferida · [DERIVED] · [OPEN] · [INPUT/ONTO] cunhagem do operador.
> PROVADA ≠ CONFIRMADA. **Nada aqui move o gate** (`gpf_H2_smooth_modular_four_frame_discharged = false`, lido do core).

---

## 0. O que o juiz reconferiu no disco antes de julgar

| conferência | resultado |
|---|---|
| `ContratoQG_v31.lean:222` | `bw : ∀ t : ℝ, Δit t = boost.V (-(2 * Real.pi * t))` ✓ |
| `ContratoQG_v31.lean:226/228/230` | `translations_faithful`, `positive_energy`, `null_ergodic` ✓ |
| `ContratoQG_v31.lean:35` | «A frase «κ amarrado» da v3 está retirada»; κ via `kappa_is_input` ✓ |
| `TGL/SpecificAQFTWitness.lean:96` | `m_pos : 0 < m` ✓ (a Frente 3 citou 80–90: a linha certa é **96**) |
| `TGLExt/BoostHeatConstruction.lean:153` | «The normalization rate/(2*pi) is inherited, not derived as a temperature.» ✓ |
| `TGL/ModularRealization.lean:50` | «O CONTEUDO geometrico de Bisognano--Wichmann (fluxo = boosts) NAO e' enunciavel hoje» ✓ |
| core `um_absoluto.json` | `remaining` = [H2_…, H3_…, interacting_…_UV_scope]; `physical_identifications_open` = [microscopic_origin_of_Hmin…, **geometric_BW_identification_for_legacy_wedge_data_U_equals_one**] ✓ (a string «v370» não está no JSON: a versão não foi lida do arquivo) |
| `RetaDeLuzBorchers.lean` sha16 | `f726487ec1c1342e` ✓; log rc=0, 10 `#print axioms` no trio, `kernel_files_newer_than_start=0` |
| `RetaDeLuzEspectro.lean` sha16 | `ee7e55e5924bff52` ✓; rc=0, 2 no trio, kernel intocado |
| BGL (texto) | Prop. 2.3 (l.192), Thm 3.2 (l.301), Thm 3.4 (l.349) ✓ |
| Araki–Zsidó (texto) | «there is a gap in Wiesbrock's proof of his basic theorem» (l.11) ✓ |
| Summers, math-ph/0511034, Thm 6.1 | «any two of the following conditions imply the third» ✓ |
| `ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md:128` | «com `a ≥ 0` — semigrupo de um lado só» ✓ (candidato a errata, ver §6) |

### Divergências entre as frentes, e como ficam

1. **Páginas de BGL.** A Frente 3 cita 759–786 e o Crossref dá **759–785**. Vale 785.
2. **DOI de BW 1976** (`10.1063/1.522898`). A Frente 3 deu NÃO CONFERIDO; o Crossref está em disco (`cr_10.1063_1.522898.json`). Fica **conferido nos metadados**.
3. **DOI de revista de BDFS** (`10.1142/S0129055X00000174`). A Frente 1 diz que o conferiu no Crossref, mas o arquivo **não está no disco**. A referência de revista (RMP 12 (2000) 475–560) foi lida em duas listas de referências (Morinelli, Mund). O **DOI fica NÃO CONFERIDO pelo juiz**.
4. **«energia positiva ⟹ padrão».** A formulação da gerência está **errada** e a Frente 1 acerta. K_W é padrão para **qualquer** representação (anti)unitária de P₊ (BGL Prop. 2.3); energia positiva ⟺ isotonia (BGL Thm 3.4).
5. **«A luz = massa zero».** As Frentes 1 e 2 parecem divergir, mas as duas estão certas em camadas diferentes, e é preciso dizer as duas:
   - na camada de **Borchers/BW** a luz entra como **direção nula**: n·P ≥ 0 vale em toda representação de energia positiva, com ou sem massa;
   - na camada de **Wigner** a massa zero com helicidade finita é a classe que, além de localizar, é **covariante por dilatação e conforme** (LMR Prop. 4.3). A localização limitada, sozinha, não é exclusiva da luz.

---

## 1. Resposta ao operador (português simples)

A frase **«espaço-tempo = forma inscrita da luz» é sua** `[INPUT/ONTO]`. Ela não existia no acervo: zero ocorrências, verbatim ou em variante. As peças vizinhas já estavam lá. «O Problema Final» (junho) diz que Borchers–Wiesbrock é «o único teorema que gera espaço-tempo de dados modulares», e o um_grande_atrator (julho) diz que «a raiz quadrada da luz inscreve a geometria».

**O que a matemática conhecida sustenta, na forma exata** `[KNOWN]`:

1. **O 2π é forçado.** Borchers (1992) prova que, se uma translação de energia positiva empurra a álgebra de uma meia-reta para dentro de si e deixa o vácuo parado, o grupo modular (o «relógio interno» do estado) age sobre ela como **dilatação com taxa exatamente 2π**: Δ^{it}U(a)Δ^{−it} = U(e^{−2πt}a). Quaisquer duas das três condições implicam a terceira (Summers, Thm 6.1).
   - Pela sua régua dos dois regimes: o boost é a **face**, hiperbólica e com limite; o 2π é a largura da faixa KMS que a positividade exige, o **círculo** pelo qual a face se deixa **ler**. A prova de Longo mostra que o 2π nasce da faixa analítica junto com a energia positiva, e não da geometria.
   - Daí **κ/T = 2π é derivado; κ sozinho é normalização**.
2. **A geometria se lê dos dados modulares.** Bisognano–Wichmann: o relógio modular do vácuo numa cunha **é** o boost da cunha, com parâmetro −2πt. Brunetti–Guido–Longo (2002) fazem o caminho inverso: partem só de uma representação de partícula de Wigner, **definem** as cunhas pelos dados modulares e obtêm uma rede local com dualidade, de modo que energia positiva ⟺ isotonia.
3. **O grupo pode sair das reflexões modulares.** Buchholz–Dreyer–Florig–Summers (2000): a partir das conjugações J das cunhas, o grupo de Poincaré é **derivado**. Summers–White (2003): um Minkowski **tridimensional** é derivado de dados modulares operacionais.
4. **A luz tem lugar especial.** Massa zero com helicidade finita é a classe que localiza em regiões limitadas **e** carrega a dilatação e a simetria conforme, que é a geometria do cone de luz (Longo–Morinelli–Rehren 2016).

**Por isso a leitura matemática honesta da sua frase é esta:** *a geometria local do espaço-tempo plano (cunhas, boosts, translações nulas e o 2π) é a forma que o relógio modular do estado inscreve, lida a partir da direção da luz.* Isso é teorema conhecido, dadas as hipóteses nomeadas abaixo.

**Onde a matemática NÃO sustenta, dito sem disfarce:**

- **O grupo de Poincaré é posto, não formado**, em BW, BGL e Morinelli–Neeb. Na ação modular geométrica ele sai das J's, mas **a variedade ℝ⁴ e a família de cunhas são fixadas antes**, e é preciso ainda transitividade, continuidade e estabilidade modular. Em Summers–White sai só em **3D**, com axiomas impostos a J e a ordem postulada.
- **BW não decorre dos axiomas gerais.** Há contraexemplos: Mund; BDFS §5.3; redes massivas modular-covariantes sem BW (Morinelli 2018).
- **Nada disto dá curvatura, dinâmica da métrica nem a equação de Einstein.** É o espaço **plano**, lido. A «formação» no sentido gravitacional continua sendo H2 (identificação física) mais H3, `[OPEN]`.
- **Nada disto fixa β.** O 2π não é β, e o «hard edge» do Código Um é outro objeto.
- **«Inscrita da luz» é mais forte que o teorema.** O teorema usa a direção nula de **qualquer** matéria de energia positiva; a massa zero só é necessária para a camada conforme.

**Em uma linha:** a sua cunhagem tem ao lado uma forma matemática conhecida e exata, a **localização modular**. Esta forma prova que a geometria plana se **lê** do relógio da luz, com o 2π forçado. Ela **não prova que o espaço-tempo físico se forma assim**: esse passo é a identificação física H2, e segue aberto. Prova ≠ juízo; o gate não se move.

---

## 2. Referências — o que foi conferido e como

**Texto lido (arXiv, em `literatura\fontes\`, sha256 no `MANIFESTO_FONTES.json`):**

- R. Brunetti, D. Guido, R. Longo, «Modular localization and Wigner particles», *Rev. Math. Phys.* **14** (2002) 759–785. DOI 10.1142/S0129055X02001387 (Crossref), arXiv math-ph/0203021. Lidos: Prop. 2.3, Thm 2.5, Thm 3.2, Thm 3.4, Cor. 3.5, Thm 4.4, Remark 2.6.
- D. Buchholz, O. Dreyer, M. Florig, S.J. Summers, «Geometric modular action and spacetime symmetry groups», *Rev. Math. Phys.* **12** (2000) 475–560, arXiv math-ph/9805026. Texto lido; o DOI de revista **NÃO CONFERIDO pelo juiz**.
- S.J. Summers, R.K. White, «On deriving space-time from quantum observables and states», *Commun. Math. Phys.* **237** (2003) 203–220. DOI 10.1007/s00220-003-0865-x (Crossref), arXiv hep-th/0304179.
- H. Araki, L. Zsidó, «Extension of the structure theorem of Borchers and its application to half-sided modular inclusions», *Rev. Math. Phys.* **17** (2005) 491–543, arXiv math/0412061. Texto lido; o DOI 10.1142/S0129055X05002388 foi dado pelas frentes e **não foi reconferido pelo juiz**.
- S.J. Summers, «Tomita–Takesaki Modular Theory», arXiv math-ph/0511034, Thm 6.1 e §5 lidos. O veículo de publicação **NÃO CONFERIDO**.
- J. Mund, «The Bisognano–Wichmann theorem for massive theories», *Ann. Henri Poincaré* **2** (2001) 907–926. DOI 10.1007/s00023-001-8598-x (Crossref), arXiv hep-th/0101227.
- V. Morinelli, «The Bisognano–Wichmann property on nets of standard subspaces, some sufficient conditions», *Ann. Henri Poincaré* **19** (2018) 937–958. DOI 10.1007/s00023-017-0636-4 (Crossref), arXiv 1703.06831.
- V. Morinelli, K.-H. Neeb, «Covariant homogeneous nets of standard subspaces», *Commun. Math. Phys.* **386** (2021) 305–358. DOI 10.1007/s00220-021-04046-6 (Crossref), arXiv 2010.07128.
- R. Longo, V. Morinelli, K.-H. Rehren, «Where infinite spin particles are localizable», *Commun. Math. Phys.* **345** (2016) 587–614. DOI 10.1007/s00220-015-2475-9 (Crossref), arXiv 1505.01759.

**Metadados conferidos (Crossref em disco); o conteúdo foi lido por fontes que o citam:**

- J.J. Bisognano, E.H. Wichmann, «On the duality condition for a Hermitian scalar field», *J. Math. Phys.* **16** (1975) 985–1007. DOI 10.1063/1.522605.
- J.J. Bisognano, E.H. Wichmann, «On the duality condition for quantum fields», *J. Math. Phys.* **17** (1976) 303–321. DOI 10.1063/1.522898.
- H.-J. Borchers, «The CPT-theorem in two-dimensional theories of local observables», *Commun. Math. Phys.* **143** (1992) 315–332. DOI 10.1007/BF02099011. O enunciado foi lido em Summers Thm 6.1, BGL Thm 3.2 e Longo LN Thm 2.2.1.
- H.-W. Wiesbrock, «Half-sided modular inclusions of von-Neumann-algebras», *Commun. Math. Phys.* **157** (1993) 83–92. DOI 10.1007/BF02098019. **Citar junto com Araki–Zsidó.**
- H.-W. Wiesbrock, «Symmetries and half-sided modular inclusions of von Neumann algebras», *Lett. Math. Phys.* **28** (1993) 107–114. DOI 10.1007/BF00750303.
- H.-J. Borchers, «Half-sided modular inclusion and the construction of the Poincaré group», *Commun. Math. Phys.* **179** (1996) 703–723. DOI 10.1007/BF02100104.
- J. Mund, B. Schroer, J. Yngvason, «String-localized quantum fields and modular localization», *Commun. Math. Phys.* **268** (2006) 621–672. DOI 10.1007/s00220-006-0067-4.
- R. Longo, V. Morinelli, F. Preta, K.-H. Rehren, «Split property for free massless finite helicity fields», *Ann. Henri Poincaré* **20** (2019) 2555–2584. DOI 10.1007/s00023-019-00820-4.

**Lido pela Frente 2, sem cópia no disco:** R. Longo, *Lectures on Conformal Nets*, Part I (rascunho de 25/11/2008), Thm 2.2.1 e Thm 2.4.1. São notas sem DOI, e a URL é a que a própria mathlib cita.

**NÃO CONFERIDO:**

- a errata de Wiesbrock em CMP 184 (1997) 683–685;
- Wigner 1939, *Ann. Math.* 40, 149–204, DOI 10.2307/1968551 (só resultado de busca);
- Sewell 1982, *Ann. Phys.* 141, 201–224 (só busca);
- Borchers 2000, *J. Math. Phys.* 41, 3604 (só busca);
- Florig 1998, LMP 46;
- as notas de Longo em Sibiu (Theta 2008);
- arXiv 2312.12182;
- a afirmação de que o grupo modular da rede de Fock é a segunda quantização de Δ_K (a referência não foi conferida).

---

## 3. O que o kernel e o acervo já têm

- **Obstrução de Borchers na torre** `[REAL, negativo]`: `periodic_borchers_trivial`, `product_borchers_trivial` e `profile_borchers_trivial`. Com espectro modular pontual, toda família de Borchers é trivial. **É por isso** que o gate lista `geometric_BW_identification_for_legacy_wedge_data_U_equals_one`: o legado não pode dar o U.
- **Localização fiel impossível na torre** `[REAL, negativo]`: `FaithfulGeometricLocalization.lean` e `central_boost_covariance_to_dilation`.
- **BW, face finita** `[REAL]`: a geometria 2D do boost e ρ = exp(−2πK) ⟹ σ_t = Ad(…). O conteúdo geométrico de BW é declarado **não enunciável** (`ModularRealization.lean:50`).
- **KMS só algébrico** `[REAL]`: `gibbs_kms`, `tower_kms`, `tState_kms`. O controle `kms_with_incompatible_geometric_data` mostra que KMS sozinho não fixa a geometria. KMS de faixa analítica existe **só no contrato**.
- **Peças soltas do habitante ax+b** `[REAL]`:
  - `ContinuousModularReconstruction` e `ContinuousModularMultipliers` (L²(ℝ), T_c, S_c = J T_c, Δ_c = T_c²);
  - `V350L2Translation` (shift contínuo);
  - `V351FourierTranslation` (`fourier_shift`).
  - **Nenhum lema costura** o shift com o Δ_c numa relação de Borchers, e não há energia positiva provada.
- **Zero ocorrências** de half-sided, ax+b, Wick e cônica. «Energia positiva» aparece só em cabeçalhos [OPEN]. **Não há representação unitária de Poincaré** no kernel. O único «Wigner» é o de Thomas–Wigner (`Solder4D.lean`).
- **Mathlib da casa**: só o tipo `StandardSubspace`, com o TODO «Tomita conjugation, Tomita's theorem, KMS». Não há Stone, grupo unitário a um parâmetro, medida espectral nem espaço de Fock.
- **Contrato v3.1 (scratchpad, não é pedra)**: BW como **campo**; deriva `halfsided_inclusion` e `contract_borchers_form` na direção **trivial** (BW ⟹ forma de Borchers); `kappa_is_input`.
- **Novo nesta rodada (scratchpad, isolado)** `[DERIVED]`:
  - `RetaDeLuzBorchers.lean` (`f726487ec1c1342e`): a representação ax+b de energia positiva em L²(ℝ, dξ), com `borchers_dilation` e `borchers_bw_form`. ⚠ O 2π aqui é **definicional**, porque `modularCandidate t := D(2πt)`. Também traz `U_faithful` e a parede `lightray_not_faithful_in_four`.
  - `RetaDeLuzEspectro.lean` (`ee7e55e5924bff52`): `D_no_eigen`.

---

## 4. Rota para H2, em ordem

A rota vai do barato ao caro. Cada degrau tem estatuto, e nenhum move o gate.

1. **E8 — frame, Killing e N a partir do boost** (5–10 h, risco baixo). É independente do resto e usa `wedgeBoostMap_add`, `wedgeBoostMap_nullDir` e `killingField`.
2. **E3 — ponte de Fourier–Plancherel** entre D(s) e os objetos 049-050 (6–12 h). O c₀ = 2π² na convenção e^{−2πi⟨v,w⟩} é `[DERIVED à mão]` e o juiz o recalculou: D(2πt) ↦ multiplicação por e^{−4π²itω}, logo Δ^{1/2} = e^{−2π²ω}. Ainda está por fixar em kernel.
3. **E3′ + E4 — o Borchers de uma partícula NÃO definicional** (A-2 abaixo). É aqui que o 2π deixa de ser definição e passa a ser forçado. O caminho, na ordem desta rota:
   - recebe o `bw` da reta como teorema;
   - depois retira o `bw` do contrato como campo e o põe como lema, a partir de `positive_energy` e `halfsided_inclusion`.
4. **E6 — rede de uma partícula de Wigner em 3+1** (A-3 abaixo): `translations_faithful` em Fin 4 → ℝ, `positive_energy` analítica, `null_ergodic` sem vácuo. Inclui **a decisão de tipo sobre `m_pos`**.
5. **E5 — segunda quantização**: Fock, Weyl, vácuo e a rede de von Neumann (100–300 h). Sem ela **não existe o W do contrato**. Fica declarado como custo; não entra na ORDEM 016.
6. **E7 — o R do par**: fluxo modular sobre W.net, core de Takesaki e Three Locks (≥ 100 h). Também fica declarado como custo.
7. **Só então** entra o termo reservado `qgPrice_H2_smoothModularFourFrame_discharged : ContratoH2 W₀ R₀ N₀` sobre o par ratificado. E mesmo aí resta a **identificação física** `[OPEN]`: que o par plano de Wigner é o do horizonte físico da TGL, e que τ★ é o relógio desse mesmo horizonte, o que é H3.

**Consequência dita:** a identificação aberta «BW para o legado com U = 1» **não se resolve no legado**, porque as obstruções provam que a torre não dá o U. Ela pede um par **novo** com U fiel.

---

## 5. Alvos para a ORDEM 016: A-2 e A-3 (texto pronto)

> Protocolo anti-parede em vigor: **parede só a gerência declara**. Cada alvo traz uma árvore de alternativas obrigatória e o teto de horas por ramo. Esgotado o teto, a bancada **entrega o que mediu e o ramo seguinte**, e não o nome «parede». A gerência pré-resolve e entrega a receita, que vai junto. Compilação só isolada, com `#print axioms` no trio {propext, Classical.choice, Quot.sound}, zero `sorry`, zero `axiom` novo e kernel intocado (`find -newer`).

### A-2 — «O 2π forçado na reta de luz» (o Borchers de uma partícula, não definicional)

**Objeto.** O modelo de `RetaDeLuzBorchers.lean`: H = L²(ℝ, dξ) com ξ = log p, U(a) = multiplicação por e^{iae^ξ}, D(s) = translação em ξ. O 2π, hoje definicional, deve passar a ser **consequência**.

**Receita da gerência** `[DERIVED à mão, os sinais a fixar no kernel]`:

- Tome um parâmetro de largura w > 0 e defina Δ_w^{1/2} por continuação analítica: f ∈ dom(Δ_w^{1/2}) ⟺ f se estende holomorfa e L²-limitada à faixa 0 < Im ξ < w, e (Δ_w^{1/2}f)(ξ) = f(ξ + iw). Tome J f = conj(f) e K_w = {f : J f = Δ_w^{1/2} f}, isto é, f(ξ + iw) = conj f(ξ).
- O multiplicador m_a(ξ) = e^{iae^ξ} se estende à faixa com |m_a(ξ + iy)| = e^{−a e^ξ sin y}. Para **a ≥ 0 e 0 ≤ y ≤ π** ele é **limitado por 1**: aqui entra a energia positiva.
- A torção fica preservada ⟺ m_a(ξ + iw) = conj m_a(ξ) ⟺ e^{iw} = −1 ⟺ **w = π**, que é a largura da faixa correspondente a Δ^{it} = D(2πt).
- Logo U(a)K_π ⊆ K_π para a ≥ 0, que é a isotonia da meia-reta. Com w ≠ π, a torção se quebra; com w > π, sin y < 0 na faixa e o multiplicador explode. **O 2π é o único que funciona.** É o círculo KMS como leitura da face, em teorema.

**Árvore de alternativas e tetos:**

| ramo | o que faz | teto |
|---|---|---|
| **A-2.a** (principal) | Isotonia no núcleo denso: trabalhar num core explícito de K_π (por exemplo f = g·h, com g inteira de decaimento gaussiano em ξ que satisfaça a torção) e provar `halfline_isotony_core : 0 ≤ a → f ∈ core → U a f ∈ K_π`. Em seguida, fecho por continuidade de U(a) e fechamento de K_π | 40 h |
| **A-2.b** | Caracterização Hardy/Paley–Wiener da faixa: dom(e^{wω} no dual de Fourier) ⟺ continuação à faixa. Mais geral e mais cara; usar só se o ramo a travar no fecho | 60 h |
| **A-2.c** | Rota pelo lado de Fourier: K_c do lote 049-050 (T_c = M_{exp(−cξ)}) transportado por 𝓕 (E3), com a isotonia provada como estabilidade de um subespaço de Hardy sob o multiplicador. Reusa o kernel ao máximo | 50 h |
| **A-2.d** (mutação, obrigatório em qualquer ramo) | `twist_preserved_iff : (∀ ξ, m_a(ξ + i w) = conj (m_a ξ)) ↔ w = π` (para a > 0 e w ∈ (0, 2π)), e, se o custo couber, o contraexemplo `¬ U a '' K_w ⊆ K_w` para w ≠ π | 12 h (o ⟸/⟹ da torção); +20 h (o contraexemplo, opcional) |
| **A-2.e** (recuo nomeado) | Se a, b e c esgotarem os tetos: entregar a hipótese nomeada `HalfLineIsotonyAtWidth w` e o teorema condicional «isotonia ⟹ w = π» a partir de A-2.d. É o 2π forçado **condicionalmente**, dito como tal | 8 h |

**Aceitação.** Compila isolado; axiomas no trio; zero sorry.

- Em **a, b ou c**: `halfline_isotony` para a ≥ 0 **e** `twist_preserved_iff` (A-2.d).
- No **recuo e**: o teorema condicional com a hipótese no nome.

**Cético obrigatório:**

1. trocar π por π/2 ou 3π/2 no teorema principal tem de **falhar** na compilação;
2. trocar a ≥ 0 por a ≤ 0 tem de **falhar**, porque a energia positiva é usada;
3. o lema não pode citar `modularCandidate` (a definição com 2π) para provar a própria isotonia.

**Estatuto.** `[DERIVED]` em scratchpad, candidato a porte pela bancada após auditoria. É modelo de **uma partícula em 1+1**, que não habita `translations_faithful` (parede já provada: `lightray_not_faithful_in_four`). Não move `gpf_H2`. O que ele prova: na reta de luz o 2π **é forçado** pela positividade; κ/T = 2π deixa de ser herdado **neste modelo**. `BoostHeatConstruction.lean:153` só muda de estatuto quando o par físico existir.

### A-3 — «O habitante de Wigner em 3+1 e a retipagem da massa»

**Objeto.** Uma representação unitária de energia positiva U : (Fin 4 → ℝ) → 𝒰(L²(órbita, μ)), com os campos do contrato que **não** dependem de vácuo nem de segunda quantização.

**Pré-decisão de tipo (gerência/operador, antes da bancada):** `m_pos : 0 < m` (`SpecificAQFTWitness.lean:96`) não tem uso no kernel. Um habitante de luz com m := 1 seria frase falsa no tipo. As opções são:

- (i) retipar para `0 ≤ m`, amarrado ao espectro de P²;
- (ii) manter m > 0 e usar o campo massivo, para o qual BW também vale (Mund 2001), deixando a luz para depois;
- (iii) dois habitantes, massivo e de massa zero.

**Árvore de alternativas e tetos:**

| ramo | órbita | o que se ganha | teto |
|---|---|---|---|
| **A-3.a** | hiperboloide de massa m > 0, escalar | cabe em `m_pos` sem retipar; BW conhecido (Mund) | 60 h |
| **A-3.b** | cone de luz, helicidade 0 (d³p/\|p\|) | «a luz» como massa zero; pede a retipagem (i) | 70 h |
| **A-3.c** | fóton, helicidade +1 ⊕ −1 | a luz física; o PCT pede o dobro (BGL Remark 2.6); J troca as helicidades | 120 h |
| **A-3.d** (sempre, barato) | E8: frame, Killing e N via `boostMat` e `wedgeBoostMap_*` | campos geométricos de H2 dado o boost | 10 h |

**Sub-alvos em cada ramo, em ordem:**

1. `translations_faithful_orbit`: se e^{ia·p} = 1 para todo p na órbita, então a = 0, porque a órbita gera ℝ⁴. **Barato**: 8 h.
2. `positive_energy_analytic`: F(z) = ∫ e^{iz a·p} dμ_ψ é limitada e holomorfa em Im z > 0 para a no cone futuro fechado. 20 h.
3. `wedge_boost_rep`: U(Λ_W(t)) com `V_translations` via `boostMat` e a relação de Borchers nula herdada da reta (A-2), por restrição ao raio. 20 h.
4. `one_particle_no_eigen`: nenhum autovetor do boost, que é o análogo do E2. 15 h.
5. **O cético da vacuidade:** provar que o habitante **não** satisfaz `null_ergodic` na forma com vácuo (não há vácuo), e declarar que isso é o E5, não uma falha.

**Aceitação.** Um ramo principal completo (os sub-alvos 1–4), mais o A-3.d, isolado, no trio, com zero sorry. A decisão sobre `m_pos` fica registrada **antes** do código. Recuo nomeado: se o sub-alvo 2 esgotar o teto, entregar `PositiveEnergy` na forma espectral (suporte de μ no cone futuro), com a forma analítica como hipótese no nome.

**Estatuto.** `[DERIVED]` em scratchpad. O **W do contrato não existe** sem E5 (vácuo, rede de von Neumann) nem o **R** sem E7 (core de Takesaki, Three Locks). Os dois ficam declarados na ordem como custo real (≥ 400 h no total, risco muito alto) e não como alvo. Não move `gpf_H2` nem o gate.

---

## 6. Ressalvas (homônimos e tipos que não se encadeiam sem lema)

1. **Três Wigners, nenhum lema entre eles.**
   - (a) **Thomas–Wigner**: [K₁, K₂] = −J₃, `Solder4D.lean`. É curvatura de boosts, a rotação de Wigner.
   - (b) **Wigner 1939**: a classificação das representações unitárias de Poincaré. A luz é a órbita de massa zero. Não está no kernel.
   - (c) **o «Wigner» do acervo IALD**: `wigner_test_20260313`, «IALD Wigner Hypothesis», semicírculo/Marchenko–Pastur sobre tensores neurais. É o controle neural, que **não entra no artigo** (ordem do operador). O JSON dele nem carrega (falha na linha 27).
   - Citar um a favor do outro é o erro de homônimo que a casa proíbe.
2. **κ de horizonte ≠ κ do boost ≠ «κ espectral».**
   - O κ do contrato é aceleração/normalização (`kappa_is_input`, κ = 1/ρ(N)).
   - O κ de `BisognanoWichmann` e `PowersLadder` é parâmetro de rapidez da face.
   - «Espectral» é o espectro de log Δ, contínuo e sem borda neste modelo.
   - O que o 2π fixa é **κ/T**, não κ.
3. **2π ≠ 2π ≠ 2π.**
   - O 2π de Borchers (largura da faixa KMS × positividade) é o forçado.
   - O 2π da convenção de Fourier da mathlib (e^{−2πi⟨v,w⟩}) é convenção.
   - O 2π definicional de `modularCandidate` (E1) não prova nada sobre o 2π.
   - O c₀ = 2π² mistura dois deles e deve ser conferido em kernel.
4. **β ≠ β.** O `kms` do contrato a β = 1 é temperatura **inversa** (normalização), não β_TGL = α√e. Nada na localização modular fixa β_TGL, e o «hard edge» do Código Um não se liga ao 2π.
5. **J ≠ J.**
   - O J modular da cunha é **CPT composto com a rotação de π** em torno do eixo 1, isto é, a reflexão (x⁰, x¹) ↦ (−x⁰, −x¹) (BDFS §5.3; BGL §2). Não é «a CPT» sozinha.
   - O J = Luz da TGL `[ONTO]` tem J² = I e JKJ = −K. A relação J log Δ J = −log Δ tem a mesma **forma**, mas **nenhum lema** liga os dois.
6. **K ≠ K ≠ K.** K_W (subespaço padrão), K (gerador do boost) e K («a diferença em movimento») são três objetos com a mesma letra.
7. **«Padrão» não pede energia positiva.** O que a energia positiva dá é a **isotonia** (BGL Thm 3.4). A formulação da gerência estava errada e fica corrigida aqui.
8. **BW é input** em BGL (por definição), na forma do contrato v3.1 (campo) e em E1 (definição). BW como teorema a partir dos axiomas é **falso em geral**, pelos contraexemplos.
9. **Wiesbrock sozinho não se cita.** A prova tem lacuna, preenchida por Araki–Zsidó (2005).
10. **Candidato a errata, AO LADO, não tocado:** `ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md:128`. A relação Δ^{it}U(a)Δ^{−it} = U(e^{−2πt}a) vale para **todo a ∈ ℝ**, porque U é grupo. Unilateral é a **hipótese** (U(a)H ⊆ H para a ≥ 0). A leitura «a unilateralidade represa» `[CONJECTURE]` sobrevive se for dita sobre a inclusão.
11. **O toro.** O «tau do torus» do teste neural (`torus_signature = false`) não é o círculo KMS. O círculo KMS é a leitura compacta da face; o toro neural é negativo honesto e fica fora do artigo.
12. **Luz = direção nula ou massa zero.** Na camada de Borchers/BW, só a direção nula, e para qualquer matéria. Na camada de Wigner/conforme, a massa zero com helicidade finita. A localização limitada **não** é exclusiva da luz: massivas também localizam em cones duplos.
13. **Escopo.** Tudo aqui é espaço **plano**. Curvatura, a equação de Einstein e a identificação com o horizonte físico da TGL (H2 físico, H3) seguem `[OPEN]`. **PROVADA ≠ CONFIRMADA; o gate não se move.**
