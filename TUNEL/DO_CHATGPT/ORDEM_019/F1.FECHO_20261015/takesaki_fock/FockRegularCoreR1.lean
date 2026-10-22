import FieldWeylR2
import BosonicFockContinuity
import CanonicalOutput
import TGLExt.V350RegularDualAction

/-!
The regular representation on L2(R; canonical bosonic Fock), using the already
constructed second quantization of B0(-2 pi t). The fibre representation, real
translations, character multipliers and bicommutant-generation machinery are
reused from V350; no tower Hilbert space is substituted for Fock.

The generated algebra, faithful embedding and dual action are constructed for
every von Neumann algebra on Fock, then instantiated at FieldWeyl.R(KWR).
Ambient covariance is proved. Restriction to a wedge-flow automorphism is also
proved for a named LightNetData using its existing K_boost field; no inhabitant
of LightNetData is claimed here. A separate theorem identifying the concrete
KWR with that field, or proving its boost invariance directly, is not hidden.
No trace, modular identification, semifiniteness or full Takesaki duality is
asserted by this representation construction.
-/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section

namespace F1Fecho.FockRegular
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open TGLV350.Regular

def boostIso (t : ℝ) : F ≃ₗᵢ[ℂ] F := gamma (B0 (-(2*Real.pi*t)))
def boostCLM (t : ℝ) : F →L[ℂ] F := (boostIso t).toContinuousLinearMap

theorem boostIso_zero : boostIso 0 = .refl ℂ F := by
  simp only [boostIso,mul_zero,neg_zero,B0_zero,gamma_refl]

theorem boostIso_add (s t : ℝ) : boostIso (s+t) = (boostIso t).trans (boostIso s) := by
  unfold boostIso
  rw [show -(2*Real.pi*(s+t)) = -(2*Real.pi*s) + -(2*Real.pi*t) by ring,
    B0_add,gamma_trans]

theorem boostIso_neg (t : ℝ) : boostIso (-t) = (boostIso t).symm := by
  unfold boostIso
  rw [show -(2*Real.pi*(-t)) = -(-(2*Real.pi*t)) by ring,B0_neg,gamma_symm]

theorem boostCLM_zero : boostCLM 0 = 1 := by rw [boostCLM,boostIso_zero]; rfl

theorem boostCLM_mul (s t : ℝ) : boostCLM s * boostCLM t = boostCLM (s+t) := by
  ext v
  change boostIso s (boostIso t v) = boostIso (s+t) v
  rw [boostIso_add]
  rfl

theorem boostCLM_star (t : ℝ) : star (boostCLM t) = boostCLM (-t) := by
  rw [boostCLM,LinearIsometryEquiv.star_eq_symm,boostCLM,boostIso_neg]

theorem boostIso_strong (v : F) : Continuous (fun t : ℝ => boostIso t v) := by
  exact (boosts_strong v).comp (continuous_const.mul continuous_id |>.neg)

theorem boostAd_sandwich (t : ℝ) (A : F →L[ℂ] F) :
    F1Fecho.WeylFlow.boostAd t A = boostCLM t * A * star (boostCLM t) := by
  rw [boostCLM,LinearIsometryEquiv.star_eq_symm]
  rfl

def regularUnitary (t : ℝ) : RegularHilbert F →L[ℂ] RegularHilbert F :=
  fibre (boostCLM t) * shift t

theorem regular_zero : regularUnitary 0 = 1 := by
  simp only [regularUnitary,boostCLM_zero,fibre_one,shift_zero,mul_one]

theorem regular_mul (s t : ℝ) : regularUnitary s * regularUnitary t = regularUnitary (s+t) := by
  unfold regularUnitary
  calc
    (fibre (boostCLM s) * shift s) * (fibre (boostCLM t) * shift t)
      = fibre (boostCLM s) * (shift s * fibre (boostCLM t)) * shift t := by simp only [mul_assoc]
    _ = fibre (boostCLM s) * (fibre (boostCLM t) * shift s) * shift t := by rw [shift_commutes_fibre]
    _ = (fibre (boostCLM s) * fibre (boostCLM t)) * (shift s * shift t) := by simp only [mul_assoc]
    _ = fibre (boostCLM (s+t)) * shift (s+t) := by rw [← fibre_mul,boostCLM_mul,shift_mul]

