import CanonicalFockPositiveShiftTransportR2

/-! DECLARADO / UNCOMPILED CANDIDATE, R50, 2026-10-16.
R2 changes the imported transport module and namespace only.
The ShiftRelated completion from V354CyclicTraceCompletion is instantiated on
the SAME represented Fock core and the EXISTING PositiveInput/value. It takes
all shift-related positive readings, including infinite values; it does not
zero-extend the weight outside the positive cone. Positive compatibility is
supplied by the constructed polar and R49 square law in the imported module.
No new trace or equality premise occurs in the final positive/cyclic laws.
This does not package PF or assert full R7. Require compilation and independent
review before regarding the declarations below as established. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 8
noncomputable section
namespace F1Fecho.CanonicalFockCyclicTraceCompletionR2
open F1Fecho.CanonicalFockRegular (core dualAction)
open F1Fecho.CanonicalFockWeight (PositiveInput positiveDual)
open F1Fecho.CanonicalFockInverseSupremum (value value_dual value_faithful value_zero)
open F1Fecho.CanonicalFockPositiveShiftTransportR2
  (positiveAsCore positiveShift_value_compatible)
open TGLV350.Regular (dualAmbient dualAmbient_symm)
open TGLV354.TraceCompletion (ShiftRelated)
open scoped ENNReal

/-- The canonical shift-related positive completion of the existing value. -/
def cyclicTraceCandidate (a : core.toStarSubalgebra) : ℝ≥0∞ :=
  ⨆ (p : PositiveInput) (_ : ShiftRelated (positiveAsCore p) a), value p

theorem positiveTrace_le_cyclicTraceCandidate (p : PositiveInput) :
    value p ≤ cyclicTraceCandidate (positiveAsCore p) :=
  le_iSup_of_le p (le_iSup_of_le (ShiftRelated.refl (positiveAsCore p)) le_rfl)
#print axioms positiveTrace_le_cyclicTraceCandidate

theorem cyclicTraceCandidate_related {a b : core.toStarSubalgebra}
    (h : ShiftRelated a b) : cyclicTraceCandidate a = cyclicTraceCandidate b := by
  apply le_antisymm
  · refine iSup_le fun p => iSup_le fun hp => ?_
    exact le_iSup_of_le p (le_iSup_of_le (hp.trans h) le_rfl)
  · refine iSup_le fun p => iSup_le fun hp => ?_
    exact le_iSup_of_le p (le_iSup_of_le (hp.trans h.symm) le_rfl)
#print axioms cyclicTraceCandidate_related

theorem cyclicTraceCandidate_cyclic (x y : core.toStarSubalgebra) :
    cyclicTraceCandidate (x * y) = cyclicTraceCandidate (y * x) :=
  cyclicTraceCandidate_related (ShiftRelated.cyclic x y)
#print axioms cyclicTraceCandidate_cyclic

private theorem star_positiveAsCore (p : PositiveInput) :
    star (positiveAsCore p) = positiveAsCore p :=
  Subtype.ext (IsSelfAdjoint.of_nonneg p.property.2).star_eq

private theorem candidate_star_le (a : core.toStarSubalgebra) :
    cyclicTraceCandidate (star a) ≤ cyclicTraceCandidate a := by
  refine iSup_le fun p => iSup_le fun hp => ?_
  have h : ShiftRelated (positiveAsCore p) a := by
    simpa only [star_positiveAsCore, star_star] using hp.star_transport
  exact le_iSup_of_le p (le_iSup_of_le h le_rfl)

theorem cyclicTraceCandidate_star (a : core.toStarSubalgebra) :
    cyclicTraceCandidate (star a) = cyclicTraceCandidate a := by
  apply le_antisymm (candidate_star_le a)
  simpa only [star_star] using candidate_star_le (star a)
#print axioms cyclicTraceCandidate_star

