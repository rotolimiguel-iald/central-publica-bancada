import TheEquationOfTruth_T20_v3
import TGL.FiniteThreeLocks
set_option autoImplicit false
noncomputable section
namespace TGLExt.EquationOfTruth
variable {n : ℕ}
variable (Dc Db Dz : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n))

/-- Exact equality of operators; no claim about floating-point runtime operands. -/
theorem penalty_eq_kernel_H3L :
    (penalty ![Dc.toContinuousLinearMap,Db.toContinuousLinearMap,Dz.toContinuousLinearMap]).toLinearMap =
      TGL.FiniteThreeLocks.H3L Dc Db Dz := by
  ext x
  simp [penalty,Fin.sum_univ_three,TGL.FiniteThreeLocks.H3L,
    ← LinearMap.adjoint_toContinuousLinearMap]

theorem reading_eq_kernel_PF :
    reading (penalty ![Dc.toContinuousLinearMap,Db.toContinuousLinearMap,Dz.toContinuousLinearMap]) =
      TGL.FiniteThreeLocks.PF Dc Db Dz := by
  unfold reading TGL.FiniteThreeLocks.PF
  simp only [penalty_eq_kernel_H3L]

#print axioms penalty_eq_kernel_H3L
#print axioms reading_eq_kernel_PF
end TGLExt.EquationOfTruth
