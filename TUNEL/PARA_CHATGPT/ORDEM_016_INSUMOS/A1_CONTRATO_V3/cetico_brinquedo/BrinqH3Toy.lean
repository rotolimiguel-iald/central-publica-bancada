import ContratoQG_v3_Teoremas
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 4000000

/-!
# BrinqH3Toy — H3 v3 HABITADO POR BRINQUEDO DADO UM H2   [CÉTICO 1 / lente BRINQUEDO; DEVE COMPILAR]
  Cético 1 do contrato v3, 23/09/2026. Scratchpad. NÃO cunha nome reservado; nada move o gate.

  O projetista mediu (`ProbeAjusteH3v3.residualH3`) que H3 v3 é habitado SE houver um frame E₁ com
  δA = 8πG·b₁ e um tensor T₁ com calor κ·b₁ — e deixou E₁, T₁ como HIPÓTESES. Este arquivo DESCARREGA as duas
  hipóteses com objetos de brinquedo e vai além:

  * a resposta de área é um frame DIAGONAL FEITO À MÃO, `toyResp c x = diag(1, 1, e^{−c x⁰}, 1)`, com c
    AJUSTADO estado a estado para que δA = 8πG·b(ψ);
  * a matéria é um tensor CONSTANTE `diag(m, 0, 0, 0)`, com m AJUSTADO estado a estado (m = 32 b(ψ)/7);
  * a classe admissível é a MÁXIMA: TODO vetor unitário no domínio de forma do gerador do boost;
  * G é QUALQUER número positivo, escolhido DEPOIS do H2.

  Se este arquivo compila: dado QUALQUER habitante hipotético C2 de `ContratoH2 W R`, um vetor com energia
  de boost ≠ 0 ([KNOWN]: existe sempre que V ≠ 1, por Stone) e a regularidade da área do frame de C2 na
  tela (que o frame `geoFrame` usado em todos os probes PAGA, provado abaixo), então `ContratoH3 W R` é
  habitado para TODO G > 0 com dados de brinquedo. Logo H3 v3 NÃO acrescenta conteúdo físico a H2: a lei de
  área e o calor do estado são satisfeitos por AJUSTE de dados, e o defeito da v2 que o cético final de W2
  mediu («BH e Clausius AJUSTÁVEIS dado um H2») SOBREVIVE na v3. O import indexado também é fabricável.

  Estatutos: tudo [DERIVED] aqui (condicional ao habitante hipotético C2, que não existe no kernel).
  Sem sorry, sem axiom. β jamais aparece.
-/

namespace TGLExt.ContratoQGv3.CeticoBrinquedo

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open MeasureTheory Complex Matrix
open scoped InnerProductSpace

noncomputable section

/-! ## 1. O frame de resposta de brinquedo e a sua área -/

