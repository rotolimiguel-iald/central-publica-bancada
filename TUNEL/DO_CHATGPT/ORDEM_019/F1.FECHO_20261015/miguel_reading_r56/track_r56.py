"""Record running/terminal local handles using the same mission and full current handle list."""
from support_r56 import *

mode=sys.argv[1]
starts=sorted((ROOT/'builds').glob('*/START.json'))
start=starts[-1];end=start.parent/'RESULT.json'
handle_id='r56-build-'+start.parent.name
snap,_=call('session_memory.py',{'operation':'get','reference':str(REFERENCE)},'TRACK_GET')
handles=snap['p'].get('handles',[])
by_id={h['id']:h for h in handles}
h=by_id.get(handle_id,{'id':handle_id,'kind':'lean_build','task_id':TASK,'no_repeat':True})
h['start_receipt']={k:v for k,v in pin(start).items() if k in {'path','sha256'}}
if mode=='terminal':
 result=json.loads(end.read_text(encoding='utf-8'))
 h['status']='completed' if result['exit_code']==0 else 'failed'
 h['receipt']={k:v for k,v in pin(end).items() if k in {'path','sha256'}}
else:h['status']='running'
by_id[handle_id]=h
review_id='r56-independent-review'
rh=by_id.get(review_id,{'id':review_id,'kind':'agent','agent':'/root/miguel_r56_review','task_id':TASK,'no_repeat':True})
rp=ROOT/'REVIEW_R56.json'
rh['status']='completed' if rp.exists() else 'running'
if rp.exists():rh['receipt']={k:v for k,v in pin(rp).items() if k in {'path','sha256'}}
by_id[review_id]=rh
call('session_memory.py',dict(operation='transition',reference=str(REFERENCE),actor=ACTOR,
 expected_revision=snap['revision'],event_id='r56-handles-'+mode+'-'+start.parent.name,
 changes={'flow':{'handles':list(by_id.values())}}),'TRACK_'+mode.upper())
print(json.dumps({'build':h['status'],'review':rh['status']},ensure_ascii=False))
