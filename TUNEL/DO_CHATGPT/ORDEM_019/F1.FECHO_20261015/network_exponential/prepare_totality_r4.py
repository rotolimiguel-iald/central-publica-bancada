from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'ExponentialTotalityR3.lean').read_text(encoding='utf-8')
s=s.replace('''  apply hs.congr
  intro n
  rw [exponential_apply, component_smul]
  exact _root_.inner_smul_right (v n) (component x n) (z^n)''','''  have he : (fun n => inner ℂ (v n) (exponential (z • x) n)) =
      (fun n => z^n * coefficient v x n) := by
    funext n
    change inner ℂ (v n) (component (z • x) n) = _
    rw [component_smul]
    exact _root_.inner_smul_right (v n) (component x n) (z^n)
  rw [he] at hs
  exact hs''')
s=s.replace('''  simp only [component, map_smulₛₗ, F1Fecho.Antilinear.sectorJ_pure,
    starRingEnd_apply, Complex.star_def, Complex.conj_ofReal]''','''  change F1Fecho.Antilinear.sectorJ j hj n ((weight n : ℂ) • pureTensor n x) =
    (weight n : ℂ) • pureTensor n (j x)
  rw [(F1Fecho.Antilinear.sectorJ j hj n).map_smulₛₗ (weight n : ℂ) (pureTensor n x),
    F1Fecho.Antilinear.sectorJ_pure]
  change star (weight n : ℂ) • pureTensor n (j x) = _
  rw [Complex.star_def, Complex.conj_ofReal]''')
s=s.replace('''    rw [lp.single_apply_ne 2 0 vacuumSector (by omega)]
    apply norm_eq_zero.mp
    rw [component, norm_smul, pureTensor_norm, norm_zero, zero_pow (by omega), mul_zero]''','''    have hs : (lp.single (E := Sectors) 2 0 vacuumSector) (n+1) = 0 :=
      lp.single_apply_ne (E := Sectors) 2 0 vacuumSector (by omega)
    calc
      component 0 (n+1) = 0 := by
        apply norm_eq_zero.mp
        rw [component, norm_smul, pureTensor_norm, norm_zero, zero_pow (by omega), mul_zero]
      _ = _ := hs.symm''')
with (b/'ExponentialTotalityR4.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(s)
