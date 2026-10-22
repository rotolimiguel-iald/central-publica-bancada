from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'OrbitalL2Equivalence.lean').read_text(encoding='utf8')
s=s.replace('(by ext f; exact orbitalL2Pullback_inverse m f)', '(by apply LinearMap.ext; intro f; exact orbitalL2Pullback_inverse m f)')
s=s.replace('(by ext f; exact orbitalL2Inverse_pullback m f)', '(by apply LinearMap.ext; intro f; exact orbitalL2Inverse_pullback m f)')
d=p/'OrbitalL2Equivalence_v2.lean';assert not d.exists()
b=s.encode();t=d.with_suffix('.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.rename(d)
