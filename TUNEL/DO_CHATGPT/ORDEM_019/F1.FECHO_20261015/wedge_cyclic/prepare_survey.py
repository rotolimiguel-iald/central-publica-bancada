from pathlib import Path
import hashlib,json,datetime
b=Path(__file__).resolve().parent
k=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
refs=[(b.parent/'wedge_exponential/RealSubspaceTotalityR4.lean',['standard_exponential_total','standard_complex_span_dense']), (b.parent/'weyl_net_wiring/FieldWeylR3.lean',['W_vacuum','R_local','W_mem_R']), (k/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/StandardSubspace.lean',['lemma mem_symplComp_iff','noncomputable def symplComp']), (k/'.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean',['theorem ext_on']), (k/'TGLExt/TheImportedSecondQuantization.lean',['wedge_cyclic :','wedge_separating :'])]
entries=[]
for p,needles in refs:
    raw=p.read_bytes();lines=raw.decode('utf8').splitlines()
    anchors=[{'needle':needle,'lines':[i+1 for i,s in enumerate(lines) if needle in s]} for needle in needles]
    assert all(x['lines'] for x in anchors)
    entries.append(dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),anchors=anchors))
d=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit='F1.FECHO_20261015',claim=845,statute='DERIVED_PLAN_FROM_READ_SOURCES',sources=entries,plan=['Use exp(iK) total, since K.mulI is standard.','W(k) vacuum is a nonzero scalar times exp(i k). Thus the vacuum orbit spans densely.','The symplectic complement is standard and its algebra commutes with R(K).','An a in R(K) that kills vacuum kills the dense commutant orbit, hence a=0 by CLM.ext_on.'],scope='Same Fock, field convention W(f)=D(i f), no assumed algebra cyclicity or separating property, no Tomita identification.')
raw=json.dumps(d,ensure_ascii=False,indent=2).encode('utf8')
with (b/'WEDGE_CYCLIC_SURVEY_R1.json').open('xb') as f:f.write(raw)
print(hashlib.sha256(raw).hexdigest())
