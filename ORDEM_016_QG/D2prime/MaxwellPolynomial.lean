import StressTensorDataLocal_v2

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix
open TGLExt.ContratoQGv31
namespace ORDEM016.D2prime

/-- Covariant Maxwell tensor in a Minkowski frame (+---), classical fields.
This polynomial is not an operator-valued Wick distribution. -/
def energy (E B : Fin 3 → ℝ) : ℝ :=
  (E 0^2+E 1^2+E 2^2+B 0^2+B 1^2+B 2^2)/2

def flux (E B : Fin 3 → ℝ) : Fin 3 → ℝ :=
  ![E 1*B 2-E 2*B 1,E 2*B 0-E 0*B 2,E 0*B 1-E 1*B 0]

def maxwellTensor (E B : Fin 3 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![energy E B, -flux E B 0, -flux E B 1, -flux E B 2;
     -flux E B 0, energy E B-E 0^2-B 0^2, -E 0*E 1-B 0*B 1, -E 0*E 2-B 0*B 2;
     -flux E B 1, -E 0*E 1-B 0*B 1, energy E B-E 1^2-B 1^2, -E 1*E 2-B 1*B 2;
     -flux E B 2, -E 0*E 2-B 0*B 2, -E 1*E 2-B 1*B 2, energy E B-E 2^2-B 2^2]

theorem maxwell_symmetric (E B : Fin 3 → ℝ) :
    (maxwellTensor E B).transpose=maxwellTensor E B := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem maxwell_trace_zero (E B : Fin 3 → ℝ) :
    (∑ i : Fin 4, ChatgptAudit.LocalStress.metricSign i * maxwellTensor E B i i)=0 := by
  simp [Fin.sum_univ_four,ChatgptAudit.LocalStress.metricSign,maxwellTensor,energy]
  ring

/-- Classical pointwise identity only; no positivity assertion for renormalized
quantum stress expectations is made or used. -/
theorem maxwell_null_flux (E B : Fin 3 → ℝ) :
    pairing (maxwellTensor E B) nullDir nullDir = (E 1-B 2)^2+(E 2+B 1)^2 := by
  simp [pairing,dotProduct,Matrix.mulVec,Fin.sum_univ_four,nullDir,maxwellTensor,energy,flux]
  ring

theorem maxwell_null_flux_nonnegative (E B : Fin 3 → ℝ) :
    0 ≤ pairing (maxwellTensor E B) nullDir nullDir := by
  rw [maxwell_null_flux]; positivity

theorem maxwell_zero : maxwellTensor 0 0=0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [maxwellTensor,energy,flux]

#print axioms maxwell_symmetric
#print axioms maxwell_trace_zero
#print axioms maxwell_null_flux
#print axioms maxwell_null_flux_nonnegative
#print axioms maxwell_zero
end ORDEM016.D2prime
