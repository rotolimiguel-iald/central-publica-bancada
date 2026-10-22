"""Same exact mission and read protocol with explicit 125000-character capacity.

The R39 helper and its pinned receipts stay unchanged. Revision 419 required
100030 characters and refused the former 100000 budget without truncation.
This wrapper changes capacity only; it does not omit or rewrite any state.
"""
import json
import sys
from live_mission_r39 import ACTOR, CORE, REFERENCE, ROOT, call, save_new

MAX_CHARS = 125000

def project():
    return call('mission_cli.py', dict(operation='project', reference=str(REFERENCE),
        max_chars=MAX_CHARS), 'R53_PROJECT')

def main():
    operation=sys.argv[1] if len(sys.argv)>1 else 'project'
    if operation not in {'project','check','handoff'}:
        raise ValueError('Only project, check and handoff are supported')
    current,receipt=project()
    p=current['projection']
    result=dict(revision=current['receipt']['revision'],project_receipt=str(receipt),
        settled=[x['id'] for x in p['settled']],
        active=[{k:x[k] for k in ('id','status','ready')} for x in p['active']],
        unresolved_handles=[{k:x.get(k) for k in ('id','status')} for x in p['unresolved_handles']])
    if operation!='project':
        task_id=sys.argv[2]
        task=next(x for x in p['active'] if x['id']==task_id)
        if task['lease'] is None or task['lease']['owner']!=ACTOR['id']:
            raise RuntimeError('No current own lease')
        payload=dict(operation='check',reference=str(REFERENCE),actor=ACTOR,task_id=task_id,
            lease_id=task['lease']['id'],expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256'])
        _,checked=call('mission_cli.py',payload,'R53_CHECK_'+task_id)
        result['preflight_receipt']=str(checked)
        if operation=='handoff':
            payload.update(operation='handoff',max_chars=MAX_CHARS)
            _,handed=call('mission_cli.py',payload,'R53_HANDOFF_'+task_id)
            result['handoff_receipt']=str(handed)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    main()
