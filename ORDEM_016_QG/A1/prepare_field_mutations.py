"""Two surgical mutations of actual contract fields; all other lines preserved."""
from pathlib import Path
import hashlib
import json
root=Path(__file__).resolve().parent
src=root/'v31/ContratoQG_v31.lean'
text=src.read_text(encoding='utf-8')
h2=text[text.index('structure ContratoH2 '):text.index('\nnamespace ContratoH2')]
h3=text[text.index('structure ContratoH3 '):text.index('\nnamespace ContratoH3')]
h2=h2.replace('structure ContratoH2 ', 'structure H2WithoutSmooth ',1)
h3=h3.replace('structure ContratoH3 ', 'structure H3WithoutUnit ',1)
old_s='smooth_on : ∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => E x i j) rightWedge'
old_u='admissible_unit : ∀ ψ ∈ admissible, ‖ψ‖ = 1'
assert h2.count(old_s)==1 and h3.count(old_u)==1
h2=h2.replace(old_s,'smooth_on : True')
h3=h3.replace(old_u,'admissible_unit : True')
header='''import ContratoQG_v31_Minimal

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace ChatgptAudit.FieldMutations
open TGL.SpecificAQFT TGL.ModularRealization TGLExt TGLExt.ContratoQGv31
open Matrix MeasureTheory Set
noncomputable section
'''
proofs=r'''
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
  {N : KillingNormalization}

def roughFrame (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![x 1, x 0, 0, 0; x 0, x 1, 0, 0;
     0, 0, 1 + |x 2|, 0; 0, 0, 0, 1]

theorem roughFrame_det (x : Fin 4 → ℝ) :
    (roughFrame x).det = (x 1 ^ 2 - x 0 ^ 2) * (1 + |x 2|) := by
  have h : Fin.succAbove (1 : Fin 4) (2 : Fin 3) = 3 := by decide
  simp [roughFrame, Matrix.det_succ_row_zero, Fin.sum_univ_succ]
  rw [h]
  simp
  ring

theorem roughFrame_det_unit (x : Fin 4 → ℝ) (hx : x ∈ rightWedge) :
    IsUnit (roughFrame x).det := by
  rw [roughFrame_det]
  have hx' : |x 0| < x 1 := hx
  obtain ⟨h1,h2⟩ := abs_lt.mp hx'
  have hpos : 0 < x 1 ^ 2 - x 0 ^ 2 := by nlinarith
  exact isUnit_iff_ne_zero.mpr (ne_of_gt (mul_pos hpos (by positivity)))

theorem roughFrame_dragged (s : ℝ) (x : Fin 4 → ℝ) :
    roughFrame (wedgeBoostMap s x) = boostMat s * roughFrame x := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [roughFrame, wedgeBoostMap, boostMat, Matrix.mul_apply, Matrix.mulVec,
      dotProduct, Fin.sum_univ_four] <;> ring

theorem roughFrame_fiducial (κ : ℝ) (hκ : 0 < κ) (x : Fin 4 → ℝ) :
    ∃ c : ℝ, 0 < c ∧ (fun i => roughFrame x i 0) = c • killingField κ x := by
  refine ⟨κ⁻¹, inv_pos.mpr hκ, ?_⟩
  funext i
  fin_cases i <;> simp [roughFrame, killingField, Pi.smul_apply, smul_eq_mul,
    ← mul_assoc, inv_mul_cancel₀ hκ.ne']

theorem roughFrame_not_smooth :
    ¬ ∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => roughFrame x i j) rightWedge := by
  intro hs
  let p : Fin 4 → ℝ := ![0,1,0,0]
  have hopen : IsOpen rightWedge :=
    isOpen_lt (continuous_apply 0).abs (continuous_apply 1)
  have hp : p ∈ rightWedge := by change |(0:ℝ)| < 1; norm_num
  have hd : DifferentiableAt ℝ (fun x => roughFrame x 2 2) p :=
    ((hs 2 2).contDiffAt (hopen.mem_nhds hp)).differentiableAt (by simp)
  have hpath : DifferentiableAt ℝ (fun t : ℝ => (![0,1,t,0] : Fin 4 → ℝ)) 0 := by
    fun_prop
  have hcomp := (hd.comp 0 hpath).sub_const 1
  apply not_differentiableAt_abs_zero
  simpa [roughFrame, Function.comp_def] using hcomp

def replaceFrame (C : ContratoH2 W R N) : H2WithoutSmooth W R N where
  kappa := C.kappa
  kappa_pos := C.kappa_pos
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer_unit := C.observer_unit
  E := roughFrame
  smooth_on := True.intro
  det_unit_on := roughFrame_det_unit
  dragged := fun s x _ => roughFrame_dragged s x
  fiducial_is_modular := fun x _ => roughFrame_fiducial C.kappa C.kappa_pos x

theorem zero_modular_energy {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (D : ℝ → (H ≃ₗᵢ[ℂ] H)) (k : ℝ) (hk : HasModularEnergy D 0 k) : k = 0 := by
  have hk' : HasDerivAt (fun _ : ℝ => (0:ℂ)) (-(Complex.I * (k:ℂ))) 0 := by
    simpa [HasModularEnergy] using hk
  have he := hk'.unique (hasDerivAt_const (0:ℝ) (0:ℂ))
  have hc : (k:ℂ) = 0 := by simpa using he
  exact_mod_cast hc

def admitZero {T : StressTensorData W} (C : ContratoH3 W R N T)
    (hT0 : ∀ x, T.T 0 x = 0) (hθ0 : ∀ x, C.theta 0 x = 0) : H3WithoutUnit W R N T where
  H2 := C.H2
  G := C.G
  G_pos := C.G_pos
  admissible := insert 0 C.admissible
  admissible_unit := True.intro
  vac_admissible := mem_insert_of_mem _ C.vac_admissible
  admissible_translate := by
    intro a ψ hψ
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · simp
    · exact mem_insert_of_mem _ (C.admissible_translate a ψ hψ)
  modular_charge := by
    intro ψ hψ k hk
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · rw [zero_modular_energy C.H2.Δit k hk]
      simp [nullPlaneCharge, nullEnergy, pairing, hT0]
    · exact C.modular_charge ψ hψ k hk
  admissible_nontrivial := by
    obtain ⟨ψ,hψ,k,hk,hne⟩ := C.admissible_nontrivial
    exact ⟨ψ,mem_insert_of_mem _ hψ,k,hk,hne⟩
  energy_continuous := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · simp [nullEnergy, pairing, hT0]
    · exact C.energy_continuous ψ hψ x
  background_screen_flat := C.background_screen_flat
  propagator := C.propagator
  propagator_zero := C.propagator_zero
  propagator_covariant := C.propagator_covariant
  response_symm := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · have hz : T.T 0 = 0 := funext hT0
      simp [hz, C.propagator_zero]
    · exact C.response_symm ψ hψ x
  lightcone_gauge := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · have hz : T.T 0 = 0 := funext hT0
      simp [hz, C.propagator_zero]
    · exact C.lightcone_gauge ψ hψ x
  theta := C.theta
  theta_is_expansion := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · have hz : T.T 0 = 0 := funext hT0
      simpa [hz, C.propagator_zero, areaDensity, hθ0] using
        (hasDerivAt_const (0:ℝ) (0:ℝ))
    · exact C.theta_is_expansion ψ hψ x
  raychaudhuri_einstein := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · simpa [hθ0, nullEnergy, pairing, hT0] using
        (hasDerivAt_const (0:ℝ) (0:ℝ))
    · exact C.raychaudhuri_einstein ψ hψ x

theorem admitZero_not_unit {T : StressTensorData W} (C : ContratoH3 W R N T)
    (hT0 : ∀ x, T.T 0 x = 0) (hθ0 : ∀ x, C.theta 0 x = 0) :
    ¬ ∀ ψ ∈ (admitZero C hT0 hθ0).admissible, ‖ψ‖ = 1 := by
  intro h
  have he := h 0 (by simp [admitZero])
  simpa using he

#print axioms roughFrame_det
#print axioms roughFrame_det_unit
#print axioms roughFrame_dragged
#print axioms roughFrame_fiducial
#print axioms roughFrame_not_smooth
#print axioms replaceFrame
#print axioms zero_modular_energy
#print axioms admitZero
#print axioms admitZero_not_unit
end
end ChatgptAudit.FieldMutations
'''
raw=(header+'\n'+h2+'\n'+h3+'\n'+proofs).encode()
out=root/'probes/ProbeFieldMutations.lean'
assert not out.exists()
tmp=out.with_suffix('.lean.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw
tmp.rename(out)
receipt={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
         'generated_sha256':hashlib.sha256(raw).hexdigest(),
         'mutations':{'H2WithoutSmooth':old_s+' -> smooth_on : True',
                      'H3WithoutUnit':old_u+' -> admissible_unit : True'},
         'scope':'Conditional controls. All other structure lines retained, only structure names renamed.'}
out=root/'probes/field_mutation_preparation.json'
tmp=out.with_suffix('.json.tmp')
content=(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode()
assert not out.exists()
with tmp.open('xb') as f:f.write(content)
assert tmp.read_bytes()==content
tmp.rename(out)
print(json.dumps(receipt,ensure_ascii=False))
