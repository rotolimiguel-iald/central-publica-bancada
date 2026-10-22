from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'OrbitalRapidityMeasure.lean').read_text(encoding='utf8')
s=s.replace('q≠0 := by simp','q≠0 := by\n    simp only [ae_iff, not_not, Set.setOf_eq_eq_singleton, measure_singleton]')
s=s.replace('(orbitalWeight_measurable m) hg]', 'momentumMeasure (orbitalWeight_measurable m) hg]')
dest=p/'OrbitalRapidityMeasure_v2.lean'
assert not dest.exists()
raw=s.encode('utf8');tmp=dest.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw
tmp.rename(dest)
