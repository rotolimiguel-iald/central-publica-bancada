import CanonicalFockWeightDomainR1
import CanonicalFockGNSR2

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.CanonicalFockWeightOrbit
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockGNS
open scoped ENNReal NNReal
noncomputable section

theorem scalarWeightOrbit_memLp 
    (A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : HasFiniteScalarSquare A) :
    MemLp (fun s : ℝ => dualAmbient s A regularFockVacuum) 2 := by
  have hq := hA
  simp only [HasFiniteScalarSquare, dualQuadraticIntegral, dualQuadraticIntegrand_star_mul] at hq
  have hn : ENNReal.ofReal dualHaarFactor ≠ 0 :=
    ne_of_gt (ENNReal.ofReal_pos.mpr dualHaarFactor_pos)
  have hi : (∫⁻ s : ℝ, ENNReal.ofReal (‖dualAmbient s A regularFockVacuum‖ ^ 2)) < ⊤ := by
    by_contra h
    have ht := top_unique (not_lt.mp h)
    rw [ht] at hq
    rw [ENNReal.mul_top hn] at hq
    exact (lt_irrefl _) hq
  refine ⟨(dualAmbient_strongly_continuous A regularFockVacuum).aestronglyMeasurable,?_⟩
  rw [eLpNorm_lt_top_iff_lintegral_rpow_enorm_lt_top (by norm_num) (by norm_num)]
  have he (s : ℝ) : ENNReal.ofReal (‖dualAmbient s A regularFockVacuum‖ ^ 2) =
      (‖dualAmbient s A regularFockVacuum‖₊ : ℝ≥0∞) ^ 2 := by
    rw [ENNReal.ofReal_pow (norm_nonneg _), ofReal_norm, enorm_eq_nnnorm]
  simp_rw [he] at hi
  simpa only [ENNReal.toReal_ofNat, ENNReal.rpow_two, enorm_eq_nnnorm, pow_two] using hi

/-- An orbit vector in a concrete Hilbert space. Completion of its range,
the left representation and the Tomita operator are separate constructions. -/
def scalarWeightOrbit  (A : scalarWeightLeftIdeal ) :
    RegularHilbert (RegularHilbert F) :=
  (Real.sqrt dualHaarFactor : ℝ) •
    (scalarWeightOrbit_memLp A.val.val A.property).toLp
      (fun s : ℝ => dualAmbient s A.val.val regularFockVacuum)

theorem scalarWeightOrbit_norm_sq  (A : scalarWeightLeftIdeal ) :
    ENNReal.ofReal (‖scalarWeightOrbit A‖ ^ 2) =
      dualQuadraticIntegral (star A.val.val * A.val.val) regularFockVacuum := by
  have hm := scalarWeightOrbit_memLp A.val.val A.property
  have hi := (memLp_two_iff_integrable_sq_norm hm.1).mp hm
  have hs : ‖scalarWeightOrbit A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val regularFockVacuum‖ ^ 2 := by
    unfold scalarWeightOrbit
    rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt dualHaarFactor_pos.le,
      ← Fourier.integral_norm_sq_eq_L2 _ hm]
  rw [hs, ENNReal.ofReal_mul dualHaarFactor_pos.le]
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul]
  rw [ofReal_integral_eq_lintegral_ofReal hi (Filter.Eventually.of_forall (fun s => sq_nonneg _))]

theorem scalarWeightOrbit_ae  (A : scalarWeightLeftIdeal ) :
    (scalarWeightOrbit A : ℝ → RegularHilbert F) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val regularFockVacuum := by
  let hm := scalarWeightOrbit_memLp A.val.val A.property
  filter_upwards [Lp.coeFn_smul (Real.sqrt dualHaarFactor : ℝ)
    (hm.toLp (fun s : ℝ => dualAmbient s A.val.val regularFockVacuum)),hm.coeFn_toLp]
    with s h1 h2
  change ((Real.sqrt dualHaarFactor : ℝ) • hm.toLp _) s = _
  simp only [Pi.smul_apply] at h1
  rw [h1,h2]

