from pathlib import Path
import hashlib,json
here=Path(__file__).resolve().parent
old=here/'RapidityJacobian.lean';new=here/'RapidityJacobian_v2.lean'
raw=old.read_bytes();text=raw.decode()
text=text.replace('    simp [longitudinal, Real.sinh_arsinh, hr.ne\']',
                  '    simp only [longitudinal, Real.sinh_arsinh]\n    field_simp')
text=text.replace('  simp [hp.ne\']',
                  '  have hc : (r*Real.cosh x) * (1/(r*Real.cosh x)) = 1 := by field_simp\n  rw [hc, ENNReal.ofReal_one]')
text=text.replace('measurableSet_univ','MeasurableSet.univ')
assert not new.exists()
with new.open('xb') as f:f.write(text.encode())
print(json.dumps(dict(output=str(new),predecessor_sha256=hashlib.sha256(raw).hexdigest())))
