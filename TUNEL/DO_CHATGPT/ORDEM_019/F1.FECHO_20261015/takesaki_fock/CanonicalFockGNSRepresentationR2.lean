import CanonicalFockGNSActionR2
import TGLExt.V350DualOrbitRepresentation
import TGLExt.V350ReducingStarRepresentation
/-! A faithful star representation of the actual Fock core on its constructed
scalar-weight GNS completion, proved using the actual finite-square averages. -/
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.CanonicalFockGNSRepresentation
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockGNSAction
open scoped Topology
def scalarGNSRepresentation  :
    (core).toStarSubalgebra →⋆ₐ[ℂ]
      (GNSHilbert →L[ℂ] GNSHilbert) :=
  reducingStarRepresentation
    (dualOrbitRepresentation.comp (core).toStarSubalgebra.subtype)
    (GNSSubspace) (scalarGNSAmbientAction_preserves)

theorem scalarGNSEmbedding_denseRange  :
    DenseRange (GNSEmbedding) := by
  let f := scalarGNSLinear
  have h : DenseRange (Set.inclusion (s := Set.range f) subset_closure) :=
    (denseRange_inclusion_iff subset_closure).2 subset_rfl
  exact h.comp Set.rangeFactorization_surjective.denseRange (continuous_inclusion subset_closure)

theorem scalarGNSRepresentation_zero_iff 
    (B : (core).toStarSubalgebra) :
    scalarGNSRepresentation B = 0 ↔ B = 0 := by
  constructor
  · intro hB
    have hann : ∀ A : finiteLeftIdeal, B.val * A.val.val = 0 := by
      intro A
      have he : GNSEmbedding (scalarGNSLeftProduct B A) = GNSEmbedding 0 :=
        calc
          _ = scalarGNSRepresentation B (GNSEmbedding A) :=
            (scalarGNSAction_intertwines B A).symm
          _ = 0 := congrArg (fun T : GNSHilbert →L[ℂ] GNSHilbert =>
            T (GNSEmbedding A)) hB
          _ = _ := (GNSEmbedding).map_zero.symm
      have hz := GNSEmbedding_injective he
      exact congrArg (fun A : finiteLeftIdeal => A.val.val) hz
    apply Subtype.ext
    ext1 v
    change B.val v = 0
    have hlim := (finite_square_strong_density B).2.2 v
    have he : (fun h : ℝ => (B.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) v) =ᶠ[𝓝[>] 0] (fun _ => 0) := by
      filter_upwards [self_mem_nhdsWithin] with h hh
      have hz := hann ⟨⟨F1Fecho.RegularCoreAverage.regularAverage fockFlow h,F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h⟩,
        F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow h hh⟩
      exact congrArg (fun T : RegularHilbert F →L[ℂ] _ => T v) hz
    have hzlim : Tendsto (fun h : ℝ => (B.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) v) (𝓝[>] 0) (𝓝 0) :=
      tendsto_const_nhds.congr' he.symm
    exact _root_.tendsto_nhds_unique (f := fun h : ℝ => (B.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) v)
      (l := 𝓝[>] (0 : ℝ)) hlim hzlim
  · rintro rfl
    exact map_zero (scalarGNSRepresentation)

theorem scalarGNSRepresentation_injective  :
    Function.Injective (scalarGNSRepresentation) := by
  intro B C h
  apply sub_eq_zero.mp
  apply (scalarGNSRepresentation_zero_iff (B-C)).mp
  rw [map_sub,h,sub_self]


end F1Fecho.CanonicalFockGNSRepresentation
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockGNSRepresentation).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
