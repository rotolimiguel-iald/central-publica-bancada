"""Exact scientific mission, own actor, immutable local receipts."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
REFERENCE = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
ACTOR = {'kind':'agent', 'id':'codex-device-continuum-r57'}
CORE = Path(r'C:\IALD\MEMORIA_IALD')

def pin(path):
    return {'path':str(path), 'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}

def save(path, value):
    path = Path(path)
    raw = (json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    temp = path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with temp.open('xb') as out:
        out.write(raw);out.flush();os.fsync(out.fileno())
    assert temp.read_bytes()==raw
    os.rename(temp,path)

def call(payload,label,cli='mission_cli.py'):
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    stem=ROOT/(stamp+'_'+label)
    save(stem.with_suffix('.request.json'),payload)
    cp=subprocess.run([sys.executable,'-B','-X','utf8',str(CORE/cli)],
        input=json.dumps(payload,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
    result=json.loads(cp.stdout)
    receipt=stem.with_suffix('.receipt.json');save(receipt,result)
    if cp.returncode or not result.get('ok'):
        raise RuntimeError(str(receipt)+': '+str(result.get('error'))+' '+str(result.get('message')))
    return result['result'],receipt

def project():
    return call({'operation':'project','reference':str(REFERENCE),'max_chars':400000},'project')

def check():
    p,pr=project();t=next(t for t in p['projection']['active'] if t['id']=='R5')
    assert t['lease']['owner']==ACTOR['id']
    c,cr=call({'operation':'check','reference':str(REFERENCE),'actor':ACTOR,'task_id':'R5',
        'lease_id':t['lease']['id'],'expected_revision':p['receipt']['revision'],
        'projection_sha256':p['projection_sha256']},'preflight')
    return p,pr,c,cr

if __name__=='__main__':
    if sys.argv[1]=='claim':
        p,pr=project();t=next(t for t in p['projection']['active'] if t['id']=='R5')
        if t['lease'] is None or t['lease']['owner']!=ACTOR['id']:
            _,claim=call({'operation':'claim','reference':str(REFERENCE),'actor':ACTOR,
                'task_id':'R5','lease_seconds':14400,'expected_revision':p['receipt']['revision'],
                'projection_sha256':p['projection_sha256'],
                'event_id':'r57-device-continuum-own-claim'},'claim')
        else:
            claim=None
        p,pr,c,cr=check();t=next(t for t in p['projection']['active'] if t['id']=='R5')
        handoff={'reference':pin(REFERENCE),'actor':ACTOR,'task':t,'revision':p['receipt']['revision'],
            'projection':pin(pr),'preflight':pin(cr),'claim':pin(claim) if claim else None}
        save(ROOT/'CLAIM_PREFLIGHT_R1.json',handoff)
        print(json.dumps(handoff,ensure_ascii=False))
    else:
        p,pr=project();print(json.dumps({'revision':p['receipt']['revision'],
            'receipt':str(pr),'R5':[t for t in p['projection']['active'] if t['id']=='R5']},ensure_ascii=False))
