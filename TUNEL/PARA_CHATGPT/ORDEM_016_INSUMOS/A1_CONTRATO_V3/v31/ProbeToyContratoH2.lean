import ContratoQG
import TGLExt.ModularPower
import TGLExt.ExpectationPositive
import TGLExt.ModularFlowAlgebra

set_option autoImplicit false
set_option maxHeartbeats 2000000

/-!
# ProbeToyContratoH2 — o contrato do ANEXO A MORDE a física? (frente W5_final, 23/09/2026)

  [DIAGNÓSTICO DE GERÊNCIA; scratchpad; NUNCA importado por TGL.lean/TGLExt.lean; NÃO cunha nome reservado]

  O ProbeTrivialH2 de W2_final testa UM habitante (o par legado com `theCurvedFrame`) e CONCEDE (B1) e
  o vácuo como hipóteses. Este arquivo tenta o habitante mais barato que a aritmética permite, SEM
  conceder nada:

  * a testemunha `toyW` = `theSpecificAQFTWitness` com UMA troca: as «translações» passam a ser
    U(a) := Δ^{i a²} — o PRÓPRIO fluxo modular da torre, parametrizado pela 3ª coordenada. Não é a
    representação de Poincaré de rede física nenhuma; é um brinquedo. Rede, Hilbert, vácuo e massa
    são os do par legado (a rede das cunhas é invariante por translação: `wedgeNet_translate`);
  * a realização `toyR` = `regularModularRealization` transportada campo a campo para `toyW`;
  * o frame `geoFrame x = [K₁x | K₁²x | e₂ | e₃]` — ESCRITO À MÃO, equivariante pelo boost.

  Se este arquivo COMPILA, o `ContratoH2` do ANEXO A é habitável por um brinquedo: (B2)/(B3) não
  distinguem uma translação de verdade de um fluxo interno, e (C)(D)(E) não leem o frame do fluxo —
  pedem só equivariância geométrica. Isso NÃO move gate nenhum; mede o contrato (v103).

  Estatutos: tudo [DERIVED] (provado aqui). β jamais aparece. Sem sorry, sem axiom.
-/

namespace W5Final.Toy

open TGL.SpecificAQFT TGL.ModularRealization ChatgptAudit TGLV354.TraceCompletion
open TGLExt TGLExt.ContratoQG TGLExt.V350Continuous Matrix

noncomputable section

/-! ## 0. O fluxo da torre como unitário, e o que ele faz -/

abbrev u (t : ℝ) : WH ≃ₗᵢ[ℂ] WH := modularFlowUnitary mixProfile t

theorem u_apply (t : ℝ) (v : WH) : u t v = modularFlow mixProfile t v := rfl

theorem u_symm_apply (t : ℝ) (v : WH) : (u t).symm v = modularFlow mixProfile (-t) v := rfl

theorem conj_apply (t : ℝ) (X : WCLM) (v : WH) :
    (u t).conjStarAlgEquiv X v = modularFlow mixProfile t (X (modularFlow mixProfile (-t) v)) := rfl

/-! ## 1. O fluxo preserva cada uma das quatro álgebras da rede -/

theorem conj_mem_factor (t : ℝ) (X : WCLM) :
    X ∈ theFactorObject mixProfile ↔ (u t).conjStarAlgEquiv X ∈ theFactorObject mixProfile :=
  modularConjugation_preserves_factor mixProfile t X

theorem conj_mem_scalar (t : ℝ) (X : WCLM) :
    X ∈ scalarAlg ↔ (u t).conjStarAlgEquiv X ∈ scalarAlg :=
  centralizer_transport ((u t).conjStarAlgEquiv) Set.univ (fun _ => by simp) X

theorem conj_mem_comm (t : ℝ) (X : WCLM) :
    X ∈ commAlg ↔ (u t).conjStarAlgEquiv X ∈ commAlg :=
  centralizer_transport ((u t).conjStarAlgEquiv) _ (fun a => conj_mem_factor t a) X

