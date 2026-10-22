import ContratoQG_v3_Teoremas
import ContratoQG
import W5ParedeEspectral
import ProbeToyContratoH2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# CONTRATO v3 — AS PAREDES: v2 ∩ v3 = ∅, o brinquedo de W5, o par legado
  [RASCUNHO DE GERÊNCIA — frente contrato_v3, 23/09/2026; scratchpad; NÃO cunha nome reservado]

  Importa, em cópias BYTE-IDÊNTICAS (sha16 conferido no manifesto): a v2 `ContratoQG.lean`
  (02fd013827dca251), `W5ParedeEspectral.lean` (a4ee57ff4b05bb84) e `ProbeToyContratoH2.lean`
  (e84250c065d6f6d8), recompiladas contra os oleans do kernel v370.

  §1 PONTES DE HOMÔNIMOS (regra dos dois regimes, item 2): `wedgeBoostMap`, `killingField`, `nullDir` e
     `NoEigenOutsideVacuum` existem na v2/W5 e na v3 — são ligadas aqui por `rfl`/`Iff.rfl`, lema a lema.
  §2 ★★★ v2 ∩ v3 = ∅: nenhum par (W, R) habita as duas (a v2 força espectro pontual, a v3 o proíbe,
     e o implementador é único).
  §3 O BRINQUEDO DE W5 (U(a) = Δ^{i a₂}): habita a v2 (W5, medido) e NÃO habita a v3 — por DUAS rotas
     independentes (fidelidade; espectro). E ele PAGA a cláusula (S)-v3 inteira (grupo de boosts + BW):
     o que o exclui é o bloco (P), não (S) — dito como teorema.
  §4 O PAR LEGADO (U = 1): paga (S)-v3, energia positiva e continuidade; falha só fidelidade e
     ergodicidade nula — por teorema.
  β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt.ContratoQGv3.Paredes

open TGL.SpecificAQFT TGL.ModularRealization TGLV354.TraceCompletion ChatgptAudit
open TGLExt.ContratoQGv3
open scoped InnerProductSpace

noncomputable section

/-! ## §1 — pontes de homônimos -/

theorem wedgeBoostMap_bridge (s : ℝ) (x : Fin 4 → ℝ) :
    TGLExt.ContratoQG.wedgeBoostMap s x = TGLExt.ContratoQGv3.wedgeBoostMap s x := rfl

theorem killingField_bridge (κ : ℝ) (x : Fin 4 → ℝ) :
    TGLExt.ContratoQG.killingField κ x = TGLExt.ContratoQGv3.killingField κ x := rfl

theorem nullDir_bridge : TGLExt.ContratoQG.nullGenerator = TGLExt.ContratoQGv3.nullDir := rfl

theorem noEigen_bridge (W : TGLSpecificAQFTWitness) (D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) :
    W5Final.Espectral.NoEigenOutsideVacuum W D ↔ TGLExt.ContratoQGv3.NoEigenOutsideVacuum W D :=
  Iff.rfl

/-! ## §2 — ★★★ v2 ∩ v3 = ∅ -/

/-- [DERIVED] ★★★ NENHUM par (W, R) habita a v2 E a v3: o implementador é único (`implementer_unique`);
    a v2 força autovetor fora de ℂΩ (`contratoH2_forces_point_spectrum`, W5); a v3 proíbe
    (`no_point_spectrum`). A correção D-B é, portanto, uma troca de lado, não um afrouxamento. -/
