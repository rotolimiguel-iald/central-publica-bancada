import TGLExt.Fundacao
import TGLExt.GeneralMetricClausius
import TGLExt.GravitationalChartGluing
import TGLExt.TopologicalAtlasGluing
import TGLExt.SmoothSelectedAtlasGluing
import TGLExt.HorizonEinsteinReconstruction
import TGLExt.TheImportedSecondQuantization

/-!
F2.3, branch C of the anti-wall tree. This remains a conditional interface.
The Lorentz wedge orbit, source identification, curved conservation and
H3 at every point and null direction are named inputs. No global metric
or solution is constructed. The finite passage identity is already provable
under its premises, so the bridge hypothesis carries H3 in full.

c1 audit probes, recorded beside this pinned branch:
* S-A: this exact theorem is a corollary of the audited F2.3 stone. The
  proof rewrites the source by source_matches_maxwell and uses only
  horizon_touch from the supplied wedge. It adds no new implication.
* S-B: 'wedge at x' has no geometric anchor in this type. The region may
  be the whole space and the boost acts around the origin; the same wedge
  can be presented at any other x. The later phrase 'at one chart point'
  names a binder and does not construct a physical Lorentz wedge family.
* S-C: horizon_touch is trivial for the whole-space region.

Non-vacuity has not been exhibited: neither FockCertificate nor
MaxwellCertificate has a kernel inhabitant for this branch. The flat
Minkowski vacuum witness S7 for the audited stone does not transfer here.
The all-direction wedge family also has no exhibited inhabitant.
-/

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.F23CurvedFieldBranchC

open Matrix Filter Topology Set TGLExt ChatgptAudit
open ChatgptAudit.GeneralMetric ChatgptAudit.GeneralClausius
open ChatgptAudit.GravitationalRecord ChatgptAudit.ChartGluing
open ChatgptAudit.TopologicalGluing ChatgptAudit.SmoothAtlasGluing
open ChatgptAudit.UnifiedRecorded ChatgptAudit.Micro021
open TGLExt.ImportedSQ

noncomputable section

/-- A Lorentz wedge of the light net at one chart point and null direction.
    Every field is input. A pointwise metric isometry alone would not supply
    covariance of the light net; the latter is stated separately. -/
structure LightLorentzWedgeAt
    (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (g : Matrix (Fin 4) (Fin 4) ℝ) (x d : Coordinate4) where
  region : Set Coordinate4
  horizon_touch : x ∈ closure region
  boost : ℝ → Matrix (Fin 4) (Fin 4) ℝ
  boost_zero : boost 0 = 1
  boost_add : ∀ s t, boost (s + t) = boost s * boost t
  metric_lorentz : ∀ s, (boost s)ᵀ * g * boost s = g
  null_expand : ∀ s, (boost s).mulVec d = Real.exp s • d
  region_preserved : ∀ s y, y ∈ region → (boost s).mulVec y ∈ region
  state_boost : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)
  state_boost_zero : state_boost 0 = LinearIsometryEquiv.refl ℂ W.H
  state_boost_add : ∀ s t, state_boost (s + t) =
    (state_boost t).trans (state_boost s)
  net_covariant : ∀ s O A, A ∈ W.net O →
    (state_boost s).conjStarAlgEquiv A ∈
      W.net ((fun y => (boost s).mulVec y) '' O)

/-- An all-point, all-null-direction family is a named input, not an object
    supplied by the one-wedge light contract. This pointwise family does not
    include coherence between directions or a global Poincare representation. -/
structure LightLorentzWedgeFamilyEveryNullDirection
    {L : LightOneParticle} (C : FockCertificate L)
    {ι : Type} (U : ι → Set Coordinate4)
    (R : ∀ i, GravitationalResponseRecord (U i)) where
  wedge_for : ∀ i x (_hx : x ∈ U i) d (_hv : d ≠ 0)
      (_hn : tensorQuad (recordMetric (R i) x) d = 0),
    LightLorentzWedgeAt (lightNet C) (recordMetric (R i) x) x d

/-- H3 of the curved record, with the 48-outcome microscopic area error,
    at every chart point and every nonzero null direction. -/
def NamedAtlasH3 {ι : Type} (eta : ℝ) (U : ι → Set Coordinate4)
    (R : ∀ i, GravitationalResponseRecord (U i))
    (screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i))) : Prop :=
  ∀ i x (hx : x ∈ U i) d (hv : d ≠ 0)
    (hn : tensorQuad (recordMetric (R i) x) d = 0),
    Tendsto (fun t => microscopicAreaError (unifiedPreparation (R i) x d) eta
      (inducedArea (recordMetric (R i))
        (screens i x hx d hv hn).curve
        (screens i x hx d hv hn).screen.vectors) t / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 0)

/-- Branch C: if a light Lorentz wedge is supplied at every null direction,
    Maxwell stress is identified with the curved recorded source, the curved
    source is covariantly conserved, and the named H3 bridge holds, then the
    existing v338 implication gives one Einstein coefficient on the atlas.
    Maxwell's flat distributional conservation is not substituted for the
    separate curved conservation premise. The recorded screen is not proved
    to be the screen of the selected wedge; hH3 assumes that physical link.
    The Maxwell state is unrestricted, and no lightH3/charge_link is used. -/
