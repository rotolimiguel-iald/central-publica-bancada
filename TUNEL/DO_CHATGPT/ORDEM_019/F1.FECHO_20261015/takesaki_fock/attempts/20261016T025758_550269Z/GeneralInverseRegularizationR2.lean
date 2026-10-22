import GeneralCutoffAverageCommutationR1
import GeneralInverseStrongFatouR1
import GeneralPositiveSandwichFaithfulR1
import RegularRightAverageR3
import RegularFiniteStarCoreR2
/-! Traciality reduces to the existing finite star core for the SAME inverse
supremum. Regular averages decrease both square values; Fatou gives extension.
The remaining finite-core tracial equality is an explicit obligation, not proved
by this reduction. The vacuum-fixed hypothesis is consumed in the weight bound. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open F1Fecho.RegularCovariantCore F1Fecho.RegularCoreAverage
open F1Fecho.RegularFiniteStarCore F1Fecho.RegularPositiveFlow
open scoped Topology ENNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:UnitaryFlow H) (M:VonNeumannAlgebra H) (zeta:RegularHilbert H)
variable (hzeta:∀t:ℝ,fibre (boostCLM B t) zeta=zeta)

/-- The full dual square value is recovered from the same one-sided regular
averages. They need not be a monotone sequence: strong Fatou and the actual
right-contraction bound provide the two inequalities. -/
theorem dualSquare_eq_iSup_averages
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) :
    dualQuadraticIntegral (star A.val*A.val) zeta =
      ⨆n:ℕ,dualQuadraticIntegral
        (star (A.val*RegularCoreAverage.regularAverage B (1/((n:ℝ)+1)))*
          (A.val*RegularCoreAverage.regularAverage B (1/((n:ℝ)+1)))) zeta := by
  let d:ℕ→ℝ:=fun n=>1/((n:ℝ)+1)
  have hd:Tendsto d atTop (𝓝[≠] (0:ℝ)) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
    exact Eventually.of_forall (fun n=>by change (1/((n:ℝ)+1):ℝ)≠0; positivity)
  apply le_antisymm
  · apply QuadraticTraceForms.dualSquare_le_of_strong
      (fun n=>A.val*RegularCoreAverage.regularAverage B (d n)) A.val zeta
      (fun v=>(A.val.continuous.tendsto v).comp
        ((RegularCoreAverage.regularAverage_tendsto_identity B v).comp hd))
    intro n
    exact le_iSup (fun n:ℕ=>dualQuadraticIntegral
      (star (A.val*RegularCoreAverage.regularAverage B (d n))*
        (A.val*RegularCoreAverage.regularAverage B (d n))) zeta) n
  · apply iSup_le
    intro n
    exact RegularRightAverage.scalarWeight_right_average_le B M zeta hzeta A _

theorem cutoffWeight_right_average_le
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) (e:ℝ) (he:0<e) (d:ℝ) :
    cutoffWeight B zeta e (star (A.val*RegularCoreAverage.regularAverage B d)*
      (A.val*RegularCoreAverage.regularAverage B d)) ≤ cutoffWeight B zeta e (star A.val*A.val) := by
  let b:=hilbertPositiveSqrt (cutoff B e)
  have hb:b∈RegularCovariantCore.core B M := sqrt_mem_core _ _
    (regularInverseGeneratorCutoff_mem B M e) (regularInverseGeneratorCutoff_nonneg B e he)
  have hc:=regularInverseCutoffSqrt_commutes_average B e he d
  have hprod:(A.val*RegularCoreAverage.regularAverage B d)*b=
      (A.val*b)*RegularCoreAverage.regularAverage B d := by
    rw [mul_assoc,←hc.eq,←mul_assoc]
  have h:=RegularRightAverage.scalarWeight_right_average_le B M zeta hzeta
    (A*⟨b,hb⟩) d
  change dualQuadraticIntegral
    (star b*(star (A.val*RegularCoreAverage.regularAverage B d)*
      (A.val*RegularCoreAverage.regularAverage B d))*b) zeta ≤
    dualQuadraticIntegral (star b*(star A.val*A.val)*b) zeta
  have hs:star b*(star (A.val*RegularCoreAverage.regularAverage B d)*
      (A.val*RegularCoreAverage.regularAverage B d))*b=
    star ((A.val*b)*RegularCoreAverage.regularAverage B d)*
      ((A.val*b)*RegularCoreAverage.regularAverage B d) := by
    rw [←hprod]
    simp only [star_mul,mul_assoc]
  rw [hs]
  simpa only [MulMemClass.coe_mul,star_mul,mul_assoc] using h

