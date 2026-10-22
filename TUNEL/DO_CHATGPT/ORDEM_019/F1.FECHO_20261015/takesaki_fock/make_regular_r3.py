from pathlib import Path
p=Path(__file__).parent
s=(p/'RegularCovariantCoreR2.lean').read_text(encoding='utf-8')
s=s.replace('theorem boostCLM_star', '''theorem boostCLM_eq_coe (t : ℝ) :
    boostCLM B t = (boostIso B t : H →L[ℂ] H) := by
  apply ContinuousLinearMap.ext
  intro v
  rfl

theorem boostCLM_star''')
s=s.replace('rw [boostCLM,LinearIsometryEquiv.star_eq_symm,boostCLM,boostIso_neg B]',
'''rw [boostCLM_eq_coe B,LinearIsometryEquiv.star_eq_symm,boostCLM_eq_coe B,boostIso_neg B]''')
s=s.replace('rw [boostCLM,LinearIsometryEquiv.star_eq_symm]\n  rfl',
'''rw [boostCLM_eq_coe B,LinearIsometryEquiv.star_eq_symm]
  rfl''')
s=s.replace('  simpa only [regularUnitary,ContinuousLinearMap.mul_apply,Function.comp_apply,boostCLM] using h.comp hp',
'''  refine (h.comp hp).congr ?_
  intro t
  change fibre (boostIso B t).toLinearIsometry.toContinuousLinearMap (shift t f) = regularUnitary B t f
  rfl''')
with (p/'RegularCovariantCoreR3.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(s)
