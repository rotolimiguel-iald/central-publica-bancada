"""Immutable receipts and exact mission synchronization for pair-covariance R59."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
BASE=Path(r'C:\IALD\MEMORIA_IALD')
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR={'id':'codex-gerente-tgl','kind':'agent'}

def new(name,value):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    raw=value if isinstance(value,bytes) else ((value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False))+'\n').encode('utf-8')
    with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return p

def pin(path):
    p=Path(path);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def call(cli,request,label):
    new(label+'_REQUEST.json',request)
    cp=subprocess.run([sys.executable,'-B','-X','utf8',str(BASE/cli)],input=json.dumps(request,ensure_ascii=False),capture_output=True,encoding='utf-8')
    d=json.loads(cp.stdout);new(label+'_RESULT.json',{'exit_code':cp.returncode,'result':d,'stderr':cp.stderr})
    if cp.returncode or not d.get('ok'):raise RuntimeError(label)
    return d['result']

def project(label):
    return call('mission_cli.py',{'operation':'project','reference':str(REF),'max_chars':400000},label)

def preflight(task_id,label):
    m=project(label+'_PROJECT');t=next(t for t in m['projection']['active'] if t['id']==task_id)
    return call('mission_cli.py',{'operation':'check','reference':str(REF),'actor':ACTOR,
        'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],
        'task_id':task_id,'lease_id':t['lease']['id']},label+'_CHECK')

def start():
    source=new('OPERADOR_R59.txt','Prossiga')
    scope=new('SCOPE_R59.json',{'unit':'F1.FECHO_20261015','claim':939,'source':pin(source),
        'prior_delivery':pin(ROOT.parent/'acervo_r58/DELIVERY_CONSOLIDATED_R58.json'),
        'task':'Derive existing pair/quadrature covariance and compare to the full OH finite generator and continuous representations.',
        'hypotheses':'Source squeezing conventions preserved; no r/phi/beta identity invented; finite cutoff is not exact bosonic CCR.',
        'limits':['No observed data or providers','No canonical code/kernel/Bancada edits','No full R4/R5 acceptance from a component','No clocks or frequencies identified by name']})
    m=project('CLAIM_R4_PROJECT')
    call('mission_cli.py',{'operation':'claim','reference':str(REF),'actor':ACTOR,
        'event_id':'r59-parent-r4-after-expired-clock-lease-20261017','expected_revision':m['receipt']['revision'],
        'projection_sha256':m['projection_sha256'],'task_id':'R4','lease_seconds':14400},'CLAIM_R4')
    preflight('R4','R4_START');preflight('R5','R5_START')
    state=call('session_memory.py',{'operation':'get','reference':str(REF)},'START_GET')
    handles=state['p']['handles']
    for suffix,agent in [('squeezing','/root/maxwell_covariance_review'),('oh-correlation','/root/miguel_r56_review')]:
        identity='r59-'+suffix;assert not any(h['id']==identity for h in handles)
        handles.append({'id':identity,'kind':'agent','task_id':'R59_'+suffix,'agent':agent,
                        'status':'running','no_repeat':True,'start_receipt':pin(scope)})
    r=call('session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,
        'expected_revision':state['revision'],'event_id':'r59-pair-covariance-start-20261017',
        'changes':{'records':[{'id':'r59-authorized-next-composition','kind':'decision','statute':'INPUT',
            'sources':[{'kind':'artifact','ref':str(p),'sha256':pin(p)['sha256']} for p in [source,scope]],
            'text':'Operador ordena prosseguir apos levantamentoR58. Calcular covariancia de pares/quadraturas e confrontar geradorOH integral, sem inventar identidade entre modos/campos ou parametros.'}],
            'flow':{'phase':'r59_pair_covariance','next_action':'Derivacao exata e controles de leitura/dinamica, depois revisao independente e registro dos elos que realmente fecharem.','handles':handles}}},'START_TRANSITION')
    print(r['revision'])

if __name__=='__main__':start()
