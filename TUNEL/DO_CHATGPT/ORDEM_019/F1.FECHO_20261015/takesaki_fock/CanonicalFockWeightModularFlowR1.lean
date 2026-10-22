import CanonicalFockWeightModularOperatorR1
/-! Strongly continuous imaginary powers of the actual positive operator
S_nu^* S_nu, on the same scalar-weight GNS Hilbert space. The complement of
its bounded resolvent is injective because the square has trivial kernel.
This is not an identification with the regular conjugation group, KMS, or
an exp(-s)-scaled trace. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightModularFlow
open TGLExt TGLV350.Regular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightModularOperator

theorem scalarTomitaResolvent_complement_injective :
    Function.Injective (1-scalarTomitaResolvent : GNSHilbert →L[ℂ] GNSHilbert) := by
  intro x y h
  apply sub_eq_zero.mp
  have hz : (1-scalarTomitaResolvent : GNSHilbert →L[ℂ] GNSHilbert) (x-y)=0 := by
    rw [map_sub,h,sub_self]
  have hfix : scalarTomitaResolvent (x-y)=x-y := by
    change (x-y)-scalarTomitaResolvent (x-y)=0 at hz
    exact (sub_eq_zero.mp hz).symm
  obtain ⟨z,hzv,heq⟩ := scalarTomitaResolvent_equation (x-y)
  have he : (z:GNSHilbert)=x-y := hzv.trans hfix
  have hd : scalarTomitaSquare z=0 := by
    rw [he] at heq
    exact add_left_cancel (heq.trans (add_zero (x-y)).symm)
  exact he.symm.trans (scalarTomitaSquare_zero_only z hd)
/-- Imaginary powers of the same S†S, defined by its already identified resolvent.
No identification with the regular modular automorphism is claimed here. -/
def scalarTomitaImaginaryPower (t : ℝ) : GNSHilbert ≃ₗᵢ[ℂ] GNSHilbert :=
  resolventImaginaryPower (scalarTomitaResolvent) (scalarTomitaResolvent_nonneg)
    (scalarTomitaResolvent_le_one) (scalarTomitaResolvent_injective)
    (scalarTomitaResolvent_complement_injective) t

theorem scalarTomitaImaginaryPower_damping (t : ℝ) (x : GNSHilbert) :
    scalarTomitaImaginaryPower t (resolventDampingOperator (scalarTomitaResolvent) x)=
      resolventPhaseOperator (scalarTomitaResolvent) t x :=
  resolventImaginaryPower_damping _ _ _ _ _ t x

/-- The dense-range identity uniquely specifies this operator among bounded maps. -/
theorem scalarTomitaImaginaryPower_unique (t : ℝ)
    (U : GNSHilbert →L[ℂ] GNSHilbert)
    (hU : ∀ x, U (resolventDampingOperator (scalarTomitaResolvent) x)=
      resolventPhaseOperator (scalarTomitaResolvent) t x) (x : GNSHilbert) :
    U x=scalarTomitaImaginaryPower t x := by
  refine (resolventDampingOperator_denseRange (scalarTomitaResolvent)
    (scalarTomitaResolvent_nonneg) (scalarTomitaResolvent_le_one)
    (scalarTomitaResolvent_injective) (scalarTomitaResolvent_complement_injective)).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  rw [hU,scalarTomitaImaginaryPower_damping]

theorem scalarTomitaImaginaryPower_zero (x : GNSHilbert) :
    scalarTomitaImaginaryPower 0 x=x :=
  resolventImaginaryPower_zero _ _ _ _ _ x

theorem scalarTomitaImaginaryPower_add (s t : ℝ) (x : GNSHilbert) :
    scalarTomitaImaginaryPower s (scalarTomitaImaginaryPower t x)=
      scalarTomitaImaginaryPower (s+t) x :=
  resolventImaginaryPower_add _ _ _ _ _ s t x

theorem scalarTomitaImaginaryPower_strongly_continuous (x : GNSHilbert) :
    Continuous (fun t : ℝ => scalarTomitaImaginaryPower t x) :=
  resolventImaginaryPower_strongly_continuous _ _ _ _ _ x

theorem scalarTomitaImaginaryPower_inverse (t : ℝ) (x : GNSHilbert) :
    scalarTomitaImaginaryPower (-t) (scalarTomitaImaginaryPower t x)=x := by
  rw [scalarTomitaImaginaryPower_add,neg_add_cancel,scalarTomitaImaginaryPower_zero]

#print axioms scalarTomitaResolvent_complement_injective
#print axioms scalarTomitaImaginaryPower
#print axioms scalarTomitaImaginaryPower_damping
#print axioms scalarTomitaImaginaryPower_unique
#print axioms scalarTomitaImaginaryPower_zero
#print axioms scalarTomitaImaginaryPower_add
#print axioms scalarTomitaImaginaryPower_strongly_continuous
#print axioms scalarTomitaImaginaryPower_inverse
end F1Fecho.CanonicalFockWeightModularFlow
