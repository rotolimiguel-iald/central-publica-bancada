"""Isolated UI fixture: no real models, no real administrative session."""
from pathlib import Path
import tempfile
from unittest.mock import patch
from flask import Flask
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.web import install

temp=tempfile.TemporaryDirectory()
app=Flask(__name__)
with patch('iald_orchestrator.web.Runtime',return_value=Runtime(temp.name)):
    runtime=install(app,lambda:None)
def fixture_connections():
    return [dict(id=n,label=n,status='ready',billing='local' if n=='local' else 'subscription',
        tier='standard' if n=='local' else 'advanced',context_budget=12000,daily_run_limit=10,
        quota_remaining=None) for n in ['local','codex']]
runtime.connections=fixture_connections
runtime.submit=lambda *args,**kw: (_ for _ in ()).throw(ValueError('Prévia visual: envio desativado.'))
app.run(host='127.0.0.1',port=8873,use_reloader=False,debug=False)
