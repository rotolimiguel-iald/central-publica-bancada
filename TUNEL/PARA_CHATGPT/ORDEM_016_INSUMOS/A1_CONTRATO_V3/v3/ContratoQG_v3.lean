import TGLExt.TheMasterFires
import TGLExt.StrongFrame
import TGLExt.V354RegularLegacyWitness
import TGLExt.PoincareGroup
import TGLExt.ProfileEntropyLimits
import TGLExt.TheImportedEquilibrium

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# CONTRATO DE TIPO v3 DE H2 / H3 / IMPORT-H3 — O TIPO (só definições)
  [RASCUNHO DE GERÊNCIA — frente contrato_v3, 23/09/2026; scratchpad; NÃO cunha nome reservado]

  Este arquivo contém SÓ o tipo (estruturas e definições que não leem campo `Prop` de contrato).
  Os teoremas vivem em `ContratoQG_v3_Teoremas.lean`; as paredes contra v2/brinquedo em
  `ContratoQG_v3_Paredes.lean`. A separação existe para a MUTAÇÃO CAMPO A CAMPO (resposta ao cético
  final de W2: probes de rc constante): cada campo `Prop` pode ser afrouxado a `True` aqui e este
  arquivo continua a compilar; quem tem de mudar de resultado são as guardas (`GuardasV3.lean`).

  É o tipo que os três nomes reservados terão de habitar quando alguém os cunhar (nenhum é cunhado aqui):

    TGLExt.qgPrice_H2_smoothModularFourFrame_discharged    : ContratoH2 W₀ R₀
    TGLExt.qgPrice_H3_localHorizonEquilibrium_discharged  : ContratoH3 W₀ R₀
    TGLExt.qgImport_H3_horizonEquilibriumData_produced    : ContratoImportH3 W₀ R₀ qgPrice_H2_…

  com (W₀, R₀) o par RATIFICADO pelo operador (partição M01). Nenhuma escolha de partição é feita aqui:
  tudo é parametrizado por (W, R).

## O que a v3 corrige da v2 (02fd013827dca251), medido
  (D-A) o brinquedo U(a) = Δ^{i a₂} HABITAVA a v2 (W5_final, ProbeToyContratoH2, rc=0). Na v3:
        `translations_faithful` (dente de fidelidade) + `null_ergodic` + a relação de BW com um GRUPO DE
        BOOSTS covariante — o brinquedo não habita (teorema em `ContratoQG_v3_Paredes.lean`).
  (D-B) a cláusula (S) da v2 (`stateIso` com uma torre + `state_flow`) FORÇAVA espectro pontual de Δ^{it}
        (W5ParedeEspectral, `contratoH2_forces_point_spectrum`). Na v3 NÃO há torre: o estado é o vácuo
        de W, Δ^{it} é o implementador do fluxo de R, é KMS a β = 1 (é O fluxo modular, não um fluxo
        qualquer) e satisfaz Bisognano–Wichmann com o boost da cunha COMO CAMPO:
        `bw : Δit t = boost.V (−2πt)`. O teorema de coerência (`no_point_spectrum`) prova o OPOSTO da v2:
        todo habitante da v3 tem Δ^{it} SEM autovetores fora de ℂΩ.
  (C4) κ era [INPUT] livre. Na v3 κ está amarrado três vezes: (i) o fluxo de Killing τ ↦ V(κτ) é KMS a
        β = 2π/κ — T = κ/2π passa de DEFINIÇÃO a TEOREMA (`unruh_is_kms`, dos campos `kms` e `bw`);
        (ii) κ = 1/ρ do observador fiducial (campo `observer_unit`, teorema `kappa_eq_inv_radius`);
        (iii) o MESMO κ entra no calor de H3 e cancela em δS (teorema).
  (H3) G, matéria e perturbação eram [INPUT] livres (BH e Clausius ajustáveis dado um H2). Na v3:
        δS := δ⟨K⟩ (primeira lei do emaranhamento, K = −log Δ, lido do DERIVADO de ⟪ψ, Δ^{it}ψ⟫ — sem
        entropia de torre); δQ := calor do tensor de matéria DO ESTADO, amarrado à energia de boost do
        estado (`matter_is_state`); G é campo ANTES do ∀ perturbação (`area_law`); Clausius deixa de ser
        campo e vira teorema; a proporcionalidade δS : δA é a mesma para toda perturbação (teorema).
  (Import) o tipo do import é INDEXADO pelo termo H2 (`ContratoImportH3 W R h2`): não se escreve o tipo
        sem um H2 no mesmo par — a vacuidade ex falso não tem nem o tipo onde morar.

