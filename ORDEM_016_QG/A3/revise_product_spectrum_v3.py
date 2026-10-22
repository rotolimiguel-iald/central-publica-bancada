from pathlib import Path
p=Path(__file__).resolve().parent
for before,after,old,new in [
 ('ProductOrbitalSpectrum_v2.lean','ProductOrbitalSpectrum_v3.lean','ae_ae_of_ae_prod hn','Measure.ae_ae_of_ae_prod hn'),
 ('IsometricCocycleSpectrum.lean','IsometricCocycleSpectrum_v2.lean','import ProductOrbitalSpectrum_v2','import ProductOrbitalSpectrum_v3')]:
    s=(p/before).read_text(encoding='utf8').replace(old,new)
    d=p/after;assert not d.exists();b=s.encode();t=d.with_suffix('.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.rename(d)
