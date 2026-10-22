from pathlib import Path
import sys,json,subprocess,hashlib
sys.path.insert(0,r"C:\IALD\Central de Patentes\work\memoria_missao_20261016")
import activate as a
out=Path(__file__).resolve().parent
a.ROOT=out
v=a.call('mission_cli.py',{'operation':'project','reference':str(a.REF),'max_chars':48000},'GLOBAL_BUILD_BEFORE')
h=list(v['projection']['flow']['handles'])
start=a.OUT/'orbital_rotation/attempts/20261016T120556_913253Z/START_RECEIPT.json'
r=json.loads(start.read_bytes())
h.append({'id':'build-20261016T120556_913253Z','name':'PhysicalCanonicalNetCompleteR1','no_repeat':True,'pid_at_start':r['pid'],'receipt':str(start),'status':'running','type':'lean_build','unit':'F1.FECHO_20261015'})
e={'operation':'transition','reference':str(a.REF),'expected_revision':v['receipt']['revision'],'event_id':'R5-global-build-start-20261016','actor':a.ACTOR,'changes':{'records':[{'id':'R5-global-build-start-20261016','kind':'fact','statute':'REAL','text':'Iniciada composição aditiva dos quatro candidatos locais. Reusa covariâncias e igualdade da cunha existentes; corrige namespace e redução de coordenadas, sem hipótese nova. Resultado ainda pendente.','sources':[a.source(start),a.source(a.OUT/'orbital_rotation/PhysicalCanonicalNetCompleteR1_SOURCE.json')]}],'flow':{'phase':'R5_global_net_build','next_action':'Recolher esta única compilação; integrar localidade e cunha não trivial se passar. Revisão independente R2/R9 delegada ao agente mission_memory_review com referência exata.','handles':h}}}
r=a.call('session_memory.py',e,'GLOBAL_BUILD_START')
print(json.dumps({'ok':True,'revision':r.get('receipt',{}).get('revision',r.get('revision')),'build':str(start)},ensure_ascii=False))
