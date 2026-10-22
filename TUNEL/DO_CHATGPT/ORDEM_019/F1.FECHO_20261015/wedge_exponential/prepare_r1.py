from pathlib import Path
import json,hashlib,datetime
b=Path(__file__).resolve().parent
k=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
m=k/'.lake/packages/mathlib/Mathlib'
files=[b.parent/'network_exponential/ExponentialVectorsR3.lean',b.parent/'network_exponential/ExponentialTotalityR4.lean',m/'Analysis/Analytic/IsolatedZeros.lean',m/'Analysis/Analytic/Uniqueness.lean',m/'Analysis/Analytic/Linear.lean',m/'Analysis/Normed/Operator/Bilinear.lean',m/'Topology/Algebra/Module/Multilinear/Basic.lean',m/'Analysis/InnerProductSpace/StandardSubspace.lean']
d=dict(unit='F1.FECHO_20261015',claim=845,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),target='Totality of exponential vectors on a real subspace whose complex span is dense; no totality field.',reuse=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in files],route=['Real scalar power-series uniqueness extracts inner(v_n,k^n)=0 for k in K.','Tensor diagonal is analytic, using bounded tensor bilinear map and completion.','Identity theorem on real line extends x+t*y to x+i*y.','Complexification K+iK equals complex span; density and continuity give all pure tensors.','Reuse sector closed-span and orthogonal-complement totality proofs.'],production_modified=False,provider_calls=False)
with (b/'WEDGE_EXPONENTIAL_SURVEY_R1.json').open('x',encoding='utf8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
src=(b.parent/'network_exponential/build_exponential.py').read_text(encoding='utf8')
src=src.replace("BASE.parent/'network_antiunitary']","BASE.parent/'network_antiunitary', BASE.parent/'network_exponential']")
with (b/'build_wedge.py').open('x',encoding='utf8',newline='\n') as f:f.write(src)
print(hashlib.sha256((b/'WEDGE_EXPONENTIAL_SURVEY_R1.json').read_bytes()).hexdigest())
