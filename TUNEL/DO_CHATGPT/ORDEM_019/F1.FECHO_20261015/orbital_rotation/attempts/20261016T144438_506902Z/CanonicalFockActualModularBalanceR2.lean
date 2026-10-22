import GenericPolarModularBalanceR1
import GeneralRepresentedRegularResolventR4
import GeneralGNSVectorInjectivityR1
import CanonicalFockGNSOrderR4
import CanonicalFockRegularGNSR9
import CanonicalFockPolarFlipR4
import CanonicalFockRightPolarBridgeR5

/-! UNCOMPILED CANDIDATE, 2026-10-16, codex-mission-memory-review.
Concrete consumer of the actual dual-weight Fock GNS suppliers.
R2 fixes name resolution, fixes both Hilbert parameters of represented transport,
and transports the complement through an explicitly typed star representation.
The modular implementation is supplied by its existing concrete theorem.
This bounded balance is one component; the full trace and finite projection
remain separate obligations. No premise is added to the R1 target. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.CanonicalFockActualModularBalanceCandidateR2
open F1Fecho.CanonicalFockGNS (GNSHilbert)
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugateRealHom
  resolventDampingOperator resolventPhaseOperator resolventImaginaryPower)

local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
local instance : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar F1Fecho.CanonicalFockGNS.GNSSubspace
local instance : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)

