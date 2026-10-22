import ClosedIndexChecks_v2
set_option autoImplicit false
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
/- This attempted promotion must fail at the actual H2 contract: the last H2
input is being removed. No physical pair is selected by this test. -/
#check (ChatgptAudit.GateProposal016.conditionalH2 :
    (W : TGLSpecificAQFTWitness) → (R : TGLModularRealization W) →
    (N : KillingNormalization) → ContratoH2 W R N)
