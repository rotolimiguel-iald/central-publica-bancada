"""One neutral test of the corrected native subscription client."""
from pathlib import Path
import json
import os
import subprocess
from iald_orchestrator.providers import client_command
from iald_orchestrator.runtime import now

root = Path(__file__).resolve().parent
work = root / 'validation' / 'diagnostic_work'
work.mkdir(parents=True, exist_ok=True)
env = {k:v for k,v in os.environ.items() if not any(t in k.upper() for t in ('API_KEY','AUTH_TOKEN','SECRET'))}
args = client_command('claude') + ['-p','--safe-mode','--restricted','--no-session-persistence',
    '--output-format','json','--tools','','--strict-mcp-config','--mcp-config','{"mcpServers":{}}',
    '--permission-prompts','none']
p = subprocess.run(args,input='Responda somente o resultado de 2 + 2.',capture_output=True,
    encoding='utf-8',errors='replace',cwd=work,env=env,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW)
try:
    data=json.loads(p.stdout)
    report={k:data.get(k) for k in ('subtype','is_error','result','usage','errors')}
except ValueError:
    report={'stdout':p.stdout[:1800]}
report.update(timestamp=now(),returncode=p.returncode,stderr=p.stderr[:1800])
# No credentials are queried; only diagnostic text from a public-input run.
text=json.dumps(report,ensure_ascii=False,indent=2)
print(text)
target=root/'validation'/'claude_corrected_run.json'
temp=target.with_suffix('.tmp');temp.write_bytes(text.encode());os.replace(temp,target)
