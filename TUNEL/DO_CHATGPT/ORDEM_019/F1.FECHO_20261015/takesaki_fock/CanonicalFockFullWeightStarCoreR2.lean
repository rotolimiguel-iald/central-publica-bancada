import CanonicalFockWeightCompletionR5
import CanonicalFockWeightClosedTomitaR2
/-! Full finite-weight star algebra on the same Fock core. This file only
constructs its raw adjunction graph and includes the original uniform core;
equality of graph closures requires the separate sandwich approximation. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockFullWeightStarCore
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightCompletion
open scoped Topology ENNReal
/-- The algebraic full scalar-weight star core, n_ν ∩ n_ν*. -/
def scalarWeightStarCore  :
    NonUnitalStarSubalgebra ℂ core.toStarSubalgebra where
  carrier := {A | HasFiniteScalarSquare A.val ∧ HasFiniteScalarSquare (star A.val)}
  zero_mem' := by
    exact ⟨HasFiniteScalarSquare.zero, by simpa only [star_zero] using HasFiniteScalarSquare.zero⟩
  add_mem' := by
    intro A B hA hB
    change HasFiniteScalarSquare (A.val+B.val) ∧
      HasFiniteScalarSquare (star (A.val+B.val))
    exact ⟨HasFiniteScalarSquare.add _ _ hA.1 hB.1,
      by simpa only [star_add] using HasFiniteScalarSquare.add _ _ hA.2 hB.2⟩
  mul_mem' := by
    intro A B hA hB
    change HasFiniteScalarSquare (A.val*B.val) ∧
      HasFiniteScalarSquare (star (A.val*B.val))
    exact ⟨HasFiniteScalarSquare.left_mul _ _ hB.1,
      by simpa only [star_mul] using
        HasFiniteScalarSquare.left_mul (star B.val) (star A.val) hA.2⟩
  smul_mem' := by
    intro c A hA
    change HasFiniteScalarSquare (c • A.val) ∧
      HasFiniteScalarSquare (star (c • A.val))
    exact ⟨HasFiniteScalarSquare.smul c _ hA.1,
      by simpa only [star_smul] using HasFiniteScalarSquare.smul (star c) _ hA.2⟩
  star_mem' := by
    intro A hA
    change HasFiniteScalarSquare (star A.val) ∧ HasFiniteScalarSquare (star (star A.val))
    exact ⟨hA.2,by simpa only [star_star] using hA.1⟩

def scalarWeightStarEmbedding  (A : scalarWeightStarCore) : GNSHilbert :=
  scalarWeightGNSEmbedding ⟨A.val,A.property.1⟩

def scalarUniformToWeightStar  (A : F1Fecho.RegularScalarTomitaGraph.finiteStarCore weightContext) : scalarWeightStarCore :=
  ⟨A.val,finiteSquare_scalar_finite _ A.property.1,
    finiteSquare_scalar_finite _ A.property.2⟩

theorem scalarUniformToWeightStar_star  (A : F1Fecho.RegularScalarTomitaGraph.finiteStarCore weightContext) :
    scalarUniformToWeightStar (star A) = star (scalarUniformToWeightStar A) := rfl

theorem scalarWeightStarEmbedding_uniform  (A : F1Fecho.RegularScalarTomitaGraph.finiteStarCore weightContext) :
    scalarWeightStarEmbedding (scalarUniformToWeightStar A) = F1Fecho.RegularScalarTomitaGraph.scalarGNSStarEmbedding weightContext A :=
  scalarWeightGNSEmbedding_uniform ⟨A.val,A.property.1⟩

def scalarWeightTomitaGraph  : Set (GNSHilbert × GNSHilbert) :=
  Set.range fun A : scalarWeightStarCore =>
    (scalarWeightStarEmbedding A,scalarWeightStarEmbedding (star A))

theorem scalarTomitaGraph_subset_weight  :
    F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph weightContext ⊆ scalarWeightTomitaGraph := by
  rintro _ ⟨A,rfl⟩
  refine ⟨scalarUniformToWeightStar A,?_⟩
  simp only [← scalarUniformToWeightStar_star,scalarWeightStarEmbedding_uniform]

#print axioms scalarWeightStarCore
#print axioms scalarWeightStarEmbedding
#print axioms scalarUniformToWeightStar
#print axioms scalarUniformToWeightStar_star
#print axioms scalarWeightStarEmbedding_uniform
#print axioms scalarWeightTomitaGraph
#print axioms scalarTomitaGraph_subset_weight
end F1Fecho.CanonicalFockFullWeightStarCore
