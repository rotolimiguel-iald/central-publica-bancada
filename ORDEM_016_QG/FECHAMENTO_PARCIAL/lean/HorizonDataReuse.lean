import Lean
import ContratoQG_v31_Minimal
import TGLExt.TriadMaster
import PolarMinimalPeriod_v2

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace TGLExt.ContratoQGv31
open TGL.SpecificAQFT TGL.ModularRealization
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace

theorem shift_point (x : Fin 4 → ℝ) (l μ : ℝ) :
    (x + l • nullDir) + (μ - l) • nullDir = x + μ • nullDir := by
  rw [add_assoc, ← add_smul]
  congr 2
  ring

namespace ContratoH3
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
  {N : KillingNormalization} {T : StressTensorData W}

theorem theta_along (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ)
    (l : ℝ) :
    HasDerivAt (fun μ => areaDensity (C.response ψ) (x + μ • nullDir))
      (C.theta ψ (x + l • nullDir)) l := by
  have h := C.theta_is_expansion ψ hψ (x + l • nullDir)
  have h' : HasDerivAt (fun ν : ℝ => areaDensity (C.response ψ) ((x + l • nullDir) + ν • nullDir))
      (C.theta ψ (x + l • nullDir)) (l - l) := by rw [sub_self]; exact h
  have h2 := h'.comp_sub_const l l
  have e : (fun μ : ℝ => areaDensity (C.response ψ) (x + μ • nullDir))
      = fun μ => areaDensity (C.response ψ) ((x + l • nullDir) + (μ - l) • nullDir) := by
    funext μ; rw [shift_point]
  rw [e]; exact h2

theorem theta_deriv_along (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (l : ℝ) :
    HasDerivAt (fun μ => C.theta ψ (x + μ • nullDir))
      (-(8 * Real.pi * C.G) * nullEnergy T ψ (x + l • nullDir)) l := by
  have h := C.raychaudhuri_einstein ψ hψ (x + l • nullDir)
  have h' : HasDerivAt (fun ν : ℝ => C.theta ψ ((x + l • nullDir) + ν • nullDir))
      (-(8 * Real.pi * C.G) * nullEnergy T ψ (x + l • nullDir)) (l - l) := by
    rw [sub_self]; exact h
  have h2 := h'.comp_sub_const l l
  have e : (fun μ : ℝ => C.theta ψ (x + μ • nullDir))
      = fun μ => C.theta ψ ((x + l • nullDir) + (μ - l) • nullDir) := by
    funext μ; rw [shift_point]
  rw [e]; exact h2

theorem first_law_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowArea (C.response ψ) x c d = 8 * Real.pi * C.G * windowCharge T ψ x c d := by
  have hcont : Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir)) :=
    C.energy_continuous ψ hψ x
  have hF : ∀ μ ∈ Set.uIcc c d,
      HasDerivAt (fun μ => (μ - c) * C.theta ψ (x + μ • nullDir)
          - areaDensity (C.response ψ) (x + μ • nullDir))
        (-(8 * Real.pi * C.G) * ((μ - c) * nullEnergy T ψ (x + μ • nullDir))) μ := by
    intro μ _
    have h1 := ((hasDerivAt_id μ).sub_const c).mul (theta_deriv_along C hψ x μ)
    have h2 := theta_along C hψ x μ
    refine (h1.sub h2).congr_deriv ?_
    simp only [id]
    ring
  have hint : IntervalIntegrable
      (fun μ => -(8 * Real.pi * C.G) * ((μ - c) * nullEnergy T ψ (x + μ • nullDir))) volume c d := by
    apply Continuous.intervalIntegrable
    exact continuous_const.mul ((continuous_id.sub continuous_const).mul hcont)
  have hI := intervalIntegral.integral_eq_sub_of_hasDerivAt hF hint
  rw [intervalIntegral.integral_const_mul] at hI
  unfold windowArea windowCharge
  rw [hθ] at hI
  simp only [sub_self, zero_mul, mul_zero, zero_sub] at hI
  linarith [hI]

theorem bekenstein_hawking_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowEntropy T ψ x c d = windowArea (C.response ψ) x c d / (4 * C.G) := by
  rw [first_law_window C hψ x c d hθ]
  unfold windowEntropy
  have hG := C.G_pos.ne'
  field_simp
  ring

