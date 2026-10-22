"""Recover the exact mission and claim the documentary extension once."""
from pathlib import Path
import json, subprocess, hashlib, sys

ROOT = Path(__file__).resolve().parent
REF = r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json'
BASE = Path(r'C:\IALD\MEMORIA_IALD')
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}

def new(name, value):
    p = ROOT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = (value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)) + '\n'
    with p.open('xb') as f:
        f.write(raw.encode('utf-8'))
    return p

def pin(p):
    p = Path(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def call(req, label, cli='mission_cli.py'):
    new(label+'_REQUEST.json', req)
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(BASE/cli)], input=json.dumps(req,ensure_ascii=False), capture_output=True, encoding='utf-8')
    d = json.loads(p.stdout)
    new(label+'_RESULT.json', {'exit_code':p.returncode, 'response':d, 'stderr':p.stderr})
    if p.returncode or not d.get('ok'): raise RuntimeError(d)
    return d['result']

def project(label):
    return call({'operation':'project','reference':REF,'max_chars':600000},label)

def mutate(op, label, **kw):
    m=project(label+'_SYNC')
    return call({'operation':op,'reference':REF,'actor':ACTOR,'expected_revision':m['receipt']['revision'], 'projection_sha256':m['projection_sha256'],'event_id':'r76-'+label, **kw},label)