theorem conj_mem_union (t : ℝ) (X : WCLM) :
    X ∈ ((theFactorObject mixProfile : Set WCLM) ∪ (commAlg : Set WCLM)) ↔
      (u t).conjStarAlgEquiv X ∈ ((theFactorObject mixProfile : Set WCLM) ∪ (commAlg : Set WCLM)) := by
  simp only [Set.mem_union, SetLike.mem_coe]
  rw [conj_mem_factor t X, conj_mem_comm t X]

theorem conj_mem_both (t : ℝ) (X : WCLM) :
    X ∈ bothAlg ↔ (u t).conjStarAlgEquiv X ∈ bothAlg :=
  centralizer_transport ((u t).conjStarAlgEquiv) _
    (fun a => centralizer_transport ((u t).conjStarAlgEquiv) _ (fun b => conj_mem_union t b) a) X

theorem conj_mem_wedgeNet (t : ℝ) (O : Set (Fin 4 → ℝ)) (X : WCLM) :
    X ∈ wedgeNet O ↔ (u t).conjStarAlgEquiv X ∈ wedgeNet O := by
  by_cases hR : hasRW O <;> by_cases hL : hasLW O
  · rw [wedgeNet_both hR hL]; exact conj_mem_both t X
  · rw [wedgeNet_M hR hL]; exact conj_mem_factor t X
  · rw [wedgeNet_comm hR hL]; exact conj_mem_comm t X
  · rw [wedgeNet_scalar hR hL]; exact conj_mem_scalar t X

/-- a rede das cunhas é monótona nas duas bandeiras (o padrão da prova de `isotony`). -/
theorem wedgeNet_le_of_flags {O₁ O₂ : Set (Fin 4 → ℝ)}
    (hRR : hasRW O₁ → hasRW O₂) (hLL : hasLW O₁ → hasLW O₂) (T : WCLM) (hT : T ∈ wedgeNet O₁) :
    T ∈ wedgeNet O₂ := by
  by_cases hR1 : hasRW O₁ <;> by_cases hL1 : hasLW O₁ <;>
    by_cases hR2 : hasRW O₂ <;> by_cases hL2 : hasLW O₂
  all_goals first
    | (exact absurd (hRR hR1) hR2)
    | (exact absurd (hLL hL1) hL2)
    | (first
        | (rw [wedgeNet_both hR1 hL1] at hT
           rw [wedgeNet_both hR2 hL2]
           exact hT)
        | (rw [wedgeNet_M hR1 hL1] at hT
           rw [wedgeNet_both hR2 hL2]
           exact union_mem_bothAlg (Or.inl hT))
        | (rw [wedgeNet_M hR1 hL1] at hT
           rw [wedgeNet_M hR2 hL2]
           exact hT)
        | (rw [wedgeNet_comm hR1 hL1] at hT
           rw [wedgeNet_both hR2 hL2]
           exact union_mem_bothAlg (Or.inr hT))
        | (rw [wedgeNet_comm hR1 hL1] at hT
           rw [wedgeNet_comm hR2 hL2]
           exact hT)
        | (rw [wedgeNet_scalar hR1 hL1] at hT
           first
            | (rw [wedgeNet_both hR2 hL2]
               exact scalarAlg_mem_centralizer hT _)
            | (rw [wedgeNet_M hR2 hL2]
               exact scalarAlg_mem_centralizer hT _)
            | (rw [wedgeNet_comm hR2 hL2]
               exact scalarAlg_mem_centralizer hT _)
            | (rw [wedgeNet_scalar hR2 hL2]
               exact hT)))

/-! ## 2. A geometria: o boost preserva as duas cunhas e leva translados em translados -/

theorem wedgeBoostMap_add (s : ℝ) (x y : Fin 4 → ℝ) :
    wedgeBoostMap s (x + y) = wedgeBoostMap s x + wedgeBoostMap s y := by
  simp [wedgeBoostMap, Matrix.mulVec_add]

