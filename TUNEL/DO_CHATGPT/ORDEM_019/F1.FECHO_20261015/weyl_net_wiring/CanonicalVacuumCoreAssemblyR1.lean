import CanonicalWeylAssemblyR5
import CanonicalFockRegularCoreR2
import WedgeNonabelianR4
import CanonicalGammaPositiveR3
import CanonicalGammaNoFixedR4

/-! Concrete core wiring on the same Fock. Core, its algebraic instances,
faithful embedding and dual action with their laws are supplied by constructed
terms. The trace and its laws, finite projection and split remain explicit
inputs on THAT core. The vacuum modular identification and other analytic
inputs remain; no inhabitant of the whole remaining input is asserted.
Noncommutativity of the concrete standard-wedge algebra is derived and is no
longer an input. Positive energy is also supplied by the concrete orbital
contraction and its bounded second quantization, not an extra premise. Only the vacuum can be fixed for the general unitary family under the existing no-projective-eigenvector hypothesis; this is now supplied by a theorem on the same Fock. The global-net glue, modular/KMS and trace obligations remain.
The separately constructed dual weight is not substituted for the trace.
-/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.NetworkVacuumCore
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ImportedSQ
open F1Rede.BosonicFock F1Fecho.NetworkReuse F1Fecho.Antilinear
open TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open F1Fecho.NetworkWeyl

abbrev RepresentedCore := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra

theorem wedge_le_canonical (D : CanonicalNetInput) :
    (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra ≤
    F1Fecho.CanonicalFockRegular.M.toStarSubalgebra := by
  rw [D.wedge_glue]
  exact le_rfl

def coreEmbedding (D : CanonicalNetInput) :
    (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra →⋆ₐ[ℂ] RepresentedCore :=
  F1Fecho.CanonicalFockRegular.embedding.comp
    (StarSubalgebra.inclusion (wedge_le_canonical D))

theorem coreEmbedding_injective (D : CanonicalNetInput) :
    Function.Injective (coreEmbedding D) :=
  F1Fecho.CanonicalFockRegular.embedding_injective.comp
    (StarSubalgebra.inclusion_injective (wedge_le_canonical D))

theorem dual_fixes_coreEmbedding (D : CanonicalNetInput) (s : ℝ)
    (A : (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra) :
    F1Fecho.CanonicalFockRegular.dualAction s (coreEmbedding D A) = coreEmbedding D A :=
  F1Fecho.CanonicalFockRegular.dual_fixes_embedding s
    (StarSubalgebra.inclusion (wedge_le_canonical D) A)

structure RemainingVacuumCoreInput (D : CanonicalNetInput) where
  /-- ★ BISOGNANO–WICHMANN da luz: o boost segundo-quantizado em 2πt satisfaz KMS a β = 1 na cunha
      [Bisognano–Wichmann 1975/76; BGL 2002 + Araki 1963]. -/
  bw_kms : KMSBody (FieldWeyl.R (D.K rightWedge)) F1Rede.BosonicFock.vacuum (fun t => F1Rede.BosonicFock.gamma (B0 (2 * Real.pi * t))) 1
  /-- a realização analítica de Tomita do par [Tomita–Takesaki]. -/
  tomita : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra F1Rede.BosonicFock.vacuum canonicalFockJ (fun t => F1Rede.BosonicFock.gamma (B0 (-(2 * Real.pi * t))))
  trace : RepresentedCore → ENNReal
  trace_zero : trace 0 = 0
  trace_tracial : ∀ x y : RepresentedCore, trace (x * y) = trace (y * x)
  trace_star : ∀ x : RepresentedCore, trace (star x) = trace x
  trace_dual_scaling : ∀ (s : ℝ) (x : RepresentedCore),
    trace ((F1Fecho.CanonicalFockRegular.dualAction s) x) = ENNReal.ofReal (Real.exp (-s)) * trace x
  /-- uma projeção finita não nula do núcleo II_∞, partida em duas metades de traço igual [Connes 1973]. -/
  PF : RepresentedCore
  PF_sa : star PF = PF
  PF_idem : PF * PF = PF
  PF_ne : PF ≠ 0
  PF_pos : 0 < trace PF
  PF_fin : trace PF < ⊤
  Pp : RepresentedCore
  Pm : RepresentedCore
  Pp_sa : star Pp = Pp
  Pp_idem : Pp * Pp = Pp
  Pm_sa : star Pm = Pm
  Pm_idem : Pm * Pm = Pm
  split : Pp + Pm = PF
  orth : Pp * Pm = 0
  trace_additive : trace PF = trace Pp + trace Pm
  equal_halves : trace Pp = trace Pm


def RemainingVacuumCoreInput.toRemainingWeyl {D : CanonicalNetInput}
    (A : RemainingVacuumCoreInput D) : RemainingWeylInput D where
  Core := RepresentedCore
  instCR := inferInstance
  instCS := inferInstance
  instCA := inferInstance
  embedding := coreEmbedding D
  embedding_injective := coreEmbedding_injective D
  dualAction := F1Fecho.CanonicalFockRegular.dualAction
  dualAction_zero := F1Fecho.CanonicalFockRegular.dualAction_zero
  dualAction_add := F1Fecho.CanonicalFockRegular.dualAction_add
  Γ_positive := F1Fecho.CanonicalGammaPositive.gamma_positive
  Γ_no_fixed := F1Fecho.CanonicalGammaNoFixed.gamma_no_fixed
  wedge_nonabelian := by
    rw [D.wedge_glue]
    exact F1Fecho.WedgeNonabelian.wedge_nonabelian
  bw_kms := A.bw_kms
  tomita := A.tomita
  trace := A.trace
  trace_zero := A.trace_zero
  trace_tracial := A.trace_tracial
  trace_star := A.trace_star
  trace_dual_scaling := A.trace_dual_scaling
  PF := A.PF
  PF_sa := A.PF_sa
  PF_idem := A.PF_idem
  PF_ne := A.PF_ne
  PF_pos := A.PF_pos
  PF_fin := A.PF_fin
  Pp := A.Pp
  Pm := A.Pm
  Pp_sa := A.Pp_sa
  Pp_idem := A.Pp_idem
  Pm_sa := A.Pm_sa
  Pm_idem := A.Pm_idem
  split := A.split
  orth := A.orth
  trace_additive := A.trace_additive
  equal_halves := A.equal_halves

def RemainingVacuumCoreInput.toCertificate {D : CanonicalNetInput}
    (A : RemainingVacuumCoreInput D) : FockCertificate D.toLightNetData.toLightOneParticle :=
  A.toRemainingWeyl.toCertificate

theorem assembled_core_is_concrete {D : CanonicalNetInput} (A : RemainingVacuumCoreInput D) :
    A.toCertificate.Core = RepresentedCore := rfl

theorem assembled_embedding_is_concrete {D : CanonicalNetInput} (A : RemainingVacuumCoreInput D) :
    A.toCertificate.embedding = coreEmbedding D := rfl

theorem assembled_dual_is_concrete {D : CanonicalNetInput} (A : RemainingVacuumCoreInput D) :
    A.toCertificate.dualAction = F1Fecho.CanonicalFockRegular.dualAction := rfl

end F1Fecho.NetworkVacuumCore
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.NetworkVacuumCore).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
