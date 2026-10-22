from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'ProductOrbitalSpectrum.lean').read_text(encoding='utf8')
s=s.replace('(measurePreserving_swap ', '(Measure.measurePreserving_swap ')
d=p/'ProductOrbitalSpectrum_v2.lean';assert not d.exists()
b=s.encode();t=d.with_suffix('.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.rename(d)
