"""One public coding test with the official K3 subscription client."""
import json
import re
import subprocess
import time
from iald_orchestrator.providers import client_command, BASE
from iald_orchestrator.profiles import client_environment
from iald_orchestrator.safe_files import save_json, utc_now

work = BASE/'state/validation/kimi'
work.mkdir(parents=True, exist_ok=True)
(work/'.git').mkdir(exist_ok=True)
empty = work/'empty-skills'
empty.mkdir(exist_ok=True)
args = client_command('kimi') + ['--model', 'kimi-code/k3', '--agent-file', str(BASE/'iald_orchestrator/kimi_text_agent.md'), '--skills-dir', str(empty), '-p', 'Escreva apenas uma função Python add(a, b) que retorna a soma. Sem ferramentas.', '--output-format', 'stream-json']
start = time.monotonic()
try:
    proc = subprocess.run(args, cwd=work, env=client_environment('kimi'), capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=90, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    events = []
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        # Fixed public test only. Do not retain internal reasoning.
        if isinstance(event, dict):
            for key in ('reasoning', 'reasoning_content', 'thinking'):
                event.pop(key, None)
            if isinstance(event.get('content'), list):
                event['content'] = [x for x in event['content'] if x.get('type') not in ('thinking', 'reasoning')]
            events.append(event)
    diagnostic = re.sub(r'https?://\S+|[\w.+-]+@[\w.-]+|[A-Za-z0-9_=-]{35,}', '[REDACTED]', proc.stderr)[-1800:] if proc.returncode else ''
    record = {'checked_at': utc_now(), 'model_requested': 'kimi-code/k3', 'returncode': proc.returncode, 'elapsed_seconds': round(time.monotonic()-start,3), 'events': events, 'diagnostic': diagnostic}
except subprocess.TimeoutExpired:
    record = {'checked_at': utc_now(), 'returncode': None, 'error': 'Official client exceeded 90 seconds'}
save_json(BASE/'validation/kimi_pro_recheck.json', record)
print(json.dumps(record, ensure_ascii=False))
