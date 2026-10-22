from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'ExponentialVectorsR1.lean').read_text(encoding='utf-8')
s=s.replace('rw [ih, TensorProduct.smul_tmul, TensorProduct.tmul_smul, smul_smul, pow_succ\']','rw [ih, TensorProduct.smul_tmul_smul, pow_succ\']')
s=s.replace('exact_mod_cast weight_sq n','simpa only [Complex.ofReal_pow, Complex.ofReal_inv, Complex.ofReal_natCast] using\n    congrArg (fun a : ℝ => (a : ℂ)) (weight_sq n)')
s=s.replace('Complex.norm_real, abs_of_pos','Complex.norm_real, Real.norm_eq_abs, abs_of_pos')
s=s.replace('inner_smul_left, inner_smul_right','_root_.inner_smul_left (𝕜 := ℂ), _root_.inner_smul_right (𝕜 := ℂ)')
s=s.replace('lp.hasSum_inner (exponential x)', 'lp.hasSum_inner (𝕜 := ℂ) (exponential x)')
with (b/'ExponentialVectorsR2.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(s)
