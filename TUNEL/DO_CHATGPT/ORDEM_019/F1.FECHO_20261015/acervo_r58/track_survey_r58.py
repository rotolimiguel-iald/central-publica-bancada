"""Track the authorized corpus readers, preserving every existing handle."""
import copy
import survey_r58 as s

state=s.cli('session_memory.py',{'operation':'get','reference':str(s.REF)},'HANDLES_GET_START')
handles=copy.deepcopy(state['p']['handles'])
source=s.pin(s.ROOT/'OPERADOR_LEVANTAMENTO_VERBATIM.txt')
receipt={k:source[k] for k in ('path','sha256')}
for suffix,agent in [('rede','/root/maxwell_covariance_review'),('dispositivos','/root/miguel_r56_review'),('gravidade','/root/mission_memory_review')]:
    identity='r58-survey-'+suffix
    assert not any(h['id']==identity for h in handles)
    handles.append({'id':identity,'kind':'agent','task_id':'R58_SURVEY_'+suffix.upper(),'agent':agent,
        'status':'running','no_repeat':True,'start_receipt':receipt})
r=s.cli('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
    'expected_revision':state['revision'],'event_id':'r58-corpus-reader-handles-start',
    'changes':{'flow':{'handles':handles}}},'HANDLES_START')
print(r['revision'])
