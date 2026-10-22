"""Track one sandbox build by flow delta, without duplicating mechanical facts."""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import sys
import live_mission_r39 as live

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent

def pin(path):
    return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def update_handles(handles,stamp,task,status,receipt_pin):
    if status not in {'running','completed','failed','terminated'}:
        raise ValueError('Unknown build status')
    result=copy.deepcopy(handles)
    hid='build-'+stamp
    matches=[h for h in result if h['id']==hid]
    if len(matches)>1:
        raise ValueError('Ambiguous duplicate handle')
    h=matches[0] if matches else None
    if h is not None:
        prior=h.get('status')
        if prior not in {'running','completed','failed','terminated'}:
            raise ValueError('Uncertain or foreign status requires explicit reconciliation')
        if 'phase' in h and h['phase']!=prior:
            raise ValueError('Conflicting phase/status requires explicit reconciliation')
    if h is None:
        h=dict(id=hid,kind='lean_build',task_id=task,no_repeat=True)
        result.append(h)
    if h.get('task_id')!=task or h.get('kind')!='lean_build':
        raise ValueError('Task or kind mismatch')
    if h.get('status') in {'completed','failed','terminated'} and h['status']!=status:
        raise ValueError('Terminal build cannot be reopened or rewritten')
    field='start_receipt' if status=='running' else 'receipt'
    if field in h and h[field]!=receipt_pin:
        raise ValueError('Pinned receipt changed; preserve evidence and reconcile explicitly')
    if 'phase' in h:
        h['phase']=status
    h['status']=status
    h[field]=copy.deepcopy(receipt_pin)
    return result

def main():
    stamp,task,status=sys.argv[1:4]
    attempts=(OUT/'orbital_rotation/attempts').resolve()
    attempt=(attempts/stamp).resolve()
    if attempt.parent!=attempts:
        raise ValueError('Outside sandbox attempts')
    path=attempt/('START_RECEIPT.json' if status=='running' else 'RECEIPT.json')
    raw=path.read_bytes()
    receipt=json.loads(raw)
    receipt_pin={'path':str(path),'sha256':hashlib.sha256(raw).hexdigest()}
    if status!='running':
        if type(receipt.get('exit_code')) is not int:
            raise ValueError('Terminal exit code required')
        if (status=='completed')!=(receipt['exit_code']==0):
            raise ValueError('Status disagrees with terminal receipt')
    state,_=live.call('session_memory.py',dict(operation='get',reference=str(live.REFERENCE)),
        'TRACK_R46_GET')
    handles=update_handles(state['p']['handles'],stamp,task,status,receipt_pin)
    if handles==state['p']['handles']:
        print(json.dumps(dict(already_tracked=True,id='build-'+stamp,status=status,
            revision=state['revision'])))
        return
    result,stored=live.call('session_memory.py',dict(operation='transition',
        reference=str(live.REFERENCE),actor=live.ACTOR,expected_revision=state['revision'],
        event_id='track-flow-build-'+stamp+'-'+status,
        changes=dict(flow=dict(handles=handles))),'TRACK_R46_TRANSITION')
    print(json.dumps(dict(id='build-'+stamp,status=status,revision=result['revision'],
        receipt=str(stored),new_fact_records=0)))

if __name__=='__main__':main()