theorem wedgeBoostMap_comp (s r : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s (wedgeBoostMap r x) = wedgeBoostMap (s + r) x := by
  have h := congrArg Subtype.val (theBoost_add s r)
  change boostMat s * boostMat r = boostMat (s + r) at h
  simp only [wedgeBoostMap, Matrix.mulVec_mulVec, h]

theorem wedgeBoostMap_zero (x : Fin 4 → ℝ) : wedgeBoostMap 0 x = x := by
  funext i
  fin_cases i <;> simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

theorem wedgeBoostMap_mem_leftWedge (s : ℝ) {x : Fin 4 → ℝ} (hx : x ∈ leftWedge) :
    wedgeBoostMap s x ∈ leftWedge := by
  have hx' : |x 0| < -(x 1) := hx
  obtain ⟨h1, h2⟩ := abs_lt.mp hx'
  have hd : 0 < -(x 1) - x 0 := by linarith
  have hs : 0 < -(x 1) + x 0 := by linarith
  have e1 : Real.cosh s - Real.sinh s = Real.exp (-s) := Real.cosh_sub_sinh s
  have e2 : Real.cosh s + Real.sinh s = Real.exp s := Real.cosh_add_sinh s
  have p1 : 0 < (Real.cosh s + Real.sinh s) * (-(x 1) - x 0) := by
    rw [e2]; exact mul_pos (Real.exp_pos _) hd
  have p2 : 0 < (Real.cosh s - Real.sinh s) * (-(x 1) + x 0) := by
    rw [e1]; exact mul_pos (Real.exp_pos _) hs
  show |wedgeBoostMap s x 0| < -(wedgeBoostMap s x 1)
  rw [wedgeBoostMap_apply0, wedgeBoostMap_apply1, abs_lt]
  constructor <;> nlinarith

/-- o boost leva o translado `a + S` no translado `Λa + S`, se `Λ` preserva `S` nos dois sentidos. -/
theorem boost_image_translate (s : ℝ) (S : Set (Fin 4 → ℝ))
    (hS : ∀ r : ℝ, ∀ x ∈ S, wedgeBoostMap r x ∈ S) (a : Fin 4 → ℝ) :
    TGL.SpecificAQFT.translate (wedgeBoostMap s a) S ⊆
      wedgeBoostMap s '' TGL.SpecificAQFT.translate a S := by
  rintro y ⟨w, hw, rfl⟩
  refine ⟨wedgeBoostMap (-s) w + a, ⟨wedgeBoostMap (-s) w, hS (-s) w hw, rfl⟩, ?_⟩
  simp only
  rw [wedgeBoostMap_add, wedgeBoostMap_comp, add_neg_cancel, wedgeBoostMap_zero]

theorem hasRW_boost (s : ℝ) {O : Set (Fin 4 → ℝ)} (h : hasRW O) : hasRW (wedgeBoostMap s '' O) := by
  obtain ⟨a, ha⟩ := h
  exact ⟨wedgeBoostMap s a, (boost_image_translate s rightWedge
    (fun r x hx => wedgeBoostMap_mem_rightWedge r hx) a).trans (Set.image_mono ha)⟩

theorem hasLW_boost (s : ℝ) {O : Set (Fin 4 → ℝ)} (h : hasLW O) : hasLW (wedgeBoostMap s '' O) := by
  obtain ⟨a, ha⟩ := h
  exact ⟨wedgeBoostMap s a, (boost_image_translate s leftWedge
    (fun r x hx => wedgeBoostMap_mem_leftWedge r hx) a).trans (Set.image_mono ha)⟩

/-! ## 3. A «translação» de brinquedo: U(a) := Δ^{i a²} -/

def toyU (a : Fin 4 → ℝ) : WCLM := ((u (a 2)).toContinuousLinearEquiv : WH →L[ℂ] WH)

theorem toyU_apply (a : Fin 4 → ℝ) (v : WH) : toyU a v = modularFlow mixProfile (a 2) v := rfl

theorem toyU_zero : toyU 0 = 1 := by
  ext v
  rw [toyU_apply]
  simpa using modularFlow_zero_time (P := mixProfile) v

theorem toyU_add (v w : Fin 4 → ℝ) : toyU (v + w) = toyU v * toyU w := by
  ext x
  rw [ContinuousLinearMap.mul_apply, toyU_apply, toyU_apply, toyU_apply, modularFlow_group]
  simp

theorem toyU_star (v : Fin 4 → ℝ) : star (toyU v) = toyU (-v) := by
  rw [ContinuousLinearMap.star_eq_adjoint]
  symm
  rw [ContinuousLinearMap.eq_adjoint_iff]
  intro x y
  have hx : x = u (v 2) (u (-(v 2)) x) := by
    rw [u_apply, u_apply, modularFlow_group, add_neg_cancel, modularFlow_zero_time]
  have h := (u (v 2)).inner_map_map (u (-(v 2)) x) y
  rw [← hx] at h
  rw [toyU_apply, toyU_apply]
  simpa [u_apply] using h.symm

theorem toyU_conj (a : Fin 4 → ℝ) (X : WCLM) :
    toyU a * X * toyU (-a) = (u (a 2)).conjStarAlgEquiv X := by
  ext v
  simp only [ContinuousLinearMap.mul_apply, toyU_apply, conj_apply, Pi.neg_apply]

theorem toyU_vac (a : Fin 4 → ℝ) : toyU a (hOmega mixProfile) = hOmega mixProfile := by
  rw [toyU_apply]; exact modularFlow_fixes_omega (a 2)

/-- a testemunha de brinquedo: o par legado com as «translações» trocadas pelo fluxo modular. -/
def toyW : TGLSpecificAQFTWitness :=
  { theSpecificAQFTWitness with
    U := toyU
    U_zero := toyU_zero
    U_add := toyU_add
    U_star := toyU_star
    covariance := fun a O x =>
      (show ∀ y : WCLM, y ∈ wedgeNet O ↔
          toyU a * y * toyU (-a) ∈ wedgeNet (TGL.SpecificAQFT.translate a O) from
        fun y => by
          rw [toyU_conj, wedgeNet_translate]
          exact conj_mem_wedgeNet (a 2) O y) x
    vac_invariant := toyU_vac }

/-- a realização legada, transportada campo a campo (rede, Hilbert e vácuo não mudaram). -/
def toyModular : WedgeModularData toyW := { towerWedgeData with }

def toyCore : ContinuousCoreData toyW toyModular := { regularLegacyCore with }

def toyThreeLocks : ThreeLocksCoreData toyW toyModular toyCore := { regularLegacyThreeLocks with }

def toyR : TGLModularRealization toyW where
  infiniteHilbert := regularModularRealization.infiniteHilbert
  modular := toyModular
  core := toyCore
  threeLocks := toyThreeLocks

/-! ## 4. (B2): o brinquedo translada de verdade (o fluxo da torre não é trivial) -/

/-- a razão logarítmica do primeiro sítio de `mixProfile` (pesos 1/3 e 2/3) é não nula. -/
theorem site0_log_ratio_ne :
    Real.log (towerW mixProfile 0 (0 : Fin 2)) - Real.log (towerW mixProfile 0 (1 : Fin 2)) ≠ 0 := by
  have h0 : towerW mixProfile 0 (0 : Fin 2) = 1 / 3 := by
    simp [towerW, siteW, show mixProfile.w 0 = 1 / 3 from rfl]
  have h1 : towerW mixProfile 0 (1 : Fin 2) = 2 / 3 := by
    simp [towerW, siteW, show mixProfile.w 0 = 1 / 3 from rfl]; norm_num
  rw [h0, h1]
  have : Real.log (1 / 3) < Real.log (2 / 3) := Real.log_lt_log (by norm_num) (by norm_num)
  linarith

theorem toy_translations_nontrivial : ∃ a : Fin 4 → ℝ, toyW.U a ≠ 1 := by
  set r := Real.log (towerW mixProfile 0 (0 : Fin 2)) - Real.log (towerW mixProfile 0 (1 : Fin 2))
    with hr
  have hr0 : r ≠ 0 := site0_log_ratio_ne
  refine ⟨![0, 0, Real.pi / r, 0], fun h => ?_⟩
  change toyU ![0, 0, Real.pi / r, 0] = 1 at h
  set c : ℝ := Real.pi / r with hc
  have hfix : ∀ v : WH, modularFlow mixProfile c v = v := by
    intro v
    have := congrArg (fun T : WCLM => T v) h
    simpa [toyU_apply] using this
  have hfix' : ∀ v : WH, modularFlow mixProfile (-c) v = v := by
    intro v
    have h2 : modularFlow mixProfile c (modularFlow mixProfile (-c) v) = v := by
      rw [modularFlow_group, add_neg_cancel, modularFlow_zero_time]
    rw [hfix] at h2
    exact h2
  let E01 : Matrix (chainIdx 0) (chainIdx 0) ℂ := fun i j => if i = 0 ∧ j = 1 then 1 else 0
  have hconj : modularConjugation mixProfile c (towerPi mixProfile E01) = towerPi mixProfile E01 := by
    ext v
    change modularFlow mixProfile c (towerPi mixProfile E01 (modularFlow mixProfile (-c) v)) = _
    rw [hfix', hfix]
  rw [modularConjugation_local] at hconj
  have hm := towerPi_injective mixProfile 0 hconj
  have h01 := congrFun (congrFun hm (0 : Fin 2)) (1 : Fin 2)
  simp only [flowLevel, E01] at h01
  simp only [and_self, if_true, mul_one] at h01
  have hcr : c * r = Real.pi := by rw [hc]; field_simp
  unfold modularPhase at h01
  rw [← hr, hcr] at h01
  rw [Complex.exp_pi_mul_I] at h01
  norm_num at h01

/-! ## 5. (B1)/(B3) no brinquedo -/

theorem toy_bw_covariance (t : ℝ) (O : Set (Fin 4 → ℝ)) (T : WH →L[ℂ] WH)
    (hT : T ∈ toyW.net O) :
    (u t).conjStarAlgEquiv T ∈ toyW.net (wedgeBoostMap (-(2 * Real.pi * t)) '' O) := by
  change T ∈ wedgeNet O at hT
  change (u t).conjStarAlgEquiv T ∈ wedgeNet (wedgeBoostMap (-(2 * Real.pi * t)) '' O)
  exact wedgeNet_le_of_flags (hasRW_boost _) (hasLW_boost _) _ ((conj_mem_wedgeNet t O T).mp hT)

theorem toy_poincare_relation (t : ℝ) (a : Fin 4 → ℝ) :
    (u t).conjStarAlgEquiv (toyW.U a) = toyW.U (wedgeBoostMap (-(2 * Real.pi * t)) a) := by
  change (u t).conjStarAlgEquiv (toyU a) = toyU (wedgeBoostMap (-(2 * Real.pi * t)) a)
  have h2 : wedgeBoostMap (-(2 * Real.pi * t)) a 2 = a 2 := by
    simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]
  ext v
  rw [conj_apply, toyU_apply, toyU_apply, h2, modularFlow_group, modularFlow_group]
  congr 1
  ring

/-- [DERIVED] ★ (B1) vale TAMBÉM no par legado: a hipótese `hBW` que o ProbeTrivialH2 de W2_final CONCEDE
    é teorema (as bandeiras hasRW/hasLW da rede das cunhas sobem sob boost e o fluxo preserva as quatro
    álgebras). -/
theorem legacy_bw_covariance (t : ℝ) (O : Set (Fin 4 → ℝ)) (T : WH →L[ℂ] WH)
    (hT : T ∈ theSpecificAQFTWitness.net O) :
    (u t).conjStarAlgEquiv T ∈ theSpecificAQFTWitness.net (wedgeBoostMap (-(2 * Real.pi * t)) '' O) :=
  toy_bw_covariance t O T hT

/-- [DERIVED] a hipótese `hvac` que o ProbeTrivialH2 CONCEDE («o kernel não tem esse lema») é o lema
    `modularFlow_fixes_omega` (ModularPower.lean:49). -/
theorem legacy_vac_fixed (t : ℝ) : u t (hOmega mixProfile) = hOmega mixProfile :=
  modularFlow_fixes_omega t

/-! ## 6. O frame ESCRITO À MÃO: [K₁x | K₁²x | e₂ | e₃], equivariante pelo boost -/

def geoFrame (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![x 1, x 0, 0, 0;
     x 0, x 1, 0, 0;
     0,   0,   1, 0;
     0,   0,   0, 1]

theorem geoFrame_det (x : Fin 4 → ℝ) : (geoFrame x).det = x 1 ^ 2 - x 0 ^ 2 := by
  have h : Fin.succAbove (1 : Fin 4) (2 : Fin 3) = 3 := by decide
  simp [geoFrame, Matrix.det_succ_row_zero, Fin.sum_univ_succ]
  rw [h]
  simp
  ring

theorem geoFrame_smooth (i j : Fin 4) :
    ContDiffOn ℝ (⊤ : ℕ∞) (fun x => geoFrame x i j) rightWedge := by
  have c0 : ContDiff ℝ (⊤ : ℕ∞) (fun x : Fin 4 → ℝ => x 0) := contDiff_apply ℝ ℝ 0
  have c1 : ContDiff ℝ (⊤ : ℕ∞) (fun x : Fin 4 → ℝ => x 1) := contDiff_apply ℝ ℝ 1
  fin_cases i <;> fin_cases j <;>
    simp [geoFrame] <;>
    first
      | exact c0.contDiffOn
      | exact c1.contDiffOn
      | exact contDiffOn_const

theorem geoFrame_det_unit_on (x : Fin 4 → ℝ) (hx : x ∈ rightWedge) : IsUnit (geoFrame x).det := by
  rw [geoFrame_det]
  have hx' : |x 0| < x 1 := hx
  obtain ⟨h1, h2⟩ := abs_lt.mp hx'
  refine isUnit_iff_ne_zero.mpr (ne_of_gt ?_)
  nlinarith

theorem geoFrame_dragged (s : ℝ) (x : Fin 4 → ℝ) (_hx : x ∈ rightWedge) :
    geoFrame (wedgeBoostMap s x) = boostMat s * geoFrame x := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [geoFrame, Matrix.mul_apply, boostMat, Fin.sum_univ_four, wedgeBoostMap_apply0,
      wedgeBoostMap_apply1] <;> ring

theorem geoFrame_fiducial (x : Fin 4 → ℝ) (_hx : x ∈ rightWedge) :
    ∃ c : ℝ, 0 < c ∧ (fun i => geoFrame x i 0) = c • killingField 1 x := by
  refine ⟨1, one_pos, ?_⟩
  funext i
  fin_cases i <;> simp [geoFrame, killingField]

/-! ## 7. O HABITANTE: se isto compila, o contrato é habitável por um brinquedo -/

def toyContract : ContratoH2 toyW toyR where
  kappa := 1
  kappa_pos := one_pos
  Δit := u
  Δit_vac := fun t => modularFlow_fixes_omega t
  flow_implemented := fun _ _ => rfl
  profile := mixProfile
  stateIso := LinearIsometryEquiv.refl ℂ WH
  state_is_vac := rfl
  state_flow := fun _ _ => rfl
  bw_covariance := toy_bw_covariance
  translations_nontrivial := toy_translations_nontrivial
  poincare_relation := toy_poincare_relation
  E := geoFrame
  smooth_on := geoFrame_smooth
  det_unit_on := geoFrame_det_unit_on
  dragged := geoFrame_dragged
  fiducial_is_modular := geoFrame_fiducial

/-- [DERIVED] ★★ o contrato H2 do ANEXO A é NÃO-VAZIO num par de brinquedo. -/
theorem contratoH2_inhabited_by_toy : Nonempty (ContratoH2 toyW toyR) := ⟨toyContract⟩

#print axioms toy_translations_nontrivial
#print axioms toy_bw_covariance
#print axioms toy_poincare_relation
#print axioms geoFrame_dragged
#print axioms legacy_bw_covariance
#print axioms legacy_vac_fixed
#print axioms contratoH2_inhabited_by_toy

end

end W5Final.Toy
