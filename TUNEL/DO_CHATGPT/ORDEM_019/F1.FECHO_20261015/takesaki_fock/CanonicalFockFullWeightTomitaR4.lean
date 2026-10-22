import CanonicalFockWeightSandwichR5
import CanonicalFockFullWeightStarCoreR3
/-! The original closed adjunction operator equals the graph closure from the
FULL finite-weight star algebra n_nu intersect n_nu^*. This is the missing
domain identification; it does not identify its modular flow with Ad(lambda). -/
set_option autoImplicit false
set_option maxErrors 2
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockFullWeightTomita
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightCompletion F1Fecho.CanonicalFockWeightSandwich
open F1Fecho.CanonicalFockFullWeightStarCore F1Fecho.CanonicalFockWeightClosedTomita
open scoped Topology ENNReal
theorem scalarWeightGNSEmbedding_sandwich_uniform 
    (A : scalarWeightLeftIdeal) (h : ℝ) (hh : 0 < h) :
    scalarWeightGNSEmbedding (scalarWeightSandwich A h) =
      F1Fecho.RegularScalarTomitaGraph.scalarGNSStarEmbedding weightContext ⟨F1Fecho.RegularFiniteStarCore.regularSandwich fockFlow M A.val h,
        F1Fecho.CanonicalFockFiniteStarCore.finiteSandwich_mem A.val h hh⟩ := by
  change _ = GNSEmbedding ⟨F1Fecho.RegularFiniteStarCore.regularSandwich fockFlow M A.val h,
    (F1Fecho.CanonicalFockFiniteStarCore.finiteSandwich_mem A.val h hh).1⟩
  rw [← scalarWeightGNSEmbedding_uniform]
  apply congrArg (scalarWeightGNSEmbedding)
  exact Subtype.ext (scalarWeightSandwich_val A h)

/-- Both coordinates of the full-weight star graph are approximated by the
same uniform-star-core sandwich, in the GNS product topology. -/
theorem scalarWeightTomitaGraph_subset_closure_original  :
    scalarWeightTomitaGraph ⊆ closure (F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph weightContext) := by
  rintro _ ⟨A,rfl⟩
  let a : scalarWeightLeftIdeal := ⟨A.val,A.property.1⟩
  let astar : scalarWeightLeftIdeal := ⟨(star A).val,(star A).property.1⟩
  have ht : Tendsto (fun h : ℝ =>
      (scalarWeightGNSEmbedding (scalarWeightSandwich a h),
        scalarWeightGNSEmbedding (scalarWeightSandwich astar h)))
      (𝓝[>] (0 : ℝ))
      (𝓝 (scalarWeightStarEmbedding A,scalarWeightStarEmbedding (star A))) :=
    ((scalarWeightGNSEmbedding_sandwich_tendsto a).prodMk_nhds
      (scalarWeightGNSEmbedding_sandwich_tendsto astar)).mono_left
        (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  apply isClosed_closure.mem_of_tendsto ht
  filter_upwards [self_mem_nhdsWithin] with h hh
  let b : F1Fecho.RegularScalarTomitaGraph.finiteStarCore weightContext := ⟨F1Fecho.RegularFiniteStarCore.regularSandwich fockFlow M A.val h,
    F1Fecho.CanonicalFockFiniteStarCore.finiteSandwich_mem A.val h hh⟩
  apply subset_closure
  refine ⟨b,?_⟩
  apply Prod.ext
  · exact (scalarWeightGNSEmbedding_sandwich_uniform a h hh).symm
  · rw [scalarWeightGNSEmbedding_sandwich_uniform astar h hh]
    apply congrArg (F1Fecho.RegularScalarTomitaGraph.scalarGNSStarEmbedding weightContext)
    exact Subtype.ext (F1Fecho.RegularFiniteStarCore.regularSandwich_star fockFlow M A.val h)

theorem scalarWeightTomitaGraph_closure_eq  :
    closure (scalarWeightTomitaGraph) = closure (F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph weightContext) :=
  Set.Subset.antisymm
    (closure_minimal (scalarWeightTomitaGraph_subset_closure_original) isClosed_closure)
    (closure_mono (scalarTomitaGraph_subset_weight))

/-- The existing closed S is exactly the closure of the full-weight star
graph. This does not assert equality with the raw algebraic graph. -/
theorem graph_eq_weight  :
    Set.range (fun x : closedTomitaDomain =>
      ((x : GNSHilbert),closedTomita x)) =
        closure (scalarWeightTomitaGraph) := by
  rw [scalarWeightTomitaGraph_closure_eq]
  exact graph_eq

theorem scalarWeightStar_mem_closedTomitaDomain 
    (A : scalarWeightStarCore) :
    scalarWeightStarEmbedding A ∈ closedTomitaDomain :=
  ⟨scalarWeightStarEmbedding (star A),
    scalarWeightTomitaGraph_subset_closure_original ⟨A,rfl⟩⟩

theorem scalarClosedTomita_extends_weight_star 
    (A : scalarWeightStarCore) :
    closedTomita ⟨scalarWeightStarEmbedding A,
      scalarWeightStar_mem_closedTomitaDomain A⟩ = scalarWeightStarEmbedding (star A) :=
  F1Fecho.RegularScalarTomitaClosure.scalarTomitaGraph_closure_single_valued (H := F) weightContext (scalarWeightStarEmbedding A) _ _
    (F1Fecho.RegularScalarClosedTomita.scalarClosedTomita_graph (H := F) (D := weightContext) ⟨scalarWeightStarEmbedding A,
      scalarWeightStar_mem_closedTomitaDomain A⟩)
    (scalarWeightTomitaGraph_subset_closure_original ⟨A,rfl⟩)

#print axioms scalarWeightGNSEmbedding_sandwich_uniform
#print axioms scalarWeightTomitaGraph_subset_closure_original
#print axioms scalarWeightTomitaGraph_closure_eq
#print axioms graph_eq_weight
#print axioms scalarWeightStar_mem_closedTomitaDomain
#print axioms scalarClosedTomita_extends_weight_star
end F1Fecho.CanonicalFockFullWeightTomita
