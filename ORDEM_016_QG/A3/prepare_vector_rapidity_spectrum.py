"""Generalize the existing scalar rapidity proof to arbitrary complex normed fibers."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
src=ROOT.parent/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A2_A3_RETA_DE_LUZ/lean/RetaDeLuzEspectro.lean'
raw=src.read_bytes(); text=raw.decode()
proof=text[text.index('theorem D_no_eigen'):text.index('/-- [DERIVED] corolario:')]
proof=proof.replace('D_no_eigen','rapidityShift_no_eigen').replace('L2R','Lp E 2 (volume : Measure ℝ)')
proof=proof.replace('D s f','rapidityShift s f').replace('D_ae','rapidityShift_ae')
proof=proof.replace('Pi.smul_apply, smul_eq_mul, enorm_mul','Pi.smul_apply, enorm_smul')
proof=proof.replace('Lp.coeFn_zero ℂ 2','Lp.coeFn_zero E 2')
prefix='''import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.Haar.Unique
import Mathlib.MeasureTheory.Group.Measure
import Mathlib.Algebra.Order.Interval.Set.Group
import Mathlib.Algebra.Order.ToIntervalMod
import Mathlib.MeasureTheory.Group.LIntegral
import Mathlib.Tactic

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal
namespace ChatgptAudit.WignerRapidity016
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

/- Adaptation of RetaDeLuzEspectro.D_no_eigen to arbitrary fibers E.
This does not itself identify the invariant orbit measure with rapidity measure. -/
def rapidityShift (s : ℝ) :
    Lp E 2 (volume : Measure ℝ) →ₗᵢ[ℂ] Lp E 2 (volume : Measure ℝ) :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun x : ℝ => x + -s)
    (measurePreserving_add_right volume (-s))

theorem rapidityShift_ae (s : ℝ) (f : Lp E 2 (volume : Measure ℝ)) :
    rapidityShift s f =ᵐ[volume] fun x => f (x + -s) :=
  Lp.coeFn_compMeasurePreserving f (measurePreserving_add_right volume (-s))

'''
tail='''
#print axioms rapidityShift_ae
#print axioms rapidityShift_no_eigen
end ChatgptAudit.WignerRapidity016
'''
out=HERE/'VectorRapiditySpectrum.lean'
assert not out.exists()
with out.open('xb') as f:f.write((prefix+proof+tail).encode())
meta=dict(source=str(src),source_sha256=hashlib.sha256(raw).hexdigest(),
          output=str(out),output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
          modifications=['scalar complex values generalized to normed complex fiber E',
                         'multiplication norm changed to scalar-action norm',
                         'local namespace and explicit measure-preserving shift'],
          status='DRAFT_NOT_COMPILED')
with (HERE/'vector_rapidity_provenance.json').open('xb') as f:
    f.write(json.dumps(meta,ensure_ascii=False,indent=2).encode())
print(json.dumps(meta,ensure_ascii=False))
