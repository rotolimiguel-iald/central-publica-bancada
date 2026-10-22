from pathlib import Path
import sys,json
sys.path.insert(0,r"C:\IALD\Central de Patentes\work\memoria_missao_20261016")
import activate as a
a.ROOT=Path(__file__).resolve().parent
v=a.call('mission_cli.py',{'operation':'project','reference':str(a.REF),'max_chars':48000},'R6_BEFORE')
r=a.call('mission_cli.py',{'operation':'claim','reference':str(a.REF),'actor':a.ACTOR,'task_id':'R6','expected_revision':v['receipt']['revision'],'projection_sha256':v['projection_sha256'],'event_id':'R6-physical-fock-assembly-20261016','lease_seconds':14400},'R6_CLAIM')
v=a.call('mission_cli.py',{'operation':'project','reference':str(a.REF),'max_chars':48000},'R6_CURRENT')
t=next(x for x in v['projection']['active'] if x['id']=='R6')
r=a.call('mission_cli.py',{'operation':'check','reference':str(a.REF),'actor':a.ACTOR,'task_id':'R6','lease_id':t['lease']['id'],'expected_revision':v['receipt']['revision'],'projection_sha256':v['projection_sha256']},'R6_PREFLIGHT')
print(json.dumps({'ready':r['ready'],'lease_id':t['lease']['id'],'revision':v['receipt']['revision']}))