## Convenções (ditas, não escondidas)
  * U(a) = e^{i a·P} (métrica (+,−,−,−)); energia positiva = P ∈ V̄₊ ⟺ para a ∈ V̄₊, t ↦ ⟪ψ, U(ta)ψ⟫ é
    valor de fronteira de função holomorfa limitada no semiplano superior (`PositiveEnergy`) [KNOWN].
  * Δ^{it} = e^{−itK}, K = −log Δ; `HasModularEnergy Δit ψ k` ⟺ d/dt⟪ψ,Δ^{it}ψ⟫|₀ = −i k (k = ⟨ψ,Kψ⟩).
  * V(s) = e^{isB}; `HasBoostEnergy V ψ b` ⟺ d/ds⟪ψ,V(s)ψ⟫|₀ = i b.  BW ⟹ K = 2πB.
  * KMS a β para α_t (vetorial): F(t) = ⟪A*Ω, α_t BΩ⟫, F(t+iβ) = ⟪B*Ω, α_{−t} AΩ⟫, F holomorfa e
    limitada na faixa 0 < Im z < β. O fluxo modular σ_t = Ad Δ^{it} satisfaz KMS a β = 1 para α_t = Δ^{−it}
    [KNOWN, Takesaki; conferido na face finita ρ^{it}]; a mathlib da casa não tem Tomita/KMS — aqui é CAMPO.

## Estatutos
  [DERIVED] os lemas geométricos deste arquivo; [KNOWN como exigência] BW, KMS, Borchers, Unruh,
  primeira lei do emaranhamento, Jacobson; [INPUT] κ-observador, G, tela, ε, λ₀, a classe admissível, a
  resposta geométrica e o tensor de matéria (DADOS, amarrados pelos campos); [OPEN] o par físico.
  β jamais literal. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt.ContratoQGv3

open TGL.SpecificAQFT TGL.ModularRealization
open MeasureTheory Matrix Complex
open scoped InnerProductSpace

noncomputable section

/-! ## 0. A geometria do boost da cunha (sem ler campo de contrato) -/

/-- a ação geométrica do boost no plano (0,1) (rapidez `s`), com a matriz `TGLExt.boostMat` do kernel. -/
def wedgeBoostMap (s : ℝ) (x : Fin 4 → ℝ) : Fin 4 → ℝ := (boostMat s).mulVec x

/-- o campo de Killing do boost normalizado por κ: ξ_κ(x) = κ·(x¹, x⁰, 0, 0). -/
def killingField (κ : ℝ) (x : Fin 4 → ℝ) : Fin 4 → ℝ := κ • ![x 1, x 0, 0, 0]

/-- o vetor nulo do horizonte futuro da cunha: n = (1, 1, 0, 0). -/
def nullDir : Fin 4 → ℝ := ![1, 1, 0, 0]

/-- [DERIVED] ★ A LEI DE GRUPO DO BOOST, na forma pedida: boostMat(a+b) = boostMat a · boostMat b
    (lida de `theBoost_add`, PoincareGroup.lean:173 — não é refeita). -/
theorem boostMat_add (a b : ℝ) : boostMat (a + b) = boostMat a * boostMat b := by
  have h := congrArg Subtype.val (theBoost_add a b)
  change boostMat a * boostMat b = boostMat (a + b) at h
  exact h.symm

theorem boostMat_zero : boostMat 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [boostMat]

