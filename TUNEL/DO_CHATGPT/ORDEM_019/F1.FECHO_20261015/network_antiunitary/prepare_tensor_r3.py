from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'AntilinearTensorR2.lean').read_text(encoding='utf8')
start=s.index('    have hs :')
end=s.index('\n\n@[simp] theorem tensorAnti_tmul',start)
s=s[:start]+'''    rw [norm_eq_sqrt_re_inner (𝕜 := ℂ), norm_eq_sqrt_re_inner (𝕜 := ℂ)]
    apply congrArg Real.sqrt
    simpa only [Complex.star_def, Complex.conj_re] using h
'''+s[end:]
with (b/'AntilinearTensorR3.lean').open('x',encoding='utf8') as f:f.write(s)
t=(b/'BosonicGammaJR2.lean').read_text(encoding='utf8').replace('import AntilinearTensorR2','import AntilinearTensorR3')
with (b/'BosonicGammaJR3.lean').open('x',encoding='utf8') as f:f.write(t)
