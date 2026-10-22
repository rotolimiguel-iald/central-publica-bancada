import TGLExt.LiganteLeiCampoCurvoRamoC
import TGLExt.O16.PeriodHeatCalibration_v3

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
