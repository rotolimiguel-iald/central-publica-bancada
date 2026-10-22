from pathlib import Path
import hashlib,json,re

HERE=Path(__file__).resolve().parent
SRC=HERE.parents[1]/'TUNEL/PARA_CHATGPT/ORDEM_016_INSUMOS/A1_CONTRATO_V3/v31/ContratoQG_v31_Teoremas.lean'
raw=SRC.read_bytes();text=raw.decode('utf-8-sig')
records=[]
def extract(name):
    hit=re.search(r'^(?:theorem|def) '+re.escape(name)+r'\b',text,re.M)
    assert hit,name
    end=text.index('\n/--',hit.start())
    namespace_end=text.find('\nend ',hit.start(),end)
    if namespace_end != -1:end=namespace_end
    block=text[hit.start():end].strip()
    assert '\nend ' not in block
    records.append(dict(name=name,start_line=text[:hit.start()].count('\n')+1,
        end_line=text[:end].count('\n'),block_sha256=hashlib.sha256(block.encode()).hexdigest()))
    return block+'\n\n'

target=HERE/'HorizonDataReuse.lean'
assert not target.exists(),'Do not overwrite a cited proof source'
code='''import ContratoQG_v31_Minimal
import TGLExt.TriadMaster
import PolarMinimalPeriod_v2

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace TGLExt.ContratoQGv31
open TGL.SpecificAQFT TGL.ModularRealization
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace

'''+extract('shift_point')+'''namespace ContratoH3
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
  {N : KillingNormalization} {T : StressTensorData W}

'''
names=['theta_along','theta_deriv_along','first_law_window','bekenstein_hawking_window',
       'clausius_window','einstein_coefficient_window','toHorizonData','feeds_the_master']
code+=''.join(extract(name) for name in names)
code+='''/-- The exported data uses exactly this H3 contract's H2 horizon. -/
theorem data_fields_same_horizon (C : ContratoH3 W R N T)
    {psi : W.H} (hpsi : psi ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d : ℝ) (htheta : C.theta psi (x+d • nullDir)=0) :
    (C.toHorizonData hpsi x c d htheta).kappa=C.H2.kappa ∧
    (C.toHorizonData hpsi x c d htheta).G=C.G ∧
    (C.toHorizonData hpsi x c d htheta).dS=2*Real.pi*windowCharge T psi x c d :=
  ⟨rfl,rfl,rfl⟩

theorem data_temperature_from_same_period (C : ContratoH3 W R N T)
    {psi : W.H} (hpsi : psi ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d period : ℝ) (htheta : C.theta psi (x+d • nullDir)=0)
    (hp : 0 < period)
    (hperiod : ChatgptAudit.PolarPeriod016.AngularQuotientFaithful C.H2.kappa period) :
    (C.toHorizonData hpsi x c d htheta).kappa/(2*Real.pi)=1/period :=
  (ChatgptAudit.PolarPeriod016.reciprocal_temperature C.H2.kappa_pos hp hperiod).symm

'''
for name in names+['data_fields_same_horizon','data_temperature_from_same_period']:
    code+=f'#print axioms {name}\n'
code+='end ContratoH3\n#print axioms shift_point\nend TGLExt.ContratoQGv31\n'
temp=target.with_suffix('.lean.tmp')
with temp.open('xb') as f:f.write(code.encode())
assert temp.stat().st_size>0
temp.replace(target)
receipt=dict(source=str(SRC),source_sha256=hashlib.sha256(raw).hexdigest(),reused=records,
             target=str(target),target_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
             note='Bodies and declarations reused exactly; added two explicit field/period compositions. No H3 inhabitant constructed.')
out=HERE/'horizon_reuse_source.json'
assert not out.exists()
with out.open('xb') as f:f.write(json.dumps(receipt,ensure_ascii=False,indent=2).encode())
print(json.dumps(dict(reused=len(records),target=str(target))))
