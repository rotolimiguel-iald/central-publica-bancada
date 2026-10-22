"""Inspect only the official initialization metadata, before sending any prompt."""
import json
import queue
import subprocess
import threading
from iald_orchestrator import antigravity as adapter
from iald_orchestrator.profiles import client_environment

proc = subprocess.Popen([str(adapter.EXE), '--agent', 'iald-text',
    '--disable-slash-commands', '--input-format','stream-json',
    '--output-format','stream-json', '--print-timeout','15s'],
    cwd=adapter.WORK, env=client_environment('antigravity'),
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
inbox=queue.Queue()
threading.Thread(target=lambda: inbox.put(proc.stdout.readline(1000000)), daemon=True).start()
try:
    line=inbox.get(timeout=25)
    event=json.loads(line)
    init=event.get('init',{})
    print(json.dumps({'event':event.get('event'), 'keys':list(event), 'init_keys':list(init),
        'agent':init.get('agent'), 'tools':init.get('tools'), 'model':init.get('model')},ensure_ascii=False))
finally:
    proc.kill()
    proc.wait(timeout=5)
