import FlagNetV3

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CÉTICO 2 — a hipótese `KMSUnique` de FlagNetV3 NÃO é Takesaki: ela proíbe simetrias Z₂
  [DIAGNÓSTICO do cético; scratchpad cetico_vacuidade; nunca importado pelo kernel; NÃO cunha nome reservado]

  `KMSUnique C` quantifica sobre TODA função D : ℝ → unitários (não só grupos a um parâmetro). Takesaki dá
  unicidade entre GRUPOS. §1: se V é unitário INVOLUTIVO, fixa Ω, comuta com Δ^{it} e preserva a álgebra
  da cunha, então D(t) := Δ^{it}·V cumpre TODAS as premissas de `KMSUnique` — logo `KMSUnique C` força
  V = 1 (`kmsUnique_forbids_Z2`). No campo escalar livre, V = Γ(−1) (φ ↦ −φ) é um tal V ≠ 1 [KNOWN]:
  lá `KMSUnique` é FALSA, e `flag_net_excludes_v3` fica sem hipótese satisfazível em modelos com Z₂.
  §2: a versão FIEL (só grupos: D 0 = 1, D(s+t) = D s ∘ D t) basta para a parede — reprovada aqui
  (`flag_net_excludes_v3_group`), com a mesma prova, porque o D usado é grupo.
-/

namespace TGLExt.ContratoQGv3.CeticoVacuidade

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3 TGLExt.ContratoQGv3.FlagNet
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

theorem Δit_preserves_wedge (C : ContratoH2 W R) (s : ℝ) (T : W.H →L[ℂ] W.H)
    (hT : T ∈ W.net rightWedge) : (C.Δit s).conjStarAlgEquiv T ∈ W.net rightWedge := by
  have h := C.bw_covariance s rightWedge T hT
  rwa [boost_image_rightWedge] at h

/-- [DERIVED] ★★ `KMSUnique` proíbe todo Z₂ unitário que comuta com o fluxo modular. -/
theorem kmsUnique_forbids_Z2 (C : ContratoH2 W R) (hTak : KMSUnique C)
    (V : W.H ≃ₗᵢ[ℂ] W.H) (hV2 : ∀ x, V (V x) = x) (hVvac : V W.vac = W.vac)
    (hVcomm : ∀ (t : ℝ) (x : W.H), C.Δit t (V x) = V (C.Δit t x))
    (hVnet : ∀ T : W.H →L[ℂ] W.H, T ∈ W.net rightWedge → V.conjStarAlgEquiv T ∈ W.net rightWedge) :
    ∀ x, V x = x := by
  have hVsymm : ∀ x, V.symm x = V x := by
    intro x
    apply V.injective
    rw [LinearIsometryEquiv.apply_symm_apply, hV2]
  let D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H) := fun s => V.trans (C.Δit s)
  have hDapply : ∀ s x, D s x = C.Δit s (V x) := fun s x => rfl
  have hvac : ∀ s, D s W.vac = W.vac := by
    intro s; rw [hDapply, hVvac, ContratoH2.Δit_vac]
  have hpres : ∀ (s : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D s).conjStarAlgEquiv T ∈ W.net rightWedge := by
    intro s T hT
    have e : (D s).conjStarAlgEquiv T = (C.Δit s).conjStarAlgEquiv (V.conjStarAlgEquiv T) := by
      ext x
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply]
      rfl
    rw [e]
    exact Δit_preserves_wedge C s _ (hVnet T hT)
  have hkms : KMSAt W (fun s => D (-s)) 1 := by
    intro A hA B hB
    obtain ⟨F, hF, hM, h1, h2⟩ := C.kms A hA (V.conjStarAlgEquiv B) (hVnet B hB)
    refine ⟨F, hF, hM, ?_, ?_⟩
    · intro t
      rw [h1 t]
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, hVsymm, hVvac]
      rfl
    · intro t
      rw [h2 t]
      have hs : star (V.conjStarAlgEquiv B) = V.conjStarAlgEquiv (star B) := (map_star _ B).symm
      rw [hs]
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, hVsymm, hVvac, neg_neg]
      rw [hDapply]
      have hadj : ⟪V ((star B) W.vac), C.Δit t (A W.vac)⟫_ℂ
          = ⟪(star B) W.vac, V (C.Δit t (A W.vac))⟫_ℂ := by
        have := V.inner_map_map ((star B) W.vac) (V (C.Δit t (A W.vac)))
        rw [hV2] at this
        exact this
      rw [hadj, ← hVcomm]
  have hD := hTak D hvac hpres hkms 0
  intro x
  have h := congrArg (fun E : W.H ≃ₗᵢ[ℂ] W.H => E x) hD
  simp only [hDapply] at h
  exact (C.Δit 0).injective h

/-- a unicidade KMS FIEL a Takesaki: só entre GRUPOS a um parâmetro. -/
def KMSUniqueGroup (C : ContratoH2 W R) : Prop :=
  ∀ D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H), D 0 = LinearIsometryEquiv.refl ℂ W.H →
    (∀ s t : ℝ, D (s + t) = (D t).trans (D s)) → (∀ t, D t W.vac = W.vac) →
    (∀ (t : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D t).conjStarAlgEquiv T ∈ W.net rightWedge) →
    KMSAt W (fun t => D (-t)) 1 → ∀ t, D t = C.Δit t

