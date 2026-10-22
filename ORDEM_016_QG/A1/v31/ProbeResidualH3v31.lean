import ContratoQG_v31

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 2000000

/-!
# ProbeResidualH3v31 — A DÍVIDA EXATA DE H3 v3.1, medida   [DIAGNÓSTICO POSITIVO; DEVE COMPILAR]
  Frente contrato_v3, RODADA 2, 23/09/2026. Importa SÓ o tipo.

  Resposta ao cético 1 (BLOQUEANTE) e ao cético 2 («a dívida real sai de graça»): na v3.1, dado um H2, o tensor T
  do par e a classe A com o elo `modular_charge`, H3 é EQUIVALENTE (as duas direções, abaixo) a UMA SOLUÇÃO
  COVARIANTE da equação nn ao longo do gerador, dada como LEI FIXA DA FONTE a = a[f] (não por estado):
        a[T(ψ)](x + λn)′ = θ_ψ(x + λn),  θ_ψ(x + λn)′ = −8πG·T_nn(ψ)(x + λn),  a[0] = 0,  a[f(· − b)] = a[f](· − b).
  Isto é a componente nn da equação de Einstein linearizada (Raychaudhuri + Einstein, gauge h·n = 0) — não um
  número ajustado por estado: a fonte T_nn(ψ) é do PAR, e a solução tem de valer em TODO ponto x.
  [DERIVED à mão, NÃO formalizado]: se T_nn(ψ) decai ao longo dos geradores (∫_λ^∞ μ|T_nn| < ∞), a solução
  teleológica θ(x) = 8πG∫_0^∞ T_nn(x + μn)dμ, a(x) = −8πG∫_0^∞ μ T_nn(x + μn)dμ existe e é covariante. O que
  H3 v3.1 NÃO contém: as demais componentes de Einstein (exigem a família de Lorentz das cunhas — W não tem
  rotações) e o valor de G (Jacobson: G = 1/(4ħη) é entrada).
-/

namespace TGLExt.ContratoQGv31.ProbeResidual

open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
open MeasureTheory Matrix

noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- o tipo das fontes: campos de tensão x ↦ T_ab(x). -/
abbrev Source := (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ

/-- uma SOLUÇÃO COVARIANTE da equação nn ao longo de n, como LEI FIXA da fonte (a densidade de área é um
    funcional da fonte, não do estado), com fonte T, na classe A. -/
structure NullSolution (W : TGLSpecificAQFTWitness) (T : StressTensorData W) (G : ℝ) (A : Set W.H) where
  a : Source → (Fin 4 → ℝ) → ℝ
  θ : W.H → (Fin 4 → ℝ) → ℝ
  a_zero : ∀ x, a 0 x = 0
  a_cov : ∀ (b : Fin 4 → ℝ) (f : Source) (x : Fin 4 → ℝ), a (fun y => f (y - b)) x = a f (x - b)
  a_deriv : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ, HasDerivAt (fun l : ℝ => a (T.T ψ) (x + l • nullDir)) (θ ψ x) 0
  θ_deriv : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ,
    HasDerivAt (fun l : ℝ => θ ψ (x + l • nullDir)) (-(8 * Real.pi * G) * nullEnergy T ψ x) 0

/-- o propagador de uma lei de área a: 𝔉(f) = diag(0, 0, −a(f), −a(f)) (gauge h·n = 0). -/
def responseOf (a : Source → (Fin 4 → ℝ) → ℝ) : Source → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ :=
  fun f x => Matrix.diagonal ![0, 0, -(a f x), -(a f x)]

theorem areaDensity_responseOf (a : Source → (Fin 4 → ℝ) → ℝ) (f : Source) :
    areaDensity (responseOf a f) = a f := by
  funext x
  simp [areaDensity, responseOf]

/-- ★ (⟸) UMA SOLUÇÃO nn COVARIANTE HABITA H3 v3.1 (com o H2, o T, a classe e o elo dados). -/
def H3_of_null_solution (C2 : ContratoH2 W R N) (T : StressTensorData W) (G : ℝ) (hG : 0 < G)
    (A : Set W.H) (hAu : ∀ ψ ∈ A, ‖ψ‖ = 1) (hAv : W.vac ∈ A)
    (hAt : ∀ (b : Fin 4 → ℝ) (ψ : W.H), ψ ∈ A → W.U b ψ ∈ A)
    (hmc : ∀ ψ ∈ A, ∀ k : ℝ, HasModularEnergy C2.Δit ψ k → k = 2 * Real.pi * nullPlaneCharge T ψ)
    (hAn : ∃ ψ ∈ A, ∃ k : ℝ, HasModularEnergy C2.Δit ψ k ∧ k ≠ 0)
    (hcont : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ, Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir)))
    (hflat : ∀ x ∈ rightWedge, screenBlock (solderMetric4 (C2.E x)⁻¹) = -1)
    (S : NullSolution W T G A) : ContratoH3 W R N T where
  H2 := C2
  G := G
  G_pos := hG
  admissible := A
  admissible_unit := hAu
  vac_admissible := hAv
  admissible_translate := hAt
  modular_charge := hmc
  admissible_nontrivial := hAn
  energy_continuous := hcont
  background_screen_flat := hflat
  propagator := responseOf S.a
  propagator_zero := by
    funext x
    ext i j
    fin_cases i <;> fin_cases j <;> simp [responseOf, S.a_zero]
  propagator_covariant := by
    intro b f
    funext x
    simp only [responseOf, S.a_cov]
  response_symm := by
    intro ψ hψ x
    exact Matrix.diagonal_transpose _
  lightcone_gauge := by
    intro ψ hψ x
    funext i
    fin_cases i <;> simp [responseOf, nullDir, Matrix.mulVec_diagonal]
  theta := S.θ
  theta_is_expansion := by
    intro ψ hψ x
    rw [areaDensity_responseOf]
    exact S.a_deriv ψ hψ x
  raychaudhuri_einstein := S.θ_deriv

