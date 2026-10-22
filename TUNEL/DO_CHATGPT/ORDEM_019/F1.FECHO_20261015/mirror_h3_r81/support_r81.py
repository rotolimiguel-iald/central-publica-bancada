"""Additive custody and mission synchronization for the recovery/H3 analysis."""
from pathlib import Path
import json, subprocess, hashlib, sys
ROOT=Path(__file__).resolve().parent
REF=r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json'
ACTOR={'id':'codex-gerente-tgl','kind':'agent'}
TASK='R13_RECOVERY_H3_SCOPE'
def new(name,value):
    p=ROOT/name
    raw=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)
    with p.open('xb') as f:f.write((raw+'\n').encode('utf-8'))
    return p
def pin(p):
    p=Path(p).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def call(req,label,cli='mission_cli.py'):
    new(label+'_REQUEST.json',req)
    r=subprocess.run([sys.executable,'-B','-X','utf8',str(Path(r'C:\IALD\MEMORIA_IALD')/cli)],input=json.dumps(req,ensure_ascii=False),capture_output=True,text=True,encoding='utf-8')
    d=json.loads(r.stdout);new(label+'_RESULT.json',{'exit_code':r.returncode,'response':d,'stderr':r.stderr})
    if r.returncode or not d.get('ok'):raise RuntimeError(d)
    return d['result']
def project(label):return call({'operation':'project','reference':REF,'max_chars':650000},label)
def mutate(op,label,**kw):
    p=project(label+'_SYNC')
    return call({'operation':op,'reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'event_id':'r81-'+label,**kw},label)
def check(label):
    p=project(label+'_SYNC');t=next(x for x in p['projection']['active'] if x['id']==TASK)
    return call({'operation':'check','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':t['lease']['id']},label)
if __name__=='__main__':
    mutate('extend','EXTEND',requirements=[{'id':TASK,'criterion':'Analisar o mecanismo de recuperacao indicado pelo operador e sua suficiencia para H3, com fontes existentes, alcance matematico explicito e revisao independente. Entrega de escopo nao equivale a derivacao universal H3.','depends_on':[]}],reason='Nova prioridade humana19out e esclarecimento Mirror; analise local autorizada, sem reconstruir rotas materiais adiadas.',sources=[pin(ROOT/'ORIGEM.txt')])
    mutate('claim','CLAIM',task_id=TASK,lease_seconds=7200)
    print(json.dumps(check('PREFLIGHT'),ensure_ascii=False))
