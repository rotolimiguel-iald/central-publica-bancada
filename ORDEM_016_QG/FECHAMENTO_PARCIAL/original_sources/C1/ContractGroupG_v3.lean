import ContractGroupF_v3

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CONTRATO v3.1 — OS TEOREMAS (leem os campos do tipo `ContratoQG_v31`)
  [RASCUNHO DE GERÊNCIA — frente contrato_v3, RODADA 2, 23/09/2026; scratchpad; NÃO cunha nome reservado]

  §A  unitariedade das translações.
  §B  o que a v2 pedia como campo e a v3/v3.1 DERIVA (Δit fixa Ω; BW geométrico; Poincaré; não-trivial).
  §C  ★★★ COERÊNCIA ESPECTRAL: todo habitante tem Δ^{it} SEM autovetor fora de ℂΩ (oposto da v2).
  §C' ★ as paredes do cético 1 transpostas (T1–T4): U transversal, boost trivial, torre, momento nulo discreto.
  §C''★ os certificados de sinal do cético 2 transpostos: inclusão semilateral, forma de Borchers, orientação.
  §D  ★★ κ: Unruh como relação KMS (β_Killing·κ = 2π); κ = 1/ρ(N); κ FIXO dado N; (W,R) NÃO fixa κ.
  §E  o implementador é ÚNICO.
  §F  as energias: K = 2πB; ★ a energia BILATERAL não tem termo de 1ª ordem (cético 2, transposto).
  §G  o frame.
  §H  ★★★ H3 v3.1: a lei local ao longo do gerador; BH/Clausius/8πG como teoremas de JANELA (integração
      exata); a energia nula não se anula; a expansão não é constante; G NÃO é predito (Jacobson).
  §I  as paredes no par legado e contra translações que comutam com Δit.
  §J  o import indexado.
  β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt.ContratoQGv31

open TGL.SpecificAQFT TGL.ModularRealization
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace ComplexConjugate

noncomputable section

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

theorem Δit_determined (C C' : ContratoH2 W R N) (t : ℝ) : C.Δit t = C'.Δit t :=
  implementer_unique C.Δit C'.Δit C.Δit_vac C'.Δit_vac C.flow_implemented C'.flow_implemented t

/-- [DERIVED] o Δit NÃO depende do índice N (dois habitantes sobre N e N' têm o mesmo Δit). -/
theorem Δit_index_free {N' : KillingNormalization} (C : ContratoH2 W R N) (C' : ContratoH2 W R N')
    (t : ℝ) : C.Δit t = C'.Δit t :=
  implementer_unique C.Δit C'.Δit C.Δit_vac C'.Δit_vac C.flow_implemented C'.flow_implemented t

/-! ## §G — o frame -/

theorem boostMat_det_isUnit (s : ℝ) : IsUnit (boostMat s).det := by
  have h := congrArg Matrix.det (boostMat_isLorentz s)
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose] at h
  have hη : eta4.det ≠ 0 := by
    unfold eta4
    rw [Matrix.det_diagonal, Fin.prod_univ_four]
    norm_num [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
      Matrix.cons_val_three, Matrix.vecHead, Matrix.vecTail]
  have hsq : (boostMat s).det * (boostMat s).det = 1 := by
    have h' : ((boostMat s).det * (boostMat s).det - 1) * eta4.det = 0 := by
      linear_combination h
    rcases mul_eq_zero.mp h' with h1 | h1
    · linarith
    · exact absurd h1 hη
  refine isUnit_iff_ne_zero.mpr ?_
  intro h0
  rw [h0, mul_zero] at hsq
  exact zero_ne_one hsq

theorem feeds_finite_face (C : ContratoH2 W R N) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    (C.E x)⁻¹ * C.E x = 1 ∧ LorentzByCongruence (solderMetric4 (C.E x)⁻¹) :=
  four_frame_gives_lorentz_metric (C.E x) (C.det_unit_on x hx)

theorem det_unit_along_orbit (C : ContratoH2 W R N) (s : ℝ) {x : Fin 4 → ℝ} (hx : x ∈ rightWedge) :
    IsUnit (C.E (wedgeBoostMap s x)).det := by
  rw [C.dragged s x hx, Matrix.det_mul]
  exact (boostMat_det_isUnit s).mul (C.det_unit_on x hx)

end ContratoH2

theorem curvedFrame_not_dragged :
    ¬ ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
        theCurvedFrame.E (wedgeBoostMap s x) = boostMat s * theCurvedFrame.E x := by
  intro h
  have hx : (![0, 1, 0, 0] : Fin 4 → ℝ) ∈ rightWedge := by
    show |(![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(0:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp
  have h10 := congrFun (congrFun (h 1 _ hx) 1) 0
  rw [curvedFrame_E_apply, curvedFrame_E_apply] at h10
  simp [Matrix.mul_apply, boostMat, Fin.sum_univ_four, profileFn] at h10
  exact (Real.sinh_pos_iff.mpr one_pos).ne' h10.symm

theorem curvedFrame_fiducial_not_modular (κ : ℝ) :
    ¬ ∀ x ∈ rightWedge, ∃ c : ℝ, 0 < c ∧
        (fun i => theCurvedFrame.E x i 0) = c • killingField κ x := by
  intro h
  have hx : (![1/2, 1, 0, 0] : Fin 4 → ℝ) ∈ rightWedge := by
    show |(![(1/2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 0| < (![(1/2:ℝ), 1, 0, 0] : Fin 4 → ℝ) 1
    simp; norm_num
  obtain ⟨c, hc, hE⟩ := h _ hx
  have h0 := congrFun hE 0
  have h1 := congrFun hE 1
  simp [curvedFrame_E_apply, killingField, profileFn] at h0 h1
  rcases h1 with h1 | h1
  · exact hc.ne' h1
  · rw [h1, mul_zero] at h0
    norm_num at h0

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

theorem frame_ne_curvedFrame_by_drag (C : ContratoH2 W R N) : C.E ≠ theCurvedFrame.E := by
  intro hE
  apply curvedFrame_not_dragged
  intro s x hx
  have h := C.dragged s x hx
  rw [hE] at h
  exact h

theorem frame_ne_curvedFrame_by_fiducial (C : ContratoH2 W R N) : C.E ≠ theCurvedFrame.E := by
  intro hE
  apply curvedFrame_fiducial_not_modular C.kappa
  intro x hx
  have h := C.fiducial_is_modular x hx
  rw [hE] at h
  exact h

end ContratoH2


end
end TGLExt.ContratoQGv31

#print axioms TGLExt.ContratoQGv31.ContratoH2.Δit_determined
#print axioms TGLExt.ContratoQGv31.ContratoH2.Δit_index_free
#print axioms TGLExt.ContratoQGv31.ContratoH2.boostMat_det_isUnit
#print axioms TGLExt.ContratoQGv31.ContratoH2.feeds_finite_face
#print axioms TGLExt.ContratoQGv31.ContratoH2.det_unit_along_orbit
#print axioms TGLExt.ContratoQGv31.curvedFrame_not_dragged
#print axioms TGLExt.ContratoQGv31.curvedFrame_fiducial_not_modular
#print axioms TGLExt.ContratoQGv31.ContratoH2.frame_ne_curvedFrame_by_drag
#print axioms TGLExt.ContratoQGv31.ContratoH2.frame_ne_curvedFrame_by_fiducial
