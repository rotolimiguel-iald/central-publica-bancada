"""Accept one independently reviewed requirement through installed CLI with fresh CAS."""
import json
import subprocess
import sys
from finish_requirement_reviews import OUT, REFERENCE, PYTHON, CLI, ACTOR, read, pin, fresh

def call(request):
    result = subprocess.run([PYTHON, '-B', '-X', 'utf8', CLI],
        input=json.dumps(request, ensure_ascii=False), text=True, encoding='utf-8',
        capture_output=True)
    data = json.loads(result.stdout)
    return {'exit_code': result.returncode, 'response': data, 'stderr': result.stderr}

def main():
    task_id = sys.argv[1]
    assert task_id in {'R2', 'R9'}
    report_path = OUT / (task_id + '_REQUIREMENT_REVIEW.json')
    report = read(report_path)
    assert report['reviewer'] == {'id': ACTOR, 'kind': 'agent'}
    assert report['requirement'] == task_id and report['verdict'].startswith('PASS_')
    assert not (OUT / (task_id + '_ACCEPT_REQUEST.json')).exists(), 'Existing request: reconcile instead of resubmitting'
    verification = report['verification']
    assert pin(verification['path'])['sha256'] == verification['sha256']
    for entry in read(verification['path'])['checked_pins']:
        assert pin(entry['path'])['sha256'] == entry['sha256'], entry['path']
    sync = call({'operation': 'project', 'reference': str(REFERENCE), 'max_chars': 60000})
    assert sync['exit_code'] == 0 and sync['response']['ok']
    state = sync['response']['result']
    projection = state['projection']
    assert projection['context_id'] == report['context_id']
    assert pin(REFERENCE)['sha256'] == report['mission_reference']['sha256']
    tasks = {t['id']: t for t in projection['active'] + projection['settled']}
    task = tasks[task_id]
    assert task['status'] == 'review_pending' and task['submitted_by'] != ACTOR
    assert task['criterion'] == report['criterion'] and task['evidence'] == report['evidence']
    assert not projection['hold']
    assert all(tasks[d]['status'] == 'satisfied' for d in task['depends_on'])
    fresh(OUT / (task_id + '_PRE_ACCEPT_PROJECT.json'), sync)
    note = ('Aceite independente do contrato quadrático e consumidor no escopo M2/âncora fixa; rito integral final permanece R3.'
            if task_id == 'R2' else
            'Aceite independente da classificação de alcance: H3 universal é antecedente explícito; não foi derivado apenas do estado. Realização conjunta e demais requisitos permanecem próprios.')
    request = {'operation': 'accept', 'reference': str(REFERENCE), 'task_id': task_id,
               'actor': {'id': ACTOR, 'kind': 'agent'},
               'event_id': task_id + '-independent-memory-review-20261016-v1',
               'expected_revision': state['receipt']['revision'],
               'projection_sha256': state['projection_sha256'],
               'review_evidence': [{k: v for k, v in pin(report_path).items() if k in {'path', 'sha256'}}],
               'note': note + ' Não fecha quadro, não altera gate nem confirma física.'}
    fresh(OUT / (task_id + '_ACCEPT_REQUEST.json'), request)
    result = call(request)
    fresh(OUT / (task_id + '_ACCEPT_RECEIPT.json'), result)
    assert result['exit_code'] == 0 and result['response']['ok'], result
    post = call({'operation': 'project', 'reference': str(REFERENCE), 'max_chars': 60000})
    fresh(OUT / (task_id + '_POST_ACCEPT_PROJECT.json'), post)
    assert post['exit_code'] == 0 and post['response']['ok']
    after = post['response']['result']['projection']
    accepted = next(t for t in after['settled'] if t['id'] == task_id)
    assert accepted['status'] == 'satisfied' and accepted['reviewed_by'] == ACTOR
    assert accepted['review_evidence'] == request['review_evidence']
    assert not after['tetelestai']
    print(json.dumps({'task_id': task_id, 'accepted': True,
        'expected_revision': request['expected_revision'],
        'receipt': result['response']['result']['receipt'],
        'verified_revision': after['revision'], 'tetelestai': after['tetelestai'],
        'review': pin(report_path), 'receipt_file': pin(OUT / (task_id + '_ACCEPT_RECEIPT.json'))}, ensure_ascii=False))

if __name__ == '__main__':
    main()
