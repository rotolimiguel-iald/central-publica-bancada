from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'OrbitalRapidityMeasure_v3.lean').read_text(encoding='utf8')
s=s.replace('  have hgc := hg.comp (rapidityChart_continuous m).measurable', '  have hgc : Measurable (fun x => g (rapidityChart m x)) :=\n    hg.comp (rapidityChart_continuous m).measurable')
dest=p/'OrbitalRapidityMeasure_v4.lean'
assert not dest.exists()
raw=s.encode('utf8');tmp=dest.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw
tmp.rename(dest)
