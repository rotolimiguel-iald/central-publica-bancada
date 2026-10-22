"""Independent synthetic probes: no listening port, real Motor or observed sources."""
import sys,importlib.util,io,json,tempfile,hashlib,types
from pathlib import Path
from unittest.mock import patch,Mock
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'candidate'))
from bancada.canonical import CanonicalRegistry,CanonicalError
spec=importlib.util.spec_from_file_location('review_candidate_server',ROOT/'candidate'/'um_bancada.py')
server=importlib.util.module_from_spec(spec);spec.loader.exec_module(server)
assert server.B is None,'import started engine'
out={'source_pins':[],'probes':{}}
for p in (ROOT/'candidate'/'bancada'/'canonical.py',ROOT/'candidate'/'um_bancada.py'):
 raw=p.read_bytes();out['source_pins'].append({'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
b=object.__new__(server.Bancada);b.pronta=False
b.ev=types.SimpleNamespace(tarefas={});b.gw=types.SimpleNamespace(tarefas={},estado={'estado':'carregando'});b.lago_res=types.SimpleNamespace(estado={'estado':'carregando'})
out['probes']['idle_while_loading']=b.atividades()
b.ev.tarefas={'a':{'estado':'pronta'},'b':{'estado':'falhou'}}
out['probes']['terminal_states']=b.atividades()
b.ev.tarefas={'a':{'estado':'rodando'}}
out['probes']['async_running']=b.atividades()

def handler(body=None):
 h=object.__new__(server.H);h.headers={'Host':'127.0.0.1:18777'};h.wfile=io.BytesIO();h.rfile=io.BytesIO(body or b'')
 h._request_receipt=None;h.send_response=Mock();h.send_header=Mock();h.end_headers=Mock()
 return h
with tempfile.TemporaryDirectory(dir=ROOT/'tests_motor') as td:
 root=Path(td);ui=root/'ui';ui.mkdir();neighbor=root/'ui_neighbor';neighbor.mkdir();(neighbor/'probe.txt').write_bytes(b'SYNTHETIC_NEIGHBOR_BYTES')
 h=handler()
 with patch.object(server,'UI',str(ui)):
  h._arquivo('../ui_neighbor/probe.txt')
 out['probes']['ui_prefix_escape']={'status':h.send_response.call_args.args[0],'body':h.wfile.getvalue().decode()}
body=json.dumps({'theta':{},'curvas':'false','opcoes':[]}).encode();h=handler(body);h.headers['Content-Length']=str(len(body));h.path='/api/avaliar'
fake=types.SimpleNamespace(pronta=True,ev=Mock());fake.ev.avaliar.return_value={'synthetic':True}
with patch.object(server,'B',fake),patch.object(server,'require_current',return_value={'canonical_manifest_sha256':'synthetic'}):h.do_POST()
out['probes']['http_coerces_invalid_types']={'status':h.send_response.call_args.args[0],'forwarded_args':list(fake.ev.avaliar.call_args.args)}
h=handler();h.headers['Content-Length']='not-an-integer';h.path='/api/avaliar'
try:h.do_POST();uncaught=None
except Exception as e:uncaught=type(e).__name__+': '+str(e)
out['probes']['invalid_content_length']={'uncaught':uncaught,'response_sent':h.send_response.called}

with tempfile.TemporaryDirectory(dir=ROOT/'tests_motor') as td:
 root=Path(td)
 def pin(name,raw):
  p=root/name;p.write_bytes(raw);return {'path':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
 prog=pin('um.py',b"UM_VERSION = 'synthetic-v1'\nALPHA_FINE_CODATA_2018 = 0.007\n")
 seal=pin('seal.json',json.dumps({'um_version':'synthetic-v1','sha256':{'um.py':prog['sha256']}}).encode())
 code=pin('engine.py',b'INSTRUMENT_VERSION=1\n');source=pin('source.txt',b'synthetic-source')
 man={'schema':1,'deployment_id':'synthetic','canonical':{'version':'synthetic-v1','script':prog,'seal':seal},'code':[code],'sources':[source]}
 mp=root/'canonical_contracts.json';mp.write_text(json.dumps(man));reg=CanonicalRegistry(root)
 out['probes']['registry_valid']=reg.check('synthetic')['ok']
 (root/'engine.py').write_bytes(b'INSTRUMENT_VERSION=2\n')
 try:reg.check('changed-code');accepted=True
 except CanonicalError:accepted=False
 out['probes']['changed_code_accepted']=accepted
 (root/'engine.py').write_bytes(b'INSTRUMENT_VERSION=1\n')
 mp.write_text(json.dumps(dict(man,deployment_id='changed')))
 try:reg.check('changed-manifest');accepted=True
 except CanonicalError:accepted=False
 out['probes']['changed_manifest_check_accepted']=accepted
 try:r=reg.source_bytes(root/'source.txt',b'synthetic-source');accepted=True
 except CanonicalError:accepted=False
 out['probes']['source_bytes_after_manifest_change_accepted']=accepted
 mp.write_text(json.dumps(dict(man,code=[])));reg2=CanonicalRegistry(root)
 out['probes']['empty_code_manifest_accepted']=reg2.check('empty-code')['ok']

path=ROOT/'tests_motor'/'REVIEW_SERVER_CANONICAL_PROBES.json'
with path.open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(out,ensure_ascii=False,indent=2));print('SHA256',hashlib.sha256(path.read_bytes()).hexdigest())