theorem kmsUnique_implies_group (C : ContratoH2 W R) (h : KMSUnique C) : KMSUniqueGroup C :=
  fun D _ _ hv hp hk t => h D hv hp hk t

/-- [DERIVED] ★ a parede das bandeiras com a hipótese FIEL (grupos): mesma prova de FlagNetV3; o D usado
    (U(−a)Δ^{is}U(a)) é grupo. -/
theorem flag_net_excludes_v3_group (C : ContratoH2 W R) (hTak : KMSUniqueGroup C)
    (hinv : ∀ (a : Fin 4 → ℝ) (T : W.H →L[ℂ] W.H),
      T ∈ W.net rightWedge → W.U a * T * W.U (-a) ∈ W.net rightWedge) : False := by
  apply C.commuting_translations_excluded
  intro t a
  let D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H) := fun s => ((Uiso W a).trans (C.Δit s)).trans (Uiso W a).symm
  have hDapply : ∀ s x, D s x = W.U (-a) (C.Δit s (W.U a x)) := fun s x => rfl
  have hD0 : D 0 = LinearIsometryEquiv.refl ℂ W.H := by
    ext x
    rw [hDapply]
    have h0 := congrArg (fun E : W.H ≃ₗᵢ[ℂ] W.H => E (W.U a x)) (C.killingFlow_zero)
    have hΔ0 : C.Δit 0 = LinearIsometryEquiv.refl ℂ W.H := by
      rw [C.bw, show -(2 * Real.pi * (0:ℝ)) = 0 by ring, C.boost.V_zero]
    rw [hΔ0]
    exact U_neg_apply W a x
  have hDadd : ∀ s u : ℝ, D (s + u) = (D u).trans (D s) := by
    intro s u
    ext x
    simp only [LinearIsometryEquiv.trans_apply, hDapply]
    have hΔadd : C.Δit (s + u) = (C.Δit u).trans (C.Δit s) := by
      ext y
      rw [C.bw, C.bw, C.bw, LinearIsometryEquiv.trans_apply]
      rw [show -(2 * Real.pi * (s + u)) = -(2 * Real.pi * s) + -(2 * Real.pi * u) by ring, C.boost.V_add]
      rfl
    rw [hΔadd, LinearIsometryEquiv.trans_apply, U_pos_neg_apply]
  have hvac : ∀ s, D s W.vac = W.vac := by
    intro s
    rw [hDapply, W.vac_invariant, C.Δit_vac, W.vac_invariant]
  have hpres : ∀ (s : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D s).conjStarAlgEquiv T ∈ W.net rightWedge := by
    intro s T hT
    have e : (D s).conjStarAlgEquiv T
        = W.U (-a) * ((C.Δit s).conjStarAlgEquiv (W.U a * T * W.U (-a))) * W.U (-(-a)) := by
      ext x
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, neg_neg]
      rfl
    rw [e]
    exact hinv (-a) _ (Δit_preserves_wedge C s _ (hinv a T hT))
  have hkms : KMSAt W (fun s => D (-s)) 1 := by
    intro A hA B hB
    obtain ⟨F, hF, hM, h1, h2⟩ := C.kms _ (hinv a A hA) _ (hinv a B hB)
    have hstar : ∀ X : W.H →L[ℂ] W.H, star (W.U a * X * W.U (-a)) = W.U a * star X * W.U (-a) := by
      intro X
      rw [star_mul, star_mul, W.U_star, W.U_star, neg_neg, mul_assoc]
    refine ⟨F, hF, hM, ?_, ?_⟩
    · intro s
      rw [h1 s, hstar]
      show ⟪W.U a (star A (W.U (-a) W.vac)), C.Δit (-s) (W.U a (B (W.U (-a) W.vac)))⟫_ℂ
        = ⟪(star A) W.vac, W.U (-a) (C.Δit (-s) (W.U a (B W.vac)))⟫_ℂ
      rw [W.vac_invariant, U_inner_adj]
    · intro s
      rw [h2 s, hstar]
      show ⟪W.U a (star B (W.U (-a) W.vac)), C.Δit (-(-s)) (W.U a (A (W.U (-a) W.vac)))⟫_ℂ
        = ⟪(star B) W.vac, W.U (-a) (C.Δit (-(-s)) (W.U a (A W.vac)))⟫_ℂ
      rw [W.vac_invariant, U_inner_adj]
  have hD := hTak D hD0 hDadd hvac hpres hkms t
  have hc : ∀ x : W.H, C.Δit t (W.U a x) = W.U a (C.Δit t x) := by
    intro x
    have h := congrArg (fun E : W.H ≃ₗᵢ[ℂ] W.H => E x) hD
    simp only [hDapply] at h
    have h' := congrArg (W.U a) h
    rw [U_pos_neg_apply] at h'
    exact h'
  ext y
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply]
  rw [hc, LinearIsometryEquiv.apply_symm_apply]

#print axioms Δit_preserves_wedge
#print axioms kmsUnique_forbids_Z2
#print axioms kmsUnique_implies_group
#print axioms flag_net_excludes_v3_group

end

end TGLExt.ContratoQGv3.CeticoVacuidade