theorem regular_star (t : ℝ) : star (regularUnitary t) = regularUnitary (-t) := by
  unfold regularUnitary
  rw [star_mul,shift_star,← fibre_star,boostCLM_star,shift_commutes_fibre]

theorem regular_unitary (t : ℝ) : star (regularUnitary t) * regularUnitary t = 1 ∧
    regularUnitary t * star (regularUnitary t) = 1 := by
  constructor
  · rw [regular_star,regular_mul,neg_add_cancel,regular_zero]
  · rw [regular_star,regular_mul,add_neg_cancel,regular_zero]

theorem regular_covariance (t : ℝ) (A : F →L[ℂ] F) :
    regularUnitary t * fibre A * star (regularUnitary t) =
      fibre (F1Fecho.WeylFlow.boostAd t A) := by
  rw [boostAd_sandwich,fibre_mul,fibre_mul,fibre_star]
  unfold regularUnitary
  calc
    _ = fibre (boostCLM t) * (shift t * fibre A * star (shift (H := F) t)) *
      star (fibre (boostCLM t)) := by simp only [star_mul,mul_assoc]
    _ = _ := by rw [shift_star,shift_fibre_sandwich]

theorem regular_strongly_continuous (f : RegularHilbert F) :
    Continuous (fun t : ℝ => regularUnitary t f) := by
  have h := fibre_jointly_continuous (H := F) (Z := ℝ)
    (fun t => (boostIso t).toLinearIsometry) boostIso_strong
  have hp : Continuous (fun t : ℝ => (shift (H := F) t f,t)) :=
    (shift_strongly_continuous f).prodMk continuous_id
  exact h.comp hp

def generators (M : VonNeumannAlgebra F) : Set (RegularHilbert F →L[ℂ] RegularHilbert F) :=
  (fibre '' (M : Set (F →L[ℂ] F))) ∪ Set.range regularUnitary

def core (M : VonNeumannAlgebra F) : VonNeumannAlgebra (RegularHilbert F) :=
  generatedAlgebra (generators M)

theorem fibre_mem (M : VonNeumannAlgebra F) (A : F →L[ℂ] F) (hA : A ∈ M) : fibre A ∈ core M :=
  generator_mem (Or.inl ⟨A,hA,rfl⟩)

theorem regular_mem (M : VonNeumannAlgebra F) (t : ℝ) : regularUnitary t ∈ core M :=
  generator_mem (Or.inr ⟨t,rfl⟩)

def amplification (M : VonNeumannAlgebra F) : M.toStarSubalgebra →⋆ₐ[ℂ]
    (RegularHilbert F →L[ℂ] RegularHilbert F) :=
  fibreRepresentation.comp M.toStarSubalgebra.subtype

def embedding (M : VonNeumannAlgebra F) : M.toStarSubalgebra →⋆ₐ[ℂ] (core M).toStarSubalgebra :=
  (amplification M).codRestrict (core M).toStarSubalgebra (fun A => fibre_mem M A A.property)

theorem embedding_injective (M : VonNeumannAlgebra F) : Function.Injective (embedding M) := by
  intro A B h
  apply Subtype.ext
  apply fibre_injective
  exact congrArg Subtype.val h

theorem core_minimal (M : VonNeumannAlgebra F) (N : VonNeumannAlgebra (RegularHilbert F))
    (hM : ∀ A ∈ M, fibre A ∈ N) (hU : ∀ t : ℝ, regularUnitary t ∈ N) : core M ≤ N := by
  apply generated_minimal
  intro A hA
  rcases hA with ⟨B,hB,rfl⟩ | ⟨t,rfl⟩
  · exact hM B hB
  · exact hU t

