import ContratoQG_v3_Teoremas

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 4000000

/-!
# CÉTICO 2 (vacuidade/fidelidade) — H3 v3 é AJUSTÁVEL POR CONSTRUÇÃO, dado QUALQUER H2
  [DIAGNÓSTICO do cético; scratchpad cetico_vacuidade; nunca importado pelo kernel; NÃO cunha nome reservado]

  O `ProbeAjusteH3v3` do projetista mediu: «com UM estado e UM horizonte, H3 reduz-se à EXISTÊNCIA da
  resposta geométrica E₁ (δA = 8πG·b₁) e de um tensor T₁ (calor κ·b₁)» — e chamou isso de «a dívida real».
  Este arquivo mostra que essa existência é GRÁTIS, por fórmula explícita, e para QUALQUER classe
  admissível (quantos estados se queira), QUALQUER G > 0:

  * resposta: o frame E_a(x) = diag(1, 1, e^{−a x⁰}, e^{−a x⁰}); a área da tela vale vol(S)·e^{2aλ},
    logo dA/dλ|₀ = 2a·vol(S) — escolhe-se a POR ESTADO para dar δA = 8πG·b(ψ) (`expFrame`, `areaVariation_expFrame`);
  * matéria: o tensor constante c·e₀₀; o calor de Jacobson vale vol(S)·c·κ·D com D = −λ₀ε − λ₀²/2 > 0 —
    escolhe-se c POR ESTADO para dar κ·b(ψ) (`heat_e00`).

  Consequências [DERIVED]:
  * `adjustH3`: de QUALQUER H2 + uma tela onde a área do vácuo (do frame de H2) é derivável + uma classe
    admissível, sai um ContratoH3 com o G que se QUISER;
  * `G_is_free`: de QUALQUER habitante de H3 sai outro com o MESMO H2, a MESMA classe admissível, a MESMA
    tela e G' ARBITRÁRIO — `area_law` não restringe G nem liga a geometria ao estado;
  * `genericImport`: um termo de `ContratoImportH3 W R h2` SEM física de Jacobson — só com (i) um vetor
    unitário de energia de boost ≠ 0 (propriedade do PAR, `boost_V_determined`) e (ii) regularidade de área
    do vácuo de cada frame H2. Ou seja: pago H2 no par físico, gpf_H3 e gpi_H3 seriam pagos por AJUSTE.
-/

namespace TGLExt.ContratoQGv3.CeticoVacuidade

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open MeasureTheory Matrix Complex
open scoped InnerProductSpace Classical

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-! ## 1. A resposta geométrica explícita -/

/-- o frame exponencial E_a(x) = diag(1, 1, e^{−a x⁰}, e^{−a x⁰}). -/
def expFrame (a : ℝ) : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ :=
  fun x => Matrix.diagonal ![1, 1, Real.exp (-(a * x 0)), Real.exp (-(a * x 0))]

theorem expFrame_inv (a : ℝ) (x : Fin 4 → ℝ) :
    (expFrame a x)⁻¹ = Matrix.diagonal ![1, 1, Real.exp (a * x 0), Real.exp (a * x 0)] := by
  apply Matrix.inv_eq_left_inv
  unfold expFrame
  rw [Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
  congr 1
  funext i
  fin_cases i <;> simp [Real.exp_neg, Real.exp_ne_zero]

theorem expFrame_det_isUnit (a : ℝ) (x : Fin 4 → ℝ) : IsUnit (expFrame a x).det := by
  unfold expFrame
  rw [Matrix.det_diagonal, Fin.prod_univ_four]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.cons_val_three,
    Matrix.head_cons, Matrix.tail_cons, one_mul]
  exact isUnit_iff_ne_zero.mpr (by positivity)

