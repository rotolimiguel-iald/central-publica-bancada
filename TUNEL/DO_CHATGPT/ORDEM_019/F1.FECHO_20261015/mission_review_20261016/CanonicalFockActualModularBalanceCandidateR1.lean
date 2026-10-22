import GenericPolarModularBalanceR1
import GeneralRepresentedRegularResolventR4
import GeneralGNSVectorInjectivityR1
import CanonicalFockGNSOrderR4
import CanonicalFockRegularGNSR9
import CanonicalFockPolarFlipR4
import CanonicalFockRightPolarBridgeR5

/-! UNCOMPILED CANDIDATE, 2026-10-16, codex-mission-memory-review.
Concrete consumer of existing results on the actual dual-weight Fock GNS.
This file does not import R12, assume a modular implementation, or establish a trace.
Only the assembly below remains to be typechecked; original sources are preserved. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.CanonicalFockActualModularBalanceCandidate
open TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockGNS F1Fecho.CanonicalFockGNSRepresentation
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockWeightPolar
open F1Fecho.CanonicalFockWeightModularOperator
open F1Fecho.RegularPositiveFlow
open scoped Topology

local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)

abbrev T := CanonicalFockWeightModularOperator.scalarTomitaResolvent
abbrev J := scalarTomitaPolarFactor
abbrev r : core.toStarSubalgebra :=
  RepresentedRegularResolvent.resolventElement fockFlow M
abbrev A := scalarGNSRepresentation r
abbrev L (t : ℝ) := scalarGNSRepresentation (regularRightCoreElement t)
abbrev R := regularRightGNS

private theorem conjugate_right (t : ℝ) :
    antiunitaryConjugate J (R t) = L (-t) := by
  simpa only [J, R, L, regularRightCoreElement_star] using
    CanonicalFockRightPolar.scalarTomitaPolar_conjugate_regular_right t

private theorem conjugate_left (t : ℝ) :
    antiunitaryConjugate J (L t) = R (-t) := by
  apply ContinuousLinearMap.ext
  intro x
  change J (L t (J.symm x)) = R (-t) x
  simpa only [J, L, R, regularRightCoreElement_star, neg_neg,
    LinearIsometryEquiv.apply_symm_apply] using
    CanonicalFockRightPolar.scalarTomitaPolarFactor_regular_left (-t) (J.symm x)

private theorem represented_commutes
    (C : GNSHilbert →L[ℂ] GNSHilbert) (hC : ∀ t, Commute C (L t)) :
    Commute C A := by
  exact RepresentedRegularResolvent.represented_resolvent_commutes
    fockFlow M scalarGNSRepresentation
    (fun b q c hb hq x =>
      CanonicalFockGNSOrder.scalarGNSRepresentation_tendsto_of_uniformly_bounded
        b q c hb hq x) C hC

/-- Bounded balance only; full traciality and semifiniteness are separate. -/
theorem actual_balance :
    let B := antiunitaryConjugate J A
    Commute T B ∧ Function.Injective B ∧
      (1-T)*A*(1-B) = T*(1-A)*B := by
  have hT0 : 0 ≤ T := scalarTomitaResolvent_nonneg
  have hT1 : T ≤ 1 := scalarTomitaResolvent_le_one
  have hiT : Function.Injective T := scalarTomitaResolvent_injective
  have hjT : Function.Injective (1-T : GNSHilbert →L[ℂ] GNSHilbert) :=
    ClosedTomitaFlow.scalarTomitaResolvent_complement_injective actualClosedInput
  have hA0 : 0 ≤ A :=
    CanonicalFockGNSOrder.scalarGNSRepresentation_nonneg r
      (show 0 ≤ r from regularSpectralResolvent_nonneg fockFlow)
  have hr1 : r ≤ 1 := regularSpectralResolvent_le_one fockFlow
  have hA1 : A ≤ 1 := by
    simpa only [map_one] using
      CanonicalFockGNSOrder.scalarGNSRepresentation_monotone hr1
  have hiA : Function.Injective A :=
    RegularScalarGNSRepresentation.representation_vector_injective weightContext r
      (regularSpectralResolvent_injective fockFlow)
  have hjA : Function.Injective (1-A : GNSHilbert →L[ℂ] GNSHilbert) := by
    have h := RegularScalarGNSRepresentation.representation_vector_injective
      weightContext (1-r)
      (show Function.Injective (1-r).val from
        regularSpectralResolvent_complement_injective fockFlow)
    simpa only [map_sub, map_one] using h
  have hflip : antiunitaryConjugate J T = 1-T :=
    scalarTomitaPolar_conjugate_resolvent
  have hTL (t : ℝ) : Commute T (L t) := by
    have h := (CanonicalFockRightRoot.scalarTomitaResolvent_regular_right_commutes
      (-t)).map (antiunitaryConjugateRealHom J)
    change Commute (antiunitaryConjugate J T)
      (antiunitaryConjugate J (R (-t))) at h
    rw [hflip, conjugate_right, neg_neg] at h
    simpa only [sub_sub_cancel] using (Commute.one_left (L t)).sub_left h
  have hTA : Commute T A := represented_commutes T hTL
  have hRcomm (t : ℝ) : Commute (R t) A :=
    CanonicalFockRegularGNS.regularRightGNS_commutes_left t r
  have hBL (t : ℝ) : Commute (antiunitaryConjugate J A) (L t) := by
    have h := (hRcomm (-t)).map (antiunitaryConjugateRealHom J)
    change Commute (antiunitaryConjugate J (R (-t)))
      (antiunitaryConjugate J A) at h
    rw [conjugate_right, neg_neg] at h
    exact h.symm
  have hAB : Commute A (antiunitaryConjugate J A) :=
    (represented_commutes (antiunitaryConjugate J A) hBL).symm
  have hleft (t : ℝ) :
      L t * resolventDampingOperator A = resolventPhaseOperator A t :=
    RepresentedRegularResolvent.represented_damped_phase
      fockFlow M scalarGNSRepresentation t
  have hmod (t : ℝ) (x : GNSHilbert) :
      resolventImaginaryPower T hT0 hT1 hiT hjT t x = L t (R (-t) x) := by
    exact CanonicalFockModularIdentification.actual_modular_implementation t x
  exact PolarModularBalance.balance T A J hT0 hT1 hiT hjT
    hA0 hA1 hiA hjA L R hTA hflip hAB hleft conjugate_left hRcomm hmod

end F1Fecho.CanonicalFockActualModularBalanceCandidate
#print axioms F1Fecho.CanonicalFockActualModularBalanceCandidate.actual_balance
