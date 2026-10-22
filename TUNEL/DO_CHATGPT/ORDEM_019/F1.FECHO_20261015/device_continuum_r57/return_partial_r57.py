"""Return own R5 lease after a partial component delivery, never submit/accept R5."""
import json
from mission_r57 import ROOT, REFERENCE, ACTOR, project, check, call, pin, save

delivery=ROOT/'DELIVERY_R57.json'
d=json.loads(delivery.read_bytes())
assert d['requirement_satisfied'] is False
for start in ROOT.glob('attempts/*/START_RECEIPT.json'):
    assert (start.parent/'RECEIPT.json').is_file(), 'Outstanding build: '+str(start.parent)
p,pr,c,cr=check()
t=next(x for x in p['projection']['active'] if x['id']=='R5')
assert t['criterion']==d['criterion_literal']
_,rr=call({'operation':'release','reference':str(REFERENCE),'actor':ACTOR,'task_id':'R5',
    'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
    'event_id':'r57-r5-partial-component-delivery-own-release-20261017',
    'reason':'Componentes R57 compilados e entregues para revisao independente. R5 integral permanece aberto: mapas fisicos da celula/estados/dinamica e identificacao com a rede nao construidos. Sem submit ou aceite do criterio.',
    'sources':[pin(delivery)]},'return_partial_release')
p,pr=project()
t=next(x for x in p['projection']['active'] if x['id']=='R5')
assert t['status']=='open' and t['lease'] is None and t['criterion']==d['criterion_literal']
result={'author':ACTOR['id'],'reference':pin(REFERENCE),'delivery':pin(delivery),
    'release':pin(rr),'final_projection':pin(pr),'final_revision':p['receipt']['revision'],
    'task':t,'requirement_satisfied':False,'all_own_builds_terminal':True,
    'handles_changed':False,'canonical_memory_changed':False}
save(ROOT/'RETURN_R57.json',result)
print(json.dumps({'return':pin(ROOT/'RETURN_R57.json'),'final_revision':p['receipt']['revision'],
    'R5_status':t['status'],'requirement_satisfied':False},ensure_ascii=False))
