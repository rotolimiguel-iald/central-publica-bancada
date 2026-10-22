"""Read-only inventory of IALD author material; immutable survey artifacts."""
from pathlib import Path
import collections
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = Path(r'C:\IALD')
REF = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}
TEXT = {'.py', '.lean', '.tex', '.md', '.txt', '.json', '.jsonl', '.rst', '.html', '.csv', '.tsv', '.ipynb', '.m', '.nb', '.wl'}
DOCS = {'.docx', '.pdf', '.doc', '.odt', '.rtf', '.pptx'}
SKIP = {'.git', '.svn', 'node_modules', '.venv', 'venv', 'site-packages', '__pycache__', '.pytest_cache', '.mypy_cache', '.next', '.gradle', 'pods'}
PRIVATE_ROOTS = {'advocacia', 'documentos luiz antonio', 'vendas'}
SECRET_NAMES = {'iald_stack_v7.py', 'iald_psion_state.json'}

def new(name, value):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = value if isinstance(value, bytes) else ((value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)) + '\n').encode('utf-8')
    with path.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    return path

def pin(p):
    p = Path(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}

def cli(name, req, label):
    new(label + '_REQUEST.json', req)
    cp = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(BASE/'MEMORIA_IALD'/name)], input=json.dumps(req, ensure_ascii=False), capture_output=True, encoding='utf-8')
    value = json.loads(cp.stdout)
    new(label + '_RESULT.json', {'exit_code': cp.returncode, 'result': value, 'stderr': cp.stderr})
    if cp.returncode or not value.get('ok'):
        raise RuntimeError(label)
    return value['result']

def start():
    source = new('OPERADOR_LEVANTAMENTO_VERBATIM.txt', 'Examine o que falta resolvermos da gravidade quântica, reexamine tudo, faça um apanhado geral de tudo que eu já produzi dentro do meu computador, especificamente dentro da pasta c:\\IALD E ENCONTRE AS PEÇAS QUE FALTAM')
    cli('session_memory.py', {'operation': 'project', 'reference': str(REF), 'max_chars': 600000}, 'ACOM_START')
    p = cli('mission_cli.py', {'operation': 'project', 'reference': str(REF), 'max_chars': 400000}, 'MISSION_START')
    task = next(t for t in p['projection']['active'] if t['id'] == 'R5')
    cli('mission_cli.py', {'operation': 'check', 'reference': str(REF), 'actor': ACTOR,
        'expected_revision': p['receipt']['revision'], 'projection_sha256': p['projection_sha256'],
        'task_id': 'R5', 'lease_id': task['lease']['id']}, 'PREFLIGHT_START')
    for label, command in [('NOS_VIVO', [r'C:\IALD\NOS_VIVO\consultar.py', '--unidade', 'F1.FECHO_20261015']),
                           ('MAP_PRIOR', [r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'consultar', 'rede dispositivo relogio']),
                           ('BOARD_PRIOR', [r'C:\IALD\PROGRAMA_IALD\iald.py', 'ver', 'F1.FECHO_20261015'])]:
        cp = subprocess.run([sys.executable, '-B', '-X', 'utf8', *command], capture_output=True, encoding='utf-8')
        new(label+'.json', {'command': command, 'exit_code': cp.returncode, 'stdout': cp.stdout, 'stderr': cp.stderr})
    state = cli('session_memory.py', {'operation': 'get', 'reference': str(REF)}, 'GET_START')
    cli('session_memory.py', {'operation': 'transition', 'reference': str(REF), 'actor': ACTOR,
        'expected_revision': state['revision'], 'event_id': 'r58-authorized-corpus-survey-20261017',
        'changes': {'records': [{'id': 'r58-user-survey-order', 'kind': 'decision', 'statute': 'INPUT',
            'sources': [{'kind': 'artifact', 'ref': str(source), 'sha256': pin(source)['sha256']}],
            'text': 'Operador ordena reexame amplo do acervo de C:\\IALD para localizar peças já produzidas e confrontar lacunas QG. Levantamento de fontes, sem presumir ausência nem fechamento.'}],
            'flow': {'phase': 'r58_reexame_acervo', 'next_action': 'Inventariar corpus, comparar fontes primárias por hipótese/consumidor e produzir matriz de reaproveitamento com cobertura explícita.'}}}, 'TRANSITION_START')
    print(json.dumps({'source': pin(source), 'nos_vivo': 'See NOS_VIVO.json; current unit absent from old graph', 'mission_revision_before': state['revision']}))

def inventory():
    counts = collections.Counter()
    top = collections.defaultdict(collections.Counter)
    skipped = []
    errors = []
    index = ROOT/'FILE_INVENTORY.jsonl'
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    with index.open('x', encoding='utf-8', newline='\n') as out:
        stack = [BASE]
        while stack:
            directory = stack.pop()
            try:
                entries = list(os.scandir(directory))
            except OSError as exc:
                errors.append({'path': str(directory), 'error': str(exc)}); continue
            for e in entries:
                p = Path(e.path)
                rel = p.relative_to(BASE)
                name = e.name.lower()
                try:
                    st = e.stat(follow_symlinks=False)
                    if e.is_symlink() or getattr(st, 'st_file_attributes', 0) & 0x400:
                        skipped.append({'path': str(p), 'reason': 'reparse_or_symlink_not_followed'}); continue
                    if e.is_dir(follow_symlinks=False):
                        if (len(rel.parts) == 1 and name in PRIVATE_ROOTS) or name == 'escritorio':
                            skipped.append({'path': str(p), 'reason': 'separate_private_house'}); continue
                        if name in SKIP or ('.lake' in rel.parts and name in {'packages', 'build'}):
                            skipped.append({'path': str(p), 'reason': 'dependency_or_generated_cache'}); continue
                        if p == ROOT:
                            skipped.append({'path': str(p), 'reason': 'current_survey_outputs'}); continue
                        stack.append(p); counts['directories'] += 1
                        continue
                    if not e.is_file(follow_symlinks=False): continue
                    ext = p.suffix.lower()
                    secret = name in SECRET_NAMES or name.startswith(('.env', 'iald_psion_state')) or ext in {'.pem', '.key', '.pfx', '.p12'}
                    historical = '.bak' in name or '_backup' in str(rel).lower() or '_cofre' in str(rel).lower() or '.trash' in rel.parts
                    kind = 'protected' if secret else ('text' if ext in TEXT else 'document' if ext in DOCS else 'other')
                    row = {'path': str(p), 'top': rel.parts[0], 'bytes': st.st_size, 'mtime_ns': st.st_mtime_ns,
                        'extension': ext, 'kind': kind, 'historical': historical}
                    out.write(json.dumps(row, ensure_ascii=False)+'\n')
                    counts['files'] += 1; counts[kind] += 1; counts['bytes'] += st.st_size
                    top[rel.parts[0]][kind] += 1
                except OSError as exc:
                    errors.append({'path': str(p), 'error': str(exc)})
        out.flush(); os.fsync(out.fileno())
    result = {'started_utc': start, 'ended_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'counts': dict(counts), 'by_top': {k: dict(v) for k,v in sorted(top.items())},
        'excluded_directories': skipped, 'errors': errors, 'inventory': pin(index),
        'scope': 'Metadata inventory is not semantic reading. Dependencies/reparse/private houses excluded explicitly. Content of protected files not read; originals unchanged.'}
    new('INVENTORY_RESULT.json', result)
    print(json.dumps({'counts': dict(counts), 'excluded_directories': len(skipped), 'errors': len(errors)}, ensure_ascii=False))

if __name__ == '__main__':
    {'start': start, 'inventory': inventory}[sys.argv[1]]()
