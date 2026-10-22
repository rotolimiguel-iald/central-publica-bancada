import GenericStarConjugationR3
import CanonicalFockConjugationActionR3
import CanonicalFockFullWeightTomitaR5
import RegularScalarRealGraphR2
/-! Regular conjugation preserves the FULL actual GNS adjunction graph.
The star action and finite domain are paid by actual left/right products;
modular identification is not assumed from this covariance. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockGNSCovariance
open TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockConjugation
open F1Fecho.CanonicalFockFullWeightStarCore F1Fecho.CanonicalFockFullWeightTomita
open F1Fecho.RegularScalarRealGraph F1Fecho.CanonicalFockWeightSandwich

 def conjugateLeft (t:ℝ) (A:scalarWeightStarCore) : scalarWeightLeftIdeal :=
  scalarWeightLeftProduct (regularRightCoreElement t)
    (scalarRegularRightProduct (-t) ⟨A.val,A.property.1⟩)

 theorem conjugateLeft_star (t:ℝ) (A:scalarWeightStarCore) :
    star (conjugateLeft t A).val=(conjugateLeft t (star A)).val := by
  apply Subtype.ext
  change star (regularUnitary t*(A.val.val*regularUnitary (-t)))=
    regularUnitary t*(star A.val.val*regularUnitary (-t))
  exact GenericStarConjugation.regular_conjugation_star fockFlow t A.val.val

 def conjugateStar (t:ℝ) (A:scalarWeightStarCore) : scalarWeightStarCore :=
  GenericStarConjugation.starCoreOfLeft weightContext (conjugateLeft t A)
    (conjugateLeft t (star A)) (conjugateLeft_star t A)


 theorem conjugateStar_star (t:ℝ) (A:scalarWeightStarCore) :
    star (conjugateStar t A)=conjugateStar t (star A) :=
  Subtype.ext (conjugateLeft_star t A)

 theorem conjugate_embedding (t:ℝ) (A:scalarWeightStarCore) :
    regularConjugationGNS t (scalarWeightStarEmbedding A)=
      scalarWeightStarEmbedding (conjugateStar t A) :=
  regularConjugationGNS_intertwines t ⟨A.val,A.property.1⟩

 def conjugatePair (t:ℝ) : (GNSHilbert×GNSHilbert)→L[ℂ](GNSHilbert×GNSHilbert) :=
  (regularConjugationGNS t).prodMap (regularConjugationGNS t)

 theorem conjugate_raw_graph (t:ℝ) (p:GNSHilbert×GNSHilbert)
    (hp:p∈scalarWeightTomitaGraph) : conjugatePair t p∈scalarWeightTomitaGraph := by
  obtain ⟨A,rfl⟩:=hp
  refine ⟨conjugateStar t A,?_⟩
  apply Prod.ext
  · exact (conjugate_embedding t A).symm
  · exact (congrArg scalarWeightStarEmbedding (conjugateStar_star t A)).trans
      (conjugate_embedding t (star A)).symm

 theorem conjugate_closed_graph (t:ℝ) (p:GNSHilbert×GNSHilbert)
    (hp:p∈closedGraph weightContext) : conjugatePair t p∈closedGraph weightContext := by
  have hmap : ∀p∈closure scalarWeightTomitaGraph,
      conjugatePair t p∈closure scalarWeightTomitaGraph :=
    closure_minimal (fun p hp=>subset_closure (conjugate_raw_graph t p hp))
      (isClosed_closure.preimage (conjugatePair t).continuous)
  change conjugatePair t p∈closure (RegularScalarTomitaGraph.scalarTomitaGraph weightContext)
  change p∈closure (RegularScalarTomitaGraph.scalarTomitaGraph weightContext) at hp
  exact Eq.mp (congrArg (fun s=>conjugatePair t p∈s) scalarWeightTomitaGraph_closure_eq)
    (hmap p (Eq.mpr (congrArg (fun s=>p∈s) scalarWeightTomitaGraph_closure_eq) hp))
end F1Fecho.CanonicalFockGNSCovariance
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugateLeft_star
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugateStar_star
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_embedding
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_raw_graph
#print axioms F1Fecho.CanonicalFockGNSCovariance.conjugate_closed_graph
