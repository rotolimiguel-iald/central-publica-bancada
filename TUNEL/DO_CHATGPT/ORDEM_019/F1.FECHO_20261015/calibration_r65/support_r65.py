"""Immutable receipts and exact mission synchronization for Physical calibration R65."""
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

