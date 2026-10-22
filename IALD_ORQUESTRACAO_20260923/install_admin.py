"""Minimal native-server attachment, with byte backup and compare-before-replace."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

base=Path(__file__).resolve().parent
target=Path(r'C:\IALD\projetos_pyhton\IALD\iald_web_server.py')
old=target.read_bytes()
marker=b'# IALD_ORCHESTRATOR_ADMIN_20260923'
if marker in old:raise SystemExit('A integração já está instalada; não reescrever.')
newline=b'\r\n' if b'\r\n' in old else b'\n'
hook=f'''# IALD_ORCHESTRATOR_ADMIN_20260923
try:
    _iald_orchestrator_path = {str(base)!r}
    if _iald_orchestrator_path not in sys.path:
        sys.path.insert(0, _iald_orchestrator_path)
    from iald_orchestrator.web import install as _install_iald_orchestrator
    _install_iald_orchestrator(app, require_admin)
except Exception as _iald_orchestrator_error:
    print("[orchestrator] UNAVAILABLE: " + type(_iald_orchestrator_error).__name__, flush=True)
    @app.route("/admin/agi/orquestracao")
    def _iald_orchestrator_unavailable():
        _denied = require_admin()
        if _denied is not None:
            return _denied
        return "Orquestracao indisponivel; verificar a instalacao local.", 503

'''.encode().replace(b'\n',newline)
entry=b'if __name__ == "__main__":'
assert old.count(entry)==1
html=b'<div class="sec" id="s-ag">'
assert old.count(html)==1
link=b'<div class="c" style="margin-bottom:16px"><div class="ct">ORQUESTRACAO IALD</div><p>Selecao automatica, conexoes e projeto Fisica.</p><a class="bt bt-p" href="/admin/agi/orquestracao">Abrir orquestracao</a></div>'
new=old.replace(entry,hook+entry).replace(html,html+newline+link)
compile(new.decode('utf-8'),str(target),'exec')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
backup=target.with_name(target.name+'.bak_'+stamp)
backup.write_bytes(old)
assert backup.read_bytes()==old
tmp=target.with_name(target.name+'.orchestrator.tmp')
tmp.write_bytes(new)
assert tmp.read_bytes()==new and len(new)>len(old)
assert target.read_bytes()==old, 'Arquivo mudou durante a preparação; recusa CAS.'
os.replace(tmp,target)
assert target.read_bytes()==new
report={'timestamp':datetime.now().isoformat(),'target':str(target),'backup':str(backup),
 'before_sha256':hashlib.sha256(old).hexdigest(),'after_sha256':hashlib.sha256(new).hexdigest(),
 'restart_status':'PENDING','scope':'Duas inserções: link admin e registro do módulo; clientes públicos não alterados.'}
out=base/'validation'/'admin_install.json'
tmp=out.with_suffix('.tmp');tmp.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode());os.replace(tmp,out)
print(json.dumps(report,ensure_ascii=False))
