from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'OrbitalRapidityTransport.lean').read_text(encoding='utf8')
s=s.replace('  unfold inverseRapidityChart transverseMass\n  fun_prop', '  have ha : Measurable Real.arsinh := Real.continuous_arsinh.measurable\n  unfold inverseRapidityChart transverseMass\n  exact measurable_fst.prodMk (ha.comp (by fun_prop))')
s=s.replace('simpa only [not_not, Set.setOf_eq_eq_singleton] using exceptional_axis_null', 'simpa [Set.prod, not_not] using exceptional_axis_null')
s=s.replace('simpa only [not_not, Set.setOf_eq_eq_singleton] using exceptional_axis_orbital_null m', 'simpa [Set.prod, not_not] using exceptional_axis_orbital_null m')
d=p/'OrbitalRapidityTransport_v2.lean'
assert not d.exists()
b=s.encode();t=d.with_suffix('.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.rename(d)
