from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'ExponentialTotalityR1.lean').read_text(encoding='utf-8').replace('import ExponentialVectorsR1','import ExponentialVectorsR3')
s=s.replace('lp.hasSum_inner v', 'lp.hasSum_inner (𝕜 := ℂ) v')
s=s.replace('inner_smul_right, coefficient','_root_.inner_smul_right (𝕜 := ℂ), coefficient')
s=s.replace('rw [inner_smul_right] at h','rw [_root_.inner_smul_right (v n) (pureTensor n x) (weight n : ℂ)] at h')
s=s.replace('end F1Fecho.Exponential',r'''theorem gamma_exponential (u : H1 ≃ₗᵢ[ℂ] H1) (x : H1) :
    gamma u (exponential x) = exponential (u x) := by
  ext n
  change gammaSector u n (component x n) = component (u x) n
  simp only [component, map_smul, gammaSector_pure]

theorem gammaJ_exponential (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1)
    (hj : Function.Involutive j) (x : H1) :
    F1Fecho.Antilinear.gammaJ j hj (exponential x) = exponential (j x) := by
  ext n
  change F1Fecho.Antilinear.sectorJ j hj n (component x n) = component (j x) n
  simp only [component, map_smulₛₗ, F1Fecho.Antilinear.sectorJ_pure,
    starRingEnd_apply, Complex.star_def, Complex.conj_ofReal]

theorem exponential_zero : exponential 0 = vacuum := by
  ext n
  change component 0 n = (lp.single 2 0 vacuumSector) n
  cases n with
  | zero => simp [component, weight, vacuumSector]
  | succ n =>
    rw [lp.single_apply_ne (by omega)]
    apply norm_eq_zero.mp
    rw [component, norm_smul, pureTensor_norm, norm_zero, zero_pow (by omega), mul_zero]

end F1Fecho.Exponential''')
s+='\n#print axioms F1Fecho.Exponential.gamma_exponential\n#print axioms F1Fecho.Exponential.gammaJ_exponential\n#print axioms F1Fecho.Exponential.exponential_zero\n'
with (b/'ExponentialTotalityR2.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(s)