theorem inverseSupremum_right_average_le
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) (d:ℝ) :
    inverseSupremum B zeta (star (A.val*RegularCoreAverage.regularAverage B d)*
      (A.val*RegularCoreAverage.regularAverage B d)) ≤ inverseSupremum B zeta (star A.val*A.val) := by
  apply iSup_le
  intro e
  exact (cutoffWeight_right_average_le B M zeta hzeta A e.val e.property d).trans
    (cutoffWeight_le_supremum B zeta e (star A.val*A.val))

private theorem contraction_left_square {E:Type}
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    (c a:E→L[ℂ]E) (hc:‖c‖≤1) : star (c*a)*(c*a)≤star a*a := by
  have hn:‖star c*c‖≤1 := by
    calc
      _ ≤ ‖star c‖*‖c‖ := norm_mul_le _ _
      _ = ‖c‖*‖c‖ := by rw [_root_.norm_star]
      _ ≤ 1*1 := mul_le_mul hc hc (norm_nonneg _) zero_le_one
      _ = 1 := one_mul 1
  have hs:star c*c≤1 :=
    (CStarAlgebra.norm_le_one_iff_of_nonneg (star c*c) (star_mul_self_nonneg c)).mp hn
  simpa only [star_mul,mul_assoc,one_mul] using star_left_conjugate_le_conjugate hs a

theorem inverseSupremum_sandwich_le
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) (d:ℝ) :
    inverseSupremum B zeta (star (RegularFiniteStarCore.regularSandwich B M A d).val*
      (RegularFiniteStarCore.regularSandwich B M A d).val) ≤
        inverseSupremum B zeta (star A.val*A.val) := by
  let e:=RegularCoreAverage.regularAverage B d
  have he:‖star e‖≤1 := by
    simpa only [_root_.norm_star] using RegularCoreAverage.regularAverage_norm_le_one B d
  have ho:=contraction_left_square (star e) (A.val*e) he
  have hp:star (RegularFiniteStarCore.regularSandwich B M A d).val*
      (RegularFiniteStarCore.regularSandwich B M A d).val ≤ star (A.val*e)*(A.val*e) := by
    change star (star e*A.val*e)*(star e*A.val*e)≤star (A.val*e)*(A.val*e)
    simpa only [mul_assoc] using ho
  exact (inverseSupremum_mono B zeta _ _ hp).trans
    (inverseSupremum_right_average_le B M zeta hzeta A d)

theorem inverseSupremum_tracial_iff_core :
    (∀A:(RegularCovariantCore.core B M).toStarSubalgebra,
      inverseSupremum B zeta (star A.val*A.val)=inverseSupremum B zeta (A.val*star A.val)) ↔
    (∀A:(RegularCovariantCore.core B M).toStarSubalgebra,
      A∈RegularFiniteStarCore.finiteDualStarCore B M →
      inverseSupremum B zeta (star A.val*A.val)=inverseSupremum B zeta (A.val*star A.val)) := by
  constructor
  · exact fun h A _=>h A
  · intro hcore
    have hle (A:(RegularCovariantCore.core B M).toStarSubalgebra) :
        inverseSupremum B zeta (star A.val*A.val) ≤ inverseSupremum B zeta (A.val*star A.val) := by
      let d:ℕ→ℝ:=fun n=>1/((n:ℝ)+1)
      have hd:Tendsto d atTop (𝓝[>] (0:ℝ)) := by
        refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
        exact Eventually.of_forall (fun n=>by change (0:ℝ)<1/((n:ℝ)+1); positivity)
      apply inverseSupremum_square_le_of_strong B zeta
        (fun n=>(RegularFiniteStarCore.regularSandwich B M A (d n)).val) A.val
        (fun v=>(RegularFiniteStarCore.regularSandwich_tendsto B M A v).comp hd)
      intro n
      rw [hcore _ (RegularFiniteStarCore.regularSandwich_mem_finiteDualStarCore B M A (d n)
        (by dsimp [d]; positivity))]
      have h:=inverseSupremum_sandwich_le B M zeta hzeta (star A) (d n)
      rw [←RegularFiniteStarCore.regularSandwich_star] at h
      simpa only [StarMemClass.coe_star,star_star] using h
    intro A
    exact le_antisymm (hle A) (by simpa only [StarMemClass.coe_star,star_star] using hle (star A))
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_right_average_le
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_right_average_le
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_sandwich_le
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_tracial_iff_core

#print axioms F1Fecho.RegularInverseWeight.dualSquare_eq_iSup_averages
