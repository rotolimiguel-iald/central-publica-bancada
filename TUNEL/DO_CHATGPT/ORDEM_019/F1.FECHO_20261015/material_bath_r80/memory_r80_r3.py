"""Append the reviewed OH mirror contract with byte backups and concurrency checks."""
from pathlib import Path
import datetime as dt, hashlib, json, os, sys
from support_r80 import ROOT, new, pin

def prepare():
    prior=json.loads((ROOT.parent/'device_profiles_r72/MEMORY_PLAN_R72.json').read_text(encoding='utf-8'))
    extra=ROOT/'MEMORY_APPEND_R80_R3.txt'; b=extra.read_bytes(); rows=[]
    for r in prior['surfaces']:
        p=Path(r['before']['path']); before=p.read_bytes()
        assert b'IALD_R80_MATERIAL_BATH' not in before
        rows.append({'before':pin(p),'bytes':len(before),'after_sha256':hashlib.sha256(before+b).hexdigest()})
    new('MEMORY_PLAN_R80_R3.json',{'claim':985,'append':pin(extra),'applier':pin(__file__),'helper':pin(ROOT/'support_r80.py'),'concurrency':'optimistic before/after hash checks; no cross-process atomic lock','surfaces':rows})

def apply():
    plan=json.loads((ROOT/'MEMORY_PLAN_R80_R3.json').read_text(encoding='utf-8'))
    assert pin(__file__)==plan['applier']
    assert pin(ROOT/'support_r80.py')==plan['helper']
    assert pin(plan['append']['path'])==plan['append']
    # Review must explicitly include this plan and the exact append/applier bytes.
    review=json.loads((ROOT/'MEMORY_REVIEW_R80_R3.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer']!='codex-gerente-tgl'
    for p in [ROOT/'MEMORY_PLAN_R80_R3.json',ROOT/'MEMORY_APPEND_R80_R3.txt',Path(__file__),ROOT/'support_r80.py']:
        assert pin(p) in review['evidence']
    extra=Path(plan['append']['path']).read_bytes()
    for r in plan['surfaces']:assert pin(r['before']['path'])==r['before']
    stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f');done=[]
    for r in plan['surfaces']:
        p=Path(r['before']['path']);raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==r['before']['sha256']
        backup=p.with_name(p.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert backup.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_r80_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.stat().st_size==len(raw)+len(extra)
        assert pin(p)==r['before']
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        done.append({'before':r['before'],'backup':pin(backup),'after':pin(p),'pure_append':True})
        new('MEMORY_SURFACE_R80_'+str(len(done))+'.json',done[-1])
    print(new('MEMORY_APPLIED_R80.json',{'claim':985,'surfaces':done}))

if __name__=='__main__':
    {'prepare':prepare,'apply':apply}[sys.argv[1]]()







