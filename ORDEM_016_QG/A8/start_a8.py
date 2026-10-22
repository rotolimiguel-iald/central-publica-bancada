"""Prepare the A8 proposal bench; never run lake against the canonical workspace."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

D=Path(__file__).resolve().parent
ROOT=D.parent
CAN=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
FALL=ROOT.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/kernel'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
    assert not p.exists(),p
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_bytes(b)
    assert tmp.read_bytes()==b;tmp.rename(p)
data={'at':datetime.now(timezone.utc).isoformat(),'branch':'A8','ceiling_hours':4,
      'opening_sha256':sha(ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_016_ABERTURA_operador.md'),
      'canonical_lake_never_executed':True,'fallback':str(FALL),'canonical_read_only_build':str(CAN/'.lake/build/lib/lean')}
for key,p in [('canonical',CAN),('fallback',FALL)]:
    manifest=json.loads((p/'lake-manifest.json').read_bytes())
    data[key+'_manifest_sha256']=sha(p/'lake-manifest.json')
    data[key+'_revisions']={x['name']:x.get('rev') for x in manifest['packages']}
assert data['canonical_revisions']==data['fallback_revisions']
new(D/'START.json',json.dumps(data,ensure_ascii=False,indent=2).encode())
src=ROOT/'A0/compile_isolated_v2.py';text=src.read_text('utf-8')
old='assert all(x.is_relative_to(allowed) for x in extra_paths)'
replacement="assert all(x.is_relative_to(allowed) or x == Path(r'C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós\\tgl_kernel\\.lake\\build\\lib\\lean').resolve() for x in extra_paths)"
assert text.count(old)==1
new(D/'compile_a8_readonly.py',text.replace(old,replacement).encode())
new(D/'HELPER_PROVENANCE.json',json.dumps({'source':str(src),'sha256':sha(src),'change':'Allow precisely canonical compiled-module directory as read-only LEAN_PATH, lake cwd stays fallback. No canonical package access or write.'},indent=2).encode())
print(json.dumps(data,ensure_ascii=False))