private theorem dual_cancel (s : ℝ) (a : core.toStarSubalgebra) :
    dualAction s (dualAction (-s) a) = a := by
  apply Subtype.ext
  change dualAmbient (H := F1Rede.BosonicFock.F) s
    (dualAmbient (-s) a.val) = a.val
  rw [← dualAmbient_symm s]
  exact (dualAmbient s).apply_symm_apply a.val

private theorem positive_dual_cancel (s : ℝ) (p : PositiveInput) :
    positiveDual s (positiveDual (-s) p) = p := by
  apply Subtype.ext
  exact congrArg (fun x : core.toStarSubalgebra => x.val)
    (dual_cancel s (positiveAsCore p))

/-- The same dual character action has the existing exp(-s) weight scaling. -/
theorem cyclicTraceCandidate_dual (s : ℝ) (a : core.toStarSubalgebra) :
    cyclicTraceCandidate (dualAction s a) =
      ENNReal.ofReal (Real.exp (-s)) * cyclicTraceCandidate a := by
  let c : ℝ≥0∞ := ENNReal.ofReal (Real.exp (-s))
  apply le_antisymm
  · refine iSup_le fun p => iSup_le fun hp => ?_
    have hq : ShiftRelated (positiveAsCore (positiveDual (-s) p)) a := by
      have h := hp.map (dualAction (-s)).toMonoidHom
      change ShiftRelated (positiveAsCore (positiveDual (-s) p))
        (dualAction (-s) (dualAction s a)) at h
      have hc : dualAction (-s) (dualAction s a) = a := by
        simpa only [neg_neg] using dual_cancel (-s) a
      simpa only [hc] using h
    have hw : value p = c * value (positiveDual (-s) p) := by
      have h := value_dual s (positiveDual (-s) p)
      rw [positive_dual_cancel] at h
      exact h
    rw [hw]
    have hbound : value (positiveDual (-s) p) ≤ cyclicTraceCandidate a :=
      le_iSup_of_le (positiveDual (-s) p) (le_iSup_of_le hq le_rfl)
    exact mul_le_mul_right hbound c
  · change c * (⨆ (p : PositiveInput) (_ : ShiftRelated (positiveAsCore p) a),
        value p) ≤ _
    rw [ENNReal.mul_iSup]
    refine iSup_le fun p => ?_
    rw [ENNReal.mul_iSup]
    refine iSup_le fun hp => ?_
    have hq : ShiftRelated (positiveAsCore (positiveDual s p)) (dualAction s a) :=
      hp.map (dualAction s).toMonoidHom
    have hw := value_dual s p
    change value (positiveDual s p) = c * value p at hw
    rw [← hw]
    exact le_iSup_of_le (positiveDual s p) (le_iSup_of_le hq le_rfl)
#print axioms cyclicTraceCandidate_dual

/-- Exact agreement on every positive operator, including infinite values.
The compatibility premise of the generic template is already discharged. -/
theorem cyclicTraceCandidate_positive (p : PositiveInput) :
    cyclicTraceCandidate (positiveAsCore p) = value p := by
  apply le_antisymm
  · refine iSup_le fun q => iSup_le fun hq => ?_
    exact le_of_eq (positiveShift_value_compatible q p hq)
  · exact positiveTrace_le_cyclicTraceCandidate p
#print axioms cyclicTraceCandidate_positive

theorem cyclicTraceCandidate_zero : cyclicTraceCandidate 0 = 0 :=
  (cyclicTraceCandidate_positive F1Fecho.CanonicalFockWeight.zero).trans value_zero
#print axioms cyclicTraceCandidate_zero

theorem cyclicTraceCandidate_positive_faithful (p : PositiveInput) :
    cyclicTraceCandidate (positiveAsCore p) = 0 ↔ p.val = 0 := by
  rw [cyclicTraceCandidate_positive]
  exact value_faithful p
#print axioms cyclicTraceCandidate_positive_faithful

end F1Fecho.CanonicalFockCyclicTraceCompletionR2
