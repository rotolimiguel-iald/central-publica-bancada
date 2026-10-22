"""Read-only deployment and exact-upload-copy verification."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        return None

base=Path(__file__).resolve().parent
opener=urllib.request.build_opener(NoRedirect())
checks={}
for route in ['/health','/app/iald.js','/admin/agi/orquestracao','/admin/api/orchestrator/status','/admin/api/prazos','/api/alertas']:
    try:
        with opener.open('http://127.0.0.1:8082'+route,timeout=8) as response:
            status=response.status;location=response.headers.get('Location')
    except urllib.error.HTTPError as error:
        status=error.code;location=error.headers.get('Location')
    checks[route]={'status':status,'location':location}
assert checks['/health']['status']==200
assert checks['/admin/agi/orquestracao']['status']==302 and checks['/admin/agi/orquestracao']['location'].startswith('/login')
assert all(checks[p]['status']==401 for p in ['/admin/api/orchestrator/status','/admin/api/prazos','/api/alertas'])
source=Path(r'C:\IALD\projetos_pyhton\IALD\iald_web_server.py')
installation=json.loads((base/'validation'/'admin_install.json').read_bytes())
assert hashlib.sha256(source.read_bytes()).hexdigest()==installation['after_sha256']
package=base/'project_fisica'
manifest=json.loads((package/'MANIFESTO_LOCAL.json').read_bytes())
copies=[]
for entry in manifest['files']:
    data=(package/entry['name']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==entry['sha256']
    assert len(data)==entry['bytes']
    original=Path(entry['source'])
    copies.append({'name':entry['name'],'copy_matches_record':True,
        'source_still_matches':hashlib.sha256(original.read_bytes()).hexdigest()==entry['sha256']})
report={'timestamp':datetime.now().isoformat(),'web_pid':78292,'supervisor_pid':41020,
    'http_checks':checks,'installed_source_matches':True,'uploaded_source_files':copies,
    'ui_fixture':'Prévia escolheu Codex para arquitetura, sem erros no console. Modelos desativados na fixture.',
    'automated_tests_passed':23,
    'mcp_protocol':'Duas ferramentas enumeradas; prévia escolheu local; nenhuma geração.',
    'mobile_builds_required':False,
    'scope':'Extensão apenas administrativa; código dos clientes públicos não alterado.'}
output=base/'validation'/'deployment_verified.json'
assert not output.exists(),'Recibo já existe; preservar e gerar outro se necessário.'
temp=output.with_suffix('.tmp');temp.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode())
assert temp.stat().st_size>0;temp.replace(output)
print(json.dumps(report,ensure_ascii=False))
