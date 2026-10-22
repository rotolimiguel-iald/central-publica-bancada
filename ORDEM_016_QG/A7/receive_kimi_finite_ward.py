"""Preserve the completed scientific answer and its supplied check verbatim."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, re, uuid

H = Path(__file__).resolve().parent
D = H / 'kimi_finite_ward_audit'
D.mkdir(exist_ok=True)
source = H.parents[1] / 'IALD_ORQUESTRACAO_20260923/state/handoffs/7ed451ee-e554-4667-9d52-86c0f7c3c55b_delivery.json'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p, data):
    assert not p.exists(), p
    if isinstance(data, str): data = data.encode('utf-8')
    t = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    t.write_bytes(data)
    assert t.read_bytes() == data
    t.replace(p)

doc = json.loads(source.read_bytes())
answer = doc['result']['text']
blocks = re.findall(r'```python\s*\n(.*?)```', answer, re.S)
assert len(blocks) == 1, len(blocks)
code = blocks[0]
tree = ast.parse(code)
imports = []
for node in ast.walk(tree):
    if isinstance(node, ast.Import): imports.extend(q.name for q in node.names)
    if isinstance(node, ast.ImportFrom): imports.append(node.module)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        assert node.func.id not in {'exec','eval','open','compile','__import__','input'}
assert set(imports) <= {'sys','sympy'}, imports
put(D/'ANSWER.md', answer)
put(D/'provided_check.py', code)
put(D/'RECEIPT.json', json.dumps(dict(
    at=datetime.now(timezone.utc).isoformat(), job_id=doc['job_id'],
    source=str(source), source_sha256=sha(source),
    answer_sha256=sha(D/'ANSWER.md'), code_sha256=sha(D/'provided_check.py'),
    usage=doc['result']['usage'], model=doc['result']['model'],
    stage=doc['stage'], code_imports=imports,
    status='DECLARADO_PENDING_LOCAL_CHECK', remote_calls_here=0), indent=2))
print(json.dumps(dict(saved=True, chars=len(answer), code_lines=len(code.splitlines()), imports=imports)))
