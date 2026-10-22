import json, subprocess, sys
import support_r66 as s
m=s.project('START_PROJECT_R66')
s.call('session_memory.py',{'operation':'project','reference':str(s.REF),'max_chars':400000},'SESSION_PROJECT_R66')
base={'reference':str(s.REF),'actor':s.ACTOR}
r4=next(t for t in m['projection']['active'] if t['id']=='R4')
assert r4['lease']['owner']==s.ACTOR['id']
s.call('mission_cli.py',{**base,'operation':'invalidate','expected_revision':m['receipt']['revision'],'state_sha256':m['receipt']['state_sha256'],'event_id':'r66-recover-expired-r4','task_id':'R4','reason':'Continuidade explicita do operador R66; revogar lease vencido da propria sessao, conservar criterios, provas e resultados; nao repetir execucoes. R3/R10 ja pendentes.','sources':[s.pin(s.ROOT/'OPERATOR_REQUEST_R66.txt')]},'RECOVER_R4_R66')
for task in ['R4','R5']:
 m=s.project('CLAIM_'+task+'_PROJECT_R66')
 s.call('mission_cli.py',{**base,'operation':'claim','expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],'event_id':'r66-claim-'+task.lower(),'task_id':task,'lease_seconds':21600},'CLAIM_'+task+'_R66')
 s.preflight(task,'START_'+task+'_R66')
state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'START_GET_R66')
handles=state['p']['handles']
for name,agent in [('sources','maxwell_covariance_review'),('construction','miguel_r56_review'),('review','mission_memory_review')]:
 handles.append({'id':'r66-'+name,'agent':'/root/'+agent,'status':'running' if name!='review' else 'awaiting_delivery'})
s.call('session_memory.py',{**base,'operation':'transition','expected_revision':state['revision'],'event_id':'r66-reservoir-bridge-start','changes':{'flow':{'phase':'r66_reservoir_drive_network_construction','next_action':'Construir reservatorio comum para J=A+B, bombeamento e gerador integral; reaproveitar R64/R65 e avancar componente dinamico da rede, com revisao independente.','handles':handles}}},'START_TRANSITION_R66')
for label,cmd in [('NOS_VIVO_R66',[r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F1.FECHO_20261015']),('MAP_R66',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','reservatorio']),('BOARD_R66',[r'C:\IALD\PROGRAMA_IALD\iald.py','ver','F1.FECHO_20261015'])]:
 cp=subprocess.run([sys.executable,'-B','-X','utf8']+cmd,capture_output=True,encoding='utf-8');s.new(label+'.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
m=s.project('HANDOFF_PROJECT_R66');s.new('HANDOFF_R66.json',{'reference':str(s.REF),'receipt':m['receipt'],'projection_sha256':m['projection_sha256'],'tasks':[t for t in m['projection']['active'] if t['id'] in ['R4','R5']],'claim':956,'nos_vivo':s.pin(s.ROOT/'NOS_VIVO_R66.json'),'source':s.pin(s.ROOT/'OPERATOR_REQUEST_R66.txt'),'allowed_output':str(s.ROOT),'scope':'Sandbox only. No providers, original modifications, kernel, Bancada, observed data or gate. Components only; no acceptance of entire R4/R5.'})
print(json.dumps({'revision':m['receipt']['revision'],'tasks':[(t['id'],t['lease']) for t in m['projection']['active'] if t['id'] in ['R4','R5']]}))
