import ContratoQG_v31_Minimal
import ExactTypeReader_v2
set_option autoImplicit false
namespace ChatgptAudit.GateProposal016
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31

/- Conditional transport only. This is deliberately NOT a closed physical witness.
The exact reader may check the arrow as an arrow, but not discard its arguments. -/
def conditionalH2 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (h : ContratoH2 W R N) : ContratoH2 W R N := h

#assert_exact_type conditionalH2 : (W : TGLSpecificAQFTWitness) →
    (R : TGLModularRealization W) → (N : KillingNormalization) →
    ContratoH2 W R N → ContratoH2 W R N

def conditionalImport (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (T : StressTensorData W) (h : ContratoH2 W R N)
    (f : ContratoImportH3 W R N T h) : ContratoH3 W R N T := f.produce h

theorem conditionalImport_sameHorizon
    (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (T : StressTensorData W) (h : ContratoH2 W R N)
    (f : ContratoImportH3 W R N T h) : (conditionalImport W R N T h f).H2 = h :=
  f.same_horizon h

#print axioms conditionalH2
#print axioms conditionalImport
#print axioms conditionalImport_sameHorizon
end ChatgptAudit.GateProposal016
