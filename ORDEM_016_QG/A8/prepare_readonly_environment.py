"""Use one canonical compiled TGL plus matching read-only package builds."""
from pathlib import Path
import json, hashlib
D=Path(__file__).resolve().parent; ROOT=D.parent
FALL=ROOT.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/kernel'
CAN=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
def new(p,b):
    assert not p.exists(),p
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b;tmp.rename(p)
env=D/'compiler_env';env.mkdir(exist_ok=False)
new(env/'lakefile.toml',b'name = "a8_type_reader_environment"\nversion = "0.1.0"\n')
new(env/'lean-toolchain',b'leanprover/lean4:v4.31.0\n')
names=[p['name'] for p in json.loads((FALL/'lake-manifest.json').read_bytes())['packages']]
paths=[CAN/'.lake/build/lib/lean']+[FALL/'.lake/packages'/n/'.lake/build/lib/lean' for n in names]
assert all(p.is_dir() for p in paths),[(str(p),p.is_dir()) for p in paths]
new(D/'READONLY_IMPORT_PATHS.json',json.dumps([str(p) for p in paths],indent=2).encode())
src=ROOT/'A0/compile_isolated_v2.py';txt=src.read_text('utf-8')
old='assert all(x.is_relative_to(allowed) for x in extra_paths)'
new_guard="readonly_paths = {Path(p).resolve() for p in json.loads((Path(__file__).parent/'READONLY_IMPORT_PATHS.json').read_bytes())}\nassert all(x.is_relative_to(allowed) or x in readonly_paths for x in extra_paths)"
assert txt.count(old)==1
new(D/'compile_a8_isolated_v2.py',txt.replace(old,new_guard).encode())
print('Prepared explicit read-only imports; fallback TGL modules excluded.')
