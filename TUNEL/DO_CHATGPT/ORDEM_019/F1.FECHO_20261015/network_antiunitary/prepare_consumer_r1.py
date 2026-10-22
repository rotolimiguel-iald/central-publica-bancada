from pathlib import Path
import re,os
b=Path(__file__).resolve().parent
old=(b.parent/'network_reuse/CanonicalFockAssemblyR1.lean').read_text(encoding='utf8')
rest=old[old.index('  /-- a condição espectral'):old.index('\nattribute [instance] RemainingFockInput.instCR')]
rest=re.sub(r'^  J :.*\n','',rest,flags=re.M)
rest=re.sub(r'^  J_invol :.*\n','',rest,flags=re.M)
rest=re.sub(r'^  J_vac :.*\n','',rest,flags=re.M)
rest=re.sub(r'(?<![\w])J(?![\w])','canonicalFockJ',rest)
fields=re.findall(r'^  ([\w]+)\s*:',rest,re.M)
instances=re.findall(r'^  \[([\w]+)\s*:',rest,re.M)
s='''import BosonicGammaJR2
import CanonicalFockAssemblyR1

/-! The three antiunitary fields are now paid by the concrete Gamma(Jcandidate).
The remaining analytic fields stay explicit; this is not an inhabitant of the
whole FockCertificate, nor a Tomita/KMS identification from kinematics alone. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.Antilinear
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ImportedSQ
open F1Rede.BosonicFock F1Fecho.NetworkReuse

structure RemainingAnalyticInput (L : LightOneParticle) where
'''+rest+'\n'
s+='attribute [instance] '+' '.join('RemainingAnalyticInput.'+n for n in instances)+'\n\n'
s+='''def RemainingAnalyticInput.toRemainingFock {L : LightOneParticle}
    (A : RemainingAnalyticInput L) : RemainingFockInput L where
  J := canonicalFockJ
  J_invol := canonicalFockJ_involutive
  J_vac := canonicalFockJ_vacuum
'''
s+=''.join(f'  {n} := A.{n}\n' for n in fields+instances)
s+='''
def RemainingAnalyticInput.toCertificate {L : LightOneParticle}
    (A : RemainingAnalyticInput L) : FockCertificate L := A.toRemainingFock.toCertificate

theorem assembled_J_is_concrete {L : LightOneParticle} (A : RemainingAnalyticInput L) :
    A.toCertificate.J = canonicalFockJ := rfl
theorem assembled_J_on_oneParticle {L : LightOneParticle} (A : RemainingAnalyticInput L)
    (x : H1) : A.toCertificate.J (A.toCertificate.ι x) =
      A.toCertificate.ι (F1Rede.CanonicalWedge.Jcandidate x) :=
  canonicalFockJ_oneParticle x
theorem assembled_J_involutive {L : LightOneParticle} (A : RemainingAnalyticInput L) :
    Function.Involutive A.toCertificate.J := canonicalFockJ_involutive
theorem assembled_J_preserves_existing_vacuum {L : LightOneParticle}
    (A : RemainingAnalyticInput L) : A.toCertificate.J vacuum = vacuum := canonicalFockJ_vacuum

/-- Actual inhabitant of the antiunitary fragment, independent of the remaining
analytic input record. It acts on exactly F1Rede.BosonicFock.F. -/
theorem antiunitary_fragment_inhabited :
    ∃ j : F ≃ₛₗᵢ[starRingEnd ℂ] F,
      Function.Involutive j ∧ j vacuum = vacuum ∧
      (∀ x : H1, j (oneParticle x) = oneParticle (F1Rede.CanonicalWedge.Jcandidate x)) :=
  ⟨canonicalFockJ,canonicalFockJ_involutive,canonicalFockJ_vacuum,canonicalFockJ_oneParticle⟩

end F1Fecho.Antilinear

#print axioms F1Fecho.Antilinear.RemainingAnalyticInput.toCertificate
#print axioms F1Fecho.Antilinear.assembled_J_is_concrete
#print axioms F1Fecho.Antilinear.assembled_J_on_oneParticle
#print axioms F1Fecho.Antilinear.assembled_J_involutive
#print axioms F1Fecho.Antilinear.assembled_J_preserves_existing_vacuum
#print axioms F1Fecho.Antilinear.antiunitary_fragment_inhabited
'''
with (b/'CanonicalFockAntiAssemblyR1.lean').open('x',encoding='utf8') as f:f.write(s);f.flush();os.fsync(f.fileno())
print('Remaining fields:',len(fields)+len(instances))
