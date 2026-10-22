import TGLExt.Fundacao
import TGLExt.GeneralMetricClausius
import TGLExt.GravitationalChartGluing
import TGLExt.TopologicalAtlasGluing
import TGLExt.SmoothSelectedAtlasGluing
import TGLExt.HorizonEinsteinReconstruction
import TGLExt.TheImportedSecondQuantization
import TGLExt.O16.PeriodHeatCalibration_v3

/-!
F2.3, branch C of the anti-wall tree. This statement is a conditional interface.
The Lorentz wedge orbit of the light net, a source identification, curved
conservation, and H3 at every point and null direction are named inputs.
No rotation of the light net, all-wedge family, or H3 is constructed here.
The finite passage identity is used through an explicit bridge hypothesis;
because that identity is already provable, the bridge contains H3 in full.
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

/-!
F2.3, temperature refinement of branch C. A faithful angular reading is
attached to the *same supplied light wedge* through observer_boost_eq.
Its period and inverse period are consequences of the O16 theorem, and the
boost-segment Clausius expression uses that inverse period. The bridge from
this one-wedge algebra to curved H3 on every screen remains a named input.
There is no KMS or state-derived H3 theorem here.
-/

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.F23CurvedFieldTemperature

open Matrix Filter Topology Set TGLExt ChatgptAudit
open ChatgptAudit.GeneralMetric ChatgptAudit.GeneralClausius
open ChatgptAudit.GravitationalRecord ChatgptAudit.ChartGluing
open ChatgptAudit.TopologicalGluing ChatgptAudit.SmoothAtlasGluing
open ChatgptAudit.UnifiedRecorded ChatgptAudit.Micro021
open ChatgptAudit.F23CurvedFieldBranchC ChatgptAudit.PolarPeriod016
open ChatgptAudit.Boost044 ChatgptAudit.Wave029 TGLExt.ImportedSQ

noncomputable section

/-- A named reading on the same wedge, with observer time t mapped to
    boost rapidity rate*t. Faithfulness concerns the angular reading
    Circle.exp(rate*t), not a global Lorentz action or KMS state. -/
