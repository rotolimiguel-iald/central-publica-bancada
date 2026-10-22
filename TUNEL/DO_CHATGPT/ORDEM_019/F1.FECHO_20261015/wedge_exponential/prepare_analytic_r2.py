from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'WedgeAnalyticR1.lean').read_text(encoding='utf8')
s=s.replace('def realSeries', '''theorem ofReal_smul_H1 (t : ℝ) (x : H1) : (t : ℂ) • x = t • x := by
  rw [show (t : ℂ) = t • (1 : ℂ) by simp [Complex.real_smul], smul_assoc, one_smul]

def realSeries''')
s=s.replace('simpa only [RCLike.real_smul_eq_coe_smul (K := ℂ)] using K.smul_mem t hx','rw [ofReal_smul_H1]\n      exact K.smul_mem t hx')
s=s.replace('''  exact (Completion.toComplL (𝕜 := ℂ) (E := Algebraic n)).analyticAt.comp
    (analytic_pureAlgebraic n x)''','''  exact ((Completion.toComplL (𝕜 := ℂ) (E := Algebraic n)).analyticAt _).comp
    (analytic_pureAlgebraic n x)''')
s=s.replace('''    exact_mod_cast Complex.continuous_ofReal.continuousAt.tendsto.comp
      (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))''','''    simpa only [a, Function.comp_def, Complex.ofReal_zero] using
      (Complex.continuous_ofReal.tendsto (0 : ℝ)).comp
        (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))''')
s=s.replace('fun n => hf (1 / ((n : ℝ)+1))','fun n : ℕ => hf (1 / ((n : ℝ)+1))')
with (b/'WedgeAnalyticR2.lean').open('x',encoding='utf8',newline='\n') as f:f.write(s)
