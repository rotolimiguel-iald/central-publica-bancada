from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parent
src=root/'v31/ContratoQG_v31_Teoremas.lean'
b=src.read_bytes()
first=b[b.index(b'theorem shift_point'):b.index('/-- [DERIVED] ★ o 8πG'.encode())]
second=b[b.index('/-- [DERIVED] κ cancela:'.encode()):b.index('/-- ★ G NÃO'.encode())]
body=first+second
head=b'import ContratoQG_v31_Minimal\n\nset_option autoImplicit false\nset_option maxHeartbeats 2000000\nnamespace TGLExt.ContratoQGv31\nopen TGL.SpecificAQFT TGL.ModularRealization\nopen MeasureTheory Matrix Complex Filter Topology\nopen scoped InnerProductSpace ComplexConjugate\nnoncomputable section\n'
names=re.findall(rb'^theorem ([^\s(]+)',body,re.M)
helper=names[:5]
tail=b'\nend ContratoH3\n'
tail+=b''.join(b'#print axioms '+n+b'\n' for n in helper)
tail+=b''.join(b'#print axioms ContratoH3.'+n+b'\n' for n in names[5:])
tail+=b'end\nend TGLExt.ContratoQGv31\n'
dest=root/'minimal_imports/WindowLemmasVerbatim.lean'
assert not dest.exists()
dest.write_bytes(head+body+tail)
meta={'source':str(src),'source_sha256':hashlib.sha256(b).hexdigest(),
      'ranges':'shift_point through clausius_window; kappa_cancels_window through exp_propagator_excluded',
      'body_verbatim':True,'first_chunk_sha256':hashlib.sha256(first).hexdigest(),
      'second_chunk_sha256':hashlib.sha256(second).hexdigest(),
      'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'declarations':len(names),
      'excluded':'einstein_coefficient_window: dependency TriadMaster not loaded in this subset; no replacement proof'}
mp=root/'minimal_imports/window_subset_preparation.json'
with mp.open('x',encoding='utf-8') as f:json.dump(meta,f,ensure_ascii=False,indent=2)
print(json.dumps(meta,ensure_ascii=False))
