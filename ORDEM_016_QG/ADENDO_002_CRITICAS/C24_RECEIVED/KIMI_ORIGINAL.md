# C2.4 — Resposta crítica (DECLARADO até confronto da bancada)

**Escopo honesto desta análise.** Nada foi compilado nesta chamada; não inspecionei arquivos fora das projeções fornecidas; as projeções são parciais (`PARTIAL_PROJECTION`), e em particular **não** foram exibidas: a assinatura exata de `KMSAt` e de `kmsStrip`, os enunciados das bordas `h1`/`h2` (lidos apenas pelo padrão de deconstrução `⟨F, hF, ⟨M, hM⟩, h1, h2⟩` em `KMSStripConditional.lean:14`), o corpo de `spectral_boundary_balance`, e o arquivo `StandardSubspace.lean` (citado apenas de segunda mão, via adendo: "TODO Tomita/KMS l.40-42"). Onde a convenção KMS padrão supre uma linha omitida, marco como inferência de convenção, não leitura. Hashes citados são os lidos nas projeções, não recomputados.

## 1. Veredito binário

**O obstáculo não excede o TODO do `StandardSubspace` — ele coincide com o TODO na primeira hipótese e exige, além dele, dois dados fortes que o TODO não cobre.** Não existe, com o que está compilado, rota em rapidez que construa a função holomorfa e as duas bordas KMS **do mesmo par regional**. O que existe em rapidez é estritamente mais fraco: a sombra funcional do pacote (A2) e uma fatia unilateral de dois pontos (A3), nenhuma das quais é KMS. Decomposição exata das duas hipóteses nomeadas:

| hipótese | conteúdo matemático | o que é |
|---|---|---|
| `H_regional_modular_strip : KMSAt W (fun t => D (-t)) 1` | Tomita–Takesaki com domínios para o fluxo modular do par: `S = JΔ^{1/2}`, `Δ` auto-adjunto, KMS_1 de `Δ^{it}` | **É o TODO** (`StandardSubspace.lean`), mais Weyl/Fock + KMS quase-livre (Araki, [KNOWN] externo, [DADO FALTA] no kernel) |
| `H_modular_equals_geometric : ∀ t, D t = B (-(2π t))` | Bisognano–Wichmann para o par | **[DADO FALTA]** — não se assume e não se anuncia como derivado |

A cola entre elas (`boost_rapidity_kms_from_modular`, `killing_kms_from_modular`, `kms_rescale_existing`, fonte `63fd7143…`, rc=0 relatado em `2ac6ad89…`) é condicional — constatado no parecer `33cff3ad`; não o repito, apenas registro que ela consome as duas hipóteses, não as produz.

## 2. Confronto dos três núcleos

**A2 (`LightRayAnalyticCore_v3.lean` `64c0a9ca…`; `LightRayBoundaryBalance_v3.lean` `7905c030…`).** O que há [REAL compilado, segundo as projeções]: inteiricidade de `multiplier` e `twistedGaussian`; contração `‖multiplier a (x+iy)‖ ≤ 1` na faixa `0 ≤ y ≤ π` para `a ≥ 0`; o twist de borda `F(x+iπ) = star F(x)`; deslocamento de contorno com decaimento vertical (`spectral_contour_shift`); fatoração da borda superior como fase real vezes o conjugado do produto (`spectral_top_factor`). O que isto é: uma **J-simetria escalar** de função — a borda superior é o *conjugado* da inferior. O que falta para ser KMS: a álgebra, o estado e o produto. A borda KMS não é conjugação; é **troca de ordem** entre correlações `⟨A, U(z)B⟩` e `⟨B, U(z)A⟩`, e o "lado trocado" só existe se `A` e `B` são operadores que multiplicam um vetor de referência. A2 não tem sequer o tipo desse lado.