theorem scalarWeightOrbit_add  (A B : scalarWeightLeftIdeal ) :
    scalarWeightOrbit (A+B) = scalarWeightOrbit A + scalarWeightOrbit B := by
  apply Lp.ext
  filter_upwards [scalarWeightOrbit_ae (A+B),scalarWeightOrbit_ae A,
    scalarWeightOrbit_ae B,Lp.coeFn_add (scalarWeightOrbit A) (scalarWeightOrbit B)]
    with s h1 h2 h3 h4
  simp only [Pi.add_apply] at h4
  rw [h1,h4,h2,h3]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (A.val.val+B.val.val) regularFockVacuum = _
  rw [dualAmbient_add_apply]
  exact _root_.smul_add (Real.sqrt dualHaarFactor : ℝ)
    (dualAmbient s A.val.val regularFockVacuum) (dualAmbient s B.val.val regularFockVacuum)

theorem scalarWeightOrbit_smul  (c : ℂ) (A : scalarWeightLeftIdeal ) :
    scalarWeightOrbit (c • A) = c • scalarWeightOrbit A := by
  apply Lp.ext
  filter_upwards [scalarWeightOrbit_ae (c • A),scalarWeightOrbit_ae A,
    Lp.coeFn_smul c (scalarWeightOrbit A)] with s h1 h2 h3
  simp only [Pi.smul_apply] at h3
  rw [h1,h3,h2]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (c • A.val.val) regularFockVacuum = _
  rw [map_smul]
  change (Real.sqrt dualHaarFactor : ℝ) • (c • dualAmbient s A.val.val regularFockVacuum) = _
  exact smul_comm _ _ _

def scalarWeightLinear  :
    scalarWeightLeftIdeal →ₗ[ℂ] RegularHilbert (RegularHilbert F) where
  toFun := scalarWeightOrbit 
  map_add' := scalarWeightOrbit_add 
  map_smul' := scalarWeightOrbit_smul 

theorem scalarWeightOrbit_zero_iff  (A : scalarWeightLeftIdeal ) :
    scalarWeightOrbit A = 0 ↔ A = 0 := by
  constructor
  · intro h
    have hq : dualQuadraticIntegral (star A.val.val * A.val.val) regularFockVacuum = 0 := by
      rw [← scalarWeightOrbit_norm_sq,h]
      simp only [norm_zero,zero_pow (by norm_num : (2 : ℕ) ≠ 0),ENNReal.ofReal_zero]
    have hm := (core).mul_mem
      ((core).toStarSubalgebra.star_mem' A.val.property) A.val.property
    have hz := (F1Fecho.CanonicalFockFaithfulWeight.weight_faithful ⟨star A.val.val * A.val.val,hm,star_mul_self_nonneg A.val.val⟩).mp hq
    apply Subtype.ext
    apply Subtype.ext
    exact (CStarRing.star_mul_self_eq_zero_iff A.val.val).mp hz
  · rintro rfl
    exact (scalarWeightLinear ).map_zero

theorem scalarWeightLinear_injective  :
    Function.Injective (scalarWeightLinear ) := by
  intro A B h
  have hz : scalarWeightLinear (A-B) = 0 := by rw [map_sub,h,sub_self]
  exact sub_eq_zero.mp ((scalarWeightOrbit_zero_iff (A-B)).mp hz)


theorem scalarWeightOrbit_uniform  (A : finiteLeftIdeal) :
    scalarWeightOrbit (Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight ) A) =
      scalarGNSOrbit A := rfl

theorem scalarWeightOrbit_norm_sq_real  (A : scalarWeightLeftIdeal ) :
    ‖scalarWeightOrbit A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val regularFockVacuum‖ ^ 2 := by
  unfold scalarWeightOrbit
  rw [norm_smul,mul_pow,Real.norm_eq_abs,sq_abs,Real.sq_sqrt dualHaarFactor_pos.le,
    ← Fourier.integral_norm_sq_eq_L2 _ (scalarWeightOrbit_memLp A.val.val A.property)]

end
end F1Fecho.CanonicalFockWeightOrbit
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockWeightOrbit).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
