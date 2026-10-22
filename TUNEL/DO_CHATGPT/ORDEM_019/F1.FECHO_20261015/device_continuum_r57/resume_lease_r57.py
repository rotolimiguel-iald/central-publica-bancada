"""Explicit recovery of the expired own R5 lease; no science/other task mutation."""
import json
from mission_r57 import ROOT, REFERENCE, ACTOR, project, call, check, save, pin

p, old_projection = project()
t=next(t for t in p['projection']['active'] if t['id']=='R5')
assert t['lease']['owner']==ACTOR['id'] and t['status']=='working'
recovery=ROOT.parent/'continuity_r57/RECOVERY_PENDING_REVIEW_R57.json'
released, release_receipt=call({
    'operation':'release','reference':str(REFERENCE),'actor':ACTOR,'task_id':'R5',
    'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
    'event_id':'r57-r5-expired-own-lease-explicit-recovery-20261017',
    'reason':'Retomada expressamente autorizada da mesma R57 apos restauracao da cota. Lease propria expirada; TowerR2 e PacketR1 terminais recuperadas sem repeticao. Criterio R5 integral preservado.',
    'sources':[pin(recovery)]},'resume_release')
p, pr=project()
claimed, claim_receipt=call({
    'operation':'claim','reference':str(REFERENCE),'actor':ACTOR,'task_id':'R5',
    'lease_seconds':14400,'expected_revision':p['receipt']['revision'],
    'projection_sha256':p['projection_sha256'],
    'event_id':'r57-r5-renew-own-lease-20261017'},'resume_claim')
p, pr, c, cr=check()
t=next(t for t in p['projection']['active'] if t['id']=='R5')
receipt={'reference':pin(REFERENCE),'actor':ACTOR,'task':t,'revision':p['receipt']['revision'],
    'old_projection':pin(old_projection),'recovery':pin(recovery),'release':pin(release_receipt),
    'claim':pin(claim_receipt),'projection':pin(pr),'preflight':pin(cr)}
save(ROOT/'RESUME_LEASE_R57_R1.json',receipt)
print(json.dumps({'revision':p['receipt']['revision'],'lease':t['lease'],'preflight':str(cr)},ensure_ascii=False))
