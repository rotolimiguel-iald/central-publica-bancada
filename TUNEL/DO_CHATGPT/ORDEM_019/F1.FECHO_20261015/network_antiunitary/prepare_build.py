from pathlib import Path
b=Path(__file__).resolve().parent
s=(b.parent/'network_reuse/build_assembly.py').read_text(encoding='utf8')
s=s.replace('CanonicalFockAssemblyR1.lean','AntilinearTensorR1.lean')
s=s.replace("srcs=[p for p in NET.glob('*/'+name+'.lean') if 'review' not in p.parent.name]", "srcs=[p for p in NET.glob('*/'+name+'.lean') if 'review' not in p.parent.name]+[p for folder in [BASE, BASE.parent/'network_reuse'] for p in folder.glob(name+'.lean')]")
with (b/'build_antiunitary.py').open('x',encoding='utf8') as f: f.write(s)