abbrev π : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra →⋆ₐ[ℂ]
    (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation
abbrev T : GNSHilbert →L[ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent
abbrev J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor
abbrev r : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra :=
  F1Fecho.RepresentedRegularResolvent.resolventElement
    F1Fecho.CanonicalFockRegular.fockFlow F1Fecho.CanonicalFockRegular.M
abbrev A : GNSHilbert →L[ℂ] GNSHilbert := π r
abbrev L (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  π (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement t)
abbrev R (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockRegularRightGNS.regularRightGNS t

private theorem conjugate_right (t : ℝ) :
    antiunitaryConjugate (H := GNSHilbert) J (R t) = L (-t) := by
  have h := F1Fecho.CanonicalFockRightPolar.scalarTomitaPolar_conjugate_regular_right t
  rw [F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement_star] at h
  exact h

private theorem conjugate_left (t : ℝ) :
    antiunitaryConjugate (H := GNSHilbert) J (L t) = R (-t) := by
  apply ContinuousLinearMap.ext
  intro x
  change J (L t (J.symm x)) = R (-t) x
  have h := F1Fecho.CanonicalFockRightPolar.scalarTomitaPolarFactor_regular_left
    (-t) (J.symm x)
  rw [F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement_star, neg_neg] at h
  change J (L t (J.symm x)) = R (-t) (J (J.symm x)) at h
  simpa only [LinearIsometryEquiv.apply_symm_apply] using h

private theorem represented_commutes
    (C : GNSHilbert →L[ℂ] GNSHilbert) (hC : ∀ t, Commute C (L t)) :
    Commute C A := by
  exact F1Fecho.RepresentedRegularResolvent.represented_resolvent_commutes
    (H := F1Rede.BosonicFock.F) (K := GNSHilbert)
    F1Fecho.CanonicalFockRegular.fockFlow F1Fecho.CanonicalFockRegular.M π
    (fun b q c hb hq x =>
      F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_tendsto_of_uniformly_bounded
        b q c hb hq x) C hC

private theorem representation_one :
    π (1 : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) =
      (1 : GNSHilbert →L[ℂ] GNSHilbert) :=
  map_one π

private theorem representation_complement :
    π (1-r : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) =
      (1-A : GNSHilbert →L[ℂ] GNSHilbert) := by
  calc
    π (1-r : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) =
        π (1 : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) - π r :=
      map_sub π (1 : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) r
    _ = 1-A := congrArg (fun C : GNSHilbert →L[ℂ] GNSHilbert => C-A) representation_one

/-- Bounded balance only; full traciality and semifiniteness are separate. -/
theorem actual_balance :
    let B := antiunitaryConjugate (H := GNSHilbert) J A
    Commute T B ∧ Function.Injective B ∧
      (1-T)*A*(1-B) = T*(1-A)*B := by
  have hT0 : 0 ≤ T := F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_nonneg
  have hT1 : T ≤ 1 := F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_le_one
  have hiT : Function.Injective T :=
    F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_injective
  have hjT : Function.Injective (1-T : GNSHilbert →L[ℂ] GNSHilbert) :=
    F1Fecho.ClosedTomitaFlow.scalarTomitaResolvent_complement_injective (H := GNSHilbert)
      F1Fecho.CanonicalFockWeightModularOperator.actualClosedInput
  have hA0 : 0 ≤ A :=
    F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_nonneg r
      (show 0 ≤ r from F1Fecho.RegularPositiveFlow.regularSpectralResolvent_nonneg
        F1Fecho.CanonicalFockRegular.fockFlow)
  have hr1 : r ≤ (1 : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) :=
    F1Fecho.RegularPositiveFlow.regularSpectralResolvent_le_one
      F1Fecho.CanonicalFockRegular.fockFlow
  have hA1 : A ≤ 1 := by
    calc
      A ≤ π (1 : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) :=
        F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_monotone hr1
      _ = 1 := representation_one
  have hiA : Function.Injective A :=
    F1Fecho.RegularScalarGNSRepresentation.representation_vector_injective
      (H := F1Rede.BosonicFock.F) F1Fecho.CanonicalFockGNS.weightContext r
      (F1Fecho.RegularPositiveFlow.regularSpectralResolvent_injective
        F1Fecho.CanonicalFockRegular.fockFlow)
  have hjA : Function.Injective (1-A : GNSHilbert →L[ℂ] GNSHilbert) := by
    have hsource : Function.Injective
        (1-r : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra).val :=
      F1Fecho.RegularPositiveFlow.regularSpectralResolvent_complement_injective
        F1Fecho.CanonicalFockRegular.fockFlow
    have hrepresented : Function.Injective
        (π (1-r : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra)) :=
      F1Fecho.RegularScalarGNSRepresentation.representation_vector_injective
        (H := F1Rede.BosonicFock.F) F1Fecho.CanonicalFockGNS.weightContext
        (1-r : F1Fecho.CanonicalFockRegular.core.toStarSubalgebra) hsource
    rw [representation_complement] at hrepresented
    exact hrepresented
  have hflip : antiunitaryConjugate (H := GNSHilbert) J T = 1-T :=
    F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolar_conjugate_resolvent
  have hTL (t : ℝ) : Commute T (L t) := by
    have h := (F1Fecho.CanonicalFockRightRoot.scalarTomitaResolvent_regular_right_commutes
      (-t)).map (antiunitaryConjugateRealHom (H := GNSHilbert) J)
    change Commute (antiunitaryConjugate (H := GNSHilbert) J T)
      (antiunitaryConjugate (H := GNSHilbert) J (R (-t))) at h
    rw [hflip, conjugate_right, neg_neg] at h
    simpa only [sub_sub_cancel] using (Commute.one_left (L t)).sub_left h
  have hTA : Commute T A := represented_commutes T hTL
  have hRcomm (t : ℝ) : Commute (R t) A :=
    F1Fecho.CanonicalFockRegularGNS.regularRightGNS_commutes_left t r
  have hBL (t : ℝ) : Commute (antiunitaryConjugate (H := GNSHilbert) J A) (L t) := by
    have h := (hRcomm (-t)).map (antiunitaryConjugateRealHom (H := GNSHilbert) J)
    change Commute (antiunitaryConjugate (H := GNSHilbert) J (R (-t)))
      (antiunitaryConjugate (H := GNSHilbert) J A) at h
    rw [conjugate_right, neg_neg] at h
    exact h.symm
  have hAB : Commute A (antiunitaryConjugate (H := GNSHilbert) J A) :=
    (represented_commutes (antiunitaryConjugate (H := GNSHilbert) J A) hBL).symm
  have hleft (t : ℝ) :
      L t * resolventDampingOperator (H := GNSHilbert) A =
        resolventPhaseOperator (H := GNSHilbert) A t :=
    F1Fecho.RepresentedRegularResolvent.represented_damped_phase
      (H := F1Rede.BosonicFock.F) (K := GNSHilbert)
      F1Fecho.CanonicalFockRegular.fockFlow F1Fecho.CanonicalFockRegular.M π t
  have hmod (t : ℝ) (x : GNSHilbert) :
      resolventImaginaryPower (H := GNSHilbert) T hT0 hT1 hiT hjT t x =
        L t (R (-t) x) := by
    exact F1Fecho.CanonicalFockModularIdentification.actual_modular_implementation t x
  exact F1Fecho.PolarModularBalance.balance (H := GNSHilbert) T A J hT0 hT1 hiT hjT
    hA0 hA1 hiA hjA L R hTA hflip hAB hleft conjugate_left hRcomm hmod

end F1Fecho.CanonicalFockActualModularBalanceCandidateR2
#print axioms F1Fecho.CanonicalFockActualModularBalanceCandidateR2.actual_balance
