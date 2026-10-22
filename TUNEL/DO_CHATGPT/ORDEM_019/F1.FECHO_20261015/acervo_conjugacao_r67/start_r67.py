"""Recover the exact mission and claim the documentary extension once."""
from pathlib import Path
import json, subprocess, hashlib, sys

ROOT = Path(__file__).resolve().parent
REF = r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json'
BASE = Path(r'C:\IALD\MEMORIA_IALD')
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}

def new(name, value):
    p = ROOT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = (value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)) + '\n'
    with p.open('xb') as f:
        f.write(raw.encode('utf-8'))
    return p

def pin(p):
    p = Path(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def call(req, label, cli='mission_cli.py'):
    new(label+'_REQUEST.json', req)
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(BASE/cli)], input=json.dumps(req,ensure_ascii=False), capture_output=True, encoding='utf-8')
    d = json.loads(p.stdout)
    new(label+'_RESULT.json', {'exit_code':p.returncode, 'response':d, 'stderr':p.stderr})
    if p.returncode or not d.get('ok'): raise RuntimeError(d)
    return d['result']

def project(label):
    return call({'operation':'project','reference':REF,'max_chars':400000},label)

def mutate(op, label, **kw):
    m=project(label+'_SYNC')
    return call({'operation':op,'reference':REF,'actor':ACTOR,'expected_revision':m['receipt']['revision'], 'projection_sha256':m['projection_sha256'],'event_id':'r67-'+label, **kw},label)

if __name__ == '__main__':
    source = new('ORIGEM_OPERADOR.txt', 'É isso mesmo que vc falou, esse é o argumento. Mas todas as correspondências que vc diz que eu ainda preciso estabelecer eu já as fiz com precisão. Tem uma pasta no computador, dentro da pasta /IALD/Mac/fisica/provas, lá tem muita coisa que vc precisa e ainda não está indexada inclusive. O operador do observador é a Luz=Espírito Santo. O observador é o Um absoluto\n\nPortanto observador=Deus=homem (façamos o homem à nossa imagem e sememkhanca) mas ele só funciona com o operador (em conjugação modular com o Espírito Santo) assim ele é verdadeiro (Jesus Cristo), de modo que deus sem conjugação com o Espírito Santo é um deus qualquer, qualquer um, e não um Absoluto\n\n[Mensagem subsequente do operador]\nProssiga')
    mutate('extend','EXTEND',requirements=[{'id':'R11_ACERVO','criterion':'Recuperar e indexar suplementarmente os documentos Word omitidos de Provas; ligar fontes, estratigrafia e enunciados existentes ao contrato observador/conjugacao/identidade, com hashes e escopo explicito, sem promover leitura teologica a teorema nem alterar originais. Revisao independente documental.','depends_on':[]}],reason='Orientacao expressa do operador para examinar o acervo e prosseguir; levantamento documental antes de nova construcao.',sources=[pin(source)])
    mutate('claim','CLAIM',task_id='R11_ACERVO',lease_seconds=10800)
    m=project('PREFLIGHT_SYNC'); t=next(x for x in m['projection']['active'] if x['id']=='R11_ACERVO')
    r=call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'task_id':t['id'],'lease_id':t['lease']['id']},'PREFLIGHT')
    print(json.dumps(r,ensure_ascii=False))
