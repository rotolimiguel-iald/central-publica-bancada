"""Track exactly one known sandbox build in the existing mission. No build launch."""
from pathlib import Path
import sys,json,hashlib,subprocess,datetime,os
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent
REF=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
CLI=Path(r'C:\IALD\MEMORIA_IALD\session_memory.py')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def call(payload):
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(CLI)],input=json.dumps(payload,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
 d=json.loads(r.stdout)
 if r.returncode or not d.get('ok'):raise RuntimeError(d)
 return d['result']
def main():
 stamp,task,status=sys.argv[1:4]
 if status not in {'running','completed','failed','terminated'}:raise ValueError(status)
 att=(OUT/'orbital_rotation/attempts'/stamp).resolve()
 if att.parent!=(OUT/'orbital_rotation/attempts').resolve():raise ValueError('Outside attempts')
 receipt=att/('START_RECEIPT.json' if status=='running' else 'RECEIPT.json')
 d=json.loads(receipt.read_bytes())
 if status=='completed' and d['exit_code']!=0:raise ValueError('Build failed')
 if status in {'failed','terminated'} and d['exit_code']==0:raise ValueError('Build succeeded')
 state=call({'operation':'get','reference':str(REF)})
 handles=state['p']['handles'];hid='build-'+stamp
 h=next((h for h in handles if h['id']==hid),None)
 if h and h['status']==status and h.get('receipt' if status!='running' else 'start_receipt')==pin(receipt):
  print(json.dumps({'already_tracked':True,'id':hid,'status':status,'revision':state['revision']}));return
 if h is None:
  h={'id':hid,'kind':'lean_build','task_id':task,'no_repeat':True};handles.append(h)
 if h['task_id']!=task:raise ValueError('Task mismatch')
 h.update(status=status)
 h['start_receipt' if status=='running' else 'receipt']=pin(receipt)
 payload={'operation':'transition','reference':str(REF),'expected_revision':state['revision'],
  'event_id':'track-'+hid+'-'+status,'actor':{'id':'codex-gerente-tgl','kind':'agent'},
  'changes':{'records':[{'id':'track-'+hid+'-'+status,'kind':'fact','statute':'REAL','text':task+' sandbox build '+stamp+' '+status+'. Full requirement remains open.','sources':[{'kind':'artifact','ref':str(receipt),'sha256':pin(receipt)['sha256']}]}],
  'flow':{'handles':handles}}}
 prefix='TRACK_'+stamp+'_'+status+'_'+datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S_%f')
 with (ROOT/(prefix+'_REQUEST.json')).open('x',encoding='utf-8') as f:json.dump(payload,f,ensure_ascii=False,indent=2)
 result=call(payload)
 with (ROOT/(prefix+'_RECEIPT.json')).open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 print(json.dumps({'id':hid,'status':status,'revision':result['revision'],'receipt':prefix+'_RECEIPT.json'}))
if __name__=='__main__':main()
