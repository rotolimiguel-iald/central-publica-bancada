"""Preserve R5 and consume the explicit-type probe; never overwrite attempts."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
p=B/'CanonicalFockModularBridgeR5.lean';s=p.read_text(encoding='utf-8')
def repl(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a))
 s=s.replace(a,b)
repl('''    scalarTomitaPolarFactor (coefficientUnitary x) = coefficientUnitary (coefficientJ x) :=
  UnitaryAntiunitaryTransport.on_unitary (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary coefficientJ x''',
'''    scalarTomitaPolarFactor (coefficientUnitary x) = coefficientUnitary (coefficientJ x) := by
  change coefficientUnitary (coefficientJ (coefficientUnitary.symm (coefficientUnitary x)))=
    coefficientUnitary (coefficientJ x)
  exact congrArg (fun v:RegularHilbert F=>coefficientUnitary (coefficientJ v))
    (coefficientUnitary.symm_apply_apply x)''')
repl('''theorem scalarTomitaPolarFactor_involutive : Function.Involutive scalarTomitaPolarFactor :=
  UnitaryAntiunitaryTransport.involutive (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary coefficientJ coefficientJ_involutive''',
'''theorem scalarTomitaPolarFactor_involutive : Function.Involutive scalarTomitaPolarFactor := by
  intro x
  change coefficientUnitary (coefficientJ (coefficientUnitary.symm
    (coefficientUnitary (coefficientJ (coefficientUnitary.symm x)))))=x
  calc
    _=coefficientUnitary (coefficientJ (coefficientJ (coefficientUnitary.symm x))):=
      congrArg (fun v:RegularHilbert F=>coefficientUnitary (coefficientJ v))
        (coefficientUnitary.symm_apply_apply (coefficientJ (coefficientUnitary.symm x)))
    _=coefficientUnitary (coefficientUnitary.symm x):=
      congrArg coefficientUnitary (coefficientJ_involutive (coefficientUnitary.symm x))
    _=x:=coefficientUnitary.apply_symm_apply x''')
repl('''  obtain ⟨x,rfl⟩:=coefficientUnitary.surjective y
  exact (imaginary_intertwines t x).symm.trans (cfc_intertwines t x)''',
'''  calc
    _=scalarTomitaImaginaryPower t (coefficientUnitary (coefficientUnitary.symm y)):=
      congrArg (fun z:GNSHilbert=>scalarTomitaImaginaryPower t z)
        (coefficientUnitary.apply_symm_apply y).symm
    _=coefficientUnitary (FibreModularCalculus.liftedFlow
        CanonicalFockPolar.modularR CanonicalFockPolar.modularR_nonneg CanonicalFockPolar.modularR_le_one
        CanonicalFockPolar.modularR_injective CanonicalFockPolar.modularR_complement_injective
        t (coefficientUnitary.symm y)):=
      (imaginary_intertwines t (coefficientUnitary.symm y)).symm
    _=regularConjugationGNS t (coefficientUnitary (coefficientUnitary.symm y)):=
      cfc_intertwines t (coefficientUnitary.symm y)
    _=regularConjugationGNS t y:=congrArg (regularConjugationGNS t)
      (coefficientUnitary.apply_symm_apply y)''')
repl('''  rw [←actual_modular_implementation]
  exact (scalarTomitaImaginaryPower t).norm_map y''',
'''  exact (congrArg norm (actual_modular_implementation t y)).symm.trans
    ((scalarTomitaImaginaryPower t).norm_map y)''')
repl('''  simp only [←actual_modular_implementation]
  exact scalarTomitaImaginaryPower_add s t y''',
'''  calc
    _=scalarTomitaImaginaryPower s (regularConjugationGNS t y):=
      (actual_modular_implementation s (regularConjugationGNS t y)).symm
    _=scalarTomitaImaginaryPower s (scalarTomitaImaginaryPower t y):=
      congrArg (fun z:GNSHilbert=>scalarTomitaImaginaryPower s z)
        (actual_modular_implementation t y).symm
    _=scalarTomitaImaginaryPower (s+t) y:=scalarTomitaImaginaryPower_add s t y
    _=regularConjugationGNS (s+t) y:=actual_modular_implementation (s+t) y''')
# The statement bodies are still explicit proof terms; fail early on a material elaboration error.
s=s.replace('-- BEGIN EXACT BODY','-- BEGIN DERIVED BODY').replace('-- END EXACT BODY','-- END DERIVED BODY')
s=s.replace('set_option autoImplicit false','set_option autoImplicit false\nset_option maxErrors 3',1)
dest=B/'CanonicalFockModularBridgeR6.lean'
with dest.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
pin=lambda q:dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),bytes=q.stat().st_size)
r=dict(status='PREPARED_NOT_COMPILED',baseline=pin(p),candidate=pin(dest),
 probe=pin(B/'attempts/20261016T033535_761139Z/RECEIPT.json'),
 note='Probe accepted definitions with explicit H/E; generic involution application timed out. R6 uses pointwise proof and avoids graph-wide rewrites.')
with (B/'MODULAR_BRIDGE_ASSEMBLY_R6.json').open('x',encoding='utf-8') as f:json.dump(r,f,ensure_ascii=False,indent=2)
print(json.dumps(r['candidate'],ensure_ascii=False))
