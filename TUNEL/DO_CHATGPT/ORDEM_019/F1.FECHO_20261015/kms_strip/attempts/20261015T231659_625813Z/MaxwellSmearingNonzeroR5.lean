import MaxwellChartSmearingR4
import Mathlib.Topology.UrysohnsLemma

/-! Non-vacuity of the concrete compact on-shell smearing: a bump test in
one antisymmetric tensor component has a nonzero original-H1 image. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.MaxwellSmearing
open MeasureTheory Matrix Filter Set
open ChatgptAudit.WignerRapidityMeasure016 TGLExt.ImportedSQ F1Fecho.MaxwellOnShell
open scoped ENNReal CompactlySupported

theorem smear_ne_zero_of_coefficient (f : TestTensor) (hreg : ∀ y∈tsupport f,y.1≠0)
    (y : MomentumCoordinates) (hy : coefficient f y≠0) : smear f hreg≠0 := by
  intro hz
  have hh := smear_rapidity_ae f hreg
  rw [hz,map_zero] at hh
  have ha : coefficient f =ᵐ[momentumMeasure] (fun _ => (0:Fib)) := by
    exact hh.symm.trans (Lp.coeFn_zero Fib 2 momentumMeasure)
  letI : momentumMeasure.IsOpenPosMeasure := by unfold momentumMeasure; infer_instance
  have he := ((coefficient_continuous f hreg).ae_eq_iff_eq momentumMeasure continuous_const).mp ha
  exact hy (congrFun he y)

def tensorUnit01 : Matrix (Fin 4) (Fin 4) ℂ :=
  fun μ ν => if μ=0 ∧ ν=1 then 1 else if μ=1 ∧ ν=0 then -1 else 0

def tensor01 (b : C_c(MomentumCoordinates,ℂ)) : TestTensor where
  toFun := fun y => b y • tensorUnit01
  continuous_toFun := b.continuous.smul continuous_const
  hasCompactSupport' := b.hasCompactSupport.of_isClosed_subset (isClosed_tsupport _)
    (tsupport_smul_subset_left _ _)

theorem tensor01_tsupport (b : C_c(MomentumCoordinates,ℂ)) :
    tsupport (tensor01 b)⊆tsupport b := tsupport_smul_subset_left _ _

theorem tensor01_coefficient0 (b : C_c(MomentumCoordinates,ℂ)) (y : MomentumCoordinates)
    (hy : y.1≠0) : coefficient (tensor01 b) y 0=b y*(transverseMass 0 y.1:ℂ) := by
  have h01 : strength (momentum y) (realLift (screen y 0)) 0 1=(transverseMass 0 y.1:ℂ) := by
    have he : circularScreen 0 y=realLift (screen y 0) := by
      funext i
      simp [circularScreen,screen,realLift]
    rw [← he]
    exact circular_01 0 y hy
  have h10 := strength_antisymmetric (momentum y) (realLift (screen y 0)) 1 0
  change (1/2:ℂ)*(∑ μ,∑ ν,strength (momentum y) (realLift (screen y 0)) μ ν*
    (b y * tensorUnit01 μ ν))=_
  have h20 : (2:Fin 4)≠0 := by decide
  have h21 : (2:Fin 4)≠1 := by decide
  have h30 : (3:Fin 4)≠0 := by decide
  have h31 : (3:Fin 4)≠1 := by decide
  norm_num [Fin.sum_univ_four,tensorUnit01,h20,h21,h30,h31]
  rw [h10,h01]
  ring

theorem exists_nonzero_smear : ∃ f : TestTensor, ∃ hreg : ∀ y∈tsupport f,y.1≠0,
    smear f hreg≠0 := by
  let y : MomentumCoordinates := (![1,0],0)
  have hy : y.1≠0 := by
    intro he
    have hh := congrFun he 0
    norm_num [y] at hh
  have ho : IsOpen {z : MomentumCoordinates | z.1≠0} :=
    isClosed_singleton.isOpen_compl.preimage continuous_fst
  obtain ⟨b,hb,hbc,hbs,_⟩ := exists_continuousMap_one_of_isCompact_subset_isOpen
    (K:={y}) isCompact_singleton ho (by simpa using hy)
  let bc : C_c(MomentumCoordinates,ℂ) :=
    ⟨⟨fun z => (b z:ℂ),Complex.continuous_ofReal.comp b.continuous⟩,
      hbc.of_isClosed_subset (isClosed_tsupport _) (by
        apply closure_mono
        intro z hz
        simpa only [Function.mem_support,Complex.ofReal_ne_zero] using hz)⟩
  have hreg : ∀ z∈tsupport (tensor01 bc),z.1≠0 := by
    intro z hz
    apply hbs
    apply (show tsupport bc⊆tsupport b from closure_mono (by
      intro w hw
      simpa only [Function.mem_support,bc,CompactlySupportedContinuousMap.coe_mk,
        ContinuousMap.coe_mk,Complex.ofReal_ne_zero] using hw))
    exact tensor01_tsupport bc hz
  refine ⟨tensor01 bc,hreg,smear_ne_zero_of_coefficient _ _ y ?_⟩
  intro hz
  have hh := congrArg (fun v : Fib => v 0) hz
  rw [tensor01_coefficient0 bc y hy] at hh
  have hby : b y=1 := hb (by simp)
  have hbc1 : bc y=1 := by simp [bc,hby]
  rw [hbc1,one_mul] at hh
  exact (transverseMass_pos_of_ne_zero 0 y.1 hy).ne' (Complex.ofReal_eq_zero.mp hh)

end F1Fecho.MaxwellSmearing
#print axioms F1Fecho.MaxwellSmearing.smear_ne_zero_of_coefficient
#print axioms F1Fecho.MaxwellSmearing.tensor01_coefficient0
#print axioms F1Fecho.MaxwellSmearing.exists_nonzero_smear
