"""Metadata-only installer. No device code, ZIP extraction or science execution.
Default is read-only check. Apply requires an independently supplied ROOT decision.
CAS is preflight + immediate recheck, not a filesystem-wide atomic transaction.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import uuid

BASE = Path(__file__).resolve().parent
CENTRAL = Path(r"C:\IALD\Central de Patentes")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_pin(path, pin):
    data = path.read_bytes()
    if len(data) != pin['bytes'] or digest(data) != pin['sha256']:
        raise ValueError('PIN_MISMATCH: ' + str(path))
    return data

def exclusive(path, data):
    with path.open('xb') as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    if path.read_bytes() != data:
        raise ValueError('WRITE_READBACK: ' + str(path))

def atomic_replace(path, data, expected):
    temp = path.with_name(path.name + '.tmp_metadata_' + uuid.uuid4().hex)
    exclusive(temp, data)
    if digest(path.read_bytes()) != expected:
        raise ValueError('CAS_CHANGED: ' + str(path))
    os.replace(temp, path)
    if path.read_bytes() != data:
        raise ValueError('REPLACE_READBACK: ' + str(path))

def resolve_entry(entry):
    target = Path(entry['target']).resolve()
    final = Path(entry['final']['path']).resolve()
    stage = (BASE / entry['stage']).resolve()
    source = (BASE / entry['baseline']).resolve()
    if not target.is_relative_to((CENTRAL/'patents').resolve()):
        raise ValueError('TARGET_OUTSIDE_PATENTS')
    if target.parent != final.parent or not target.name.endswith('_FINAL.manifest.json'):
        raise ValueError('TARGET_ROLE')
    if target.name != final.name.removesuffix('.py') + '.manifest.json':
        raise ValueError('FINAL_MANIFEST_PAIR')
    if not stage.is_relative_to(BASE) or not source.is_relative_to(BASE):
        raise ValueError('STAGE_ESCAPE')
    return target, final, stage, source

def inspect(plan):
    if plan['action'] != 'CORRECT_16_FINAL_METADATA_ONLY' or len(plan['entries']) != 16:
        raise ValueError('PLAN_SCOPE')
    seen=set(); rows=[]
    for entry in plan['entries']:
        target, final, stage, source = resolve_entry(entry)
        if target in seen: raise ValueError('DUPLICATE_TARGET')
        seen.add(target)
        raw = read_pin(source, entry['before'])
        desired = read_pin(stage, entry['after'])
        payload = read_pin(final, entry['final'])
        before = json.loads(raw); after = json.loads(desired)
        expected = dict(before, final_bytes=len(payload), final_sha256=digest(payload))
        if after != expected: raise ValueError('EXTRA_METADATA_CHANGE')
        live = target.read_bytes(); h = digest(live)
        if h == entry['before']['sha256']: state='BEFORE'
        elif h == entry['after']['sha256']: state='ALREADY_CORRECTED'
        else: raise ValueError('LIVE_DRIFT: '+str(target))
        rows.append((entry,target,final,raw,desired,state))
    for pin in plan['read_only_guards']:
        read_pin(Path(pin['path']),pin)
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--decision')
    parser.add_argument('--decision-sha256')
    args=parser.parse_args()
    plan_bytes=(BASE/'PLAN.json').read_bytes(); plan=json.loads(plan_bytes)
    read_pin(Path(__file__).resolve(),plan['installer'])
    rows=inspect(plan)
    if not args.apply:
        print(json.dumps({'status':'READ_ONLY_CHECK','counts':{s:sum(r[5]==s for r in rows) for s in ['BEFORE','ALREADY_CORRECTED']}}))
        return 0
    if not args.decision or not args.decision_sha256:
        raise ValueError('EXTERNAL_DECISION_REQUIRED')
    decision_bytes=Path(args.decision).read_bytes()
    if digest(decision_bytes)!=args.decision_sha256: raise ValueError('DECISION_PIN')
    decision=json.loads(decision_bytes)
    expected={'approved':True,'action':plan['action'],'stage_id':plan['stage_id'],'plan_sha256':digest(plan_bytes)}
    if any(decision.get(k)!=v for k,v in expected.items()) or type(decision.get('approved')) is not bool:
        raise ValueError('DECISION_SCOPE')
    # Exclusive lock refuses concurrent installations; failures retain it for inspection.
    lock=BASE/'APPLY_LOCK.json'
    exclusive(lock,json.dumps({'decision_sha256':digest(decision_bytes),'plan_sha256':digest(plan_bytes)}).encode())
    receipt={'status':'IN_PROGRESS','plan_sha256':digest(plan_bytes),'decision_sha256':digest(decision_bytes),'items':[]}
    try:
        # Back up every original before any mutation, alongside the target, exact bytes.
        for entry,target,final,raw,desired,state in rows:
            backup=target.with_name(target.name+'.bak_v389_metadata_'+plan['stage_id'])
            if backup.exists():
                if backup.read_bytes()!=raw: raise ValueError('BACKUP_DRIFT')
            elif state=='BEFORE': exclusive(backup,raw)
            else: raise ValueError('ALREADY_CORRECTED_WITHOUT_ORIGINAL_BACKUP')
        rows=inspect(plan)
        for entry,target,final,raw,desired,state in rows:
            read_pin(final,entry['final'])
            if state=='BEFORE': atomic_replace(target,desired,entry['before']['sha256'])
            receipt['items'].append({'target':str(target),'status':'CORRECTED' if state=='BEFORE' else state,'sha256':digest(target.read_bytes())})
        verified=inspect(plan)
        if any(r[5]!='ALREADY_CORRECTED' for r in verified): raise ValueError('FINAL_STATE')
        receipt['status']='ALL_16_METADATA_VERIFIED_FINALS_UNCHANGED'
    except BaseException as exc:
        receipt['status']='PARTIAL_OR_FAILED_NO_AUTOMATIC_RETRY'
        receipt['error']=type(exc).__name__+': '+str(exc)
        exclusive(BASE/('RECEIPT_FAILED_'+uuid.uuid4().hex+'.json'),json.dumps(receipt,ensure_ascii=False,indent=2).encode())
        raise
    exclusive(BASE/('RECEIPT_APPLIED_'+uuid.uuid4().hex+'.json'),json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    lock.unlink()
    print(json.dumps({'status':receipt['status']}))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
