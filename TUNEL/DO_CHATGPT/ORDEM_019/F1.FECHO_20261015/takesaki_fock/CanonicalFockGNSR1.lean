import CanonicalFockFiniteWeightR2
import TGLExt.V350ScalarGNSLinear
/-! The actual scalar GNS orbit of the same Fock regular core.
It is constructed in L2(R; L2(R; Fock)), with the prescribed dual Haar
normalization and no assumed norm equality or faithfulness. The completion
is the closure of this actual orbit range, not the original Fock space. -/
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockGNS
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockFiniteWeight
open scoped ENNReal NNReal Topology
/-- Square integrability of the actual dual orbit follows from the finite
weight, with the fixed positive Haar factor removed explicitly. -/
theorem scalarOrbit_memLp 
    (A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : HasFiniteDualSquare A) :
    MemLp (fun s : ℝ => dualAmbient s A regularFockVacuum) 2 := by
  have hq := finiteSquare_scalar_finite A hA
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul] at hq
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
def scalarGNSOrbit  (A : finiteLeftIdeal) :
    RegularHilbert (RegularHilbert F) :=
  (Real.sqrt dualHaarFactor : ℝ) •
    (scalarOrbit_memLp A.val.val A.property).toLp
      (fun s : ℝ => dualAmbient s A.val.val regularFockVacuum)

theorem scalarGNSOrbit_norm_sq  (A : finiteLeftIdeal) :
    ENNReal.ofReal (‖scalarGNSOrbit A‖ ^ 2) =
      dualQuadraticIntegral (star A.val.val * A.val.val) regularFockVacuum := by
  have hm := scalarOrbit_memLp A.val.val A.property
  have hi := (memLp_two_iff_integrable_sq_norm hm.1).mp hm
  have hs : ‖scalarGNSOrbit A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val regularFockVacuum‖ ^ 2 := by
    unfold scalarGNSOrbit
    rw [norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, Real.sq_sqrt dualHaarFactor_pos.le,
      ← Fourier.integral_norm_sq_eq_L2 _ hm]
  rw [hs, ENNReal.ofReal_mul dualHaarFactor_pos.le]
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul]
  rw [ofReal_integral_eq_lintegral_ofReal hi (Filter.Eventually.of_forall (fun s => sq_nonneg _))]

theorem scalarGNSOrbit_ae  (A : finiteLeftIdeal) :
    (scalarGNSOrbit A : ℝ → RegularHilbert F) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val regularFockVacuum := by
  let hm := scalarOrbit_memLp A.val.val A.property
  filter_upwards [Lp.coeFn_smul (Real.sqrt dualHaarFactor : ℝ)
    (hm.toLp (fun s : ℝ => dualAmbient s A.val.val regularFockVacuum)),hm.coeFn_toLp]
    with s h1 h2
  change ((Real.sqrt dualHaarFactor : ℝ) • hm.toLp _) s = _
  simp only [Pi.smul_apply] at h1
  rw [h1,h2]

theorem scalarGNSOrbit_add  (A B : finiteLeftIdeal) :
    scalarGNSOrbit (A+B) = scalarGNSOrbit A + scalarGNSOrbit B := by
  apply Lp.ext
  filter_upwards [scalarGNSOrbit_ae (A+B),scalarGNSOrbit_ae A,
    scalarGNSOrbit_ae B,Lp.coeFn_add (scalarGNSOrbit A) (scalarGNSOrbit B)]
    with s h1 h2 h3 h4
  simp only [Pi.add_apply] at h4
  rw [h1,h4,h2,h3]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (A.val.val+B.val.val) regularFockVacuum = _
  rw [dualAmbient_add_apply]
  exact _root_.smul_add (Real.sqrt dualHaarFactor : ℝ)
    (dualAmbient s A.val.val regularFockVacuum) (dualAmbient s B.val.val regularFockVacuum)

theorem scalarGNSOrbit_smul  (c : ℂ) (A : finiteLeftIdeal) :
    scalarGNSOrbit (c • A) = c • scalarGNSOrbit A := by
  apply Lp.ext
  filter_upwards [scalarGNSOrbit_ae (c • A),scalarGNSOrbit_ae A,
    Lp.coeFn_smul c (scalarGNSOrbit A)] with s h1 h2 h3
  simp only [Pi.smul_apply] at h3
  rw [h1,h3,h2]
  change (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s (c • A.val.val) regularFockVacuum = _
  rw [map_smul]
  change (Real.sqrt dualHaarFactor : ℝ) • (c • dualAmbient s A.val.val regularFockVacuum) = _
  exact smul_comm _ _ _

def scalarGNSLinear  :
    finiteLeftIdeal →ₗ[ℂ] RegularHilbert (RegularHilbert F) where
  toFun := scalarGNSOrbit
  map_add' := scalarGNSOrbit_add
  map_smul' := scalarGNSOrbit_smul

theorem scalarGNSOrbit_zero_iff  (A : finiteLeftIdeal) :
    scalarGNSOrbit A = 0 ↔ A = 0 := by
  constructor
  · intro h
    have hq : dualQuadraticIntegral (star A.val.val * A.val.val) regularFockVacuum = 0 := by
      rw [← scalarGNSOrbit_norm_sq,h]
      simp only [norm_zero,zero_pow (by norm_num : (2 : ℕ) ≠ 0),ENNReal.ofReal_zero]
    have hm := (core).mul_mem
      ((core).toStarSubalgebra.star_mem' A.val.property) A.val.property
    have hz := (F1Fecho.CanonicalFockFaithfulWeight.weight_faithful
      ⟨star A.val.val * A.val.val,hm,star_mul_self_nonneg A.val.val⟩).mp hq
    apply Subtype.ext
    apply Subtype.ext
    exact (CStarRing.star_mul_self_eq_zero_iff A.val.val).mp hz
  · rintro rfl
    exact (scalarGNSLinear).map_zero

theorem scalarGNSLinear_injective  :
    Function.Injective (scalarGNSLinear) := by
  intro A B h
  have hz : scalarGNSLinear (A-B) = 0 := by rw [map_sub,h,sub_self]
  exact sub_eq_zero.mp ((scalarGNSOrbit_zero_iff (A-B)).mp hz)


def GNSSubspace : Submodule ℂ (RegularHilbert (RegularHilbert F)) :=
  scalarGNSLinear.range.topologicalClosure
abbrev GNSHilbert := GNSSubspace
instance gnsCompleteSpace : CompleteSpace GNSHilbert :=
  Submodule.topologicalClosure.completeSpace scalarGNSLinear.range

def GNSEmbedding : finiteLeftIdeal →ₗ[ℂ] GNSHilbert :=
  scalarGNSLinear.codRestrict GNSSubspace
    (fun A => scalarGNSLinear.range.le_topologicalClosure ⟨A,rfl⟩)

theorem GNSEmbedding_injective : Function.Injective GNSEmbedding := by
  intro A B h
  exact scalarGNSLinear_injective (congrArg Subtype.val h)

end F1Fecho.CanonicalFockGNS
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockGNS).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
