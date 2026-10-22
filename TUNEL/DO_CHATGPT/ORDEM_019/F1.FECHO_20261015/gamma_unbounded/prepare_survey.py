from pathlib import Path
import hashlib,json,datetime
b=Path(__file__).resolve().parent
k=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
refs=[(b.parent.parent/'F1.REDE/modular_wedge/CanonicalWedge.lean',['def TW','theorem TW_selfadjoint','theorem TW_positive']), (b.parent.parent/'F1.REDE/modular_wedge/CanonicalOutput.lean',['theorem delta_is_SdagS','def spectralOutput']), (b.parent/'network_exponential/ExponentialVectorsR3.lean',['theorem exponential_inner']), (b.parent/'wedge_exponential/RealSubspaceTotalityR5.lean',['theorem exponential_real_subspace_total']), (k/'TGLExt/V350RealGraphCore.lean',['theorem realGraphInclusion_dense','theorem realGraphCore_sequence']), (k/'TGLExt/V350ScalarTomitaGraphCore.lean',['theorem scalarTomitaSquare_graph_core']), (k/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/LinearPMap.lean',['theorem adjoint_isFormalAdjoint','theorem _root_.IsSelfAdjoint.dense_domain'])]
entries=[]
for p,ns in refs:
 raw=p.read_bytes();lines=raw.decode('utf8').splitlines()
 anchors=[dict(needle=n,lines=[i+1 for i,s in enumerate(lines) if n in s]) for n in ns]
 assert all(a['lines'] for a in anchors),(p,anchors)
 entries.append(dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),anchors=anchors))
d=dict(unit='F1.FECHO_20261015',claim=845,author='codex atrator_lean',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),statute='DERIVED_CONSTRUCTION_PLAN',sources=entries,construction=['The span of pairs (e(f),e(Tf)), f in D(T), is a concrete linear relation in the already constructed F x F.','For self-adjoint T, the exponential kernel proves symmetry of generator pairings.','Totality of e(D(T)) implies functionality even after graph closure, hence an actual closed LinearPMap.','The relation span is a graph core by closure definition, with simultaneous approximation of both coordinates.','Apply to the existing TW; keep the same sectors and exponential vectors.'],reused_vs_new=['The V350 realGraphCore theorem needs a weak-resolvent hypothesis not yet constructed here; it is NOT used as an automatic bridge.','The V350 scalar graph core applies to ScalarGNSHilbert P, not this Fock; no identification inferred.','New closed exponential lift is not yet asserted self-adjoint/positive, equal to spectral second quantization, or equal to the positive factor of the algebra-vacuum Tomita operator.'],provider_calls=False,production_modified=False)
with (b/'GAMMA_UNBOUNDED_SURVEY_R1.json').open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2)
print(hashlib.sha256((b/'GAMMA_UNBOUNDED_SURVEY_R1.json').read_bytes()).hexdigest())