**A3 (`OrbitalStateAnalytic.lean` `c4df0f69…`).** O que há: a ponte vetor→medida (`stateDensityMeasure`, `stateDensity_integral_multiplier`) e energia positiva orbital. O que isto compra genuinamente em rapidez: para `U(t) = e^{itH}`, `H ≥ 0`, e `f, g` vetores, `F(z) = ∫ e^{izλ} dμ_{f,g}(λ)` é holomorfa num semiplano e contínua no fecho — **analiticidade unilateral de dois pontos**. É real e é a única fatia positiva da rota; mas depende de API de teorema espectral/Laplace de medida finita na mathlib — disponibilidade **a verificar, não afirmada**. E não dá KMS: a positividade da energia dá holomorfia unilateral e decaimento; **não** dá a relação de borda que codifica estado+modularidade.

**`KMSAt` do contrato.** Vive sobre `W : TGLSpecificAQFTWitness` (`ContratoQG_v31_Minimal.lean` `37987765…`), em namespace e Hilbert distintos dos namespaces de A2/A3 (`ChatgptAudit.LightRayCore016`, `WignerRapidityMeasure016`). Colar a sombra escalar ao pacote do contrato exigiria que o Hilbert da reta de luz **seja** `W.H` com uma álgebra regional agindo — exatamente os elos Fock/R da rota de sete elos da ORDEM 016, não construídos e não construíveis por definição nesta chamada.

## 3. Por que borda de função de onda ≠ borda de correlação KMS

Resposta explícita à pergunta, em quatro pontos:

1. **Objeto diferente.** A borda de função de onda é propriedade de vetores sob um grupo; a borda KMS é propriedade de pares `(A, B)` de elementos de uma álgebra sob estado+grupo. Sem produto de operadores, o "lado trocado" não tem tipo.
2. **Conteúdo diferente.** A borda unilateral codifica positividade espectral; a borda KMS codifica equilíbrio (Gibbs) ou modularidade (Tomita). A segunda implica a primeira, nunca o contrário.
3. **O teste decisivo em uma partícula.** As únicas álgebras de von Neumann naturais no domínio de uma partícula são: (a) os multiplicadores `L∞` — abelianos, logo `σ_t = id`, KMS trivial com `F` constante, que não codifica rapidez alguma; (b) `B(H)` inteiro — sem noção de regionalidade. A regionalidade com modular não-trivial exige subespaços padrão + Tomita (o TODO) e a álgebra de Weyl (Fock). Mesmo a formulação ingênua do "vetor de Rindler de uma partícula", `e^{-πK}f`, **falha de domínio** para `f` genérica — e a existência de um conjunto denso de vetores analíticos é o conteúdo de BW/Tanimoto, não um lema de rapidez.
4. **O twist escalar não é a troca de ordem.** O `gaussian_twist`/`spectral_top_factor` de A2 dá `F(x+iπ) = fase · conj(F(x))`: uma involução antilinear no nível de função. A ponte entre essa J-simetria e a troca de ordem operatorial é precisamente `S = JΔ^{1/2}` — o TODO.

## 4. O tipo que falta, exatamente

Falta um tipo de dados `RegionalModularPair` contendo: `A_O` (álgebra de von Neumann sobre `W.H`), `Ω ∈ W.H` cíclico (`A_O Ω` denso) e separante (`AΩ = 0 ⟹ A = 0`), e `U : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)` com lei de grupo e covariância (`Ad(U_t) A_O ⊆ A_O`, ou a família regional indexada). Em uma partícula esse tipo **não habita** pelas razões do item 3: o habitante natural é a álgebra de Weyl/CCR — nomeada aqui como **dado**, não construída (proibido fingir), e fora do escopo desta rota.

## 5. Sequência MÍNIMA de lemas, com estatutos

