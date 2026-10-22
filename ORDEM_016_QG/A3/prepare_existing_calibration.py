"""Extract existing calibration proofs unchanged, then compose geometric suppliers."""
from pathlib import Path
import hashlib, json

HERE = Path(__file__).resolve().parent
source = HERE.parent/'A1/v31/ContratoQG_v31_Teoremas.lean'
raw = source.read_bytes()
text = raw.decode('utf-8-sig')
first = text[text.index('def refRadius ('):text.index('/-- [DERIVED] κ·ρ(N)')]
second = text[text.index('theorem observer_unit_of_index ('):text.index('/-- ★ RE-INDEXAR:')]
prefix = '''import WedgeDraggedFrame_v6

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.WignerGeometry016.ExistingCalibration
open TGLExt TGLExt.ContratoQGv31 TGL.SpecificAQFT Matrix

/- Existing proofs copied unchanged from ContratoQG_v31_Teoremas.
Only the namespace/import context changes for isolated compilation.
This is reuse, not a new derivation of the calibration. -/
'''
tail = '''
/-- The geometric fields are assembled from existing suppliers for any supplied N. -/
theorem geometric_fields_reused (N : KillingNormalization) :
    0 < 1 / refRadius N ∧
    minkowskiSq (killingField (1 / refRadius N) N.point) = 1 ∧
    (∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => wedgeFrame x i j) rightWedge) ∧
    (∀ x ∈ rightWedge, IsUnit (wedgeFrame x).det) ∧
    (∀ s x, x ∈ rightWedge →
      wedgeFrame (wedgeBoostMap s x) = boostMat s * wedgeFrame x) ∧
    (∀ x ∈ rightWedge, ∃ c : ℝ, 0 < c ∧
      (fun i => wedgeFrame x i 0) = c • killingField (1 / refRadius N) x) := by
  have hk : 0 < 1 / refRadius N := one_div_pos.mpr (refRadius_pos N)
  exact ⟨hk, observer_unit_of_index N,
    fun i j => (wedgeFrame_smooth i j).contDiffOn,
    wedgeFrame_det_unit, fun s x _ => wedgeFrame_dragged s x,
    fun x _ => wedgeFrame_fiducial _ hk x⟩

#print axioms refRadius_pos
#print axioms observer_unit_of_index
#print axioms geometric_fields_reused
end ChatgptAudit.WignerGeometry016.ExistingCalibration
'''
def create(path, data):
    assert not path.exists(), path
    tmp = path.with_name(path.name+'.tmp')
    with tmp.open('xb') as f: f.write(data)
    assert tmp.read_bytes() == data
    tmp.rename(path)

out = HERE/'ExistingKillingCalibration.lean'
create(out, (prefix+first+second+tail).encode())
metadata = dict(source=str(source), source_sha256=hashlib.sha256(raw).hexdigest(),
                output=str(out), output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                copied_declarations=['refRadius','refRadius_pos','observer_unit_of_index'],
                new_composition=['geometric_fields_reused'],
                status='SOURCE_EXTRACTED_NOT_YET_COMPILED')
create(HERE/'existing_calibration_provenance.json',json.dumps(metadata,ensure_ascii=False,indent=2).encode())
print(json.dumps(metadata,ensure_ascii=False))
