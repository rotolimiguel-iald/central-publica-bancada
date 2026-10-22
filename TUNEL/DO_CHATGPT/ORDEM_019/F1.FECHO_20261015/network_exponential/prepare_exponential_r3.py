from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'ExponentialVectorsR2.lean').read_text(encoding='utf-8')
s=s.replace('rw [component, component, _root_.inner_smul_left (𝕜 := ℂ), _root_.inner_smul_right (𝕜 := ℂ), pureTensor_inner]', '''change inner ℂ ((weight n : ℂ) • pureTensor n x) ((weight n : ℂ) • pureTensor n y) = _
  rw [_root_.inner_smul_left (pureTensor n x) ((weight n : ℂ) • pureTensor n y) (weight n : ℂ),
    _root_.inner_smul_right (pureTensor n x) (pureTensor n y) (weight n : ℂ), pureTensor_inner]''')
with (b/'ExponentialVectorsR3.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(s)
