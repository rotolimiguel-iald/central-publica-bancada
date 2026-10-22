import CanonicalFockGNSR5
import CanonicalFockFiniteStarCoreR1
import RegularScalarGNSRepresentationR2
import RegularScalarTomitaGraphR1
import TGLExt.V350DualOrbitStrongLimits

/-! Density of the original finite-star weight domain in the actual scalar
Fock GNS norm. This is stronger than strong operator density in the core. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightStarDensity
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockGNS
open F1Fecho.RegularScalarTomitaGraph
open scoped Topology

def leftRegularization (A : finiteLeftIdeal) (h : ℝ) : finiteLeftIdeal :=
  F1Fecho.RegularScalarGNSAction.scalarGNSLeftProduct weightContext
    ⟨star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h),
      core.toStarSubalgebra.star_mem' (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h)⟩ A

theorem leftRegularization_mem_starCore (A : finiteLeftIdeal) (h : ℝ) (hh : 0<h) :
    (leftRegularization A h).val ∈ finiteStarCore weightContext := by
  refine ⟨(leftRegularization A h).property,?_⟩
  change HasFiniteDualSquare (star (star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h)*A.val.val))
  rw [star_mul,star_star]
  exact HasFiniteDualSquare.left_mul _ _
    (F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow h hh)

theorem orbit_leftRegularization_tendsto (A : finiteLeftIdeal) :
    Tendsto (fun h : ℝ => scalarGNSOrbit (leftRegularization A h))
      (𝓝[>] 0) (𝓝 (scalarGNSOrbit A)) := by
  have hb : ∀ h : ℝ, ‖star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h)‖ ≤ 1 := by
    intro h
    exact (_root_.norm_star _).le.trans (F1Fecho.RegularCoreAverage.regularAverage_norm_le_one fockFlow h)
  have hs : ∀ v, Tendsto (fun h : ℝ => star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h) v)
      (𝓝[>] 0) (𝓝 ((1 : RegularHilbert F →L[ℂ] _) v)) := by
    intro v
    exact (F1Fecho.RegularFiniteStarCore.regularAverage_star_tendsto_identity fockFlow v).mono_left
      (nhdsWithin_mono _ (by intro h hh; exact ne_of_gt hh))
  have ht := dualOrbit_tendsto_of_uniformly_bounded
    (fun h : ℝ => star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h)) 1 1 hb hs (scalarGNSOrbit A)
  rw [map_one] at ht
  have he : (fun h : ℝ => scalarGNSOrbit (leftRegularization A h)) =
      (fun h : ℝ => dualOrbitRepresentation (star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h)) (scalarGNSOrbit A)) := by
    funext h
    exact (F1Fecho.RegularScalarGNSAction.scalarGNSAmbientAction_intertwines weightContext
      ⟨star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h),
        core.toStarSubalgebra.star_mem' (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h)⟩ A).symm
  rw [he]
  exact ht

theorem embedding_leftRegularization_tendsto (A : finiteLeftIdeal) :
    Tendsto (fun h : ℝ => GNSEmbedding (leftRegularization A h))
      (𝓝[>] 0) (𝓝 (GNSEmbedding A)) :=
  tendsto_subtype_rng.mpr (orbit_leftRegularization_tendsto A)

theorem starEmbedding_denseRange : DenseRange (scalarGNSStarEmbedding weightContext) := by
  have hs : Set.range GNSEmbedding ⊆ closure (Set.range (scalarGNSStarEmbedding weightContext)) := by
    rintro v ⟨A,rfl⟩
    apply isClosed_closure.mem_of_tendsto (embedding_leftRegularization_tendsto A)
    filter_upwards [self_mem_nhdsWithin] with h hh
    apply subset_closure
    exact ⟨⟨(leftRegularization A h).val,leftRegularization_mem_starCore A h hh⟩,rfl⟩
  intro v
  exact (closure_minimal hs isClosed_closure)
    ((F1Fecho.RegularScalarGNSRepresentation.GNSEmbedding_denseRange weightContext) v)

theorem scalarTomitaGraph_domain_dense : Dense (Prod.fst '' scalarTomitaGraph weightContext) := by
  apply starEmbedding_denseRange.mono
  rintro x ⟨A,rfl⟩
  exact ⟨(scalarGNSStarEmbedding weightContext A,scalarGNSStarEmbedding weightContext (star A)),⟨A,rfl⟩,rfl⟩

end F1Fecho.CanonicalFockWeightStarDensity
#print axioms F1Fecho.CanonicalFockWeightStarDensity.leftRegularization
#print axioms F1Fecho.CanonicalFockWeightStarDensity.leftRegularization_mem_starCore
#print axioms F1Fecho.CanonicalFockWeightStarDensity.orbit_leftRegularization_tendsto
#print axioms F1Fecho.CanonicalFockWeightStarDensity.embedding_leftRegularization_tendsto
#print axioms F1Fecho.CanonicalFockWeightStarDensity.starEmbedding_denseRange
#print axioms F1Fecho.CanonicalFockWeightStarDensity.scalarTomitaGraph_domain_dense
