import GeneralInverseSupremumR3
import TGLExt.V350DualFormNormality
/-! Order normality of the same inverse supremum, including internal suprema
in the represented von Neumann algebra. Strong convergence is constructed
from monotone bounded operators rather than supplied as an extra premise. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open scoped Topology ENNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:RegularCovariantCore.UnitaryFlow H) (zeta:RegularHilbert H)
variable {ι:Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]

theorem inverseSupremum_preserves_positive_isLUB
    (A:ι→RegularHilbert H→L[ℂ]RegularHilbert H)
    (S:RegularHilbert H→L[ℂ]RegularHilbert H)
    (hpos:∀i,0≤A i) (hmono:Monotone A) (hS:IsLUB (Set.range A) S) :
    inverseSupremum B zeta S=⨆i,inverseSupremum B zeta (A i) := by
  have hbound:∀i,‖A i‖≤‖S‖:=fun i=>
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hS.1 (Set.mem_range_self i))
  obtain ⟨L,_,_,hlim,hL⟩:=ChatgptAudit.Expectation047.monotone_operator_limit
    A hpos hmono ‖S‖ (norm_nonneg S) hbound
  have hLS:L=S:=hL.unique hS
  subst L
  exact inverseSupremum_normal B zeta A S hpos hmono hlim

theorem inverseSupremum_preserves_internal_isLUB
    (N:VonNeumannAlgebra (RegularHilbert H))
    (A:ι→N.toStarSubalgebra) (S:N.toStarSubalgebra)
    (hpos:∀i,0≤A i) (hmono:Monotone A) (hS:IsLUB (Set.range A) S) :
    inverseSupremum B zeta S.val=⨆i,inverseSupremum B zeta (A i).val :=
  inverseSupremum_preserves_positive_isLUB B zeta
    (fun i=>(A i).val) S.val hpos hmono (vonNeumann_isLUB_coe N A S hpos hmono hS)

end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_preserves_positive_isLUB
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_preserves_internal_isLUB