theorem wedgeBoostMap_add (a b : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap (a + b) x = wedgeBoostMap a (wedgeBoostMap b x) := by
  simp only [wedgeBoostMap, boostMat_add, Matrix.mulVec_mulVec]

theorem wedgeBoostMap_zero (x : Fin 4 → ℝ) : wedgeBoostMap 0 x = x := by
  simp [wedgeBoostMap, boostMat_zero]

theorem wedgeBoostMap_smul (s c : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s (c • x) = c • wedgeBoostMap s x := by
  simp [wedgeBoostMap, Matrix.mulVec_smul]

theorem wedgeBoostMap_apply0 (s : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s x 0 = Real.cosh s * x 0 + Real.sinh s * x 1 := by
  simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

theorem wedgeBoostMap_apply1 (s : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s x 1 = Real.sinh s * x 0 + Real.cosh s * x 1 := by
  simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

/-- [DERIVED] o vetor nulo é autodireção do boost com dilatação e^s. -/
theorem wedgeBoostMap_nullDir (s : ℝ) : wedgeBoostMap s nullDir = Real.exp s • nullDir := by
  funext i
  fin_cases i <;>
    simp [nullDir, wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four,
      ← Real.cosh_add_sinh]

/-! ## 1. As condições analíticas nomeadas (KMS, energia positiva) e as expectativas dos geradores -/

/-- a faixa aberta 0 < Im z < β. -/
def kmsStrip (β : ℝ) : Set ℂ := {z | 0 < z.im ∧ z.im < β}

/-- o semiplano superior aberto. -/
def upperHalf : Set ℂ := {z | 0 < z.im}

/-- o cone futuro FECHADO: a⁰ ≥ 0 e a·a ≥ 0 (métrica (+,−,−,−), `minkowskiSq` do kernel). -/
def forwardCone : Set (Fin 4 → ℝ) := {a | 0 ≤ a 0 ∧ 0 ≤ minkowskiSq a}

/-- **KMS a β** (forma vetorial) de um grupo a um parâmetro de unitários α sobre (W.net cunha, W.vac):
    para A, B da álgebra da cunha existe F holomorfa na faixa 0 < Im z < β, contínua e limitada no fecho,
    com F(t) = ⟪A*Ω, α_t BΩ⟫ e F(t + iβ) = ⟪B*Ω, α_{−t} AΩ⟫. [KNOWN: é a condição que caracteriza o grupo
    modular (Takesaki); aqui é DEFINIÇÃO de tipo, não teorema.] -/
def KMSAt (W : TGLSpecificAQFTWitness) (α : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) (β : ℝ) : Prop :=
  ∀ A ∈ W.net rightWedge, ∀ B ∈ W.net rightWedge, ∃ F : ℂ → ℂ,
    DiffContOnCl ℂ F (kmsStrip β) ∧
    (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ β → ‖F z‖ ≤ M) ∧
    (∀ t : ℝ, F t = ⟪(star A) W.vac, α t (B W.vac)⟫_ℂ) ∧
    (∀ t : ℝ, F (t + β * I) = ⟪(star B) W.vac, α (-t) (A W.vac)⟫_ℂ)

/-- **Energia positiva** (condição espectral, forma analítica): para todo a no cone futuro fechado e todo
    vetor ψ, t ↦ ⟪ψ, U(t·a)ψ⟫ é valor de fronteira de uma F holomorfa limitada no semiplano superior
    [KNOWN: equivalente a a·P ≥ 0 para o gerador; aqui é DEFINIÇÃO]. -/
def PositiveEnergy (W : TGLSpecificAQFTWitness) : Prop :=
  ∀ a ∈ forwardCone, ∀ ψ : W.H, ∃ F : ℂ → ℂ,
    DiffContOnCl ℂ F upperHalf ∧
    (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖F z‖ ≤ M) ∧
    (∀ t : ℝ, F t = ⟪ψ, W.U (t • a) ψ⟫_ℂ)

/-- **a expectativa do hamiltoniano modular** K = −log Δ, sem operador ilimitado: ψ tem energia modular k
    sse d/dt ⟪ψ, Δ^{it}ψ⟫|_{t=0} = −i·k (Δ^{it} = e^{−itK}). -/
def HasModularEnergy {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (Δit : ℝ → (H ≃ₗᵢ[ℂ] H)) (ψ : H) (k : ℝ) : Prop :=
  HasDerivAt (fun t : ℝ => ⟪ψ, Δit t ψ⟫_ℂ) (-(I * (k : ℂ))) 0

/-- **a expectativa do gerador do boost** B (V(s) = e^{isB}): d/ds ⟪ψ, V(s)ψ⟫|_{s=0} = i·b. -/
def HasBoostEnergy {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (V : ℝ → (H ≃ₗᵢ[ℂ] H)) (ψ : H) (b : ℝ) : Prop :=
  HasDerivAt (fun s : ℝ => ⟪ψ, V s ψ⟫_ℂ) (I * (b : ℂ)) 0

/-- «Δit não tem autovetor fora da reta do vácuo» — a MESMA forma de `W5Final.Espectral.NoEigenOutsideVacuum`
    (W5ParedeEspectral.lean), para que o teorema de coerência seja a negação exata da parede da v2. -/
def NoEigenOutsideVacuum (W : TGLSpecificAQFTWitness) (D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) : Prop :=
  ∀ (v : W.H) (r : ℝ), (∀ t : ℝ, D t v = ChatgptAudit.modularPhase t r • v) → v ∈ (ℂ ∙ W.vac)

/-! ## 2. O GRUPO DE BOOSTS da cunha, representado em W.H -/

/-- **WedgeBoostRep W** — a representação unitária fortemente contínua do grupo de boosts da cunha em W.H,
    tipada pela `boostMat` do kernel: lei de grupo, vácuo invariante, covariância das translações
    (V(s) U(a) V(−s) = U(Λ_s a)) e covariância geométrica da rede (Ad V(s) net(O) ⊆ net(Λ_s O)).
    ⚠ As paredes do kernel continuam de pé e NÃO são contrariadas: V age em W.H e U é MULTIPLICATIVO;
    nenhuma aplicação LINEAR injetiva ℝ⁴ → W.H é entrelaçada (`no_injective_isometric_boost_intertwiner`,
    ModularSignatureObstruction.lean:102; `tower_modular_cannot_intertwine_nonzero_boost`,
    Order007Bridges.lean:47). -/
structure WedgeBoostRep (W : TGLSpecificAQFTWitness) where
  V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)
  V_zero : V 0 = LinearIsometryEquiv.refl ℂ W.H
  V_add : ∀ a b : ℝ, V (a + b) = (V b).trans (V a)
  V_continuous : ∀ ψ : W.H, Continuous (fun s : ℝ => V s ψ)
  V_vac : ∀ s : ℝ, V s W.vac = W.vac
  V_translations : ∀ (s : ℝ) (a : Fin 4 → ℝ),
    (V s).conjStarAlgEquiv (W.U a) = W.U (wedgeBoostMap s a)
  V_net : ∀ (s : ℝ) (O : Set (Fin 4 → ℝ)) (T : W.H →L[ℂ] W.H),
    T ∈ W.net O → (V s).conjStarAlgEquiv T ∈ W.net (wedgeBoostMap s '' O)

/-! ## 3. CONTRATO H2 v3 -/

/-- **ContratoH2 W R** (v3) — o tipo que `qgPrice_H2_smoothModularFourFrame_discharged` terá de habitar.

    (A) κ > 0, a normalização do campo de Killing — AMARRADO por (K) e por `unruh_is_kms` (teorema).
    (Δ) `Δit`: o implementador em vetores do fluxo modular de R (`flow_implemented`).
    (KMS) Δit é O fluxo modular de (W.net cunha, W.vac): KMS a β = 1 para t ↦ Δit(−t).
    (S) A CLÁUSULA DE ESTADO v3, COMPATÍVEL COM ESPECTRO CONTÍNUO: nenhuma torre, nenhum isomorfismo com
        espaço de espectro pontual. O estado é W.vac; `boost` é o grupo de boosts representado em W.H e
        `bw` é Bisognano–Wichmann COMO CAMPO: Δ^{it} = V(Λ(−2πt)).
    (P) A REDE FÍSICA: translações fortemente contínuas, FIÉIS (o dente de W5), de ENERGIA POSITIVA, e
        ERGÓDICAS na direção nula (vetores invariantes por U(λn) estão em ℂΩ — [KNOWN] no campo livre).
    (K) o observador fiducial: na sua órbita |ξ_κ| = 1, logo κ = 1/ρ_obs (teorema).
    (C)(D)(E) o frame, como na v2: regional, arrastado pelo boost, fiducial ∝ ξ_κ. -/
structure ContratoH2 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W) where
  /-- (A) a normalização do campo de Killing. -/
  kappa : ℝ
  kappa_pos : 0 < kappa
  /-- (Δ) o implementador do fluxo de R em vetores. -/
  Δit : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)
  /-- (Δ) o fluxo da camada 1A de R É Ad(Δ^{it}). -/
  flow_implemented : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
    ((R.modular.modularFlow t) a).val = (Δit t).conjStarAlgEquiv a.val
  /-- (KMS) Δit é o grupo modular de (W.net rightWedge, W.vac): KMS a β = 1 para t ↦ Δit(−t). -/
  kms : KMSAt W (fun t => Δit (-t)) 1
  /-- (S) o grupo de boosts da cunha, representado em W.H. -/
  boost : WedgeBoostRep W
  /-- (S) BISOGNANO–WICHMANN COMO CAMPO: Δ^{it} = V(Λ(−2πt)). -/
  bw : ∀ t : ℝ, Δit t = boost.V (-(2 * Real.pi * t))
  /-- (P) translações fortemente contínuas. -/
  translations_continuous : ∀ ψ : W.H, Continuous (fun a : Fin 4 → ℝ => W.U a ψ)
  /-- (P) O DENTE DE FIDELIDADE: só a translação nula age trivialmente. -/
  translations_faithful : ∀ a : Fin 4 → ℝ, W.U a = 1 → a = 0
  /-- (P) energia positiva (condição espectral), forma analítica. -/
  positive_energy : PositiveEnergy W
  /-- (P) ergodicidade nula: os invariantes da translação nula são múltiplos do vácuo. -/
  null_ergodic : ∀ ψ : W.H, (∀ l : ℝ, W.U (l • nullDir) ψ = ψ) → ψ ∈ (ℂ ∙ W.vac)
  /-- (K) o observador fiducial, na cunha. -/
  observer : Fin 4 → ℝ
  observer_in_wedge : observer ∈ rightWedge
  /-- (K) na órbita do observador o campo de Killing tem norma 1: κ fica determinado (κ = 1/ρ_obs). -/
  observer_unit : minkowskiSq (killingField kappa observer) = 1
  /-- (C) o campo de frames, REGIONAL. -/
  E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  smooth_on : ∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => E x i j) rightWedge
  det_unit_on : ∀ x ∈ rightWedge, IsUnit (E x).det
  /-- (D) o jato: arrasto pelo diferencial da ação geométrica do boost. -/
  dragged : ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
    E (wedgeBoostMap s x) = boostMat s * E x
  /-- (E) a fiducial é a direção do tempo modular, positivamente. -/
  fiducial_is_modular : ∀ x ∈ rightWedge,
    ∃ c : ℝ, 0 < c ∧ (fun i => E x i 0) = c • killingField kappa x

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- a temperatura de Unruh em tempo de Killing — aqui ainda só o NÚMERO κ/2π; que ele É a temperatura
    KMS do fluxo de Killing é o teorema `unruh_is_kms` (arquivo de teoremas), não esta definição. -/
def unruhTemperature (C : ContratoH2 W R) : ℝ := C.kappa / (2 * Real.pi)

/-- o FLUXO DE KILLING do campo ξ_κ, em tempo de Killing τ: τ ↦ V(κτ). -/
def killingFlow (C : ContratoH2 W R) (τ : ℝ) : W.H ≃ₗᵢ[ℂ] W.H := C.boost.V (C.kappa * τ)

end ContratoH2

/-! ## 4. A geometria do horizonte da MESMA cunha, para um campo de frames QUALQUER -/

/-- o ponto do horizonte esticado: x = (λ, ε + λ, y², y³). -/
def horizonPoint (ε l : ℝ) (y : Fin 2 → ℝ) : Fin 4 → ℝ := ![l, ε + l, y 0, y 1]

theorem horizonPoint_mem_rightWedge {ε l : ℝ} (hε : 0 < ε) (hl : -ε / 2 < l) (y : Fin 2 → ℝ) :
    horizonPoint ε l y ∈ rightWedge := by
  show |(![l, ε + l, y 0, y 1] : Fin 4 → ℝ) 0| < (![l, ε + l, y 0, y 1] : Fin 4 → ℝ) 1
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
  rw [abs_lt]
  constructor <;> linarith

/-- o bloco (2,3) de uma métrica: a métrica induzida na tela. -/
def screenBlock (g : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![g 2 2, g 2 3; g 3 2, g 3 3]

/-- a área da tela S transladada nulamente por λ, na métrica soldada DO frame E (g = eᵀηe, e = E⁻¹). -/
def screenAreaOf (E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) (S : Set (Fin 2 → ℝ)) (ε l : ℝ) : ℝ :=
  ∫ y in S, Real.sqrt |(screenBlock (solderMetric4 (E (horizonPoint ε l y))⁻¹)).det|

/-- a variação de área ao longo do gerador nulo, no frame E: dA/dλ|_{λ=0}. -/
def areaVariationOf (E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) (S : Set (Fin 2 → ℝ)) (ε : ℝ) : ℝ :=
  deriv (fun l => screenAreaOf E S ε l) 0

/-- a RESPOSTA de área: variação no frame perturbado menos a do frame de fundo (o H2). -/
def deltaArea (E₀ E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) (S : Set (Fin 2 → ℝ)) (ε : ℝ) : ℝ :=
  areaVariationOf E S ε - areaVariationOf E₀ S ε

/-- o pareamento T(u, v) = uᵀ T v. -/
def pairing (A : Matrix (Fin 4) (Fin 4) ℝ) (u v : Fin 4 → ℝ) : ℝ := dotProduct u (A.mulVec v)

/-- o calor através do segmento [λ₀, 0] do horizonte, com o campo de Killing ξ_κ (Jacobson). -/
def horizonHeatK (κ : ℝ) (S : Set (Fin 2 → ℝ)) (ε l₀ : ℝ)
    (T : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) : ℝ :=
  ∫ l in l₀..(0:ℝ), ∫ y in S,
    pairing (T (horizonPoint ε l y)) (killingField κ (horizonPoint ε l y)) nullDir

/-! ## 5. CONTRATO H3 v3 -/

/-- **ContratoH3 W R** (v3) — o tipo que `qgPrice_H3_localHorizonEquilibrium_discharged` terá de habitar.

    O MESMO horizonte (o `H2`), G FIXO antes de qualquer perturbação (campo, precede o ∀ de `area_law`),
    a classe ADMISSÍVEL de perturbações (vetores unitários de W.H no domínio de forma do gerador do boost,
    contendo o vácuo e ao menos uma de energia de boost ≠ 0 — proíbe o balanço vazio 0 = 0), a RESPOSTA
    geométrica de cada estado (`response`, DADO amarrado: no vácuo é o frame de H2) e o tensor de matéria
    DE CADA ESTADO (`matter`, DADO amarrado pela energia de boost do estado: `matter_is_state`).
    δS := δ⟨K⟩ (primeira lei do emaranhamento) e δQ := calor de `matter ψ` — NÃO são campos livres.
    Clausius NÃO é campo: é teorema (`clausius`). Bekenstein–Hawking é `area_law`, para TODA perturbação
    admissível com o MESMO G. -/
structure ContratoH3 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W) where
  /-- o MESMO horizonte: o contrato H2 sobre o MESMO par (W, R). -/
  H2 : ContratoH2 W R
  /-- G [INPUT], fixo ANTES da perturbação. -/
  G : ℝ
  G_pos : 0 < G
  /-- a tela e o horizonte esticado da MESMA cunha [INPUT]. -/
  screen : Set (Fin 2 → ℝ)
  screen_measurable : MeasurableSet screen
  screen_pos : 0 < volume screen
  screen_finite : volume screen < ⊤
  eps : ℝ
  eps_pos : 0 < eps
  lam0 : ℝ
  lam0_neg : lam0 < 0
  lam0_in_wedge : -eps / 2 < lam0
  /-- a classe admissível de perturbações do MESMO estado. -/
  admissible : Set W.H
  admissible_unit : ∀ ψ ∈ admissible, ‖ψ‖ = 1
  vac_admissible : W.vac ∈ admissible
  admissible_energy : ∀ ψ ∈ admissible, ∃ b : ℝ, HasBoostEnergy H2.boost.V ψ b
  admissible_nontrivial : ∃ ψ ∈ admissible, ∃ b : ℝ, HasBoostEnergy H2.boost.V ψ b ∧ b ≠ 0
  /-- a resposta geométrica de cada estado (o frame perturbado) — DADO; no vácuo é o frame de H2. -/
  response : W.H → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  response_vac : response W.vac = H2.E
  response_det_unit_on : ∀ ψ ∈ admissible, ∀ x ∈ rightWedge, IsUnit (response ψ x).det
  area_differentiable : ∀ ψ ∈ admissible,
    DifferentiableAt ℝ (fun l => screenAreaOf (response ψ) screen eps l) 0
  /-- o tensor de matéria DE CADA ESTADO — DADO, amarrado pelo campo seguinte. -/
  matter : W.H → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  /-- A MATÉRIA É A DO ESTADO: o calor de Jacobson de `matter ψ` pelo MESMO ξ_κ é κ vezes a energia de
      boost de ψ. -/
  matter_is_state : ∀ ψ ∈ admissible, ∀ b : ℝ, HasBoostEnergy H2.boost.V ψ b →
    horizonHeatK H2.kappa screen eps lam0 (matter ψ) = H2.kappa * b
  /-- BEKENSTEIN–HAWKING NA PRIMEIRA LEI, com G fixo: para TODA perturbação admissível,
      δS = δ⟨K⟩ = δA/(4G). -/
  area_law : ∀ ψ ∈ admissible, ∀ k : ℝ, HasModularEnergy H2.Δit ψ k →
    k = deltaArea H2.E (response ψ) screen eps / (4 * G)

/-! ## 6. CONTRATO IMPORT-H3 v3 — INDEXADO pelo termo H2 do MESMO par -/

/-- **ContratoImportH3 W R h2** (v3) — o tipo que `qgImport_H3_horizonEquilibriumData_produced` terá de
    habitar, NO MOLDE `ContratoImportH3 W₀ R₀ qgPrice_H2_…`: o índice `h2` é o termo H2 do MESMO par, logo
    (i) o TIPO não se escreve sem um H2 (a sonda ex falso da v2 não tem onde morar) e (ii) o leitor pode
    exigir por tipo que o import foi instanciado com o H2 RESERVADO (gpf_H2). A função produz, de todo H2
    no par, um H3 sobre o MESMO H2 (Jacobson + BW + Unruh + primeira lei, importados). -/
structure ContratoImportH3 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (h2 : ContratoH2 W R) where
  produce : ContratoH2 W R → ContratoH3 W R
  same_horizon : ∀ h : ContratoH2 W R, (produce h).H2 = h

#print axioms boostMat_add
#print axioms boostMat_zero
#print axioms wedgeBoostMap_add
#print axioms wedgeBoostMap_zero
#print axioms wedgeBoostMap_smul
#print axioms wedgeBoostMap_nullDir
#print axioms horizonPoint_mem_rightWedge

end

end TGLExt.ContratoQGv3
