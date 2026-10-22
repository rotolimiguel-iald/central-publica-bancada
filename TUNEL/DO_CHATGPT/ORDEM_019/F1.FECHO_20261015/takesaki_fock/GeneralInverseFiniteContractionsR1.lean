import GeneralInverseFiniteMinorantsR1
import GeneralRegularDomainCutR1
import RegularCoreFiniteWeightR3
/-! Construct the SAME regular-average/domain-cut approximate identity.
The domain-cut bound remains explicit here; its concrete polar-right proof is
a separate consumer. No trace or alternative representation is postulated. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open F1Fecho.RegularPositiveFlow F1Fecho.RegularCovariantCore
open scoped Topology ENNReal NNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:UnitaryFlow H) (M:VonNeumannAlgebra H) (zeta:RegularHilbert H)

theorem inverseSupremum_finite_contractions_of_domain_bound
    (hbound:∀(a:(core B M).toStarSubalgebra) (d:ℝ), 0<d →
      inverseSupremum B zeta
        (star(a.val*(regularDomainCut B M d).val)*(a.val*(regularDomainCut B M d).val)) ≤
          ENNReal.ofReal d⁻¹*dualQuadraticIntegral (star a.val*a.val) zeta) :
    ∃E:ℕ→(core B M).toStarSubalgebra,
      (∀n,‖(E n).val‖≤1) ∧
      (∀n,inverseSupremum B zeta (star(E n).val*(E n).val)<⊤) ∧
      (∀v,Tendsto (fun n=>(E n).val v) atTop (𝓝 v)) := by
  let d:ℕ→ℝ:=fun n=>1/((n:ℝ)+1)
  have hd(n:ℕ):0<d n:=by dsimp[d];positivity
  let e(n:ℕ):(core B M).toStarSubalgebra:=
    ⟨RegularCoreAverage.regularAverage B (d n),RegularCoreAverage.regularAverage_mem B M (d n)⟩
  let E(n:ℕ):=e n*regularDomainCut B M (d n)
  have hqn(n:ℕ):‖(regularDomainCut B M (d n)).val‖≤1:=by
    obtain ⟨h0,h1⟩:=regularDomainCut_bounds B M (d n) (hd n)
    exact (CStarAlgebra.norm_le_norm_of_nonneg_of_le h0 h1).trans ContinuousLinearMap.norm_id_le
  refine ⟨E,?_,?_,?_⟩
  · intro n
    exact (norm_mul_le _ _).trans (by
      simpa only [one_mul] using mul_le_mul (RegularCoreAverage.regularAverage_norm_le_one B (d n))
        (hqn n) (norm_nonneg _) zero_le_one)
  · intro n
    exact (hbound (e n) (d n) (hd n)).trans_lt
      (ENNReal.mul_lt_top ENNReal.ofReal_lt_top
        (RegularCoreFiniteWeight.regularAverage_dualQuadraticIntegral_lt_top B (d n) (hd n) zeta))
  · intro v
    have ht:Tendsto d atTop (𝓝[≠] (0:ℝ)):=by
      refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
      exact Eventually.of_forall (fun n=>ne_of_gt (hd n))
    exact bounded_application_tendsto atTop (fun n=>(e n).val) 1
      (fun n=>RegularCoreAverage.regularAverage_norm_le_one B (d n))
      (fun n=>(regularDomainCut B M (d n)).val v) v v
      (regularDomainCut_tendsto_identity B M v)
      ((RegularCoreAverage.regularAverage_tendsto_identity B v).comp ht)

theorem inverseSupremum_finite_minorants_of_domain_bound
    (hbound:∀(a:(core B M).toStarSubalgebra) (d:ℝ), 0<d →
      inverseSupremum B zeta
        (star(a.val*(regularDomainCut B M d).val)*(a.val*(regularDomainCut B M d).val)) ≤
          ENNReal.ofReal d⁻¹*dualQuadraticIntegral (star a.val*a.val) zeta)
    (htr:∀a:(core B M).toStarSubalgebra,
      inverseSupremum B zeta (star a.val*a.val)=inverseSupremum B zeta (a.val*star a.val))
    (X:(core B M).toStarSubalgebra) (hX:0≤X.val) :
    inverseSupremum B zeta X.val =
      ⨆ (Y:(core B M).toStarSubalgebra) (_:0≤Y.val) (_:Y.val≤X.val)
        (_:inverseSupremum B zeta Y.val<⊤),inverseSupremum B zeta Y.val := by
  obtain ⟨E,hn,hf,ht⟩:=inverseSupremum_finite_contractions_of_domain_bound B M zeta hbound
  exact inverseSupremum_finite_minorants_of_contractions B M zeta htr E hn hf ht X hX
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_finite_contractions_of_domain_bound
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_finite_minorants_of_domain_bound
