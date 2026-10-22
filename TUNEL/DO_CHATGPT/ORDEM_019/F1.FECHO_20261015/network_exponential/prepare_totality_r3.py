from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'ExponentialTotalityR2.lean').read_text(encoding='utf-8')
s=s.replace('simpa only [exponential_apply, component_smul, _root_.inner_smul_right (𝕜 := ℂ), coefficient] using hs', '''apply hs.congr
  intro n
  rw [exponential_apply, component_smul]
  exact _root_.inner_smul_right (v n) (component x n) (z^n)''')
s=s.replace('  ext n\n','  apply lp.ext\n  funext n\n')
s=s.replace('apply Submodule.mem_bot.mpr','change v = 0')
s=s.replace('lp.single 2 0 vacuumSector','lp.single (E := Sectors) 2 0 vacuumSector')
s=s.replace('lp.single_apply_ne (by omega)','lp.single_apply_ne 2 0 vacuumSector (by omega)')
with (b/'ExponentialTotalityR3.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(s)
