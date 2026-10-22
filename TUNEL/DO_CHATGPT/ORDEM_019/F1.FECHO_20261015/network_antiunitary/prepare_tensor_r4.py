from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'AntilinearTensorR3.lean').read_text(encoding='utf8').replace('Complex.star_def, Complex.conj_re] using h','Complex.star_def, Complex.conj_re, RCLike.re_to_complex] using h')
with (b/'AntilinearTensorR4.lean').open('x',encoding='utf8') as f:f.write(s)
t=(b/'BosonicGammaJR3.lean').read_text(encoding='utf8').replace('import AntilinearTensorR3','import AntilinearTensorR4')
with (b/'BosonicGammaJR4.lean').open('x',encoding='utf8') as f:f.write(t)
