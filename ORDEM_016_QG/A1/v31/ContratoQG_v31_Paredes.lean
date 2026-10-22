import ContratoQG_v31_Teoremas
import ContratoQG
import W5ParedeEspectral
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CONTRATO v3.1 — AS PAREDES: v2 ∩ v3.1 = ∅, o brinquedo de W5, o par legado, o único W do kernel
  [RASCUNHO DE GERÊNCIA — frente contrato_v3, RODADA 2, 23/09/2026; scratchpad; NÃO cunha nome reservado]

  Importa, em cópias BYTE-IDÊNTICAS: a v2 `ContratoQG.lean` (02fd013827dca251), `W5ParedeEspectral.lean`
  (a4ee57ff4b05bb84) e `ProbeToyContratoH2.lean` (e84250c065d6f6d8), recompiladas contra o kernel v370.
  Tudo quantificado sobre TODO índice N (normalização) e, em H3, TODO tensor T — nenhuma escolha.
-/

namespace TGLExt.ContratoQGv31.Paredes

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion ChatgptAudit
open TGLExt.ContratoQGv31
open scoped InnerProductSpace

noncomputable section

/-! ## §1 — pontes de homônimos com a v2 (regra dos dois regimes, item 2: ligadas lema a lema) -/

theorem wedgeBoostMap_bridge (s : ℝ) (x : Fin 4 → ℝ) :
    TGLExt.ContratoQG.wedgeBoostMap s x = TGLExt.ContratoQGv31.wedgeBoostMap s x := rfl

theorem killingField_bridge (κ : ℝ) (x : Fin 4 → ℝ) :
    TGLExt.ContratoQG.killingField κ x = TGLExt.ContratoQGv31.killingField κ x := rfl

theorem nullDir_bridge : TGLExt.ContratoQG.nullGenerator = TGLExt.ContratoQGv31.nullDir := rfl

theorem noEigen_bridge (W : TGLSpecificAQFTWitness) (D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) :
    W5Final.Espectral.NoEigenOutsideVacuum W D ↔ TGLExt.ContratoQGv31.NoEigenOutsideVacuum W D :=
  Iff.rfl

/-! ## §2 — ★★★ v2 ∩ v3.1 = ∅ (para todo N) -/

theorem v2_v31_disjoint {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization}
    (C2 : TGLExt.ContratoQG.ContratoH2 W R) (C3 : TGLExt.ContratoQGv31.ContratoH2 W R N) : False := by
  have heq : ∀ t, C2.Δit t = C3.Δit t := fun t =>
    implementer_unique C2.Δit C3.Δit C2.Δit_vac C3.Δit_vac C2.flow_implemented C3.flow_implemented t
  apply W5Final.Espectral.contratoH2_forces_point_spectrum C2
  intro v r hv
  apply C3.no_point_spectrum v r
  intro t
  rw [← heq t]
  exact hv t

