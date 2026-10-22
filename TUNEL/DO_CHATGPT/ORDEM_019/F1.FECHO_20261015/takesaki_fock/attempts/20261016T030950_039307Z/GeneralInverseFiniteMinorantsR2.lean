import GeneralInverseStrongFatouR1
import GeneralPositiveSandwichFaithfulR1
/-! Positive minorants in the same represented core. The tracial square law and
an actual finite-square approximate identity are explicit auxiliary hypotheses.
This lemma does not assert either hypothesis for the inverse weight. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open scoped Topology ENNReal NNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:RegularCovariantCore.UnitaryFlow H) (M:VonNeumannAlgebra H)
variable (zeta:RegularHilbert H)

private theorem square_norm_bound {E:Type} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] [CompleteSpace E] (a:E→L[ℂ]E) :
    star a*a ≤ (‖a‖^2:ℝ) • (1:E→L[ℂ]E) := by
  simpa only [Algebra.algebraMap_eq_smul_one] using
    (CStarAlgebra.star_mul_le_algebraMap_norm_sq (a:=a))

private theorem compressed_square_bound {E:Type} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] [CompleteSpace E] (a e:E→L[ℂ]E) :
    (e*a)*star (e*a) ≤ (‖a‖^2:ℝ) • (e*star e) := by
  have h:=star_left_conjugate_le_conjugate (square_norm_bound (star a)) (star e)
  simpa only [star_star,_root_.norm_star,star_mul,mul_assoc,
    mul_smul_comm,smul_mul_assoc,one_mul] using h

/-- A positive square in the existing core, using its actual CFC square root. -/
private theorem core_square_source {E:Type} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] [CompleteSpace E]
    (N:VonNeumannAlgebra E) (X:N.toStarSubalgebra)
    (hX:0≤X.val) : ∃a:N.toStarSubalgebra,
      star a.val*a.val=X.val := by
  let r:=hilbertPositiveSqrt X.val
  have hr:r∈N:=sqrt_mem_core _ _ X.property hX
  refine ⟨⟨r,hr⟩,?_⟩
  change star (CFC.sqrt X.val)*CFC.sqrt X.val=X.val
  rw [(CFC.sqrt_nonneg X.val).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self X.val hX]

theorem inverseSupremum_finite_minorants_of_contractions
    (htr:∀a:(RegularCovariantCore.core B M).toStarSubalgebra,
      inverseSupremum B zeta (star a.val*a.val)=
        inverseSupremum B zeta (a.val*star a.val))
    (E:ℕ→(RegularCovariantCore.core B M).toStarSubalgebra)
    (hn:∀n,‖(E n).val‖≤1)
    (hf:∀n,inverseSupremum B zeta (star (E n).val*(E n).val)<⊤)
    (ht:∀v,Tendsto (fun n=>(E n).val v) atTop (𝓝 v))
    (X:(RegularCovariantCore.core B M).toStarSubalgebra) (hX:0≤X.val) :
    inverseSupremum B zeta X.val =
      ⨆ (Y:(RegularCovariantCore.core B M).toStarSubalgebra) (_:0≤Y.val)
        (_:Y.val≤X.val) (_:inverseSupremum B zeta Y.val<⊤),
        inverseSupremum B zeta Y.val := by
  obtain ⟨a,ha⟩:=core_square_source (RegularCovariantCore.core B M) X hX
  let Y (n:ℕ):(RegularCovariantCore.core B M).toStarSubalgebra :=
    star (E n*a)*(E n*a)
  have hy (n:ℕ): (Y n).val≤X.val := by
    have hs:=square_norm_bound (E n).val
    have hc:(‖(E n).val‖^2:ℝ)≤1:=by nlinarith only [hn n,norm_nonneg (E n).val]
    have hc':(‖(E n).val‖^2:ℝ) • (1:RegularHilbert H→L[ℂ]RegularHilbert H)≤1 := by
      simpa only [one_smul] using smul_le_smul_of_nonneg_right hc
        (show (0:RegularHilbert H→L[ℂ]RegularHilbert H)≤1 from zero_le_one)
    have hp:=star_left_conjugate_le_conjugate (hs.trans hc') a.val
    rw [←ha]
    simpa only [Y,MulMemClass.coe_mul,StarMemClass.coe_star,star_mul,mul_assoc,one_mul] using hp
  have hfin (n:ℕ):inverseSupremum B zeta (Y n).val<⊤ := by
    let r:ℝ≥0:=⟨‖a.val‖^2,sq_nonneg _⟩
    have ho:=compressed_square_bound a.val (E n).val
    have hle:=inverseSupremum_mono B zeta _ _ ho
    rw [inverseSupremum_scale B zeta r,←htr (E n)] at hle
    have hfinite:=hle.trans_lt (ENNReal.mul_lt_top ENNReal.coe_lt_top (hf n))
    exact (htr (E n*a)).trans_lt hfinite
  apply le_antisymm
  · rw [←ha]
    apply inverseSupremum_square_le_of_strong B zeta
      (fun n=>(E n).val*a.val) a.val (fun v=>ht (a.val v))
    intro n
    exact le_iSup_of_le (Y n) (le_iSup_of_le (star_mul_self_nonneg _)
      (le_iSup_of_le (hy n) (le_iSup_of_le (hfin n) le_rfl)))
  · apply iSup_le
    intro Y
    apply iSup_le
    intro _
    apply iSup_le
    intro hYX
    apply iSup_le
    intro _
    exact inverseSupremum_mono B zeta Y.val X.val hYX
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_finite_minorants_of_contractions
