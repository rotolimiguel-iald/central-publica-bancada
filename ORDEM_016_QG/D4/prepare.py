"""Retype isolated dependency copies; preserve original names only in provenance."""
from pathlib import Path
from datetime import datetime,timezone
import sys,re,json
R=Path(__file__).resolve().parents[1];D=R/'D4'
CAN=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha
now=datetime.now(timezone.utc);sources={}
def read(rel):
 p=CAN/rel;sources[rel]=dict(path=str(p),sha256=sha(p));return p.read_text('utf-8-sig')
def head(rel):return '-- ORDEM016 D4: isolated retyped copy, not a photon-network inhabitant.\n-- Source SHA256: '+sources[rel]['sha256']+'\n'
def ns(s):return s.replace('TGL.SpecificAQFT','ORDEM016.Photon.SpecificAQFT').replace('TGL.ModularRealization','ORDEM016.Photon.ModularRealization')
s=read('TGL/SpecificAQFTWitness.lean')
assert s.count('  m_pos : 0 < m')==1
sp=ns(s).replace('  m_pos : 0 < m','  helicity : ℤ\n  peso_do_nome : 0 < m ∨ helicity ≠ 0')
write(D/'PhotonWitness.lean',(head('TGL/SpecificAQFTWitness.lean')+sp).encode())
s=read('TGL/ModularRealization.lean');mod=s
s=s.replace('import TGL.SpecificAQFTWitness','import PhotonWitness');s=ns(s)
write(D/'PhotonModularRealization.lean',(head('TGL/ModularRealization.lean')+s).encode())
# Exact fieldwise transport of existing MASSIVE witnesses, solely to preserve legacy
# controls when recompiling the contract. This does not construct a massless witness.
oldw=read('TGL/SpecificAQFTWitness.lean')
def fields(src,name):
 block=src.split('structure '+name,1)[1].split('\nattribute ',1)[0]
 block=re.split(r'\n(?:structure|/--)',block)[0] if False else block
 # Stop at the next top-level declaration; comments do not carry fields at column two.
 block=re.split(r'\n(?:structure |attribute |theorem |def |abbrev )',block)[0]
 return re.findall(r'^  (?:\[)?([A-Za-z][A-Za-z0-9_]*)\s*:',block,re.M)
wf=fields(oldw,'TGLSpecificAQFTWitness')
assert 'm_pos' in wf and len(wf)>=20,wf
text='''import PhotonModularRealization
import TGLExt.V354RegularLegacyWitness

set_option autoImplicit false
noncomputable section
namespace ORDEM016.Photon.Transport
def liftW (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) :
    ORDEM016.Photon.SpecificAQFT.TGLSpecificAQFTWitness where
'''
for f in wf:
 text+=('  helicity := 0\n  peso_do_nome := Or.inl W.m_pos\n' if f=='m_pos' else f'  {f} := W.{f}\n')
text+='\n'
for name,out,old,typ in [
 ('WedgeModularData','liftD','d','(W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (d : TGL.ModularRealization.WedgeModularData W) : ORDEM016.Photon.ModularRealization.WedgeModularData (liftW W)'),
 ('ContinuousCoreData','liftC','c','(W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (d : TGL.ModularRealization.WedgeModularData W) (c : TGL.ModularRealization.ContinuousCoreData W d) : ORDEM016.Photon.ModularRealization.ContinuousCoreData (liftW W) (liftD W d)'),
 ('ThreeLocksCoreData','liftL','l','(W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (d : TGL.ModularRealization.WedgeModularData W) (c : TGL.ModularRealization.ContinuousCoreData W d) (l : TGL.ModularRealization.ThreeLocksCoreData W d c) : ORDEM016.Photon.ModularRealization.ThreeLocksCoreData (liftW W) (liftD W d) (liftC W d c)')]:
 fs=fields(mod,name);assert len(fs)>5,(name,fs)
 text+=f'def {out} {typ} where\n'+''.join(f'  {f} := {old}.{f}\n' for f in fs)+'\n'
text+='''def liftR (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (R : TGL.ModularRealization.TGLModularRealization W) :
    ORDEM016.Photon.ModularRealization.TGLModularRealization (liftW W) where
  infiniteHilbert := R.infiniteHilbert
  modular := liftD W R.modular
  core := liftC W R.modular R.core
  threeLocks := liftL W R.modular R.core R.threeLocks
def legacyW := liftW TGLExt.theSpecificAQFTWitness
def legacyR := liftR TGLExt.theSpecificAQFTWitness TGLV354.TraceCompletion.regularModularRealization
#print axioms liftW
#print axioms liftD
#print axioms liftC
#print axioms liftL
#print axioms liftR
end ORDEM016.Photon.Transport
'''
write(D/'PhotonMassiveTransport.lean',text.encode())
s=read('TGLExt/ContratoQG_v31.lean')
s='import PhotonMassiveTransport\n'+s
s=ns(s).replace('TGLExt.ContratoQGv31','ORDEM016.Photon.Contract')
write(D/'PhotonContract.lean',(head('TGLExt/ContratoQG_v31.lean')+s).encode())
s=read('TGLExt/ContratoQG_v31_Teoremas.lean')
s=s.replace('import TGLExt.ContratoQG_v31','import PhotonContract')
s=ns(s).replace('TGLExt.ContratoQGv31','ORDEM016.Photon.Contract')
s=s.replace('theSpecificAQFTWitness','ORDEM016.Photon.Transport.legacyW').replace('regularModularRealization','ORDEM016.Photon.Transport.legacyR')
write(D/'PhotonContractTheorems.lean',(head('TGLExt/ContratoQG_v31_Teoremas.lean')+s).encode())
save(D/'START.json',dict(at=now.isoformat(),timebox_hours=6,scope='D4 dependency copies, old massive witnesses lifted only for legacy controls, no photon existence asserted'))
save(D/'COPY_MANIFEST.json',dict(at=now.isoformat(),sources=sources,copies={p.name:sha(p) for p in D.glob('*.lean')},witness_fields=wf,theorem_print_count=len(re.findall(r'^#print axioms',s,re.M)),modifications=['rename isolated dependency namespaces','replace m_pos field with helicity integer and peso_do_nome disjunction','lift old massive witnesses fieldwise for three legacy controls','retarget contract/theorem imports, no theorem proof edits']))
print(json.dumps(dict(copies=len(list(D.glob('*.lean'))),theorem_print_count=len(re.findall(r'^#print axioms',s,re.M)),witness_fields=len(wf))))