/-- ★ (⟹) todo habitante de H3 v3.1 FORNECE uma solução nn covariante (a sua densidade de área e a sua θ). -/
def null_solution_of_H3 {T : StressTensorData W} (C : ContratoH3 W R N T) :
    NullSolution W T C.G C.admissible where
  a := fun f => areaDensity (C.propagator f)
  θ := C.theta
  a_zero := by
    intro x
    rw [C.propagator_zero]
    simp [areaDensity]
  a_cov := by
    intro b f x
    simp only [areaDensity, C.propagator_covariant]
  a_deriv := C.theta_is_expansion
  θ_deriv := C.raychaudhuri_einstein

/-- [DERIVED] ★★ A LEITURA: dados (H2, T, A, elo), H3 v3.1 é habitado SE E SÓ SE existe solução nn covariante. -/
theorem H3_iff_null_solution (C2 : ContratoH2 W R N) (T : StressTensorData W) (G : ℝ) (hG : 0 < G)
    (A : Set W.H) (hAu : ∀ ψ ∈ A, ‖ψ‖ = 1) (hAv : W.vac ∈ A)
    (hAt : ∀ (b : Fin 4 → ℝ) (ψ : W.H), ψ ∈ A → W.U b ψ ∈ A)
    (hmc : ∀ ψ ∈ A, ∀ k : ℝ, HasModularEnergy C2.Δit ψ k → k = 2 * Real.pi * nullPlaneCharge T ψ)
    (hAn : ∃ ψ ∈ A, ∃ k : ℝ, HasModularEnergy C2.Δit ψ k ∧ k ≠ 0)
    (hcont : ∀ ψ ∈ A, ∀ x : Fin 4 → ℝ, Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir)))
    (hflat : ∀ x ∈ rightWedge, screenBlock (solderMetric4 (C2.E x)⁻¹) = -1) :
    (∃ C : ContratoH3 W R N T, C.H2 = C2 ∧ C.G = G ∧ C.admissible = A) ↔ Nonempty (NullSolution W T G A) := by
  constructor
  · rintro ⟨C, _, hG', hA⟩
    subst hG' hA
    exact ⟨null_solution_of_H3 C⟩
  · rintro ⟨S⟩
    exact ⟨H3_of_null_solution C2 T G hG A hAu hAv hAt hmc hAn hcont hflat S, rfl, rfl, rfl⟩

#print axioms areaDensity_responseOf
#print axioms H3_of_null_solution
#print axioms null_solution_of_H3
#print axioms H3_iff_null_solution

end

end TGLExt.ContratoQGv31.ProbeResidual
