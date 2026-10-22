import TGLExt.V354TraceShiftEquivalence
import TGLExt.V351RegularCoreTraceConstruction

set_option autoImplicit false

namespace TGLV354.TraceCompletion
open TGLExt TGLV350.Regular TGLV351
noncomputable section

private def asCore {P : SiteProfile} (p : PositiveCoreInput P) :
    (regularCoreAlgebra P).toStarSubalgebra := ⟨p.val, p.property.1⟩

/-- A cyclic candidate, defined on the actual regular core. Agreement with A1
on the positive cone is a separate analytic obligation, not part of this definition. -/
def cyclicTraceCandidate (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) : ENNReal :=
  ⨆ (p : PositiveCoreInput P) (_ : ShiftRelated (asCore p) a),
    scalarInverseLimitWeight P p

theorem cyclicTraceCandidate_related (P : SiteProfile)
    {a b : (regularCoreAlgebra P).toStarSubalgebra} (h : ShiftRelated a b) :
    cyclicTraceCandidate P a = cyclicTraceCandidate P b := by
  apply le_antisymm
  · refine iSup_le fun p => iSup_le fun hp => ?_
    exact le_iSup_of_le p (le_iSup_of_le (hp.trans h) le_rfl)
  · refine iSup_le fun p => iSup_le fun hp => ?_
    exact le_iSup_of_le p (le_iSup_of_le (hp.trans h.symm) le_rfl)

theorem cyclicTraceCandidate_cyclic (P : SiteProfile)
    (x y : (regularCoreAlgebra P).toStarSubalgebra) :
    cyclicTraceCandidate P (x*y) = cyclicTraceCandidate P (y*x) :=
  cyclicTraceCandidate_related P (ShiftRelated.cyclic x y)

private theorem star_asCore {P : SiteProfile} (p : PositiveCoreInput P) :
    star (asCore p) = asCore p :=
  Subtype.ext (IsSelfAdjoint.of_nonneg p.property.2).star_eq

private theorem candidate_star_le (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) :
    cyclicTraceCandidate P (star a) ≤ cyclicTraceCandidate P a := by
  refine iSup_le fun p => iSup_le fun hp => ?_
  have h : ShiftRelated (asCore p) a := by
    simpa only [star_asCore, star_star] using hp.star_transport
  exact le_iSup_of_le p (le_iSup_of_le h le_rfl)

theorem cyclicTraceCandidate_star (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) :
    cyclicTraceCandidate P (star a) = cyclicTraceCandidate P a := by
  apply le_antisymm (candidate_star_le P a)
  simpa only [star_star] using candidate_star_le P (star a)

private theorem dual_cancel (P : SiteProfile) (s : ℝ)
    (a : (regularCoreAlgebra P).toStarSubalgebra) :
    regularDualAction P s (regularDualAction P (-s) a) = a := by
  apply Subtype.ext
  change dualAmbient s (dualAmbient (-s) a.val) = a.val
  rw [← dualAmbient_symm s]
  exact (dualAmbient s).apply_symm_apply a.val

private theorem positive_dual_cancel (P : SiteProfile) (s : ℝ)
    (p : PositiveCoreInput P) : positiveDual P s (positiveDual P (-s) p) = p := by
  apply Subtype.ext
  exact congrArg (fun x : (regularCoreAlgebra P).toStarSubalgebra => x.val)
    (dual_cancel P s (asCore p))

-- The 200000 default timed out while elaborating the concrete core/dual-action
-- coercions (recorded DEV attempt 20260915_135101_052872). Local budget only.
set_option maxHeartbeats 1000000 in
theorem cyclicTraceCandidate_dual (P : SiteProfile) (s : ℝ)
    (a : (regularCoreAlgebra P).toStarSubalgebra) :
    cyclicTraceCandidate P (regularDualAction P s a) =
      ENNReal.ofReal (Real.exp (-s)) * cyclicTraceCandidate P a := by
  let c : ENNReal := ENNReal.ofReal (Real.exp (-s))
  apply le_antisymm
  · refine iSup_le fun p => iSup_le fun hp => ?_
    have hq : ShiftRelated (asCore (positiveDual P (-s) p)) a := by
      have h := hp.map (regularDualAction P (-s)).toMonoidHom
      change ShiftRelated (asCore (positiveDual P (-s) p))
        (regularDualAction P (-s) (regularDualAction P s a)) at h
      have hc : regularDualAction P (-s) (regularDualAction P s a) = a := by
        simpa only [neg_neg] using dual_cancel P (-s) a
      simpa only [hc] using h
    have hw : scalarInverseLimitWeight P p =
        c * scalarInverseLimitWeight P (positiveDual P (-s) p) := by
      have h := scalarInverseLimitWeight_dual P s (positiveDual P (-s) p)
      rw [positive_dual_cancel] at h
      exact h
    rw [hw]
    have hbound : scalarInverseLimitWeight P (positiveDual P (-s) p) ≤
        cyclicTraceCandidate P a :=
      le_iSup_of_le (positiveDual P (-s) p) (le_iSup_of_le hq le_rfl)
    exact mul_le_mul_left' hbound c
  · change c * (⨆ (p : PositiveCoreInput P) (_ : ShiftRelated (asCore p) a),
        scalarInverseLimitWeight P p) ≤ _
    rw [ENNReal.mul_iSup]
    refine iSup_le fun p => ?_
    rw [ENNReal.mul_iSup]
    refine iSup_le fun hp => ?_
    have hq : ShiftRelated (asCore (positiveDual P s p)) (regularDualAction P s a) :=
      hp.map (regularDualAction P s).toMonoidHom
    have hw := scalarInverseLimitWeight_dual P s p
    change scalarInverseLimitWeight P (positiveDual P s p) =
      c * scalarInverseLimitWeight P p at hw
    rw [← hw]
    exact le_iSup_of_le (positiveDual P s p) (le_iSup_of_le hq le_rfl)

/-- Exact remaining analytic obligation. This implication does not construct
its premise and does not instantiate ContinuousCoreData or move a gate. -/
theorem cyclicTraceCandidate_positive_of_compatibility (P : SiteProfile)
    (compatible : ∀ p q : PositiveCoreInput P,
      ShiftRelated (asCore p) (asCore q) →
      scalarInverseLimitWeight P p = scalarInverseLimitWeight P q)
    (p : PositiveCoreInput P) :
    cyclicTraceCandidate P (asCore p) = scalarInverseLimitWeight P p := by
  apply le_antisymm
  · refine iSup_le fun q => iSup_le fun hq => ?_
    exact le_of_eq (compatible q p hq)
  · exact le_iSup_of_le p (le_iSup_of_le (ShiftRelated.refl (asCore p)) le_rfl)

end
end TGLV354.TraceCompletion