/-- o frame de resposta FEITO À MÃO: diagonal, com o fator e^{−c x⁰} na direção 2. -/
def toyResp (c : ℝ) (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal ![1, 1, Real.exp (-(c * x 0)), 1]

def toyRespInv (c : ℝ) (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal ![1, 1, Real.exp (c * x 0), 1]

theorem toyResp_inv (c : ℝ) (x : Fin 4 → ℝ) : (toyResp c x)⁻¹ = toyRespInv c x := by
  apply Matrix.inv_eq_left_inv
  unfold toyResp toyRespInv
  rw [Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
  congr 1
  funext i
  fin_cases i <;> simp [← Real.exp_add]

theorem toyResp_det (c : ℝ) (x : Fin 4 → ℝ) : (toyResp c x).det = Real.exp (-(c * x 0)) := by
  unfold toyResp
  rw [Matrix.det_diagonal, Fin.prod_univ_four]
  simp

theorem toyResp_det_unit (c : ℝ) (x : Fin 4 → ℝ) : IsUnit (toyResp c x).det := by
  rw [toyResp_det]
  exact isUnit_iff_ne_zero.mpr (Real.exp_pos _).ne'

theorem toy_screen_det (c : ℝ) (x : Fin 4 → ℝ) :
    (screenBlock (solderMetric4 (toyResp c x)⁻¹)).det = Real.exp (c * x 0) ^ 2 := by
  rw [toyResp_inv]
  unfold screenBlock solderMetric4 toyRespInv eta4
  rw [Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal, Matrix.diagonal_mul_diagonal,
    Matrix.det_fin_two_of]
  simp [Matrix.diagonal_apply]
  ring

/-- ★ a área da tela [0,1]² no frame de brinquedo, ao longo do gerador nulo: A(λ) = e^{cλ}. -/
theorem toy_area (c l : ℝ) : screenAreaOf (toyResp c) (Set.Icc 0 1) 1 l = Real.exp (c * l) := by
  unfold screenAreaOf
  have hpt : ∀ y : Fin 2 → ℝ,
      Real.sqrt |(screenBlock (solderMetric4 (toyResp c (horizonPoint 1 l y))⁻¹)).det|
        = Real.exp (c * l) := by
    intro y
    rw [toy_screen_det]
    have h0 : (horizonPoint 1 l y) 0 = l := by simp [horizonPoint]
    rw [h0, abs_of_nonneg (sq_nonneg _), Real.sqrt_sq (Real.exp_pos _).le]
  simp_rw [hpt]
  rw [setIntegral_const]
  simp [Measure.real, Real.volume_Icc_pi]

theorem toy_hasDeriv (c : ℝ) : HasDerivAt (fun l => Real.exp (c * l)) c 0 := by
  have h := ((hasDerivAt_id (0:ℝ)).const_mul c).exp
  simpa using h

/-- ★ a variação de área do frame de brinquedo é EXATAMENTE o parâmetro c (à escolha). -/
theorem toy_areaVariation (c : ℝ) : areaVariationOf (toyResp c) (Set.Icc 0 1) 1 = c := by
  unfold areaVariationOf
  have hf : (fun l => screenAreaOf (toyResp c) (Set.Icc 0 1) 1 l) = fun l => Real.exp (c * l) := by
    funext l; exact toy_area c l
  rw [hf]
  exact (toy_hasDeriv c).deriv

theorem toy_area_differentiable (c : ℝ) :
    DifferentiableAt ℝ (fun l => screenAreaOf (toyResp c) (Set.Icc 0 1) 1 l) 0 := by
  have hf : (fun l => screenAreaOf (toyResp c) (Set.Icc 0 1) 1 l) = fun l => Real.exp (c * l) := by
    funext l; exact toy_area c l
  rw [hf]
  exact (toy_hasDeriv c).differentiableAt

/-! ## 2. A matéria de brinquedo: um tensor CONSTANTE -/

def toyMatter (m : ℝ) : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ :=
  fun _ => Matrix.diagonal ![m, 0, 0, 0]

/-- ★ o calor de Jacobson do tensor constante na janela [−1/4, 0] da tela [0,1]², ε = 1: κ·m·7/32. -/
theorem toy_heat (κ m : ℝ) :
    horizonHeatK κ (Set.Icc 0 1) 1 (-1 / 4) (toyMatter m) = κ * m * (7 / 32) := by
  unfold horizonHeatK
  have hpt : ∀ (l : ℝ) (y : Fin 2 → ℝ),
      pairing (toyMatter m (horizonPoint 1 l y)) (killingField κ (horizonPoint 1 l y)) nullDir
        = κ * m * (1 + l) := by
    intro l y
    simp [pairing, toyMatter, killingField, horizonPoint, nullDir, Matrix.mulVec, dotProduct,
      Fin.sum_univ_four, Matrix.diagonal_apply]
    ring
  simp_rw [hpt]
  have hin : ∀ l : ℝ, ∫ y in (Set.Icc (0 : Fin 2 → ℝ) 1), κ * m * (1 + l) = κ * m * (1 + l) := by
    intro l
    rw [setIntegral_const]
    simp [Measure.real, Real.volume_Icc_pi]
  simp_rw [hin]
  have hF : ∀ x ∈ Set.uIcc (-1 / 4 : ℝ) 0,
      HasDerivAt (fun l : ℝ => κ * m * (l + l ^ 2 / 2)) (κ * m * (1 + x)) x := by
    intro x _
    have h1 : HasDerivAt (fun l : ℝ => l + l ^ 2 / 2) (1 + x) x :=
      ((hasDerivAt_id x).add ((hasDerivAt_pow 2 x).div_const 2)).congr_deriv (by norm_num)
    exact h1.const_mul (κ * m)
  have hint : IntervalIntegrable (fun l : ℝ => κ * m * (1 + l)) volume (-1 / 4) 0 :=
    (by fun_prop : Continuous fun l : ℝ => κ * m * (1 + l)).intervalIntegrable _ _
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hF hint]
  ring

/-! ## 3. A energia de boost escolhida (única quando existe) -/

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

theorem boostEnergy_unique' {V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)} {ψ : W.H} {b b' : ℝ}
    (h : HasBoostEnergy V ψ b) (h' : HasBoostEnergy V ψ b') : b = b' := by
  have hu := h.unique h'
  have : (b : ℂ) = b' := mul_left_cancel₀ Complex.I_ne_zero hu
  exact_mod_cast this

open Classical in
def bOf (V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) (ψ : W.H) : ℝ :=
  if h : ∃ b : ℝ, HasBoostEnergy V ψ b then Classical.choose h else 0

theorem bOf_spec {V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)} {ψ : W.H} {b : ℝ} (h : HasBoostEnergy V ψ b) :
    bOf V ψ = b := by
  classical
  have hex : ∃ b : ℝ, HasBoostEnergy V ψ b := ⟨b, h⟩
  unfold bOf
  rw [dif_pos hex]
  exact boostEnergy_unique' (Classical.choose_spec hex) h