structure FaithfullyReadLightWedgeAt
    (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (g : Matrix (Fin 4) (Fin 4) ℝ) (x d : Coordinate4) where
  wedge : LightLorentzWedgeAt W g x d
  rate : ℝ
  period : ℝ
  rate_pos : 0 < rate
  period_pos : 0 < period
  observer_boost : ℝ → Matrix (Fin 4) (Fin 4) ℝ
  observer_boost_eq : ∀ t, observer_boost t = wedge.boost (rate * t)
  faithful : AngularQuotientFaithful rate period

/-- Readings on the supplied wedge family at every chart point and null
    direction. This is an input: no other-wedge action is constructed. -/
structure FaithfullyReadLightWedgeFamily
    {L : LightOneParticle} (C : FockCertificate L)
    {ι : Type} (U : ι → Set Coordinate4)
    (R : ∀ i, GravitationalResponseRecord (U i)) where
  reading_for : ∀ i x (_hx : x ∈ U i) d (_hv : d ≠ 0)
      (_hn : tensorQuad (recordMetric (R i) x) d = 0),
    FaithfullyReadLightWedgeAt (lightNet C) (recordMetric (R i) x) x d

/-- Positive faithful reading forces exactly one positive angular turn. -/
theorem faithful_reading_one_turn
    {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    {g : Matrix (Fin 4) (Fin 4) ℝ} {x d : Coordinate4}
    (r : FaithfullyReadLightWedgeAt W g x d) :
    r.rate * r.period = 2 * Real.pi := by
  rcases (faithful_period_iff (ne_of_gt r.rate_pos)).mp r.faithful with h | h
  · exact h
  · have hm : 0 < r.rate * r.period := mul_pos r.rate_pos r.period_pos
    have hpi : 0 < Real.pi := Real.pi_pos
    nlinarith

/-- The temperature coefficient is a theorem of the faithful reading;
    no independent temperature value appears in the premises. -/
theorem faithful_reading_inverse_period
    {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    {g : Matrix (Fin 4) (Fin 4) ℝ} {x d : Coordinate4}
    (r : FaithfullyReadLightWedgeAt W g x d) :
    1 / r.period = r.rate / (2 * Real.pi) :=
  reciprocal_temperature r.rate_pos r.period_pos r.faithful

/-- The existing boost defect already uses rate/(2*pi) by definition.
    O16 rewrites it with the derived 1/period of this same reading. -/
def BoostDefectIdentity
    {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    {g : Matrix (Fin 4) (Fin 4) ℝ} {x d : Coordinate4}
    (r : FaithfullyReadLightWedgeAt W g x d) : Prop :=
  ∀ a c mass eta t : ℝ,
    boostSegmentDefect a c r.rate mass eta t =
      boostSegmentHeat a c r.rate (waveMatter a c mass) t -
        ((1 / r.period) * eta) * boostSegmentArea a c t

theorem faithful_reading_boost_defect
    {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    {g : Matrix (Fin 4) (Fin 4) ℝ} {x d : Coordinate4}
    (r : FaithfullyReadLightWedgeAt W g x d) :
    BoostDefectIdentity r := by
  intro a c mass eta t
  exact boost_defect_with_derived_period a c r.rate mass eta t r.period
    r.rate_pos r.period_pos r.faithful

/-- Branch C with a faithful angular reading attached to each supplied
    light wedge. The one-turn result, inverse period and boost balance are
    passed to the *named* all-screen H3 bridge. Hence this theorem does not
    infer curved Clausius or KMS from the 2x2 angular algebra. -/
theorem faithful_boost_reading_all_wedges_named_h3_to_einstein_atlas
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
    (readings : FaithfullyReadLightWedgeFamily C U R)
    (source_matches_maxwell : ∀ i x, x ∈ U i →
      recordSource (R i) x = M.T.T ψ x)
    (conserved_curved : ∀ i, ∀ x ∈ U i, ∀ j,
      tensorFieldDivergence (metricInverse (recordMetric (R i)))
        (leviCivitaField (recordMetric (R i))
          (metricInverse (recordMetric (R i))))
        (recordSource (R i)) x j = 0)
    (hH3_from_reading :
      (∀ y, adU W (diagExpect y) = diagExpect (adU W y)) →
      ∀ i x (hx : x ∈ U i) v (hv : v ≠ 0)
        (hn : tensorQuad (recordMetric (R i) x) v = 0)
        (r : FaithfullyReadLightWedgeAt
          (lightNet C) (recordMetric (R i) x) x v),
        x ∈ closure r.wedge.region →
        r.rate * r.period = 2 * Real.pi →
        1 / r.period = r.rate / (2 * Real.pi) →
        BoostDefectIdentity r →
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
  let wedges : LightLorentzWedgeFamilyEveryNullDirection C U R :=
    { wedge_for := fun i x hx v hv hn =>
        (readings.reading_for i x hx v hv hn).wedge }
  exact passage_with_light_lorentz_wedges_all_null_h3_to_einstein_atlas
    hd hinj hW hω C M ψ G hG U hopenU hconnU R screens wedges
    source_matches_maxwell conserved_curved
    (by
      intro hpost i x hx v hv hn _w _htouch
      let r := readings.reading_for i x hx v hv hn
      exact hH3_from_reading hpost i x hx v hv hn r
        r.wedge.horizon_touch (faithful_reading_one_turn r)
        (faithful_reading_inverse_period r)
        (faithful_reading_boost_defect r))
    anchor S hopenS hcover hne chart htransitions

#print axioms FaithfullyReadLightWedgeAt
#print axioms FaithfullyReadLightWedgeFamily
#print axioms faithful_reading_one_turn
#print axioms faithful_reading_inverse_period
#print axioms faithful_reading_boost_defect
#print axioms faithful_boost_reading_all_wedges_named_h3_to_einstein_atlas

end
end ChatgptAudit.F23CurvedFieldTemperature