theorem v31_empty_of_v2_nonempty {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    (N : KillingNormalization) (h : Nonempty (TGLExt.ContratoQG.ContratoH2 W R)) :
    IsEmpty (TGLExt.ContratoQGv31.ContratoH2 W R N) :=
  ⟨fun C3 => v2_v31_disjoint h.some C3⟩

/-! ## §3 — o brinquedo de W5 -/

open W5Final.Toy

theorem toy_inhabits_v2 : Nonempty (TGLExt.ContratoQG.ContratoH2 toyW toyR) :=
  contratoH2_inhabited_by_toy

/-- [DERIVED] ★★ ROTA 1 (espectro): o brinquedo NÃO habita a v3.1, para NENHUM N. -/
theorem toy_not_v31_by_spectrum (N : KillingNormalization) :
    IsEmpty (TGLExt.ContratoQGv31.ContratoH2 toyW toyR N) :=
  v31_empty_of_v2_nonempty N toy_inhabits_v2

theorem toy_null_trivial (l : ℝ) : toyW.U (l • nullDir) = 1 := by
  change toyU (l • nullDir) = 1
  ext v
  rw [toyU_apply]
  simpa [nullDir] using modularFlow_zero_time (P := mixProfile) v

/-- [DERIVED] ★★ ROTA 2 (fidelidade): o brinquedo NÃO habita a v3.1, para NENHUM N. -/
theorem toy_not_v31_by_fidelity (N : KillingNormalization) :
    IsEmpty (TGLExt.ContratoQGv31.ContratoH2 toyW toyR N) :=
  contratoH2_empty_of_unfaithful _ _ N ⟨nullDir, by
    intro h; have := congrFun h 0; simp [nullDir] at this, by simpa using toy_null_trivial 1⟩

theorem toy_not_null_ergodic :
    ¬ ∀ ψ : toyW.H, (∀ l : ℝ, toyW.U (l • nullDir) ψ = ψ) → ψ ∈ (ℂ ∙ toyW.vac) := by
  intro h
  have hall : ∀ ψ : toyW.H, ψ ∈ (ℂ ∙ toyW.vac) := by
    intro ψ
    apply h
    intro l
    rw [toy_null_trivial]
    rfl
  let S : Submodule ℂ toyW.H := ℂ ∙ toyW.vac
  have hsurj : Function.Surjective S.subtype := fun w => ⟨⟨w, hall w⟩, rfl⟩
  exact toyR.infiniteHilbert (Module.Finite.of_surjective S.subtype hsurj)

def towerV (s : ℝ) : WH ≃ₗᵢ[ℂ] WH := u (-(s / (2 * Real.pi)))

theorem towerV_apply (s : ℝ) (v : WH) : towerV s v = modularFlow mixProfile (-(s / (2 * Real.pi))) v := rfl

theorem towerV_zero : towerV 0 = LinearIsometryEquiv.refl ℂ WH := by
  ext v
  rw [towerV_apply]
  simpa using modularFlow_zero_time (P := mixProfile) v

theorem towerV_add (a b : ℝ) : towerV (a + b) = (towerV b).trans (towerV a) := by
  ext v
  rw [LinearIsometryEquiv.trans_apply, towerV_apply, towerV_apply, towerV_apply, modularFlow_group]
  congr 1
  ring

theorem towerV_continuous (ψ : WH) : Continuous (fun s : ℝ => towerV s ψ) := by
  have h : Continuous (fun s : ℝ => -(s / (2 * Real.pi))) := by fun_prop
  exact (modularFlow_strongly_continuous (P := mixProfile) ψ).comp h

theorem towerV_vac (s : ℝ) : towerV s (hOmega mixProfile) = hOmega mixProfile :=
  modularFlow_fixes_omega _

theorem two_pi_rescale (s : ℝ) : -(2 * Real.pi * (-(s / (2 * Real.pi)))) = s := by
  have : (2 * Real.pi) ≠ 0 := by positivity
  field_simp

def toyBoost : WedgeBoostRep toyW where
  V := towerV
  V_zero := towerV_zero
  V_add := towerV_add
  V_continuous := towerV_continuous
  V_vac := towerV_vac
  V_translations := by
    intro s a
    have h := toy_poincare_relation (-(s / (2 * Real.pi))) a
    rw [two_pi_rescale] at h
    exact h
  V_net := by
    intro s O T hT
    have h := toy_bw_covariance (-(s / (2 * Real.pi))) O T hT
    rw [two_pi_rescale] at h
    exact h

theorem toy_bw (t : ℝ) : u t = toyBoost.V (-(2 * Real.pi * t)) := by
  ext v
  change modularFlow mixProfile t v = modularFlow mixProfile (-((-(2 * Real.pi * t)) / (2 * Real.pi))) v
  congr 1
  have : (2 * Real.pi) ≠ 0 := by positivity
  field_simp

/-- [DERIVED] ★★ A LEITURA EXATA do D-A na v3.1: (S)+BW sozinha NÃO exclui o brinquedo; o bloco (P) exclui. -/
theorem toy_pays_state_clause_but_not_P :
    (∃ B : WedgeBoostRep toyW, ∀ t, u t = B.V (-(2 * Real.pi * t))) ∧
    (∃ a : Fin 4 → ℝ, a ≠ 0 ∧ toyW.U a = 1) ∧
    ¬ (∀ ψ : toyW.H, (∀ l : ℝ, toyW.U (l • nullDir) ψ = ψ) → ψ ∈ (ℂ ∙ toyW.vac)) :=
  ⟨⟨toyBoost, toy_bw⟩,
   ⟨nullDir, by intro h; have := congrFun h 0; simp [nullDir] at this, by simpa using toy_null_trivial 1⟩,
   toy_not_null_ergodic⟩

/-- [DERIVED] ★ (T4 do cético 1, aplicada ao brinquedo) o brinquedo tem momento nulo DISCRETO trivial: todo
    vetor é autovetor de U(λn) com ω = 0 — excluído também por `discrete_null_momentum_excluded`. -/
theorem toy_not_v31_by_null_momentum (N : KillingNormalization) :
    IsEmpty (TGLExt.ContratoQGv31.ContratoH2 toyW toyR N) := by
  apply discrete_null_momentum_excluded
  by_contra hcon
  push_neg at hcon
  apply toy_not_null_ergodic
  intro ψ hψ
  by_contra hψ'
  obtain ⟨l, hl⟩ := hcon ψ 0 hψ'
  apply hl
  rw [toy_null_trivial]
  simp

/-! ## §4 — o par legado (U = 1) -/

def legacyBoost : WedgeBoostRep theSpecificAQFTWitness where
  V := towerV
  V_zero := towerV_zero
  V_add := towerV_add
  V_continuous := towerV_continuous
  V_vac := towerV_vac
  V_translations := by
    intro s a
    rw [TGLExt.ContratoQG.legacy_translations_trivial, TGLExt.ContratoQG.legacy_translations_trivial]
    exact map_one _
  V_net := by
    intro s O T hT
    have h := legacy_bw_covariance (-(s / (2 * Real.pi))) O T hT
    rw [two_pi_rescale] at h
    exact h

theorem legacy_bw (t : ℝ) : modularFlowUnitary mixProfile t = legacyBoost.V (-(2 * Real.pi * t)) :=
  toy_bw t

theorem legacy_positive_energy : PositiveEnergy theSpecificAQFTWitness := by
  intro a ha ψ
  refine ⟨fun _ => ⟪ψ, ψ⟫_ℂ, diffContOnCl_const, ⟨‖⟪ψ, ψ⟫_ℂ‖, fun z _ => le_refl _⟩, ?_⟩
  intro t
  rw [TGLExt.ContratoQG.legacy_translations_trivial]
  rfl

theorem legacy_translations_continuous (ψ : theSpecificAQFTWitness.H) :
    Continuous (fun a : Fin 4 → ℝ => theSpecificAQFTWitness.U a ψ) := by
  have : (fun a : Fin 4 → ℝ => theSpecificAQFTWitness.U a ψ) = fun _ => ψ := by
    funext a; rw [TGLExt.ContratoQG.legacy_translations_trivial]; rfl
  rw [this]; exact continuous_const

theorem legacy_not_null_ergodic :
    ¬ ∀ ψ : theSpecificAQFTWitness.H,
      (∀ l : ℝ, theSpecificAQFTWitness.U (l • nullDir) ψ = ψ) → ψ ∈ (ℂ ∙ theSpecificAQFTWitness.vac) := by
  intro h
  have hall : ∀ ψ : theSpecificAQFTWitness.H, ψ ∈ (ℂ ∙ theSpecificAQFTWitness.vac) := by
    intro ψ
    apply h
    intro l
    rw [TGLExt.ContratoQG.legacy_translations_trivial]
    rfl
  let S : Submodule ℂ theSpecificAQFTWitness.H := ℂ ∙ theSpecificAQFTWitness.vac
  have hsurj : Function.Surjective S.subtype := fun w => ⟨⟨w, hall w⟩, rfl⟩
  exact regularModularRealization.infiniteHilbert (Module.Finite.of_surjective S.subtype hsurj)

theorem legacy_pays_all_but_P_teeth :
    (∃ B : WedgeBoostRep theSpecificAQFTWitness,
        ∀ t, modularFlowUnitary mixProfile t = B.V (-(2 * Real.pi * t))) ∧
    PositiveEnergy theSpecificAQFTWitness ∧
    (∀ ψ : theSpecificAQFTWitness.H, Continuous (fun a : Fin 4 → ℝ => theSpecificAQFTWitness.U a ψ)) ∧
    (∃ a : Fin 4 → ℝ, a ≠ 0 ∧ theSpecificAQFTWitness.U a = 1) ∧
    ¬ (∀ ψ : theSpecificAQFTWitness.H,
      (∀ l : ℝ, theSpecificAQFTWitness.U (l • nullDir) ψ = ψ) → ψ ∈ (ℂ ∙ theSpecificAQFTWitness.vac)) :=
  ⟨⟨legacyBoost, legacy_bw⟩, legacy_positive_energy, legacy_translations_continuous,
   ⟨nullDir, by intro h; have := congrFun h 0; simp [nullDir] at this, rfl⟩,
   legacy_not_null_ergodic⟩

theorem legacy_empty_both (N : KillingNormalization) :
    IsEmpty (TGLExt.ContratoQG.ContratoH2 theSpecificAQFTWitness regularModularRealization) ∧
    IsEmpty (TGLExt.ContratoQGv31.ContratoH2 theSpecificAQFTWitness regularModularRealization N) :=
  ⟨TGLExt.ContratoQG.contratoH2_empty_on_legacy_realization, contratoH2_empty_on_legacy N⟩

/-- `theHorizon` (o habitante genérico de H3 que acende a bandeira formal) NÃO é projeção de H3 v3.1 algum no
    par legado nem no brinquedo, para TODO N, T e janela. -/
theorem theHorizon_not_a_v31_projection (N : KillingNormalization) :
    (∀ T : StressTensorData theSpecificAQFTWitness,
      IsEmpty (TGLExt.ContratoQGv31.ContratoH3 theSpecificAQFTWitness regularModularRealization N T)) ∧
    (∀ T : StressTensorData toyW, IsEmpty (TGLExt.ContratoQGv31.ContratoH3 toyW toyR N T)) :=
  ⟨fun T => ⟨fun C => (contratoH2_empty_on_legacy N).false C.H2⟩,
   fun T => ⟨fun C => (toy_not_v31_by_fidelity N).false C.H2⟩⟩

/-! ## §5 — o ÚNICO W do kernel v370 -/

/-- [DERIVED] ★★ o kernel v370 tem UM termo de `TGLSpecificAQFTWitness` (`theSpecificAQFTWitness`,
    WedgeNet.lean:357), com U = 1: NENHUM contrato H2 v3.1, para NENHUMA realização R e NENHUM N. -/
theorem v31_empty_on_the_kernel_witness (R : TGLModularRealization theSpecificAQFTWitness)
    (N : KillingNormalization) :
    IsEmpty (TGLExt.ContratoQGv31.ContratoH2 theSpecificAQFTWitness R N) :=
  contratoH2_empty_of_unfaithful _ R N ⟨nullDir, by
    intro h; have := congrFun h 0; simp [nullDir] at this, rfl⟩

theorem v31H3_empty_on_the_kernel_witness (R : TGLModularRealization theSpecificAQFTWitness)
    (N : KillingNormalization) (T : StressTensorData theSpecificAQFTWitness) :
    IsEmpty (TGLExt.ContratoQGv31.ContratoH3 theSpecificAQFTWitness R N T) :=
  ⟨fun C => (v31_empty_on_the_kernel_witness R N).false C.H2⟩

theorem v31Import_impossible_on_the_kernel_witness (R : TGLModularRealization theSpecificAQFTWitness)
    (N : KillingNormalization) (T : StressTensorData theSpecificAQFTWitness) :
    ¬ ∃ h2 : TGLExt.ContratoQGv31.ContratoH2 theSpecificAQFTWitness R N,
        Nonempty (TGLExt.ContratoQGv31.ContratoImportH3 theSpecificAQFTWitness R N T h2) :=
  fun ⟨h2, _⟩ => (v31_empty_on_the_kernel_witness R N).false h2

#print axioms wedgeBoostMap_bridge
#print axioms killingField_bridge
#print axioms nullDir_bridge
#print axioms noEigen_bridge
#print axioms v2_v31_disjoint
#print axioms v31_empty_of_v2_nonempty
#print axioms toy_inhabits_v2
#print axioms toy_not_v31_by_spectrum
#print axioms toy_not_v31_by_fidelity
#print axioms toy_not_null_ergodic
#print axioms toyBoost
#print axioms toy_bw
#print axioms toy_pays_state_clause_but_not_P
#print axioms toy_not_v31_by_null_momentum
#print axioms legacyBoost
#print axioms legacy_positive_energy
#print axioms legacy_not_null_ergodic
#print axioms legacy_pays_all_but_P_teeth
#print axioms legacy_empty_both
#print axioms theHorizon_not_a_v31_projection
#print axioms v31_empty_on_the_kernel_witness
#print axioms v31H3_empty_on_the_kernel_witness
#print axioms v31Import_impossible_on_the_kernel_witness

end

end TGLExt.ContratoQGv31.Paredes
