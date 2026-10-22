"""Track an existing R57 execution without repeating it or adding scientific facts."""
import argparse
import copy
import json
from pathlib import Path
import support_r57 as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('identity')
    parser.add_argument('task')
    parser.add_argument('kind')
    parser.add_argument('status', choices=['running', 'completed', 'failed', 'terminated'])
    parser.add_argument('receipt', type=Path)
    args = parser.parse_args()
    item = s.pin(args.receipt)
    item.pop('bytes')
    state, _ = s.call('session_memory.py', {'operation': 'get', 'reference': str(s.REFERENCE)}, 'TRACK_GET')
    handles = copy.deepcopy(state['p']['handles'])
    matches = [h for h in handles if h['id'] == args.identity]
    if len(matches) > 1:
        raise ValueError('duplicate execution identity')
    if matches:
        handle = matches[0]
        if handle['status'] in ['completed', 'failed', 'terminated'] and handle['status'] != args.status:
            raise ValueError('terminal execution cannot be reopened')
        if handle['task_id'] != args.task or handle['kind'] != args.kind:
            raise ValueError('execution identity mismatch')
    else:
        handle = dict(id=args.identity, task_id=args.task, kind=args.kind, no_repeat=True)
        handles.append(handle)
    field = 'start_receipt' if args.status == 'running' else 'receipt'
    if field in handle and handle[field] != item:
        raise ValueError('receipt mismatch')
    handle.update(status=args.status, **{field: item})
    if handles == state['p']['handles']:
        print(json.dumps({'unchanged': True, 'revision': state['revision']}))
        return
    result, receipt = s.call('session_memory.py', {
        'operation': 'transition', 'reference': str(s.REFERENCE), 'actor': s.ACTOR,
        'expected_revision': state['revision'],
        'event_id': 'r57-track-' + args.identity + '-' + args.status,
        'changes': {'flow': {'handles': handles}},
    }, 'TRACK')
    print(json.dumps({'revision': result['revision'], 'receipt': str(receipt)}))


if __name__ == '__main__':
    main()
