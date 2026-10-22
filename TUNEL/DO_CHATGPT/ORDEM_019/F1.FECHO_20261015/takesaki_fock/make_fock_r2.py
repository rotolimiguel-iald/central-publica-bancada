from pathlib import Path
p=Path(__file__).parent
s=(p/'CanonicalFockRegularCoreR1.lean').read_text(encoding='utf-8')
s=s.replace('namespace RCC := F1Fecho.RegularCovariantCore\n','')
s=s.replace('RCC.','F1Fecho.RegularCovariantCore.')
with (p/'CanonicalFockRegularCoreR2.lean').open('x',encoding='utf-8',newline='\n') as f:f.write(s)