/-! ## 4. ★★★ O H3 DE BRINQUEDO, com a classe admissível MÁXIMA e G QUALQUER -/

/-- o parâmetro de área ajustado ao estado: c(ψ) = A₀' + 8πG·b(ψ). -/
def fitC (C2 : ContratoH2 W R) (G : ℝ) (ψ : W.H) : ℝ :=
  areaVariationOf C2.E (Set.Icc 0 1) 1 + 8 * Real.pi * G * bOf C2.boost.V ψ

open Classical in
def toyH3 (C2 : ContratoH2 W R) (G : ℝ) (hG : 0 < G)
    (hd₀ : DifferentiableAt ℝ (fun l => screenAreaOf C2.E (Set.Icc 0 1) 1 l) 0)
    (hnt : ∃ ψ : W.H, ‖ψ‖ = 1 ∧ ∃ b : ℝ, HasBoostEnergy C2.boost.V ψ b ∧ b ≠ 0) :
    ContratoH3 W R where
  H2 := C2
  G := G
  G_pos := hG
  screen := Set.Icc 0 1
  screen_measurable := measurableSet_Icc
  screen_pos := by rw [Real.volume_Icc_pi]; simp
  screen_finite := by rw [Real.volume_Icc_pi]; simp
  eps := 1
  eps_pos := one_pos
  lam0 := -1 / 4
  lam0_neg := by norm_num
  lam0_in_wedge := by norm_num
  admissible := {ψ | ‖ψ‖ = 1 ∧ ∃ b : ℝ, HasBoostEnergy C2.boost.V ψ b}
  admissible_unit := fun ψ h => h.1
  vac_admissible := ⟨W.vac_norm, 0, C2.vac_boostEnergy⟩
  admissible_energy := fun ψ h => h.2
  admissible_nontrivial := by
    obtain ⟨ψ, h1, b, hb, hb0⟩ := hnt
    exact ⟨ψ, ⟨h1, b, hb⟩, b, hb, hb0⟩
  response := fun ψ => if ψ = W.vac then C2.E else toyResp (fitC C2 G ψ)
  response_vac := by simp
  response_det_unit_on := by
    intro ψ hψ x hx
    by_cases h : ψ = W.vac
    · simp only [h, if_true]; exact C2.det_unit_on x hx
    · simp only [h, if_false]; exact toyResp_det_unit _ x
  area_differentiable := by
    intro ψ hψ
    by_cases h : ψ = W.vac
    · simp only [h, if_true]; exact hd₀
    · simp only [h, if_false]; exact toy_area_differentiable _
  matter := fun ψ => toyMatter (32 / 7 * bOf C2.boost.V ψ)
  matter_is_state := by
    intro ψ hψ b hb
    show horizonHeatK C2.kappa (Set.Icc 0 1) 1 (-1 / 4) (toyMatter (32 / 7 * bOf C2.boost.V ψ))
      = C2.kappa * b
    rw [toy_heat, bOf_spec hb]
    ring
  area_law := by
    intro ψ hψ k hk
    obtain ⟨_, b, hb⟩ := hψ
    have hk' : k = 2 * Real.pi * b :=
      ContratoH2.modularEnergy_unique hk (C2.modularEnergy_of_boostEnergy hb)
    by_cases hv : ψ = W.vac
    · subst hv
      have hb0 : b = 0 := boostEnergy_unique' hb C2.vac_boostEnergy
      simp [deltaArea, hk', hb0]
    · simp only [hv, if_false]
      unfold deltaArea
      rw [toy_areaVariation]
      unfold fitC
      rw [bOf_spec hb, hk']
      field_simp
      ring

/-- ★★★ H3 v3 NÃO ACRESCENTA CONTEÚDO A H2: dado um H2 (+ um vetor de energia de boost ≠ 0 + a regularidade
    da área do frame de H2), há habitante de H3 com o MESMO horizonte para CADA G > 0. -/
theorem H3_toy_for_every_G (C2 : ContratoH2 W R)
    (hd₀ : DifferentiableAt ℝ (fun l => screenAreaOf C2.E (Set.Icc 0 1) 1 l) 0)
    (hnt : ∃ ψ : W.H, ‖ψ‖ = 1 ∧ ∃ b : ℝ, HasBoostEnergy C2.boost.V ψ b ∧ b ≠ 0) :
    ∀ G : ℝ, 0 < G → ∃ H : ContratoH3 W R, H.H2 = C2 ∧ H.G = G :=
  fun G hG => ⟨toyH3 C2 G hG hd₀ hnt, rfl, rfl⟩

/-- a classe admissível do brinquedo é a MÁXIMA do tipo (todo vetor unitário com energia de boost). -/
theorem toyH3_admissible_maximal (C2 : ContratoH2 W R) (G : ℝ) (hG : 0 < G)
    (hd₀ : DifferentiableAt ℝ (fun l => screenAreaOf C2.E (Set.Icc 0 1) 1 l) 0)
    (hnt : ∃ ψ : W.H, ‖ψ‖ = 1 ∧ ∃ b : ℝ, HasBoostEnergy C2.boost.V ψ b ∧ b ≠ 0)
    (H : ContratoH3 W R) (hH : H.H2 = C2) :
    H.admissible ⊆ (toyH3 C2 G hG hd₀ hnt).admissible := by
  intro ψ hψ
  refine ⟨H.admissible_unit ψ hψ, ?_⟩
  obtain ⟨b, hb⟩ := H.admissible_energy ψ hψ
  subst hH
  exact ⟨b, hb⟩

/-- a resposta de área do brinquedo, fora do vácuo, é o frame DIAGONAL FEITO À MÃO (não lê o estado
    senão pelo número b(ψ)). -/
theorem toyH3_response_is_handmade (C2 : ContratoH2 W R) (G : ℝ) (hG : 0 < G)
    (hd₀ : DifferentiableAt ℝ (fun l => screenAreaOf C2.E (Set.Icc 0 1) 1 l) 0)
    (hnt : ∃ ψ : W.H, ‖ψ‖ = 1 ∧ ∃ b : ℝ, HasBoostEnergy C2.boost.V ψ b ∧ b ≠ 0)
    (ψ : W.H) (hψ : ψ ≠ W.vac) :
    (toyH3 C2 G hG hd₀ hnt).response ψ = toyResp (fitC C2 G ψ) := by
  classical
  show (if ψ = W.vac then C2.E else toyResp (fitC C2 G ψ)) = toyResp (fitC C2 G ψ)
  rw [if_neg hψ]

/-! ## 5. A regularidade que falta é PAGA pelo frame dos probes (`geoFrame`) -/

open W5Final.Toy in
def geoInv (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![x 1 / (x 1 ^ 2 - x 0 ^ 2), -(x 0) / (x 1 ^ 2 - x 0 ^ 2), 0, 0;
     -(x 0) / (x 1 ^ 2 - x 0 ^ 2), x 1 / (x 1 ^ 2 - x 0 ^ 2), 0, 0;
     0, 0, 1, 0;
     0, 0, 0, 1]

open W5Final.Toy in
theorem geoFrame_inv {x : Fin 4 → ℝ} (hd : x 1 ^ 2 - x 0 ^ 2 ≠ 0) : (geoFrame x)⁻¹ = geoInv x := by
  apply Matrix.inv_eq_left_inv
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [geoInv, geoFrame, Matrix.mul_apply, Fin.sum_univ_four] <;> field_simp <;> ring

open W5Final.Toy in
theorem geoFrame_screen_det {x : Fin 4 → ℝ} (hd : x 1 ^ 2 - x 0 ^ 2 ≠ 0) :
    (screenBlock (solderMetric4 (geoFrame x)⁻¹)).det = 1 := by
  rw [geoFrame_inv hd]
  unfold screenBlock solderMetric4 eta4
  rw [Matrix.det_fin_two_of]
  simp [geoInv, Matrix.mul_apply, Fin.sum_univ_four, Matrix.diagonal_apply]

open W5Final.Toy in
/-- ★ no frame dos probes a área da tela é CONSTANTE (= 1) perto de λ = 0. -/
theorem geoFrame_area_const {l : ℝ} (hl : -1 / 2 < l) :
    screenAreaOf geoFrame (Set.Icc 0 1) 1 l = 1 := by
  unfold screenAreaOf
  have hpt : ∀ y : Fin 2 → ℝ,
      Real.sqrt |(screenBlock (solderMetric4 (geoFrame (horizonPoint 1 l y))⁻¹)).det| = 1 := by
    intro y
    have hd : (horizonPoint 1 l y) 1 ^ 2 - (horizonPoint 1 l y) 0 ^ 2 ≠ 0 := by
      simp [horizonPoint]
      nlinarith
    rw [geoFrame_screen_det hd]
    simp
  simp_rw [hpt]
  rw [setIntegral_const]
  simp [Measure.real, Real.volume_Icc_pi]

open W5Final.Toy in
theorem geoFrame_area_differentiable :
    DifferentiableAt ℝ (fun l => screenAreaOf geoFrame (Set.Icc 0 1) 1 l) 0 := by
  have hev : (fun l => screenAreaOf geoFrame (Set.Icc 0 1) 1 l) =ᶠ[nhds 0] fun _ => (1 : ℝ) := by
    have : Set.Ioi (-1 / 2 : ℝ) ∈ nhds (0 : ℝ) := Ioi_mem_nhds (by norm_num)
    filter_upwards [this] with l hl
    exact geoFrame_area_const hl
  exact (differentiableAt_const (1 : ℝ)).congr_of_eventuallyEq hev

open W5Final.Toy in
/-- ★★★ COROLÁRIO SEM HIPÓTESE DE REGULARIDADE: para todo H2 cujo frame é o `geoFrame` dos probes, e um vetor
    de energia de boost ≠ 0, H3 v3 é habitado por brinquedo para CADA G > 0. -/
theorem H3_toy_on_geoFrame (C2 : ContratoH2 W R) (hE : C2.E = geoFrame)
    (hnt : ∃ ψ : W.H, ‖ψ‖ = 1 ∧ ∃ b : ℝ, HasBoostEnergy C2.boost.V ψ b ∧ b ≠ 0) :
    ∀ G : ℝ, 0 < G → ∃ H : ContratoH3 W R, H.H2 = C2 ∧ H.G = G := by
  have hd₀ : DifferentiableAt ℝ (fun l => screenAreaOf C2.E (Set.Icc 0 1) 1 l) 0 := by
    rw [hE]; exact geoFrame_area_differentiable
  exact H3_toy_for_every_G C2 hd₀ hnt

/-! ## 6. O IMPORT INDEXADO também é fabricável pelo brinquedo -/

theorem boost_V_determined (h h' : ContratoH2 W R) (s : ℝ) : h.boost.V s = h'.boost.V s := by
  have e : -(2 * Real.pi * (-(s / (2 * Real.pi)))) = s := by
    have : (2 * Real.pi) ≠ 0 := by positivity
    field_simp
  have h1 := h.bw (-(s / (2 * Real.pi)))
  have h2 := h'.bw (-(s / (2 * Real.pi)))
  rw [e] at h1 h2
  rw [← h1, ← h2]
  exact ContratoH2.Δit_determined h h' _

theorem boostEnergy_transfer (h h' : ContratoH2 W R) {ψ : W.H} {b : ℝ}
    (hb : HasBoostEnergy h'.boost.V ψ b) : HasBoostEnergy h.boost.V ψ b := by
  unfold HasBoostEnergy at hb ⊢
  have hf : (fun s : ℝ => ⟪ψ, h.boost.V s ψ⟫_ℂ) = (fun s : ℝ => ⟪ψ, h'.boost.V s ψ⟫_ℂ) := by
    funext s; rw [boost_V_determined h h' s]
  rw [hf]; exact hb

/-- ★★ o import (Jacobson + BW + Unruh + 1ª lei «importados») SUBSTITUÍDO por brinquedo: dado o índice h2,
    um G qualquer, um vetor de energia de boost ≠ 0 e a regularidade uniforme da área dos frames. -/
def toyImport (h2 : ContratoH2 W R) (G : ℝ) (hG : 0 < G)
    (hreg : ∀ h : ContratoH2 W R, DifferentiableAt ℝ (fun l => screenAreaOf h.E (Set.Icc 0 1) 1 l) 0)
    (hnt : ∃ ψ : W.H, ‖ψ‖ = 1 ∧ ∃ b : ℝ, HasBoostEnergy h2.boost.V ψ b ∧ b ≠ 0) :
    ContratoImportH3 W R h2 where
  produce := fun h => toyH3 h G hG (hreg h) (by
    obtain ⟨ψ, h1, b, hb, hb0⟩ := hnt
    exact ⟨ψ, h1, b, boostEnergy_transfer h h2 hb, hb0⟩)
  same_horizon := fun _ => rfl

#print axioms toyResp_inv
#print axioms toy_screen_det
#print axioms toy_area
#print axioms toy_areaVariation
#print axioms toy_area_differentiable
#print axioms toy_heat
#print axioms bOf_spec
#print axioms toyH3
#print axioms H3_toy_for_every_G
#print axioms toyH3_admissible_maximal
#print axioms toyH3_response_is_handmade
#print axioms geoFrame_inv
#print axioms geoFrame_screen_det
#print axioms geoFrame_area_const
#print axioms geoFrame_area_differentiable
#print axioms H3_toy_on_geoFrame
#print axioms boost_V_determined
#print axioms boostEnergy_transfer
#print axioms toyImport

end

end TGLExt.ContratoQGv3.CeticoBrinquedo
