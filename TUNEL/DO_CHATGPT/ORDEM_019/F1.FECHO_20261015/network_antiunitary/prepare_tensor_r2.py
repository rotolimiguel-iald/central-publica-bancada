from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'AntilinearTensorR1.lean').read_text(encoding='utf8')
s=s.replace('simp [antiunitary_inner_conj, star_mul]','simp [antiunitary_inner_conj, star_mul, mul_comm]')
s=s.replace('simpa using h','simpa only [Complex.star_def, Complex.conj_re, inner_self_eq_norm_sq] using h')
with (b/'AntilinearTensorR2.lean').open('x',encoding='utf8') as f:f.write(s)
t=(b/'BosonicGammaJR1.lean').read_text(encoding='utf8').replace('import AntilinearTensorR1','import AntilinearTensorR2')
with (b/'BosonicGammaJR2.lean').open('x',encoding='utf8') as f:f.write(t)
