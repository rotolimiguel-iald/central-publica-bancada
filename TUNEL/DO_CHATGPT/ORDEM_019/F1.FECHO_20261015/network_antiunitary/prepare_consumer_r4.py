from pathlib import Path
b=Path(__file__).resolve().parent
s=(b/'CanonicalFockAntiAssemblyR3.lean').read_text(encoding='utf8')
s=s.replace('open F1Rede.BosonicFock F1Fecho.NetworkReuse','open F1Rede.BosonicFock F1Fecho.NetworkReuse\nopen TGLExt.ContratoQGv31 TGLExt.ContratoQGv32')
s=s.replace('  /-- a conjugação modular [Tomita–Takesaki; BGL 2002 — o PCT]. -/\n','')
with (b/'CanonicalFockAntiAssemblyR4.lean').open('x',encoding='utf8') as f:f.write(s)