theorem solder_expFrame (a : ℝ) (x : Fin 4 → ℝ) :
    solderMetric4 (expFrame a x)⁻¹ =
      Matrix.diagonal ![1, -1, -(Real.exp (a * x 0)) ^ 2, -(Real.exp (a * x 0)) ^ 2] := by
  rw [expFrame_inv]
  unfold solderMetric4 eta4
  rw [Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal, Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  fin_cases i <;> simp <;> ring

theorem screen_sqrt_expFrame (a : ℝ) (x : Fin 4 → ℝ) :
    Real.sqrt |(screenBlock (solderMetric4 (expFrame a x)⁻¹)).det| = Real.exp (2 * a * x 0) := by
  rw [solder_expFrame]
  unfold screenBlock
  rw [Matrix.det_fin_two_of]
  simp only [Matrix.diagonal_apply_eq, Matrix.cons_val_two, Matrix.cons_val_three,
    Matrix.head_cons, Matrix.tail_cons]
  have hoff : (Matrix.diagonal ![(1:ℝ), -1, -(Real.exp (a * x 0)) ^ 2, -(Real.exp (a * x 0)) ^ 2]) 2 3 = 0 := by
    simp
  have hoff' : (Matrix.diagonal ![(1:ℝ), -1, -(Real.exp (a * x 0)) ^ 2, -(Real.exp (a * x 0)) ^ 2]) 3 2 = 0 := by
    simp
  rw [hoff, hoff', mul_zero, sub_zero]
  have hsq : (-(Real.exp (a * x 0)) ^ 2) * (-(Real.exp (a * x 0)) ^ 2) = (Real.exp (2 * a * x 0)) ^ 2 := by
    rw [show (2 * a * x 0) = a * x 0 + a * x 0 by ring, Real.exp_add]
    ring
  rw [hsq, abs_of_nonneg (sq_nonneg _), Real.sqrt_sq (Real.exp_pos _).le]

theorem screenArea_expFrame (a : ℝ) (S : Set (Fin 2 → ℝ)) (ε l : ℝ) :
    screenAreaOf (expFrame a) S ε l = volume.real S * Real.exp (2 * a * l) := by
  unfold screenAreaOf
  have h : ∀ y : Fin 2 → ℝ,
      Real.sqrt |(screenBlock (solderMetric4 (expFrame a (horizonPoint ε l y))⁻¹)).det|
        = Real.exp (2 * a * l) := by
    intro y
    rw [screen_sqrt_expFrame]
    simp [horizonPoint]
  simp_rw [h]
  rw [setIntegral_const, smul_eq_mul]

theorem hasDerivAt_expArea (a μ : ℝ) :
    HasDerivAt (fun l : ℝ => μ * Real.exp (2 * a * l)) (μ * (2 * a)) 0 := by
  have h1 : HasDerivAt (fun l : ℝ => 2 * a * l) (2 * a) 0 := by
    simpa using (hasDerivAt_id (0:ℝ)).const_mul (2 * a)
  have h2 := (h1.exp).const_mul μ
  refine h2.congr_deriv ?_
  simp

theorem areaVariation_expFrame (a : ℝ) (S : Set (Fin 2 → ℝ)) (ε : ℝ) :
    areaVariationOf (expFrame a) S ε = volume.real S * (2 * a) := by
  unfold areaVariationOf
  have hf : (fun l => screenAreaOf (expFrame a) S ε l) = fun l => volume.real S * Real.exp (2 * a * l) := by
    funext l; exact screenArea_expFrame a S ε l
  rw [hf]
  exact (hasDerivAt_expArea a _).deriv

theorem area_differentiable_expFrame (a : ℝ) (S : Set (Fin 2 → ℝ)) (ε : ℝ) :
    DifferentiableAt ℝ (fun l => screenAreaOf (expFrame a) S ε l) 0 := by
  have hf : (fun l => screenAreaOf (expFrame a) S ε l) = fun l => volume.real S * Real.exp (2 * a * l) := by
    funext l; exact screenArea_expFrame a S ε l
  rw [hf]
  exact (hasDerivAt_expArea a _).differentiableAt

/-! ## 2. A matéria explícita -/

/-- o tensor e₀₀. -/
def e00 : Matrix (Fin 4) (Fin 4) ℝ := Matrix.of fun i j => if i = 0 ∧ j = 0 then 1 else 0

theorem pairing_e00 (c : ℝ) (u : Fin 4 → ℝ) : pairing (c • e00) u nullDir = c * u 0 := by
  simp [pairing, e00, Matrix.mulVec, dotProduct, Fin.sum_univ_four, nullDir]
  ring

/-- o fator geométrico do calor: D = −λ₀ε − λ₀²/2. -/
def heatFactor (ε l0 : ℝ) : ℝ := -(l0 * ε) - l0 ^ 2 / 2

theorem heatFactor_pos {ε l0 : ℝ} (hε : 0 < ε) (h1 : l0 < 0) (h2 : -ε / 2 < l0) : 0 < heatFactor ε l0 := by
  unfold heatFactor
  nlinarith

theorem heat_e00 (κ c : ℝ) (S : Set (Fin 2 → ℝ)) (ε l0 : ℝ) :
    horizonHeatK κ S ε l0 (fun _ => c • e00) = volume.real S * c * κ * heatFactor ε l0 := by
  unfold horizonHeatK
  have hin : ∀ l : ℝ, (∫ y in S, pairing ((fun _ => c • e00) (horizonPoint ε l y))
      (killingField κ (horizonPoint ε l y)) nullDir) = volume.real S * c * κ * (ε + l) := by
    intro l
    have hp : ∀ y : Fin 2 → ℝ, pairing ((fun _ => c • e00) (horizonPoint ε l y))
        (killingField κ (horizonPoint ε l y)) nullDir = c * κ * (ε + l) := by
      intro y
      simp only
      rw [pairing_e00]
      simp [killingField, horizonPoint]
      ring
    simp_rw [hp]
    rw [setIntegral_const, smul_eq_mul]
    ring
  simp_rw [hin]
  have hsplit : (∫ x in l0..(0:ℝ), ε + x) = (∫ x in l0..(0:ℝ), ε) + ∫ x in l0..(0:ℝ), x :=
    intervalIntegral.integral_add (continuous_const.intervalIntegrable _ _)
      (continuous_id'.intervalIntegrable _ _)
  rw [intervalIntegral.integral_const_mul, hsplit, intervalIntegral.integral_const, integral_id]
  unfold heatFactor
  simp only [smul_eq_mul]
  ring

/-! ## 3. A energia de boost escolhida -/

theorem boostEnergy_unique' {V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)} {ψ : W.H} {b b' : ℝ}
    (h : HasBoostEnergy V ψ b) (h' : HasBoostEnergy V ψ b') : b = b' := by
  have hu := h.unique h'
  have : (b : ℂ) = b' := mul_left_cancel₀ Complex.I_ne_zero hu
  exact_mod_cast this

/-- a energia de boost de ψ, quando existe (0 caso contrário). -/
def bOf (V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) (ψ : W.H) : ℝ :=
  if h : ∃ b : ℝ, HasBoostEnergy V ψ b then Classical.choose h else 0

theorem bOf_spec {V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)} {ψ : W.H} {b : ℝ} (hb : HasBoostEnergy V ψ b) :
    bOf V ψ = b := by
  have hex : ∃ b : ℝ, HasBoostEnergy V ψ b := ⟨b, hb⟩
  unfold bOf
  rw [dif_pos hex]
  exact boostEnergy_unique' (Classical.choose_spec hex) hb

/-! ## 4. O AJUSTADOR -/

/-- os dados de tela para um H2: uma tela, um ε, e a derivabilidade da área do VÁCUO no frame de H2. -/
structure AdjData (h : ContratoH2 W R) where
  S : Set (Fin 2 → ℝ)
  S_meas : MeasurableSet S
  S_pos : 0 < volume S
  S_fin : volume S < ⊤
  eps : ℝ
  eps_pos : 0 < eps
  vac_diff : DifferentiableAt ℝ (fun l => screenAreaOf h.E S eps l) 0

theorem AdjData.mu_pos {h : ContratoH2 W R} (D : AdjData h) : 0 < volume.real D.S := by
  rw [measureReal_def]
  exact ENNReal.toReal_pos D.S_pos.ne' D.S_fin.ne

/-- a inclinação escolhida POR ESTADO: dá δA = 8πG·b(ψ). -/
def slope (h : ContratoH2 W R) (G : ℝ) (D : AdjData h) (ψ : W.H) : ℝ :=
  (8 * Real.pi * G * bOf h.boost.V ψ + areaVariationOf h.E D.S D.eps) / (2 * volume.real D.S)

/-- ★★★ O AJUSTADOR: de QUALQUER H2, QUALQUER G > 0, QUALQUER tela com área do vácuo derivável e QUALQUER
    classe admissível que cumpra as cláusulas de classe, um habitante de ContratoH3 sobre o MESMO H2. -/
def adjustH3 (h : ContratoH2 W R) (G : ℝ) (hG : 0 < G) (D : AdjData h)
    (A : Set W.H) (hAu : ∀ ψ ∈ A, ‖ψ‖ = 1) (hAv : W.vac ∈ A)
    (hAe : ∀ ψ ∈ A, ∃ b : ℝ, HasBoostEnergy h.boost.V ψ b)
    (hAn : ∃ ψ ∈ A, ∃ b : ℝ, HasBoostEnergy h.boost.V ψ b ∧ b ≠ 0) : ContratoH3 W R where
  H2 := h
  G := G
  G_pos := hG
  screen := D.S
  screen_measurable := D.S_meas
  screen_pos := D.S_pos
  screen_finite := D.S_fin
  eps := D.eps
  eps_pos := D.eps_pos
  lam0 := -(D.eps / 4)
  lam0_neg := by have := D.eps_pos; linarith
  lam0_in_wedge := by have := D.eps_pos; linarith
  admissible := A
  admissible_unit := hAu
  vac_admissible := hAv
  admissible_energy := hAe
  admissible_nontrivial := hAn
  response := fun ψ => if ψ = W.vac then h.E else expFrame (slope h G D ψ)
  response_vac := by simp
  response_det_unit_on := by
    intro ψ hψ x hx
    by_cases hv : ψ = W.vac
    · simp only [hv, if_true]; exact h.det_unit_on x hx
    · simp only [hv, if_false]; exact expFrame_det_isUnit _ x
  area_differentiable := by
    intro ψ hψ
    by_cases hv : ψ = W.vac
    · simp only [hv, if_true]; exact D.vac_diff
    · simp only [hv, if_false]; exact area_differentiable_expFrame _ _ _
  matter := fun ψ => fun _ => (bOf h.boost.V ψ / (volume.real D.S * heatFactor D.eps (-(D.eps / 4)))) • e00
  matter_is_state := by
    intro ψ hψ b hb
    rw [heat_e00, bOf_spec hb]
    have hμ := D.mu_pos
    have hD : 0 < heatFactor D.eps (-(D.eps / 4)) :=
      heatFactor_pos D.eps_pos (by have := D.eps_pos; linarith) (by have := D.eps_pos; linarith)
    field_simp
  area_law := by
    intro ψ hψ k hk
    by_cases hv : ψ = W.vac
    · subst hv
      have hk0 : k = 0 := ContratoH2.modularEnergy_unique hk h.vac_modularEnergy
      simp [deltaArea, hk0]
    · obtain ⟨b, hb⟩ := hAe ψ hψ
      have hk1 : k = 2 * Real.pi * b :=
        ContratoH2.modularEnergy_unique hk (h.modularEnergy_of_boostEnergy hb)
      simp only [hv, if_false]
      unfold deltaArea
      rw [areaVariation_expFrame]
      unfold slope
      rw [bOf_spec hb, hk1]
      have hμ := D.mu_pos
      field_simp
      ring

/-- ★★ G É UM BOTÃO LIVRE: de QUALQUER habitante de H3 sai outro com o MESMO H2, a MESMA classe
    admissível, a MESMA tela e G' arbitrário. -/
theorem G_is_free (C : ContratoH3 W R) (G' : ℝ) (hG' : 0 < G') :
    ∃ C' : ContratoH3 W R, C'.H2 = C.H2 ∧ C'.G = G' ∧ C'.admissible = C.admissible ∧
      C'.screen = C.screen ∧ C'.eps = C.eps := by
  let D : AdjData C.H2 :=
    { S := C.screen
      S_meas := C.screen_measurable
      S_pos := C.screen_pos
      S_fin := C.screen_finite
      eps := C.eps
      eps_pos := C.eps_pos
      vac_diff := by
        have := C.area_differentiable W.vac C.vac_admissible
        rwa [C.response_vac] at this }
  exact ⟨adjustH3 C.H2 G' hG' D C.admissible C.admissible_unit C.vac_admissible C.admissible_energy
    C.admissible_nontrivial, rfl, rfl, rfl, rfl, rfl⟩

/-- ★★ H3 A PARTIR DE H2, com UM vetor de energia de boost ≠ 0 e a regularidade de área do vácuo: nada de
    Jacobson, nada de Einstein, G qualquer. -/
theorem H3_of_H2 (h : ContratoH2 W R) (D : AdjData h) (G : ℝ) (hG : 0 < G)
    (ψ₁ : W.H) (hψ₁ : ‖ψ₁‖ = 1) (b₁ : ℝ) (hb₁ : HasBoostEnergy h.boost.V ψ₁ b₁) (hb0 : b₁ ≠ 0) :
    ∃ C : ContratoH3 W R, C.H2 = h ∧ C.G = G := by
  refine ⟨adjustH3 h G hG D {W.vac, ψ₁} ?_ (Set.mem_insert _ _) ?_ ⟨ψ₁, Set.mem_insert_of_mem _ rfl, b₁, hb₁, hb0⟩,
    rfl, rfl⟩
  · intro ψ hψ
    rcases hψ with hv | hv
    · rw [hv]; exact W.vac_norm
    · rw [Set.mem_singleton_iff.mp hv]; exact hψ₁
  · intro ψ hψ
    rcases hψ with hv | hv
    · rw [hv]; exact ⟨0, h.vac_boostEnergy⟩
    · rw [Set.mem_singleton_iff.mp hv]; exact ⟨b₁, hb₁⟩

/-! ## 5. O grupo de boosts é do PAR (não do termo H2) -/

/-- [DERIVED] dois habitantes de H2 no MESMO par têm o MESMO grupo de boosts (V(s) = Δit(−s/2π), e Δit é
    único). Logo «existe vetor de energia de boost ≠ 0» é propriedade do PAR. -/
theorem boost_V_determined (C C' : ContratoH2 W R) : C.boost.V = C'.boost.V := by
  funext s
  have h1 := C.bw (-(s / (2 * Real.pi)))
  have h2 := C'.bw (-(s / (2 * Real.pi)))
  have hs : -(2 * Real.pi * -(s / (2 * Real.pi))) = s := by
    have : (2 * Real.pi) ≠ 0 := by positivity
    field_simp
  rw [hs] at h1 h2
  rw [← h1, ← h2, ContratoH2.Δit_determined C C']

/-! ## 6. O IMPORT GENÉRICO (sem física) -/

/-- ★★★ UM TERMO DE `ContratoImportH3 W R h2` SEM JACOBSON: basta (i) um vetor unitário de energia de boost
    ≠ 0 (propriedade do par) e (ii) para cada frame H2 uma tela com área do vácuo derivável. -/
def genericImport (h2 : ContratoH2 W R)
    (ψ₁ : W.H) (hψ₁ : ‖ψ₁‖ = 1) (b₁ : ℝ) (hb₁ : HasBoostEnergy h2.boost.V ψ₁ b₁) (hb0 : b₁ ≠ 0)
    (hD : ∀ h : ContratoH2 W R, AdjData h) : ContratoImportH3 W R h2 where
  produce := fun h =>
    adjustH3 h 1 one_pos (hD h) {W.vac, ψ₁}
      (by
        intro ψ hψ
        rcases hψ with hv | hv
        · rw [hv]; exact W.vac_norm
        · rw [Set.mem_singleton_iff.mp hv]; exact hψ₁)
      (Set.mem_insert _ _)
      (by
        intro ψ hψ
        rcases hψ with hv | hv
        · rw [hv]; exact ⟨0, h.vac_boostEnergy⟩
        · rw [Set.mem_singleton_iff.mp hv, boost_V_determined h h2]; exact ⟨b₁, hb₁⟩)
      ⟨ψ₁, Set.mem_insert_of_mem _ rfl, b₁, by rw [boost_V_determined h h2]; exact hb₁, hb0⟩
  same_horizon := fun h => rfl

/-- [DERIVED] ★ leitura: pago H2 no par (com as duas regularidades), gpf_H3 e gpi_H3 seriam pagos por ajuste. -/
theorem import_is_adjustment (h2 : ContratoH2 W R)
    (ψ₁ : W.H) (hψ₁ : ‖ψ₁‖ = 1) (b₁ : ℝ) (hb₁ : HasBoostEnergy h2.boost.V ψ₁ b₁) (hb0 : b₁ ≠ 0)
    (hD : ∀ h : ContratoH2 W R, AdjData h) :
    Nonempty (ContratoImportH3 W R h2) ∧ Nonempty (ContratoH3 W R) :=
  ⟨⟨genericImport h2 ψ₁ hψ₁ b₁ hb₁ hb0 hD⟩, ⟨(genericImport h2 ψ₁ hψ₁ b₁ hb₁ hb0 hD).produce h2⟩⟩

#print axioms expFrame_inv
#print axioms expFrame_det_isUnit
#print axioms solder_expFrame
#print axioms screen_sqrt_expFrame
#print axioms screenArea_expFrame
#print axioms areaVariation_expFrame
#print axioms area_differentiable_expFrame
#print axioms pairing_e00
#print axioms heat_e00
#print axioms bOf_spec
#print axioms adjustH3
#print axioms G_is_free
#print axioms H3_of_H2
#print axioms boost_V_determined
#print axioms genericImport
#print axioms import_is_adjustment

end

end TGLExt.ContratoQGv3.CeticoVacuidade
