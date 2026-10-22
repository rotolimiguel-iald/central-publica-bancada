import EmptyImportControl
set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.EmptyIndexRejected016
open TGLExt.ContratoQGv31 TGL.SpecificAQFT TGL.ModularRealization
open ChatgptAudit.EmptyImport016
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
variable {N : KillingNormalization}

/-- EXPECTED FAILURE: original v3.1 index attack, in generalized form.
No H2 witness is supplied; ex falso inside produce cannot fill the index. -/
def vacuousImport (T : StressTensorData W) (hu : W.U nullDir = 1) :
    ContratoImportH3 W R N T (Classical.choice ⟨_⟩) where
  produce := fun h => absurd (h.translations_faithful nullDir hu) nullDir_ne_zero
  same_horizon := fun h => absurd (h.translations_faithful nullDir hu) nullDir_ne_zero
end ChatgptAudit.EmptyIndexRejected016