theorem clausius_window (C : ContratoH3 W R N T) (ψ : W.H) (x : Fin 4 → ℝ) (c d : ℝ) :
    windowHeat C.H2.kappa T ψ x c d = C.H2.unruhTemperature * windowEntropy T ψ x c d := by
  unfold windowHeat windowEntropy ContratoH2.unruhTemperature
  field_simp

theorem einstein_coefficient_window (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible)
    (x : Fin 4 → ℝ) (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowHeat C.H2.kappa T ψ x c d
      = C.H2.kappa * windowArea (C.response ψ) x c d / (8 * Real.pi * C.G) := by
  rw [clausius_window, bekenstein_hawking_window C hψ x c d hθ]
  unfold ContratoH2.unruhTemperature
  exact einstein_coefficient_from_clausius _ _ _ C.G_pos.ne'

def toHorizonData (C : ContratoH3 W R N T) {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d : ℝ) (hθ : C.theta ψ (x + d • nullDir) = 0) : HorizonEquilibriumData where
  kappa := C.H2.kappa
  G := C.G
  G_pos := C.G_pos
  dA := windowArea (C.response ψ) x c d
  dS := windowEntropy T ψ x c d
  dQ := windowHeat C.H2.kappa T ψ x c d
  area_entropy := bekenstein_hawking_window C hψ x c d hθ
  clausius := by
    have := clausius_window C ψ x c d
    unfold ContratoH2.unruhTemperature at this
    exact this

theorem feeds_the_master (C : ContratoH3 W R N T)
    {L : Type} [Lattice L] [BoundedOrder L] {Tr : SubadditiveTraceData L}
    (S : SusyRelativeData L Tr) {x₀ : Fin 4 → ℝ} (hx₀ : x₀ ∈ rightWedge)
    {ψ : W.H} (hψ : ψ ∈ C.admissible) (x : Fin 4 → ℝ) (c d : ℝ)
    (hθ : C.theta ψ (x + d • nullDir) = 0) :
    (0 < Tr.tau S.ker ∧ Tr.tau S.ker < ⊤) ∧
      Tr.tau S.ker / Tr.tau S.ker = 1 ∧
      ((C.H2.E x₀)⁻¹ * C.H2.E x₀ = 1 ∧ LorentzByCongruence (solderMetric4 (C.H2.E x₀)⁻¹)) ∧
      (C.toHorizonData hψ x c d hθ).dQ = (C.toHorizonData hψ x c d hθ).kappa
        * (C.toHorizonData hψ x c d hθ).dA / (8 * Real.pi * (C.toHorizonData hψ x c d hθ).G) :=
  emergence_master_full_triad S (C.H2.E x₀) (C.H2.det_unit_on x₀ hx₀) (C.toHorizonData hψ x c d hθ)

/-- The exported data uses exactly this H3 contract's H2 horizon. -/
theorem data_fields_same_horizon (C : ContratoH3 W R N T)
    {psi : W.H} (hpsi : psi ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d : ℝ) (htheta : C.theta psi (x+d • nullDir)=0) :
    (C.toHorizonData hpsi x c d htheta).kappa=C.H2.kappa ∧
    (C.toHorizonData hpsi x c d htheta).G=C.G ∧
    (C.toHorizonData hpsi x c d htheta).dS=2*Real.pi*windowCharge T psi x c d :=
  ⟨rfl,rfl,rfl⟩

theorem data_temperature_from_same_period (C : ContratoH3 W R N T)
    {psi : W.H} (hpsi : psi ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d period : ℝ) (htheta : C.theta psi (x+d • nullDir)=0)
    (hp : 0 < period)
    (hperiod : ChatgptAudit.PolarPeriod016.AngularQuotientFaithful C.H2.kappa period) :
    (C.toHorizonData hpsi x c d htheta).kappa/(2*Real.pi)=1/period :=
  (ChatgptAudit.PolarPeriod016.reciprocal_temperature C.H2.kappa_pos hp hperiod).symm

#print axioms theta_along
#print axioms theta_deriv_along
#print axioms first_law_window
#print axioms bekenstein_hawking_window
#print axioms clausius_window
#print axioms einstein_coefficient_window
#print axioms toHorizonData
#print axioms feeds_the_master
#print axioms data_fields_same_horizon
#print axioms data_temperature_from_same_period
end ContratoH3
#print axioms shift_point
end TGLExt.ContratoQGv31


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
