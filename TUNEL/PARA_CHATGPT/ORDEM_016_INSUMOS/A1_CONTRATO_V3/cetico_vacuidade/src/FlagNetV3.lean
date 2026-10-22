import ContratoQG_v3_Teoremas

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# FlagNetV3 — a rede das cunhas POR BANDEIRAS não carrega a v3, em Hilbert algum
  [RASCUNHO DE GERÊNCIA — frente contrato_v3, 23/09/2026; scratchpad; condicional a Takesaki, NOMEADO]

  A rede do kernel (`wedgeNet`, WedgeNet.lean) dá a MESMA álgebra a toda região que contém um transladado
  da cunha (`wedgeNet_translate`): a álgebra da cunha é invariante por TODAS as translações. Aqui:
  se U(a)·M·U(−a) ⊆ M para todo a (M = W.net cunha), então — DADA a unicidade KMS do grupo modular
  (hipótese `KMSUnique`, [KNOWN: Takesaki], não formalizada na mathlib da casa) — U comuta com Δ^{it}, e o
  dente de fidelidade (via `commuting_translations_excluded`) esvazia a v3. Leitura para a bancada: o
  par físico não sai de trocar o Hilbert sob a rede de bandeiras; é preciso REDE com localização genuína
  (M(W + a) ⊊ M(W) para a no interior da cunha — inclusões semilaterais, Borchers).
-/

namespace TGLExt.ContratoQGv3.FlagNet

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv3
open scoped InnerProductSpace

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}

theorem U_pos_neg_apply (W : TGLSpecificAQFTWitness) (a : Fin 4 → ℝ) (x : W.H) :
    W.U a (W.U (-a) x) = x := by
  have := U_neg_apply W (-a) x
  rwa [neg_neg] at this

/-- a translação como isometria unitária. -/
def Uiso (W : TGLSpecificAQFTWitness) (a : Fin 4 → ℝ) : W.H ≃ₗᵢ[ℂ] W.H where
  toFun := W.U a
  invFun := W.U (-a)
  map_add' := map_add _
  map_smul' := map_smul _
  left_inv := fun x => U_neg_apply W a x
  right_inv := fun x => U_pos_neg_apply W a x
  norm_map' := U_norm W a

/-- o boost preserva a cunha, como igualdade de conjuntos. -/
theorem boost_image_rightWedge (s : ℝ) : wedgeBoostMap s '' rightWedge = rightWedge := by
  have hmem : ∀ (r : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge → wedgeBoostMap r x ∈ rightWedge := by
    intro r x hx
    have hx' : |x 0| < x 1 := hx
    show |wedgeBoostMap r x 0| < wedgeBoostMap r x 1
    rw [wedgeBoostMap_apply0, wedgeBoostMap_apply1, abs_lt]
    obtain ⟨h1, h2⟩ := abs_lt.mp hx'
    have e1 := Real.cosh_sub_sinh r
    have e2 := Real.cosh_add_sinh r
    have p1 : 0 < (Real.cosh r - Real.sinh r) * (x 1 - x 0) := by
      rw [e1]; exact mul_pos (Real.exp_pos _) (by linarith)
    have p2 : 0 < (Real.cosh r + Real.sinh r) * (x 1 + x 0) := by
      rw [e2]; exact mul_pos (Real.exp_pos _) (by linarith)
    constructor <;> nlinarith
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    exact hmem s x hx
  · intro hy
    refine ⟨wedgeBoostMap (-s) y, hmem (-s) y hy, ?_⟩
    rw [← wedgeBoostMap_add, add_neg_cancel, wedgeBoostMap_zero]

/-- **a unicidade KMS** (Takesaki), como HIPÓTESE NOMEADA: todo grupo de unitários que fixa Ω, preserva a
    álgebra da cunha e é KMS a β = 1 (na convenção do contrato) É o Δit do contrato. -/
def KMSUnique (C : ContratoH2 W R) : Prop :=
  ∀ D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H), (∀ t, D t W.vac = W.vac) →
    (∀ (t : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D t).conjStarAlgEquiv T ∈ W.net rightWedge) →
    KMSAt W (fun t => D (-t)) 1 → ∀ t, D t = C.Δit t

/-- [DERIVED, condicional a `KMSUnique`] ★★ REDE POR BANDEIRAS ⟹ v3 VAZIA: se a álgebra da cunha é invariante
    por todas as translações, nenhum contrato v3 existe (com a unicidade KMS de Takesaki). -/
theorem flag_net_excludes_v3 (C : ContratoH2 W R) (hTak : KMSUnique C)
    (hinv : ∀ (a : Fin 4 → ℝ) (T : W.H →L[ℂ] W.H),
      T ∈ W.net rightWedge → W.U a * T * W.U (-a) ∈ W.net rightWedge) : False := by
  apply C.commuting_translations_excluded
  intro t a
  let D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H) := fun s => ((Uiso W a).trans (C.Δit s)).trans (Uiso W a).symm
  have hDapply : ∀ s x, D s x = W.U (-a) (C.Δit s (W.U a x)) := fun s x => rfl
  have hvac : ∀ s, D s W.vac = W.vac := by
    intro s
    rw [hDapply, W.vac_invariant, C.Δit_vac, W.vac_invariant]
  have hΔpres : ∀ (s : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (C.Δit s).conjStarAlgEquiv T ∈ W.net rightWedge := by
    intro s T hT
    have h := C.bw_covariance s rightWedge T hT
    rwa [boost_image_rightWedge] at h
  have hpres : ∀ (s : ℝ) (T : W.H →L[ℂ] W.H), T ∈ W.net rightWedge →
      (D s).conjStarAlgEquiv T ∈ W.net rightWedge := by
    intro s T hT
    have e : (D s).conjStarAlgEquiv T
        = W.U (-a) * ((C.Δit s).conjStarAlgEquiv (W.U a * T * W.U (-a))) * W.U (-(-a)) := by
      ext x
      simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply, neg_neg]
      rfl
    rw [e]
    exact hinv (-a) _ (hΔpres s _ (hinv a T hT))
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
  have hD := hTak D hvac hpres hkms t
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

#print axioms boost_image_rightWedge
#print axioms flag_net_excludes_v3

end

end TGLExt.ContratoQGv3.FlagNet
