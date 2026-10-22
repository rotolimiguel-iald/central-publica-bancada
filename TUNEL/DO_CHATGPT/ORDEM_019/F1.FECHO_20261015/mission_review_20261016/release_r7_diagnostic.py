"""Release only the reviewer's R7 lease; no build, accept or process operation."""
import json
from finish_requirement_reviews import OUT, REFERENCE, ACTOR, read, pin, fresh
from accept_reviewed_requirement import call

def main():
    report = OUT / 'R7_CANCELLATION_AND_REPLACEMENT_RECOMMENDATION_R1.json'
    recorded = read(report)
    assert recorded['actor'] == ACTOR
    assert pin(REFERENCE)['sha256'] == recorded['mission_reference']['sha256']
    assert not (OUT / 'R7_COST_RELEASE_REQUEST.json').exists(), 'Reconcile existing request before retry'
    sync = call({'operation':'project','reference':str(REFERENCE),'max_chars':60000})
    assert sync['exit_code'] == 0 and sync['response']['ok'], sync
    state = sync['response']['result']
    p = state['projection']
    assert p['context_id'] == '34290aaa-3dcc-51d5-b224-f3eeec93509b'
    t = next(t for t in p['active'] if t['id'] == 'R7')
    assert t['status'] == 'working' and t['lease']['owner'] == ACTOR
    assert t['lease']['id'] == recorded['R7_lease']['id']
    fresh(OUT / 'R7_COST_PRE_RELEASE_PROJECT.json', sync)
    check = {'operation':'check','reference':str(REFERENCE),'task_id':'R7',
             'actor':{'id':ACTOR,'kind':'agent'},'expected_revision':p['revision'],
             'projection_sha256':state['projection_sha256'],'lease_id':t['lease']['id']}
    checked = call(check)
    fresh(OUT / 'R7_COST_PRE_RELEASE_PREFLIGHT.json', checked)
    assert checked['exit_code'] == 0 and checked['response']['ok'], checked
    request = {'operation':'release','reference':str(REFERENCE),'task_id':'R7',
               'actor':{'id':ACTOR,'kind':'agent'},
               'event_id':'R7-compile-cost-diagnostic-20261016-release-v1',
               'expected_revision':p['revision'],'projection_sha256':state['projection_sha256'],
               'reason':'Diagnóstico concluído; root assume intervenção e eventual build. R7 integral permanece aberto, sem aceite.',
               'sources':[{k:v for k,v in pin(report).items() if k in {'path','sha256'}}]}
    fresh(OUT / 'R7_COST_RELEASE_REQUEST.json', request)
    result = call(request)
    fresh(OUT / 'R7_COST_RELEASE_RECEIPT.json', result)
    assert result['exit_code'] == 0 and result['response']['ok'], result
    post = call({'operation':'project','reference':str(REFERENCE),'max_chars':60000})
    fresh(OUT / 'R7_COST_POST_RELEASE_PROJECT.json', post)
    assert post['exit_code'] == 0 and post['response']['ok'], post
    after = post['response']['result']['projection']
    task = next(t for t in after['active'] if t['id'] == 'R7')
    assert task['status'] == 'open' and task['lease'] is None
    assert task['epoch'] == t['epoch'] + 1
    print(json.dumps({'release':result['response']['result'],'R7':{'status':task['status'],'lease':task['lease'],'epoch':task['epoch']},
                      'verified_revision':after['revision'],'receipt_file':pin(OUT/'R7_COST_RELEASE_RECEIPT.json')},ensure_ascii=False))

if __name__ == '__main__':
    main()
