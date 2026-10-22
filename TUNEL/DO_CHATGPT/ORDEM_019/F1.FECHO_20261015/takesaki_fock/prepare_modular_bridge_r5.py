"""Preserve R4 and produce an explicit-type R5 candidate; no compilation claim."""
from pathlib import Path
import re, hashlib, json
B=Path(__file__).resolve().parent
old=B/'CanonicalFockModularBridgeR4.lean'
s=old.read_text(encoding='utf-8')
blocks=re.findall(r'-- BEGIN EXACT BODY (\w+)\n(.*?)\n-- END EXACT BODY \1',s,re.S)
names={
 'CanonicalFockWeightPolarBasicsR3':'CanonicalFockWeightPolarBasicsR4',
 'CanonicalFockCoefficientFlowR15':'CanonicalFockCoefficientFlowR16',
 'CanonicalFockCoefficientGraphEqualityR11':'CanonicalFockCoefficientGraphEqualityR12',
 'CanonicalFockModularIdentificationR11':'CanonicalFockModularIdentificationR12',
 'CanonicalFockWeightPolarR5':'CanonicalFockWeightPolarR6',
}
out=[]
def replace_once(s,a,b):
 assert s.count(a)==1,(a,s.count(a))
 return s.replace(a,b)
for name,body in blocks:
 new=names.get(name,name)
 if name=='CanonicalFockWeightPolarBasicsR3':
  for api in ('conjugate','on_unitary','involutive'):
   body=body.replace('UnitaryAntiunitaryTransport.'+api+' coefficientUnitary',
    'UnitaryAntiunitaryTransport.'+api+' (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary')
 if name=='CanonicalFockCoefficientFlowR15':
  body=replace_once(body,'  rw [CoefficientFockConjugation.coefficient_modular_flow]\n  exact intertwines t f',
    '  have he := CoefficientFockConjugation.coefficient_modular_flow t f\n  exact (congrArg coefficientEmbedding he).trans (intertwines t f)')
  body=replace_once(body,
   '  exact Eq.mpr (congrArg (fun p=>p∈RegularScalarRealGraph.closedGraph weightContext) he)\n    (conjugate_closed_graph t _ ((coefficientGraph_mem f g).mp hfg))',
   '''  have hp := conjugate_closed_graph t (coefficientEmbedding f,coefficientEmbedding g)
    ((coefficientGraph_mem f g).mp hfg)
  change (regularConjugationGNS t (coefficientEmbedding f),
    regularConjugationGNS t (coefficientEmbedding g))∈
      RegularScalarRealGraph.closedGraph weightContext at hp
  exact Eq.mpr (congrArg (fun p:GNSHilbert×GNSHilbert=>
    p∈RegularScalarRealGraph.closedGraph weightContext) he) hp''')
 if name=='CanonicalFockCoefficientGraphEqualityR11':
  body=replace_once(body,'  simpa only [coefficientJ_involutive] using hy',
    '''  rw [coefficientJ_involutive y]
  change (coefficientAverage n x,y)∈(resolventSquareRoot coefficientR hR hi).graph
  exact hy''')
 if name=='CanonicalFockModularIdentificationR11':
  start=body.index(' theorem unitary_graph :')
  end=body.index(' theorem source_resolvent_mem',start)
  body=body[:start]+''' theorem target_graph_mem_iff (x y:GNSHilbert) :
    (x,y)∈ClosedTomitaSquareGraph.graph actualClosedInput ↔
      (x,y)∈RegularScalarRealGraph.closedGraph weightContext :=
  Iff.of_eq (congrArg (fun S:Set (GNSHilbert×GNSHilbert)=>(x,y)∈S) target_graph_eq)

 theorem unitary_graph :
    (coefficientUnitary.toHomeomorph.prodCongr coefficientUnitary.toHomeomorph) ''
      CoefficientTomitaSquare.graph coefficientRoot coefficientJ=
        ClosedTomitaSquareGraph.graph actualClosedInput := by
  apply Set.ext
  intro p
  constructor
  · rintro ⟨q,hq,rfl⟩
    apply (target_graph_mem_iff (coefficientUnitary q.1) (coefficientUnitary q.2)).mpr
    exact coefficient_graph_into_GNS q.1 q.2 hq
  · intro hp
    obtain ⟨x,hx⟩:=coefficientUnitary.surjective p.1
    obtain ⟨y,hy⟩:=coefficientUnitary.surjective p.2
    have he:(coefficientUnitary.toHomeomorph.prodCongr coefficientUnitary.toHomeomorph) (x,y)=p :=
      Prod.ext hx hy
    refine ⟨(x,y),?_,he⟩
    apply Eq.mpr (congrArg (fun S:Set (RegularHilbert F×RegularHilbert F)=>(x,y)∈S)
      coefficient_graph_eq_GNS)
    apply (coefficientGraph_mem x y).mpr
    have hpt := (target_graph_mem_iff p.1 p.2).mp hp
    exact Eq.mpr (congrArg (fun p:GNSHilbert×GNSHilbert=>
      p∈RegularScalarRealGraph.closedGraph weightContext) he) hpt

'''+body[end:]
  body=replace_once(body,'  rw [resolvent_graph_equation]',
   '  apply (resolvent_graph_equation (H := RegularHilbert F) coefficientR hi\n    (coefficientR x) (x-coefficientR x)).mpr')
  body=body.replace('unitary_recognizes_square_resolvent coefficientUnitary',
   'unitary_recognizes_square_resolvent (H := RegularHilbert F) (K := GNSHilbert) coefficientUnitary')
  body=body.replace('SpectralTransport.transported coefficientUnitary',
   'SpectralTransport.transported (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary')
  body=body.replace('SpectralTransport.imaginaryPower coefficientUnitary',
   'SpectralTransport.imaginaryPower (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary')
 if name=='CanonicalFockWeightPolarR5':
  body=body.replace('UnitaryRootGraphTransport.root_graph_iff coefficientUnitary',
   'UnitaryRootGraphTransport.root_graph_iff (H := RegularHilbert F) (E := GNSHilbert) coefficientUnitary')
 if name in ('CanonicalFockModularIdentificationR11','CanonicalFockWeightPolarR5'):
  body=re.sub(r'(?<![\w.])scalarTomitaResolvent\b',
    'CanonicalFockWeightModularOperator.scalarTomitaResolvent',body)
 out.append((new,body))
 # Each body is separately custodied as a component, not imported on its own.
 if new!=name:
  p=B/(new+'_body.txt')
  with p.open('x',encoding='utf-8',newline='\n') as f:f.write(body+'\n')
header=s[:s.index('-- BEGIN EXACT BODY')]
result=header+'\n'.join('-- BEGIN EXACT BODY '+n+'\n'+b+'\n-- END EXACT BODY '+n+'\n' for n,b in out)
dest=B/'CanonicalFockModularBridgeR5.lean'
with dest.open('x',encoding='utf-8',newline='\n') as f:f.write(result)
pin=lambda p:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
receipt=dict(status='PREPARED_NOT_COMPILED',baseline=pin(old),candidate=pin(dest),
 components=[pin(B/(n+'_body.txt')) for n,_ in out if n in names.values()],
 corrections=['Explicit Hilbert source and target before instantiating unitary transport',
 'Typed membership equivalences instead of rewriting expanded graph carriers',
 'Explicit antiunitary involution and independently constructed root identity',
 'Fully qualified actual weight resolvent, avoiding scalar profile homonym'])
with (B/'MODULAR_BRIDGE_ASSEMBLY_R5.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
print(json.dumps(receipt['candidate'],ensure_ascii=False))
