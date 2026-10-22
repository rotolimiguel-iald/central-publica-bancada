from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t13'
(D/'sources').mkdir(exist_ok=False)
rows=[]
for n in ['e2_private_directory_native.py','repair_e2_runtime_custody_013bis.py']:
    p=B/'refeito'/n;raw=p.read_bytes();out=D/'sources'/n
    with out.open('xb') as f:f.write(raw)
    assert out.read_bytes()==raw
    rows.append(dict(source=str(p),copy=str(out),sha256=hashlib.sha256(raw).hexdigest()))
value=dict(rows=rows,helper_copy_sha256=rows[0]['sha256'],repair_copy='NOT_EXECUTED__PRODUCTION_MAIN_NOT_CALLED',scope='Only helper rebased to fixture by harness; repair copy preserved for scoped review')
with (D/'FIXTURE_SOURCE_MANIFEST.json').open('xb') as f:f.write((json.dumps(value,indent=2)+'\n').encode())
print('Two verified copies; no helper or repair execution during copy.')