theorem v2_v3_disjoint {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    (C2 : TGLExt.ContratoQG.ContratoH2 W R) (C3 : TGLExt.ContratoQGv3.ContratoH2 W R) : False := by
  have heq : ∀ t, C2.Δit t = C3.Δit t := fun t =>
    implementer_unique C2.Δit C3.Δit C2.Δit_vac C3.Δit_vac C2.flow_implemented C3.flow_implemented t
  apply W5Final.Espectral.contratoH2_forces_point_spectrum C2
  intro v r hv
  apply C3.no_point_spectrum v r
  intro t
  rw [← heq t]
  exact hv t

theorem v3_empty_of_v2_nonempty {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    (h : Nonempty (TGLExt.ContratoQG.ContratoH2 W R)) :
    IsEmpty (TGLExt.ContratoQGv3.ContratoH2 W R) :=
  ⟨fun C3 => v2_v3_disjoint h.some C3⟩

/-! ## §3 — o brinquedo de W5 -/

open W5Final.Toy

/-- [DERIVED] (medido em W5, recompilado aqui) o brinquedo HABITA a v2. -/
theorem toy_inhabits_v2 : Nonempty (TGLExt.ContratoQG.ContratoH2 toyW toyR) :=
  contratoH2_inhabited_by_toy

/-- [DERIVED] ★★ ROTA 1 (espectro): o brinquedo NÃO habita a v3 — porque habita a v2. -/
theorem toy_not_v3_by_spectrum : IsEmpty (TGLExt.ContratoQGv3.ContratoH2 toyW toyR) :=
  v3_empty_of_v2_nonempty toy_inhabits_v2

/-- o brinquedo é infiel na direção nula: U(n) = Δ^{i·0} = 1. -/
theorem toy_null_trivial (l : ℝ) : toyW.U (l • nullDir) = 1 := by
  change toyU (l • nullDir) = 1
  ext v
  rw [toyU_apply]
  simpa [nullDir] using modularFlow_zero_time (P := mixProfile) v

/-- [DERIVED] ★★ ROTA 2 (fidelidade): o brinquedo NÃO habita a v3 — U(n) = 1 com n ≠ 0. -/
theorem toy_not_v3_by_fidelity : IsEmpty (TGLExt.ContratoQGv3.ContratoH2 toyW toyR) :=
  contratoH2_empty_of_unfaithful _ _ ⟨nullDir, by
    intro h; have := congrFun h 0; simp [nullDir] at this, by simpa using toy_null_trivial 1⟩

/-- [DERIVED] o brinquedo viola a ergodicidade nula (todo vetor é invariante; W.H tem dimensão ∞). -/
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

/-- o candidato natural a grupo de boosts do brinquedo: V(s) := Δ^{−is/2π} (o fluxo da torre em rapidez). -/
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

/-- [DERIVED] ★ o brinquedo PAGA a cláusula (S)-v3: há um grupo de boosts covariante em W.H. -/
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

/-- [DERIVED] ★ e satisfaz BW com ele: Δ^{it} (o fluxo da torre) = V(−2πt). -/
theorem toy_bw (t : ℝ) : u t = toyBoost.V (-(2 * Real.pi * t)) := by
  ext v
  change modularFlow mixProfile t v = modularFlow mixProfile (-((-(2 * Real.pi * t)) / (2 * Real.pi))) v
  congr 1
  have : (2 * Real.pi) ≠ 0 := by positivity
  field_simp

/-- [DERIVED] ★★ A LEITURA EXATA do D-A na v3: a cláusula (S)+BW sozinha NÃO exclui o brinquedo (ele a paga,
    com o espectro PONTUAL da torre); o que o exclui é o bloco (P) — fidelidade e ergodicidade nula.
    Por isso `no_point_spectrum` usa (P): (S) sozinha é compatível com espectro pontual; (S)+(P) não. -/
theorem toy_pays_state_clause_but_not_P :
    (∃ B : WedgeBoostRep toyW, ∀ t, u t = B.V (-(2 * Real.pi * t))) ∧
    (∃ a : Fin 4 → ℝ, a ≠ 0 ∧ toyW.U a = 1) ∧
    ¬ (∀ ψ : toyW.H, (∀ l : ℝ, toyW.U (l • nullDir) ψ = ψ) → ψ ∈ (ℂ ∙ toyW.vac)) :=
  ⟨⟨toyBoost, toy_bw⟩,
   ⟨nullDir, by intro h; have := congrFun h 0; simp [nullDir] at this, by simpa using toy_null_trivial 1⟩,
   toy_not_null_ergodic⟩

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

/-- [DERIVED] o par legado tem energia positiva (U = 1: a correlação é constante). -/
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

/-- [DERIVED] ★★ A LEITURA EXATA no par legado: paga (S)+BW, energia positiva e continuidade; falha
    SÓ a fidelidade e a ergodicidade nula. -/
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

/-- [DERIVED] a v2 também é vazia no par legado, e a v3 idem (duas razões: fidelidade; ergodicidade). -/
theorem legacy_empty_both :
    IsEmpty (TGLExt.ContratoQG.ContratoH2 theSpecificAQFTWitness regularModularRealization) ∧
    IsEmpty (TGLExt.ContratoQGv3.ContratoH2 theSpecificAQFTWitness regularModularRealization) :=
  ⟨TGLExt.ContratoQG.contratoH2_empty_on_legacy_realization, contratoH2_empty_on_legacy⟩

/-- [DERIVED] `theHorizon` (o habitante genérico de H3 que acende a bandeira formal) NÃO é a projeção de
    contrato H3 v3 algum no par legado, nem no brinquedo. -/
theorem theHorizon_not_a_v3_projection :
    (¬ ∃ C : TGLExt.ContratoQGv3.ContratoH3 theSpecificAQFTWitness regularModularRealization,
        C.toHorizonData = theHorizon) ∧
    (¬ ∃ C : TGLExt.ContratoQGv3.ContratoH3 toyW toyR, C.toHorizonData = theHorizon) :=
  ⟨fun ⟨C, _⟩ => contratoH2_empty_on_legacy.false C.H2,
   fun ⟨C, _⟩ => toy_not_v3_by_fidelity.false C.H2⟩

/-! ## §5 — o ÚNICO W do kernel v370 -/

/-- [DERIVED] ★★ O kernel v370 tem UM termo de `TGLSpecificAQFTWitness` (`theSpecificAQFTWitness`,
    WedgeNet.lean:357; o `trivialWitness` de ProbeTrivial não compila por projeto). Com U = 1 ele não admite
    contrato H2 v3 com NENHUMA realização R — a resposta à pergunta «há par no kernel que habite a v3?» é
    NÃO, por teorema, para todo R. -/
theorem v3_empty_on_the_kernel_witness (R : TGLModularRealization theSpecificAQFTWitness) :
    IsEmpty (TGLExt.ContratoQGv3.ContratoH2 theSpecificAQFTWitness R) :=
  contratoH2_empty_of_unfaithful _ R ⟨nullDir, by
    intro h; have := congrFun h 0; simp [nullDir] at this, rfl⟩

theorem v3H3_empty_on_the_kernel_witness (R : TGLModularRealization theSpecificAQFTWitness) :
    IsEmpty (TGLExt.ContratoQGv3.ContratoH3 theSpecificAQFTWitness R) :=
  ⟨fun C => (v3_empty_on_the_kernel_witness R).false C.H2⟩

theorem v3Import_impossible_on_the_kernel_witness (R : TGLModularRealization theSpecificAQFTWitness) :
    ¬ ∃ h2 : TGLExt.ContratoQGv3.ContratoH2 theSpecificAQFTWitness R,
        Nonempty (TGLExt.ContratoQGv3.ContratoImportH3 theSpecificAQFTWitness R h2) :=
  fun ⟨h2, _⟩ => (v3_empty_on_the_kernel_witness R).false h2

/-! ## §6 — o import no MESMO horizonte (consumidor de `same_horizon`, medido como sem consumidor na mutação) -/

/-- [DERIVED] (lê `same_horizon`) o H3 produzido pelo import sobre o índice tem o MESMO κ, o MESMO Δit e o
    MESMO grupo de boosts do índice — a temperatura de Unruh do H3 importado é a do H2 reservado. -/
theorem import_same_horizon_data {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {h2 : TGLExt.ContratoQGv3.ContratoH2 W R} (I : TGLExt.ContratoQGv3.ContratoImportH3 W R h2) :
    (I.produce h2).H2.kappa = h2.kappa ∧ (I.produce h2).H2.Δit = h2.Δit ∧
      (I.produce h2).H2.boost = h2.boost := by
  rw [I.same_horizon h2]
  exact ⟨rfl, rfl, rfl⟩

/-- [DERIVED] e a Clausius do H3 importado é lida com a temperatura do índice. -/
theorem import_clausius_on_index {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {h2 : TGLExt.ContratoQGv3.ContratoH2 W R} (I : TGLExt.ContratoQGv3.ContratoImportH3 W R h2)
    {ψ : W.H} (hψ : ψ ∈ (I.produce h2).admissible) {b : ℝ}
    (hb : HasBoostEnergy (I.produce h2).H2.boost.V ψ b) :
    (I.produce h2).heat ψ = h2.unruhTemperature * (2 * Real.pi * b) := by
  rw [ContratoH3.clausius _ hψ hb]
  unfold ContratoH2.unruhTemperature
  rw [(import_same_horizon_data I).1]

#print axioms wedgeBoostMap_bridge
#print axioms killingField_bridge
#print axioms nullDir_bridge
#print axioms noEigen_bridge
#print axioms v2_v3_disjoint
#print axioms v3_empty_of_v2_nonempty
#print axioms toy_inhabits_v2
#print axioms toy_not_v3_by_spectrum
#print axioms toy_not_v3_by_fidelity
#print axioms toy_not_null_ergodic
#print axioms toyBoost
#print axioms toy_bw
#print axioms toy_pays_state_clause_but_not_P
#print axioms legacyBoost
#print axioms legacy_positive_energy
#print axioms legacy_not_null_ergodic
#print axioms legacy_pays_all_but_P_teeth
#print axioms legacy_empty_both
#print axioms theHorizon_not_a_v3_projection
#print axioms v3_empty_on_the_kernel_witness
#print axioms v3H3_empty_on_the_kernel_witness
#print axioms v3Import_impossible_on_the_kernel_witness
#print axioms import_same_horizon_data
#print axioms import_clausius_on_index

end

end TGLExt.ContratoQGv3.Paredes
