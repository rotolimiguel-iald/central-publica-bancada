import CanonicalFockPolarRightClosureR2
import CanonicalFockPerturbedWeightOrderR2
import GeneralRegularDomainCutR1
import GeneralInverseFiniteApproximationR1
import CanonicalFockInverseSupremumR2
/-! The bounded-domain estimate on the SAME Fock core. Polar-right membership
of the actual regular translations is an explicit intermediate input here;
it is consumed by the concrete polar consumer, not a trace axiom. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockInverseFiniteness
open TGLExt TGLV350.Regular Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockRegularRightGNS
open F1Fecho.CanonicalFockPolarRight F1Fecho.RegularPositiveFlow F1Fecho.RegularInverseWeight
open scoped ENNReal Topology
local instance : CompleteSpace GNSHilbert := F1Fecho.CanonicalFockGNS.gnsCompleteSpace
variable (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
variable (hreg : ∀t,regularRightCoreElement t∈scalarPolarRightAlgebra J)

include hreg in
 theorem domainCut_right (d:ℝ) (hd:0<d) :
    regularDomainCut fockFlow M d∈scalarPolarRightAlgebra J := by
  exact (scalarPolarRightAlgebra J).sub_mem (scalarPolarRightAlgebra J).one_mem
    ((scalarPolarRightAlgebra J).smul_mem (regularInverseGeneratorCutoff_right J hreg d hd) _)

private theorem hilbert_sqrt_mul_star {H:Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (B:H→L[ℂ]H) (hB:0≤B) : hilbertPositiveSqrt B*star (hilbertPositiveSqrt B)=B := by
  change CFC.sqrt B*star (CFC.sqrt B)=B
  rw [(CFC.sqrt_nonneg B).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self B hB]

include hreg in
 theorem domainCut_bound (d:ℝ) (hd:0<d) (a:scalarWeightLeftIdeal) :
    inverseSupremum fockFlow regularFockVacuum
      (star (a.val.val*(regularDomainCut fockFlow M d).val)*
        (a.val.val*(regularDomainCut fockFlow M d).val)) ≤
      ENNReal.ofReal d⁻¹*dualQuadraticIntegral (star a.val.val*a.val.val) regularFockVacuum := by
  let q:=regularDomainCut fockFlow M d
  have hq:=domainCut_right J hreg d hd
  have hqstar:star q.val=q.val:=(regularDomainCut_bounds fockFlow M d hd).1.isSelfAdjoint.star_eq
  let c:core.toStarSubalgebra:=(Real.sqrt d⁻¹:ℂ) • 1
  have hc:c∈scalarPolarRightAlgebra J:=(scalarPolarRightAlgebra J).smul_mem
    (scalarPolarRightAlgebra J).one_mem _
  have hcoef:(Real.sqrt d⁻¹:ℂ)*(Real.sqrt d⁻¹:ℂ)=(d⁻¹:ℂ):=by
    exact_mod_cast Real.mul_self_sqrt (inv_nonneg.mpr hd.le)
  have hcc:c.val*star c.val=(d⁻¹:ℂ) • 1:=by
    change ((Real.sqrt d⁻¹:ℂ) • 1)*star ((Real.sqrt d⁻¹:ℂ) • 1)=_
    simp only [star_smul,Complex.star_def,Complex.conj_ofReal,star_one,
      smul_mul_assoc,mul_smul_comm,smul_smul,hcoef,one_mul]
  apply iSup_le
  intro e
  obtain ⟨hs,hrs⟩:=regularInverseGeneratorCutoff_sqrt_right J hreg e.val e.property
  let s:core.toStarSubalgebra:=⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow e.val),hs⟩
  let b:=q*s
  have hb:b∈scalarPolarRightAlgebra J:=(scalarPolarRightAlgebra J).mul_mem hq hrs
  have hss:s.val*star s.val=regularInverseGeneratorCutoff fockFlow e.val:=
    hilbert_sqrt_mul_star _ (regularInverseGeneratorCutoff_nonneg fockFlow e.val e.property)
  have hbc:b*star b≤c*star c:=by
    change (q.val*s.val)*star (q.val*s.val)≤c.val*star c.val
    rw [hcc]
    calc
      _=q.val*(s.val*star s.val)*q.val:=by simp only [star_mul,hqstar,mul_assoc]
      _=q.val*regularInverseGeneratorCutoff fockFlow e.val*q.val:=by rw [hss]
      _=regularInverseGeneratorCutoff fockFlow e.val*q.val*q.val:=by
        rw [←(regularDomainCut_commutes fockFlow M e.val d e.property hd).eq]
      _≤_:=regularDomainCut_product_bound fockFlow M e.val d e.property hd
  have hm:=scalarWeight_right_perturbed_mono J b c hb hc hbc a
  calc
    cutoffWeight fockFlow regularFockVacuum e.val (star (a.val.val*q.val)*(a.val.val*q.val))=
        dualQuadraticIntegral (star b.val*(star a.val.val*a.val.val)*b.val) regularFockVacuum:=by
      apply congrArg (fun T=>dualQuadraticIntegral T regularFockVacuum)
      change star s.val*(star (a.val.val*q.val)*(a.val.val*q.val))*s.val=
        star (q.val*s.val)*(star a.val.val*a.val.val)*(q.val*s.val)
      simp only [star_mul,mul_assoc]
    _≤dualQuadraticIntegral (star c.val*(star a.val.val*a.val.val)*c.val) regularFockVacuum:=hm
    _=_:=by
      change dualQuadraticIntegral (star ((Real.sqrt d⁻¹:ℂ) • 1)*(star a.val.val*a.val.val)*
        ((Real.sqrt d⁻¹:ℂ) • 1)) regularFockVacuum=_
      simp only [star_smul,Complex.star_def,Complex.conj_ofReal,star_one,
        smul_mul_assoc,mul_smul_comm,smul_smul,hcoef,one_mul,mul_one]
      rw [←Complex.ofReal_inv]
      exact dualQuadraticIntegral_smul_operator d⁻¹ (inv_nonneg.mpr hd.le) _ regularFockVacuum

include hreg in
 theorem domainCut_bound_all (a:core.toStarSubalgebra) (d:ℝ) (hd:0<d) :
    inverseSupremum fockFlow regularFockVacuum
      (star (a.val*(regularDomainCut fockFlow M d).val)*(a.val*(regularDomainCut fockFlow M d).val)) ≤
      ENNReal.ofReal d⁻¹*dualQuadraticIntegral (star a.val*a.val) regularFockVacuum := by
  by_cases hf:dualQuadraticIntegral (star a.val*a.val) regularFockVacuum<⊤
  · exact domainCut_bound J hreg d hd ⟨a,hf⟩
  · have ht:dualQuadraticIntegral (star a.val*a.val) regularFockVacuum=⊤:=not_lt_top.mp hf
    have hc:ENNReal.ofReal d⁻¹≠0:=ne_of_gt (ENNReal.ofReal_pos.mpr (inv_pos.mpr hd))
    simp only [ht,ENNReal.mul_top hc,le_top]

include hreg in
 theorem finite_contracting_approximate_identity :
    ∃E:ℕ→core.toStarSubalgebra,
      (∀n,‖(E n).val‖≤1) ∧
      (∀n,inverseSupremum fockFlow regularFockVacuum (star (E n).val*(E n).val)<⊤) ∧
      (∀v,Tendsto (fun n=>(E n).val v) atTop (𝓝 v)) :=
  inverseSupremum_finite_contractions_of_domain_bound fockFlow M regularFockVacuum
    (domainCut_bound_all J hreg)

include hreg in
/-- The concrete regular vacuum witnesses a nonzero finite positive element.
This conclusion uses the already proved faithfulness of the SAME inverse
supremum; a zero-valued surrogate cannot satisfy the construction. -/
 theorem exists_positive_finite : ∃X:PositiveInput,
    0<CanonicalFockInverseSupremum.value X ∧ CanonicalFockInverseSupremum.value X<⊤ := by
  obtain ⟨E,hn,hf,ht⟩:=finite_contracting_approximate_identity J hreg
  have hnonzero:∃n,(E n).val regularFockVacuum≠0:=by
    by_contra! hz
    have hzlim:Tendsto (fun n=>(E n).val regularFockVacuum) atTop (𝓝 0):=by
      simpa only [hz] using (tendsto_const_nhds:Tendsto (fun _:ℕ=>(0:RegularHilbert F1Rede.BosonicFock.F)) atTop (𝓝 0))
    exact regularFockVacuum_ne_zero (tendsto_nhds_unique (ht regularFockVacuum) hzlim)
  obtain ⟨n,hnz⟩:=hnonzero
  let X:PositiveInput:=⟨star (E n).val*(E n).val,
    core.mul_mem (core.toStarSubalgebra.star_mem' (E n).property) (E n).property,
    star_mul_self_nonneg _⟩
  have hx:X.val≠0:=by
    intro hz
    have he:(E n).val=0:=(CStarAlgebra.star_mul_self_eq_zero_iff _).mp hz
    exact hnz (by rw [he];rfl)
  refine ⟨X,?_,hf n⟩
  exact pos_iff_ne_zero.mpr (fun h=>hx ((CanonicalFockInverseSupremum.value_faithful X).mp h))

end F1Fecho.CanonicalFockInverseFiniteness
#print axioms F1Fecho.CanonicalFockInverseFiniteness.domainCut_right
#print axioms F1Fecho.CanonicalFockInverseFiniteness.domainCut_bound
#print axioms F1Fecho.CanonicalFockInverseFiniteness.domainCut_bound_all
#print axioms F1Fecho.CanonicalFockInverseFiniteness.finite_contracting_approximate_identity

#print axioms F1Fecho.CanonicalFockInverseFiniteness.exists_positive_finite