theorem dual_on_regular (s t : ℝ) :
    dualAmbient s (regularUnitary t) = characterPhase s t • regularUnitary t := by
  rw [dualAmbient_apply]
  unfold regularUnitary
  calc
    _ = fibre (boostCLM t) * (characterMultiplier s * shift t *
      star (characterMultiplier (H := F) s)) := by
      rw [← mul_assoc (characterMultiplier s),characterMultiplier_commutes_fibre]
      simp only [mul_assoc]
    _ = _ := by rw [characterMultiplier_weyl,mul_smul_comm]; rfl

theorem dual_preserves_generators (M : VonNeumannAlgebra F) (s : ℝ) :
    ∀ A ∈ generators M, dualAmbient s A ∈ core M := by
  intro A hA
  rcases hA with ⟨B,hB,rfl⟩ | ⟨t,rfl⟩
  · rw [dualAmbient_fibre]
    exact fibre_mem M B hB
  · rw [dual_on_regular]
    exact (core M).toStarSubalgebra.smul_mem (regular_mem M t) _

def dualAction (M : VonNeumannAlgebra F) (s : ℝ) :
    (core M).toStarSubalgebra ≃⋆ₐ[ℂ] (core M).toStarSubalgebra :=
  generatedAutomorphism (dualAmbient s) (generators M) (dual_preserves_generators M s) (by
    rw [dualAmbient_symm]
    exact dual_preserves_generators M (-s))

theorem dualAction_zero (M : VonNeumannAlgebra F) : dualAction M 0 = StarAlgEquiv.refl := by
  apply StarAlgEquiv.ext
  intro A
  apply Subtype.ext
  change dualAmbient (H := F) 0 (A : RegularHilbert F →L[ℂ] RegularHilbert F) = A
  rw [dualAmbient_zero]
  rfl

theorem dualAction_add (M : VonNeumannAlgebra F) (s t : ℝ) :
    dualAction M (s+t) = (dualAction M s).trans (dualAction M t) := by
  apply StarAlgEquiv.ext
  intro A
  apply Subtype.ext
  change dualAmbient (H := F) (s+t) (A : RegularHilbert F →L[ℂ] RegularHilbert F) =
    dualAmbient t (dualAmbient s A)
  rw [dualAmbient_add]
  rfl

theorem dual_fixes_embedding (M : VonNeumannAlgebra F) (s : ℝ) (A : M.toStarSubalgebra) :
    dualAction M s (embedding M A) = embedding M A := by
  apply Subtype.ext
  exact dualAmbient_fibre s A

theorem dual_strongly_continuous (M : VonNeumannAlgebra F)
    (A : (core M).toStarSubalgebra) (f : RegularHilbert F) :
    Continuous (fun s : ℝ => (dualAction M s A).val f) :=
  dualAmbient_strongly_continuous A f

def canonicalWedge : VonNeumannAlgebra F :=
  F1Fecho.FieldWeyl.R F1Rede.CanonicalWedge.KWR.toClosedSubmodule.toSubmodule

def canonicalCore : VonNeumannAlgebra (RegularHilbert F) := core canonicalWedge

def canonicalEmbedding : canonicalWedge.toStarSubalgebra →⋆ₐ[ℂ] canonicalCore.toStarSubalgebra :=
  embedding canonicalWedge

theorem canonicalEmbedding_injective : Function.Injective canonicalEmbedding :=
  embedding_injective canonicalWedge

theorem covariance_on_named_light_net (L : TGLExt.QGSolution.LightNetData) (t : ℝ)
    (A : (F1Fecho.FieldWeyl.R (L.K TGL.SpecificAQFT.rightWedge)).toStarSubalgebra) :
    regularUnitary t * fibre (A : F →L[ℂ] F) * star (regularUnitary t) =
      fibre ((F1Fecho.FieldWeyl.wedgeFlow L t A) : F →L[ℂ] F) := regular_covariance t A

end F1Fecho.FockRegular

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.FockRegular).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
