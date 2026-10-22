"""Append reviewed R64 readout results under the existing eight-surface claim."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys
import support_r64 as s

def pin(p):
    return s.pin(p)

def prepare():
    a=s.ROOT/'MEMORY_APPEND_R64.txt'
    extra=a.read_bytes()
    prior=json.loads((s.ROOT.parent/'physical_receiver_r63/MEMORY_PLAN_R63.json').read_text(encoding='utf8'))
    rows=[]
    for x in prior['surfaces']:
        p=Path(x['path']);raw=p.read_bytes()
        assert b'IALD_R64_TEMPORAL_OUTPUT_20261017' not in raw
        rows.append({'path':str(p),'before':pin(p),'before_bytes':len(raw),'append':pin(a),'after_sha256':hashlib.sha256(raw+extra).hexdigest()})
    print(s.new('MEMORY_PLAN_R64.json',{'claim':952,'marker':'IALD_R64_TEMPORAL_OUTPUT_20261017','surfaces':rows,'applier':pin(__file__),'report':pin(s.ROOT/'RELATORIO_R64.txt')}))

def apply():
    plan_path=s.ROOT/'MEMORY_PLAN_R64.json';review_path=s.ROOT/'MEMORY_REVIEW_R64.json'
    plan=json.loads(plan_path.read_text(encoding='utf-8'));review=json.loads(review_path.read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!=s.ACTOR['id']
    assert review['plan']==pin(plan_path) and review['applier']==pin(__file__)
    assert plan['report']==pin(s.ROOT/'RELATORIO_R64.txt')
    m=s.call('mission_cli.py',{'operation':'project','reference':str(s.REF),'max_chars':400000},'MEMORY_PROJECT')
    t=next(t for t in m['projection']['active'] if t['id']=='R4')
    s.call('mission_cli.py',{'operation':'check','reference':str(s.REF),'actor':s.ACTOR,
        'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],
        'task_id':'R4','lease_id':t['lease']['id']},'MEMORY_PREFLIGHT')
    assert not (s.ROOT/'MEMORY_APPLIED_R64.json').exists()
    originals=[]
    for row in plan['surfaces']:
        p=Path(row['path']);raw=p.read_bytes();extra=Path(row['append']['path']).read_bytes()
        assert pin(p)==row['before'] and pin(row['append']['path'])==row['append']
        assert len(raw)==row['before_bytes'] and hashlib.sha256(raw+extra).hexdigest()==row['after_sha256']
        originals.append((p,raw,extra,row))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    s.new('MEMORY_INTENT_R64.json',{'plan':pin(plan_path),'review':pin(review_path),'claim':952})
    backups=[]
    for p,raw,extra,row in originals:
        b=p.with_name(p.name+'.bak_'+stamp)
        with b.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert b.read_bytes()==raw;backups.append(b)
    results=[]
    for i,((p,raw,extra,row),b) in enumerate(zip(originals,backups)):
        assert p.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        result={'before':row['before'],'after':pin(p),'backup':pin(b),'append':row['append'],
                'prefix_preserved':True,'growth_bytes':len(extra)}
        s.new(f'memory_surfaces/SURFACE_{i:02d}_R64.json',result);results.append(result)
    print(s.new('MEMORY_APPLIED_R64.json',{'status':'APPLIED_VERIFIED','author':s.ACTOR['id'],
             'plan':pin(plan_path),'review':pin(review_path),'surfaces':results}))

if __name__=='__main__':
    {'prepare':prepare,'apply':apply}[sys.argv[1]]()


