import CeticoH3Ajuste
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 4000000

/-!
# CÉTICO 2 — com o frame `geoFrame` (o que o projetista diz já pago no par físico), H3 v3 sai SEM hipótese
  de regularidade: a área da tela do vácuo é CONSTANTE perto de λ = 0.
  [DIAGNÓSTICO do cético; scratchpad cetico_vacuidade; nunca importado pelo kernel; NÃO cunha nome reservado]

  `geoFrame x = [[x¹, x⁰],[x⁰, x¹]] ⊕ 1₂`: o bloco (2,3) da métrica soldada é −1₂ (det 1) onde det ≠ 0, logo
  screenArea = vol(S) numa vizinhança de 0 (`geo_vac_diff`). Resultado: para QUALQUER H2 cujo frame seja
  `geoFrame`, H3 existe com QUALQUER G, dado só UM vetor unitário de energia de boost ≠ 0 (`H3_of_H2_geo`).
-/

namespace TGLExt.ContratoQGv3.CeticoVacuidade

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open MeasureTheory Matrix Filter Topology
open scoped InnerProductSpace Classical

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

/-- o inverso explícito de `geoFrame` (onde d = x¹² − x⁰² ≠ 0). -/
def geoInv (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![x 1 / (x 1 ^ 2 - x 0 ^ 2), -(x 0) / (x 1 ^ 2 - x 0 ^ 2), 0, 0;
     -(x 0) / (x 1 ^ 2 - x 0 ^ 2), x 1 / (x 1 ^ 2 - x 0 ^ 2), 0, 0;
     0, 0, 1, 0;
     0, 0, 0, 1]

theorem geoFrame_inv (x : Fin 4 → ℝ) (hd : x 1 ^ 2 - x 0 ^ 2 ≠ 0) :
    (W5Final.Toy.geoFrame x)⁻¹ = geoInv x := by
  apply Matrix.inv_eq_left_inv
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [W5Final.Toy.geoFrame, geoInv, Matrix.mul_apply, Fin.sum_univ_four] <;>
    field_simp <;> ring

theorem geo_screen_sqrt (x : Fin 4 → ℝ) (hd : x 1 ^ 2 - x 0 ^ 2 ≠ 0) :
    Real.sqrt |(screenBlock (solderMetric4 (W5Final.Toy.geoFrame x)⁻¹)).det| = 1 := by
  rw [geoFrame_inv x hd]
  unfold screenBlock solderMetric4 eta4
  rw [Matrix.det_fin_two_of]
  simp [geoInv, Matrix.mul_apply, Fin.sum_univ_four, Matrix.diagonal_apply]

theorem geo_screenArea_near (S : Set (Fin 2 → ℝ)) {ε : ℝ} (hε : 0 < ε) :
    (fun l => screenAreaOf W5Final.Toy.geoFrame S ε l) =ᶠ[𝓝 (0:ℝ)] fun _ => volume.real S := by
  have hopen : Set.Ioi (-(ε / 2)) ∈ 𝓝 (0:ℝ) := Ioi_mem_nhds (by linarith)
  filter_upwards [hopen] with l hl
  unfold screenAreaOf
  have h : ∀ y : Fin 2 → ℝ,
      Real.sqrt |(screenBlock (solderMetric4 (W5Final.Toy.geoFrame (horizonPoint ε l y))⁻¹)).det| = 1 := by
    intro y
    apply geo_screen_sqrt
    have hl' : -(ε / 2) < l := hl
    simp only [horizonPoint, Matrix.cons_val_zero, Matrix.cons_val_one]
    nlinarith
  simp_rw [h]
  rw [setIntegral_const, smul_eq_mul, mul_one]

theorem geo_vac_diff (S : Set (Fin 2 → ℝ)) {ε : ℝ} (hε : 0 < ε) :
    DifferentiableAt ℝ (fun l => screenAreaOf W5Final.Toy.geoFrame S ε l) 0 :=
  ((hasDerivAt_const (0:ℝ) (volume.real S)).congr_of_eventuallyEq (geo_screenArea_near S hε)).differentiableAt

/-- os dados de tela, SEM hipótese, para todo H2 cujo frame é `geoFrame` (tela [0,1]², ε = 1). -/
def geoAdjData (h : ContratoH2 W R) (hE : h.E = W5Final.Toy.geoFrame) : AdjData h where
  S := Set.Icc 0 1
  S_meas := measurableSet_Icc
  S_pos := by rw [Real.volume_Icc_pi]; simp
  S_fin := by rw [Real.volume_Icc_pi]; simp
  eps := 1
  eps_pos := one_pos
  vac_diff := by rw [hE]; exact geo_vac_diff _ one_pos

/-- [DERIVED] ★★★ para QUALQUER H2 com o frame `geoFrame` e QUALQUER G > 0: um vetor unitário de energia de
    boost ≠ 0 basta para habitar H3 v3 sobre o MESMO H2. -/
theorem H3_of_H2_geo (h : ContratoH2 W R) (hE : h.E = W5Final.Toy.geoFrame) (G : ℝ) (hG : 0 < G)
    (ψ₁ : W.H) (hψ₁ : ‖ψ₁‖ = 1) (b₁ : ℝ) (hb₁ : HasBoostEnergy h.boost.V ψ₁ b₁) (hb0 : b₁ ≠ 0) :
    ∃ C : ContratoH3 W R, C.H2 = h ∧ C.G = G :=
  H3_of_H2 h (geoAdjData h hE) G hG ψ₁ hψ₁ b₁ hb₁ hb0

#print axioms geoFrame_inv
#print axioms geo_screen_sqrt
#print axioms geo_screenArea_near
#print axioms geo_vac_diff
#print axioms geoAdjData
#print axioms H3_of_H2_geo

end

end TGLExt.ContratoQGv3.CeticoVacuidade
