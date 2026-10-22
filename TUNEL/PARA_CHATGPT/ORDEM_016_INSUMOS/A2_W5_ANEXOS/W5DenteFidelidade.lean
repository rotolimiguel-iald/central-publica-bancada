import ProbeToyContratoH2

set_option autoImplicit false

/-!
# W5DenteFidelidade — um dente PROPOSTO para o ANEXO A v3 (frente W5_final, 23/09/2026)

  [PROPOSTA DE GERÊNCIA, scratchpad; o contrato é da gerência (frente W2), não desta frente nem da bancada]

  `ProbeToyContratoH2` mostrou [REAL, rc=0] que `ContratoH2` (W2_final, 02fd013827dca251) é habitado por
  um brinquedo cujas «translações» são o próprio fluxo modular (U(a) = Δ^{i a²}). Aqui:

  1. `commuting_translations_are_not_faithful` [DERIVED]: em QUALQUER contrato, se as translações comutam
     com Δ^{it}, a relação de Poincaré (B3) aplicada ao vetor nulo n = (1,1,0,0) da cunha força
     U((e^{−2π} − 1)·n) = 1 — uma translação não nula age trivialmente. Puramente algébrico (U_add), sem
     continuidade nem espectro.
  2. `ContratoH2F` = `ContratoH2` + `translations_faithful : ∀ a, W.U a = 1 → a = 0` (o dente proposto).
     Pelo item 1, a fidelidade exclui TODA a classe de brinquedos em que U comuta com o fluxo.
  3. `toy_fails_faithful` [DERIVED]: o brinquedo concreto não habita `ContratoH2F`.

  O que NÃO se mede aqui [OPEN]: se `ContratoH2F` ainda admite brinquedos de outra classe (U que não
  comuta com Δ^{it} mas também não é representação de energia positiva). A fidelidade é a sombra
  algébrica da covariância de Poincaré (Borchers); a condição espectral não está enunciada.
  Estatutos: [DERIVED] os teoremas; [CONJECTURE] que o dente baste. Sem sorry, sem axiom; β não aparece.
-/

namespace W5Final.Dente

open TGL.SpecificAQFT TGL.ModularRealization ChatgptAudit
open TGLExt TGLExt.ContratoQG W5Final.Toy

noncomputable section

/-- o vetor nulo do horizonte futuro da cunha. -/
def nullDir : Fin 4 → ℝ := ![1, 1, 0, 0]

theorem boost_nullDir (χ : ℝ) : wedgeBoostMap χ nullDir = Real.exp χ • nullDir := by
  funext i
  fin_cases i <;>
    simp [nullDir, wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four,
      ← Real.cosh_add_sinh] <;> ring

/-- [DERIVED] ★★ translações que comutam com o fluxo modular não são fiéis (via (B3) no vetor nulo). -/
theorem commuting_translations_are_not_faithful {W : TGLSpecificAQFTWitness}
    {R : TGLModularRealization W} (C : ContratoH2 W R)
    (hcomm : ∀ (t : ℝ) (a : Fin 4 → ℝ), (C.Δit t).conjStarAlgEquiv (W.U a) = W.U a) :
    ∃ a : Fin 4 → ℝ, a ≠ 0 ∧ W.U a = 1 := by
  set m : Fin 4 → ℝ := (Real.exp (-(2 * Real.pi * 1)) - 1) • nullDir with hm
  refine ⟨m, ?_, ?_⟩
  · intro h0
    have h := congrFun h0 0
    have hpi : (0 : ℝ) < 2 * Real.pi := by positivity
    have hlt : Real.exp (-(2 * Real.pi)) < 1 := by
      have := Real.exp_lt_exp.mpr (show -(2 * Real.pi) < 0 by linarith)
      simpa using this
    simp [hm, nullDir] at h
    linarith
  · have hB := C.poincare_relation 1 nullDir
    rw [hcomm, boost_nullDir] at hB
    have hsplit : Real.exp (-(2 * Real.pi * 1)) • nullDir = nullDir + m := by
      rw [hm, sub_smul, one_smul]; abel
    rw [hsplit, W.U_add] at hB
    have hinv : W.U (-nullDir) * W.U nullDir = 1 := by
      rw [← W.U_add, neg_add_cancel, W.U_zero]
    calc W.U m = (W.U (-nullDir) * W.U nullDir) * W.U m := by rw [hinv, one_mul]
      _ = W.U (-nullDir) * (W.U nullDir * W.U m) := by rw [mul_assoc]
      _ = W.U (-nullDir) * W.U nullDir := by rw [← hB]
      _ = 1 := hinv

/-- o contrato com o dente proposto. -/
structure ContratoH2F (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    extends ContratoH2 W R where
  translations_faithful : ∀ a : Fin 4 → ℝ, W.U a = 1 → a = 0

/-- [DERIVED] ★ com o dente, a classe inteira dos brinquedos que comutam com o fluxo é excluída. -/
theorem faithful_excludes_commuting_toys {W : TGLSpecificAQFTWitness}
    {R : TGLModularRealization W} (C : ContratoH2F W R) :
    ¬ ∀ (t : ℝ) (a : Fin 4 → ℝ), (C.Δit t).conjStarAlgEquiv (W.U a) = W.U a := by
  intro hcomm
  obtain ⟨a, ha, hU⟩ := commuting_translations_are_not_faithful C.toContratoH2 hcomm
  exact ha (C.translations_faithful a hU)

/-- [DERIVED] ★ o brinquedo de `ProbeToyContratoH2` NÃO habita o contrato com o dente
    (U(1,1,0,0) = Δ^{i·0} = 1). -/
theorem toy_fails_faithful : IsEmpty (ContratoH2F toyW toyR) := by
  refine ⟨fun C => ?_⟩
  have h := C.translations_faithful nullDir (by
    change toyU nullDir = 1
    ext v
    rw [toyU_apply]
    simpa [nullDir] using modularFlow_zero_time (P := mixProfile) v)
  have := congrFun h 0
  simp [nullDir] at this

/-- [DERIVED] o par legado também não habita (U = 1 é o caso extremo). -/
theorem legacy_fails_faithful :
    IsEmpty (ContratoH2F theSpecificAQFTWitness TGLV354.TraceCompletion.regularModularRealization) :=
  ⟨fun C => contratoH2_empty_on_legacy_realization.false C.toContratoH2⟩

#print axioms boost_nullDir
#print axioms commuting_translations_are_not_faithful
#print axioms faithful_excludes_commuting_toys
#print axioms toy_fails_faithful
#print axioms legacy_fails_faithful

end

end W5Final.Dente
