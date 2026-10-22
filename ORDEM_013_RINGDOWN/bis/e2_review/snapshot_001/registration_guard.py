"""Read-only authorization of a whole code tree and its E2 tunnel witness."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re

BASE=Path(__file__).resolve().parents[2]
ROOT=BASE.parent
CODE=Path(__file__).resolve().parent

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def contained(name,root=ROOT):
    p=(root/name).resolve()
    if not p.is_relative_to(root.resolve()):raise ValueError('Path outside registered root')
    return p

def checked_registration():
    path=BASE/'RINGDOWN_5SIGMA_V1.json'
    digest=sha(path);reg=json.loads(path.read_text(encoding='utf-8'))
    if reg['status']!='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST':raise ValueError('Not an active E2 registration')
    note=contained(reg['witness_relative_to_Chatgpt'])
    text=note.read_text(encoding='utf-8')
    matches=re.findall(r'^registro_sha256: ([0-9a-f]{64})$',text,re.M)
    if matches!=[digest]:raise ValueError('Tunnel witness hash differs or is ambiguous')
    own={str(p.relative_to(CODE)).replace('\\','/'):sha(p) for p in CODE.rglob('*.py')}
    if own!=reg['own_code_tree_sha256']:raise ValueError('Own code tree differs from complete registered tree')
    for name,wanted in reg['input_pins_relative_to_Chatgpt'].items():
        if sha(contained(name))!=wanted:raise ValueError('Registered input changed: '+name)
    runtime=contained(reg['runtime_manifest_relative_to_Chatgpt'])
    if sha(runtime)!=reg['runtime_manifest_sha256']:raise ValueError('Runtime manifest changed')
    environment=json.loads(runtime.read_bytes())
    for name,wanted in environment['files'].items():
        p=Path(name).resolve()
        if not p.is_relative_to('/opt/lal_env') or sha(p)!=wanted['sha256']:raise ValueError('Scientific runtime code changed')
    if sha(Path(environment['python_executable']))!=environment['python_executable_sha256']:raise ValueError('Python interpreter changed')
    time_guard(reg)
    return reg,digest

def time_guard(reg):
    budget=contained(reg['budget_relative_to_Chatgpt'])
    if sha(budget)!=reg['budget_sha256']:raise ValueError('Budget changed')
    b=json.loads(budget.read_bytes())
    deadline=datetime.fromisoformat(b['hard_deadline_utc'])
    if deadline.tzinfo is None or datetime.now(timezone.utc)>=deadline:raise TimeoutError('Part B hard deadline reached')
    return deadline

def authorize_event(reg,event,mode):
    if mode not in ('calibration','blind_test'):raise ValueError('Unknown analysis mode')
    known=set(reg['calibration_event_ids'])
    if mode=='calibration' and event not in known:raise ValueError('New event cannot enter calibration path')
    if mode=='blind_test':
        if event in known:raise ValueError('Published calibration event cannot enter blind test')
        entry=reg['test_candidates'].get(event)
        if entry is None:raise ValueError('Event has no registered pre-analysis candidate entry')
        if entry['eligible'] is not True:raise ValueError('Pre-analysis eligibility unpaid or failed')
        if entry['published_deformation_at_registration'] is not False:raise ValueError('Blindness census not established')
    return True

def output_path(name):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,150}',name):raise ValueError('Unsafe output name')
    return BASE/'cache'/name
