from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'OrbitalRapidityTransport_v2.lean').read_text(encoding='utf8')
s=s.replace('    simpa [Set.prod, not_not] using exceptional_axis_null', '''    simp only [not_not]
    have hs : (({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ)) =
        {y : MomentumCoordinates | y.1 = 0} := by ext y; simp
    rw [← hs]
    exact exceptional_axis_null''')
s=s.replace('    simpa [Set.prod, not_not] using exceptional_axis_orbital_null m', '''    simp only [not_not]
    have hs : (({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ)) =
        {y : MomentumCoordinates | y.1 = 0} := by ext y; simp
    rw [← hs]
    exact exceptional_axis_orbital_null m''')
d=p/'OrbitalRapidityTransport_v3.lean';assert not d.exists()
b=s.encode();t=d.with_suffix('.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.rename(d)
