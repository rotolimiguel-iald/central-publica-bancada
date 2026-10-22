from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'BosonicGammaJR4.lean').read_text(encoding='utf8')
s=s.replace("map_smul' c f := by ext n; simp [diagonalAntiFun]", "map_smul' c f := by ext n; exact (j n).map_smulₛₗ c (f n)")
with (b/'BosonicGammaJR5.lean').open('x',encoding='utf8') as f:f.write(s)
t=(b/'CanonicalFockAntiAssemblyR2.lean').read_text(encoding='utf8').replace('import BosonicGammaJR4','import BosonicGammaJR5')
with (b/'CanonicalFockAntiAssemblyR3.lean').open('x',encoding='utf8') as f:f.write(t)
