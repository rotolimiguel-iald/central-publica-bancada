"""Exact algebraic controls and additive custody; no canonical imports or execution."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parent
REF = r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json'
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}
TASK = 'R16_INTEGRATED_P_H3'

def new(name, value):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    with (ROOT / name).open('xb') as f:
        f.write((text + '\n').encode('utf-8'))
    return ROOT / name

def pin(path):
    p = Path(path).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def call(req, label, cli='mission_cli.py'):
    new(label + '_REQUEST.json', req)
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(Path(r'C:\IALD\MEMORIA_IALD') / cli)], input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding='utf-8')
    d = json.loads(p.stdout)
    new(label + '_RESULT.json', {'exit_code': p.returncode, 'response': d, 'stderr': p.stderr})
    if p.returncode or not d.get('ok'):
        raise RuntimeError(d)
    return d['result']

def project(label):
    return call({'operation': 'project', 'reference': REF, 'max_chars': 650000}, label)

def mutate(op, label, **kw):
    p = project(label + '_SYNC')
    return call({'operation': op, 'reference': REF, 'actor': ACTOR, 'expected_revision': p['receipt']['revision'], 'projection_sha256': p['projection_sha256'], 'event_id': 'r84-' + label, **kw}, label)

def check(label):
    p=project(label+'_SYNC')
    t=next(t for t in p['projection']['active'] if t['id']==TASK)
    r=call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':t['lease']['id']},label)
    if r.get('ready') is not True: raise RuntimeError(r)
    return r