theorem passage_with_light_lorentz_wedges_all_null_h3_to_einstein_atlas
    {n X ι : Type} [Fintype n] [DecidableEq n]
    [TopologicalSpace X] [PreconnectedSpace X]
    {d : n → ℝ} (hd : ∀ i, 0 < d i) (hinj : Function.Injective d)
    {W : Matrix n n ℂ} (hW : Wᴴ * W = 1)
    (hω : ∀ y, (rhoD d * adU W y).trace = (rhoD d * y).trace)
    {L : LightOneParticle} (C : FockCertificate L)
    (M : MaxwellCertificate C) (ψ : (lightNet C).H)
    (G : ℝ) (hG : 0 < G)
    (U : ι → Set Coordinate4) (hopenU : ∀ i, IsOpen (U i))
    (hconnU : ∀ i, IsPreconnected (U i))
    (R : ∀ i, GravitationalResponseRecord (U i))
    (screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i)))
    (wedges : LightLorentzWedgeFamilyEveryNullDirection C U R)
    (source_matches_maxwell : ∀ i x, x ∈ U i →
      recordSource (R i) x = M.T.T ψ x)
    (conserved_curved : ∀ i, ∀ x ∈ U i, ∀ j,
      tensorFieldDivergence (metricInverse (recordMetric (R i)))
        (leviCivitaField (recordMetric (R i))
          (metricInverse (recordMetric (R i))))
        (recordSource (R i)) x j = 0)
    (hH3_from_passage_and_wedges :
      (∀ y, adU W (diagExpect y) = diagExpect (adU W y)) →
      ∀ i x (hx : x ∈ U i) v (hv : v ≠ 0)
        (hn : tensorQuad (recordMetric (R i) x) v = 0)
        (w : LightLorentzWedgeAt (lightNet C) (recordMetric (R i) x) x v),
        x ∈ closure w.region →
        Tendsto (fun t => microscopicAreaError (unifiedPreparation (R i) x v)
          ((4 * G)⁻¹)
          (inducedArea (recordMetric (R i))
            (screens i x hx v hv hn).curve
            (screens i x hx v hv hn).screen.vectors) t / t^2)
          (𝓝[<] (0 : ℝ)) (𝓝 0))
    (anchor : ι) (S : ι → Set X) (hopenS : ∀ i, IsOpen (S i))
    (hcover : ∀ x, ∃ i, x ∈ S i) (hne : ∀ i, (S i).Nonempty)
    (chart : ∀ i, S i ≃ₜ U i)
    (htransitions : ∀ i j p (_hi : p ∈ S i) (hj : p ∈ S j),
      ∃ D : SmoothRecordTransition U R S chart i j,
        (chart j ⟨p, hj⟩).val ∈ D.source) :
    ∃! a : ℝ, ∀ i x, x ∈ U i →
      recordEinstein (R i) x + a • recordMetric (R i) x =
        (8 * Real.pi * G) • M.T.T ψ x := by
  have hpost : ∀ y, adU W (diagExpect y) = diagExpect (adU W y) :=
    TGLExt.Fundacao.the_post_lives_in_the_passage hd hinj hW hω
  have harea : NamedAtlasH3 ((4 * G)⁻¹) U R screens := by
    intro i x hx v hv hn
    let w := wedges.wedge_for i x hx v hv hn
    exact hH3_from_passage_and_wedges hpost i x hx v hv hn w w.horizon_touch
  have hG0 : G ≠ 0 := ne_of_gt hG
  have heta : (4 * G)⁻¹ ≠ 0 := inv_ne_zero (mul_ne_zero (by norm_num) hG0)
  let A : ι → AreaChart ((4 * G)⁻¹) := fun i => {
    domain := U i
    open_domain := hopenU i
    connected_domain := hconnU i
    record := R i
    screens := screens i
    conserved := conserved_curved i
    area := by
      intro x hx v hv hn
      exact harea i x hx v hv hn
  }
  have htransA : ∀ i j p (_hi : p ∈ S i) (hj : p ∈ S j),
      ∃ D : SmoothRecordTransition (fun i => (A i).domain)
        (fun i => (A i).record) S chart i j,
        (chart j ⟨p, hj⟩).val ∈ D.source := by
    intro i j p hi hj
    simpa only [A] using htransitions i j p hi hj
  have hfield := connected_smooth_atlas_einstein ((4 * G)⁻¹) heta A anchor
    S hopenS hcover hne chart htransA
  have hfieldG : ∃! a : ℝ, ∀ i x, x ∈ U i →
      recordEinstein (R i) x + a • recordMetric (R i) x =
        (8 * Real.pi * G) • recordSource (R i) x := by
    simpa only [A, ChatgptAudit.entropy_density_einstein_coefficient G hG0] using hfield
  rcases hfieldG with ⟨a, ha, huniq⟩
  refine ⟨a, ?_, ?_⟩
  · intro i x hx
    simpa only [source_matches_maxwell i x hx] using ha i x hx
  · intro b hb
    apply huniq b
    intro i x hx
    simpa only [source_matches_maxwell i x hx] using hb i x hx

#print axioms LightLorentzWedgeAt
#print axioms LightLorentzWedgeFamilyEveryNullDirection
#print axioms NamedAtlasH3
#print axioms passage_with_light_lorentz_wedges_all_null_h3_to_einstein_atlas

end
end ChatgptAudit.F23CurvedFieldBranchC