| # | lema | estatuto | dado exigido |
|---|---|---|---|
| L1 | `F(z) = ⟨f, U(z)g⟩` holomorfa unilateral, borda `F(t) = ⟨f, U(t)g⟩` (dois pontos, energia positiva) | **[PROPOSTA — rapidez]** | API espectral/Laplace — **a verificar** |
| L2 | lema-quebra: estado vetorial KMS_β (`β>0`) para `Ad(e^{itH})` com `Ω` cíclico-separante ⟹ dinâmica trivial no suporte de `Ω` | **[PROPOSTA — rapidez; caso finito imediato]** | estados normais/centralizador na mathlib — **a verificar** |
| L3 | Tomita do subespaço padrão: `S` fechado e denso → polar `S = JΔ^{1/2}` → KMS de `Δ^{it}` | **= o TODO** | desenvolvimento substancial; não é rapidez |
| L4 | Weyl/quase-livre: KMS_2π do estado de Fock sobre o subespaço padrão (Araki [KNOWN] externo) | **[DADO FALTA — Fock]** | construção CCR — fora desta chamada |
| L5 | meia-lateralidade/BW: `Δ^{it} U(a) Δ^{-it} = U(e^{-2πt}a)` ⟹ `D = B(-2π·)` (Borchers [KNOWN] externo) | **[DADO FALTA — é H2]** | negativos registrados na torre-produto; rotas: estado não-produto, subálgebra não-alinhada, outra representação |
| L6 | cola condicional já compilada | [REAL — condicional] | — (não repetir) |

**Em rapidez não se supre nenhuma das duas hipóteses; em rapidez se mede o terreno (L1), se fecha a porta errada (L2) e se abre a porta certa (primeiro passo de L3).** O controle `kms_with_incompatible_geometric_data` (citado na entrega `2ac6ad89…`) é identidade KMS algébrica, não contraexemplo à rota — mas também não dispensa a igualdade de grupos exigida por H2.

## 6. Menor lema/artefato faltante

Dois, com papéis distintos:

- **(a) `oneParticle_vectorKMS_trivial` (L2).** O mais barato e mais informativo: converte o diagnóstico desta resposta em teorema, proibindo definitivamente a leitura "borda de função de onda = borda KMS". Esboço (não compilado): KMS + separante ⟹ estado fiel; `Ω` vetorial KMS para `Ad(e^{itH})` ⟹ `Ω` no centralizador e autovetor de `H`; aplicado a projeções espectrais, `e^{itH}` age trivialmente no ciclo de `Ω`; ciclicidade estende a `H`. Caso finito: imediato.
- **(b) o primeiro lema do TODO: `S` do subespaço padrão é densamente definido e fechado.** Puramente Hilbert-espacial, sem física, ~dezenas de linhas, e pré-requisito de tudo o mais em L3. Se `StandardSubspace.lean` já definir `S`, o menor passa a ser a decomposição polar de `S` — condicionado à inspeção do arquivo, que **não fiz** ([LACUNA] declarada).

Recomendação: (b) destrava a rota certa; (a) documenta por que a rota errada morre. Nenhum dos dois cria nome reservado nem toca o gate.

## 7. Delimitações

Não afirmo compilação, inspeção integral, derivação de BW, construção de Fock, escolha de partição física, nem movimento de gate. Concordância de modelos não foi usada como prova. Provas formais só valem por compilação isolada rc=0, `#print axioms ⊆ {propext, Classical.choice, Quot.sound}`, zero `sorry`/axioma novo. Resposta **DECLARADO** até confronto da bancada.

**Lacunas que bloqueiam precisão adicional:** a assinatura de `KMSAt`/`kmsStrip` e os enunciados de `h1`/`h2` (fora da projeção); o conteúdo de `LightRayVerticalDecay_v4` (a bound uniforme `⟨M, hM⟩` pode já estar parcialmente lá — não alego); o conteúdo de `StandardSubspace.lean` além da menção do adendo; a disponibilidade na mathlib do teorema espectral de Stone para grupos uniparamétricos (pré-requisito de L1).