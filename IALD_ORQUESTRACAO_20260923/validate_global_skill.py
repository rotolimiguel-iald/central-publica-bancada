"""Read-only discovery from fresh processes and unrelated working directories."""
import asyncio
import json
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
from iald_orchestrator.safe_files import save_json, utc_now

BASE = Path(__file__).resolve().parent
PYTHON = r'C:\Python314\python.exe'

def app_discovery(cwd):
    codex = shutil.which('codex')
    assert codex
    process = subprocess.Popen([codex, 'app-server', '--stdio'], cwd=cwd,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
    inbox = queue.Queue()
    def reader():
        for line in process.stdout:
            try:
                inbox.put(json.loads(line))
            except json.JSONDecodeError:
                continue
    threading.Thread(target=reader, daemon=True).start()
    def send(value):
        process.stdin.write(json.dumps(value)+'\n')
        process.stdin.flush()
    def response(identifier):
        import time
        deadline = time.monotonic()+40
        while time.monotonic()<deadline:
            item = inbox.get(timeout=max(.1, deadline-time.monotonic()))
            if item.get('id') == identifier:
                assert 'error' not in item, item.get('error')
                return item['result']
        raise TimeoutError('No discovery response')
    try:
        send({'id':1, 'method':'initialize', 'params':{'clientInfo':{
            'name':'iald-global-skill-check', 'version':'1.0'}}})
        response(1)
        send({'method':'initialized'})
        send({'id':2, 'method':'skills/list', 'params':{
            'cwds':[str(BASE), str(cwd)], 'forceReload':True}})
        result = response(2)
        matches = []
        for entry in result['data']:
            found = [s for s in entry['skills'] if s['name']=='iald-orquestrar']
            assert len(found)==1, 'Skill absent or duplicate for requested cwd'
            skill = found[0]
            assert skill['enabled']
            matches.append({'cwd':entry['cwd'], 'path':skill['path'],
                            'scope':skill['scope'], 'enabled':skill['enabled']})
        assert len(matches)==2
        return matches
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

async def mcp_discovery(cwd):
    from fastmcp import Client
    from fastmcp.client.transports import PythonStdioTransport
    transport = PythonStdioTransport(str(BASE/'mcp_server.py'), python_cmd=PYTHON, cwd=str(cwd))
    async with Client(transport) as client:
        names = [t.name for t in await client.list_tools()]
        assert {'iald_coordination_submit','iald_coordination_get','iald_transport_next'} <= set(names)
        selected = await client.call_tool('iald_selection_preview', {'task':'Calcule 2 + 2.'})
        return {'tools':names, 'selection_status':selected.data['status'], 'provider_calls':0}

def main():
    check = subprocess.run([PYTHON, '-X','utf8',
        r'C:\Users\rotol\.codex\skills\.system\skill-creator\scripts\quick_validate.py',
        r'C:\Users\rotol\.agents\skills\iald-orquestrar'], capture_output=True, text=True, encoding='utf-8')
    assert check.returncode==0, check.stderr
    with tempfile.TemporaryDirectory(prefix='iald-global-discovery-') as cwd:
        discovery = app_discovery(cwd)
        mcp = asyncio.run(mcp_discovery(cwd))
        call = subprocess.run([PYTHON,'-X','utf8',str(BASE/'transport_cli.py')], cwd=cwd,
            input=json.dumps({'operation':'next'}), text=True, encoding='utf-8',
            capture_output=True, timeout=30, check=True)
        state = json.loads(call.stdout)
    report = {'at':utc_now(), 'skill_validation':check.stdout.strip(),
        'fresh_app_server_discovery':discovery, 'fresh_mcp_server':mcp,
        'cli_from_unrelated_cwd':{'state':state['state'], 'pending':state['pending']},
        'new_tasks_created':0, 'models_called':0}
    save_json(BASE/'validation/global_skill_validation.json', report)
    print(json.dumps(report, ensure_ascii=False))

if __name__=='__main__':
    main()
